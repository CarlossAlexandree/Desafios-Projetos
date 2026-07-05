"""Comando: contar uma piada (mantido do script original do curso)."""
from __future__ import annotations

import pyjokes

from virtual_assistant.commands.base import Command
from virtual_assistant.tts.text_to_speech import TextToSpeech


class JokeCommand(Command):
    triggers = ("piada", "joke")

    def __init__(self, tts: TextToSpeech) -> None:
        self.tts = tts

    def execute(self, text: str) -> None:
        self.tts.speak(pyjokes.get_joke(language="pt"))
