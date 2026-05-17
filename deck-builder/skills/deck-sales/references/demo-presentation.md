# Modo `demo-presentation` — Great Demo! + Gong Labs

> Modo especifico para demos guiadas de produto/servico apos discovery. 12-15 slides com Great Demo! framework. NAO substitui modo `padrao` — use APENAS quando contexto = demo apos discovery ja realizada.

## Quando ativar modo `demo-presentation`

Triggers (qualquer um):
- Input do usuario contem: "demo", "demonstracao do produto", "demo presencial", "mostrar o produto funcionando", "demo guiada", "POC apresentacao"
- S3 indica que ja houve discovery anterior ("ja conversamos com o decisor, agora e demo tecnica")
- Fase do funil = demo/eval (entre discovery e closing)

**NAO ativar quando:**
- Primeiro contato com o prospect (use `padrao` com Discovery deck encurtado)
- Closing/proposal (use `padrao` com Closing deck expandido)
- Demo de produto em deck publico/marketing (use `/copy` para social ou outro deck)

## Estrutura 12-15 slides (modo `demo-presentation`)

| # | Slide | Framework | Conteudo |
|---|-------|-----------|----------|
| 1 | Capa | — | Action title = Big Idea da demo |
| 2 | **Insight provocador** | Challenger | Mesmo padrao do modo `padrao` — NUNCA "obrigado pela reuniao" |
| 3 | Recap discovery | — | "Voce nos disse X, Y, Z — vamos endereçar nessa ordem" |
| 4 | Promised Land especifico | Raskin | Como e seu mundo se isso funcionar (1 slide) |
| 5 | **Output final do produto** | **Great Demo! "Do the Last Thing First"** | Mostre o resultado de MAIOR VALOR — nao o login |
| 6-9 | Peel back the layers | Great Demo! | Camadas reveladas APENAS se prospect demonstrar interesse |
| 10 | Casos de uso por persona | Solution Selling | 1 slide por persona-chave do buying committee |
| 11 | Prova social tecnica | — | Case com metricas, similar ao prospect |
| 12 | ROI / payback | Forrester TEI | Sensitivity 3 cenarios (vide roi-payback.md) |
| 13 | Implementacao | — | Timeline visual: semana 0 → mes 3 → mes 6 |
| 14 | Comparativo responsavel | April Dunford | SEM badmouth (vide comparativo-responsavel.md) — opcional |
| 15 | CTA tecnico | — | Pilot / POC / SOW preliminary — 1 unico CTA |

## Great Demo! (Peter Cohan) — princípios operacionais

### Principio 1 — Do the Last Thing First (slide 5)

Mostre o resultado mais valioso **nos primeiros 5 min** — nao no final. Prospect precisa ver relevancia imediata.

**Anti-padrao:** demo que segue UI do produto (login → dashboard → config → relatorios). Mostra produto na perspectiva do desenvolvedor.

**Padrao:** abra com output final (relatorio executivo consolidado, automacao concluida, dashboard de impacto). Depois "peel back the layers" sob demanda.

### Principio 2 — Peel Back the Layers (slides 6-9)

Apos mostrar resultado final, explique de TRAS PRA FRENTE. Cada camada revelada APENAS se prospect demonstrar interesse.

**Estrutura recomendada para slides 6-9:**
- Slide 6: "Como chegamos ao output do slide 5" — etapa final do fluxo
- Slide 7: etapa intermediaria mais critica
- Slide 8: integracoes/inputs (dados que entram)
- Slide 9: setup/onboarding (somente se prospect perguntar)

### Principio 3 — Illustration antes de Navigation

Mostre o VALOR antes de ensinar como usar. Use telas estaticas / mockups / video pre-gravado para slides 5-7. Demo ao vivo (interativa) so se contexto presencial permitir.

### 7 Validated Habits (Gong Labs 67k demos analisadas)

1. **Alinhe a demo com a discovery** — slide 3 do storyboard faz isso explicitamente
2. **Do the Last Thing First** — slide 5
3. **Limite o conteudo** — max 76s de pitch continuo (Gong)
4. **Use Situational Fluency** — vocabulario do setor do prospect (vendedor adapta on-the-fly)
5. **Mantenha dialogo constante** — talk:listen ratio 65:35, trocas de speaker +21% mais frequentes que demos perdedoras
6. **Prepare Vision Generation Demos** para executivos — slide 4 (Promised Land) cumpre
7. **Confirme proximos passos concretos ao final** — slide 15 CTA tecnico especifico

### Estatistica de demos vencedoras (Gong Labs base 67.149 demos)

