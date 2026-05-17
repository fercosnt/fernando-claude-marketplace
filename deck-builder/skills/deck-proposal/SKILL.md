---
name: deck-proposal
description: Cria STORYBOARD para propostas comerciais visuais (B2B BR, ticket medio-alto). 3 modos (commercial / strategic-partnership M&A/JV / retainer). Pyramid (Minto, BLUF) + SCQA + ROI framing + Win Without Pitching (Enns). Termos juridicos BR.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core
  - 5a0aaabb-78c1-4d03-a400-e9ce1973737b  # NB3 Comerciais
references:
  - references/framework-pyramid-scqa-roi.md
  - references/framework-win-without-pitching.md
  - references/compliance-termos-juridicos-br.md
  - references/eval-cases-proposal.md
assets:
  - assets/templates/storyboard-skeleton-commercial.md
  - assets/templates/storyboard-skeleton-partnership.md
  - assets/templates/storyboard-skeleton-retainer.md
  - assets/checklists/proposal-checklist.md
---

# deck-proposal

Vertical do plugin **deck-builder**. Gera STORYBOARD.md de propostas comerciais visuais B2B BR de ticket medio-alto em 3 modos: `commercial` (one-shot), `strategic-partnership` (M&A/JV) e `retainer` (recorrente). Aplica Pyramid Principle (Minto, BLUF), SCQA (Situation-Complication-Question-Answer / SCR McKinsey), ROI framing 3-tier e o tom Win Without Pitching de Blair Enns (posicionamento expert, NAO suplica). Termos juridicos BR (IPCA, foro Lei 14.879/2024, multa 2%/mes cap 20% STJ, CADE).

## Quando ativa

**Modo encadeado (default — `deck-orchestrator`):** keywords "proposta", "orcamento", "escopo", "retainer", "consultoria", "M&A", "parceria estrategica" roteiam pra ca conforme matriz §10.3 do SHARED.md.

**Modo standalone:** `/deck-proposal` ou frases como "preciso fazer proposta pra Fotona", "monta retainer Beauty Smile R$30k/mes", "JV Carnaval 360 com agencia X". Roda entrevista U1-U6 (universal §10.1 SHARED.md) + vertical P1-P5.

**Quando NAO usar:**
- Pitch pra investidor (captacao equity) → `deck-fundraising`
- Proposta SaaS B2B com demo de produto e funil de vendas → `deck-sales`
- Orcamento simples (1 paginador, sem narrativa) → escrever direto, sem skill
- Term sheet/MoU/SPA finais juridicos → escritorio juridico, NAO esta skill (a skill produz a versao comercial visual; legal final e outro artefato)

## Entrevista vertical (apos U1-U6 do SHARED.md §10.1)

- **P1: Tipo de servico/escopo.** Consultoria estrategica / agencia / servico longo continuo / M&A advisory / JV. Determina o modo (commercial / retainer / strategic-partnership).
- **P2: Decisor + sponsor interno.** "Decisor economico" (Alan Weiss) — quem assina o cheque. Sponsor interno — quem advoga internamente. Sem decisor mapeado → flag no STORYBOARD.
- **P3: Orcamento alvo + faixa aceitavel.** Numero ancora pra construir os 3 tiers (Essencial / Profissional / Enterprise — NAO "bom/melhor/premium"). Se ausente → derivar do P1 + benchmarks BR §3 do `references/framework-pyramid-scqa-roi.md`.
- **P4: Cronograma esperado.** Inicio + duracao + marcos. Em retainer: 6/12/24 meses (default 12). Em M&A: LOI → CADE → Closing tipicamente 240+90 dias BR.
- **P5: Diferencial vs alternativas.** vs in-house / vs concorrente nomeado / vs status quo. Alimenta o tom Win Without Pitching ("ja diagnosticamos X clinicas similares" > "somos os melhores").

**Inferencia automatica:** se U1 mencionar "fechar retainer" + valor mensal + duracao → preencher P1=continuo, P4=duracao, P3=valor, partir direto pro modo `retainer` sem perguntar redundantemente.

