"""
logger_config.py
----------------
Configuração centralizada de logging para o projeto.
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | str | None = None,
) -> None:
    """
    Configura o sistema de logging da aplicação.

    Parâmetros
    ----------
    level : int
        Nível de log (ex: logging.DEBUG, logging.INFO).
    log_file : Path | str | None
        Se fornecido, escreve logs também em arquivo.
    """
    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
    ]

    if log_file is not None:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(file_path, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )