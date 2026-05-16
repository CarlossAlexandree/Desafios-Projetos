import random

def main():
    nivel = get_positive_int("Level: ")
    numero_secreto = random.randint(1, nivel)
    
    while True:
        try:
            chute = int(input("Guess: "))
            
            if chute > 0:
                if chute < numero_secreto:
                    print("Too small!")
                elif chute > numero_secreto:
                    print("Too large!")
                else:
                    print("Just right!")
                    break
        except ValueError:
            pass

def get_positive_int(prompt):
    while True:
        try:
            entrada = int(input(prompt))
            if entrada > 0:
                return entrada
        except ValueError:
            pass

main()