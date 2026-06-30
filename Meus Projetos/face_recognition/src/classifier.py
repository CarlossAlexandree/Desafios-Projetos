"""
classifier.py
-------------
Módulo de RECONHECIMENTO facial — Rede 2 do projeto.

Usa MobileNetV2 (Transfer Learning) via TensorFlow/Keras.
Responsabilidade: dado o recorte de um rosto já detectado,
identificar QUEM é a pessoa e com qual confiança.

Fluxo de Transfer Learning:
  Fase 1 — Fine-Tuning rápido:
      Base MobileNetV2 congelada + Dense(softmax) treinada do zero.
  Fase 2 — Fine-Tuning profundo:
      Descongelamento das últimas 30 camadas da base + LR menor.
"""

import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
    from tensorflow import keras
    _TF_OK = True
except ImportError:
    _TF_OK = False
    logger.warning("TensorFlow não instalado. Classificador indisponível.")

# Tamanho de entrada do MobileNetV2
IMG_SIZE = (224, 224)
UNKNOWN_LABEL = "Desconhecido"


# ─────────────────────────────────────────────────────────────
# Construção do modelo
# ─────────────────────────────────────────────────────────────

def build_model(num_classes: int, dropout: float = 0.4):
    """
    Constrói o classificador com MobileNetV2 como backbone (Transfer Learning).

    Arquitetura:
        MobileNetV2 pré-treinado (ImageNet) — camadas congeladas
        → GlobalAveragePooling2D
        → Dropout(dropout)
        → Dense(num_classes, activation='softmax')

    Parâmetros
    ----------
    num_classes : int    Número de identidades a classificar.
    dropout     : float  Taxa de dropout (padrão 0.4).

    Retorna
    -------
    keras.Model  Modelo compilado, pronto para treino (Fase 1).
    """
    if not _TF_OK:
        raise RuntimeError("TensorFlow não está instalado.")

    # Backbone: MobileNetV2 pré-treinado no ImageNet
    base = keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False  # congela na Fase 1

    inputs = keras.Input(shape=(*IMG_SIZE, 3))
    x = keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(dropout)(x)
    outputs = keras.layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="face_recognizer")
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    trainable_params = sum(
        int(tf.size(v).numpy()) for v in model.trainable_variables
    )
    logger.info(
        "Modelo criado: MobileNetV2 + Dense(%d) | Parâmetros treináveis: %d",
        num_classes, trainable_params,
    )
    return model


def _find_backbone_layer(model):
    """Localiza a camada MobileNetV2 dentro do modelo pelo nome, não pelo índice."""
    for layer in model.layers:
        if "mobilenetv2" in layer.name.lower():
            return layer
    raise ValueError("Camada MobileNetV2 não encontrada no modelo.")


def unfreeze_top_layers(model, num_layers: int = 30):
    """
    Descongela as últimas `num_layers` camadas do backbone (Fase 2 — Fine-Tuning).

    Parâmetros
    ----------
    model      : keras.Model  Modelo treinado na Fase 1.
    num_layers : int          Camadas do topo a descongelar (padrão 30).

    Retorna
    -------
    keras.Model  Recompilado com learning rate menor para fine-tuning.
    """
    if not _TF_OK:
        raise RuntimeError("TensorFlow não está instalado.")

    base = _find_backbone_layer(model)
    base.trainable = True

    for layer in base.layers[:-num_layers]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),  # LR menor no fine-tuning
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    trainable_params = sum(
        int(tf.size(v).numpy()) for v in model.trainable_variables
    )
    logger.info(
        "Fine-tuning: %d camadas descongeladas | Params treináveis: %d",
        num_layers, trainable_params,
    )
    return model


# ─────────────────────────────────────────────────────────────
# Dataset
# ─────────────────────────────────────────────────────────────

