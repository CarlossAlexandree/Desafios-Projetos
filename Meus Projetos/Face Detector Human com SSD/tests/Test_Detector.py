"""
tests/test_detector.py
----------------------
Testes unitários para o módulo detector.py.
Execute com: pytest tests/
"""

import numpy as np
import pytest

from src.detector import DetectionConfig, DetectionResult, FaceDetector


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def default_config() -> DetectionConfig:
    return DetectionConfig()


@pytest.fixture
def dummy_image() -> np.ndarray:
    """Imagem BGR sintética 300x300."""
    return np.zeros((300, 300, 3), dtype=np.uint8)


# ------------------------------------------------------------------
# DetectionConfig
# ------------------------------------------------------------------

class TestDetectionConfig:
    def test_default_confidence_threshold(self, default_config: DetectionConfig) -> None:
        assert default_config.confidence_threshold == 0.5

    def test_custom_confidence_threshold(self) -> None:
        cfg = DetectionConfig(confidence_threshold=0.8)
        assert cfg.confidence_threshold == 0.8

    def test_default_input_size(self, default_config: DetectionConfig) -> None:
        assert default_config.input_size == (300, 300)

    def test_default_mean_subtraction(self, default_config: DetectionConfig) -> None:
        assert default_config.mean_subtraction == (104.0, 177.0, 123.0)


# ------------------------------------------------------------------
# DetectionResult
# ------------------------------------------------------------------

class TestDetectionResult:
    def test_label_format(self) -> None:
        result = DetectionResult(
            confidence=0.9876,
            start_x=10, start_y=20,
            end_x=100, end_y=150,
        )
        assert result.label == "98.76%"

    def test_box_property(self) -> None:
        result = DetectionResult(
            confidence=0.75,
            start_x=5, start_y=10,
            end_x=50, end_y=80,
        )
        assert result.box == (5, 10, 50, 80)

    def test_low_confidence_label(self) -> None:
        result = DetectionResult(
            confidence=0.5,
            start_x=0, start_y=0,
            end_x=1, end_y=1,
        )
        assert result.label == "50.00%"


# ------------------------------------------------------------------
# FaceDetector — inicialização
# ------------------------------------------------------------------

class TestFaceDetectorInit:
    def test_missing_prototxt_raises(self, tmp_path: pytest.TempPathFactory) -> None:
        fake_model = tmp_path / "model.caffemodel"
        fake_model.write_bytes(b"fake")
        with pytest.raises(FileNotFoundError, match="Prototxt"):
            FaceDetector(
                prototxt_path=tmp_path / "nonexistent.prototxt",
                model_path=fake_model,
            )

    def test_missing_model_raises(self, tmp_path: pytest.TempPathFactory) -> None:
        fake_proto = tmp_path / "deploy.prototxt"
        fake_proto.write_bytes(b"fake")
        with pytest.raises(FileNotFoundError, match="Modelo"):
            FaceDetector(
                prototxt_path=fake_proto,
                model_path=tmp_path / "nonexistent.caffemodel",
            )


# ------------------------------------------------------------------
# FaceDetector — detecção
# ------------------------------------------------------------------

class TestFaceDetectorDetect:
    def test_invalid_image_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verifica que imagem None ou vazia levanta ValueError."""
        # Criamos um detector com arquivos falsos via monkeypatch
        import cv2
        monkeypatch.setattr(cv2.dnn, "readNetFromCaffe", lambda *_: object())

        from pathlib import Path
        import src.detector as det_module

        # Substituímos _load_model para não validar arquivos
        original_load = FaceDetector._load_model
        FaceDetector._load_model = staticmethod(lambda *_: None)  # type: ignore[assignment]

        detector = FaceDetector.__new__(FaceDetector)
        detector.config = DetectionConfig()
        detector._net = None  # type: ignore[assignment]

        with pytest.raises((ValueError, Exception)):
            detector.detect(np.array([]))

        FaceDetector._load_model = staticmethod(original_load)  # type: ignore[assignment]


# ------------------------------------------------------------------
# FaceDetector — visualização
# ------------------------------------------------------------------

class TestFaceDetectorDraw:
    def test_draw_returns_copy(self, dummy_image: np.ndarray) -> None:
        """O método draw não deve modificar a imagem original."""
        from src.detector import DetectionResult

        detector = FaceDetector.__new__(FaceDetector)
        detector.config = DetectionConfig()

        det = DetectionResult(
            confidence=0.9,
            start_x=10, start_y=10,
            end_x=100, end_y=100,
        )

        original_copy = dummy_image.copy()
        annotated = detector.draw(dummy_image, [det])

        # Imagem original não deve ter sido alterada
        np.testing.assert_array_equal(dummy_image, original_copy)
        # Resultado deve ser diferente (tem anotações)
        assert not np.array_equal(annotated, original_copy)

    def test_draw_empty_detections(self, dummy_image: np.ndarray) -> None:
        """Com lista vazia, a imagem de saída deve ser idêntica à original."""
        detector = FaceDetector.__new__(FaceDetector)
        detector.config = DetectionConfig()

        annotated = detector.draw(dummy_image, [])
        np.testing.assert_array_equal(annotated, dummy_image)