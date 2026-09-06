---
name: pmo-relatorio-mensal
description: Escreve os relatórios de gestão do Marketing da Fotona a partir do Notion e do GoHighLevel, em quatro escopos — o mensal do MKT para diretoria e CEO, o mensal de uma área, o andamento de um projeto, e o individual de uma pessoa (só para a coordenação, em absoluto, sem comparação) — no template da casa, em markdown, .docx, PDF ou HTML. Use sempre que pedirem "relatório mensal", "relatório da diretoria", "fechamento do mês do marketing", "como foi o mês", "números para o CEO", "consolidar o mês", "relatório da área X", "relatório de andamento do projeto Y", "como está o projeto Y no mês", "relatório do fulano", "o mês da fulana", ou quando for dia de fechar o mês. Aceita os números já consolidados pelo n8n. Também use para a leitura de um trimestre ou de uma campanha encerrada.
---

# Relatórios de gestão do MKT — quatro escopos, um método

Este relatório é lido por quem não acompanha o Notion. Ele funciona quando responde três coisas:
**o que avançou, o que está em risco, e o que precisa de decisão.** Número que não muda nenhuma
decisão é ruído — e ocupa o lugar do que importa.

Leia `../../CONTEXTO.md` e carregue o contexto. O template do escopo MKT está em
`assets/template-relatorio.md`, a definição de cada KPI em `assets/kpis.md`, e o template do
individual em `assets/template-pessoa.md` — **leia antes de escrever**, porque quase todo erro
neste relatório é de definição, não de conta.

## 1. Escolha o escopo e o formato, e confirme em uma frase

| Escopo | Para quem | Formato padrão |
|---|---|---|
| **MKT** | diretoria / CEO, via diretor | `.docx` (a diretoria edita) |
| **Área** | o coordenador da área e o diretor | PDF |
| **Projeto** (andamento) | owner do projeto e o diretor | PDF |
| **Pessoa** | **só a coordenação** (diretor, gerente de MKT, coordenador de criação) | PDF |

Formato é parâmetro: `md` (sempre gerado — é o canônico e vai para o Log), `docx`, `pdf`, `html`
(com até 3 gráficos simples: entregas por semana, aberto × atrasado, reativo por área — regras da
skill `dataviz`). Período padrão: mês anterior fechado. Diga escopo, período e formato na primeira
frase e siga — se estiver errado, é barato corrigir.

**Escopo Pessoa tem uma regra de acesso:** só executa se quem pede é da coordenação (confira o
usuário do conector contra o "quem é quem" do contexto). Para qualquer outra pessoa, recuse e
aponte o `mkt-meu-mes` do plugin do time — cada um gera o próprio. Creators (PJ) não têm relatório
individual.

## 2. Colete os números — de preferência os que o n8n já contou

No dia 1º o workflow `MKT — Fechamento mensal` consolida o mês (total, por área, por projeto e por
responsável) e manda um JSON. **Se o pedido trouxer esse JSON, use-o** e diga "números do
fechamento do n8n de <data>". Se não trouxer, consulte (queries.md) e diga que consultou — é o
mesmo dado, mas custa mais e a diretoria gosta de saber de onde veio.

Do **Notion**, sempre sem contêiner e sem `Cancelada`:

| O que | Onde |
|---|---|
| Entregas: contagem **e** pontos das concluídas no período | Q11 |
| % no prazo | `Data de conclusão ≤ Data desejada` (e `≤ Prazo` só sem data desejada) |
| Atrasadas no fim do mês, e o que travou | Q3, Q6 |
| Projetos por RAG, com `Motivo (se 🟡/🔴)` | Q13 |
| Conteúdo publicado por canal e pilar; aderência ao calendário | Q12 |
| Investimento, leads, CPL, ROI por campanha | 🚀 Campanhas |
| Carga: pontos abertos por **área** (e por pessoa só nos escopos Área/Pessoa) | Q9 |
| % reativo em pontos | Q2 + `formulas-espelho` |
| Progresso dos OKRs | 🎯 Metas & OKRs |
| O que o PMO apontou no mês e os desfechos | 🤖 Log do PMO |

Do **GoHighLevel**: leads, qualificados, oportunidades, receita influenciada. Se o GHL não estiver
acessível, escreva "não disponível nesta rodada" no lugar — deixar em branco faz o leitor achar
que foi zero.

