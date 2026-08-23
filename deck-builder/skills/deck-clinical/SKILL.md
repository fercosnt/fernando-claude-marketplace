---
name: deck-clinical
description: Cria STORYBOARD para apresentacao de protocolos clinicos (peer-facing ou patient-facing). EBM + AIDET + Calgary-Cambridge. Compliance CFO 196/2019 + CFM 1974/2011 + Anvisa em bloco final 3 tiers.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core Transversal
  - 1635d16b-773c-480d-89c2-79c717f4b2e1  # NB2 Verticais Densas (clinical + scientific + equipment)
references:
  - references/framework-ebm-aidet-calgary.md
  - references/compliance-cfo-cfm-anvisa.md
  - references/eval-cases-clinical.md
assets:
  - assets/templates/storyboard-skeleton-peer.md
  - assets/templates/storyboard-skeleton-patient.md
  - assets/checklists/clinical-compliance-3tiers.md
---

# deck-clinical

Skill vertical do plugin **deck-builder**. Gera STORYBOARD para apresentacoes clinicas — protocolos, tratamentos, casos — em dois modos: `peer-facing` (dentistas/medicos) e `patient-facing` (paciente leigo).

Compliance regulatorio (CFO Res. 196/2019 + CFM 1974/2011 + Anvisa) e OBRIGATORIO — porem aplicado em **soft enforcement** (D7): a skill SEMPRE gera o deck completo e consolida issues em bloco final de 3 tiers (🔴/🟡/✅). Nunca bloqueia geracao.

## Quando ativa

Roteada pelo `deck-orchestrator` quando detecta keywords:
- "protocolo", "tratamento", "paciente", "indicacao clinica", "evidencia clinica", "aula clinica", "apresentar tratamento pro paciente"
- Auto-detection Fotona/Er:YAG/Nd:YAG → injeta compliance tag `anvisa-laser-classe-iii` (carrega skill `laser-physics` se disponivel)
- Auto-detection Beauty Smile → carrega `beauty-smile-design-system`

Tambem invocavel diretamente via `/deck-clinical`.

## Diferenca entre os dois modos

| Aspecto | `peer-facing` | `patient-facing` |
|---------|--------------|------------------|
| Audiencia | Dentista/medico (especialista ou generalista) | Paciente leigo (sem formacao em saude) |
| Framework | EBM hierarchy + Calgary-Cambridge | AIDET |
| Linguagem | Tecnica (osseointegracao, GRADE, RCT) | Leiga obrigatoria (substituir jargao) |
| Estrutura | caso → diagnostico → tratamento → outcome → follow-up | Acknowledge → Introduce → Duration → Explanation → Thank |
| Slides | 10-14 | 6-8 |
| Bloco evidencia | Slide dedicado com GRADE + papers citados | Pulado (irrelevante pro paciente) |
| Alternativas | Implicito (literatura) | OBRIGATORIO (consentimento informado) |

Detalhe dos frameworks em [references/framework-ebm-aidet-calgary.md](references/framework-ebm-aidet-calgary.md).

## Entrevista vertical (apos U1-U6 universais do SHARED §10.1)

| # | Pergunta | Tipo |
|---|----------|------|
| C1 | Protocolo/tratamento especifico? (ex: clareamento Er:YAG, implante Bicon, All-on-4) | texto |
| C2 | Indicacao clinica + contraindicacoes | texto |
| C3 | Nivel de evidencia disponivel? (RCT / meta-analise / case series / opiniao especialista / GRADE) | texto + GRADE opcional |
| C4 | Audiencia: (1) especialista (2) generalista (3) paciente leigo | escolha |
| C5 | Tem antes-e-depois? → SE sim, ha TCLE assinado para uso? | sim+TCLE / sim sem TCLE / nao |

**C4 define o modo:** (1) ou (2) → `peer-facing`; (3) → `patient-facing`.

**C5 dispara compliance:** "sim sem TCLE" → 🔴 BLOCKER no bloco final, sem excecao (CFO Res. 196/2019).

## Protocolo de geracao

1. **Detectar modo** via C4 + auto-detection equipamentos (injeta tag se Fotona/laser).
2. **Consultar NBs** (template em SHARED §10.6):
   - NB1 Core sempre (estrutura narrativa, action titles, principios)
   - NB2 Densas para evidencia clinica + apresentacoes-protocolos-clinicos + apresentacoes-cientificas-congressos-saude (Alley + Hofmann + Carter)
   - Falha de NB NAO bloqueia — degrada com warning
3. **Carregar template** correspondente (`storyboard-skeleton-peer.md` ou `storyboard-skeleton-patient.md`).
4. **Preencher slides** conforme estrutura (10-14 peer / 6-8 patient).
5. **Aplicar linguagem proibida → substituir/marcar** (lista canonica abaixo).
6. **Invocar `deck-image-prompts`** apenas para slides na whitelist D5 (capa | problema | conceitual | comparativo | demo | prova-social).
7. **Preencher bloco Compliance & Disclaimers (3 tiers)** ANTES de fechar o storyboard — checklist em [assets/checklists/clinical-compliance-3tiers.md](assets/checklists/clinical-compliance-3tiers.md).
8. **Salvar** em `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md` (SHARED §10.4).

