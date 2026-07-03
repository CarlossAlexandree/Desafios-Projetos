#!/usr/bin/env python3
"""
Copiloto FYS — CLI
Priorização de padarias + copiloto de vendas (objeções e mensagens), 100% local.

Uso:
    python3 copiloto_cli.py
"""
from pathlib import Path

from engine import carregar_padarias, priorizar_padarias, gerar_resposta_copiloto

DATA_PATH = Path(__file__).parent / "data" / "padarias.json"


def imprimir_ranking(ranking: list[dict]) -> None:
    print("\n=== Ranking de Priorização de Padarias ===\n")
    print(f"{'#':<3}{'Padaria':<28}{'Bairro':<18}{'Score':<8}{'Classificação':<18}{'Vende FYS?'}")
    print("-" * 95)
    for i, p in enumerate(ranking, 1):
        vende = "Sim" if p["vende_fys"] else "Não"
        print(f"{i:<3}{p['nome']:<28}{p['bairro']:<18}{p['score']:<8}{p['classificacao']:<18}{vende}")


def escolher_padaria(ranking: list[dict]):
    escolha = input(
        "\nDigite o número da padaria para usar como contexto no copiloto "
        "(ou ENTER para pular): "
    ).strip()
    if not escolha:
        return None
    try:
        idx = int(escolha) - 1
        return ranking[idx]
    except (ValueError, IndexError):
        print("Número inválido, seguindo sem contexto de PDV.")
        return None


def rodar_copiloto(padaria) -> None:
    print("\n=== Copiloto de Vendas ===")
    print("Descreva a situação/objeção do cliente (ex.: 'ele disse que já vende Coca e não tem espaço').")
    situacao = input("> ").strip()
    if not situacao:
        print("Nada digitado, encerrando.")
        return

    resposta = gerar_resposta_copiloto(situacao, padaria)

    print("\n--- A) Leitura da situação ---")
    print(resposta["leitura_situacao"])
    print("\n--- Contexto do PDV ---")
    print(resposta["contexto_pdv"])
    print("\n--- B) Diagnóstico da objeção ---")
    print(resposta["diagnostico"])
    print("\n--- C) Classificação da oportunidade ---")
    print(resposta["classificacao_oportunidade"])
    print("\n--- D) Argumento recomendado ---")
    print(resposta["argumento_recomendado"])
    print("\n--- E) Mensagem pronta para WhatsApp ---")
    print(resposta["mensagem_whatsapp"])
    print("\n--- F) Próximo passo ---")
    print(resposta["proximo_passo"])


def main() -> None:
    print("Copiloto FYS — Priorização de Padarias + Copiloto de Vendas (protótipo local)")
    padarias = carregar_padarias(str(DATA_PATH))
    ranking = priorizar_padarias(padarias)
    imprimir_ranking(ranking)

    padaria = escolher_padaria(ranking)
    rodar_copiloto(padaria)

    print("\nFim. Rode novamente para testar outra situação ou padaria.")


if __name__ == "__main__":
    main()
