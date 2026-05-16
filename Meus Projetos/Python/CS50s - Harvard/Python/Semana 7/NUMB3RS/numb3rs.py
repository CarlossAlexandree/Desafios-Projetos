import re
import sys

def main():
    # Solicita o endereço IP
    ip = input("IPv4 Address: ").strip()
    if validate(ip):
        print("Valid")
    else:
        print("Invalid")

def validate(ip):
    # Regex para validar cada octeto (0-255)
    # ^: início, \d: dígito, {1,3}: 1 a 3 vezes, $: fim
    # (25[0-5]|2[0-4]\d|[01]?\d\d?): 250-255 OU 200-249 OU 0-199
    # Repetido 4 vezes separado por ponto literal (\.)
    padrao = r"^(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$"
    if re.search(padrao, ip):
        return True
    return False

if __name__ == "__main__":
    main()