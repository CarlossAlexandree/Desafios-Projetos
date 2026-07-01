"""
tests/test_visualizer.py
--------------------------
Testes unitários para o módulo visualizer.py.
"""

import numpy as np
import pytest

from src.detector import Detection
from src.visualizer import draw_detections, draw_fps


@pytest.fixture
def dummy_image():
    return np.zeros((480, 640, 3), dtype=np.uint8)


@pytest.fixture
def sample_detections():
    return [
        Detection("person", 0.92, 50, 50, 200, 400),
        Detection("laptop", 0.85, 250, 100, 500, 350),
        Detection("cell phone", 0.78, 10, 10, 60, 120),
    ]


class TestDrawDetections:
    def test_returns_copy(self, dummy_image, sample_detections):
        original = dummy_image.copy()
        result = draw_detections(dummy_image, sample_detections)
        np.testing.assert_array_equal(dummy_image, original)
        assert not np.array_equal(result, original)

    def test_empty_detections_same_as_original(self, dummy_image):
        result = draw_detections(dummy_image, [], show_count=False)
        np.testing.assert_array_equal(result, dummy_image)

    def test_returns_ndarray(self, dummy_image, sample_detections):
        result = draw_detections(dummy_image, sample_detections)
        assert isinstance(result, np.ndarray)

    def test_output_shape_unchanged(self, dummy_image, sample_detections):
        result = draw_detections(dummy_image, sample_detections)
        assert result.shape == dummy_image.shape


class TestDrawFps:
    def test_returns_image(self, dummy_image):
        result = draw_fps(dummy_image, fps=30.5)
        assert isinstance(result, np.ndarray)

    def test_modifies_image(self, dummy_image):
        original = dummy_image.copy()
        draw_fps(dummy_image, fps=25.0)
        # A função modifica in-place, então a imagem original muda
        assert not np.array_equal(dummy_image, original)