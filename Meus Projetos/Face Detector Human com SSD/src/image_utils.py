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


def load_image(image_path: Path | str) -> np.ndarray:
    """
    Carrega uma imagem do disco com validações.

    Parâmetros
    ----------
    image_path : Path | str
        Caminho para o arquivo de imagem.

    Retorna
    -------
    np.ndarray
        Imagem BGR carregada.

    Lança
    -----
    FileNotFoundError
        Se o arquivo não existir.
    ValueError
        Se a extensão não for suportada ou a imagem não puder ser lida.
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Extensão '{path.suffix}' não suportada. "
            f"Use: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Não foi possível ler a imagem: {path}")

    logger.info("Imagem carregada: %s (%dx%d)", path.name, image.shape[1], image.shape[0])
    return image


def resize_image(image: np.ndarray, width: int) -> np.ndarray:
    """
    Redimensiona a imagem mantendo a proporção (aspect ratio).

    Parâmetros
    ----------
    image : np.ndarray
        Imagem de entrada.
    width : int
        Largura desejada em pixels.

    Retorna
    -------
    np.ndarray
        Imagem redimensionada.
    """
    h, w = image.shape[:2]
    if w == width:
        return image

    ratio = width / w
    new_height = int(h * ratio)
    resized = cv2.resize(image, (width, new_height), interpolation=cv2.INTER_AREA)
    logger.debug("Imagem redimensionada para %dx%d.", width, new_height)
    return resized


def save_image(image: np.ndarray, output_path: Path | str) -> Path:
    """
    Salva a imagem no disco, criando diretórios intermediários se necessário.

    Parâmetros
    ----------
    image : np.ndarray
        Imagem a ser salva.
    output_path : Path | str
        Caminho de destino.

    Retorna
    -------
    Path
        Caminho absoluto onde a imagem foi salva.

    Lança
    -----
    IOError
        Se a escrita falhar.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(path), image)
    if not success:
        raise IOError(f"Falha ao salvar imagem em: {path}")

    logger.info("Imagem salva em: %s", path.resolve())
    return path.resolve()