/**
 * Gestao de Pagamentos — valor LIQUIDO que a Rede deposita, ja descontados MDR e debitos.
 *
 * Um pagamento agrupa varias parcelas de vendas diferentes ("pacote"). Para abrir o pacote,
 * use rede_parcelas_do_pagamento; para saber o que foi descontado dele, rede_debitos_do_pagamento.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { contexto, seguro } from "./ctx.js";
import { api, apiPaginado, juntar, type Params } from "./client.js";
import { validarJanela, LIMITE } from "./periodo.js";
import { validarGroupBy } from "./dominios.js";
import { bandeiras, pBandeiras, pFim, pInicio, pPageKey, pPv, pTamanho, pTudo, resumoPaginacao } from "./comum.js";

const STATUS_PGTO = [
  "PENDING", "PAID", "REJECTED", "EXPECTED", "RECEIVED", "FORETHOUGHT", "CANCELLED",
  "SUSPENDED", "PAWNED", "BLOCKED", "PAWNED_BLOCKED", "RETAINED", "CHARGED",
] as const;

export function registrarPagamentos(server: McpServer): void {
  // ------------------------------------------------------------ pagamentos (v1)
  server.registerTool(
    "rede_pagamentos",
    {
      title: "Pagamentos — visao CIP",
      description:
        "Lista os pagamentos (depositos) do periodo com valor liquido, banco, agencia, conta, bandeira, " +
        "status e tipo (credito, debito, antecipacao). A data usada e a do PAGAMENTO, nao a da venda. " +
        "Janela maxima de 30 dias.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        bandeiras: pBandeiras,
        status: z.enum(["PENDING", "PAID", "REJECTED"]).optional().describe("Status do pagamento nesta rota."),
        tipo: z.enum(["CREDIT", "DEBIT", "ANTICIPATION"]).optional().describe("Tipo de movimento."),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.pagamentos, "A consulta de pagamentos");
      const chamada = {
        caminho: "/merchant-statement/v1/payments",
        pv: pv.numero,
        params: {
          parentCompanyNumber: pv.numero,
          subsidiaries: pv.numero,
          startDate: j.inicio,
          endDate: j.fim,
          brands: bandeiras(a.bandeiras),
          status: a.status,
          types: a.tipo,
          size: a.tamanho,
          pageKey: a.page_key,
        } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const pagamentos = juntar(r.paginas, "payments");
      return { pv: pv.nome, periodo: j, total_de_pagamentos: pagamentos.length, ...resumoPaginacao(r), pagamentos };
    })
  );

  // ------------------------------------------------------------ pagamentos diarios (v2)
  server.registerTool(
    "rede_pagamentos_diario",
    {
      title: "Pagamentos — visao diaria (v2)",
      description:
        "Pagamentos do periodo agrupados por dia, com os totais separados por situacao (pagos, pendentes, " +
        "suspensos, rejeitados) e a lista de pagamentos de cada dia, incluindo cobrancas e dados de negociacao " +
        "de recebiveis. E a visao mais rica de pagamentos e nao tem limite de janela documentado.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        status: z.array(z.enum(STATUS_PGTO)).optional().describe("Um ou mais status."),
        tipo: z.enum(["CRE", "DEB", "ANT"]).optional().describe("Nesta rota o tipo vai abreviado: CRE, DEB ou ANT."),
        bandeiras: pBandeiras,
        contas_bancarias: z.array(z.string()).optional().describe("Codigos de domicilio bancario."),
        payment_ids: z.array(z.string()).optional().describe("Filtra por ids de pagamento especificos."),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.pagamentos_diario, "A visao diaria de pagamentos");
      const chamada = {
        caminho: "/merchant-statement/v2/payments/daily",
        pv: pv.numero,
        params: {
          parentCompanyNumber: pv.numero,
          startDate: j.inicio,
          endDate: j.fim,
          status: a.status?.length ? a.status.join(",") : undefined,
          types: a.tipo,
          brands: bandeiras(a.bandeiras),
          bankAccounts: a.contas_bancarias?.length ? a.contas_bancarias.join(",") : undefined,
          paymentIds: a.payment_ids?.length ? a.payment_ids.join(",") : undefined,
          size: a.tamanho,
          pageKey: a.page_key,
        } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const dias = juntar(r.paginas, "paymentsDaily");
      return { pv: pv.nome, periodo: j, total_de_dias: dias.length, ...resumoPaginacao(r), dias };
    })
  );

  // ------------------------------------------------------------ resumo de pagamentos (v2)
  server.registerTool(
    "rede_pagamentos_resumo",
    {
      title: "Pagamentos — visao sumarizada (v2)",
      description:
        "Totais consolidados de pagamento no periodo: liquido, esperado, cobrado e quantidade. O corpo da " +
        "resposta MUDA conforme agrupar_por (day, week, month, brand, status, type, bank, agency, accountNumber) " +
        "— sempre minusculo nesta rota. Sem limite de janela documentado. O PV vai no header Merchant-Id.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        agrupar_por: z
          .string()
          .optional()
          .describe("day, week, month, brand, status, type, bank, agency ou accountNumber (minusculo)."),
        status: z.enum(["CHARGED", "PAID", "PENDING", "REJECTED", "SUSPENDED"]).optional(),
        tipo: z.enum(["CREDIT", "DEBIT", "ANTICIPATION"]).optional(),
        bandeira: z.union([z.string(), z.number()]).optional().describe("Uma bandeira (codigo ou nome)."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.pagamentos_resumo, "O resumo de pagamentos");
      return {
        pv: pv.nome,
        periodo: j,
        agrupado_por: a.agrupar_por ?? "nenhum (totais do periodo)",
        resposta: await api(cfg, {
          caminho: "/merchant-statement/v2/payments/summary",
          merchantIdHeader: pv.numero,
          pv: pv.numero,
          params: {
            startDate: j.inicio,
            endDate: j.fim,
            groupBy: a.agrupar_por ? validarGroupBy("pagamentos_resumo", a.agrupar_por) : undefined,
            status: a.status,
            type: a.tipo,
            brand: a.bandeira ? bandeiras([a.bandeira]) : undefined,
          } as Params,
        }),
      };
    })
  );

  // ------------------------------------------------------------ um pagamento
  server.registerTool(
    "rede_pagamento",
    {
      title: "Um pagamento pelo id",
      description:
        "Detalhe de um pagamento especifico: valor liquido, datas de pagamento e envio, status, domicilio " +
        "bancario e dados do estabelecimento.",
      inputSchema: { pv: pPv, payment_id: z.string().describe("Codigo identificador do pagamento.") },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      return {
        pv: pv.nome,
        payment_id: a.payment_id,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v1/payments/${pv.numero}/${encodeURIComponent(a.payment_id)}`,
          pv: pv.numero,
        }),
      };
    })
  );

  server.registerTool(
    "rede_pagamento_esperado",
    {
      title: "Valor esperado de um pagamento",
      description: "Valor que a Rede espera pagar para um paymentId — util para comparar o previsto com o pago.",
      inputSchema: { pv: pPv, payment_id: z.string().describe("Codigo identificador do pagamento.") },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      return {
        pv: pv.nome,
        payment_id: a.payment_id,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v1/payments/expected/${pv.numero}/${encodeURIComponent(a.payment_id)}`,
          pv: pv.numero,
        }),
      };
    })
  );

  // ------------------------------------------------------------ ordens de credito
  server.registerTool(
    "rede_ordens_de_credito",
    {
      title: "Ordens de credito",
      description:
        "Ordens de credito do periodo, liquidas de MDR. E A UNICA rota de pagamento que traz o " +
        "saleSummaryNumber junto com o paymentId — ou seja, e a ponte entre uma venda e o deposito " +
        "que a pagou. Janela maxima de 30 dias.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.ordens_de_credito, "A consulta de ordens de credito");
      const chamada = {
        caminho: "/merchant-statement/v1/payments/credit-orders",
        pv: pv.numero,
        params: {
          parentCompanyNumber: pv.numero,
          subsidiaries: pv.numero,
          startDate: j.inicio,
          endDate: j.fim,
          size: a.tamanho,
          pageKey: a.page_key,
        } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const ordens = juntar(r.paginas, "paymentsCreditOrders");
      return { pv: pv.nome, periodo: j, total_de_ordens: ordens.length, ...resumoPaginacao(r), ordens };
    })
  );

  // ------------------------------------------------------------ debitos e cashbacks de um pagamento
  server.registerTool(
    "rede_debitos_do_pagamento",
    {
      title: "Debitos descontados de um pagamento",
      description:
        "O que foi descontado de um pagamento especifico, por tipo de ajuste: valor do debito, valor " +
        "efetivamente compensado e o que ficou para compensar depois. Explica a diferenca entre o " +
        "esperado e o pago. O PV vai no header Merchant-Id.",
      inputSchema: {
        pv: pPv,
        payment_id: z.string().describe("Codigo identificador do pagamento."),
        tipos_de_ajuste: z.array(z.union([z.string(), z.number()])).optional().describe("Codigos de ajuste (ver rede_tipos_de_ajuste)."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      return {
        pv: pv.nome,
        payment_id: a.payment_id,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v1/payments/charges/${encodeURIComponent(a.payment_id)}`,
          merchantIdHeader: pv.numero,
          pv: pv.numero,
          params: { adjustmentTypes: a.tipos_de_ajuste?.length ? a.tipos_de_ajuste.join(",") : undefined } as Params,
        }),
      };
    })
  );

  server.registerTool(
    "rede_cashbacks_do_pagamento",
    {
      title: "Cashbacks de um pagamento",
      description: "Cashbacks referentes a um pagamento, por tipo de ajuste. O PV vai no header Merchant-Id.",
      inputSchema: { pv: pPv, payment_id: z.string().describe("Codigo identificador do pagamento.") },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      return {
        pv: pv.nome,
        payment_id: a.payment_id,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v1/payments/cashbacks/${encodeURIComponent(a.payment_id)}`,
          merchantIdHeader: pv.numero,
          pv: pv.numero,
        }),
      };
    })
  );

  // ------------------------------------------------------------ bloqueios
  server.registerTool(
    "rede_bloqueios_resumo",
    {
      title: "Bloqueios de pagamento — visao sumarizada",
      description:
        "Bloqueios de pagamento no periodo (SUSPENDED, PAWNED, RETAINED), com valor bloqueado e o evento " +
        "(BLOCK ou RELEASE). A data considerada e a do pagamento. Agrupar por dia resume; sem agrupamento " +
        "vem o detalhe com rvNumber e paymentId.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        agrupar_por_dia: z.boolean().optional().describe("true = groupBy=day (unico agrupamento aceito aqui)."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.bloqueios, "A consulta de bloqueios");
      return {
        pv: pv.nome,
        periodo: j,
        resposta: await api(cfg, {
          caminho: "/merchant-statement/v1/blocks/summary",
          pv: pv.numero,
          params: {
            parentCompanyNumber: pv.numero,
            startDate: j.inicio,
            endDate: j.fim,
            groupBy: a.agrupar_por_dia ? validarGroupBy("bloqueios_resumo", "day") : undefined,
          } as Params,
        }),
      };
    })
  );

  server.registerTool(
    "rede_bloqueios_do_pagamento",
    {
      title: "Bloqueios de um pagamento",
      description:
        "Bloqueios e desbloqueios de um paymentId, com o tipo e o valor de cada um. Use quando um " +
        "pagamento apareceu como SUSPENDED, PAWNED ou RETAINED e voce precisa saber o motivo e se ja foi liberado.",
      inputSchema: { pv: pPv, payment_id: z.string().describe("Codigo identificador do pagamento.") },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      return {
        pv: pv.nome,
        payment_id: a.payment_id,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v1/blocks/${pv.numero}/${encodeURIComponent(a.payment_id)}`,
          pv: pv.numero,
        }),
      };
    })
  );
}
