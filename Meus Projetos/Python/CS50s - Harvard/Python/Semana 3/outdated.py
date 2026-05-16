def main():
    meses = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    while True:
        data_entrada = input("Date: ").strip()
        
        try:
            # Tenta o formato MM/DD/YYYY (ex: 9/8/1636)
            if "/" in data_entrada:
                mes_str, dia_str, ano_str = data_entrada.split("/")
                mes = int(mes_str)
                dia = int(dia_str)
                ano = int(ano_str)
                
                # Valida mês (1-12) e dia (1-31, simplificado)
                if 1 <= mes <= 12 and 1 <= dia <= 31:
                    print(f"{ano}-{mes:02}-{dia:02}")
                    break
            
            # Tenta o formato "Month Day, Year" (ex: September 8, 1636)
            elif "," in data_entrada:
                # Remove a vírgula e divide por espaço
                partes = data_entrada.replace(",", "").split(" ")
                
                # Deve haver exatamente 3 partes
                if len(partes) == 3:
                    mes_nome = partes[0].title()
                    dia_str = partes[1]
                    ano_str = partes[2]
                    
                    # Converte dia e ano para inteiro
                    dia = int(dia_str)
                    ano = int(ano_str)
                    
                    # Verifica se o nome do mês é válido e obtém o índice (+1)
                    if mes_nome in meses:
                        mes = meses.index(mes_nome) + 1
                        
                        # Valida dia (1-31, simplificado)
                        if 1 <= dia <= 31:
                            print(f"{ano}-{mes:02}-{dia:02}")
                            break
                            
        # Captura erros se o input for inválido para as operações
        except (ValueError, KeyError, IndexError):
            pass

main()