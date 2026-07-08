import pytest

from app.core.exceptions import AIResponseParsingError
from app.services.threat_analysis_service import _extract_json


def test_extracts_clean_json():
    raw = '{"summary": "ok", "threat_model": [], "improvement_suggestions": []}'
    result = _extract_json(raw)
    assert result["summary"] == "ok"


def test_extracts_json_wrapped_in_markdown_fence():
    raw = '```json\n{"summary": "ok", "threat_model": []}\n```'
    result = _extract_json(raw)
    assert result["summary"] == "ok"


def test_extracts_json_with_surrounding_text():
    raw = 'Aqui está a análise:\n{"summary": "ok"}\nEspero ter ajudado!'
    result = _extract_json(raw)
    assert result["summary"] == "ok"


def test_raises_when_no_json_found():
    with pytest.raises(AIResponseParsingError):
        _extract_json("isso não é json de jeito nenhum")
