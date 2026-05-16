import os
from PIL import Image, ImageDraw, ImageFont

# Configurações do Card
CARD_SIZE = (600, 400)
BACKGROUND_COLOR = (255, 255, 240)  # Off-white
TEXT_COLOR = (0, 0, 0)             # Preto
FONT_SIZE = 30
# Tenta carregar uma fonte padrão, se falhar usa a básica
try:
    # No Windows, Arial é comum. 
    FONT_PATH = "arial.ttf" 
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except IOError:
    font = ImageFont.load_default()

def create_card_image(text: str, type: str) -> str:
    """
    Gera uma imagem de flashcard com o texto centralizado.
    type: 'frente' ou 'verso' (define o título e cor da borda).
    Retorna o caminho da imagem gerada.
    """
    # Cria imagem base
    img = Image.new('RGB', CARD_SIZE, color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Desenha Borda e Título baseado no tipo
    border_color = (70, 130, 180) if type == 'frente' else (34, 139, 34) # Azul vs Verde
    title_text = "PERGUNTA (FRENTE)" if type == 'frente' else "RESPOSTA (VERSO)"
    
    # Borda simples
    draw.rectangle([(10, 10), (CARD_SIZE[0]-10, CARD_SIZE[1]-10)], outline=border_color, width=5)
    
    # Título (Arial bold se possível, ou apenas texto)
    draw.text((20, 20), title_text, fill=border_color, font=font)

    # Posição central da imagem
    center_x = CARD_SIZE[0] / 2
    center_y = CARD_SIZE[1] / 2
    
    # Desenha o texto centralizado
    draw.multiline_text((center_x, center_y), text, fill=TEXT_COLOR, font=font, anchor="mm", align="center")

    # Salva a imagem temporária
    folder = "temp_cards"
    os.makedirs(folder, exist_ok=True)
    filepath = f"{folder}/{type}_card.png"
    img.save(filepath)
    
    return filepath