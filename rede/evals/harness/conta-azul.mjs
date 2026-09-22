#!/usr/bin/env node
/**
 * CLI do MCP conta-azul para os evals da Rede em que as duas skills disputam a mesma pergunta
 * ("quanto tenho a receber?"). Usa o servidor e a API simulada do proprio plugin conta-azul
 * (../../../conta-azul), com o "hoje" alinhado ao da API simulada da Rede: 2026-09-30.
 *
 *   node conta-azul.mjs list                     -> instrucoes do servidor MCP e as tools (descricao e parametros)
 *   node conta-azul.mjs <tool> '<json de args>'  -> chama a tool e imprime o resultado
 *
 * CA_RUN_DIR isola cada execucao (config, token e o log das chamadas em api_log.jsonl).
 * Sem dependencias, como rede.mjs: fala JSON-RPC direto com o servidor por stdio. (O ca.mjs do
 * conta-azul importa o SDK do MCP, que nao vem instalado no repositorio.)
 */
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const plugin = join(aqui, "../../../conta-azul");
const { iniciar } = await import(join(plugin, "evals/harness/fixture-mock.mjs"));

const runDir = process.env.CA_RUN_DIR || join(aqui, "run-default-conta-azul");
mkdirSync(join(runDir, "state/tokens"), { recursive: true });
const cfg = join(runDir, "cfg.json");
if (!existsSync(cfg)) {
  writeFileSync(cfg, JSON.stringify({ escrita: false, client_id: "cid", client_secret: "csec", redirect_uri: "https://www.contaazul.com", empresas: [{ nome: "Beauty Smile" }] }));
}
const tok = join(runDir, "state/tokens/beauty-smile.json");
if (!existsSync(tok)) {
  writeFileSync(tok, JSON.stringify({ access_token: "at-fix", refresh_token: "rt-fix", expira_em: Date.now() + 864e5, atualizado_em: new Date().toISOString() }));
}

const srv = await iniciar(join(runDir, "api_log.jsonl"));
const base = `http://127.0.0.1:${srv.address().port}`;
const mcp = spawn("node", [join(plugin, "servers/conta-azul-mcp.js")], {
  env: {
    ...process.env,
    CONTAAZUL_HOJE: "2026-09-30",
    CONTAAZUL_CONFIG_FILE: cfg,
    CONTAAZUL_STATE_DIR: join(runDir, "state"),
    CONTAAZUL_BASE_URL: base,
    CONTAAZUL_TOKEN_URL: `${base}/oauth/token`,
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
  const ini = await enviar("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "rede-eval-conta-azul", version: "1" } });
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
      console.log(r.result?.content?.map((c) => c.text).join("\n") ?? JSON.stringify(r.error ?? r));
      if (r.result?.isError) codigo = 1;
    }
  }
} finally {
  mcp.kill();
  srv.close();
}
process.exit(codigo);
