# Eval Cases — deck-fundraising

3 casos obrigatorios. Cada caso testa 1 modo + auto-deteccao de marca + compliance especifico.

## Case 1 — Beauty Smile pitch anjo R$500k (modo `padrao`)

### Inputs

| Pergunta | Resposta |
|----------|----------|
| U1 (objetivo) | "Conseguir R$500k pra abrir 2a unidade Beauty Smile em SP em 6 meses" |
| U2 (audiencia) | "Anjo individual, alto patrimonio Iguatemi SP, sem experiencia previa em healthcare" |
| U3 (duracao) | 12 min (escolha 3 — 7-12min) |
| U4 (formato) | Pitch presencial 1:1 (cafe Iguatemi) |
| U5 (Big Idea) | "Beauty Smile prova que dentista premium escala como rede butique — nao como franquia comoditizada" |
| U6 (marca) | Beauty Smile (auto-detect via regex) |
| F1 (estagio) | seed |
| F2 (ticket) | R$500k em troca de 8% equity post-money (cap R$6,25M) |
| F3 (tracao) | R$180k/mes receita, NPS 91, 247 pacientes ativos, 89% retention 12 meses |
| F4 (concorrente) | clinica generica de bairro; diferencial = protocolos com evidencia + UX butique premium |
| F5 (risco) | escalabilidade — "vai manter a qualidade na 2a unidade?" |

### Output esperado

**Path:** `$DECKS_DIR/2026-05/STORYBOARD-beauty-smile-pitch-anjo-XXXX.md`

**Meta:**
- Skill: deck-fundraising
- Modo: padrao
- Framework: Sequoia + Andy Raskin
- max_ctas: 1
- Marca: Beauty Smile (com `beauty-smile-design-system` carregado se instalado)
- Compliance tags: odontologia-br, cfo-cfm

**Estrutura 13 slides:**

| # | Tipo | Action title esperado | Conteudo-chave |
|---|------|----------------------|----------------|
| 1 | capa | "Beauty Smile: rede butique de dentista premium" | Big Idea derivada |
| 2 | problema | "78% das clinicas premium fecham 2a unidade em 24 meses" | Loss aversion BR healthcare |
| 3 | comparativo | "Franquia comoditizada vs rede butique" | Winners (rede butique) & Losers (franquia comoditizada) |
| 4 | conceitual | "Beauty Smile prova que dentista premium escala como rede butique — nao como franquia" | **Big Idea (U5) AQUI como Promised Land** |
| 5 | demo | "3 movimentos: protocolo evidencia + UX butique + ops scale-ready" | Magic Gift |
| 6 | dados | "Por que agora: mercado premium dental BR cresce 14% a/a + classe A buscando exclusividade" | Why Now tailwinds |
| 7 | dados | "Mercado BR: 12k clinicas premium × R$45k/mes × 8% capture = R$5,2bi TAM" | TAM bottom-up |
| 8 | financeiro | "Unit economics: LTV R$18k / CAC R$2,3k / payback 4 meses" | Business model |
| 9 | prova-social | "Tracao: R$180k/mes / NPS 91 / 247 pacientes ativos / 89% retention" | Evidence |
| 10 | dados | "Roadmap: 2a unidade Q4'26 + 3a unidade Q3'27 + breakeven Q1'28" | Financials |
| 11 | equipe | "Por que ESSE time: [CEO insight clinico] + [COO ops escalavel]" | Team com insight, nao currículo |
| 12 | CTA | "Ask: R$500k SAFE 8% post-money cap R$6,25M → 2a unidade SP em 6m" | **Tripartido: valor + uso + timeline** |
| 13 | disclaimer | "Forward-looking statements + CVM compliance" | Auto-disparo |

**Image prompts (whitelist D5):** capa + problema + conceitual + comparativo + demo + prova-social + equipe (7 slides) — invocar `deck-image-prompts` com tokens Beauty Smile design system.

**Compliance:**
- ✅ Disclaimer slide separado presente
- ✅ Ask tripartido (R$500k + uso "2a unidade" + timeline "6m")
- ✅ TAM bottom-up
- ✅ Big Idea no slide 4 (Promised Land), nao no titulo
- 🟡 Verificar: NDA assinado antes da reuniao? (skill alerta, nao bloqueia)
- 🟡 Verificar: footnote CFO/CFM no slide 9 (claim clinico "NPS 91" + dado retention)

### Asserts (auto-graders)

- STORYBOARD tem entre 12 e 14 slides (incluindo disclaimer)
- Slide 4 contem frase de Big Idea (U5) verbatim ou paraphrase com 70%+ overlap
- Slide CTA contem 3 partes: valor + uso + timeline (regex `R\$\d|SAFE|equity|cap` + `unidade|GTM|Produto` + `\d+\s*(m|mes|meses)`)
- Slide disclaimer presente com texto "forward-looking" ou "declaracoes prospectivas"
- 7 slides whitelist tem campo `**Prompt de imagem:**` preenchido (nao `—`)
- Slide 9 contem NPS, receita, retention (regex `NPS|retention|R\$\d.*mes`)
- Compliance tags `odontologia-br`, `cfo-cfm` aplicadas

