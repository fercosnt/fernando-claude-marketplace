# Academic Scoring — reference

Documentação do `paper_scorer.py` e das 3 APIs acadêmicas que o alimentam (Semantic Scholar, OpenAlex, bioRxiv). Este é o motor v3 da skill: transforma uma lista heterogênea de URLs científicas num ranking por sinal acadêmico real (citações, venue, recência), substituindo a heurística v1 baseada em stars/views.

**Leia quando:**
- A Fase 4.5 rodou e você quer entender o `academic-ranking-report.md` gerado
- Um paper recebeu tier surpreendente (Nature em tier 2? preprint bioRxiv em tier 1?)
- Precisa decidir se ativa `--skip-scoring` (degrada para heurística v1) ou mantém o scorer ON
- Vai estender o scorer com novo sinal (ex: author h-index) em v3+

---

## 1. As três APIs

Todas free, todas stdlib-only (urllib), todas com cache + token bucket (ver `references/cache-and-rate-limits.md`).

### Semantic Scholar (`semantic_scholar.py`)

**Endpoint:** `https://api.semanticscholar.org/graph/v1/paper/{prefixed_id}?fields=...`

Input aceita DOI (`"10.xxx/yyy"`) ou PMID numérico; a função `_normalize_id()` aplica prefixo automático:
- Começa com `10.` → `DOI:10.xxx/yyy`
- Só dígitos → `PMID:12345`
- Já tem prefixo → deixa como está

**Fields retornados:**
```json
{
  "paperId": "abc123...",
  "citationCount": 156,
  "influentialCitationCount": 23,
  "year": 2015,
  "venue": "Thyroid",
  "tldr": {"text": "Magnesium supplementation..."},
  "authors": [{"name": "...", "hIndex": 42}]
}
```

**Env:** `SEMANTIC_SCHOLAR_API_KEY` (opcional). Sem key = 1 req/s. Com key = 10 req/s (bucket `semantic_scholar`).

**Rate limit behavior:**
- 404 → retorna `None` silenciosamente + error cached `not_found` por 7d (evita re-bater)
- 429 → `handle_429("semantic_scholar", 60)`, propaga exception pro caller
- 500/503 → retry do `_http.py` (max 2), se persistir propaga

**Cache:** TTL 90d (`s2/`). Citation count sobe, mas dramaticamente pouco em 3 meses.

**CLI:**
```bash
python scripts/sci_fetch/semantic_scholar.py "DOI:10.1089/thy.2014.0028"
python scripts/sci_fetch/semantic_scholar.py "PMID:33567185"
python scripts/sci_fetch/semantic_scholar.py "10.1089/thy.2014.0028"  # auto-DOI prefix
```

### OpenAlex (`openalex.py`)

**Endpoint:** `https://api.openalex.org/works/doi:{doi}?mailto={OPENALEX_EMAIL}`

Aceita só DOI (OpenAlex não indexa por PMID diretamente no endpoint polite).

**Fields retornados:**
```json
{
  "work_id": "W2057382412",
  "doi": "10.1089/thy.2014.0028",
  "year": 2015,
  "cited_by_count": 234,
  "venue": "Thyroid",
  "venue_h_index": 68,
  "venue_quartile": "Q1",
  "concepts": [
    {"display_name": "Hashimoto disease", "score": 0.89},
    {"display_name": "Autoimmunity", "score": 0.76}
  ]
}
```

**Derivação de `venue_quartile` (em `_compute_quartile()`):**

| h-index do venue | Quartile |
|---|---|
| > 50 | Q1 (top-tier: NEJM, Nature, JAMA, Cell, Lancet) |
| 20–50 | Q2 (established: PLOS, JBC, Thyroid) |
| 5–20 | Q3 (specialty: subject-specific journals) |
| < 5 | Q4 (predatory ou emerging: MDPI edge, Frontiers edge) |

Thresholds ajustados a partir de amostragem manual na pesquisa farmacologia 2026-04-22 (16 venues conhecidos).

**Top 3 concepts com score > 0.7** — filtra ruído (concepts fracos que não deveriam pesar no score).

**Env:** `OPENALEX_EMAIL` recomendada (polite pool, 10 req/s). Sem email = anonymous pool, rate menor e sujeito a throttling. Skill avisa no boot se não setada.

**Rate limit behavior:** 404 silencioso (DOI não indexado) + error cached 7d. 429 → `handle_429("openalex", 60)`.

**Cache:** TTL 90d (`openalex/`).

**CLI:**
```bash
python scripts/sci_fetch/openalex.py "10.1089/thy.2014.0028"
```

### bioRxiv / medRxiv fallback (`biorxiv_fallback.py`)

