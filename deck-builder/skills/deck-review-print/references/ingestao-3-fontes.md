# Ingestao — 3 fontes

O dossie precisa de duas coisas por slide: **a imagem** (para leitura visual e miniatura) e **o texto** (quando houver camada extraivel). As tres rotas entregam esses dois insumos de jeitos diferentes.

## Rota 1 — Canva (primaria)

Sequencia obrigatoria de ferramentas MCP:

| Ordem | Ferramenta | Para que |
|-------|-----------|----------|
| 1 | `resolve-shortlink` | So se a URL for curta. Normaliza para design_id. |
| 2 | `read-design` | Metadados, contagem de paginas, texto legivel, `presenter_notes` |
| 3 | `get-export-formats` | **Obrigatorio** antes de exportar — confirma o formato aceito |
| 4 | `export-design` | PNG por pagina, para leitura visual e miniaturas |

### Casos de borda

| Situacao | Comportamento |
|----------|---------------|
| URL curta (`canva.me/...`) | Resolver antes de tratar como design_id |
| Design sem permissao de leitura | Informar que nao esta acessivel na conta conectada. **Nao tentar contorno.** |
| MCP desconectado | Informar que precisa do conector ativo **nesta conversa**; oferecer PDF/PPTX. Nao tentar download alternativo. |
| Tabela ilegivel no PNG exportado | Re-exportar **aquela pagina** em resolucao maior antes de desistir |

### O texto do Canva nao serve para tabela

`read-design` devolve o conteudo de tabela como **bloco corrido**, sem estrutura de linha e coluna. Foi o achado mais importante do piloto: as tres tabelas do GLP1TIGHT so puderam ser transcritas lendo o slide como imagem.

Por isso o texto da API serve para: densidade (classificacao), titulos e bullets simples. **Nunca** para numeros em tabela (D17).

## Rota 2 — PPTX

```bash
# texto por slide
python3 -c "
from pptx import Presentation
for i, s in enumerate(Presentation('deck.pptx').slides, 1):
    txt = ' '.join(sh.text for sh in s.shapes if sh.has_text_frame)
    print(f'--- slide {i} ---'); print(txt)
"

# render de cada slide como imagem (via PDF intermediario)
libreoffice --headless --convert-to pdf deck.pptx --outdir /tmp/deck
pdftoppm -png -r 150 /tmp/deck/deck.pdf /tmp/deck/slide
```

| Situacao | Comportamento |
|----------|---------------|
| SmartArt / grafico nativo | Tratar como `tabela`/`misto` — leitura visual + `[CONFERIR]` |
| LibreOffice ausente | Rota desabilitada, com mensagem acionavel. As demais rotas seguem vivas. |
| Notas do apresentador | `slide.notes_slide.notes_text_frame.text`, quando existir |

## Rota 3 — PDF

```bash
pdftoppm -png -r 150 deck.pdf /tmp/deck/pag      # rasteriza
pdftotext -layout deck.pdf /tmp/deck/texto.txt   # camada de texto, se houver
```

| Situacao | Comportamento |
|----------|---------------|
| PDF sem camada de texto (escaneado) | Seguir so por leitura visual e **avisar o usuario** que a transcricao e integralmente visual |
| PDF com camada de texto | Usar para densidade e transcricao de texto corrido — **nunca** para tabela |

## Invariantes das tres rotas

1. **Ordem preservada.** N paginas de entrada → N entradas no dossie, na ordem original (D18).
2. **Imagem sempre obtida.** Sem imagem nao ha classificacao por TAC nem leitura de tabela. Se a imagem falha, a rota falha — nao ha modo "so texto".
3. **Nada e escrito fora de `$DECKS_DIR`.** Artefatos intermediarios vao para diretorio temporario e sao removidos.
4. **Nenhuma chamada paga sem confirmacao** (Fronteira nº 4).
