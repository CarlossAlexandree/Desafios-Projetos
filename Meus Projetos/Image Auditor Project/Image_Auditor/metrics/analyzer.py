import numpy as np
from PIL import Image

def has_alpha_channel(image: Image.Image) -> bool:
    """Verifica se a imagem possui canal de transparência (Alpha)."""
    return image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)

def calculate_brightness(image: Image.Image) -> float:
    """Calcula o brilho médio da imagem (escala de 0 a 255) para detectar fotos muito escuras."""
    grayscale = image.convert('L')
    np_img = np.array(grayscale)
    return float(np.mean(np_img))