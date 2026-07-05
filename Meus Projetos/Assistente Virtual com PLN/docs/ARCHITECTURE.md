# Arquitetura

## Visão geral

O assistente segue uma arquitetura em camadas, isolando I/O (áudio,
rede) de lógica de negócio (roteamento de comandos), o que facilita
testes e extensão.

```
┌─────────────────────────────────────────────┐
│                 core/assistant.py            │  Orquestração (laço principal)
└───────────────┬───────────────┬─────────────┘
                 │               │
     ┌───────────▼───┐   ┌───────▼────────┐
     │ stt/           │   │ tts/            │  Camada de I/O de áudio
     │ SpeechToText   │   │ TextToSpeech    │
     └───────────┬───┘   └───────┬────────┘
                 │               │
        ┌────────▼───────────────▼────────┐
        │      commands/router.py          │  Roteamento
        │        CommandRouter             │
        └────────┬─────────────────────────┘
                  │
   ┌──────────────┼───────────────┬───────────────┐
   ▼               ▼               ▼               ▼
Wikipedia       YouTube         Farmácia          Piada
Command         Command         Command           Command
```

## Decisões de design

### Padrão Command para os comandos de voz

Cada ação disparada por voz implementa a interface `Command`
(`triggers`, `matches()`, `execute()`). O `CommandRouter` apenas
itera sobre a lista de comandos registrados e delega ao primeiro que
casar com o texto reconhecido. Isso segue o **princípio
Aberto/Fechado**: adicionar um comando novo (ex.: "tocar música")
significa criar uma nova classe e registrá-la — nenhum código
existente precisa ser modificado.

### Configuração via variáveis de ambiente

Seguindo os princípios de [12-factor app](https://12factor.net/pt_br/config),
nenhuma configuração (idioma, nomes de diretório, raio de busca) fica
hardcoded no código-fonte. Tudo é lido de variáveis de ambiente via
`python-dotenv`, permitindo comportamento diferente em dev/staging/produção
sem alterar uma linha de código.

### Geolocalização sem chave de API paga

O requisito "farmácia mais próxima" foi implementado com duas APIs
gratuitas e sem necessidade de cadastro/cartão de crédito:

1. **ip-api.com** — geolocalização aproximada a partir do IP público.
2. **Overpass API** (dados OpenStreetMap) — consulta de pontos de
   interesse (`amenity=pharmacy`) num raio configurável.

A distância real entre o usuário e cada farmácia candidata é
calculada com `geopy.distance.geodesic` (fórmula geodésica, mais
precisa que distância euclidiana em coordenadas).

> **Trade-off:** geolocalização por IP é aproximada (normalmente ao
> nível de cidade). Para maior precisão, seria necessário GPS real
> (ex.: em um app mobile) — fora do escopo de um assistente desktop.

### Logging estruturado em vez de `print()`

Todos os módulos usam um logger configurado centralmente
(`utils/logger.py`), com saída simultânea em console e em arquivo
rotativo (5 MB, 3 backups). Isso é essencial para depurar um processo
de longa duração rodando em produção/servidor, onde não há terminal
interativo para ler `print()`.

### Testabilidade

Todo I/O externo (microfone, gTTS, requisições HTTP) é isolado atrás
de classes com métodos pequenos e injeção de dependência simples
(`TextToSpeech`, `SpeechToText` são passados como parâmetros aos
comandos). Isso permite testar toda a lógica de negócio com mocks,
sem hardware real — ver `tests/`.
