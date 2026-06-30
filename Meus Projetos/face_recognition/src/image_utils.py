"""
image_utils.py
--------------
Utilitários para I/O de imagens e anotação visual dos resultados.
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Paleta de cores BGR (uma por identidade, ciclada automaticamente)
COLOR_PALETTE = [
    (0, 120, 255),   # azul
    (0, 200, 50),    # verde
    (200, 50, 0),    # vermelho
    (255, 180, 0),   # laranja
    (180, 0, 255),   # roxo
    (0, 200, 200),   # ciano
    (255, 80, 180),  # rosa
    (80, 255, 80),   # verde claro
]


def load_image(image_path) -> np.ndarray:
    """
    Carrega imagem do disco com validações.

    Lança FileNotFoundError ou ValueError em caso de erro.
    """
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


def get_color_for_name(name: str, name_list: list) -> tuple:
    """Retorna uma cor BGR consistente para cada nome."""
    if name == "Desconhecido":
        return (80, 80, 80)  # cinza para desconhecido
    try:
        idx = name_list.index(name)
    except ValueError:
        idx = hash(name) % len(COLOR_PALETTE)
    return COLOR_PALETTE[idx % len(COLOR_PALETTE)]


def draw_recognition(
    image: np.ndarray,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    name: str,
    confidence: float,
    color: tuple = (0, 120, 255),
    thickness: int = 2,
    font_scale: float = 0.6,
) -> np.ndarray:
    """
    Desenha bounding box + label de reconhecimento na imagem.

    Label exibe:  "Nome (confiança%)"   ex: "Carlos (97.3%)"
    Fundo colorido atrás do texto para legibilidade.
    """
    label = f"{name} ({confidence * 100:.1f}%)"

    # Bounding box
    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color, thickness)

    # Posição do texto (acima do box, ou abaixo se não couber)
    y_text = start_y - 12 if start_y - 12 > 15 else start_y + 20

    # Fundo do texto
    (text_w, text_h), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
    )
    cv2.rectangle(
        image,
        (start_x, y_text - text_h - baseline - 2),
        (start_x + text_w + 4, y_text + 2),
        color,
        cv2.FILLED,
    )

    # Texto branco sobre fundo colorido
    cv2.putText(
        image, label,
        (start_x + 2, y_text - baseline),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (255, 255, 255),
        thickness,
    )
    return image