## Modos

| Modo | Quando aplica | Slides | Estrutura backbone |
|------|---------------|-------:|---|
| `commercial` | One-shot (consultoria/servico finito) | 12-15 | Capa → BLUF → SCQA → Solucao → Escopo → Cronograma → 3-tier → Termos → CTA |
| `strategic-partnership` | M&A / JV / parceria longa | 15-20 | Deal thesis → Why now/us/them → Sinergias → Football field → Term sheet visual → Governanca → DD reverso → CADE disclaimer |
| `retainer` | Servico continuo mensal/anual | 12-18 | Capa → BLUF → Why retainer → Escopo In/Out/Flexible → SLA P1/P2/P3 → 3-tier → Termos (IPCA + foro + multa) → Renewal + Termination → CTA |

Templates esqueleto em [assets/templates/](assets/templates/).

## Frameworks aplicados (resumo — detalhes nos refs)

### Pyramid Principle (Minto) — BLUF Bottom Line Up Front

**Regra dura:** slide 2 (apos capa) **e** o BLUF — recomendacao em 1 frase + 3 razoes-suporte. NAO pode estar enterrado. Headlines dos slides seguintes sao **conclusoes** ("Voce perde R$ 2M/ano por ineficiencia logistica"), NAO temas ("Analise de Logistica"). Detalhes vao em apendice.

### SCQA / SCR (McKinsey)

- **Situation** — status quo do cliente (fatos sem julgamento, com dado proprio do cliente quando possivel)
- **Complication** — o que mudou / por que doi agora (custo do nao-agir explicito)
- **Question** — implicita: "o que fazer?"
- **Answer** — a proposta como resposta inevitavel

Exec summary ≤250 palavras (Proposify 2024: acima disso, win rate cai 32%).

### ROI framing

Tres tiers obrigatorios em modos `commercial` + `retainer` — Good/Better/Best ancora o tier medio em 30-50% (HBR 2018 + Blair Enns). Nomes BR enterprise: **Essencial / Profissional / Enterprise**. Tier premium NAO precisa ser realista — ele existe pra ancorar.

Framing: **"investimento", nunca "custo"**. Sempre apresentar valor entregue ANTES do preco. **Regra 5X** (Consulting Success): fee ≈ 20% do valor mensal gerado pro cliente — mostrar a equacao remove percepcao de preco arbitrario.

Patterns de metrica por modo: agencia → ROAS/CPL/CAC payback; consultoria → EBITDA delta / payback meses; M&A → synergy NPV / accretion EPS; retainer → cost-of-not-having / valor / fee ≥ 5×.

### Win Without Pitching (Blair Enns) — tom obrigatorio em todos os modos

**Posicionamento expert, NAO suplica.** Regras tonais:
- **Discovery antes de proposta.** Proposta enviada antes de acordo verbal e "brochura" (Weiss). Liderar com diagnostico documentado: "Conversamos com X stakeholders e identificamos Y" — NAO "Gostariamos de propor".
- **Preco como funcao de valor entregue,** nao horas. "Investimento R$ 200k pra capturar R$ 1.8M de receita incremental" > "20h/mes × R$ X".
- **Termos definitivos,** nao "vamos ver". Datas, donos, valores fechados. Vagueza = falta de autoridade.
- **Equity de mesa.** Cliente decide ENTRE 3 tiers, nao "se vai contratar". Eleva conversa.

Frases banidas (auditor verifica): "gostariamos de", "se possivel", "humildemente propomos", "aguardamos retorno", "fica a criterio", "qualquer coisa estamos a disposicao".

Frases-ancora: "Recomendamos", "Os proximos passos sao", "Pra esta fase voce escolhe entre 3 opcoes", "Decisao ate {data}".

Detalhes em [references/framework-win-without-pitching.md](references/framework-win-without-pitching.md).

## Compliance BR (obrigatorio em todos os modos quando aplicavel)

### Termos juridicos basicos (modo `retainer` — bloco fixo)

