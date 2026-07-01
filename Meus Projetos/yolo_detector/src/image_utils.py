"""
image_utils.py
--------------
Utilitários para carregamento, redimensionamento e salvamento de imagens.
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def load_image(image_path) -> np.ndarray:
    """Carrega imagem do disco com validações."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Extensão '{path.suffix}' não suportada.")
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Não foi possível ler: {path}")
    logger.info("Imagem carregada: %s (%dx%d)", path.name, image.shape[1], image.shape[0])
    return image


def resize_image(image: np.ndarray, width: int) -> np.ndarray:
    """Redimensiona mantendo aspect ratio."""
    h, w = image.shape[:2]
    if w == width:
        return image
    ratio = width / w
    return cv2.resize(image, (width, int(h * ratio)), interpolation=cv2.INTER_AREA)


def save_image(image: np.ndarray, output_path) -> Path:
    """Salva imagem no disco, criando diretórios se necessário."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise IOError(f"Falha ao salvar imagem em: {path}")
    logger.info("Resultado salvo em: %s", path.resolve())
    return path.resolve()


def list_images(folder) -> list:
    """Lista todas as imagens suportadas em uma pasta."""
    folder = Path(folder)
    images = []
    for ext in SUPPORTED_EXTENSIONS:
        images.extend(folder.glob(f"*{ext}"))
        images.extend(folder.glob(f"*{ext.upper()}"))
    return sorted(images)