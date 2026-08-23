---
name: deck-review-print
description: Transforma um deck pronto (Canva, PPTX ou PDF) em dossie A4 de revisao — legivel, numerado e anotavel a caneta, com ~30x menos tinta que imprimir os slides. Use ao pedir "imprimir esse deck", "preparar para a presidencia revisar", "dossie de revisao", "handout para cliente", "copia de apresentador", "revisar no papel".
intent: action
effort: medium
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/ingestao-3-fontes.md
  - references/classificacao-slides.md
  - references/modos-saida.md
assets:
  - assets/templates/dossie-layout.html
  - assets/checklists/conferencia-tabelas.md
  - evals/review-print-cases.md
---

# deck-review-print

Skill do plugin `deck-builder` (v2.0.0). Pega um deck **que ja existe** e devolve um `DOSSIE-{slug}-{HHmm}.pdf`: copia A4 em preto sobre branco, com numeracao espelhada do original e espaco pautado para anotar a caneta.

> **Nao gera storyboard.** Esta skill e a unica do plugin que **consome** um deck em vez de produzir um. Se o usuario quer criar um deck, a rota e `/deck` (orchestrator).

## O problema

Deck de marca e feito para projecao: fundo escuro de sangria total, texto branco. Impresso, vira uma folha encharcada por slide. E revisao em tela nao deixa rastro — a correcao volta sem endereco de slide e alguem adivinha onde aplicar.

Piloto GLP1TIGHT v4 (17 slides, 2026-08-10): **193% TAC x 17 folhas → 16,8% TAC x 6 folhas.** Cerca de **30x** menos tinta, com 100% do conteudo textual e das 4 tabelas preservado.

## Quando ativa

- "imprimir esse deck", "preciso imprimir para revisar"
- "preparar para a presidencia", "mandar para o presidente corrigir"
- "dossie", "versao para revisao", "revisar no papel"
- "handout para o cliente", "leave-behind"
- "copia de apresentador", "minhas notas para apresentar"
- `/deck-review-print {url|arquivo}`

## Fronteiras (§10.8)

- NAO gera slides finais sem pedido explicito (D15) — render e exclusividade de `deck-render-canva`.
- NAO imprime. Entrega um PDF; o plugin nao tem acesso a periferico.
- NAO reescreve nem melhora o conteudo do deck. Transcreve o que esta la, incluindo o que estiver errado.
- NAO reconstroi tabela a partir do texto da API (D17) — leitura visual, sempre.
- NAO reproduz imagem clinica de paciente nos modos `revisao` e `apresentador`.
- NAO escreve fora de `$DECKS_DIR`.
- NAO chama API paga sem confirmacao.

## Passo 0 — dependencias

Rode `scripts/check-print-deps.sh` **antes de prometer qualquer coisa** ao usuario.

Ausencia de dependencia exclusiva de uma rota desabilita **apenas aquela rota**, com mensagem acionavel. Nucleo incompleto (Chrome headless, Pillow, numpy) bloqueia tudo — nesse caso, informe o que falta e aponte o [`INSTALL.md`](../../INSTALL.md), e pare.

**Se o usuario disser que ja instalou e o check continuar acusando falta:** quase sempre o `pip` instalou em outro interpretador (pyenv, mise, asdf, venv, brew). A primeira linha do check imprime o `python3` ativo — compare com onde o pacote foi parar, e instale com `python3 -m pip install -r scripts/requirements-print.txt`.

## Pipeline

