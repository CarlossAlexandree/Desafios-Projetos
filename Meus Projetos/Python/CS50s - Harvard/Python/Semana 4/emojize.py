import emoji

def main():
    # Solicitar a string com código de emoji
    entrada = input("Input: ")
    
    # Imprimir a versão emojizada (Shortcodes)
    print(f"Output: {emoji.emojize(entrada, language='alias')}")

main()