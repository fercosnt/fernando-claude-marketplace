# ROI / Payback obrigatorio — slides 12-13

> RNF compliance: TODO storyboard `deck-sales` precisa ter ROI/payback explicito. Sem isso, deck e bloqueado em 🔴 da seccao Compliance.

## Por que e obrigatorio

- **60-70% das decisoes B2B acima de ticket medio tem CFO participando** (Halifax Consulting)
- **85% dos B2B buyers esperam que vendors quantifiquem resultados** (Forrester 2025)
- Buying committee medio: **8,2 stakeholders** — todos precisam de justificativa interna
- ROI/TCO deixaram de ser diferenciais → sao **requisitos de entrada**
- Em healthcare/dental BR: dentista-proprietario concentra usuario+decisor+financeiro; objecao financeira critica
- **Nucleus Research:** "A opcao mais barata e sempre nao fazer nada" — slide ROI tem que vencer essa opcao

## Modelo canonico (slides 12-13)

### Slide 12 — Payback Period (metrica de abertura)

**Quando usar:** TODO deal acima de ticket medio. Metrica mais persuasiva para nao-financeiros. Nucleus Research recomenda como abertura.

**Formula:**

```
Payback (meses) = Investimento Total ÷ (Receita Adicional Mensal Liquida)
```

**Onde:** Receita Adicional Mensal Liquida = Receita bruta adicional mensal − Custos operacionais mensais incrementais.

**Estrutura do slide:**

```
SLIDE 12 — QUANDO VOCE RECUPERA O INVESTIMENTO

Action title: "Payback em {N} meses no cenario base."

[Barra de tempo — 0 a 36 meses]
          |----Break-even----|
  Mes 0    Mes 12            Mes 18         Mes 36
  Custo    Ponto de           Payback        Lucro
  Inicial  equilibrio         completo       acumulado

Inputs usados (transparencia metodologica):
  • Investimento inicial: R$ {X}
  • Receita adicional por sessao: R$ {Y}
  • Sessoes/mes conservadoras: {Z}
  • Custos operacionais mensais: R$ {W}
  • Payback resultante: {N} meses
```

**Benchmarks de payback aceitavel por categoria:**

| Categoria | Payback tipico | Payback otimizado |
|-----------|---------------|---------------------|
| SaaS B2B | 6-12 meses | < 6 meses |
| Plataformas enterprise | 12-24 meses | 9-12 meses |
| Equipamento medico/laser | 15-24 meses | 10-15 meses |
| Franchising premium | 18-30 meses | 12-18 meses |
| Plataforma corporativa de marca | 6-12 meses (ano fiscal) | 3-6 meses |

**Tatica de framing (Nucleus):** Prefira "voce recupera o investimento em 14 meses" a "ROI de 85%". Tempo e mais tangivel que percentual.

### Slide 13 — Sensitivity Analysis (3 cenarios)

**Quando usar:** SEMPRE que houver incerteza nas premissas. Constroi confianca via rigor metodologico (Forrester TEI).

**Formato canonico:**

```
SLIDE 13 — ANALISE DE SENSIBILIDADE — PAYBACK EM MESES

                       PESSIMISTA   BASE      OTIMISTA
─────────────────────────────────────────────────────
Sessoes/mes               8           12          18
Receita/sessao         R$ 2.000    R$ 2.500    R$ 3.000
Custo operacional      R$ 5.000    R$ 4.000    R$ 3.500
─────────────────────────────────────────────────────
Receita liquida/mes    R$ 11.000   R$ 26.000   R$ 50.500
Payback (meses)            27         12           6
ROI (3 anos)              45%         92%        168%
─────────────────────────────────────────────────────
[Barra:  6 ←── 12 ──→ 27 meses]
[Seta: mesmo no pior caso < 30 meses]
```

**Tatica:** destaque que MESMO NO PIOR CASO o investimento se paga em X meses — reduz percepcao de risco sem overpromise.

