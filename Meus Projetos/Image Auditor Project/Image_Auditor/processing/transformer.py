from PIL import Image, ImageEnhance

def resize_to_web(image: Image.Image, max_width: int = 1200) -> Image.Image:
    """Redimensiona a imagem proporcionalmente se ela for maior que a largura máxima."""
    if image.width <= max_width:
        return image
    
    proportion = max_width / float(image.width)
    new_height = int(float(image.height) * proportion)
    return image.resize((max_width, new_height), Image.Resampling.LANCZOS)

def boost_contrast(image: Image.Image, factor: float = 1.2) -> Image.Image:
    """Melhora o contraste da imagem para garantir melhor legibilidade na web."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)