import pytest

from examples.validador_cpf import validar_cpf


def test_cpf_valido_sem_formatacao():
    assert validar_cpf("52998224725") is True


def test_cpf_valido_com_formatacao():
    assert validar_cpf("529.982.247-25") is True


def test_cpf_com_todos_digitos_iguais_e_invalido():
    assert validar_cpf("111.111.111-11") is False


def test_cpf_com_tamanho_incorreto_e_invalido():
    assert validar_cpf("123456") is False


def test_cpf_com_digitos_verificadores_incorretos_e_invalido():
    assert validar_cpf("529.982.247-00") is False


def test_cpf_vazio_e_invalido():
    assert validar_cpf("") is False
