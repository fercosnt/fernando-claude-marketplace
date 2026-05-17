# Orchestrator Eval Cases — Smoke Test Script

> Roda os 6 cases manualmente apos instalacao em `~/.claude/skills/deck-orchestrator/`. Cada case eh 1 prompt + assercoes binarias.
>
> **Como executar:** abre `/deck` no Claude Code, cola o input, valida comportamento contra assercoes. Se ANY case falha → revisar SKILL.md antes de declarar DoD.
>
> Detalhes completos em [../references/eval-cases-orchestrator.md](../references/eval-cases-orchestrator.md).

---

## Case 1 — Routing direto

**Input:** `/deck preciso pitchar Beauty Smile pra anjo do Iguatemi, R$500k`

**PASS criteria:**
- [ ] NAO chamou AskUserQuestion
- [ ] Delegou `deck-fundraising`
- [ ] Marca = Beauty Smile (via input_regex)
- [ ] Design system carregado: beauty-smile-design-system
- [ ] Compliance tags: odontologia-br, cfo-cfm

---

## Case 2 — Ambiguidade rotas

**Input:** `/deck vou dar aula de Er:YAG pra dentistas em curso`

**PASS criteria:**
- [ ] Chamou AskUserQuestion T1 (deck-teaching vs deck-clinical)
- [ ] 2 opcoes na pergunta
- [ ] Marca = Fotona (via input_regex)
- [ ] Compliance tag: anvisa-laser-classe-iii
- [ ] Apos resposta usuario, delegou a rota escolhida

---

## Case 3 — Delegacao externa

**Input:** `/deck tem como voce criar um carrossel sobre tratamento?`

**PASS criteria:**
- [ ] Detectou "carrossel" → delegacao externa
- [ ] Mensagem clara "isso NAO e deck — delegando para /copy"
- [ ] NAO chamou deck-clinical mesmo com "tratamento" presente

---

## Case 4 — Input vago + idea-to-brief

**Input:** `/deck preciso de slides`

**PASS criteria:**
- [ ] Chamou AskUserQuestion T2 (U1-U3) antes de qualquer routing
- [ ] Apos U1 vago, chamou AskUserQuestion T3 (sugerir /idea-to-brief)
- [ ] **NAO chamou /idea-to-brief automaticamente** (D12)
- [ ] So delegaria /idea-to-brief se usuario explicitamente escolhesse opcao 1

---

## Case 5 — Concept-reveal pipeline D3

**Input:** `/deck queria apresentar o conceito da sala VIP do Carnaval 360 pro board`

**PASS criteria:**
- [ ] Rota = deck-internal modo concept-reveal
- [ ] Chamou AskUserQuestion T4 (pipeline cenografia)
- [ ] Mensagem mencionou skill-cenografia como pre-requisito
- [ ] Marca = Carnaval 360
- [ ] Se opcao "gerar primeiro" → PAUSA sem delegar

---

## Case 6 — 3 rotas ambiguas (smoke test extra)

**Input:** `/deck preciso de um pitch tecnico-comercial pra investidor em congresso clinico semana que vem`

**PASS criteria:**
- [ ] Chamou AskUserQuestion T1.b com 3 opcoes (fundraising / sales / scientific)
- [ ] NAO chutou fundraising so por ter score=2
- [ ] Apos resposta usuario, delegou rota escolhida

---

## Verificacao final

```bash
# Verificar instalacao Claude Code
ls -la ~/.claude/skills/deck-orchestrator/

# Verificar instalacao Cowork Desktop
ls -la "/Users/fernando/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/ca8a3e06-7863-4eb2-b67f-f418eb43333f/4c7c76ce-5f86-42b7-a377-09a1e5759119/skills/deck-orchestrator/"

# Verificar SKILL.md frontmatter valido
head -15 ~/.claude/skills/deck-orchestrator/SKILL.md

# Listar dependencias (10 skills deck-*)
ls -d ~/.claude/skills/deck-* | grep -v orchestrator | wc -l   # esperado: 10
```

**DoD final:**
- [ ] 6/6 cases passam comportamento esperado
- [ ] Skill instalada em ~/.claude/skills/ e Cowork Desktop skills-plugin
- [ ] Dependencias (10 skills) presentes
- [ ] Memoria do projeto atualizada
- [ ] ROADMAP.md marca Onda 3 completa, libera Onda 4 (packaging plugin)
