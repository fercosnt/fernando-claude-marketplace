# STORYBOARD esqueleto — modo `strategic-partnership` (M&A / JV, 15-20 slides)

Esqueleto para parceria estrategica, M&A ou JV. Termos juridicos M&A em camada extra; CADE obrigatorio quando atinge criterios da Lei 12.529/2011.

---

# Deck: {nome-deal}

## Meta
- Skill geradora: deck-proposal (modo strategic-partnership)
- Objetivo unico: {U1}
- Audiencia: {U2 — geralmente board + C-level + IB advisors}
- Duracao: {U3} min
- Formato: {U4 — geralmente presencial board meeting ou data room PDF}
- Big Idea (Deal Thesis): {U5}
- Marca/parte: {U6}
- Framework principal: Pyramid Minto + Deal Thesis + Sinergias + Football Field + Term Sheet visual + DD Reverso
- Modo: strategic-partnership
- max_ctas: 1 (assinatura LOI)
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

M&A/JV deck e 60% numero, 40% narrativa. Storytelling minimo (BR enterprise: dados > pitch emocional). Slide 2 e Deal Thesis (versao BLUF da Pyramid) — Why this deal / Why now / Synergy headline / Timeline em 4 bullets. Slides 3-5 mapeiam contexto e target. Slide 6 e o mais importante apos thesis: sinergias com revenue (25-35% realization haircut), cost (65-85%), capability — sempre com e sem haircut, comites BR rejeitam numero sem realization rate. Slide 7 e football field valuation (4-5 metodologias horizontais — DCF, comparables, precedent transactions, asset, synergy-adjusted). Slide 8 e term sheet visual semaforo (6-8 termos materiais, NAO 20 do legal). Slide 10 e Due Diligence Reverso — diferenciador BR, target apresenta sua propria analise de risco antes de ser DD'd → acelera negociacao, reduz escrow exigido (de 10-12% pra 8-10%). Slide 13 e disclaimer CADE (literal, obrigatorio se R$750M+R$75M). Slide 15 fecha com timeline LOI → Exclusivity → DD → SPA → CADE → Closing.

Tom: factual + posicionamento estrategico. "Recomendamos LOI ate {data}" — equity de mesa.

---

## Slide 1 — Capa
Tipo: capa
Action title: Deal Proposal: {Acquirer/Parte A} + {Target/Parte B}
Mensagem-chave: Data + versao + confidencial
Speaker notes: Disclaimer "Strictly confidential — for discussion purposes only" no rodape. Razao social + CNPJ ambas partes.
Visual: capa institucional.
Prompt de imagem: (deck-image-prompts whitelist — capa)
Tempo estimado: 5s

## Slide 2 — Deal Thesis (BLUF M&A)
Tipo: conceitual
Action title: Recomendamos {tipo de deal} entre {Parte A} e {Parte B}, valor indicativo R$ {X}, fechamento Q{N}/{ano}
Mensagem-chave: 4 bullets — why this deal / why now / synergy headline / timeline
Speaker notes:
- **Why this deal:** {transformacao estrategica em 1 linha}
- **Why now:** {janela de mercado / regulatorio / competitivo}
- **Synergy headline:** R$ {Y}M NPV em {N} anos
- **Timeline indicativo:** LOI Q{N} → Closing Q{N+2}, sujeito a CADE
Visual: diagrama acquirer → target → combined entity.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 60s

