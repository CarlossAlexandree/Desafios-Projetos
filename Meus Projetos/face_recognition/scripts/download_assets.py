#!/usr/bin/env python3
"""
scripts/download_assets.py
---------------------------
Baixa os arquivos do detector SSD ResNet-10 pré-treinado (Rede 1),
diretamente do repositório oficial do OpenCV.

A Rede 2 (classificador) é treinada localmente com train.py
e não requer download — ela usa o MobileNetV2 pré-treinado do
próprio Keras (baixado automaticamente na primeira execução).

Uso
---
    python scripts/download_assets.py
"""

import sys
import urllib.request
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent / "models"

ASSETS = [
    {
        "url": (
            "https://raw.githubusercontent.com/opencv/opencv/master/"
            "samples/dnn/face_detector/deploy.prototxt"
        ),
        "filename": "deploy.prototxt",
    },
    {
        "url": (
            "https://github.com/opencv/opencv_3rdparty/raw/"
            "dnn_samples_face_detector_20170830/"
            "res10_300x300_ssd_iter_140000.caffemodel"
        ),
        "filename": "res10_300x300_ssd_iter_140000.caffemodel",
    },
]


def download(url: str, dest: Path) -> None:
    print(f"  ↓ Baixando {dest.name}...")
    urllib.request.urlretrieve(url, dest)
    size_mb = dest.stat().st_size / (1024 ** 2)
    print(f"  ✓ {dest.name} ({size_mb:.1f} MB)")


def main() -> int:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Diretório de modelos: {MODELS_DIR.resolve()}\n")

    for asset in ASSETS:
        dest = MODELS_DIR / asset["filename"]
        if dest.exists():
            print(f"  ✓ {asset['filename']} já existe. Pulando.")
            continue
        try:
            download(asset["url"], dest)
        except Exception as exc:
            print(f"  ✗ Falha ao baixar {asset['filename']}: {exc}", file=sys.stderr)
            return 1

    print("\nRede 1 (detector SSD) pronta para uso!")
    print("Próximo passo: organize o dataset/train/ e execute python train.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())