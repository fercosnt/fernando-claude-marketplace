/**
 * Tabelas de dominio da Rede e o tradutor que as aplica nas respostas.
 *
 * A API devolve quase tudo como codigo numerico (brandCode: 14, statusCode: 8). Sem traducao,
 * qualquer leitura vira consulta a tabela. Aqui as tabelas viram campos legiveis adicionados
 * ao lado do codigo original — nada e removido nem sobrescrito.
 *
 * Divergencias REAIS da documentacao, mantidas de proposito:
 *  - bandeira 3 aparece como "Dinners" em umas tabelas e "Diners" em outras; 12 aparece como
 *    "Credsystem" e como "Mais!". Adotamos a grafia correta e registramos o alias.
 *  - status de parcela de VENDA e "SCHEDULLED" (dois L). Status de RECEBIVEL e "SCHEDULED"
 *    (um L). Nao e erro de digitacao: sao rotas diferentes com grafias diferentes.
 *  - groupBy e MAIUSCULO em /v1/sales/{pv}/summary e minusculo em /v2/payments/summary,
 *    /v3/receivables/summary e /v1/blocks/summary. Ver GROUP_BY por rota.
 */

export const BANDEIRAS: Record<number, string> = {
  1: "Mastercard", 2: "Visa", 3: "Diners", 4: "Cabal", 5: "Sicredi", 6: "Sorocred",
  7: "Hipercard", 8: "CUP", 9: "Calcard", 10: "Construcard", 11: "Avista", 12: "Credsystem",
  13: "Amex", 14: "Elo", 15: "Hiper", 16: "Alelo", 20: "Sodexo", 21: "VR", 22: "Greencard",
  23: "Nutricash", 24: "Planvale", 25: "Verocheque", 26: "Coopercard", 27: "Abrapetite",
  28: "Bamex Beneficios", 29: "Biq Beneficios", 30: "Bonuscred", 31: "Convenios Card",
  32: "Credialimentacao", 33: "Eucard", 34: "Facecard", 35: "Flex", 36: "Goodcard",
  37: "Lecard", 38: "Libercard", 39: "Maxxcard", 40: "Nutricard", 41: "Ok Cartoes",
  42: "Onecard", 43: "Sindplus", 44: "UauhBeneficios", 45: "Vale Shop", 46: "Vegas Card",
  47: "Visasoft Pay", 48: "Volus", 49: "Vscard", 50: "Up Brasil", 51: "Verocard",
  52: "Ticket", 53: "VAN", 54: "PL Itau FAI", 55: "PL Bradesco", 56: "PL Banco do Brasil",
  57: "PL Citibank", 58: "PL Credsystem", 59: "PL Porto Seguro", 60: "Pagamento de Fatura",
  72: "Nova Bandeira", 74: "Banescard", 76: "JCB", 77: "Credz", 999: "Outros",
};

/** Grafias alternativas que aparecem na doc da Rede, para busca por nome nao falhar. */
const ALIAS_BANDEIRA: Record<string, number> = {
  dinners: 3, diners: 3, sicred: 5, sicredi: 5, cup: 8, "mais!": 12, mais: 12,
  credsystem: 12, amex: 13, "american express": 13, elo: 14, jcb: 76,
};

export const MODALIDADES: Record<number, string> = { 1: "CREDIT", 2: "DEBIT", 3: "VAN" };
export const MODALIDADE_PT: Record<string, string> = {
  CREDIT: "Credito", DEBIT: "Debito", VAN: "Voucher",
};

/** productCode -> nome do produto (modalityProduct). */
export const PRODUTOS: Record<number, string> = {
  0: "NO_INSTALLMENTS_DEBIT", 1: "NO_INSTALLMENTS", 2: "IN_INSTALLMENTS_WITH_INTEREST",
  3: "IN_INSTALLMENTS_NO_INTEREST", 4: "CREDIT_PLAN", 5: "PRE_DATED", 6: "FUEL", 7: "FOOD",
  8: "AWARD", 9: "PRIVATE_LABEL", 10: "COVENANT", 11: "MEAL", 12: "PREMIUM",
  13: "MULT_BENEFITS", 14: "DRUGSTORE", 15: "FLEET", 16: "CULTURE", 17: "AUTOMOBILE",
  18: "GIFT", 19: "VOUCHER", 99: "OTHERS",
};

