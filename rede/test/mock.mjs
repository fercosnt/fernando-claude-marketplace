/**
 * API da Rede simulada, para testar o plugin inteiro sem credencial real.
 *
 * Reproduz o que o swagger oficial descreve: o OAuth (password, refresh_token e
 * client_credentials), o formato das respostas, a paginacao por cursor, o 204 de consulta
 * vazia, o 422 de parametro invalido e o 401 de token vencido.
 *
 * Os dados sao ficticios e montados de proposito para exercitar a conciliacao: ha resumo de
 * venda que bate, um que diverge por desconto, uma venda ainda nao paga e um pagamento cuja
 * venda e anterior ao periodo.
 */
import { createServer } from "node:http";

const PV = "13381369";
/** "Hoje" da API simulada: parcelas vencidas ate aqui aparecem pagas, as demais agendadas. */
const HOJE = "2026-09-30";
const maisDias = (data, n) => new Date(Date.parse(`${data}T00:00:00Z`) + n * 864e5).toISOString().slice(0, 10);
const CLIENT_ID = "id-de-teste";
const CLIENT_SECRET = "secret-de-teste";
const USUARIO = "usuario-de-teste";
const SENHA = "senha-de-teste";

// ---------------------------------------------------------------- dados
const venda = (nsu, data, rv, bruto, liquido, modalidade, produto, extra = {}) => ({
  merchant: { companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE", tradeName: "LOJA TESTE LTDA" },
  brandCode: modalidade === "DEBIT" ? 2 : 1,
  authorizationCode: 123456,
  modality: {
    type: modalidade,
    code: modalidade === "DEBIT" ? 2 : 1,
    product: produto,
    productCode: produto === "NO_INSTALLMENTS_DEBIT" ? 0 : produto === "NO_INSTALLMENTS" ? 1 : 3,
  },
  installmentQuantity: produto === "IN_INSTALLMENTS_NO_INTEREST" ? 3 : 1,
  nsu,
  saleSummaryNumber: rv,
  movementDate: data,
  saleDate: data,
  saleHour: "14:32:10",
  status: "APPROVED",
  statusType: "COMPLETE",
  deviceType: "POS",
  device: "PV650319",
  captureType: "PDV",
  captureTypeCode: 5,
  amount: bruto,
  mdrFee: modalidade === "DEBIT" ? 1.5 : 2.5,
  mdrAmount: Math.round((bruto - liquido) * 100) / 100,
  flex: false,
  flexFee: 0,
  flexAmount: 0,
  feeTotal: modalidade === "DEBIT" ? 1.5 : 2.5,
  discountAmount: Math.round((bruto - liquido) * 100) / 100,
  netAmount: liquido,
  boardingFeeAmount: 0,
  cardNumber: "532930******7894",
  tokenized: false,
  tracking: [{ amount: bruto, date: data, status: "APPROVED" }],
  ...extra,
});

const VENDAS = [
  venda(111001, "2026-09-01", 900001, 200.0, 197.0, "DEBIT", "NO_INSTALLMENTS_DEBIT"),
  venda(111002, "2026-09-01", 900001, 150.0, 147.75, "DEBIT", "NO_INSTALLMENTS_DEBIT"),
  venda(111003, "2026-09-02", 900002, 1000.0, 975.0, "CREDIT", "NO_INSTALLMENTS"),
  venda(111004, "2026-09-03", 900003, 900.0, 877.5, "CREDIT", "IN_INSTALLMENTS_NO_INTEREST"),
  venda(111005, "2026-09-28", 900004, 500.0, 487.5, "CREDIT", "NO_INSTALLMENTS"),
  // Julho, parcelada em 4x: so a primeira parcela cai na janela — nao pode virar "divergente".
  venda(111006, "2026-07-10", 900005, 1200.0, 1170.0, "CREDIT", "IN_INSTALLMENTS_NO_INTEREST", { installmentQuantity: 4 }),
  // Julho, a vista, intacta — mas o deposito dela leva o estorno da venda abaixo (caso real de producao).
  venda(111007, "2026-07-15", 900006, 1000.0, 975.0, "CREDIT", "NO_INSTALLMENTS"),
  // Junho, estornada parcialmente em 13/08: e a origem do debito de R$ 100 no deposito da 111007.
  venda(111008, "2026-06-20", 900007, 500.0, 487.5, "CREDIT", "NO_INSTALLMENTS", {
    tracking: [
      { amount: 500.0, date: "2026-06-20", status: "APPROVED" },
      { amount: 400.0, date: "2026-08-13", status: "PARTIAL_CANCELLED" },
    ],
  }),
];

/** RV 900003 paga a menos (debito descontado) e RV 899999 e de venda anterior ao periodo. */
const ORDENS = [
  { paymentId: "P20260902001", paymentDate: "2026-09-02", creditOrderNumber: 269010647, saleSummaryNumber: 900001, brandCode: 2, companyNumber: PV, amount: 350.0, discountAmount: 5.25, netAmount: 344.75, type: "DEBIT", typeCode: "DEB" },
  { paymentId: "P20261002001", paymentDate: "2026-10-02", creditOrderNumber: 269010648, saleSummaryNumber: 900002, brandCode: 1, companyNumber: PV, amount: 1000.0, discountAmount: 25.0, netAmount: 975.0, type: "CREDIT", typeCode: "CRE" },
  { paymentId: "P20261002002", paymentDate: "2026-10-02", creditOrderNumber: 269010649, saleSummaryNumber: 900003, brandCode: 1, companyNumber: PV, amount: 900.0, discountAmount: 50.0, netAmount: 850.0, type: "CREDIT", typeCode: "CRE" },
  { paymentId: "P20260901001", paymentDate: "2026-09-01", creditOrderNumber: 269010640, saleSummaryNumber: 899999, brandCode: 1, companyNumber: PV, amount: 310.0, discountAmount: 10.0, netAmount: 300.0, type: "CREDIT", typeCode: "CRE" },
  { paymentId: "P20260810001", paymentDate: "2026-08-10", creditOrderNumber: 269010630, saleSummaryNumber: 900005, brandCode: 1, companyNumber: PV, amount: 300.0, discountAmount: 7.5, netAmount: 292.5, type: "CREDIT", typeCode: "CRE" },
  // Deposito da 111007: previsto 975, pago 875 — os R$ 100 sao o estorno da 111008.
  { paymentId: "P20260815001", paymentDate: "2026-08-15", creditOrderNumber: 269010631, saleSummaryNumber: 900006, brandCode: 1, companyNumber: PV, amount: 1000.0, discountAmount: 25.0, netAmount: 875.0, type: "CREDIT", typeCode: "CRE" },
];

const PAGAMENTOS = [
  { paymentId: "P20260902001", paymentDate: "2026-09-02", bankCode: 237, bankBranchCode: 3757, accountNumber: 3697, brandCode: 2, companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE", tradeName: "LOJA TESTE LTDA", netAmount: 344.75, status: "PAID", statusCode: 2, type: "DEBIT", typeCode: "DEB" },
  { paymentId: "P20261002001", paymentDate: "2026-10-02", bankCode: 237, bankBranchCode: 3757, accountNumber: 3697, brandCode: 1, companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE", tradeName: "LOJA TESTE LTDA", netAmount: 975.0, status: "PAID", statusCode: 2, type: "CREDIT", typeCode: "CRE" },
  { paymentId: "P20261002002", paymentDate: "2026-10-02", bankCode: 237, bankBranchCode: 3757, accountNumber: 3697, brandCode: 1, companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE", tradeName: "LOJA TESTE LTDA", netAmount: 850.0, status: "SUSPENDED", statusCode: 8, type: "CREDIT", typeCode: "CRE" },
  // Deposito da venda 111007 (julho), com o estorno da 111008 descontado.
  { paymentId: "P20260815001", paymentDate: "2026-08-15", bankCode: 237, bankBranchCode: 3757, accountNumber: 3697, brandCode: 1, companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE", tradeName: "LOJA TESTE LTDA", netAmount: 875.0, status: "PAID", statusCode: 2, type: "CREDIT", typeCode: "CRE" },
];

/** Debitos descontados de cada deposito — usados pelo "esperado" e pela rota de charges. */
const DEBITOS = {
  P20261002002: [{ adjustmentTypeCode: 23, debitAmount: 27.5, debitCompensatedAmount: 27.5, debitToBeCompensatedAmount: 0, quantity: 1 }],
  P20260815001: [{ adjustmentTypeCode: 18, debitAmount: 100.0, debitCompensatedAmount: 100.0, debitToBeCompensatedAmount: 0, quantity: 1 }],
};

// ---------------------------------------------------------------- estado do servidor
const tokens = new Map(); // access_token -> { expira, refresh }
const refreshs = new Map(); // refresh_token -> true
let contador = 0;
export const chamadas = [];

const novoToken = () => {
  const access = `access-${++contador}`;
  const refresh = `refresh-${contador}`;
  tokens.set(access, { expira: Date.now() + 1440 * 1000, refresh });
  refreshs.set(refresh, true);
  return { access_token: access, refresh_token: refresh, token_type: "Bearer", expires_in: 1440, scope: "merchant-statement feature_merchant_statement" };
};

/** Permite ao teste simular token vencido do lado do servidor. */
export const invalidarTokens = () => tokens.clear();

const json = (res, status, corpo) => {
  const texto = JSON.stringify(corpo);
  res.writeHead(status, { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(texto) });
  res.end(texto);
};

const cursor = (temMais, chave) => ({ hasNextKey: temMais, ...(temMais ? { nextKey: chave } : {}) });

const dentro = (d, ini, fim) => (!ini || d >= ini) && (!fim || d <= fim);

export function criarMock(porta = 0) {
  const servidor = createServer(async (req, res) => {
    const url = new URL(req.url, "http://local");
    const p = url.pathname;
    const q = Object.fromEntries(url.searchParams);

    // -------------------------------------------------- OAuth
    if (p === "/oauth/token" && req.method === "POST") {
      const corpo = await new Promise((r) => {
        let b = "";
        req.on("data", (d) => (b += d));
        req.on("end", () => r(new URLSearchParams(b)));
      });
      const auth = req.headers.authorization ?? "";
      const [id, secret] = Buffer.from(auth.replace(/^Basic /i, ""), "base64").toString().split(":");
      if (id !== CLIENT_ID || secret !== CLIENT_SECRET) {
        return json(res, 401, { error_description: "Bad credentials", status: "UNAUTHORIZED" });
      }
      const grant = corpo.get("grant_type");
      chamadas.push({ rota: "/oauth/token", grant });
      if (grant === "password") {
        if (corpo.get("username") !== USUARIO || corpo.get("password") !== SENHA) {
          return json(res, 400, { error: "invalid_grant", error_description: "usuario ou senha invalidos" });
        }
        return json(res, 200, novoToken());
      }
      if (grant === "refresh_token") {
        if (!refreshs.has(corpo.get("refresh_token"))) {
          return json(res, 401, { error_description: "Bad credentials", status: "UNAUTHORIZED" });
        }
        refreshs.delete(corpo.get("refresh_token"));
        return json(res, 200, novoToken());
      }
      if (grant === "client_credentials") return json(res, 200, { ...novoToken(), scope: "payment-link" });
      return json(res, 400, { error: "unsupported_grant_type" });
    }

    // -------------------------------------------------- autenticacao das rotas de negocio
    const bearer = (req.headers.authorization ?? "").replace(/^Bearer /i, "");
    const t = tokens.get(bearer);
    if (!t || t.expira < Date.now()) return json(res, 401, { message: "Unauthorized" });

    chamadas.push({ rota: p, query: q, merchantId: req.headers["merchant-id"] ?? null });

    const exigeHeader = () => {
      if (!req.headers["merchant-id"]) {
        json(res, 400, { errors: { MerchantId: ["MerchantId is a required field"] } });
        return true;
      }
      return false;
    };
    const exigeQuery = (campo) => {
      if (!q[campo]) {
        json(res, 422, { [campo]: ["Missing data for required field."] });
        return true;
      }
      return false;
    };

    // -------------------------------------------------- vendas
    if (p === "/merchant-statement/v2/sales" || p === "/merchant-statement/v1/sales") {
      const v2 = p.includes("/v2/");
      // Na API real, a v2 exige parentCompanyNumber apesar de o swagger dizer parentMerchantId.
      if (exigeQuery("parentCompanyNumber")) return;
      void v2;
      if (exigeQuery("subsidiaries") || exigeQuery("startDate") || exigeQuery("endDate")) return;
      let lista = VENDAS.filter((v) => dentro(v.saleDate, q.startDate, q.endDate));
      if (q.brands) lista = lista.filter((v) => q.brands.split(",").includes(String(v.brandCode)));
      if (q.modalities) lista = lista.filter((v) => q.modalities.split(",").includes(v.modality.type));
      if (q.status) lista = lista.filter((v) => v.status === q.status);
      if (!lista.length) return res.writeHead(204).end();
      // Duas paginas de proposito, para exercitar o cursor.
      const pagina2 = q.pageKey === "pagina-2";
      const metade = Math.ceil(lista.length / 2);
      const fatia = pagina2 ? lista.slice(metade) : lista.slice(0, metade);
      return json(res, 200, {
        content: { transactions: fatia },
        cursor: cursor(!pagina2 && lista.length > metade, "pagina-2"),
      });
    }

    let m = p.match(/^\/merchant-statement\/v([12])\/sales\/(\d+)\/summary$/);
    if (m) {
      // Como em producao: um item por dia com venda, do mais recente para o mais antigo.
      const lista = VENDAS.filter((v) => dentro(v.saleDate, q.startDate, q.endDate));
      const dias = [...new Set(lista.map((v) => v.saleDate))].sort().reverse();
      const soma = (l, f) => Math.round(l.reduce((t, v) => t + f(v), 0) * 100) / 100;
      return json(res, 200, {
        content: {
          sales: dias.map((d) => {
            const l = lista.filter((v) => v.saleDate === d);
            return {
              startDate: d, endDate: d,
              amount: soma(l, (v) => v.amount),
              amountCredit: soma(l, (v) => (v.modality.type === "CREDIT" ? v.amount : 0)),
              amountDebit: soma(l, (v) => (v.modality.type === "DEBIT" ? v.amount : 0)),
              netAmount: soma(l, (v) => v.netAmount),
              discountAmount: soma(l, (v) => v.discountAmount),
              quantity: l.length,
            };
          }),
        },
      });
    }

    m = p.match(/^\/merchant-statement\/v1\/sales\/(\d+)\/daily$/);
    if (m) {
      if (exigeQuery("startDate") || exigeQuery("endDate")) return;
      let lista = VENDAS.filter((v) => dentro(v.saleDate, q.startDate, q.endDate));
      if (q.nsu) lista = lista.filter((v) => String(v.nsu) === String(q.nsu));
      if (q.device) lista = lista.filter((v) => v.device === q.device);
      if (!lista.length) return res.writeHead(204).end();
      const dias = [...new Set(lista.map((v) => v.saleDate))].map((d) => {
        const doDia = lista.filter((v) => v.saleDate === d);
        return {
          date: d, count: doDia.length,
          amount: Math.round(doDia.reduce((t, v) => t + v.amount, 0) * 100) / 100,
          netAmount: Math.round(doDia.reduce((t, v) => t + v.netAmount, 0) * 100) / 100,
          sales: doDia,
        };
      });
      return json(res, 200, { content: { salesDaily: dias }, cursor: cursor(false) });
    }

    m = p.match(/^\/merchant-statement\/v2\/payments\/installments\/(\d+)$/);
    if (m) {
      if (exigeQuery("saleDate") || exigeQuery("nsu")) return;
      const v = VENDAS.find((x) => String(x.nsu) === String(q.nsu) && x.saleDate === q.saleDate);
      if (!v) return res.writeHead(204).end();
      const qtd = v.installmentQuantity;
      return json(res, 200, {
        content: {
          installments: Array.from({ length: qtd }, (_, i) => {
            // Credito cai 30 dias apos a venda, uma parcela por mes.
            const vencimento = maisDias(v.saleDate, 30 * (i + 1));
            const paga = vencimento <= HOJE;
            return {
            installmentNumber: i + 1, installmentQuantity: qtd,
            amount: Math.round((v.amount / qtd) * 100) / 100,
            saleAmount: v.amount,
            mdrAmount: Math.round((v.mdrAmount / qtd) * 100) / 100,
            mdrFee: v.mdrFee, flexAmount: 0, flexFee: 0, flex: false, feeTotal: v.feeTotal,
            brand: v.brandCode === 1 ? "MASTERCARD" : "VISA", brandCode: v.brandCode,
            cardNumber: v.cardNumber, authorizationCode: "0116223",
            expirationDate: vencimento,
            status: paga ? "PAID" : "SCHEDULLED",
            paymentId: paga ? `P${vencimento.replace(/-/g, "")}9${String(i + 1).padStart(2, "0")}` : "",
            amountInfo: {
              netAmount: Math.round((v.netAmount / qtd) * 100) / 100,
              originalNetAmount: Math.round((v.netAmount / qtd) * 100) / 100,
              amount: Math.round((v.amount / qtd) * 100) / 100,
              originalAmount: Math.round((v.amount / qtd) * 100) / 100,
              discountAmount: Math.round((v.discountAmount / qtd) * 100) / 100,
              originalDiscountAmount: Math.round((v.discountAmount / qtd) * 100) / 100,
              valueChange: false,
            },
          };
          }),
        },
      });
    }

    if (p === "/merchant-statement/v1/sales/installments") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate")) return;
      const lista = VENDAS.filter((v) => dentro(v.saleDate, q.startDate, q.endDate));
      if (!lista.length) return res.writeHead(204).end();
      return json(res, 200, {
        content: {
          installments: lista.map((v) => ({
            companyNumber: PV, nsu: v.nsu, saleDate: v.saleDate, movementDate: v.saleDate,
            expirationDate: "2026-10-01", installmentQuantity: v.installmentQuantity,
            installmentNumber: 1, saleSummaryNumber: v.saleSummaryNumber,
            mdrAmount: v.mdrAmount, mdrFee: v.mdrFee, amount: v.amount, saleAmount: v.amount,
            discountAmount: v.discountAmount, netAmount: v.netAmount,
          })),
        },
        cursor: cursor(false),
      });
    }

    m = p.match(/^\/merchant-statement\/v2\/payments\/installments\/(\d+)\/(.+)$/);
    if (m) {
      const pid = decodeURIComponent(m[2]);
      const ordens = ORDENS.filter((o) => o.paymentId === pid);
      if (!ordens.length) return res.writeHead(204).end();
      return json(res, 200, {
        content: {
          installments: ordens.map((o) => {
            const v = VENDAS.find((x) => x.saleSummaryNumber === o.saleSummaryNumber) ?? VENDAS[0];
            return {
              installmentQuantity: v.installmentQuantity, nsu: v.nsu, rvNumber: o.saleSummaryNumber,
              orderNumber: "987306", tid: "10011910291921183943", saleDate: v.saleDate,
              parentCompanyNumber: Number(PV), hashUniqueSale: "24b456dd64e1cde8b795c489ba5ab5ee247248af",
              modality: v.modality.type, modalityCode: v.modality.code,
              modalityProduct: v.modality.product, modalityProductCode: v.modality.productCode,
              tokenized: false, originalMdrAmount: v.mdrAmount, originalFlexAmount: 0,
              amountInfo: { netAmount: o.netAmount, originalNetAmount: o.netAmount, amount: o.amount, originalAmount: o.amount, discountAmount: o.discountAmount, originalDiscountAmount: o.discountAmount, valueChange: false },
            };
          }),
          cursor: cursor(false),
        },
      });
    }

    if (p.startsWith("/merchant-statement/v3/payments/installments/central-merchant-id/")) {
      return json(res, 200, {
        content: {
          installments: [{
            headquarterHash: "ab8312a645ad42a6d9bca28346b0aabf06f3f1e9", nsu: 111003, brandCode: 1,
            cardNumber: "650485******3844", amount: 1000.0, netAmount: 975.0, mdrFee: 2.5, mdrAmount: 25.0,
            installmentQuantity: 1, installmentNumber: 1, rvNumber: 900002, saleDate: "2026-09-02",
            pvCode: PV, saleAmount: 1000.0, modality: "CREDIT", modalityCode: 1,
            modalityProduct: "NO_INSTALLMENTS", modalityProductCode: 1, status: "PAID",
            paymentId: "P20261002001", negotiationType: "ENCUMBRANCE", creditOrderOriginPercentageValue: 100,
          }],
          totalNetAmount: 975.0,
        },
        cursor: { hasNextKey: false },
      });
    }

    // -------------------------------------------------- pagamentos
    if (p === "/merchant-statement/v1/payments") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate") || exigeQuery("endDate")) return;
      let lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (q.status) lista = lista.filter((x) => x.status === q.status);
      if (!lista.length) return res.writeHead(204).end();
      return json(res, 200, { content: { payments: lista }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v2/payments/daily") {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (!lista.length) return res.writeHead(204).end();
      const dias = [...new Set(lista.map((x) => x.paymentDate))].map((d) => {
        const doDia = lista.filter((x) => x.paymentDate === d);
        const por = (s) => doDia.filter((x) => x.status === s);
        const tot = (l) => Math.round(l.reduce((t, x) => t + x.netAmount, 0) * 100) / 100;
        return {
          date: d, count: doDia.length, netAmount: tot(doDia),
          paid: { count: por("PAID").length, netAmount: tot(por("PAID")) },
          pending: { count: por("PENDING").length, netAmount: tot(por("PENDING")) },
          suspended: { count: por("SUSPENDED").length, netAmount: tot(por("SUSPENDED")) },
          rejected: { count: por("REJECTED").length, netAmount: tot(por("REJECTED")) },
          payments: doDia,
        };
      });
      return json(res, 200, { content: { paymentsDaily: dias }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v2/payments/summary") {
      if (exigeHeader()) return;
      const lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (!q.groupBy) {
        return json(res, 200, { payments: [{ netAmount: Math.round(lista.reduce((t, x) => t + x.netAmount, 0) * 100) / 100, chargeAmount: 0, expectedAmount: Math.round(lista.reduce((t, x) => t + x.netAmount, 0) * 100) / 100, quantity: lista.length }] });
      }
      if (q.groupBy === "brand") {
        const marcas = [...new Set(lista.map((x) => x.brandCode))];
        return json(res, 200, { payments: marcas.map((b) => { const l = lista.filter((x) => x.brandCode === b); const s = Math.round(l.reduce((t, x) => t + x.netAmount, 0) * 100) / 100; return { brandCode: b, netAmount: s, expectedAmount: s, chargeAmount: 0, quantity: l.length }; }) });
      }
      return json(res, 200, { payments: [{ startDate: q.startDate, endDate: q.endDate, amount: Math.round(lista.reduce((t, x) => t + x.netAmount, 0) * 100) / 100, total: lista.length }] });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/expected\/(\d+)\/(.+)$/);
    if (m) {
      const pg = PAGAMENTOS.find((x) => x.paymentId === decodeURIComponent(m[2]));
      if (!pg) return res.writeHead(204).end();
      // Como na vida real: esperado = pago + o que foi descontado do deposito.
      const descontado = (DEBITOS[pg.paymentId] ?? []).reduce((t, d) => t + d.debitAmount, 0);
      return json(res, 200, { content: { expectedAmount: Math.round((pg.netAmount + descontado) * 100) / 100 } });
    }

    if (p === "/merchant-statement/v1/payments/credit-orders") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate")) return;
      const lista = ORDENS.filter((o) => dentro(o.paymentDate, q.startDate, q.endDate));
      if (!lista.length) return res.writeHead(204).end();
      return json(res, 200, { content: { paymentsCreditOrders: lista }, cursor: cursor(false) });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/charges\/(.+)$/);
    if (m) {
      if (exigeHeader()) return;
      const pid = decodeURIComponent(m[1]);
      if (!DEBITOS[pid]) return res.writeHead(204).end();
      return json(res, 200, { charges: DEBITOS[pid] });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/cashbacks\/(.+)$/);
    if (m) {
      if (exigeHeader()) return;
      return json(res, 200, { cashbacks: [{ adjustmentTypeCode: 211, netAmount: 12.35 }] });
    }

    if (p === "/merchant-statement/v1/blocks/summary") {
      if (exigeQuery("parentCompanyNumber")) return;
      return json(res, 200, { content: [{ blockType: "SUSPENDED", blockTypeCode: 8, startDate: q.startDate, endDate: q.endDate, amountBlock: 850.0, rvNumber: 900003, centralPvCode: PV, paymentId: "P20261002002", event: "BLOCK" }] });
    }

    m = p.match(/^\/merchant-statement\/v1\/blocks\/(\d+)\/(.+)$/);
    if (m) {
      return json(res, 200, { content: { blockSize: 1, blocks: [{ blockType: "SUSPENDED", blockTypeCode: 8, startDate: "2026-10-02", endDate: "2026-10-02", amountBlock: 850.0, centralPvCode: PV, paymentId: decodeURIComponent(m[2]) }], releaseSize: 0, release: [] } });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/(\d+)\/(.+)$/);
    if (m) {
      const pg = PAGAMENTOS.find((x) => x.paymentId === decodeURIComponent(m[2]));
      if (!pg) return res.writeHead(204).end();
      return json(res, 200, { content: { payments: [{ ...pg, headquarterHash: "24b456dd64e1cde8b795c489ba5ab5ee247248af", agency: pg.bankBranchCode, sendDate: pg.paymentDate, hasUpdateValue: "false" }] }, cursor: cursor(false) });
    }

    // -------------------------------------------------- recebiveis
    if (p === "/merchant-statement/v3/receivables/summary") {
      if (exigeHeader()) return;
      const base = { amount: 1362.5, total: 2 };
      if (q.groupBy === "brand") return json(res, 200, { content: [{ brandCode: 1, ...base }] });
      if (q.groupBy) return json(res, 200, { content: [{ startDate: q.startDate, endDate: q.endDate, ...base }] });
      return json(res, 200, { content: [base] });
    }

    m = p.match(/^\/merchant-statement\/v([12])\/receivables\/summary$/);
    if (m) {
      if (exigeQuery("parentCompanyNumber")) return;
      if (m[1] === "2") return json(res, 200, { content: { startDate: q.startDate, endDate: q.endDate, amount: 1362.5, pvCode: PV, type: q.types ?? "DAY", total: 2 } });
      return json(res, 200, { content: { receivables: [{ amount: 1362.5, companyNumber: PV, companyName: "LOJA TESTE", date: "2026-10-02", types: q.types ?? "DAY" }] }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v1/receivables/calendar") {
      if (exigeQuery("parentCompanyNumber")) return;
      return json(res, 200, { content: { daily: { totalAmount: 1362.5, total: 2, receivables: [{ totalAmount: 1362.5, startDate: q.startDate, endDate: q.endDate, amount: 1362.5, pvCode: PV }] }, mouthly: { totalAmount: 1362.5, total: 2, receivables: [] } } });
    }

    if (p === "/merchant-statement/v1/receivables/daily") {
      if (exigeHeader()) return;
      return json(res, 200, { content: { receivables: [{ accountNumber: 3697, accountType: "CC", agency: 3757, bankCode: 237, brandCode: 1, brandName: "Mastercard", date: "2026-10-02", merchantId: PV, merchantName: "LOJA TESTE", modality: "CREDIT", negotiationType: "FREE_AMOUNT", netAmount: 975.0, paymentType: "FREE_AMOUNT", status: "SCHEDULED" }] } });
    }

    if (p === "/merchant-statement/v1/receivables/installments") {
      if (exigeHeader()) return;
      if (exigeQuery("brands")) return;
      return json(res, 200, { content: { installments: [{ accountNumber: 3697, agency: 3757, amount: 1000.0, authorizationCode: "123456", bankCode: 237, brandCode: 1, brandName: "Mastercard", cardNumber: "532930******7894", centralMerchantId: PV, date: "2026-10-02", discountAmount: 25.0, installmentNumber: 1, installmentQuantity: 1, mdrAmount: 25.0, mdrFee: 2.5, merchantId: PV, modality: "CREDIT", netAmount: 975.0, nsu: 111003, rvNumber: 900002, saleAmount: 1000.0, saleDate: "2026-09-02", status: "SCHEDULLED" }], totalNetAmount: 975.0 }, cursor: cursor(false) });
    }

    // -------------------------------------------------- debitos
    if (p === "/merchant-statement/v1/charges") {
      if (exigeQuery("parentCompanyNumber")) return;
      return json(res, 200, { content: { charges: [{ debitCompensatedAmount: 27.5, adjustmentTypeCode: 23, adjustmentTypeDescription: "Aluguel de equipamento", companyNumber: PV, salesSummaryNumber: 900003, paymentDate: "2026-10-02", compensatedDate: "2026-10-02", debitNumber: 1234567, documentNumber: "42010762000380", debitToBeCompensatedAmount: 0, tradeName: "LOJA TESTE LTDA", companyName: "LOJA TESTE", creditOrderExpirationDate: "2026-10-02", creditOrderNumber: 269010649, type: "NET", debitAmount: 27.5 }] }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v1/charges/summary") {
      if (exigeQuery("parentCompanyNumber")) return;
      return json(res, 200, { content: [{ startDate: q.startDate, endDate: q.endDate, adjustmentTypeCode: 23, debitAmount: 27.5, debitCompensatedAmount: 27.5 }] });
    }

    if (p === "/merchant-statement/v1/charges/adjustment-types") {
      return json(res, 200, [
        { code: 1, description: "Pacote ERede" },
        { code: 18, description: "cancelamento de vendas" },
        { code: 23, description: "Aluguel de equipamento" },
        { code: 211, description: "Cashback" },
      ]);
    }

    return json(res, 404, { message: "Not found" });
  });

  return new Promise((r) => servidor.listen(porta, "127.0.0.1", () => r({ servidor, porta: servidor.address().port })));
}

export const CREDENCIAIS = { CLIENT_ID, CLIENT_SECRET, USUARIO, SENHA, PV };
