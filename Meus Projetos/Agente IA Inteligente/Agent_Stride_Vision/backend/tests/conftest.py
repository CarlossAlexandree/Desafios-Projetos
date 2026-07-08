import io
import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("AI_PROVIDER", "gemini")
os.environ.setdefault("GEMINI_API_KEY", "test-key-fake")

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake_image_bytes() -> bytes:
    # PNG 1x1 mínimo válido (cabeçalho + IHDR + IDAT + IEND)
    return bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108020000009077"
        "53de0000000c4944415478da6360606000000005000101fda0d92e0000000049454e44ae426082"
    )
