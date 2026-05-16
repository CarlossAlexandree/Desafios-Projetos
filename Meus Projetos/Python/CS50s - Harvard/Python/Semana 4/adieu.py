import inflect

def main():
    p = inflect.engine()
    nomes = []
    
    while True:
        try:
            # Solicita o nome
            nome = input("Name: ").strip()
            nomes.append(nome)
        # Captura Ctrl-D
        except EOFError:
            print("\nAdieu, adieu, to " + p.join(nomes))
            break

main()
