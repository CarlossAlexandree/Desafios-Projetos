import os
import sys
import socket
from dotenv import load_dotenv

def verificar_sistema():
    print("=== INICIALIZANDO AUDITORIA DE INFRAESTRUTURA (SYSTEM CHECK) ===")
    erros = 0

    # 1. Validar Versão do Python
    print(f"[*] Python Versão: {sys.version.split()[0]} - OK")

    # 2. Validar Status da Venv
    if 'VIRTUAL_ENV' in os.environ:
        print(f"[*] Ambiente Virtual (Venv): Ativo ({os.environ['VIRTUAL_ENV']}) - OK")
    else:
        print("[!] Ambiente Virtual (Venv): NÃO DETECTADO! Ative o labenv.")
        erros += 1

    # 3. Validar Carregamento do .env
    load_dotenv()
    if os.getenv("HF_TOKEN"):
        print("[*] Configuração .env: Variáveis carregadas com segurança - OK")
    else:
        print("[!] Configuração .env: Token de autenticação não encontrado.")
        erros += 1

    # 4. Validar Dependências do Google GenAI
    try:
        from google import genai
        print("[*] Dependências: SDK 'google-genai' resolvido com sucesso - OK")
    except ImportError:
        print("[!] Dependências: SDK 'google-genai' não está instalado.")
        erros += 1

    # 5. Validar Conectividade DNS
    try:
        socket.create_connection(("huggingface.co", 80), timeout=3)
        print("[*] Conectividade: Resolução de DNS externa para HuggingFace - OK")
    except OSError:
        print("[!] Conectividade: Falha de rede ou bloqueio de DNS. Verifique o Proxy.")
        erros += 1

    # 6. Validar Porta do Servidor MCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", 8050))
        print("[*] Porta 8050: Disponível para inicialização do MCP Server - OK")
    except socket.error:
        print("[!] Porta 8050: Já está em uso por outra instância.")
        erros += 1
    finally:
        s.close()

    print("=================================================================")
    if erros == 0:
        print("STATUS: Fundação pronta para produção! Sistema operacional estável.")
    else:
        print(f"STATUS: Auditoria concluída com {erros} aviso(s). Ajuste os pontos acima.")

if __name__ == "__main__":
    verificar_sistema()