# Routing Matrix — `deck-orchestrator`

> **Fonte canonica:** SHARED.md §10.3 do plugin `deck-builder`.
> Este arquivo espelha a matriz para autonomia do orchestrator. Em caso de divergencia, SHARED.md vence.

---

## Matriz de Routing (D10)

| # | Sinal detectado (keywords/regex) | Rota | Tipo |
|--:|---------------------------------|------|------|
| 1 | "investidor", "VC", "anjo", "captacao", "Series A/B", "Rouanet", "patrocinio", "term sheet", "valuation", "cap table" | `deck-fundraising` | vertical |
| 2 | "vendas", "B2B", "demo", "proposta de software", "lead", "funil", "SDR", "discovery call", "demo do produto" | `deck-sales` | vertical |
| 3 | "protocolo", "tratamento", "paciente", "indicacao clinica", "evidencia clinica", "GRADE", "diagnostico", "consentimento" | `deck-clinical` | vertical |
| 4 | "equipamento", "device", "laser", "Fotona", "LightWalker", "ROI clinica", "amortizacao equipamento", "compra de aparelho" | `deck-equipment` | vertical |
| 5 | "aula", "curso", "treinamento", "workshop", "ensinar", "TED", "keynote inspiracional", "modulo didatico", "pos-graduacao" | `deck-teaching` | vertical |
| 6 | "proposta", "orcamento", "escopo", "retainer", "consultoria", "M&A", "JV", "parceria estrategica", "carta-proposta" | `deck-proposal` | vertical |
| 7 | "congresso", "paper", "poster", "abstract", "AAOMS", "ICOI", "CIOSP", "IADR", "publicacao", "submission" | `deck-scientific` | vertical |
| 8 | "all-hands", "pitch interno", "CEO", "board interno", "estrategia mkt", "town hall", "kickoff", "reorg" | `deck-internal` | vertical |
| 9 | "concept reveal", "ativacao", "conceito sala", "conceito booth", "conceito camarote", "apresentar conceito" | `deck-internal` modo `concept-reveal` (D3) | vertical+pipeline |
| 10 | "render", "layout 3D", "stand", "booth", "camarote", "set design", "mood board espaco", "planta 3D" | `skill-cenografia` (NAO e deck) | delegacao-externa |
| 11 | "carrossel", "Instagram", "reel", "TikTok", "post", "stories", "feed" | `/copy` | delegacao-externa |
| 12 | "cultura", "onboarding", "valores Beauty Smile", "ritual de equipe", "valores da empresa" | agente `culture-lab` | delegacao-externa |
| ∅ | Input vago: 0 keywords + apos U1 ainda sem contexto | **SUGERE** `/idea-to-brief` via AskUserQuestion (D12) | meta |

---

## Algoritmo (passo-a-passo)

### Passo 1: Pre-processamento

- Normaliza input (lowercase, strip diacriticos para match de keywords latinas/brand names case-sensitive separadamente)
- Carrega `~/.config/deck-builder/brands.yaml` (3 marcas pre-povoadas)
- Roda auto-detection §10.5 (5 niveis precedencia) — **antes** do count de keywords

### Passo 2: Contagem de keywords

Para cada rota da matriz acima, conta quantas keywords da rota aparecem no input:

```
rota_score = {
  fundraising: count(input, kw_fundraising),
  sales: count(input, kw_sales),
  clinical: count(input, kw_clinical),
  equipment: count(input, kw_equipment),
  teaching: count(input, kw_teaching),
  proposal: count(input, kw_proposal),
  scientific: count(input, kw_scientific),
  internal: count(input, kw_internal),
  concept_reveal: count(input, kw_concept_reveal),
  cenografia: count(input, kw_cenografia),
  copy: count(input, kw_copy),
  culture_lab: count(input, kw_culture_lab)
}
```

### Passo 3: Decisao (D10)

