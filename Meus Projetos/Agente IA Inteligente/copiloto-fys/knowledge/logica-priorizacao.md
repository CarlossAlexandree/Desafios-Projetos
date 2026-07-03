# Lógica de Priorização de Padarias (regra local, sem IA generativa)

Pontuação de 0 a 100, somando 4 fatores:

1. **Potencial do PDV (0–40 pts)** — usa o volume de cerveja/mês como proxy de movimento/fluxo do ponto de venda: `(volume_do_pdv / maior_volume_da_base) * 40`.
2. **Facilidade de ativação (0–15 pts)** — espaço de geladeira disponível: baixo=5, médio=10, alto=15.
3. **Urgência (0–20 pts)** — tempo desde a última visita do vendedor: `min(dias_sem_visita / 120, 1) * 20`. Quanto mais tempo sem visita, maior a urgência de priorizar.
4. **Oportunidade (0–25 pts)** — se o PDV ainda não vende FYS: +25. Se já vende: +5 (oportunidade de expandir sortimento, mas menor).
5. **Bônus de demanda validada (0–5 pts)** — se o PDV já vende 2+ marcas concorrentes de refrigerante, é sinal de que a categoria vende bem ali: +5.

**Classificação final:**
- Score ≥ 70 → **Alta prioridade**
- Score 40–69 → **Média prioridade**
- Score < 40 → **Baixa prioridade**

Esse é um modelo simples e transparente de propósito — o objetivo do protótipo é mostrar a lógica de forma auditável, não otimizar precisão estatística.
