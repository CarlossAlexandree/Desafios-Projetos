import io

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from app.core.exceptions import ImageTooLargeError, InvalidImageError
from app.services.image_service import validate_and_encode_image


def _make_upload(filename: str, content: bytes, content_type: str) -> UploadFile:
    """Helper: cria um UploadFile com content_type definido (API do Starlette)."""
    headers = Headers({"content-type": content_type})
    return UploadFile(filename=filename, file=io.BytesIO(content), headers=headers)


@pytest.mark.asyncio
async def test_rejects_unsupported_content_type():
    upload = _make_upload("arquivo.txt", b"nao e imagem", "text/plain")

    with pytest.raises(InvalidImageError):
        await validate_and_encode_image(upload)


@pytest.mark.asyncio
async def test_rejects_empty_file():
    upload = _make_upload("vazio.png", b"", "image/png")

    with pytest.raises(InvalidImageError):
        await validate_and_encode_image(upload)


@pytest.mark.asyncio
async def test_accepts_valid_png(fake_image_bytes):
    upload = _make_upload("diagrama.png", fake_image_bytes, "image/png")

    encoded, mime = await validate_and_encode_image(upload)

    assert mime == "image/png"
    assert isinstance(encoded, str)
    assert len(encoded) > 0


@pytest.mark.asyncio
async def test_rejects_oversized_image(monkeypatch):
    from app.services import image_service

    monkeypatch.setattr(image_service.settings, "MAX_IMAGE_SIZE_MB", 0.0000001)
    upload = _make_upload("grande.png", b"x" * 1000, "image/png")

    with pytest.raises(ImageTooLargeError):
        await validate_and_encode_image(upload)
