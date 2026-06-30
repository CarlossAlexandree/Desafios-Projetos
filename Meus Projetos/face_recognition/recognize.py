"""
recognize.py
------------
Script principal: DETECÇÃO + RECONHECIMENTO facial em imagens.

Rede 1 (SSD OpenCV)  →  detecta ONDE estão os rostos
Rede 2 (TensorFlow)  →  identifica QUEM é cada rosto

Uso
---
    python recognize.py --image assets/foto.jpg
    python recognize.py --image assets/foto.jpg --output output/resultado.jpg
    python recognize.py --image assets/foto.jpg --confidence 0.6 --threshold 0.7
    python recognize.py --image assets/foto.jpg --width 800 --debug
"""

import argparse
import logging
import sys
from pathlib import Path

from src import (
    DetectionConfig,
    FaceClassifier,
    FaceDetector,
    draw_recognition,
    get_color_for_name,
    load_image,
    resize_image,
    save_image,
    setup_logging,
)

# ── Caminhos padrão ───────────────────────────────────────────
MODELS_DIR   = Path("models")
PROTOTXT     = MODELS_DIR / "deploy.prototxt"
CAFFEMODEL   = MODELS_DIR / "res10_300x300_ssd_iter_140000.caffemodel"
OUTPUT_DIR   = Path("output")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="recognize",
        description="Detecção + Reconhecimento facial (SSD + MobileNetV2).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--image", "-i",
        type=Path, required=True,
        help="Imagem de entrada.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path, default=OUTPUT_DIR / "resultado.jpg",
        help="Onde salvar a imagem anotada.",
    )
    parser.add_argument(
        "--confidence", "-c",
        type=float, default=0.5,
        help="Limiar de confiança do detector SSD (0.0–1.0).",
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float, default=0.60,
        help="Limiar de confiança do classificador TF (0.0–1.0).",
    )
    parser.add_argument(
        "--width", "-w",
        type=int, default=600,
        help="Largura de redimensionamento da imagem.",
    )
    parser.add_argument(
        "--prototxt",
        type=Path, default=PROTOTXT,
        help="Caminho para deploy.prototxt.",
    )
    parser.add_argument(
        "--caffemodel",
        type=Path, default=CAFFEMODEL,
        help="Caminho para o .caffemodel SSD.",
    )
    parser.add_argument(
        "--model-dir",
        type=Path, default=MODELS_DIR,
        help="Pasta com face_recognizer.keras e class_names.json.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logs DEBUG.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "app.log")
    logger = logging.getLogger(__name__)

    logger.info("━" * 60)
    logger.info("SISTEMA DE RECONHECIMENTO FACIAL")
    logger.info("  Rede 1: SSD ResNet-10 (OpenCV DNN) — Detecção")
    logger.info("  Rede 2: MobileNetV2 (TensorFlow)   — Reconhecimento")
    logger.info("━" * 60)

    try:
        # ── 1. Carregar imagem ────────────────────────────────
        image = load_image(args.image)
        image = resize_image(image, width=args.width)
        logger.info("Imagem: %s", args.image)

        # ── 2. Rede 1 — Detector SSD ─────────────────────────
        logger.info("\n[Rede 1] Carregando detector SSD...")
        config = DetectionConfig(confidence_threshold=args.confidence)
        detector = FaceDetector(
            prototxt_path=args.prototxt,
            model_path=args.caffemodel,
            config=config,
        )

        detections = detector.detect(image)
        logger.info("[Rede 1] %d rosto(s) detectado(s).", len(detections))

        if not detections:
            logger.warning("Nenhum rosto detectado acima do limiar de confiança.")
            save_image(image, args.output)
            return 0

        # ── 3. Rede 2 — Classificador TensorFlow ─────────────
        logger.info("\n[Rede 2] Carregando classificador TensorFlow...")
        classifier = FaceClassifier.from_dir(
            model_dir=args.model_dir,
            threshold=args.threshold,
        )

        # ── 4. Reconhecer cada rosto detectado ───────────────
        annotated = image.copy()
        logger.info("\n[Resultado] Reconhecendo identidades:")

        for i, roi in enumerate(detections):
            # Recorta o rosto detectado
            face_crop = roi.crop(image, padding=config.padding)

            if face_crop.size == 0:
                logger.warning("Rosto %d ignorado (recorte vazio).", i + 1)
                continue

            # Classifica o rosto — Rede 2
            name, confidence = classifier.predict(face_crop)

            logger.info(
                "  Rosto %d: %-20s (%.1f%%)",
                i + 1, name, confidence * 100,
            )

            # Cor consistente por identidade
            color = get_color_for_name(name, classifier.class_names)

            # Desenha resultado na imagem
            draw_recognition(
                image=annotated,
                start_x=roi.start_x,
                start_y=roi.start_y,
                end_x=roi.end_x,
                end_y=roi.end_y,
                name=name,
                confidence=confidence,
                color=color,
            )

        # ── 5. Salvar resultado ───────────────────────────────
        saved = save_image(annotated, args.output)
        logger.info("\n✓ Resultado salvo em: %s", saved)
        logger.info("  Para visualizar: start %s", saved)

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