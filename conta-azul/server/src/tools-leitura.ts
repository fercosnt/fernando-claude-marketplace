import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import type { Config, Empresa } from "./config.js";
import { contexto, seguro } from "./ctx.js";
import {
  api,
  todasPaginas,
  itensDe,
  totalDe,
  validarData,
  dataIso,
  num,
  arred,
  brl,
  type Params,
} from "./client.js";

// ---------------------------------------------------------------- parametros comuns
const pEmpresa = z
  .string()
  .optional()
  .describe("Nome da empresa configurada. Opcional se houver so uma (ex.: Beauty Smile).");
const pPagina = z.number().int().positive().default(1).describe("Pagina (comeca em 1)");
const TAMANHOS = [10, 20, 50, 100, 200, 500, 1000] as const;
const pTamanho = z
  .number()
  .int()
  .default(50)
  .describe("Itens por pagina. A API so aceita 10, 20, 50, 100, 200, 500 ou 1000 — outros valores sao arredondados para cima.");
const pData = (d: string) => z.string().describe(`${d} — YYYY-MM-DD`);
const pIds = (d: string) => z.array(z.string()).optional().describe(d);

/** A API rejeita tamanho_pagina fora do enum; arredonda para o proximo valido. */
export const tamanhoValido = (n: number, max = 1000) =>
  Math.min(TAMANHOS.find((t) => t >= n) ?? 1000, max);

const STATUS_FIN = ["EM_ABERTO", "ATRASADO", "RECEBIDO", "RECEBIDO_PARCIAL", "RENEGOCIADO", "PERDIDO"] as const;

// ---------------------------------------------------------------- financeiro: busca de parcelas

type Lado = "receber" | "pagar";

function filtrosFinanceiros(a: {
  vencimento_de: string;
  vencimento_ate: string;
  status?: string[];
  descricao?: string;
  competencia_de?: string;
  competencia_ate?: string;
  pagamento_de?: string;
  pagamento_ate?: string;
  valor_de?: number;
  valor_ate?: number;
  ids_contas_financeiras?: string[];
  ids_categorias?: string[];
  ids_centros_de_custo?: string[];
  ids_clientes?: string[];
}): Params {
  validarData(a.vencimento_de, "vencimento_de");
  validarData(a.vencimento_ate, "vencimento_ate");
  for (const k of ["competencia_de", "competencia_ate", "pagamento_de", "pagamento_ate"] as const) {
    if (a[k]) validarData(a[k]!, k);
  }
  return {
    data_vencimento_de: a.vencimento_de,
    data_vencimento_ate: a.vencimento_ate,
    status: a.status,
    descricao: a.descricao,
    data_competencia_de: a.competencia_de,
    data_competencia_ate: a.competencia_ate,
    data_pagamento_de: a.pagamento_de,
    data_pagamento_ate: a.pagamento_ate,
    valor_de: a.valor_de,
    valor_ate: a.valor_ate,
    ids_contas_financeiras: a.ids_contas_financeiras,
    ids_categorias: a.ids_categorias,
    ids_centros_de_custo: a.ids_centros_de_custo,
    ids_clientes: a.ids_clientes,
  };
}

const caminhoLado = (l: Lado) =>
  `/v1/financeiro/eventos-financeiros/contas-a-${l === "receber" ? "receber" : "pagar"}/buscar`;

/** Data de hoje em Sao Paulo (YYYY-MM-DD) — a API trabalha em GMT-3. */
export function hojeSP(): string {
  return process.env.CONTAAZUL_HOJE ?? new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date());
}

const somaDias = (iso: string, d: number) => {
  const x = new Date(`${iso}T12:00:00Z`);
  x.setUTCDate(x.getUTCDate() + d);
  return x.toISOString().slice(0, 10);
};

/**
 * Vencida = venceu antes de hoje e ainda tem saldo em aberto.
 * NAO confiar no status ATRASADO da listagem: na API real ele atrasa (parcela vencida ha dias
 * continua PENDING/EM_ABERTO na busca, embora o detalhe da parcela ja diga ATRASADO).
 */
const vencida = (p: Record<string, unknown>, hoje = hojeSP()) =>
  num(p.nao_pago) > 0 && (dataIso(p.data_vencimento) ?? "9999") < hoje;

const diasAtraso = (p: Record<string, unknown>, hoje = hojeSP()) => {
  const v = dataIso(p.data_vencimento);
  return v ? Math.round((Date.parse(hoje) - Date.parse(v)) / 864e5) : 0;
};

function resumoParcela(p: Record<string, unknown>) {
  const pessoa = (p.cliente ?? p.fornecedor ?? p.contato) as Record<string, unknown> | undefined;
  return {
    id_parcela: p.id,
    descricao: p.descricao,
    vencimento: dataIso(p.data_vencimento) ?? p.data_vencimento,
    competencia: dataIso(p.data_competencia) ?? p.data_competencia,
    status: p.status_traduzido ?? p.status,
    ...(vencida(p) ? { vencida: true, dias_atraso: diasAtraso(p) } : {}),
    total: num(p.total),
    pago: num(p.pago),
    nao_pago: num(p.nao_pago),
    pessoa: pessoa?.nome,
    id_pessoa: pessoa?.id,
    categorias: Array.isArray(p.categorias) ? (p.categorias as Array<{ nome?: string }>).map((c) => c.nome) : undefined,
    centros_custo: Array.isArray(p.centros_custo)
      ? (p.centros_custo as Array<{ nome?: string }>).map((c) => c.nome)
      : undefined,
  };
}

