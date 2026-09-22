/**
 * API da Rede simulada, para testar o plugin inteiro sem credencial real.
 *
 * Reproduz o que o swagger oficial descreve: o OAuth (password, refresh_token e
 * client_credentials), o formato das respostas, a paginacao por cursor, o 204 de consulta
 * vazia, o 422 de parametro invalido e o 401 de token vencido.
 *
 * Os dados sao de uma clinica ficticia (PV 13381369, hoje = 2026-09-30) e saem de uma fonte so:
 * a lista de VENDAS. Dela sai o cronograma de cada parcela (debito em D+1, credito em D+30 por
 * parcela, sempre no proximo dia util), e do cronograma saem as ordens de credito, os pagamentos,
 * os recebiveis, os debitos e os bloqueios. Nenhuma rota conta uma historia diferente das outras:
 * o que venceu ate hoje foi pago (ou esta suspenso), o que vence depois e recebivel.
 *
 * Cenarios montados de proposito:
 *  - setembro: o debito do dia 1 caiu em D+1 com o aluguel da maquininha descontado; o credito
 *    de setembro so cai a partir de outubro;
 *  - parcelado 4x de julho com 2 das 4 parcelas pagas;
 *  - deposito de 14/08 menor pelo estorno parcial de OUTRA venda (a de 20/06, estornada em 13/08);
 *  - deposito de 08/09 que junta parcelas de duas vendas (pagamento e pacote);
 *  - deposito de 28/09 suspenso, sem liberacao ate hoje;
 *  - PV nao liberado (qualquer PV diferente de 13381369): 403/401 por rota, como em producao;
 *  - credencial de projeto Payment Link: autentica, escopo payment-link, 401 em toda rota de extrato.
 */
import { createServer } from "node:http";

const PV = "13381369";
/** "Hoje" da API simulada: o que vence ate aqui aparece pago, o que vence depois e recebivel. */
const HOJE = "2026-09-30";
const maisDias = (data, n) => new Date(Date.parse(`${data}T00:00:00Z`) + n * 864e5).toISOString().slice(0, 10);
const cent = (v) => Math.round(v * 100) / 100;
const soma = (l, f) => cent(l.reduce((t, x) => t + f(x), 0));
const CLIENT_ID = "id-de-teste";
const CLIENT_SECRET = "secret-de-teste";
/** Credencial de um projeto do pacote Payment Link: autentica, mas o token sai com escopo payment-link. */
const CLIENT_ID_PAYMENT_LINK = "id-payment-link";
const CLIENT_SECRET_PAYMENT_LINK = "secret-payment-link";
/** PV que existe mas nao foi liberado para o parceiro. Qualquer PV diferente de PV responde assim. */
const PV_NAO_LIBERADO = "22523510";
const USUARIO = "usuario-de-teste";
const SENHA = "senha-de-teste";

/** Dias sem liquidacao em 2026: sabado, domingo e feriados nacionais bancarios. */
const FERIADOS = new Set([
  "2026-01-01", "2026-02-16", "2026-02-17", "2026-04-03", "2026-04-21", "2026-05-01", "2026-06-04",
  "2026-09-07", "2026-10-12", "2026-11-02", "2026-11-20", "2026-12-25",
]);
const diaUtil = (d) => {
  let x = d;
  while (FERIADOS.has(x) || [0, 6].includes(new Date(`${x}T00:00:00Z`).getUTCDay())) x = maisDias(x, 1);
  return x;
};