## Linguagem proibida (canonica)

A skill substitui automaticamente OU marca como 🔴 no bloco final:

| Termo proibido | Substituir por | Razao |
|----------------|---------------|-------|
| "Cura" / "curar" | "tratamento", "manejo", "resolucao clinica" | CFO/CFM proibem promessa de cura |
| "Garantido" / "garantia" | "tipicamente", "na maioria dos casos" | CFO/CFM proibem garantia de resultado |
| "100%" / "100 por cento" | "documentado em N% dos casos (literatura)" | Promessa absoluta |
| "Reverte completamente" | "melhora documentada em..." | Promessa absoluta |
| "Sem dor" (em procedimento invasivo) | "anestesia local minimiza desconforto" | Desinformacao clinica |
| "Sem riscos" / "totalmente seguro" | "riscos minimizados conforme protocolo" | Negacao de risco viola consentimento informado |

Se termo aparecer em input do usuario (U1 Big Idea, C1) e nao puder ser substituido sem trair intencao → marca como 🔴 BLOCKER no bloco final e propoe alternativa no campo "evidencia de remediacao".

## Compliance enforcement (D7 — SEM hard-block)

A skill **NUNCA bloqueia geracao**. Issues consolidados em bloco final do STORYBOARD com 3 tiers:

### 🔴 BLOCKER (sempre marca, resolver antes de apresentar)
- Linguagem proibida nao removivel sem trair Big Idea
- Antes-e-depois SEM TCLE explicito mencionado → CFO Res. 196/2019
- Promete resultado especifico sem disclaimer "individual variation"
- Equipamento Anvisa Classe III mencionado SEM declaracao de registro (Fotona)
- Procedimento invasivo apresentado a paciente SEM slide de alternativas (viola consentimento informado)
- Promessa de cura/garantia/100% no body de slide

### 🟡 VERIFICAR (revisar antes de apresentar)
- Conflito de interesse (Fotona patrocinador) declarado em slide proprio?
- Citacao GRADE pelo menos no slide nivel de evidencia? (modo peer)
- Limites de uso off-label mencionados explicitamente?
- Disclaimer "individual variation" presente em slide pos-procedimento?
- Jargao tecnico restante em modo patient-facing? (revisar slide-a-slide)
- Tempo procedimento + recuperacao realistas? (modo patient)

### ✅ OK
- Confirmacoes do que esta correto (TCLE mencionado, GRADE citado, COI declarado, AIDET aplicado, alternativas mostradas)

Mapeamento detalhado issue → tier em [assets/checklists/clinical-compliance-3tiers.md](assets/checklists/clinical-compliance-3tiers.md).
Resolucoes citaveis em [references/compliance-cfo-cfm-anvisa.md](references/compliance-cfo-cfm-anvisa.md).

## Output STORYBOARD

Schema canonico em SHARED §10.2. Particularidades clinical:

- `## Meta` inclui `Modo: peer-facing | patient-facing` e `max_ctas: 1`
- Slide tipo `disclaimer` sempre presente quando aplicavel (antes-e-depois, off-label, COI)
- Antes-e-depois (`comparativo`) sempre acompanhado de mencao explicita ao TCLE no body do slide
- Bloco `## Compliance & Disclaimers (3 tiers)` preenchido pela skill ANTES de `deck-reviewer` rodar (reviewer pode reclassificar)

## Whitelist deck-image-prompts (D5 default)

- **Preencher:** `capa`, `problema` (caso clinico abertura), `conceitual` (esquema anatomico), `comparativo` (antes/depois COM placeholder TCLE), `demo` (procedimento), `prova-social` (caso completo)
- **Skip:** `dados` (usar grafico SE necessario; override `--include-dados` se citar RCT), `financeiro`, `CTA`, `disclaimer` (texto-only), `agradecimento`, `apendice`

**Critico:** ao passar brief de imagem para tipo `comparativo`, sempre incluir:
- Placeholder TCLE na descricao
- Tom clinico (NAO cosmetico-vendedor)
- Sem rosto identificavel se TCLE pendente (sugerir crop boca/area tratada)

## NBs a consultar

- **NB1 Core** (`7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da`): estrutura narrativa, action titles, principios
- **NB2 Densas** (`1635d16b-773c-480d-89c2-79c717f4b2e1`): apresentacoes-protocolos-clinicos + apresentacoes-cientificas-congressos-saude (Alley, Hofmann, Carter)

Query exemplo (template SHARED §10.6):
```bash
notebooklm use 1635d16b-773c-480d-89c2-79c717f4b2e1
notebooklm ask "EBM GRADE Er:YAG clareamento dental evidencia RCT systematic review hipersensibilidade — Big Idea: Dentistas aprovam protocolo Er:YAG como alternativa a peroxido" --max-citations 5
```

## Eval cases (3)

Detalhe completo em [references/eval-cases-clinical.md](references/eval-cases-clinical.md) e fixtures em [evals/evals.json](evals/evals.json):

