# 🚀 Fraud Detection API

Este projeto implementa uma **API de Detecção de Fraudes Bancárias** utilizando **FastAPI** e **Uvicorn**, com suporte a **predição de fraudes**, **KPIs gerenciais** e um **dashboard visual em HTML** para apresentação a stakeholders.

---

## 📌 Objetivos do Projeto
- Detectar **anomalias em transações bancárias**.
- Fornecer **predições de fraude** em tempo real via API.
- Expor **KPIs gerenciais** para acompanhamento de risco.
- Criar um **dashboard visual** com gráficos e métricas para apresentação executiva.

---

## 🏗️ Estrutura do Projeto

```
banking-fraud-detection/
├── app/
│   ├── api/
│   │   ├── main.py              # Arquivo principal da API
│   │   └── routes/
│   │       ├── predict.py       # Endpoint de predição
│   │       ├── kpi.py           # Endpoint de KPIs
│   │       ├── dashboard.py     # Geração de gráficos (PNG)
│   │       └── dashboard_html.py# Dashboard HTML com KPIs + gráficos
│   ├── utils/
│   │   └── metrics.py           # Funções de cálculo de métricas
│   └── data/
│       ├── raw/                 # Dataset original
│       └── processed/dashboard/ # Gráficos gerados
└── venv/                        # Ambiente virtual Python
```

---

## Endpoints Disponíveis

### 1. Predição de Fraude

Endpoint: /predict

Método: POST

Descrição: Recebe dados de transação em JSON e retorna se é fraude ou não.

Exemplo de requisição:

```
{
  "transaction_amount": 20000,
  "login_attempts": 6,
  "device_risk_score": 0.8,
  "transfer_frequency": 3,
  "anomaly_score": 0.5,
  "account_age_days": 120,
  "transaction_time_hour": 14,
  "failed_transactions_last_30d": 12,
  "avg_monthly_balance": 5000,
  "daily_transaction_count": 15,
  "geo_distance_km": 50,
  "session_duration_minutes": 30,
  "transaction_velocity_score": 0.7,
  "payment_channel": "online",
  "authentication_type": "password",
  "card_present_flag": 0,
  "international_transaction_flag": 1,
  "suspicious_ip_flag": 1
}
```

---

### 2. KPIs Gerenciais

- Endpoint: /kpi

- Método: GET

- Descrição: Retorna métricas globais de fraude.

Exemplo de resposta:

```
{
  "fraud_rate": 0.12,
  "high_risk_transactions": 340,
  "total_transactions": 10000
}
```
---

### 3. Dashboard Gráfico

- Endpoint: /dashboard

- Método: GET

- Descrição: Gera gráficos em PNG e salva em app/data/processed/dashboard.

---

### 3.1 Gráficos disponíveis:

- Distribuição de fraudes:
```
 /static/dashboard/fraud_distribution.png
```
- Fraudes por canal:
```
/static/dashboard/fraud_by_channel.png
```
- Fraudes por horário:
```
 /static/dashboard/fraud_by_hour.png
```
---

### 4. Dashboard HTML Executivo

- Endpoint: /dashboard/html

- Método: GET

- Descrição: Exibe uma página HTML com KPIs numéricos + gráficos visuais em um único lugar.


Exemplo de visualização:

```
http://127.0.0.1:8000/dashboard/html
```
---

## 🎯 Finalidade do Projeto

Este projeto foi desenvolvido para:

- Analisar transações bancárias e identificar possíveis fraudes.

- Fornecer insights gerenciais através de KPIs.

- Apresentar resultados visuais em dashboards para stakeholders.

- Servir como base para integração com sistemas de monitoramento e ferramentas de BI.


## ⚙️ Instalação e Execução

### 1. Clonar o repositório

```Bash
git clone https://github.com/CarlossAlexandree/Desafios-Projetos.git
```

### 2. Criar ambiente virtual
```
python -m venv venv
```
### 3. Ativar ambiente virtual
```
.\venv\Scripts\Activate.ps1
```
### 4. Instalar dependências
```
pip install -r requirements.txt
```
### 5. Rodar o servidor FastAPI
```
uvicorn app.api.main:app --reload
```
### 6. Acessar a API
```
http://127.0.0.1:8000/docs
```