// ---------------------------------------------------------------- vendas (a fonte)
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
  mdrAmount: cent(bruto - liquido),
  flex: false,
  flexFee: 0,
  flexAmount: 0,
  feeTotal: modalidade === "DEBIT" ? 1.5 : 2.5,
  discountAmount: cent(bruto - liquido),
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
  // Julho, parcelada em 4x: em 30/09 duas parcelas pagas, duas a receber — nao e "divergente".
  venda(111006, "2026-07-10", 900005, 1200.0, 1170.0, "CREDIT", "IN_INSTALLMENTS_NO_INTEREST", { installmentQuantity: 4 }),
  // Julho, a vista, intacta — mas o deposito dela leva o estorno da venda abaixo (caso real de producao).
  venda(111007, "2026-07-15", 900006, 1000.0, 975.0, "CREDIT", "NO_INSTALLMENTS"),
  // Junho, ja paga em 20/07 e estornada em R$ 100 em 13/08: e a origem do debito no deposito da 111007.
  // Como em producao, o valor do evento de estorno e o valor ESTORNADO (la, 5.400 de uma venda de 6.000).
  venda(111008, "2026-06-20", 900007, 500.0, 487.5, "CREDIT", "NO_INSTALLMENTS", {
    statusType: "PARTIAL",
    tracking: [
      { amount: 500.0, date: "2026-06-20", status: "APPROVED" },
      { amount: 100.0, date: "2026-08-13", status: "PARTIAL_CANCELLED" },
    ],
  }),
  // Agosto: pagas em setembro, entram nas conciliacoes de setembro como "pago sem venda no periodo".
  venda(111009, "2026-08-03", 899999, 310.0, 302.25, "CREDIT", "NO_INSTALLMENTS"),
  // D+30 cai no domingo 06/09, o dia 07/09 e feriado: paga em 08/09, no mesmo deposito da 2a parcela da 111006.
  venda(111010, "2026-08-07", 900008, 450.0, 438.75, "CREDIT", "NO_INSTALLMENTS"),
  // D+30 cai no domingo 27/09: o deposito de 28/09 foi suspenso e nao foi liberado.
  venda(111011, "2026-08-28", 900009, 800.0, 780.0, "CREDIT", "NO_INSTALLMENTS"),
];

/** Debitos descontados do repasse: compensados no deposito do dia, na ordem de credito do resumo `rv`. */
const AJUSTES = [
  // Estorno parcial de R$ 100 da 111008 (20/06), feito em 13/08, descontado do deposito seguinte — que
  // paga a 111007. O debito e LIQUIDO: a Rede devolve a taxa proporcional (2,5% de 100), como no caso
  // real de producao, em que o debito foi 90% da parcela liquida (R$ 526,32).
  { data: "2026-08-14", rv: 900006, codigo: 18, valor: 97.5, numero: 1234560 },
  { data: "2026-09-02", rv: 900001, codigo: 23, valor: 27.5, numero: 1234567 },
];
/** Resumos de venda cujo deposito esta suspenso em HOJE (bloqueio sem liberacao). */
const SUSPENSOS = new Set([900009]);

// ---------------------------------------------------------------- tudo o que deriva das vendas
/** Uma linha por parcela, com a data em que o credito cai. */
const PARCELAS = VENDAS.flatMap((v) => {
  const debito = v.modality.type === "DEBIT";
  const n = debito ? 1 : v.installmentQuantity;
  return Array.from({ length: n }, (_, i) => ({
    venda: v,
    numero: i + 1,
    quantidade: n,
    data: diaUtil(maisDias(v.saleDate, debito ? 1 : 30 * (i + 1))),
    bruto: cent(v.amount / n),
    liquido: cent(v.netAmount / n),
    mdr: cent(v.mdrAmount / n),
    paymentId: "",
  }));
});