---

## Case 2 — Carnaval 360 patrocinio master R$2M (modo `sponsorship`)

### Inputs

| Pergunta | Resposta |
|----------|----------|
| U1 | "Patrocinio master Carnaval 360 R$2M com contrapartida visibilidade + ativacao" |
| U2 | "Diretor de marketing marca de cerveja/bebida premium, decisao de R$5-10M anuais em patrocinio" |
| U3 | 15 min (escolha 3 — 15-20min) |
| U4 | Apresentacao em escritorio do patrocinador |
| U5 | "Carnaval 360 e o unico evento que entrega 80k cariocas classe A em 360 graus de imersao de marca, nao so logo na fachada" |
| U6 | Carnaval 360 (auto-detect) |
| F1 | patrocinio cultural (Rouanet aplicavel) |
| F2 | R$2M cota master (1 unica) |
| F3 | 80k pessoas/edicao, presenca midia (G1, Globo Rio, Veja Rio), 15 marcas patrocinadoras edicoes anteriores |
| F4 | (skip — patrocinio nao tem "concorrente direto") |
| F5 | "ROI nao mensuravel — como calcula retorno de patrocinio cultural?" |

### Output esperado

**Path:** `$DECKS_DIR/2026-05/STORYBOARD-carnaval-360-master-XXXX.md`

**Meta:**
- Modo: sponsorship
- Framework: Sequoia adaptado + Raskin Big Idea
- Marca: Carnaval 360
- Compliance tags: [] (cultural, sem Anvisa/CFO)

**Estrutura 10 + 4 slides:**

| # | Tipo | Action title esperado | Conteudo-chave |
|---|------|----------------------|----------------|
| 1 | capa | "Carnaval 360: imersao 360 graus em 80k cariocas classe A" | hook |
| 2 | problema | "Marca premium nao consegue entrar em ativacao de Carnaval real" | Big Change |
| 3 | comparativo | "Patrocinio fachada vs experiencia imersiva" | Winners (imersao) & Losers (logo) |
| 4 | conceitual | "Carnaval 360 e o unico evento que entrega 360 graus de imersao" | **Big Idea = visao do EVENTO** |
| 5 | demo | "Como funciona: 3 dias × 5 espacos × 80k pessoas tocadas" | Magic Gift |
| 6 | dados | "Why now: classe A retomando eventos presenciais pos-2024 + nova lei Rouanet 2025" | Tailwinds |
| 7 | prova-social | "Tracao: edicoes 2023-2025 com 80k+ pessoas / G1 / Globo Rio / 15 marcas" | Evidence |
| 8 | comparativo | "Niveis: Bronze R$200k / Silver R$500k / Gold R$1M / **Master R$2M**" | Substituicao de Business Model |
| 9 | conceitual | "Contrapartidas master: naming + ativacao 24h + branding 360 + ROI calculado" | Substituicao de Financials |
| 10 | dados | "ROI master: 8M impressoes / R$0,25 CPM equivalente / 12k experiencias diretas / earned media R$4M" | ROI patrocinador |
| 11 | CTA | "Investimento master R$2M / 60% via Lei Rouanet (R$1,2M dedutivel IRPJ) / signing 30 dias" | Ask **+ Rouanet aplicavel** |
| 12 | disclaimer | "PRONAC nº XXXXXX + forward-looking + nao oferta publica" | Auto-disparo |

**Image prompts (whitelist D5):** capa + problema + conceitual + comparativo + demo + prova-social (6 slides). Slide niveis (8) e comparativo entao prompt OK; slides 9-10 sao financeiro/dados → skip.

**Compliance:**
- ✅ Numero PRONAC mencionado (mesmo que placeholder)
- ✅ Lei 8.313/91 citada
- ✅ Mecanismo de deducao explicito (4% IRPJ pessoa juridica)
- ✅ Big Idea no slide 4
- ✅ Ask tripartido (R$2M + uso "Rouanet + ativacao" + timeline "signing 30 dias")
- 🟡 Verificar: ROI declarado 8M impressoes — fonte da metodologia?
- 🟡 Verificar: edicoes anteriores tem direito de imagem dos 15 patrocinadores citados?

### Asserts

- STORYBOARD tem entre 11 e 13 slides (10 padrao + 2-3 substituicoes + disclaimer)
- Meta contem `Modo: sponsorship`
- Slide com "Niveis" contem 4 tiers (bronze/silver/gold/master) + R$ values
- Slide ROI contem metodologia (impressoes / CPM / earned media)
- Slide CTA contem "Rouanet" ou "PRONAC" ou "8.313/91"
- Slide disclaimer contem "PRONAC" + "Lei" + "MinC"
- 6 slides whitelist tem campo `**Prompt de imagem:**` preenchido

---

## Case 3 — Fotona distribuidor exclusivo BR R$5M (modo `padrao` + compliance Anvisa)

### Inputs