**Endpoints (tentados em ordem):**
1. `https://api.biorxiv.org/details/biorxiv/{doi}`
2. `https://api.biorxiv.org/details/medrxiv/{doi}` (fallthrough se primeiro retorna `collection: []`)

**Output:**
```json
{
  "preprint_doi": "10.1101/2024.01.15.123456",
  "pdf_url": "https://www.biorxiv.org/content/10.1101/2024.01.15.123456v3.full.pdf",
  "preprint_server": "bioRxiv",
  "version": 3,
  "posted_date": "2024-01-15"
}
```

- Retorna **versão mais recente** (maior `version`) — preprints têm v1, v2, v3...
- `pdf_url` é HEAD-validado antes de retornar (evita URLs mortos que o server lista mas não serve mais)

**Quando é chamado:** exclusivamente de `_handle_doi()` em `upload_to_nblm.py` quando `unpaywall.is_oa=false`. Nunca é chamado proativamente para DOIs já OA — desperdício de tráfego sem ganho claro.

**Rate limit:** bucket `biorxiv` 2 req/s (conservador; API não documenta limite formal).

**Cache:** TTL 30d (`biorxiv/`). Preprints podem ganhar versão nova (`v1→v2`) mais rápido que papers publicados, TTL curto força refresh.

**CLI:**
```bash
python scripts/sci_fetch/biorxiv_fallback.py "10.1101/2024.01.15.123456"
```

---

## 2. Fórmula do scorer (RF-21)

Documentada literalmente em `paper_scorer.py::score_paper()`. Composição aditiva de sinais, cada um com ceiling próprio — ninguém domina sozinho.

```python
age_years = max(1, current_year - paper_year)  # min 1 para não dividir por zero
citations_per_year = citation_count / age_years

base              = min(50, citations_per_year * 3)                    # max 50
influential_bonus = min(20, influential_citations * 0.5)               # max 20
venue_bonus       = {"Q1": 20, "Q2": 10, "Q3": 5, "Q4": 0}[quartile]   # max 20
preprint_bonus    = 10 if (preprint_available and age_years < 2) else 0
recency_bonus     = 10 if (age_years < 3 and citations_per_year > 5) else 0

score = min(100, base + influential_bonus + venue_bonus + preprint_bonus + recency_bonus)

tier = 1 if score >= 70 else (2 if score >= 40 else 3)
```

### Por que cada componente

| Componente | Por que existe | Ceiling | Fonte |
|---|---|---|---|
| `base` | Citações/ano é o sinal clássico "papel realmente citado". Normalizado por idade para não penalizar papers novos | 50 | S2 `citationCount` |
| `influential_bonus` | S2 distingue citação com contexto (figura/tabela/discussão) de citação ritualística. Peso forte pra papers seminais | 20 | S2 `influentialCitationCount` |
| `venue_bonus` | Q1 (Nature/NEJM) passou peer review de qualidade independente do conteúdo. Boost direto | 20 | OpenAlex `venue_h_index` → quartile |
| `preprint_bonus` | Paper novo em bioRxiv/medRxiv com trend positivo merece visibilidade antes de acumular citações | 10 | bioRxiv API (só se `age < 2`) |
| `recency_bonus` | Paper <3 anos com tração já >5 cit/yr está em trajetória de seminal — sobe mais cedo | 10 | S2 + OpenAlex |

### Exemplos numéricos

**Exemplo 1: NEJM seminal (Kahn et al., 2021, diabetes review)**
```
year = 2021, age = 5, citationCount = 1200, influentialCitations = 180, venue = NEJM (h=205 → Q1)
citations_per_year = 240
base = min(50, 240*3) = 50
influential_bonus = min(20, 180*0.5) = 20
venue_bonus = 20 (Q1)
preprint_bonus = 0 (não é preprint)
recency_bonus = 0 (age=5, gate falha)
score = 50+20+20+0+0 = 90 → tier 1
rationale: "High influential citations (180) in top venue (NEJM, Q1)"
```

**Exemplo 2: MDPI ruído (autor desconhecido, 2024)**
```
year = 2024, age = 2, citationCount = 3, influentialCitations = 0, venue = MDPI Nutrients (h=12 → Q3)
citations_per_year = 1.5
base = min(50, 1.5*3) = 4.5
influential_bonus = 0
venue_bonus = 5 (Q3)
preprint_bonus = 0
recency_bonus = 0 (citations_per_year < 5)
score = 4.5 + 0 + 5 + 0 + 0 = 9.5 → tier 3
rationale: "Low citation rate (1.5/yr), specialty venue (Q3)"
```

