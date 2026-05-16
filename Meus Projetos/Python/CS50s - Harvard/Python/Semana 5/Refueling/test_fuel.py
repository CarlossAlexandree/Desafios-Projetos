import pytest
from fuel import convert, gauge

# Teste da função convert com entradas válidas
def test_convert_valid():
    assert convert("3/4") == 75
    assert convert("1/2") == 50
    assert convert("1/100") == 1
    assert convert("0/100") == 0

# Teste da função convert com entradas inválidas (lançamento de exceções)
def test_convert_invalid():
    with pytest.raises(ValueError):
        convert("4/3") # X > Y
    with pytest.raises(ZeroDivisionError):
        convert("1/0") # Y = 0
    with pytest.raises(ValueError):
        convert("a/b") # Não inteiros

# Teste da função gauge
def test_gauge():
    assert gauge(75) == "75%"
    assert gauge(50) == "50%"
    assert gauge(1) == "E"
    assert gauge(0) == "E"
    assert gauge(99) == "F"
    assert gauge(100) == "F"