- **Reajuste IPCA** (IBGE) anual — IGP-M caiu em desuso pos-pandemia. INPC pra contratos menores.
- **Foro de eleicao Lei 14.879/2024:** pertinencia com domicilio de uma das partes ou local da obrigacao. Default Sao Paulo/SP capital, foro central. **NAO** colocar foro aleatorio — lei jun/2024 invalida.
- **Multa moratoria:** 2%/mes, cap 20% (STJ invalida acima de 20%).
- **Multa compensatoria rescisao antecipada:** 3 meses de fee (default; range 1-3). Documentar notice period (30-90 dias).
- **LGPD:** controlador vs operador, finalidade/adequacao/necessidade/transparencia, prazo de retencao, destruicao ao termino. Obrigatorio pos-2020.
- **Mediacao previa:** 60 dias antes de litigacao reduz custos ~40% (CNJ).

### CADE (modo `strategic-partnership` — disclaimer obrigatorio se aplicavel)

Notificacao **obrigatoria** se atingir simultaneamente:
- Faturamento bruto BR de um grupo ≥ **R$ 750 milhoes** no ultimo exercicio, **E**
- Faturamento bruto BR do outro grupo ≥ **R$ 75 milhoes** no ultimo exercicio.

Quando aplicavel → slide dedicado com disclaimer literal: *"Sujeito a aprovacao do CADE conforme criterios da Lei 12.529/2011. Prazo total estimado 240+90 dias."* Sem cumprir o disclaimer no slide de timeline → flag 🔴.

Detalhes em [references/compliance-termos-juridicos-br.md](references/compliance-termos-juridicos-br.md).

### Outros compliances (heredados do bundle do cliente)

- **Beauty Smile / clinicas:** odontologia BR — CFO Resolucao 196/2019 (publicidade, sem promessa de cura), CFM 2.336/2023 (telesservicos), LGPD dados saude (categoria sensivel).
- **Fotona / equipamentos laser:** Anvisa Classe III, sem comparativo direto com concorrente em material promocional sem evidencia.
- **Carnaval 360 / eventos:** ECAD direitos autorais musicais, Lei Geral do Esporte 14.597/2023 quando aplicavel, Anvisa eventos com alimentos.

## Output STORYBOARD

Schema §10.2 do SHARED.md. **`max_ctas: 1`** (default global). Path default `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`.

### Modo `commercial` (12-15 slides)

1. Capa (cliente + data + versao)
2. **BLUF — Recomendacao em 1 frase + 3 razoes** (Pyramid Minto)
3. SCQA: Situacao do cliente (com dado proprio dele quando possivel)
4. SCQA: Complicacao + custo-do-nao-agir
5-6. Solucao em 2 slides (diagnostico → plano)
7-8. Escopo detalhado **com 3 colunas In / Out / Flexible** (anti-padrao 2 — sem limites negativos)
9. Cronograma (com dependencias e premissas do cliente explicitas)
10. **Investimento 3-tier: Essencial / Profissional / Enterprise**, com ROI framing por tier e parcelamento BR
11. Termos (pagamento, validade da proposta 15-30 dias, condicoes)
12. Equipe responsavel (quem executa, nomes — DocSend: slide de time tem 1m02s atencao media)
13. Caso / prova social (Before / After / Because)
14. Proximos passos (CTA: 3 acoes com data e dono — call de duvidas, decisao ate {data}, instrucao de assinatura)
15. (Opcional) Apendice / FAQ

### Modo `strategic-partnership` (15-20 slides)

Estrutura `commercial` enxuta + bloco extras (Parte 2.5 do `references/framework-pyramid-scqa-roi.md`):

1. Capa
2. **Deal Thesis (BLUF)** — diagrama acquirer/target/combined + 3-4 bullets (por que este deal, por que agora, synergy headline, timeline)
3. Why Now / Why Us / Why Them (Venn diagram)
4. Market Context (TAM/SAM combinado, mapa competitivo pre/pos)
5. Company Overview (target — financials, produtos, clientes, key people)
6. **Sinergias** (slide mais importante apos deal thesis):
   - Revenue synergies — realization 25-35% em 18-36 meses (sempre com haircut)
   - Cost synergies — realization 65-85% em 6-18 meses
   - Capability synergies (qualitativo)
