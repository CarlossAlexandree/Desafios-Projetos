# 🛒 Projeto Conceitual – Banco de Dados E-commerce

Este repositório contém a modelagem conceitual de um sistema de E-commerce,
estruturado para suportar **clientes PF e PJ**, múltiplos vendedores,
fornecedores, estoque, pedidos, pagamentos múltiplos e rastreamento de entrega.

---

## 🎯 Objetivo do Projeto
Desenvolver um **Modelo Entidade-Relacionamento (MER)** eficaz e coerente
seguindo boas práticas de modelagem de banco de dados,
com aderência a um cenário real de E-commerce.

---

## 🧠 Regras Principais Implementadas

### 👤 Clientes
- Cliente é uma superentidade
- Segregado em:
  - Cliente PF
  - Cliente PJ
- Cada cliente pode realizar pedidos

---

### 📦 Produtos e Fornecimento
- Produto pode ser fornecido por fornecedores
- Produto pode ser vendido por terceiros (marketplace)
- Controle de estoque
- Quantidade disponível

---

### 📝 Pedido
- Pedido está associado a um cliente
- Um pedido possui vários produtos
- Um produto pode estar em vários pedidos
- Relacionamento N:N representado por entidade associativa

---

### 💳 Pagamento
- Suporta múltiplas formas de pagamento
- Pagamento pode ser dividido
- Registro de pagamento realizado

---

### 🚚 Entrega
- Cada pedido possui uma entrega
- Entrega com rastreamento
- Status da entrega armazenado

---

## 🗺️ Modelo Conceitual

### 🔹 Diagrama Geral do E-commerce
![Modelo Conceitual](docs/diagramas/projeto_conceitual.png)

---

## 👤 Especialização Cliente PF / PJ
![Especialização Cliente](docs/diagramas/especializacao_cliente.png)

---

## 🏗️ Tecnologias / Ferramentas Utilizadas
- MySQL Workbench
- Modelagem MER
- Notação de relacionamentos (Classic)

---

## 📚 Status do Projeto
✔️ Modelo Conceitual Finalizado  
⬜ Modelo Lógico  
⬜ Modelo Físico  
⬜ Scripts SQL

---



<img width="962" height="1334" alt="Projeto Conceitual - Ecommerce_Refinado" src="https://github.com/user-attachments/assets/78ce3dc3-08be-4181-aa95-1068256fc1d6" />


## ✨ Autor
Projeto Conceitual desenvolvido por:
**Carlos Alexandre**

---

Se quiser acompanhar a evolução, fique à vontade para contribuir 👍 😊
