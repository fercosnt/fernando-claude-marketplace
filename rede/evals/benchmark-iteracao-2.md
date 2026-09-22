# Benchmark: rede — iteração 2

**Data:** 2026-09-22 · **Versão:** 0.1.3 nas execuções; as correções da crítica viraram a 0.1.4
**Evals:** 9 casos, 1 execução por configuração, 42 asserções
**Método:** o mesmo da iteração 1 (skill-creator, caminho C). Cada caso roda em dois subagentes contra
a API simulada (`test/mock.mjs`, hoje = 2026-09-30), que agora é coerente (ver "Dívidas do mock"):

- **com skill:** lê `rede`, `rede-conciliacao` e `rede-setup` antes de responder; no eval 9, lê também
  a skill `conta-azul`;
- **sem skill:** conta só com as tools e as descrições delas.

O eval 9 usa também `evals/harness/conta-azul.mjs`, a API simulada do plugin conta-azul com o mesmo
"hoje". A correção foi feita por 18 avaliadores independentes, um por execução, seguindo
`agents/grader.md` e sempre com a seção de crítica. Cada um leu a resposta final, a lista de comandos
e o log da API, e conferiu os números rodando o mesmo CLI. Os avaliadores das execuções com skill
leram também as skills, para dizer de onde vinha cada erro.

## Resultado

| Métrica | Com skill | Sem skill | Diferença |
|---|---|---|---|
| Asserções | **95%** (40/42) | 86% (36/42) | +9,5 pontos |
| Tempo médio | 197s | 195s | +2s |
| Tokens médios | 131k | 118k | +13k |

| Eval | Com skill | Sem skill | Tempo com / sem | Tokens com / sem |
|---|---|---|---|---|
| 1 vendido não é recebido | 5/5 | 5/5 | 157s / 160s | 130k / 114k |
| 2 "quanto rendeu" (pergunta ambígua) — novo | 5/5 | 5/5 | 187s / 209s | 136k / 126k |
| 3 depósito menor por estorno de outra venda | 5/5 | **4/5** | 191s / 155s | 129k / 112k |
| 4 parcela paga dentro de um pacote — novo | 4/4 | 4/4 | 121s / 107s | 122k / 107k |
| 5 conciliação com parcelado e estorno | 4/6 | 4/6 | 261s / 171s | 140k / 118k |
| 6 feriado sem venda não é erro | 3/3 | 3/3 | 102s / 169s | 117k / 101k |
| 7 produção sem segredo no chat | 6/6 | **5/6** | 206s / 239s | 121k / 112k |
| 8 erro 401 não é credencial | 4/4 | **2/4** | 181s / 268s | 127k / 123k |
| 9 "quanto tenho a receber?" com Conta Azul — novo | 4/4 | 4/4 | 370s / 280s | 160k / 153k |

## Comparação com a iteração 1

| | Iteração 1 | Iteração 2 |
|---|---|---|
| Casos / asserções | 8 / 31 | 9 / 42 |
| Com skill | 100% | 95% |
| Sem skill | 91% | 86% |
| Diferença | +9 pontos | +9,5 pontos |
| Evals que separaram | 2 (1 e 7) | 3 (3, 7 e 8) |
| Custo da skill | +12s, +13k tokens | +2s, +13k tokens |

Os números não se comparam um a um: o mock mudou, três evals são novos e cinco foram reforçados. O
que dá para comparar é **onde** a skill fez diferença:

- **Eval 1** (o único mantido igual) separou na iteração 1 e empatou agora. A asserção que separou
  era "débito D+1, crédito D+30", e isso está nas *instructions* do servidor MCP, que o harness não
  mostrava (ver "Método"). O empate de agora é o resultado mais honesto.
- **Eval 3** separou pela asserção nova de dedução. Sem skill, a resposta disse "a Rede usou esse
  depósito para descontar o cancelamento da venda de 20/06", tirando o "provável" que a tool dava.
- **Eval 7** separou de novo, agora pela liberação do PV. Sem skill, a resposta pediu "me passe os
  números que eu acrescento no arquivo", sem dizer que cada PV precisa de solicitação e aprovação.
- **Eval 8** (variante 401) separou mais que todos. Sem skill, a resposta acertou "não gere secret
  novo", mas só porque o login funcionava no mock. Pôs "sessão vencida" como causa nº 1 (o plugin já
  renova o token sozinho) e não disse que credencial errada falha no login.
- **Eval 5** empatou por baixo: as duas execuções perderam as mesmas duas asserções. Na execução com
  skill, as duas falhas vieram do texto da skill (defeitos 3 e 4 abaixo).

## Leitura

