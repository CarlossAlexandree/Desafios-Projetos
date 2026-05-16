from datetime import date
import inflect
import sys

def main():
    # Solicita a data de nascimento
    nascimento_str = input("Date of Birth (YYYY-MM-DD): ").strip()
    try:
        # Tenta calcular os minutos e imprimir
        print(calculate_minutes(nascimento_str))
    except ValueError:
        sys.exit("Invalid format")

def calculate_minutes(birth_date_str):
    # Converte a string de data para um objeto datetime.date
    year, month, day = map(int, birth_date_str.split("-"))
    birth_date = date(year, month, day)
    
    # Obtém a data de hoje
    today = date.today()
    
    # Calcula a diferença de tempo (timedelta)
    delta = today - birth_date
    
    # Se a data de nascimento for no futuro, lança erro de valor
    if delta.days < 0:
        raise ValueError("Invalid format")
        
    # Calcula total de minutos arredondado para o minuto mais próximo
    minutes = delta.days * 24 * 60
    
    # Usa inflect para converter o número de minutos em palavras
    p = inflect.engine()
    words = p.number_to_words(minutes, andword="").capitalize()
    
    return f"{words} minutes"

if __name__ == "__main__":
    main()