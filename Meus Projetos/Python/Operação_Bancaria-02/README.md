# Core Banking Automatizado

Evolução da primeira versão do Sistema Bancário em Python. O escopo do projeto foi expandido para cobrir o paradigma de modularização estrita através de funções, além de implementar o mapeamento relacional em memória para suportar múltiplos usuários e contas concorrentes.

O projeto deixa de ser um script linear e passa a operar como um pacote modular de microsserviço de transações, focado em alta manutenibilidade, Clean Code e tipagem estruturada de chamadas.

---

## 🏗️ Atualizações Arquiteturais e Novas Funcionalidades

Esta versão 2 trouxe melhorias significativas na estrutura e regras de negócio:

### 🧩 1. Modularização Avançada e Regras de Escopo (PEP 448 & PEP 570)
Cada operação foi isolada em funções independentes, aplicando os conceitos rigorosos de controle de argumentos do Python:
* **`depositar` (Positional-only):** Garante desempenho e restrição posicional dos argumentos utilizando a sintaxe `/`.
* **`sacar` (Keyword-only):** Aumenta a segurança do código forçando que parâmetros sensíveis (como saldos e limites) sejam explicitamente nomeados com a sintaxe `*`, mitigando erros humanos de acoplamento.
* **`exibir_extrato` (Misto):** Demonstra o domínio combinado de ambas as regras de parametrização.

### 👥 2. Cadastro de Usuários (Clientes)
* Armazenamento dinâmico dentro de estruturas de dicionários mapeados em listas.
* **Validação de Chave Única (CPF):** Varredura linear automatizada para impedir a duplicidade de cadastros sob um mesmo CPF (armazenando estritamente caracteres numéricos).
* Estruturação de dados completos contendo Nome, Data de Nascimento e Endereço formatado.

### 💳 3. Abertura e Vínculo de Contas Correntes
* Sistema de numeração sequencial automático iniciando em 1.
* Código da agência fixado estritamente como `"0001"`.
* **Mapeamento de Dependência:** Uma conta corrente só pode ser gerada se o CPF do usuário já constar previamente na base de dados (relacionamento de 1:N — um usuário pode possuir várias contas, mas uma conta pertence a um único usuário).

---

## 🛠️ Tecnologias e Conceitos Demonstrados

* **Python 3.10+** (Módulos nativos como `textwrap` para formatação de layouts limpos em terminal).
* **List Comprehensions** de alta performance para busca e filtragem rápida de registros.
* **Paradigma Funcional** aplicado à limpeza e desacoplamento de escopo global.

---