**Exemplo 3: bioRxiv preprint recente com tração (2025)**
```
year = 2025, age = 1, citationCount = 18, influentialCitations = 4, venue = bioRxiv (preprint server, Q4 ou unknown)
preprint_available = True
citations_per_year = 18
base = min(50, 18*3) = 50
influential_bonus = min(20, 4*0.5) = 2
venue_bonus = 0 (preprint não é journal)
preprint_bonus = 10 (preprint AND age<2)
recency_bonus = 10 (age<3 AND cit/yr>5)
score = 50+2+0+10+10 = 72 → tier 1
rationale: "Recent preprint with strong citation traction (18/yr in 1yr), published on bioRxiv"
```

Exemplo 3 é o *ponto forte do scorer v2*: v1 (heurística por stars/views) daria tier baixo para este paper porque bioRxiv não tem "stars" e views de blog não existem. v2 reconhece tração real em citações mesmo antes do paper virar journal.

### Rationale rule-based

Gerado em `_build_rationale()` por identificação do **sinal dominante** (maior contribuição ao score) + **secundário** (segundo maior). Sempre 1–2 frases, determinístico, não usa LLM (reproduzível).

Exemplos de saídas:
- `"High citation rate (120/yr), strong influential citations (45)"` — dominante = base, secundário = influential
- `"Top venue (NEJM, Q1), moderate citation rate (14/yr)"` — dominante = venue, secundário = base
- `"Recent preprint on bioRxiv with growing traction"` — preprint + recency
- `"Specialty venue (Q3), too new to evaluate citations"` — baixo sinal

---

## 3. Tiers — interpretação

| Tier | Score | Significado prático |
|---|---|---|
| **1** | ≥70 | Paper seminal OU top venue OU preprint com tração excepcional. Ler primeiro, tratar como autoridade |
| **2** | 40–69 | Paper estabelecido em venue OK ou recente com sinais de crescimento. Útil pra contexto e detalhamento |
| **3** | <40 | Paper de baixo sinal acadêmico. Pode ser: muito novo sem citações, venue fraco, papel de revisão menor. **Não descartar** — pode ter valor contextual, mas não priorizar |
| **unknown** | — | Não indexado em S2 nem OpenAlex. Causa comum: conference paper, technical report, paper muito específico |

### Quando confiar num tier

- **Tier 1 com `influential_bonus >= 15`**: altíssimo sinal — citado com contexto por >30 papers. Provavelmente seminal de verdade
- **Tier 1 só por `venue_bonus + recency`**: paper novo em Nature/NEJM — confiar mas marcar como "jovem demais pra saber se replica"
- **Tier 2 estável**: papel de referência em subfield, não revolucionário mas útil
- **Tier 3 baixo (score < 20)** com idade < 2: ainda é cedo demais para julgar; re-ranquear em 6-12 meses (citations vão acumular)
- **Tier 3 baixo com idade > 5**: paper que não pegou tração — provavelmente não mudou o campo

### Quando "unknown" aparece e o que fazer

Causa mais comum: **paper não tem DOI** (working paper, relatório governamental, conference proceedings não indexados). Scorer pula e reporta `tier: unknown` — pipeline continua normalmente (paper vai pro NotebookLM via generic_web se acessível).

Outras causas:
1. **DOI muito novo** (<1 semana após publicação) — S2/OpenAlex demoram dias-semanas para indexar. Re-rodar com `--invalidate-cache-before HOJE` após 7d
2. **DOI inválido ou typo** — checar se URL original redireciona corretamente; às vezes "DOI:10.xxx/yyy" tem barra a menos
3. **Paper retratado** — retraction às vezes apaga do índice. Verificar no PubMed/publisher direto

Debugar manualmente:
```bash
python scripts/sci_fetch/semantic_scholar.py "DOI:10.xxx/yyy"
python scripts/sci_fetch/openalex.py "10.xxx/yyy"
# Se ambos retornam null → unknown é correto
# Se um retorna dados e outro não → scorer degradou para "só 1 API", verificar cache errors
```

### Quando debugar um score surpreendente

Cenário: Nature 2020 saindo como tier 2 em vez de tier 1.

1. Verificar signals brutos:
```bash
python scripts/sci_fetch/paper_scorer.py --doi "10.1038/xxx"
# Output inclui signals + rationale
```

2. Se `citation_count` está baixo: cache stale? S2 demora a atualizar count. Force refresh:
```bash
python -m scripts.sci_fetch._cache clear --kind s2 --kind openalex
python scripts/sci_fetch/paper_scorer.py --doi "10.1038/xxx"  # re-fetch
```

3. Se `venue_h_index` está wrong (Nature saindo h=10?): é OpenAlex retornando venue diferente (ex: "Nature Communications" vs "Nature"). `primary_location.source` pode ser o repositório, não o journal. Verificar raw OpenAlex response.

