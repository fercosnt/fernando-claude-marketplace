#!/usr/bin/env node
/**
 * Teste de integracao: as 29 tools contra a API da Rede simulada (test/mock.mjs).
 *
 * O que so da para provar aqui, e nao no sandbox da Rede:
 *  - o cruzamento da conciliacao, porque no sandbox os saleSummaryNumber de vendas e de ordens
 *    de credito sao conjuntos disjuntos (fixtures independentes) e nada concilia por construcao;
 *  - as rotas que o sandbox nao habilita (v2 de vendas, resumos, recebiveis, bloqueios);
 *  - a renovacao de token quando o access vence e quando o refresh e recusado;
 *  - o 204 virando "sem registro" em vez de erro.
 *
 * Uso: node test/integracao.mjs
 */
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { criarMock, invalidarTokens, chamadas, CREDENCIAIS, CENARIO } from "./mock.mjs";

const raiz = dirname(dirname(fileURLToPath(import.meta.url)));
const { servidor, porta } = await criarMock();
const base = `http://127.0.0.1:${porta}`;

const tmp = mkdtempSync(join(tmpdir(), "rede-integracao-"));
const configFile = join(tmp, "config.json");
writeFileSync(configFile, JSON.stringify({
  ambiente: "sandbox",
  client_id: CREDENCIAIS.CLIENT_ID,
  client_secret: CREDENCIAIS.CLIENT_SECRET,
  usuario: CREDENCIAIS.USUARIO,
  senha: CREDENCIAIS.SENHA,
  pvs: [{ nome: "Loja Teste", numero: CREDENCIAIS.PV }],
}));

const mcp = spawn("node", [join(raiz, "servers", "rede-mcp.js")], {
  env: {
    ...process.env,
    REDE_CONFIG_FILE: configFile,
    REDE_STATE_DIR: join(tmp, "estado"),
    // Aponta o servidor para o mock em vez da Rede de verdade.
    REDE_BASE_URL: base,
    REDE_TOKEN_URL: `${base}/oauth/token`,
    REDE_INTERVALO_MS: "0",
  },
  stdio: ["pipe", "pipe", "pipe"],
});

let buffer = "";
const pendentes = new Map();
mcp.stdout.on("data", (d) => {
  buffer += d.toString();
  let corte;
  while ((corte = buffer.indexOf("\n")) >= 0) {
    const linha = buffer.slice(0, corte).trim();
    buffer = buffer.slice(corte + 1);
    if (!linha) continue;
    try {
      const m = JSON.parse(linha);
      pendentes.get(m.id)?.(m);
      pendentes.delete(m.id);
    } catch { /* ruido */ }
  }
});
mcp.stderr.on("data", (d) => process.env.VERBOSE && process.stderr.write(`[mcp] ${d}`));

let proximoId = 1;
const enviar = (method, params) =>
  new Promise((resolve) => {
    const id = proximoId++;
    pendentes.set(id, resolve);
    mcp.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
    setTimeout(() => resolve({ timeout: true }), 20000).unref();
  });

const chamar = async (nome, args = {}) => {
  const r = await enviar("tools/call", { name: nome, arguments: args });
  const texto = r.result?.content?.[0]?.text ?? JSON.stringify(r);
  let json = null;
  try { json = JSON.parse(texto); } catch { /* erro vem como texto */ }
  return { erro: !!r.result?.isError, texto, json };
};

let passou = 0, falhou = 0;
const ok = (nome, cond, detalhe = "") => {
  if (cond) { passou++; console.log(`  ok   ${nome}`); }
  else { falhou++; console.log(`  FALHA ${nome}${detalhe ? ` — ${detalhe}` : ""}`); }
};

