# Status — o que está pronto e o que falta

Atualizado em **2026-09-22**. Este arquivo existe para retomar o trabalho sem reconstruir o
contexto. Detalhe técnico fica nos docs apontados; aqui é o estado.

## Em uma linha

O plugin de **conciliação** está **em produção, publicado e conferido contra o portal da Rede** nas
duas unidades da clínica (Matriz e Hirata) desde 2026-09-21: vendas, resumos, pagamentos,
recebíveis e a conciliação venda ↔ pagamento, todos com dado real. A API de **Link de
Pagamento** foi mapeada e testada, mas por decisão não virou tool: vai virar workflow n8n.

## Pronto e validado

| Item | Estado |
|---|---|
| Servidor MCP, 29 tools de leitura | Pronto. `servers/rede-mcp.js`, bundle sem dependências |
| OAuth com renovação automática | Pronto. `client_credentials` ou `password`, escolhido pelo arquivo de config |
| Validação de janela de data por rota | Pronto. 62/60/30 dias, com as fatias sugeridas no erro |
| Tradução dos códigos da Rede | Pronto. 60+ bandeiras, status, produtos, traduzidos ao lado do original |
| Conciliação venda ↔ pagamento | Pronto. Cruza pelo `saleSummaryNumber` via ordens de crédito |
| Fallback automático v2 → v1 em vendas | Pronto. Nasceu do 403 do sandbox |
| 3 skills + 2 references + 5 docs | Pronto |
| 54 testes offline | Passando |
| 119 testes de integração (API simulada) | Passando. Mock coerente desde a v0.1.4: uma fonte só (vendas → cronograma em dia útil → ordens, pagamentos, recebíveis, débitos, bloqueios) |
| `claude plugin validate` | Passando |
| Produção (Matriz e Hirata) | **Funcionando** desde 2026-09-21 — login, consultas e conciliação com dado real |
| Teste contra o sandbox real da Rede | Feito. Vendas, parceladas, pagamentos, ordens de crédito e débitos respondendo com dado real |

## Falta fazer

### Para usar na clínica

1. ~~Pedir credenciais de produção~~ — **feito em 2026-09-21.** Login ok, escopo `merchant-statement`,
   configurado em `~/.rede-mcp.json`. Parceiro cadastrado como *Clinica Dental Laser LTDA*.
   PVs: **96504463 (Matriz)** e **106119095 (unidade Hirata)**, filial da Matriz.
2. ~~Criar a solicitação de acesso~~ — **feita por API em 2026-09-21 15:39.** Tipo Total na Matriz,
   permissão Leitura; a Rede incluiu a Hirata automaticamente.
   `requestId`: `5633825c-e466-43b9-8e77-82baa667d649` — status **PENDENTE**.
   Cópia da resposta em `~/.rede-mcp/solicitacao-acesso.json`.
3. ~~Aprovar a solicitação~~ — **aprovada em 2026-09-21 16:02** pela área do lojista. Status
   `APROVADO`, Total, Leitura, cobrindo Matriz e Hirata.
4. ~~Primeira consulta real~~ — **feita.** Setembro (1 a 20): Matriz R$ 95.750,00 bruto em 11 vendas,
   Hirata R$ 20.000,00 em 3. O resumo somado bate centavo a centavo com a lista detalhada.
   `Insufficient access level` sumiu com a liberação.
5. ~~Conferir um número contra o extrato do portal~~ — **conferido pelo Fernando em 2026-09-21.**
   Setembro (1 a 20) bate em valor e quantidade nas duas unidades: Matriz R$ 95.750,00 em 11 vendas,
   Hirata R$ 20.000,00 em 3. Os relatórios do plugin podem ser usados sem conferência manual.
6. ~~Investigar o RV 21230662~~ — **explicado em 2026-09-21, não é erro.** A venda do RV (R$ 7.350,
   Visa, 03/08) está intacta. O depósito de 03/09 veio R$ 526,32 menor porque a Rede descontou dele
   um **estorno parcial de outra venda**: NSU 185587562, R$ 6.000 em 10x no Mastercard (24/07),
   estornada em 90% em 01/09. A 1ª parcela já tinha sido paga cheia (R$ 584,82) e passou a valer
   R$ 58,48; a diferença (R$ 526,34, arredondada a R$ 526,32) foi recuperada no depósito seguinte,
   ajuste código 18 "cancelamento de vendas", aviso 326244171056281. As 9 parcelas restantes já
   estão reduzidas para R$ 58,48.
7. ~~Conciliação explicar divergência sozinha~~ — **feito na v0.1.3.** Cada resumo divergente tem os
   débitos do depósito consultados; se fecham a conta, vira `ajuste_no_repasse` com o ajuste nomeado
   e, para estorno, a venda de origem. Rodado de novo em produção: o RV 21230662 saiu explicado sem
   ajuda (estorno da NSU 185587562) e agosto ficou com **zero** divergências nas duas unidades.

### Do plugin em si

4. ~~Rodar os evals~~ — **iteração 2 em 2026-09-22: 95% com skill × 86% sem** (42 asserções, 9
   casos). Separaram 3 evals (dedução de estorno, liberação de PV na ida para produção e o 401 que
   não é credencial), contra 2 na iteração 1. A crítica dos avaliadores achou 13 defeitos no texto
   da skill, corrigidos na v0.1.4. Ver [evals/benchmark-iteracao-2.md](evals/benchmark-iteracao-2.md)
   (e o [da iteração 1](evals/benchmark-iteracao-1.md)).
   **Próximo:** as dívidas novas do mock e os reforços de eval listados no benchmark, com a linha
   de base vendo as instructions do servidor (o `list` do harness já mostra).
