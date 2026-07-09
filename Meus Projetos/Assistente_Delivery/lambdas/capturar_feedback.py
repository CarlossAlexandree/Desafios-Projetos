"""
Lambda: capturar-feedback
Normaliza o payload de feedback recebido antes de enviar para analise de sentimento.
"""


def lambda_handler(event, context):
    feedback = event.get("feedback", "")

    if not feedback.strip():
        raise ValueError("Campo 'feedback' vazio ou ausente no evento de entrada.")

    return {
        "pedidoId": event.get("pedidoId"),
        "feedback": feedback,
    }
