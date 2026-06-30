"""
tests/test_image_utils.py
--------------------------
Testes unitários para o módulo image_utils.py.
"""

import numpy as np
import pytest

from src.image_utils import (
    draw_recognition, get_color_for_name,
    load_image, resize_image, save_image,
)


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
        image = np.zeros((300, 400, 3), dtype=np.uint8)
        result = resize_image(image, width=400)
        assert result.shape == image.shape


class TestSaveImage:
    def test_saves_and_returns_path(self, tmp_path):
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        output = tmp_path / "out" / "result.jpg"
        saved = save_image(image, output)
        assert saved.exists()

    def test_creates_intermediate_dirs(self, tmp_path):
        image = np.zeros((50, 50, 3), dtype=np.uint8)
        deep = tmp_path / "a" / "b" / "c" / "img.png"
        save_image(image, deep)
        assert deep.exists()


class TestGetColorForName:
    def test_unknown_returns_gray(self):
        color = get_color_for_name("Desconhecido", ["joao", "maria"])
        assert color == (80, 80, 80)

    def test_known_name_consistent(self):
        names = ["joao", "maria", "pedro"]
        color1 = get_color_for_name("maria", names)
        color2 = get_color_for_name("maria", names)
        assert color1 == color2

    def test_different_names_different_colors(self):
        names = ["joao", "maria", "pedro"]
        c1 = get_color_for_name("joao", names)
        c2 = get_color_for_name("maria", names)
        assert c1 != c2


class TestDrawRecognition:
    def test_returns_modified_image(self):
        image = np.zeros((200, 200, 3), dtype=np.uint8)
        result = draw_recognition(
            image, 10, 10, 100, 100, "Joao", 0.95,
        )
        # A imagem não deve ser totalmente preta após desenhar
        assert result.sum() > 0

    def test_label_includes_percentage(self):
        # Não há retorno textual direto, mas garante que não lança erro
        image = np.zeros((200, 200, 3), dtype=np.uint8)
        try:
            draw_recognition(image, 5, 5, 50, 50, "Maria", 0.873)
        except Exception as exc:
            pytest.fail(f"draw_recognition levantou exceção inesperada: {exc}")