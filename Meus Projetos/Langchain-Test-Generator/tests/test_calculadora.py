import pytest

from examples.calculadora import dividir, multiplicar, somar, subtrair


def test_somar_caso_sucesso():
    assert somar(2, 3) == 5


def test_somar_com_negativos():
    assert somar(-2, -3) == -5


def test_subtrair_caso_sucesso():
    assert subtrair(10, 4) == 6


def test_multiplicar_caso_sucesso():
    assert multiplicar(3, 4) == 12


def test_multiplicar_por_zero():
    assert multiplicar(5, 0) == 0


def test_dividir_caso_sucesso():
    assert dividir(10, 2) == 5


def test_dividir_por_zero_levanta_excecao():
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0)
