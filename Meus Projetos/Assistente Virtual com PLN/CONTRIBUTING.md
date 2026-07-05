# Guia de Contribuição

Obrigado por considerar contribuir com este projeto! Siga o fluxo abaixo.

## Fluxo de branches

- `main` — código estável, sempre "deployável"
- `develop` — integração de novas features
- `feature/<nome-da-feature>` — desenvolvimento de uma funcionalidade específica
- `fix/<nome-do-bug>` — correção de bug

## Passo a passo

1. Faça um fork do repositório e clone-o localmente.
2. Crie uma branch a partir de `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/minha-feature
   ```
3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Escreva testes para qualquer código novo (`tests/`).
5. Rode lint e testes localmente antes de commitar:
   ```bash
   flake8 src tests
   pytest
   ```
6. Siga o padrão de **Conventional Commits**:
   - `feat: adiciona comando de previsão do tempo`
   - `fix: corrige cálculo de distância da farmácia`
   - `docs: atualiza README com nova variável de ambiente`
   - `test: adiciona testes para o CommandRouter`
7. Abra um Pull Request para `develop`, descrevendo claramente o que
   foi alterado e por quê.

## Checklist do Pull Request

- [ ] Testes novos/atualizados cobrindo a mudança
- [ ] `pytest` passando localmente
- [ ] `flake8` sem erros
- [ ] Documentação (`README.md`/`docs/`) atualizada, se aplicável
- [ ] Nenhuma credencial ou dado sensível commitado

## Adicionando um novo comando de voz

Graças ao padrão *Command*, adicionar um comando novo é simples:

1. Crie um arquivo em `src/virtual_assistant/commands/meu_comando.py`
   implementando a interface `Command` (veja `commands/base.py`).
2. Registre a nova classe em `core/assistant.py`, na lista passada ao
   `CommandRouter`.
3. Adicione testes em `tests/test_commands.py`.
