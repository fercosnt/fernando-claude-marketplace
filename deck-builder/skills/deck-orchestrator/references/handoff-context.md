# Handoff Context — `deck-orchestrator` → vertical destino

> O orchestrator **NAO gera STORYBOARD**. Ele apenas roteia + passa contexto. Este arquivo define o pacote canonico de handoff.

---

## Schema do handoff

```yaml
handoff:
  # 1) INPUT ORIGINAL (sempre)
  input_original: "string verbatim do usuario, sem normalizacao"
  timestamp: "ISO 8601 UTC"
  
  # 2) ROTA ESCOLHIDA (sempre)
  vertical_destino: "deck-fundraising | deck-sales | deck-clinical | deck-equipment | deck-teaching | deck-proposal | deck-scientific | deck-internal"
  modo: "concept-reveal | peer-facing | patient-facing | aula-tecnica | workshop-hands-on | keynote-inspirational | padrao | commercial | strategic-partnership | retainer | demo-presentation | sponsorship | demo-day | poster | oral-short | oral-long | keynote | comparativo | pitch-to-leadership | strategy | all-hands | null"
  
  # 3) ROTEAMENTO (sempre — auditavel)
  rota_score:
    fundraising: 3
    sales: 0
    clinical: 0
    equipment: 0
    teaching: 0
    proposal: 0
    scientific: 0
    internal: 0
    concept_reveal: 0
    cenografia: 0
    copy: 0
    culture_lab: 0
  keywords_matched:
    - "pitchar"
    - "anjo"
    - "R$500k"
  algoritmo_branch: "2+_mesma_rota_direto | 2+_empate_AskUserQuestion | 0-1_kw_perguntou_U1-U3 | apos_U1_sugeriu_idea_to_brief"
  
  # 4) RESPOSTAS PRE-COLETADAS (so existe se input vago + perguntou U1-U3)
  respostas_pre_coletadas:
    U1: "objetivo unico (acao da audiencia)"
    U2: "audiencia (perfil + senioridade + conhecimento previo)"
    U3: "duracao (1-5 categorias)"
  # null se rotou direto sem perguntar (caminho 90%)
  
  # 5) AUTO-DETECTION §10.5 (sempre)
  marca_detectada: "Beauty Smile | Fotona | Carnaval 360 | generico"
  marca_origem: "input_regex | claude_md | culture_lab_fallback | laser_physics_fallback | nenhum"
  design_system_skill: "beauty-smile-design-system | null"
  design_system_loaded: true | false
  compliance_tags:
    - "odontologia-br"
    - "cfo-cfm"
  brands_yaml_path: "~/.config/deck-builder/brands.yaml"
  
  # 6) PIPELINE FLAGS (so quando concept-reveal — D3)
  pipeline_cenografia:
    status: "artefatos_prontos | aguardando_cenografia | sem_artefatos_warning | nao_aplica"
    artefatos_paths:
      - "/path/to/render-1.png"
      - "/path/to/mood-board.json"
    warning: "string opcional se status=sem_artefatos_warning"
  
  # 7) FRONTEIRA (sempre)
  vertical_responsabilidades:
    - "Fazer entrevista universal U1-U6 (completar as faltantes se ja tem)"
    - "Fazer entrevista vertical (F1-F5 / S1-S5 / C1-C5 / ...)"
    - "Gerar STORYBOARD em $DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md"
    - "Sugerir deck-image-prompts para slides whitelist D5"
    - "Sugerir deck-reviewer em decks de alta consequencia"
```

---

## Quando passar o handoff

### Caso routing direto (2+ keywords mesma rota — caminho 90%)

`respostas_pre_coletadas` = `null`. Vertical fara U1-U6 do zero.

```yaml
handoff:
  input_original: "preciso pitchar Beauty Smile pra anjo do Iguatemi R$500k"
  vertical_destino: "deck-fundraising"
  modo: "padrao"
  rota_score: {fundraising: 3, ...}
  keywords_matched: ["pitchar", "anjo", "R$500k"]
  algoritmo_branch: "2+_mesma_rota_direto"
  respostas_pre_coletadas: null
  marca_detectada: "Beauty Smile"
  marca_origem: "input_regex"
  design_system_skill: "beauty-smile-design-system"
  design_system_loaded: true
  compliance_tags: ["odontologia-br", "cfo-cfm"]
  pipeline_cenografia: {status: "nao_aplica"}
```

