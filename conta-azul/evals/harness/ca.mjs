#!/usr/bin/env node
// CLI para chamar as tools do MCP conta-azul contra a API simulada.
//   node ca.mjs list                      -> lista tools + descricao + parametros
//   node ca.mjs <tool> '<json de args>'   -> chama a tool e imprime o resultado
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { iniciar } from "./fixture-mock.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const runDir = process.env.CA_RUN_DIR || join(here, "run-default");
mkdirSync(join(runDir, "state/tokens"), { recursive: true });
const cfg = join(runDir, "cfg.json");
if (!existsSync(cfg)) writeFileSync(cfg, JSON.stringify({ escrita: process.env.CA_ESCRITA === "1", client_id: "cid", client_secret: "csec", redirect_uri: "https://www.contaazul.com", empresas: [{ nome: "Beauty Smile" }] }));
const tok = join(runDir, "state/tokens/beauty-smile.json");
if (!existsSync(tok)) writeFileSync(tok, JSON.stringify({ access_token: "at-fix", refresh_token: "rt-fix", expira_em: Date.now() + 864e5, atualizado_em: new Date().toISOString() }));

const srv = await iniciar(join(runDir, "api_log.jsonl"));
const port = srv.address().port;
const t = new StdioClientTransport({ command: "node", args: [join(here, "../../servers/conta-azul-mcp.js")], stderr: "ignore",
  env: { ...process.env, CONTAAZUL_HOJE: "2026-09-20", CONTAAZUL_CONFIG_FILE: cfg, CONTAAZUL_STATE_DIR: join(runDir, "state"), CONTAAZUL_BASE_URL: `http://127.0.0.1:${port}`, CONTAAZUL_TOKEN_URL: `http://127.0.0.1:${port}/oauth/token` } });
const c = new Client({ name: "ca-cli", version: "1" });
await c.connect(t);
const [cmd, arg] = process.argv.slice(2);
try {
  if (!cmd || cmd === "list") {
    const { tools } = await c.listTools();
    for (const x of tools) console.log(`\n## ${x.name} — ${x.title ?? ""}\n${x.description}\nparametros: ${JSON.stringify(x.inputSchema.properties)}`);
  } else {
    const r = await c.callTool({ name: cmd, arguments: arg ? JSON.parse(arg) : {} });
    console.log(r.content.map((x) => x.text).join("\n"));
    writeFileSync(join(runDir, "tool_calls.jsonl"), JSON.stringify({ tool: cmd, args: arg ? JSON.parse(arg) : {}, erro: !!r.isError }) + "\n", { flag: "a" });
  }
} finally { await c.close(); srv.close(); }
