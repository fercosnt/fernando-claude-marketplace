# Proposal Checklist — DoD final antes de entregar STORYBOARD

Checklist auditor da skill `deck-proposal`. Cada item produz veredito 🔴/🟡/✅ no bloco "Compliance & Disclaimers" do STORYBOARD.

## Pyramid + Estrutura (universal — todos os modos)

- [ ] **BLUF no slide 2.** Recomendacao em 1 frase + 3 razoes-suporte. Sem isso → 🔴 bloqueia.
- [ ] **Action titles sao conclusao,** nao tema. ("Voce perde R$ 2M/ano por X" > "Analise de X")
- [ ] **1 ideia por slide.** Slide com >1 conclusao independente → 🟡 flag.
- [ ] **Exec summary ≤250 palavras** (Proposify 2024: >250 perde 32% win rate).
- [ ] **C-level pode ler so os primeiros 7 slides** e entender a recomendacao. Apendice fora do fluxo principal.

## SCQA (todos os modos)

- [ ] **Slide 3 tem dado proprio do cliente** (citado em discovery). Sem dado proprio → 🟡 flag "voltar ao discovery".
- [ ] **Slide 4 tem custo-do-nao-agir quantificado** em R$ ou %.
- [ ] **Slide 5 conecta Resolution ao BLUF** do slide 2.

## ROI 3-tier (modos `commercial` + `retainer`)

- [ ] **3 tiers presentes** (Essencial / Profissional / Enterprise). 1 tier so → 🔴 bloqueia.
- [ ] **Nomes BR enterprise** (NAO "bom/melhor/melhor ainda"). Nomes errados → 🟡 flag tonal.
- [ ] **Tier Profissional destacado visualmente** como recomendado.
- [ ] **Tier Enterprise existe pra ancorar** (pode nao ser realista). Ausencia → 🔴 (perde efeito de ancoragem).
- [ ] **Formato monetario BR:** R$ X.XXX,XX (ponto milhar, virgula decimal). Por extenso em formal.
- [ ] **Forma de pagamento BR oferecida** (a vista com desconto + parcelado + boleto por fase).

## Escopo (todos os modos)

- [ ] **3 colunas In / Out / Flexible.** Coluna "Out" ausente → 🔴 bloqueia (anti-padrao 2, 43% scope creep).

## Cronograma (todos os modos)

- [ ] **Premissas e dependencias do cliente explicitas** (anti-padrao 5). Aprovacoes, dados, acessos.
- [ ] **Datas absolutas,** nao relativas ("inicio 15/06/2026" > "inicio em meados de junho").

## CTA (todos os modos)

- [ ] **CTA com 3 acoes datadas + dono** (anti-padrao 6).
- [ ] **NAO** "aguardamos retorno", "fica a criterio", "qualquer coisa estamos a disposicao".
- [ ] **Frase-ancora:** "Os proximos passos sao..." ou "Decisao recomendada ate {data}."

## Tom Win Without Pitching (universal)

- [ ] **Grep de frases banidas** retorna vazio:
  ```
  gostariamos de | se possivel | humildemente | aguardamos retorno
  fica a criterio | qualquer coisa estamos a disposicao
  acreditamos ser uma boa opcao | caso aprovado | se for do interesse
  estimamos aproximadamente | a combinar | a definir | em torno de | mais ou menos
  ```
- [ ] **Termos definitivos:** datas, valores, condicoes fechadas (nao "vamos ver").
- [ ] **Preco em valor entregue,** nao em horas.
- [ ] **Posicionamento expert:** "ja diagnosticamos N clinicas similares" > "somos os melhores".

## Bloco juridico BR — modo `retainer` (obrigatorio)

- [ ] **IPCA reajuste anual** (NUNCA IGP-M).
- [ ] **Foro com pertinencia** Lei 14.879/2024 (default SP capital).
- [ ] **Multa moratoria 2%/mes** com **cap 20%** (STJ). Multa >20% → 🔴 bloqueia.
- [ ] **Multa compensatoria rescisao antecipada:** 3 meses fee (default).
- [ ] **Notice period 30-90 dias** (default 60).
- [ ] **LGPD presente:** controlador vs operador + finalidade + retencao + destruicao.
- [ ] **SLA matriz P1/P2/P3** com response + resolution + penalty + targets 99/95/90%.

