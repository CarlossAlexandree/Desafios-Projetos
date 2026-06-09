# 🤖 Agente IA Inteligente — MCP Toolbox + ADK

> Sistema de inteligência de negócios com agente de IA conversacional conectado a banco de dados PostgreSQL via Model Context Protocol (MCP).

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Banco de Dados](#-banco-de-dados)
- [Configuração do MCP Toolbox](#-configuração-do-mcp-toolbox)
- [Configuração do Agente ADK](#-configuração-do-agente-adk)
- [Ferramentas Disponíveis](#-ferramentas-disponíveis)
- [Como Executar](#-como-executar)
- [Atividades Práticas com o ADK](#-atividades-práticas-com-o-adk)

---

## 🌐 Visão Geral

Este projeto implementa um **ecossistema de inteligência de negócios** focado em **controle de inventário** e **análise de feedbacks de clientes**. O sistema permite que um agente de IA converse em linguagem natural com o usuário e consulte dados reais de um banco de dados PostgreSQL em tempo real, sem necessidade de SQL manual.

### O que o sistema faz?
- 🔍 Consulta estoque de produtos em tempo real
- 📊 Analisa métricas de vendas por canal (E-commerce, Loja Física)
- 💬 Recupera feedbacks e avaliações de clientes por produto
- 🤖 Responde perguntas de negócio em linguagem natural via chat

---

## 🏗️ Arquitetura do Projeto

O sistema é composto por **três camadas** que operam em conjunto:

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO (Navegador)                   │
│              http://127.0.0.1:8000  (ADK UI)            │
└─────────────────────┬───────────────────────────────────┘
                      │ Linguagem Natural
┌─────────────────────▼───────────────────────────────────┐
│              AGENTE IA (Google ADK)                      │
│         Agent Development Kit — agent.py                 │
│    Interpreta perguntas e aciona ferramentas MCP         │
└─────────────────────┬───────────────────────────────────┘
                      │ Chamadas de Ferramentas (MCP)
┌─────────────────────▼───────────────────────────────────┐
│           MCP TOOLBOX SERVER (toolbox.exe)               │
│       http://127.0.0.1:5000  — tools.yaml                │
│   Expõe consultas SQL como ferramentas utilizáveis       │
└─────────────────────┬───────────────────────────────────┘
                      │ Queries SQL
┌─────────────────────▼───────────────────────────────────┐
│           BANCO DE DADOS (PostgreSQL)                    │
│              localhost:5432 — banco: postgres            │
│      Tabelas: produto, venda, feedback_venda             │
└─────────────────────────────────────────────────────────┘
```

### Como as camadas se comunicam?

| Camada | Função | Porta |
|--------|--------|-------|
| 🖥️ **ADK Web UI** | Interface de chat com o agente | `8000` |
| 🔧 **MCP Toolbox** | Servidor que expõe as ferramentas SQL | `5000` |
| 🗄️ **PostgreSQL** | Banco de dados transacional | `5432` |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|-----------|--------|-----------|
| 🐍 **Python** | 3.13+ | Runtime do agente |
| 🤖 **Google ADK** | 2.2.0 | Framework do agente de IA |
| 🔧 **MCP Toolbox** | v0.30.0 | Servidor MCP para bancos de dados |
| 🧩 **MCP SDK** | Latest | Protocolo de comunicação MCP |
| 🐘 **PostgreSQL** | 15+ | Banco de dados relacional |
| 🛢️ **DBeaver** | Latest | Gerenciamento do banco |
| 📝 **YAML** | — | Configuração das ferramentas MCP |
| ⚡ **Uvicorn** | Latest | Servidor ASGI para o ADK |

---

## 📁 Estrutura de Pastas

```
AgentsV/
├── agent01/                    # Agente versão 1
├── agent02/                    # Agente versão 2
│   ├── agent.py
│   └── .env
├── agent03/                    # Agente versão 3
│   ├── agent.py
│   └── .env
├── mcp_database/               # 📌 Módulo principal MCP
│   ├── agent.py                # Agente ADK conectado ao MCP
│   ├── .env                    # Variáveis de ambiente (API keys)
│   ├── toolbox.exe             # Binário do MCP Toolbox v0.30.0
│   ├── tools.yaml              # Configuração das fontes e ferramentas
│   ├── 01-sources.yaml         # (Referência) Configuração de fontes
│   ├── 02-tools.yaml           # (Referência) Configuração de ferramentas
│   ├── 03-toolsets.yaml        # (Referência) Configuração de toolsets
│   └── __init__.py             # Inicializador do módulo Python
├── main.py                     # Entry point global
└── system_check.py             # Verificação global do sistema
```

---

## 🗄️ Banco de Dados

O banco `postgres` (servidor local `localhost:5432`) contém **3 tabelas transacionais**:

### 📦 Tabela `produto`
Armazena o catálogo de produtos com controle de estoque.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_produto` | SERIAL PK | Identificador único |
| `nome` | VARCHAR(100) | Nome do produto |
| `categoria` | VARCHAR(50) | Categoria (Bebida, Alimento...) |
| `preco` | DECIMAL(10,2) | Preço unitário |
| `status_active` | BOOLEAN | Produto ativo/inativo |
| `total_stock` | INT | Quantidade em estoque |
| `created_at` | TIMESTAMP | Data de cadastro |

### 🛒 Tabela `venda`
Registra todas as transações de venda realizadas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_venda` | SERIAL PK | Identificador único |
| `id_produto` | INT FK | Referência ao produto |
| `data_venda` | TIMESTAMP | Data da venda |
| `quantidade` | INT | Quantidade vendida |
| `valor_unitario` | DECIMAL(10,2) | Valor na data da venda |
| `canal_venda` | VARCHAR(50) | `E-commerce` ou `Loja Física` |
| `cliente_id` | VARCHAR(50) | Identificador do cliente |

### ⭐ Tabela `feedback_venda`
Armazena avaliações e comentários dos clientes.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_feedback` | SERIAL PK | Identificador único |
| `id_venda` | INT FK | Referência à venda |
| `id_cliente` | VARCHAR(10) | Identificador do cliente |
| `rating` | INT | Nota de 1 a 5 |
| `comentario` | TEXT | Comentário livre |
| `criado_em` | TIMESTAMP | Data do feedback |

### 📊 Dados de Exemplo Carregados

**Produtos:**
- ☕ Café Especial 250g — R$ 29,90 — 120 un.
- 🍺 Cerveja Artesanal IPA 500ml — R$ 18,50 — 200 un.
- 🍵 Chá Verde Orgânico 200g — R$ 22,00 — 80 un.
- 🍊 Suco Natural de Laranja 1L — R$ 9,90 — 150 un.
- 💪 Barra de Proteína 60g — R$ 8,50 — 300 un.

---

## ⚙️ Configuração do MCP Toolbox

O arquivo `tools.yaml` usa o **formato v2** (compatível com MCP Toolbox v0.30.0+), com documentos separados por `---`.

> ⚠️ **Atenção:** Versões anteriores ao v0.30.0 usam um formato diferente (v1) e não são compatíveis com esta configuração.

### Estrutura do `tools.yaml`

```yaml
# 1️⃣ Fonte de dados
kind: sources
name: postgres-local
type: postgres
host: 127.0.0.1
port: 5432
database: postgres
user: postgres
password: sua_senha
---
# 2️⃣ Ferramenta (exemplo)
kind: tools
name: search-all-products-inventory
type: postgres-sql
source: postgres-local
description: "Busca produtos no estoque pelo nome."
parameters:
  - name: search_term
    type: string
statement: |
  SELECT nome, categoria, preco, total_stock 
  FROM produto 
  WHERE nome ILIKE '%' || $1 || '%';
---
# 3️⃣ Toolset
kind: toolsets
name: metricas_corporativas
tools:
  - search-all-products-inventory
  - get-sales-metrics-by-channel
  - get-product-customer-feedback
```

> 💡 **Nota:** Os parâmetros SQL usam `$1`, `$2` (positional) — não `:nome_param` (named). O campo `database:` do source deve conter o nome real do banco retornado por `SELECT current_database();` no DBeaver.

---

## 🤖 Configuração do Agente ADK

### Dependências necessárias

```bash
pip install google-adk
pip install mcp
pip install python-dotenv
```

> ⚠️ O pacote `mcp` é obrigatório — sem ele o `MCPToolset` falha silenciosamente sem mensagem de erro clara.

### Estrutura do `agent.py`

```python
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:5000/sse")

root_agent = Agent(
    name="mcp_database",
    model="gemini-2.0-flash",
    instruction="""Você é um auditor sênior de inteligência de negócios.
    Responda sempre em português do Brasil.
    Use as ferramentas disponíveis para consultar dados reais do banco de dados.
    Nunca invente dados — consulte sempre o banco antes de responder.""",
    tools=[
        MCPToolset(
            connection_params=SseConnectionParams(
                url=MCP_SERVER_URL
            )
        )
    ]
)
```

> ⚠️ **Import crítico:** No ADK 2.2.0 o nome correto é `SseConnectionParams` — não `SseServerParams`. Usar o nome errado causa erro silencioso sem resposta no chat.

### Estrutura do `.env`

```env
GOOGLE_API_KEY=sua_chave_aqui
MCP_SERVER_URL=http://127.0.0.1:5000/sse
```

> 🔑 Obtenha sua chave gratuita em: https://aistudio.google.com/apikey
> ⚠️ **Nunca versione o arquivo `.env` no GitHub.** Adicione-o ao `.gitignore`.

---

## 🔧 Ferramentas Disponíveis

O sistema expõe **3 ferramentas** via MCP que o agente utiliza automaticamente:

### 🔍 `search-all-products-inventory`
- **O que faz:** Busca produtos no estoque pelo nome
- **Parâmetro:** `search_term` — nome ou termo do produto
- **Retorna:** Nome, categoria, preço e quantidade em estoque

### 📈 `get-sales-metrics-by-channel`
- **O que faz:** Calcula total vendido e receita por produto e canal
- **Parâmetros:** `product_name` + `channel` (E-commerce / Loja Física)
- **Retorna:** Total de unidades vendidas e receita gerada

### 💬 `get-product-customer-feedback`
- **O que faz:** Recupera avaliações e comentários de clientes
- **Parâmetro:** `product_name` — nome do produto
- **Retorna:** Rating (1-5) e comentário de cada cliente

---

## ▶️ Como Executar

### Pré-requisitos
- ✅ PostgreSQL rodando na porta `5432`
- ✅ Python 3.13+ instalado
- ✅ Pacotes instalados: `pip install google-adk mcp python-dotenv`
- ✅ `toolbox.exe` v0.30.0 na pasta `mcp_database`
- ✅ Chave `GOOGLE_API_KEY` configurada no `.env`

### Passo a Passo

**Terminal 1 — Iniciar o MCP Toolbox:**
```powershell
cd "caminho\para\AgentsV\mcp_database"
.\toolbox.exe --tools-file tools.yaml --ui
```
> ✅ Aguarde: `Server ready to serve!` e `Toolbox UI is up and running at: http://127.0.0.1:5000/ui`

**Terminal 2 — Iniciar o Agente ADK:**
```powershell
cd "caminho\para\AgentsV"
adk web
```
> ✅ Aguarde: `ADK Web Server started` e `Uvicorn running on http://127.0.0.1:8000`

**Acessar as interfaces:**

| Interface | URL | Finalidade |
|-----------|-----|-----------|
| 💬 ADK Chat | http://127.0.0.1:8000 | Chat com o agente |
| 🔧 MCP Dev UI | http://127.0.0.1:5000/ui | Teste direto das ferramentas |

> ⚠️ **Importante:** Os dois terminais devem permanecer abertos simultaneamente. Fechar qualquer um derruba o sistema.

---

## 🎯 Atividades Práticas com o ADK

Acesse **http://127.0.0.1:8000**, selecione o agente `mcp_database` e teste as interações abaixo:

---

### 🧪 Atividade 1 — Consulta de Estoque em Tempo Real

**Objetivo:** Verificar como o agente consulta o banco e retorna dados de inventário em linguagem natural.

**Perguntas para digitar no chat:**

```
Oi, quantas cervejas ainda temos em estoque?
```
```
Quais produtos da categoria Bebida estão disponíveis e qual o preço de cada um?
```
```
Temos algum produto com "proteína" no nome? Qual a quantidade em estoque?
```

**O que observar:**
- 👁️ No painel **Trace** (lateral esquerda), veja a ferramenta `search-all-products-inventory` sendo acionada automaticamente
- 👁️ O agente interpreta a pergunta, identifica o termo de busca e executa a query SQL
- 👁️ A resposta vem formatada em linguagem natural, não como tabela SQL crua

---

### 🧪 Atividade 2 — Análise de Métricas de Vendas por Canal

**Objetivo:** Demonstrar como o agente cruza dados de vendas e calcula métricas de negócio.

**Perguntas para digitar no chat:**

```
Quanto a cerveja artesanal vendeu no E-commerce? Me dá o total de unidades e a receita gerada.
```
```
Qual foi a receita total do café especial nas vendas pelo E-commerce?
```
```
Compare as vendas da cerveja entre E-commerce e Loja Física.
```

**O que observar:**
- 👁️ O agente aciona `get-sales-metrics-by-channel` com dois parâmetros: produto + canal
- 👁️ Para a pergunta de comparação, o agente faz **duas chamadas** à ferramenta automaticamente (uma para cada canal)
- 👁️ Observe no **Trace** como o agente raciocina antes de responder

---

### 🧪 Atividade 3 — Análise de Satisfação de Clientes

**Objetivo:** Mostrar como o agente recupera feedbacks qualitativos e os interpreta para o negócio.

**Perguntas para digitar no chat:**

```
O que os clientes estão achando da cerveja artesanal? Tem algum comentário?
```
```
Qual a avaliação dos clientes sobre o café especial? A nota foi boa?
```
```
Com base nos feedbacks disponíveis, qual produto tem a melhor avaliação dos clientes?
```

**O que observar:**
- 👁️ O agente usa `get-product-customer-feedback` para buscar ratings e comentários
- 👁️ Na última pergunta, o agente consulta **múltiplos produtos** e faz uma análise comparativa
- 👁️ Perceba como o agente vai além dos dados brutos — ele interpreta e dá uma **conclusão de negócio**

---

## 📌 Observações Importantes

- 🔐 **Segurança:** Nunca versione o `.env` no GitHub. Adicione-o ao `.gitignore`
- 🔐 **Produção:** Nunca deixe senhas expostas no `tools.yaml`. Use variáveis de ambiente com `${NOME_VAR}`
- 🔄 **Reload automático:** O MCP Toolbox v0.30.0 recarrega o `tools.yaml` automaticamente ao salvar alterações
- 🪟 **Windows:** O ADK exibe um aviso sobre `--reload` — isso é esperado e não afeta o funcionamento
- 📡 **MCP Protocol:** O toolbox expõe as ferramentas via protocolo MCP padrão, compatível com qualquer cliente MCP
- ⏱️ **Cota gratuita:** O Gemini free tier permite 15 req/min e 1.500 req/dia. Se receber erro `429 RESOURCE_EXHAUSTED`, aguarde 1 minuto e tente novamente

---

## 🐛 Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `unknown tool kind` | Versão errada do toolbox | Baixe o v0.30.0 |
| `ModuleNotFoundError: No module named 'mcp'` | Pacote mcp não instalado | `pip install mcp` |
| `cannot import name 'SseServerParams'` | Nome errado no ADK 2.2.0 | Use `SseConnectionParams` |
| `Invalid agent name: 'mcp-database'` | Hífen no nome da pasta | Renomeie para `mcp_database` |
| `429 RESOURCE_EXHAUSTED` | Cota da API esgotada | Aguarde 1 minuto |
| `FATAL: banco de dados não existe` | Nome do banco errado | Confirme com `SELECT current_database()` |

---

## 👨‍💻 Desenvolvido durante

> 📚 **DIO — Curso: Agente IA Inteligente**  
> Módulo: Implementação de MCP com banco de dados PostgreSQL e Google ADK