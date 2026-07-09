"""
calculadora.py
--------------
Exemplo SIMPLES: operações aritméticas básicas, incluindo um caso de
exceção esperada (divisão por zero) para exercitar testes de falha.
"""


def somar(a: float, b: float) -> float:
    return a + b


def subtrair(a: float, b: float) -> float:
    return a - b


def multiplicar(a: float, b: float) -> float:
    return a * b


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return a / b
