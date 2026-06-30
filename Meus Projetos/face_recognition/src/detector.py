"""
detector.py
-----------
Módulo de DETECÇÃO facial — Rede 1 do projeto.

Usa SSD (Single Shot Detector) + ResNet-10 via OpenCV DNN (Caffe).
Responsabilidade: localizar ONDE estão os rostos na imagem.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class DetectionConfig:
    """Parâmetros de configuração do detector SSD."""
    confidence_threshold: float = 0.5
    input_size: tuple = (300, 300)
    mean_subtraction: tuple = (104.0, 177.0, 123.0)
    scale_factor: float = 1.0
    resize_width: int = 600
    box_thickness: int = 2
    font_scale: float = 0.6
    padding: int = 20   # pixels extras ao recortar o rosto para o classificador


@dataclass
class FaceROI:
    """
    Região de interesse de um rosto detectado (bounding box).

    Atributos
    ---------
    confidence  : float   Confiança da detecção (0–1).
    start_x/y   : int     Canto superior esquerdo do bounding box.
    end_x/y     : int     Canto inferior direito do bounding box.
    """
    confidence: float
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    detection_label: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.detection_label = f"{self.confidence * 100:.1f}%"

    @property
    def box(self) -> tuple:
        return (self.start_x, self.start_y, self.end_x, self.end_y)

    @property
    def width(self) -> int:
        return self.end_x - self.start_x

    @property
    def height(self) -> int:
        return self.end_y - self.start_y

    def crop(self, image: np.ndarray, padding: int = 0) -> np.ndarray:
        """Recorta o rosto da imagem com padding opcional."""
        h, w = image.shape[:2]
        x1 = max(0, self.start_x - padding)
        y1 = max(0, self.start_y - padding)
        x2 = min(w, self.end_x + padding)
        y2 = min(h, self.end_y + padding)
        return image[y1:y2, x1:x2]


class FaceDetector:
    """
    Detector facial — Rede 1.

    Usa SSD + ResNet-10 (modelo Caffe, carregado via OpenCV DNN).
    Detecta ONDE estão os rostos sem identificar quem são.

    Parâmetros
    ----------
    prototxt_path : str | Path   Arquivo de arquitetura deploy.prototxt.
    model_path    : str | Path   Pesos do modelo .caffemodel.
    config        : DetectionConfig  (opcional)
    """

    def __init__(
        self,
        prototxt_path,
        model_path,
        config: Optional[DetectionConfig] = None,
    ) -> None:
        self.config = config or DetectionConfig()
        self._net = self._load_model(Path(prototxt_path), Path(model_path))

    @staticmethod
    def _load_model(prototxt: Path, model: Path) -> cv2.dnn.Net:
        for p in (prototxt, model):
            if not p.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {p}")
        logger.info("Carregando detector SSD de '%s'", model.name)
        net = cv2.dnn.readNetFromCaffe(str(prototxt), str(model))
        logger.info("Detector SSD pronto.")
        return net

    def detect(self, image: np.ndarray) -> list:
        """
        Detecta rostos em uma imagem BGR.

        Retorna lista de FaceROI com confiança acima do threshold.
        """
        if image is None or image.size == 0:
            raise ValueError("Imagem inválida.")

        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, self.config.input_size),
            self.config.scale_factor,
            self.config.input_size,
            self.config.mean_subtraction,
        )
        self._net.setInput(blob)
        raw = self._net.forward()

        results = []
        for i in range(raw.shape[2]):
            conf = float(raw[0, 0, i, 2])
            if conf < self.config.confidence_threshold:
                continue
            box = raw[0, 0, i, 3:7] * np.array([w, h, w, h])
            sx, sy, ex, ey = box.astype("int")
            results.append(FaceROI(
                confidence=conf,
                start_x=max(0, sx),
                start_y=max(0, sy),
                end_x=min(w, ex),
                end_y=min(h, ey),
            ))

        logger.debug("%d face(s) detectada(s).", len(results))
        return results