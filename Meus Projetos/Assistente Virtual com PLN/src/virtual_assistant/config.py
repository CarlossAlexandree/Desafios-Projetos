"""
Configuração centralizada do assistente virtual.

Carrega variáveis de ambiente de um arquivo .env (se existir) e expõe
um objeto `settings` único, seguindo o padrão de configuração
12-factor app: nada de valores hardcoded espalhados pelo código.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Carrega o .env da raiz do projeto, se existir. Em produção (Docker/CI)
# as variáveis normalmente já vêm do ambiente, então isso é apenas um
# fallback conveniente para desenvolvimento local.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    assistant_name: str = os.getenv("ASSISTANT_NAME", "Jarvis")
    assistant_language: str = os.getenv("ASSISTANT_LANGUAGE", "pt-BR")
    tts_language: str = os.getenv("TTS_LANGUAGE", "pt")

    audio_output_dir: Path = Path(os.getenv("AUDIO_OUTPUT_DIR", "./audio_output"))

    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_dir: Path = Path(os.getenv("LOG_DIR", "./logs"))

    ambient_noise_duration: float = float(os.getenv("AMBIENT_NOISE_DURATION", "1"))
    pharmacy_search_radius_m: int = int(os.getenv("PHARMACY_SEARCH_RADIUS_M", "3000"))

    def ensure_directories(self) -> None:
        """Garante que os diretórios necessários existam antes do uso."""
        self.audio_output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
