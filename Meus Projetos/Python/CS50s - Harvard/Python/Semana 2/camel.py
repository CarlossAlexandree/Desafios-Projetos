# Solicitar a variável em camelCase
camel = input("camelCase: ")

# Variável para armazenar o resultado em snake_case
snake = ""

# Caractere da string camelCase
for char in camel:
    # Se o caractere for maiúsculo, adicionar '_' e a versão minúscula
    if char.isupper():
        snake += "_" + char.lower()
    # Se não, apenas adicionar o caractere
    else:
        snake += char

# Imprimir o resultado
print(f"snake_case: {snake}")