export const PRODUTO_PT: Record<string, string> = {
  NO_INSTALLMENTS_DEBIT: "Debito a vista", NO_INSTALLMENTS: "Credito a vista",
  IN_INSTALLMENTS_WITH_INTEREST: "Parcelado com juros", IN_INSTALLMENTS_NO_INTEREST: "Parcelado sem juros",
  CREDIT_PLAN: "Crediario", PRE_DATED: "Pre-datado", FUEL: "Combustivel", FOOD: "Alimentacao",
  AWARD: "Premiacao", PRIVATE_LABEL: "Private label", COVENANT: "Convenio", MEAL: "Refeicao",
  PREMIUM: "Premium", MULT_BENEFITS: "Multi beneficio", DRUGSTORE: "Farmacia",
  FLEET: "Gestao de frota", CULTURE: "Cultura", AUTOMOBILE: "Auto", GIFT: "Gift",
  VOUCHER: "Voucher", NO_INSTALLMENTS_PIX: "Pix nao parcelado", OTHERS: "Outros",
  TOTAL_HATES: "Taxas cobradas (MDR + Flex)", TOTALS: "Totais",
  TOTAL_RECEIVABLES: "Total de recebimentos", TOTAL_ADJUSTMENTS_AND_CHARGES: "Total de ajustes e cobrancas",
  IN_INSTALLMENTS_2_6: "Credito parcelado 2 a 6", IN_INSTALLMENTS_7_12: "Credito parcelado 7 a 12",
  IN_INSTALLMENTS_13_21: "Credito parcelado 13 a 21",
};

export const STATUS_VENDA: Record<string, string> = { APPROVED: "Aprovada", CANCELLED: "Cancelada" };

export const STATUS_TYPE_VENDA: Record<string, string> = {
  COMPLETE: "Aprovada total", PARTIAL: "Aprovada com cancelamento parcial",
  CHARGEBACK: "Cancelamento total por chargeback", CANCELLATION: "Cancelamento total",
  REVERSED: "Estorno realizado", DENIED: "Negada", UNDONE: "Desfeita",
  IN_DISPUTE: "Aprovada em disputa", IN_DISPUTE_PARTIAL: "Parcialmente aprovada em disputa",
  PENDING_PAYMENT: "Pagamento pendente", PAYMENT_REFUND: "Pagamento reembolsado",
};

export const STATUS_PAGAMENTO: Record<number, string> = {
  1: "PENDING", 2: "PAID", 3: "REJECTED", 4: "EXPECTED", 5: "RECEIVED", 6: "FORETHOUGHT",
  7: "CANCELLED", 8: "SUSPENDED", 9: "PAWNED", 10: "BLOCKED", 11: "PAWNED_BLOCKED",
  12: "RETAINED", 14: "CHARGED",
};

export const STATUS_PAGAMENTO_PT: Record<string, string> = {
  PENDING: "Pagamento pendente", PAID: "Pago", REJECTED: "Rejeitado", EXPECTED: "Esperado",
  RECEIVED: "Recebido", FORETHOUGHT: "Previsto", CANCELLED: "Cancelado", SUSPENDED: "Suspenso",
  PAWNED: "Penhorado (gravame)", BLOCKED: "Bloqueado", PAWNED_BLOCKED: "Penhorado e bloqueado",
  RETAINED: "Retido", CHARGED: "Cobrado",
};

export const TIPO_PAGAMENTO: Record<string, string> = {
  CRE: "CREDIT", DEB: "DEBIT", ANT: "ANTICIPATION",
};
export const TIPO_PAGAMENTO_PT: Record<string, string> = {
  CREDIT: "Credito", DEBIT: "Debito", ANTICIPATION: "Antecipacao",
};

/** Parcela de VENDA (dois L, como a API escreve). */
export const STATUS_PARCELA: Record<string, string> = {
  SCHEDULLED: "Agendada", PAID: "Paga", ANTICIPATED: "Antecipada",
  UNBOOK: "Desagendada", BLOCKED: "Bloqueada",
};

