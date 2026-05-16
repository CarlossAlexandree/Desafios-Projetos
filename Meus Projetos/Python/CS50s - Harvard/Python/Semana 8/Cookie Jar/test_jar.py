# test_jar.py (Arquivo de testes unitários para a classe Jar)
import pytest
from jar_shirt import Jar

# Teste de inicialização padrão e com capacidade específica
def test_init():
    jar = Jar()
    assert jar.capacity == 12
    assert jar.size == 0
    jar2 = Jar(20)
    assert jar2.capacity == 20

# Teste da representação em string (emoji)
def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪" * 12

# Teste do método deposit e exceções
def test_deposit():
    jar = Jar(5)
    jar.deposit(3)
    assert jar.size == 3
    jar.deposit(2)
    assert jar.size == 5
    with pytest.raises(ValueError):
        jar.deposit(1) # Excede capacidade

# Teste do método withdraw e exceções
def test_withdraw():
    jar = Jar(10)
    jar.deposit(5)
    jar.withdraw(2)
    assert jar.size == 3
    jar.withdraw(3)
    assert jar.size == 0
    with pytest.raises(ValueError):
        jar.withdraw(1) # Excede quantidade atual