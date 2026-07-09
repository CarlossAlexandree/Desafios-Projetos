"""
Lambda: gerar-mensagem
Monta o texto da notificacao a partir do status atual do pedido.
"""

MENSAGENS = {
    "PEDIDO_RECEBIDO": "Recebemos seu pedido! Em instantes o restaurante ira confirmar.",
    "ACEITO": "Seu pedido foi aceito pelo restaurante e ja esta sendo preparado.",
    "EM_ENTREGA": "Seu pedido saiu para entrega!",
    "CONCLUIDO": "Seu pedido foi entregue. Bom apetite!",
}


def lambda_handler(event, context):
    status = event.get("status", "PEDIDO_RECEBIDO")

    return {
        "pedidoId": event.get("pedidoId"),
        "status": status,
        "mensagem": MENSAGENS.get(status, "Atualizacao do seu pedido disponivel."),
    }
