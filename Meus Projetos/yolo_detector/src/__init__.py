"""yolo_detector.src — pacote de módulos internos."""

from .detector import CLASS_COLORS, TARGET_CLASSES, Detection, DetectionConfig, YOLODetector
from .image_utils import list_images, load_image, resize_image, save_image
from .logger_config import setup_logging
from .visualizer import draw_detections, draw_fps

__all__ = [
    # Detector
    "YOLODetector", "DetectionConfig", "Detection",
    "TARGET_CLASSES", "CLASS_COLORS",
    # Visualizador
    "draw_detections", "draw_fps",
    # Utilitários
    "load_image", "resize_image", "save_image", "list_images",
    # Logging
    "setup_logging",
]