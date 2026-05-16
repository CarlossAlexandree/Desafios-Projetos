def main():
    # Solicita a frase ao usuário
    frase = input("Como você está se sentindo? (use :) ou :() ")
    
    # Chama a função de conversão e imprime o resultado
    print(converter(frase))

def converter(texto):
    # Substitui :) por 🙂
    texto = texto.replace(":)", "🙂")
    # Substitui :( por 🙁
    texto = texto.replace(":(", "🙁")
    return texto

main()