import re
import sys

def main():
    # Solicita o texto
    texto = input("Text: ").strip()
    # Chama a função de contagem e imprime
    print(count(texto))

def count(s):
    # Regex para encontrar a palavra inteira "um" (\b: limite de palavra)
    # re.findall() retorna uma lista de todas as correspondências
    # re.IGNORECASE para ignorar maiúsculas/minúsculas
    padrao = r"\bum\b"
    matches = re.findall(padrao, s, re.IGNORECASE)
    # Retorna o tamanho da lista de correspondências
    return len(matches)

if __name__ == "__main__":
    main()