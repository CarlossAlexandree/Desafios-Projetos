"""
tests/test_image_utils.py
--------------------------
Testes unitários para o módulo image_utils.py.
"""

import numpy as np
import pytest

from src.image_utils import list_images, load_image, resize_image, save_image


class TestLoadImage:
    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_image(tmp_path / "nonexistent.jpg")

    def test_unsupported_extension(self, tmp_path):
        fake = tmp_path / "file.txt"
        fake.write_text("not an image")
        with pytest.raises(ValueError, match="não suportada"):
            load_image(fake)

    def test_loads_valid_image(self, tmp_path):
        import cv2
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        path = tmp_path / "test.jpg"
        cv2.imwrite(str(path), img)
        loaded = load_image(path)
        assert loaded.shape == (100, 100, 3)


class TestResizeImage:
    def test_aspect_ratio_preserved(self):
        image = np.zeros((400, 800, 3), dtype=np.uint8)
        resized = resize_image(image, width=400)
        assert resized.shape[1] == 400
        assert resized.shape[0] == 200

    def test_same_width_returns_same(self):
        image = np.zeros((300, 640, 3), dtype=np.uint8)
        result = resize_image(image, width=640)
        assert result.shape == image.shape


class TestSaveImage:
    def test_saves_correctly(self, tmp_path):
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        output = tmp_path / "output" / "result.jpg"
        saved = save_image(image, output)
        assert saved.exists()

    def test_creates_dirs(self, tmp_path):
        image = np.zeros((50, 50, 3), dtype=np.uint8)
        deep = tmp_path / "a" / "b" / "c" / "img.png"
        save_image(image, deep)
        assert deep.exists()


class TestListImages:
    def test_lists_only_images(self, tmp_path):
        import cv2
        img = np.zeros((50, 50, 3), dtype=np.uint8)
        cv2.imwrite(str(tmp_path / "a.jpg"), img)
        cv2.imwrite(str(tmp_path / "b.png"), img)
        (tmp_path / "c.txt").write_text("not image")

        images = list_images(tmp_path)
        names = [p.name for p in images]
        assert "a.jpg" in names
        assert "b.png" in names
        assert "c.txt" not in names

    def test_empty_folder_returns_empty(self, tmp_path):
        assert list_images(tmp_path) == []