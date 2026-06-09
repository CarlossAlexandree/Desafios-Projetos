# 📊 Automação de Tarefas no Trello com Google Agent Development Kit (ADK)

Componente de automação e governança visual de atividades integrado à API oficial do **Trello** utilizando o framework **Google ADK**.

---

## 📝 Descrição do Projeto

Projeto de Desenvolvimento e Deploy do **AgentCoder**. Um agente inteligente especialista projetado para gerenciar e organizar fluxos de trabalho através da interface interação do Google ADK. A principal missão deste componente é eliminar registros manuais e simulações fictícias em texto, transformando comandos de linguagem natural em cartões reais, físicos e rastreáveis dentro de um quadro Kanban no Trello.

O projeto segue rigorosamente o padrão arquitetural exigido pelo framework, implementando o isolamento completo de escopo entre a inteligência generativa e os braços operacionais de execução (funções puras com assinaturas de tipos primitivos).

---

## 🛠️ Arquitetura de Solução e Componentes

Para total estabilidade do ecossistema e conformidade com boas práticas de engenharia de software, a lógica foi desacoplada em arquivos independentes de alta coesão:

### 1. 🧠 O Cérebro: `agent.py`
Responsável pela inicialização do agente utilizando o modelo de linguagem **Gemini 2.0 Flash** (executado sob chaves de API dedicadas para gerenciamento de cota). Este arquivo configura a persona do assistente, estabelece as instruções de conduta em português do Brasil e expõe as ferramentas (*Function Calling*) por meio de tipagens (`type hints`) e descrições detalhadas (`docstrings`) que o ADK usa para mapear os esquemas JSON.

### 2. 🔌 O Braço Operacional: `trello_tool.py`
Uma ferramenta isolada e purificada que encapsula toda a comunicação HTTP com os endpoints oficiais da API da Atlassian. Utilizando os cabeçalhos de autorização do protocolo OAuth seguro, a função executa requisições `POST` diretas para criação imediata de cartões na web.

---

## 🧬 Fluxo de Trabalho do Agente (Workflow)

```
🔄 INICIALIZAÇÃO DA SESSÃO
 └── [ Usuário ] ────► Inicia o Chat
        │
        └───► ⚙️ tool: get_temporal_context()
                 └───► Retorna Data/Hora Atual do Sistema

💬 TRIAGEM CONVERSACIONAL
 └── [ AgentCoder ] ──► Apresenta o timestamp e pergunta as tarefas do dia
        │
        └───► [ Usuário ] ──► Descreve a atividade e confirma o registro

🚀 AUTOMAÇÃO E PERSISTÊNCIA
 └── [ AgentCoder ] ──► ⚙️ tool: criar_cartao_trello(titulo, descricao)
        │
        └───► 🌐 API requests.post() ──► [ Servidores do Trello ]
                 │
                 └───► Retorna Sucesso + URL Curta do Cartão
                          │
                          └───► Assistente exibe o Link no Chat ──► [ Usuário ]
```

---

## 📋 Etapas de Execução

* **⏱️ Contexto Temporal Dinâmico**
  O ciclo de vida da interação começa com o acionamento automático da ferramenta `get_temporal_context`. O agente captura o horário exato da máquina para saudar o usuário com precisão cronológica.

* **💬 Triagem e Coleta de Requisitos**
  Através de uma abordagem conversacional fluida, o assistente interroga o usuário sobre as metas e atividades pendentes do dia, extraindo títulos e descrições textuais de forma orgânica.

* **🔐 Validação Humana (*Human-in-the-Loop*)**
  Antes de realizar qualquer transação de dados na nuvem, o agente atua sob uma diretriz de segurança rígida: solicita a autorização expressa do usuário para confirmar se a tarefa listada deve ou não ser gravada no painel.

* **⚙️ Persistência Automatizada (Chamada Real)**
  Assim que recebe o sinal verde, o cérebro da IA orquestra a execução da ferramenta `criar_cartao_trello`. Os parâmetros de título e descrição são injetados diretamente na requisição, sem qualquer simulação ou geração de texto fictício.

* **🌐 Feedback em Tempo Real**
  O ecossistema consome o payload de resposta dos servidores da Atlassian, extrai a URL curta de visualização e renderiza o link direto do cartão no chat para que o usuário possa acessá-lo instantaneamente.

---