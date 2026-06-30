"""
detector.py
-----------
Módulo principal de detecção facial usando SSD (Single Shot Detector)
com backbone ResNet-10 via OpenCV DNN.
"""

import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class DetectionConfig:
    """Configurações do detector facial."""
    confidence_threshold: float = 0.5
    input_size: tuple[int, int] = (300, 300)
    mean_subtraction: tuple[float, float, float] = (104.0, 177.0, 123.0)
    scale_factor: float = 1.0
    resize_width: int = 400
    box_color: tuple[int, int, int] = (0, 255, 0)
    box_thickness: int = 2
    font_scale: float = 0.45
    font: int = cv2.FONT_HERSHEY_SIMPLEX


@dataclass
class DetectionResult:
    """Resultado de uma detecção individual."""
    confidence: float
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    label: str = field(init=False)

    def __post_init__(self) -> None:
        self.label = f"{self.confidence * 100:.2f}%"

    @property
    def box(self) -> tuple[int, int, int, int]:
        return (self.start_x, self.start_y, self.end_x, self.end_y)


class FaceDetector:
    """
    Detector facial baseado em SSD com backbone ResNet-10.

    Utiliza modelo pré-treinado do OpenCV DNN para detecção
    eficiente em tempo real.

    Parâmetros
    ----------
    prototxt_path : Path | str
        Caminho para o arquivo de arquitetura deploy.prototxt.
    model_path : Path | str
        Caminho para os pesos do modelo .caffemodel.
    config : DetectionConfig, opcional
        Configurações customizadas de detecção.
    """

    def __init__(
        self,
        prototxt_path: Path | str,
        model_path: Path | str,
        config: Optional[DetectionConfig] = None,
    ) -> None:
        self.config = config or DetectionConfig()
        self._net = self._load_model(Path(prototxt_path), Path(model_path))

    # ------------------------------------------------------------------
    # Inicialização
    # ------------------------------------------------------------------

    @staticmethod
    def _load_model(prototxt: Path, model: Path) -> cv2.dnn.Net:
        """Carrega e valida o modelo SSD via OpenCV DNN."""
        if not prototxt.exists():
            raise FileNotFoundError(f"Prototxt não encontrado: {prototxt}")
        if not model.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {model}")

        logger.info("Carregando modelo SSD de '%s'", model)
        net = cv2.dnn.readNetFromCaffe(str(prototxt), str(model))
        logger.info("Modelo carregado com sucesso.")
        return net

    # ------------------------------------------------------------------
    # Detecção
    # ------------------------------------------------------------------

    def detect(self, image: np.ndarray) -> list[DetectionResult]:
        """
        Executa a detecção facial em uma imagem.

        Parâmetros
        ----------
        image : np.ndarray
            Imagem BGR lida com OpenCV.

        Retorna
        -------
        list[DetectionResult]
            Lista de detecções com confiança acima do threshold.
        """
        if image is None or image.size == 0:
            raise ValueError("Imagem inválida ou vazia.")

        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, self.config.input_size),
            self.config.scale_factor,
            self.config.input_size,
            self.config.mean_subtraction,
        )

        self._net.setInput(blob)
        raw_detections = self._net.forward()

        return self._parse_detections(raw_detections, w, h)

    def _parse_detections(
        self,
        raw: np.ndarray,
        width: int,
        height: int,
    ) -> list[DetectionResult]:
        """Filtra e converte as detecções brutas da rede."""
        results: list[DetectionResult] = []
        num_detections = raw.shape[2]

        for i in range(num_detections):
            confidence = float(raw[0, 0, i, 2])
            if confidence < self.config.confidence_threshold:
                continue

            box = raw[0, 0, i, 3:7] * np.array([width, height, width, height])
            start_x, start_y, end_x, end_y = box.astype("int")

            # Garante coordenadas dentro dos limites da imagem
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(width, end_x)
            end_y = min(height, end_y)

            results.append(
                DetectionResult(
                    confidence=confidence,
                    start_x=start_x,
                    start_y=start_y,
                    end_x=end_x,
                    end_y=end_y,
                )
            )
            logger.debug("Face detectada com %.2f%% de confiança.", confidence * 100)

        logger.info("%d face(s) detectada(s).", len(results))
        return results

    # ------------------------------------------------------------------
    # Visualização
    # ------------------------------------------------------------------

    def draw(self, image: np.ndarray, detections: list[DetectionResult]) -> np.ndarray:
        """
        Desenha os bounding boxes e labels na imagem.

        Parâmetros
        ----------
        image : np.ndarray
            Imagem BGR original.
        detections : list[DetectionResult]
            Detecções retornadas por `detect()`.

        Retorna
        -------
        np.ndarray
            Imagem anotada (cópia).
        """
        annotated = image.copy()
        cfg = self.config

        for det in detections:
            y_label = det.start_y - 10 if det.start_y - 10 > 10 else det.start_y + 10

            cv2.rectangle(
                annotated,
                (det.start_x, det.start_y),
                (det.end_x, det.end_y),
                cfg.box_color,
                cfg.box_thickness,
            )
            cv2.putText(
                annotated,
                det.label,
                (det.start_x, y_label),
                cfg.font,
                cfg.font_scale,
                cfg.box_color,
                cfg.box_thickness,
            )

        return annotated