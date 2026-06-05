# Fetch Fallback — Firecrawl como tier de escalação

Quando carregar: ao despachar subagentes (Fase 2-3) ou rodar o pipeline científico (Fase 4.5) e uma página voltar bloqueada. Define a escalação de fetch e quando vale gastar crédito Firecrawl.

## Por que existe

O fetch default dos subagentes é **WebFetch** — grátis, mas não renderiza JavaScript e toma bloqueio de Cloudflare/bot-protection ("Checking your browser", reCAPTCHA, "Just a moment"). Páginas de SPA e publishers protegidos voltam vazias ou com o desafio em vez do conteúdo.

A Fase 4.5 já resolve isso para o domínio **científico** (NCBI/Unpaywall/PMC via APIs oficiais), mas para o resto — blogs, docs SaaS JS-heavy, publishers fora do circuito OA — não havia plano B: a fonte caía no bucket manual ou era anotada como gap.

O **Firecrawl** preenche esse buraco: renderiza JS, bypassa Cloudflare e devolve markdown limpo otimizado para LLM. O custo é que é **pago por crédito**, então ele é um *tier de escalação*, nunca o fetch default.

## Tiers de fetch

| Tier | Ferramenta | Custo | Quando |
|------|-----------|-------|--------|
| **1** | WebFetch / WebSearch | grátis | **Default** — toda fonte começa aqui |
| **2** | `firecrawl scrape` | 1 crédito/URL | Quando o Tier 1 volta bloqueado/CAPTCHA/vazio (<100 chars úteis) |
| **3** | `firecrawl interact` / `scrape --actions` | 1+ créditos | Página exige login/cliques/formulário (raro) |
| **sci** | NCBI/Unpaywall (Fase 4.5) | grátis | Domínio científico — dá metadata estruturada que o Firecrawl não dá |

A regra: **só escale quando o tier anterior falhou de fato.** Não chame Firecrawl preventivamente.

## Pré-requisitos (gate)

O fallback só está disponível quando `FIRECRAWL_API_KEY` está no ambiente. Sem a key, todo o comportamento degrada para o tier anterior (graceful degradation) — o subagente anota a limitação nos gaps e segue.

```bash
[ -n "$FIRECRAWL_API_KEY" ] && echo "fallback disponível" || echo "sem key — só Tier 1"
```

O CLI (`firecrawl`) já está instalado. `firecrawl --status` mostra créditos restantes e o limite de concorrência.

## Limite de concorrência — importante

O plano expõe **apenas 2 scrapes paralelos** (`Concurrency: 0/2 jobs` no `--status`). A deep-research dispara 5-6 subagentes em paralelo; se todos chamarem Firecrawl ao mesmo tempo, batem no teto e enfileiram.

Por isso o fallback é **pontual, não em lote**: cada subagente escala no máximo as poucas URLs que realmente falharam no Tier 1, uma de cada vez. Não monte um fan-out de dezenas de `firecrawl scrape` simultâneos.

## Comando — Tier 2 (scrape)

Sinais de que o Tier 1 falhou e vale escalar: corpo com "Checking your browser" / "Just a moment" / "Access Denied" / reCAPTCHA, ou conteúdo útil < ~100 caracteres num domínio que claramente deveria ter conteúdo.

```bash
firecrawl scrape "<url>" --only-main-content -o <tmpfile>.md
```

- `--only-main-content` corta nav/rodapé/sidebar — markdown mais limpo para síntese.
- `-o <file>` grava o markdown direto no arquivo (sem `-o` vai pro `.firecrawl/`).
- Renderiza JS e bypassa Cloudflare por padrão; não precisa de flag extra.

Depois de obter o markdown, trate-o como qualquer fonte: extraia insights, cite a URL original (não o tmpfile), registre relevância.

Se o scrape **ainda** voltar bloqueado ou vazio, não insista — anote nos gaps e siga. Uma retentativa, não um loop.

## Comando — Tier 3 (interact, raro)

Só quando a página exige interação (login, aceitar cookies, clicar "load more", paginação JS) antes de revelar o conteúdo:

```bash
# scrape com ações inline (clicks/inputs/scroll antes de extrair)
firecrawl scrape "<url>" --only-main-content --actions '[{"type":"click","selector":"#load-more"}]' -o <tmpfile>.md

# ou interagir sobre um scrape anterior por jobId
firecrawl interact <scrape-id> -p "clique em Aceitar e role até o fim, depois retorne o conteúdo"
```

Tier 3 é exceção. A maioria dos bloqueios resolve no Tier 2.

## Diagnóstico de falha

Quando uma chamada Firecrawl falhar de forma inesperada, o CLI tem auto-diagnóstico (consome o `jobId` do job que falhou):

```bash
firecrawl ask --scrape-id <jobId> "por que esse scrape falhou e como corrigir?"
```

## Custo — ordem de grandeza

- `firecrawl scrape`: 1 crédito/URL. `--query` (extração estruturada): +5 créditos.
- O fallback só dispara em fontes que falharam no Tier 1, então o gasto típico por pesquisa é baixo (poucas URLs).
- Cheque o saldo com `firecrawl --status` antes de pesquisas grandes.

## Integração no pipeline científico (Fase 4.5)

O orquestrador `scripts/sci_fetch/upload_to_nblm.py` tem a flag `--firecrawl-fallback`: URLs classificadas como `cloudflare_known` (MDPI, Karger, Wiley, ScienceDirect, etc. — ver `classify_url.py`) tentam `firecrawl scrape` e, se obtêm conteúdo real, sobem como arquivo ao NotebookLM em vez de cair no bucket manual.

```bash
python scripts/sci_fetch/upload_to_nblm.py \
  --urls <urls.txt> --notebook <NB_ID> --pesquisa <slug> \
  --pesquisas-root pesquisas/ \
  --firecrawl-fallback
```

Gate interno: sem `FIRECRAWL_API_KEY`, sem o CLI, ou se o scrape voltar < 600 bytes ou ainda com cara de bloqueio, a URL cai no bucket manual como antes. O método fica registrado no manifesto (`ingest_metadata.fetch_method = "firecrawl_scrape"`).

Sem a flag, o comportamento é idêntico ao anterior — o fallback é estritamente opt-in.
