import os
from PIL import Image

def load_image(path: str) -> Image.Image:
    """Carrega uma imagem a partir de um caminho local."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagem não encontrada no caminho: {path}")
    return Image.open(path)

def convert_and_save_webp(image: Image.Image, output_path: str, quality: int = 80) -> str:
    """Converte e salva a imagem no formato moderno WebP otimizado."""
    if image.mode in ('RGBA', 'LA'):
        # Mantém transparência se houver
        image.save(output_path, 'WEBP', quality=quality)
    else:
        # Garante conversão segura para RGB se for JPEG/BMP
        image.convert('RGB').save(output_path, 'WEBP', quality=quality)
    return output_path