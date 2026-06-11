# Processamento de Dados Simplificado com Power BI
## Desafio de Projeto: Modelagem Star Schema e Inteligência de Tempo com DAX

### 📝 Descrição do Projeto
Este repositório contém a resolução do desafio de modelagem dimensional, onde uma base de dados flat (`Financial Sample`) foi transformada em um modelo **Star Schema**. A reestruturação visa otimizar a performance analítica e organizar os dados em tabelas de Fato e Dimensões.

### 🛠️ Etapas do Desenvolvimento

#### 1. Extração e Transformação (ETL)
As tabelas foram derivadas da base original para isolar os contextos de análise:
* **financials_origem**: Cópia fiel da base, mantida como backup e oculta no modelo.
* **D_Produtos**: Tabela agrupada para fornecer métricas estatísticas (médias, mediana, máximo e mínimo) por produto.
* **D_Produtos_Detalhes**: Contém informações específicas de preços (venda/manufatura) e unidades vendidas.
* **D_Descontos**: Focada na gestão de bandas de desconto e valores.
* **D_Detalhes**: Agrupa informações de contexto como Segmento e País.
* **D_Categoria**: Tabela de dimensão para classificação dos produtos.
* **F_Vendas**: Tabela Fato central que armazena os dados transacionais e as chaves estrangeiras.

#### 2. Criação de Chaves (Surrogate Keys)
* **ID_Produto**: Criado via **Coluna Condicional** no Power Query para converter os nomes dos produtos em chaves numéricas únicas.
* **SK_ID**: Coluna de índice adicionada à tabela Fato para garantir a unicidade dos registros.

#### 3. Inteligência de Tempo com DAX
Foi criada a tabela **D_Calendario** utilizando a linguagem DAX para permitir filtros temporais robustos e cálculos de *Time Intelligence*:
```dax
D_Calendario = CALENDAR(MIN(F_Vendas[Date]), MAX(F_Vendas[Date]))