---
name: clinicorp
description: Use when the user asks about clinic performance data held in Clinicorp (dental practice management software) — faturamento da clinica, orcamentos, taxa de conversao, agenda, ocupacao, faltas ou no-show, inadimplencia, ticket medio, pagamentos, fluxo de caixa, aniversariantes, metas, dados do Clinicorp — or phrases such as "quanto a clinica X fechou", "como foi o mes", "quantas faltas tivemos", "quem tem orcamento aberto", "quanto entrou de dinheiro". Applies when the Clinicorp MCP tools are available and the question needs real clinic numbers, not estimates.
---

# Clinicorp — camada de julgamento

As tools do MCP fazem as chamadas. Esta skill decide **qual** chamada responde a pergunta
e **como** ler o resultado sem entregar numero errado. Todas as tools sao somente leitura.

## Antes da primeira chamada

1. Se a conta e de **grupo/franquia**, `subscriber_id` e obrigatorio — sem ele a API devolve 401.
   Em conta unica ele e inferido do token. Na duvida, rode `clinicorp_clinicas` /
   `clinicorp_unidades` primeiro e confirme com o usuario de qual unidade ele fala.
2. Pergunta sem periodo explicito ("como foi o mes") = mes corrente fechado ate hoje. Diga qual
   janela usou na resposta.
3. Varias unidades sem filtro = resultado agregado. Se o usuario citou uma clinica pelo nome,
   resolva o id antes, nao some tudo.

## Roteamento pergunta -> tool

| Pergunta do usuario | Tool | Observacao |
|---|---|---|
| "Como foi o mes da unidade X?" | `clinicorp_painel` | Uma chamada ja traz receita, recebido, conversao, ticket medio, agendamentos, faltas e novos pacientes |
| "Quanto a clinica X faturou?" | `clinicorp_painel` ou `clinicorp_resumo_financeiro` | Painel para visao gerencial; resumo para o recorte contabil do periodo |
| "Quanto de dinheiro entrou de fato?" | `clinicorp_pagamentos` | Regime de caixa — atencao ao tipo de data (abaixo) |
| "Como esta o caixa / vai fechar no azul?" | `clinicorp_fluxo_caixa` | Traz realizado e projetado; saldo = entradas menos saidas |
| "Quanto temos a receber em atraso?" | `clinicorp_inadimplencia` | Devolve previsto, recebido e valor em aberto |
| "Nossa taxa de conversao caiu?" | `clinicorp_conversao` | Serie por mes, com ticket medio junto |
| "Quais orcamentos estao abertos?" | `clinicorp_orcamentos` | Listagem; use `clinicorp_orcamento_detalhe` para abrir um caso |
| "Por que esse orcamento nao fechou?" | `clinicorp_orcamento_detalhe` | Procedimentos, valores e status do tratamento |
| "A agenda esta cheia?" / "temos espaco?" | `clinicorp_ocupacao` | Calculo oficial do Clinicorp; `clinicorp_agenda` so para conferir item a item |
| "Quantas faltas tivemos?" | `clinicorp_kpis_agenda` ou `clinicorp_painel` | KPIs traz faltas, primeiras consultas e finalizados |
| "O que tem na agenda de amanha?" | `clinicorp_agenda` | Listagem detalhada por periodo |
| "Qual o historico desse paciente?" | `clinicorp_buscar_paciente` + `clinicorp_agendamentos_paciente` | Busque o paciente antes; nao chute id |
| "Quem faz aniversario hoje?" | `clinicorp_aniversariantes` | Base para acao de relacionamento |
| "Batemos a meta?" | `clinicorp_metas` | Meta de venda, realizado e projecao; meta de falta so via `clinicorp_get` (operational/list_misses_goals) |
| "Quais profissionais atendem na unidade?" | `clinicorp_profissionais` | Resolve nomes antes de filtrar por profissional |

Quando a pergunta e de diagnostico ("por que caiu?"), comece pelo `clinicorp_painel` para achar
qual indicador se moveu e so entao desca para a tool especifica. Evita 5 chamadas as cegas.

## Tres exemplos completos

**1. Panorama — "como foi julho?"**

`clinicorp_painel` com `from=2026-07-01`, `to=2026-07-31`. Retorno traz, por unidade,
`receita`, `recebido`, `conversao`, `ticket_medio_aprovado`, `agendamentos`, `faltas`.
Resposta: "Em julho (01 a 31/07) a Matriz fez R$ 412 mil em venda aprovada, com R$ 190 mil
efetivamente recebidos no mes — a diferenca e o parcelamento, nao perda. Conversao de 38% e
ticket medio de R$ 6.480. 214 agendamentos com 24 faltas (11%)."

**2. Diagnostico — "por que caiu esse mes?"**

