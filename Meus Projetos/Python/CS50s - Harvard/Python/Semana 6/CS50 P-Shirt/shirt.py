import sys
import os
from PIL import Image, ImageOps

def main():
    # Verifica argumentos
    if len(sys.argv) != 3:
        sys.exit("Usage: python shirt.py input_image output_image")
    
    input_image = sys.argv[1]
    output_image = sys.argv[2]
    
    # Lista de extensões válidas
    extensoes_validas = [".jpg", ".jpeg", ".png"]
    
    # Obtém as extensões dos arquivos
    input_ext = os.path.splitext(input_image)[1].lower()
    output_ext = os.path.splitext(output_image)[1].lower()
    
    # Valida extensões de entrada e saída
    if input_ext not in extensoes_validas:
        sys.exit("Invalid input extension")
    if output_ext not in extensoes_validas:
        sys.exit("Invalid output extension")
    if input_ext != output_ext:
        sys.exit("Input and output extensions must be the same")
        
    try:
        # Abre a imagem da camiseta
        shirt = Image.open("shirt.png")
        size = shirt.size
        
        # Abre a imagem de entrada
        with Image.open(input_image) as im:
            # Redimensiona e corta a imagem de entrada para caber na camiseta
            im_resized = ImageOps.fit(im, size)
            
            # Sobrepõe a camiseta na imagem de entrada
            im_resized.paste(shirt, shirt)
            
            # Salva a imagem resultante
            im_resized.save(output_image)
                
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()