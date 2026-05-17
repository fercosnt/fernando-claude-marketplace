# Eval cases — `deck-proposal`

3 cases que cobrem os 3 modos (retainer / commercial / strategic-partnership) e as 3 marcas Fernando (Beauty Smile / Fotona / Carnaval 360). Auditor verifica os criterios DoD em cada um.

---

## Case 1 — Beauty Smile retainer agencia R$30k/mes 12 meses

### Modo: `retainer`

### Input do usuario

> "Beauty Smile vai fechar retainer com agencia de marketing digital. R$30k/mes por 12 meses. Decisor: COO Beauty Smile, sponsor CEO. Diferencial vs in-house e vs agencia generica. Faz proposta."

### Inferencia automatica

- **U6 (marca):** Beauty Smile (auto-detect via regex `\bBeauty Smile\b`). Carrega `beauty-smile-design-system`. `compliance_tags`: ["odontologia-br", "cfo-cfm"].
- **U5 (Big Idea):** "Crescimento de leads qualificados Beauty Smile com agencia dedicada".
- **U3 (duracao):** inferida ~15min (call remota com COO + CEO).
- **U4 (formato):** call remota.
- **P1:** agencia marketing digital.
- **P2:** COO + CEO sponsor.
- **P3:** R$30k/mes.
- **P4:** 12 meses.
- **P5:** vs in-house overload, vs agencia generica sem expertise odonto.

### Output esperado

STORYBOARD modo `retainer`, **16 slides**:

1. Capa Beauty Smile retainer
2. **BLUF:** "Recomendamos retainer Profissional de 12 meses para gerar 200+ leads qualificados/mes" + 3 razoes
3. SCQA Situacao (status quo marketing in-house Beauty Smile)
4. SCQA Complicacao (custo-do-nao-ter: oportunidades perdidas por velocidade lenta — R$ X/mes)
5. Why Retainer over Project (3 vantagens)
6. **Escopo 3 colunas:** In (campanhas, posts, anuncios, copy, briefings) / Out (producao audiovisual, redesign branding, midia paga externa) / Flexible (campanhas sazonais, lancamentos)
7. **SLA P1/P2/P3** (P1 15min response Insta/anuncios down / P2 1h reclamacao publica / P3 4h request normal — targets 99/95/90%)
8. Como trabalhamos (weekly status + monthly review + QBR trimestral)
9. **Investimento 3-tier:**
   - Essencial R$ 20.000,00/mes (Fixed Monthly, sem QBR, SLA P2/P3)
   - **Profissional R$ 30.000,00/mes (recomendado, Fixed + Overflow, todos SLA, QBR mensal)**
   - Enterprise R$ 45.000,00/mes (Base + Performance Bonus, QBR semanal, senior dedicado)
10. **Termos juridicos BR (bloco fixo):**
    - IPCA reajuste anual
    - Foro Sao Paulo/SP comarca central (Lei 14.879/2024)
    - Multa moratoria 2%/mes cap 20% (STJ)
    - **Multa rescisao 3 meses fee**
    - LGPD (Beauty Smile = CONTROLADORA, agencia = OPERADORA — dados pacientes saude SENSIVEIS art. 5 II)
11. Renewal mechanics (auto-renew + opt-out 60 dias + escalacao IPCA)
12. Termination & transition (notice 60 dias + handover + IP rights)
13. Equipe responsavel (nomes — Lead Account 8+ anos odonto, social media, performance)
14. Caso retainer longa data (cliente odonto similar, N renovacoes, resultado X)
15. CTA: call duvidas {data} + decisao ate {data} + inicio {data}
16. Agradecimento

### Auditor — criterios PASS (DoD)

- [x] BLUF no slide 2 ✓
- [x] SCQA com custo-do-nao-ter no slide 4 ✓
- [x] Escopo 3 colunas In/Out/Flexible ✓
- [x] SLA P1/P2/P3 com targets 99/95/90% ✓
- [x] 3 tiers Essencial/Profissional/Enterprise ✓
- [x] Tier Profissional destacado como recomendado ✓
- [x] Formato monetario BR (R$ 30.000,00) ✓
- [x] **IPCA reajuste anual** ✓ (NUNCA IGP-M)
- [x] **Foro SP com pertinencia Lei 14.879/2024** ✓
- [x] **Multa moratoria 2%/mes cap 20% STJ** ✓
- [x] **Multa rescisao 3 meses fee** ✓
- [x] **LGPD com categoria sensivel saude** ✓ (Beauty Smile = saude bucal)
- [x] CTA 3 acoes datadas (sem "aguardamos retorno") ✓
- [x] Frases banidas Win Without Pitching ausentes ✓
- [x] Tom expert (recomendamos) ✓
- [x] Compliance odontologia: sem promessa de cura, sem antes/depois agressivo ✓

