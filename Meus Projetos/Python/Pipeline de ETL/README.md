# Pipeline de ETL para Engajamento de Clientes Bancários com IA

Projeto desenvolvido com foco na implementação prática de um fluxo de ETL (Extract, Transform, Load) utilizando Python, integração com APIs REST e geração de conteúdo dinâmico por IA Generativa através da Google Gemini API.

O objetivo principal do projeto é demonstrar como pipelines de dados podem ser utilizados para automatizar processos de enriquecimento de informações, personalização de conteúdo e atualização de sistemas externos de forma estruturada e escalável.

---

# Visão Geral

O pipeline realiza três etapas principais:

1. **Extract (Extração)**  
   Leitura de dados de usuários a partir de um arquivo CSV e consumo de uma API REST local simulada.

2. **Transform (Transformação)**  
   Utilização de IA Generativa para criar mensagens personalizadas sobre investimentos para cada usuário.

3. **Load (Carregamento)**  
   Atualização da base de dados simulada através de requisições HTTP PUT.

---

# Objetivo do Projeto

Este projeto foi construído para simular um cenário comum em ambientes corporativos:

- Coleta de dados de clientes;
- Processamento automatizado de informações;
- Enriquecimento com Inteligência Artificial;
- Atualização de sistemas internos;
- Integração entre arquivos, APIs e modelos generativos.

Embora o ambiente utilizado seja o Google Colab, a arquitetura do fluxo reproduz conceitos utilizados diariamente em áreas como:

- Engenharia de Dados;
- Analytics Engineering;
- Automação de Processos;
- DataOps;
- Plataformas de CRM;
- Sistemas bancários e financeiros;
- Plataformas de recomendação e personalização.

---

# 🏗️ Arquitetura do Pipeline

```text
[ Arquivo CSV ]           [ Google AI Studio ]          [ API de CRM ]
        │                            │                          ▲
        ▼                            ▼                          │
┌───────────────┐            ┌───────────────┐          ┌───────────────┐
│    EXTRACT    │ ────────>  │   TRANSFORM   │ ──────>  │     LOAD      │
└───────────────┘            └───────────────┘          └───────────────┘
 Leitura de IDs e             Geração de Mensagens       Persistência e 
 Busca de Perfis              Hiper-Personalizadas       Atualização da Base
```

Fluxo detalhado:

```text
SDW2026.csv
      ↓
Leitura com Pandas
      ↓
Requisição GET na API local
      ↓
Estruturação dos dados em memória
      ↓
Geração de mensagens personalizadas com Gemini
      ↓
Atualização do usuário via PUT
      ↓
Persistência no db.json
```

---

# Tecnologias Utilizadas

## Linguagem

- Python 3

## Bibliotecas

- pandas
- requests
- subprocess
- json
- google-genai

## Ambiente

- Google Colab
- json-server
- API REST local simulada

## IA Generativa

- Google Gemini API (`gemini-2.5-flash`)

---

# Estrutura do Projeto

```text
.
├── Pipeline_de_ETL_com_Python
├── SDW2026.csv
├── db.json
└── README.md
```

---

# Etapa 1 — Extract (Extração)

A fase de extração é responsável por obter os dados que serão processados ao longo do pipeline.

## Fonte de Dados

Os IDs dos usuários são armazenados em um arquivo CSV:

```csv
UserID:
11
12
13
14
15
16
```

O pipeline utiliza o Pandas para realizar a leitura do arquivo:

```python
df = pd.read_csv('SDW2026.csv')
user_ids = df['UserID:'].tolist()
```

Após a leitura, o sistema realiza requisições GET na API local para buscar os dados completos dos usuários.

```python
response = requests.get(f'{sdw2023_api_url}/users/{id}')
```

---

# API REST Simulada

Para simular um ambiente real de backend, foi utilizado o `json-server`, que transforma o arquivo `db.json` em uma API REST funcional.

## Exemplo de estrutura do usuário

```json
{
  "id": 11,
  "name": "Marina Albuquerque",
  "account": {
    "number": "45872-1",
    "agency": "1021",
    "balance": 8450.75
  }
}
```

Esse tipo de abordagem é amplamente utilizado em:

- testes locais;
- validação de integrações;
- prototipação de APIs;
- ambientes de desenvolvimento;
- simulação de microsserviços.

---

# Etapa 2 — Transform (Transformação)

A fase de transformação representa o núcleo do pipeline.

