# 📊 Power BI: Análise de Sensibilidade e Parâmetros Dinâmicos

Este repositório foca na implementação de **What-if Analysis** (Análise de Cenários) e **Parâmetros de Campo**, permitindo que o usuário final interaja com os dados de forma preditiva e personalizada.

## 🚀 Funcionalidades Implementadas

### 1. Parâmetro de Cenário (What-if Analysis)
Criamos um parâmetro numérico de **Ajuste de Custo %** para simular o impacto de variações operacionais no lucro final.
- **Lógica:** O usuário pode ajustar o custo (COGS) em uma escala de -50% a +50%.
- **Objetivo:** Identificar o ponto de equilíbrio (*break-even*) de cada segmento de mercado perante inflação ou aumento de insumos.

### 2. Parâmetros de Campo (Field Parameters)
Implementação de seletores dinâmicos que permitem alternar as dimensões dos gráficos (Country, Month, Product, Segment, Semestres) sem a necessidade de múltiplos visuais, otimizando a performance do relatório.

## 🛠️ Detalhes Técnicos

### Medida DAX: Lucro Simulado
A principal inteligência deste módulo reside na medida DAX abaixo, que calcula o lucro em tempo real com base na entrada do usuário via segmentador:

```dax
Profit Simulado = 
SUM(financials[Sales]) - (SUM(financials[COGS]) * (1 + [Valor Ajuste de Custo %]))