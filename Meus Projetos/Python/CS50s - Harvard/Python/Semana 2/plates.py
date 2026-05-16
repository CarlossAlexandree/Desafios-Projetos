def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    # Regra 1: Tamanho entre 2 e 6 caracteres
    if not (2 <= len(s) <= 6):
        return False
    
    # Regra 2: Começar com pelo menos duas letras
    if not s[0:2].isalpha():
        return False
    
    # Regra 3: Números devem vir no final, e o primeiro número não pode ser '0'
    # Regra 4: Não pode haver letras após um número
    found_digit = False
    for char in s:
        if char.isdigit():
            # Se for o primeiro dígito encontrado, não pode ser '0'
            if not found_digit and char == '0':
                return False
            found_digit = True
        elif char.isalpha():
            # Se já for encontrado um dígito e agora encontrado uma letra, é inválido
            if found_digit:
                return False
    
    # Regra 5: Não pode haver pontuação (implícito: apenas letras e números)
    if not s.isalnum():
        return False
        
    return True

main()