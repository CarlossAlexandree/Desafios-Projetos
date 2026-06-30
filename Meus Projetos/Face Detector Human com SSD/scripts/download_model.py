#!/usr/bin/env python3
"""
scripts/download_model.py
-------------------------
Baixa os arquivos do modelo SSD ResNet-10 pré-treinado do repositório
oficial do OpenCV.

Uso
---
    python scripts/download_model.py
"""

import hashlib
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
        "md5": None,  # arquivo pequeno, verificação opcional
    },
    {
        "url": (
            "https://github.com/opencv/opencv_3rdparty/raw/"
            "dnn_samples_face_detector_20170830/"
            "res10_300x300_ssd_iter_140000.caffemodel"
        ),
        "filename": "res10_300x300_ssd_iter_140000.caffemodel",
        "md5": None,
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
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ Falha ao baixar {asset['filename']}: {exc}", file=sys.stderr)
            return 1

    print("\nModelos prontos para uso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())