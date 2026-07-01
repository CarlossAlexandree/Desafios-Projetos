"""
detector.py
-----------
Módulo principal de detecção de objetos usando YOLOv8 (Ultralytics).

Classes alvo deste projeto:
  - person     (pessoa)
  - laptop     (notebook)
  - cell phone (celular)

Responsabilidade única: dado uma imagem ou frame, retornar
os objetos detectados com suas caixas, labels e confianças.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Classes alvo do projeto (subconjunto das 80 classes COCO)
TARGET_CLASSES = {"person", "laptop", "cell phone"}

# Paleta de cores BGR por classe
CLASS_COLORS = {
    "person":     (0,   165, 255),   # laranja
    "laptop":     (0,   255, 0),     # verde
    "cell phone": (255, 0,   0),     # azul
    "default":    (128, 128, 128),   # cinza para outras classes
}


@dataclass
class DetectionConfig:
    """Parâmetros de configuração do detector YOLOv8."""
    confidence_threshold: float = 0.40
    iou_threshold: float = 0.45
    resize_width: int = 640
    target_classes: set = field(default_factory=lambda: TARGET_CLASSES.copy())
    filter_classes: bool = True    # Se True, mostra apenas as classes alvo
    box_thickness: int = 2
    font_scale: float = 0.6


@dataclass
class Detection:
    """Resultado de uma detecção individual."""
    class_name: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int
    label: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.label = f"{self.class_name} ({self.confidence * 100:.1f}%)"

    @property
    def box(self) -> tuple:
        return (self.x1, self.y1, self.x2, self.y2)

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def color(self) -> tuple:
        return CLASS_COLORS.get(self.class_name, CLASS_COLORS["default"])


class YOLODetector:
    """
    Detector de objetos baseado em YOLOv8 (Ultralytics).

    Utiliza Transfer Learning sobre o modelo pré-treinado no COCO,
    focando nas classes: person, laptop, cell phone.

    Parâmetros
    ----------
    model_path : str | Path
        Caminho para o arquivo .pt do YOLOv8.
        Use 'yolov8n.pt' para nano (mais rápido) ou
        'yolov8s.pt' para small (mais preciso).
    config : DetectionConfig, opcional
        Configurações customizadas.
    """

    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        config: Optional[DetectionConfig] = None,
    ) -> None:
        self.config = config or DetectionConfig()
        self._model = self._load_model(model_path)

    def _load_model(self, model_path: str):
        """Carrega o modelo YOLOv8 via Ultralytics."""
        try:
            from ultralytics import YOLO
        except ImportError:
            raise RuntimeError(
                "Ultralytics não instalado. Execute: pip install ultralytics"
            )

        logger.info("Carregando modelo YOLOv8 de '%s'...", model_path)
        model = YOLO(model_path)
        logger.info("Modelo YOLOv8 carregado. Classes disponíveis: %d", len(model.names))
        return model

    @property
    def class_names(self) -> dict:
        """Dicionário {id: nome} de todas as classes do modelo."""
        return self._model.names

    def detect(self, image: np.ndarray) -> list:
        """
        Executa detecção de objetos em uma imagem BGR.

        Parâmetros
        ----------
        image : np.ndarray
            Imagem BGR (lida com OpenCV).

        Retorna
        -------
        list[Detection]
            Lista de detecções filtradas pelas classes alvo.
        """
        if image is None or image.size == 0:
            raise ValueError("Imagem inválida.")

        results = self._model(
            image,
            conf=self.config.confidence_threshold,
            iou=self.config.iou_threshold,
            verbose=False,
        )

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self._model.names[class_id]

                # Filtra apenas classes alvo se configurado
                if self.config.filter_classes:
                    if class_name not in self.config.target_classes:
                        continue

                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append(Detection(
                    class_name=class_name,
                    confidence=confidence,
                    x1=max(0, x1),
                    y1=max(0, y1),
                    x2=x2,
                    y2=y2,
                ))

        logger.debug(
            "%d objeto(s) detectado(s): %s",
            len(detections),
            [d.class_name for d in detections],
        )
        return detections

    def detect_all_classes(self, image: np.ndarray) -> list:
        """
        Detecta objetos de TODAS as classes COCO (sem filtro).
        Útil para demonstração completa do modelo pré-treinado.
        """
        original_filter = self.config.filter_classes
        self.config.filter_classes = False
        detections = self.detect(image)
        self.config.filter_classes = original_filter
        return detections