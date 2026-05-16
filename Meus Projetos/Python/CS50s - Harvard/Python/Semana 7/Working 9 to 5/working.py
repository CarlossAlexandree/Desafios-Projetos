import re
import sys

def main():
    # Solicita o horário de trabalho
    tempo = input("Hours: ").strip()
    try:
        # Converte e imprime o resultado no formato 24h
        print(convert(tempo))
    except ValueError as e:
        # Levanta erro de valor se a entrada for inválida
        sys.exit(e)

def convert(s):
    # Regex para validar formatos AM/PM com ou sem minutos
    # ([1-9]|1[0-2])(:[0-5]\d)?: Captura hora (grupo 1) e minutos opcionais (grupo 2)
    # (AM|PM): Captura AM ou PM (grupo 3)
    # to: literal
    # ([1-9]|1[0-2])(:[0-5]\d)?: Captura hora (grupo 4) e minutos opcionais (grupo 5)
    # (AM|PM): Captura AM ou PM (grupo 6)
    padrao = r"^([1-9]|1[0-2])(:[0-5]\d)? (AM|PM) to ([1-9]|1[0-2])(:[0-5]\d)? (AM|PM)$"
    match = re.search(padrao, s)
    
    if match:
        hora_incio, minutos_inicio, ampm_inicio = int(match.group(1)), match.group(2), match.group(3)
        hora_fim, minutos_fim, ampm_fim = int(match.group(4)), match.group(5), match.group(6)
        
        # Converte horários de início e fim para 24h
        inicio_24h = to_24h(hora_incio, minutos_inicio, ampm_inicio)
        fim_24h = to_24h(hora_fim, minutos_fim, ampm_fim)
        
        # Retorna a string no formato HH:MM to HH:MM
        return f"{inicio_24h} to {fim_24h}"
    else:
        # Se não houver correspondência com o padrão, levanta erro de valor
        raise ValueError("Invalid format")

def to_24h(hora, minutos_str, ampm):
    # Define minutos como "00" se não forem fornecidos
    minutos = "00" if not minutos_str else minutos_str.replace(":", "")
    
    # Lógica de conversão baseada em AM/PM e horas (12h -> 24h)
    if ampm == "AM":
        if hora == 12:
            hora = 0
    else: # PM
        if hora != 12:
            hora += 12
            
    # Retorna hora formatada com preenchimento de zeros e minutos
    return f"{hora:02}:{minutos}"

if __name__ == "__main__":
    main()