try {
  await enviar("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "integracao", version: "0" } });
  mcp.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");

  console.log("\nconexao");
  let r = await chamar("rede_conectar");
  ok("login com grant password", !r.erro && r.json?.conectado === true);
  ok("usa o grant password quando ha usuario e senha", r.json?.grant === "password");
  ok("consulta de teste passou", r.json?.consulta_de_teste?.ok === true);
  ok("sem alerta de escopo quando o escopo e merchant-statement", !r.json?.ALERTA);

  console.log("\nvendas");
  r = await chamar("rede_vendas", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  ok("lista as 5 vendas do periodo", r.json?.total_de_vendas === 5, String(r.json?.total_de_vendas));
  ok("seguiu as duas paginas do cursor", r.json?.paginas_lidas === 2, String(r.json?.paginas_lidas));
  ok("marcou a paginacao como completa", r.json?.completo === true);
  const v = r.json?.vendas?.[0];
  ok("traduziu a bandeira", v?.bandeira === "Visa" || v?.bandeira === "Mastercard", v?.bandeira);
  ok("traduziu o status da venda", v?.status_descricao === "Aprovada");
  ok("traduziu o produto dentro de modality", !!v?.modality?.produto_descricao, JSON.stringify(v?.modality));
  ok("preservou o codigo original", typeof v?.brandCode === "number");

  r = await chamar("rede_vendas", { data_inicio: "2026-09-01", data_fim: "2026-09-30", modalidade: "credito", paginar_tudo: true });
  ok("aceita modalidade em portugues e filtra credito", !r.erro && r.json?.total_de_vendas === 3, String(r.json?.total_de_vendas));

  r = await chamar("rede_vendas", { data_inicio: "2020-01-01", data_fim: "2020-01-31" });
  ok("204 vira 'sem registro', nao erro", !r.erro && r.json?.resposta?.vazio === true);
  r = await chamar("rede_vendas_resumo", { data_inicio: "2020-01-01", data_fim: "2020-01-31" });
  ok("resumo sem venda devolve total zero, nao null", r.json?.total_do_periodo?.valor_bruto === 0 && r.json?.total_do_periodo?.quantidade_de_vendas === 0, JSON.stringify(r.json?.total_do_periodo));
  ok("resumo sem venda diz que nao e erro", r.json?.como_ler?.includes("Nao e erro"));

  r = await chamar("rede_vendas_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30" });
  ok("resumo vem um item por dia com venda", r.json?.resposta?.content?.sales?.length === 4, String(r.json?.resposta?.content?.sales?.length));
  ok("total_do_periodo soma os dias (bruto 2.750)", r.json?.total_do_periodo?.valor_bruto === 2750, String(r.json?.total_do_periodo?.valor_bruto));
  ok("total_do_periodo conta as 5 vendas", r.json?.total_do_periodo?.quantidade_de_vendas === 5);
  ok("o primeiro item NAO e o total", r.json?.resposta?.content?.sales?.[0]?.amount !== 2750);
  ok("resposta explica como ler", r.json?.como_ler?.includes("nunca o primeiro item"));
  r = await chamar("rede_vendas_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30", agrupar_por: "DAY" });
  ok("agrupar_por forca a v1", r.json?.versao === 1);

  r = await chamar("rede_vendas_por_nsu", { data_inicio: "2026-09-01", data_fim: "2026-09-30", nsu: 111003 });
  ok("filtra pelo NSU", r.json?.resposta?.content?.salesDaily?.[0]?.sales?.[0]?.nsu === 111003);

  r = await chamar("rede_parcelas_da_venda", { data_venda: "2026-09-03", nsu: 111004 });
  const parcelas = r.json?.resposta?.content?.installments;
  ok("abre as 3 parcelas da venda parcelada", parcelas?.length === 3, String(parcelas?.length));
  ok("traduz SCHEDULLED (dois L)", parcelas?.[1]?.status_descricao === "Agendada", parcelas?.[1]?.status_descricao);
  ok("venda de 03/09 ainda nao tem parcela vencida em 30/09", parcelas?.every((p) => p.status === "SCHEDULLED"));
  // D+30 cai no sabado 03/10; a 2a parcela, no feriado de 02/11. Credito so cai em dia util.
  ok("1a parcela cai no primeiro dia util depois de D+30", parcelas?.[0]?.expirationDate === "2026-10-05", parcelas?.[0]?.expirationDate);
  ok("parcela no feriado de Finados passa para o dia seguinte", parcelas?.[1]?.expirationDate === "2026-11-03", parcelas?.[1]?.expirationDate);
  ok("parcela agendada ainda nao tem paymentId", parcelas?.every((p) => p.paymentId === ""));
  r = await chamar("rede_parcelas_da_venda", { data_venda: "2026-07-10", nsu: 111006 });
  const antigas = r.json?.resposta?.content?.installments;
  ok("traduz PAID mesmo sendo ambiguo entre pagamento e parcela", antigas?.[0]?.status_descricao === "Pago" || antigas?.[0]?.status_descricao === "Paga", antigas?.[0]?.status_descricao);
  ok("4x de julho: 2 parcelas pagas e 2 agendadas em 30/09", antigas?.filter((p) => p.status === "PAID").length === 2 && antigas?.filter((p) => p.status === "SCHEDULLED").length === 2, JSON.stringify(antigas?.map((p) => p.status)));
  ok("2a parcela paga em 08/09", antigas?.[1]?.expirationDate === "2026-09-08" && antigas?.[1]?.paymentId === "P20260908001", `${antigas?.[1]?.expirationDate} ${antigas?.[1]?.paymentId}`);
  r = await chamar("rede_parcelas_da_venda", { data_venda: "2026-08-28", nsu: 111011 });
  ok("parcela do deposito suspenso aparece bloqueada", r.json?.resposta?.content?.installments?.[0]?.status === "BLOCKED", r.json?.resposta?.content?.installments?.[0]?.status);

  r = await chamar("rede_vendas_parceladas", { data_inicio: "2026-09-01", data_fim: "2026-09-25", paginar_tudo: true });
  // Uma linha por parcela: 2 debitos, 1 credito a vista e as 3 parcelas da 111004.
  ok("vendas parceladas: uma linha por parcela", r.json?.total_de_parcelas === 6, String(r.json?.total_de_parcelas));
  ok("vencimento de cada parcela e o do cronograma", r.json?.parcelas?.filter((p) => p.nsu === 111004).map((p) => p.expirationDate).join(",") === "2026-10-05,2026-11-03,2026-12-02");

  r = await chamar("rede_parcelas_do_pagamento", { payment_id: "P20260908001", paginar_tudo: true });
  const pacote = r.json?.parcelas;
  ok("o deposito de 08/09 e um pacote de duas vendas", r.json?.total_de_parcelas === 2 && pacote?.some((p) => p.nsu === 111006) && pacote?.some((p) => p.nsu === 111010), String(r.json?.total_de_parcelas));

  r = await chamar("rede_parcelas_gravame", { pv_centralizador: CREDENCIAIS.PV, payment_id_hash: CENARIO.hashDoPagamento("P20260908001") });
  ok("v3 com gravame responde", !r.erro && r.json?.resposta?.content?.installments?.length === 2);
  ok("traduz o tipo de negociacao", r.json?.resposta?.content?.installments?.[0]?.negociacao_descricao === "Pagamento livre");
  r = await chamar("rede_parcelas_gravame", { pv_centralizador: CREDENCIAIS.PV, payment_id_hash: "MjAyMjAx" });
  ok("hash que nao e de pagamento nenhum volta vazio", !r.erro && r.json?.resposta?.vazio === true);

  console.log("\ncoerencia do cenario (o que venceu foi pago; o resto e recebivel)");
  ok("nenhum pagamento com data depois de hoje", CENARIO.PAGAMENTOS.every((p) => p.paymentDate <= CENARIO.HOJE));
  ok("toda ordem de credito aponta para um pagamento que existe", CENARIO.ORDENS.every((o) => CENARIO.PAGAMENTOS.some((p) => p.paymentId === o.paymentId)));
  ok("nenhum recebivel com data ate hoje", CENARIO.RECEBIVEIS.every((x) => x.data > CENARIO.HOJE));
  const pagoOuDescontado = CENARIO.PAGAMENTOS.filter((p) => p.status === "PAID").every((p) => {
    const ordens = CENARIO.ORDENS.filter((o) => o.paymentId === p.paymentId);
    return Math.abs(ordens.reduce((t, o) => t + o.netAmount, 0) - p.netAmount) < 0.005;
  });
  ok("liquido de cada pagamento pago = soma das suas ordens de credito", pagoOuDescontado);

  console.log("\npagamentos");
  r = await chamar("rede_pagamentos", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  ok("lista os 4 pagamentos de setembro", r.json?.total_de_pagamentos === 4, String(r.json?.total_de_pagamentos));
  ok("traduz status SUSPENDED", r.json?.pagamentos?.some((p) => p.status_descricao === "Suspenso"));
  ok("traduz os tipos CREDIT e DEBIT", r.json?.pagamentos?.some((p) => p.tipo_descricao === "Credito") && r.json?.pagamentos?.some((p) => p.tipo_descricao === "Debito"), JSON.stringify(r.json?.pagamentos?.map((p) => p.tipo_descricao)));
  r = await chamar("rede_pagamentos", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("outubro ainda nao tem pagamento (e futuro)", !r.erro && r.json?.resposta?.vazio === true);

  r = await chamar("rede_pagamentos_diario", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  ok("visao diaria agrupa por dia (02, 08 e 28/09)", r.json?.total_de_dias === 3, String(r.json?.total_de_dias));
  ok("diaria separa pagos e suspensos", r.json?.dias?.find((d) => d.date === "2026-09-28")?.suspended?.count === 1 && r.json?.dias?.find((d) => d.date === "2026-09-02")?.paid?.count === 2);

  r = await chamar("rede_pagamentos_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30" });
  // 317,25 + 302,25 + 731,25 pagos e 780,00 suspenso: sem filtro de status, o resumo soma tudo.
  ok("resumo de pagamentos soma o liquido do periodo", r.json?.resposta?.payments?.[0]?.netAmount === 2130.75, String(r.json?.resposta?.payments?.[0]?.netAmount));
  ok("resumo traz o cobrado (aluguel) e o esperado", r.json?.resposta?.payments?.[0]?.chargeAmount === 27.5 && r.json?.resposta?.payments?.[0]?.expectedAmount === 2158.25);
  const comHeader = chamadas.filter((c) => c.rota === "/merchant-statement/v2/payments/summary" && c.merchantId === CREDENCIAIS.PV);
  ok("mandou o PV no header Merchant-Id", comHeader.length > 0);
  r = await chamar("rede_pagamentos_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30", status: "PAID" });
  ok("resumo so dos pagos exclui o suspenso", r.json?.resposta?.payments?.[0]?.netAmount === 1350.75, String(r.json?.resposta?.payments?.[0]?.netAmount));

  r = await chamar("rede_pagamentos_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30", agrupar_por: "brand" });
  ok("agrupado por bandeira traduz a marca", r.json?.resposta?.payments?.some((x) => x.bandeira === "Mastercard") && r.json?.resposta?.payments?.some((x) => x.bandeira === "Visa"));

  r = await chamar("rede_pagamento", { payment_id: "P20260928001" });
  ok("um pagamento pelo id", r.json?.resposta?.content?.payments?.[0]?.paymentId === "P20260928001" && r.json?.resposta?.content?.payments?.[0]?.status === "SUSPENDED");
  r = await chamar("rede_pagamento_esperado", { payment_id: "P20260814001" });
  ok("valor esperado = pago + debitos (875 + 100)", r.json?.resposta?.content?.expectedAmount === 975, String(r.json?.resposta?.content?.expectedAmount));

  r = await chamar("rede_ordens_de_credito", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  // O deposito suspenso de 28/09 nao gera ordem; o de 08/09 tem duas (uma por resumo de vendas).
  ok("ordens de credito de setembro", r.json?.total_de_ordens === 4, String(r.json?.total_de_ordens));
  ok("ordem traz saleSummaryNumber", typeof r.json?.ordens?.[0]?.saleSummaryNumber === "number");
  ok("parcela paga e ordem de credito usam o mesmo paymentId", r.json?.ordens?.some((o) => o.paymentId === "P20260908001" && o.saleSummaryNumber === 900005));

  r = await chamar("rede_debitos_do_pagamento", { payment_id: "P20260902001" });
  ok("debitos do pagamento explicam o desconto", r.json?.resposta?.charges?.[0]?.debitAmount === 27.5);
  r = await chamar("rede_debitos_do_pagamento", { payment_id: "P20260908001" });
  ok("pagamento sem debito volta vazio", !r.erro && r.json?.resposta?.vazio === true);
  r = await chamar("rede_cashbacks_do_pagamento", { payment_id: "P20260902001" });
  ok("pagamento sem cashback volta vazio, nao erro", !r.erro && r.json?.resposta?.vazio === true);

  r = await chamar("rede_bloqueios_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30" });
  ok("bloqueios traduzem o tipo", r.json?.resposta?.content?.[0]?.bloqueio_descricao === "SUSPENDED");
  ok("bloqueio e o do deposito de 28/09 (R$ 780)", r.json?.resposta?.content?.[0]?.amountBlock === 780 && r.json?.resposta?.content?.[0]?.paymentId === "P20260928001");
  r = await chamar("rede_bloqueios_resumo", { data_inicio: "2026-08-01", data_fim: "2026-08-31" });
  ok("agosto nao tem bloqueio", !r.erro && r.json?.resposta?.vazio === true);
  r = await chamar("rede_bloqueios_do_pagamento", { payment_id: "P20260928001" });
  ok("bloqueio por pagamento", r.json?.resposta?.content?.blockSize === 1 && r.json?.resposta?.content?.releaseSize === 0);
  r = await chamar("rede_bloqueios_do_pagamento", { payment_id: "P20260908001" });
  ok("pagamento sem bloqueio volta vazio", !r.erro && r.json?.resposta?.vazio === true);

  console.log("\nrecebiveis");
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-31" });
  ok("v3 e o padrao", r.json?.versao === 3);
  // 02/10 975 + 05/10 292,50 + 08/10 292,50 + 28/10 487,50
  ok("a receber em outubro: R$ 2.047,50 em 4 parcelas", r.json?.resposta?.content?.[0]?.amount === 2047.5 && r.json?.resposta?.content?.[0]?.total === 4, JSON.stringify(r.json?.resposta?.content));
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2027-09-30" });
  ok("a receber daqui para frente: R$ 2.925,00 em 7 parcelas", r.json?.resposta?.content?.[0]?.amount === 2925 && r.json?.resposta?.content?.[0]?.total === 7, JSON.stringify(r.json?.resposta?.content));
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30" });
  ok("o que ja venceu nao e recebivel", !r.erro && r.json?.resposta?.vazio === true);
  const v3Header = chamadas.filter((c) => c.rota === "/merchant-statement/v3/receivables/summary" && c.merchantId === CREDENCIAIS.PV);
  ok("v3 manda Merchant-Id no header", v3Header.length > 0);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-12-31", agrupar_por: "month" });
  ok("v3 agrupa por mes", r.json?.resposta?.content?.map((x) => x.amount).join(",") === "2047.5,585,292.5", JSON.stringify(r.json?.resposta?.content));
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 2, agrupar_por: "DAY" });
  ok("v2 aceita groupBy MAIUSCULO", !r.erro && r.json?.versao === 2);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 1, tipo: "DAY" });
  ok("v1 aceita types", !r.erro && r.json?.versao === 1);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 3, tipo: "DAY" });
  ok("v3 recusa 'tipo' com explicacao", r.erro && r.texto.includes("v3"));

  r = await chamar("rede_recebiveis_calendario", { data_inicio: "2026-10-01", data_fim: "2026-11-29" });
  ok("calendario traz blocos diario e mensal", !!r.json?.resposta?.content?.daily && !!r.json?.resposta?.content?.mouthly);
  ok("calendario soma os meses do periodo", r.json?.resposta?.content?.mouthly?.receivables?.length === 2 && r.json?.resposta?.content?.daily?.totalAmount === 2632.5, JSON.stringify(r.json?.resposta?.content?.daily?.totalAmount));
  r = await chamar("rede_recebiveis_diario", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("recebiveis diario traduz SCHEDULED (um L)", r.json?.resposta?.content?.receivables?.[0]?.status_descricao === "Agendado");
  r = await chamar("rede_recebiveis_parcelas", { data_inicio: "2026-10-01", data_fim: "2026-10-30", bandeiras: ["Mastercard"], paginar_tudo: true });
  ok("parcelas de recebiveis com bandeira", r.json?.total_de_parcelas === 4, String(r.json?.total_de_parcelas));
  r = await chamar("rede_recebiveis_parcelas", { data_inicio: "2026-10-01", data_fim: "2026-10-30", bandeiras: ["Visa"], paginar_tudo: true });
  ok("bandeira sem recebivel no periodo volta vazio", !r.erro && !r.json?.total_de_parcelas, String(r.json?.total_de_parcelas));

  console.log("\ndebitos");
  r = await chamar("rede_debitos", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  ok("debitos detalhados de setembro: o aluguel", r.json?.total_de_debitos === 1 && r.json?.debitos?.[0]?.adjustmentTypeCode === 23);
  ok("traduz o tipo de cobranca NET", r.json?.debitos?.[0]?.tipo_descricao?.includes("repasse"), r.json?.debitos?.[0]?.tipo_descricao);
  r = await chamar("rede_debitos", { data_inicio: "2026-08-01", data_fim: "2026-08-30", paginar_tudo: true });
  ok("debitos de agosto: o estorno de R$ 100", r.json?.total_de_debitos === 1 && r.json?.debitos?.[0]?.adjustmentTypeCode === 18 && r.json?.debitos?.[0]?.debitAmount === 100);
  r = await chamar("rede_debitos_resumo", { data_inicio: "2026-09-01", data_fim: "2026-09-30" });
  ok("resumo de debitos por tipo de ajuste", r.json?.resposta?.content?.[0]?.debitAmount === 27.5 && r.json?.resposta?.content?.length === 1);
  r = await chamar("rede_debitos_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("mes sem debito volta vazio", !r.erro && r.json?.resposta?.vazio === true);
  r = await chamar("rede_tipos_de_ajuste");
  ok("tabela de tipos de ajuste", r.json?.resposta?.length === 4);

  console.log("\nconciliacao (o cruzamento que o sandbox nao permite provar)");
  r = await chamar("rede_conciliar", { venda_inicio: "2026-09-01", venda_fim: "2026-09-30" });
  const sit = r.json?.situacao;
  ok("leu as 5 vendas", r.json?.totais?.vendas_lidas === 5, String(r.json?.totais?.vendas_lidas));
  ok("leu as 4 ordens de credito ate hoje", r.json?.totais?.ordens_de_credito_lidas === 4, String(r.json?.totais?.ordens_de_credito_lidas));
  // Em 30/09 so o debito de setembro caiu; o credito de setembro vence de outubro em diante.
  ok("nenhum resumo de setembro conciliado ainda (credito em D+30)", sit?.conciliado?.resumos === 0, JSON.stringify(sit?.conciliado));
  ok("nada fica como divergente", sit?.valor_divergente?.resumos === 0, JSON.stringify(sit?.valor_divergente));
  ok("o debito de 01/09 vira 'ajuste no repasse' explicado pelo aluguel", sit?.ajuste_no_repasse?.resumos === 1 && sit?.ajuste_no_repasse?.descontado === 27.5, JSON.stringify(sit?.ajuste_no_repasse));
  const aj = r.json?.amostra?.ajuste_no_repasse?.[0];
  ok("diz qual ajuste: Aluguel de equipamento, R$ 27,50", aj?.resumo_de_vendas === "900001" && aj?.ajustes?.[0]?.descricao === "Aluguel de equipamento" && aj?.ajustes?.[0]?.valor === 27.5, JSON.stringify(aj));
  ok("aluguel nao dispara busca de venda estornada", !aj?.provavel_origem);
  ok("3 resumos de credito sem pagamento ainda", sit?.sem_pagamento?.resumos === 3 && sit?.sem_pagamento?.previsto === 2340, JSON.stringify(sit?.sem_pagamento));
  ok("3 pagamentos de vendas anteriores ao periodo", sit?.pago_sem_venda?.resumos === 3 && sit?.pago_sem_venda?.pago === 1033.5, JSON.stringify(sit?.pago_sem_venda));
  ok("janela de pagamento deslocada 40 dias", r.json?.periodo_de_pagamento?.fim === "2026-11-09", r.json?.periodo_de_pagamento?.fim);
  r = await chamar("rede_conciliar", { venda_inicio: "2026-08-01", venda_fim: "2026-08-31" });
  ok("agosto: 2 resumos conciliados (02/09 e 08/09)", r.json?.situacao?.conciliado?.resumos === 2 && r.json?.situacao?.conciliado?.valor_pago === 741, JSON.stringify(r.json?.situacao?.conciliado));
  ok("agosto: o deposito suspenso fica 'sem pagamento', nao conciliado", r.json?.situacao?.sem_pagamento?.resumos === 1 && r.json?.amostra?.sem_pagamento?.[0]?.resumo_de_vendas === "900009", JSON.stringify(r.json?.situacao?.sem_pagamento));
  r = await chamar("rede_conciliar", { venda_inicio: "2026-07-01", venda_fim: "2026-07-31" });
  const pa = r.json?.situacao?.parcelado_em_andamento;
  ok("parcelado 4x com parte das parcelas pagas NAO e divergente", r.json?.situacao?.valor_divergente?.resumos === 0, JSON.stringify(r.json?.situacao?.valor_divergente));
  ok("vira 'parcelado em andamento'", pa?.resumos === 1, JSON.stringify(pa));
  ok("falta receber 585,00 (2 de 4 parcelas)", pa?.falta_receber === 585, String(pa?.falta_receber));
  ok("marca 2 de 4 parcelas pagas", r.json?.amostra?.parcelado_em_andamento?.[0]?.parcelas_pagas === 2 && r.json?.amostra?.parcelado_em_andamento?.[0]?.parcelas === 4);
  const est = r.json?.amostra?.ajuste_no_repasse?.[0];
  ok("deposito com estorno de outra venda vira 'ajuste no repasse'", r.json?.situacao?.ajuste_no_repasse?.resumos === 1, JSON.stringify(r.json?.situacao?.ajuste_no_repasse));
  ok("identifica o ajuste: cancelamento de vendas, R$ 100", est?.ajustes?.[0]?.codigo === 18 && est?.ajustes?.[0]?.valor === 100, JSON.stringify(est?.ajustes));
  ok("acha a venda estornada de outra data (NSU 111008)", est?.provavel_origem?.nsu === 111008, JSON.stringify(est?.provavel_origem));
  ok("mostra o evento do estorno", est?.provavel_origem?.evento === "PARTIAL_CANCELLED" && est?.provavel_origem?.data_do_evento === "2026-08-13");
  ok("o valor do evento e o valor estornado (R$ 100)", est?.provavel_origem?.valor_do_evento === 100, String(est?.provavel_origem?.valor_do_evento));
  r = await chamar("rede_conciliar", { venda_inicio: "2026-07-01", venda_fim: "2026-07-31", explicar_divergencias: false });
  ok("explicar_divergencias=false deixa como divergente", r.json?.situacao?.valor_divergente?.resumos === 1 && !r.json?.situacao?.ajuste_no_repasse?.resumos);
  r = await chamar("rede_conciliar", { venda_inicio: "2026-09-01", venda_fim: "2026-09-30", detalhar: true });
  ok("detalhar devolve a lista completa", r.json?.resumos_de_venda?.length === 7, String(r.json?.resumos_de_venda?.length));

  console.log("\nrenovacao de token");
  const antes = chamadas.filter((c) => c.rota === "/oauth/token").length;
  invalidarTokens(); // o servidor esquece os tokens: o proximo GET volta 401
  r = await chamar("rede_tipos_de_ajuste");
  const depois = chamadas.filter((c) => c.rota === "/oauth/token").length;
  ok("401 dispara renovacao e a consulta passa", !r.erro && r.json?.resposta?.length === 4);
  ok("houve nova chamada ao /oauth/token", depois > antes, `${antes} -> ${depois}`);

  console.log("\nrede_get (escape hatch)");
  r = await chamar("rede_get", { caminho: "/merchant-statement/v1/charges/adjustment-types" });
  ok("GET livre funciona", !r.erro && r.json?.resposta?.length === 4);
  r = await chamar("rede_get", { caminho: "/merchant-statement/v2/payments/summary", params: { startDate: "2026-10-01", endDate: "2026-10-30" } });
  ok("sem Merchant-Id o erro explica o header", r.erro && r.texto.includes("Merchant-Id"));

  console.log(`\n${passou} passaram, ${falhou} falharam\n`);
} catch (e) {
  console.error("erro no teste:", e.stack);
  falhou++;
} finally {
  mcp.kill();
  servidor.close();
}
process.exit(falhou ? 1 : 0);
