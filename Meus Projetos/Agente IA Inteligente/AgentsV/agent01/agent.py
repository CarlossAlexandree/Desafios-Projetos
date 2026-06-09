import os
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, instruction: str, tools: list):
        self.instruction = instruction
        self.tools = tools

def google_search(query: str) -> str:
    return f"Resultado simulado de busca para: {query}"

def criar_agente():
    agente = Agent(
        instruction="Você é um assistente focado em automação e análise de dados.",
        tools=[google_search]
    )
    return agente