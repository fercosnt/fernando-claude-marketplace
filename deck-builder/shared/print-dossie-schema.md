# §10.9 Print Dossie Schema (v2.0.0)

> Contrato do artefato `DOSSIE-{slug}-{HHmm}.pdf`, produzido por `deck-review-print`.
> Decisoes que governam este contrato: **D17** (transcricao visual), **D18** (numeracao espelhada), **D24** (o TAC mede tinta, nao classifica).

## O problema que o dossie resolve

Deck de marca e desenhado para **projecao**: fundo escuro de sangria total, texto branco. No papel isso vira uma folha encharcada de tinta por slide, e a revisao em tela nao deixa rastro — a correcao volta por WhatsApp, sem endereco de slide, e alguem precisa adivinhar onde aplicar.

O dossie inverte as tres coisas: preto sobre branco, numerado, com espaco pautado para escrever.

Medicao piloto (GLP1TIGHT v4, 17 slides, 2026-08-10): **193% TAC medio x 17 paginas → 16,8% TAC medio x 6 paginas.** Reducao do produto paginas x cobertura de 3.281 para 101 — aproximadamente **30x**.

## Regra de numeracao (D18 — INVIOLAVEL)

**Todo artefato derivado de um deck preserva a numeracao do deck de origem, inclusive para slides omitidos visualmente.**

Deck de 17 slides → dossie com exatamente 17 entradas, numeradas 01 a 17. Um slide de foto que entra sem imagem **continua ocupando seu numero**. Nao ha renumeracao, nao ha compactacao, nao ha "slides 4-6 omitidos".

A numeracao e o **protocolo de enderecamento** entre revisor e operador. Quebra-la quebra o ciclo de correcao inteiro — e o ciclo de correcao e a razao de existir da skill.

Com `--slides 5-12`, saem so as entradas do intervalo, **com a numeracao original preservada** (a primeira entrada e "05", nao "01").

## Estrutura de uma entrada

Cada slide do deck de origem vira uma entrada com quatro zonas:

```
┌─────────────────────────────────────────────────────────┐
│  07                                     [tipo: conteudo] │  ← numero espelhado
├──────────────────┬──────────────────────────────────────┤
│                  │  Action title do slide                │
│   [miniatura]    │                                       │
│   <= 62mm        │  - bullet transcrito                  │
│                  │  - bullet transcrito                  │
│                  │  - bullet transcrito                  │
├──────────────────┴──────────────────────────────────────┤
│  ________________________________________________       │  ← pauta de anotacao
│  ________________________________________________       │
└─────────────────────────────────────────────────────────┘
```

| Zona | Regra |
|------|-------|
| **Numero** | Espelha o deck de origem (D18). Sempre 2 digitos. |
| **Rotulo de tipo** | `conteudo` / `foto` / `tabela` / `misto`, resultado da classificacao (D24). Sempre visivel — o revisor precisa saber por que um slide entrou sem imagem. |
| **Miniatura** | <= 62 mm de largura. Presente em `conteudo`, `tabela` e `misto`. **Ausente** em `foto`. |
| **Corpo** | Texto transcrito. Tabela redesenhada em preto sobre branco, linhas finas, corpo >= 7,5 pt. |
| **Pauta** | Linhas de anotacao, quantidade **proporcional a densidade**: slide simples 3-4 linhas, slide denso 2-3. |

### Slide `foto` — entrada sem imagem

Slide puramente fotografico entra como **moldura tracejada** identificando o que e, sem nenhum pixel da foto:

```
┌─────────────────────────────────────────────────────────┐
│  10                                        [tipo: foto]  │
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐   │
│    Slide de cases (7 pares antes/depois de pacientes)    │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘   │
│  ________________________________________________       │
└─────────────────────────────────────────────────────────┘
```

Duas razoes, nao uma: economiza tinta **e** evita circular imagem clinica de paciente em material impresso que sai da clinica (CFO 196/2019, LGPD). Slide de foto sem texto nenhum vira entrada minima: numero + descricao do que e a imagem + pauta.

## Marcacao `[CONFERIR]` (D17 — INVIOLAVEL)

**Toda tabela transcrita sai marcada `[CONFERIR]`, sem excecao**, e a miniatura do slide original fica ao lado dela.

A transcricao e feita **lendo a imagem do slide**, nunca o texto corrido devolvido pela API — o Canva devolve o conteudo de tabela como bloco corrido, sem estrutura de linha e coluna, e reconstruir a partir dali e o caminho mais rapido para publicar um numero errado.

Casos de borda:

| Situacao | Comportamento |
|----------|---------------|
| Tabela ilegivel na resolucao exportada | Re-exportar **aquele slide** em resolucao maior antes de desistir |
| Ainda ilegivel | Transcrever o que for legivel, marcar `[ILEGIVEL: linha N]`. **Nunca inventar valor.** |
| Mais de 8 colunas | Reduzir corpo ate 7 pt; abaixo disso, quebrar em duas tabelas e sinalizar a quebra |
| Grafico nativo / SmartArt (PPTX) | Tratar como `tabela`/`misto` — leitura visual + `[CONFERIR]` |