```
   fonte                 ingestao            analise         composicao      entrega
┌──────────┐        ┌─────────────┐    ┌─────────────┐   ┌────────────┐  ┌──────────┐
│  Canva   │─url/id→│ read-design │───→│ classificar │──→│  HTML A4   │─→│   PDF    │
│  (MCP)   │        │ export png  │    │  por slide  │   │ (tema da   │  │ + medicao│
└──────────┘        └─────────────┘    └─────────────┘   │   marca)   │  │   TAC    │
┌──────────┐        ┌─────────────┐           │          └────────────┘  └──────────┘
│  .pptx   │─arquivo→│texto+render│           │                ▲               │
└──────────┘        └─────────────┘           ▼                │               ▼
┌──────────┐        ┌─────────────┐    ┌─────────────┐         │          $DECKS_DIR
│  .pdf    │─arquivo→│raster+texto│    │ transcrever │─────────┘          DOSSIE-*.pdf
└──────────┘        └─────────────┘    │ (visual p/  │
                                       │  tabelas)   │
                                       └─────────────┘
```

## Passo 1 — ingestao

Tres fontes, detalhe em [references/ingestao-3-fontes.md](references/ingestao-3-fontes.md).

| Fonte | Como | Requisito |
|-------|------|-----------|
| **Canva** (primaria) | `resolve-shortlink` → `read-design` → `get-export-formats` → `export-design` (PNG por pagina) | MCP do Canva conectado |
| **PPTX** | `python-pptx` extrai texto; LibreOffice headless renderiza cada slide | LibreOffice + python-pptx |
| **PDF** | `pdftoppm` rasteriza; camada de texto extraida quando existir | poppler-utils |

**MCP do Canva indisponivel:** NAO tente rota alternativa de download. Informe que precisa do conector ativo **nesta conversa** e ofereca a alternativa de receber o deck exportado como PDF ou PPTX.

**PDF escaneado, sem camada de texto:** siga so por leitura visual e **avise** que a transcricao e integralmente visual.

## Passo 2 — classificacao

Cada slide vira `conteudo`, `foto`, `tabela` ou `misto`. Algoritmo completo e justificativa em [references/classificacao-slides.md](references/classificacao-slides.md).

```
se estrutura tabular presente          → tabela   (misto, se houver foto de fundo)
senao se densidade_texto >= 220 chars  → conteudo
senao                                  → leitura visual decide: foto ou conteudo
```

**O TAC nao classifica (D24).** Ele e medido e reportado como metrica de tinta — nunca como criterio de decisao. Duas versoes anteriores desta skill usaram TAC para separar `foto` de `conteudo` (limiar absoluto, depois baseline relativa ao deck) e as duas estavam erradas: na execucao real da GLP1TIGHT, fotos mediram 65% e 273%, conteudo mediu 37% e 266%. Num deck de fundo escuro chapado a foto e frequentemente **mais clara** que o fundo, e o sinal se inverte. Nenhum limiar conserta um sinal que nao existe.

**Leitura visual e trabalho seu, nao de heuristica.** Voce esta olhando as imagens exportadas. Monte uma folha de contato com as N paginas e classifique olhando — e o mesmo mecanismo que o D17 ja exige para transcrever tabela, aplicado a classificacao.

**Mostre os rotulos ao usuario antes de compor** e aceite override. Este e o verdadeiro guarda-costas da regra, e e por isso que ela pode ser simples.

## Passo 3 — transcricao

- **Texto corrido:** transcreva fielmente. Nao melhore, nao resuma, nao corrija.
- **Tabelas (D17 — INVIOLAVEL):** transcreva **lendo a imagem do slide**, nunca o texto da API. Toda tabela sai marcada `[CONFERIR]`, com a miniatura ao lado.
- **Ilegivel:** re-exporte aquele slide em resolucao maior. Se persistir, marque `[ILEGIVEL: linha N]` e **nao invente valor**.
- **Auditoria aritmetica (obrigatoria quando ha totais):** some linhas e colunas e confira contra os totais declarados. Divergencia → `[DIVERGE: soma = X, declarado = Y]`, transcreve o valor do slide **como esta**, e avisa o usuario explicitamente. Corrigir e decisao de quem escreveu o deck.

Checklist obrigatorio antes de entregar: [assets/checklists/conferencia-tabelas.md](assets/checklists/conferencia-tabelas.md).

## Passo 4 — composicao

Contrato completo da entrada em [`shared/print-dossie-schema.md`](../../shared/print-dossie-schema.md).

