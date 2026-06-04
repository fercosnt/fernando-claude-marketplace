---
name: presentation-text-extractor
description: Extrai texto de PDFs de apresentacoes (slides, decks, aulas) com OCR hibrido (PyMuPDF + Claude vision + Apple Vision). Use para extrair slide/deck PDF, OCR, transformar em markdown pra RAG/NotebookLM.
intent: Skill operacional para transformar PDFs de apresentacao em markdown estruturado em <2min, com custo controlado por roteamento inteligente (texto direto onde possivel, vision so onde precisa). Output plugavel diretamente em notebooklm, knowledge-optimizer e deep-research. Workflow automatico com hard cap de custo (compativel com cron/batch noturno).
effort: medium
---

# presentation-text-extractor

Skill Python para extrair texto estruturado de PDFs de apresentacoes e gerar markdown pronto para RAG.

## Quando usar

Triggers explicitos:
- "extrair texto desse PDF/slide/apresentacao/deck"
- "OCR neste PDF"
- "transcrever esta aula em slides"
- "transformar este deck em markdown/notas"
- "preparar este PDF pro NotebookLM/RAG"

Triggers implicitos:
- Usuario anexa `.pdf` e menciona "slides", "deck", "aula", "apresentacao"
- Usuario pede para "absorver/ingerir" conteudo de PDF em base de conhecimento

**NAO use quando:**
- PDF e contrato/documento juridico (use `triagem-nda` ou skill juridica)
- PDF e artigo cientifico denso (use `deep-research` com sci-pipeline)
- Operacoes basicas de PDF (merge/split/forms) — use `document-skills:pdf`

## O que a skill faz

Workflow automatico de 4 passos:

1. **Inventario** — scan rapido do PDF: paginas, tipo (text-based/scanned/mixed), idioma, SHA, presenca de Notes Pages
2. **Plano informativo** — estima custo por engine (text_native/apple_vision/claude_haiku/claude_sonnet) em tabela. Hard cap via `--max-cost` (default $0.10). Aborta se exceder.
3. **Execucao paralela** — cada engine roda em ThreadPoolExecutor. Modo `--batch` paraleliza por arquivo.
4. **Output estruturado** — `.md` ao lado do PDF original com frontmatter explicito + headers `## Slide N` + callout `> [!image]` para imagens descritas via vision

## Como rodar

A skill tem um wrapper em `bin/extract` que usa um venv dedicado (`.venv/`) automaticamente — voce nao precisa ativar venv ou se preocupar com path.

### Setup inicial (uma vez so)

```bash
cd ~/.claude/skills/presentation-text-extractor
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."  # adicione ao ~/.zshrc para persistir
```

Atalho opcional no PATH:

```bash
ln -sf ~/.claude/skills/presentation-text-extractor/bin/extract /usr/local/bin/extract
```

### Modo single-file (default)

```bash
~/.claude/skills/presentation-text-extractor/bin/extract deck.pdf
# output: ./deck.md (ao lado do PDF)
```

### Modo batch

```bash
~/.claude/skills/presentation-text-extractor/bin/extract --batch ~/Downloads/congresso-2026/
# output: 1 .md ao lado de cada PDF
```

### Modo automacao (cron-friendly)

```bash
~/.claude/skills/presentation-text-extractor/bin/extract --batch ~/Inbox/ --quiet --max-cost 0.20
```

### Modo auditoria (sem gastar API)

```bash
~/.claude/skills/presentation-text-extractor/bin/extract deck.pdf --dry-run
# So passos 1 e 2: inventario + tabela de plano com custo estimado
```

## Flags

| Flag | Default | Efeito |
|---|---|---|
| `--dry-run` | off | So passos 1+2, sem extracao real |
| `--max-cost N` | `0.10` | Hard cap em USD. Aborta antes de executar se estimativa exceder |
| `--interactive` | off | Pergunta confirmacao apos passo 2 (use quando estiver na frente do PC) |
| `--batch DIR` | - | Processa todos os PDFs da pasta com `--workers N` paralelos |
| `--workers N` | `4` | Numero de subprocessos em modo batch |
| `--engine [auto\|claude\|apple]` | `auto` | Forca engine (override heuristica) |
| `--model [haiku\|sonnet]` | `auto` | Forca modelo Claude (override deteccao formula) |
| `--force-ocr` | off | Ignora texto extraivel, vision em tudo |
| `--quiet` | off | So output final em stdout, logs em stderr |

## Heuristica de roteamento

Implementada em `scripts/router.py`. Para cada pagina do PDF:

```
texto = page.get_text()
area_imagem = sum(img.area) / page.area

se len(texto) >= 100 e area_imagem < 0.5:
    metodo = "text_native"
    # PyMuPDF extrai direto + roda vision SO em imagens >100x100px

senao se len(texto) < 100 e area_imagem >= 0.95:
    metodo = "claude_vision_full"
    # Renderiza pagina inteira para PNG 1568px e manda pra Claude

senao:
    metodo = "hybrid"
    # Texto direto + vision em imagens individuais

se regex de formula detecta (LaTeX, simbolos cientificos):
    upgrade Haiku --> Sonnet 4.6 nesse slide
```

**Threshold de 100 chars** cobre slides "keynote-style" com apenas titulo. Detalhes em [references/heuristica.md](references/heuristica.md).

