import pytest
from twittr import shorten

# Teste com strings comuns (maiúsculas e minúsculas)
def test_shorten_strings():
    assert shorten("Twitter") == "Twttr"
    assert shorten("TwiTTer") == "TwTTr"
    assert shorten("HELLO") == "HLL"

# Teste com números e pontuação
def test_shorten_numbers_punctuation():
    assert shorten("12345") == "12345"
    assert shorten("Hello, World!") == "Hll, Wrld!"

# Teste com strings vazias
def test_shorten_empty():
    assert shorten("") == ""