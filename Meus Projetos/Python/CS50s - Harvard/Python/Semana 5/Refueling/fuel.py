def main():
    while True:
        entrada = input("Fraction: ")
        try:
            porcentagem = convert(entrada)
            print(gauge(porcentagem))
            break
        except (ValueError, ZeroDivisionError):
            pass

def convert(fraction):
    try:
        x_str, y_str = fraction.split("/")
        x = int(x_str)
        y = int(y_str)
        if y == 0:
            raise ZeroDivisionError("Y cannot be zero")
        if x > y:
            raise ValueError("X cannot be greater than Y")
        return round((x / y) * 100)
    except (ValueError, ZeroDivisionError):
        # Relança as exceções para que possam ser testadas
        raise

def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"

if __name__ == "__main__":
    main()