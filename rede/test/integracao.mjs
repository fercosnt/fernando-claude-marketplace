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
import { criarMock, invalidarTokens, chamadas, CREDENCIAIS } from "./mock.mjs";

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
  ok("traduz PAID mesmo sendo ambiguo entre pagamento e parcela", parcelas?.[0]?.status_descricao === "Pago" || parcelas?.[0]?.status_descricao === "Paga", parcelas?.[0]?.status_descricao);

  r = await chamar("rede_vendas_parceladas", { data_inicio: "2026-09-01", data_fim: "2026-09-25", paginar_tudo: true });
  ok("vendas parceladas do periodo", r.json?.total_de_parcelas === 4, String(r.json?.total_de_parcelas));

  r = await chamar("rede_parcelas_do_pagamento", { payment_id: "P20261002002", paginar_tudo: true });
  ok("abre o pacote do pagamento", r.json?.total_de_parcelas === 1, String(r.json?.total_de_parcelas));

  r = await chamar("rede_parcelas_gravame", { pv_centralizador: CREDENCIAIS.PV, payment_id_hash: "MjAyMjAx" });
  ok("v3 com gravame responde", !r.erro && !!r.json?.resposta?.content?.installments?.length);
  ok("traduz o tipo de negociacao", r.json?.resposta?.content?.installments?.[0]?.negociacao_descricao === "Onus gravame");

  console.log("\npagamentos");
  r = await chamar("rede_pagamentos", { data_inicio: "2026-10-01", data_fim: "2026-10-30", paginar_tudo: true });
  ok("lista pagamentos de outubro", r.json?.total_de_pagamentos === 2, String(r.json?.total_de_pagamentos));
  ok("traduz status SUSPENDED", r.json?.pagamentos?.some((p) => p.status_descricao === "Suspenso"));
  ok("traduz tipo CREDIT", r.json?.pagamentos?.every((p) => p.tipo_descricao === "Credito"));

  r = await chamar("rede_pagamentos_diario", { data_inicio: "2026-10-01", data_fim: "2026-10-30", paginar_tudo: true });
  ok("visao diaria agrupa por dia", r.json?.total_de_dias === 1, String(r.json?.total_de_dias));
  ok("diaria separa pagos e suspensos", r.json?.dias?.[0]?.suspended?.count === 1);

  r = await chamar("rede_pagamentos_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("resumo de pagamentos soma o liquido", r.json?.resposta?.payments?.[0]?.netAmount === 1825, String(r.json?.resposta?.payments?.[0]?.netAmount));
  const comHeader = chamadas.filter((c) => c.rota === "/merchant-statement/v2/payments/summary" && c.merchantId === CREDENCIAIS.PV);
  ok("mandou o PV no header Merchant-Id", comHeader.length > 0);

  r = await chamar("rede_pagamentos_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", agrupar_por: "brand" });
  ok("agrupado por bandeira traduz a marca", r.json?.resposta?.payments?.[0]?.bandeira === "Mastercard");

  r = await chamar("rede_pagamento", { payment_id: "P20261002002" });
  ok("um pagamento pelo id", r.json?.resposta?.content?.payments?.[0]?.paymentId === "P20261002002");
  r = await chamar("rede_pagamento_esperado", { payment_id: "P20261002002" });
  ok("valor esperado difere do pago", r.json?.resposta?.content?.expectedAmount === 900);

  r = await chamar("rede_ordens_de_credito", { data_inicio: "2026-09-01", data_fim: "2026-09-30", paginar_tudo: true });
  ok("ordens de credito de setembro", r.json?.total_de_ordens === 2, String(r.json?.total_de_ordens));
  ok("ordem traz saleSummaryNumber", typeof r.json?.ordens?.[0]?.saleSummaryNumber === "number");

  r = await chamar("rede_debitos_do_pagamento", { payment_id: "P20261002002" });
  ok("debitos do pagamento explicam o desconto", r.json?.resposta?.charges?.[0]?.debitAmount === 27.5);
  r = await chamar("rede_cashbacks_do_pagamento", { payment_id: "P20261002002" });
  ok("cashbacks do pagamento", r.json?.resposta?.cashbacks?.[0]?.netAmount === 12.35);

  r = await chamar("rede_bloqueios_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("bloqueios traduzem o tipo", r.json?.resposta?.content?.[0]?.bloqueio_descricao === "SUSPENDED");
  r = await chamar("rede_bloqueios_do_pagamento", { payment_id: "P20261002002" });
  ok("bloqueio por pagamento", r.json?.resposta?.content?.blockSize === 1);

  console.log("\nrecebiveis");
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("v3 e o padrao", r.json?.versao === 3);
  const v3Header = chamadas.filter((c) => c.rota === "/merchant-statement/v3/receivables/summary" && c.merchantId === CREDENCIAIS.PV);
  ok("v3 manda Merchant-Id no header", v3Header.length > 0);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 2, agrupar_por: "DAY" });
  ok("v2 aceita groupBy MAIUSCULO", !r.erro && r.json?.versao === 2);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 1, tipo: "DAY" });
  ok("v1 aceita types", !r.erro && r.json?.versao === 1);
  r = await chamar("rede_recebiveis_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30", versao: 3, tipo: "DAY" });
  ok("v3 recusa 'tipo' com explicacao", r.erro && r.texto.includes("v3"));

  r = await chamar("rede_recebiveis_calendario", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("calendario traz blocos diario e mensal", !!r.json?.resposta?.content?.daily && !!r.json?.resposta?.content?.mouthly);
  r = await chamar("rede_recebiveis_diario", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("recebiveis diario traduz SCHEDULED (um L)", r.json?.resposta?.content?.receivables?.[0]?.status_descricao === "Agendado");
  r = await chamar("rede_recebiveis_parcelas", { data_inicio: "2026-10-01", data_fim: "2026-10-30", bandeiras: ["Mastercard"], paginar_tudo: true });
  ok("parcelas de recebiveis com bandeira", r.json?.total_de_parcelas === 1, String(r.json?.total_de_parcelas));

  console.log("\ndebitos");
  r = await chamar("rede_debitos", { data_inicio: "2026-10-01", data_fim: "2026-10-30", paginar_tudo: true });
  ok("debitos detalhados", r.json?.total_de_debitos === 1);
  ok("traduz o tipo de cobranca NET", r.json?.debitos?.[0]?.tipo_descricao?.includes("repasse"), r.json?.debitos?.[0]?.tipo_descricao);
  r = await chamar("rede_debitos_resumo", { data_inicio: "2026-10-01", data_fim: "2026-10-30" });
  ok("resumo de debitos por tipo de ajuste", r.json?.resposta?.content?.[0]?.debitAmount === 27.5);
  r = await chamar("rede_tipos_de_ajuste");
  ok("tabela de tipos de ajuste", r.json?.resposta?.length === 3);

  console.log("\nconciliacao (o cruzamento que o sandbox nao permite provar)");
  r = await chamar("rede_conciliar", { venda_inicio: "2026-09-01", venda_fim: "2026-09-30" });
  const sit = r.json?.situacao;
  ok("leu as 5 vendas", r.json?.totais?.vendas_lidas === 5, String(r.json?.totais?.vendas_lidas));
  ok("leu as 4 ordens de credito", r.json?.totais?.ordens_de_credito_lidas === 4, String(r.json?.totais?.ordens_de_credito_lidas));
  ok("2 resumos conciliados", sit?.conciliado?.resumos === 2, JSON.stringify(sit?.conciliado));
  ok("conciliado soma 1.319,75", sit?.conciliado?.valor_pago === 1319.75, String(sit?.conciliado?.valor_pago));
  ok("1 resumo com valor divergente (RV 900003)", sit?.valor_divergente?.resumos === 1, JSON.stringify(sit?.valor_divergente));
  ok("divergencia e de 27,50", Math.round((sit?.valor_divergente?.previsto - sit?.valor_divergente?.pago) * 100) / 100 === 27.5);
  ok("1 venda sem pagamento (28/09, D+30)", sit?.sem_pagamento?.resumos === 1, JSON.stringify(sit?.sem_pagamento));
  ok("1 pagamento sem venda no periodo", sit?.pago_sem_venda?.resumos === 1, JSON.stringify(sit?.pago_sem_venda));
  ok("janela de pagamento deslocada 40 dias", r.json?.periodo_de_pagamento?.fim === "2026-11-09", r.json?.periodo_de_pagamento?.fim);
  r = await chamar("rede_conciliar", { venda_inicio: "2026-07-01", venda_fim: "2026-07-31" });
  const pa = r.json?.situacao?.parcelado_em_andamento;
  ok("parcelado 4x com 1 parcela paga NAO e divergente", r.json?.situacao?.valor_divergente?.resumos === 0, JSON.stringify(r.json?.situacao?.valor_divergente));
  ok("vira 'parcelado em andamento'", pa?.resumos === 1, JSON.stringify(pa));
  ok("falta receber 877,50 (3 de 4 parcelas)", pa?.falta_receber === 877.5, String(pa?.falta_receber));
  ok("marca 1 de 4 parcelas pagas", r.json?.amostra?.parcelado_em_andamento?.[0]?.parcelas_pagas === 1 && r.json?.amostra?.parcelado_em_andamento?.[0]?.parcelas === 4);
  r = await chamar("rede_conciliar", { venda_inicio: "2026-09-01", venda_fim: "2026-09-30", detalhar: true });
  ok("detalhar devolve a lista completa", r.json?.resumos_de_venda?.length === 5, String(r.json?.resumos_de_venda?.length));

  console.log("\nrenovacao de token");
  const antes = chamadas.filter((c) => c.rota === "/oauth/token").length;
  invalidarTokens(); // o servidor esquece os tokens: o proximo GET volta 401
  r = await chamar("rede_tipos_de_ajuste");
  const depois = chamadas.filter((c) => c.rota === "/oauth/token").length;
  ok("401 dispara renovacao e a consulta passa", !r.erro && r.json?.resposta?.length === 3);
  ok("houve nova chamada ao /oauth/token", depois > antes, `${antes} -> ${depois}`);

  console.log("\nrede_get (escape hatch)");
  r = await chamar("rede_get", { caminho: "/merchant-statement/v1/charges/adjustment-types" });
  ok("GET livre funciona", !r.erro && r.json?.resposta?.length === 3);
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
