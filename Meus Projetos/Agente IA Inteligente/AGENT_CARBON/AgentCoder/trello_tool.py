import os
import requests
from dotenv import load_dotenv

load_dotenv()

def criar_cartao_trello(titulo: str, descricao: str) -> str:
    """
    Cria um cartão de tarefa no quadro Trello do usuário.
    Use esta ferramenta sempre que o usuário confirmar uma tarefa para ser registrada.

    Args:
        titulo (str): O título resumido da tarefa a ser criada no Trello.
        descricao (str): A descrição detalhada ou observações da tarefa.

    Returns:
        str: Mensagem de confirmação de sucesso com a URL ou detalhes do erro.
    """
    api_key = os.getenv("TRELLO_API_KEY", "932d33b7b1c67c432eda71fab088615f")
    token = os.getenv("TRELLO_OAUTH_TOKEN", "6cea039a10112fe35ad15d379f195c939aafb9a00ddff39649f49b1e485ab7a7")
    list_id = os.getenv("TRELLO_LIST_ID", "6a276c03a4fb0a3f24c7e8c8")
    
    url = "https://api.trello.com/1/cards"

    query = {
        "idList": list_id,
        "name": titulo,
        "desc": descricao
    }

    headers = {
        "Authorization": f'OAuth oauth_consumer_key="{api_key}", oauth_token="{token}"'
    }

    try:
        response = requests.post(url, params=query, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            return f"Sucesso: Cartão '{titulo}' criado! Link de acesso: {dados.get('shortUrl')}"
        else:
            return f"Erro retornado pelo Trello (Status {response.status_code}): {response.text}"
    except Exception as e:
        return f"Falha de conexão com os servidores do Trello: {str(e)}"