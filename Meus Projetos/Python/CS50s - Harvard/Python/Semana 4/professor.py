import random

def main():
    level = get_level()
    score = 0
    
    # 10 problemas
    for _ in range(10):
        x, y = generate_integer(level)
        resposta_correta = x + y
        tentativas = 3
        
        while tentativas > 0:
            try:
                resposta_usuario = int(input(f"{x} + {y} = "))
                if resposta_usuario == resposta_correta:
                    score += 1
                    break
                else:
                    print("EEE")
                    tentativas -= 1
            except ValueError:
                print("EEE")
                tentativas -= 1
        
        # Se esgotar as tentativas, exibe a resposta
        if tentativas == 0:
            print(f"{x} + {y} = {resposta_correta}")
            
    print(f"Score: {score}")

def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level in [1, 2, 3]:
                return level
        except ValueError:
            pass

def generate_integer(level):
    # Define os limites baseados no nível (número de dígitos)
    if level == 1:
        lower = 0
        upper = 9
    elif level == 2:
        lower = 10
        upper = 99
    elif level == 3:
        lower = 100
        upper = 999
        
    # Gera dois números aleatórios
    x = random.randint(lower, upper)
    y = random.randint(lower, upper)
    return x, y

if __name__ == "__main__":
    main()