| Metrica | Demo vencedora | Demo perdedora |
|---------|---------------|-----------------|
| Duracao | 47 min | 36 min |
| Talk:listen ratio | 65:35 | (mais monologo) |
| Pitch continuo max | 76s | longos monologos |
| Trocas speaker/min | +21% | menor |
| Tempo em pricing | 38-46 min do total | excesso → 8% mais que ideal |
| Tempo em proximos passos | +12.7% que demo perdedora | menor |

**Erro mais comum:** 8% mais tempo em pricing do que necessario.

## CAR Framework (Context-Action-Result) — para cada feature mostrada

Para cada feature demo (slides 5-9), aplicar internamente:

- **C — Context:** persona + cenario atual do prospect ("dentista premium SP, 12 implantes/mes")
- **A — Action:** o que o produto permite (fluxo demonstrado)
- **R — Result:** impacto (metrica, tempo salvo, receita gerada)

Para cada feature: resposta explicita ao "E DAI?" do prospect. Sem resposta clara ao "e dai?" = corte a feature do deck.

## SPICED Framework (Winning by Design) — qualificacao da demo

Garantir que o deck enderecou cada dimensao:

| Letra | Significado | Onde no deck |
|-------|-------------|---------------|
| S | Situation | Slide 3 (recap discovery) |
| P | Pain | Slide 2 (insight) + slide 4 implicito |
| I | Impact | Slide 4 (Promised Land) + slide 12 (ROI) |
| C | Critical Event | Slide 13 (timeline) — data/evento que cria urgencia |
| E | Decision | Slide 15 (CTA) — proximo passo do processo decisorio |
| D | Decision Maker | Slide 10 (casos por persona) — endereca cada stakeholder |

## Ferramentas de demo interativa (referencia — fora do escopo desta skill)

Caso o usuario peca ferramenta de demo interativa apos o deck:

| Plataforma | Posicionamento | Melhor para |
|------------|----------------|--------------|
| Navattic | Full-funnel | Escala de demo creation |
| Storylane | Early-stage rapido AI-native | Startups; CSAT 99/100 |
| Reprise | Enterprise + scripted | Enterprise deals complexos |
| Demodesk | Demo coaching | Times com coaching |
| Arcade | Videos + interactive | TOFU/website embedding |

**Tendencias 2025-2026:**
- Demos interativas geram **7.9x mais conversao** (24.35% vs 3.05%) — Walnut
- B2B buyers em jornada self-guided: **147% mais propensos a comprar** — Demostack
- 71% dos top-performing demos sao **ungated**
- 86% dos top-performers usam **web captures (HTML/CSS)**, NAO screenshots
- Anti-padrao: demo-as-slide-deck (prints estaticos)

Esta skill NAO escolhe / configura ferramenta. So gera STORYBOARD para a apresentacao.

## Anti-padroes demo-presentation (NAO fazer)

| # | Anti-padrao | Como corrigir |
|---|-------------|----------------|
| 1 | Demo que segue UI do produto (login → dashboard → config) | Do the Last Thing First — abra com output final |
| 2 | Feature-dump linear sem "e dai?" | CAR Framework para cada feature |
| 3 | Monologo > 76s contínuos | Dialogar; preparar perguntas-gancho a cada slide |
| 4 | Pricing demo cedo demais (antes do slide 12) | Pricing entre minutos 38-46 (slide 12-13) — Gong data |
| 5 | Sem confirmacao de proximos passos | Slide 15 CTA tecnico especifico com data |
| 6 | Demo igual para todos os perfis | Adaptar slide 10 (personas) ao buying committee real |

## Fontes

- Peter Cohan — [Great Demo! site oficial](https://greatdemo.com/7-validated-habits-for-stunningly-successful-demos/)
- Peter Cohan — *Great Demo!* (livro, Amazon)
- Gong Labs — [Sales Demo Tips com 67k demos](https://www.gong.io/blog/sales-demos)
- Gong — [Best Sales Insights 2025](https://www.gong.io/blog/the-best-sales-insights-of-2025)
- Walnut — Interactive Demo Statistics 2026
- Navattic — [Interactive Demo Best Practices 2026](https://www.navattic.com/blog/interactive-demos)
- Winning by Design — [SPICED Framework](https://winningbydesign.com/resources/blueprints/the-saas-sales-method/)
- Paul Smith — CAR Framework (Lead with a Story, 2012)
- Pesquisa local: `~/Cursor Repo/Pesquisas/pesquisas/skill-apresentacao/sales-decks-b2b-vendas-consultivas/PESQUISA-sales-decks-b2b-vendas-consultivas.md` Parte 4
