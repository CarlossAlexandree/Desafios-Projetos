# 🎯 Análise de Feedbacks de Atendimento Bancário

---

## 📌 Visão Geral

| Item | Detalhe |
|---|---|
| 🎯 Foco da análise | Atendimento humano vs. Chatbot |
| 👥 Público-alvo do resultado | Diretoria Executiva |
| 🔍 Objetivo principal | Identificar gargalos que elevam o custo operacional |
| 🗣️ Tom do prompt | Consultivo com recomendações estratégicas |
| 🤖 IA utilizada | Claude (Anthropic) |
| 🌐 Linguagem | Português (BR) |

---

## 📌 Objetivo

> O objetivo é construir, passo a passo, um prompt estruturado capaz de orientar uma IA a extrair insights estratégicos a partir de feedbacks de clientes bancários.

---

## ✅ Prompt Completo

- Atue como consultor estratégico especializado em eficiência operacional bancária.

Sua tarefa é analisar feedbacks de clientes sobre atendimento humano e chatbot para identificar gargalos operacionais, pontos de fricção e motivos recorrentes de insatisfação que elevam o custo de atendimento.

**Contexto:** Os feedbacks foram coletados nos canais de atendimento de um banco digital, cobrindo interações realizadas via chatbot automatizado e atendentes humanos. A análise será apresentada à Diretoria Executiva como insumo para decisões estratégicas sobre alocação de recursos e redesenho dos canais de atendimento. O foco principal é transformar comentários brutos em diagnósticos claros que evidenciem onde estão as ineficiências com maior impacto no custo operacional.

**Dados disponíveis:** A base de feedbacks contém os seguintes campos:
- Canal de atendimento (humano ou chatbot)
- Nota de satisfação (escala de 1 a 5)
- Texto do comentário do cliente
- Tempo de resolução do atendimento
- Motivo do contato
- Data do atendimento

**Instruções de análise:**
1. Classifique os feedbacks por canal, sentimento (positivo, neutro, negativo), urgência e impacto operacional estimado.
2. Identifique padrões recorrentes que indiquem ineficiência, retrabalho ou falhas sistêmicas em cada canal.
3. Compare o desempenho entre chatbot e atendimento humano considerando satisfação, tempo de resolução e motivos de contato.
4. Aponte evidências diretas nos dados fornecidos, utilizando trechos curtos dos comentários como suporte.
5. Sugira recomendações estratégicas priorizadas para a Diretoria Executiva, com foco em redução de custo e melhoria de eficiência operacional.

**Formato da resposta:**
- **Diagnóstico executivo:** parágrafos curtos (máximo 3 parágrafos) com os principais achados por canal.
- **Matriz de priorização:** tabela com os gargalos identificados, classificados por urgência (alta/média/baixa) e impacto operacional estimado (alto/médio/baixo).
- **Recomendações estratégicas:** lista com as 3 principais ações sugeridas, cada uma acompanhada de justificativa baseada nos dados analisados.

**Restrições:**
- Use apenas os dados fornecidos. Não invente números, métricas ou conclusões.
- Não exponha dados pessoais ou informações sensíveis dos clientes.
- Caso os dados sejam insuficientes para alguma conclusão, indique explicitamente a limitação.
- Use linguagem consultiva, direta e adequada para apresentação à liderança executiva.

---

## 📊 Resultados Esperados com o Prompt

Ao aplicar o prompt final em uma IA com uma base de feedbacks real, o output será estruturado em três entregas objetivas e diretamente acionáveis pela Diretoria Executiva.

---

### 1️⃣ Diagnóstico Executivo

Três parágrafos curtos e diretos, contendo:

| Parágrafo | Conteúdo |
|---|---|
| **Panorama geral** | Sentimento predominante dos clientes nos dois canais (chatbot e humano) |
| **Chatbot** | Principais problemas identificados — ex: falhas de compreensão, loops sem resolução, baixa taxa de conclusão |
| **Atendimento humano** | Principais problemas identificados — ex: tempo de espera elevado, inconsistência nas respostas, retrabalho |

---

### 2️⃣ Matriz de Priorização

Tabela comparativa com os gargalos encontrados, classificados por urgência e impacto operacional — permitindo à Diretoria visualizar prioridades de forma rápida, sem precisar interpretar os comentários brutos.

| Gargalo Identificado | Canal | Urgência | Impacto Operacional |
|---|---|---|---|
| Chatbot não resolve dúvidas sobre bloqueio de conta | Chatbot | 🔴 Alta | 🔴 Alto |
| Atendentes repetem perguntas já respondidas no chat | Humano | 🟡 Média | 🟡 Médio |

> **Nota:** Os gargalos reais serão preenchidos pela IA com base nos feedbacks fornecidos. Os exemplos acima são ilustrativos.

---

### 3️⃣ Recomendações Estratégicas

Lista com as **3 ações prioritárias**, cada uma acompanhada de justificativa baseada nos dados analisados:

**Ação 1 — Redesenhar os fluxos do chatbot**
> Focar nos 3 motivos de contato mais frequentes que não chegam à resolução automatizada, reduzindo o volume de escaladas para o atendimento humano e o custo operacional associado.

**Ação 2 — Criar protocolo de continuidade entre chatbot e atendente**
> Clientes relatam precisar repetir informações ao ser transferidos, gerando retrabalho e insatisfação. Um protocolo de handoff com histórico compartilhado eliminaria esse atrito.

**Ação 3 — Revisar o SLA de tempo de resolução no atendimento humano**
> Feedbacks com notas 1 e 2 concentram-se em atendimentos com tempo de resolução acima do padrão, indicando que o prazo atual não está sendo cumprido ou é inadequado para determinados motivos de contato.

---

### 🎯 Síntese do Output

> O prompt foi desenhado para entregar exatamente o que a Diretoria Executiva precisa: **clareza, evidência e direção** — sem ruído, sem dados sensíveis e sem especulação.  
> O output funciona tanto como **insumo para reunião estratégica** quanto como **base para um plano de ação operacional**.

---

## 💡 Aprendizados do Desafio

| Princípio | Aplicação prática |
|---|---|
| **Intenção clara** | Definir quem usa o resultado e para qual decisão elimina ambiguidade |
| **Contexto e restrições** | Evitam alucinações e garantem respostas seguras e éticas |
| **Papel da IA** | Atribuir um papel específico melhora o tom e a profundidade da resposta |
| **Formato definido** | Especificar a estrutura da entrega aumenta a utilidade do output |
| **Critério de qualidade** | Dizer o que torna o resultado "bom" orienta a IA para o que realmente importa |

---

## 🛠️ Tecnologias e Ferramentas

- **Método:** Prompt Engineering estruturado em 3 passos progressivos
- **Linguagem:** Português (BR)
- **Versionamento:** Git / GitHub

---

## 👤 Autor

**Carlos Alexandre**

---


```
* ⭐Prompt desenvolvido com o objetivo de Extrair Insights de Feedback de Clientes Bancários*
```