7. Football Field Valuation (4-5 metodologias horizontais)
8. Term Sheet visual (semaforo, 6-8 termos mais materiais — nao os 20 do legal)
9. Deal Structure (asset / stock / merger + funding)
10. **Due Diligence Reverso** (diferenciador BR — target apresenta sua propria analise de risco)
11. Integration Plan 100-day + Year 1 (Gantt swim lanes, ownership)
12. Risk Mitigation (matriz probabilidade × impacto)
13. **Disclaimer CADE** + criterios + prazo (R$ 750M + R$ 75M, Lei 12.529/2011, 240+90 dias)
14. Governanca (board, decisoes, exit, deadlock resolution)
15. Timeline + LOI → Exclusivity → DD → SPA → CADE → Closing
16. Proximos passos

### Modo `retainer` (12-18 slides)

Estrutura `commercial` + bloco extras:

1. Capa / setup de contexto (periodo proposto, tier sugerido, tagline)
2. **BLUF** + tese (por que retainer vs projeto, com custo-do-nao-ter)
3. SCQA contexto do cliente
4. Why Retainer Over Project (curva de aprendizagem, priority access, custo total 20-30% menor que projetos avulsos equivalentes)
5. **Escopo: 3 colunas In / Out / Flexible** (obrigatorio — anti-padrao 2)
6. **SLA matriz P1/P2/P3** (response time + resolution + penalty + compliance targets 99/95/90%)
7-8. Solucao operacional (como o trabalho acontece — discovery monthly, weekly status, QBR trimestral)
9. **Investimento 3-tier:** Essencial / Profissional / Enterprise, com fee model nomeado (Fixed Monthly / Fixed + Overflow / Value-Based / Base + Performance Bonus)
10. **Termos juridicos BR (bloco fixo):**
    - Reajuste IPCA anual, base IBGE
    - Foro Sao Paulo/SP comarca central (Lei 14.879/2024)
    - Multa moratoria 2%/mes cap 20% (STJ)
    - **Multa compensatoria rescisao antecipada: 3 meses de fee**
    - LGPD: controlador/operador, finalidade, retencao, destruicao
11. Renewal Mechanics (auto-renew, opt-out window 30-90 dias, escalacao IPCA)
12. Termination & Transition (notice period, handover obrigatorio, IP rights)
13. Governance (cadencia: weekly status / monthly review / QBR)
14. Equipe responsavel (nomes, alocacao)
15. Caso de retainer de longa data + Proximos passos (CTA + data decisao)

## Whitelist `deck-image-prompts` (regra D5 SHARED.md)

Em todos os modos:
- **Preencher prompt:** `capa`, `problema` (SCQA Complicacao), `conceitual` (solucao/sinergias em diagrama), `comparativo` (3-tier investimento), `demo`, `prova-social` (equipe + caso)
- **Skip:** `dados`, `financeiro`, `CTA`, `disclaimer`, `agradecimento`, `apendice`
- **Override usuario:** `--include-dados` se ROI chart for chave visual

Apos escrever STORYBOARD, encadear `deck-image-prompts` passando lista de slides whitelisted + brief + Big Idea + marca.

## Protocolo de execucao

1. **Auto-detect marca** (§10.5 SHARED.md). Carrega `design_system_skill` se declarado (Beauty Smile → `beauty-smile-design-system`). Injeta `compliance_tags` no checklist.
2. **Entrevista** universal U1-U6 + vertical P1-P5 (pulando perguntas ja inferidas de U1 + contexto).
3. **Decidir modo** (commercial/strategic-partnership/retainer) — confirmar com usuario se ambiguo.
4. **Consultar NB1 + NB3 Comerciais** (max 5 citacoes cada, falha = degrade com warning):
   ```bash
   notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
   notebooklm ask "Pyramid + SCR exec summary deck commercial proposal B2B BR ticket {valor}, Big Idea = {U5}" --max-citations 5

   notebooklm use 5a0aaabb-78c1-4d03-a400-e9ce1973737b
   notebooklm ask "Blair Enns Win Without Pitching 3-tier pricing {modo} BR sector {setor}" --max-citations 5
   ```
