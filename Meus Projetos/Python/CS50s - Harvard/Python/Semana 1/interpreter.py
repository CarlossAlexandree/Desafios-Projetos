# Solicitar a expressão
expressao = input("Expression: ").strip()

# Dividir a expressão em três partes: x, operador, y
x_str, operador, y_str = expressao.split(" ")

# Converter operandos para float
x = float(x_str)
y = float(y_str)

# Realizar a operação baseada no operador
if operador == "+":
    resultado = x + y
elif operador == "-":
    resultado = x - y
elif operador == "*":
    resultado = x * y
elif operador == "/":
    # Assume que y não é 0 para este exercício
    resultado = x / y

# Imprimir o resultado formatado com 1 casa decimal
print(f"{resultado:.1f}")