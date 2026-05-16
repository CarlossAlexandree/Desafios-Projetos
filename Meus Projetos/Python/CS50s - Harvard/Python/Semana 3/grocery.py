def main():
    lista_compras = {}
    
    while True:
        try:
            # Solicita o item
            item = input().strip().upper()
            
            # Adiciona ou incrementa a contagem no dicionário
            if item in lista_compras:
                lista_compras[item] += 1
            else:
                lista_compras[item] = 1
                
        # Captura EOFError (Ctrl-D) para encerrar a lista
        except EOFError:
            # Itera sobre as chaves ordenadas alfabeticamente
            for item in sorted(lista_compras.keys()):
                # Imprime contagem e item
                print(f"{lista_compras[item]} {item}")
            break

main()