"""
Módulo Speech-to-Text (fala -> texto).

Evolução do exemplo `Speech-to-text.py` do curso: separa a captura de
áudio do microfone (I/O) do reconhecimento propriamente dito, e troca
exceções silenciosas por logging + exceções tipadas.
"""
from __future__ import annotations

import speech_recognition as sr

from virtual_assistant.config import settings
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)


class SpeechRecognitionError(Exception):
    """Erro genérico do módulo de reconhecimento de voz."""


class SpeechToText:
    """Captura áudio do microfone e o converte em texto."""

    def __init__(self, language: str | None = None) -> None:
        self.language = language or settings.assistant_language
        self.recognizer = sr.Recognizer()

    def listen(self) -> str:
        """Ouve o microfone e retorna o texto reconhecido em minúsculas.

        Returns:
            Texto reconhecido (string vazia se nada foi entendido).

        Raises:
            SpeechRecognitionError: se o serviço de reconhecimento
                estiver indisponível (ex.: sem internet).
        """
        with sr.Microphone() as source:
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(
                source, duration=settings.ambient_noise_duration
            )
            logger.info("Ouvindo...")
            audio = self.recognizer.listen(source)

        return self._transcribe(audio)

    def _transcribe(self, audio: sr.AudioData) -> str:
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info("Reconhecido: %s", text)
            return text.lower()
        except sr.UnknownValueError:
            logger.warning("Áudio não compreendido.")
            return ""
        except sr.RequestError as exc:
            logger.error("Serviço de reconhecimento indisponível: %s", exc)
            raise SpeechRecognitionError(
                "Serviço de reconhecimento de voz indisponível no momento."
            ) from exc
