"""
scripts/download_sample_images.py
----------------------------------
Baixa imagens de exemplo do COCO para testar o detector
nas classes alvo: person, laptop, cell phone.

Uso
---
    python scripts/download_sample_images.py
"""

import sys
import urllib.request
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets"

# Imagens públicas do COCO com as classes alvo
SAMPLE_IMAGES = [
    {
        "url": "http://images.cocodataset.org/val2017/000000397133.jpg",
        "filename": "coco_person_laptop.jpg",
        "desc": "Pessoa com laptop",
    },
    {
        "url": "http://images.cocodataset.org/val2017/000000037777.jpg",
        "filename": "coco_person_phone.jpg",
        "desc": "Pessoa com celular",
    },
    {
        "url": "http://images.cocodataset.org/val2017/000000252219.jpg",
        "filename": "coco_person.jpg",
        "desc": "Pessoa",
    },
    {
        "url": "http://images.cocodataset.org/val2017/000000087038.jpg",
        "filename": "coco_laptop.jpg",
        "desc": "Laptop",
    },
]


def download(url: str, dest: Path, desc: str) -> bool:
    print(f"  ↓ Baixando: {desc} ({dest.name})...")
    try:
        urllib.request.urlretrieve(url, dest)
        size_kb = dest.stat().st_size / 1024
        print(f"  ✓ {dest.name} ({size_kb:.0f} KB)")
        return True
    except Exception as exc:
        print(f"  ✗ Falha: {exc}")
        return False


def main() -> int:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Baixando imagens de exemplo em: {ASSETS_DIR.resolve()}\n")

    success = 0
    for img in SAMPLE_IMAGES:
        dest = ASSETS_DIR / img["filename"]
        if dest.exists():
            print(f"  ✓ {img['filename']} já existe. Pulando.")
            success += 1
            continue
        if download(img["url"], dest, img["desc"]):
            success += 1

    print(f"\n{success}/{len(SAMPLE_IMAGES)} imagens prontas.")
    if success > 0:
        print("\nPróximo passo:")
        print("  python detect.py --image assets/coco_person_laptop.jpg")
    return 0 if success > 0 else 1


if __name__ == "__main__":
    sys.exit(main())