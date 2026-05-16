from um import count
import pytest

def test_single_um():
    # Testar palavra isolada e com maiúsculas
    assert count("um") == 1
    assert count("UM") == 1
    assert count("Um...") == 1

def test_sentence_with_um():
    # Testar frases com múltiplas ocorrências
    assert count("Um, obrigado pelo um.") == 2
    assert count("um, um, um") == 3

def test_substring_exclusion():
    # Testar palavras que contém "um" mas não são a palavra "um"
    # Exemplos: humano, resumo, comum, algoritmo
    assert count("O resumo do humano é comum.") == 0
    assert count("Um algoritmo comum.") == 1

def test_punctuation():
    # Testar se a pontuação ao redor da palavra é tratada corretamente
    assert count("um?") == 1
    assert count("Olá, um...") == 1
    assert count("um!") == 1