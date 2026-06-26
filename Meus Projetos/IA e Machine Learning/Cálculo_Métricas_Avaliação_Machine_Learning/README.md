# 📊 Cálculo de Métricas de Avaliação de Aprendizado de Máquina

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Colab](https://colab.research.google.com/assets/colab-badge.svg)

## 📌 Sobre o Projeto

Implementação e cálculo manual das principais métricas de avaliação de modelos de classificação, aplicadas a uma CNN treinada no dataset MNIST. As métricas são calculadas a partir da Matriz de Confusão utilizando as fórmulas da Tabela 1 do enunciado do projeto.

## 🎯 Métricas Implementadas

| Métrica | Fórmula |
|---|---|
| Sensibilidade (Recall) | VP / (VP + FN) |
| Especificidade | VN / (FP + VN) |
| Acurácia | (VP + VN) / N |
| Precisão | VP / (VP + FP) |
| F-Score | 2 × (P × S) / (P + S) |

> VP: Verdadeiro Positivo | VN: Verdadeiro Negativo | FP: Falso Positivo | FN: Falso Negativo | N: Total

## 🗂️ Estrutura do Projeto
```
metricas-avaliacao-ml/

├── metricas_avaliacao.ipynb   ← notebook principal

├── metricas_avaliacao.csv     ← tabela de resultados exportada

├── confusion_matrix.png       ← matriz de confusão

├── metricas_por_classe.png    ← gráficos das métricas

├── learning_curves.png        ← curvas de aprendizado

└── README.md
```
## 🧠 Modelo Utilizado

- **Arquitetura:** CNN (Convolutional Neural Network)
- **Dataset:** MNIST (70.000 imagens de dígitos 0–9)
- **Framework:** TensorFlow / Keras
- **Ambiente:** Google Colab (GPU T4)

## 📈 Resultados

Acurácia geral do modelo superior a **99%** no conjunto de teste, com métricas calculadas individualmente para cada uma das 10 classes usando a abordagem **One-vs-Rest**.


## 🛠️ Tecnologias

- Python 3.x
- TensorFlow 2.x / Keras
- NumPy · Pandas · Matplotlib · Seaborn · Scikit-learn

