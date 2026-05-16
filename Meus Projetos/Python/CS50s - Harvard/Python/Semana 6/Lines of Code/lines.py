import sys

def main():
    # Verifica argumentos da linha de comando
    if len(sys.argv) != 2:
        sys.exit("Usage: python lines.py filename.py")
    
    filename = sys.argv[1]
    
    # Verifica se o arquivo é .py
    if not filename.endswith(".py"):
        sys.exit("Not a Python file")
        
    try:
        linhas_de_codigo = 0
        # Abre o arquivo em modo leitura
        with open(filename, "r") as file:
            for line in file:
                # Remove espaços em branco
                line_stripped = line.strip()
                # Verifica se a linha não está vazia e não é um comentário
                if line_stripped and not line_stripped.startswith("#"):
                    linhas_de_codigo += 1
        print(linhas_de_codigo)
                
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()