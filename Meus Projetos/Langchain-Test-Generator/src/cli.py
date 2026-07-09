"""
cli.py
------
Ponto de entrada de linha de comando.

Uso:
    python -m src.cli calculadora
    python -m src.cli validador_cpf --provider gemini
"""
from __future__ import annotations

import argparse
import logging
import sys

from src.agent import TestGeneratorAgent
from src.llm_provider import get_llm
from src.logger_setup import setup_logging, write_run_report

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera testes unitários com LangChain + Azure OpenAI/Gemini."
    )
    parser.add_argument(
        "module_name",
        help="Nome do módulo em examples/ (sem .py), ex.: calculadora",
    )
    parser.add_argument(
        "--provider",
        choices=["azure", "gemini"],
        default=None,
        help="Força um provedor específico (senão usa fallback automático)",
    )
    args = parser.parse_args()

    setup_logging()
    llm = get_llm(force_provider=args.provider)
    agent = TestGeneratorAgent(llm=llm)

    result = agent.run(args.module_name)
    report_path = write_run_report(result)

    logger.info("Relatório salvo em: %s", report_path)
    if result.success:
        logger.info("✅ Testes gerados e passando para '%s'!", args.module_name)
        sys.exit(0)
    else:
        logger.error(
            "❌ Não foi possível gerar testes 100%% verdes após %s iterações.",
            result.iterations,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