**Premissas que DEVEM aparecer:**
- Sessoes/mes (volume): base = projecao realista do prospect (validar com S3)
- Receita por sessao: base = mediana praticada na regiao
- Custo operacional: base = consumiveis + tempo da equipe + manutencao + amortizacao
- Taxa de desconto (se NPV): WACC ou custo de capital BR (8-15% a.a.)

## Modelos complementares (use conforme contexto)

### TCO (Total Cost of Ownership) — incluir como sub-slide 12b se houver concorrente

**Quando usar:** comparacao com concorrente ou com "nao fazer nada" (status quo).

**Componentes (diagrama iceberg):**

```
              CUSTOS VISIVEIS (ponta do iceberg)
              ─── Preco lista / Licenca / Equipamento
        ═══════════════════════════════════
              CUSTOS OCULTOS (abaixo da linha d'agua)
              Frete | Instalacao | Customizacao
              Change management | Integracao | Migracao
              Consumiveis | Calibracao | Energia
              Treinamento | Curva de aprendizado
              Manutencao | Downtime | Pecas
              Compliance | Multas | Seguro
              Descontinuacao | Atualizacao | Descarte
```

**Limitacao critica (Nucleus):** "A opcao mais barata e sempre nao fazer nada." Use TCO para contextualizar, NAO como argumento principal de valor.

### NPV (Net Present Value) — incluir como sub-slide 13b se enterprise

**Quando usar:** deals enterprise, CFO tecnico, multiplos projetos competindo pelo mesmo budget.

**Formula:**

```
NPV = Σ [Fluxo de Caixa_t / (1 + Taxa Desconto)^t] − Investimento Inicial

Taxa Desconto = WACC ou custo de capital (tipicamente 8-15% BR)
```

**Slide recomendado:** waterfall chart por ano, linha base do investimento (negativo), barras crescentes (fluxo descontado), linha horizontal de break-even.

**Cuidado (Nucleus):** NPV problematico para tecnologia de beneficios continuos. Evite IRR — "facilmente manipulavel".

### Forrester TEI — referencia para enterprise

| Componente | Mede | Aplicacao em deck |
|------------|------|-------------------|
| Cost | Gastos com tecnologia | Slide TCO |
| Benefits | Ganhos mensuraveis | Slide ROI/payback |
| Flexibility | Valor de opcoes futuras | Slide visao longo prazo |
| Risk | Incerteza e ajuste | Slide sensitivity |

Use a estrutura como esqueleto do business case mesmo sem contratar Forrester.

## Exemplos calculados por caso (template pronto)

### Caso Fotona LightWalker / dentista premium SP

**Inputs Fernando (case 1):**
- Investimento: R$ 280.000 (LightWalker mid-tier + instalacao + treinamento)
- Sessoes/mes (3 cenarios): 8 / 12 / 18
- Receita/sessao: R$ 1.500 / R$ 2.000 / R$ 2.500
- Custo operacional/mes: R$ 5.000 / R$ 4.000 / R$ 3.500

**Calculo:**

| Cenario | Receita Bruta | Receita Liquida | Payback |
|---------|---------------|------------------|---------|
| Pessimista | R$ 12.000 | R$ 7.000 | 40 meses |
| Base | R$ 24.000 | R$ 20.000 | **14 meses** |
| Otimista | R$ 45.000 | R$ 41.500 | 7 meses |

**Headline do slide 12:** "Payback de 14 meses no cenario base — alinhado com benchmark Fotona ROI Calculator."

### Caso Beauty Smile franchising

**Inputs:**
- Investimento: R$ 150.000 entrada + R$ 30.000 fit-out medio inicial
- Receita liquida media franquia consolidada: R$ 28.000-45.000/mes (validar com S5)
- Royalty fee (NAO entra no payback do franqueado, e cost-of-revenue): X%

**Calculo (cenario base):**

| Cenario | Receita liquida/mes | Payback |
|---------|---------------------|---------|
| Pessimista | R$ 18.000 | 10 meses |
| Base | R$ 30.000 | **6 meses** |
| Otimista | R$ 45.000 | 4 meses |

**Headline:** "Payback de 6 meses no cenario base — abaixo de qualquer franquia consolidada SP categoria premium."

