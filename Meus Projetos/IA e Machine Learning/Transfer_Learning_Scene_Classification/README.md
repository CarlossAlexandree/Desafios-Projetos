# Transfer Learning — Scene Classification

Projeto de classificação de imagens usando Transfer Learning com VGG16.

## Dataset
Intel Image Classification — 6 classes: buildings, forest, glacier, mountain, sea, street

## Abordagem
- **Baseline:** CNN treinada do zero
- **Transfer Learning:** VGG16 pré-treinado (ImageNet) + Feature Extraction
- **Fine-Tuning:** Ajuste fino das últimas camadas convolucionais

## Resultados
| Modelo | Acurácia |
|---|---|
| Baseline CNN | 85.40% |
| Transfer Learning + Fine-Tuning | 90.40% |

## Como executar
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1vaqBd82wi7XVOeb-2HaA9JoBfsq7J_76#scrollTo=IJMQs_ExcBmW)

## Tecnologias
Python · TensorFlow/Keras · VGG16 · Google Colab (GPU T4)