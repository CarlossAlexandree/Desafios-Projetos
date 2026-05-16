# Projeto: Calculadora Modular com Funções

# 1. Defina as funções para as operações matemáticas
def somar(a, b):
    return a + b

def subtrair(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "Erro: Divisão por zero!"
    return a / b

# 2. Defina a função principal 'main' para controlar o programa
def main():
    # Pede os números e a operação ao usuário
    numero1 = float(input("Digite o primeiro número: "))
    numero2 = float(input("Digite o segundo número: "))
    operacao = input("Escolha a operação (+, -, *, /): ")

    # Usa as funções para realizar a operação
    if operacao == '+':
        resultado = somar(numero1, numero2)
    elif operacao == '-':
        resultado = subtrair(numero1, numero2)
    elif operacao == '*':
        resultado = multiplicar(numero1, numero2)
    elif operacao == '/':
        resultado = dividir(numero1, numero2)
    else:
        resultado = "Operação inválida."

    # Imprime o resultado final
    if type(resultado) == float:
        print(f"O resultado é: {resultado:,.2f}")
    else:
        print(resultado)

# 3. Executa a função principal para iniciar o programa
main()