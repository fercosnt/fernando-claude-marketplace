# Como redigir o briefing de montagem

Contrato em [`shared/briefing-annotation-contract.md`](../../../shared/briefing-annotation-contract.md).
Aqui esta o **como escrever bem**, com exemplos dos 13 briefings reais que
passaram no teste de campo.

## A regra que resume tudo

Voce esta escrevendo para quem **revisa conteudo e monta o slide** — nao para
quem confere, nao para quem faz design, nao para quem apresenta. A primeira
pergunta dessa pessoa e *"qual e o meu trabalho aqui?"*.

## `PROVAR` — por que o slide existe

Escreva a funcao do slide **no arco**, nao o assunto dele. E a unica linha que
nao esta em lugar nenhum do Canva; o resto ela infere olhando a pagina.

> **Bom:** "Que o mercado se partiu em dois e que o que se perdeu foi margem, nao
> paciente. E o gancho do arco — se cair aqui, nada depois se sustenta."
>
> **Ruim:** "Slide sobre o problema do mercado dental." — descreve o assunto, nao
> a funcao.

Slide que nao argumenta merece honestidade:

> "Nada. Este slide nao argumenta — ele protege. Forward-looking conforme
> Res. CVM 160/22."

## `ESCREVER` — a tarefa de escrita

**Olhe a pagina antes.** Este rotulo so vale se refletir o que a pagina
realmente tem. Briefing generico e ruido.

> **Bom, porque especifico:** "A pagina veio com dois blocos (crise / boutique
> curada) quando o storyboard pedia um. Fundir num argumento so, maximo 4 bullets
> de 1 linha."
>
> **Bom, porque aponta ausencia:** "FALTA o primeiro tailwind — acrescentar '78%
> dos novos pacientes chegam com hipotese de plano'."
>
> **Bom, porque pega defeito:** "Os titulos vieram em INGLES ('High Average
> Ticket', 'Strong Margin'). Traduzir os tres."

De **limite mensuravel** quando houver: "maximo 12 palavras por coluna — se
passar disso, virou manual".

E diga quando **nao ha trabalho**:

> "Nada. E o unico slide do deck sem trabalho de redacao. Copiar literal, sem
> melhorar e sem trocar palavra por sinonimo mais leve."

Dizer "aqui voce nao escreve" e tao util quanto dizer o que escrever.

## `NAO MEXER` — o que e decisao fechada

Numeros, claims com `[VERIFICAR]`, travas de compliance. **Diga o porque**, senao
soa arbitrario.

> "Os 40% e a queda de margem 28% -> 19%. Os dois estao [VERIFICAR] e os 40%
> estao marcados como **FABRICADO** no storyboard. Sem fonte CFO/ABO o slide nao
> vai — falar com o Fernando, nao trocar o dado por outro."

Repare no fecho: diz o que fazer quando o dado **nao** se confirmar. Sem isso, a
pessoa inventa um substituto.

Marque relacoes que nenhum slide sozinho contem:

> "Os KPIs sao os mesmos da capa: **tem que bater** entre os dois slides."

### Item bloqueante

Nao ha 5º rotulo (D23). Item que impede apresentar entra **no topo do
`NAO MEXER`**, em caixa alta:

> "**BLOQUEANTE** — a quote de paciente so entra com TCLE assinado confirmado.
> Sem TCLE, montar sem ela. Apresentar sem TCLE e falha grave, nao detalhe."

> Esta acomodacao e reconhecidamente apertada. Se o teste mostrar que item
> bloqueante passa batido, D23 precisa ser revista.

## `DECIDIR` — o que esta em aberto

Escolhas reais que **cabem a quem monta**. Se nao ha nenhuma, diga:

> "Nada de conteudo. So garantir que fica legivel impresso."

Nao empurre para ela decisao que ja foi tomada no storyboard.

## O que o bloco nunca carrega

| Fora | Por que |
|------|---------|
| Prompt de imagem completo | ~60% do volume do storyboard, e material de outra etapa |
| Framework, tempo estimado, objecao esperada | Contexto de autoria |
| A copia integral do slide | Ja esta **na propria pagina** |
| Caminho do storyboard | Vai uma vez so, no comentario-indice |

## Corte quando estoura 900

De baixo para cima: `DECIDIR` → `NAO MEXER` → `ESCREVER` → `PROVAR`.
Se so uma linha sobreviver, e o `PROVAR`.
Bloco truncado entra na lista do comentario-indice.

## Medicao real dos 13 briefings validados

517 a 713 caracteres. Nenhum chegou perto do teto. Se os seus estao raspando
900, provavelmente ha contexto de autoria vazando para dentro do bloco.
