# 🛵 Assistente de Delivery — AWS Step Functions + IA Gratuita (Hugging Face)

Assistente inteligente para um app de delivery que orquestra todo o ciclo de vida
de um pedido (recebido → validado → notificado → entregue) usando **AWS Step
Functions**, e usa **IA gratuita (Hugging Face Inference API)** para analisar o
sentimento do feedback dos clientes e alertar a administração quando algo vai mal.

> **Nota sobre IA:** o projeto original previa o Amazon Bedrock, mas o Bedrock
> não tem nível gratuito perene (cobra por token). Para manter o projeto 100%
> dentro do free tier, a análise de sentimento foi implementada com a
> **Hugging Face Inference API** (gratuita, com limite de requisições), usando
> o modelo multilíngue `cardiffnlp/twitter-xlm-roberta-base-sentiment`. Trocar
> por Bedrock no futuro exige apenas reescrever a Lambda
> `analisar_sentimento_hf.py` — o restante da arquitetura não muda.

---

## 📐 Visão Geral do Projeto

**Objetivo:** dar a um app de delivery um "cérebro" de orquestração que:
- Recebe pedidos via API REST.
- Valida e persiste pedidos no DynamoDB.
- Notifica cliente e restaurante em cada mudança de status.
- Analisa o sentimento do feedback do cliente e alerta a administração
  automaticamente quando o feedback é negativo.
- Escala horizontalmente sem servidores para gerenciar (100% serverless).

**Arquitetura (visão geral):**

```
Usuário → API Gateway → Lambda → Step Functions (Pedido)
                                       ├─ Lambda (validação) → DynamoDB
                                       ├─ SNS (notifica restaurante)
                                       └─ SQS (status)

Step Functions (Notificações): Lambda → SNS (push cliente)

Step Functions (IA): Lambda (captura feedback)
                        → Lambda (Hugging Face - sentimento)
                        → DynamoDB (registra)
                        → Choice (bom/ruim) → SNS (alerta admin)
```

Diagramas completos (incluindo versão Mermaid) estão em
[`diagramas/arquitetura.md`](diagramas/arquitetura.md).

**Componentes AWS usados:**

| Serviço | Função | Free tier? |
|---|---|---|
| AWS Step Functions | Orquestração dos 3 workflows | ✅ 4.000 transições/mês |
| AWS Lambda | Lógica de negócio | ✅ 1M requisições/mês |
| Amazon DynamoDB | Persistência de pedidos e feedbacks | ✅ 25GB + capacidade sob demanda no free tier |
| Amazon SNS / SQS | Notificações e filas | ✅ generoso free tier |
| Amazon API Gateway | Endpoint REST público | ✅ 1M chamadas/mês (12 meses) |
| Amazon CloudWatch | Logs, métricas, alarmes | ✅ tier básico gratuito |
| Hugging Face Inference API | Análise de sentimento (substitui Bedrock) | ✅ gratuito, com rate limit |

---

## ✅ Pré-requisitos

- Conta AWS (o free tier é suficiente).
- Usuário IAM com permissões para: Step Functions, Lambda, DynamoDB, SNS, SQS,
  API Gateway, CloudWatch, IAM (para criar roles).
