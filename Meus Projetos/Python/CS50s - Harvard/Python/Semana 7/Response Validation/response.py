import re
from validator_collection import validators, checkers

def main():
    # Solicita o endereço de e-mail
    email = input("E-mail: ").strip()
    # Verifica se é um e-mail válido usando checkers
    if checkers.is_email(email):
        print("Valid")
    else:
        print("Invalid")

main()