"""Provedor Groq — LPU ultrarrápida, tier gratuito com modelos de visão Llama."""
import httpx

from app.core.config import get_settings
from app.core.exceptions import AIProviderError
from app.services.providers.base import AIVisionProvider

settings = get_settings()


class GroqProvider(AIVisionProvider):
    name = "groq"
    _url = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise AIProviderError(
                "GROQ_API_KEY não configurada. Defina-a no arquivo .env "
                "(obtenha uma chave gratuita em https://console.groq.com/keys)."
            )

    async def generate_threat_model(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        image_mime_type: str,
    ) -> str:
        payload = {
            "model": settings.GROQ_MODEL,
            "temperature": 0.4,
            "response_format": {"type": "json_object"},
            "messages": [
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
        }
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}

        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(self._url, json=payload, headers=headers)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise AIProviderError(
                    f"Erro na API Groq ({exc.response.status_code}): {exc.response.text[:300]}"
                ) from exc
            except httpx.RequestError as exc:
                raise AIProviderError(f"Falha de conexão com Groq: {exc}") from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise AIProviderError(f"Resposta inesperada da API Groq: {data}") from exc
