import re
import webbrowser  # Biblioteca para abrir links no navegador

def main():
    html = input("HTML: ").strip()
    resultado = parse(html)
    
    if resultado:
        print(resultado)
        webbrowser.open(resultado)  # Abre o vídeo automaticamente
    else:
        print("No YouTube URL found")

def parse(s):
    padrao = r'<iframe.*src="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
    
    match = re.search(padrao, s)
    
    if match:
        video_id = match.group(1)
        return f"https://youtu.be/{video_id}"
    
    return None

if __name__ == "__main__":
    main()