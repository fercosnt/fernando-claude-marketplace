# Working Backwards Amazon (6-pager + PR/FAQ) — Anexo `pitch-to-leadership`

Quase sempre obrigatorio em modo `pitch-to-leadership` da skill `deck-internal`. NAO substitui slides — anexa.

---

## Origem e racional

Jeff Bezos baniu PowerPoint em reunioes seniores da Amazon em **2004** por uma razao explicita:

> "Narrativa forca melhor pensamento, melhor entendimento do que importa mais e como as coisas se relacionam." — Bezos memo interno

Slides escondem raciocinio incompleto atras de bullets. Prosa narrativa forca o autor a articular logica causal explicita.

Custo de tempo e alto — so vale para decisoes de alto impacto (~aprovar projeto, alocar capital, mudar estrategia).

---

## O 6-pager (variante Strategic / Planning memo)

Memorando narrativo de **6 paginas** — sem bullets, sem slides, sem graficos embutidos. Apendice ilimitado para dados de suporte.

### Estrutura canonica

1. **Introducao** — Contexto e escopo
2. **Goals (Objetivos)** — Metricas de sucesso no inicio (lente de analise)
3. **Tenets** — Principios orientadores nao-negociaveis
4. **State of the Business** — Estrutura, execucao, desempenho vs metas; positivos e negativos
5. **Lessons Learned** — O que funcionou/nao funcionou, com dados (refs ao apendice)
6. **Strategic Priorities** — Acoes especificas, responsaveis, cronograma

### Regras de escrita (LOCKED)

- Maximo **30 palavras por sentenca**
- Adjetivos → dados ("melhor" → "23% mais rapido")
- Zero jargao corporativo
- Prosa densa, logica causal explicita
- Voz unica (NAO comite — uma pessoa escreve, outros revisam)
- **Sem bullets** no corpo principal (apendice pode ter)
- **Sem graficos embutidos** no corpo (vao para apendice)

### Variante 2 — New Initiative memo

Primeira pagina = Press Release ficticia (ver secao PR/FAQ abaixo). Demais 5 paginas = FAQ.

---

## Protocolo de reuniao (study hall)

1. Memos impressos e distribuidos no inicio da reuniao
2. **20-30 min de leitura silenciosa** (study hall)
3. Computador desencorajado na leitura — concentracao em prosa
4. Discussao comeca SO apos leitura completa de todos
5. Silencio de leitura e sagrado — nao interromper

Cofunda com decisao na sala. O memo carrega toda a informacao; a discussao foca em decisao e ajustes, nao em apresentacao.

---

## PR/FAQ Method (Working Backwards)

Logica: escrever a **nota de imprensa ficticia + FAQ ANTES de construir** o produto.

### Press Release (< 1 pagina)

1. **Heading** (nome do produto em linguagem do cliente)
2. **Subheading** (cliente + beneficio principal em 1 sentenca)
3. **Summary** (local, data ficticia, resumo)
4. **Problem** (sob perspectiva do cliente, NAO da empresa)
5. **Solution** (como resolve, simples e diferenciada)
6. **Quotes & Getting Started** (porta-vozes ficticios + acesso)

### FAQ Externo

Perguntas do cliente: preco, funcionamento, suporte, onde comprar.

### FAQ Interno (ate 5 paginas)

- TAM (mercado total)
- Alternativas (build/buy/partner)
- Diferenciais mensuraveis
- 3 razoes para falhar
- Problemas tecnicos/legais
- Mudanca de comportamento do cliente requerida
- Retorno vs investimento (NPV/payback)

### Criterio eliminatorio

Se a PR ficticia NAO descreve produto **mensuravelmente melhor** (mais rapido, mais barato, ou muda qualitativamente a experiencia), NAO vale construir.

PR funciona como **filtro de ideia antes de qualquer codigo**. Validado em: AWS S3/EC2, Amazon Prime, Kindle, Amazon Studios.

---

## Quando usar em `pitch-to-leadership`

**Quase sempre obrigatorio** quando:
- Ask envolve recurso significativo (≥R$50k ou ≥1 FTE)
- Decisao tem impacto multi-trimestral
- Audiencia tem habito de leitura previa (CEOs maduros, boards estruturados)
- Marca Beauty Smile / Fotona em decisoes estrategicas

**Opcional** quando:
- Pitch curto 1:1 de aprovacao tatica
- Decisao reversivel rapidamente
- Audiencia sem habito de leitura (raro — preferir gerar mesmo assim)

---

## Adaptacao Brasil para 6-pager

Bezos exige study hall (leitura silenciosa) — modelo dificil de impor em culturas relacionais.

Adaptacao recomendada:
1. Enviar 6-pager por email **24-48h antes** da reuniao
2. Comecar reuniao perguntando "O que ressoou? O que ficou confuso?" — preserva abertura relacional
3. NAO ler em silencio na reuniao (cultura BR estranha)
4. Apresentacao verbal segue o 6-pager mas inicia com reciprocidade ("Obrigado pela leitura, alguma pergunta de partida?")

---

## Asset associado

Template skeleton em [../assets/templates/amazon-6pager-skeleton.md](../assets/templates/amazon-6pager-skeleton.md).

Gerado pela skill em arquivo separado: `STORYBOARD-{slug}-{HHmm}.6pager.md` no mesmo diretorio do STORYBOARD principal.

---

## Cases canonicos validados

- AWS S3 (2006) — PR/FAQ escrita ANTES do desenvolvimento, validada em 2 anos
- AWS EC2 (2006) — mesmo padrao
- Amazon Prime (2005) — PR/FAQ revelou friccao de aquisicao do cliente
- Kindle (2007) — PR/FAQ forcou clareza sobre experiencia de leitura
- Amazon Studios (2010) — PR/FAQ usado para greenlight de series

Fonte: livro *Working Backwards* (Colin Bryar & Bill Carr, 2021) + memos Bezos publicos + Bryar/Carr Working Backwards podcast.