Nao saia chamando cinco tools. Comece pelo `clinicorp_painel` do mes atual e do anterior e
compare para achar **qual** indicador se moveu. Se caiu a conversao, desca para
`clinicorp_conversao` (serie por mes) e depois `clinicorp_orcamentos` com `status=REJECTED`
para ver o que nao fechou. Se caiu o volume de agendamento, o caminho e `clinicorp_kpis_agenda`
(primeiras consultas e faltas) e `clinicorp_ocupacao`. Diga na resposta qual indicador explicou
a queda e qual nao se moveu — descartar hipotese e parte da resposta.

**3. Caixa — "quanto entrou de dinheiro em agosto?"**

`clinicorp_pagamentos` com `base_data=recebimento` (padrao) e `apenas_recebidos=true`.
Resposta: "Entraram R$ 203.400 em agosto, contando pela data de recebimento. Desse total,
62% em cartao de credito. Atencao: isso e caixa, nao venda — o que foi **vendido** em agosto
esta em `clinicorp_painel` e da outro numero."

## Regras que evitam resposta errada

**Ocupacao sem compromissos e sempre subestimada.**
`clinicorp_agenda` sem `incluir_compromissos` nao enxerga bloqueios de agenda, reunioes e
horarios travados. O denominador fica errado e a clinica parece mais vazia do que esta.
Para qualquer conta de capacidade, inclua compromissos — ou use `clinicorp_ocupacao`, que ja e
o calculo oficial. Se os dois divergirem, o oficial manda; a divergencia costuma ser eventos de
dia inteiro entrando na soma manual.

**Sincronizacao e auditoria precisam de cancelados e excluidos.**
Sem eles, um agendamento cancelado simplesmente some da resposta e continua vivo na base local —
vira fantasma. Sempre que a tarefa for comparar, reconciliar ou espelhar dados, inclua cancelados
e excluidos e trate a flag de cancelamento explicitamente. Para responder "o que acontece amanha",
o padrao (so ativos) e o certo.

**`clinicorp_pagamentos`: a escolha da data muda o numero inteiro.**

| Data usada | Responde a pergunta |
|---|---|
| Recebimento (padrao) | "Quanto dinheiro entrou no caixa no periodo" — regime de caixa, conciliacao contabil |
| `postDate` (lancamento) | "Quando o lancamento foi criado no sistema" — auditoria de digitacao |
| `checkoutDate` (pagamento/checkout) | "Quanto foi vendido e fechado no periodo" — acompanhamento comercial |

Detalhe dos campos de pagamento: `references/api-clinicorp.md` secao 7.10.

Nunca compare um mes calculado por recebimento com outro por checkout. Ao apresentar o valor,
diga qual criterio usou.

**Endpoints agregados nao aceitam periodo fatiado.**
Painel, fluxo de caixa, conversao, resumo financeiro, ocupacao e metas devolvem indicadores ja
calculados: taxa de conversao, ticket medio, percentual de ocupacao. Somar ou mediar as fatias
produz numero falso — media de medias nao e media. Peca o periodo inteiro de uma vez.
Endpoints de listagem (agenda, orcamentos, pagamentos analitico) podem e devem ser fatiados:
a API nao tem paginacao, entao periodos longos em clinica de alto volume vao por janelas de
1 a 3 meses e sao concatenados depois.

**Fuso: agendamento e evento nao usam a mesma referencia.**
Agendamentos trazem data/hora em UTC — precisa converter para o fuso da clinica antes de exibir
ou de contar "quantos atendimentos na terca". Um agendamento de 21h em Brasilia aparece no dia
seguinte em UTC e desloca a contagem diaria. Eventos e compromissos ja vem no fuso da clinica —
nao converta esses de novo, ou o erro dobra. Os quatro formatos de data que a API usa estao em
`references/api-clinicorp.md` secao 3.3.

**Conta de grupo exige a clinica; conta unica nao.**
Em franquia, esquecer o identificador da unidade retorna 401 ou mistura unidades. Algumas rotas
financeiras (fluxo de caixa, inadimplencia, parcelamento medio) exigem a clinica sempre, mesmo
em conta unica. Se a chamada falhar por autorizacao, o primeiro suspeito e a unidade faltando,
nao o token. Quais rotas exigem a unidade: `references/api-clinicorp.md` secao 9.8.

## Nomes que a API erra

Com as tools dedicadas isso e transparente. Ao usar `clinicorp_get`, os campos voltam com os
typos originais — procure por eles, nao pela grafia correta:

| Campo real na resposta | Grafia esperada | Onde |
|---|---|---|
| `Ocupaccion` | Occupation | ocupacao da agenda |
| `FirsAppointmentTotal` | First | KPIs de agendamento |
| `AppoinmentsFinished` | Appointments | painel analitico |
| `StatusDescrition` | Description | status de agendamento |
| `ShedulingAccepted` / `ShedulingReason` | Scheduling | detalhe de agendamento |
| `SubscriberBussinessUID` | Business | listagem de unidades da franquia |