## CADE — modo `strategic-partnership` (obrigatorio quando aplicavel)

- [ ] **Disclaimer CADE literal** se faturamentos atingem **R$ 750M + R$ 75M** (Lei 12.529/2011).
- [ ] **Prazo 240+90 dias** mencionado na timeline.
- [ ] **Se nao atinge criterios** → mencionar isso explicitamente ("Lei 12.529/2011 nao se aplica").
- [ ] Sem disclaimer quando atinge → 🔴 bloqueia.

## M&A / strategic-partnership — outros

- [ ] **Deal Thesis no slide 2** (BLUF M&A) — why this deal / why now / synergy headline / timeline.
- [ ] **Sinergias COM e SEM haircut** (revenue 25-35% realization, cost 65-85%, capability qualitativo). Sem haircut → 🔴 (anti-padrao M&A 1).
- [ ] **Football field 4-5 metodologias** horizontais (DCF + comparables + precedent + asset + synergy-adjusted).
- [ ] **Term sheet visual semaforo** (6-8 termos materiais, NAO 20 do legal).
- [ ] **DD Reverso presente** (anti-padrao M&A 5).
- [ ] **Cultural fit considerado** (anti-padrao M&A 4 — Bain: 50% mais chance de hit synergy).
- [ ] **Integration plan 100-day + Year 1** com owners nomeados (anti-padrao M&A 3).
- [ ] **Escrow 10-12% / Cap 15-25%** (range BR).
- [ ] **Non-compete key people 2-5 anos.**

## Compliance setorial (heredado do bundle)

- [ ] **Beauty Smile / saude:** CFO 196/2019 (sem promessa de cura, antes/depois com TCLE) + LGPD sensivel.
- [ ] **Fotona / laser:** Anvisa Classe III + sem comparativo head-to-head sem evidencia + disclaimer "resultados podem variar".
- [ ] **Carnaval 360 / eventos:** ECAD + Lei Geral do Esporte se aplicavel + ECA se publico infantojuvenil.

## Output STORYBOARD (schema §10.2 SHARED.md)

- [ ] Cabecalho `## Meta` completo com 13 campos.
- [ ] Slides numerados sequencialmente com tipo canonico.
- [ ] Cada slide tem: tipo + action title + mensagem-chave + speaker notes + visual + prompt de imagem + tempo estimado.
- [ ] Bloco `## Storyboard de Imagens` (handoff `deck-image-prompts`) presente.
- [ ] Bloco `## Checklist de Revisao` (handoff `deck-reviewer`) presente.
- [ ] Bloco `## Compliance & Disclaimers` (3 tiers 🔴 🟡 ✅) presente.

## Pos-skill (proximos passos)

- [ ] **Encadear `deck-image-prompts`** para slides whitelist (capa/problema/conceitual/comparativo/demo/prova-social).
- [ ] **Sugerir `deck-reviewer`** se ticket > R$ 100k ou modo `strategic-partnership`.
- [ ] **Salvar em `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`** v1.

## DoD da skill (alinhado ao bundle 08)

- [ ] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1 + NB3
- [ ] 3 eval cases passando ([../../references/eval-cases-proposal.md](../../references/eval-cases-proposal.md))
- [ ] 3 modos implementados (commercial / strategic-partnership / retainer)
- [ ] BLUF no slide 2 garantido (Pyramid Minto)
- [ ] 3-tier garantido em commercial + retainer
- [ ] Termos juridicos BR garantidos em retainer
- [ ] CADE garantido em strategic-partnership quando aplicavel
- [ ] Win Without Pitching tom (posicionamento expert)
- [ ] Schema §10.2 valido
- [ ] Instalada em Claude Code + Cowork Desktop
