"""
tests/test_image_utils.py
-------------------------
Testes unitários para o módulo image_utils.py.
"""

import numpy as np
import pytest

from src.image_utils import load_image, resize_image, save_image


# ------------------------------------------------------------------
# load_image
# ------------------------------------------------------------------

class TestLoadImage:
    def test_file_not_found(self, tmp_path: pytest.TempPathFactory) -> None:
        with pytest.raises(FileNotFoundError):
            load_image(tmp_path / "nonexistent.jpg")

    def test_unsupported_extension(self, tmp_path: pytest.TempPathFactory) -> None:
        fake = tmp_path / "file.txt"
        fake.write_text("not an image")
        with pytest.raises(ValueError, match="não suportada"):
            load_image(fake)

    def test_loads_valid_image(self, tmp_path: pytest.TempPathFactory) -> None:
        import cv2
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        path = tmp_path / "test.jpg"
        cv2.imwrite(str(path), img)
        loaded = load_image(path)
        assert loaded is not None
        assert loaded.shape == (100, 100, 3)


# ------------------------------------------------------------------
# resize_image
# ------------------------------------------------------------------

class TestResizeImage:
    def test_aspect_ratio_preserved(self) -> None:
        image = np.zeros((400, 800, 3), dtype=np.uint8)  # 2:1 ratio
        resized = resize_image(image, width=400)
        assert resized.shape[1] == 400
        assert resized.shape[0] == 200  # mantém proporção

    def test_same_width_returns_same(self) -> None:
        image = np.zeros((300, 400, 3), dtype=np.uint8)
        result = resize_image(image, width=400)
        assert result.shape == image.shape

    def test_output_type(self) -> None:
        image = np.zeros((200, 200, 3), dtype=np.uint8)
        result = resize_image(image, width=100)
        assert isinstance(result, np.ndarray)


# ------------------------------------------------------------------
# save_image
# ------------------------------------------------------------------

class TestSaveImage:
    def test_saves_and_returns_path(self, tmp_path: pytest.TempPathFactory) -> None:
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        output = tmp_path / "out" / "result.jpg"
        saved = save_image(image, output)
        assert saved.exists()

    def test_creates_intermediate_dirs(self, tmp_path: pytest.TempPathFactory) -> None:
        image = np.zeros((50, 50, 3), dtype=np.uint8)
        deep = tmp_path / "a" / "b" / "c" / "img.png"
        save_image(image, deep)
        assert deep.exists()