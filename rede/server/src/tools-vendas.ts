/**
 * Gestao de Vendas — valor BRUTO das transacoes (sem desconto de MDR).
 *
 * Venda e pagamento sao coisas diferentes na Rede: uma venda vira parcelas, e varias parcelas
 * de vendas diferentes sao pagas juntas em um pagamento. O campo que costura os dois mundos e
 * o saleSummaryNumber (numero do resumo de vendas). Ver tools-conciliacao.ts.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { contexto, seguro } from "./ctx.js";
import { api, apiPaginado, juntar, rotaNaoHabilitada, type Params } from "./client.js";
import { validarJanela, validarData, LIMITE } from "./periodo.js";
import { validarGroupBy } from "./dominios.js";
import { bandeiras, modalidade, pBandeiras, pFim, pInicio, pPageKey, pPv, pTamanho, pTudo, resumoPaginacao } from "./comum.js";

export function registrarVendas(server: McpServer): void {
  // ------------------------------------------------------------ vendas detalhadas
  server.registerTool(
    "rede_vendas",
    {
      title: "Vendas — visao detalhada",
      description:
        "Lista transacao a transacao (valor bruto) do PV no periodo, com bandeira, modalidade, NSU, " +
        "resumo de vendas, taxa MDR, valor liquido e o rastreamento do ciclo de vida da venda. " +
        "Janela maxima de 62 dias. Use a v2 (padrao) para filtrar por status_tipo e produto; a v1 " +
        "so existe para comparar com integracoes antigas.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        bandeiras: pBandeiras,
        modalidade: z.string().optional().describe("CREDIT, DEBIT ou VAN (aceita 'credito'/'debito')."),
        status: z.enum(["APPROVED", "CANCELLED"]).optional().describe("Status da venda."),
        status_tipo: z
          .string()
          .optional()
          .describe("So na v2: COMPLETE, PARTIAL, CHARGEBACK, CANCELLATION, REVERSED, DENIED, UNDONE, IN_DISPUTE, IN_DISPUTE_PARTIAL, PENDING_PAYMENT, PAYMENT_REFUND."),
        produto: z
          .string()
          .optional()
          .describe("So na v2: modalityProduct, ex. IN_INSTALLMENTS_NO_INTEREST, NO_INSTALLMENTS_DEBIT."),
        versao: z.union([z.literal(1), z.literal(2)]).optional().describe("Versao da rota (padrao 2)."),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.vendas, "A consulta de vendas");
      const v2 = (a.versao ?? 2) === 2;

      const params: Params = {
        // subsidiaries e obrigatorio e, nesta versao da API, tem de ser igual ao PV principal.
        parentCompanyNumber: pv.numero,
        subsidiaries: pv.numero,
        startDate: j.inicio,
        endDate: j.fim,
        brands: bandeiras(a.bandeiras),
        modalities: modalidade(a.modalidade),
        status: a.status,
        size: a.tamanho,
        pageKey: a.page_key,
      };
      if (v2) {
        params.statusType = a.status_tipo;
        params.modalityProducts = a.produto;
      } else if (a.status_tipo || a.produto) {
        throw new Error("status_tipo e produto so existem na v2. Remova o filtro ou use versao=2.");
      }

      const monta = (usarV2: boolean) => {
        const p: Params = { ...params };
        // A v1 chama o PV por outro nome e nao conhece os filtros exclusivos da v2.
        // O swagger manda a v2 usar parentMerchantId, mas producao recusa (422) sem
        // parentCompanyNumber — confirmado em 2026-09-21. A v2 leva os dois nomes.
        p.parentCompanyNumber = pv.numero;
        if (usarV2) p.parentMerchantId = pv.numero;
        else delete p.parentMerchantId;
        if (!usarV2) {
          delete p.statusType;
          delete p.modalityProducts;
        }
        return { caminho: `/merchant-statement/v${usarV2 ? 2 : 1}/sales`, params: p, pv: pv.numero };
      };

      /**
       * A v2 nao esta habilitada em todo aplicativo (no sandbox ela responde 403 "Requisicao
       * invalida" mesmo com credencial correta). Quando a versao nao foi pedida a mao e nenhum
       * filtro exclusivo da v2 esta em uso, caimos na v1 em vez de devolver erro — e avisamos.
       */
      const podeCair = (a.versao ?? 0) !== 2 && !a.status_tipo && !a.produto;
      let usarV2 = v2;
      let aviso: string | undefined;

      const executar = async (u: boolean) =>
        a.paginar_tudo ? await apiPaginado(cfg, monta(u)) : await api(cfg, monta(u));

      let saida: unknown;
      try {
        saida = await executar(usarV2);
      } catch (e) {
        if (!(usarV2 && podeCair && rotaNaoHabilitada(e))) throw e;
        usarV2 = false;
        aviso = "A v2 de vendas nao esta habilitada para este aplicativo (403). Refiz a consulta na v1, que devolve os mesmos campos menos statusType e modalityProduct.";
        saida = await executar(false);
      }

      const versao = usarV2 ? 2 : 1;
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, versao, ...(aviso ? { aviso } : {}), resposta: saida };
      const r = saida as Awaited<ReturnType<typeof apiPaginado>>;
      const vendas = juntar(r.paginas, "transactions");
      return { pv: pv.nome, periodo: j, versao, ...(aviso ? { aviso } : {}), total_de_vendas: vendas.length, ...resumoPaginacao(r), vendas };
    })
  );

  // ------------------------------------------------------------ resumo de vendas
  server.registerTool(
    "rede_vendas_resumo",
    {
      title: "Vendas — visao sumarizada",
      description:
        "Totais de venda do periodo — valor bruto, credito, debito, liquido, quantidade e desconto — ja " +
        "somados em total_do_periodo. A Rede devolve um item por dia com venda (ou por semana/mes, com " +
        "agrupar_por); o total do periodo e total_do_periodo, nunca o primeiro item da lista. " +
        "Informe agrupar_por (DAY, WEEK ou MONTH) ou terminais para cair na v1, que e a unica que agrupa; " +
        "sem isso usa a v2, que aceita filtro por status_tipo e produto. Janela maxima de 62 dias.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        agrupar_por: z.string().optional().describe("DAY, WEEK ou MONTH (maiusculo). Forca a v1."),
        bandeiras: pBandeiras,
        modalidades: z.array(z.string()).optional().describe("Lista: CREDIT, DEBIT, VAN."),
        status: z.array(z.enum(["APPROVED", "CANCELLED"])).optional(),
        status_tipo: z.string().optional().describe("So na v2."),
        produto: z.string().optional().describe("So na v2."),
        terminais: z.array(z.string()).optional().describe("Codigos de terminal (ex.: PV650319). Forca a v1."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.vendas_resumo, "O resumo de vendas");
      const usaV1 = !!a.agrupar_por || !!a.terminais?.length;
      if (!usaV1 && (a.status_tipo || a.produto)) {
        // fica na v2 mesmo — os filtros so existem la
      }
      if (usaV1 && (a.status_tipo || a.produto)) {
        throw new Error("status_tipo e produto so existem na v2, que nao agrupa. Escolha: agrupar_por OU esses filtros.");
      }

      const params: Params = {
        startDate: j.inicio,
        endDate: j.fim,
        brands: bandeiras(a.bandeiras),
        modalities: a.modalidades?.length ? a.modalidades.map((m: string) => modalidade(m)).join(",") : undefined,
        status: a.status?.length ? a.status.join(",") : undefined,
      };
      if (usaV1) {
        if (a.agrupar_por) params.groupBy = validarGroupBy("vendas_resumo_v1", a.agrupar_por);
        if (a.terminais?.length) params.terminals = a.terminais.join(",");
      } else {
        params.statusType = a.status_tipo;
        params.modalityProducts = a.produto;
      }

      const caminho = `/merchant-statement/v${usaV1 ? 1 : 2}/sales/${pv.numero}/summary`;
      const resposta = await api(cfg, { caminho, params, pv: pv.numero });

      // A Rede devolve UM ITEM POR PERIODO (por dia, sem groupBy), so para os dias com venda.
      // Ler sales[0] como se fosse o total e o erro natural — aconteceu no primeiro teste em
      // producao. Por isso o total vem somado aqui, na frente da lista.
      const itens = ((resposta as { content?: { sales?: Record<string, unknown>[] } })?.content?.sales ?? []);
      const soma = (k: string) => Math.round(itens.reduce((t, x) => t + (Number(x[k]) || 0), 0) * 100) / 100;
      const total = itens.length
        ? {
            valor_bruto: soma("amount"),
            credito: soma("amountCredit"),
            debito: soma("amountDebit"),
            valor_liquido: soma("netAmount"),
            desconto: soma("discountAmount"),
            quantidade_de_vendas: soma("quantity"),
          }
        : null;

      return {
        pv: pv.nome,
        periodo: j,
        versao: usaV1 ? 1 : 2,
        total_do_periodo: total,
        como_ler:
          `A lista em resposta.content.sales tem ${itens.length} item(ns), um por ` +
          `${a.agrupar_por ? String(a.agrupar_por).toLowerCase() : "dia com venda"}. ` +
          `Use total_do_periodo para o total; nunca o primeiro item.`,
        resposta,
      };
    })
  );

  // ------------------------------------------------------------ venda por NSU
  server.registerTool(
    "rede_vendas_por_nsu",
    {
      title: "Vendas por NSU (visao diaria)",
      description:
        "Vendas do periodo agrupadas por dia, com a lista de transacoes de cada dia. Informando o NSU, " +
        "devolve so as vendas daquele NSU — e o caminho para achar UMA venda especifica. Tambem filtra por " +
        "terminal (device) e por TID de e-commerce. Janela maxima de 62 dias. " +
        "Atencao: no sandbox esta rota roda em uma base diferente das demais; se der 404, preencha base_nsu no ~/.rede-mcp.json.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        nsu: z.union([z.string(), z.number()]).optional().describe("Numero sequencial unico da transacao."),
        terminal: z.string().optional().describe("Codigo do terminal (device), ex.: PV650319."),
        tid: z.string().optional().describe("Transaction ID de transacoes e-commerce."),
        bandeiras: pBandeiras,
        modalidade: z.string().optional(),
        status: z.enum(["APPROVED", "CANCELLED"]).optional(),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.vendas_por_nsu, "A consulta de vendas por NSU");
      const chamada = {
        caminho: `/merchant-statement/v1/sales/${pv.numero}/daily`,
        base: cfg.baseNsu,
        pv: pv.numero,
        params: {
          startDate: j.inicio,
          endDate: j.fim,
          nsu: a.nsu,
          device: a.terminal,
          tid: a.tid,
          brands: bandeiras(a.bandeiras),
          modalities: modalidade(a.modalidade),
          status: a.status,
          size: a.tamanho,
          pageKey: a.page_key,
        } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const dias = juntar(r.paginas, "salesDaily");
      return { pv: pv.nome, periodo: j, total_de_dias: dias.length, ...resumoPaginacao(r), dias };
    })
  );

  // ------------------------------------------------------------ parcelas de uma venda
  server.registerTool(
    "rede_parcelas_da_venda",
    {
      title: "Parcelas de uma venda (por data + NSU)",
      description:
        "Detalha as parcelas de UMA venda: valor, MDR, flex, vencimento, status da parcela " +
        "(SCHEDULLED, PAID, ANTICIPATED, UNBOOK, BLOCKED) e o paymentId em que cada parcela sera paga. " +
        "Debito e credito a vista voltam com uma parcela so. Exige data da venda e NSU — pegue os dois em rede_vendas.",
      inputSchema: {
        pv: pPv,
        data_venda: z.string().describe("Data da venda — YYYY-MM-DD"),
        nsu: z.union([z.string(), z.number()]).describe("NSU da venda"),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const saleDate = validarData(a.data_venda, "data_venda");
      return {
        pv: pv.nome,
        data_venda: saleDate,
        nsu: a.nsu,
        resposta: await api(cfg, {
          caminho: `/merchant-statement/v2/payments/installments/${pv.numero}`,
          params: { saleDate, nsu: a.nsu },
          pv: pv.numero,
        }),
      };
    })
  );

  // ------------------------------------------------------------ vendas parceladas do periodo
  server.registerTool(
    "rede_vendas_parceladas",
    {
      title: "Vendas parceladas — visao detalhada (periodo)",
      description:
        "Parcelas a receber/recebidas de todas as vendas do periodo, uma linha por parcela, com numero " +
        "e quantidade de parcelas, vencimento, MDR e valor liquido. Janela maxima de 30 dias (data da venda).",
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
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.vendas_parceladas, "A consulta de vendas parceladas");
      const chamada = {
        caminho: "/merchant-statement/v1/sales/installments",
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
      const parcelas = juntar(r.paginas, "installments");
      return { pv: pv.nome, periodo: j, total_de_parcelas: parcelas.length, ...resumoPaginacao(r), parcelas };
    })
  );

  // ------------------------------------------------------------ parcelas de um pagamento
  server.registerTool(
    "rede_parcelas_do_pagamento",
    {
      title: "Parcelas que compoem um pagamento",
      description:
        "Abre um pagamento e mostra QUAIS vendas entraram nele: NSU, resumo de venda (rvNumber), hash da venda, " +
        "modalidade, produto e valores originais x atuais de cada parcela. E o caminho mais direto para " +
        "conciliar um deposito com as vendas que o originaram.",
      inputSchema: {
        pv: pPv,
        payment_id: z.string().describe("Codigo identificador do pagamento (paymentId)."),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const chamada = {
        caminho: `/merchant-statement/v2/payments/installments/${pv.numero}/${encodeURIComponent(a.payment_id)}`,
        pv: pv.numero,
        params: { size: a.tamanho, pageKey: a.page_key } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, payment_id: a.payment_id, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const parcelas = juntar(r.paginas, "installments");
      return { pv: pv.nome, payment_id: a.payment_id, total_de_parcelas: parcelas.length, ...resumoPaginacao(r), parcelas };
    })
  );

  // ------------------------------------------------------------ parcelas com gravame (v3)
  server.registerTool(
    "rede_parcelas_gravame",
    {
      title: "Parcelas com informacao de gravame (v3)",
      description:
        "Versao 3 das parcelas de um pagamento, com os campos de negociacao de recebiveis: tipo de gravame, " +
        "ordem de credito pai e origem, percentual e cessionario. Use quando os recebiveis do PV estao dados " +
        "em garantia. Exige o PV centralizador e o hash do pagamento (paymentIdHash).",
      inputSchema: {
        pv_centralizador: z.string().describe("Numero do PV centralizador dos recebimentos."),
        payment_id_hash: z.string().describe("Hash de ids de pagamento (paymentIdHash)."),
        tamanho: pTamanho,
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv_centralizador);
      const chamada = {
        caminho:
          `/merchant-statement/v3/payments/installments/central-merchant-id/${pv.numero}` +
          `/payment-id-hash/${encodeURIComponent(a.payment_id_hash)}`,
        pv: pv.numero,
        params: { size: a.tamanho, pageKey: a.page_key } as Params,
      };
      if (!a.paginar_tudo) return { pv_centralizador: pv.numero, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const parcelas = juntar(r.paginas, "installments");
      return { pv_centralizador: pv.numero, total_de_parcelas: parcelas.length, ...resumoPaginacao(r), parcelas };
    })
  );
}