5. **Gerar STORYBOARD** conforme schema §10.2 + esqueleto do modo escolhido. **BLUF no slide 2 e regra dura.**
6. **3-tier obrigatorio** em modos `commercial` + `retainer`. Em `strategic-partnership` → opcional, substituido por football field.
7. **Termos juridicos BR** preenchidos com defaults (IPCA + foro SP + multa 2%/mes cap 20% + multa rescisao 3 meses) em modo `retainer`. Em `strategic-partnership` aplicavel → slide CADE com disclaimer literal.
8. **Auditoria tonal Win Without Pitching** — grep frases banidas, sugerir reescrita.
9. **Compliance & Disclaimers** (3 tiers — D7 SHARED.md):
   - 🔴 bloqueante: BLUF ausente / 3-tier ausente em commercial-retainer / multa >20% / foro aleatorio / CADE faltando quando atinge criterios
   - 🟡 verificar: nomes de tier ("bom/melhor" vez de "Essencial/Profissional/Enterprise") / sem dependencias-do-cliente no cronograma / exec summary >250 palavras
   - ✅ OK: lista do que passou
10. **Encadear** `deck-image-prompts` (slides whitelisted) e sugerir `deck-reviewer` se ticket > R$ 100k.

## Defaults

- **Modo default** se ambiguo: perguntar; jamais inferir entre M&A e retainer sem confirmar.
- **Tier nomes BR enterprise:** Essencial / Profissional / Enterprise.
- **Validade proposta:** 15-30 dias (default 30).
- **Forma de pagamento BR:** boleto / PIX / transferencia; oferecer (a) a vista com desconto, (b) parcelado em N vezes, (c) boleto mensal por fase. 77% B2B BR e a prazo (Carta Capital 2025).
- **Reajuste:** IPCA anual; **NUNCA** IGP-M (desuso pos-pandemia).
- **Foro:** Sao Paulo/SP comarca central.
- **Multa moratoria:** 2%/mes, cap 20%.
- **Multa rescisao retainer:** 3 meses de fee.
- **Notice period retainer:** 60 dias (range 30-90).
- **Escrow M&A:** 10-12% por 18 meses (range BR).
- **Cap indenizacao M&A:** 15-25% do deal value (range BR).

## Guardrails

### Anti-padroes (auditor bloqueia ou flag)

| # | Anti-padrao | Acao auditor |
|---|-------------|--------------|
| 1 | Proposta sem diagnostico previo (Enns/Weiss) | 🟡 flag — sugerir slide 3-4 com dado proprio do cliente |
| 2 | Escopo sem coluna "Out" (limites negativos) | 🔴 bloqueia — adicionar 3 colunas In/Out/Flexible |
| 3 | Preco sem ancoragem (1 opcao) em commercial/retainer | 🔴 bloqueia — gerar 3 tiers |
| 4 | Exec summary enterrado ou >250 palavras | 🔴 bloqueia se ausente; 🟡 se >250 |
| 5 | Cronograma sem premissas/dependencias do cliente | 🟡 flag |
| 6 | CTA vago ("aguardamos retorno") | 🔴 bloqueia — substituir por 3 acoes com data+dono |
| 7 | Linguagem vendor-centric ("nossa metodologia" antes do problema) | 🟡 flag tonal |

### Frases banidas (tom Win Without Pitching)

`gostariamos de`, `se possivel`, `humildemente propomos`, `aguardamos retorno`, `fica a criterio`, `qualquer coisa estamos a disposicao`, `acreditamos ser uma boa opcao`, `caso aprovado`, `se for do interesse`.

### Compliance BR (auditor — modos especificos)

