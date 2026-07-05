"""
Contrato base para todos os comandos de voz.

Cada comando (Wikipedia, YouTube, farmácia, piada...) implementa esta
interface. Isso permite adicionar um novo comando sem alterar o
roteador nem o núcleo do assistente — basta registrar a nova classe.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    """Interface para um comando de voz executável."""

    #: Palavras-chave que, se presentes no texto reconhecido, ativam o comando.
    triggers: tuple[str, ...] = ()

    def matches(self, text: str) -> bool:
        """Verifica se o texto do usuário aciona este comando."""
        return any(trigger in text for trigger in self.triggers)

    @abstractmethod
    def execute(self, text: str) -> None:
        """Executa a ação do comando. `text` é a frase completa do usuário."""
        raise NotImplementedError
