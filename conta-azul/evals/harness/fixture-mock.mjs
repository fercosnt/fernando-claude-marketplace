// API Conta Azul simulada com dados ficticios da "Beauty Smile" (hoje = 2026-09-20).
import { createServer } from "node:http";
import { appendFileSync } from "node:fs";

const P = (id, descricao, venc, total, pago, pessoa, cat, dataPag, comp) => {
  const hoje = "2026-09-20";
  const status = pago >= total ? "RECEBIDO" : pago > 0 ? "RECEBIDO_PARCIAL" : venc < hoje ? "ATRASADO" : "EM_ABERTO";
  return { id, descricao, data_vencimento: venc, data_competencia: comp ?? venc, status_traduzido: status, total, pago, nao_pago: +(total - pago).toFixed(2),
    _data_pagamento: dataPag ?? null, cliente: pessoa, categorias: [{ id: cat.id, nome: cat.nome }] };
};
const CAT = { laser: { id: "cat-laser", nome: "Tratamentos Laser" }, clareamento: { id: "cat-clar", nome: "Clareamento" },
  aluguel: { id: "cat-alug", nome: "Aluguel" }, insumos: { id: "cat-ins", nome: "Insumos odontologicos" },
  folha: { id: "cat-folha", nome: "Salarios" }, mkt: { id: "cat-mkt", nome: "Marketing" }, energia: { id: "cat-ener", nome: "Energia" } };
const pes = (id, nome) => ({ id, nome });
const MARIA = pes("pes-maria", "Maria Souza"), JOAO = pes("pes-joao", "Joao Pereira"), ANA = pes("pes-ana", "Ana Lima"),
  CARLA = pes("pes-carla", "Carla Mendes"), PEDRO = pes("pes-pedro", "Pedro Alves");

export const RECEBER = [
  // vencidas em agosto, pagas em setembro (pegadinha do caixa)
  P("par-r01", "Protocolo Melasma 3/3", "2026-08-25", 2400, 2400, ANA, CAT.laser, "2026-09-03"),
  P("par-r02", "Clareamento laser 2/2", "2026-08-30", 1800, 1800, JOAO, CAT.clareamento, "2026-09-02"),
  // setembro pagas em setembro
  P("par-r03", "Protocolo NightLase 1/3", "2026-09-05", 3500, 3500, MARIA, CAT.laser, "2026-09-05"),
  P("par-r04", "Laser gengival", "2026-09-10", 1500, 1500, CARLA, CAT.laser, "2026-09-11"),
  P("par-r05", "Clareamento laser 1/2", "2026-09-12", 1200, 600, PEDRO, CAT.clareamento, "2026-09-12"),
  // setembro em aberto / atrasadas
  P("par-r06", "Protocolo Melasma 1/3", "2026-09-15", 2800, 0, CARLA, CAT.laser),
  P("par-r07", "Protocolo NightLase 2/3", "2026-09-25", 3500, 0, MARIA, CAT.laser),
  P("par-r08", "Laser TMJ", "2026-09-28", 2200, 0, JOAO, CAT.laser),
  // outubro (pago adiantado em setembro)
  P("par-r09", "Protocolo NightLase 3/3", "2026-10-05", 3500, 3500, MARIA, CAT.laser, "2026-09-18"),
  // agosto pago em agosto (nao conta no caixa de setembro)
  P("par-r10", "Laser TMJ entrada", "2026-08-10", 2000, 2000, JOAO, CAT.laser, "2026-08-10"),
];
const F = (id, nome) => ({ id, nome });
const IMOB = F("pes-imob", "Imobiliaria Paulista"), DENTAL = F("pes-dental", "Dental Cremer"), ENEL = F("pes-enel", "Enel SP"), AG = F("pes-ag", "Agencia Pixel");
export const PAGAR = [
  P("par-p01", "Aluguel setembro", "2026-09-05", 12000, 12000, IMOB, CAT.aluguel, "2026-09-05"),
  P("par-p02", "Folha agosto", "2026-09-05", 38000, 38000, F("pes-folha", "Folha de pagamento"), CAT.folha, "2026-09-05"),
  P("par-p03", "Insumos NF 8812", "2026-09-12", 4300, 0, DENTAL, CAT.insumos),
  P("par-p04", "Energia agosto", "2026-09-16", 1850, 0, ENEL, CAT.energia),
  P("par-p05", "Gestao de trafego setembro", "2026-09-22", 6500, 0, AG, CAT.mkt),
  P("par-p06", "Insumos NF 8920", "2026-09-24", 2900, 0, DENTAL, CAT.insumos),
  P("par-p07", "Aluguel outubro", "2026-10-05", 12000, 0, IMOB, CAT.aluguel),
  P("par-p08", "Energia setembro", "2026-10-16", 1900, 0, ENEL, CAT.energia),
].map(({ cliente, ...x }) => ({ ...x, fornecedor: cliente }));