Duas rotas tambem tem typo no caminho: `get_avaliable_days` e `get_avaliable_times_calendar`
(avaliable, nao available). Alem disso, o mesmo conceito muda de grafia entre rotas —
id de clinica aparece como `business_id`, `businessId` e `Clinic_BusinessId`. Nunca reaproveite
o mesmo dicionario de parametros entre endpoints diferentes.

## Interpretacao de negocio

As faixas abaixo sao **referencia setorial, nao meta da clinica**. Servem para dizer se um numero
merece atencao — nunca as apresente como objetivo definido. O parametro que vale e o historico da
propria clinica: antes de chamar um numero de bom ou ruim, compare com os meses anteriores dela
(`clinicorp_painel` em dois periodos resolve).

**Taxa de conversao** (orcamentos aprovados sobre apresentados). Em clinica odontologica,
30-40% e faixa comum, acima de 50% e forte, abaixo de 25% costuma indicar problema de
apresentacao do plano de tratamento ou orcamento inflado, nao falta de paciente. Conversao alta
com ticket baixo pode significar que so o simples esta sendo vendido.

**Ticket medio.** Sempre diga se e ticket de orcamento aprovado ou de valor recebido — sao
numeros diferentes. Um caso reabilitador isolado distorce a media do mes; se a amostra e pequena,
mencione isso em vez de tratar a variacao como tendencia.

**Ocupacao.** 70-85% e saudavel. Perto de 100% nao e bom sinal: significa zero folga para
urgencia e retorno, e costuma vir acompanhado de atraso e falta. Abaixo de 60% e capacidade
ociosa paga. Compare sempre com compromissos incluidos, senao o numero e ficcao.

**Faltas / no-show.** Ate 10% e tolerado; acima de 15% e problema operacional de confirmacao.
Leia junto com primeiras consultas: falta alta em primeira consulta e problema de captacao e
confirmacao; falta alta em retorno e problema de vinculo e agendamento longo demais.

**Inadimplencia.** Valor em aberto sobre previsto. Interprete junto ao parcelamento: clinica que
vende em 10x tem inadimplencia estrutural maior e isso e esperado, nao deterioracao.

**O erro de leitura mais comum:** comparar faturamento por competencia (venda aprovada no mes)
com dinheiro recebido no mes. Numa clinica que vende em 10x, o orcamento de 10 mil fechado hoje
entra como 10 mil de venda e como 1 mil de caixa. Ver "receita caiu" olhando o caixa de um mes
em que a venda cresceu e diagnostico invertido. Sempre nomeie qual dos dois esta na mesa, e ao
comparar meses, mantenha o mesmo criterio dos dois lados.

## LGPD

A API trafega dado pessoal sensivel de saude: nome, CPF, telefone, data de nascimento,
procedimentos e motivo da consulta.

- Agregado e o padrao. Responda com numeros, faixas e contagens; nao despeje lista de pacientes.
- Dado nominal so quando o usuario pede explicitamente e para um caso concreto (confirmar
  agenda, ligar para um paciente, tratar um orcamento especifico).
- Nunca traga CPF, telefone ou data de nascimento sem que sejam necessarios para a tarefa.
  Busca de paciente por CPF e vetor de enumeracao — use com um alvo definido, nao para varrer.
- Nao persista listas de pacientes em arquivos, relatorios ou artifacts sem o usuario pedir.

## Antes de entregar a resposta

Confira os cinco itens. Cada um corresponde a um erro que ja aconteceu:

1. **Unidade resolvida** — a resposta e da unidade que a pessoa perguntou, nao a soma da rede.
2. **Janela declarada** — o texto diz qual periodo foi consultado, com as datas.
3. **Criterio de data declarado** — em pagamento, esta escrito se e recebimento, lancamento
   ou checkout.
4. **Competencia x caixa nomeado** — esta claro se o numero e venda aprovada ou dinheiro que
   entrou. Nunca deixe o leitor adivinhar.
5. **Agregado por padrao** — nao ha lista de paciente na resposta sem que tenha sido pedida.

Se algum item nao se aplica, tudo bem. O que nao pode e passar batido.

## Fallback

Para endpoints sem tool dedicada (procedimentos, especialidades, cadeiras, notas fiscais,
recibos, parcelamento medio, faturamento por convenio, campanhas de CRM, usuarios), use
`clinicorp_get` com o caminho do endpoint. Parametros, formatos de data, flags booleanas no
formato string "X" e o schema de resposta de cada rota estao em `references/api-clinicorp.md`.