### Limites da nota de rodape do Canva (verificado 2026-08-23)

`replace_speaker_notes` aceita **texto puro**, ate 5.000 caracteres. Nao ha formatacao: sem negrito, sem cor, **sem tamanho de fonte**. Pedido de "letras maiores nos titulos" e impossivel neste canal.

O que da para fazer, e que resolve a maior parte do problema de leitura: **estrutura em texto puro**. Formato v2 do bloco de briefing — rotulo em linha propria, corpo indentado em 3 espacos, linha em branco entre blocos. Custa ~40 caracteres a mais por bloco e melhora muito a varredura visual no painel de notas.

Se a formatacao rica for mesmo necessaria, o unico canal com ela e o **texto na propria pagina** — que a Fronteira nº 10 e o RF-40 proibem, por sujar a arte.

### Marcacao `[DIVERGE]` — quando a tabela nao fecha

Alem de transcrever fielmente, a skill **audita a aritmetica** de toda tabela que declare totais: soma de linha, soma de coluna, e colunas derivadas. Divergencia encontrada:

- a celula sai marcada `[DIVERGE: soma da linha = X, total declarado = Y]`;
- o **valor do slide e transcrito como esta** — o dossie reproduz o original, nao o corrige;
- a divergencia entra no resumo final e e comunicada explicitamente ao usuario.

Corrigir e decisao de quem escreveu o deck. O trabalho da skill e **encontrar e apontar**. Fidelidade ao slide e correcao do slide sao coisas diferentes: o dossie garante a primeira e sinaliza a ausencia da segunda.

O resumo final da execucao lista **todos** os slides com tabela, por numero, para conferencia explicita. Se o usuario apontar divergencia depois de conferir, a skill regrava o PDF e registra a divergencia no log da execucao.

## Modos de saida

| Modo | Slides/folha | Pauta | Imagem de paciente | Uso |
|------|--------------|-------|--------------------|-----|
| `revisao` (default) | 2, A4 retrato | Sim | **Nunca** | Revisao da presidencia — caso dominante |
| `handout` | 2, respiro maior | Nao | So com confirmacao explicita **por execucao** | Leave-behind de cliente |
| `apresentador` | 2 | Sim | **Nunca** | Copia de quem apresenta |
| `aplicar` (Fase 3) | — | — | — | Correcoes enderecadas → `edit-design` (D25) |

**Modo `apresentador`** inclui as speaker notes, **filtrando** o bloco entre `▪ BRIEFING DE MONTAGEM` e `▪ FIM DO BRIEFING` (D22) — nota interna de montagem nao vai para o papel do apresentador. Precedencia da fonte das notas: `STORYBOARD.md` vinculado via `DECKLINK` → notas da propria pagina no Canva → nenhuma.

**Modo `handout`** nao leva marcacao interna de processo: sem `[CONFERIR]`, sem rotulo de tipo, sem pauta. E peca apresentavel a cliente.

## Tematizacao por marca

Resolve via `brands.yaml` (D6) e carrega `design_system_skill` quando declarado. Sem marca detectada ou `brands.yaml` ausente/malformado → **tema neutro em cinza**, sem travar o fluxo (mesma degradacao de §10.5).

O tema afeta apenas cor de titulo, fio e rotulo. **O corpo do texto e sempre preto sobre branco** — a razao de existir do dossie e legibilidade impressa, e nenhuma marca sobrepoe isso.

## Medicao de TAC — o que o numero significa e o que nao significa

TAC = media por pixel da soma dos 4 canais CMYK normalizados, escala 0-400%.

A conversao CMYK e a **ingenua do Pillow, sem perfil ICC**. Isso torna o numero um **proxy comparativo** — adequado para dizer "esta pagina gasta 8x menos tinta que aquela" — e **nao** uma estimativa de consumo real de impressora. A skill reporta o numero sempre com essa qualificacao. Reportar "16,8% TAC" sem ela e induzir a erro.

Alvo: **<= 25% TAC medio** por pagina do dossie.

> Observacao metodologica do piloto: as miniaturas respondem pela maior parte do TAC residual. Uma variante sem miniaturas mediu ~6% por pagina, ao custo de o revisor perder a referencia visual do slide. E trade-off que o modo de saida deve **expor**, nao decidir sozinho.

## Cross-references

- `fronteiras-explicitas.md` — nº 9 (nao imprime — entrega PDF)
- `output-convention.md` — path canonico do `DOSSIE-*.pdf`
- `auto-detection-brands.md` — resolucao de marca (D6)
- `../scripts/measure-tac.py` — medicao
- `../scripts/check-print-deps.sh` — dependencias de sistema
