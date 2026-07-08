"""
Provedor Azure OpenAI — mantido para compatibilidade com o material do curso.

Use este provedor se/quando você tiver uma assinatura paga do Azure OpenAI.
Requer o pacote `openai` (já incluso em requirements.txt).
"""
from openai import AsyncAzureOpenAI

from app.core.config import get_settings
from app.core.exceptions import AIProviderError
from app.services.providers.base import AIVisionProvider

settings = get_settings()


class AzureOpenAIProvider(AIVisionProvider):
    name = "azure_openai"

    def __init__(self) -> None:
        missing = [
            var
            for var, val in {
                "AZURE_OPENAI_API_KEY": settings.AZURE_OPENAI_API_KEY,
                "AZURE_OPENAI_ENDPOINT": settings.AZURE_OPENAI_ENDPOINT,
                "AZURE_OPENAI_DEPLOYMENT_NAME": settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            }.items()
            if not val
        ]
        if missing:
            raise AIProviderError(
                f"Variáveis ausentes para Azure OpenAI: {', '.join(missing)}"
            )

        self._client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

    async def generate_threat_model(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        image_mime_type: str,
    ) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{image_mime_type};base64,{image_base64}"
                                },
                            },
                        ],
                    },
                ],
            )
        except Exception as exc:  # SDK lança várias subclasses de OpenAIError
            raise AIProviderError(f"Erro na API Azure OpenAI: {exc}") from exc

        content = response.choices[0].message.content
        if not content:
            raise AIProviderError("Azure OpenAI retornou conteúdo vazio.")
        return content
