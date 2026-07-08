# 🛡️ STRIDE Vision Agent

> Agente de IA que analisa **imagens de diagramas de arquitetura de software** e gera automaticamente um **modelo de ameaças** baseado na metodologia **STRIDE**.

[![CI](https://github.com/CarlossAlexandree/Agent_Stride_Vision/actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-informational)

---

## 📌 Sobre o projeto

Você envia uma **imagem** do diagrama de arquitetura da sua aplicação + um pouco de contexto (tipo de app, autenticação, exposição à internet, dados sensíveis). O backend usa **prompt engineering** para instruir um modelo de IA multimodal a atuar como um especialista em cibersegurança e devolver, em JSON estruturado:

- Um **resumo executivo** da análise;
- Uma lista de **ameaças** organizadas pelas 6 categorias STRIDE (*Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege*), cada uma com cenário, impacto, componente afetado e severidade;
- **Sugestões de melhoria** — o que faltou de informação para uma análise mais precisa.

O frontend renderiza tudo isso de forma visual, incluindo um **grafo interativo** dos componentes citados (Cytoscape.js) e um botão de **impressão/exportação em PDF**.

> 💡 **Sem custo de API**: o projeto usa por padrão o **Google Gemini** (free tier com visão computacional). A camada de IA é abstraída (*Strategy Pattern*), então trocar para **Groq**, **Ollama** (100% local) ou **Azure OpenAI** é só mudar uma variável de ambiente — nenhum código muda.

---

## 🖼️ Como funciona (visão geral)

```
┌──────────────┐      multipart/form-data       ┌───────────────────┐      REST/JSON       ┌──────────────────┐
│   Frontend   │ ───────────────────────────────▶│   FastAPI backend │ ────────────────────▶│  Provedor de IA  │
│ (HTML/CSS/JS │◀─────────────────────────────── │  (Python 3.12)    │◀──────────────────── │ Gemini / Groq /  │
│  Cytoscape)  │        JSON estruturado          │                   │    JSON com ameaças   │ Ollama / Azure   │
└──────────────┘                                  └───────────────────┘                       └──────────────────┘
```

---

## 🗂️ Estrutura do projeto

```
stride-vision-agent/
├── backend/
│   ├── app/
│   │   ├── main.py                  # Entrypoint FastAPI + exception handlers
│   │   ├── api/routes.py            # Endpoints HTTP
│   │   ├── core/                    # Config, logging, exceções, rate limit
│   │   ├── models/schemas.py        # Contratos Pydantic (request/response)
│   │   └── services/
│   │       ├── prompt_builder.py    # Prompt engineering (STRIDE)
│   │       ├── image_service.py     # Validação/encoding da imagem
│   │       ├── threat_analysis_service.py  # Orquestração + parsing do JSON
│   │       └── providers/           # Abstração dos provedores de IA
│   │           ├── base.py
│   │           ├── gemini_provider.py
│   │           ├── groq_provider.py
│   │           ├── ollama_provider.py
│   │           ├── azure_openai_provider.py
│   │           └── factory.py
│   ├── tests/                       # Testes automatizados (pytest)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/{app.js, graph.js}
│   ├── Dockerfile
│   └── nginx.conf
├── .github/workflows/ci.yml         # Lint + testes automáticos
├── docker-compose.yml
└── README.md
```

---

## 🚀 Como rodar localmente

### Pré-requisitos
- Python 3.12+
- Uma chave gratuita de um provedor de IA com visão (veja abaixo)

### 1. Obtenha uma chave de API gratuita

| Provedor | Onde obter | Observação |
|---|---|---|
| **Google Gemini** (padrão) | https://aistudio.google.com/apikey | Free tier generoso, boa visão computacional |
| **Groq** | https://console.groq.com/keys | Extremamente rápido, também gratuito |
| **Ollama** | https://ollama.com | 100% local, sem chave, requer `ollama pull llama3.2-vision` |

### 2. Configure e rode o backend

```bash
cd backend
cp .env.example .env
# edite o .env e cole sua GEMINI_API_KEY (ou configure outro provider)

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

A API estará em `http://localhost:8000` e a documentação interativa (Swagger) em `http://localhost:8000/docs`.

### 3. Rode o frontend

```bash
cd frontend
python3 -m http.server 8080
```

Acesse `http://localhost:8080`.

### 4. (Opcional) Rodar tudo com Docker Compose

```bash
docker compose up --build
```
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`

> ℹ️ Este projeto **não requer nenhuma VM** — ele roda em contêineres leves ou diretamente na sua máquina. Se você pretende publicar em nuvem, veja a seção de deploy abaixo; não é necessário provisionar uma VM do Azure para este escopo.

---

## ☁️ Deploy gratuito (produção)

| Camada | Opção recomendada | Como |
|---|---|---|
| Backend | [Render](https://render.com) (Web Service, free tier) | Apontar para `backend/`, use o `Dockerfile` incluso, configure as env vars do `.env.example` |
| Frontend | [Render Static Site](https://render.com) ou [Netlify](https://netlify.com) | Apontar para a pasta `frontend/` |
| Alternativa tudo-em-um | [Hugging Face Spaces](https://huggingface.co/spaces) (Docker Space) | Subir o `docker-compose.yml` adaptado a um único `Dockerfile` |

Depois do deploy, editar `frontend/js/app.js` e ajustar `API_BASE_URL` para a URL pública do seu backend (ou defina `window.STRIDE_API_BASE_URL` antes de carregar o script).

---

## 🔄 Trocando o provedor de IA

Toda a lógica de IA está isolada atrás de uma interface (`AIVisionProvider`). Para trocar de provedor, editar apenas o `.env`:

```env
AI_PROVIDER=groq  # gemini | groq | azure_openai | ollama
GROQ_API_KEY=sua_chave_aqui
```

Nenhum outro arquivo precisa ser tocado. A *factory* em `app/services/providers/factory.py` cuida da seleção.

---

## 🧪 Testes e qualidade

```bash
cd backend
pip install -r requirements-dev.txt
ruff check app/          # lint
pytest tests/ -v         # testes automatizados
```

O pipeline de CI (`.github/workflows/ci.yml`) roda lint + testes automaticamente em todo push/PR para `main`.

---

## 🔐 Notas de segurança

- Imagens são processadas **em memória** (nunca gravadas em disco) e descartadas após a chamada à IA.
- Rate limiting simples por IP (10 req/min, configurável) protege contra abuso do free tier da IA.
- CORS restrito por variável de ambiente (`ALLOWED_ORIGINS`) — ajuste para o domínio real do seu frontend em produção.
- Nenhuma stack trace é exposta ao cliente; erros são logados no servidor e retornados como mensagens amigáveis.

---

## 🛣️ Possíveis evoluções

- Autenticação de usuários e histórico de análises persistido em banco de dados;
- Detecção automática de componentes via visão computacional (bounding boxes) em vez de depender só do texto retornado pela IA;
- Exportação do relatório em PDF gerado no backend (hoje é impressão via navegador);
- Cache de respostas por hash da imagem, para evitar reprocessar o mesmo diagrama.

---

> **Nota sobre o ambiente de desenvolvimento:** este projeto foi construído em um ambiente com espaço em disco local limitado, o que motivou decisões como processar imagens em memória (sem gravação em disco), evitar dependências de build via Node/`node_modules` no frontend e dispensar o uso de VM. Essas restrições não são limitações da arquitetura em si: o projeto foi desenhado desde o início para ser adaptável e escalar para um ambiente de produção mais complexa. Basta trocar o rate limiter em memória por Redis, adicionar armazenamento persistente (banco de dados / object storage) e provisionar a infraestrutura (VM, Kubernetes, etc.) conforme a demanda real do negócio exigir.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](./LICENSE).
