# 1. Pedir dois números.
# O input() sempre retorna uma string, então precisamos convertê-la para um número.
# Usamos float() para permitir números com casas decimais.
numero1 = float(input("Digite o primeiro número: "))
numero2 = float(input("Digite o segundo número: "))

# 2. Escolher uma operação.
operacao = input("Escolha a operação (+, -, *, /): ")

# 3. Estrutura de decisão para realizar a operação e armazenar o resultado.
# Adicionar uma verificação para evitar a divisão por zero.

if operacao == '+':
  resultado = numero1 + numero2
elif operacao == '-':
  resultado = numero1 - numero2
elif operacao == '*':
  resultado = numero1 * numero2
elif operacao == '/':
  if numero2 != 0:
    resultado = numero1 / numero2
  else:
    resultado = "Erro: Divisão por zero não é permitida."
else:
  resultado = "Operação inválida."

# 4. Resultado usando uma f-string para uma saída clara.
print(f"O resultado é: {resultado}")