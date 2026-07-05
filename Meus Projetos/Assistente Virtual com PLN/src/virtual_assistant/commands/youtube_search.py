"""Comando: abrir uma pesquisa no YouTube."""
from __future__ import annotations

import webbrowser
from urllib.parse import quote_plus

from virtual_assistant.commands.base import Command
from virtual_assistant.stt.speech_to_text import SpeechToText
from virtual_assistant.tts.text_to_speech import TextToSpeech
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)


class YoutubeSearchCommand(Command):
    triggers = ("youtube",)

    def __init__(self, tts: TextToSpeech, stt: SpeechToText) -> None:
        self.tts = tts
        self.stt = stt

    def execute(self, text: str) -> None:
        self.tts.speak("O que você quer buscar no YouTube?")
        keyword = self.stt.listen()

        if not keyword:
            self.tts.speak("Não entendi o que buscar.")
            return

        url = f"https://www.youtube.com/results?search_query={quote_plus(keyword)}"
        logger.info("Abrindo YouTube: %s", url)
        webbrowser.get().open(url)
        self.tts.speak(f"Aqui está o que encontrei para {keyword} no YouTube.")
