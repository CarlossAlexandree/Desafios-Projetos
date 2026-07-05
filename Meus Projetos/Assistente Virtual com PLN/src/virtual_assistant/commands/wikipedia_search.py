"""Comando: pesquisar um termo no Wikipedia."""
from __future__ import annotations

import wikipedia

from virtual_assistant.commands.base import Command
from virtual_assistant.stt.speech_to_text import SpeechToText
from virtual_assistant.tts.text_to_speech import TextToSpeech
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)


class WikipediaSearchCommand(Command):
    triggers = ("pesquisar", "pesquise", "wikipedia", "search")

    def __init__(self, tts: TextToSpeech, stt: SpeechToText, language: str = "pt") -> None:
        self.tts = tts
        self.stt = stt
        wikipedia.set_lang(language)

    def execute(self, text: str) -> None:
        self.tts.speak("O que você quer pesquisar?")
        query = self.stt.listen()

        if not query:
            self.tts.speak("Não entendi o termo da pesquisa.")
            return

        try:
            summary = wikipedia.summary(query, sentences=3)
        except wikipedia.exceptions.DisambiguationError as exc:
            logger.warning("Termo ambíguo '%s': %s", query, exc.options[:5])
            self.tts.speak(
                f"O termo {query} é ambíguo. Pode ser mais específico?"
            )
            return
        except wikipedia.exceptions.PageError:
            self.tts.speak(f"Não encontrei nada sobre {query} na Wikipedia.")
            return

        logger.info("Resumo encontrado para '%s'", query)
        self.tts.speak("De acordo com a Wikipedia:")
        self.tts.speak(summary)