### Falhas comuns a evitar

- ❌ Esquecer LGPD com categoria sensivel saude (so "LGPD generico" → 🟡 flag)
- ❌ Multa rescisao 6 meses (range BR e 1-3, default 3) → 🟡 flag
- ❌ Foro "Brasilia" sem pertinencia → 🔴 bloqueia (Lei 14.879/2024)
- ❌ Nomes "Basic / Standard / Premium" → 🟡 flag (usar Essencial/Profissional/Enterprise)

---

## Case 2 — Fotona BR consultoria estrategica R$200k 6 meses

### Modo: `commercial`

### Input do usuario

> "Fotona BR contrata consultoria de 6 meses pra reestruturar canal de distribuicao no Brasil. R$200k total. Diferencial vs McKinsey/Bain (preco) e vs in-house (velocidade + expertise laser odonto). Faz proposta."

### Inferencia automatica

- **U6 (marca):** Fotona (auto-detect via regex `\bFotona\b|LightWalker|Er:YAG|Nd:YAG`). `compliance_tags`: ["anvisa-laser-classe-iii", "cfo-laser"]. Skill `laser-physics` disponivel se necessario.
- **U5 (Big Idea):** "Triplicar canal de clinicas Fotona Brasil em 6 meses sem trocar estrutura corporativa".
- **U3 (duracao):** inferida ~20min (call remota com Diretor Comercial BR).
- **U4 (formato):** call remota.
- **P1:** consultoria estrategica (one-shot 6 meses).
- **P3:** R$200k 6 meses (R$33k/mes equivalente).
- **P4:** 6 meses (diagnostico 2m + desenho 2m + implementacao 2m).
- **P5:** vs McKinsey/Bain (mais barato, mais foco vertical), vs in-house (sem expertise laser odonto + velocidade).

### Output esperado

STORYBOARD modo `commercial`, **14 slides**:

1. Capa Fotona consultoria
2. **BLUF:** "Recomendamos consultoria de 6 meses pra triplicar canal de clinicas Fotona Brasil de 80 para 240 ativos" + 3 razoes
3. SCQA Situacao (canal Fotona Brasil hoje — 80 clinicas ativas, churn 18%, sem CRM dedicado)
4. SCQA Complicacao (sem reestruturacao = perda de R$ 8M/ano em revenue + share competitivo)
5. Solucao em 3 fases (diagnostico → desenho → implementacao)
6. Como executamos (metodologia "Channel Reset" proprietaria, framework SPIN + Challenger adaptado)
7. **Escopo 3 colunas:** In (mapeamento, segmentacao, playbook, treinamento, CRM setup, governance trimestral) / Out (custos de hardware/CRM, hire de pessoas, midia paga) / Flexible (suporte 90 dias pos-implementacao)
8. Cronograma com dependencias do cliente (acesso a base de clinicas, executivo dedicado, decisoes mensais board BR)
9. Equipe responsavel (Lead 12+ anos canais saude, especialista CRM, treinador comercial)
10. **Investimento 3-tier:**
    - Essencial R$ 200.000,00 (Fixed) — 3 fases padrao, sem suporte pos-implementacao
    - **Profissional R$ 250.000,00 (recomendado)** — 3 fases + 90 dias suporte + 1 senior alocado 50%
    - Enterprise R$ 300.000,00 — tudo + execucao operacional + senior 100%
    - Parcelamento BR: 6x R$ 41.666,67 sem juros / a vista PIX 8% desconto
11. Termos: validade 30 dias + Foro SP Lei 14.879/2024 + multa moratoria 2%/mes cap 20% + NDA 5 anos
12. Caso (similar — distribuidor equipamento odonto BR, resultado X)
13. CTA: call duvidas + decisao ate {data} + inicio {data}, condicionado a assinatura ate {data-7}
14. Agradecimento

### Win Without Pitching aplicado (frases-ancora explicitas)

