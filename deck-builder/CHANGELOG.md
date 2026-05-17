# Changelog

Todas as mudanças notáveis do plugin `deck-builder` são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/) e versionamento [SemVer](https://semver.org/).

## [1.0.0] - 2026-05-17

### Added

- **11 skills** completas: `deck-orchestrator` (entrypoint) + 8 verticais (`deck-fundraising`, `deck-sales`, `deck-clinical`, `deck-equipment`, `deck-teaching`, `deck-proposal`, `deck-scientific`, `deck-internal`) + 2 auxiliares (`deck-image-prompts`, `deck-reviewer`).
- **8 contratos compartilhados** (§10 SHARED.md) em `shared/`:
  - Entrevista universal U1-U6
  - STORYBOARD.md schema
  - Routing matrix (16 rotas)
  - Output convention (`$DECKS_DIR` + slug + versionamento)
  - Auto-detection brands.yaml
  - NotebookLM query template
  - Skill frontmatter padrão
  - Fronteiras explícitas (o que o plugin NÃO faz)
- **4 templates** em `templates/`:
  - `storyboard-skeleton.md` — esqueleto canônico
  - `poster-skeleton.md` (D8) — schema próprio para `deck-scientific` modo poster
  - `brands.yaml.example` (D6) — 3 marcas pré-povoadas (Beauty Smile / Fotona / Carnaval 360)
  - `env-decks-dir.example` (D4) — configuração de `$DECKS_DIR`
- **3 walkthroughs end-to-end** documentados no README:
  - W1: Pitch Beauty Smile pra investidor anjo (deck-fundraising + Sequoia + Andy Raskin)
  - W2: Aula Fotona Er:YAG (deck-teaching + laser-physics + chunks ≤7min)
  - W3: Pitch CEO política viagens com ROI (deck-internal pitch-to-leadership + BLUF + 6-pager)
- **Pipeline `skill-cenografia` → `deck-internal concept-reveal` (D3)** documentado com exemplo de paths e regra "consome verbatim".
- **Suporte a 3 NotebookLMs** (734 sources curados):
  - NB1 Core Transversal (243 sources)
  - NB2 Verticais Densas (223 sources)
  - NB3 Verticais Comerciais (268 sources)
- **Lint script shell+grep** em `scripts/lint-storyboard-schema.sh` validando:
  - Bloco `## Meta` completo (12 campos)
  - Tipos de slide na whitelist canônica
  - Bloco compliance 3 tiers (🔴 🟡 ✅)
- **Distribuição dupla (D13):**
  - Marketplace `fercosnt/fernando-claude-marketplace` (Claude Code via `/plugin install`)
  - Cowork Desktop nativo (suporte confirmado com legal-analyzer)
- **11 decisões LOCKED** declaradas em `plugin.json` metadata.
- **Tabela de overrides por vertical** (whitelist image-prompts D5 / max_ctas D14 / compliance D7).
- **Frameworks embutidos** por skill (resumo):
  - Sequoia, Andy Raskin, Klaff, TED, Heath Brothers (SUCCESs), Pyramid Minto, Working Backwards Amazon, Calgary-Cambridge, AIDET, GRADE, CONSORT, STROBE, IMRAD, Tufte, Doumont, Better Poster Morrison, Andragogy (Knowles), Bloom, Mayer, Sparkline Duarte, Win Without Pitching (Enns), 5X Rule, Challenger, Gap Selling, SPIN, Great Demo (Cohan), Sinek, Kotter.

### Inviolable Rules (LOCKED)

- D3 — Pipeline `skill-cenografia` → `deck-internal concept-reveal` (sempre via AskUserQuestion, nunca auto-delega)
- D4 — `$DECKS_DIR` env var default `~/Documents/decks/`
- D5 — Whitelist image-prompts por tipo de slide (override scientific: +dados)
- D6 — `brands.yaml` extensível com 3 marcas pré-povoadas
- D7 — Compliance 3 tiers (🔴 🟡 ✅) **sem hard-block** (bloco final sempre preenchido)
- D8 — `poster-skeleton.md` schema próprio para `deck-scientific` modo poster
- D10 — Routing-first 90% (2+ keywords mesma rota → roteia direto sem perguntar U1-U3)
- D11 — NotebookLM **NÃO** é pré-requisito (degrada com warning)
- D12 — **NUNCA** auto-delega `/idea-to-brief` (sempre AskUserQuestion)
- D13 — Distribuição dupla marketplace + Cowork Desktop nativo
- D14 — `max_ctas` override (`teaching:4` / `scientific:3` / demais:`1`)

### Boundaries (Fronteiras explícitas)

- Não gera slides finais (PPTX/Gamma/Figma) — só STORYBOARD.md
- Não busca dados em tempo real
- Não faz design visual (prompts sim, imagens não)
- Não chama APIs pagas sem confirmação
- Não escreve post de redes sociais (delega `/copy`)
- Não projeta espaço/cenografia (delega `skill-cenografia`)
- Não roda `/idea-to-brief` automaticamente

### Build summary

- **Ondas paralelas:** 4 (Onda 1: 2 auxiliares / Onda 2: 8 verticais / Onda 3: orchestrator / Onda 4: este plugin packaging)
- **Total linhas SKILL.md:** 2.594 linhas em 11 skills
- **Eval cases:** 32 casos em 11 evals/*.json
- **References:** 41 arquivos
- **Assets:** 16 arquivos (templates, checklists, exemplos)
- **NotebookLM:** 734 sources em 3 NBs
- **Modelo:** Opus 4.7 (1M context)
- **Duração:** 3 dias

### Compatibility

- Claude Code: `>= 2.0.10`
- Cowork Desktop: instalação nativa via marketplace (testado com legal-analyzer)
- Sistemas: macOS (testado), Linux (esperado funcionar — sem deps platform-specific)
- Dependências externas opcionais: `notebooklm` CLI, `yq`, `jq`

### Known limitations

- `notebooklm` CLI não é distribuído com o plugin — usuário instala separadamente
- Walkthroughs assumem usuário tem acesso aos 3 NBs (IDs fixos podem ser substituídos por NBs próprios via override futuro)
- Lint script é Bash 4+ (testado bash 5.x)

---

## [Unreleased]

### Planned (v1.1.0 candidate)

- Refinamento de 1-2 skills baseado em feedback dos 5 primeiros decks reais (D1)
- v1.1.0 candidato apenas se walkthroughs §12 revelarem problemas sistemáticos
- Possível adição de skill `deck-summary` (resumo 1-slide para emails)

### Potential (v2.0.0)

- Integração nativa com Gamma API (opt-in, hoje só prompts)
- NotebookLM override via brands.yaml (NBs próprios por marca)
- Multi-language support (hoje só PT-BR)
