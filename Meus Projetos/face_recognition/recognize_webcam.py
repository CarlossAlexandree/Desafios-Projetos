"""
recognize_webcam.py
--------------------
Reconhecimento facial em TEMPO REAL via webcam.

Mesmo pipeline de recognize.py (Rede 1 SSD + Rede 2 TensorFlow),
aplicado a cada frame capturado da câmera.

Uso
---
    python recognize_webcam.py
    python recognize_webcam.py --confidence 0.6 --threshold 0.7
    python recognize_webcam.py --camera 1

Pressione 'q' para sair.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

import cv2

from src import (
    DetectionConfig,
    FaceClassifier,
    FaceDetector,
    draw_recognition,
    get_color_for_name,
    resize_image,
    setup_logging,
)

MODELS_DIR = Path("models")
PROTOTXT   = MODELS_DIR / "deploy.prototxt"
CAFFEMODEL = MODELS_DIR / "res10_300x300_ssd_iter_140000.caffemodel"
OUTPUT_DIR = Path("output")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="recognize_webcam",
        description="Reconhecimento facial em tempo real via webcam.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--camera", type=int, default=0, help="Índice da webcam.")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                         help="Limiar de confiança do detector SSD.")
    parser.add_argument("--threshold", "-t", type=float, default=0.60,
                         help="Limiar de confiança do classificador TF.")
    parser.add_argument("--width", "-w", type=int, default=640,
                         help="Largura de processamento do frame.")
    parser.add_argument("--prototxt", type=Path, default=PROTOTXT)
    parser.add_argument("--caffemodel", type=Path, default=CAFFEMODEL)
    parser.add_argument("--model-dir", type=Path, default=MODELS_DIR)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "webcam.log")
    logger = logging.getLogger(__name__)

    logger.info("Carregando Rede 1 (detector SSD)...")
    config = DetectionConfig(confidence_threshold=args.confidence)
    detector = FaceDetector(args.prototxt, args.caffemodel, config=config)

    logger.info("Carregando Rede 2 (classificador TensorFlow)...")
    classifier = FaceClassifier.from_dir(args.model_dir, threshold=args.threshold)

    logger.info("Abrindo webcam (índice %d)...", args.camera)
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        logger.error("Não foi possível abrir a webcam.")
        return 1

    logger.info("Pressione 'q' para sair.")
    prev_time = time.time()

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                logger.warning("Falha ao capturar frame.")
                break

            frame = resize_image(frame, width=args.width)
            detections = detector.detect(frame)

            for roi in detections:
                face_crop = roi.crop(frame, padding=config.padding)
                if face_crop.size == 0:
                    continue

                name, confidence = classifier.predict(face_crop)
                color = get_color_for_name(name, classifier.class_names)

                draw_recognition(
                    image=frame,
                    start_x=roi.start_x, start_y=roi.start_y,
                    end_x=roi.end_x, end_y=roi.end_y,
                    name=name, confidence=confidence, color=color,
                )

            # FPS no canto
            now = time.time()
            fps = 1 / (now - prev_time) if now != prev_time else 0
            prev_time = now
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Reconhecimento Facial - SSD + MobileNetV2", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Webcam encerrada.")

    return 0


if __name__ == "__main__":
    sys.exit(main())