- **`retainer`:** IPCA obrigatorio | foro com pertinencia | multa ≤20% | LGPD presente.
- **`strategic-partnership`:** CADE disclaimer se R$750M+R$75M | escrow 10-12% / cap 15-25% se BR | non-compete 2-5 anos key people.
- **Setoriais:** se marca tem `compliance_tags`, validar (CFO/CFM odontologia, Anvisa laser, LGPD saude).

### Falha graceful

- **NB1/NB3 indisponivel:** seguir com defaults da pesquisa, warning `<!-- NB indisponivel; defaults aplicados -->`.
- **`design_system_skill` nao instalado:** seguir sem tokens, warning.
- **Marca sem benchmarks BR no NB3:** usar benchmarks por setor genericos da Parte 2 do framework ref, marcar `<!-- benchmark inferido por setor, validar com cliente -->`.

## Templates pronto-para-copy

3 esqueletos completos em [assets/templates/](assets/templates/):
- [storyboard-skeleton-commercial.md](assets/templates/storyboard-skeleton-commercial.md) — 14 slides
- [storyboard-skeleton-partnership.md](assets/templates/storyboard-skeleton-partnership.md) — 16 slides com CADE
- [storyboard-skeleton-retainer.md](assets/templates/storyboard-skeleton-retainer.md) — 15 slides com termos BR

Checklist final em [assets/checklists/proposal-checklist.md](assets/checklists/proposal-checklist.md).

## Eval cases

3 cases em [references/eval-cases-proposal.md](references/eval-cases-proposal.md):

1. **Beauty Smile retainer agencia R$30k/mes 12 meses** — modo `retainer`, 16 slides, BLUF + SCQA + 3-tier (20/30/45k) + SLA mensal + IPCA + multa rescisao 3 meses + LGPD.
2. **Fotona BR consultoria R$200k 6 meses canal distribuicao** — modo `commercial`, 14 slides, BLUF + SCQA + 3 fases (diagnostico/desenho/implementacao) + 3-tier (200/250/300k) + tom Win Without Pitching ("ja diagnosticamos clinicas similares").
3. **Carnaval 360 + agencia JV sponsorship verticais marcas** — modo `strategic-partnership`, 18 slides, deal thesis + sinergias + revenue share 60/40 + earn-out + governanca + DD cronograma + disclaimer CADE.

## Limites

- NAO renderiza slides finais (PPTX/Gamma/Figma) — so STORYBOARD.md.
- NAO faz term sheet/MoU/SPA juridicos finais — entrega versao comercial visual; juridico final e de escritorio.
- NAO valida CADE caso a caso — gera disclaimer literal quando criterios atingidos; assessoria CADE e externa.
- NAO precifica baseado em dados reais do cliente — usa benchmarks de mercado + numero ancora do P3.
- NAO substitui discovery call — assume diagnostico ja feito ou flag pra fazer antes de enviar.
- NAO faz post de redes sociais (delega `/copy`).
- NAO projeta cenografia/espaco fisico (delega `skill-cenografia` — D3).
- Cita NB1 + NB3 com max 5 hits cada; falha de NB nao bloqueia.

## Referencias

- [references/framework-pyramid-scqa-roi.md](references/framework-pyramid-scqa-roi.md) — Pyramid Minto + SCQA McKinsey + ROI 3-tier + 5X Rule + benchmarks BR por setor.
- [references/framework-win-without-pitching.md](references/framework-win-without-pitching.md) — Blair Enns + Alan Weiss + tom expert + frases banidas/ancora + 12 proclamacoes WWP.
- [references/compliance-termos-juridicos-br.md](references/compliance-termos-juridicos-br.md) — IPCA / Lei 14.879/2024 foro / multa STJ / LGPD / CADE criterios / mediacao / setoriais Beauty Smile-Fotona.
- [references/eval-cases-proposal.md](references/eval-cases-proposal.md) — 3 eval cases detalhados.
- [assets/templates/](assets/templates/) — 3 esqueletos STORYBOARD (commercial / partnership / retainer).
- [assets/checklists/proposal-checklist.md](assets/checklists/proposal-checklist.md) — checklist final + DoD.

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
