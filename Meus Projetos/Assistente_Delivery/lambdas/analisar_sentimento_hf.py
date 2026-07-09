"""
Lambda: analisar-sentimento-hf
Substitui o Amazon Bedrock por um modelo gratuito hospedado na Hugging Face
Inference API. Usa apenas a biblioteca padrao (urllib) para nao depender de
camadas (layers) extras no deploy.

Variavel de ambiente necessaria:
  HF_API_TOKEN -> token gratuito criado em https://huggingface.co/settings/tokens

Modelo usado (multilingue, cobre portugues):
  cardiffnlp/twitter-xlm-roberta-base-sentiment
"""
import json
import os
import urllib.request
import urllib.error

HF_API_URL = (
    "https://api-inference.huggingface.co/models/"
    "cardiffnlp/twitter-xlm-roberta-base-sentiment"
)
HF_TOKEN = os.environ["HF_API_TOKEN"]


def lambda_handler(event, context):
    texto = event.get("feedback", "")
    if not texto:
        raise ValueError("Campo 'feedback' e obrigatorio no evento de entrada.")

    payload = json.dumps({"inputs": texto}).encode("utf-8")
    req = urllib.request.Request(
        HF_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            resultado = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        # Modelos "dormem" apos ociosidade; a HF retorna 503 enquanto carrega.
        corpo = erro.read().decode("utf-8")
        raise RuntimeError(f"Erro ao chamar Hugging Face ({erro.code}): {corpo}")

    # Formato de resposta: [[{"label": "Positive", "score": 0.87}, ...]]
    melhor = max(resultado[0], key=lambda item: item["score"])

    return {
        "pedidoId": event.get("pedidoId"),
        "sentimento": melhor["label"],
        "score": str(round(melhor["score"], 4)),
        "feedbackOriginal": texto,
    }
