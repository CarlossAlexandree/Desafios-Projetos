# Solicitar a string de entrada
entrada = input("Input: ")

# String para armazenar o resultado sem vogais
saida = ""

# Vogais a serem removidas (maiúsculas e minúsculas)
vogais = "AEIOUaeiou"

# Itera sobre cada caractere da entrada
for char in entrada:
    # Se o caractere NÃO for uma vogal, adiciona à saída
    if char not in vogais:
        saida += char

# Imprimir o resultado
print(f"Output: {saida}")