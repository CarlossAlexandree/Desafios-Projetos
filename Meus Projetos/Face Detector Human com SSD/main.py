"""
main.py
-------
Ponto de entrada principal da aplicação de detecção facial SSD.

Uso
---
    python main.py --image photo.jpg
    python main.py --image photo.jpg --output output/resultado.jpg --confidence 0.6
    python main.py --image photo.jpg --width 600 --debug
"""

import argparse
import logging
import sys
from pathlib import Path

from src import (
    DetectionConfig,
    FaceDetector,
    load_image,
    resize_image,
    save_image,
    setup_logging,
)

# ------------------------------------------------------------------
# Constantes de caminho
# ------------------------------------------------------------------
MODELS_DIR = Path("models")
PROTOTXT = MODELS_DIR / "deploy.prototxt"
CAFFEMODEL = MODELS_DIR / "res10_300x300_ssd_iter_140000.caffemodel"
OUTPUT_DIR = Path("output")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Define e analisa os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        prog="face_detector",
        description="Detecção facial em imagens usando SSD + ResNet-10.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--image", "-i",
        type=Path,
        required=True,
        help="Caminho para a imagem de entrada.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=OUTPUT_DIR / "resultado.jpg",
        help="Caminho para salvar a imagem com as detecções.",
    )
    parser.add_argument(
        "--confidence", "-c",
        type=float,
        default=0.5,
        help="Limiar mínimo de confiança para considerar uma detecção (0.0–1.0).",
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=400,
        help="Largura de redimensionamento da imagem de entrada.",
    )
    parser.add_argument(
        "--prototxt",
        type=Path,
        default=PROTOTXT,
        help="Caminho para o arquivo deploy.prototxt.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=CAFFEMODEL,
        help="Caminho para o arquivo .caffemodel.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logs no nível DEBUG.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Fluxo principal da aplicação.

    Retorna
    -------
    int
        Código de saída: 0 para sucesso, 1 para erro.
    """
    args = parse_args(argv)

    # Configura logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "app.log")
    logger = logging.getLogger(__name__)

    try:
        # 1. Carregar e redimensionar imagem
        image = load_image(args.image)
        image = resize_image(image, width=args.width)

        # 2. Configurar e instanciar o detector
        config = DetectionConfig(confidence_threshold=args.confidence)
        detector = FaceDetector(
            prototxt_path=args.prototxt,
            model_path=args.model,
            config=config,
        )

        # 3. Detectar rostos
        detections = detector.detect(image)

        if not detections:
            logger.warning("Nenhuma face detectada acima do limiar de confiança.")

        # 4. Anotar e salvar resultado
        annotated = detector.draw(image, detections)
        saved_path = save_image(annotated, args.output)

        logger.info("Processo concluído. Resultado salvo em: %s", saved_path)
        return 0

    except FileNotFoundError as exc:
        logger.error("Arquivo não encontrado: %s", exc)
        return 1
    except ValueError as exc:
        logger.error("Erro de valor: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("Erro inesperado: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())