### Caso Carnaval 360 corporativo

**Inputs:**
- Investimento: R$ 500.000/ano (plano corporativo multi-cliente para agencia)
- Receita gerada por cliente da agencia que ativa plataforma: R$ 80-200k margem por cliente
- Cenario: agencia roda 6 clientes/ano na plataforma

**Calculo:**

| Cenario | Clientes/ano | Margem media | Receita anual | Payback |
|---------|--------------|--------------|---------------|---------|
| Pessimista | 4 clientes | R$ 80k | R$ 320k | NAO atinge ano 1 (extender pra 18m) |
| Base | 6 clientes | R$ 120k | R$ 720k | **8 meses** |
| Otimista | 9 clientes | R$ 180k | R$ 1.620k | 4 meses |

**Headline:** "Payback de 8 meses no cenario base — quebra de 1.44x do investimento ja no ano 1."

## Anti-padroes ROI (NAO fazer)

| # | Anti-padrao | Por que ruim | Como corrigir |
|---|-------------|--------------|---------------|
| 1 | ROI sem inputs visiveis ("300% em 12 meses!") | CFO descarta sem transparencia metodologica | Mostrar inputs (sessoes, receita, custo) e fontes |
| 2 | So cenario otimista | Vira "marketing pitch" | Sempre 3 cenarios (pess/base/otim) |
| 3 | Promessa absoluta ("garantimos payback de X meses") | Risco juridico + perda de credibilidade | "Em cenarios similares observamos", "tipicamente" |
| 4 | NPV/IRR para ticket pequeno (< R$100k) | Complexidade desnecessaria | Payback simples + sensitivity basta |
| 5 | Comparar payback com concorrente sem fonte publica | Risco juridico (concorrencia desleal) + dado nao-confiavel | So usar dados do PROPRIO prospect |
| 6 | Esquecer custo operacional | Payback artificialmente curto, CFO detecta na hora | Sempre Receita LIQUIDA, nao bruta |
| 7 | Taxa de desconto omitida em NPV | Premissas opacas = business case rejeitado | Declarar WACC/custo de capital usado |

## Checklist final ROI (autoaplicar antes de fechar deck)

- [ ] Slide 12 contem Payback em meses + estrutura linha do tempo
- [ ] Slide 13 contem Sensitivity 3 cenarios (Pessimista / Base / Otimista)
- [ ] Inputs visiveis: sessoes/mes + receita/sessao + custo operacional/mes
- [ ] Receita usada e LIQUIDA (descontados custos operacionais incrementais)
- [ ] Premissas conservadoras nao otimistas (base ≠ otimista)
- [ ] Headline = Payback no cenario BASE (nao otimista)
- [ ] Sem absolutos ("garantimos", "asseguramos") — usar "tipicamente", "em cenarios similares"
- [ ] Sem comparativo de payback de concorrente sem fonte publicada
- [ ] Speaker notes anotam que vendedor pode reabrir Sensitivity ao vivo se cliente questionar premissa
- [ ] Se NPV usado: taxa de desconto declarada explicitamente

## Fontes

- Nucleus Research — [ROI, TCO, NPV, Payback Complete Guide](https://nucleusresearch.com/everything-to-know-about-roi-tco-npv-and-payback/)
- Forrester TEI — [methodology](https://www.forrester.com/policies/tei/)
- Halifax Consulting — pesquisa CFO involvement 2025
- Fotona — [ROI Calculator oficial](https://www.fotona.com/en/dentistry/) (referencia setor laser dental)
- ServiceNow — [Value Calculator](https://www.servicenow.com/success/value-calculator-impact.html) (modelo de business case publico)
- The Laser Agent — [Aesthetic Laser ROI Breakdown](https://www.thelaseragent.com/aesthetic-laser-roi-breakdown-how-fast-can-a-used-laser-pay-for-itself/)
- Pesquisa local: `~/Cursor Repo/Pesquisas/pesquisas/skill-apresentacao/sales-decks-b2b-vendas-consultivas/PESQUISA-sales-decks-b2b-vendas-consultivas.md` Parte 5
