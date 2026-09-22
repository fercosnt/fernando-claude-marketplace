# Changelog

## 0.1.5 — 2026-09-22

- **Parcelado cai parcela a parcela.** A skill dizia que no parcelado com juros "o lojista recebe como
  se fosse a vista em 30 dias", e a frase se contradizia. Na clinica nao ha antecipacao: cada parcela
  cai no seu mes. A skill agora diz isso e manda conferir em `rede_parcelas_da_venda`.
- **Mensagens do servidor alinhadas com a skill.** O ALERTA de escopo `payment-link` dizia para criar
  projeto em *Meus Projetos*, o que so vale para o sandbox; e o erro 401/403 dizia que a liberacao do
  PV era "feita pela Rede". Agora: projeto novo no sandbox, pedido a Rede em producao; e o parceiro
  solicita, o lojista aprova.
- **Dividas do mock da iteracao 2** (`test/mock.mjs`):
  - o debito de estorno passa a ser liquido (R$ 97,50 por um estorno de R$ 100 com MDR de 2,5%), como
    em producao — o deposito de 14/08 fica em R$ 877,50;
  - PV diferente de 13381369 responde como PV nao liberado, com o erro de producao de cada rota (403
    nas vendas, 401 codigo 1001 nos recebiveis v3, 401 "Insufficient access level" no resumo de
    pagamentos), em vez de devolver os dados de outro PV;
  - credencial de projeto Payment Link: login ok, escopo `payment-link`, 401 em toda rota de extrato.
- Teste de integracao: 113 → 119 verificacoes (PV nao liberado por rota; cenario Payment Link numa
  segunda instancia do servidor). Os testes do debito mudaram porque o valor mudou de proposito.
- Harness: `REDE_CENARIO=payment-link` ou `pv-nao-liberado` muda a config do run. O eval 8 passa a
  rodar no cenario Payment Link, em que o 401 e real; evals 3 e 5 atualizados para o debito de R$ 97,50.

## 0.1.4 — 2026-09-22

Correcoes que vieram da critica dos avaliadores na iteracao 2 dos evals (ver
`evals/benchmark-iteracao-2.md`). Nenhuma mudou nota de assercao sozinha; todas estavam no texto da
skill e levaram a resposta a errar ou a afirmar sem base.

- **"Pago sem venda" nao e so venda anterior.** A skill e o `como_ler` de `rede_conciliar` mandavam
  esticar `venda_inicio` para tras. Com a janela de pagamento esticada em 40 dias, boa parte desse
  grupo e venda **posterior** ao periodo (debito e credito do comeco do mes seguinte) — na conciliacao
  de julho do teste, 3 de 4. Agora os dois dizem "de fora do periodo, anterior ou posterior" e
  mandam abrir o deposito com `rede_parcelas_do_pagamento`.
- **"Quanto caiu na conta" soma so os pagos.** A lista de pagamentos traz tambem `SUSPENDED`,
  `BLOCKED` e `RETAINED`; somar tudo contava dinheiro preso como recebido.
- **Bloqueio sem motivo inventado.** A API nao traz motivo nem prazo de liberacao; a skill passa a
  dizer isso.
