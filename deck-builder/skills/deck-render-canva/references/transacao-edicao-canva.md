# Transacao de edicao no Canva — o que quebra e como evitar

Complementa [`shared/canva-render-contract.md`](../../../shared/canva-render-contract.md)
com o passo a passo operacional.

## Ciclo obrigatorio

```
1. read-design (open_transaction: true)   → transaction_id + locator_ids + formatacao
2. edit-design (operations, keep_open)    → uma pagina por chamada
3. conferir o `document` e o thumbnail devolvidos
4. edit-design (finalize: commit)         → SEM operations. IRREVERSIVEL
```

`operations` e `finalize` **nao podem ir na mesma chamada**.

## Capture ANTES de editar

Para cada elemento que voce vai tocar, guarde:

```
lineHeight · listMarker · listLevel · top · left · width · height
```

A `height` e a testemunha: se depois da edicao ela divergir da original, o texto
nao coube ou a formatacao se perdeu.

## `replace_text` nao preserva formatacao

Medido em elemento real (fonte custom, 128,7 pt, texto de comprimento identico):

| Atributo | Antes | Depois |
|----------|-------|--------|
| `lineHeight` | 1.08 | **1.4** |
| `listMarker` | `none` | **`disc`** |
| `listLevel` | 0 | **1** |
| altura | 153,5 | **332,8** |

Nao depende de comprimento nem de numero de regioes. O `1.4` e o default do
`add_text` — o `replace_text` reaplica padroes.

### Receita para elemento de regiao unica

```
replace_text      → texto novo
format_text       → line_height, list_marker, list_level capturados
position_element  → top e left capturados
conferir height contra a original
```

### Receita para elemento de regioes mistas

`find_and_replace_text` — preserva regioes e atributos sozinho. Use sempre que a
caixa tiver negrito e normal misturados; `replace_text` colapsaria tudo numa
regiao so.

Cuidado: `find_text` e literal. Aspas tipograficas (`“ ”`), travessoes (`—`) e
espacos iniciais precisam bater exatamente.

## Largura renderizada, nao contagem de caracteres

`"00%"` quebrou linha onde `"62%"` cabia — mesmo numero de caracteres, glifos
mais largos. Texto novo deve ser **mais estreito** que o original, nao apenas
mais curto.

Sintoma: `height` do elemento vira multiplo da original (2x = duas linhas).

## `add_text` entra sempre em preto 16 pt

Invisivel em fundo escuro. Sempre siga com `format_text` (cor + corpo) numa
**segunda** chamada — o `element_id` so existe depois do add.

## Coordenadas

`pos` no `read-design` e **`(top, left)`**, nao `(left, top)`.

## Paginas que rejeitam edicao

Pagina marcada `(NON-EDITABLE)` ou `type: "responsive"` **rejeita o lote
inteiro**. Ecoe `is_editable` / `is_responsive` do `read-design` na chamada.

## Tabela: opaco

`type: "sheet"` expoe so geometria. Celulas vem com `rowId: ""`, `colId: ""`, sem
`locator_id` e sem texto. Escrita retorna:

```json
{"code": "not_supported", "message": "\"sheet-element\" has no text content"}
```

Nao ha leitura nem escrita de celula. Nunca prometa preencher tabela.

## Falhou no meio? Cancela.

```
edit-design(transaction_id, finalize: "cancel")
```

Deck parcialmente editado e pior que deck intocado — a ausencia de uma edicao
passa a significar duas coisas (RNF-14). O `cancel` descarta tudo e nao deixa
rastro.
