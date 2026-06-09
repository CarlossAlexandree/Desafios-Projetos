import os
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, model: str, name: str, description: str, instruction: str):
        self.model = model
        self.name = name
        self.description = description
        self.instruction = instruction

root_agent = Agent(
    model='hf-open-llm',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="Você é um assistente engraçado e educado e sempre responde com bom humor com um emoji no final e detalhe torce para o Brasil. 🐳"
)