const CONTAS = [
  { id: "cf-itau-bs", nome: "Itau Beauty Smile", tipo: "CONTA_CORRENTE", banco: "ITAU", ativo: true, conta_padrao: true, _saldo: 48210.37 },
  { id: "cf-itau-inv", nome: "Itau Investimentos", tipo: "APLICACAO", banco: "ITAU", ativo: true, conta_padrao: false, _saldo: 150000 },
  { id: "cf-caixa", nome: "Caixa recepcao", tipo: "OUTROS", ativo: true, conta_padrao: false, _saldo: 820 },
  { id: "cf-cobr", nome: "Cobrancas Conta Azul", tipo: "COBRANCAS_CONTA_AZUL", ativo: true, conta_padrao: false, _saldo: 0 },
];
const PESSOAS = [
  { ...MARIA, documento: "11122233344", perfis: ["Cliente"], tipo_pessoa: "Física" },
  { ...JOAO, documento: "22233344455", perfis: ["Cliente"], tipo_pessoa: "Física" },
  { ...ANA, documento: "33344455566", perfis: ["Cliente"], tipo_pessoa: "Física" },
  { ...CARLA, documento: "44455566677", perfis: ["Cliente"], tipo_pessoa: "Física" },
  { ...PEDRO, documento: "55566677788", perfis: ["Cliente"], tipo_pessoa: "Física" },
  { ...IMOB, documento: "12345678000199", perfis: ["Fornecedor"], tipo_pessoa: "Jurídica" },
  { ...DENTAL, documento: "98765432000111", perfis: ["Fornecedor"], tipo_pessoa: "Jurídica" },
  { ...ENEL, documento: "61695227000193", perfis: ["Fornecedor"], tipo_pessoa: "Jurídica" },
  { ...AG, documento: "45678912000100", perfis: ["Fornecedor"], tipo_pessoa: "Jurídica" },
];

const fold = (s) => String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

