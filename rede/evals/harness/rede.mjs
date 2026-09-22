#!/usr/bin/env node
/**
 * CLI para os evals: chama as tools do MCP rede contra a API simulada (test/mock.mjs).
 *
 *   node rede.mjs list                     -> instrucoes do servidor MCP e as tools (descricao e parametros)
 *   node rede.mjs <tool> '<json de args>'  -> chama a tool e imprime o resultado
 *
 * REDE_RUN_DIR isola cada execucao (config, tokens e o log das chamadas a API em api_log.jsonl).
 * Dados da API simulada: uma clinica ficticia, PV 13381369, hoje = 2026-09-30.
 * REDE_CENARIO muda a config criada na primeira chamada do run:
 *   payment-link    -> credencial de projeto Payment Link: login ok, escopo payment-link, 401 em tudo
 *   pv-nao-liberado -> um segundo PV (Hirata, 22523510) que responde como PV nao liberado
 * Sem dependencias: fala JSON-RPC direto com o servidor por stdio.
 */
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync, appendFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { criarMock, chamadas, CREDENCIAIS } from "../../test/mock.mjs";

const aqui = dirname(fileURLToPath(import.meta.url));
const runDir = process.env.REDE_RUN_DIR || join(aqui, "run-default");
mkdirSync(join(runDir, "estado"), { recursive: true });
const cfgFile = join(runDir, "config.json");
if (!existsSync(cfgFile)) {
  const cenario = process.env.REDE_CENARIO ?? "";
  const cfg = {
    ambiente: "sandbox",
    client_id: CREDENCIAIS.CLIENT_ID,
    client_secret: CREDENCIAIS.CLIENT_SECRET,
    usuario: CREDENCIAIS.USUARIO,
    senha: CREDENCIAIS.SENHA,
    pvs: [{ nome: "Clinica", numero: CREDENCIAIS.PV }],
  };
  if (cenario === "payment-link") {
    // Projeto do pacote errado: so client_id/secret, como vem do portal.
    Object.assign(cfg, { client_id: CREDENCIAIS.CLIENT_ID_PAYMENT_LINK, client_secret: CREDENCIAIS.CLIENT_SECRET_PAYMENT_LINK });
    delete cfg.usuario;
    delete cfg.senha;
  } else if (cenario === "pv-nao-liberado") {
    cfg.pvs.push({ nome: "Hirata", numero: CREDENCIAIS.PV_NAO_LIBERADO });
  } else if (cenario) {
    console.error(`REDE_CENARIO desconhecido: ${cenario} (use payment-link ou pv-nao-liberado)`);
    process.exit(2);
  }
  writeFileSync(cfgFile, JSON.stringify(cfg, null, 2));
}

const { servidor, porta } = await criarMock();
const base = `http://127.0.0.1:${porta}`;
const mcp = spawn("node", [join(aqui, "../../servers/rede-mcp.js")], {
  env: {
    ...process.env,
    REDE_CONFIG_FILE: cfgFile,
    REDE_STATE_DIR: join(runDir, "estado"),
    REDE_BASE_URL: base,
    REDE_TOKEN_URL: `${base}/oauth/token`,
    REDE_INTERVALO_MS: "0",
  },
  stdio: ["pipe", "pipe", "ignore"],
});

let buf = "";
const pend = new Map();
mcp.stdout.on("data", (d) => {
  buf += d;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const l = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (!l) continue;
    try {
      const m = JSON.parse(l);
      pend.get(m.id)?.(m);
      pend.delete(m.id);
    } catch { /* ruido */ }
  }
});
let id = 1;
const enviar = (method, params) =>
  new Promise((ok) => {
    const n = id++;
    pend.set(n, ok);
    mcp.stdin.write(JSON.stringify({ jsonrpc: "2.0", id: n, method, params }) + "\n");
    setTimeout(() => ok({ timeout: true }), 120000).unref();
  });

let codigo = 0;
try {
  const ini = await enviar("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "rede-eval", version: "1" } });
  mcp.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");
  const [cmd, arg] = process.argv.slice(2);
  if (!cmd || cmd === "list") {
    // Em producao o cliente MCP poe as instructions do servidor no contexto, com ou sem skill.
    if (ini.result?.instructions) console.log(`# Instrucoes do servidor\n${ini.result.instructions}`);
    const r = await enviar("tools/list", {});
    for (const t of r.result.tools) {
      console.log(`\n## ${t.name} — ${t.title ?? ""}\n${t.description}\nparametros: ${JSON.stringify(t.inputSchema?.properties ?? {})}`);
    }
  } else {
    let args = {};
    if (arg) {
      try {
        args = JSON.parse(arg);
      } catch (e) {
        console.error(`JSON de argumentos invalido: ${e.message}`);
        codigo = 2;
      }
    }
    if (!codigo) {
      const r = await enviar("tools/call", { name: cmd, arguments: args });
      const texto = r.result?.content?.map((c) => c.text).join("\n") ?? JSON.stringify(r.error ?? r);
      console.log(texto);
      if (r.result?.isError) codigo = 1;
    }
  }
} finally {
  for (const c of chamadas) appendFileSync(join(runDir, "api_log.jsonl"), JSON.stringify(c) + "\n");
  mcp.kill();
  servidor.close();
}
process.exit(codigo);
