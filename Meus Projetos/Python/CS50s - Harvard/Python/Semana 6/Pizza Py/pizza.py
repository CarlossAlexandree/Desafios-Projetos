import sys
import csv
from tabulate import tabulate

def main():
    # Verifica argumentos
    if len(sys.argv) != 2:
        sys.exit("Usage: python pizza.py filename.csv")
    
    filename = sys.argv[1]
    
    # Verifica se o arquivo é .csv
    if not filename.endswith(".csv"):
        sys.exit("Not a CSV file")
        
    try:
        with open(filename, "r") as file:
            # Lê o CSV usando csv.reader
            reader = csv.reader(file)
            # Transforma as linhas em uma lista de listas
            tabela = [row for row in reader]
            # Imprime a tabela formatada (primeira linha como cabeçalho, grid style)
            print(tabulate(tabela[1:], headers=tabela[0], tablefmt="grid"))
                
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()