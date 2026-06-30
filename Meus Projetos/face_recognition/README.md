# 🧠 Sistema de Reconhecimento Facial — SSD + TensorFlow

> Detecção e reconhecimento de múltiplos rostos em tempo real, combinando **SSD ResNet-10** (detecção) com **MobileNetV2** via **TensorFlow** (identificação), seguindo a arquitetura de duas redes proposta no projeto do curso.

![status](https://img.shields.io/badge/status-completo-brightgreen)
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![tensorflow](https://img.shields.io/badge/TensorFlow-2.15%2B-orange)
![opencv](https://img.shields.io/badge/OpenCV-4.9%2B-red)

---

## 📌 Sobre o Projeto

Este projeto implementa um **sistema de reconhecimento facial do zero**, exigindo duas redes neurais trabalhando em conjunto:

| Rede | Framework | Função |
|---|---|---|
| 🔍 **Rede 1 — Detecção** | OpenCV DNN (Caffe) | Localiza **onde** estão os rostos na imagem |
| 🧬 **Rede 2 — Reconhecimento** | TensorFlow / Keras | Identifica **quem** é cada rosto detectado |

O resultado final exibe, para cada rosto encontrado, o **nome da pessoa** e a **confiança da identificação** — exatamente como no exemplo de referência do curso (`leonard (0.49)`, `penny (0.49)`, etc.).

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────────┐
│   Imagem    │ ───▶ │  Rede 1: SSD     │ ───▶ │  Rede 2: MobileNetV2│
│  de entrada │      │  (localização)   │      │  (identificação)    │
└─────────────┘      └──────────────────┘      └────────────────────┘
                              │                          │
                              ▼                          ▼
                      bounding boxes            nome + confiança
                              │                          │
                              └────────────┬─────────────┘
                                           ▼
                                  Imagem anotada final
```

---

## 🗂️ Estrutura do Projeto

```
face_recognition/
│
├── 📁 models/                     # Artefatos das duas redes
│   ├── deploy.prototxt            # Arquitetura da Rede 1 (SSD)
│   ├── res10_300x300_ssd_iter_140000.caffemodel
│   ├── face_recognizer.keras      # Rede 2 treinada (gerado por train.py)
│   ├── class_names.json           # Nomes das identidades treinadas
│   └── training_meta.json         # Métricas e parâmetros do treino
│
├── 📁 dataset/                    # Dataset de treino da Rede 2
│   ├── train/
│   │   ├── joao/      foto1.jpg  foto2.jpg ...
│   │   ├── maria/     foto1.jpg  ...
│   │   └── pedro/     foto1.jpg  ...
│   └── val/                       # (opcional — split automático já incluso)
│
├── 📁 scripts/
│   ├── download_assets.py         # Baixa os arquivos da Rede 1
│   └── capture_faces.py           # Captura fotos via webcam p/ montar dataset
│
├── 📁 src/                        # Código-fonte principal
│   ├── __init__.py
│   ├── detector.py                # Rede 1 — FaceDetector (SSD)
│   ├── classifier.py               # Rede 2 — FaceClassifier (TensorFlow)
│   ├── image_utils.py             # I/O, redimensionamento, anotação visual
│   └── logger_config.py           # Logging centralizado
│
├── 📁 tests/                      # Testes unitários
│   ├── test_detector.py
│   ├── test_classifier.py
│   └── test_image_utils.py
│
├── 📁 assets/                     # Imagens de teste do usuário
├── 📁 output/                     # Resultados gerados (imagens + logs)
│
├── train.py                       # Treina a Rede 2 (2 fases de fine-tuning)
├── recognize.py                   # Pipeline completo em imagens
├── recognize_webcam.py            # Pipeline completo em tempo real (webcam)
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

- **Python 3.11+**
- **VS Code** com a extensão [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Webcam (opcional, apenas para captura de dataset e modo tempo real)
- ~500 MB livres para os modelos e dependências

---

## 🚀 Passo a Passo Completo — Da Instalação à Produção

### 1️⃣ Clonar / abrir o projeto e criar ambiente virtual

```bash
cd face_recognition

# Criar ambiente virtual
python -m venv .venv

# Ativar — Git Bash / MINGW64 (VS Code no Windows)
source .venv/Scripts/activate

# Ativar — CMD
.venv\Scripts\activate.bat

# Ativar — PowerShell
.venv\Scripts\Activate.ps1

# Ativar — macOS / Linux
source .venv/bin/activate
```

Você saberá que funcionou quando o prompt mostrar `(.venv)` no início da linha.

---

### 2️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

> ⏳ O TensorFlow é uma biblioteca grande — a instalação pode levar alguns minutos.

---

### 3️⃣ Baixar os arquivos da Rede 1 (detector SSD)

```bash
python scripts/download_assets.py
```

Isso salva em `models/`:
- `deploy.prototxt`
- `res10_300x300_ssd_iter_140000.caffemodel`

> 💡 A Rede 2 (MobileNetV2) **não precisa de download manual** — o Keras baixa os pesos pré-treinados automaticamente na primeira execução do treino.

---

### 4️⃣ Montar o dataset de treino (fotos por pessoa)

Você tem **duas opções**:

#### Opção A — Capturar fotos pela webcam (recomendado)

```bash
python scripts/capture_faces.py --name joao --count 40
python scripts/capture_faces.py --name maria --count 40
python scripts/capture_faces.py --name pedro --count 40
```

Controles durante a captura:
| Tecla | Ação |
|---|---|
| `espaço` | Captura manual de uma foto |
| `a` | Liga/desliga modo automático (captura contínua) |
| `q` | Sai |

#### Opção B — Adicionar fotos manualmente

Organize suas próprias fotos na estrutura:

```
dataset/train/
    joao/    foto1.jpg  foto2.jpg  foto3.jpg ...
    maria/   foto1.jpg  foto2.jpg ...
    pedro/   foto1.jpg  ...
```

> ⚠️ **Recomendação:** pelo menos **30–50 fotos por pessoa**, com variação de ângulo, iluminação e expressão, para um treino mais robusto.

---

### 5️⃣ Treinar a Rede 2 (reconhecedor facial)

```bash
python train.py --dataset dataset/train
```

O treino acontece em **duas fases**, conforme transfer learning padrão:

| Fase | O que acontece | Épocas padrão |
|---|---|---|
| **Fase 1** | Base MobileNetV2 congelada; só a camada Dense aprende | 20 |
| **Fase 2** | Últimas 30 camadas da base são descongeladas (fine-tuning) | 10 |

Parâmetros customizáveis:

```bash
python train.py \
  --dataset dataset/train \
  --epochs1 25 \
  --epochs2 15 \
  --batch 16 \
  --threshold 0.65
```

Ao final, são gerados em `models/`:
- `face_recognizer.keras` — modelo treinado
- `class_names.json` — lista de identidades
- `training_meta.json` — métricas de acurácia e parâmetros usados

---

### 6️⃣ Rodar o reconhecimento em uma imagem

```bash
python recognize.py --image assets/foto_grupo.jpg
```

Com parâmetros customizados:

```bash
python recognize.py \
  --image assets/foto_grupo.jpg \
  --output output/resultado.jpg \
  --confidence 0.6 \
  --threshold 0.7 \
  --width 800
```

Visualizar o resultado:

```bash
start output/resultado.jpg
```

---

### 7️⃣ Rodar em tempo real pela webcam (produção)

```bash
python recognize_webcam.py
```

Com parâmetros customizados:

```bash
python recognize_webcam.py --confidence 0.6 --threshold 0.7 --camera 0
```

Pressione `q` para encerrar a captura.

---

## 🎛️ Parâmetros de CLI — Referência completa

### `train.py`

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--dataset` / `-d` | `dataset/train` | Pasta raiz do dataset |
| `--epochs1` | `20` | Épocas da Fase 1 (base congelada) |
| `--epochs2` | `10` | Épocas da Fase 2 (fine-tuning) |
| `--batch` / `-b` | `32` | Tamanho do batch |
| `--dropout` | `0.4` | Taxa de dropout |
| `--val-split` | `0.2` | Fração para validação |
| `--threshold` | `0.60` | Confiança mínima salva no modelo |
| `--output` / `-o` | `models/` | Pasta de saída do modelo treinado |
| `--debug` | `False` | Logs detalhados |

### `recognize.py`

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--image` / `-i` | *(obrigatório)* | Imagem de entrada |
| `--output` / `-o` | `output/resultado.jpg` | Caminho de saída |
| `--confidence` / `-c` | `0.5` | Limiar de confiança da Rede 1 (SSD) |
| `--threshold` / `-t` | `0.60` | Limiar de confiança da Rede 2 (TF) |
| `--width` / `-w` | `600` | Largura de redimensionamento |
| `--model-dir` | `models/` | Pasta com o modelo treinado |
| `--debug` | `False` | Logs detalhados |

### `recognize_webcam.py`

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--camera` | `0` | Índice da webcam |
| `--confidence` / `-c` | `0.5` | Limiar Rede 1 |
| `--threshold` / `-t` | `0.60` | Limiar Rede 2 |
| `--width` / `-w` | `640` | Largura de processamento |

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=term-missing
```

> 📌 Os testes da Rede 2 usam `pytest.importorskip("tensorflow")`, então rodam normalmente mesmo que o TensorFlow ainda não esteja instalado no ambiente de CI.

---

## 🏛️ Arquitetura e Boas Práticas

- **Separação de responsabilidades** — cada módulo tem uma única função:
  - `detector.py` → Rede 1 (detecção via SSD)
  - `classifier.py` → Rede 2 (reconhecimento via TensorFlow)
  - `image_utils.py` → I/O e anotação visual
  - `logger_config.py` → logging centralizado
  - `train.py` / `recognize.py` / `recognize_webcam.py` → scripts de orquestração

- **Tipagem e dataclasses** — `DetectionConfig` e `FaceROI` encapsulam dados com clareza

- **Transfer Learning em 2 fases** — boa prática padrão da indústria para datasets pequenos: primeiro treina-se apenas a cabeça da rede, depois ajusta-se finamente as camadas superiores do backbone

- **Data Augmentation** — `RandomFlip`, `RandomRotation`, `RandomZoom`, `RandomBrightness` e `RandomContrast` aumentam a robustez do modelo com poucos dados

- **Threshold de confiança configurável** — rostos não reconhecidos com confiança suficiente são marcados como `"Desconhecido"`, evitando falsos positivos

- **Logging estruturado** — substitui `print()` por `logging` com níveis e gravação em arquivo

- **Testes unitários** — cobertura de ambas as redes com `pytest`, incluindo casos de borda

---

## 🔬 Como funciona internamente

### Rede 1 — Detecção (SSD + ResNet-10)

```
Imagem → resize 300×300 → blob (normalização) → forward pass SSD
       → bounding boxes com confiança > threshold
```

### Rede 2 — Reconhecimento (MobileNetV2 + Transfer Learning)

```
Recorte do rosto → resize 224×224 → preprocess MobileNetV2
                 → backbone (features) → GlobalAveragePooling
                 → Dropout → Dense(softmax)
                 → nome + confiança
```

### Pipeline completo

```
Imagem de entrada
       │
       ▼
  [Rede 1] Detecta N rostos → N bounding boxes
       │
       ▼
  Para cada rosto detectado:
       │
       ▼
  [Rede 2] Classifica → nome + confiança
       │
       ▼
  Desenha box colorido + label "Nome (XX.X%)"
       │
       ▼
  Imagem anotada final
```

---

## 📦 Dependências

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `opencv-python` | 4.9.0 | Leitura de imagens, DNN (Rede 1), desenho de anotações |
| `tensorflow` | 2.15.0 | Rede 2 — MobileNetV2, treino, inferência |
| `numpy` | 1.26.0 | Operações matriciais |
| `imutils` | 0.5.4 | Utilitários de conveniência |
| `pillow` | 10.0.0 | Suporte de imagem para o TensorFlow |
| `pytest` | 8.0.0 | Testes unitários |
| `pytest-cov` | 5.0.0 | Cobertura de testes |

---

## ❓ Solução de Problemas (FAQ)

**"ModuleNotFoundError: No module named 'src'"**
→ Verifique se está executando os comandos a partir da **raiz do projeto** (onde está `train.py`), não de dentro de `src/`.

**"Nenhum rosto detectado"**
→ Reduza o `--confidence` (ex: `0.3`) ou use uma imagem com boa iluminação e rosto bem visível.

**"Desconhecido" para uma pessoa cadastrada**
→ Diminua o `--threshold` (ex: `0.5`) ou adicione mais fotos variadas dessa pessoa no dataset e retreine.

**Treino muito lento / sem GPU**
→ Normal em CPU. Reduza `--epochs1` e `--epochs2`, ou use Google Colab com GPU gratuita para o treino, depois copie `models/face_recognizer.keras` de volta para o projeto local.

---

## 🗺️ Roadmap

- [ ] Suporte a múltiplas câmeras simultâneas
- [ ] API REST com FastAPI para integração externa
- [ ] Exportação do modelo para TensorFlow Lite (uso em dispositivos móveis)
- [ ] Dashboard de métricas de treino com TensorBoard
- [ ] Sistema de cadastro contínuo (re-treino incremental)

---

## 📄 Licença

Distribuído sob a licença **MIT**.

---

## 🙏 Referências

- [OpenCV DNN Face Detector](https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector)
- [SSD: Single Shot MultiBox Detector — Liu et al., 2016](https://arxiv.org/abs/1512.02325)
- [MobileNetV2 — Sandler et al., 2018](https://arxiv.org/abs/1801.04381)
- [TensorFlow Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)