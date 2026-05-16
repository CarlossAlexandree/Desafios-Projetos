def main():
    entrada = input("Input: ")
    print(f"Output: {shorten(entrada)}")

def shorten(word):
    vogais = "AEIOUaeiou"
    saida = ""
    for char in word:
        if char not in vogais:
            saida += char
    return saida

if __name__ == "__main__":
    main()