- **Numeracao espelha o original (D18)** — deck de 17 slides → 17 entradas, 01 a 17, inclusive os omitidos visualmente. Com `--slides 5-12`, a primeira entrada e "05".
- **`conteudo` / `tabela` / `misto`:** miniatura <= 62 mm + texto + pauta.
- **`foto`:** moldura tracejada descrevendo o slide, **sem nenhum pixel da imagem** + pauta.
- **Pauta proporcional a densidade:** slide simples 3-4 linhas; slide denso 2-3.
- **Tema por marca** via `brands.yaml` (D6); `design_system_skill` quando declarado. Sem marca ou arquivo malformado → cinza neutro, sem travar. **Corpo sempre preto sobre branco**, em qualquer tema.

Renderize `assets/templates/dossie-layout.html` para PDF com Chrome headless:

```bash
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$DECKS_DIR/$(date +%Y-%m)/DOSSIE-{slug}-$(date +%H%M).pdf" \
  "file://$TMP/dossie.html"
```

## Passo 5 — medicao e entrega

```bash
python3 scripts/measure-tac.py original.pdf DOSSIE-{slug}-{HHmm}.pdf
```

Reporte ao usuario **tres numeros**: nº de paginas, TAC medio, e comparacao com o original — **sempre** com a qualificacao de que o TAC e proxy comparativo sem perfil ICC, nao estimativa de consumo de impressora. Reportar o numero sem a ressalva induz a erro.

Liste tambem, por numero de slide, todas as tabelas marcadas `[CONFERIR]`.

## Modos

Detalhe em [references/modos-saida.md](references/modos-saida.md).

| Modo | Pauta | Marcacoes internas | Imagem de paciente |
|------|-------|--------------------|--------------------|
| `revisao` (default) | Sim | Sim | **Nunca** |
| `handout` | Nao | Nao | So com confirmacao explicita **a cada execucao** |
| `apresentador` | Sim | Sim | **Nunca** |

**`apresentador`** inclui speaker notes, **filtrando** o bloco entre `▪ BRIEFING DE MONTAGEM` e `▪ FIM DO BRIEFING` (D22). Precedencia da fonte: `STORYBOARD.md` via `DECKLINK` → notas da pagina no Canva → nenhuma.

## Volume

Deck com mais de 40 slides: **estime paginas e tempo, e pergunte antes de processar.** Ofereca tres saidas: seguir, recortar intervalo (`--slides N-M`), ou 3 slides por folha.

## Output

```
$DECKS_DIR/{YYYY-MM}/DOSSIE-{slug}-{HHmm}.pdf
```

`$DECKS_DIR` nao gravavel → erro claro com o caminho tentado. **Nao escreva em nenhum outro lugar.**

## Regras inviolaveis (DoD)

- **D17:** toda tabela lida da imagem e marcada `[CONFERIR]`. Sem excecao.
- **D18:** numeracao espelhada, inclusive para slides omitidos visualmente.
- **Zero numeros divergentes** do original em amostragem de 100% das tabelas.
- **Modos `revisao` e `apresentador` nunca reproduzem imagem de paciente** (CFO 196/2019, LGPD).
- **Nada e escrito fora de `$DECKS_DIR`.**
- TAC sempre reportado com a ressalva metodologica.
- Rotulos de classificacao apresentados ao usuario antes da composicao, com override.

## Eval cases

Em [evals/review-print-cases.md](evals/review-print-cases.md). Fixture de regressao: **W4 GLP1TIGHT** — baseline 6 paginas, 16,8% TAC medio.

## Cross-references

- [`shared/print-dossie-schema.md`](../../shared/print-dossie-schema.md) — contrato do artefato
- [`shared/output-convention.md`](../../shared/output-convention.md) — path canonico
- [`shared/fronteiras-explicitas.md`](../../shared/fronteiras-explicitas.md) — nº 9 (nao imprime)
- [`shared/auto-detection-brands.md`](../../shared/auto-detection-brands.md) — resolucao de marca
