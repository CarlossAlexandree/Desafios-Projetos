"""face_recognition.src — pacote de módulos internos."""

from .classifier import FaceClassifier, build_model, load_dataset, unfreeze_top_layers
from .detector import DetectionConfig, FaceDetector, FaceROI
from .image_utils import (
    draw_recognition, get_color_for_name,
    load_image, resize_image, save_image,
)
from .logger_config import setup_logging

__all__ = [
    # Rede 1 — Detecção
    "DetectionConfig", "FaceDetector", "FaceROI",
    # Rede 2 — Reconhecimento (TensorFlow)
    "FaceClassifier", "build_model", "load_dataset", "unfreeze_top_layers",
    # Utilitários
    "draw_recognition", "get_color_for_name",
    "load_image", "resize_image", "save_image",
    # Logging
    "setup_logging",
]