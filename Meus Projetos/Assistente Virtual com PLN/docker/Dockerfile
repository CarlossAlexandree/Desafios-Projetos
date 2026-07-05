# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# Dependências de sistema necessárias para pyaudio, playsound e áudio em geral
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    python3-dev \
    libasound2-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .
COPY src ./src
COPY main.py .

RUN pip install --no-cache-dir .

# Usuário não-root por segurança
RUN useradd --create-home appuser
USER appuser

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
