# Changelog

Este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-07-03

### Adicionado
- Módulo Text-to-Speech baseado em `gTTS`.
- Módulo Speech-to-Text baseado em `SpeechRecognition` (Google Speech API).
- Comando de voz: pesquisa e resumo no Wikipedia.
- Comando de voz: busca no YouTube.
- Comando de voz: localização da farmácia mais próxima (IP geolocation + Overpass API).
- Comando de voz: contar piadas.
- Roteador de comandos extensível (padrão Command).
- Configuração via `.env` (12-factor app).
- Logging estruturado com rotação de arquivos.
- Suíte de testes automatizados com `pytest` e mocks (sem dependência de hardware).
- Dockerfile e `docker-compose.yml` para execução em produção.
- Pipeline de CI no GitHub Actions (lint + testes + build Docker).
- Documentação completa (README, arquitetura, contribuição).

### Baseado em
- Exemplos originais do curso: `Text-to-Speech-DIO.py` e `Speech-to-text.py`.
