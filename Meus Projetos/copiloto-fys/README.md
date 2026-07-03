# Copiloto FYS — Copiloto de Vendas

Protótipo funcional feito para o desafio de IA aplicado à FYS (Grupo Heineken).
Resolve dois problemas em um único fluxo: **onde priorizar visitas** e **o que dizer**
quando o vendedor chega ao ponto de venda.

## 1. O problema de negócio

Padarias são um canal relevante para bebidas não alcoólicas (SP concentra 21% das
padarias do Brasil), mas a força de vendas prioriza naturalmente clientes de maior
volume — normalmente ligados à linha de cervejas. Resultado: a FYS captura hoje
apenas **0,9%** do mercado de refrigerante sem cola em padarias (245,8 mil HL),
mesmo o público de padaria (compra rápida, consumo individual) sendo o perfil ideal
para o portfólio single serve da marca.

Detalhes completos em [`knowledge/contexto-do-negocio.md`](knowledge/contexto-do-negocio.md).

## 2. A solução

Um **copiloto de duas frentes**, pensado para o vendedor/representante de campo:

1. **Priorização** — ranqueia as padarias da carteira por um score local (0–100),
   combinando potencial do PDV, facilidade de ativação, urgência de visita e
   oportunidade (já vende FYS ou não). Lógica documentada e auditável em
   [`knowledge/logica-priorizacao.md`](knowledge/logica-priorizacao.md).
2. **Copiloto de vendas** — o vendedor descreve a objeção do cliente em texto livre
   ("já vende Coca e não tem espaço") e recebe: diagnóstico da objeção, classificação
   da oportunidade, argumento recomendado, mensagem pronta para WhatsApp e o próximo
   passo sugerido. Base de objeções em
   [`knowledge/objecoes.md`](knowledge/objecoes.md).

**Importante:** por decisão de escopo, a "inteligência" aqui é **100% local**
(pontuação ponderada + casamento de palavras-chave), sem chamada a API de IA paga.
Isso torna o protótipo auditável, reprodutível e gratuito de rodar — e a mesma
estrutura de resposta poderia, no futuro, ser gerada por um LLM real sem mudar a
interface (ver seção 6).

## 3. Estrutura do repositório

```
copiloto-fys/
├── README.md
├── engine.py                  # motor de regras (priorização + diagnóstico de objeção)
├── copiloto_cli.py             # protótipo em linha de comando
├── data/
│   └── padarias.json           # dataset fictício de 12 padarias
├── knowledge/
│   ├── contexto-do-negocio.md  # o problema de negócio (padarias)
│   ├── produtos.md              # portfólio FYS e demais marcas do grupo
│   ├── objecoes.md               # objeções mapeadas + argumento recomendado
│   ├── perguntas-frequentes.md   # FAQ de marca usado como contexto do copiloto
│   └── logica-priorizacao.md     # fórmula do score, explicada
└── app/
└── index.html               # protótipo web (dashboard + chat), single-file
```

## 4. Como rodar

### Script (terminal)

```bash
cd copiloto-fys
python copiloto_cli.py
```
Mostra o ranking das 12 padarias, deixa você escolher uma como contexto e depois
descrever a situação do cliente para receber a orientação do copiloto.

### App web (dashboard + chat)

Não precisa de servidor nem instalação — é um único arquivo HTML com o dataset
embutido:

```bash
open copiloto-fys/app/index.html
```
(ou simplesmente arraste o arquivo para o navegador)

## 5. Exemplo de uso

**Entrada:** "ele disse que já vende Coca e não tem espaço"
**Padaria selecionada:** Padaria Trigo & Cia (Moema) — ainda não vende FYS

**Saída do copiloto:**
- **Diagnóstico:** Sem espaço na geladeira
- **Classificação:** Potencial moderado — abordagem padrão
- **Argumento:** Propor trade simples — substituir o SKU de menor giro por 1 sabor
  FYS Zero, sem aumentar o espaço ocupado (lata 350ml, single serve).
- **Mensagem pronta:** "Oi! Passando pra te apresentar rapidinho a FYS — refrigerante
  zero açúcar do Grupo Heineken. Sei que já vende outras marcas por aí, topa testar
  1 sabor por umas semanas pra ver a saída? Sem compromisso de trocar tudo, só somar
  uma opção que o pessoal anda pedindo."
- **Próximo passo:** Confirmar 1 sabor + quantidade de teste e agendar retorno em 2
  semanas para checar giro.

