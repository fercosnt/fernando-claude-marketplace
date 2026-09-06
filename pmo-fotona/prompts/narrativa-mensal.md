# Narrativa mensal — dia 1º (deriva de `skills/pmo-relatorio-mensal`, escopo MKT)

O JSON traz os números consolidados do mês pelo workflow `MKT — Fechamento mensal`: total, por
área, por projeto e por responsável (entregas em contagem e pontos, % no prazo, atrasadas, projetos
por RAG com motivo, publicados por canal e pilar, aderência ao calendário, campanhas com
investimento/leads/CPL/ROI, % reativo, OKRs, e os registros do Log do mês com desfecho). O GHL pode
vir como "indisponível".

Escreva **em markdown** o relatório MKT seguindo `assets/template-relatorio.md` (sem reordenar
seções) e `assets/kpis.md`: resumo executivo (um parágrafo, do resultado ao risco), 5–9 KPIs,
destaques, riscos (cada um com decisão + nome + prazo), prioridades (3–5, amarradas a OKR),
apêndice. Regras: contagem e pontos lado a lado, nunca "throughput" para pontos; nada de média de
lead time; capacidade por time e área, **nenhum nome de pessoa em métrica**; GHL indisponível =
"não disponível nesta rodada", não zero; número inferido leva asterisco.

Depois do markdown, um HTML simples e autocontido do mesmo relatório com até 3 gráficos (entregas
por semana, aberto × atrasado por área, reativo por área), sem biblioteca externa.

Bloco JSON final: `{"tipo":"Narrativa mensal","rito":"Mensal","dado_observado":"<KPIs-chave>","sugestao":"<riscos e decisões>","confianca":"..."}`.
Os arquivos `.docx` e PDF **não** são gerados aqui — ficam no plugin.