5. ~~Publicar no marketplace~~ — **publicado em 2026-09-21** (v0.1.1), depois da validação em
   produção, e instalado no Claude Code. Este diretório do marketplace é a fonte; o
   `skill-prompt/plugins/rede` é só um symlink.
6. ~~Conciliação em dados reais~~ — **validada em 2026-09-21** com as vendas de agosto: 7 resumos
   conciliados na Matriz, 2 na Hirata. O teste revelou que venda parcelada com parte das parcelas
   paga caía como "divergente"; corrigido com o grupo `parcelado_em_andamento` (v0.1.1).
7. **`base_nsu`** — só preencher se `rede_vendas_por_nsu` der 404 em produção.

### Link de Pagamento

8. **Montar o workflow n8n — próxima sessão** (combinado em 2026-09-21). É o destino escolhido. O que importa para montar (credencial OAuth2
   do n8n, a armadilha da data `MM/DD/YYYY`, polling sem webhook) está em
   [docs/payment-link.md](docs/payment-link.md).
9. **Credencial separada** de um projeto do pacote *Payment Link* em produção.
10. **Testar `cancel` e `details` em produção** — ambos inservíveis no sandbox (`cancel` quebrado,
    `details` mockado).
11. Se um dia virar tool MCP: prévia obrigatória + `confirmar=true`, já decidido.

## Decisões tomadas (para não reabrir)

- **Plugin com MCP local dentro**, não MCP solto: um MCP puro não carrega skills nem docs e não é
  distribuível pelo marketplace.
- **Sem camada de escrita** na conciliação — a API da Rede não tem rota que altere nada.
- **Link de Pagamento vai para o n8n**, não para tool: precisa rodar sozinho, disparado pelo CRM.
  O Claude fica com a análise e a conciliação.
- **Publicar só depois de validar em conta real** — o conta-azul precisou de um v0.1.1 logo após o
  v0.1.0 justamente por isso.
- **Prévia obrigatória** se o Link de Pagamento virar tool, porque cria cobrança real.

## Armadilhas já pagas (não redescobrir)

Estas custaram tempo e estão resolvidas no código ou documentadas:

1. **Credencial de Payment Link ≠ de Conciliação.** Cada uma autentica normalmente e recebe 401 nas
   rotas da outra. O escopo do token denuncia: `payment-link` vs `merchant-statement`.
2. **`client_credentials` funciona**, apesar de o PDF de 2023 só descrever `password`. A doc de
   Autenticação de 2024 confirma. Não é preciso esperar usuário/senha da Rede.
3. **`403 "Requisição inválida"` = rota não habilitada** para o aplicativo, não filtro errado.
4. **`400 "This scenario is not available in the sandbox"`** — formato de erro fora do swagger.
   `/v1/payments` exige um filtro do roteiro (`size` 1/5/10, `status`, `brands`, `types`).
5. **`groupBy` muda de caixa por rota** — MAIÚSCULO em vendas v1, minúsculo em pagamentos v2.
6. **`SCHEDULLED`** (parcela, dois L) vs **`SCHEDULED`** (recebível, um L).
7. **`expirationDate` do Link de Pagamento é `MM/DD/YYYY`** — falha silenciosa para dia < 13.
8. **O swagger erra o nome do PV na v2 de vendas** — diz `parentMerchantId`, produção exige
   `parentCompanyNumber`. Invisível no sandbox, onde a v2 inteira dá 403. Corrigido na v0.1.1.
9. **O resumo de vendas vem um item por dia** — ler o primeiro como total dá o valor de um dia só.
   Corrigido: `total_do_periodo` já somado.
10. **Parcelado pago pela metade não é divergência** — o crédito parcelado cai uma parcela por mês.
    Corrigido: grupo `parcelado_em_andamento` na conciliação.
11. **O sandbox só tem dado em novembro de 2022**, nos PVs 13381369 e 22523510 (e 1254405 para NSU).
12. **"Pago sem venda" não é só venda anterior.** Com a janela de pagamento esticada em 40 dias,
    débito e crédito do começo do mês seguinte caem nesse grupo. Corrigido na skill e no `como_ler`
    da conciliação (v0.1.4).
13. **Na lista de pagamentos vem o que não caiu.** `SUSPENDED`, `BLOCKED` e `RETAINED` aparecem junto
    dos `PAID`; "quanto caiu" soma só os pagos (v0.1.4).

## Mapa dos arquivos

| Arquivo | Para quê |
|---|---|
| [README.md](README.md) | Visão geral e instalação |
| [docs/producao.md](docs/producao.md) | **Como obter credenciais e liberar PVs** |
| [docs/ferramentas.md](docs/ferramentas.md) | As 29 tools, uma a uma |
| [docs/credenciais.md](docs/credenciais.md) | Onde guardar e como o token funciona |
| [docs/testes.md](docs/testes.md) | O que é testado e o que o sandbox responde |
| [docs/payment-link.md](docs/payment-link.md) | A segunda API, mapeada e testada |
| [docs/referencia/](docs/referencia/) | Swagger oficial do Link de Pagamento |
| [skills/rede/references/endpoints.md](skills/rede/references/endpoints.md) | Mapa tool → rota |
| [skills/rede/references/dominios.md](skills/rede/references/dominios.md) | Tabelas de código |

## Outras APIs da Rede (não exploradas)

O portal publica swagger de: `chargeback`, `credenciamento`, `erede` (e-commerce),
`gestao-acessos`, `gestao-vendas`, `numero-logico`, `payment-link-api`, `qr-code`. Padrão da URL:
`https://developer.userede.com.br/dev-portal-swaggers/<slug>/swagger.json`. Docs em
`https://developer.userede.com.br/files/documentacoes/<slug>/<arquivo>.md` — o portal é SPA, esses
caminhos saem do bundle `main.js`.
