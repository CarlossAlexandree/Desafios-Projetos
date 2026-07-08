"""Exceções de domínio da aplicação, com status HTTP associado."""


class AppError(Exception):
    """Exceção base — sempre carrega uma mensagem amigável e um status HTTP."""

    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidImageError(AppError):
    status_code = 422


class ImageTooLargeError(AppError):
    status_code = 413


class AIProviderError(AppError):
    status_code = 502


class AIResponseParsingError(AppError):
    status_code = 502


class RateLimitExceededError(AppError):
    status_code = 429