### Caso input vago (0-1 keyword — orchestrator pergunta U1-U3 antes)

`respostas_pre_coletadas` preenchidas, vertical NAO repete U1-U3.

```yaml
handoff:
  input_original: "preciso de slides"
  vertical_destino: "deck-internal"
  modo: "all-hands"
  rota_score: {internal: 0, ...}  # todas zero
  keywords_matched: []
  algoritmo_branch: "0-1_kw_perguntou_U1-U3"
  respostas_pre_coletadas:
    U1: "alinhar squad sobre nova politica de viagens"
    U2: "10 lideres de squad, conhecem politica antiga"
    U3: "3"  # opcao 3 = 15-20min
  marca_detectada: "generico"
  marca_origem: "nenhum"
  design_system_skill: null
  compliance_tags: []
  pipeline_cenografia: {status: "nao_aplica"}
```

### Caso concept-reveal pipeline D3

Adiciona bloco `pipeline_cenografia` com status real.

```yaml
handoff:
  input_original: "queria apresentar o conceito da sala VIP do Carnaval 360 pro board"
  vertical_destino: "deck-internal"
  modo: "concept-reveal"
  rota_score: {internal: 1, concept_reveal: 2, ...}
  keywords_matched: ["apresentar conceito", "sala VIP", "board"]
  algoritmo_branch: "2+_mesma_rota_direto"  # concept-reveal venceu
  marca_detectada: "Carnaval 360"
  marca_origem: "input_regex"
  design_system_skill: null
  compliance_tags: []
  pipeline_cenografia:
    status: "aguardando_cenografia"  # usuario disse "vou rodar skill-cenografia primeiro"
    artefatos_paths: []
    warning: "PAUSA — orchestrator nao delegou ate usuario voltar com artefatos"
```

---

## Como a vertical destino consome o handoff

### Passo 1: Verifica completude

- `respostas_pre_coletadas != null`? Pula U1-U3 na entrevista universal, faz so U4-U6
- `marca_detectada != "generico"`? Pula U6, usa marca detectada
- `design_system_loaded == true`? Carrega tokens; senao deixa visual neutro

### Passo 2: Injeta compliance tags

- Vertical mapeia tags do handoff para suas proprias guardrails:
  - `odontologia-br` → bloco compliance §10.2 inclui CFO 196/2019 + CFM 1974/2011
  - `cfo-cfm` → linguagem proibida ("garante resultado", "100% sucesso")
  - `anvisa-laser-classe-iii` → disclaimer obrigatorio + classe do equipamento
  - `cfo-laser` → idem + responsavel tecnico

### Passo 3: Inicia entrevista

```
[Carrega handoff context]
Marca detectada: Beauty Smile (via input regex)
Design system carregado: beauty-smile-design-system ✓
Compliance tags: odontologia-br, cfo-cfm

Vou completar a entrevista (U1-U6 + F1-F5 fundraising):

U1. Qual o objetivo unico deste deck? (acao que a audiencia deve tomar apos assistir)
...
```

---

## Casos especiais

### Empate apos AskUserQuestion T1 (usuario escolheu)

Orchestrator escolhe a rota que o usuario selecionou, e marca `algoritmo_branch: "2+_empate_AskUserQuestion"`. Keywords da rota perdedora SAO preservadas em `keywords_matched` para auditoria.

### Delegacao externa (NAO deck)

NAO gera handoff completo — apenas mensagem clara:
```
Isso nao e um deck. {Carrossel/cultura/render} e da skill {/copy | culture-lab | skill-cenografia}.
Delegando agora.
```
Se a skill externa precisar de contexto da marca, orchestrator passa: `marca + brands.yaml path + input original`.

### Brand NAO detectada mas vertical exige (ex: deck-equipment + Fotona ausente)

Vertical pergunta U6 normalmente. NAO e responsabilidade do orchestrator forcar deteccao de marca.
