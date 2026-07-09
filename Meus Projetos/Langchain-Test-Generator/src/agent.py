"""
agent.py
--------
O "agente" do projeto: percebe o ambiente (código-fonte, resultado do
pytest), decide a próxima ação (gerar, rodar, corrigir) e age sobre o
sistema de arquivos — fechando o ciclo TDD (Red -> Green -> Refactor)
de forma automatizada.

Por que um orquestrador customizado em vez de
`initialize_agent(..., AgentType.ZERO_SHOT_REACT_DESCRIPTION)`?
- Essa API está deprecada nas versões atuais do LangChain.
- Nosso fluxo é bem definido (gerar -> rodar -> corrigir se falhar),
  então um loop explícito é mais previsível, mais barato em tokens e
  mais fácil de debugar do que um agente ReAct genérico — uma escolha
  de engenharia consciente, não uma limitação.
- As ferramentas (`tools.py`) continuam expostas também como `Tool`
  do LangChain (`as_langchain_tools`) para quem quiser plugar um
  AgentExecutor ReAct por cima, se desejar explorar esse padrão.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from src.chains import build_refactor_chain, build_test_generation_chain
from src.config import settings
from src.llm_provider import get_llm
from src.tools import read_source_code, run_pytest, write_test_file

logger = logging.getLogger(__name__)


@dataclass
class TDDResult:
    module_name: str
    success: bool
    iterations: int
    test_file: Path
    final_output: str
    history: list[str] = field(default_factory=list)


class TestGeneratorAgent:
    """Agente de geração de testes unitários com ciclo TDD automático."""

    def __init__(self, llm=None, max_iterations: int | None = None):
        self.llm = llm or get_llm()
        self.max_iterations = max_iterations or settings.max_tdd_iterations
        self.generation_chain = build_test_generation_chain(self.llm)
        self.refactor_chain = build_refactor_chain(self.llm)

    def run(self, module_name: str) -> TDDResult:
        """
        Executa o ciclo completo para um módulo em examples/{module_name}.py:

          1) PERCEBER   -> lê o código-fonte
          2) RED        -> gera a primeira versão dos testes (ainda não roda)
          3) GREEN      -> roda pytest; se passar, termina
          4) REFACTOR   -> se falhar, envia o erro real ao LLM e corrige
                           o teste, repetindo até `max_iterations`
        """
        history: list[str] = []
        source_code = read_source_code(module_name)
        logger.info("Gerando testes iniciais para '%s'...", module_name)

        test_code = self.generation_chain.invoke(
            {"module_name": module_name, "source_code": source_code}
        )
        test_path = write_test_file(module_name, test_code)
        history.append(f"[iter 0] Testes gerados em {test_path}")

        success, output = run_pytest(test_path)
        history.append(f"[iter 0] pytest sucesso={success}")

        iteration = 0
        while not success and iteration < self.max_iterations:
            iteration += 1
            logger.warning(
                "Testes falharam (iteração %s/%s). Corrigindo com base no erro real...",
                iteration,
                self.max_iterations,
            )
            test_code = self.refactor_chain.invoke(
                {
                    "module_name": module_name,
                    "source_code": source_code,
                    "test_code": test_code,
                    "pytest_output": output,
                }
            )
            test_path = write_test_file(module_name, test_code)
            success, output = run_pytest(test_path)
            history.append(f"[iter {iteration}] pytest sucesso={success}")

        return TDDResult(
            module_name=module_name,
            success=success,
            iterations=iteration,
            test_file=test_path,
            final_output=output,
            history=history,
        )