## 6. Simulação completa (saída real do terminal)

Execução real de `python copiloto_cli.py`, escolhendo a padaria #8 e descrevendo a
objeção "ele disse que já vende coca e não tem espaço":

```
=== Ranking de Priorização de Padarias ===


Padaria                     Bairro            Score   Classificação     Vende FYS?

1  Padaria Estrela do Sul      Ipiranga          83.0    Alta prioridade   Não
2  Padaria Bom Dia             Vila Mariana      72.7    Alta prioridade   Não
3  Padaria União               Mooca             70.7    Alta prioridade   Não
4  Padaria Boulevard           Itaim Bibi        65.0    Média prioridade  Não
5  Padaria Trigo & Cia         Moema             63.2    Média prioridade  Não
6  Padaria Central da Vila     Vila Madalena     63.1    Média prioridade  Não
7  Padaria Pão Quente 24h      Centro            60.5    Média prioridade  Não
8  Padaria Cantinho do Pão     Santo Amaro       58.7    Média prioridade  Não
9  Padaria Raízes              Campo Belo        56.9    Média prioridade  Não
10 Padaria Sabor da Manhã      Vila Prudente     52.3    Média prioridade  Não
11 Padaria Recanto Doce        Tatuapé           46.6    Média prioridade  Sim
12 Panificadora Nova Aurora    Pinheiros         32.7    Baixa prioridade  Sim

Digite o número da padaria para usar como contexto no copiloto (ou ENTER para pular): 8


=== Copiloto de Vendas ===

Descreva a situação/objeção do cliente (ex.: 'ele disse que já vende Coca e não tem espaço').

ele disse que já vende coca e não tem espaço

--- A) Leitura da situação ---
ele disse que já vende coca e não tem espaço

--- Contexto do PDV ---
Padaria Cantinho do Pão (Santo Amaro) — ainda não vende FYS, espaço de geladeira baixo, 95 dias sem visita.

--- B) Diagnóstico da objeção ---
Sem espaço na geladeira

--- C) Classificação da oportunidade ---
Potencial moderado — abordagem padrão

--- D) Argumento recomendado ---
Proponha um trade simples: substituir o SKU de menor giro atual por 1 sabor FYS Zero. A lata 350ml é compacta e pensada para single serve — não exige aumento de espaço.

--- E) Mensagem pronta para WhatsApp ---
Oi! Passando pra te apresentar rapidinho a FYS — refrigerante zero açúcar do Grupo Heineken. Sei que já vende outras marcas por aí, topa testar 1 sabor por umas semanas pra ver a saída? Sem compromisso de trocar tudo, só somar uma opção que o pessoal anda pedindo.

--- F) Próximo passo ---
Confirmar 1 sabor + quantidade de teste e agendar retorno em 2 semanas para checar giro.
Fim. Rode novamente para testar outra situação ou padaria.
```

- Repare que a Padaria Cantinho do Pão (#8) ficou em **Média prioridade** mesmo tendo
95 dias sem visita — isso acontece porque o score combina vários fatores ao mesmo
tempo (o espaço de geladeira baixo dela puxa a nota para baixo), não só a urgência
isolada. É esse equilíbrio entre fatores que o `knowledge/logica-priorizacao.md`
documenta em detalhe.

## 7. Limitações e próximos passos

- **Dataset fictício.** Em produção, `data/padarias.json` seria substituído por uma
  extração real do CRM/ERP comercial (volume, histórico de visita, sortimento atual).
- **Diagnóstico por palavra-chave.** Funciona bem para objeções recorrentes, mas não
  generaliza para frases fora do padrão mapeado (cai no fallback genérico). Trocar o
  motor de `diagnosticar_objecao()` por uma chamada a um LLM (ex.: Claude, via API) é
  o próximo passo natural — a estrutura de saída (diagnóstico → argumento → mensagem →
  próximo passo) já foi desenhada para não mudar quando isso acontecer.
- **Sem persistência.** O app web não salva qual padaria já foi visitada ou o
  resultado da abordagem — seria o requisito seguinte para um piloto real de campo.

## 8. Base de conhecimento

Todo o conteúdo usado pelo copiloto (portfólio, FAQ, objeções e contexto do negócio)
está em [`knowledge/`](knowledge/), separado da lógica de código — para que qualquer
pessoa da área comercial (não só quem programa) possa revisar e atualizar os
argumentos sem tocar no `engine.py`.