const PAGAMENTOS = [];
const ORDENS = [];
/** paymentId -> debitos compensados naquele deposito. */
const DEBITOS = {};
const COBRANCAS = [];
const BLOQUEIOS = [];
{
  // Um pagamento por dia, tipo e bandeira; ids do dia em ordem (debito antes de credito).
  const grupos = new Map();
  for (const p of PARCELAS.filter((x) => x.data <= HOJE)) {
    const k = `${p.data}|${p.venda.modality.type === "DEBIT" ? 0 : 1}|${p.venda.brandCode}`;
    if (!grupos.has(k)) grupos.set(k, []);
    grupos.get(k).push(p);
  }
  const seq = {};
  let ordem = 269010630;
  for (const k of [...grupos.keys()].sort()) {
    const ps = grupos.get(k);
    const [data] = k.split("|");
    const v0 = ps[0].venda;
    seq[data] = (seq[data] ?? 0) + 1;
    const paymentId = `P${data.replace(/-/g, "")}${String(seq[data]).padStart(3, "0")}`;
    for (const p of ps) p.paymentId = paymentId;
    const tipo = v0.modality.type;
    const suspenso = ps.some((p) => SUSPENSOS.has(p.venda.saleSummaryNumber));
    const ajustes = AJUSTES.filter((a) => a.data === data && ps.some((p) => p.venda.saleSummaryNumber === a.rv));
    const liquido = cent(soma(ps, (p) => p.liquido) - soma(ajustes, (a) => a.valor));

    PAGAMENTOS.push({
      paymentId, paymentDate: data, bankCode: 237, bankBranchCode: 3757, accountNumber: 3697,
      brandCode: v0.brandCode, companyNumber: PV, documentNumber: "42010762000380", companyName: "LOJA TESTE",
      tradeName: "LOJA TESTE LTDA", netAmount: liquido,
      status: suspenso ? "SUSPENDED" : "PAID", statusCode: suspenso ? 8 : 2,
      type: tipo, typeCode: tipo === "DEBIT" ? "DEB" : "CRE",
    });

    if (suspenso) {
      // Deposito suspenso nao vira ordem de credito: a parcela fica bloqueada e a conciliacao ve "sem pagamento".
      BLOQUEIOS.push({ blockType: "SUSPENDED", blockTypeCode: 8, date: data, amountBlock: liquido, rvNumber: v0.saleSummaryNumber, centralPvCode: PV, paymentId, event: "BLOCK" });
      continue;
    }

    // Uma ordem de credito por resumo de vendas; o debito sai da ordem do resumo em que foi compensado.
    for (const rv of [...new Set(ps.map((p) => p.venda.saleSummaryNumber))]) {
      const doRv = ps.filter((p) => p.venda.saleSummaryNumber === rv);
      const aj = ajustes.filter((a) => a.rv === rv);
      ORDENS.push({
        paymentId, paymentDate: data, creditOrderNumber: ++ordem, saleSummaryNumber: rv,
        brandCode: v0.brandCode, companyNumber: PV,
        amount: soma(doRv, (p) => p.bruto), discountAmount: soma(doRv, (p) => p.mdr),
        netAmount: cent(soma(doRv, (p) => p.liquido) - soma(aj, (a) => a.valor)),
        type: tipo, typeCode: tipo === "DEBIT" ? "DEB" : "CRE",
      });
      for (const a of aj) {
        (DEBITOS[paymentId] ??= []).push({ adjustmentTypeCode: a.codigo, debitAmount: a.valor, debitCompensatedAmount: a.valor, debitToBeCompensatedAmount: 0, quantity: 1 });
        COBRANCAS.push({
          debitCompensatedAmount: a.valor, adjustmentTypeCode: a.codigo, adjustmentTypeDescription: a.codigo === 18 ? "cancelamento de vendas" : "Aluguel de equipamento",
          companyNumber: PV, salesSummaryNumber: rv, paymentDate: data, compensatedDate: data, debitNumber: a.numero,
          documentNumber: "42010762000380", debitToBeCompensatedAmount: 0, tradeName: "LOJA TESTE LTDA", companyName: "LOJA TESTE",
          creditOrderExpirationDate: data, creditOrderNumber: ordem, type: "NET", debitAmount: a.valor,
        });
      }
    }
  }
}

/** O que ainda vai cair: parcelas com credito depois de HOJE. */
const RECEBIVEIS = PARCELAS.filter((p) => p.data > HOJE).sort((a, b) => a.data.localeCompare(b.data));
const statusDaParcela = (p) => (p.data > HOJE ? "SCHEDULLED" : SUSPENSOS.has(p.venda.saleSummaryNumber) ? "BLOCKED" : "PAID");
/** Hash do pagamento na rota v3 de parcelas: aqui, o paymentId em base64. */
const hashDoPagamento = (pid) => Buffer.from(pid).toString("base64");

// ---------------------------------------------------------------- estado do servidor
const tokens = new Map(); // access_token -> { expira, refresh, escopo }
const refreshs = new Map(); // refresh_token -> escopo
let contador = 0;
export const chamadas = [];

