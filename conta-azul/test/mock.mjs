// API Conta Azul simulada: OAuth com refresh rotativo, paginacao, 401 e 429.
import { createServer } from "node:http";
export function iniciarMock(porta) {
  const log = [];
  const st = { validRefresh: new Set(), validAccess: new Map(), refreshCalls: 0, falhar429: 0, falhar500Post: false, proto: 0 };
  const CID = "cid", CSEC = "csec";
  const receber = Array.from({ length: 1234 }, (_, i) => ({
    id: `r${i}`, descricao: `Tratamento ${i}`, data_vencimento: i % 2 ? "2026-09-10" : "15/09/2026",
    status_traduzido: i % 3 === 0 ? "RECEBIDO" : i % 3 === 1 ? "EM_ABERTO" : "ATRASADO",
    total: 100, pago: i % 3 === 0 ? 100 : 0, nao_pago: i % 3 === 0 ? 0 : 100,
    cliente: { id: `c${i % 7}`, nome: `Paciente ${i % 7}` }, categorias: [{ id: "k1", nome: "Laser" }],
  }));
  const pagar = Array.from({ length: 40 }, (_, i) => ({
    id: `p${i}`, descricao: `Fornecedor ${i}`, data_vencimento: "2026-09-05", status_traduzido: i < 30 ? "RECEBIDO" : "EM_ABERTO",
    total: 250, pago: i < 30 ? 250 : 0, nao_pago: i < 30 ? 0 : 250, fornecedor: { id: `f${i % 3}`, nome: `Forn ${i % 3}` },
    categorias: [{ id: "k2", nome: "Aluguel" }],
  }));
  let n = 0;
  const emitir = () => { const a = `at${++n}`, r = `rt${n}`; st.validAccess.set(a, Date.now() + 3600e3); st.validRefresh.add(r); return { access_token: a, refresh_token: r, expires_in: 3600, token_type: "Bearer" }; };
  const srv = createServer(async (req, res) => {
    let body = ""; for await (const c of req) body += c;
    const u = new URL(req.url, "http://x");
    log.push({ m: req.method, p: u.pathname, q: u.search, body });
    const json = (code, o) => { res.writeHead(code, { "Content-Type": "application/json" }); res.end(JSON.stringify(o)); };
    if (u.pathname === "/oauth/token") {
      if (req.headers.authorization !== "Basic " + Buffer.from(`${CID}:${CSEC}`).toString("base64")) return json(400, { error: "invalid_grant", error_subtype: "invalid_client" });
      const f = new URLSearchParams(body);
      if (f.get("grant_type") === "authorization_code") {
        if (f.get("code") !== "CODEOK") return json(400, { error: "invalid_grant" });
        return json(200, emitir());
      }
      st.refreshCalls++;
      await new Promise((r) => setTimeout(r, 300)); // janela para corrida
      const rt = f.get("refresh_token");
      if (!st.validRefresh.has(rt)) return json(400, { error: "invalid_grant", error_subtype: "invalid_refresh_token" });
      st.validRefresh.delete(rt); // ROTATIVO
      return json(200, emitir());
    }
    const tok = (req.headers.authorization || "").replace("Bearer ", "");
    if (!st.validAccess.has(tok) || st.validAccess.get(tok) < Date.now()) return json(401, { message: "The Token has expired." });
    if (req.method === "GET" && st.falhar429 > 0) { st.falhar429--; return json(429, { message: "slow down" }); }
    const pg = Number(u.searchParams.get("pagina") || 1), tam = Number(u.searchParams.get("tamanho_pagina") || 10);
    const pagina = (arr) => ({ itens_totais: arr.length, itens: arr.slice((pg - 1) * tam, pg * tam) });
    const p = u.pathname;
    if (p === "/v1/pessoas/conta-conectada") return json(200, { id_empresa: "999", razao_social: "Beauty Smile Ltda", documento: "00000000000100" });
    if (p.endsWith("contas-a-receber/buscar")) return json(200, pagina(receber));
    if (p.endsWith("contas-a-pagar/buscar")) return json(200, pagina(pagar));
    if (p === "/v1/conta-financeira") return json(200, pagina([{ id: "cf1", nome: "Itau", tipo: "CONTA_CORRENTE" }, { id: "cf2", nome: "Caixa", tipo: "OUTROS" }]));
    if (/saldo-atual$/.test(p)) return json(200, { saldo_atual: p.includes("cf1") ? 1000.5 : 200 });
    if (p === "/v1/notas-fiscais-servico") return json(200, pagina([{ id: `n${u.searchParams.get("data_competencia_de")}` }]));
    if (p === "/v1/pessoas" && req.method === "GET") return json(200, { itens: u.searchParams.get("busca") === "12345678900" ? [{ id: "dup", nome: "Ja existe" }] : [], totalItems: 0 });
    if (p.endsWith("/contas-a-receber") && req.method === "POST") {
      if (st.falhar500Post) return json(500, { message: "boom" });
      return json(202, { protocolo: "pr1", status: "PENDING" });
    }
    if (p === "/v1/protocolo/pr1") return json(200, { id: "pr1", status: ++st.proto > 1 ? "SUCCESS" : "PENDING", evento_financeiro_id: "ev1" });
    if (p.startsWith("/v1/financeiro/eventos-financeiros/parcelas/")) return json(200, { id: "x", versao: 3, status: "PENDENTE", nao_pago: 100, data_vencimento: "2026-09-30", valor_composicao: { valor_bruto: 100 } });
    return json(404, { message: "rota nao simulada " + p });
  });
  return new Promise((r) => srv.listen(porta, () => r({ srv, log, st, emitir })));
}