- **Pagamento e pacote, mas pode ter uma parcela so.** A skill generalizava ("agrupa parcelas de
  varias vendas") e a resposta chegou a prever que a proxima parcela viria somada, contra os
  recebiveis. Agora manda achar o deposito pelo `paymentId` e prever pelos recebiveis do dia.
- **Credito tambem vai para o proximo dia util.** So o debito dizia isso.
- **Exemplo de estorno contaminava o eval.** O exemplo de "como dizer a origem" era a propria resposta
  da API simulada (e com a conta de dias errada). Troca pelo caso real de producao, sem NSU. A skill
  tambem avisa que o `salesSummaryNumber` do debito e o do resumo em que ele foi compensado, e que a
  ressalva sobre a origem nao vira tarefa para a pessoa ("confira", "ligue para a Rede") e vale
  tambem para o resumo no topo da resposta.
- **Janela da conciliacao: dizer por que.** Alem de declarar a janela, explicar por que ela passa do
  fim do mes, e declarar a que o cruzamento usou.
- **Erro por rota com PV nao liberado.** A skill dizia 401 codigo 1001 como regra geral; em producao
  foi 403 nas vendas, 401 1001 nos recebiveis v3 e 401 "Insufficient access level" no resumo de
  pagamentos. Um 401 nas vendas aponta primeiro para o pacote errado. Diagnosticar no ambiente em que
  o erro aconteceu.
- **Quem pede e quem aprova a liberacao do PV.** O parceiro pede (portal ou API de Gestao de
  Acessos) e o lojista aprova; a skill dizia "solicitacao e aprovacao na area do lojista".
- **Credencial de producao nao e self-service.** `rede-setup` mandava pegar e trocar o secret em
  *Meus Projetos*, que so vale para o sandbox; producao e por e-mail a Rede. E nao declarar a
  configuracao pronta se o login falhar.
- **"A receber" em dois sistemas.** Com um ERP instalado (Conta Azul), mostrar Rede e ERP separados,
  sem abrir com um total somado: a mesma venda pode estar nos dois.
- **204 conforme a tool.** Chega como `vazio: true`, lista vazia ou total zero; e nao se inventa causa
  para o vazio.

**API simulada coerente** (`test/mock.mjs`): uma fonte so, a lista de vendas, da qual saem cronograma
em dia util (com feriados), ordens de credito, pagamentos, recebiveis, debitos e bloqueios. Corrige
as dividas da iteracao 1: ordem unica de R$ 850 da venda 3x, 2a parcela da 4x paga sem deposito e com
ids que nao batiam, pagamento `PAID` no futuro, deposito num sabado, rotas de debitos, bloqueios e
recebiveis que devolviam sempre o mesmo item, evento de estorno com o valor restante (agora o
estornado, R$ 100) e `client_credentials` com escopo `payment-link`. Novos cenarios: deposito de
08/09 que junta duas vendas e deposito de 28/09 suspenso. Teste de integracao: 84 → 113 verificacoes,
com um bloco que confere a coerencia entre as rotas. Testes que mudaram porque o dado mudou de
proposito: 1a parcela da 3x em 05/10 (o D+30 caia num sabado); vendas parceladas com 6 linhas (uma por
parcela, como a tool descreve); pagamentos, debitos, bloqueios e recebiveis consultados no mes em que
existem (outubro e futuro); conciliacao de setembro com 0 conciliados (o credito de setembro vence em
outubro); julho com 2 de 4 parcelas pagas e R$ 585 a receber (a 2a venceu em 08/09); esperado de
R$ 975 no deposito de 14/08; cashback vazio (nenhum deposito teve).

**Evals:** iteracao 2 com 9 casos (2, 4 e 9 novos; 3, 5, 6, 7 e 8 reforcados). Com skill 95% (40/42),
sem skill 86% (36/42). Novo `evals/harness/conta-azul.mjs` para o eval de disputa com o Conta Azul, e
o `list` do harness passa a mostrar as instructions do servidor MCP, como em producao.

## 0.1.3 — 2026-09-21

- **`rede_conciliar` explica as divergencias sozinha.** Para cada resumo divergente, consulta os
  debitos do deposito; se fecham a diferenca, o resumo vira **`ajuste_no_repasse`** com o ajuste
  nomeado (`ajustes`). Para estorno, procura nos 6 meses anteriores a venda estornada e devolve
  `provavel_origem` (NSU, data, evento). O que continua em `valor_divergente` e o que de fato nao tem
  explicacao. Novo parametro `explicar_divergencias` (padrao true). Motivado pelo caso real do
  RV 21230662, que precisou de investigacao manual: estorno de outra venda descontado do deposito.
- Mock ganhou o cenario de estorno de outra venda; o antigo "divergente" do aluguel de R$ 27,50
  passa a sair explicado.
- **Evals rodados pela primeira vez** (8 casos, com skill x sem skill, contra a API simulada):
  100% x 91%. Ver `evals/benchmark-iteracao-1.md`. Os avaliadores acharam dois defeitos na skill,
  corrigidos aqui:
  - a origem de um estorno era dita como fato; e deducao por data (o debito nao traz o NSU) e agora
    a skill manda dizer assim;
  - ao ir para producao, a skill mandava trocar so ambiente, credenciais e PV — os `usuario`/`senha`
    do sandbox ficavam no arquivo e o login de producao cairia no grant password com o par de teste.
    A skill manda remover os dois, e `rede_status` e o erro `invalid_grant` passam a avisar.
- `rede_vendas_resumo` sem venda no periodo devolve total zero em vez de `null`.
- Novo harness de evals (`evals/harness/rede.mjs`), sem dependencias, contra `test/mock.mjs`.

## 0.1.2 — 2026-09-21

- **`rede_parcelas_da_venda` respondia 415 em producao.** A rota `/v2/payments/installments/{pv}`
  exige `Content-Type: application/json` mesmo sendo GET, sem corpo. O client agora envia o
  cabecalho em toda chamada. Achado ao investigar a primeira divergencia real da conciliacao.

## 0.1.1 — 2026-09-21, primeiro contato com producao

Credenciais de producao recebidas e testadas nos PVs reais. O login funciona (escopo
`merchant-statement`, 56 tipos de ajuste); as consultas ainda param na liberacao dos PVs, como
esperado. O teste revelou um erro no swagger oficial:

- **A v2 de vendas exige `parentCompanyNumber`, nao `parentMerchantId`.** O swagger manda usar
  `parentMerchantId`; producao responde `422 parentCompanyNumber: Missing data for required field`.
  Com `parentCompanyNumber` a validacao passa. A v2 agora envia os dois nomes, em `rede_vendas` e em
  `rede_conciliar`. No sandbox isso era invisivel, porque la a v2 inteira responde 403.
- **Mensagens especificas para as respostas de producao**: `Partner not allowed for this company
  number` (403) e `Partner not allowed for this merchant` (401, codigo 1001) agora dizem que o PV
  nao foi liberado e apontam o passo 2 de `docs/producao.md`; `Insufficient access level to access
  this feature` explica o nivel de permissao.
- **A API de Gestao de Acessos responde com a mesma credencial de Gestao de Vendas**, entao a
  solicitacao de acesso aos PVs pode ser feita por API.
- O mock passou a exigir `parentCompanyNumber` na v2, como a API real.
- **`rede_vendas_resumo` agora entrega `total_do_periodo` ja somado.** A Rede devolve um item por dia
  com venda, do mais recente para o mais antigo; ler o primeiro item como se fosse o total — que foi
  exatamente o que aconteceu no primeiro teste em producao — dava R$ 2.900 onde o certo era R$ 95.750.
  A skill dizia que o resumo "trazia o total de uma vez", o que induzia ao erro; corrigida tambem.
  Validado: a soma dos dias bate centavo a centavo com a lista detalhada nas duas unidades.
- **`rede_conciliar` validada com dado real** — cruzou 7 resumos na Matriz e 2 na Hirata (vendas de
  agosto). E revelou um erro de logica: venda **parcelada** com so a 1a parcela paga caia em "valor
  divergente" (ex.: previsto 10.270,05, pago 2.054,01 — exatamente 1/5). Agora ha o grupo
  **`parcelado_em_andamento`**, com `parcelas_pagas`, `parcelas` e `falta_receber`; o pago precisa ser
  multiplo inteiro da parcela. O mock ganhou uma venda 4x com 1 parcela paga para cobrir o caso.

## 0.1.0

Primeira versão. Servidor MCP local das APIs de Gestão de Vendas da Rede, com 29 tools de leitura,
três skills e documentação.

**Servidor**

- OAuth 2.0 com `grant_type=password` e renovação por `refresh_token`. Como o refresh da Rede vale
  só 24 horas, o login é refeito sozinho quando ele vence — sem reconexão manual.
- Trava de arquivo na renovação (Claude Code e Cowork podem subir dois servidores ao mesmo tempo).
- Tokens gravados com escrita atômica, permissão 600, separados por ambiente.
- Cliente HTTP com 3 tentativas em rede/429/5xx, renovação automática em 401 e mensagens de erro
  que explicam a causa provável em vez de repetir o status.
- Validação de janela de data por rota (62/60/30 dias) antes da chamada, com as fatias sugeridas
  no erro.
- Paginação por cursor com `paginar_tudo` e teto de 20 páginas.
- Tradução automática dos códigos da Rede (bandeira, modalidade, produto, status) ao lado do
  código original, sem sobrescrever nada.
- `rede_conciliar`: cruza vendas e ordens de crédito pelo `saleSummaryNumber`, fatiando as janelas
  sozinho e deslocando a janela de pagamento em 40 dias para alcançar o crédito em D+30.
- 204 tratado como "sem registro", não como erro.

**Skills**

- `rede` — julgamento de qual tool responde o quê, os três conceitos (venda, recebível, pagamento)
  e as armadilhas da API.
- `rede-setup` — credenciais e ambiente sem segredo no chat.
- `rede-conciliacao` — o fluxo do fechamento e como investigar divergência.

**Autenticação: o que a documentação não diz**

Validado contra o sandbox real em 2026-09-20:

- `grant_type=client_credentials` funciona com apenas client_id/secret e devolve token com escopo
  `merchant-statement`. A doc oficial só descreve `password`, que exige um par usuário/senha enviado
  por e-mail pelo time de Integrações. O plugin escolhe o grant sozinho e aceita o campo `grant`
  para forçar.
- Credencial de um projeto de *Payment Link* autentica normalmente, mas o token sai com escopo
  `payment-link` e **toda** rota de extrato responde 401. `rede_conectar` mostra o escopo e alerta.
- `403 "Requisição inválida"` significa rota não habilitada para o aplicativo — no sandbox, a v2 de
  vendas, os resumos, os recebíveis e os bloqueios respondem assim mesmo com credencial correta.
  `rede_vendas` detecta isso e cai sozinha na v1, avisando na resposta.
- `400 "This scenario is not available in the sandbox"` é um formato de erro fora do swagger; em
  `/v1/payments` o sandbox exige um filtro do roteiro (`size` 1/5/10, `status`, `brands`, `types`).

**Testes**

- 54 verificações offline (`node test/run.mjs`), sem tocar na API.
- 65 verificações de integração (`node test/integracao.mjs`) contra a API simulada em
  `test/mock.mjs`, cobrindo as 29 tools, a renovação de token e o cruzamento da conciliação — que o
  sandbox não permite provar, porque suas fixtures de venda e de ordem de crédito são independentes.
