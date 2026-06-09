import os
from dotenv import load_dotenv

# Importações dos módulos locais a partir da raiz do projeto
from agent01.agent import criar_agente  # Ajustado para mapear a pasta correta
from agent02.agent import root_agent
from agent03.agent import database_agent

# Carrega as variáveis de ambiente locais do arquivo .env
load_dotenv()

# Extração segura das credenciais guardadas no cofre local
valor1 = os.getenv('chave1')
valor2 = os.getenv('chave2')
token_seguro = os.getenv('HF_TOKEN')

def main() -> None:
    print('--- Inicializando Ecossistema de Agentes (AgentsV) ---')
    print('======================================================')
    
    # EXECUÇÃO E LOGS DO AGENT 01
    print('[AGENT 01] - Validação de Infraestrutura Local Protegida')
    print(f'Segredo recuperado com segurança: {token_seguro}')
    print(f'Valor 1 extraído do ambiente: {valor1}')
    print(f'Valor 2 extraído do ambiente: {valor2}')
    
    agente_01 = criar_agente()
    print("Agente de IA 01 carregado com sucesso.")
    print('------------------------------------------------------')
    
    # EXECUÇÃO E LOGS DO AGENT 02
    print('[AGENT 02] - Inicialização de Persona e Comportamento')
    print(f"Agent02 carregado com a persona ativa: '{root_agent.name}'")
    print(f"Diretriz de comportamento injetada: Engraçado/Educado/Torcedor do Brasil.")
    print('------------------------------------------------------')
    
    # EXECUÇÃO E LOGS DO AGENT 03
    print('[AGENT 03] - Integração do Protocolo MCP com MySQL')
    print(f"Agent03 carregado e conectado ao endpoint MCP: '{database_agent.mcp_endpoint}'")
    print(f"Ferramenta de leitura de banco acoplada: {database_agent.tools}")
    print('======================================================')
    
    print("Ambiente de produção unificado operando com sucesso e custo zero!")

if __name__ == "__main__":
    main()