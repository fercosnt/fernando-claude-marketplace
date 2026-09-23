# Definição dos KPIs do relatório (resumo de `kpis-e-metricas.md` v2.0)

Quase todo erro deste relatório é de **definição**, não de conta. Este arquivo é a definição.

## Definition of Workflow — sem isto nenhuma métrica de fluxo existe

- **Started** = a tarefa entra em `Em produção`. **Finished** = entra em `Concluída`.
- **Cancelada sai de tudo. Arquivada conta como entregue.**
- A unidade de contagem é a **fase** (sub-item). A tarefa-mãe de conteúdo é contêiner: aparece no
  calendário, não nas contagens.
- Item **bloqueado conta** no trabalho em andamento. Isentá-lo esconde exatamente o problema que
  se quer enxergar.
- Cycle time é tempo **decorrido**, não tempo trabalhado: card parado 6 dias esperando aprovação
  são 6 dias.

## Entregas & Produtividade

| KPI | Definição exata | Armadilha |
|---|---|---|
| **Throughput** | Contagem exata de tarefas concluídas no mês | Não é pontos. Nunca chame pontos de throughput |
| **Pontos concluídos** | Soma de `Pontos` (P=1 · M=3 · G=8) das concluídas | Métrica interna de capacidade. Publique **sempre ao lado** da contagem |
| **% de entregas no prazo** | Concluídas dentro do prazo ÷ concluídas. Denominador = `Data desejada` quando existir; `Prazo` só quando a tarefa nasceu interna | Usar só `Prazo` premia quem renegocia a data |
| **Work Item Age** | `Idade em produção (dias)` da tarefa aberta; no projeto, `Maior idade em produção` | É a única métrica sobre a qual dá para agir hoje. As outras são retrospectivas |
| **Cycle time (p85)** | ⏳ **Não existe ainda.** Depende de ~2 meses de histórico no 📜 Log de Status | Enquanto isso, **não reporte média** — média esconde a cauda |
| **Atrasadas no fim do mês** | Abertas com prazo vencido | Excluir contêineres e Canceladas |
| **Aprovação sem × com refação** | Das concluídas no mês que **passaram por aprovação** (`Entrou em aprovação em` preenchido, ≥ 21/09/2026): quantas com `Refações` vazio ou 0 (**sem refação**) e quantas com ≥ 1 (**com refação**), mais a distribuição 1 · 2 · 3+ voltas. Publique a contagem dos dois lados e o % sem refação | (1) Tarefa que nunca foi para aprovação **não** entra no denominador. (2) Antes de 21/09 é "sem dado". (3) Sem motivo, o número mistura ajuste clínico/jurídico com erro — leia por tipo de entrega/empresa, **nunca por pessoa**, e não chame de "retrabalho" |

## Resultados de Campanha

CPL = investimento ÷ leads · ROI = (receita − investimento) ÷ investimento.
**Receita influenciada** tem regra fechada: oportunidades **ganhas** no GHL cujo contato nasceu de
origem de MKT (first-touch: form, campanha, evento), fechadas em até **90 dias** após o lead.
Nunca estimativa manual.

## Volume de Conteúdo

Publicado = tem `Link do post` (a fórmula `Publicado?` lê o link, não o status).
Aderência ao calendário = `Publicado em ≤ Data planejada` ÷ planejadas no mês.

## Capacidade do Time

**Reporte no nível do time e da área, nunca por pessoa.** A visão individual existe na view
👥 Carga por responsável e é ferramenta do coordenador.

- **Carga da semana:** pontos com prazo nos próximos 7 dias contra a capacidade semanal.
  **Sem meta percentual** — não há taxa de utilização defensável para time in-house, e utilização
  alta com demanda variável piora o cycle time.
- **% reativo (taxa de ad-hoc):** pontos de `Tipo de trabalho` Ad-hoc/Fire-drill ÷ pontos totais.
  Classificado **na entrada**, nunca depois. É o número politicamente mais valioso do relatório.
- Pessoa sem `Capacidade semanal` cadastrada: escreva "sem capacidade cadastrada". Não invente 0.

## A regra que vale para o relatório inteiro

Métrica que não muda nenhuma decisão é ruído. Se o número entra na página mas ninguém age sobre
ele, ele não deveria estar na página. Cinco a nove KPIs no corpo; o resto no apêndice.
