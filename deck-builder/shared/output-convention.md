# §10.4 Output Convention

> Contrato LOCKED — D4 (`$DECKS_DIR` env var). Todas as skills do plugin gravam outputs no mesmo formato.

## Path default

```
$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md
```

- `$DECKS_DIR` é env var configurável. **Default:** `~/Documents/decks/`
- Exemplo: `~/Documents/decks/2026-05/STORYBOARD-beauty-smile-pitch-anjo-1647.md`

## Customizando `$DECKS_DIR`

Setar permanente no shell:

```bash
echo 'export DECKS_DIR=~/Documents/decks/' >> ~/.zshrc
```

Override por contexto (recomendado para clientes específicos):

```bash
cd ~/Clientes/Fotona/
export DECKS_DIR=./decks/
# A partir daqui, /deck salva em ~/Clientes/Fotona/decks/{YYYY-MM}/
```

Se `$DECKS_DIR` não estiver setado, skills usam `~/Documents/decks/` silenciosamente.

## Slug

- Kebab-case do Big Idea (U5) ou nome do cliente
- Máximo **30 caracteres**
- Lowercase, sem acentos, sem `_` (sempre `-`)

Exemplos:
- "Pitch Beauty Smile anjo R$500k" → `beauty-smile-pitch-anjo`
- "Aula Er:YAG dentistas" → `aula-eryag-dentistas`
- "Política viagens ROI 3x" → `politica-viagens-roi-3x`

## Versionamento

- `v1` no primeiro draft
- `v2`, `v3` quando usuário pede revisão na mesma sessão
- Cada versão é um arquivo separado (não sobrescreve v1)

## Anexos

| Tipo | Path |
|------|------|
| Imagens (output `deck-image-prompts`) | `$DECKS_DIR/{YYYY-MM}/img/{slug}/slide-N.png` |
| Review (output `deck-reviewer`) | `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.review.md` |
| Poster (D8 — `deck-scientific` modo poster) | `$DECKS_DIR/{YYYY-MM}/POSTER-{slug}-{HHmm}.md` |
| 6-pager Amazon (D11 — `deck-internal` pitch-to-leadership) | `$DECKS_DIR/{YYYY-MM}/SIXPAGER-{slug}-{HHmm}.md` |
| Dossiê de revisão (v2.0.0 — `deck-review-print`) | `$DECKS_DIR/{YYYY-MM}/DOSSIE-{slug}-{HHmm}.pdf` |
| Manifesto de vínculo (v2.0.0 — `deck-render-canva`) | `$DECKS_DIR/{YYYY-MM}/DECKLINK-{slug}-{HHmm}.md` |
| Briefing reduzido (v2.0.0 — caminho degradado sem Canva) | `$DECKS_DIR/{YYYY-MM}/BRIEFING-{slug}-{HHmm}.md` |

## Convenções de nome

- **STORYBOARD** = arco narrativo (documento de **autoria**, input pra quem revisa e monta)
- **POSTER** = slide-único cientifico (Better Poster Morrison)
- **SIXPAGER** = documento prosa (anexo de pitch interno Amazon-style)
- **DOSSIE** = cópia A4 de revisão, legível e anotável (peça de leitura em preto sobre branco)
- **DECKLINK** = manifesto que liga storyboard ↔ design_id do Canva ↔ dossiê, mais o hash do briefing por página (D26)
- **BRIEFING** = visão reduzida do storyboard para quem monta, ≤900 chars por slide — caminho degradado quando o Canva não está disponível

Linter `lint-storyboard-schema.sh` valida apenas STORYBOARD.md — POSTER tem schema próprio (D8), SIXPAGER não é schemado (texto livre), DOSSIE é binário e DECKLINK/BRIEFING seguem `print-dossie-schema.md` e `briefing-annotation-contract.md`.

> **STORYBOARD é documento de autoria, não de execução.** Ele carrega ~120 linhas por slide, das quais a maior parte é material de outras etapas (prompts de imagem, frameworks, objeções). Quem revisa e monta precisa de uma **view reduzida**, não da fonte inteira — daí BRIEFING e a camada de anotação. O schema v1.1 do STORYBOARD é LOCKED e **não** deve ser amputado para resolver isso.

## Cross-references

- `storyboard-schema.md` — schema do output principal
- `canva-render-contract.md` — regras de edicao programatica no Canva (Bloco B)
- `../templates/poster-skeleton.md` — schema de POSTER (D8)
- `../scripts/lint-storyboard-schema.sh` — valida STORYBOARD
- `../templates/env-decks-dir.example` — exemplo de configuração de `$DECKS_DIR`