## Output esperado

### Frontmatter

```yaml
---
source: "deck-fotona.pdf"
source_sha256: "a3f8b2c1..."
slide_count: 42
lang: "pt-BR"
extracted_at: "2026-05-23T14:30:00Z"
extracao_modo: "hybrid"        # text | multimodal | hybrid
paginas_multimodal: [3, 7, 12-15, 22]
paginas_apple_vision: [4, 22-25]
paginas_claude_haiku: [5]
paginas_claude_sonnet: [12-15]
custo_real_usd: 0.048
deck_title: "LightWalker AT — Aplicacoes Clinicas"
generator: "presentation-text-extractor v1.0"
---
```

Vantagem do formato explicito: voce abre o `.md` e ve EXATAMENTE quais slides foram OCR'ados. Ranges contiguos colapsam para legibilidade (`12-15` = 4 slides consecutivos).

### Body markdown

```markdown
# LightWalker AT — Aplicacoes Clinicas

## Slide 1 — Capa

LightWalker AT
Sistema Er:YAG + Nd:YAG dual-wavelength

> **Notas do palestrante:** Apresentacao para CIOSP 2026, foco em endodontia

## Slide 12 — Parametros clinicos

| Tecido | Fluencia | Frequencia |
|---|---|---|
| Esmalte | 8-15 J/cm² | 20 Hz |
| Dentina | 4-8 J/cm² | 15 Hz |

> [!image] Slide 12 (claude_sonnet)
> Grafico de barras — fluencia x tempo de exposicao. Eixo Y "Fluencia (J/cm2)", eixo X "Tempo (ms)". 3 curvas: Er:YAG / Nd:YAG / combinado. Legenda inferior em vermelho/azul/verde.

## Slide 13 — ...
```

**Convencao do callout `> [!image]`**:
- Sintaxe Obsidian-friendly (renderiza como bloco visual destacado)
- NotebookLM aceita como texto comum (vira contexto no RAG)
- Sufixo `(claude_haiku)`, `(claude_sonnet)` ou `(apple_vision)` indica engine
- Descricao em uma frase + detalhes curtos

## Stack tecnico

**Dependencias Python** (instaladas via `pip install -r requirements.txt`):
- `pymupdf` — parser base + extracao de imagens (wheels ARM, zero deps)
- `ocrmac` — wrapper Apple Vision (macOS ARM nativo)
- `pillow` — redimensionar imagens para 1568px antes de Claude
- `anthropic` — SDK Claude vision (modelos `claude-haiku-4-5` default, `claude-sonnet-4-6` para formulas)
- `langdetect` — auto-detect idioma (PT/EN/ES)

**Sem deps de sistema** (brew). PyMuPDF tem wheels ARM completos.

**Decisao v1**: usar `pymupdf` direto sem `docling`. Razao: docling adiciona ~500MB e e otimizado para papers densos, nao slides. Cobertura de 95% dos slides com pymupdf. `docling` entra como flag opcional v1.1 se demanda real aparecer.

Detalhes em [references/stack.md](references/stack.md).

## Custo estimado

Por deck tipico (30 slides, 5 imagens embarcadas):
- 100% Apple Vision (so texto): **$0.00**
- Hibrido Haiku 4.5: **~$0.009**
- Hibrido Sonnet 4.6 (laser/cientifico): **~$0.028**
- Vision-only Sonnet 4.6 (forced): **~$0.36**

Por mes (volume tipico do usuario, 15-20 decks): **$0.50-1.00**.

Detalhes em [references/custos.md](references/custos.md).

## Plug-points downstream

| Skill | Como conecta |
|---|---|
| **notebooklm** | `.md` gerado vai direto como source via `notebooklm add-source` |
| **knowledge-optimizer** | `.md` com `## Slide N` ja esta no formato esperado para chunking |
| **deep-research** | Quando deck e fonte cientifica, manifesto pode ser absorvido por `_notebook-manifest.json` |
| **laser-physics** | Formulas LaTeX preservadas --> alimentam calculos dosimetria |

## Out of scope (v1)

- PPTX/DOCX/XLSX nativos — exporte para PDF antes
- Imagem solta (PNG/JPG/HEIC) — v1.1 se demanda real aparecer
- Video de aula com frames — fora do escopo, skill separada futura
- Auto-upload NotebookLM — use `notebooklm` skill
- Sumarizacao do deck — fora do escopo (output e transcricao, nao analise)
- Tag suggester automatico — `knowledge-optimizer` faz isso

## Reference files

- [references/heuristica.md](references/heuristica.md) — detalhes do roteador + thresholds
- [references/stack.md](references/stack.md) — deps + Apple Vision setup + troubleshooting
- [references/custos.md](references/custos.md) — calculo de custo por modelo/cenario

## Scripts

- [scripts/extract.py](scripts/extract.py) — entrypoint principal (CLI + workflow 4 passos)
- [scripts/router.py](scripts/router.py) — heuristica de roteamento por pagina
- [scripts/vision_client.py](scripts/vision_client.py) — wrapper Claude vision (Haiku/Sonnet) + Apple Vision (ocrmac)
- [scripts/markdown_writer.py](scripts/markdown_writer.py) — geracao do .md com frontmatter + callouts
