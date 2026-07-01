"""
logger_config.py
----------------
Configuração centralizada de logging para o projeto.
"""

import logging
import sys
from pathlib import Path


def setup_logging(level: int = logging.INFO, log_file=None) -> None:
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file is not None:
        p = Path(log_file)
        p.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(p, encoding="utf-8"))
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )