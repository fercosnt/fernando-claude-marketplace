# deck-builder

Plugin para Claude Code + Cowork Desktop. Cria `STORYBOARD.md` (markdown agnóstico ao engine visual) para **8 verticais** de apresentação + **2 auxiliares** + **1 orquestrador**.

> Não gera slides finais (PPTX/Gamma/Figma) — gera o arco narrativo. Designer/IA visual gera os slides a partir do storyboard.

---

## Quick Start (5 passos)

```bash
# 1) Instalar via marketplace
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install deck-builder@fernando-claude-marketplace

# 2) Setar $DECKS_DIR (opcional — default ~/Documents/decks/)
echo 'export DECKS_DIR=~/Documents/decks/' >> ~/.zshrc
source ~/.zshrc

# 3) Inicializar brands.yaml (auto-detection de marca)
mkdir -p ~/.config/deck-builder
cp ~/.claude/plugins/deck-builder/templates/brands.yaml.example \
   ~/.config/deck-builder/brands.yaml

# 4) (opcional) Customizar brands.yaml com marcas próprias
$EDITOR ~/.config/deck-builder/brands.yaml

# 5) Verificar instalação
/deck "preciso de slides pra demo"
```

> **Cowork Desktop:** o mesmo `/plugin install deck-builder@fernando-claude-marketplace` funciona nativamente (D13 — confirmado com legal-analyzer publicado anteriormente).

---

## As 11 skills

| Skill | Onda | Função |
|-------|------|--------|
| `deck-orchestrator` | 3 | **ENTRYPOINT.** Recebe `/deck <texto>`, classifica por keywords e roteia para a vertical correta. NUNCA auto-delega — sempre confirma rotas externas via AskUserQuestion. |
| `deck-fundraising` | 2 | Pitch pra investidor (anjo/Series A) ou sponsorship Rouanet ou demo-day. Sequoia + Andy Raskin Promised Land + Klaff opcional. |
| `deck-sales` | 2 | Venda B2B com Challenger + Gap Selling + ROI/payback Sensitivity 3 cenários. Comparativo SEM badmouth (Lei 9.279 + CONAR + CDC). |
| `deck-clinical` | 2 | Apresentação clínica peer-facing (EBM/GRADE) ou patient-facing (AIDET). Compliance CFO 196/2019 + CFM 1974/2011 + Anvisa em 3 tiers. |
| `deck-equipment` | 2 | Vender equipamento médico/dental. FAB + TCO 5 anos + Payback + Sensitivity. Auto-detect Fotona/LightWalker injeta compliance Anvisa Classe II/III. |
| `deck-teaching` | 2 | Aula técnica (chunks ≤7min) / workshop hands-on / keynote inspiracional Sparkline Duarte. Andragogy + Bloom + Mayer + max_ctas 4. |
| `deck-proposal` | 2 | Proposta comercial B2B BR (3 modos: commercial / strategic-partnership M&A / retainer). Pyramid Minto BLUF + SCQA + termos jurídicos BR. |
| `deck-scientific` | 2 | Poster / oral-short 7min / oral-long 12-20min / keynote 45min. IMRAD + GRADE + Tufte + Doumont + Better Poster Morrison. COI inviolável. |
| `deck-internal` | 2 | 4 modos (pitch-to-leadership BLUF Amazon 6-pager / strategy SCR / **concept-reveal pipeline com skill-cenografia** / all-hands Sinek+Kotter). |
| `deck-image-prompts` | 1 | Gera prompts de imagem (MJ v7 / Imagen 4 / Nano Banana Pro / Higgsfield / DALL-E / Ideogram) para slides na whitelist D5. |
| `deck-reviewer` | 1 | 3 críticos adversariais (clareza / persuasão via /copy / SUCCESs Heath). Severidades 🔴🟡🟢 sem score numérico. |

---

## 3 Walkthroughs end-to-end

### Walkthrough 1 — Pitch Beauty Smile pra investidor anjo

**Contexto:** Anjo do Iguatemi, ticket alvo R$500k em troca de 8% equity. Reunião em 5 dias.

```
$ /deck Beauty Smile pitch pra investidor anjo, R$500k, reuniao sexta
```

**Fluxo:**

1. `deck-orchestrator` detecta **3 keywords fundraising** ("investidor", "anjo", "R$500k") → roteia DIRETO `deck-fundraising` **SEM** perguntar U1-U3 (routing-first D10).
2. Auto-detection Beauty Smile (regex match) → carrega skill `beauty-smile-design-system` se instalada.
3. Entrevista universal U1-U6 abreviada (já tem objetivo, audiência, marca; pergunta duração + formato + Big Idea).
4. Entrevista vertical F1-F5 (estágio empresa, MRR, traction, valuation, uso dos fundos).
5. `deck-fundraising` consulta NB1 + NB3 + gera 13 slides Sequoia + Andy Raskin:
   - Capa, Old World, New World (Promised Land), Problem, Solution, Why Now, Market Size, Product, Traction, Business Model, Team, Ask R$500k tripartido, Vision.
6. Invoca `deck-image-prompts` para slides whitelist (capa, problema, conceitual, equipe).
7. **Output:** `$DECKS_DIR/2026-05/STORYBOARD-beauty-smile-pitch-anjo-1647.md` v1.
8. `/deck review` → `deck-reviewer` aponta 2 issues 🔴 + 1 🟡 com sugestão.
9. v2 → designer / Gamma.

**Tempo total:** ~25min skill + 2-3h ajuste humano + 1 dia designer.

---

### Walkthrough 2 — Aula Fotona Er:YAG pra dentistas em curso

**Contexto:** Curso pós-graduação, módulo "Aplicações Er:YAG", 4h, 18 dentistas (mix iniciantes/experientes).

```
$ /deck preciso preparar aula de 4h sobre Er:YAG pra dentistas no curso Beauty Smile
```

**Fluxo:**

1. `deck-orchestrator` detecta keywords **teaching** + **clinical/equipment** + **Beauty Smile** → roteia `deck-teaching` modo `aula-tecnica` + auto-detection Fotona (carrega `laser-physics` skill se instalada).
2. Entrevista universal + vertical T1-T5 (objetivos pedagógicos Bloom, pré-requisitos, hands-on disponível, equipamento de prática, avaliação).
3. `deck-teaching` consulta NB1 + invoca `laser-physics` + NB2 → estrutura segmentada (chunks ≤7min):
   - **Módulo 1 (60min):** Física do laser Er:YAG (4 chunks de 12-15 slides)
   - **Hands-on 1 (30min):** Cálculo de fluence (worksheet)
   - **Módulo 2 (60min):** Aplicações clínicas (endodontia, cirurgia, periodontia)
   - **Hands-on 2 (45min):** Protocolo simulado em modelo
   - **Módulo 3 (30min):** Casos clínicos discutidos
   - **Avaliação (15min):** Quiz Bloom-aplicar
4. STORYBOARD ~35 slides + 2 worksheets + quiz.
5. `deck-image-prompts` para slides técnicos (diagramas, esquemas dosimétricos).
6. `deck-reviewer`: chunks ≤7min ✓, hands-on ≥2 ✓, max_ctas=4 OK (override teaching D14).
7. **Output:** `$DECKS_DIR/2026-05/STORYBOARD-aula-eryag-pos-grad-XX.md`.

**Tempo total:** ~40min skill + 2-3 dias preparando casos clínicos.

---

### Walkthrough 3 — Pitch interno pra CEO sobre política viagens com ROI

**Contexto:** Convencer CEO Beauty Smile a aprovar política de viagens com gating de ROI ≥3x. Reunião 1:1 de 30min.

```
$ /deck preciso pitchar pro CEO nova politica viagens com gating de ROI
```

**Fluxo:**

1. `deck-orchestrator` detecta keywords **"pitchar" + "CEO" + "política"** → roteia `deck-internal` modo `pitch-to-leadership`.
2. Auto-detection Beauty Smile.
3. Entrevista universal + vertical I1-I5 (decisor primário, friction esperada, ask específico, métricas que ele acompanha, prazo de aprovação).
4. `deck-internal` consulta NB1 + NB3 (Pyramid Minto BLUF + Working Backwards Amazon) → 9 slides:
   - Capa relacional (BR Hofstede high-context)
   - **Slide 2 BLUF** ("Aprovar política viagens com gating ROI ≥3x — R$80k orçado, payback 4 meses")
   - Problema (viagens hoje 60% sem ROI mensurável)
   - Política proposta (4 critérios objetivos)
   - Business case 4 viagens reais (Q1-Q2)
   - ROI projetado (Sensitivity 3 cenários)
   - Fricção mitigada (3 objeções antecipadas)
   - Ask R$80k + cronograma
   - Próximos passos com responsável
5. Anexo: 6-pager Amazon style (`$DECKS_DIR/2026-05/SIXPAGER-politica-viagens-ceo-1430.md`).
6. `deck-image-prompts` minimalista (CEO valoriza foco).
7. `deck-reviewer`: BLUF slide 2 ✓, ask específico ✓, objeção antecipada ✓.
8. **Output:** `$DECKS_DIR/2026-05/STORYBOARD-politica-viagens-ceo-XX.md` + 6-pager.

**Tempo total:** ~20min skill + 2h business case + 30min reunião.

---

## Pipeline `skill-cenografia` → `deck-internal concept-reveal` (D3)

Quando o pitch é apresentar um **conceito de espaço** (sala VIP, booth de evento, ativação de marca):

```
1. Usuário: "/deck preciso apresentar conceito Sala VIP Fotona pro CEO"

2. deck-orchestrator detecta "conceito" + "sala" + "apresentar"
   → roteia deck-internal modo concept-reveal

3. deck-internal SUGERE via AskUserQuestion:
   "Pra esse concept-reveal precisamos de artefatos visuais.
    Você já rodou /skill-cenografia para gerar renders/JSON/mood?
      (a) Sim — me passa o path
      (b) Não — quero rodar agora antes
      (c) Vou descrever em texto"

4. Se (b): usuário roda /skill-cenografia separadamente,
   gera artefatos em ~/Documents/cenografia/sala-vip-fotona/:
     - mood-board.png
     - render-frontal.png
     - render-perspectiva.png
     - layout-planta.png
     - prompts-nano-banana-pro.json

5. Usuário retorna ao /deck e passa o path:
   "Pronto, rodei. Artefatos em ~/Documents/cenografia/sala-vip-fotona/"

6. deck-internal CONSOME paths absolutos como `Prompt de imagem` verbatim
   (NÃO regenera prompts — usa os do cenografia diretamente)

7. Output: STORYBOARD-sala-vip-fotona-XX.md focado em
   "vender o conceito visualmente pro board"
```

**Inviolável (D3):** `deck-internal concept-reveal` **nunca** invoca `skill-cenografia` automaticamente. Sempre via AskUserQuestion.

---

## Tabela de overrides por vertical

| Vertical | Whitelist image-prompts (D5) | max_ctas (D14) | Compliance (D7) |
|----------|------------------------------|----------------|-----------------|
| `fundraising` | default | **1** | Forward-looking statements (Disclaimer slide opcional) |
| `sales` | default | **1** | Comparativo SEM badmouth (Lei 9.279 art 195 + CONAR 32 + CDC 37) |
| `clinical` | default | **1** | CFO 196/2019 + CFM 1974/2011 + Anvisa em 3 tiers |
| `equipment` | default | **1** | Anvisa Classe II/III; Fotona injeta laser-classe-iii |
| `teaching` | default | **4** *(override)* | — |
| `proposal` | default | **1** | Termos jurídicos BR (IPCA + foro SP + multa rescisão STJ) + CADE se M&A R$750M+ |
| `scientific` | **+dados** *(override)* | **3** *(override)* | CONSORT / STROBE / PRISMA / CARE + COI inviolável + GRADE |
| `internal` | default | **1** | — |

> **Whitelist default:** `capa | problema | conceitual | comparativo | demo | prova-social` recebem prompt; `dados | financeiro | CTA | disclaimer | agradecimento | apêndice` não recebem.
> **Override scientific:** inclui `dados` (gráficos científicos são imagens com mensagem visual).
> **Override usuário:** flags `--include-dados` ou `--exclude-prova-social` em qualquer skill.

---

## Configuração avançada

### Adicionar marca própria

Editar `~/.config/deck-builder/brands.yaml`:

```yaml
brands:
  - name: "Cliente XYZ"
    regex: '\bXYZ\b|xyz-corp|clientexyz\.com'
    design_system_skill: null
    compliance_tags: ["b2b-saas", "lgpd"]
```

Tags livres — cada skill decide se reconhece a tag. Tags desconhecidas são ignoradas (não bloqueiam).

### Override `$DECKS_DIR` por contexto (cliente específico)

```bash
cd ~/Clientes/Fotona/
export DECKS_DIR=./decks/
# /deck a partir daqui salva em ~/Clientes/Fotona/decks/{YYYY-MM}/
```

### NotebookLM (opcional mas recomendado)

3 NBs do plugin (734 sources total):

- **NB1 Core Transversal:** `7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da` (243 sources) — frameworks gerais
- **NB2 Verticais Densas:** `1635d16b-773c-480d-89c2-79c717f4b2e1` (223 sources) — clínico, científico, ensino, equipamentos
- **NB3 Verticais Comerciais:** `5a0aaabb-78c1-4d03-a400-e9ce1973737b` (268 sources) — vendas, fundraising, proposal, pitch interno

Skills degradam graciosamente se NB estiver offline (warning + segue com conhecimento base).

---

## Troubleshooting

| Sintoma | Causa provável | Fix |
|---------|----------------|-----|
| `NotebookLM offline` warning | NBs não setados ou notebooklm CLI ausente | Verificar `notebooklm use <NB_ID>` funciona; senão skills seguem sem NB |
| `brands.yaml malformado` | YAML inválido em `~/.config/deck-builder/brands.yaml` | Validar com `yq . ~/.config/deck-builder/brands.yaml` |
| `deck-orchestrator` não roteia | Skills não foram instaladas pelo marketplace | `ls ~/.claude/plugins/deck-builder/skills/` → deve listar 11 |
| Cowork Desktop não instalou | Plugin não apareceu na lista | Reabrir Cowork Desktop; se persistir, ver issue [#NN] |
| `STORYBOARD.md` sem bloco compliance | Skill antiga, lint falhou | Rodar `scripts/lint-storyboard-schema.sh STORYBOARD.md` para diagnóstico |
| Slug com >30 chars | Big Idea muito longa | Skill encurta automaticamente; ou passar `--slug=meu-slug` |

---

## Lint script

```bash
# Validar um STORYBOARD.md
~/.claude/plugins/deck-builder/scripts/lint-storyboard-schema.sh \
  ~/Documents/decks/2026-05/STORYBOARD-meu-deck-1647.md

# Saída:
# [PASS] Meta block completo
# [PASS] Tipos canonicos presentes
# [PASS] Bloco compliance 3 tiers presente
# OK
```

Validações:
- Bloco `## Meta` com 12 campos obrigatórios
- Tipos de slide em whitelist canônica
- Bloco compliance com 3 tiers (🔴 🟡 ✅)

---

## Estrutura do plugin

```
deck-builder/
├── .claude-plugin/
│   └── plugin.json
├── README.md                            # este arquivo
├── CHANGELOG.md
├── LICENSE
├── skills/                              # 11 skills
│   ├── deck-orchestrator/                # entrypoint
│   ├── deck-fundraising/
│   ├── deck-sales/
│   ├── deck-clinical/
│   ├── deck-equipment/
│   ├── deck-teaching/
│   ├── deck-proposal/
│   ├── deck-scientific/
│   ├── deck-internal/
│   ├── deck-image-prompts/
│   └── deck-reviewer/
├── shared/                              # 8 contratos §10
│   ├── entrevista-universal-u1-u6.md
│   ├── storyboard-schema.md
│   ├── routing-matrix.md
│   ├── output-convention.md
│   ├── auto-detection-brands.md
│   ├── nb-query-template.md
│   ├── skill-frontmatter.md
│   └── fronteiras-explicitas.md
├── templates/                           # 4 templates
│   ├── storyboard-skeleton.md
│   ├── poster-skeleton.md               # D8 (deck-scientific poster)
│   ├── brands.yaml.example              # 3 marcas pré-povoadas (D6)
│   └── env-decks-dir.example
└── scripts/
    └── lint-storyboard-schema.sh        # shell+grep (QA-3)
```

---

## Fronteiras (o que o plugin NÃO faz)

- ❌ Não gera slides finais (PPTX/Gamma/Figma) — só STORYBOARD.md
- ❌ Não busca dados em tempo real — usuário fornece números
- ❌ Não faz design visual — `deck-image-prompts` faz prompts; designer/IA gera
- ❌ Não chama APIs pagas sem confirmação
- ❌ Não escreve post de redes sociais — delega `/copy`
- ❌ Não projeta espaço/cenografia — delega `skill-cenografia` (D3)
- ❌ Não roda `/idea-to-brief` automaticamente — sugere via AskUserQuestion (D12)

---

## Decisões LOCKED (D1-D14)

11 decisões invioláveis carregadas no `plugin.json` metadata. Resumo:

- **D3** Pipeline cenografia → concept-reveal documentado
- **D4** `$DECKS_DIR` env var (default `~/Documents/decks/`)
- **D5** Whitelist image-prompts por tipo de slide
- **D6** `brands.yaml` extensível, 3 marcas pré-povoadas
- **D7** Compliance 3 tiers (🔴 bloqueante / 🟡 verificar / ✅ OK), sem hard-block
- **D8** `poster-skeleton.md` schema próprio (deck-scientific poster)
- **D10** Routing-first 90% (2+ keywords mesma rota → roteia direto)
- **D11** NotebookLM **NÃO é pré-requisito** (degrada gracioso)
- **D12** **NUNCA** auto-delega `/idea-to-brief` (sempre AskUserQuestion)
- **D13** Distribuição dupla (marketplace + Cowork Desktop nativo)
- **D14** max_ctas override (teaching:4, scientific:3, demais:1)

---

## Contribuição

Issues e PRs em [fercosnt/fernando-claude-marketplace](https://github.com/fercosnt/fernando-claude-marketplace).

Diretrizes:
- 1 skill por PR (não bundle múltiplas mudanças)
- Eval cases atualizados se mudou comportamento
- Lint shell PASS antes de pedir review
- Não adicionar dependência de API paga sem flag opt-in

---

## Licença

MIT — ver [LICENSE](LICENSE).

---

## Reconhecimentos

- **Frameworks:** Sequoia, Andy Raskin, Klaff, Chris Anderson (TED), Nancy Duarte, Heath Brothers (SUCCESs), Pyramid Minto, Working Backwards Amazon, Calgary-Cambridge, AIDET, GRADE, CONSORT, STROBE, IMRAD, Tufte, Doumont, Better Poster Morrison, Andragogy Malcolm Knowles, Bloom, Mayer, Sparkline Duarte, Win Without Pitching (Enns), 5X Rule, Forrester TEI, Nucleus Research, Challenger, Gap Selling, SPIN, Great Demo (Cohan), Sinek, Kotter.
- **Pesquisa-base:** 734 sources curados em 3 NotebookLMs.
- **Build:** 3 dias / 11 skills / Opus 4.7 1M context / Claude Code + Cowork Desktop.
