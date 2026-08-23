# §10.10 Contrato de Render no Canva (v2.0.0)

> Regras de edicao programatica de design no Canva, derivadas de execucao real
> (2026-08-23). Governa o Bloco B (`deck-render-canva`) e qualquer skill que
> escreva num design.

## A regra que custou uma pagina quebrada

**`replace_text` NAO preserva a formatacao do elemento.** Ele reaplica valores
padrao em `lineHeight`, `listMarker` e `listLevel`, mesmo quando o texto novo
tem exatamente o mesmo comprimento e o elemento tem uma unica regiao.

Medido em elemento real (fonte custom, 128,7 pt):

| Atributo | Antes | Depois de `replace_text` |
|----------|-------|--------------------------|
| `lineHeight` | 1.08 | **1.4** (o default do `add_text`) |
| `listMarker` | `none` | **`disc`** |
| `listLevel` | 0 | **1** |
| altura do elemento | 153,5 | **332,8** |

Efeito visivel: marcadores de lista aparecendo do nada, texto quebrando em
duas linhas, elemento invadindo o de baixo.

## As duas receitas testadas

### Elemento de regiao unica → `replace_text` + restauracao

```
1. read-design  → capturar lineHeight, listMarker, listLevel, top, left, width
2. replace_text → o texto novo
3. format_text  → devolver line_height, list_marker, list_level capturados
4. position_element → devolver top e left capturados
5. conferir a altura contra a original; se divergir, o texto nao coube
```

**Comprimento importa, mas nao do jeito ingenuo.** Nao e o numero de caracteres
— e a **largura renderizada**. `"00%"` e mais largo que `"62%"` na mesma fonte e
quebrou linha; `"0%"` coube. Placeholder de template deve ser **mais estreito**
que o original, nao apenas mais curto.

### Elemento com regioes mistas → `find_and_replace_text`

Preserva as regioes e os atributos. E a ferramenta correta para caixa de texto
com negrito e normal misturados — `replace_text` colapsaria tudo numa regiao so.

```
find_and_replace_text(element_id, find_text="trecho exato", replace_text="novo")
```

Cuidado com aspas tipograficas (`“ ”`) e espacos iniciais: o `find_text` e
literal.

## Verificacao obrigatoria por pagina

O `edit-design` devolve `status: "edits_unverified"` de proposito. Antes de
commitar:

- [ ] Comparar a altura de cada elemento editado com a altura original
- [ ] Conferir `listMarker`/`listLevel` no `document` de retorno
- [ ] Olhar o thumbnail devolvido
- [ ] Divergencia → corrigir **antes** do commit. O commit e irreversivel
- [ ] Falha no meio → `finalize: "cancel"`. Deck meio editado e pior que deck intocado (RNF-14)

## Tabelas: o limite duro

A API de edicao **nao tem operacao de criar tabela**. As 27 operacoes cobrem
texto, formas, imagens e paginas — nenhuma cria estrutura tabular.

Tabela nativa do Canva aparece no `read-design` como elemento `type: "sheet"`,
com `layout.columns` e `layout.rows` — **geometria apenas**. As celulas vem com
`rowId: ""`, `colId: ""`, sem `locator_id` e **sem nenhum texto**, mesmo quando
consultadas diretamente por `filter.element_ids`.

Tentativa de escrita, verificada em 2026-08-23:

```json
{"status": "failure",
 "error": {"code": "not_supported",
           "message": "\"sheet-element\" has no text content"}}
```

A tabela renderiza perfeitamente na imagem exportada, mas para a API ela e
**opaca**: nao ha leitura nem escrita de celula. A estrutura sobrevive no brand
template e serve para quem monta a mao; o render nao a preenche.

Consequencias:

1. Slide com tabela **exige** brand template que ja a contenha (reforca D19).
2. Mesmo com o template, o preenchimento da tabela e trabalho humano.
3. Simular tabela com retangulos + caixas de texto **e proibido** — produz algo
   que ninguem consegue editar como tabela depois.

4. **Numero dentro de tabela nao pode ser neutralizado por API.** Ao preparar
   brand template a partir de deck real, os valores das tabelas so saem no
   editor, a mao. Se ficarem, o template propaga dado real para todo deck novo.

> Pedido real da redatora em 2026-08-23: "quando tiver tabela, ja consegue
> montar?". A resposta honesta e: a estrutura sim, via template; o conteudo
> nao, ate a API expor as celulas.

## Corolario para o D17

A opacidade do `sheet-element` confirma o **D17** por um caminho mais forte do
que o original. A decisao dizia "transcreva tabela lendo a imagem, nunca o texto
da API" por seguranca de dado. Agora sabe-se que **nao existe alternativa**: a
API nao devolve conteudo de tabela em hipotese nenhuma. Leitura visual nao e a
opcao preferida — e a unica.

## Cross-references

- `fronteiras-explicitas.md` — nº 1 (D15), nº 10 (nao publica/compartilha)
- `print-dossie-schema.md` — limites da nota de rodape
- `briefing-annotation-contract.md` — camada de anotacao

## Publicar brand template — bloqueio verificado (2026-08-23)

Tentativa de `publish-brand-template` sobre um design proprio da conta:

```
Error publishing brand template: Not allowed to access brand template
with id 'EAHTFlSGcM8'
```

Depois da falha, `search-brand-templates` continuou devolvendo lista **vazia** —
o template nao foi criado.

Duas causas possiveis, nao distinguiveis pela mensagem:

1. **Escopo ausente no conector** — `brandtemplate:content:write`. A propria
   descricao da ferramenta instrui a desconectar e reconectar o conector do
   Canva para gerar token novo com o escopo.
2. **Recurso de plano** — Brand Templates e funcionalidade de Canva
   Teams/Enterprise. Sem o plano, nenhum escopo resolve.

**Como distinguir:** reconectar o conector e repetir. Se a busca continuar vazia
e o publish falhar igual, e plano.

> **Releitura importante.** A ausencia total de brand templates na conta foi
> interpretada primeiro como "a designer ainda nao montou". A hipotese mais
> provavel agora e que **a conta nao pode ter brand templates**. Isso muda o
> bloqueio do Bloco B de "esperar janela da designer" para "resolver
> permissao ou plano" — que e problema de conta, nao de agenda.
