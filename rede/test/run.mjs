#!/usr/bin/env node
/**
 * Teste de fumaca do servidor MCP da Rede, sem tocar na API.
 *
 * Sobe o bundle com uma configuracao temporaria e confere o que da para conferir offline:
 * as tools aparecem, os erros de configuracao sao legiveis, as janelas de data sao validadas
 * antes de qualquer chamada, os dominios traduzem e o groupBy respeita a caixa de cada rota.
 *
 * Uso: node test/run.mjs
 */
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const raiz = dirname(dirname(fileURLToPath(import.meta.url)));
const tmp = mkdtempSync(join(tmpdir(), "rede-mcp-teste-"));
const configFile = join(tmp, "config.json");

writeFileSync(
  configFile,
  JSON.stringify({
    ambiente: "sandbox",
    client_id: "id-de-teste",
    client_secret: "secret-de-teste",
    usuario: "usuario-de-teste",
    senha: "senha-de-teste",
    pvs: [
      { nome: "Sandbox A", numero: "13381369" },
      { nome: "Sandbox B", numero: "22523510" },
    ],
  })
);

const servidor = spawn("node", [join(raiz, "servers", "rede-mcp.js")], {
  env: { ...process.env, REDE_CONFIG_FILE: configFile, REDE_STATE_DIR: join(tmp, "estado") },
  stdio: ["pipe", "pipe", "pipe"],
});

let buffer = "";
const pendentes = new Map();
servidor.stdout.on("data", (d) => {
  buffer += d.toString();
  let corte;
  while ((corte = buffer.indexOf("\n")) >= 0) {
    const linha = buffer.slice(0, corte).trim();
    buffer = buffer.slice(corte + 1);
    if (!linha) continue;
    let msg;
    try {
      msg = JSON.parse(linha);
    } catch {
      continue;
    }
    const resolve = pendentes.get(msg.id);
    if (resolve) {
      pendentes.delete(msg.id);
      resolve(msg);
    }
  }
});
servidor.stderr.on("data", (d) => process.env.VERBOSE && process.stderr.write(`[servidor] ${d}`));

let proximoId = 1;
const enviar = (method, params) =>
  new Promise((resolve, reject) => {
    const id = proximoId++;
    pendentes.set(id, resolve);
    servidor.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
    setTimeout(() => reject(new Error(`timeout em ${method}`)), 15000).unref();
  });

const chamar = async (nome, args = {}) => {
  const r = await enviar("tools/call", { name: nome, arguments: args });
  const txt = r.result?.content?.[0]?.text ?? "";
  let json = null;
  try {
    json = JSON.parse(txt);
  } catch {
    /* resposta de erro e texto puro */
  }
  return { erro: !!r.result?.isError, texto: txt, json };
};

let passou = 0;
let falhou = 0;
const ok = (nome, condicao, detalhe = "") => {
  if (condicao) {
    passou++;
    console.log(`  ok   ${nome}`);
  } else {
    falhou++;
    console.log(`  FALHA ${nome}${detalhe ? ` — ${detalhe}` : ""}`);
  }
};

