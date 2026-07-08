"""Interface (contrato) que todo provedor de IA com visão deve implementar."""
from abc import ABC, abstractmethod


class AIVisionProvider(ABC):
    """
    Cada provedor (Gemini, Groq, Azure OpenAI, Ollama) implementa esta
    interface. Isso permite trocar de provedor apenas mudando a variável
    de ambiente AI_PROVIDER, sem tocar no restante da aplicação
    (Strategy Pattern / Dependency Inversion).
    """

    name: str

    @abstractmethod
    async def generate_threat_model(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        image_mime_type: str,
    ) -> str:
        """Deve retornar a resposta bruta (texto) do modelo, idealmente um JSON."""
        raise NotImplementedError
