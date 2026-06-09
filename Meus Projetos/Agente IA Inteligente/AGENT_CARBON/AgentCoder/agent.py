import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# RESOLUÇÃO DE CAMINHO: Injeta dinamicamente a pasta atual no PATH do sistema
# Isso evita o erro ModuleNotFoundError ao carregar o arquivo trello_tool.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importação oficial das dependências do framework Google ADK
from google.adk.agents.llm_agent import Agent

# Conecta a ferramenta externa pura de integração com o Trello
from trello_tool import criar_cartao_trello

load_dotenv()

def get_temporal_context() -> str:
    """
    Retorna a data e a hora atual do sistema para ajudar a organizar as tarefas do dia.

    Returns:
        str: Texto contendo o timestamp formatado (ex: 'DD/MM/AAAA HH:MM:SS').
    """
    now = datetime.now()
    return f"Data e Hora atual do sistema: {now.strftime('%d/%m/%Y %H:%M:%S')}"


root_agent = Agent(
    model="gemini-2.0-flash", 
    name="AgentCoder",
    description="Agente de Organização de Tarefas com integração Trello baseado no Carbon Footprint",
    instruction="""Você é o Agente de Metas (Carbon Goal) baseado no ecossistema Carbon Footprint.
    Sua missão absoluta é receber tarefas de mitigação ambiental e registrá-las fisicamente no quadro Kanban do Trello do usuário.

    Seu fluxo de trabalho conversacional rígido:
    1. Assim que a sessão iniciar, invoque a ferramenta 'get_temporal_context' para capturar o momento atual do sistema.
    2. Cumprimente o usuário informando a data/hora obtida e pergunte quais são as tarefas ou metas de sustentabilidade do dia.
    3. Para cada tarefa de redução que o usuário descrever, pergunte de forma clara e educada se ele deseja registrá-la no Kanban.
    4. Quando o usuário confirmar a intenção de gravação, você deve OBRIGATORIAMENTE chamar a ferramenta 'criar_cartao_trello' passando um título claro e uma descrição com os detalhes técnicos.
    5. Após o retorno da ferramenta, apresente o link curto de acesso fornecido por ela diretamente na mensagem do chat.
    6. Continue investigando se há novas atividades para adicionar até o usuário declarar que finalizou.
    7. No fechamento da interação, gere um breve resumo amigável dos cartões que você salvou no dia.

    Regras Críticas de Execução:
    - Você está proibido de utilizar os termos "simular" ou inventar ficticiamente que salvou um registro em texto.
    - Se o usuário disse para registrar, a chamada para a função real 'criar_cartao_trello' é mandatória e obrigatória.
    - Responda sempre em português do Brasil de maneira profissional e limpa.""",
    tools=[get_temporal_context, criar_cartao_trello]
)