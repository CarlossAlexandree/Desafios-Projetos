# 🎯 YOLO Detector — YOLOv8 + COCO

> Detecção de objetos em imagens e vídeo em tempo real usando **YOLOv8 (Ultralytics)** com Transfer Learning sobre o dataset **COCO**, focando nas classes **person**, **laptop** e **cell phone**.

![status](https://img.shields.io/badge/status-completo-brightgreen)
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![yolov8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![coco](https://img.shields.io/badge/dataset-COCO-orange)

---

## 📌 Sobre o Projeto

Este projeto implementa um **sistema de detecção de objetos** usando a arquitetura **YOLO (You Only Look Once)** na sua versão mais moderna — **YOLOv8** da Ultralytics. O modelo utiliza **Transfer Learning** sobre pesos pré-treinados no dataset **COCO** (80 classes), com foco em três classes do cotidiano tecnológico:

| Classe | Descrição | Cor no resultado |
|---|---|---|
| 👤 `person` | Pessoa humana | 🟠 Laranja |
| 💻 `laptop` | Notebook/computador | 🟢 Verde |
| 📱 `cell phone` | Celular/smartphone | 🔵 Azul |

### 🔍 O que é YOLO?

O **YOLO (You Only Look Once)** é uma das arquiteturas de detecção de objetos mais rápidas e precisas existentes. Diferente de métodos em duas etapas (como Faster R-CNN), o YOLO realiza a **detecção em uma única passagem** pela rede neural, tornando-o ideal para aplicações em tempo real.

O **YOLOv8** traz melhorias significativas em relação às versões anteriores: arquitetura anchor-free, backbone CSPDarknet aprimorado e suporte nativo a Python/pip via pacote `ultralytics`.

---

## 🗂️ Estrutura do Projeto

```
yolo_detector/
│
├── 📁 models/                     # Pesos do YOLOv8 (baixados automaticamente)
│   └── yolov8n.pt                 # Modelo nano (baixado na primeira execução)
│
├── 📁 dataset/                    # Dataset COCO (opcional para retreino)
│   ├── images/                    # Imagens do dataset
│   └── labels/                    # Anotações no formato YOLO (.txt)
│
├── 📁 scripts/
│   └── download_sample_images.py  # Baixa imagens de exemplo do COCO
│
├── 📁 src/                        # Código-fonte principal
│   ├── __init__.py
│   ├── detector.py                # YOLODetector + Detection + DetectionConfig
│   ├── visualizer.py              # Anotação visual dos resultados
│   ├── image_utils.py             # I/O e utilitários de imagem
│   └── logger_config.py           # Logging centralizado
│
├── 📁 tests/                      # Testes unitários
│   ├── test_detector.py
│   ├── test_image_utils.py
│   └── test_visualizer.py
│
├── 📁 assets/                     # Imagens de teste do usuário
├── 📁 output/                     # Resultados gerados (criado automaticamente)
│
├── detect.py                      # Detecção em imagem(ns) — CLI
├── detect_webcam.py               # Detecção em tempo real — webcam
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

- **Python 3.11+**
- **VS Code** com a extensão [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Webcam (opcional, apenas para modo tempo real)
- ~200 MB livres (modelo YOLOv8n)

> 💡 **Sem GPU?** Sem problema. O YOLOv8n (nano) foi projetado para rodar eficientemente em CPU, com boa velocidade mesmo em notebooks comuns.

---

## 🚀 Passo a Passo Completo — Da Instalação ao Resultado

### 1️⃣ Criar e ativar o ambiente virtual

```bash
cd yolo_detector

# Criar
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

O prompt mostrará `(.venv)` quando estiver ativo.

---

### 2️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

> ⏳ O pacote `ultralytics` instalará automaticamente PyTorch e todas as dependências necessárias. Pode levar alguns minutos.

---

### 3️⃣ Baixar imagens de exemplo para testar

```bash
python scripts/download_sample_images.py
```

Isso baixa imagens do COCO com as classes alvo para a pasta `assets/`.

> 💡 Alternativamente, coloque **qualquer imagem sua** em `assets/` — uma foto com você no notebook, celular na mão, etc.

---

### 4️⃣ Detectar objetos em uma imagem

```bash
# Detecção básica (classes alvo: person, laptop, cell phone)
python detect.py --image assets/coco_person_laptop.jpg

# Ver o resultado
start output/resultado.jpg
```

Com parâmetros customizados:

```bash
python detect.py \
  --image assets/coco_person_laptop.jpg \
  --output output/meu_resultado.jpg \
  --confidence 0.5 \
  --model yolov8s.pt
```

Modo **todas as 80 classes COCO** (demonstração completa):

```bash
python detect.py --image assets/coco_person_laptop.jpg --all-classes
```

Modo **batch** (processar uma pasta inteira de imagens):

```bash
python detect.py --batch assets/
```

---

### 5️⃣ Detecção em tempo real via webcam

```bash
python detect_webcam.py
```

| Tecla | Ação |
|---|---|
| `q` | Encerra a captura |
| `s` | Salva o frame atual em `output/` |
| `a` | Alterna entre classes alvo e todas as 80 classes COCO |

Com parâmetros:

```bash
python detect_webcam.py --confidence 0.5 --camera 0 --save
```

---

## 🎛️ Parâmetros de CLI — Referência Completa

### `detect.py`

| Parâmetro | Atalho | Padrão | Descrição |
|---|---|---|---|
| `--image` | `-i` | *(obrigatório\*)* | Imagem de entrada |
| `--batch` | `-b` | *(obrigatório\*)* | Pasta com várias imagens |
| `--output` | `-o` | `output/resultado.jpg` | Caminho de saída |
| `--model` | `-m` | `yolov8n.pt` | Modelo YOLOv8 a usar |
| `--confidence` | `-c` | `0.40` | Confiança mínima (0–1) |
| `--iou` | — | `0.45` | Threshold IoU para NMS |
| `--width` | `-w` | `640` | Largura de redimensionamento |
| `--all-classes` | — | `False` | Detecta todas as 80 classes COCO |
| `--debug` | — | `False` | Logs detalhados |

\* `--image` e `--batch` são mutuamente exclusivos; um deles é obrigatório.

### `detect_webcam.py`

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--camera` | `0` | Índice da webcam |
| `--model` / `-m` | `yolov8n.pt` | Modelo YOLOv8 |
| `--confidence` / `-c` | `0.40` | Confiança mínima |
| `--width` / `-w` | `640` | Largura de processamento |
| `--all-classes` | `False` | Todas as classes COCO |
| `--save` | `False` | Salva o vídeo em `output/webcam.avi` |

---

## 🤖 Modelos YOLOv8 disponíveis

O modelo é baixado **automaticamente** na primeira execução. Escolha conforme sua necessidade:

| Modelo | Tamanho | Velocidade (CPU) | Precisão |
|---|---|---|---|
| `yolov8n.pt` | ~6 MB | ⚡ Mais rápido | ⭐⭐⭐ |
| `yolov8s.pt` | ~22 MB | 🚀 Rápido | ⭐⭐⭐⭐ |
| `yolov8m.pt` | ~50 MB | 🐢 Médio | ⭐⭐⭐⭐⭐ |

> Para o projeto do curso, `yolov8n.pt` (padrão) é suficiente e o mais adequado para uso em CPU.

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=term-missing
```

---

## 🏛️ Arquitetura e Boas Práticas

- **Separação de responsabilidades** — cada módulo tem função única:
  - `detector.py` → lógica de detecção (YOLOv8)
  - `visualizer.py` → anotação visual dos resultados
  - `image_utils.py` → I/O e manipulação de imagens
  - `logger_config.py` → logging centralizado

- **Dataclasses tipadas** — `DetectionConfig` e `Detection` encapsulam dados com clareza e autocompletar no VS Code

- **Filtro de classes configurável** — o detector pode focar apenas nas 3 classes alvo ou expandir para todas as 80 do COCO com uma flag simples (`--all-classes`)

- **Paleta de cores consistente** — cada classe sempre aparece com a mesma cor, facilitando a interpretação visual

- **Logging estruturado** — substitui `print()` por `logging` com níveis e escrita em arquivo

- **Testes unitários** — cobertura com `pytest` de todos os módulos principais

---

## 🔬 Como funciona internamente

```
Imagem de entrada
      │
      ▼
  Resize (640px largura)
      │
      ▼
  YOLOv8 forward pass (única passagem)
      │
      ▼
  NMS (Non-Maximum Suppression) — remove sobreposições
      │
      ▼
  Filtro de classes alvo (person | laptop | cell phone)
      │
      ▼
  Bounding boxes + labels + cores
      │
      ▼
  Imagem anotada final
```

---

## 📦 Dependências

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `ultralytics` | 8.0.0 | YOLOv8 — detecção, inferência, modelos pré-treinados |
| `opencv-python` | 4.9.0 | Leitura de imagens/vídeo, desenho, webcam |
| `numpy` | 1.26.0 | Operações matriciais |
| `pytest` | 8.0.0 | Testes unitários |
| `pytest-cov` | 5.0.0 | Relatório de cobertura |

> O `ultralytics` instala automaticamente `torch`, `torchvision` e `pillow` como dependências.

---

## ❓ Solução de Problemas (FAQ)

**"ModuleNotFoundError: No module named 'src'"**
→ Execute os scripts sempre a partir da **raiz do projeto** (onde está `detect.py`), não de dentro de `src/`.

**Webcam não abre (`Não foi possível abrir a webcam`)**
→ Verifique se outra aplicação está usando a câmera. Tente `--camera 1` se houver mais de uma câmera.

**Detecções muito sensíveis (muitos objetos falsos)**
→ Aumente a confiança: `--confidence 0.6`

**Detecções faltando objetos visíveis**
→ Reduza a confiança: `--confidence 0.3`

**Lentidão no processamento**
→ Use o modelo nano (padrão): `--model yolov8n.pt` e reduza a largura: `--width 416`

---

## 🗺️ Roadmap

- [ ] Suporte a detecção em vídeos (`--video arquivo.mp4`)
- [ ] Export de resultados em JSON com coordenadas dos objetos
- [ ] Interface web com FastAPI + StreamLit
- [ ] Fine-tuning customizado com dataset próprio
- [ ] Suporte a GPU via CUDA

---

## 📚 Referências

- [YOLOv8 — Ultralytics Docs](https://docs.ultralytics.com/)
- [COCO Dataset](https://cocodataset.org/#home)
- [You Only Look Once — Redmon et al., 2015](https://arxiv.org/abs/1506.02640)
- [YOLOv8 GitHub](https://github.com/ultralytics/ultralytics)


---

## 📄 Licença

Distribuído sob a licença **MIT**.