function totaisParcelas(itens: Record<string, unknown>[]) {
  const porStatus: Record<string, { qtd: number; total: number }> = {};
  let total = 0,
    pago = 0,
    naoPago = 0,
    vencido = 0,
    qtdVencidas = 0;
  const hoje = hojeSP();
  for (const p of itens) {
    if (vencida(p, hoje)) {
      vencido += num(p.nao_pago);
      qtdVencidas++;
    }
    const s = String(p.status_traduzido ?? p.status ?? "?");
    porStatus[s] ??= { qtd: 0, total: 0 };
    porStatus[s].qtd++;
    porStatus[s].total = arred(porStatus[s].total + num(p.total));
    total += num(p.total);
    pago += num(p.pago);
    naoPago += num(p.nao_pago);
  }
  return {
    qtd_parcelas: itens.length,
    total: arred(total),
    pago: arred(pago),
    nao_pago: arred(naoPago),
    vencido_nao_pago: { qtd: qtdVencidas, valor: arred(vencido), criterio: `vencimento antes de ${hoje} e saldo em aberto` },
    por_status_da_api: porStatus,
  };
}

function ranking(itens: Record<string, unknown>[], chave: (p: Record<string, unknown>) => string[], campo: "total" | "nao_pago", n = 10) {
  const acc = new Map<string, number>();
  for (const p of itens) {
    for (const k of chave(p)) acc.set(k, (acc.get(k) ?? 0) + num(p[campo]));
  }
  return [...acc.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([nome, valor]) => ({ nome, valor: arred(valor) }));
}

const nomePessoa = (p: Record<string, unknown>) => {
  const x = (p.cliente ?? p.fornecedor ?? p.contato) as { nome?: string } | undefined;
  return [x?.nome ?? "(sem pessoa)"];
};

/**
 * Quanto de cada parcela foi pago DENTRO do periodo, pelas baixas (o detalhe da parcela traz `baixas[]`
 * com data_pagamento). O campo `pago` da busca e o acumulado de todas as baixas — numa parcela paga em
 * partes ao longo de meses, somar `pago` infla o caixa do mes (visto na conta real: R$ 244 mil x o que de fato entrou).
 */
async function pagoNoPeriodo(cfg: Config, emp: Empresa, itens: Record<string, unknown>[], de: string, ate: string, maxDetalhes = 800) {
  let total = 0;
  let semDetalhe = 0;
  let detalhes = 0;
  const porParcela: Array<{ id: unknown; descricao: unknown; pessoa: unknown; no_periodo: number; pago_acumulado: number }> = [];
  for (const p of itens) {
    const pagoAcum = num(p.pago);
    if (!pagoAcum) continue;
    let noPeriodo = pagoAcum;
    if (detalhes < maxDetalhes) {
      try {
        detalhes++;
        const d = (await api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/parcelas/${p.id}` })) as {
          baixas?: Array<{ data_pagamento?: string; valor_composicao?: { valor_liquido?: number; valor_bruto?: number } }>;
        };
        if (Array.isArray(d?.baixas)) {
          noPeriodo = d.baixas
            .filter((b) => {
              const dt = dataIso(b.data_pagamento);
              return !!dt && dt >= de && dt <= ate;
            })
            .reduce((s, b) => s + num(b.valor_composicao?.valor_liquido ?? b.valor_composicao?.valor_bruto), 0);
        } else semDetalhe += pagoAcum;
      } catch {
        semDetalhe += pagoAcum;
      }
    } else semDetalhe += pagoAcum;
    total += noPeriodo;
    const pessoa = (p.cliente ?? p.fornecedor) as { nome?: string } | undefined;
    porParcela.push({ id: p.id, descricao: p.descricao, pessoa: pessoa?.nome, no_periodo: arred(noPeriodo), pago_acumulado: pagoAcum });
  }
  return { total: arred(total), sem_detalhe_de_baixas: arred(semDetalhe), por_parcela: porParcela };
}

/**
 * Valor por categoria usando o rateio do lancamento (a busca so diz QUAIS categorias, nao QUANTO).
 * Parcela com uma categoria: valor inteiro nela. Com mais de uma: busca o detalhe e distribui a parcela
 * na proporcao do `valor` (liquido) de cada rateio — descontos incondicionais tem valor 0 e nao inflam nada.
 * Um detalhe por evento (parcelas do mesmo lancamento compartilham o rateio).
 */
async function categoriasPorRateio(cfg: Config, emp: Empresa, itens: Record<string, unknown>[], maxDetalhes = 400) {
  const acc = new Map<string, number>();
  const somar = (nome: string, v: number) => acc.set(nome, (acc.get(nome) ?? 0) + v);
  const cachePorEvento = new Map<string, Array<{ nome: string; valor: number }>>();
  let detalhes = 0;
  let semRateio = 0;
  for (const p of itens) {
    const cats = Array.isArray(p.categorias) ? (p.categorias as Array<{ nome?: string }>) : [];
    const total = num(p.total);
    if (cats.length <= 1) {
      somar(cats[0]?.nome ?? "(sem categoria)", total);
      continue;
    }
    if (detalhes >= maxDetalhes) {
      semRateio += total;
      continue;
    }
    try {
      detalhes++;
      const d = (await api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/parcelas/${p.id}` })) as {
        evento?: { id?: string; rateio?: Array<{ nome_categoria?: string; valor?: number }> };
      };
      const idEv = d?.evento?.id ?? String(p.id);
      let r = cachePorEvento.get(idEv);
      if (!r) {
        r = (d?.evento?.rateio ?? []).map((x) => ({ nome: x.nome_categoria ?? "?", valor: num(x.valor) }));
        cachePorEvento.set(idEv, r);
      }
      const base = r.reduce((s, x) => s + x.valor, 0);
      if (!base) {
        semRateio += total;
        continue;
      }
      for (const x of r) if (x.valor) somar(x.nome, (total * x.valor) / base);
    } catch {
      semRateio += total;
    }
  }
  if (semRateio) somar("(rateio nao consultado)", semRateio);
  return [...acc.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([nome, valor]) => ({ nome, valor: arred(valor) }));
}

