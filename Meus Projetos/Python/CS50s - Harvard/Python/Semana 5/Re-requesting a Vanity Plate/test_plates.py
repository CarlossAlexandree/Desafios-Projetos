import pytest
from plates import is_valid

# Teste de placas válidas
def test_is_valid_valid():
    assert is_valid("CS50") == True
    assert is_valid("AAA222") == True
    assert is_valid("AAA022") == False # 0 não pode ser o primeiro dígito
    assert is_valid("ECTO88") == True

# Teste de tamanho
def test_is_valid_length():
    assert is_valid("A") == False
    assert is_valid("AAAA") == True
    assert is_valid("AAAAAAA") == False

# Teste de letras iniciais
def test_is_valid_start():
    assert is_valid("A1") == False
    assert is_valid("1A") == False
    assert is_valid("AA") == True

# Teste de posição de números e pontuação
def test_is_valid_numbers_punctuation():
    assert is_valid("AAA22A") == False # Letra após número
    assert is_valid("AAA2.2") == False # Pontuação
    assert is_valid("PI3.14") == False # Pontuação