1. **Case 1 — Protocolo Er:YAG clareamento (peer):** 12 slides Calgary-Cambridge, GRADE moderate, COI Fotona, off-label disclaimer, TCLE mencionado → bloco final 3 tiers preenchido.
2. **Case 2 — All-on-4 paciente 55 anos (patient sem TCLE):** 7 slides AIDET, linguagem leiga obrigatoria, alternativas mostradas → bloco final 🔴 BLOCKER TCLE pendente (valida regra D7 sem hard-block).
3. **Case 3 — CIOSP "Laser na endodontia" (peer):** 14 slides Calgary-Cambridge + 3 slides bloco evidencia + apendice 5 papers + GRADE por outcome (high para descontaminacao, low para cura sintomatica) + COI declarado.

## Fronteiras (SHARED §10.8)

- NAO gera slides finais sem pedido explicito (D15) — default e STORYBOARD.md. Render e exclusividade de `deck-render-canva`, opt-in e so com MCP do Canva conectado. PPTX/Google Slides/Figma/Gamma seguem proibidos.
- NAO faz busca de literatura em tempo real — usuario fornece nivel de evidencia (C3)
- NAO substitui parecer clinico — gera material de apresentacao, decisao clinica e do profissional
- NAO escreve TCLE — apenas exige mencao explicita quando antes-e-depois presente
- NAO bloqueia geracao por compliance (D7) — consolida em bloco final 3 tiers

## Handoff: render no Canva (v2.0.0 — opt-in, D16)

Ao entregar o `STORYBOARD.md`, **se e somente se** o MCP do Canva estiver conectado, ofereca via `AskUserQuestion`:

> "Gero a base deste deck no Canva a partir do storyboard?"
> - Sim → `deck-render-canva`
> - Nao → encerra normalmente

Invioláveis:
- **Nunca** chama `deck-render-canva` automaticamente (D16).
- MCP do Canva desconectado → **nao oferece**. Sem aviso e sem opcao quebrada (D15).
- Recusa encerra o fluxo normalmente — nao insiste, nao repergunta.
- Sem brand template para a marca, o render reporta e pula. Nunca cai para geracao livre (D19).

## DoD especifico (alem do generico SHARED §13.6)

- [ ] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1 + NB2
- [ ] 3 eval cases passando (Er:YAG peer / All-on-4 patient sem TCLE / CIOSP endodontia)
- [ ] 2 modos funcionais (peer-facing / patient-facing)
- [ ] Compliance D7: SEM hard-block, bloco final 3 tiers SEMPRE preenchido
- [ ] Linguagem proibida automaticamente substituida ou marcada 🔴
- [ ] Antes-e-depois SEM TCLE → 🔴 BLOCKER (Case 2 valida)
- [ ] Equipamento Fotona/laser detectado → injeta `anvisa-laser-classe-iii`
- [ ] Linguagem leiga obrigatoria em modo patient-facing (Case 2 valida)
- [ ] Schema §10.2 valido
- [ ] Instalada Claude Code + Cowork Desktop (D13)

## v1.1 — Adendo: `modo_entrega` + `[VERIFICAR]` + Layout sugerido

A partir de v1.1 do plugin, esta skill aplica 4 disciplinas adicionais ao gerar STORYBOARD. Detalhes canônicos em `../../shared/storyboard-schema.md` e `../../shared/verificar-flag.md`.

**1. `modo_entrega` adapta densidade do slide** (regra 7 do schema):
- `apresentado-ao-vivo` (U4=1/2): slides minimalistas (2-3 bullets) + speaker notes RICOS
- `enviado-para-leitura` (U4=3): slides DENSOS (4-6 bullets + dados inline + 1 quote curto) + speaker notes opcionais ou curtos
- `hibrido` (U4=4): meio-termo, ambos preenchidos

Preencher bloco `Conteúdo do slide (visível na projeção)` em cada slide, calibrado ao `modo_entrega`.

**2. `Layout sugerido` em cada slide** (regra 8 do schema): grid + tipografia + componentes visuais + animação. Sem isso, designer/Gamma/Claude Design/PowerPoint recebe o deck "no escuro".

**3. `[VERIFICAR]` em dados fabricados** (regra 9 do schema + `verificar-flag.md`): todo R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa que a skill **inferir** (não veio do usuário; não é público canonicamente conhecido) recebe `[VERIFICAR: descrição]` inline ou em footnote. Lint v1.1 emite WARN quando ausente. Reviewer converte em 🟡 ou 🔴 no segundo passe.

**4. Bold opcional nos rótulos:** preferir `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` para facilitar leitura visual. Lint aceita ambos formatos.

**Checklist v1.1 ao gerar cada slide:**
- [ ] `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` em bold
- [ ] Bloco `Conteúdo do slide (visível na projeção)` preenchido com densidade adaptada ao `modo_entrega`
- [ ] Bloco `Layout sugerido` com grid + tipografia + componentes
- [ ] Dados específicos inferidos marcados com `[VERIFICAR: ...]`
- [ ] `Imagens sugeridas` no formato v1.1 (Quantidade explícita + variações em blocos separados)
