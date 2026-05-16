# Solicita o cumprimento
cumprimento = input("Greeting: ").strip().lower()

# Verifica o cumprimento e define o valor
if cumprimento.startswith("hello"):
    print("$0")
elif cumprimento.startswith("h"):
    print("$20")
else:
    print("$100")