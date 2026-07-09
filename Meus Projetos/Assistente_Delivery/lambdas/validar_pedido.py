"""
Lambda: validar-pedido
Valida campos obrigatorios do pedido e grava um registro inicial no DynamoDB.

Variavel de ambiente necessaria:
  TABELA_PEDIDOS -> nome da tabela DynamoDB de pedidos
"""
import os
import uuid
import boto3

dynamodb = boto3.resource("dynamodb")
tabela = dynamodb.Table(os.environ["TABELA_PEDIDOS"])

CAMPOS_OBRIGATORIOS = ["usuarioId", "restauranteId", "itens"]


def lambda_handler(event, context):
    pedido = event.get("pedido", event)

    valido = all(pedido.get(campo) for campo in CAMPOS_OBRIGATORIOS)
    pedido_id = str(uuid.uuid4())

    if valido:
        tabela.put_item(Item={
            "pedidoId": pedido_id,
            "usuarioId": pedido["usuarioId"],
            "restauranteId": pedido["restauranteId"],
            "itens": pedido["itens"],
            "status": "PEDIDO_RECEBIDO",
        })

    return {
        "pedidoId": pedido_id,
        "valido": valido,
        "pedido": pedido,
    }
