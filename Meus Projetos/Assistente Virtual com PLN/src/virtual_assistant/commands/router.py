"""
Roteador de comandos.

Recebe o texto reconhecido do STT e delega ao primeiro `Command`
registrado cujo `matches()` retorne True. Novos comandos são
adicionados apenas registrando-os na lista — nenhuma outra parte do
sistema precisa ser alterada (princípio Aberto/Fechado).
"""
from __future__ import annotations

from virtual_assistant.commands.base import Command
from virtual_assistant.tts.text_to_speech import TextToSpeech
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)


class CommandRouter:
    def __init__(self, commands: list[Command], tts: TextToSpeech) -> None:
        self._commands = commands
        self.tts = tts

    def register(self, command: Command) -> None:
        self._commands.append(command)

    def route(self, text: str) -> bool:
        """Executa o primeiro comando compatível com o texto.

        Returns:
            True se algum comando foi executado, False caso contrário.
        """
        if not text:
            return False

        for command in self._commands:
            if command.matches(text):
                logger.info("Comando '%s' acionado por: '%s'", type(command).__name__, text)
                command.execute(text)
                return True

        logger.info("Nenhum comando reconhecido para: '%s'", text)
        return False
