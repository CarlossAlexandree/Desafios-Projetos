def main():
    porcentagem = get_fuel_percentage()
    
    # Verifica os limites para exibir E ou F
    if porcentagem <= 1:
        print("E")
    elif porcentagem >= 99:
        print("F")
    else:
        print(f"{porcentagem}%")

def get_fuel_percentage():
    # Loop infinito até obter uma entrada válida
    while True:
        entrada = input("Fraction: ")
        try:
            # Tenta dividir a string em x e y
            x_str, y_str = entrada.split("/")
            x = int(x_str)
            y = int(y_str)
            
            # Verifica se x e y são inteiros, se x <= y e se y != 0
            if x <= y and y != 0:
                # Calcula a porcentagem arredondada
                return round((x / y) * 100)
                
        # Captura erros de valor (não inteiros, formato inválido) ou divisão por zero
        except (ValueError, ZeroDivisionError):
            pass # Apenas ignora e repete o loop

main()