const ESCOPO_EXTRATO = "merchant-statement feature_merchant_statement";
const novoToken = (escopo = ESCOPO_EXTRATO) => {
  const access = `access-${++contador}`;
  const refresh = `refresh-${contador}`;
  tokens.set(access, { expira: Date.now() + 1440 * 1000, refresh, escopo });
  refreshs.set(refresh, escopo);
  return { access_token: access, refresh_token: refresh, token_type: "Bearer", expires_in: 1440, scope: escopo };
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

/** Agrupa uma lista por uma chave, preservando a ordem de chegada. */
const agrupar = (lista, chave) => {
  const m = new Map();
  for (const x of lista) {
    const k = chave(x);
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(x);
  }
  return [...m.entries()];
};
/** Inicio da semana (segunda-feira) de uma data. */
const semana = (d) => maisDias(d, -((new Date(`${d}T00:00:00Z`).getUTCDay() + 6) % 7));

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
      const paymentLink = id === CLIENT_ID_PAYMENT_LINK && secret === CLIENT_SECRET_PAYMENT_LINK;
      if (!paymentLink && (id !== CLIENT_ID || secret !== CLIENT_SECRET)) {
        return json(res, 401, { error_description: "Bad credentials", status: "UNAUTHORIZED" });
      }
      const escopo = paymentLink ? "payment-link" : ESCOPO_EXTRATO;
      const grant = corpo.get("grant_type");
      chamadas.push({ rota: "/oauth/token", grant });
      if (grant === "password") {
        if (corpo.get("username") !== USUARIO || corpo.get("password") !== SENHA) {
          return json(res, 400, { error: "invalid_grant", error_description: "usuario ou senha invalidos" });
        }
        return json(res, 200, novoToken(escopo));
      }
      if (grant === "refresh_token") {
        if (!refreshs.has(corpo.get("refresh_token"))) {
          return json(res, 401, { error_description: "Bad credentials", status: "UNAUTHORIZED" });
        }
        const anterior = refreshs.get(corpo.get("refresh_token"));
        refreshs.delete(corpo.get("refresh_token"));
        return json(res, 200, novoToken(anterior));
      }
      // Como no sandbox real com projeto de APIs de Conciliacao: o escopo sai merchant-statement.
      // Projeto de Payment Link autentica igual, mas o token sai com escopo payment-link.
      if (grant === "client_credentials") return json(res, 200, novoToken(escopo));
      return json(res, 400, { error: "unsupported_grant_type" });
    }

    // -------------------------------------------------- autenticacao das rotas de negocio
    const bearer = (req.headers.authorization ?? "").replace(/^Bearer /i, "");
    const t = tokens.get(bearer);
    if (!t || t.expira < Date.now()) return json(res, 401, { message: "Unauthorized" });

    chamadas.push({ rota: p, query: q, merchantId: req.headers["merchant-id"] ?? null });

    // Token de projeto Payment Link: nenhuma rota de extrato abre, todas respondem 401.
    if (!/merchant-statement/.test(t.escopo)) return json(res, 401, { message: "Unauthorized" });

    // PV nao liberado para o parceiro: como em producao em 2026-09-21, o erro muda com a rota.
    const pvPedido =
      req.headers["merchant-id"] ?? q.parentCompanyNumber ?? q.parentMerchantId ?? (p.match(/\/(\d{7,})(?=\/|$)/) ?? [])[1];
    if (pvPedido && String(pvPedido) !== PV) {
      if (/\/v3\/receivables\//.test(p)) return json(res, 401, { error_code: "1001", message: "Partner not allowed for this merchant" });
      if (p === "/merchant-statement/v2/payments/summary") return json(res, 401, { message: "Insufficient access level to access this feature." });
      return json(res, 403, { message: "Partner not allowed for this company number." });
    }

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
    const vazio = () => res.writeHead(204).end();
    const marcas = () => (q.brands ? q.brands.split(",") : null);

    // -------------------------------------------------- vendas
    if (p === "/merchant-statement/v2/sales" || p === "/merchant-statement/v1/sales") {
      // Na API real, a v2 exige parentCompanyNumber apesar de o swagger dizer parentMerchantId.
      if (exigeQuery("parentCompanyNumber")) return;
      if (exigeQuery("subsidiaries") || exigeQuery("startDate") || exigeQuery("endDate")) return;
      let lista = VENDAS.filter((v) => dentro(v.saleDate, q.startDate, q.endDate));
      if (q.brands) lista = lista.filter((v) => marcas().includes(String(v.brandCode)));
      if (q.modalities) lista = lista.filter((v) => q.modalities.split(",").includes(v.modality.type));
      if (q.status) lista = lista.filter((v) => v.status === q.status);
      if (!lista.length) return vazio();
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
      if (!lista.length) return vazio();
      const dias = [...new Set(lista.map((v) => v.saleDate))].map((d) => {
        const doDia = lista.filter((v) => v.saleDate === d);
        return {
          date: d, count: doDia.length,
          amount: soma(doDia, (v) => v.amount),
          netAmount: soma(doDia, (v) => v.netAmount),
          sales: doDia,
        };
      });
      return json(res, 200, { content: { salesDaily: dias }, cursor: cursor(false) });
    }

    m = p.match(/^\/merchant-statement\/v2\/payments\/installments\/(\d+)$/);
    if (m) {
      if (exigeQuery("saleDate") || exigeQuery("nsu")) return;
      const v = VENDAS.find((x) => String(x.nsu) === String(q.nsu) && x.saleDate === q.saleDate);
      if (!v) return vazio();
      return json(res, 200, {
        content: {
          installments: PARCELAS.filter((x) => x.venda === v).map((x) => ({
            installmentNumber: x.numero, installmentQuantity: x.quantidade,
            amount: x.bruto, saleAmount: v.amount, mdrAmount: x.mdr,
            mdrFee: v.mdrFee, flexAmount: 0, flexFee: 0, flex: false, feeTotal: v.feeTotal,
            brand: v.brandCode === 1 ? "MASTERCARD" : "VISA", brandCode: v.brandCode,
            cardNumber: v.cardNumber, authorizationCode: "0116223",
            expirationDate: x.data,
            status: statusDaParcela(x),
            paymentId: x.paymentId,
            amountInfo: {
              netAmount: x.liquido, originalNetAmount: x.liquido,
              amount: x.bruto, originalAmount: x.bruto,
              discountAmount: x.mdr, originalDiscountAmount: x.mdr,
              valueChange: false,
            },
          })),
        },
      });
    }

    if (p === "/merchant-statement/v1/sales/installments") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate")) return;
      const lista = PARCELAS.filter((x) => dentro(x.venda.saleDate, q.startDate, q.endDate));
      if (!lista.length) return vazio();
      return json(res, 200, {
        content: {
          installments: lista.map((x) => ({
            companyNumber: PV, nsu: x.venda.nsu, saleDate: x.venda.saleDate, movementDate: x.venda.saleDate,
            expirationDate: x.data, installmentQuantity: x.quantidade,
            installmentNumber: x.numero, saleSummaryNumber: x.venda.saleSummaryNumber,
            mdrAmount: x.mdr, mdrFee: x.venda.mdrFee, amount: x.bruto, saleAmount: x.venda.amount,
            discountAmount: x.mdr, netAmount: x.liquido,
          })),
        },
        cursor: cursor(false),
      });
    }

    /** Uma parcela dentro de um pagamento, no formato das rotas que abrem o pacote. */
    const parcelaDoPagamento = (x) => {
      const v = x.venda;
      return {
        installmentQuantity: x.quantidade, installmentNumber: x.numero, nsu: v.nsu, rvNumber: v.saleSummaryNumber,
        orderNumber: "987306", tid: "10011910291921183943", saleDate: v.saleDate,
        parentCompanyNumber: Number(PV), hashUniqueSale: "24b456dd64e1cde8b795c489ba5ab5ee247248af",
        modality: v.modality.type, modalityCode: v.modality.code,
        modalityProduct: v.modality.product, modalityProductCode: v.modality.productCode,
        tokenized: false, originalMdrAmount: x.mdr, originalFlexAmount: 0,
        amountInfo: { netAmount: x.liquido, originalNetAmount: x.liquido, amount: x.bruto, originalAmount: x.bruto, discountAmount: x.mdr, originalDiscountAmount: x.mdr, valueChange: false },
      };
    };

    m = p.match(/^\/merchant-statement\/v2\/payments\/installments\/(\d+)\/(.+)$/);
    if (m) {
      const pid = decodeURIComponent(m[2]);
      const doPagamento = PARCELAS.filter((x) => x.paymentId === pid);
      if (!doPagamento.length) return vazio();
      return json(res, 200, { content: { installments: doPagamento.map(parcelaDoPagamento), cursor: cursor(false) } });
    }

    m = p.match(/^\/merchant-statement\/v3\/payments\/installments\/central-merchant-id\/(\d+)\/payment-id-hash\/(.+)$/);
    if (m) {
      const hash = decodeURIComponent(m[2]);
      const doPagamento = PARCELAS.filter((x) => x.paymentId && hashDoPagamento(x.paymentId) === hash);
      if (!doPagamento.length) return vazio();
      return json(res, 200, {
        content: {
          installments: doPagamento.map((x) => ({
            headquarterHash: "ab8312a645ad42a6d9bca28346b0aabf06f3f1e9", nsu: x.venda.nsu, brandCode: x.venda.brandCode,
            cardNumber: x.venda.cardNumber, amount: x.bruto, netAmount: x.liquido, mdrFee: x.venda.mdrFee, mdrAmount: x.mdr,
            installmentQuantity: x.quantidade, installmentNumber: x.numero, rvNumber: x.venda.saleSummaryNumber,
            saleDate: x.venda.saleDate, pvCode: PV, saleAmount: x.venda.amount, modality: x.venda.modality.type,
            modalityCode: x.venda.modality.code, modalityProduct: x.venda.modality.product,
            modalityProductCode: x.venda.modality.productCode, status: statusDaParcela(x),
            paymentId: x.paymentId, negotiationType: "FREE_AMOUNT", creditOrderOriginPercentageValue: 100,
          })),
          totalNetAmount: soma(doPagamento, (x) => x.liquido),
        },
        cursor: { hasNextKey: false },
      });
    }

    // -------------------------------------------------- pagamentos
    if (p === "/merchant-statement/v1/payments") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate") || exigeQuery("endDate")) return;
      let lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (q.status) lista = lista.filter((x) => x.status === q.status);
      if (q.brands) lista = lista.filter((x) => marcas().includes(String(x.brandCode)));
      if (q.types) lista = lista.filter((x) => x.type === q.types);
      if (!lista.length) return vazio();
      return json(res, 200, { content: { payments: lista }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v2/payments/daily") {
      if (exigeQuery("parentCompanyNumber")) return;
      let lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (q.status) lista = lista.filter((x) => q.status.split(",").includes(x.status));
      if (q.paymentIds) lista = lista.filter((x) => q.paymentIds.split(",").includes(x.paymentId));
      if (!lista.length) return vazio();
      const dias = agrupar(lista, (x) => x.paymentDate).map(([d, doDia]) => {
        const por = (s) => doDia.filter((x) => x.status === s);
        return {
          date: d, count: doDia.length, netAmount: soma(doDia, (x) => x.netAmount),
          paid: { count: por("PAID").length, netAmount: soma(por("PAID"), (x) => x.netAmount) },
          pending: { count: por("PENDING").length, netAmount: soma(por("PENDING"), (x) => x.netAmount) },
          suspended: { count: por("SUSPENDED").length, netAmount: soma(por("SUSPENDED"), (x) => x.netAmount) },
          rejected: { count: por("REJECTED").length, netAmount: soma(por("REJECTED"), (x) => x.netAmount) },
          payments: doDia,
        };
      });
      return json(res, 200, { content: { paymentsDaily: dias }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v2/payments/summary") {
      if (exigeHeader()) return;
      let lista = PAGAMENTOS.filter((x) => dentro(x.paymentDate, q.startDate, q.endDate));
      if (q.status) lista = lista.filter((x) => x.status === q.status);
      if (q.type) lista = lista.filter((x) => x.type === q.type);
      if (q.brand) lista = lista.filter((x) => String(x.brandCode) === String(q.brand));
      // Sem filtro de status, o resumo soma TODOS os pagamentos do periodo, inclusive os suspensos.
      const totais = (l) => {
        const cobrado = soma(l, (x) => soma(DEBITOS[x.paymentId] ?? [], (d) => d.debitAmount));
        const liquido = soma(l, (x) => x.netAmount);
        return { netAmount: liquido, chargeAmount: cobrado, expectedAmount: cent(liquido + cobrado), quantity: l.length };
      };
      if (!q.groupBy) return json(res, 200, { payments: [totais(lista)] });
      const campo = {
        day: (x) => x.paymentDate, week: (x) => semana(x.paymentDate), month: (x) => x.paymentDate.slice(0, 7),
        brand: (x) => x.brandCode, status: (x) => x.status, type: (x) => x.type,
        bank: (x) => x.bankCode, agency: (x) => x.bankBranchCode, accountNumber: (x) => x.accountNumber,
      }[q.groupBy];
      if (!campo) return json(res, 422, { groupBy: ["Invalid value."] });
      const nome = { brand: "brandCode", status: "status", type: "type", bank: "bankCode", agency: "agency", accountNumber: "accountNumber" }[q.groupBy];
      return json(res, 200, {
        payments: agrupar(lista, campo).map(([k, l]) => ({
          ...(nome ? { [nome]: k } : { startDate: l[0].paymentDate, endDate: l[l.length - 1].paymentDate }),
          ...totais(l),
        })),
      });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/expected\/(\d+)\/(.+)$/);
    if (m) {
      const pg = PAGAMENTOS.find((x) => x.paymentId === decodeURIComponent(m[2]));
      if (!pg) return vazio();
      // Como na vida real: esperado = pago + o que foi descontado do deposito.
      const descontado = soma(DEBITOS[pg.paymentId] ?? [], (d) => d.debitAmount);
      return json(res, 200, { content: { expectedAmount: cent(pg.netAmount + descontado) } });
    }

    if (p === "/merchant-statement/v1/payments/credit-orders") {
      if (exigeQuery("parentCompanyNumber") || exigeQuery("startDate")) return;
      const lista = ORDENS.filter((o) => dentro(o.paymentDate, q.startDate, q.endDate));
      if (!lista.length) return vazio();
      return json(res, 200, { content: { paymentsCreditOrders: lista }, cursor: cursor(false) });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/charges\/(.+)$/);
    if (m) {
      if (exigeHeader()) return;
      const pid = decodeURIComponent(m[1]);
      if (!DEBITOS[pid]) return vazio();
      return json(res, 200, { charges: DEBITOS[pid] });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/cashbacks\/(.+)$/);
    if (m) {
      if (exigeHeader()) return;
      // Nenhum deposito da clinica ficticia teve cashback.
      return vazio();
    }

    if (p === "/merchant-statement/v1/blocks/summary") {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = BLOQUEIOS.filter((b) => dentro(b.date, q.startDate, q.endDate));
      if (!lista.length) return vazio();
      if (q.groupBy === "day") {
        return json(res, 200, { content: agrupar(lista, (b) => b.date).map(([d, l]) => ({ startDate: d, endDate: d, amountBlock: soma(l, (b) => b.amountBlock), quantity: l.length })) });
      }
      return json(res, 200, { content: lista.map(({ date, ...b }) => ({ ...b, startDate: date, endDate: date })) });
    }

    m = p.match(/^\/merchant-statement\/v1\/blocks\/(\d+)\/(.+)$/);
    if (m) {
      const pid = decodeURIComponent(m[2]);
      const blocos = BLOQUEIOS.filter((b) => b.paymentId === pid && b.event === "BLOCK");
      const liberacoes = BLOQUEIOS.filter((b) => b.paymentId === pid && b.event === "RELEASE");
      if (!blocos.length && !liberacoes.length) return vazio();
      const fmt = ({ date, event, rvNumber, ...b }) => ({ ...b, startDate: date, endDate: date });
      return json(res, 200, { content: { blockSize: blocos.length, blocks: blocos.map(fmt), releaseSize: liberacoes.length, release: liberacoes.map(fmt) } });
    }

    m = p.match(/^\/merchant-statement\/v1\/payments\/(\d+)\/(.+)$/);
    if (m) {
      const pg = PAGAMENTOS.find((x) => x.paymentId === decodeURIComponent(m[2]));
      if (!pg) return vazio();
      return json(res, 200, { content: { payments: [{ ...pg, headquarterHash: "24b456dd64e1cde8b795c489ba5ab5ee247248af", agency: pg.bankBranchCode, sendDate: pg.paymentDate, hasUpdateValue: "false" }] }, cursor: cursor(false) });
    }

    // -------------------------------------------------- recebiveis (o que vence depois de HOJE)
    const recebiveis = () => {
      let lista = RECEBIVEIS.filter((x) => dentro(x.data, q.startDate, q.endDate));
      if (q.brands) lista = lista.filter((x) => marcas().includes(String(x.venda.brandCode)));
      // Tudo aqui esta agendado; nada foi enviado a CIP ainda.
      if (q.status === "IN_TRANSIT") lista = [];
      return lista;
    };
    const valor = (l) => ({ amount: soma(l, (x) => x.liquido), total: l.length });

    if (p === "/merchant-statement/v3/receivables/summary") {
      if (exigeHeader()) return;
      const lista = recebiveis();
      if (!lista.length) return vazio();
      if (!q.groupBy) return json(res, 200, { content: [valor(lista)] });
      const campo = {
        day: (x) => x.data, week: (x) => semana(x.data), month: (x) => x.data.slice(0, 7),
        brand: (x) => x.venda.brandCode, modality: (x) => x.venda.modality.type, terminal: (x) => x.venda.device,
      }[q.groupBy];
      if (!campo) return json(res, 422, { groupBy: ["Invalid value."] });
      const nome = { brand: "brandCode", modality: "modality", terminal: "terminal" }[q.groupBy];
      return json(res, 200, {
        content: agrupar(lista, campo).map(([k, l]) => ({
          ...(nome ? { [nome]: k } : { startDate: l[0].data, endDate: l[l.length - 1].data }),
          ...valor(l),
        })),
      });
    }

    m = p.match(/^\/merchant-statement\/v([12])\/receivables\/summary$/);
    if (m) {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = recebiveis();
      if (!lista.length) return vazio();
      if (m[1] === "2") return json(res, 200, { content: { startDate: q.startDate, endDate: q.endDate, ...valor(lista), pvCode: PV, type: q.types ?? "DAY" } });
      const porMes = q.types === "MONTH";
      return json(res, 200, {
        content: {
          receivables: agrupar(lista, (x) => (porMes ? x.data.slice(0, 7) : x.data)).map(([k, l]) => ({
            amount: soma(l, (x) => x.liquido), companyNumber: PV, companyName: "LOJA TESTE", date: porMes ? `${k}-01` : k, types: q.types ?? "DAY",
          })),
        },
        cursor: cursor(false),
      });
    }

    if (p === "/merchant-statement/v1/receivables/calendar") {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = recebiveis();
      if (!lista.length) return vazio();
      const bloco = (chave) => ({
        totalAmount: soma(lista, (x) => x.liquido),
        total: lista.length,
        receivables: agrupar(lista, chave).map(([, l]) => ({
          totalAmount: soma(l, (x) => x.liquido), startDate: l[0].data, endDate: l[l.length - 1].data,
          amount: soma(l, (x) => x.liquido), total: l.length, pvCode: PV,
        })),
      });
      return json(res, 200, { content: { daily: bloco((x) => x.data), mouthly: bloco((x) => x.data.slice(0, 7)) } });
    }

    if (p === "/merchant-statement/v1/receivables/daily") {
      if (exigeHeader()) return;
      const lista = recebiveis();
      if (!lista.length) return vazio();
      return json(res, 200, {
        content: {
          receivables: agrupar(lista, (x) => `${x.data}|${x.venda.brandCode}|${x.venda.modality.type}`).map(([, l]) => ({
            accountNumber: 3697, accountType: "CC", agency: 3757, bankCode: 237, brandCode: l[0].venda.brandCode,
            brandName: l[0].venda.brandCode === 1 ? "Mastercard" : "Visa", date: l[0].data, merchantId: PV,
            merchantName: "LOJA TESTE", modality: l[0].venda.modality.type, negotiationType: "FREE_AMOUNT",
            netAmount: soma(l, (x) => x.liquido), paymentType: "FREE_AMOUNT", status: "SCHEDULED",
          })),
        },
      });
    }

    if (p === "/merchant-statement/v1/receivables/installments") {
      if (exigeHeader()) return;
      if (exigeQuery("brands")) return;
      const lista = recebiveis();
      if (!lista.length) return vazio();
      return json(res, 200, {
        content: {
          installments: lista.map((x) => ({
            accountNumber: 3697, agency: 3757, amount: x.bruto, authorizationCode: "123456", bankCode: 237,
            brandCode: x.venda.brandCode, brandName: x.venda.brandCode === 1 ? "Mastercard" : "Visa",
            cardNumber: x.venda.cardNumber, centralMerchantId: PV, date: x.data, discountAmount: x.mdr,
            installmentNumber: x.numero, installmentQuantity: x.quantidade, mdrAmount: x.mdr, mdrFee: x.venda.mdrFee,
            merchantId: PV, modality: x.venda.modality.type, netAmount: x.liquido, nsu: x.venda.nsu,
            rvNumber: x.venda.saleSummaryNumber, saleAmount: x.venda.amount, saleDate: x.venda.saleDate, status: "SCHEDULLED",
          })),
          totalNetAmount: soma(lista, (x) => x.liquido),
        },
        cursor: cursor(false),
      });
    }

    // -------------------------------------------------- debitos
    if (p === "/merchant-statement/v1/charges") {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = COBRANCAS.filter((c) => dentro(c.paymentDate, q.startDate, q.endDate));
      if (!lista.length) return vazio();
      return json(res, 200, { content: { charges: lista }, cursor: cursor(false) });
    }

    if (p === "/merchant-statement/v1/charges/summary") {
      if (exigeQuery("parentCompanyNumber")) return;
      const lista = COBRANCAS.filter((c) => dentro(c.paymentDate, q.startDate, q.endDate));
      if (!lista.length) return vazio();
      return json(res, 200, {
        content: agrupar(lista, (c) => c.adjustmentTypeCode).map(([codigo, l]) => ({
          startDate: q.startDate, endDate: q.endDate, adjustmentTypeCode: codigo,
          debitAmount: soma(l, (c) => c.debitAmount), debitCompensatedAmount: soma(l, (c) => c.debitCompensatedAmount),
        })),
      });
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

export const CREDENCIAIS = { CLIENT_ID, CLIENT_SECRET, USUARIO, SENHA, PV, CLIENT_ID_PAYMENT_LINK, CLIENT_SECRET_PAYMENT_LINK, PV_NAO_LIBERADO };
/** Exposto para os testes conferirem o cenario (ids de pagamento e hash da rota v3). */
export const CENARIO = { HOJE, PAGAMENTOS, ORDENS, RECEBIVEIS, hashDoPagamento };
