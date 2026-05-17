# Sistema Bancário Otimizado com Programação Orientada a Objetos (POO) em Python

Modelagem de um sistema bancário utilizando conceitos avançados de Programação Orientada a Objetos (POO) com Python. Este projeto realiza a transição de uma estrutura anterior baseada em dicionários para um modelo mais completo baseado em classes estruturadas, totalmente aderente a um diagrama de classes UML.

## 📌 Objetivos do Desafio

* **Modelagem Estruturada:** Implementar classes para representar os componentes do ecossistema bancário (Clientes, Contas, Transações e Histórico).
* **Aderência ao Padrão UML:** Mapear de forma precisa atributos, métodos, heranças e interfaces propostas pelo modelo conceitual.
* **Refatoração do Fluxo:** Atualizar as funções de interação com o usuário (Menu) para consumir os novos objetos e métodos encapsulados.
* **Suporte Multi-Contas:** Ajustar o sistema para permitir que um mesmo cliente possua mais de uma conta associada de forma dinâmica.

## 📐 Arquitetura do Sistema (Modelo UML)

O sistema foi modelado aplicando conceitos fundamentais de POO:

* **Abstração e Classes Abstratas:** A classe `Transacao` atua como uma interface abstrata utilizando o módulo `abc`, obrigando a implementação dos métodos de registro pelas operações filhas.
* **Herança:** `PessoaFisica` estende as propriedades genéricas de `Cliente`, enquanto `ContaCorrente` herda as características da classe base `Conta`.
* **Encapsulamento:** Utilização de propriedades (`@property`) para proteger e expor atributos internos de saldo, histórico, número e agência.
* **Associação e Composição:** Um `Cliente` possui uma lista de `Contas`. Cada `Conta` possui uma instância própria de `Historico` para composição de logs de transações.

## ⚙️ Funcionalidades Implementadas

* **Cadastro de Clientes (Pessoa Física):** Registro de nome, data de nascimento, CPF e endereço completo.
* **Abertura de Contas Correntes:** Criação de contas vinculadas ao CPF do cliente com limite padrão de saque de R$ 500,00 e restrição de até 3 saques diários.
* **Depósitos e Saques Orientados a Objetos:** Processamento de transações que validam regras de negócio através de objetos específicos (`Deposito` e `Saque`).
* **Extrato Detalhado:** Exibição cronológica das movimentações da conta contendo data, hora, tipo de transação e saldo atualizado.
* **Seleção Dinâmica de Contas:** Mecanismo inteligente capaz de identificar se o cliente possui mais de uma conta corrente ativa e solicitar qual delas ele deseja utilizar na operação.


## 📄 Licença

Este projeto é de caráter estritamente educacional e está sob a licença MIT. Sinta-se à vontade para clonar, estudar e propor melhorias através de Pull Requests.