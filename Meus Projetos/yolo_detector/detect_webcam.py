"""
detect_webcam.py
----------------
Detecção de objetos em TEMPO REAL via webcam usando YOLOv8.

Classes detectadas: person | laptop | cell phone

Uso
---
    python detect_webcam.py
    python detect_webcam.py --confidence 0.5 --camera 1
    python detect_webcam.py --all-classes
    python detect_webcam.py --save

Pressione 'q' para sair.
Pressione 's' para salvar o frame atual.
Pressione 'a' para alternar entre classes alvo e todas as classes.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

import cv2

from src import (
    DetectionConfig,
    YOLODetector,
    draw_detections,
    draw_fps,
    save_image,
    setup_logging,
)

OUTPUT_DIR = Path("output")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="detect_webcam",
        description="Detecção de objetos em tempo real com YOLOv8.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--camera", type=int, default=0, help="Índice da webcam.")
    parser.add_argument("--model", "-m", type=str, default="yolov8n.pt")
    parser.add_argument("--confidence", "-c", type=float, default=0.40)
    parser.add_argument("--iou", type=float, default=0.45)
    parser.add_argument("--width", "-w", type=int, default=640)
    parser.add_argument("--all-classes", action="store_true",
                         help="Mostra todas as 80 classes COCO.")
    parser.add_argument("--save", action="store_true",
                         help="Salva o vídeo processado em output/webcam.avi.")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "webcam.log")
    logger = logging.getLogger(__name__)

    logger.info("Carregando YOLOv8...")
    config = DetectionConfig(
        confidence_threshold=args.confidence,
        iou_threshold=args.iou,
        filter_classes=not args.all_classes,
    )
    detector = YOLODetector(model_path=args.model, config=config)

    logger.info("Abrindo webcam (índice %d)...", args.camera)
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        logger.error("Não foi possível abrir a webcam.")
        return 1

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)

    # Configurar gravação de vídeo (opcional)
    video_writer = None
    if args.save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        video_writer = cv2.VideoWriter(
            str(OUTPUT_DIR / "webcam.avi"),
            fourcc, 20.0,
            (args.width, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
        )
        logger.info("Gravando em output/webcam.avi")

    logger.info("━" * 45)
    logger.info("Controles:")
    logger.info("  [q] Sair")
    logger.info("  [s] Salvar frame atual")
    logger.info("  [a] Alternar todas as classes / classes alvo")
    logger.info("━" * 45)

    prev_time = time.time()
    frame_count = 0
    filter_active = not args.all_classes

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                logger.warning("Falha ao capturar frame.")
                break

            # Ajusta filtro de classes dinamicamente
            detector.config.filter_classes = filter_active

            detections = detector.detect(frame)
            annotated = draw_detections(frame, detections)

            # FPS
            now = time.time()
            fps = 1 / (now - prev_time) if now != prev_time else 0
            prev_time = now
            annotated = draw_fps(annotated, fps)

            # Modo ativo no canto inferior
            mode_text = "Alvo: person|laptop|phone" if filter_active else "Todas as classes COCO"
            cv2.putText(
                annotated, mode_text,
                (10, annotated.shape[0] - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
            )

            cv2.imshow("YOLO Detector — YOLOv8 | Pressione Q para sair", annotated)

            if video_writer:
                video_writer.write(annotated)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("s"):
                frame_count += 1
                out = OUTPUT_DIR / f"frame_{frame_count:04d}.jpg"
                save_image(annotated, out)
                logger.info("Frame salvo: %s", out)
            elif key == ord("a"):
                filter_active = not filter_active
                mode = "classes alvo" if filter_active else "todas as classes"
                logger.info("Modo alterado para: %s", mode)

    finally:
        cap.release()
        if video_writer:
            video_writer.release()
        cv2.destroyAllWindows()
        logger.info("Webcam encerrada.")

    return 0


if __name__ == "__main__":
    sys.exit(main())