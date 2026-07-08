"""Provedor Google Gemini — opção gratuita padrão (tem tier gratuito com visão)."""
import httpx

from app.core.config import get_settings
from app.core.exceptions import AIProviderError
from app.services.providers.base import AIVisionProvider

settings = get_settings()


class GeminiProvider(AIVisionProvider):
    name = "gemini"

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise AIProviderError(
                "GEMINI_API_KEY não configurada. Defina-a no arquivo .env "
                "(obtenha uma chave gratuita em https://aistudio.google.com/apikey)."
            )
        self._base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{settings.GEMINI_MODEL}:generateContent"
        )

    async def generate_threat_model(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        image_mime_type: str,
    ) -> str:
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_prompt},
                        {
                            "inline_data": {
                                "mime_type": image_mime_type,
                                "data": image_base64,
                            }
                        },
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "response_mime_type": "application/json",
            },
        }

        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(
                    self._base_url,
                    params={"key": settings.GEMINI_API_KEY},
                    json=payload,
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise AIProviderError(
                    f"Erro na API Gemini ({exc.response.status_code}): {exc.response.text[:300]}"
                ) from exc
            except httpx.RequestError as exc:
                raise AIProviderError(f"Falha de conexão com Gemini: {exc}") from exc

        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise AIProviderError(
                f"Resposta inesperada da API Gemini: {data}"
            ) from exc