4. Se `influential_bonus = 0` em paper claramente influente: S2 ainda não classificou as citações (novo demais). Espera natural.

---

## 4. Flag `--skip-scoring` — quando usar

Desliga o Epic 4 inteiro. Volta ao tiering heurístico v1 (stars/views/recency).

**Quando ativar:**
- **Pesquisa não-científica** (marketing, tech, framework) — scorer roda mas nunca encontra DOI válido → gasta chamadas API + cache para retornar `unknown` em tudo. `--skip-scoring` economiza.
- **APIs acadêmicas degradadas** — S2 rate-limiting, OpenAlex 503 prolongado. Ativar para não segurar pipeline.
- **Delta research muito rápido** — se <5 URLs novas e todas conhecidas do cache v1, scorer adiciona overhead sem ganho.
- **Debug de etapa anterior** — querendo isolar problema de cache ou paralelismo sem scorer no meio.

**Quando NÃO ativar:**
- Pesquisa científica real (farmacologia, longevidade, saúde) — scorer é o diferencial v2
- Primeira rodada num domínio novo — calibrar o ranking bate com expectativa manual
- Quando o usuário pede "me dê os top 5 papers seminais" — sem scorer, caímos em heurística fraca

Default: **ON**. `--skip-scoring` é opt-out consciente.

---

## 5. Como o scorer roda em paralelo (`_maybe_score`)

O scorer é invocado dentro dos workers `_worker_ncbi` e `_worker_academic` via wrapper `_maybe_score()`:

```python
def _maybe_score(task: UploadTask, enable_scoring: bool) -> None:
    if not enable_scoring:
        return
    try:
        doi = task.canonical.replace("doi:", "") if task.canonical.startswith("doi:") else None
        pmid = task.canonical.replace("pmid:", "") if task.canonical.startswith("pmid:") else None
        if not doi and not pmid:
            return
        result = paper_scorer.score_paper(doi=doi, pmid=pmid)
        task.academic_score = result.get("score")
        task.academic_tier = result.get("tier")
        task.academic_rationale = result.get("rationale")
        task.academic_signals = result.get("signals")
    except Exception as e:
        # Best-effort: scorer never blocks upload
        log.warning(f"scorer failed for {task.canonical}: {e}")
```

**Garantias:**
1. **Best-effort** — exception em S2/OpenAlex/bioRxiv nunca derruba pipeline. Worker continua, task vai pro uploader, manifesto é gravado sem `academic_score`.
2. **Paralelo por worker** — scorer é chamado por cada worker no seu próprio thread, não em pool separado. O scorer *internamente* faz as 3 chamadas API em paralelo via `ThreadPoolExecutor(3)` dentro de `score_paper()`.
3. **Não bloqueia upload** — upload serial via `upload_queue` consome tasks tão logo o worker `put()` a task. Scorer rodando mais lento apenas atrasa o enrich do manifesto, não o upload.

**Propagação para manifesto + report:**
- `_upload_and_record()` mescla `academic_score`, `academic_tier`, `academic_rationale`, `academic_signals` em `ingest_metadata` via `record_source()`
- Após Fase 4.5, `_write_ranking_report()` lê o manifesto, filtra sources com `academic_score`, ordena desc, substitui `{{TABLE_ROWS}}` + `{{TIER_N_COUNT}}` no template `assets/templates/academic-ranking-report.md`
- Arquivo final: `<work_dir>/academic-ranking-report.md` (ao lado do PDF e do manifesto)
- Summary JSON retornado pelo orquestrador inclui `tier_distribution: {tier_1: N, tier_2: N, tier_3: N, unknown: N}` e `academic_ranking_report: <path>`

---

## 6. Extensões futuras (não implementadas em v2)

- **F11 Venue whitelist/blacklist** — usuário declara venues confiáveis; scorer usa pesos customizados. Externalizar `QUARTILE_THRESHOLDS` e `VENUE_OVERRIDES` para JSON
- **F12 Author h-index** — OpenAlex já retorna `authors[].hIndex`; adicionar `author_bonus = min(15, max_author_hindex / 10)` à fórmula
- **F10 Citation graph expansion** — dado top-5 tier 1, consultar S2 "papers that cite this" para descobrir papers relacionados que não apareceram na busca original
- **LLM rationale enrichment** — opcional, pay-per-call: dado signals + TLDR, gerar 2-3 frases explicando *por que* o paper é importante (hoje é rule-based, determinístico)

Todos requerem validação com >1 usuário antes de comprometer complexity — v2 scorer atual cobre o caso dominante (pesquisa científica individual).
