"""
validador_cpf.py
----------------
Exemplo mais COMPLEXO: validação de CPF (documento brasileiro) usando o
algoritmo real dos dígitos verificadores. Bom candidato para testes de
borda (CPFs com todos os dígitos iguais, tamanho errado, dígitos
verificadores inválidos, formatação com pontuação, etc.).
"""

import re


def _somente_digitos(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def _calcular_digito(cpf_parcial: str) -> int:
    pesos = list(range(len(cpf_parcial) + 1, 1, -1))
    soma = sum(int(d) * p for d, p in zip(cpf_parcial, pesos))
    resto = (soma * 10) % 11
    return 0 if resto == 10 else resto


def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF (com ou sem pontuação).

    Regras:
    - Deve conter exatamente 11 dígitos após remover pontuação.
    - Não pode ter todos os dígitos iguais (ex.: '111.111.111-11').
    - Os dois dígitos verificadores devem bater com o algoritmo oficial.
    """
    numeros = _somente_digitos(cpf)

    if len(numeros) != 11:
        return False

    if numeros == numeros[0] * 11:
        return False

    primeiro_digito = _calcular_digito(numeros[:9])
    segundo_digito = _calcular_digito(numeros[:9] + str(primeiro_digito))

    return numeros[-2:] == f"{primeiro_digito}{segundo_digito}"
