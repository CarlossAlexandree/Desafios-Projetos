"""Validação e pré-processamento da imagem de arquitetura enviada."""
import base64

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.exceptions import ImageTooLargeError, InvalidImageError

settings = get_settings()


async def validate_and_encode_image(imagem: UploadFile) -> tuple[str, str]:
    """
    Valida tipo/tamanho da imagem e retorna (base64_string, mime_type).

    Mantemos tudo em memória (sem salvar em disco) — mais seguro, mais rápido
    e evita o problema de espaço em disco/arquivos temporários órfãos que o
    código original do curso tinha (tempfile + os.remove manual).
    """
    if imagem.content_type not in settings.allowed_image_types_list:
        raise InvalidImageError(
            f"Tipo de arquivo não suportado: {imagem.content_type}. "
            f"Tipos aceitos: {', '.join(settings.allowed_image_types_list)}"
        )

    content = await imagem.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise ImageTooLargeError(
            f"Imagem tem {size_mb:.1f}MB. O limite é {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    if len(content) == 0:
        raise InvalidImageError("Arquivo de imagem vazio.")

    encoded = base64.b64encode(content).decode("utf-8")
    return encoded, imagem.content_type
