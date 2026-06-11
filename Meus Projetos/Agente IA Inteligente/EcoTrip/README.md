<div align="center">

# 🍃 CarbonTrack

### Calculadora de Emissão de CO₂ para Viagens

**Calcule, compare e compense o impacto ambiental das suas viagens pelo Brasil**

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/features/copilot)

![Status](https://img.shields.io/badge/status-concluído-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Como Executar](#-como-executar)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Módulos JavaScript](#-módulos-javascript)
- [Fatores de Emissão](#-fatores-de-emissão)
- [Créditos de Carbono](#-créditos-de-carbono)
- [Aprendizados e Desafios Técnicos](#-aprendizados-e-desafios-técnicos)
- [Autor](#-autor)

---

## 🌱 Sobre o Projeto

O **CarbonTrack** é uma aplicação web front-end que permite ao usuário calcular e visualizar as emissões de CO₂ geradas por viagens entre cidades brasileiras, comparar diferentes meios de transporte e entender o equivalente em créditos de carbono da sua pegada ambiental.

O projeto foi desenvolvido como parte do **Projeto GitHub Copilot**, explorando o desenvolvimento assistido por IA para construir uma ferramenta com propósito real: **conscientizar sobre o impacto ambiental dos deslocamentos e incentivar escolhas mais sustentáveis.**

> 💡 A consciência sobre emissões de carbono começa com informação acessível. Este projeto torna esse dado visível e compreensível para qualquer pessoa.

---

## 🖥️ Demonstração

```
Origem:      Fortaleza, CE
Destino:     São Paulo, SP
Distância:   2.845 km (preenchida automaticamente)

Resultado com Carro:
  🍃 Emissão: 341,40 kg de CO₂
  💳 Créditos de carbono: 0,3414
  💰 Valor estimado: R$ 17,07 – R$ 51,21

Comparação entre meios:
  🚴 Bicicleta  →   0,00 kg  (0% do carro)
  🚌 Ônibus     → 278,81 kg  (74,17% do carro)
  🚗 Carro      → 341,40 kg  (100%)
  🚚 Caminhão   → 2.731,20 kg (800%)
```

---

## ✨ Funcionalidades

### 🗺️ Seleção Inteligente de Rotas
- Autocomplete de cidades com **datalist HTML nativo** — sem dependências externas
- Base de dados com **33 cidades brasileiras** e **46 rotas** pré-mapeadas
- Preenchimento automático da distância ao selecionar origem e destino
- Busca bidirecional: Fortaleza → SP equivale a SP → Fortaleza
- Opção de inserir distância manualmente para rotas não cadastradas

### 🧮 Cálculo de Emissões
- Cálculo em tempo real baseado em fatores de emissão por km por modal
- Suporte a 4 meios de transporte: **Bicicleta, Carro, Ônibus e Caminhão**
- Exibição da economia gerada ao escolher transportes mais sustentáveis

### 📊 Comparação entre Transportes
- Tabela comparativa com emissão absoluta (kg CO₂) e relativa (% vs carro)
- Barras de progresso coloridas por nível de impacto ambiental:
  - 🟢 Verde — até 25% do carro (muito ecológico)
  - 🟡 Amarelo — 26% a 75% (moderado)
  - 🟠 Laranja — 76% a 100% (alto)
  - 🔴 Vermelho — acima de 100% (muito alto)
- Destaque visual para o modal selecionado

### 💳 Créditos de Carbono
- Conversão automática de kg CO₂ em créditos de carbono (1 crédito = 1.000 kg CO₂)
- Estimativa de valor em reais com faixa de variação de mercado (R$ 50 – R$ 150/crédito)
- Botão de compensação de emissões

### 🎨 Interface e UX
- Design responsivo — funciona em desktop e mobile
- Tema verde com gradiente, reforçando a identidade sustentável
- Estado de carregamento no botão com spinner animado
- Scroll automático suave até os resultados
- Feedback visual imediato ao preencher campos

---

## 🏗️ Arquitetura

O projeto adota uma arquitetura **modular orientada a objetos em JavaScript puro (Vanilla JS)**, sem frameworks ou bibliotecas externas. Cada arquivo encapsula uma responsabilidade clara:

```
┌─────────────────────────────────────────────┐
│                  index.html                  │
│         (estrutura e orquestração)           │
└──────────┬──────────────────────────────────┘
           │ carrega em ordem
    ┌──────▼──────┐
    │ routes-data │  Base de rotas e cidades brasileiras
    └──────┬──────┘
    ┌──────▼──────┐
    │   config    │  Fatores de emissão, modos de transporte,
    │             │  populateDatalist, setupDistanceAutofill
    └──────┬──────┘
    ┌──────▼──────┐
    │ calculator  │  Lógica de cálculo: emissão, comparação,
    │             │  economia, créditos de carbono
    └──────┬──────┘
    ┌──────▼──────┐
    │     ui      │  Renderização de HTML: resultados,
    │             │  comparação, créditos de carbono
    └──────┬──────┘
    ┌──────▼──────┐
    │     app     │  Inicialização, eventos DOM,
    │             │  orquestração do fluxo principal
    └─────────────┘
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| **HTML5** | Estrutura semântica, `<datalist>` para autocomplete nativo |
| **CSS3** | Layout com Grid e Flexbox, variáveis CSS, animações, responsividade |
| **JavaScript ES6+** | Módulos em objetos literais, manipulação de DOM, eventos |
| **GitHub Copilot** | Assistência no desenvolvimento e geração de código |
| **Live Server (VS Code)** | Servidor de desenvolvimento local |

> ⚡ Zero dependências externas — nenhum `npm install` necessário.

---

## 🚀 Como Executar

### Pré-requisitos
- Navegador moderno (Chrome, Firefox, Edge, Safari)
- [VS Code](https://code.visualstudio.com/) com extensão [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) *(recomendado)*

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/carbontrack-brasil.git

# 2. Acesse a pasta do projeto
cd carbontrack

# 3. Abra no VS Code
code .
```

No VS Code, clique com o botão direito em `index.html` e selecione **"Open with Live Server"**.

Ou acesse diretamente pelo browser:
```
http://127.0.0.1:5500/EcoTrip/index.html
```

> ⚠️ **Importante:** abra o projeto via servidor local (Live Server), não diretamente pelo `file://`. O browser bloqueia certos recursos quando aberto como arquivo local.

---

## 📁 Estrutura de Arquivos

```
carbontrack-brasil/
│
├── index.html              # Página principal
│
├── css/
│   └── style.css           # Estilos globais, componentes e responsividade
│
└── js/
    ├── routes-data.js      # Base de dados de rotas e cidades
    ├── config.js           # Configurações, fatores de emissão, autocomplete
    ├── calculator.js       # Motor de cálculo de emissões e créditos
    ├── ui.js               # Renderização de componentes HTML dinâmicos
    └── app.js              # Inicialização e controle do fluxo da aplicação
```

---

## 📦 Módulos JavaScript

### `RoutesDB` — routes-data.js
Banco de dados de rotas brasileiras com busca bidirecional e normalização de strings.

```javascript
RoutesDB.getAllCities()
// Retorna: ['Angra dos Reis, RJ', 'Belém, PA', 'Belo Horizonte, MG', ...]

RoutesDB.findDistance('Fortaleza, CE', 'São Paulo, SP')
// Retorna: 2845
```

### `CONFIG` — config.js
Configurações centrais da aplicação. Popula o datalist de cidades e configura o autofill de distância.

```javascript
CONFIG.EMISSION_FACTORS   // { bicycle: 0, car: 0.12, bus: 0.098, truck: 0.96 }
CONFIG.populateDatalist() // injeta as 33 cidades no <datalist>
CONFIG.setupDistanceAutofill() // monitora os inputs e preenche a distância
```

### `Calculator` — calculator.js
Motor de cálculos. Todas as operações matemáticas do projeto.

```javascript
Calculator.calculateEmission(2845, 'car')
// Retorna: 341.40 (kg CO₂)

Calculator.calculateAllModes(2845)
// Retorna: array ordenado por emissão com os 4 modais

Calculator.calculateSavings(278.81, 341.40)
// Retorna: { savedKg: 62.59, percentage: 18.33 }

Calculator.calculateCarbonCredits(341.40)
// Retorna: 0.3414

Calculator.estimateCreditPrice(0.3414)
// Retorna: { min: 17.07, max: 51.21, average: 34.14 }
```

### `UI` — ui.js
Renderização dinâmica de HTML. Todos os métodos retornam strings HTML prontas para injeção no DOM.

```javascript
UI.renderResults(data)        // cards de resultado da viagem
UI.renderComparison(modes, selected) // tabela comparativa com barras de progresso
UI.renderCarbonCredits(data)  // painel de créditos de carbono
```

### `app.js`
Orquestra a inicialização e o submit do formulário. Conecta todos os módulos.

---

## 🌡️ Fatores de Emissão

Os fatores utilizados são baseados em médias de emissão por passageiro por km:

| Modal | Fator (kg CO₂/km) | Fonte de referência |
|---|---|---|
| 🚴 Bicicleta | 0,000 | Emissão zero |
| 🚌 Ônibus | 0,098 | IPCC / ANTT |
| 🚗 Carro | 0,120 | CETESB / SEEG |
| 🚚 Caminhão | 0,960 | ANTT / EPE |

---

## 💳 Créditos de Carbono

O projeto estima o valor dos créditos de carbono com base em:

- **1 crédito de carbono** = 1.000 kg de CO₂ evitado ou removido
- **Faixa de preço**: R$ 50,00 – R$ 150,00 por crédito (mercado voluntário brasileiro)
- **Valor médio**: média aritmética da faixa

---

## 🧠 Aprendizados e Desafios Técnicos

Este projeto envolveu a identificação e resolução de bugs não triviais:

### 1. `const` vs `window` em JavaScript
Variáveis declaradas com `const` e `let` **não ficam disponíveis em `window`**, ao contrário de `var`. O código gerado pelo Copilot misturava `const CONFIG = {}` com verificações `if (window.CONFIG)`, que sempre retornavam `false`. A correção foi padronizar todas as verificações para `typeof VARIAVEL !== 'undefined'`.

### 2. `autocomplete="off"` bloqueando o `<datalist>`
O atributo `autocomplete="off"` nos inputs suprimia o dropdown do `<datalist>` no Chrome e Safari. A solução foi usar `autocomplete="nope"` — um valor desconhecido que os browsers ignoram, preservando o comportamento do datalist.

### 3. Evento `input` vs `change` no datalist
Ao selecionar uma opção do datalist com o mouse, o browser dispara `change` — não `input`. O listener estava apenas no `input`, então a busca de distância rodava antes do valor ser preenchido. A correção foi registrar ambos os eventos em cada campo.

### 4. Classes CSS ausentes para os resultados
O `ui.js` gerava HTML com classes como `comparison_item`, `comparison_grid`, `comparison_badge`, etc., que não existiam no `style.css`. Os elementos existiam no DOM mas ficavam invisíveis. A solução foi mapear todas as classes usadas pelo JS e implementá-las no CSS.

---

## 👨‍💻 Autor: Carlos Alexandre


<div align="center">

```
Responsabilidade Ambiental alinhado aos Objetivos de Desenvolvimento Sustentável (ODS).

*"Cada viagem tem um custo para o planeta. Conhecer esse custo é o primeiro passo para reduzi-lo."*
```
</div>
