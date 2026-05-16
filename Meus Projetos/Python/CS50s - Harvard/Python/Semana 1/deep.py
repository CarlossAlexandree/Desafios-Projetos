# Solicitae a resposta
resposta = input("What is the Answer to the Great Question of Life, the Universe, and Everything? ").strip().lower()

# Verificae a resposta
if resposta == "42" or resposta == "forty-two" or resposta == "forty two":
    print("Yes")
else:
    print("No")