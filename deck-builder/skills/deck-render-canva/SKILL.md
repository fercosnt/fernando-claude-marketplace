---
name: deck-render-canva
description: Leva o STORYBOARD.md para o Canva — escreve o briefing de montagem nas notas de cada pagina e publica o comentario-indice (modo `anotar`), e preenche brand template quando houver (modo `render`). Use ao pedir "anotar o deck no Canva", "por o briefing nas notas", "montar a base no Canva", "gerar o deck a partir do storyboard".
intent: action
effort: medium
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/briefing-de-montagem.md
  - references/transacao-edicao-canva.md
assets:
  - evals/render-canva-cases.md
---

# deck-render-canva

Skill do plugin `deck-builder` (v2.0.0). Faz a ponte entre o `STORYBOARD.md` e o
Canva, em **dois modos independentes**.

| Modo | O que faz | Estado |
|------|-----------|--------|
| **`anotar`** | Escreve o briefing de montagem nas notas de cada pagina de um design que **ja existe**, e publica o comentario-indice | **Disponivel** — validado em campo |
| **`render`** | Cria o deck a partir de brand template da marca e preenche os campos | **Bloqueado** — ver "Pre-requisito do modo render" |

Os dois sao **opt-in** (D16). Sem MCP do Canva conectado, nenhum e oferecido.

## Por que dois modos, e por que o `anotar` vem primeiro

O `anotar` **nao depende de brand template**. Ele opera sobre qualquer design que
ja exista — inclusive um montado a mao. Foi assim que a hipotese foi validada em
2026-08-23: a redatora recebeu um deck anotado, montou em cima e respondeu **"nao
abri o markdown"**.

O `render` depende de brand template, que hoje nao existe na conta.

Separar os dois foi decisao de realidade: a metade que funciona nao pode ficar
refem da metade que esta travada.

## Fronteiras (§10.8)

- NAO gera slides finais sem pedido explicito (D15). Esta e a **unica** skill do
  plugin autorizada a render, e so em modo `render`, opt-in.
- NAO publica, compartilha nem move de pasta (Fronteira nº 10). Entrega o link de
  edicao e para.
- NAO escreve texto de anotacao na camada visual da pagina (RF-40). Anotacao vive
  em notas e comentario.
- NAO cai para geracao livre quando falta template (D19).
- NAO persegue acabamento visual (D20).

---

# Modo `anotar`

## Passo 1 — parear storyboard e design

Precisa de duas coisas: o `STORYBOARD.md` e o `design_id` do Canva.

- Confira que a **contagem de paginas bate** com a de slides do storyboard.
- Se nao bater, **mostre o mapeamento proposto e peca confirmacao** antes de
  escrever. Gerador de deck reestrutura por conta propria — 13 slides ja viraram
  12 paginas numa execucao real.
- Numeracao espelha o storyboard (D18).

## Passo 2 — compor os briefings

Contrato completo em [`shared/briefing-annotation-contract.md`](../../shared/briefing-annotation-contract.md)
e redacao em [references/briefing-de-montagem.md](references/briefing-de-montagem.md).

Quatro rotulos, nesta ordem, teto de **900 caracteres**:

```
▪ BRIEFING DE MONTAGEM · slide NN/TT · tipo

PROVAR
   Por que este slide existe no arco.

ESCREVER
   Qual e a tarefa de escrita nesta pagina.

NAO MEXER
   Decisao fechada ou trava de compliance.

DECIDIR
   O que esta em aberto para quem monta.

▪ FIM DO BRIEFING
```

**Olhe a pagina antes de escrever.** O `ESCREVER` so vale se refletir o que
aquela pagina **realmente tem** — "veio com dois blocos quando o storyboard pedia
um", "os titulos vieram em ingles", "falta o tailwind dos 78%". Briefing generico
nao ajuda ninguem.

## Passo 3 — escrever nas notas

Uma pagina por chamada, via `replace_speaker_notes`:

- **Prefixe** — nunca substitua o campo. As notas do apresentador ficam abaixo
  do marcador de fim (D22).
- Notas ja com mais de 4.100 chars: nao cabe. Grave so a linha de origem e liste
  a pagina como "briefing omitido" no indice.
- **Falha no meio → `finalize: "cancel"`.** Deck parcialmente anotado e pior que
  deck sem anotacao, porque a ausencia passa a significar duas coisas (RNF-14).

## Passo 4 — comentario-indice

