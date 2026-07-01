"""
tests/test_detector.py
-----------------------
Testes unitários para o módulo detector.py (YOLOv8).
Execute com: pytest tests/
"""

import numpy as np
import pytest

from src.detector import (
    CLASS_COLORS,
    TARGET_CLASSES,
    Detection,
    DetectionConfig,
    YOLODetector,
)


class TestDetectionConfig:
    def test_default_confidence(self):
        cfg = DetectionConfig()
        assert cfg.confidence_threshold == 0.40

    def test_default_target_classes(self):
        cfg = DetectionConfig()
        assert "person" in cfg.target_classes
        assert "laptop" in cfg.target_classes
        assert "cell phone" in cfg.target_classes

    def test_custom_confidence(self):
        cfg = DetectionConfig(confidence_threshold=0.7)
        assert cfg.confidence_threshold == 0.7

    def test_filter_classes_default_true(self):
        cfg = DetectionConfig()
        assert cfg.filter_classes is True


class TestDetection:
    def test_label_format(self):
        det = Detection(
            class_name="person",
            confidence=0.923,
            x1=10, y1=20, x2=100, y2=200,
        )
        assert det.label == "person (92.3%)"

    def test_box_property(self):
        det = Detection("laptop", 0.8, 5, 10, 50, 80)
        assert det.box == (5, 10, 50, 80)

    def test_width_height(self):
        det = Detection("cell phone", 0.75, 0, 0, 60, 120)
        assert det.width == 60
        assert det.height == 120

    def test_area(self):
        det = Detection("person", 0.9, 0, 0, 100, 200)
        assert det.area == 20000

    def test_color_person(self):
        det = Detection("person", 0.9, 0, 0, 100, 100)
        assert det.color == CLASS_COLORS["person"]

    def test_color_unknown_class(self):
        det = Detection("unknown_class", 0.5, 0, 0, 10, 10)
        assert det.color == CLASS_COLORS["default"]


class TestTargetClasses:
    def test_target_classes_content(self):
        assert TARGET_CLASSES == {"person", "laptop", "cell phone"}

    def test_class_colors_have_all_targets(self):
        for cls in TARGET_CLASSES:
            assert cls in CLASS_COLORS, f"Cor não definida para: {cls}"

    def test_class_colors_are_bgr_tuples(self):
        for cls, color in CLASS_COLORS.items():
            assert len(color) == 3, f"Cor inválida para {cls}: {color}"
            for val in color:
                assert 0 <= val <= 255


class TestYOLODetectorInit:
    def test_missing_ultralytics_raises(self, monkeypatch):
        """Garante que RuntimeError é levantado sem ultralytics instalado."""
        import builtins
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "ultralytics":
                raise ImportError("No module named 'ultralytics'")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        with pytest.raises(RuntimeError, match="Ultralytics não instalado"):
            detector = YOLODetector.__new__(YOLODetector)
            detector.config = DetectionConfig()
            detector._load_model("yolov8n.pt")


class TestYOLODetectorDetect:
    def test_invalid_image_raises(self):
        detector = YOLODetector.__new__(YOLODetector)
        detector.config = DetectionConfig()
        detector._model = None
        with pytest.raises(ValueError, match="Imagem inválida"):
            detector.detect(np.array([]))

    def test_empty_image_raises(self):
        detector = YOLODetector.__new__(YOLODetector)
        detector.config = DetectionConfig()
        detector._model = None
        with pytest.raises(ValueError):
            detector.detect(None)