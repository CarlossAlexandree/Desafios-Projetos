# Mask R-CNN — Segmentação de Imagens 🐶🖼️

Este repositório contém um notebook (`Mask_R_CNN_(segmentação_de_imagens).ipynb`) que demonstra o uso do Mask R-CNN disponível em `torchvision` para inferência de segmentação de instâncias.

O notebook realiza o fluxo completo: download de uma imagem de exemplo, carregamento do modelo `maskrcnn_resnet50_fpn` com pesos pré-treinados no COCO, inferência, e visualização/salvamento das máscaras sobre a imagem.

## 🔎 O que há no notebook
- Download robusto de uma imagem (`test.jpg`) a partir de URLs alternativas
- Carregamento do modelo `maskrcnn_resnet50_fpn` com `MaskRCNN_ResNet50_FPN_Weights.DEFAULT`
- Pré-processamento usando as transforms do próprio `weights`
- Inferência com PyTorch (CPU/GPU automático)
- Extração de `boxes`, `labels`, `scores` e `masks`
- Funções utilitárias para aplicar máscaras e desenhar detecções
- Saída salva em `test_results.jpg`

## 🧾 Arquivos principais
- `Mask_R_CNN_(segmentação_de_imagens).ipynb` — notebook principal (executável)
- `README.md` — este arquivo

## ⚙️ Requisitos
- Python 3.8+ recomendado
- Dependências principais (exemplo):
  - torch
  - torchvision
  - pillow
  - matplotlib
  - numpy

Instale via pip (recomendo criar um virtualenv/venv):

```bash
pip install torch torchvision pillow matplotlib numpy
```

Observação: para treinar ou executar mais rápido, utilize uma GPU com CUDA configurado.

## ▶️ Como executar

Opção 1 — Abrir e executar no Jupyter/VS Code/Colab (recomendado):

1. Abra `Mask_R_CNN_(segmentação_de_imagens).ipynb` no Jupyter Notebook, JupyterLab ou VS Code.
2. Execute as células sequencialmente (ou `Run All`).

Opção 2 — Executar headless (executa todas as células):

```bash
jupyter nbconvert --to notebook --execute "Mask_R_CNN_(segmentação_de_imagens).ipynb" --ExecutePreprocessor.timeout=600
```

Ao final, o notebook cria/atualiza os arquivos:
- `test.jpg` — imagem baixada usada como entrada
- `test_results.jpg` — imagem anotada com máscaras e boxes

## 🔧 Personalização rápida
- Para usar sua própria imagem, substitua `image_path = 'test.jpg'` pelo caminho da sua imagem ou modifique a lista de URLs.
- Para alterar sensibilidade: ajuste `min_score_thresh`, `mask_threshold` e `max_boxes_to_draw` nas células de inferência/visualização.

## 📌 Observações técnicas
- O notebook usa `MaskRCNN_ResNet50_FPN_Weights.DEFAULT`, que já aplica as transforms recomendadas — use `weights.transforms()` para consistência.
- O modelo retorna máscaras em formato `N x 1 x H x W` com probabilidades por pixel; as máscaras são binarizadas com um `mask_threshold` antes de desenhar.

## 🧪 Resultados esperados
- Ao executar, você verá o número de detecções, as top-scores e a imagem anotada salva em `test_results.jpg`.


---