- Slide 5: "Ja diagnosticamos 6 fabricantes de equipamento medico no Brasil nos ultimos 4 anos. O padrao que vimos foi {X}. Recomendamos {Y}."
- Slide 9: "Lead da proposta: {Nome}, 12 anos em canais de saude (incluiu Stryker BR + Henry Schein)" (autoridade, NAO suplica)
- Slide 13: "Pra que possamos iniciar 15/06, precisamos ter assinatura ate 05/06."
- **NAO usar:** "gostariamos de propor", "se possivel agendar", "humildemente apresentamos", "aguardamos retorno"

### Auditor — criterios PASS (DoD)

- [x] BLUF no slide 2 ✓
- [x] SCQA com numero do impacto (R$ 8M/ano) ✓
- [x] Escopo 3 colunas ✓
- [x] 3 tiers (200k/250k/300k) ✓
- [x] Tier Profissional recomendado destacado ✓
- [x] Tier Enterprise existe pra ancorar ✓
- [x] Forma de pagamento BR (parcelado + a vista desconto) ✓
- [x] Validade 30 dias ✓
- [x] Tom expert (frases-ancora WWP) ✓
- [x] Foro SP Lei 14.879/2024 ✓
- [x] Equipe nomeada com credencial ✓
- [x] Compliance Anvisa Classe III mencionado (mesmo que skill seja sobre canal, nao produto) ✓

### Falhas comuns a evitar

- ❌ Pricing em "horas × R$/h" (proposta consultoria deve ser fee fixo + ROI framing)
- ❌ Comparativo head-to-head com Fotona vs concorrente (sem evidencia controlada — Anvisa Classe III)
- ❌ "Estimamos aproximadamente R$200k" → 🟡 flag (definitivo: "R$ 200.000,00")

---

## Case 3 — Carnaval 360 + agencia JV sponsorship verticais marcas

### Modo: `strategic-partnership`

### Input do usuario

> "Carnaval 360 + agencia X formam JV pra vender sponsorship em verticais (cosmetico, bebida, fintech). Revenue share 60/40 (Carnaval 360 / agencia). 3 anos com renovacao. Faz proposta."

### Inferencia automatica

- **U6 (marca):** Carnaval 360 (auto-detect via regex `\bCarnaval 360\b|carnaval360`). `compliance_tags`: [] (eventos — ECAD/LGE quando aplicavel).
- **U5 (Big Idea):** "JV Carnaval 360 + agencia X gera R$ 15M em sponsorship verticais nos primeiros 3 anos".
- **U3 (duracao):** inferida ~25min (call presencial ou hibrida com diretoria de ambas).
- **U4 (formato):** hibrido.
- **P1:** parceria estrategica longa (JV).
- **P3:** revenue share 60/40, target 3 anos.
- **P5:** vs cada empresa atuar separadamente (faltam capilaridade + relacionamento marca).

### Triagem CADE

**Verificar:** faturamento bruto BR de Carnaval 360 + faturamento bruto BR da agencia X no ultimo exercicio.

- Se **Carnaval 360 ≥ R$ 750M e agencia ≥ R$ 75M (ou vice-versa)** → disclaimer CADE OBRIGATORIO (Lei 12.529/2011).
- Se NAO atinge criterios → mencionar literal "Lei 12.529/2011 nao se aplica a este caso (faturamentos abaixo dos thresholds)".

Cenario realista deste case: agencia provavelmente abaixo de R$ 75M → disclaimer no formato "nao se aplica", mas com texto formal pra antecipar pergunta do juridico.

### Output esperado

STORYBOARD modo `strategic-partnership`, **18 slides**:

1. Capa "Deal Proposal: Carnaval 360 × Agencia X — JV Sponsorship Verticals"
2. **Deal Thesis (BLUF):** 4 bullets — why this deal / why now / synergy headline / timeline
3. Why Now / Why Us / Why Them (Venn 3 circulos — janela mercado carnaval 2027 + capilaridade Carnaval 360 + relacionamento marca da agencia)
4. Market Context (TAM sponsorship carnaval BR, mapa competitivo)
5. Company Overview — Carnaval 360 + Agencia X (financials, ativos, key people)
6. **Sinergias** (slide mais importante):
   - Revenue: cross-sell marca-marca (haircut 30% → R$ X liquido)
   - Cost: SG&A duplicado, eventos compartilhados (haircut 75% → R$ Y liquido)
   - Capability: relacionamento marca + capilaridade evento (qualitativo)