export function iniciar(logFile) {
  const srv = createServer(async (req, res) => {
    let body = ""; for await (const c of req) body += c;
    const u = new URL(req.url, "http://x"); const q = u.searchParams; const p = u.pathname;
    if (logFile) appendFileSync(logFile, JSON.stringify({ metodo: req.method, caminho: p, query: u.search, corpo: body || undefined }) + "\n");
    const json = (code, o) => { res.writeHead(code, { "Content-Type": "application/json" }); res.end(JSON.stringify(o)); };
    if (p === "/oauth/token") return json(200, { access_token: "at-" + Date.now(), refresh_token: "rt-" + Date.now(), expires_in: 3600 });
    if (!(req.headers.authorization || "").startsWith("Bearer at")) return json(401, { message: "The Token has expired." });
    const pg = Number(q.get("pagina") || 1), tam = Number(q.get("tamanho_pagina") || 10);
    const pagina = (arr) => ({ itens_totais: arr.length, itens: arr.slice((pg - 1) * tam, pg * tam) });
    const entre = (v, de, ate) => (!de || (v && v >= de)) && (!ate || (v && v <= ate));
    const filtrar = (arr) => arr.filter((x) =>
      entre(x.data_vencimento, q.get("data_vencimento_de"), q.get("data_vencimento_ate")) &&
      (!q.get("data_pagamento_de") && !q.get("data_pagamento_ate") || entre(x._data_pagamento, q.get("data_pagamento_de"), q.get("data_pagamento_ate"))) &&
      entre(x.data_competencia, q.get("data_competencia_de"), q.get("data_competencia_ate")) &&
      (!q.getAll("status").length || q.getAll("status").includes(x.status_traduzido)) &&
      (!q.get("descricao") || fold(x.descricao).includes(fold(q.get("descricao")))) &&
      (!q.getAll("ids_categorias").length || q.getAll("ids_categorias").includes(x.categorias[0].id)) &&
      (!q.getAll("ids_clientes").length || q.getAll("ids_clientes").includes(x.cliente?.id))
    ).map(({ _data_pagamento, ...x }) => x);
    if (req.method === "GET") {
      if (p === "/v1/pessoas/conta-conectada") return json(200, { id_empresa: "777", razao_social: "Beauty Smile Odontologia Ltda", nome_fantasia: "Beauty Smile", documento: "00111222000133" });
      if (p.endsWith("contas-a-receber/buscar")) { if (!q.get("data_vencimento_de") || !q.get("data_vencimento_ate")) return json(400, { message: "data_vencimento_de e data_vencimento_ate sao obrigatorios" }); return json(200, pagina(filtrar(RECEBER))); }
      if (p.endsWith("contas-a-pagar/buscar")) { if (!q.get("data_vencimento_de") || !q.get("data_vencimento_ate")) return json(400, { message: "data_vencimento_de e data_vencimento_ate sao obrigatorios" }); return json(200, pagina(filtrar(PAGAR))); }
      if (p === "/v1/conta-financeira") return json(200, pagina(CONTAS.filter((c) => !q.get("nome") || fold(c.nome).includes(fold(q.get("nome")))).map(({ _saldo, ...c }) => c)));
      const ms = p.match(/^\/v1\/conta-financeira\/([^/]+)\/saldo-atual$/);
      if (ms) { const c = CONTAS.find((x) => x.id === ms[1]); return c ? json(200, { saldo_atual: c._saldo }) : json(404, { message: "conta nao encontrada" }); }
      if (p === "/v1/categorias") return json(200, pagina(Object.values(CAT).map((c) => ({ ...c, tipo: ["cat-laser", "cat-clar"].includes(c.id) ? "RECEITA" : "DESPESA" })).filter((c) => !q.get("tipo") || c.tipo === q.get("tipo")).filter((c) => !q.get("busca") || fold(c.nome).includes(fold(q.get("busca"))))));
      if (p === "/v1/centro-de-custo") return json(200, pagina([{ id: "cc-clinica", nome: "Clinica Jardins", ativo: true }]));
      if (p === "/v1/pessoas") {
        const b = fold(q.get("busca"));
        const l = PESSOAS.filter((x) => (!b || fold(x.nome).includes(b) || x.documento.includes(b.replace(/\D/g, "") || "@@")) &&
          (!q.get("tipo_perfil") || x.perfis.includes(q.get("tipo_perfil"))));
        return json(200, { totalItems: l.length, items: l.slice((pg - 1) * tam, pg * tam) });
      }
      const mp = p.match(/^\/v1\/financeiro\/eventos-financeiros\/parcelas\/([^/]+)(\/baixa)?$/);
      if (mp) {
        const x = [...RECEBER, ...PAGAR].find((i) => i.id === mp[1]); if (!x) return json(404, { message: "parcela nao encontrada" });
        if (mp[2]) return json(200, { itens: x.pago ? [{ id: "bx-" + x.id, data_pagamento: x._data_pagamento, valor: x.pago, conta_financeira: "cf-itau-bs" }] : [] });
        const st = { RECEBIDO: "QUITADO", EM_ABERTO: "PENDENTE" }[x.status_traduzido] ?? x.status_traduzido;
        return json(200, { id: x.id, versao: 2, status: st, descricao: x.descricao, data_vencimento: x.data_vencimento, valor_pago: x.pago, nao_pago: x.nao_pago,
          valor_composicao: { valor_bruto: x.total, valor_liquido: x.total }, id_conta_financeira: "cf-itau-bs", evento: { tipo: RECEBER.includes(x) ? "RECEITA" : "DESPESA", rateio: [{ id_categoria: x.categorias[0].id, nome_categoria: x.categorias[0].nome, valor: x.total }] } });
      }
      if (p === "/v1/financeiro/categorias-dre") return json(200, [{ nome: "Receita bruta", filhos: ["Tratamentos Laser", "Clareamento"] }, { nome: "Despesas operacionais", filhos: ["Aluguel", "Salarios", "Insumos odontologicos", "Energia", "Marketing"] }]);
      if (p === "/v1/venda/busca") return json(200, { totais: { total: 0, aprovado: 0 }, quantidades: { total: 0 }, total_itens: 0, itens: [] });
      if (p.startsWith("/v1/protocolo/")) return json(200, { id: p.split("/").pop(), status: "SUCCESS", evento_financeiro_id: "ev-novo" });
      return json(404, { message: "rota nao encontrada " + p });
    }
    // escrita
    if (p.endsWith("/contas-a-pagar") || p.endsWith("/contas-a-receber")) return json(202, { protocolo: "prot-1", status: "PENDING" });
    if (p.endsWith("/baixa")) return json(201, { id: "bx-novo" });
    return json(201, { ok: true });
  });
  return new Promise((r) => srv.listen(0, "127.0.0.1", () => r(srv)));
}
