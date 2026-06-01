# 🚗 Sistema de Venda de Carros Usados

**MVP** de aplicação web desenvolvido para listagem e simulação de venda de veículos seminovos. O projeto foi estruturado utilizando a arquitetura modular do framework **Flask (Python)** no backend para renderização dinâmica de dados, integrada à manipulação de eventos com **JavaScript** no frontend. Todo o processo de desenvolvimento foi conduzido sob a abordagem de **Vibe Coding**, utilizando o **GitHub Copilot** diretamente no VS Code para acelerar a construção da interface e a lógica dos scripts.

---

## 💻 Sobre o Projeto

O objetivo principal deste projeto é listar dinamicamente o estoque de veículos da concessionária "Grandes Veículos", permitindo interações em tempo real com o usuário. A aplicação simula o fluxo de dados desde o servidor até a interface do usuário (UI), aplicando conceitos fundamentais de desenvolvimento web.

### 🚀 Funcionalidades Principais
* **Renderização Dinâmica**: Listagem de carros enviada diretamente do backend via Python e estruturada na interface usando a engine de templates Jinja2.
* **Manipulação de Eventos**: Captura de cliques nos botões de compra utilizando seletores Javascript e atributos customizados (`data-*`).
* **Arquitetura Modular**: Organização de pastas seguindo o padrão de Fábrica de Aplicações (*Application Factory*), separando rotas, arquivos estáticos e templates.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**: Linguagem base do backend.
* **Flask 3.0.3**: Micro-framework para gerenciamento de rotas e renderização.
* **Jinja2**: Mecanismo de template para integração de dados Python no HTML.
* **JavaScript (ES6+)**: Camada de comportamento e interatividade no frontend.
* **HTML5 / CSS3**: Estruturação e estilização da interface.
* **GitHub Copilot**: Assistente de Inteligência Artificial para geração e otimização de código.

---

## 📂 Estrutura de Pastas

A arquitetura do projeto foi desenhada para garantir escalabilidade e fácil manutenção:

```text
car-app/
└── my-flask-app/
    ├── app/
    │   ├── static/
    │   │   └── car_sales.js      # Comportamento interativo (Frontend)
    │   ├── templates/
    │   │   └── car_sales.html    # Interface estruturada (Jinja2)
    │   ├── __init__.py           # Inicialização e Fábrica do App
    │   └── routes.py             # Definição de rotas e dados de estoque
    ├── venv/                     # Ambiente virtual isolado
    ├── requirements.txt          # Dependências do projeto
    └── run.py                    # Ponto de entrada da aplicação
```



---

## 🤖 Uso Estratégico do GitHub Copilot

```markdown
Este projeto foi desenvolvido na cultura Vibe Coding, utilizando inteligência artificial diretamente no VS Code para acelerar a escrita do código. O fluxo de trabalho com o GitHub Copilot ocorreu de duas formas:
```
1. Chat em Linha (Inline - Ctrl + I): Utilizado para a criação da interface do usuário no arquivo HTML através do prompt direto:

- "Criar uma pagina HTML para ser a home de uma plataforma web de carros usados, vai o nome da loja grande, uma tabela de carros"

2. Painel de Chat Lateral (Ctrl + Shift + I): Utilizado para sanar dúvidas estruturais sobre a passagem de listas de dicionários do Python para o ecossistema do Flask.


## 📈 Utilidade em Ambiente de Produção

Embora este projeto funcione de forma simplificada localmente, sua estrutura reflete os padrões necessários para um ambiente produtivo real:

- Desacoplamento de Dados: Os dados expostos na rota podem ser facilmente substituídos por consultas em bancos de dados relacionais (como PostgreSQL ou MySQL) ou APIs externas sem alterar a estrutura do frontend.

- Segurança e Isolamento: O uso do arquivo requirements.txt e da pasta venv garante que a aplicação rode exatamente com as mesmas versões de pacotes em servidores de nuvem (AWS, Azure, Render), eliminando o clássico problema do "na minha máquina funciona".

- Pronto para WSGI: O ponto de entrada configurado em run.py permite que servidores de produção robustos (como o Gunicorn ou uWSGI) gerenciem múltiplos acessos simultâneos de clientes sem travar a aplicação.