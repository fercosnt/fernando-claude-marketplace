# §10.3 Routing Matrix do `deck-orchestrator`

> Contrato LOCKED — D10 (routing-first) + D12 (NUNCA auto-delega `/idea-to-brief`).
> Entry-point: `/deck <texto livre>`.

## Matriz keyword → rota

| Sinal detectado | Rota |
|-----------------|------|
| "investidor", "VC", "anjo", "captação", "Series A/B", "Rouanet", "patrocínio" | `deck-fundraising` |
| "vendas", "B2B", "demo", "proposta de software", "lead", "funil" | `deck-sales` |
| "protocolo", "tratamento", "paciente", "indicação clínica", "evidência clínica" | `deck-clinical` |
| "equipamento", "device", "laser", "Fotona", "LightWalker", "ROI clínica" | `deck-equipment` |
| "aula", "curso", "treinamento", "workshop", "ensinar", "TED", "keynote inspiracional" | `deck-teaching` |
| "proposta", "orçamento", "escopo", "retainer", "consultoria", "M&A", "parceria estratégica" | `deck-proposal` |
| "congresso", "paper", "poster", "abstract", "AAOMS", "ICOI", "CIOSP" | `deck-scientific` |
| "all-hands", "pitch interno", "CEO", "board interno", "estratégia mkt" | `deck-internal` |
| "concept reveal", "ativação", "conceito sala/booth/camarote", "apresentar conceito" | `deck-internal` modo `concept-reveal` → **encadeia `skill-cenografia`** (D3) |
| "render", "layout 3D", "stand", "booth", "camarote", "set design", "mood board espaço" | delega `skill-cenografia` (NÃO é deck) |
| "carrossel", "Instagram", "reel", "TikTok", "post" | delega `/copy` |
| "cultura", "onboarding", "valores Beauty Smile" | delega agente `culture-lab` |
| Input vago: 0 keywords + após U1 ainda sem contexto | orchestrator **SUGERE** `/idea-to-brief` via AskUserQuestion (D12 — nunca auto-delega) |

## Algoritmo (D10 — routing-first 90%)

```
1. Conta keywords contra a matriz acima.
2. Se 2+ keywords da MESMA rota → roteia direto, SEM perguntar U1-U3.
3. Se 0-1 keyword → pergunta U1-U3 (subset da entrevista universal),
   depois re-classifica.
4. Se 2+ keywords de 2+ rotas distintas → AskUserQuestion: "É mais [A] ou [B]?"
5. Se após U1 ainda vago → SUGERE /idea-to-brief (D12).
   NUNCA delega automaticamente — usuário decide.
```

## Inviolável (D12)

- `deck-orchestrator` **NUNCA** invoca `/idea-to-brief` sem confirmação explícita.
- Se input vago, a saída é SEMPRE `AskUserQuestion` com 3 opções:
  - "(a) Tentar refinar aqui" → segue para U1-U3
  - "(b) Rodar /idea-to-brief primeiro" → orchestrator encerra com instrução
  - "(c) Cancelar" → orchestrator encerra

## Rotas externas (não-deck)

3 rotas que **NÃO** geram STORYBOARD.md — delegam pra fora do plugin:

| Trigger | Skill externa | Output esperado |
|---------|---------------|-----------------|
| `concept-reveal` | `skill-cenografia` (pré) → `deck-internal concept-reveal` (pós) | Pipeline D3 |
| Layout 3D / render | `skill-cenografia` (standalone) | JSON Nano Banana Pro + prompts |
| Redes sociais | `/copy` | Carrossel/reel/legenda |
| Cultura/onboarding | agente `culture-lab` | Material institucional |

## Empate via AskUserQuestion

Quando duas rotas têm a mesma contagem de keywords (ex: "demo de equipamento Fotona"):

```
AskUserQuestion:
  question: "É mais um pitch de vendas (deck-sales) ou ROI de equipamento (deck-equipment)?"
  options:
    - label: "deck-sales"
      description: "Foco em fechar contrato — Challenger + ROI + comparativo"
    - label: "deck-equipment"
      description: "Foco em TCO/Payback do device — FAB + Sensitivity 3 cenários"
```

## Cross-references

- `entrevista-universal-u1-u6.md` — U1-U3 são o subset que orchestrator pode usar
- `auto-detection-brands.md` — roda **antes** do routing
- `fronteiras-explicitas.md` — o que o plugin NÃO faz (não invade outras skills)