7. Football Field Valuation (5 metodologias horizontais)
8. **Revenue Share Structure (Term Sheet visual semaforo):**
   - 60% Carnaval 360 / 40% agencia X 🟢
   - Earn-out adicional 10% pra agencia se exceder R$ 8M ano 1 🟡
   - Escrow 10% por 18 meses 🟢
   - Cap indenizacao 20% 🟢
   - Lock-up 2 anos 🟢
   - Non-compete 3 anos key people 🟢
9. Deal Structure (constituicao JV em SP, holding combinada)
10. **Due Diligence Reverso** (Carnaval 360 + agencia X apresentam analises de risco — diferenciador BR)
11. Integration Plan 100-day (operacional + comercial + financeiro + comunicacao com marcas)
12. Risk Mitigation (matriz prob × impacto: regulatorio ECAD/Anvisa eventos + operacional + cultural fit + mercado)
13. **Disclaimer CADE** (literal): "Os criterios da Lei 12.529/2011 (R$ 750M + R$ 75M) **nao se aplicam** a este caso. Notificacao ao CADE dispensada. Caso o faturamento das partes evolua para os thresholds em exercicios futuros, sera necessaria nova analise."
14. Governanca pos-JV (board 5 cadeiras 3:2 Carnaval 360 : agencia, decisoes super-majoritarias em orcamento >R$2M e exit)
15. Due Diligence cronograma (60 dias DD + 30 dias SPA)
16. Timeline + LOI → DD → SPA → Closing Q{N}/{ano}
17. Setoriais (ECAD direitos musicais + Lei Geral do Esporte 14.597/2023 + Anvisa eventos com alimentos se aplicavel)
18. Agradecimento + contato confidencial

### Auditor — criterios PASS (DoD)

- [x] Deal Thesis (BLUF) no slide 2 ✓
- [x] Sinergias COM e SEM haircut (anti-padrao M&A 1) ✓
- [x] Football field 4-5 metodologias ✓
- [x] Term sheet visual semaforo (8 termos materiais) ✓
- [x] Escrow 10% / Cap 20% (range BR 10-12% / 15-25%) ✓
- [x] Non-compete 3 anos (range 2-5) ✓
- [x] **Disclaimer CADE literal** ✓ (mesmo no formato "nao se aplica")
- [x] **DD Reverso** (anti-padrao M&A 5) ✓
- [x] Integration plan 100-day com owners (anti-padrao M&A 3) ✓
- [x] Cultural fit considerado (anti-padrao M&A 4) ✓
- [x] Governanca pos-deal (deadlock + exit) ✓
- [x] Setoriais eventos (ECAD + LGE + Anvisa eventos) ✓
- [x] Tom expert (sem suplica em deal) ✓

### Falhas comuns a evitar

- ❌ Esquecer disclaimer CADE (mesmo quando nao se aplica — antecipa pergunta juridico) → 🟡 flag
- ❌ Synergias sem haircut (numeros brutos) → 🔴 bloqueia (anti-padrao M&A 1)
- ❌ "Criaremos comite" sem nomes/datas/owners → 🔴 (anti-padrao M&A 3)
- ❌ Term sheet com 20 campos do legal → 🟡 (limitar a 6-8 materiais)
- ❌ Pular setoriais eventos (ECAD obrigatorio) → 🟡 flag

---

## Resumo dos 3 cases

| # | Caso | Modo | Slides | Tier obrigatorio | Termos BR | Setoriais |
|---|------|------|-------:|------------------|-----------|-----------|
| 1 | Beauty Smile retainer R$30k/mes | retainer | 16 | Essencial/Profissional/Enterprise | IPCA+foro+multa 3m+LGPD sensivel | CFO 196/2019 |
| 2 | Fotona consultoria R$200k/6m | commercial | 14 | 200k/250k/300k | Foro+multa+validade 30d | Anvisa Classe III |
| 3 | Carnaval 360 + agencia JV | strategic-partnership | 18 | (substituido por football field) | Escrow+cap+non-compete | ECAD+LGE+Anvisa eventos |

Cada case exercita um modo diferente, uma marca diferente do Fernando, um ticket diferente (R$30k recorrente / R$200k one-shot / revenue share multi-anual), e um perfil de compliance diferente (saude / equipamento medico / eventos).
