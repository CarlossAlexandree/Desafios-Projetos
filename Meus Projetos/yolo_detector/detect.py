"""
detect.py
---------
Script principal de detecção de objetos em imagens usando YOLOv8.

Classes detectadas: person | laptop | cell phone

Uso
---
    python detect.py --image assets/foto.jpg
    python detect.py --image assets/foto.jpg --all-classes
    python detect.py --image assets/foto.jpg --confidence 0.5 --output output/resultado.jpg
    python detect.py --batch assets/          (processa todas as imagens de uma pasta)
    python detect.py --image assets/foto.jpg --debug
"""

import argparse
import logging
import sys
from pathlib import Path

from src import (
    DetectionConfig,
    YOLODetector,
    draw_detections,
    list_images,
    load_image,
    resize_image,
    save_image,
    setup_logging,
)

OUTPUT_DIR = Path("output")
MODELS_DIR = Path("models")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="detect",
        description="Detecção de objetos com YOLOv8 — person, laptop, cell phone.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--image", "-i", type=Path,
        help="Imagem de entrada para detecção.",
    )
    group.add_argument(
        "--batch", "-b", type=Path,
        help="Pasta com múltiplas imagens para processar em lote.",
    )
    parser.add_argument(
        "--output", "-o", type=Path,
        default=OUTPUT_DIR / "resultado.jpg",
        help="Caminho para salvar a imagem anotada.",
    )
    parser.add_argument(
        "--model", "-m", type=str,
        default="yolov8n.pt",
        help="Modelo YOLOv8 a usar (yolov8n.pt, yolov8s.pt, yolov8m.pt).",
    )
    parser.add_argument(
        "--confidence", "-c", type=float, default=0.40,
        help="Confiança mínima para aceitar uma detecção (0.0–1.0).",
    )
    parser.add_argument(
        "--iou", type=float, default=0.45,
        help="Threshold IoU para supressão de sobreposições (NMS).",
    )
    parser.add_argument(
        "--width", "-w", type=int, default=640,
        help="Largura de redimensionamento da imagem de entrada.",
    )
    parser.add_argument(
        "--all-classes", action="store_true",
        help="Detecta todas as 80 classes COCO (não só as 3 classes alvo).",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Ativa logs DEBUG.",
    )
    return parser.parse_args(argv)


def process_image(image_path: Path, detector: YOLODetector, args, idx: int = 1) -> dict:
    """Processa uma única imagem e retorna métricas."""
    image = load_image(image_path)
    image = resize_image(image, width=args.width)

    if args.all_classes:
        detections = detector.detect_all_classes(image)
    else:
        detections = detector.detect(image)

    annotated = draw_detections(image, detections)

    # Define o caminho de saída
    if args.batch:
        output_path = OUTPUT_DIR / f"resultado_{idx:03d}_{image_path.name}"
    else:
        output_path = args.output

    saved = save_image(annotated, output_path)

    # Resumo por classe
    counts = {}
    for det in detections:
        counts[det.class_name] = counts.get(det.class_name, 0) + 1

    return {
        "image": image_path.name,
        "total": len(detections),
        "counts": counts,
        "saved": saved,
    }


def main(argv=None) -> int:
    args = parse_args(argv)

    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "detect.log")
    logger = logging.getLogger(__name__)

    logger.info("━" * 55)
    logger.info("YOLO DETECTOR — YOLOv8 + COCO")
    logger.info("  Classes alvo: person | laptop | cell phone")
    logger.info("━" * 55)

    try:
        config = DetectionConfig(
            confidence_threshold=args.confidence,
            iou_threshold=args.iou,
            filter_classes=not args.all_classes,
        )
        detector = YOLODetector(model_path=args.model, config=config)

        # ── Modo batch ────────────────────────────────────────
        if args.batch:
            if not args.batch.exists():
                logger.error("Pasta não encontrada: %s", args.batch)
                return 1

            images = list_images(args.batch)
            if not images:
                logger.error("Nenhuma imagem encontrada em: %s", args.batch)
                return 1

            logger.info("Modo batch: %d imagem(ns) encontrada(s).", len(images))
            total_detections = 0

            for idx, img_path in enumerate(images, 1):
                logger.info("[%d/%d] Processando: %s", idx, len(images), img_path.name)
                result = process_image(img_path, detector, args, idx)
                total_detections += result["total"]
                logger.info(
                    "  → %d objeto(s): %s | Salvo: %s",
                    result["total"], result["counts"], result["saved"].name,
                )

            logger.info("\n✓ Batch concluído: %d objeto(s) em %d imagem(ns).",
                        total_detections, len(images))
            logger.info("Resultados em: %s", OUTPUT_DIR.resolve())

        # ── Modo imagem única ─────────────────────────────────
        else:
            result = process_image(args.image, detector, args)

            logger.info("\n✓ Detecção concluída!")
            logger.info("  Total de objetos: %d", result["total"])
            for cls, cnt in result["counts"].items():
                logger.info("  %-15s: %d", cls, cnt)
            logger.info("  Resultado salvo : %s", result["saved"])
            logger.info("  Visualizar      : start %s", result["saved"])

        return 0

    except FileNotFoundError as exc:
        logger.error("Arquivo não encontrado: %s", exc)
        return 1
    except ValueError as exc:
        logger.error("Erro de valor: %s", exc)
        return 1
    except Exception as exc:
        logger.exception("Erro inesperado: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())