Nesta etapa, os dados extraídos são enriquecidos com IA Generativa para produzir mensagens personalizadas.

## Integração com Google Gemini API

Ao invés da OpenAI API originalmente utilizada no laboratório base, o projeto foi adaptado para utilizar a Google Gemini API.

Essa alteração permitiu:

- integração com o ecossistema Google AI;
- uso do SDK oficial `google-genai`;
- geração de conteúdo com baixo custo operacional;
- testes locais mais acessíveis;
- flexibilidade para prototipação rápida.

## Inicialização do Cliente

```python
from google import genai

client = genai.Client(api_key=gemini_api_key)
```

## Geração das mensagens

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos"
)
```

## Resultado esperado

```text
1. Mensagem gerada para Marina Albuquerque: Marina, invista no seu futuro! Faça seu dinheiro trabalhar por você e multiplique suas conquistas.

2. Mensagem gerada para Ricardo Menezes: Ricardo, invista no seu futuro! Faça seu dinheiro crescer e realize seus sonhos. É o momento!

3. Mensagem gerada para Fernanda Costa: Fernanda, invista! Seu futuro merece crescer e seus sonhos se realizarem. Comece a construir hoje.

4. Mensagem gerada para Lucas Andrade: Lucas, não deixe seu dinheiro parado! Invista agora e construa o futuro financeiro que você merece.
```

---

# 📈 Uso da IA Generativa em Cenários Reais

Utilizando modelos generativos em pipelines de ETL em aplicações corporativas.

Exemplos práticos:

- Personalização de campanhas;
- Geração automática de insights;
- Classificação textual;
- Sumarização de documentos;
- Automação de atendimento;
- Geração de descrições de produtos;
- Enriquecimento de CRM;
- Automação de comunicação bancária.

A etapa de transformação deixa de ser apenas manipulação de dados estruturados e passa a incorporar processamento semântico e contextual.

---

# Etapa 3 — Load (Carregamento)

Após a geração das mensagens, os dados são enviados novamente para a API através de requisições PUT.

```python
response = requests.put(
    f'{sdw2023_api_url}/users/{user["id"]}',
    json=user
)
```

O pipeline atualiza dinamicamente o campo `news` de cada usuário.

## Exemplo

```json
"news": [
  {
    "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
    "description": "Invista hoje para construir estabilidade financeira no futuro."
  }
]
```

---

# Aplicações no Mercado

Pipelines ETL como este são utilizados diariamente em empresas para:

- automação de dados financeiros;
- integração entre sistemas;
- campanhas de marketing personalizadas;
- atualização de CRMs;
- processamento de APIs;
- análise de comportamento de clientes;
- motores de recomendação;
- automação operacional.

Em ambientes de produção, esse mesmo fluxo normalmente é integrado com:

- bancos de dados SQL e NoSQL;
- mensageria (Kafka/RabbitMQ);
- orquestração com Airflow;
- containers Docker;
- serviços em nuvem;
- pipelines CI/CD.

---

# Principais Conceitos Trabalhados

- ETL
- APIs REST
- Manipulação de JSON
- Processamento de dados com Pandas
- Requisições HTTP
- Integração com IA Generativa
- Estruturação de pipelines
- Automação de processos
- Simulação de ambiente backend
- Integração entre serviços

---

# Possíveis Evoluções

O projeto pode ser expandido para incluir:

- banco de dados PostgreSQL;
- autenticação JWT;
- logs estruturados;
- tratamento avançado de erros;
- processamento assíncrono;
- orquestração com Airflow;
- deploy em cloud;
- filas de mensageria;
- dashboards analíticos;
- monitoramento de pipelines.

---

# Execução do Projeto

## Instalação das dependências

```bash
pip install google-genai pandas requests
npm install -g json-server
```

## Execução
```
1. Iniciar o notebook
2. Executar o mock da API
3. Ler o CSV
4. Processar os usuários
5. Gerar mensagens com Gemini
6. Atualizar os dados via API
```
---

# Considerações Finais

Este projeto demonstra como pipelines ETL podem ir além da simples movimentação de dados, incorporando Inteligência Artificial como etapa estratégica de transformação.

A integração entre Python, APIs REST e modelos generativos amplia significativamente as possibilidades de automação, personalização e enriquecimento de dados em aplicações modernas.

Mesmo em um ambiente simplificado, a estrutura utilizada reproduz conceitos presentes em pipelines utilizados em produção em empresas de tecnologia, bancos, fintechs e plataformas digitais.