- [AWS CLI](https://aws.amazon.com/cli/) instalada e configurada (`aws configure`).
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
  instalada (usada para deploy da infraestrutura como código).
- Python 3.12 (as Lambdas usam só `boto3` + biblioteca padrão — **sem
  dependências pagas ou pesadas para instalar localmente**).
- Conta gratuita em [huggingface.co](https://huggingface.co/join) + um
  **Access Token** gratuito (Settings → Access Tokens → New Token, tipo "Read").

> **Sobre o disco local:** este projeto é só código + configuração (não requer
> treinar modelos nem baixar datasets), então **não precisa de Google Colab**.
> Ele roda tranquilamente com pouco espaço em disco. Se ainda assim preferir
> editar em nuvem, dá para clonar o repositório dentro do Colab (`!git clone`)
> só para editar texto/JSON e depois fazer `git push` — mas o deploy real
> (`sam deploy`) precisa ser feito de uma máquina com AWS CLI configurada
> (pode ser seu desktop mesmo, o projeto é leve).

---

## ⚙️ Instalação (deploy passo a passo)

### 1. Clonar/organizar o repositório

```bash
git clone https://github.com/SEU_USUARIO/assistente-delivery.git
cd assistente-delivery
```

### 2. Criar o token da Hugging Face

1. Acesse https://huggingface.co/join e crie uma conta gratuita.
2. Vá em **Settings → Access Tokens** → **New token** (tipo "Read").
3. Copie o token — ele será passado como parâmetro no deploy (nunca commitar
   o token no repositório).

### 3. Deploy da infraestrutura com AWS SAM

```bash
cd infra
sam build
sam deploy --guided
```

Durante o `--guided`, informe:
- **Stack Name:** `assistente-delivery`
- **AWS Region:** `us-west-2` (Oregon) — ou a região de sua preferência
- **Parameter HuggingFaceToken:** cole o token criado no passo anterior
- Demais perguntas: aceite os valores padrão (`Y`)

Ao final, o SAM mostra a **URL da API** nos `Outputs` — guarde essa URL.

### 4. Passo a passo manual pelo Console AWS (alternativa ao SAM, ou para conferência)

Caso prefira acompanhar visualmente cada etapa no Console (ou o `sam deploy`
falhar em algum recurso específico), siga:

**01 — Acessar o Console AWS**
Entre em https://console.aws.amazon.com/ e selecione a região **US West (Oregon)**
no canto superior direito.

**02 — Criar as tabelas DynamoDB**
Console → busque "DynamoDB" → **Create table**:
- Tabela 1: nome `Pedidos`, partition key `pedidoId` (String).
- Tabela 2: nome `FeedbacksPedidos`, partition key `pedidoId` (String).
- Capacidade: **On-demand** (fica dentro do free tier para uso baixo/moderado).

**03 — Criar os tópicos SNS e a fila SQS**
Console → "SNS" → **Create topic** (Standard): crie `novo-pedido-restaurante`,
`push-cliente` e `alertas-admin`.
Console → "SQS" → **Create queue** (Standard): crie `status-pedido`.

**04 — Criar as funções Lambda**
Console → "Lambda" → **Create function** → Author from scratch → Runtime
`Python 3.12`. Repita para cada arquivo em `lambdas/`, colando o código
correspondente e configurando as variáveis de ambiente indicadas no topo de
cada arquivo (ex.: `TABELA_PEDIDOS`, `HF_API_TOKEN`, etc.). Em
**Configuration → Permissions**, anexe as policies necessárias (DynamoDB,
SNS Publish, Step Functions StartExecution) à role de cada função.

**05 — Criar as Step Functions (State Machines)**
Console → busque "Step Functions" → **Create state machine** → escolha
**Write your workflow in code** → cole o conteúdo de um dos arquivos em
`workflows/*.asl.json` (substituindo `ACCOUNT_ID` pelo seu Account ID da AWS e
os ARNs das Lambdas criadas no passo anterior) → **Standard** type → Next →
dê um nome (ex.: `assistente-delivery-pedido`) → Create. Repita para os 3
workflows.

**06 — Criar o API Gateway**
Console → "API Gateway" → **Create API** → REST API → **Build** → crie o
recurso `/pedidos` com método `POST`, tipo de integração **Lambda Function**,
apontando para `api-iniciar-pedido` → **Deploy API** → stage `prod`.

**07 — Testar a execução**
Na Step Function `assistente-delivery-pedido`, clique **Start execution** e
use como input:
```json
{
  "pedido": {
    "usuarioId": "user-123",
    "restauranteId": "rest-456",
    "itens": ["Pizza Margherita", "Refrigerante"]
  }
}
```
Acompanhe o grafo visual: cada estado deve ficar verde ("Com êxito"). Veja o
output JSON e os logs no console para confirmar.

---

## ▶️ Uso

### Criar um pedido (via API)

```bash
curl -X POST https://SUA_API_URL/prod/pedidos \
  -H "Content-Type: application/json" \
  -d '{
    "usuarioId": "user-123",
    "restauranteId": "rest-456",
    "itens": ["Pizza Margherita", "Refrigerante"]
  }'
```

Resposta esperada:
```json
{
  "mensagem": "Pedido recebido, processamento iniciado.",
  "executionArn": "arn:aws:states:us-west-2:...:execution:assistente-delivery-pedido:..."
}
```

### Enviar feedback para análise de sentimento

Inicie manualmente (ou via outro endpoint da API, se você adicionar um) a
state machine `assistente-delivery-ia-sentimento` com:

```json
{
  "pedidoId": "abc-123",
  "feedback": "A entrega demorou muito e a comida chegou fria."
}
```

O workflow classifica o sentimento (Positive/Neutral/Negative) usando a
Hugging Face API, grava no DynamoDB e, se for negativo, dispara um alerta via
SNS para o tópico `alertas-admin`.

---

## 🗂️ Documentação de Workflows

| Workflow | Arquivo ASL | Gatilho |
|---|---|---|
| Processamento de pedido | `workflows/workflow_pedido.asl.json` | API Gateway → Lambda `api-iniciar-pedido` |
| Notificações push | `workflows/workflow_notificacoes.asl.json` | Disparado pelo workflow de pedido ou por eventos de mudança de status |
| Análise de sentimento (IA) | `workflows/workflow_ia_sentimento.asl.json` | Endpoint/evento de feedback do usuário |

Diagramas completos (ASCII + Mermaid) em
[`diagramas/arquitetura.md`](diagramas/arquitetura.md).

---

## 🧭 Boas Práticas adotadas

- Nomes de estados consistentes e descritivos (`ValidarPedido`,
  `NotificarRestaurante`, etc.).
- Cada Lambda tem um docstring no topo explicando propósito e variáveis de
  ambiente necessárias.
- Retries automáticos configurados nos estados críticos (`Retry` no ASL).
- Lógica de decisão (Choice) fica no Step Functions, não dentro das Lambdas —
  Lambdas ficam simples e testáveis isoladamente.
- Custos monitorados via CloudWatch: transições de estado do Step Functions e
  chamadas à Hugging Face API (gratuitas, mas com rate limit — monitore erros
  503/429 nos logs).
- Uso de `PAY_PER_REQUEST` no DynamoDB para evitar custo fixo de capacidade
  provisionada.

---

## 🧪 Testes

- **Unitários (Lambdas):** teste cada `lambda_handler` isoladamente com
  eventos JSON de exemplo (ex.: `pytest` + mocks de `boto3` com `moto`).
- **Integração (Step Functions):** use o botão **Start execution** no console
  com os payloads de exemplo deste README.
- **Carga (API Gateway):** ferramentas gratuitas como `hey` ou `k6` para
  simular requisições concorrentes.
- **IA (Hugging Face):** teste a Lambda `analisar-sentimento-hf` com frases
  claramente positivas/negativas para validar a classificação antes de ligar
  ao fluxo de produção.

---

## 📡 Observabilidade

- CloudWatch Logs habilitados por padrão em cada Lambda e Step Function.
- Configure alarmes de **ExecutionsFailed** e **ExecutionsTimedOut** nas 3
  state machines.
- Configure alarme de latência (`Latency`) e `5XXError` no API Gateway.
- (Opcional) Monte um dashboard no CloudWatch reunindo: execuções por
  workflow, taxa de sentimento negativo, latência da API.

---

## 🔗 Links úteis

- AWS Step Functions: https://aws.amazon.com/pt/step-functions/
- Exemplos oficiais de Step Functions: https://github.com/aws-samples/aws-stepfunctions-examples
- Amazon States Language (especificação): https://states-language.net/spec.html
- Statelint (validador de ASL): https://github.com/awslabs/statelint
- Hugging Face Inference API: https://huggingface.co/docs/api-inference/
- AWS SAM CLI: https://docs.aws.amazon.com/serverless-application-model/

---

## 🤝 Contribuição

1. Abra uma *issue* descrevendo o bug ou a melhoria proposta.
2. Crie um branch a partir de `main`: `git checkout -b minha-feature`.
3. Faça commit das mudanças com mensagens claras.
4. Abra um Pull Request explicando o que foi alterado e por quê.

## 📄 Licença

Distribuído sob a licença **MIT** — veja o arquivo `LICENSE` (crie um com o
texto padrão da MIT License, substituindo `[ano]` e `[seu nome]`).
