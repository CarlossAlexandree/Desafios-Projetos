"""
logger_setup.py
---------------
"Monitoramento" leve e apropriado para um projeto deste porte:
- Logging estruturado em console + arquivo (logs/run.log)
- Um relatório em Markdown por execução (logs/report_<modulo>.md),
  fácil de anexar como artefato no CI/CD ou ler no Colab.

Para um projeto maior em produção real, isso evoluiria para algo como
OpenTelemetry + Grafana, mas aqui mantemos simples de propósito
(o usuário pediu para não pesar o projeto).
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from src.config import settings

LOGS_DIR = Path("logs")


def setup_logging() -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOGS_DIR / "run.log", encoding="utf-8"),
        ],
    )


def write_run_report(result) -> Path:
    """Gera um relatório Markdown simples a partir de um TDDResult."""
    LOGS_DIR.mkdir(exist_ok=True)
    report_path = LOGS_DIR / f"report_{result.module_name}.md"

    status_emoji = "✅" if result.success else "❌"
    lines = [
        f"# Relatório de Geração de Testes — `{result.module_name}`",
        "",
        f"**Data/hora:** {datetime.now().isoformat(timespec='seconds')}",
        f"**Status final:** {status_emoji} {'SUCESSO' if result.success else 'FALHA'}",
        f"**Iterações do ciclo TDD:** {result.iterations}",
        f"**Arquivo de teste:** `{result.test_file}`",
        "",
        "## Histórico do ciclo Red-Green-Refactor",
        "",
    ]
    lines += [f"- {h}" for h in result.history]
    lines += ["", "## Saída final do pytest", "", "```", result.final_output.strip(), "```"]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
