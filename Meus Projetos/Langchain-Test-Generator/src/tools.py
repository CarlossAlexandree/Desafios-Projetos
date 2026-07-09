"""
tools.py
--------
Funções que o agente usa para "agir sobre o ambiente": ler código-fonte,
escrever arquivos de teste e executar o pytest de verdade.

Conceito: no LangChain, uma `Tool` é qualquer função com uma descrição
clara o suficiente para o modelo (ou nosso orquestrador) decidir quando
usá-la. Aqui expomos essas funções tanto como utilitárias em Python puro
quanto, opcionalmente, como `Tool` do LangChain (ver `as_langchain_tools`).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EXAMPLES_DIR = Path("examples")
TESTS_DIR = Path("tests")


def read_source_code(module_name: str, base_dir: Path = EXAMPLES_DIR) -> str:
    """Lê o conteúdo de `{module_name}.py`."""
    path = base_dir / f"{module_name}.py"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def write_test_file(module_name: str, content: str, base_dir: Path = TESTS_DIR) -> Path:
    """Escreve/atualiza `tests/test_{module_name}.py`."""
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"test_{module_name}.py"
    path.write_text(content, encoding="utf-8")
    return path


def run_pytest(test_path: Path) -> tuple[bool, str]:
    """
    Executa `pytest` no arquivo indicado usando o mesmo interpretador
    Python do processo atual (evita problemas de PATH no Colab/venv).

    Retorna (sucesso, saída_completa).
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
        capture_output=True,
        text=True,
    )
    output = result.stdout + "\n" + result.stderr
    return result.returncode == 0, output


def as_langchain_tools(agent_callbacks: dict):
    """
    Expõe as funções acima como `Tool` do LangChain, caso se queira
    plugar num AgentExecutor clássico (ReAct) em vez do orquestrador
    determinístico usado em `agent.py`. Mantido como opção didática.
    """
    from langchain_core.tools import Tool

    return [
        Tool(
            name="LerCodigoFonte",
            func=lambda module_name: read_source_code(module_name),
            description="Lê o conteúdo de um módulo Python em examples/. Entrada: nome do módulo sem .py",
        ),
        Tool(
            name="EscreverArquivoDeTeste",
            func=lambda args: str(write_test_file(*args.split("|", 1))),
            description="Escreve um arquivo de teste. Entrada: 'nome_modulo|conteudo'",
        ),
        Tool(
            name="RodarPytest",
            func=lambda test_path: run_pytest(Path(test_path)),
            description="Executa pytest em um caminho de arquivo de teste e retorna (sucesso, saída).",
        ),
    ]
