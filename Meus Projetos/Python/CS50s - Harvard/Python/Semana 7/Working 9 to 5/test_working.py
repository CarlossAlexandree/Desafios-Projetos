from working import convert
import pytest

def test_valid_formats():
    # Testar formatos sem minutos
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("10 PM to 8 AM") == "22:00 to 08:00"
    # Testar formatos com minutos
    assert convert("10:30 PM to 8:50 AM") == "22:30 to 08:50"
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"

def test_noon_and_midnight():
    # Testar casos específicos de 12 AM e 12 PM
    assert convert("12:00 AM to 12:00 PM") == "00:00 to 12:00"
    assert convert("12 AM to 12 PM") == "00:00 to 12:00"

def test_invalid_format():
    # Testar formatos que não seguem o padrão "to" ou espaço
    with pytest.raises(ValueError):
        convert("9 AM - 5 PM")
    with pytest.raises(ValueError):
        convert("09:00 AM to 17:00 PM")
    with pytest.raises(ValueError):
        convert("9AM to 5PM")

def test_invalid_time():
    # Testar horários impossíveis (minutos > 59 ou horas > 12)
    with pytest.raises(ValueError):
        convert("9:60 AM to 5:60 PM")
    with pytest.raises(ValueError):
        convert("13 AM to 1 PM")
    with pytest.raises(ValueError):
        convert("12:60 AM to 12:00 PM")