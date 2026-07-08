"""
Rate limiter simples em memória, por IP, janela fixa de 60s.

Suficiente para uma API de portfólio/estudo com deploy único (free tier).
Para múltiplas réplicas em produção real, troque por Redis — a interface
abaixo foi desenhada para isso ser uma troca isolada.
"""
import time
from collections import defaultdict

from app.core.config import get_settings
from app.core.exceptions import RateLimitExceededError

settings = get_settings()
_requests_by_ip: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(client_ip: str) -> None:
    now = time.time()
    window_start = now - 60

    timestamps = [t for t in _requests_by_ip[client_ip] if t > window_start]
    _requests_by_ip[client_ip] = timestamps

    if len(timestamps) >= settings.RATE_LIMIT_PER_MINUTE:
        raise RateLimitExceededError(
            f"Limite de {settings.RATE_LIMIT_PER_MINUTE} requisições/minuto excedido. "
            "Tente novamente em instantes."
        )

    _requests_by_ip[client_ip].append(now)
