# skill-prd

Skill de criacao, validacao e melhoria de PRDs (Product Requirements Documents) estruturados para humanos e agentes de IA.

## O que faz

Transforma contexto (ideia solta, brief existente, pesquisa upstream, conversa com stakeholder) em PRD com detalhe tecnico suficiente para Claude Code implementar diretamente, sem ambiguidade.

## Quando usar

- "Quero um PRD para [feature/projeto]"
- "Planejar projeto", "definir escopo", "doc de requisitos"
- Antes de comecar implementacao de qualquer feature media ou complexa
- Validar ou melhorar um PRD existente

## 4 Modos de entrada

| Modo | Quando |
|------|--------|
| **A) Guided** | Sem material upstream — entrevista 3-5 perguntas estruturadas |
| **B) Context Dump** | Usuario cola material extenso — analise de gaps automatica |
| **C) Best Guess** | PRD gerado com suposicoes marcadas `[ASSUMIDO]` para validacao |
| **D) From Brief** | Herda de `BRIEF/BRIEF.md` (skill `idea-to-brief`) — perguntas so sobre gaps |

## 3 Niveis de complexidade

| Nivel | Quando |
|-------|--------|
| **Lean** | Feature unica, 1-2 sprints, escopo claro |
| **Standard** | Feature media, 1-3 meses, multiplas entidades, integracao |
| **Comprehensive** | Produto novo, quarter+, multi-tenant, 5+ entidades |

## Frameworks embutidos (thinking cuidadoso)

- **MITRE Problem Framing** (Suposicoes? Quem sofre? HMW?)
- **Opportunity Solution Tree** (Outcome → Opportunities → Solutions)
- **Epic Hypothesis** + Tiny Acts of Discovery (Std+)
- **MoSCoW** (max 60% Must)
- **INVEST** para user stories
- **Metricas em 3 camadas** (Primaria + Secundarias + Guardrails)
- **Deep Modules** (Ousterhout *A Philosophy of Software Design*)

## Saida (PRD Comprehensive)

11 secoes mapeadas: Problema & Contexto / Objetivos & Metricas / Escopo (in+out separados) / Personas & Casos de Uso / Epic Hypotheses / Requisitos Funcionais / Requisitos Nao-Funcionais / **Testing Decisions (com prior art)** / Consideracoes Tecnicas (com deep modules) / Riscos & Mitigacoes / Questoes em Aberto / Timeline & Fases.

## Hygiene tecnica (anti-rot)

NAO cola paths especificos nem code-dumps que ficam outdated em semanas. Excecao: snippet de prototype que encoda DECISAO (state machine, schema SQL, JSON shape, tipo TS publico) marcado `[do prototype]`. Topologia (mapa de arquivos) e estavel e fica.

## Validacao

Scorecard 5 dimensoes com pesos — Problema 25% / Escopo 15% / Requisitos 25% / Tecnico 20% / Riscos 15%. Threshold de entrega: >= 7.5. 15 anti-patterns verificados antes de entregar.

## Pipeline upstream/downstream

**Recebe de**:
- `idea-to-brief` (BRIEF.md) — Modo D
- `deep-research` (PESQUISA-*.md) — evidencia
- NotebookLM — RAG para gaps

**Entrega para**:
- `skill-creator` — se PRD requer criar nova skill
- `prompt-engineer` — se PRD requer prompt/system prompt
- `claude-md-improver` — auditoria pos-PRD

## Instalacao

### Claude Code (via marketplace)

```bash
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install skill-prd@fernando-claude-marketplace
```

Apos instalar, reinicie o Claude Code. Invoque com `/skill-prd` ou apenas peca um PRD.

### Cowork (Claude Desktop)

Settings → Plugins → Install from GitHub → `fercosnt/fernando-claude-marketplace` → selecionar `skill-prd`.

## Estrutura

```
skill-prd/
├── .claude-plugin/plugin.json
└── skills/skill-prd/
    ├── SKILL.md
    ├── references/
    │   ├── entry-modes.md
    │   ├── secao-problema.md
    │   ├── secao-requisitos.md      # Testing Decisions section
    │   ├── secao-tecnica.md         # Deep Modules + Anti-rot
    │   ├── secao-metricas.md
    │   ├── task-generation.md
    │   └── quality-checklist.md     # 15 anti-patterns + scorecard
    ├── assets/templates/
    │   ├── prd-lean.md
    │   ├── prd-standard.md
    │   └── prd-comprehensive.md
    └── evals/
```

## Changelog

- **v0.3.0** (2026-05-16) — Cross-pollination com `to-issues` de Matt Pocock: task generation passa de horizontal slicing (DB→Backend→Frontend, anti-padrao) para **vertical slicing (tracer bullets)** como default — cada slice toca multiplas camadas e e demonstravel sozinha. Cada slice ganha label `[Direto]` (executavel) ou `[Bloqueante]` (precisa decisao humana — declara decisor). Header do `tasks-*.md` ganha **Parent** (link pro PRD), **Slicing**, **Total slices**. Slices declaram **Demo** (1 frase end-to-end), **Camadas tocadas**, **Bloqueado por** formal. Horizontal slicing so com justificativa explicita declarada. Exemplo CRUD de Pagamentos reescrito mostrando 4 slices verticais demonstraveis vs 6 tarefas horizontais.
- **v0.2.0** (2026-05-16) — Cross-pollination com `to-prd` de Matt Pocock: Deep Modules (Ousterhout), Testing Decisions com prior art (secao 7b obrigatoria Std+), regra anti-rot (NAO colar paths/code-dumps), busca de ADRs + domain glossary no Passo 0, 5 novos anti-patterns no quality-checklist.
- **v0.1.0** (2026-04-21) — Migracao Opus 4.7: `effort: xhigh`, vocabulario atualizado (Extended Thinking → Adaptive Thinking).