/** Recebivel na v3 (um L so). */
export const STATUS_RECEBIVEL: Record<string, string> = {
  SCHEDULED: "Agendado", IN_TRANSIT: "Enviado a CIP para pagamento",
};

export const TIPO_BLOQUEIO: Record<number, string> = { 8: "SUSPENDED", 9: "PAWNED", 12: "RETAINED" };

export const STATUS_CHARGEBACK: Record<string, string> = {
  CHARGEBACK_IN_DISPUTE: "Chargeback em disputa",
  CHARGEBACK_SOLVED_DEBIT: "Chargeback de debito solucionado (impacta o cliente)",
  CHARGEBACK_SOLVED_CREDIT: "Chargeback de credito solucionado (impacta o cliente)",
  CHARGEBACK_SOLVED_NO_IMPACT: "Chargeback solucionado (nao impacta o cliente)",
};

export const TIPO_COBRANCA: Record<string, string> = {
  NET: "Desconta automaticamente do repasse ao estabelecimento",
  NET_EXTERNO: "Debita direto da conta bancaria",
};

export const TIPO_NEGOCIACAO: Record<string, string> = {
  ENCUMBRANCE: "Onus gravame", ENCUMBRANCE_FIDUCIARY: "Onus gravame com cessao fiduciaria",
  ENCUMBRANCE_PAWN: "Onus gravame penhor", ALLOWANCE: "Troca de titularidade (cessao)",
  FREE: "Pagamento livre", FREE_AMOUNT: "Pagamento livre",
};

/**
 * groupBy aceito por rota — a caixa MUDA entre rotas e a Rede devolve 422 se errar.
 * Chave = apelido da rota usado nas tools.
 */
export const GROUP_BY: Record<string, string[]> = {
  vendas_resumo_v1: ["DAY", "WEEK", "MONTH"],
  pagamentos_resumo: ["day", "week", "month", "brand", "status", "type", "bank", "agency", "accountNumber"],
  recebiveis_resumo_v3: ["day", "week", "month", "brand", "modality", "terminal"],
  recebiveis_v2: ["DAY", "WEEK", "MONTH"],
  bloqueios_resumo: ["day"],
};

/** Aceita nome ou codigo e devolve o codigo numerico da bandeira. */
export function codigoBandeira(v: string | number): number {
  if (typeof v === "number") return v;
  const s = String(v).trim();
  if (/^\d+$/.test(s)) return Number(s);
  const k = s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  if (ALIAS_BANDEIRA[k] !== undefined) return ALIAS_BANDEIRA[k];
  const achou = Object.entries(BANDEIRAS).find(
    ([, nome]) => nome.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase() === k
  );
  if (achou) return Number(achou[0]);
  throw new Error(
    `Bandeira "${v}" nao reconhecida. Use o codigo ou o nome exato — os mais comuns: ` +
      `1 Mastercard, 2 Visa, 13 Amex, 14 Elo, 15 Hiper, 7 Hipercard. Lista completa em rede_dominios.`
  );
}

/** Aceita "credito"/"credit"/1 e devolve CREDIT. */
export function nomeModalidade(v: string | number): string {
  if (typeof v === "number" || /^\d+$/.test(String(v))) {
    const n = MODALIDADES[Number(v)];
    if (!n) throw new Error(`Modalidade "${v}" nao existe. Use 1 (CREDIT), 2 (DEBIT) ou 3 (VAN).`);
    return n;
  }
  const k = String(v).normalize("NFD").replace(/[̀-ͯ]/g, "").trim().toUpperCase();
  const mapa: Record<string, string> = {
    CREDITO: "CREDIT", CREDIT: "CREDIT", DEBITO: "DEBIT", DEBIT: "DEBIT",
    VOUCHER: "VAN", VAN: "VAN",
  };
  const n = mapa[k];
  if (!n) throw new Error(`Modalidade "${v}" nao reconhecida. Use CREDIT, DEBIT ou VAN.`);
  return n;
}

