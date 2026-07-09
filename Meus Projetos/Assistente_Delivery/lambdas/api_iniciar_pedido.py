"""
Lambda: api-iniciar-pedido
Recebe a chamada HTTP do API Gateway (POST /pedidos) e inicia a execucao
da Step Function de processamento de pedido.

Variavel de ambiente necessaria:
  STATE_MACHINE_ARN -> ARN da state machine "assistente-delivery-pedido"
"""
import json
import os
import boto3

sfn = boto3.client("stepfunctions")
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]


def lambda_handler(event, context):
    corpo = json.loads(event.get("body") or "{}")

    execucao = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({"pedido": corpo}),
    )

    return {
        "statusCode": 202,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "mensagem": "Pedido recebido, processamento iniciado.",
            "executionArn": execucao["executionArn"],
        }),
    }
