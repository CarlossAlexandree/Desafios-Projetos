"""
scripts/capture_faces.py
--------------------------
Utilitário para CRIAR o dataset de treino capturando fotos via webcam.

Detecta o rosto com a Rede 1 (SSD) em tempo real e salva recortes
automaticamente na pasta da pessoa, facilitando a montagem do dataset.

Uso
---
    python scripts/capture_faces.py --name joao
    python scripts/capture_faces.py --name maria --count 50

Pressione 'espaço' para capturar manualmente, 'a' para modo automático,
'q' para sair.
"""

import argparse
import sys
import time
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from src import DetectionConfig, FaceDetector, resize_image  # noqa: E402

MODELS_DIR = Path(__file__).parent.parent / "models"
DATASET_DIR = Path(__file__).parent.parent / "dataset" / "train"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="capture_faces",
        description="Captura fotos de rosto via webcam para montar o dataset.",
    )
    parser.add_argument("--name", "-n", required=True,
                         help="Nome da pessoa (será o nome da subpasta/classe).")
    parser.add_argument("--count", "-c", type=int, default=30,
                         help="Quantidade de fotos a capturar.")
    parser.add_argument("--camera", type=int, default=0, help="Índice da webcam.")
    parser.add_argument("--interval", type=float, default=0.5,
                         help="Segundos entre capturas no modo automático.")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    person_dir = DATASET_DIR / args.name.strip().lower().replace(" ", "_")
    person_dir.mkdir(parents=True, exist_ok=True)
    existing = len(list(person_dir.glob("*.jpg")))

    print(f"Salvando fotos em: {person_dir.resolve()}")
    print(f"Fotos já existentes: {existing}")
    print(f"Meta: {args.count} fotos novas")
    print("\nControles:")
    print("  [espaço]  capturar manualmente")
    print("  [a]       alternar modo automático")
    print("  [q]       sair\n")

    config = DetectionConfig(confidence_threshold=0.6)
    detector = FaceDetector(
        MODELS_DIR / "deploy.prototxt",
        MODELS_DIR / "res10_300x300_ssd_iter_140000.caffemodel",
        config=config,
    )

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("ERRO: não foi possível abrir a webcam.")
        return 1

    captured = 0
    auto_mode = False
    last_capture = 0.0

    try:
        while captured < args.count:
            ok, frame = cap.read()
            if not ok:
                break

            frame = resize_image(frame, width=640)
            detections = detector.detect(frame)

            display = frame.copy()
            for roi in detections:
                cv2.rectangle(display, (roi.start_x, roi.start_y),
                              (roi.end_x, roi.end_y), (0, 255, 0), 2)

            cv2.putText(
                display,
                f"Capturadas: {captured}/{args.count}  |  Auto: {'ON' if auto_mode else 'OFF'}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2,
            )
            cv2.imshow("Captura de Dataset - " + args.name, display)

            key = cv2.waitKey(1) & 0xFF
            should_capture = False

            if key == ord("q"):
                break
            elif key == ord("a"):
                auto_mode = not auto_mode
            elif key == 32:  # espaço
                should_capture = True
            elif auto_mode and (time.time() - last_capture) > args.interval:
                should_capture = True

            if should_capture and detections:
                roi = max(detections, key=lambda r: r.confidence)
                face = roi.crop(frame, padding=20)
                if face.size > 0:
                    filename = person_dir / f"{args.name}_{existing + captured + 1:03d}.jpg"
                    cv2.imwrite(str(filename), face)
                    captured += 1
                    last_capture = time.time()
                    print(f"  ✓ Capturada {captured}/{args.count}: {filename.name}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"\nConcluído! {captured} fotos salvas em {person_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())