try {
  await enviar("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "teste", version: "0" },
  });
  servidor.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");

  console.log("\ntools registradas");
  const lista = await enviar("tools/list", {});
  const nomes = lista.result.tools.map((t) => t.name);
  ok(`${nomes.length} tools expostas`, nomes.length >= 25, nomes.length.toString());
  for (const esperada of [
    "rede_status", "rede_conectar", "rede_vendas", "rede_vendas_resumo", "rede_vendas_por_nsu",
    "rede_parcelas_da_venda", "rede_vendas_parceladas", "rede_parcelas_do_pagamento", "rede_parcelas_gravame",
    "rede_pagamentos", "rede_pagamentos_diario", "rede_pagamentos_resumo", "rede_pagamento",
    "rede_pagamento_esperado", "rede_ordens_de_credito", "rede_debitos_do_pagamento",
    "rede_cashbacks_do_pagamento", "rede_bloqueios_resumo", "rede_bloqueios_do_pagamento",
    "rede_recebiveis_resumo", "rede_recebiveis_calendario", "rede_recebiveis_diario",
    "rede_recebiveis_parcelas", "rede_debitos", "rede_debitos_resumo", "rede_tipos_de_ajuste",
    "rede_conciliar", "rede_dominios", "rede_get",
  ]) {
    ok(esperada, nomes.includes(esperada));
  }

  console.log("\nstatus e configuracao");
  const status = await chamar("rede_status");
  ok("status responde configurado", status.json?.configurado === true);
  ok("ambiente sandbox", status.json?.ambiente === "sandbox");
  ok("base do sandbox correta", status.json?.base_da_api === "https://rl7-sandbox-api.useredecloud.com.br");
  ok("dois PVs listados", status.json?.pvs?.length === 2);
  ok("client_secret nao aparece", !status.texto.includes("secret-de-teste"));
  ok("senha nao aparece", !status.texto.includes("senha-de-teste"));

  console.log("\ndominios (consulta local)");
  const dom = await chamar("rede_dominios", { tabela: "bandeiras" });
  ok("bandeira 1 = Mastercard", dom.json?.valores?.["1"] === "Mastercard");
  ok("bandeira 14 = Elo", dom.json?.valores?.["14"] === "Elo");
  const todas = await chamar("rede_dominios");
  ok("group_by por rota exposto", !!todas.json?.tabelas?.group_by?.pagamentos_resumo);
  ok("nota sobre SCHEDULLED", todas.json?.notas?.some((n) => n.includes("SCHEDULLED")));
  const domRuim = await chamar("rede_dominios", { tabela: "inexistente" });
  ok("tabela inexistente explica as opcoes", domRuim.erro && domRuim.texto.includes("Disponiveis"));

  console.log("\nvalidacao de janela de data (antes de chamar a Rede)");
  const janelaGrande = await chamar("rede_vendas", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-06-30" });
  ok("62 dias barrado em vendas", janelaGrande.erro && janelaGrande.texto.includes("62 dias"));
  ok("erro sugere as fatias", janelaGrande.texto.includes("Divida em"));
  const trintaDias = await chamar("rede_debitos", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-03-01" });
  ok("30 dias barrado em debitos", trintaDias.erro && trintaDias.texto.includes("30 dias"));
  const invertida = await chamar("rede_pagamentos", { pv: "13381369", data_inicio: "2024-03-01", data_fim: "2024-01-01" });
  ok("data_fim antes de data_inicio barrado", invertida.erro && invertida.texto.includes("anterior"));
  const formatoRuim = await chamar("rede_vendas", { pv: "13381369", data_inicio: "01/01/2024", data_fim: "2024-01-10" });
  ok("formato de data explicado", formatoRuim.erro && formatoRuim.texto.includes("YYYY-MM-DD"));
  const dataIrreal = await chamar("rede_vendas", { pv: "13381369", data_inicio: "2024-02-31", data_fim: "2024-03-01" });
  ok("data inexistente barrada", dataIrreal.erro && dataIrreal.texto.includes("nao e uma data valida"));

  console.log("\nregras proprias de cada rota");
  const semBandeira = await chamar("rede_recebiveis_parcelas", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-01-10", bandeiras: [] });
  ok("parcelas de recebiveis exigem bandeira", semBandeira.erro && semBandeira.texto.includes("bandeira"));
  const groupRuim = await chamar("rede_pagamentos_resumo", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-01-10", agrupar_por: "DIA" });
  ok("groupBy invalido lista os aceitos", groupRuim.erro && groupRuim.texto.includes("accountNumber"));
  ok("groupBy avisa que a caixa importa", groupRuim.texto.includes("caixa importa"));
  const v1ComFiltroV2 = await chamar("rede_vendas", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-01-10", versao: 1, status_tipo: "PARTIAL" });
  ok("filtro so-da-v2 barrado na v1", v1ComFiltroV2.erro && v1ComFiltroV2.texto.includes("v2"));
  const bandeiraRuim = await chamar("rede_vendas", { pv: "13381369", data_inicio: "2024-01-01", data_fim: "2024-01-10", bandeiras: ["Bandeirinha"] });
  ok("bandeira desconhecida explicada", bandeiraRuim.erro && bandeiraRuim.texto.includes("nao reconhecida"));

  console.log("\nresolucao de PV");
  const pvAmbiguo = await chamar("rede_vendas", { data_inicio: "2024-01-01", data_fim: "2024-01-10" });
  ok("dois PVs sem escolher pede o pv", pvAmbiguo.erro && pvAmbiguo.texto.includes("informe"));
  const pvInexistente = await chamar("rede_vendas", { pv: "Loja Fantasma", data_inicio: "2024-01-01", data_fim: "2024-01-10" });
  ok("PV desconhecido lista os disponiveis", pvInexistente.erro && pvInexistente.texto.includes("Sandbox A"));

  console.log(`\n${passou} passaram, ${falhou} falharam\n`);
} catch (e) {
  console.error("erro no teste:", e.message);
  falhou++;
} finally {
  servidor.kill();
}

process.exit(falhou ? 1 : 0);
