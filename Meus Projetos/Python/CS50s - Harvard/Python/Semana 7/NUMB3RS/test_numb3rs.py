from numb3rs import validate

def test_valid_ipv4():
    # Testando IPs válidos comuns
    assert validate("127.0.0.1") == True
    assert validate("255.255.255.255") == True
    assert validate("0.0.0.0") == True
    assert validate("192.168.1.1") == True

def test_invalid_range():
    # Testando números fora do intervalo 0-255
    assert validate("256.1.1.1") == False
    assert validate("1.256.1.1") == False
    assert validate("1.1.256.1") == False
    assert validate("1.1.1.256") == False
    assert validate("512.512.512.512") == False

def test_invalid_format():
    # Testando formatos incorretos (mais ou menos octetos)
    assert validate("1.2.3") == False
    assert validate("1.2.3.4.5") == False
    assert validate("1.2.3.4.") == False
    assert validate(".1.2.3.4") == False

def test_non_numeric():
    # Testando strings que não são IPs
    assert validate("cat") == False
    assert validate("1.2.3.cat") == False
    assert validate("google.com") == False