# 🎯 Face Detector Human SSD

> Detecção facial em imagens usando **SSD (Single Shot Detector)** com backbone **ResNet-10** via **OpenCV DNN** — rápido, preciso e pronto para produção.

---

## 📌 Sobre o Projeto

Este projeto implementa um detector facial baseado em **aprendizado profundo**, utilizando o modelo **SSD + ResNet-10** pré-treinado disponibilizado pelo OpenCV. Ele é capaz de localizar um ou múltiplos rostos em uma imagem, exibindo a porcentagem de confiança de cada detecção diretamente sobre a imagem anotada.

### 🔍 O que é o SSD?

O **Single Shot Multibox Detector (SSD)** é uma arquitetura de detecção de objetos em tempo real que realiza a localização e classificação em uma **única passagem** pela rede neural, sem a necessidade de uma etapa separada de proposta de regiões (como nas redes Faster R-CNN). Isso o torna significativamente mais rápido e eficiente para aplicações práticas.

Neste projeto, o SSD utiliza o **ResNet-10** como extrator de características e foi treinado com o **Caffe framework**, sendo carregado diretamente pelo módulo `cv2.dnn` do OpenCV.

---

## 🗂️ Estrutura do Projeto

```
Face_Detector_Human_com_SSD/
│
├── 📁 models/                  # Modelos pré-treinados (baixar com o script)
│   ├── deploy.prototxt         # Arquitetura da rede SSD
│   └── res10_300x300_ssd_iter_140000.caffemodel
│
├── 📁 output/                  # Imagens processadas e logs gerados
│
├── 📁 scripts/
│   └── download_model.py       # Script para baixar os modelos automaticamente
│
├── 📁 src/                     # Código-fonte principal
│   ├── __init__.py
│   ├── detector.py             # Classes FaceDetector, DetectionConfig, DetectionResult
│   ├── image_utils.py          # Utilitários de I/O e redimensionamento de imagens
│   └── logger_config.py        # Configuração centralizada de logging
│
├── 📁 tests/                   # Testes unitários
│   ├── __init__.py
│   ├── test_detector.py
│   └── test_image_utils.py
│
├── main.py                     # Ponto de entrada da aplicação (CLI)
├── pyproject.toml              # Metadados e configuração do projeto
├── requirements.txt            # Dependências
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

- **Python 3.11+**
- **VS Code** (recomendado) com a extensão [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- `pip` atualizado

---


## 🖼️ Uso

### Comando básico

```bash
python main.py --image assets/photo.jpg
```

### Com opções avançadas

```bash
python main.py \
  --image assets/photo.jpg \
  --output output/resultado.jpg \
  --confidence 0.6 \
  --width 600 \
  --debug
```

### Parâmetros disponíveis

| Parâmetro       | Atalho | Padrão                    | Descrição                                           |
|-----------------|--------|---------------------------|-----------------------------------------------------|
| `--image`       | `-i`   | *(obrigatório)*           | Caminho para a imagem de entrada                    |
| `--output`      | `-o`   | `output/resultado.jpg`    | Caminho para salvar a imagem anotada                |
| `--confidence`  | `-c`   | `0.5`                     | Confiança mínima para aceitar uma detecção (0–1)    |
| `--width`       | `-w`   | `400`                     | Largura de redimensionamento da imagem de entrada   |
| `--prototxt`    | —      | `models/deploy.prototxt`  | Caminho customizado para o arquivo prototxt         |
| `--model`       | —      | `models/res10_...model`   | Caminho customizado para o caffemodel               |
| `--debug`       | —      | `False`                   | Ativa logs detalhados no nível DEBUG                |

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

Este projeto foi estruturado seguindo princípios de **Clean Code** e **SOLID**:

- **Separação de responsabilidades** — cada módulo tem uma única função bem definida:
  - `detector.py` → lógica de detecção e visualização
  - `image_utils.py` → I/O e manipulação de imagens
  - `logger_config.py` → configuração de logging
  - `main.py` → orquestração via CLI

- **Tipagem estática** — uso extensivo de *type hints* para segurança e autocompletar no VS Code

- **Dataclasses** — `DetectionConfig` e `DetectionResult` encapsulam dados com clareza

- **Tratamento de erros** — exceções explícitas (`FileNotFoundError`, `ValueError`) com mensagens descritivas

- **Logging estruturado** — em vez de `print()`, uso de `logging` com níveis e escrita em arquivo

- **Testes unitários** — cobertura das funções críticas com `pytest`, incluindo casos de borda

---

## 🔬 Como funciona a detecção

```
Imagem de entrada
      │
      ▼
  Redimensionar para 300×300 px
      │
      ▼
  Criar blob (normalização + mean subtraction)
      │
      ▼
  Forward pass na rede SSD + ResNet-10
      │
      ▼
  Filtrar detecções acima do threshold de confiança
      │
      ▼
  Calcular coordenadas dos bounding boxes
      │
      ▼
  Anotar imagem e salvar resultado
```

---

## 📦 Dependências

| Pacote            | Versão mínima | Finalidade                                      |
|-------------------|---------------|-------------------------------------------------|
| `opencv-python`   | 4.9.0         | Leitura de imagens, DNN, desenho de anotações   |
| `numpy`           | 1.26.0        | Operações matriciais sobre detecções            |
| `imutils`         | 0.5.4         | Utilitários de conveniência para OpenCV         |
| `pytest`          | 8.0.0         | Testes unitários                                |
| `pytest-cov`      | 5.0.0         | Relatório de cobertura de testes                |

---

## 🗺️ Roadmap

- [ ] Suporte a processamento de vídeos (`--video`)
- [ ] Interface web simples com FastAPI
- [ ] Modo batch para múltiplas imagens
- [ ] Export dos resultados em JSON
- [ ] Suporte a GPU via `cv2.dnn.DNN_TARGET_CUDA`

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

1. Faça um **fork** do projeto
2. Crie uma branch: `git checkout -b feat/minha-feature`
3. Commit suas mudanças: `git commit -m "feat: adiciona suporte a vídeo"`
4. Push: `git push origin feat/minha-feature`
5. Abra um **Pull Request**

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

---

## 🙏 Referências

- [OpenCV DNN Face Detector](https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector)
- [SSD: Single Shot MultiBox Detector — Liu et al., 2016](https://arxiv.org/abs/1512.02325)
- [OpenCV DNN Module Docs](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)