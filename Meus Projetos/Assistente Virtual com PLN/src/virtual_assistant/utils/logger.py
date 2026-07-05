"""
Configuração de logging estruturado para o assistente.

Substitui os `print()` do script original por um logger de verdade,
com saída simultânea em console e em arquivo rotativo — essencial
para depurar um assistente que roda continuamente em produção.
"""
import logging
from logging.handlers import RotatingFileHandler

from virtual_assistant.config import settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado e pronto para uso.

    Args:
        name: normalmente `__name__` do módulo chamador.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Evita adicionar handlers duplicados se get_logger for chamado
        # mais de uma vez para o mesmo módulo.
        return logger

    logger.setLevel(settings.log_level)

    formatter = logging.Formatter(_LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        settings.log_dir / "virtual_assistant.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
