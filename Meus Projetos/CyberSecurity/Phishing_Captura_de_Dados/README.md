# Cybersecurity: Phishing para Captura de Dados

## 📝 Descrição do Projeto

Este projeto demonstra a criação de um ambiente de laboratório para testes de **Engenharia Social (Phishing)**. O objetivo principal é utilizar o framework **Social-Engineer Toolkit (SET)** para demonstrar como atacantes podem capturar informações inseridas por usuários em páginas falsas, reforçando a importância da vigilância e do uso de autenticação multifator.

## 🛠️ Ferramentas e Ambiente

* **Sistema Operacional:** Kali Linux (Máquina Atacante)
* **Ferramenta de Ataque:** Social-Engineer Toolkit (SET)
* **Ambiente de Virtualização:** VirtualBox
* **Vetor de Ataque:** Credential Harvester Attack Method (Web Templates)

## 🚀 Passo a Passo Executado

1.  **Privilégios Administrativos:** Acesso root via comando `sudo su`.
2.  **Configuração de Rede:** *Identificação do IP local através do comando `ifconfig`.
3.  **Preparação do SET:** 
* Navegação pelos menus: `Social-Engineering Attacks` -> `Website Attack Vectors` -> `Credential Harvester Attack Method`.
4.  **Estratégia de Clonagem:** Utilização de `Web Templates` para garantir a funcionalidade do servidor local na porta 80.
5.  **Simulação do Ataque:** O servidor foi ativado e a página falsa foi acessada através do IP do atacante.

## 📸 Evidências do Desafio

#### 1. Página de Phishing em Execução
O usuário acessa o IP do atacante e visualiza uma página de solicitação de dados (Template: Java Required).

![Phishing Attack](1-%20Phishing%20Attack.png)

#### 2. Intercepção de Dados no Terminal
Assim que o formulário é enviado, o SET captura a entrada e exibe o campo capturado (ex: `search_text=carlos`).

![Phishing Resposta](2-%20Phishing%20Resposta.png)

## 📊 Resultados Obtidos

O terminal exibiu a mensagem `[*] WE GOT A HIT!`, confirmando a interceptação de dados inseridos remotamente. Isso comprova a eficácia da ferramenta na colheita de dados em um cenário de teste controlado.

## ⚠️ Aviso Legal
Este projeto foi desenvolvido estritamente para fins educacionais. O uso dessas técnicas em cenários reais sem autorização prévia é ilegal e antiético.