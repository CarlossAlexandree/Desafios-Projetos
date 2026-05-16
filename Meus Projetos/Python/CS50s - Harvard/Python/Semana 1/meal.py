def main():
    # Solicitar o horário
    tempo = input("What time is it? ")
    
    # Converter o horário para horas em float
    horas = convert(tempo)
    
    # Verificar o intervalo de refeição
    if 7.0 <= horas <= 8.0:
        print("breakfast time")
    elif 12.0 <= horas <= 13.0:
        print("lunch time")
    elif 18.0 <= horas <= 19.0:
        print("dinner time")

def convert(time):
    # Dividir a string de tempo em horas e minutos
    horas_str, minutos_str = time.split(":")
    
    # Converter para float e calcular o total de horas
    horas = float(horas_str)
    minutos = float(minutos_str)
    return horas + (minutos / 60)

if __name__ == "__main__":
    main()