# §10.11 Contrato da Camada de Anotacao (v2.0.0)

> Contrato do briefing de montagem escrito nas speaker notes de um design do
> Canva, e do comentario-indice que o acompanha.
> Decisoes: **D21** (todo handoff carrega sua instrucao), **D22** (notas sao
> campo compartilhado, delimitado), **D23** (view, nao copia), **D26** (editavel,
> limpeza arquiva).
>
> **Validado em campo em 2026-08-23.** A redatora recebeu o link, montou o deck
> e respondeu "nao abri o markdown". A hipotese do Epico C se sustenta.

## O problema

O `STORYBOARD.md` tem ~120 linhas por slide e e documento de **autoria**. Quem
revisa e monta precisa de ~6 linhas e de um documento de **execucao**. Entregar a
fonte inteira transfere o trabalho de leitura em vez de resolve-lo.

A camada de anotacao entrega a instrucao **no lugar onde a pessoa ja esta
trabalhando** — a nota da propria pagina.

## Formato do bloco (v2)

```
▪ BRIEFING DE MONTAGEM · slide 02/13 · problema

PROVAR
   Que o mercado se partiu em dois e que o que se perdeu foi
   margem, nao paciente. E o gancho do arco.

ESCREVER
   A pagina veio com dois blocos quando o storyboard pedia um.
   Fundir num argumento so, maximo 4 bullets de 1 linha.

NAO MEXER
   Os 40% e a queda de margem 28% -> 19%. Os dois estao
   [VERIFICAR] e os 40% estao marcados como FABRICADO.

DECIDIR
   Variacao de imagem (3 opcoes) e se o grafico fica em split
   50:50 ou full-width.

▪ FIM DO BRIEFING

[speaker notes do apresentador seguem daqui]
```

### Regras do formato

| Regra | Valor |
|-------|-------|
| Teto | **900 caracteres** por bloco (medido: 517–713 nos 13 reais) |
| Rotulos | Exatamente 4, nesta ordem: `PROVAR` `ESCREVER` `NAO MEXER` `DECIDIR` |
| Layout | Rotulo em linha propria · corpo indentado 3 espacos · linha em branco entre blocos |
| Largura da linha | Quebrar em ~64 colunas |
| Marcadores | `▪ BRIEFING DE MONTAGEM` / `▪ FIM DO BRIEFING`, literais |

O layout v2 veio de **pedido da usuaria real**: "se conseguir usar tamanhos de
letras diferentes e pular linhas pode ajudar na leitura". Quebra de linha e
hierarquia foram atendidas; tamanho de fonte **nao existe** neste canal (ver
"Limites duros").

### Os quatro rotulos

| Rotulo | Responde | Origem no storyboard |
|--------|----------|---------------------|
| `PROVAR` | Por que este slide existe no arco | `**Mensagem-chave:**` + posicao narrativa |
| `ESCREVER` | Qual e a tarefa de escrita **nesta** pagina | `Conteudo do slide` + `Layout sugerido` |
| `NAO MEXER` | Decisao fechada ou trava de compliance | `[VERIFICAR]`, numeros, tags de compliance |
| `DECIDIR` | O que esta em aberto para quem monta | Variacoes de imagem, layout, campos que estouraram |

Ordem de corte quando estoura os 900: de baixo para cima. `PROVAR` e a unica
linha que nao esta em lugar nenhum do Canva — se so uma sobreviver, e ela.

**`ESCREVER` foi a correcao mais importante do contrato.** O conjunto original
terminava em `ORIGEM` e nenhum rotulo respondia "qual e o meu trabalho de escrita
aqui?" — a primeira pergunta de quem redige. O briefing tinha sido desenhado para
quem **confere**, nao para quem **escreve**. `ORIGEM` saiu; o caminho do
storyboard passou para o comentario-indice.

## Limites duros do canal (verificados)

`replace_speaker_notes` aceita **texto puro**, ate 5.000 caracteres.

| Recurso | Disponivel? |
|---------|-------------|
| Quebra de linha, indentacao, linha em branco | **Sim** |
| Negrito, cor, **tamanho de fonte** | **Nao** |
| Ancoragem por pagina | Sim — e o unico canal com ela |

`comment-on-design` aceita so `design_id` + ate 1.000 chars, **sem ancora de
pagina**. Por isso o comentario e **indice do deck**, nunca anotacao de slide.

Formatacao rica so existiria em texto na propria pagina — proibido pela
Fronteira nº 10 e pelo RF-40, porque sujaria a arte.

## Campo compartilhado (D22)

As notas tem dois donos com necessidades opostas: quem **monta** e quem
**apresenta**. A disputa se resolve por delimitacao, nao por escolha:

- bloco de montagem no topo, entre marcadores;
- notas do apresentador abaixo, intactas;
- promocao a deck final = **remocao do bloco**, nunca sobrescrita do campo.

O briefing e sempre **prefixado**. O que ja existia permanece.

## Limpeza e arquivamento (D26)

O bloco **e editavel** — quem monta vai escrever ali, e isso e sinal de adocao.

O render grava no `DECKLINK` o **hash do briefing gerado** por pagina. Na
limpeza, cada bloco e comparado com seu hash:

| Estado | Acao |
|--------|------|
| Identico ao gerado | Remove em silencio |
| **Divergente** | **Arquiva** em `## Recados arquivados` no `DECKLINK`, com nº de slide e data, e so entao remove |
| Marcador de abertura sem fechamento | **Nao remove nada.** Reporta a pagina |

Apagar por heuristica arrisca comer nota de outra pessoa. Marcador quebrado vira
aviso, nunca adivinhacao.

## Comentario-indice (uma vez por design)

<= 1.000 chars. Conteudo obrigatorio:

1. caminho do `STORYBOARD.md` de origem;
2. nº de slides que vieram de template;
3. slides **pendentes** (sem template — RF-23);
4. slides com `[VERIFICAR]` aberto;
5. como ler o briefing e como limpa-lo.

E o unico ponto do fluxo com visao do deck inteiro. Enderecamento por slide
continua sendo a numeracao espelhada (D18).

## Um unico destinatario

Nao existe deck que pule a revisao de conteudo e va direto para a designer
(Questao 11, fechada). O briefing tem **um** publico — quem revisa e monta — e
nao precisa de segundo registro para design.

## Cross-references

- `canva-render-contract.md` — regras de edicao programatica (o briefing usa `replace_speaker_notes`)
- `print-dossie-schema.md` — modo `apresentador` filtra este bloco (D22)
- `output-convention.md` — `DECKLINK-*.md` guarda os hashes
- `fronteiras-explicitas.md` — nº 10 (nao publica nem compartilha)
