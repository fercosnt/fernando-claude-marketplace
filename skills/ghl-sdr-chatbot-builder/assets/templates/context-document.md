# Context Document — SDR Chatbot [NICHO]

> Gerado pela skill `ghl-sdr-chatbot-builder` | Data: [DATA]

---

## 1. Contexto do Negocio

| Campo | Valor |
|-------|-------|
| **Nicho** | [PREENCHER] |
| **Empresa** | [PREENCHER] |
| **Canal principal** | [WhatsApp / SMS / Web Chat / Facebook] |
| **Produtos/Servicos** | [PREENCHER] |
| **Tom de voz** | [PREENCHER — ex: profissional empatetico, casual amigavel, premium sofisticado] |
| **Horario de atendimento** | [PREENCHER — ex: seg-sex 8h-18h, 24/7] |
| **Idioma** | [pt-BR / en / outro] |
| **Posicionamento** | [popular / medio / premium] |

---

## 2. Frameworks Estrategicos (se Beauty Smile)

### ICP (Cliente Ideal)
[Resumo do ICP buscado no Notion, ou N/A se outro nicho]
- Perfil demografico:
- Comportamento de compra:
- Canais preferidos:
- Gatilhos de decisao:

### Framework 3D (Dores, Duvidas, Desejos)
[Resumo do 3D buscado no Notion, ou N/A]
- Top 3 dores:
- Top 3 duvidas:
- Top 3 desejos:

### Matriz de Objecoes
[Resumo das objecoes mais frequentes, ou N/A]
- Objecao 1 (mais frequente):
- Objecao 2:
- Objecao 3:

### Matriz de Implicacao
[Perguntas de implicacao relevantes, ou N/A]

---

## 3. Analise de Scripts SDR

### Scripts Recebidos
[Colar ou resumir os scripts atuais da SDR humana]

### Arvore Decisoria Mapeada
```
[Fluxo logico extraido dos scripts]
Saudacao → Pergunta 1 → Se X: caminho A / Se Y: caminho B → ...
```

### O que Funciona Bem (replicar no bot)
- [Padrao 1 que converte bem]
- [Padrao 2]
- [Padrao 3]

### O que e Exclusivamente Humano (NAO replicar)
- [Acao que exige intuicao humana]
- [Acao que exige conhecimento tecnico profundo]

---

## 4. Estado Atual do GHL

### Custom Fields Existentes
| Nome do Campo | Tipo | Objeto | Uso Atual |
|---------------|------|--------|-----------|
| [campo] | [text/number/select/...] | [contact/opportunity] | [descricao] |

> Fonte: `ghl_get_custom_fields_by_object_key`

### Tags Existentes
| Tag | Proposito | Usada em Automacao? |
|-----|-----------|---------------------|
| [tag] | [proposito] | [sim/nao] |

### Pipelines e Stages
| Pipeline | Stage | Ordem | Automacao Associada |
|----------|-------|-------|---------------------|
| [pipeline] | [stage] | [1,2,3...] | [descricao ou N/A] |

> Fonte: `get_pipelines`

### Workflows Existentes
| Workflow | Trigger | Status | Relevante para Bot? |
|----------|---------|--------|---------------------|
| [workflow] | [trigger] | [ativo/inativo] | [sim/nao] |

> Fonte: `ghl_get_workflows`

### Lead Scoring Atual
| Regra | Pontos | Tipo |
|-------|--------|------|
| [acao] | [+/-N] | [soma/subtrai] |

**Thresholds:**
- Frio: [0-X]
- Morno: [X-Y]
- Quente: [Y-Z]
- Qualificado: [>= Z]

---

## 5. Gaps Identificados

### Custom Fields Faltantes (criar na Fase 2)
- [ ] [campo necessario para qualificacao]

### Tags Faltantes (criar na Fase 2)
- [ ] [tag necessaria para o fluxo do bot]

### Workflows Faltantes (criar na Fase 2)
- [ ] [workflow de handoff]
- [ ] [workflow de nurturing]

### Lead Scoring a Configurar
- [ ] [regras de pontuacao necessarias]

---

## 6. Decisoes Pendentes

| Decisao | Opcoes | Recomendacao | Status |
|---------|--------|--------------|--------|
| [decisao] | [A, B, C] | [recomendacao] | [pendente/aprovado] |