// ================================================================== registro
export function registrarLeitura(server: McpServer) {
  // ------------------------------------------------------------ empresa
  server.registerTool(
    "contaazul_empresa",
    {
      title: "Empresa conectada",
      description: "Dados da empresa conectada (razao social, CNPJ, id_empresa). Bom teste de que a conexao funciona.",
      inputSchema: { empresa: pEmpresa },
    },
    seguro(async (a: { empresa?: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: "/v1/pessoas/conta-conectada" });
    })
  );

  // ------------------------------------------------------------ financeiro
  for (const lado of ["receber", "pagar"] as const) {
    server.registerTool(
      `contaazul_contas_${lado}`,
      {
        title: lado === "receber" ? "Contas a receber (parcelas)" : "Contas a pagar (parcelas)",
        description:
          `Lista as PARCELAS de contas a ${lado} por intervalo de VENCIMENTO (obrigatorio), com filtros opcionais ` +
          `de status, competencia, pagamento, valor, categoria, centro de custo e conta financeira. ` +
          `Traz totais (total, pago, nao pago, por status) calculados sobre tudo o que foi buscado. ` +
          `Status aceitos: ${STATUS_FIN.join(", ")} (a API usa RECEBIDO tambem para contas a pagar quitadas). ` +
          `ATENCAO: o status ATRASADO da busca da API atrasa — parcelas vencidas ha dias aparecem como EM_ABERTO. ` +
          `Para "o que esta atrasado" use somente_vencidas=true (ou leia totais.vencido_nao_pago / o campo vencida de cada parcela), nunca so status=ATRASADO. ` +
          `Para "quanto entrou no mes" use pagamento_de/ate e leia pago_no_periodo_de_pagamento (NAO totais.pago, que e o acumulado da parcela); para "quanto vence" use so o vencimento.`,
        inputSchema: {
          empresa: pEmpresa,
          vencimento_de: pData("Vencimento inicial"),
          vencimento_ate: pData("Vencimento final"),
          status: z.array(z.enum(STATUS_FIN)).optional().describe("Filtra por status"),
          descricao: z.string().optional().describe("Busca na descricao"),
          competencia_de: z.string().optional(),
          competencia_ate: z.string().optional(),
          pagamento_de: z.string().optional().describe("Data de pagamento inicial (YYYY-MM-DD)"),
          pagamento_ate: z.string().optional(),
          valor_de: z.number().optional(),
          valor_ate: z.number().optional(),
          ids_contas_financeiras: pIds("UUIDs de contas financeiras (ver contaazul_contas_financeiras)"),
          ids_categorias: pIds("UUIDs de categorias (ver contaazul_categorias)"),
          ids_centros_de_custo: pIds("UUIDs de centros de custo"),
          ...(lado === "receber" ? { ids_clientes: pIds("UUIDs de clientes (ver contaazul_pessoas)") } : {}),
          somente_vencidas: z
            .boolean()
            .default(false)
            .describe("true = so parcelas com vencimento antes de hoje e saldo em aberto (calculado pela data, nao pelo status da API)"),
          limite: z.number().int().positive().max(5000).default(200).describe("Maximo de parcelas listadas na resposta"),
          formato: z.enum(["resumo", "detalhado"]).default("resumo").describe("detalhado = payload cru da API"),
        },
      },
      seguro(async (a: Record<string, unknown>) => {
        const { cfg, emp } = contexto(a.empresa as string | undefined);
        const params = filtrosFinanceiros(a as never);
        if (a.somente_vencidas) {
          const ontem = somaDias(hojeSP(), -1);
          if (String(params.data_vencimento_ate) > ontem) params.data_vencimento_ate = ontem;
          if (!params.status) params.status = ["EM_ABERTO", "ATRASADO", "RECEBIDO_PARCIAL"];
        }
        const r = await todasPaginas(cfg, emp, { caminho: caminhoLado(lado), params }, { tamanho: 500, maxItens: 5000 });
        if (a.somente_vencidas) r.itens = r.itens.filter((p) => vencida(p));
        const limite = a.limite as number;
        let noPeriodo: Awaited<ReturnType<typeof pagoNoPeriodo>> | null = null;
        if (a.pagamento_de || a.pagamento_ate) {
          noPeriodo = await pagoNoPeriodo(cfg, emp, r.itens, (a.pagamento_de as string) ?? "0000-01-01", (a.pagamento_ate as string) ?? "9999-12-31");
        }
        const mapaPeriodo = new Map((noPeriodo?.por_parcela ?? []).map((x) => [x.id, x.no_periodo]));
        return {
          periodo_vencimento: `${a.vencimento_de} a ${a.vencimento_ate}`,
          ...(noPeriodo
            ? {
                pago_no_periodo_de_pagamento: {
                  valor: noPeriodo.total,
                  criterio: "soma das baixas com data de pagamento dentro do filtro (nao o acumulado pago da parcela)",
                  ...(noPeriodo.sem_detalhe_de_baixas ? { sem_detalhe_de_baixas: noPeriodo.sem_detalhe_de_baixas } : {}),
                },
              }
            : {}),
          totais: totaisParcelas(r.itens),
          total_informado_pela_api: r.total_informado,
          aviso: r.truncado ? "Mais de 5000 parcelas — totais parciais. Reduza o periodo." : null,
          exibindo: `${Math.min(limite, r.itens.length)} de ${r.itens.length}`,
          parcelas: r.itens
            .slice(0, limite)
            .map((p) => (a.formato === "detalhado" ? p : { ...resumoParcela(p), ...(noPeriodo ? { pago_no_periodo: mapaPeriodo.get(p.id) ?? 0 } : {}) })),
        };
      })
    );
  }

  server.registerTool(
    "contaazul_resumo_financeiro",
    {
      title: "Resumo financeiro do periodo",
      description:
        "Visao consolidada de um periodo em uma chamada. (1) Por VENCIMENTO: a receber e a pagar que vencem no periodo " +
        "(total, quitado, em aberto, vencido sem pagamento), saldo previsto, maiores clientes/fornecedores e valor por " +
        "categoria calculado pelo rateio real (descontos nao inflam o ranking). (2) CAIXA: o que foi efetivamente recebido " +
        "e pago com data de pagamento no periodo. (3) Saldo atual de cada conta financeira. Use para 'como esta o " +
        "financeiro de setembro?' — e diga sempre qual dos criterios cada numero usa.",
      inputSchema: {
        empresa: pEmpresa,
        de: pData("Inicio do periodo"),
        ate: pData("Fim do periodo"),
        incluir_saldos: z.boolean().default(true).describe("Consulta o saldo atual de cada conta financeira"),
        incluir_categorias: z
          .boolean()
          .default(true)
          .describe("Calcula o valor por categoria pelo rateio de cada lancamento (1 chamada extra por lancamento com mais de uma categoria)"),
      },
    },
    seguro(async (a: { empresa?: string; de: string; ate: string; incluir_saldos: boolean; incluir_categorias: boolean }) => {
      const { cfg, emp } = contexto(a.empresa);
      const params = filtrosFinanceiros({ vencimento_de: a.de, vencimento_ate: a.ate });
      // Caixa: pagamento dentro do periodo, qualquer vencimento num horizonte de 2 anos para cada lado.
      const paramsCaixa = filtrosFinanceiros({
        vencimento_de: somaDias(a.de, -730),
        vencimento_ate: somaDias(a.ate, 730),
        pagamento_de: a.de,
        pagamento_ate: a.ate,
      });
      const buscar = (l: Lado, p: Params) =>
        todasPaginas(cfg, emp, { caminho: caminhoLado(l), params: p }, { tamanho: 500, maxItens: 10000 });
      const [rec, pag] = await Promise.all([buscar("receber", params), buscar("pagar", params)]);
      const [recCx, pagCx] = await Promise.all([buscar("receber", paramsCaixa), buscar("pagar", paramsCaixa)]);
      const tr = totaisParcelas(rec.itens);
      const tp = totaisParcelas(pag.itens);

      let catRec: unknown = "nao calculado";
      let catPag: unknown = "nao calculado";
      if (a.incluir_categorias) {
        catRec = await categoriasPorRateio(cfg, emp, rec.itens);
        catPag = await categoriasPorRateio(cfg, emp, pag.itens);
      }

      let saldos: unknown = "nao consultado";
      if (a.incluir_saldos) {
        const contas = await todasPaginas(cfg, emp, { caminho: "/v1/conta-financeira", params: { apenas_ativo: true } }, { tamanho: 100 });
        const lista = [];
        for (const c of contas.itens) {
          try {
            const s = (await api(cfg, emp, { caminho: `/v1/conta-financeira/${c.id}/saldo-atual` })) as { saldo_atual?: number };
            lista.push({ conta: c.nome, tipo: c.tipo, saldo: num(s?.saldo_atual) });
          } catch (e) {
            lista.push({ conta: c.nome, tipo: c.tipo, erro: (e as Error).message });
          }
        }
        const soma = lista.reduce((s, x) => s + ("saldo" in x ? (x.saldo as number) : 0), 0);
        saldos = { total: arred(soma), total_brl: brl(soma), contas: lista };
      }

      const [cxIn, cxOut] = [await pagoNoPeriodo(cfg, emp, recCx.itens, a.de, a.ate), await pagoNoPeriodo(cfg, emp, pagCx.itens, a.de, a.ate)];
      const entradas = cxIn.total;
      const saidas = cxOut.total;

      return {
        periodo: `${a.de} a ${a.ate}`,
        por_vencimento: {
          criterio: "parcelas com VENCIMENTO no periodo, qualquer que seja a data de pagamento",
          a_receber: { ...tr, maiores_clientes: ranking(rec.itens, nomePessoa, "total"), por_categoria: catRec },
          a_pagar: { ...tp, maiores_fornecedores: ranking(pag.itens, nomePessoa, "total"), por_categoria: catPag },
          saldo_previsto: arred(tr.total - tp.total),
        },
        caixa_no_periodo: {
          criterio: "parcelas com DATA DE PAGAMENTO no periodo (inclui atrasados de meses anteriores e adiantamentos)",
          entradas,
          saidas,
          liquido: arred(entradas - saidas),
          qtd_parcelas_com_recebimento: recCx.itens.length,
          qtd_parcelas_com_pagamento: pagCx.itens.length,
          obs: "Soma so as baixas (pagamentos) com data dentro do periodo, valor liquido. Parcela paga em partes ao longo de meses entra so com a parte do periodo.",
          ...(cxIn.sem_detalhe_de_baixas || cxOut.sem_detalhe_de_baixas
            ? { aviso: `Sem detalhe de baixas para R$ ${cxIn.sem_detalhe_de_baixas} de entradas e R$ ${cxOut.sem_detalhe_de_baixas} de saidas — nesses entrou o acumulado pago.` }
            : {}),
        },
        saldos_atuais: saldos,
        avisos: [
          rec.truncado || pag.truncado || recCx.truncado || pagCx.truncado
            ? "ATENCAO: limite de 10000 parcelas atingido — totais parciais."
            : null,
          Math.abs(tr.pago + tr.nao_pago - tr.total) > 1 || Math.abs(tp.pago + tp.nao_pago - tp.total) > 1
            ? "pago + nao_pago difere do total em algumas parcelas (juros, multa, desconto ou taxa na baixa) — normal."
            : null,
        ].filter(Boolean),
      };
    })
  );

  server.registerTool(
    "contaazul_parcela",
    {
      title: "Parcela por id",
      description:
        "Detalhe de uma parcela (receber ou pagar): evento, rateio por categoria e centro de custo, composicao de valor, status, versao. " +
        "Com incluir_baixas=true traz tambem os pagamentos (baixas) registrados.",
      inputSchema: {
        empresa: pEmpresa,
        id: z.string().describe("UUID da parcela (id_parcela das listagens)"),
        incluir_baixas: z.boolean().default(false),
      },
    },
    seguro(async (a: { empresa?: string; id: string; incluir_baixas: boolean }) => {
      const { cfg, emp } = contexto(a.empresa);
      const parcela = await api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/parcelas/${a.id}` });
      if (!a.incluir_baixas) return parcela;
      const baixas = await api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/parcelas/${a.id}/baixa` });
      return { parcela, baixas };
    })
  );

  server.registerTool(
    "contaazul_parcelas_do_evento",
    {
      title: "Parcelas de um lancamento",
      description: "Lista todas as parcelas de um evento financeiro (lancamento de receber ou pagar) pelo id_evento.",
      inputSchema: { empresa: pEmpresa, id_evento: z.string() },
    },
    seguro(async (a: { empresa?: string; id_evento: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/${a.id_evento}/parcelas` });
    })
  );

  server.registerTool(
    "contaazul_contas_financeiras",
    {
      title: "Contas financeiras e saldos",
      description:
        "Lista as contas financeiras (banco, caixa, cartao, cobrancas Conta Azul...) com id, tipo e, opcionalmente, o saldo atual de cada uma.",
      inputSchema: {
        empresa: pEmpresa,
        apenas_ativo: z.boolean().default(true),
        com_saldo: z.boolean().default(true),
        nome: z.string().optional(),
      },
    },
    seguro(async (a: { empresa?: string; apenas_ativo: boolean; com_saldo: boolean; nome?: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/conta-financeira",
        params: { apenas_ativo: a.apenas_ativo, nome: a.nome },
      }, { tamanho: 100 });
      const contas = [];
      for (const c of r.itens) {
        const base = { id: c.id, nome: c.nome, tipo: c.tipo, banco: c.banco, ativo: c.ativo, conta_padrao: c.conta_padrao };
        if (!a.com_saldo) {
          contas.push(base);
          continue;
        }
        try {
          const s = (await api(cfg, emp, { caminho: `/v1/conta-financeira/${c.id}/saldo-atual` })) as { saldo_atual?: number };
          contas.push({ ...base, saldo_atual: num(s?.saldo_atual) });
        } catch (e) {
          contas.push({ ...base, saldo_erro: (e as Error).message });
        }
      }
      const total = contas.reduce((s, c) => s + num((c as { saldo_atual?: number }).saldo_atual), 0);
      return { qtd: contas.length, ...(a.com_saldo ? { saldo_total: arred(total) } : {}), contas };
    })
  );

  server.registerTool(
    "contaazul_categorias",
    {
      title: "Categorias financeiras",
      description: "Lista categorias de receita/despesa (id, nome, tipo, hierarquia). Os ids servem para filtrar e para criar lancamentos.",
      inputSchema: {
        empresa: pEmpresa,
        tipo: z.enum(["RECEITA", "DESPESA"]).optional(),
        busca: z.string().optional().describe("Busca por nome ou codigo"),
        apenas_filhos: z.boolean().optional().describe("So categorias-filhas (as que aceitam lancamento)"),
      },
    },
    seguro(async (a: { empresa?: string; tipo?: string; busca?: string; apenas_filhos?: boolean }) => {
      const { cfg, emp } = contexto(a.empresa);
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/categorias",
        params: { tipo: a.tipo, busca: a.busca, apenas_filhos: a.apenas_filhos, permite_apenas_filhos: false },
      }, { tamanho: 500 });
      return { qtd: r.itens.length, categorias: r.itens };
    })
  );

  server.registerTool(
    "contaazul_categorias_dre",
    {
      title: "Estrutura do DRE",
      description: "Categorias do DRE (Demonstracao do Resultado) com a hierarquia contabil usada pela empresa.",
      inputSchema: { empresa: pEmpresa },
    },
    seguro(async (a: { empresa?: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: "/v1/financeiro/categorias-dre" });
    })
  );

  server.registerTool(
    "contaazul_centros_de_custo",
    {
      title: "Centros de custo",
      description: "Lista centros de custo (id, codigo, nome, ativo).",
      inputSchema: {
        empresa: pEmpresa,
        busca: z.string().optional(),
        filtro: z.enum(["ATIVO", "INATIVO", "TODOS"]).default("ATIVO"),
      },
    },
    seguro(async (a: { empresa?: string; busca?: string; filtro: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/centro-de-custo",
        params: { busca: a.busca, filtro_rapido: a.filtro },
      }, { tamanho: 500 });
      return { qtd: r.itens.length, centros_de_custo: r.itens };
    })
  );

  server.registerTool(
    "contaazul_transferencias",
    {
      title: "Transferencias entre contas",
      description: "Transferencias entre contas financeiras num periodo.",
      inputSchema: {
        empresa: pEmpresa,
        data_inicio: pData("Inicio"),
        data_fim: pData("Fim"),
        ids_conta_financeira: pIds("Filtra por conta financeira"),
      },
    },
    seguro(async (a: { empresa?: string; data_inicio: string; data_fim: string; ids_conta_financeira?: string[] }) => {
      const { cfg, emp } = contexto(a.empresa);
      validarData(a.data_inicio, "data_inicio");
      validarData(a.data_fim, "data_fim");
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/financeiro/transferencias",
        params: { data_inicio: a.data_inicio, data_fim: a.data_fim, ids_conta_financeira: a.ids_conta_financeira },
      }, { tamanho: 500 });
      return { qtd: r.itens.length, transferencias: r.itens };
    })
  );

  server.registerTool(
    "contaazul_alteracoes_financeiras",
    {
      title: "Lancamentos alterados no periodo",
      description:
        "IDs dos eventos financeiros (receber/pagar) criados ou alterados entre duas datas-hora. A API nao tem webhook: " +
        "esta e a forma de saber o que mudou desde a ultima consulta.",
      inputSchema: {
        empresa: pEmpresa,
        data_inicio: z.string().describe("YYYY-MM-DD ou YYYY-MM-DDTHH:mm:ss (horario de Sao Paulo)"),
        data_fim: z.string().describe("YYYY-MM-DD ou YYYY-MM-DDTHH:mm:ss"),
      },
    },
    seguro(async (a: { empresa?: string; data_inicio: string; data_fim: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/financeiro/eventos-financeiros/alteracoes",
        params: { data_inicio: a.data_inicio, data_fim: a.data_fim },
      }, { tamanho: 100 });
      return { qtd: r.itens.length, eventos: r.itens };
    })
  );

  server.registerTool(
    "contaazul_protocolo",
    {
      title: "Status de um protocolo",
      description:
        "Consulta o processamento de um lancamento criado (a criacao de contas a receber/pagar e assincrona e devolve um protocolo). " +
        "PENDING = processando, SUCCESS = criado (traz evento_financeiro_id), ERROR = falhou (traz o motivo).",
      inputSchema: { empresa: pEmpresa, id: z.string() },
    },
    seguro(async (a: { empresa?: string; id: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: `/v1/protocolo/${a.id}` });
    })
  );

  // ------------------------------------------------------------ pessoas
  server.registerTool(
    "contaazul_pessoas",
    {
      title: "Clientes, fornecedores e transportadoras",
      description:
        "Busca pessoas por nome/documento e filtros. ATENCAO: se tipo_perfil e tipo_pessoa forem omitidos, a propria API " +
        "aplica os padroes Cliente e Fisica — para achar um fornecedor PJ, informe os dois.",
      inputSchema: {
        empresa: pEmpresa,
        busca: z.string().optional().describe("Nome ou CPF/CNPJ"),
        tipo_perfil: z.enum(["Cliente", "Fornecedor", "Transportadora"]).optional(),
        tipo_pessoa: z.enum(["Física", "Jurídica", "Estrangeira"]).optional(),
        emails: z.string().optional(),
        documentos: z.string().optional().describe("CPF/CNPJ, separados por virgula"),
        com_endereco: z.boolean().default(false),
        pagina: pPagina,
        tamanho_pagina: pTamanho,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      const r = await api(cfg, emp, {
        caminho: "/v1/pessoas",
        params: {
          busca: a.busca as string,
          tipo_perfil: a.tipo_perfil as string,
          tipos_pessoa: a.tipo_pessoa as string,
          emails: a.emails as string,
          documentos: a.documentos as string,
          com_endereco: a.com_endereco as boolean,
          pagina: a.pagina as number,
          tamanho_pagina: tamanhoValido(a.tamanho_pagina as number),
        },
      });
      return { total: totalDe(r), pagina: a.pagina, pessoas: itensDe(r), ...(itensDe(r).length ? {} : { resposta: r }) };
    })
  );

  server.registerTool(
    "contaazul_pessoa",
    {
      title: "Pessoa por id",
      description: "Cadastro completo de uma pessoa (cliente/fornecedor) pelo UUID.",
      inputSchema: { empresa: pEmpresa, id: z.string() },
    },
    seguro(async (a: { empresa?: string; id: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: `/v1/pessoas/${a.id}` });
    })
  );

  // ------------------------------------------------------------ vendas
  server.registerTool(
    "contaazul_vendas",
    {
      title: "Vendas",
      description:
        "Busca vendas por periodo de emissao, cliente, situacao ou texto. Devolve tambem os totais que a API calcula " +
        "(aprovado, cancelado, esperando aprovacao).",
      inputSchema: {
        empresa: pEmpresa,
        data_inicio: z.string().optional().describe("Emissao inicial YYYY-MM-DD"),
        data_fim: z.string().optional().describe("Emissao final YYYY-MM-DD"),
        termo_busca: z.string().optional().describe("Numero, cliente ou texto"),
        ids_clientes: pIds("UUIDs de clientes"),
        ids_vendedores: pIds("UUIDs de vendedores"),
        situacoes: pIds("Situacoes (ex.: APROVADO, EM_ANDAMENTO, CANCELADO)"),
        ordenar_por: z.enum(["NUMERO", "CLIENTE", "DATA"]).default("DATA"),
        crescente: z.boolean().default(false),
        pagina: pPagina,
        tamanho_pagina: pTamanho,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      for (const k of ["data_inicio", "data_fim"]) if (a[k]) validarData(a[k] as string, k);
      const r = (await api(cfg, emp, {
        caminho: "/v1/venda/busca",
        params: {
          data_inicio: a.data_inicio as string,
          data_fim: a.data_fim as string,
          termo_busca: a.termo_busca as string,
          ids_clientes: a.ids_clientes as string[],
          ids_vendedores: a.ids_vendedores as string[],
          situacoes: a.situacoes as string[],
          [a.crescente ? "campo_ordenado_ascendente" : "campo_ordenado_descendente"]: a.ordenar_por as string,
          pagina: a.pagina as number,
          tamanho_pagina: tamanhoValido(a.tamanho_pagina as number),
        },
      })) as Record<string, unknown>;
      return {
        totais: r?.totais,
        quantidades: r?.quantidades,
        total_itens: totalDe(r),
        pagina: a.pagina,
        vendas: itensDe(r).map((v) => ({
          id: v.id,
          numero: v.numero,
          data: v.data,
          cliente: (v.cliente as { nome?: string })?.nome,
          id_cliente: (v.cliente as { id?: string })?.id,
          total: v.total,
          situacao: (v.situacao as { nome?: string })?.nome ?? v.situacao,
          tipo: v.tipo,
          id_contrato: v.id_contrato,
        })),
      };
    })
  );

  server.registerTool(
    "contaazul_venda",
    {
      title: "Venda por id",
      description: "Detalhe completo de uma venda, com os itens.",
      inputSchema: { empresa: pEmpresa, id: z.string(), incluir_itens: z.boolean().default(true) },
    },
    seguro(async (a: { empresa?: string; id: string; incluir_itens: boolean }) => {
      const { cfg, emp } = contexto(a.empresa);
      const venda = await api(cfg, emp, { caminho: `/v1/venda/${a.id}` });
      if (!a.incluir_itens) return venda;
      const itens = await api(cfg, emp, { caminho: `/v1/venda/${a.id}/itens` }).catch((e) => ({ erro: (e as Error).message }));
      return { venda, itens };
    })
  );

  server.registerTool(
    "contaazul_vendedores",
    {
      title: "Vendedores",
      description: "Lista vendedores cadastrados (id para filtrar vendas e orcamentos).",
      inputSchema: { empresa: pEmpresa },
    },
    seguro(async (a: { empresa?: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: "/v1/venda/vendedores" });
    })
  );

  // ------------------------------------------------------------ orcamentos
  server.registerTool(
    "contaazul_orcamentos",
    {
      title: "Orcamentos",
      description: "Busca orcamentos por periodo, cliente, situacao ou texto.",
      inputSchema: {
        empresa: pEmpresa,
        data_inicio: z.string().optional(),
        data_fim: z.string().optional(),
        termo_busca: z.string().optional(),
        ids_clientes: pIds("UUIDs de clientes"),
        situacoes: pIds("Situacoes do orcamento"),
        pagina: pPagina,
        tamanho_pagina: pTamanho,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      const r = await api(cfg, emp, {
        caminho: "/v1/orcamentos",
        params: {
          data_inicio: a.data_inicio as string,
          data_fim: a.data_fim as string,
          termo_busca: a.termo_busca as string,
          ids_clientes: a.ids_clientes as string[],
          situacoes: a.situacoes as string[],
          campo_ordenado_descendente: "DATA",
          pagina: a.pagina as number,
          tamanho_pagina: tamanhoValido(a.tamanho_pagina as number),
        },
      });
      return r;
    })
  );

  server.registerTool(
    "contaazul_orcamento",
    {
      title: "Orcamento por id",
      description: "Detalhe de um orcamento.",
      inputSchema: { empresa: pEmpresa, id: z.string() },
    },
    seguro(async (a: { empresa?: string; id: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: `/v1/orcamentos/${a.id}` });
    })
  );

  // ------------------------------------------------------------ contratos
  server.registerTool(
    "contaazul_contratos",
    {
      title: "Contratos (vendas recorrentes)",
      description: "Lista contratos recorrentes num intervalo de datas (obrigatorio), com status e busca por nome.",
      inputSchema: {
        empresa: pEmpresa,
        data_inicio: pData("Inicio do intervalo"),
        data_fim: pData("Fim do intervalo"),
        status: z.enum(["TODOS", "ATIVO", "INATIVO", "PROXIMO_AO_VENCIMENTO"]).default("TODOS"),
        busca: z.string().optional(),
        pagina: pPagina,
        tamanho_pagina: z.number().int().min(1).max(50).default(50).describe("Maximo 50"),
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      validarData(a.data_inicio as string, "data_inicio");
      validarData(a.data_fim as string, "data_fim");
      return api(cfg, emp, {
        caminho: "/v1/contratos",
        params: {
          data_inicio: a.data_inicio as string,
          data_fim: a.data_fim as string,
          status: a.status as string,
          busca_textual: a.busca as string,
          pagina: a.pagina as number,
          tamanho_pagina: a.tamanho_pagina as number,
        },
      });
    })
  );

  server.registerTool(
    "contaazul_contrato",
    {
      title: "Contrato por id",
      description: "Detalhe de um contrato recorrente.",
      inputSchema: { empresa: pEmpresa, id: z.string() },
    },
    seguro(async (a: { empresa?: string; id: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: `/v1/contratos/${a.id}` });
    })
  );

  // ------------------------------------------------------------ catalogo
  server.registerTool(
    "contaazul_produtos",
    {
      title: "Produtos",
      description: "Lista produtos por nome/SKU/EAN, status e faixa de preco.",
      inputSchema: {
        empresa: pEmpresa,
        busca: z.string().optional(),
        status: z.enum(["ATIVO", "INATIVO"]).default("ATIVO"),
        pagina: pPagina,
        tamanho_pagina: pTamanho,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      return api(cfg, emp, {
        caminho: "/v1/produtos",
        params: {
          busca: a.busca as string,
          status: a.status as string,
          pagina: a.pagina as number,
          tamanho_pagina: tamanhoValido(a.tamanho_pagina as number),
        },
      });
    })
  );

  server.registerTool(
    "contaazul_servicos",
    {
      title: "Servicos",
      description: "Lista servicos cadastrados (procedimentos, no caso de clinica) por nome, codigo ou descricao.",
      inputSchema: {
        empresa: pEmpresa,
        busca: z.string().optional(),
        pagina: pPagina,
        tamanho_pagina: pTamanho,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      return api(cfg, emp, {
        caminho: "/v1/servicos",
        params: { busca_textual: a.busca as string, pagina: a.pagina as number, tamanho_pagina: a.tamanho_pagina as number },
      });
    })
  );

  // ------------------------------------------------------------ notas fiscais
  server.registerTool(
    "contaazul_notas_fiscais",
    {
      title: "Notas fiscais de produto (NF-e)",
      description: "NF-e emitidas num periodo (obrigatorio), com filtros por documento do tomador, numero ou venda.",
      inputSchema: {
        empresa: pEmpresa,
        data_inicial: pData("Inicio"),
        data_final: pData("Fim"),
        documento_tomador: z.string().optional(),
        numero_nota: z.string().optional(),
        id_venda: z.string().optional(),
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      validarData(a.data_inicial as string, "data_inicial");
      validarData(a.data_final as string, "data_final");
      const r = await todasPaginas(cfg, emp, {
        caminho: "/v1/notas-fiscais",
        params: {
          data_inicial: a.data_inicial as string,
          data_final: a.data_final as string,
          documento_tomador: a.documento_tomador as string,
          numero_nota: a.numero_nota as string,
          id_venda: a.id_venda as string,
        },
      }, { tamanho: 100, maxItens: 2000 });
      return { qtd: r.itens.length, truncado: r.truncado, notas: r.itens };
    })
  );

  server.registerTool(
    "contaazul_notas_servico",
    {
      title: "Notas fiscais de servico (NFS-e)",
      description:
        "NFS-e por periodo de competencia. A API limita cada consulta a 15 dias — periodos maiores sao quebrados " +
        "automaticamente em janelas de 15 dias e somados.",
      inputSchema: {
        empresa: pEmpresa,
        de: pData("Competencia inicial"),
        ate: pData("Competencia final"),
        status: z.array(z.string()).optional().describe("Ex.: EMITIDA, CANCELADA, FALHA, PENDENTE"),
        tipo_negociacao: z.enum(["VENDA", "CONTRATO"]).optional(),
      },
    },
    seguro(async (a: { empresa?: string; de: string; ate: string; status?: string[]; tipo_negociacao?: string }) => {
      const { cfg, emp } = contexto(a.empresa);
      validarData(a.de, "de");
      validarData(a.ate, "ate");
      const janelas = janelasDeDias(a.de, a.ate, 15);
      if (janelas.length > 30) throw new Error("Periodo longo demais (mais de ~15 meses). Reduza.");
      const notas: Record<string, unknown>[] = [];
      for (const [ini, fim] of janelas) {
        const r = await todasPaginas(cfg, emp, {
          caminho: "/v1/notas-fiscais-servico",
          params: { data_competencia_de: ini, data_competencia_ate: fim, status: a.status, tipo_negociacao: a.tipo_negociacao },
          virgula: ["status"],
        }, { tamanho: 100, maxItens: 5000 });
        notas.push(...r.itens);
      }
      return { qtd: notas.length, janelas_consultadas: janelas.length, notas };
    })
  );

  // ------------------------------------------------------------ escape hatch
  server.registerTool(
    "contaazul_get",
    {
      title: "GET generico na API",
      description:
        "Faz um GET em qualquer endpoint /v1/... da API Conta Azul sem tool dedicada (ex.: /v1/produtos/ncm, " +
        "/v1/categorias/configuracao-padrao, /v1/financeiro/eventos-financeiros/saldo-inicial). So leitura. " +
        "Arrays em params viram parametros repetidos.",
      inputSchema: {
        empresa: pEmpresa,
        caminho: z.string().describe("Caminho comecando em /v1/"),
        params: z.record(z.union([z.string(), z.number(), z.boolean(), z.array(z.string())])).optional(),
      },
    },
    seguro(async (a: { empresa?: string; caminho: string; params?: Params }) => {
      if (!/^\/?v1\//.test(a.caminho)) throw new Error("O caminho deve comecar com /v1/.");
      const { cfg, emp } = contexto(a.empresa);
      return api(cfg, emp, { caminho: a.caminho, params: a.params });
    })
  );
}

export function janelasDeDias(de: string, ate: string, dias: number): Array<[string, string]> {
  const out: Array<[string, string]> = [];
  let ini = new Date(`${de}T00:00:00Z`);
  const fim = new Date(`${ate}T00:00:00Z`);
  if (ini > fim) throw new Error("A data inicial e maior que a final.");
  while (ini <= fim) {
    const f = new Date(ini);
    f.setUTCDate(f.getUTCDate() + dias - 1);
    const corte = f > fim ? fim : f;
    out.push([ini.toISOString().slice(0, 10), corte.toISOString().slice(0, 10)]);
    ini = new Date(corte);
    ini.setUTCDate(ini.getUTCDate() + 1);
  }
  return out;
}
