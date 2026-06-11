# 📊 Processamento de Dados com MySQL na Azure e Power BI

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300000f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## 📝 Descrição do Projeto
Este repositório contém a resolução do desafio de projeto focado na integração, extração e transformação de dados (ETL). O objetivo central é conectar uma base de dados **MySQL hospedada na nuvem (Azure)** ao **Power BI**, realizando o saneamento dos dados para prepará-los para modelagens futuras (Star Schema).

---

## 🏗️ Arquitetura do Ambiente (Azure)

Durante o desenvolvimento, foi configurado o ecossistema na Azure para sustentar a análise:

* **Resource Name:** `idiomasantiago` 👤
* **Resource Group:** `Santiago.profissional-rg` 📁
* **Region:** East US 🌎
* **API Type:** TextAnalytics (Legacy model)
* **Endpoint:** `https://idiomasantiago.cognitiveservices.azure.com/` 🔗

> [!IMPORTANT]
> **Status do Deploy:** A arquitetura lógica e o mapeamento de ETL foram concluídos. Contudo, a finalização do deploy total da instância MySQL na Azure está em estágio de transição e será concluída em um ciclo posterior de atualização.

---

## 🛠️ Etapas de Transformação de Dados (Power Query)

O processo de ETL seguiu diretrizes rígidas para garantir a integridade da informação:

1.  **Saneamento de Tipos:**
    * Valores monetários ajustados para **Decimal Fixo (Double Preciso)**.
2.  **Tratamento de Nulos:**
    * Análise da coluna `Super_ssn`: Identificação de colaboradores sem gerente (cargos de diretoria).
    * Verificação de departamentos sem gerentes preenchidos com dados fictícios de controle.
3.  **Engenharia de Atributos:**
    * **Separação de Colunas:** Granularidade do endereço (`Address`) expandida para facilitar análises regionais.
    * **Combinação de Nomes:** Junção de `Fname` e `Lname` para facilitar a leitura.
4.  **Integração de Consultas (Merge):**
    * **Employee + Department:** Associação dos nomes de departamentos aos respectivos funcionários.
    * **Colaboradores + Gerentes:** Realização de *Self-Join* para exibir o nome do supervisor direto de cada colaborador.
    * **Dept + Location:** Criação de combinações únicas de departamento e local.

---

## 🧠 Justificativa Teórica: Mesclar vs. Acrescentar

No contexto de **Departamentos e Localizações**, utilizamos a função **Mesclar (Merge)** em vez de **Acrescentar (Append)**.

* **Por que Mesclar?** Pois o objetivo é enriquecer a tabela de departamentos com novas colunas (informação horizontal). 
* **Por que não Acrescentar?** O comando "Acrescentar" é utilizado para empilhar linhas de tabelas com a mesma estrutura (informação vertical), o que causaria redundância e erro de lógica neste modelo relacional.

---

## 📂 Estrutura do Repositório

```text
├── sql_scripts/      # Scripts de criação e inserção (Esquema Company)
├── pbix_files/       # Relatório do Power BI (.pbix)
├── screenshots/      # Prints do modelo e dashboards
└── README.md         # Documentação do projeto
