# 📊 Relatório de Vendas e Lucros com Data Analytics

Este repositório faz parte do meu portfólio de **Engenharia de Dados e Business Intelligence**, com foco em análise de performance comercial e lucratividade. O relatório foi desenvolvido a partir ds dados **Financials** disponibilizado no **Power BI** para transformar dados brutos em insights estratégicos para a tomada de decisão. 

---

## 📝 Descrição Geral
Este repositório contém um arquivo `.pbix` que apresenta um dashboard interativo para monitoramento de KPIs comerciais. O objetivo principal é fornecer uma visão clara sobre o volume de vendas, margem de lucro e comportamento de mercado, utilizando técnicas avançadas de modelagem de dados e visualização.

### Principais Funcionalidades:
* **Análise de Vendas:** Acompanhamento de receita bruta e volume de transações.
* **Gestão de Lucratividade:** Visualização de margens e identificação de produtos/regiões mais rentáveis.
* **Visuals Customizados:** Utilização de componentes avançados como *Power KPI*, *Bullet Chart* e ícones dinâmicos para facilitar a leitura dos dados.
* **Filtros Dinâmicos:** Segmentação por data, categoria e outros atributos essenciais.

## 🛠️ Tecnologias e Ferramentas
* **Power BI Desktop:** Construção do relatório e visualizações.
* **DAX (Data Analysis Expressions):** Criação de medidas calculadas para indicadores de performance.
* **Power Query (M):** Extração, transformação e carregamento (ETL) dos dados brutos.

## ☁️ Guia de Deploy e Integração Cloud
Conforme as boas práticas de Data Analytics, este projeto foi estruturado para integração com ambientes em nuvem, visando escalabilidade:

### 1. Publicação no Power BI Service
* O relatório pode ser publicado em um **Workspace** dedicado no Azure para governança.
* Configuração de **Scheduled Refresh** (atualização agendada) via Gateway de Dados para manter os dashboards sincronizados.

### 2. Integração com Azure Data Lake / SQL Database
* A fonte de dados está preparada para migração de arquivos locais para um **Azure SQL Database** ou arquivos parquet em um **Data Lake Storage Gen2**.
* Implementação de segurança via **Row-Level Security (RLS)** para garantir que cada nível hierárquico acesse apenas os dados pertinentes.

## 📁 Estrutura do Repositório
O arquivo principal é o `Relatorio com Vendas e Lucros usando Data Analytics.pbix`, que contém internamente:
* **DataModel:** Esquema de dados otimizado (Star Schema).
* **Recursos Estáticos:** Imagens de fundo personalizadas e ícones de interface (`sales_icon`).
* **Visuals Customizados:** Plugins integrados como `BulletChart` e `powerKPI`.

---
*Nota: Este projeto foi desenvolvido como parte de atividade prática de Data Analytics e Business Intelligence.*