Todo derivado vem de `formulas-espelho.md`; a API não devolve fórmula. Carimbo vazio (`Data de
conclusão`, `Publicado em`) é "carimbo ausente", nunca zero.

## 3. Trate os números com honestidade

- **Nunca preencha uma célula com estimativa sem marcar.** Número inferido leva asterisco e nota.
- **Contagem e pontos andam juntos.** E **não chame pontos de "throughput"** — throughput é contagem.
- **Não reporte média de lead time.** Enquanto não houver ~2 meses de 📜 Log de Status para o p85,
  a linha não existe.
- **Mês sem base:** "primeiro mês de medição", não coluna vazia.
- **Capacidade se reporta por time e por área no escopo MKT.** Nome de pessoa em métrica não vai
  para a diretoria.

## 4. As regras de cada escopo

### MKT
Siga `assets/template-relatorio.md` sem reordenar. O **resumo executivo** é a única parte que muitos
vão ler inteira: um parágrafo, do resultado de negócio ao risco principal. Em **riscos**, cada linha
pede uma decisão a alguém com nome e prazo. **Prioridades do próximo mês**: 3 a 5, cada uma amarrada
a um OKR. 5 a 9 KPIs no corpo.

### Área
A mesma estrutura do MKT, filtrada pela `Área`: entregas, reativo, aging máximo, projetos da área
por RAG, o que escorregou e o padrão por trás (com contagem), carga da área em pontos. Se mostrar
mais de uma área, **ordem alfabética** — nunca ordenada por desempenho.

### Projeto (andamento)
Progresso (concluídas ÷ total, 0–100), tarefas abertas por status, atrasadas, aging máximo,
dependências travadas (`Bloqueada por`), RAG e motivo, **o que mudou desde o último relatório** (leia
o Log: `Tipo = Relatório de projeto` deste projeto), próximos marcos, risco em uma frase. Nome de
pessoa nunca aparece como causa de atraso.

### Pessoa
Siga `assets/template-pessoa.md`. Tudo em **absoluto**, contra a **série histórica da própria
pessoa** (mês atual × meses anteriores dela): o que entregou (contagem e pontos), o que está com ela
(aberto, atrasado, em produção), aging dos itens dela, quanto do que pegou foi reativo, o que ficou
parado em aprovação **com ela como aprovadora**. Zero comparação com colegas, zero % de utilização,
zero adjetivo de desempenho, zero `Motivo do bloqueio`. A skill descreve carga e fluxo; quem julga é
o gestor, no 1:1. Se pedirem "compara com o fulano" ou "quem está pior", recuse e ofereça a leitura
por área.

Por que assim: métrica de fluxo usada como performance individual gera gaming previsível, e o Guia
ANPD trata medição de produtividade de empregado como inadmissível quando vai além do necessário —
mesmo com transparência prévia. O que sobrevive a isso é um relatório que descreve o que o gestor já
vê, para a conversa 1:1.

## 5. Escreva e entregue

Todo escopo abre com o **dado bruto** e fecha com **uma pergunta de decisão** (`formato-de-saida.md`).

Gere o markdown sempre; converta para o formato pedido (skills `docx` / `pdf`; HTML com os gráficos
da skill `dataviz`). Nomeie `Relatorio-<Escopo>-<AAAA-MM>.<ext>` (Pessoa: `Relatorio-1a1-<AAAA-MM>`,
sem sobrenome no nome do arquivo). No chat, **três linhas**: o resultado, o risco principal, a
decisão pedida. Quem abriu o chat no celular deve conseguir agir sem abrir o anexo.

Grave no 🤖 Log do PMO um registro (`Tipo = Narrativa mensal` / `Relatório de projeto` / `Relatório
individual`, `Rito = Mensal` ou `Sob demanda`) com o escopo, o link do arquivo e os números-chave em
`Dado observado`. Ofereça registrar o relatório MKT na 📚 Base de Conhecimento — é o que constrói a
série histórica.

## Sinais de que o relatório está errado

- Todos os KPIs verdes. Ou o mês foi excepcional, ou as metas não são metas.
- Nenhum risco. Um time de 11 pessoas com 4 marcas sempre tem um.
- Mais de 9 KPIs no corpo. O resto é apêndice.
- Um número que você não consegue apontar de onde veio. Tire.
- Um nome de pessoa perto de um adjetivo. Tire o adjetivo.