def load_dataset(
    dataset_dir,
    batch_size: int = 32,
    validation_split: float = 0.2,
    seed: int = 42,
):
    """
    Carrega dataset organizado em subpastas (uma por pessoa).

    Estrutura esperada:
        dataset/train/
            joao/    foto1.jpg  foto2.jpg ...
            maria/   foto1.jpg  ...
            pedro/   foto1.jpg  ...

    Parâmetros
    ----------
    dataset_dir      : str | Path  Pasta raiz do dataset.
    batch_size       : int
    validation_split : float       Fração para validação.
    seed             : int

    Retorna
    -------
    (train_ds, val_ds, class_names)
    """
    if not _TF_OK:
        raise RuntimeError("TensorFlow não está instalado.")

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="int",
    )
    val_ds = keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="int",
    )

    class_names = train_ds.class_names
    logger.info("Classes encontradas (%d): %s", len(class_names), class_names)

    # Data Augmentation apenas no treino
    augment = keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.12),
        keras.layers.RandomZoom(0.12),
        keras.layers.RandomBrightness(0.1),
        keras.layers.RandomContrast(0.1),
    ], name="augmentation")

    train_ds = (
        train_ds
        .map(lambda x, y: (augment(x, training=True), y),
             num_parallel_calls=AUTOTUNE)
        .cache()
        .shuffle(1000)
        .prefetch(AUTOTUNE)
    )
    val_ds = val_ds.cache().prefetch(AUTOTUNE)

    return train_ds, val_ds, class_names


# ─────────────────────────────────────────────────────────────
# Inferência
# ─────────────────────────────────────────────────────────────

class FaceClassifier:
    """
    Wrapper de inferência para o modelo treinado — Rede 2.

    Carrega o modelo salvo e realiza predição em recortes de rosto.

    Parâmetros
    ----------
    model_path   : str | Path   Arquivo .keras salvo pelo treinamento.
    class_names  : list[str]    Nomes das classes (mesma ordem do treino).
    threshold    : float        Confiança mínima para aceitar predição (padrão 0.60).
    """

    def __init__(self, model_path, class_names: list, threshold: float = 0.60) -> None:
        if not _TF_OK:
            raise RuntimeError("TensorFlow não está instalado.")
        self.class_names = class_names
        self.threshold = threshold
        self._model = self._load(Path(model_path))

    def _load(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {path}")
        logger.info("Carregando classificador de '%s'", path.name)
        model = keras.models.load_model(str(path))
        logger.info("Classificador pronto. Classes: %s", self.class_names)
        return model

    def predict(self, face_bgr: np.ndarray) -> tuple:
        """
        Classifica um recorte de rosto BGR.

        Parâmetros
        ----------
        face_bgr : np.ndarray  Imagem BGR do rosto (qualquer tamanho).

        Retorna
        -------
        (nome: str, confiança: float)
        Se confiança < threshold, retorna (UNKNOWN_LABEL, confiança).
        """
        import cv2 as _cv2
        rgb = _cv2.cvtColor(face_bgr, _cv2.COLOR_BGR2RGB)
        resized = _cv2.resize(rgb, IMG_SIZE)
        tensor = tf.expand_dims(tf.cast(resized, tf.float32), 0)

        probs = self._model(tensor, training=False).numpy()[0]
        idx = int(np.argmax(probs))
        confidence = float(probs[idx])

        if confidence < self.threshold:
            return UNKNOWN_LABEL, confidence

        return self.class_names[idx], confidence

    @classmethod
    def from_dir(cls, model_dir, threshold: float = 0.60):
        """
        Carrega o classificador de uma pasta que contém:
          - face_recognizer.keras
          - class_names.json

        Parâmetros
        ----------
        model_dir : str | Path  Pasta com os artefatos do modelo.
        threshold : float
        """
        model_dir = Path(model_dir)
        model_path = model_dir / "face_recognizer.keras"
        names_path = model_dir / "class_names.json"

        if not names_path.exists():
            raise FileNotFoundError(f"class_names.json não encontrado em {model_dir}")

        with open(names_path, "r", encoding="utf-8") as f:
            class_names = json.load(f)

        return cls(model_path, class_names, threshold)