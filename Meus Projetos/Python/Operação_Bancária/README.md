# Sistema Bancário Automatizado em Python

Implementação da primeira versão de um Sistema Bancário desenvolvido em Python. O sistema criado simula as operações essenciais de uma conta bancária (Depósito, Saque e Extrato) para um único usuário, aplicando conceitos fundamentais de lógica de programação, estruturas de repetição e condicionais.

O objetivo principal é fornecer uma base, replicável e limpa (Clean Code), estruturada com foco em boas práticas de indentação, mensagens claras de erro e validações rigorosas de regras de negócio.

---

## 🎯 Funcionalidades Implementadas

O sistema atende de forma estrita aos seguintes requisitos de negócio:

### 💵 1. Operação de Depósito
* Permite depositar apenas valores positivos.
* Todas as movimentações bem-sucedidas são registradas no histórico do extrato.
* Atualização em tempo real do saldo bancário.

### 🏧 2. Operação de Saque
* Limite diário de até **3 saques**.
* Valor máximo por saque limitado a **R$ 500,00**.
* Verificação automática de saldo suficiente antes de efetivar a transação.
* Tratamento de erros detalhado para cada uma das regras (excesso de saldo, excesso de limite ou limite de saques atingido).

### 📄 3. Operação de Extrato
* Exibição cronológica de todos os depósitos e saques realizados.
* Caso não existam movimentações na conta, exibe a mensagem: `Não foram realizadas movimentações.`.
* Exibição formatada do saldo atualizado no rodapé do extrato no padrão monetário brasileiro.

---

## 💻 Estrutura do Código

O script principal utiliza uma estrutura de repetição contínua (`while True`) associada a um bloco de tomada de decisões (`if/elif/else`). As variáveis de controle monitoram o estado da conta durante a execução do processo:

* `saldo`: Armazena o montante disponível.
* `limite`: Define o teto financeiro individual por transação.
* `extrato`: String acumuladora que registra o histórico de operações.
* `numero_saques`: Contador de saques efetuados na sessão.
* `LIMITE_SAQUES`: Constante que fixa a quantidade permitida de saques.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.8 ou superior instalado em sua máquina.
* Visual Studio Code (VS Code) ou qualquer terminal de sua preferência.

### Passo a Passo

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. **Executar a Aplicação:**
   ```bash
   python sistema_bancario.py
   ```

3. **Interagir com o Menu:**
   Utilize os comandos exibidos no terminal (`d` para depositar, `s` para sacar, `e` para extrato e `q` para sair) para navegar pelas opções do sistema.

---

## 🗂️ Boas Práticas Adotadas

* **Validação de Entradas:** Proteção contra inserção de valores negativos ou nulos.
* **Mensagens Informativas:** Feedbacks claros ao usuário sobre o status de cada tentativa de transação.
* **Formatação Monetária:** Exibição padronizada de valores utilizando duas casas decimais (`:.2f`).
* **Estrutura Replicável:** Arquitetura limpa propícia para futuras refatorações, como a implementação de funções ou persistência em bancos de dados.