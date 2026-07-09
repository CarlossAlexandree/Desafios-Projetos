"""
chains.py
---------
Aqui montamos as "Chains" (no sentido moderno do LangChain: LCEL —
LangChain Expression Language, o operador `|`) que conectam
Prompt -> LLM -> Parser.

Nota de boas práticas: a antiga classe `LLMChain` está deprecada desde
o LangChain 0.1+. O padrão atual e recomendado é compor Runnables com
o operador `|`, que é o que fazemos abaixo.
"""
from __future__ import annotations

import re

from langchain_core.output_parsers import StrOutputParser

from src.prompts import REFACTOR_PROMPT, TEST_GENERATION_PROMPT


def _strip_markdown_fences(text: str) -> str:
    """
    Rede de segurança: mesmo pedindo "sem markdown" no prompt, LLMs às
    vezes envolvem a resposta em ```python ... ```. Removemos aqui para
    garantir um .py válido.
    """
    text = text.strip()
    text = re.sub(r"^```(?:python)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip() + "\n"


def build_test_generation_chain(llm):
    """Chain: código-fonte -> conteúdo do arquivo de teste (str limpa)."""
    return TEST_GENERATION_PROMPT | llm | StrOutputParser() | _strip_markdown_fences


def build_refactor_chain(llm):
    """Chain: teste com falha + erro do pytest -> teste corrigido (str limpa)."""
    return REFACTOR_PROMPT | llm | StrOutputParser() | _strip_markdown_fences
