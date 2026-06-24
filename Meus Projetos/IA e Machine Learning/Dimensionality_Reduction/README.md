# 🔲 Redução de Dimensionalidade — Binarização de Imagem

> **Desafio DIO** · Trilha de Machine Learning / Visão Computacional

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?logo=opencv)](https://opencv.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Sobre o Projeto

Este projeto implementa um pipeline de **redução de dimensionalidade por binarização de imagens** utilizando Python e OpenCV.

A proposta é transformar uma imagem colorida em duas representações de menor complexidade:

| Etapa | Canais | Valores possíveis | Dimensionalidade |
|-------|--------|-------------------|-----------------|
| Colorida (BGR) | 3 | 0–255 por canal | Alta |
| Escala de cinza | 1 | 0–255 | Média |
| Binária (P&B) | 1 | 0 ou 255 | Baixa |

### Resultado esperado

```
┌─────────────────┬──────────────────┬──────────────────┐
│  Imagem Original│  Imagem em Cinza │  Imagem Binária  │
│   (colorida)    │   (0 a 255)      │   (0 ou 255)     │
└─────────────────┴──────────────────┴──────────────────┘
```

---

## 🗂️ Estrutura do Projeto

```
dimensionality-reduction/
│
├── src/
│   ├── binarizacao.py           # Script principal (simples e direto)
│   └── binarizacao_avancada.py  # Com Blur Gaussiano (reproduz o slide da aula)
│
├── assets/
│   └── Foto_01.png              # Imagem de exemplo (substitua pela sua)
│   └── Foto_02.png
│   └── Foto_03.jpg
│
├── binarizacao.ipynb            # Notebook Jupyter / Google Colab
├── requirements.txt             # Dependências Python
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

- Python **3.10+**
- pip

---

## 🚀 Como Executar

### Opção 1 — VS Code (recomendado para uso local e GitHub)

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/dimensionality-reduction.git
cd dimensionality-reduction

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Coloque sua imagem na pasta assets/ e execute
python src/binarizacao.py
# ou passe o caminho como argumento:
python src/binarizacao.py assets/minha_foto.jpg 127
```

### Opção 2 — Google Colab (sem instalação local)

1. Acesse [Google Colab](https://colab.research.google.com/)
2. Faça upload do arquivo `binarizacao.ipynb`
3. Execute célula por célula (Shift + Enter)
4. Na célula de upload, selecione sua imagem

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

---

## 🧠 Como Funciona

### Script principal (`binarizacao.py`)

```python
# 1. Carrega a imagem colorida (BGR)
img = cv2.imread('assets/lena.jpg')

# 2. Converte para escala de cinza (reduz 3 canais → 1 canal)
img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Aplica threshold: pixels > 127 → 255 (branco); demais → 0 (preto)
_, img_bin = cv2.threshold(img_cinza, 127, 255, cv2.THRESH_BINARY)
```

### Versão avançada (`binarizacao_avancada.py`)

Reproduz o exemplo do slide da aula com:

```python
# Blur Gaussiano para suavizar antes do threshold
suave = cv2.GaussianBlur(img_cinza, (7, 7), 0)

# Threshold normal e invertido
_, bin_normal = cv2.threshold(suave, 160, 255, cv2.THRESH_BINARY)
_, bin_inv    = cv2.threshold(suave, 160, 255, cv2.THRESH_BINARY_INV)

# Máscara bitwise
mascara = cv2.bitwise_and(img_cinza, img_cinza, mask=bin_inv)
```

### Parâmetro principal: Limiar (threshold)

| Limiar | Efeito |
|--------|--------|
| **Baixo (< 100)** | Maioria dos pixels → branco |
| **127** | Ponto médio equilibrado (padrão) |
| **Alto (> 180)** | Maioria dos pixels → preto |

---

## 📸 Exemplos de Uso

```bash
# Imagem padrão (assets/Foto_01.png) com limiar 127
python src/binarizacao.py

# Imagem personalizada
python src/binarizacao.py assets/Foto_01.png

# Imagem personalizada com limiar customizado
python src/binarizacao.py assets/imagem_cinza.jpg 160

# Versão avançada (com blur) — parâmetros: arquivo limiar kernel_blur
python src/binarizacao_avancada.py assets/imagem_binaria.jpg 160 7
```

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| [OpenCV](https://opencv.org/) | ≥ 4.8 | Leitura, conversão e threshold de imagens |
| [NumPy](https://numpy.org/) | ≥ 1.24 | Operações matriciais sobre pixels |
| [Matplotlib](https://matplotlib.org/) | ≥ 3.7 | Visualização no Jupyter/Colab |

---

## 👤 Autor - Carlos Alexandre


---

*"Reduzir dimensionalidade é simplificar sem perder o essencial."*