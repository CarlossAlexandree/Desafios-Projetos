# CS50's Introduction to Programming with Python 🐍

Este repositório contém a coleção completa de exercícios, laboratórios e o projeto final desenvolvidos por mim  (**Carlos Alexandre**) durante o curso **CS50P da Harvard University**. O foco principal foi o domínio da linguagem Python, aplicando boas práticas de programação, testes automatizados e arquitetura de sistemas.

## 🎓 Sobre o Curso
O curso abrange desde os fundamentos de sintaxe até conceitos avançados, incluindo:
* **Funções e Variáveis**: Manipulação de inputs e lógica básica (`indoor.py`, `einstein.py`).
* **Estruturas de Controle**: Condicionais e laços de repetição (`deep.py`, `coke.py`).
* **Exceções e Bibliotecas**: Tratamento de erros e uso de pacotes externos (`fuel.py`, `figlet.py`).
* **Testes Unitários**: Garantia de qualidade com `pytest` (`test_bank.py`, `test_plates.py`).
* **File I/O e Regex**: Manipulação de arquivos CSV/Imagens e expressões regulares (`scourgify.py`, `numb3rs.py`).
* **POO (Programação Orientada a Objetos)**: Classes, métodos e propriedades (`jar.py`, `seasons.py`).

---

## 🚀 Projeto Final: Flashcard System with Spaced Repetition

O projeto de conclusão consiste em um sistema de gerenciamento de **Flashcards** baseado no conceito de **Repetição Espaçada**.

### Funcionalidades:
* **Gerenciamento de Decks**: Criação e organização de baralhos por temas.
* **Algoritmo de Agendamento**: Interface que prioriza cards com maior dificuldade de memorização.
* **Persistência**: Salvamento automático do progresso e dos dados em arquivos JSON.
* **Testes Automatizados**: Suite de testes completa para validar a lógica de estudo.

---

## 🛠️ Tecnologias e Ferramentas
* **Linguagem**: Python 3.12+
* **Ambiente de Desenvolvimento**: VS Code Desktop
* **Testes**: Pytest
* **Bibliotecas Relevantes**: `requests`, `fpdf2`, `pillow`, `inflect`, `pyfiglet`, `emoji`.

---

## ☁️ Guia de Deploy e Integração

Para transformar estes scripts em ferramentas utilizáveis em ambiente de produção, siga os passos abaixo:

### 1. Preparação do Ambiente
Certifique-se de ter o Python instalado e crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```