## Slide 3 — Strategic Rationale (Why Now / Why Us / Why Them)
Tipo: conceitual
Action title: 3 condicoes alinhadas pela primeira vez
Mensagem-chave: Venn diagram — janela mercado + capacidades A + ativos B
Speaker notes: Why Now (janela mercado), Why Us (capacidades unicas Parte A), Why Them (ativos unicos Parte B). Interseccao = oportunidade.
Visual: Venn 3 circulos.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 4 — Market Context
Tipo: dados
Action title: TAM/SAM combinado {R$ Z}B; consolidacao em curso
Mensagem-chave: TAM/SAM + mapa competitivo pre/pos
Speaker notes: TAM/SAM combinado pos-deal. Mapa competitivo: onde a entidade combinada se posiciona (#N → #M).
Visual: chart TAM/SAM + grid competitivo.
Prompt de imagem: skip — dados fora da whitelist
Tempo estimado: 45s

## Slide 5 — Target Overview
Tipo: dados
Action title: {Target}: R$ {receita} 2025, {N} clientes, {key asset}
Mensagem-chave: Financials + produtos + clientes + geografia + key people
Speaker notes: Financials 3 anos (receita, EBITDA, margem). Top produtos/segmentos. Top clientes (% receita concentrada). Geografia. Key people (founders, C-level, lock-up ja negociado?).
Visual: dashboard 4-quadrantes.
Prompt de imagem: skip — dados
Tempo estimado: 50s

## Slide 6 — Sinergias (slide mais importante apos thesis)
Tipo: conceitual
Action title: NPV total R$ {Y}M, realization weighted R$ {Y_haircut}M
Mensagem-chave: Revenue + cost + capability, COM e SEM haircut
Speaker notes:
| Tipo | Bruto | Realization rate | Liquido | Prazo |
|------|------:|-----------------:|--------:|------:|
| Revenue (cross-sell, upsell) | R$ {a}M | 25-35% | R$ {a_liq}M | 18-36 meses |
| Cost (SG&A, TI, procurement) | R$ {b}M | 65-85% | R$ {b_liq}M | 6-18 meses |
| Capability (IP, talento, tech) | qualitativo | — | — | — |

**Comites BR rejeitam numero sem realization rate** (anti-padrao M&A 1: synergias magicas sem evidencia).

Visual: chart 3 categorias bruto vs liquido.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 70s

## Slide 7 — Football Field Valuation
Tipo: dados
Action title: Faixa indicativa R$ {min} — R$ {max}, midpoint R$ {mid}
Mensagem-chave: 4-5 metodologias horizontais
Speaker notes:
| Metodologia | Faixa | Premissa-chave |
|-------------|------:|----------------|
| DCF (3 cenarios) | R$ {a-b} | WACC {x}%, crescimento perpetuo {y}% |
| Comparable companies | R$ {c-d} | Multiplos peers {N}× EBITDA |
| Precedent transactions | R$ {e-f} | +20-40% control premium |
| Asset valuation | R$ {g-h} | NAV ajustado |
| Synergy-adjusted | R$ {i-j} | DCF + NPV sinergias liquidas |

Visual: football field bar chart horizontal.
Prompt de imagem: skip — dados
Tempo estimado: 60s

## Slide 8 — Term Sheet Summary (Visual Semaforo)
Tipo: comparativo
Action title: 6-8 termos materiais, nao os 20 do legal
Mensagem-chave: Tabela semaforo (verde = padrao mercado / amarelo = atencao / vermelho = nao-negociavel)
Speaker notes:
| Termo | Proposto | vs Mercado BR |
|-------|----------|:---:|
| Purchase Price | R$ {X} cash + R$ {Y} earn-out | 🟢 |
| Escrow | 10% / 18 meses | 🟢 (range 10-12% BR) |
| Cap indenizacao | 20% deal value | 🟢 (range 15-25% BR) |
| Basket | 1% deal value | 🟢 |
| Earn-out | {metrica}, {N} anos | 🟡 (precedente STJ REsp 2.117.094) |
| Non-compete key people | 3 anos | 🟢 (range 2-5) |
| Lock-up | 18 meses | 🟢 |
| Break-up fee | 3% | 🟢 |

Visual: tabela com semaforo.
Prompt de imagem: skip — comparativo de tabela
Tempo estimado: 60s

## Slide 9 — Deal Structure
Tipo: conceitual
Action title: Estrutura {asset deal / stock deal / merger / drop-down}
Mensagem-chave: Diagrama estrutura + fontes de funding
Speaker notes: Diagrama de estrutura. Funding: cash equity + divida + earn-out + stock. Tax treatment overview.
Visual: organograma pos-deal + bar chart funding.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 10 — Due Diligence Reverso (diferenciador BR)
Tipo: conceitual
Action title: Apresentamos nossa propria analise de risco antes da DD do comprador
Mensagem-chave: Transparencia acelera negociacao + reduz escrow exigido
Speaker notes:
- 4 categorias auto-mapeadas: comercial / operacional / regulatorio / cultural
- Cada risco: descricao + probabilidade + impacto + mitigacao ja em curso
- Beneficio: escrow exigido cai de 10-12% pra 8-10% (target sinaliza maturidade)

Anti-padrao M&A 5: omitir DD reverso = posicao fraca na mesa.

Visual: matriz 2×2 prob × impacto com riscos plotados.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 60s

## Slide 11 — Integration Plan 100-day + Year 1
Tipo: dados
Action title: 4 workstreams + quick wins primeiros 30 dias
Mensagem-chave: Gantt com swim lanes + ownership
Speaker notes:
- 100-day plan: integration office, Day-1 readiness, comunicacao stakeholders, sistemas criticos
- Year 1 plan: synergy capture milestones, cultural integration, talent retention
- Cada workstream tem owner nomeado.

Anti-padrao M&A 3: integration plan vago perde 30-40% do synergy target (McKinsey).

Visual: Gantt 12 meses com swim lanes.
Prompt de imagem: skip — dados
Tempo estimado: 50s

## Slide 12 — Risk Mitigation
Tipo: dados
Action title: Matriz probabilidade × impacto, 4 categorias
Mensagem-chave: Mercado / operacional / regulatorio / cultural
Speaker notes:
- Cultural fit (anti-padrao M&A 4): empresas com cultural diligence tem 50% mais chance de hit synergy targets (Bain).
- Listar riscos altos com mitigacao especifica.
Visual: matriz 2×2 com riscos + tabela mitigacao.
Prompt de imagem: skip — dados
Tempo estimado: 50s

## Slide 13 — Disclaimer CADE (OBRIGATORIO se R$750M + R$75M)
Tipo: disclaimer
Action title: Sujeito a aprovacao do CADE
Mensagem-chave: Criterios Lei 12.529/2011 + prazo 240+90 dias
Speaker notes:
> Esta proposta esta sujeita a aprovacao do Conselho Administrativo de Defesa Economica (CADE) caso atinja os criterios da Lei 12.529/2011 (faturamento bruto BR de R$ 750 milhoes para um grupo e R$ 75 milhoes para o outro).
>
> Prazo estimado de aprovacao: 240 a 330 dias corridos apos protocolo. O closing fica condicionado a obtencao desta aprovacao.

Se NAO atinge criterios: trocar pelo texto "Os criterios da Lei 12.529/2011 nao se aplicam a este caso (faturamentos abaixo dos thresholds). Notificacao ao CADE dispensada."

Visual: bloco de texto formal.
Prompt de imagem: skip — disclaimer
Tempo estimado: 30s

## Slide 14 — Governanca pos-deal
Tipo: conceitual
Action title: Board {N} cadeiras: {A:B}, decisoes super-majoritarias em {temas}
Mensagem-chave: Composicao board + decisoes reservadas + deadlock + exit
Speaker notes:
- Composicao board: {N} cadeiras, ratio {A}:{B}
- Decisoes ordinarias: maioria simples
- Decisoes reservadas (super-majoritarias 2/3 ou unanime): orcamento >R${X}, M&A, dividendos, alteracao estatutaria
- Deadlock resolution: mediacao → buy/sell → expert determination
- Exit: IPO trigger / drag-along / tag-along / put-call

Visual: diagrama governanca + tabela decisoes.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 50s

## Slide 15 — Timeline + Proximos Passos
Tipo: dados
Action title: Recomendamos assinatura LOI ate {data}
Mensagem-chave: LOI → Exclusivity → DD → SPA → CADE → Closing
Speaker notes:
| Marco | Data |
|-------|------|
| LOI assinada (exclusividade 60 dias) | {data} |
| DD inicio | {data} |
| DD conclusao | {data} |
| SPA assinada | {data} |
| Protocolo CADE | {data} |
| CADE decisao | {data} (240-330 dias) |
| Closing | {data} |

CTA unico: assinatura LOI via Clicksign.

Visual: timeline horizontal com marcos.
Prompt de imagem: skip — dados
Tempo estimado: 40s

## Slide 16 — Agradecimento + Contato
Tipo: agradecimento
Action title: Confidencial — proximos passos
Mensagem-chave: Lead advisor + email + telefone direto
Speaker notes: Contato direto do IB advisor / dealmaker. Disclaimer confidencialidade reiterado.
Visual: contato + logo.
Prompt de imagem: skip
Tempo estimado: 10s

## Apendice (slides opcionais)
- A: Modelo DCF completo (3 cenarios)
- B: Comparables detalhados (peer set)
- C: Sinergias bottom-up por workstream
- D: Risk register completo
- E: Lista de aprovacoes regulatorias

## Storyboard de Imagens (handoff)
- Slide 1 (capa)
- Slide 2 (conceitual): deal thesis diagram
- Slide 3 (conceitual): Venn diagram 3 condicoes
- Slide 6 (conceitual): sinergias visualizadas
- Slide 9 (conceitual): organograma pos-deal
- Slide 10 (conceitual): matriz risco DD reverso
- Slide 14 (conceitual): governanca

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Deal Thesis (BLUF) no slide 2
- [ ] Sinergias COM e SEM haircut (anti-padrao M&A 1)
- [ ] Football field 4-5 metodologias (anti-padrao M&A 2)
- [ ] Integration plan 100-day nomeado com owners (anti-padrao M&A 3)
- [ ] Cultural fit considerado (anti-padrao M&A 4)
- [ ] DD Reverso presente (anti-padrao M&A 5)
- [ ] Disclaimer CADE literal SE R$750M+R$75M
- [ ] Term sheet semaforo (6-8 termos materiais)
- [ ] Escrow 10-12% / Cap 15-25% (range BR)
- [ ] Non-compete 2-5 anos key people
- [ ] Timeline com CADE 240+90 dias
- [ ] Confidencialidade reiterada rodape

## Compliance & Disclaimers
🔴 Issues bloqueantes:
- {se atingiu criterios CADE e disclaimer ausente}

🟡 Verificar antes:
- {se aplicavel}

✅ OK:
- {confirmacoes}