**A diferença continua pequena e mora onde a iteração 1 disse:** no conhecimento que não está em
tool nenhuma. São a semântica dos erros da Rede, o caminho de produção e a linguagem de dedução.
Onde a tool já entrega a resposta pronta, as duas configurações acertam. É o caso de
`total_do_periodo`, `provavel_origem`, `parcelado_em_andamento`, do `como_ler` de consulta vazia e do
`paymentId` da parcela. Os avaliadores repetiram isso em 7 dos 9 evals.

**As armadilhas novas do mock não separaram, e isso diz algo do modelo, não da skill.** O depósito
suspenso de R$ 780 (eval 2) foi visto e deixado fora do "recebido" pelas duas configurações, e a
skill nem ensinava isso. O pacote de 08/09 (eval 4) foi aberto pelas duas.

**A disputa com o Conta Azul (eval 9) passou "no limite" nas duas.** As duas respostas abriram com
um total somado (R$ 21.805 com skill, R$ 21.025 sem), depois de conferir que não havia sobreposição.
Nenhuma das quatro skills falava da outra fonte, e a skill `rede` reivindicava "quanto tenho a
receber?" sozinha. Corrigido na 0.1.4 (defeito 12). Os dados de teste não têm nenhuma venda de
cartão lançada no ERP, então a dupla contagem ainda não é testável (ver "Evals a reforçar").

**O custo da skill:** cerca de 13k tokens a mais por pergunta, gastos em ler as skills. O tempo ficou
igual.

## Defeitos que a crítica achou na skill (corrigidos na v0.1.4)

Nenhum mudou nota sozinho, mas todos estavam no texto da skill e levaram a resposta a errar ou a
afirmar sem base. Estão na ordem de gravidade.

1. **"Pago sem venda" mandava olhar só para trás** (eval 5, execução com skill e avaliador). A skill e
   o `como_ler` da tool diziam "a venda é anterior ao período: estique `venda_inicio`". Na conciliação
   de julho, 3 dos 4 casos eram vendas **posteriores** (03/08, 07/08 e o débito de 01/09) pagas dentro
   da janela de +40 dias. A execução só acertou porque consultou agosto e setembro por conta própria.
2. **O exemplo de estorno era a resposta do eval** (avaliadores dos evals 3 e 5, com skill). O "como
   dizer a origem" citava a NSU 111008 de 20/06, que é exatamente o dado do mock, e dizia "dois dias
   antes do depósito" quando agora é um. Por isso as asserções do estorno mediam cópia. Trocado pelo
   caso real de produção, sem NSU.
3. **A ressalva virou tarefa** (eval 5, com skill). "Apresentar a origem como certeza é errado" virou
   "se ninguém na clínica lembra de ter devolvido R$ 100, vale conferir", com o estorno registrado na
   API. A skill agora diz que a ressalva é sobre a ligação débito ↔ venda, não sobre o estorno.
4. **Janela declarada, não justificada** (eval 5, com e sem skill). A skill mandava "diga qual
   janela". A resposta disse a janela, mas não disse por que ela passa do fim de julho. E declarou até
   30/09 quando o cruzamento usou até 09/09. A skill agora manda dizer o porquê e declarar a janela
   que o cruzamento usou.
5. **"Pacote" generalizado demais** (eval 4, com skill). "Agrupa parcelas de várias vendas" levou a
   "parcela quase nunca aparece sozinha" e "a de 08/10 provavelmente vem somada". Os dados dizem o
   contrário: a 1ª parcela caiu sozinha, e o único recebível de 08/10 é a parcela de R$ 292,50.
6. **Só o débito ia para o próximo dia útil** (eval 4, com skill). O crédito também vai, e é o que
   explica a venda de 07/08 ter caído em 08/09.
7. **"Quanto caiu na conta" não mandava somar só os pagos** (eval 2, com skill). A lista mistura
   `SUSPENDED`, e somar tudo dá R$ 2.130,75 em vez de R$ 1.350,75.
8. **Bloqueio com prazo inventado** (eval 2, com skill). "Quando liberarem, os R$ 780 entram na data
   da liberação": a API não traz nem motivo nem prazo.
9. **Erro de PV não liberado dito como regra geral** (eval 8, com skill). "A mensagem costuma ser
   Partner not allowed for this merchant, código 1001". Em produção, nas vendas foi 403. O 401 com
   código 1001 foi nos recebíveis v3, e o "Insufficient access level" no resumo de pagamentos. Um 401
   nas vendas aponta primeiro para o pacote errado.
10. **Liberação do PV descrita pela metade** (eval 8, com skill). "Na área logada do lojista, peça o
    acesso e aprove como lojista": quem pede é o parceiro (portal ou API de Gestão de Acessos), e o
    lojista só aprova.
