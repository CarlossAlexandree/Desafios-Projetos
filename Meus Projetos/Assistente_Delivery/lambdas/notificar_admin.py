"""
Lambda: notificar-admin
Publica um alerta no SNS quando um feedback negativo e detectado.

Variavel de ambiente necessaria:
  TOPICO_ADMIN_ARN -> ARN do topico SNS de alertas administrativos
"""
import os
import boto3

sns = boto3.client("sns")
TOPICO_ADMIN = os.environ["TOPICO_ADMIN_ARN"]


def lambda_handler(event, context):
    mensagem = (
        "Feedback negativo recebido!\n"
        f"Pedido: {event.get('pedidoId')}\n"
        f"Sentimento: {event.get('sentimento')}\n"
        f"Score: {event.get('score')}\n"
        f"Texto: {event.get('feedbackOriginal')}"
    )

    sns.publish(
        TopicArn=TOPICO_ADMIN,
        Message=mensagem,
        Subject="Alerta de Feedback Negativo - Assistente de Delivery",
    )

    return {"notificado": True, "pedidoId": event.get("pedidoId")}
