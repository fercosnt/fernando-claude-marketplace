# §10.2 STORYBOARD.md Schema (v1.1)

> Contrato LOCKED — schema único para todos os modos **EXCETO** `deck-scientific` poster (que usa `POSTER.md`, ver D8).
> Linter shell `scripts/lint-storyboard-schema.sh` valida outputs reais.

## O que mudou em v1.1 (em relação a v1.0)

1. **Bold nos rótulos** (`**Tipo:**` em vez de `Tipo:`) — facilita scan visual quando o STORYBOARD é lido por humano. Lint aceita ambos.
2. **Novo bloco `Conteúdo do slide (visível na projeção)`** — separa o que vai APARECER no slide do que o apresentador FALA (speaker notes). Densidade adaptada ao `modo_entrega` (apresentado-ao-vivo vs enviado-para-leitura).
3. **Novo bloco `Layout sugerido`** — handoff para designer / Gamma / Claude Design / PowerPoint com instruções concretas de grid + tipografia + componentes visuais.
4. **Bloco `Imagens sugeridas` reformatado** — quantidade explícita, cada variação em bloco visualmente separado (Aspect / Estilo / Composição / Prompt / Negative).
5. **Flag `[VERIFICAR]`** — todo dado fabricado ou citação não conferida DEVE ser marcado `[VERIFICAR: descrição]` para captura no review.
6. **Campo `Modo de entrega:`** no `## Meta` (derivado de U4 — ver `entrevista-universal-u1-u6.md`).

## Esqueleto canônico (v1.1)

```markdown
# Deck: {nome-deck}

## Meta
- **Skill geradora:** deck-{vertical}
- **Objetivo único:** {U1}
- **Audiência:** {U2}
- **Duração:** {U3} min
- **Formato:** {U4}
- **Modo de entrega:** apresentado-ao-vivo | enviado-para-leitura | hibrido  (NOVO v1.1 — derivado de U4)
- **Big Idea:** {U5}
- **Marca:** {U6}
- **Framework principal:** {ex: Sequoia + Andy Raskin}
- **Modo:** {se aplicável — ex: padrao | sponsorship | demo-day}
- **max_ctas:** {1 default; deck-teaching até 4; deck-scientific até 3 — D14}
- **Gerado em:** {ISO date}
- **Versão:** v1 | v2 | ...
- **Storyboard ID:** STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
{2-3 parágrafos sobre o arco narrativo escolhido. Por que esse framework, qual a transformação que o deck força no leitor.}

## Slide 1 — Capa

**Tipo:** capa
**Action title:** {headline assertivo de 5-9 palavras, NÃO título descritivo}
**Mensagem-chave:** {1 frase com a tese do slide}

**Conteúdo do slide (visível na projeção):**
- {Bullet 1 — ≤8 palavras, frase imperativa ou dado destacado}
- {Bullet 2}
- {Número grande ou quote curto se aplicável}

> Densidade do bloco varia com `modo_entrega`:
> - `apresentado-ao-vivo`: 2-3 bullets enxutos
> - `enviado-para-leitura`: 4-6 bullets + dados inline + 1 quote curto
> - `hibrido`: 3-4 bullets + dados-chave

**Layout sugerido (handoff designer/Gamma/Claude Design):**
- **Grid:** {split-60:40 texto-imagem | full-bleed imagem com overlay | center-stack | 3-card horizontal}
- **Tipografia:** H1 {cor brand} para Action title; H2 {cor secundária} para bullets; body cinza
- **Componentes:** {tabela 4 linhas | bar chart horizontal | 3 cards | 1 frase grande}
- **Animação:** {fade-in sequencial se modo=apresentado | estático se modo=enviado}

**Speaker notes:** {2-3 parágrafos — o que apresentador FALA, não o que está no slide}

> Speaker notes obrigatórios se `modo_entrega ∈ {apresentado-ao-vivo, hibrido}`. Opcionais ou curtos se `enviado-para-leitura` (texto autossuficiente substitui apresentador).

**Imagens sugeridas:**

> **Quantidade:** 1 imagem hero (3 variações para o designer escolher) | OU: N imagens distintas (uma para cada componente do slide)

**Variação A — Higgsfield**
- Aspect ratio: 16:9
- Estilo: cinematic editorial
- Composição: rule-of-thirds, subject 1/3 esquerda, espaço negativo direita
- Prompt: Interior of premium dental boutique clinic in Sao Paulo, soft natural light through large windows, turquoise and deep blue accents, minimalist modern furniture, single dentist consulting one patient in foreground, sense of calm and exclusivity, editorial quality
- Negative: stock-photo aesthetic, generic dental office, plastic skin, watermarks
- Referência mood (opcional): {link ou descrição}

**Variação B — Imagen 4**
- Aspect ratio: 16:9
- Estilo: editorial documental
- Composição: center, espaço negativo superior
- Prompt: ...
- Negative: ...

**Variação C — Nano Banana Pro** (opcional, quando há design system para acoplar)
- Aspect ratio: 16:9
- Estilo: mockup brand-aware
- Composição: full-bleed com overlay sutil
- Prompt: ...
- Negative: ...

> Em slides com tipo SKIP da whitelist (D5) — `dados | financeiro | CTA | disclaimer | agradecimento | apêndice` —, este bloco é substituído por `**Imagens sugeridas:** — (slide sem imagem hero por whitelist D5)`.

**Tempo estimado:** {seg} — (só relevante se `modo_entrega` inclui apresentado)
**Objeção esperada:** {se aplicável + resposta concreta}

## Slide 2..N — {Tipo}
(tipos canônicos: capa | problema | contexto | conceitual | dados | comparativo |
 prova-social | equipe | demo | financeiro | CTA | disclaimer | agradecimento | apêndice)

(mesma estrutura — Tipo / Action title / Mensagem-chave / Conteúdo do slide / Layout sugerido / Speaker notes / Imagens sugeridas / Tempo estimado / Objeção esperada)

## Apêndice (slides opcionais)
- A1 — {descrição backup material}
- ...

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide N — {tipo}: {brief curto pra image-prompts gerar variações}

## Checklist de Revisão (handoff pra deck-reviewer)
- [ ] Action titles em todos os slides (não títulos descritivos)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test (titles em sequência contam a história)
- [ ] Hook do slide 1 testado contra /copy
- [ ] CTA único (ou até max_ctas)
- [ ] Conteúdo do slide compatível com modo_entrega (denso se enviado / enxuto se apresentado)
- [ ] Layout sugerido preenchido em todos os slides (handoff designer)
- [ ] Dados/citações fabricados marcados com [VERIFICAR]
- [ ] {se clínico} Compliance CFO/CFM/Anvisa
- [ ] {se científico} Citações com GRADE
- [ ] {se vendas/captação} ROI/payback explícito

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {issues 🔴 — ex: Slide 7: TCLE pendente para antes/depois (CFO Res. 196/2019)}

🟡 Verificar antes:
- {issues 🟡 — ex: COI Fotona declarado verbalmente E em footnote escrita?}
- {issues 🟡 — ex: [VERIFICAR] todos os dados com flag verificados pelo usuário antes de apresentar}

✅ OK:
- {confirmações}
```

