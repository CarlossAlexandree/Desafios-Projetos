def main():
    menu = {
        "Baja Taco": 4.00,
        "Burrito": 7.50,
        "Bowl": 8.50,
        "Nachos": 11.00,
        "Quesadilla": 8.50,
        "Super Burrito": 8.50,
        "Super Quesadilla": 9.50,
        "Taco": 3.00,
        "Tortilla Salad": 8.00
    }
    
    total = 0.0
    
    while True:
        try:
            # Solicita o item ao usuário
            item = input("Item: ").title()
            
            # Se o item estiver no menu, adiciona ao total
            if item in menu:
                total += menu[item]
                # Imprime o total acumulado formatado
                print(f"Total: ${total:.2f}")
                
        # Captura KeyError se o item não estiver no menu (embora 'in' resolva)
        except KeyError:
            pass
        # Captura EOFError (Ctrl-D) para encerrar o pedido
        except EOFError:
            print("\nOrder complete.")
            break

main()