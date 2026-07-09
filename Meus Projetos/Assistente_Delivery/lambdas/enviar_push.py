"""
Lambda: enviar-push
Publica a mensagem gerada em um topico SNS (push para cliente/restaurante).

Variavel de ambiente necessaria:
  TOPICO_PUSH_ARN -> ARN do topico SNS usado para push notifications
"""
import os
import boto3

sns = boto3.client("sns")
TOPICO_PUSH = os.environ["TOPICO_PUSH_ARN"]


def lambda_handler(event, context):
    mensagem = event.get("mensagem", "Atualizacao do seu pedido.")
    pedido_id = event.get("pedidoId")

    sns.publish(
        TopicArn=TOPICO_PUSH,
        Message=mensagem,
        Subject=f"Pedido {pedido_id}",
    )

    return {"pedidoId": pedido_id, "enviado": True}
