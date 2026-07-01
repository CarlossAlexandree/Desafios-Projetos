"""
visualizer.py
-------------
Módulo de visualização — desenha bounding boxes e labels nas imagens.

Responsabilidade única: dado uma imagem e lista de Detection,
retornar a imagem anotada com visual profissional.
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def draw_detections(
    image: np.ndarray,
    detections: list,
    thickness: int = 2,
    font_scale: float = 0.6,
    show_count: bool = True,
) -> np.ndarray:
    """
    Desenha bounding boxes e labels de todas as detecções na imagem.

    Parâmetros
    ----------
    image      : np.ndarray   Imagem BGR original.
    detections : list[Detection]  Detecções retornadas pelo YOLODetector.
    thickness  : int          Espessura das linhas.
    font_scale : float        Tamanho da fonte.
    show_count : bool         Exibe contador de objetos no canto superior.

    Retorna
    -------
    np.ndarray  Imagem anotada (cópia).
    """
    annotated = image.copy()

    for det in detections:
        color = det.color

        # Bounding box
        cv2.rectangle(
            annotated,
            (det.x1, det.y1),
            (det.x2, det.y2),
            color,
            thickness,
        )

        # Fundo do label
        (text_w, text_h), baseline = cv2.getTextSize(
            det.label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )
        y_label = det.y1 - 8 if det.y1 - 8 > text_h + 4 else det.y1 + text_h + 8

        cv2.rectangle(
            annotated,
            (det.x1, y_label - text_h - baseline - 2),
            (det.x1 + text_w + 4, y_label + 2),
            color,
            cv2.FILLED,
        )

        # Texto branco sobre fundo colorido
        cv2.putText(
            annotated,
            det.label,
            (det.x1 + 2, y_label - baseline),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            thickness,
        )

    # Contador de objetos por classe no canto superior esquerdo
    if show_count and detections:
        counts = {}
        for det in detections:
            counts[det.class_name] = counts.get(det.class_name, 0) + 1

        y_pos = 28
        for class_name, count in sorted(counts.items()):
            from src.detector import CLASS_COLORS
            color = CLASS_COLORS.get(class_name, CLASS_COLORS["default"])
            text = f"{class_name}: {count}"
            cv2.putText(
                annotated, text,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, color, 2,
            )
            y_pos += 28

    return annotated


def draw_fps(image: np.ndarray, fps: float) -> np.ndarray:
    """Desenha o FPS no canto superior direito da imagem."""
    h, w = image.shape[:2]
    text = f"FPS: {fps:.1f}"
    (text_w, text_h), _ = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2
    )
    cv2.putText(
        image, text,
        (w - text_w - 10, text_h + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 255), 2,
    )
    return image