## Tipos de slide canônicos

| Tipo | Quando usar | Whitelist image-prompts (D5) |
|------|-------------|------------------------------|
| `capa` | Slide 1 sempre | ✅ Preencher prompt |
| `problema` | Articular dor | ✅ Preencher prompt |
| `contexto` | Background/setup | Skip |
| `conceitual` | Apresentar tese/framework | ✅ Preencher prompt |
| `dados` | Números, gráficos, charts | Skip *(override scientific: ✅)* |
| `comparativo` | A vs B, antes/depois | ✅ Preencher prompt |
| `prova-social` | Logos, depoimentos, cases | ✅ Preencher prompt |
| `equipe` | Founders, team slide | ✅ Preencher prompt |
| `demo` | Demonstração funcional | ✅ Preencher prompt |
| `financeiro` | Pricing, projeções, unit economics | Skip |
| `CTA` | Call to action / ask | Skip |
| `disclaimer` | Forward-looking, compliance | Skip |
| `agradecimento` | Slide final relacional | Skip |
| `apêndice` | Backup material | Skip |

## Regras invioláveis

1. **Action titles** (não títulos descritivos). Errado: "Mercado". Certo: "Mercado dobra a cada 18 meses."
2. **1 ideia por slide.** Múltiplas ideias = mais slides, não mais texto.
3. **Hook do slide 1** testado contra a Escala de Schwartz (consciência da audiência).
4. **CTA único** (ou até `max_ctas` declarado no `## Meta`).
5. **Bloco compliance 3 tiers sempre presente** (mesmo que ✅ OK seja "Nenhuma issue").
6. **Versão `## Meta` completa** — linter rejeita Meta truncada.
7. **NOVO v1.1 — Conteúdo do slide adaptado ao modo_entrega.** Slide minimalista em deck `enviado-para-leitura` vira pôster vazio. Slide denso em deck `apresentado-ao-vivo` compete com apresentador.
8. **NOVO v1.1 — Layout sugerido obrigatório.** Designer/Gamma/PowerPoint não recebe deck "no escuro" — cada slide especifica grid + tipografia + componentes.
9. **NOVO v1.1 — `[VERIFICAR]` em dados fabricados.** Todo número específico (R$X, N%, n=N, "RCT X 2024") sem fonte conferida marca `[VERIFICAR: descrição]`. Reviewer detecta e classifica como 🟡 obrigatório de resolver antes de apresentar.

## Como aplicar v1.1 a um STORYBOARD v1.0 existente

Migração simples:

1. Adicionar campo `Modo de entrega:` em Meta (derivar de Formato U4).
2. Para cada slide, adicionar bloco `Conteúdo do slide` (extrair os bullets que estão hoje implícitos na Mensagem-chave + parte do Speaker notes).
3. Para cada slide, adicionar bloco `Layout sugerido` (grid + tipografia + componentes).
4. Reformatar bloco `Prompt de imagem` em `Imagens sugeridas` com Quantidade explícita + variações em blocos separados (Aspect / Estilo / Composição / Prompt / Negative).
5. Auditoria de [VERIFICAR]: marcar todos os números específicos sem fonte conferida.
6. Bold nos rótulos (`Tipo:` → `**Tipo:**`).
7. Rodar `lint-storyboard-schema.sh` — DEVE passar.

## Cross-references

- `entrevista-universal-u1-u6.md` — origem dos campos `## Meta` + modo_entrega derivado de U4
- `output-convention.md` — onde o arquivo é salvo
- `../scripts/lint-storyboard-schema.sh` — validação automática (v1.1 aceita ambos formatos)
- `../skills/deck-image-prompts/SKILL.md` — gera o bloco `Imagens sugeridas`
- D8 (override): `deck-scientific` modo poster usa `POSTER.md`, não este schema
