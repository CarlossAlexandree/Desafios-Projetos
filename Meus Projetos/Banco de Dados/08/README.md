# 📊 Relatório de Vendas — Power BI

## 🧠 Visão Geral
Este projeto apresenta um **dashboard de análise de vendas**, desenvolvido no **Power BI**, com foco em **boas práticas de modelagem, visualização de dados e storytelling analítico**.

O relatório foi construído com o objetivo de demonstrar **maturidade profissional** para atuação como **Analista de Dados (nível Pleno)**, seguindo padrões comuns em ambientes corporativos e BigTechs.

---

## 🎯 Objetivo do Projeto
- Analisar **desempenho de vendas e lucro** em diferentes países  
- Identificar **regiões mais rentáveis**  
- Avaliar a **participação de lucro por segmento**  
- Comunicar insights de forma clara para **stakeholders não técnicos**

---

## 📌 Principais Indicadores (KPIs)
- 💰 **Total de Vendas**
- 📦 **Total de Unidades Vendidas**
- 📈 **Lucro Total**
- 🌍 **Distribuição Geográfica de Vendas e Lucro**
- 🧩 **Participação de Lucro por Segmento**

---

## 🗺️ Estrutura do Relatório
O relatório é composto por **3 páginas principais**:

### 1️⃣ Visão Geral
- Indicadores principais
- Análise consolidada de vendas e lucro

### 2️⃣ Análise Temporal
- Evolução das métricas ao longo do tempo
- Comparação entre períodos

### 3️⃣ Análise Geográfica e Segmentação
- 🗺️ **Mapa:** Distribuição de Vendas e Unidades por País  
- 🗺️ **Mapa:** Lucro Total por País  
- 🥧 **Gráfico de Pizza:** Participação de Lucro por Segmento  

Essa organização permite uma leitura **progressiva e executiva** dos dados.

---

## 🎨 Design e Storytelling
- 🎯 Tema visual corporativo
- 🔵 Azul escuro como cor primária
- ⚪ Cinza neutro para apoio visual
- 🟣 Roxo utilizado como destaque para **Lucro**
- 📌 Títulos claros e orientados ao negócio
- 🧠 Tooltips estratégicos para contexto adicional

O foco do design é **clareza, consistência e tomada de decisão**, evitando excesso de elementos visuais.

---

## 🧮 Modelagem e DAX
Foram utilizadas **medidas DAX** para garantir boas práticas analíticas:

```DAX
Total Vendas = SUM ( Fato_Vendas[Sales] )

Total Unidades = SUM ( Fato_Vendas[Units Sold] )

Lucro Total = SUM ( Fato_Vendas[Profit] )