11. **Credencial de produção "no portal"** (eval 7, com skill). O passo 1 mandava gerar o secret de
    produção em *Meus Projetos*, o que contradiz o `docs/producao.md`: só o sandbox é self-service;
    produção é por e-mail.
12. **"A receber" sem a outra fonte** (eval 9, com e sem skill). Ver "Leitura".
13. **"204 vem com `vazio: true`"** (eval 6, com skill). O resumo devolve total zero e a lista com
    `paginar_tudo` devolve lista vazia. Também entrou "não invente causa para o vazio", porque a
    resposta especulou "provavelmente outra maquininha" a partir do buraco de vendas do mock.

A skill `rede` também deixou de dizer que a liberação do PV "é feita pela Rede", e a `rede-setup`
passou a mandar não declarar a configuração pronta quando o login de produção falha.

## Verificação da 0.1.4

Os dois evals em que as falhas vinham do texto da skill rodaram de novo, só com skill, com a 0.1.4 e
um avaliador novo para cada um. O `list` do harness já mostrava as instructions do servidor.

| Eval | 0.1.3 | 0.1.4 | Tempo | Tokens |
|---|---|---|---|---|
| 5 conciliação com parcelado e estorno | 4/6 | **6/6** | 261s → 245s | 140k → 142k |
| 9 "quanto tenho a receber?" com Conta Azul | 4/4, com total somado na manchete | 4/4, total só no fim e condicional | 370s → 260s | 160k → 140k |

- **Eval 5:** a resposta passou a justificar a janela ("crédito em D+30, uma parcela por mês") e a
  declarar a que o cruzamento usou (até 09/09). Deixou de pedir para a pessoa conferir o estorno.
  Explicou os "pagos sem venda" como depósitos de junho, agosto e setembro, e não inventou motivo
  para o depósito suspenso. O avaliador ainda achou o resumo do topo dizendo "o estorno é de uma venda
  de junho" sem a ressalva que o corpo trazia. A skill passou a dizer que a ressalva vale também para o
  resumo.
- **Eval 9:** Rede, suspenso e Conta Azul aparecem separados, e a soma só vem no fim, condicionada a
  "o cartão não é lançado no Conta Azul". A resposta afirmou "nenhum valor bate" sem ter consultado as
  vendas da Rede (há R$ 1.200 nos dois lados, em vendas diferentes). O CNPJ diferente do mock virou a
  pergunta "a maquininha é da clínica?"; é uma distração do mock, anotada nas dívidas.

Uma execução só por eval, então isto confirma a direção das correções, não mede o tamanho do efeito.

## Dívidas do mock da iteração 1: o que foi feito

O mock tem agora uma fonte só: a lista de vendas. Dela sai o cronograma de cada parcela (débito em
D+1, crédito em D+30 por parcela, no próximo dia útil, com os feriados nacionais). Do cronograma
saem ordens de crédito, pagamentos, recebíveis, débitos e bloqueios. Um bloco novo do teste de
integração confere que as rotas contam a mesma história.

| Dívida | Correção |
|---|---|
| Ordem única de R$ 850 da venda 3x | Sumiu. As 3 parcelas de R$ 292,50 vencem em 05/10, 03/11 e 02/12 e são recebíveis |
| 2ª parcela da 4x paga sem depósito, ids que não batiam | Paga em 08/09 no P20260908001, que existe como pagamento e como ordem, com o mesmo id da parcela |
| Pagamento `PAID` em 02/10 | Não existe pagamento depois de hoje; o que vence depois é recebível |
| Débitos, bloqueios e recebíveis sempre com o mesmo item | Filtram pelo período e voltam vazios quando não há nada |
| Estorno com o valor restante (400) | Traz o estornado (R$ 100), e a venda tem `statusType` PARTIAL |

Três incoerências que não estavam na lista também foram corrigidas: o depósito de 15/08 caía num
sábado (passou a 14/08), `/v1/sales/installments` devolvia uma linha por venda com vencimento fixo, e
`client_credentials` devolvia escopo `payment-link`, ao contrário do sandbox real. O teste de
integração foi de 84 para 113 verificações. Todo teste que mudou foi por dado alterado de propósito;
os casos estão no CHANGELOG da 0.1.4.

## Dívidas novas (corrigir antes da iteração 3)

Apontadas por executores e avaliadores:

- **Débito de estorno bruto.** O mock desconta R$ 100 por um estorno de R$ 100 numa venda com MDR de
  2,5%. Em produção, o débito foi o **líquido** (R$ 526,32 = 90% da parcela líquida). Sem skill, a
  resposta leu isso como "a Rede não devolveu a taxa de R$ 2,50".
- **O mock ignora o PV.** Qualquer número devolve os dados do 13381369 (evals 7 e 8). Para o eval 8
  ter um 401 de verdade, o mock precisa responder "Partner not allowed" para PV não liberado, ou
  emitir escopo `payment-link` num cenário.
