"""
Motor de regras do Copiloto FYS.

Sem dependência de API paga: toda a "inteligência" aqui é lógica local
(pontuação ponderada + casamento de palavras-chave), documentada em
knowledge/logica-priorizacao.md e knowledge/objecoes.md.
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ESPACO_PONTOS = {"baixo": 5, "medio": 10, "alto": 15}

# ---------------------------------------------------------------------------
# Priorização de padarias
# ---------------------------------------------------------------------------

def carregar_padarias(caminho: str) -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def calcular_prioridade(padaria: dict, maior_volume: float) -> dict:
    potencial = (padaria["volume_cerveja_hl_mes"] / maior_volume) * 40 if maior_volume else 0
    facilidade = ESPACO_PONTOS.get(padaria["espaco_geladeira"], 5)
    urgencia = min(padaria["dias_desde_ultima_visita"] / 120, 1) * 20
    oportunidade = 5 if padaria["vende_fys"] else 25
    bonus = 5 if len(padaria.get("concorrencia", [])) >= 2 else 0

    score = round(potencial + facilidade + urgencia + oportunidade + bonus, 1)
    score = min(score, 100)

    if score >= 70:
        classificacao = "Alta prioridade"
    elif score >= 40:
        classificacao = "Média prioridade"
    else:
        classificacao = "Baixa prioridade"

    return {
        **padaria,
        "score": score,
        "classificacao": classificacao,
        "detalhe": {
            "potencial_pdv": round(potencial, 1),
            "facilidade_ativacao": facilidade,
            "urgencia": round(urgencia, 1),
            "oportunidade": oportunidade,
            "bonus_demanda_validada": bonus,
        },
    }


def priorizar_padarias(padarias: list[dict]) -> list[dict]:
    maior_volume = max(p["volume_cerveja_hl_mes"] for p in padarias) if padarias else 1
    ranqueadas = [calcular_prioridade(p, maior_volume) for p in padarias]
    return sorted(ranqueadas, key=lambda p: p["score"], reverse=True)


# ---------------------------------------------------------------------------
# Copiloto de vendas — diagnóstico de objeção por palavra-chave
# ---------------------------------------------------------------------------

OBJECOES = [
    {
        "chave": "marca_desconhecida",
        "titulo": "Marca desconhecida",
        "gatilhos": ["não conheço", "nunca vi", "quem é essa marca", "isso vende", "marca nova"],
        "argumento": (
            "Ancore na Heineken (credibilidade e distribuição) e cite o investimento "
            "recente em mídia (campanha no BBB gerou 2 bilhões de impactos no 1º semestre). "
            "Sugira começar pequeno: 1-2 sabores, para reduzir o risco percebido."
        ),
    },
    {
        "chave": "sem_espaco",
        "titulo": "Sem espaço na geladeira",
        "gatilhos": ["sem espaço", "não tenho espaço", "não tem espaço", "geladeira cheia", "não cabe"],
        "argumento": (
            "Proponha um trade simples: substituir o SKU de menor giro atual por 1 sabor "
            "FYS Zero. A lata 350ml é compacta e pensada para single serve — não exige "
            "aumento de espaço."
        ),
    },
    {
        "chave": "ja_vende_concorrente",
        "titulo": "Já vende o concorrente / cliente fiel a outra marca",
        "gatilhos": ["já vendo coca", "já vende coca", "vende coca", "já vendo outra marca", "já vende outra marca", "cliente é fiel", "não vou trocar", "já tenho fornecedor"],
        "argumento": (
            "Reforce que FYS complementa, não substitui: ocupa o espaço do consumidor que "
            "busca algo diferente ou menos açúcar e que hoje pode estar saindo sem comprar "
            "nada por falta de opção."
        ),
    },
    {
        "chave": "medo_nao_girar",
        "titulo": "Medo de não girar / produto encalhar",
        "gatilhos": ["medo de não vender", "vai encalhar", "não quero risco", "produto parado"],
        "argumento": (
            "Sugira um pedido inicial pequeno (1-2 caixas, 1 sabor) com visibilidade simples "
            "no balcão/geladeira, para gerar giro rápido e reduzir a decisão a baixo risco."
        ),
    },
    {
        "chave": "preco_margem",
        "titulo": "Preço / margem",
        "gatilhos": ["tá caro", "margem apertada", "desconto", "preço alto"],
        "argumento": (
            "Desloque o argumento de preço para giro incremental: é venda adicional (atende "
            "demanda hoje não atendida), não substituição de margem já conquistada."
        ),
    },
    {
        "chave": "sem_tempo_agora",
        "titulo": "Baixa prioridade / sem tempo agora",
        "gatilhos": ["depois a gente vê", "agora não", "me liga outro dia", "sem tempo"],
        "argumento": (
            "Peça uma decisão pequena e rápida — não 'adotar o portfólio', só 'testar 1 sabor "
            "por 2 semanas' — para não competir por atenção com decisões maiores do dono."
        ),
    },
]

DEFAULT_OBJECAO = {
    "chave": "generica",
    "titulo": "Situação não mapeada automaticamente",
    "argumento": (
        "Comece pela credibilidade Heineken + dado de zero açúcar (48% dos consumidores "
        "buscam menos açúcar) e proponha um teste pequeno de 1 sabor, sem pressionar o "
        "portfólio inteiro."
    ),
}


def diagnosticar_objecao(texto: str) -> dict:
    texto_norm = texto.lower()
    for objecao in OBJECOES:
        for gatilho in objecao["gatilhos"]:
            if gatilho in texto_norm:
                return objecao
    return DEFAULT_OBJECAO


def classificar_ticket(padaria: dict | None) -> str:
    if not padaria:
        return "Indefinido — sem dados do PDV"
    if padaria["classificacao"] == "Alta prioridade" and not padaria["vende_fys"]:
        return "Alto potencial de conversão — priorizar visita"
    if padaria["vende_fys"]:
        return "Cliente ativo — foco em expandir sortimento"
    return "Potencial moderado — abordagem padrão"


def gerar_resposta_copiloto(situacao: str, padaria: dict | None = None) -> dict:
    objecao = diagnosticar_objecao(situacao)

    contexto_pdv = ""
    if padaria:
        contexto_pdv = (
            f"{padaria['nome']} ({padaria['bairro']}) — "
            f"{'já vende FYS' if padaria['vende_fys'] else 'ainda não vende FYS'}, "
            f"espaço de geladeira {padaria['espaco_geladeira']}, "
            f"{padaria['dias_desde_ultima_visita']} dias sem visita."
        )

    mensagem_whatsapp = (
        f"Oi! Passando pra te apresentar rapidinho a FYS — refrigerante zero açúcar do "
        f"Grupo Heineken. {('Sei que já vende outras marcas por aí, ' if padaria and padaria.get('concorrencia') else '')}"
        f"topa testar 1 sabor por umas semanas pra ver a saída? Sem compromisso de "
        f"trocar tudo, só somar uma opção que o pessoal anda pedindo."
    )

    return {
        "leitura_situacao": situacao.strip(),
        "contexto_pdv": contexto_pdv or "Nenhum PDV selecionado — resposta genérica.",
        "diagnostico": objecao["titulo"],
        "classificacao_oportunidade": classificar_ticket(padaria),
        "argumento_recomendado": objecao["argumento"],
        "mensagem_whatsapp": mensagem_whatsapp,
        "proximo_passo": "Confirmar 1 sabor + quantidade de teste e agendar retorno em 2 semanas para checar giro.",
    }
