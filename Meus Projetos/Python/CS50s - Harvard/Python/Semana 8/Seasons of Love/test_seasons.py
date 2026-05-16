from seasons import calculate_minutes
import pytest

def test_calculate_minutes_one_year():
    # Testar exatamente um ano atrás (365 dias * 24 * 60 = 525600 minutos)
    # Nota: Este teste assume que hoje não é um dia após um ano bissexto para simplificar
    # Mas para o CS50, testar strings específicas de datas conhecidas é o padrão
    assert calculate_minutes("2025-04-26") == "Five hundred twenty-five thousand, six hundred minutes"

def test_calculate_minutes_two_years():
    # Testar dois anos atrás (1051200 minutos)
    assert calculate_minutes("2024-04-26") == "One million, fifty-one thousand, two hundred minutes"

def test_invalid_date_format():
    # Testar se o código levanta ValueError para formatos incorretos
    with pytest.raises(ValueError):
        calculate_minutes("January 1, 1999")
    with pytest.raises(ValueError):
        calculate_minutes("1999/01/01")
    with pytest.raises(ValueError):
        calculate_minutes("1999-13-01")

def test_future_date():
    # Testar data no futuro
    with pytest.raises(ValueError):
        calculate_minutes("2030-01-01")