- **Um mock novo a cada chamada do CLI.** O token guardado no run é desconhecido do mock seguinte, e
  então toda chamada faz `refresh_token` (que falha) e depois `password`. O caminho de refresh nunca
  roda nos evals; o teste de integração o cobre.
- **Dados esparsos.** Não há venda de 04 a 27/09, e isso levou a especulação ("outra maquininha").
- **Fixture do Conta Azul** (plugin conta-azul): as baixas da Liana se contradizem (3 × R$ 10 mil na
  parcela, 1 × R$ 30 mil na rota de baixas), o CNPJ é diferente do PV da Rede, e não há venda de
  cartão lançada no ERP. O `ca.mjs` de lá também não roda sem o SDK do MCP; por isso o wrapper
  `evals/harness/conta-azul.mjs`.

## Método: o que mudou e o que falta

- **A linha de base não via as instructions do servidor.** O `rede.mjs list` só mostrava as tools. Em
  produção, o cliente MCP põe no contexto as *instructions* do servidor, com ou sem skill, e elas já
  dizem "débito cai em D+1 e crédito em D+30" e a diferença entre venda, pagamento e recebível. Isso
  valeu para as duas iterações. Na iteração 1, parte da vantagem do eval 1 era esse artefato. Na
  iteração 2, nenhum dos evals que separaram depende dessas instructions: dedução, liberação de PV e
  semântica do 401 não estão lá. O `list` agora imprime as instructions (e o `conta-azul.mjs` também).
- **Uma execução por configuração.** A variação entre execuções não foi medida.
- **Os gabaritos dos evals 6, 7 e 8 tinham erro de fato,** apontado pela crítica. O 6 dizia "204" para
  uma rota que devolve 200 com lista vazia. O 7 dizia "trocar no portal" para o secret de produção. O
  8 dava o 401 código 1001 nas vendas, onde produção dá 403. Os gabaritos foram corrigidos no
  `evals.json`; as asserções ficaram como foram avaliadas.

## Evals a reforçar (iteração 3)

Sugestões dos avaliadores, para as asserções medirem o que só a skill ensina:

- **Eval 1:** as asserções 1 a 3 medem a tool. Cobrar o que cai de fato: líquido de MDR contra
  depositado, com o aluguel no meio.
- **Eval 2:** a asserção 5 está imprecisa (os R$ 317,25 são do débito de 01/09, venda de setembro). O
  gabarito aceita só perguntar, mas as asserções exigem os números. Cobrar o aluguel e "não inventa
  prazo de bloqueio".
- **Eval 3:** com o exemplo da skill trocado, a dedução deixa de ser cópia. Acrescentar uma asserção
  sobre o `salesSummaryNumber` do débito (900006, o resumo onde foi compensado, e não 900007) e exigir
  a base da dedução.
- **Eval 4:** cobrar o porquê do pacote (domingo e feriado) e a previsão das parcelas seguintes sem
  supor soma. A asserção 4 não discrimina.
- **Eval 5:** decidir se avisar do bloqueio real fora de julho conta como "pedir ação". Conferir que a
  janela declarada é a usada, e cobrar a composição do depósito de 08/09. A asserção 4 aprova uma resposta que
  afirma a origem do estorno como certeza (pedir a ressalva também no resumo do topo), e nenhuma
  asserção cobra a comparação dos totais (vendido R$ 2.200 × pago na janela R$ 3.005,75).
- **Eval 6:** mede a tool. Trocar por "quanto caiu na conta no feriado?": o que cairia em 06 e 07/09
  caiu em 08/09.
- **Eval 7:** a asserção 3 cita `~/.rede-mcp.json` ao pé da letra, mas no harness o arquivo é outro.
  Cobrar "não gravar o secret colado no chat", "não declarar pronto depois do 401", "trocar o PV do
  sandbox" e "canal certo da credencial de produção".
- **Eval 8:** o mock reproduzir o 401. Novas asserções: "diagnostica no ambiente em que o erro
  aconteceu" e "não atribui o 401 a token vencido".
- **Eval 9:** plantar uma venda de cartão também lançada no Conta Azul, para a dupla contagem ser
  testável, e cobrar os R$ 780 suspensos e o "tudo vencido" do ERP.

## Pergunta em aberto (fora dos evals)

A skill `rede` diz, sobre crédito parcelado: "uma parcela por mês, inclusive no parcelado com juros
(quem financia é o emissor; o lojista recebe como se fosse à vista em 30 dias)". A frase se contradiz.
No mercado, parcelado emissor quer dizer que o lojista recebe tudo em D+30. Não mexi sem ver um
parcelado com juros real na Rede.
