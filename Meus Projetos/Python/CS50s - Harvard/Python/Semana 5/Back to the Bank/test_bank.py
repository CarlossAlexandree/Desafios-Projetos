import pytest
from bank import value

# Teste para o cenário de 0 dólares (começa com hello)
def test_value_0():
    assert value("hello") == 0
    assert value("Hello, friend") == 0
    assert value("HELLO WORLD") == 0

# Teste para o cenário de 20 dólares (começa com h, mas não hello)
def test_value_20():
    assert value("hi") == 20
    assert value("Hey there") == 20
    assert value("How are you?") == 20

# Teste para o cenário de 100 dólares (outros)
def test_value_100():
    assert value("What's up?") == 100
    assert value("good morning") == 100
    assert value("   ") == 100