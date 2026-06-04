## Papers ranqueados por sinal academico (v3)

**Metodo:** Semantic Scholar + OpenAlex + bioRxiv. Scoring composto (citacoes/ano + influential + venue + recencia).

| Tier | Titulo | Venue | Year | Citations/yr | Infl. Cit. | Score | Rationale |
|------|--------|-------|------|-------------:|-----------:|------:|-----------|
{{TABLE_ROWS}}

**Distribuicao:**
- Tier 1 (>=70): {{TIER_1_COUNT}} papers
- Tier 2 (40-69): {{TIER_2_COUNT}} papers
- Tier 3 (<40): {{TIER_3_COUNT}} papers
- Unknown (sem indexacao): {{TIER_UNKNOWN_COUNT}} papers

**Notas de interpretacao:**
- **Tier 1** = papers seminais ou de alto impacto sustentado (>=70 pontos). Use como ancora para argumentos.
- **Tier 2** = papers solidos com tracao moderada. Bom para corroborar Tier 1.
- **Tier 3** = papers recentes sem citacoes ainda OU papers antigos com pouca tracao. Trate com cautela.
- **Unknown** = nao indexado em Semantic Scholar nem OpenAlex (geralmente: working papers, gov reports, blog posts). Avalie qualitativamente.

**Sinais por componente:**
- `citations/yr` normaliza por idade do paper (evita vies anti-papers-novos)
- `influential cit.` (Semantic Scholar) = citacoes com contexto nao-trivial, melhor sinal de impacto real
- `venue quartile` (OpenAlex) baseado no h-index do journal: Q1 > 50, Q2 20-50, Q3 5-20, Q4 < 5
- Bonus de recencia para papers <3 anos com >5 cit/ano (tracao precoce)
- Bonus de preprint para papers <2 anos com versao OA em bioRxiv/medRxiv