```
top = sorted(rota_score, descending)

if top[0].score == 0 and top[1].score == 0:
  # 0 keywords — input vago
  → AskUserQuestion U1-U3 (template T2)
  → re-classifica com input + respostas
  → se ainda vago apos U1 → AskUserQuestion T3 (sugere /idea-to-brief, D12)

elif top[0].score == 1 and top[1].score == 0:
  # 1 keyword — input fraco mas dirigido
  → confirma com usuario via AskUserQuestion T1 simplificada
    "Detectei sinal de [rota]. Esta certo ou e outra coisa?"
  
elif top[0].score >= 2 and top[1].score < top[0].score:
  # 2+ keywords mesma rota, sem empate — caminho 90%
  → roteia DIRETO para top[0].rota SEM perguntar U1-U3
  → vertical destino fara U1-U6 + suas perguntas

elif top[0].score == top[1].score and top[0].score >= 1:
  # Empate entre 2+ rotas
  → AskUserQuestion T1 "É mais [A] ou [B]?" (ou A/B/C se 3 empate)

# Delegacoes externas (rotas 10-12) vencem mesmo com score igual a rota vertical?
# NAO — se top[0] e delegacao externa E nao empata com vertical, delega externamente.
# Se EMPATA com vertical, AskUserQuestion T1 desambigua.
```

### Passo 4: Pipeline cenografia D3 (caso especial concept-reveal)

Se rota=`concept-reveal`:

```
1. Roteia `deck-internal` modo `concept-reveal`
2. AskUserQuestion T4 (pipeline cenografia):
   - Se "ja tenho artefatos" → segue para vertical com paths no handoff
   - Se "preciso gerar" → orchestrator PAUSA, instrui usuario a rodar `skill-cenografia` antes
   - Se "vou sem artefatos visuais" → segue com warning no handoff
```

---

## Casos de borda

### Brand name overlap

Se input menciona "Fotona" mas keywords sao de teaching ("aula sobre Fotona"):
- Marca detectada: Fotona (auto-detection §10.5 nivel 1)
- Rota: `deck-teaching` (keywords teaching dominam)
- Handoff: marca=Fotona + design_system=null + tags=`anvisa-laser-classe-iii` injetadas em deck-teaching

### Negacao explicita

Se usuario diz "NAO e um deck cientifico, e comercial" → ignora kw "cientifico", soma kw "comercial"/"vendas".

### Routing direto + delegacao externa empate

Ex: "preciso de carrossel pra apresentar pro investidor"
- Score: copy=1, fundraising=1 → empate
- AskUserQuestion T1: "É mais carrossel (post social) ou deck de investidor (apresentacao)?"

### NB1 tie-breaker (raro)

Se ainda houver empate apos AskUserQuestion (usuario respondeu vago), consulta NB1 com query:
```
"Qual vertical de deck e mais adequada para: {input} + {respostas U1-U3}?"
```
Falha de NB nao bloqueia — degrada para "vai no melhor palpite + flag warning".

---

## Brand auto-detection §10.5 (5 niveis precedencia, primeiro match vence)

```
1. Input do usuario → regex de ~/.config/deck-builder/brands.yaml
2. CLAUDE.md ativo (working dir) → mencao explicita de marca
3. Agente `culture-lab` carregado → Beauty Smile (fallback)
4. Skill `laser-physics` carregada → Fotona (fallback)
5. Nenhum match → marca = "generico" (vertical pergunta U6)
```

### brands.yaml schema

```yaml
brands:
  - name: "Beauty Smile"
    regex: '\bBeauty Smile\b|beautysmile'
    design_system_skill: "beauty-smile-design-system"
    compliance_tags: ["odontologia-br", "cfo-cfm"]
  - name: "Fotona"
    regex: '\bFotona\b|LightWalker|Er:YAG|Nd:YAG'
    design_system_skill: null
    compliance_tags: ["anvisa-laser-classe-iii", "cfo-laser"]
  - name: "Carnaval 360"
    regex: '\bCarnaval 360\b|carnaval360'
    design_system_skill: null
    compliance_tags: []
```

Usuario pode adicionar marcas editando o YAML — orchestrator releu a cada invocacao.
