# Changelog

Todas as mudanças notáveis do plugin `deck-builder` são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/) e versionamento [SemVer](https://semver.org/).

## [1.1.0] - 2026-05-17

### Added

- **`modo_entrega` em `## Meta`** — derivado de U4. Valores: `apresentado-ao-vivo` (U4=1/2), `enviado-para-leitura` (U4=3), `hibrido` (U4=4). Adapta densidade dos slides (minimalista para apresentado vs denso para enviado).
- **Bloco `Conteúdo do slide (visível na projeção)`** em cada slide — separa o que aparece no slide do que o apresentador fala (speaker notes). Densidade calibrada ao `modo_entrega`. Resolve issue: slides minimalistas demais quando deck é enviado para leitura.
- **Bloco `Layout sugerido`** em cada slide — handoff explícito para designer / Gamma / Claude Design / PowerPoint com grid + tipografia + componentes visuais + animação. Resolve issue: instruções vagas para construção visual.
- **Formato `Imagens sugeridas` reformatado** — Quantidade declarada explicitamente (1 imagem hero com 3 variações vs N imagens distintas) + cada variação em bloco markdown separado com 6 campos labeled (Aspect ratio / Estilo / Composição / Prompt / Negative / Mood ref). Resolve issue: prompts confusos com config misturada com prompt.
- **`[VERIFICAR]` flag** — disciplina anti-fabricação. Toda data específica inferida (R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa) sem fonte conferida pela skill marca `[VERIFICAR: descrição]`. Documentado em novo `shared/verificar-flag.md`. Lint v1.1 emite WARN quando ausente. Reviewer converte flags em 🟡 ou 🔴.
- **Bold opcional nos rótulos** (`**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**`, etc.) — facilita scan visual ao revisar STORYBOARD. Lint aceita ambos formatos (texto puro e bold).
- **Adendo v1.1 em todas as 8 verticais** — cada SKILL.md das skills verticais documenta as 4 disciplinas novas (modo_entrega / Conteúdo do slide / Layout sugerido / [VERIFICAR]).

### Changed

- **Lint script `lint-storyboard-schema.sh`** atualizado:
  - Regex aceita campos com bold opcional (`\*?\*?Field:\*?\*?`)
  - Adicionado check obrigatório: `Modo de entrega:` em Meta (13 campos no total agora)
  - Adicionado check (WARN): bloco `Conteúdo do slide` em cada slide
  - Adicionado check (WARN): bloco `Layout sugerido` em cada slide
  - Adicionado check (WARN): dados R$/%/n=/RCT/NPS/GRADE sem `[VERIFICAR]` flag
  - Header de usage atualizado para refletir validações v1.1
- **Schema `storyboard-schema.md`** reformulado com 3 regras adicionais (7, 8, 9):
  - Regra 7: Conteúdo do slide adaptado ao `modo_entrega`
  - Regra 8: Layout sugerido obrigatório em cada slide
  - Regra 9: `[VERIFICAR]` em dados fabricados
- **`deck-image-prompts/SKILL.md`** seção "Formato de output" reformulada com novo bloco `Imagens sugeridas:` (Quantidade + 3 variações em blocos separados). Formato v1.0 deprecated mas ainda aceito pelo lint para retrocompatibilidade.
- **`entrevista-universal-u1-u6.md`** documenta como `modo_entrega` deriva de U4 + impacto explícito no STORYBOARD (densidade vs speaker notes).

### Migration v1.0 → v1.1

STORYBOARDs gerados em v1.0 ainda passam o lint v1.1 EXCETO no novo campo obrigatório `Modo de entrega:` em Meta. Para migrar manualmente:

1. Adicionar `- Modo de entrega: <apresentado-ao-vivo|enviado-para-leitura|hibrido>` em `## Meta` (derive de U4 / Formato).
2. Para cada slide, adicionar bloco `Conteúdo do slide` extraindo bullets implícitos da Mensagem-chave + Speaker notes.
3. Para cada slide, adicionar bloco `Layout sugerido` (grid + tipografia + componentes + animação).
4. Reformatar bloco `Prompt de imagem` em `Imagens sugeridas` com Quantidade explícita + variações em blocos.
5. Marcar dados fabricados com `[VERIFICAR: descrição]`.
6. (Opcional) Bold nos rótulos: `Tipo:` → `**Tipo:**`.

### Why v1.1

Após o build v1.0 ser validado por simulação com lint PASS em 3 walkthroughs, o usuário forneceu feedback substantivo (UAT humano real) apontando 4 issues estruturais:

1. Speaker notes dominam o conteúdo, slide visual fica vazio
2. Falta pergunta "deck será apresentado ou enviado?" — densidade adaptativa ausente
3. Instruções para handoff visual (Claude Design / Gamma / PowerPoint) fracas
4. Prompts de imagem confusos (quantidade, config vs prompt, qualidade)

Adicionalmente, durante o feedback foi identificado que skills inventam números plausíveis (NPS 91 n=131, "40% fecharam", papers RCT fabricados) sem flag — risco de over-claiming em apresentação real. v1.1 introduz `[VERIFICAR]` para resolver.

Esse é exatamente o "ponto de falsificação do trade-off D1" previsto no PRD §9 risco #1 — input humano real captou o que a simulação determinística não pegou.

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
