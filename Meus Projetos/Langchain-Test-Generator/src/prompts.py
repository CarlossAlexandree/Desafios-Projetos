"""
prompts.py
----------
Templates de prompt usados nas chains. Mantidos separados do código de
orquestração para facilitar iteração/ajuste fino (uma boa prática:
prompts são "configuração", não deveriam ficar misturados à lógica).
"""
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------------------------------------
# Prompt principal: gera um arquivo de teste pytest a partir de código-fonte
# ---------------------------------------------------------------------
TEST_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um engenheiro de qualidade de software sênior, especialista "
            "em Python e pytest. Você gera SOMENTE código Python puro, nunca "
            "explicações em texto e nunca cercas de código markdown (```).",
        ),
        (
            "human",
            """Gere um arquivo de testes unitários com pytest para o código-fonte abaixo.

Regras obrigatórias:
1. A primeira linha do arquivo deve ser exatamente: import pytest
2. Toda função de teste deve começar com `def test_`.
3. Cubra casos de SUCESSO (caminho feliz) e de FALHA/borda
   (valores inválidos, exceções esperadas, limites).
4. Use `pytest.raises` quando a função original deve lançar exceção.
5. Importe as funções/classes do módulo `{module_name}` usando:
   from {module_name} import <nomes>
6. Não inclua nenhum texto fora do código Python (nada de ```python, nada de comentários explicativos longos).
7. O arquivo deve ser executável diretamente com `pytest`.

Código-fonte ({module_name}.py):
---
{source_code}
---

Gere agora o conteúdo completo do arquivo test_{module_name}.py:""",
        ),
    ]
)

# ---------------------------------------------------------------------
# Prompt de refatoração: usado no ciclo TDD quando os testes falham
# ---------------------------------------------------------------------
REFACTOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um engenheiro de qualidade de software sênior. Você corrige "
            "arquivos de teste pytest com base na saída de erro real do pytest. "
            "Você gera SOMENTE código Python puro, sem markdown.",
        ),
        (
            "human",
            """O arquivo de teste abaixo falhou ao rodar com pytest.

Código-fonte original ({module_name}.py):
---
{source_code}
---

Arquivo de teste atual (test_{module_name}.py):
---
{test_code}
---

Saída de erro do pytest:
---
{pytest_output}
---

Corrija o arquivo de teste para que todos os testes passem, mantendo a
cobertura de casos de sucesso e falha. Regras:
1. Primeira linha: import pytest
2. Não altere o código-fonte, apenas o teste.
3. Nenhum texto fora do código Python.

Gere agora o conteúdo COMPLETO e CORRIGIDO de test_{module_name}.py:""",
        ),
    ]
)
