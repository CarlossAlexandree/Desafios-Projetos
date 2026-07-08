"""Provedor Ollama — modelo rodando 100% local, sem chave de API, sem custo."""
import httpx

from app.core.config import get_settings
from app.core.exceptions import AIProviderError
from app.services.providers.base import AIVisionProvider

settings = get_settings()


class OllamaProvider(AIVisionProvider):
    name = "ollama"

    def __init__(self) -> None:
        self._url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    async def generate_threat_model(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        image_mime_type: str,
    ) -> str:
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "images": [image_base64],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.4},
        }

        async with httpx.AsyncClient(timeout=120) as client:
            try:
                response = await client.post(self._url, json=payload)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise AIProviderError(
                    f"Erro no Ollama ({exc.response.status_code}): {exc.response.text[:300]}"
                ) from exc
            except httpx.RequestError as exc:
                raise AIProviderError(
                    f"Não foi possível conectar ao Ollama em {settings.OLLAMA_BASE_URL}. "
                    f"Verifique se ele está rodando (`ollama serve`). Detalhe: {exc}"
                ) from exc

        data = response.json()
        try:
            return data["response"]
        except KeyError as exc:
            raise AIProviderError(f"Resposta inesperada do Ollama: {data}") from exc