Um unico `comment-on-design`, <= 1.000 chars, com: caminho do storyboard,
pendencias, slides com `[VERIFICAR]`, e como ler e limpar o briefing.

A API **nao ancora comentario em pagina** — por isso ele e indice do deck, nunca
anotacao de slide.

## Passo 5 — manifesto

Grave `DECKLINK-{slug}-{HHmm}.md` em `$DECKS_DIR/{YYYY-MM}/` com storyboard ↔
design_id ↔ mapa slide→pagina **e o hash do briefing de cada pagina** (insumo da
limpeza).

## Rota `--limpar-briefing {design_id}`

Antes de apresentar. Para cada pagina, compara o bloco com o hash do `DECKLINK`:

| Estado | Acao |
|--------|------|
| Identico ao gerado | Remove em silencio |
| **Divergente** | **Arquiva** em `## Recados arquivados` no `DECKLINK` e so entao remove |
| Marcador quebrado | **Nao remove nada.** Reporta a pagina |

Reporte quantas paginas foram limpas e quantos recados foram arquivados. As
notas do apresentador precisam voltar **byte a byte** iguais.

---

# Modo `render`

## Pre-requisito do modo render

```
search-brand-templates(design_types: ["presentation"])
```

Lista vazia → **nao renderize**. Informe que falta brand template da marca e
ofereca o modo `anotar` sobre um deck existente.

> **Estado em 2026-08-23:** a conta nao tem brand template nenhum, e
> `publish-brand-template` falha. Pode ser escopo ausente
> (`brandtemplate:content:write` — reconectar o conector) ou recurso de plano
> (Teams/Enterprise). Detalhe em [`shared/canva-render-contract.md`](../../shared/canva-render-contract.md).

## Preenchimento

`create-design-from-brand-template` → `read-design` com `open_transaction` →
edicao por `locator_id` → validar → commit.

**Nao existe `autofill-design` neste conector.** `get-brand-template-dataset`
serve so para diagnostico.

### A regra que quebra deck se ignorada

`replace_text` **nao preserva formatacao** — reaplica defaults em `lineHeight`,
`listMarker` e `listLevel`. Receita obrigatoria:

| Elemento | Como |
|----------|------|
| Regiao unica | `replace_text` → `format_text` restaurando os atributos capturados → `position_element` restaurando `top`/`left` |
| Regioes mistas (negrito + normal) | **`find_and_replace_text`**, que preserva sozinho |

E **largura renderizada**, nao numero de caracteres: `"00%"` quebrou linha onde
`"62%"` cabia. Detalhe e medicoes em [references/transacao-edicao-canva.md](references/transacao-edicao-canva.md).

### Tabela: o limite duro

A API **nao cria tabela** e **nao preenche celula**. Tabela nativa e elemento
`type: "sheet"`, opaco: escrita retorna `not_supported: "sheet-element has no
text content"`.

- Slide com tabela **exige** template que ja a contenha (D19).
- O preenchimento da tabela e humano, mesmo com template.
- **Proibido** simular tabela com retangulos + caixas de texto.

## Tipo sem template (D19)

**Reporta e pula.** Nunca cai para geracao livre. Nao e preferencia estetica: no
render manual de 2026-08-12, a geracao livre descartou em silencio o slide de
disclaimer CVM 160/22, o footnote de compliance cfo-cfm e o qualificador
metodologico de um NPS.

---

## Handoff opt-in nas verticais (D16)

Oferecido via `AskUserQuestion` ao fim das 8 verticais, **nunca automatico**.
Com o MCP desconectado, nem e oferecido. Recusa encerra o fluxo — nao insiste.

## Regras inviolaveis (DoD)

- **D22:** briefing e prefixado e delimitado por marcador. Nota do apresentador nunca e sobrescrita.
- **D23:** 4 rotulos, 900 chars. Quinto rotulo exige nova decisao D.
- **D26:** limpeza nunca descarta escrita humana sem arquivar.
- **D19:** sem template, sem geracao livre.
- **RF-40:** nenhuma anotacao na camada visual.
- **RNF-14:** falha no meio cancela a transacao inteira.
- Nada e publicado, compartilhado ou movido de pasta.

## Eval cases

[evals/render-canva-cases.md](evals/render-canva-cases.md).

## Cross-references

- [`shared/briefing-annotation-contract.md`](../../shared/briefing-annotation-contract.md)
- [`shared/canva-render-contract.md`](../../shared/canva-render-contract.md)
- [`shared/output-convention.md`](../../shared/output-convention.md)