| Pergunta | Resposta |
|----------|----------|
| U1 | "Captar US$1M (≈R$5M) de fundo de healthcare para tornar distribuidor exclusivo Fotona LightWalker no Brasil" |
| U2 | "Fundo de healthcare BR ou US (tier 1), com tese em medical devices LATAM, ticket US$1-3M" |
| U3 | 18 min (escolha 3 — 15-20min) |
| U4 | Pitch presencial ou call zoom (fundo decide) |
| U5 | "A janela competitiva BR pra dental laser de alta potencia esta abrindo agora — em 24 meses tera 3 distribuidores nacionais bloqueando entrada" |
| U6 | Fotona (auto-detect via regex `LightWalker` + `Er:YAG` + `Nd:YAG`) → carrega tag `anvisa-laser-classe-iii` |
| F1 | Series A |
| F2 | US$1M ≈ R$5M em equity (negociar % com fundo) |
| F3 | 12 unidades LightWalker instaladas BR ate hoje, pipeline 30 clinicas premium (Beauty Smile inclusiva), 4 anos relacionamento Fotona Eslovenia |
| F4 | Konig + LASERmed (distribuidores generalistas multi-marca); diferencial = exclusividade Fotona + capacitacao tecnica + suporte clinico |
| F5 | "Por que voces e nao a Fotona Brasil direta? Fotona poderia abrir filial." |

### Output esperado

**Path:** `$DECKS_DIR/2026-05/STORYBOARD-fotona-distribuidor-br-XXXX.md`

**Meta:**
- Modo: padrao
- Framework: Sequoia + Raskin
- Marca: Fotona
- Compliance tags: anvisa-laser-classe-iii, cfo-laser

**Estrutura 14 slides (Sequoia + 1 slide extra de compliance Anvisa):**

| # | Tipo | Action title esperado |
|---|------|----------------------|
| 1 | capa | "Distribuidor exclusivo Fotona LightWalker no Brasil" |
| 2 | problema | "Dentista premium BR nao consegue acesso a dental laser high-end" |
| 3 | comparativo | "Importacao individual vs distribuidor exclusivo capacitado" |
| 4 | conceitual | "A janela competitiva BR fecha em 24 meses — quem domina capacitacao tecnica trava o mercado" |
| 5 | demo | "Er:YAG + Nd:YAG dual-wavelength: cavidade sem broca + estetica" |
| 6 | dados | "Why now: mercado dental laser BR cresce 22% a/a + regulamentacao Anvisa estabilizada 2024" |
| 7 | dados | "Mercado: 8k clinicas premium BR × 6% adocao × US$80k ticket = US$38M TAM" |
| 8 | financeiro | "Unit economics: margem 35% / LTV US$120k / payback 8 meses" |
| 9 | prova-social | "Tracao: 12 unidades instaladas + 30 clinicas pipeline + 4 anos Fotona Eslovenia" |
| 10 | dados | "Compliance: Anvisa Resolucao RDC 185/2001 — laser Classe III + responsavel tecnico CRO" |
| 11 | dados | "Roadmap: 36 unidades em 24m + treinamento 200 dentistas + lab clinico parceria USP" |
| 12 | equipe | "Por que ESSE time: [CEO 4 anos Fotona] + [CTO laser PhD] + [Med Director CFO laser]" |
| 13 | CTA | "Ask: US$1M Series A / Produto 30% + GTM 50% + Compliance 20% / 24m ate breakeven" |
| 14 | disclaimer | "Forward-looking + Anvisa Classe III + nao oferta publica" |

**Image prompts (whitelist D5):** capa + problema + conceitual + comparativo + demo + prova-social + equipe (7 slides). Slide 10 (Anvisa) e tipo `dados` → skip default, mas e candidato a `--include-dados` se grafico do funil regulatorio for visual chave.

**Compliance:**
- ✅ Slide especifico Anvisa Classe III (slide 10)
- ✅ RDC 185/2001 citada
- ✅ Responsavel tecnico CRO mencionado
- ✅ Footnote Anvisa em slide 5 (demo do produto)
- ✅ TAM bottom-up
- ✅ Big Idea no slide 4
- ✅ Ask tripartido (US$1M + uso 3 buckets + 24m timeline)
- 🟡 Verificar: footnote CFO no slide 5 — usar laser dental requer responsavel tecnico CRO + cap horaria?
- 🟡 Verificar: relacao com Fotona Eslovenia tem contrato escrito de exclusividade? (F5 risk)

### Asserts

- STORYBOARD tem entre 13 e 15 slides
- Slide 10 contem "Anvisa" + "Classe III" + "RDC 185" ou similar regulatorio
- Slide demo (5) contem footnote ou disclaimer regulatorio
- Slide CTA contem 3 buckets de uso (Produto + GTM + Compliance) com %
- Slide 4 contem frase Big Idea (janela competitiva)
- Compliance tags `anvisa-laser-classe-iii` + `cfo-laser` aplicadas
- Slide disclaimer presente

---

## Como rodar os asserts

Asserts implementadas em [evals/evals.json](../evals/evals.json) como rubrica para grader semantic (`agents/grader.md` do skill-creator) + regex de presenca de termos-chave.

**Aproximacao de pass/fail:**
- 80%+ asserts passam → eval PASS
- 60-79% → eval PARTIAL (revisar 1 iteracao)
- <60% → eval FAIL (reescrever skill)
