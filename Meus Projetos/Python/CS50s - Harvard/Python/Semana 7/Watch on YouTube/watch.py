import re   
import sys  

def main():
    # Solicita o HTML e remove espaços extras no início/fim
    html = input("HTML: ").strip()
    
    # Chama a função parse para extrair o link do YouTube
    resultado = parse(html)
    
    # Verifica se encontrou um resultado válido
    if resultado:
        print(resultado)  # Exibe o link curto do YouTube
    else:
        print("No YouTube URL found")  # Mensagem caso não encontre

def parse(s):
    # Define o padrão regex para encontrar o link de embed do YouTube
    # Explicação do padrão:
    # <iframe.*src="        → encontra a tag iframe e o atributo src
    # https?://             → aceita http ou https
    # (?:www\.)?           → "www." é opcional
    # youtube\.com/embed/  → caminho padrão de embed do YouTube
    # ([a-zA-Z0-9_-]+)     → captura o ID do vídeo (letras, números, _ ou -)
    padrao = r'<iframe.*src="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
    
    # Procura no texto (string s) correspondente ao padrão regex
    match = re.search(padrao, s)
    
    # Se encontrar correspondência
    if match:
        video_id = match.group(1)  # Extrai o ID do vídeo capturado pelo regex
        return f"https://youtu.be/{video_id}"  # Retorna o link curto do YouTube
    
    # Caso não encontre nenhum vídeo válido
    return None

# Garante que o programa só será executado diretamente (e não importado como módulo)
if __name__ == "__main__":
    main()