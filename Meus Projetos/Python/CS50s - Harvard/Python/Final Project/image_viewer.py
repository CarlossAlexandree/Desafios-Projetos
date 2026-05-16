import platform
import os

def show_image(filepath: str):
    """
    Abre a imagem usando o caminho absoluto para evitar erros de diretório.
    """
    current_os = platform.system()
    # Converte o caminho relativo para absoluto (completo)
    absolute_path = os.path.abspath(filepath)
    
    try:
        if not os.path.exists(absolute_path):
            print(f"Erro: O arquivo {absolute_path} não foi criado.")
            return

        if current_os == "Windows":
            os.startfile(absolute_path)
        else:
            import subprocess
            cmd = "open" if current_os == "Darwin" else "xdg-open"
            subprocess.call([cmd, absolute_path])
            
        print(f"--- [Card exibido: {os.path.basename(filepath)}] ---")
        
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")