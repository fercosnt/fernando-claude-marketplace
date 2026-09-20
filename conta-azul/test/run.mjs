import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { mkdtempSync, writeFileSync, readFileSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { iniciarMock } from "./mock.mjs";

const PORTA = 18765;
const { srv, log, st } = await iniciarMock(PORTA);
const dir = mkdtempSync(join(tmpdir(), "ca-"));
const cfgFile = join(dir, "cfg.json");
const SERVER = new URL("../servers/conta-azul-mcp.js", import.meta.url).pathname;
let ok = 0, falhas = 0;
const check = (nome, cond, info) => { if (cond) { ok++; console.log("  ✓", nome); } else { falhas++; console.log("  ✗", nome, info ?? ""); } };

async function abrir(extraEnv = {}) {
  const t = new StdioClientTransport({
    command: "node", args: [SERVER], stderr: "pipe",
    env: { ...process.env, CONTAAZUL_CONFIG_FILE: cfgFile, CONTAAZUL_STATE_DIR: join(dir, "state"),
      CONTAAZUL_BASE_URL: `http://127.0.0.1:${PORTA}`, CONTAAZUL_TOKEN_URL: `http://127.0.0.1:${PORTA}/oauth/token`, ...extraEnv },
  });
  const c = new Client({ name: "teste", version: "1" });
  await c.connect(t);
  c.call = async (name, args = {}) => {
    const r = await c.callTool({ name, arguments: args });
    const txt = r.content[0].text;
    try { return { err: !!r.isError, j: JSON.parse(txt), txt }; } catch { return { err: !!r.isError, txt }; }
  };
  return c;
}

console.log("1. sem configuracao");
let c = await abrir();
let r = await c.call("contaazul_status");
check("status aponta falta de config", r.j.configurado === false && /conta-azul-setup/.test(r.j.problema));
const tools = (await c.listTools()).tools;
check(`tools registradas (${tools.length})`, tools.length >= 30);
check("todas as tools de escrita tem 'confirmar'", tools.filter(t => /ESCRITA/.test(t.title ?? "")).every(t => "confirmar" in t.inputSchema.properties));
await c.close();

console.log("2. placeholder e conexao OAuth");
writeFileSync(cfgFile, JSON.stringify({ client_id: "COLE_AQUI", client_secret: "csec", redirect_uri: "https://www.contaazul.com", empresas: [{ nome: "Beauty Smile" }] }));
c = await abrir();
r = await c.call("contaazul_status");
check("placeholder detectado", /client_id/.test(r.j.problema ?? ""));
writeFileSync(cfgFile, JSON.stringify({ client_id: "cid", client_secret: "csec", redirect_uri: "https://www.contaazul.com", empresas: [{ nome: "Beauty Smile" }] }));
r = await c.call("contaazul_resumo_financeiro", { de: "2026-09-01", ate: "2026-09-30" });
check("sem token pede para conectar", r.err && /contaazul_conectar/.test(r.txt));
r = await c.call("contaazul_conectar");
const link = new URL(r.j.link_de_autorizacao.replace("#/", ""));
check("link usa login.contaazul.com + scope literal", r.j.link_de_autorizacao.startsWith("https://login.contaazul.com/#/oauth/authorize") && r.j.link_de_autorizacao.includes("scope=openid+profile+aws.cognito.signin.user.admin"));
const state = r.j.state;
r = await c.call("contaazul_concluir_conexao", { url_ou_codigo: `https://www.contaazul.com/?code=CODEOK&state=forjado` });
check("state forjado e recusado", r.err && /state/.test(r.txt));
r = await c.call("contaazul_concluir_conexao", { url_ou_codigo: `https://www.contaazul.com/?code=CODEOK&state=${state}` });
check("conexao concluida e empresa identificada", r.j?.conectado && r.j.empresa_na_conta_azul.razao_social === "Beauty Smile Ltda", r.txt);
const tokFile = join(dir, "state/tokens/beauty-smile.json");
check("arquivo de token com permissao 600", (statSync(tokFile).mode & 0o777) === 0o600);
r = await c.call("contaazul_concluir_conexao", { url_ou_codigo: `https://www.contaazul.com/?code=CODEOK&state=${state}` });
check("state reutilizado e recusado", r.err);

console.log("3. leitura");
r = await c.call("contaazul_resumo_financeiro", { de: "2026-09-01", ate: "2026-09-30" });
check("resumo pagina todas as 1234 parcelas", r.j?.a_receber?.qtd_parcelas === 1234, r.txt?.slice(0, 300));
check("total a receber 123400", r.j.a_receber.total === 123400);
check("recebido = 412 * 100", r.j.a_receber.pago === 41200);
check("pagar total 10000 / pago 7500", r.j.a_pagar.total === 10000 && r.j.a_pagar.pago === 7500);
check("saldos somados 1200.5", r.j.saldos_atuais.total === 1200.5);
const buscas = log.filter(l => l.p.endsWith("contas-a-receber/buscar"));
check("paginas de 500 (3 chamadas)", buscas.length === 3 && buscas.every(b => b.q.includes("tamanho_pagina=500")));
r = await c.call("contaazul_contas_receber", { vencimento_de: "2026-09-01", vencimento_ate: "2026-09-30", status: ["ATRASADO", "EM_ABERTO"], limite: 5 });
const ult = log.filter(l => l.p.endsWith("contas-a-receber/buscar")).at(-1);
check("status vira parametro repetido", ult.q.includes("status=ATRASADO&status=EM_ABERTO"));
check("data DD/MM/AAAA normalizada", r.j.parcelas[0].vencimento === "2026-09-15");
check("limite respeitado", r.j.parcelas.length === 5);
r = await c.call("contaazul_contas_receber", { vencimento_de: "01/09/2026", vencimento_ate: "2026-09-30" });
check("data BR na entrada e rejeitada com mensagem clara", r.err && /YYYY-MM-DD/.test(r.txt));
r = await c.call("contaazul_notas_servico", { de: "2026-08-01", ate: "2026-09-09" });
check("NFS-e 40 dias -> 3 janelas de 15", r.j.janelas_consultadas === 3 && r.j.qtd === 3);
st.falhar429 = 2;
r = await c.call("contaazul_empresa");
check("GET repete apos 429", !r.err && r.j.id_empresa === "999");
r = await c.call("contaazul_pessoas", { busca: "x", tamanho_pagina: 30 });
check("tamanho_pagina 30 -> 50 (enum)", log.at(-1).q.includes("tamanho_pagina=50"));
r = await c.call("contaazul_get", { caminho: "/oauth/token" });
check("contaazul_get so aceita /v1/", r.err);

console.log("4. rotacao do refresh token");
let t = JSON.parse(readFileSync(tokFile, "utf8"));
t.expira_em = Date.now() - 1000; writeFileSync(tokFile, JSON.stringify(t));
const antes = st.refreshCalls;
const c2 = await abrir(); // segundo processo (ex.: Claude Code + Desktop)
const [a1, a2] = await Promise.all([c.call("contaazul_empresa"), c2.call("contaazul_empresa")]);
check("dois processos simultaneos: ambos funcionam", !a1.err && !a2.err, a1.txt + a2.txt);
check("...e so UMA renovacao aconteceu (trava)", st.refreshCalls - antes === 1, st.refreshCalls - antes);
const t2 = JSON.parse(readFileSync(tokFile, "utf8"));
check("novo refresh_token gravado", t2.refresh_token !== t.refresh_token && st.validRefresh.has(t2.refresh_token));
// token revogado no servidor (401) -> renova e repete
st.validAccess.delete(t2.access_token);
r = await c.call("contaazul_empresa");
check("401 -> renova sozinho e repete", !r.err);
// refresh invalidado -> mensagem util
t = JSON.parse(readFileSync(tokFile, "utf8")); st.validRefresh.clear(); t.expira_em = 0; writeFileSync(tokFile, JSON.stringify(t));
r = await c.call("contaazul_empresa");
check("refresh morto -> explica e manda reconectar", r.err && /invalid_refresh_token/.test(r.txt) && /contaazul_conectar/.test(r.txt));
await c2.close(); await c.close();
// reconecta para as proximas etapas
c = await abrir();
r = await c.call("contaazul_conectar"); r = await c.call("contaazul_concluir_conexao", { url_ou_codigo: `https://www.contaazul.com/?code=CODEOK&state=${r.j.state}` });

console.log("5. escrita");
const argsReceber = { descricao: "Protocolo Laser", valor: 3000, data_competencia: "2026-09-20", id_contato: "c1", id_conta_financeira: "cf1", id_categoria: "k1",
  parcelas: [{ data_vencimento: "2026-10-20", valor: 1000 }, { data_vencimento: "2026-11-20", valor: 1000 }, { data_vencimento: "2026-12-20", valor: 1000 }] };
r = await c.call("contaazul_criar_conta_receber", { ...argsReceber, confirmar: true });
check("escrita desligada recusa", r.err && /DESLIGADA/.test(r.txt));
await c.close();
writeFileSync(cfgFile, JSON.stringify({ escrita: true, client_id: "cid", client_secret: "csec", redirect_uri: "https://www.contaazul.com", empresas: [{ nome: "Beauty Smile" }] }));
c = await abrir();
const posts0 = log.filter(l => l.m !== "GET" && l.p.startsWith("/v1")).length;
r = await c.call("contaazul_criar_conta_receber", argsReceber);
check("sem confirmar -> so previa", r.j.PREVIA_NADA_FOI_ENVIADO === true && log.filter(l => l.m !== "GET" && l.p.startsWith("/v1")).length === posts0);
check("previa: 3 parcelas com descricao (i/n) e rateio 100%", r.j.corpo.condicao_pagamento.parcelas.length === 3 && r.j.corpo.condicao_pagamento.parcelas[1].descricao === "Protocolo Laser (2/3)" && r.j.corpo.rateio[0].valor === 3000);
r = await c.call("contaazul_criar_conta_receber", { ...argsReceber, valor: 2999 });
check("soma de parcelas divergente e recusada", r.err && /nao bate/.test(r.txt));
r = await c.call("contaazul_criar_conta_receber", { ...argsReceber, confirmar: true });
check("confirmar=true envia e acompanha protocolo ate SUCCESS", r.j?.situacao?.status === "SUCCESS", r.txt);
st.falhar500Post = true;
const n0 = log.filter(l => l.m === "POST" && l.p.endsWith("/contas-a-receber")).length;
r = await c.call("contaazul_criar_conta_receber", { ...argsReceber, confirmar: true });
check("POST com 500 NAO e repetido", r.err && log.filter(l => l.m === "POST" && l.p.endsWith("/contas-a-receber")).length === n0 + 1);
r = await c.call("contaazul_criar_pessoa", { nome: "Maria", tipo_pessoa: "Física", cpf: "123.456.789-00" });
check("previa de pessoa avisa duplicidade por CPF", r.j.avisos.some(a => /ja existe/.test(a)));
r = await c.call("contaazul_atualizar_parcela", { id_parcela: "x", vencimento: "2026-10-05" });
check("atualizar parcela busca versao atual (3)", r.j.corpo.versao === 3 && r.j.corpo.vencimento === "2026-10-05");
r = await c.call("contaazul_status");
check("status mostra escrita ligada e empresa conectada", /LIGADA/.test(r.j.escrita) && r.j.empresas[0].conectada);
check("status nao vaza segredo", !r.txt.includes("csec") && !/at\d|rt\d/.test(r.txt));
await c.close();

srv.close();
console.log(`\n${ok} ok, ${falhas} falha(s)`);
process.exit(falhas ? 1 : 0);
