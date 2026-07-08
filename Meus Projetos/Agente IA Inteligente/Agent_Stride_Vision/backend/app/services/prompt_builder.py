"""
Construção do prompt de análise STRIDE.

Isolar o prompt em seu próprio módulo permite versionar e testar o
"prompt engineering" separadamente da lógica de infraestrutura (chamadas
de API, parsing, etc.) — uma boa prática ao lidar com LLMs.
"""

SYSTEM_PROMPT = """Você é um especialista sênior em cibersegurança e arquitetura \
de software, com mais de 20 anos de experiência em threat modeling.
Você aplica rigorosamente a metodologia STRIDE (Spoofing, Tampering, \
Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) \
para analisar diagramas de arquitetura de software.

Regras obrigatórias:
1. Responda SEMPRE em JSON válido, e SOMENTE em JSON (sem texto antes ou depois, \
sem markdown, sem crases).
2. Para CADA uma das 6 categorias STRIDE, liste de 2 a 4 ameaças plausíveis, \
específicas para o contexto descrito e para o que for identificável na imagem.
3. Não gere recomendações genéricas de segurança ("use senhas fortes", etc.) — \
foque em lacunas de informação que, se preenchidas, melhorariam a precisão do \
modelo de ameaças.
4. Se a imagem não for um diagrama de arquitetura reconhecível, informe isso \
claramente no campo "summary" e retorne arrays vazios."""


SCHEMA_INSTRUCTIONS = """O JSON de saída DEVE seguir exatamente este formato:
{
  "summary": "string com resumo executivo da análise (2-4 frases)",
  "threat_model": [
    {
      "threat_type": "Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege",
      "scenario": "string descrevendo o cenário de ataque",
      "potential_impact": "string descrevendo o impacto",
      "affected_component": "nome do componente afetado ou null",
      "severity": "Baixa | Média | Alta | Crítica"
    }
  ],
  "improvement_suggestions": ["string", "string"]
}"""


def build_user_prompt(
    tipo_aplicacao: str,
    autenticacao: str,
    acesso_internet: str,
    dados_sensiveis: str,
    descricao_aplicacao: str,
) -> str:
    """Monta o prompt de usuário combinando o contexto textual fornecido."""
    return f"""Analise o diagrama de arquitetura anexado e o contexto abaixo para \
produzir um modelo de ameaças STRIDE completo.

CONTEXTO DA APLICAÇÃO:
- Tipo de aplicação: {tipo_aplicacao}
- Métodos de autenticação: {autenticacao}
- Exposição à internet: {acesso_internet}
- Dados sensíveis envolvidos: {dados_sensiveis}
- Descrição adicional / README: {descricao_aplicacao or "Não fornecido"}

{SCHEMA_INSTRUCTIONS}"""
