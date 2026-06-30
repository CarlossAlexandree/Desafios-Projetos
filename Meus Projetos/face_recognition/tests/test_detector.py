"""
tests/test_detector.py
-----------------------
Testes unitários para o módulo detector.py (Rede 1 — SSD).
Execute com: pytest tests/
"""

import numpy as np
import pytest

from src.detector import DetectionConfig, FaceDetector, FaceROI


@pytest.fixture
def default_config():
    return DetectionConfig()


@pytest.fixture
def dummy_image():
    return np.zeros((300, 300, 3), dtype=np.uint8)


class TestDetectionConfig:
    def test_default_confidence_threshold(self, default_config):
        assert default_config.confidence_threshold == 0.5

    def test_default_padding(self, default_config):
        assert default_config.padding == 20

    def test_custom_values(self):
        cfg = DetectionConfig(confidence_threshold=0.8, padding=10)
        assert cfg.confidence_threshold == 0.8
        assert cfg.padding == 10


class TestFaceROI:
    def test_label_format(self):
        roi = FaceROI(confidence=0.9876, start_x=10, start_y=20, end_x=100, end_y=150)
        assert roi.detection_label == "98.8%"

    def test_box_property(self):
        roi = FaceROI(confidence=0.75, start_x=5, start_y=10, end_x=50, end_y=80)
        assert roi.box == (5, 10, 50, 80)

    def test_width_height(self):
        roi = FaceROI(confidence=0.9, start_x=10, start_y=20, end_x=110, end_y=170)
        assert roi.width == 100
        assert roi.height == 150

    def test_crop_within_bounds(self, dummy_image):
        roi = FaceROI(confidence=0.9, start_x=50, start_y=50, end_x=150, end_y=150)
        crop = roi.crop(dummy_image, padding=0)
        assert crop.shape == (100, 100, 3)

    def test_crop_with_padding_clips_to_image(self, dummy_image):
        roi = FaceROI(confidence=0.9, start_x=0, start_y=0, end_x=50, end_y=50)
        crop = roi.crop(dummy_image, padding=100)
        # padding não deve sair dos limites da imagem (300x300)
        assert crop.shape[0] <= 300
        assert crop.shape[1] <= 300


class TestFaceDetectorInit:
    def test_missing_prototxt_raises(self, tmp_path):
        fake_model = tmp_path / "model.caffemodel"
        fake_model.write_bytes(b"fake")
        with pytest.raises(FileNotFoundError):
            FaceDetector(
                prototxt_path=tmp_path / "nonexistent.prototxt",
                model_path=fake_model,
            )

    def test_missing_model_raises(self, tmp_path):
        fake_proto = tmp_path / "deploy.prototxt"
        fake_proto.write_bytes(b"fake")
        with pytest.raises(FileNotFoundError):
            FaceDetector(
                prototxt_path=fake_proto,
                model_path=tmp_path / "nonexistent.caffemodel",
            )


class TestFaceDetectorDetect:
    def test_invalid_image_raises(self):
        detector = FaceDetector.__new__(FaceDetector)
        detector.config = DetectionConfig()
        detector._net = None
        with pytest.raises(ValueError):
            detector.detect(np.array([]))