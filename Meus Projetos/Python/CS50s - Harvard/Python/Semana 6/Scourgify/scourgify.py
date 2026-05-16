import sys
import csv

def main():
    # Verifica argumentos
    if len(sys.argv) != 3:
        sys.exit("Usage: python scourgify.py input.csv output.csv")
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Verifica extensões .csv
    if not input_file.endswith(".csv") or not output_file.endswith(".csv"):
        sys.exit("Not a CSV file")
        
    try:
        # Lista para armazenar os dados limpos
        dados_limpos = []
        
        # Abre o arquivo de entrada para leitura
        with open(input_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Separa o nome em sobrenome e nome
                sobrenome, nome = row["name"].split(", ")
                # Cria um novo dicionário com os dados separados
                dados_limpos.append({
                    "first_name": nome,
                    "last_name": sobrenome,
                    "house": row["house"]
                })
                
        # Abre o arquivo de saída para escrita
        with open(output_file, "w", newline='') as file:
            # Define os cabeçalhos
            fieldnames = ["first_name", "last_name", "house"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Escreve o cabeçalho e os dados
            writer.writeheader()
            writer.writerows(dados_limpos)
                
    except FileNotFoundError:
        sys.exit(f"Could not read {input_file}")

if __name__ == "__main__":
    main()