# Template — Relatório Mensal de Marketing (Diretoria & CEO)

> **v1.1 (04/09/2026) — alinhado ao sistema construído no Notion.** Correções: (a) `Utilização do time` **não existe mais como número do banco** — o Time só guarda `Capacidade semanal`; a carga sai da view 👥 Carga por responsável (soma de `Pontos abertos` por pessoa) e a comparação com a capacidade é feita na hora de escrever o relatório; (b) **volume de entrega vai em contagem E em pontos, lado a lado** — nunca comparar pessoas de funções diferentes por pontos; (c) tarefas-mãe (contêiner) e **Canceladas** ficam fora de toda contagem, Arquivadas contam como entregues; (d) percentuais no Notion aparecem de **0 a 100**; (e) `% reativo` é medido **em pontos**, não em número de cards. Fonte técnica: `01-blueprint-notion/12-referencia-tecnica-construida.md`.
>
> **v1.2 (05/09/2026):** definições dos KPIs agora vêm de `kpis-e-metricas.md` **v2.0**, reconciliado com o `dicionario-kpis-fluxo.md`. Três mudanças que afetam este template: **Throughput** é contagem de itens (pontos entram como linha separada, nunca com esse nome) · o denominador do **% no prazo** é a `Data desejada` quando ela existir · **cycle time por percentil (SLE)** ainda não existe e não deve aparecer como média enquanto isso.
>
> **Formato:** 1 página principal (resumo + KPIs + destaques + riscos + próximos passos) e um **apêndice** com o detalhamento. Lidere pelo impacto no negócio. Preencha os campos entre `[ ]`.
>
> Para gerar automaticamente, use o **prompt 1** da `00-instrucoes/biblioteca-de-prompts.md`. O Claude pode entregar como `.docx`.

---

# Relatôrio de Marketing — [Mês/Ano]

**Responsável:** [nome] · **Período:** [01–30/mês] · **Distribuição:** Diretoria, CEO

---

## 1. Resumo executivo

> Um parágrafo. O que o marketing fez avançar no negócio neste mês? Foque em resultado, não em atividade.

[Ex.: "Em junho, marketing gerou 142 leads qualificados (+23% vs. maio) a um CPL 18% menor, impulsionados pela campanha de lançamento do LightWalker. Entregamos 92% dos projetos no prazo e publicamos 34 conteúdos. Principal risco: a área de Criação entrou no mês com mais pontos abertos do que sua capacidade das próximas duas semanas — recomendamos repriorizar ou reforçar pontualmente."]

---

## 2. KPIs do mês (vs. meta e vs. mês anterior)

> 5 a 9 indicadores. Use ▲/▼ para tendência.

| KPI | Mês atual | Mês anterior | Meta | Status |
|-----|-----------|--------------|------|--------|
| Leads qualificados | [ ] | [ ] | [ ] | 🟢/🟡/🔴 |
| CPL (R$) | [ ] | [ ] | [ ] | |
| Receita influenciada (R$) | [ ] | [ ] | [ ] | |
| ROI das campanhas | [ ] | [ ] | [ ] | |
| Projetos concluídos / no prazo | [ ] / [ ]% | [ ] | ≥85% | |
| Conteúdos publicados | [ ] | [ ] | [ ] | |
| Aderência ao calendário editorial | [ ]% | [ ]% | ≥90% | |
| **Trabalho reativo (% dos pontos abertos)** | [ ]% | [ ]% | ≤30% | |
| **Entregas no mês (contagem / pontos)** | [ ] / [ ] | [ ] / [ ] | — | |

---

## 3. Destaques do mês (wins) 🏆

> 3 a 5 marcos. Cada um com o impacto.

- [Destaque 1 — com número/impacto]
- [Destaque 2]
- [Destaque 3]

---

## 4. Riscos e bloqueios ⚠️

> O que pode comprometer os resultados e o que estamos fazendo a respeito.

| Risco/Bloqueio | Impacto | Ação / Decisão necessária | Dono |
|----------------|---------|---------------------------|------|
| [ex.: Criação a 110% de capacidade] | Atraso em lançamentos | Priorizar / reforço | [nome] |
| [ ] | [ ] | [ ] | [ ] |

---

## 5. Prioridades do próximo mês 🎯

> 3 a 5 focos, conectados às metas/OKRs.

1. [Prioridade 1]
2. [Prioridade 2]
3. [Prioridade 3]

---

---

# Apêndice (detalhamento)

## A. Entregas & Produtividade
- Projetos concluídos no mês: [lista]
- Projetos em andamento e % de progresso: [lista]
- Atrasos relevantes e causa: [ ]

## B. Resultados de Campanha
> Por campanha ativa no mês.

| Campanha | Investimento | Leads | CPL | Conversões | ROI |
|----------|--------------|-------|-----|------------|-----|
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

## C. Volume de Conteúdo
- Publicados por canal: [Instagram X · Blog Y · E-mail Z]
- Distribuição por pilar: [ ]
- Engajamento médio: [ ]
- Destaques de performance: [melhor conteúdo do mês]

## D. Capacidade do Time
> Fonte: view **👥 Carga por responsável** (soma de `Pontos abertos` por pessoa) × `Capacidade semanal` do banco 👥 Time. Se a pessoa não tem capacidade cadastrada, escrever "sem capacidade cadastrada" — não inventar 0%.

| Pessoa | Pontos abertos | Pontos atrasados | Capacidade semanal | Leitura |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | 🟢 folga / 🟡 no limite / 🔴 acima / ⚪ sem capacidade cadastrada |

- Observações sobre carga e necessidade de recursos: [ ]
- **Trabalho reativo por área** (view 🧭 Painel de áreas, coluna `% reativo`): [ ]

## E. Metas & OKRs — acompanhamento
| OKR | Métrica atual / alvo | Progresso (%) | Status |
|-----|---|-----------|--------|
| [ ] | [ ] / [ ] | [ ] | Não iniciado / No caminho / Em risco / Atingido / Não atingido |

---

> **Fontes dos dados:** Notion — views 🚦 Saúde (RAG), 📈 Resultados (Campanhas), 📣 Publicados, 👥 Carga por responsável, 🧭 Painel de áreas e o 🛰️ Painel Executivo de Portfólio (Projetos, Tarefas, Campanhas, Metas, Áreas, Time) · GoHighLevel (leads, oportunidades, stats sociais) · [outras]. Sinalizar qualquer número estimado.
