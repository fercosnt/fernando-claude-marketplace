# Review: {NOME_DECK}

## Meta
- STORYBOARD revisado: {BASENAME_ORIGINAL} (versao v{VERSAO})
- Reviewer rodado em: {ISO_DATE}
- Criticos aplicados: clareza + persuasao{COPY_STATUS} + SUCCESs
- max_ctas (lido da Meta): {MAX_CTAS_EFETIVO} (default vertical: {VERTICAL_DEFAULT})
- Vertical: deck-{VERTICAL}
- Big Idea: {BIG_IDEA}

## Issues por severidade

### 🔴 BLOCKER (resolver ANTES de apresentar)

{LOOP_BLOCKER — cada item:}
- **Slide {N} — Tipo {TIPO}:** {PROBLEMA_CONCRETO}
  Sugestao: {ACAO_ESPECIFICA}
  Critico(s): {CRITICOS}
{/LOOP_BLOCKER}

{SE_VAZIO_BLOCKER: "_(nenhum blocker)_"}

### 🟡 MAJOR (resolver se sobrar tempo)

{LOOP_MAJOR}
- **Slide {N} — Tipo {TIPO}:** {PROBLEMA_CONCRETO}
  Sugestao: {ACAO_ESPECIFICA}
  Critico(s): {CRITICOS}
{/LOOP_MAJOR}

{SE_VAZIO_MAJOR: "_(nenhum major)_"}

### 🟢 MINOR (pular se urgente)

{LOOP_MINOR}
- **Slide {N} — Tipo {TIPO}:** {PROBLEMA_CONCRETO}
  Sugestao: {ACAO_ESPECIFICA}
  Critico(s): {CRITICOS}
{/LOOP_MINOR}

{SE_VAZIO_MINOR: "_(nenhum minor)_"}

## Recommended next action

{RECOMMENDED_ACTION}

## Observacoes do reviewer

{OBSERVACOES_OPCIONAIS — incluir somente se relevante:}
- Pontos fortes detectados: {EX: "Action titles consistentes em 11/13 slides", "Big Idea bem destilada"}
- Limitacoes da revisao: {EX: "/copy indisponivel — Critico Persuasao usou heuristico", "NB1 nao consultado por timeout"}
{/OBSERVACOES_OPCIONAIS}

---

_Reviewer: deck-reviewer (parte do plugin deck-builder)_
_Sem score numerico por design (D9). Severidades categoricas + acao recomendada._

<!--
INSTRUCOES DE PREENCHIMENTO (consumir e remover antes de salvar):

PLACEHOLDERS:
- {NOME_DECK}            = Meta.nome_deck do STORYBOARD original
- {BASENAME_ORIGINAL}    = nome do arquivo .md sem path (ex: STORYBOARD-anjo-1647.md)
- {VERSAO}               = Meta.versao (v1 / v2 / etc)
- {ISO_DATE}             = timestamp ISO da execucao do reviewer
- {COPY_STATUS}          = "" se /copy disponivel; " (heuristico — /copy indisponivel)" se fallback
- {MAX_CTAS_EFETIVO}     = max_ctas lido da Meta OU default da vertical
- {VERTICAL_DEFAULT}     = default da tabela em SKILL.md §max_ctas
- {VERTICAL}             = ex: "fundraising" / "teaching" / etc.
- {BIG_IDEA}             = Meta.big_idea
- LOOPS                  = renderizar 1 bullet por issue do bucket; ordem por slide_n asc
- {CRITICOS}             = lista deduplicada: ex "clareza" ou "clareza, success" se 2 criticos pegaram
- {RECOMMENDED_ACTION}   = aplicar tabela do SKILL.md §recommended-next-action

EXCLUIR ESTE BLOCO HTML COMMENT ANTES DE GRAVAR O ARQUIVO FINAL.
-->
