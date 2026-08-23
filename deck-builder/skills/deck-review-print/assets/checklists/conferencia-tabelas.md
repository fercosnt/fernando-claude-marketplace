# Checklist de conferencia de tabelas

> **Obrigatorio antes de entregar o dossie.** Guardrail do PRD: *zero numeros divergentes do original, em amostragem de 100% das tabelas.*
>
> Este checklist existe por causa do Risco nº 1: um numero transcrito com um digito trocado chega ao presidente como se fosse o original, e a decisao comercial e tomada sobre dado errado. Se isso acontecer uma vez, todo dossie passa a ser conferido linha a linha contra o Canva — e a economia de tempo que justifica a skill desaparece.

## Por tabela transcrita

- [ ] A transcricao foi feita **lendo a imagem do slide** — nao o texto corrido da API (D17)
- [ ] A miniatura do slide original esta **ao lado** da tabela transcrita, na mesma entrada
- [ ] A marcacao `[CONFERIR]` esta visivel
- [ ] Nº de linhas transcrito == nº de linhas no slide
- [ ] Nº de colunas transcrito == nº de colunas no slide
- [ ] Cabecalhos conferidos um a um
- [ ] **Cada celula numerica conferida digito a digito** contra a imagem
- [ ] Unidades preservadas (R$, %, x, meses, n=) — unidade trocada e erro de valor
- [ ] Separadores decimais preservados (`8.3x` != `83x`; `R$180k` != `R$1.80k`)
- [ ] Sinais preservados (queda, negativo, seta)
- [ ] Notas de rodape da tabela transcritas — footnote de compliance **nao e ornamento**
- [ ] Nenhuma celula foi preenchida por inferencia. Vazio no original == vazio na transcricao
- [ ] Corpo >= 7 pt (RNF-02). Abaixo disso, quebrar em duas tabelas e sinalizar a quebra

## Auditoria aritmetica — obrigatoria quando a tabela tem totais

Transcrever fielmente garante que o dossie **reproduz** o slide. Nao garante que o slide **fecha**. Sao coisas diferentes, e esta secao existe porque a primeira execucao real encontrou um erro que nenhum outro item deste checklist teria pego.

- [ ] Se ha coluna ou linha de **TOTAL**, somar e conferir **nos dois eixos**
- [ ] Soma de cada linha == total declarado da linha
- [ ] Soma de cada coluna == total declarado da coluna
- [ ] Soma dos totais de linha == soma dos totais de coluna == total geral
- [ ] Colunas derivadas conferidas (ex.: `valor x quantidade == subtotal`, `subtotal x 12 == anual`)
- [ ] Percentuais que deveriam somar 100% somam 100%

**Divergencia encontrada:**

- [ ] Marcar a celula com `[DIVERGE: soma da linha = X, total declarado = Y]`
- [ ] **Transcrever o valor do slide como esta** — o dossie reproduz o original, nao o corrige
- [ ] Listar a divergencia no resumo final, por numero de slide
- [ ] Avisar o usuario **explicitamente** ao entregar. Nao enterrar no resumo

Corrigir o numero e decisao de quem escreveu o deck, nunca da skill. O trabalho aqui e **encontrar e apontar**.

> **Caso real (GLP1TIGHT, slide 13).** Linha *Massa muscular (StarFormer)*: celulas `8X 8X 6X 2X 2X 2X` somam **28**, total declarado **27X**. As colunas fechavam em 68 e o total geral estava certo — so a celula de total daquela linha estava errada. Deck comercial, em circulacao. O erro foi achado por habito, nao por exigencia do checklist; por isso esta secao passou a existir.

## Quando algo esta ilegivel

- [ ] Aquele slide foi **re-exportado em resolucao maior** antes de qualquer desistencia
- [ ] Se ainda ilegivel: transcrito o que da, marcado `[ILEGIVEL: linha N]`
- [ ] **Nenhum valor foi inventado, estimado ou "deduzido pelo padrao das outras linhas"**
- [ ] Os trechos ilegiveis aparecem no resumo final, por numero de slide

## Antes de fechar o PDF

- [ ] O resumo final lista **todas** as tabelas, por numero de slide
- [ ] O nº de tabelas no resumo == nº de `[CONFERIR]` no corpo do dossie
- [ ] Nenhuma tabela ficou sem `[CONFERIR]` (modo `handout` e a unica excecao, e nele a marcacao some por design)

## Se o usuario apontar divergencia depois

- [ ] Corrigir a celula
- [ ] **Regravar o PDF** — nao entregar errata
- [ ] Registrar a divergencia no log da execucao: slide, celula, valor transcrito, valor correto
- [ ] Se for a segunda divergencia no mesmo deck: parar, reconferir a tabela inteira, e avisar o usuario de que a transcricao daquele slide nao esta confiavel

## O que este checklist nao cobre

Ele garante que o dossie e **fiel ao slide**. Nao garante que o slide esta **certo** — se o deck original tem um numero errado, o dossie reproduz o numero errado, fielmente.

Conferir se o dado e verdadeiro e trabalho do `deck-reviewer` (Critico 4 — auditor de `[VERIFICAR]`) e da pessoa que confirma a fonte. Sao coisas diferentes e nao se substituem.
