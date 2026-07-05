"""
Módulo Text-to-Speech (texto -> áudio).

Evolução do exemplo `Text-to-Speech-DIO.py` do curso: em vez de um
script solto que salva sempre no mesmo caminho, temos uma classe
reutilizável, testável e com tratamento de erros.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

from gtts import gTTS
from playsound3 import playsound

from virtual_assistant.config import settings
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)


class TextToSpeechError(Exception):
    """Erro genérico do módulo de síntese de fala."""


class TextToSpeech:
    """Converte texto em áudio falado e o reproduz."""

    def __init__(self, language: str | None = None, slow: bool = False) -> None:
        self.language = language or settings.tts_language
        self.slow = slow

    def synthesize(self, text: str) -> Path:
        """Gera um arquivo de áudio a partir de um texto.

        Args:
            text: texto a ser convertido em fala.

        Returns:
            Caminho do arquivo de áudio gerado.

        Raises:
            TextToSpeechError: se a síntese falhar (ex.: sem internet,
                idioma inválido).
        """
        if not text or not text.strip():
            raise TextToSpeechError("Texto vazio não pode ser sintetizado.")

        filename = settings.audio_output_dir / f"{uuid.uuid4().hex}.mp3"
        try:
            tts_object = gTTS(text=text, lang=self.language, slow=self.slow)
            tts_object.save(str(filename))
            logger.debug("Áudio gerado em %s", filename)
            return filename
        except Exception as exc:  # gTTS pode levantar vários tipos de erro de rede
            logger.error("Falha ao sintetizar texto: %s", exc)
            raise TextToSpeechError(str(exc)) from exc

    def speak(self, text: str) -> None:
        """Sintetiza e reproduz o texto imediatamente, removendo o
        arquivo temporário em seguida."""
        filename = self.synthesize(text)
        try:
            playsound(str(filename))
        finally:
            self._cleanup(filename)

    @staticmethod
    def _cleanup(filename: Path) -> None:
        try:
            os.remove(filename)
        except OSError as exc:
            logger.warning("Não foi possível remover arquivo temporário %s: %s", filename, exc)
