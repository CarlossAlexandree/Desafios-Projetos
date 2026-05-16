def main():
    # Preço da Coca-Cola
    preco = 50
    # Total inserido até o momento
    total_inserido = 0
    # Moedas aceitas
    moedas_aceitas = [25, 10, 5]

    # Continuar
    # o loop enquanto o total inserido for menor que o preço
    while total_inserido < preco:
        # Exibir o valor devido
        print(f"Amount Due: {preco - total_inserido}")
        # Solicitar uma moeda
        moeda = int(input("Insert Coin: "))
        
        # Se a moeda for aceita, adicionar ao total
        if moeda in moedas_aceitas:
            total_inserido += moeda

    # Calcular e imprimir o troco
    troco = total_inserido - preco
    print(f"Change Owed: {troco}")

main()