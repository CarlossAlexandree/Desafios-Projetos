import sys
import random
from pyfiglet import Figlet

def main():
    figlet = Figlet()
    fontes_disponiveis = figlet.getFonts()
    
    fonte_escolhida = ""
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) == 1:
        # Sem argumentos: escolhe uma fonte aleatória
        fonte_escolhida = random.choice(fontes_disponiveis)
    elif len(sys.argv) == 3 and (sys.argv[1] == "-f" or sys.argv[1] == "--font"):
        # Argumentos específicos de fonte
        fonte_escolhida = sys.argv[2]
        if fonte_escolhida not in fontes_disponiveis:
            sys.exit("Invalid usage")
    else:
        # Uso inválido da linha de comando
        sys.exit("Invalid usage")
        
    try:
        # Tenta definir a fonte
        figlet.setFont(font = fonte_escolhida)
        # Solicita o texto e imprime na fonte FIGlet
        texto = input("Input: ")
        print(figlet.renderText(texto))
    except Exception:
        # Tratamento genérico caso algo dê errado
        sys.exit("Invalid usage")

main()