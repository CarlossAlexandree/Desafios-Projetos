"""
Núcleo do assistente virtual: laço principal de escuta e resposta.
"""
from __future__ import annotations

from virtual_assistant.commands.joke import JokeCommand
from virtual_assistant.commands.pharmacy_locator import PharmacyLocatorCommand
from virtual_assistant.commands.router import CommandRouter
from virtual_assistant.commands.wikipedia_search import WikipediaSearchCommand
from virtual_assistant.commands.youtube_search import YoutubeSearchCommand
from virtual_assistant.config import settings
from virtual_assistant.stt.speech_to_text import SpeechRecognitionError, SpeechToText
from virtual_assistant.tts.text_to_speech import TextToSpeech
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)

EXIT_TRIGGERS = ("sair", "exit", "encerrar")


class VirtualAssistant:
    """Orquestra STT, TTS e o roteamento de comandos em um laço contínuo."""

    def __init__(self) -> None:
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        self.router = CommandRouter(
            commands=[
                WikipediaSearchCommand(self.tts, self.stt),
                YoutubeSearchCommand(self.tts, self.stt),
                PharmacyLocatorCommand(self.tts),
                JokeCommand(self.tts),
            ],
            tts=self.tts,
        )

    def run(self) -> None:
        logger.info("%s iniciado. Aguardando comandos de voz...", settings.assistant_name)
        self.tts.speak(f"{settings.assistant_name} pronto para ajudar.")

        while True:
            try:
                text = self.stt.listen()
            except SpeechRecognitionError:
                self.tts.speak("Estou com problemas para acessar o reconhecimento de voz.")
                continue

            if not text:
                continue

            if any(trigger in text for trigger in EXIT_TRIGGERS):
                self.tts.speak("Até logo!")
                logger.info("Encerrando por comando do usuário.")
                break

            handled = self.router.route(text)
            if not handled:
                self.tts.speak("Desculpe, não entendi esse comando.")


def main() -> None:
    """Ponto de entrada do console script `virtual-assistant`."""
    assistant = VirtualAssistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        logger.info("Interrompido pelo usuário (Ctrl+C).")


if __name__ == "__main__":
    main()