/** Valida groupBy contra a rota, preservando a caixa exigida. */
export function validarGroupBy(rota: string, valor: string): string {
  const aceitos = GROUP_BY[rota] ?? [];
  const achou = aceitos.find((a) => a.toLowerCase() === valor.trim().toLowerCase());
  if (!achou) {
    throw new Error(
      `groupBy "${valor}" nao e aceito nesta rota. Valores validos (a caixa importa): ${aceitos.join(", ")}.`
    );
  }
  return achou;
}

// ------------------------------------------------------------------ traducao das respostas

const rotulos: Array<{ de: string; para: string; mapa: (v: unknown) => string | undefined }> = [
  { de: "brandCode", para: "bandeira", mapa: (v) => BANDEIRAS[Number(v)] },
  { de: "modalityCode", para: "modalidade_descricao", mapa: (v) => MODALIDADE_PT[MODALIDADES[Number(v)] ?? ""] },
  { de: "modalityProductCode", para: "produto_descricao", mapa: (v) => PRODUTO_PT[PRODUTOS[Number(v)] ?? ""] },
  { de: "productCode", para: "produto_descricao", mapa: (v) => PRODUTO_PT[PRODUTOS[Number(v)] ?? ""] },
  { de: "statusCode", para: "status_descricao", mapa: (v) => STATUS_PAGAMENTO_PT[STATUS_PAGAMENTO[Number(v)] ?? ""] },
  { de: "blockTypeCode", para: "bloqueio_descricao", mapa: (v) => TIPO_BLOQUEIO[Number(v)] },
  { de: "modalityProduct", para: "produto_descricao", mapa: (v) => PRODUTO_PT[String(v)] },
  { de: "product", para: "produto_descricao", mapa: (v) => PRODUTO_PT[String(v)] },
  { de: "modality", para: "modalidade_descricao", mapa: (v) => (typeof v === "string" ? MODALIDADE_PT[v] : undefined) },
  { de: "chargebackStatus", para: "chargeback_descricao", mapa: (v) => STATUS_CHARGEBACK[String(v)] },
  { de: "statusType", para: "status_tipo_descricao", mapa: (v) => STATUS_TYPE_VENDA[String(v)] },
  { de: "negotiationType", para: "negociacao_descricao", mapa: (v) => TIPO_NEGOCIACAO[String(v)] },
  { de: "type", para: "tipo_descricao", mapa: (v) => TIPO_PAGAMENTO_PT[String(v)] ?? TIPO_COBRANCA[String(v)] },
];

/**
 * Percorre a resposta e acrescenta os campos legiveis. Nao remove nem altera nada do original:
 * quem conferir contra o extrato da Rede continua vendo os mesmos codigos.
 *
 * `status` e ambiguo (venda usa APPROVED, pagamento usa PAID, parcela usa SCHEDULLED), entao
 * so traduzimos quando o valor pertence a exatamente uma das tabelas.
 */
export function traduzir<T>(dado: T, profundidade = 0): T {
  if (profundidade > 12 || dado === null || typeof dado !== "object") return dado;
  if (Array.isArray(dado)) return dado.map((d) => traduzir(d, profundidade + 1)) as unknown as T;

  const o = dado as Record<string, unknown>;
  const saida: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(o)) {
    saida[k] = traduzir(v, profundidade + 1);
  }
  for (const r of rotulos) {
    if (o[r.de] === undefined || o[r.de] === null || saida[r.para] !== undefined) continue;
    const texto = r.mapa(o[r.de]);
    if (texto) saida[r.para] = texto;
  }
  if (typeof o.status === "string" && saida.status_descricao === undefined) {
    const s = o.status;
    const achados = [STATUS_VENDA[s], STATUS_PAGAMENTO_PT[s], STATUS_PARCELA[s], STATUS_RECEBIVEL[s]].filter(Boolean);
    // `status` e ambiguo entre rotas: APPROVED so existe em venda, PAID existe em pagamento
    // ("Pago") e em parcela ("Paga"). Quando as leituras divergem so no genero, sao a mesma
    // coisa e traduzir ajuda; quando divergem de verdade, calar e mais seguro que chutar.
    const raiz = (t: string) => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[oa]$/, "");
    if (achados.length === 1 || (achados.length > 1 && new Set(achados.map(raiz)).size === 1)) {
      saida.status_descricao = achados[0];
    }
  }
  return saida as unknown as T;
}
