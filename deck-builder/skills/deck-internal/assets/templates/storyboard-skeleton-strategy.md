# Skeleton STORYBOARD — Modo `strategy-presentation`

Aplica Pyramid Minto + SCR (Situation → Complication → Resolution) + 3 Horizontes McKinsey.

---

```markdown
# Deck: {slug}

## Meta
- Skill geradora: deck-internal
- Objetivo unico: {U1}
- Audiencia: {U2 — VP/C-level + gerentes/leads, 10-30 pessoas}
- Duracao: {U3} min (tipicamente 45-90)
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Pyramid Minto + SCR + 3 Horizontes McKinsey
- Modo: strategy-presentation
- max_ctas: 1
- Anexo 6-pager: opcional
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

SCR macro + 3 Horizontes McKinsey como cascata do "R" (Resolution).
SCR direction definida pela audiencia: resistente → S→C→R; alinhada → R→S→C.
Regra 70/20/10 de alocacao (H1/H2/H3).
Sequencia recomendada de horizontes: H1 → H3 → H2 (familiar → visao → ponte).

## Slide 1 — Capa + Headline estrategica
Tipo: capa
Action title: {a aposta central em 1 frase}
Mensagem-chave: {situar tema + agradecer presenca + sinalizar arco}
Speaker notes: 30s
Visual: brand-safe
Prompt de imagem: {preencher — whitelist D5}
Tempo estimado: 30s

## Slide 2 — Executive summary (Pyramid top)
Tipo: conceitual
Action title: {recomendacao + 3 pilares em 1 frase}
Mensagem-chave: "Recomendamos {estrategia} com 3 pilares: {H1}, {H2}, {H3}"
Speaker notes: 2min — top da piramide; depois descer com cascata
Visual: piramide visual ou diagrama 3 pilares
Prompt de imagem: {preencher}
Tempo estimado: 2min

## Slide 3 — Situation (SCR S)
Tipo: contexto
Action title: {onde estamos hoje}
Mensagem-chave: contexto compartilhado incontestavel
Speaker notes: 3-5min — fatos sobre o core (H1 atual)
Visual: dados de baseline
Prompt de imagem: {preencher OU skip se tipo dados — D5 default skip; override usuario}
Tempo estimado: 3-5min

## Slide 4 — Complication (SCR C)
Tipo: problema
Action title: {o que muda/ameaca em 1 frase}
Mensagem-chave: gap estrategico + custo de inacao
Speaker notes: 3-5min — nomear a Grande Mudanca (Raskin) + perdedores
Visual: ameaca quantificada
Prompt de imagem: {preencher — whitelist D5}
Tempo estimado: 3-5min

## Slide 5 — Resolution (SCR R) + visao macro
Tipo: conceitual
Action title: {estrategia proposta em 1 frase}
Mensagem-chave: Terra Prometida (Raskin) — visao 36 meses
Speaker notes: 2min — visao macro antes de descer para pilares
Visual: visao
Prompt de imagem: {preencher}
Tempo estimado: 2min

## Slide 6 — Pilar 1: H1 (core — defender e expandir)
Tipo: conceitual
Action title: {como defendemos e expandimos o core}
Mensagem-chave: 3 iniciativas H1 + KPIs
Speaker notes: 5-7min — 70% do budget vai aqui
Visual: roadmap H1
Prompt de imagem: {preencher}
Tempo estimado: 5-7min

## Slide 7 — Pilar 3: H3 (futuro — semear opcoes)
Tipo: conceitual
Action title: {o que estamos semeando}
Mensagem-chave: 2-3 apostas exploratorias + criterio de promocao
Speaker notes: 3-5min — 10% budget; sequencia H1→H3 (salto)
Visual: opcoes H3
Prompt de imagem: {preencher}
Tempo estimado: 3-5min

## Slide 8 — Pilar 2: H2 (emergente — ponte H1→H3)
Tipo: conceitual
Action title: {quais oportunidades cultivamos}
Mensagem-chave: 3 iniciativas H2 com tracao + KPIs + criterio de promocao para H1
Speaker notes: 5-7min — 20% budget; H2 conecta familiar e futuro
Visual: ponte H1→H2→H3
Prompt de imagem: {preencher}
Tempo estimado: 5-7min

## Slide 9 — Roadmap visual (12-36 meses)
Tipo: dados
Action title: {sequenciamento em 1 frase}
Mensagem-chave: timeline com marcos por horizonte
Speaker notes: 5min — dependencias criticas + paralelismo
Visual: gantt simplificado
Prompt de imagem: — (skip — tipo dados D5 default)
Tempo estimado: 5min

## Slide 10 — Alocacao de recursos (70/20/10)
Tipo: financeiro
Action title: {alocacao 70/20/10 ou justificativa de desvio}
Mensagem-chave: orcamento total + split por horizonte
Speaker notes: 3min
Visual: pizza ou stacked bar
Prompt de imagem: — (skip — tipo financeiro)
Tempo estimado: 3min

## Slide 11 — KPIs por horizonte
Tipo: dados
Action title: {como medimos avanco}
Mensagem-chave: 2-3 KPIs por horizonte + meta + sponsor
Speaker notes: 3min
Visual: tabela
Prompt de imagem: — (skip — tipo dados)
Tempo estimado: 3min

## Slide 12 — Riscos e dependencias criticas
Tipo: comparativo
Action title: {top 3-5 riscos com mitigacao}
Mensagem-chave: riscos + probabilidade + impacto + mitigacao
Speaker notes: 3min
Visual: matriz risco
Prompt de imagem: {preencher — whitelist D5}
Tempo estimado: 3min

## Slide 13 — Proximos passos + owners
Tipo: CTA
Action title: {primeiros 90 dias}
Mensagem-chave: 5-7 marcos + owner + data
Speaker notes: 2min
Visual: tabela
Prompt de imagem: — (skip — tipo CTA)
Tempo estimado: 2min

## Apendice (opcional, mas recomendado)
- A1 — Premissas e cenarios
- A2 — Decisoes ja tomadas vs em aberto
- A3 — Riscos detalhados (top 10)
- A4 — Benchmark/comparativos

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1 (capa), 4 (problema), 5 (Terra Prometida), 6/7/8 (pilares), 12 (riscos)
- Skip: slides 9, 10, 11, 13 (tipos dados/financeiro/CTA)

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] SCR estrutural correto (S=3, C=4, R=5)
- [ ] 3 Horizontes presentes (H1=6, H3=7, H2=8 — sequencia recomendada)
- [ ] Alocacao 70/20/10 explicita slide 10 ou justificativa de desvio
- [ ] KPIs por horizonte (NAO unico KPI agregado)
- [ ] Action titles em todos os slides
- [ ] Riscos top 3-5 com mitigacao
- [ ] Roadmap visual com dependencias
- [ ] CTA unico no slide 13 (max_ctas: 1)
- [ ] Direction SCR alinhado com audiencia (resistente vs alinhada)

## Compliance & Disclaimers
{aplicar 3 tiers conforme contexto}
```
