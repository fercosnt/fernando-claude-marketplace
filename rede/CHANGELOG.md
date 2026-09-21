# Changelog

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
