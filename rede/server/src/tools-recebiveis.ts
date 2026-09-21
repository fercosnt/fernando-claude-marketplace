/**
 * Gestao de Recebiveis — o que o estabelecimento TEM A RECEBER (agendado ou em transito),
 * antes de virar pagamento. Tres geracoes da mesma consulta convivem:
 *   v3 -> PV no header Merchant-Id, agrupa por dia/semana/mes/bandeira/modalidade/terminal, sem limite de janela
 *   v2 -> PV na query, agrupa por DAY/WEEK/MONTH (maiusculo)
 *   v1 -> PV na query, so types DAY|MONTH, janela de 30 dias
 * O padrao aqui e a v3; as outras ficam acessiveis por "versao" para comparar com relatorios antigos.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { contexto, seguro } from "./ctx.js";
import { api, apiPaginado, juntar, type Params } from "./client.js";
import { validarJanela, LIMITE } from "./periodo.js";
import { validarGroupBy } from "./dominios.js";
import { bandeiras, pBandeiras, pFim, pInicio, pPageKey, pPv, pTamanho, pTudo, resumoPaginacao } from "./comum.js";

export function registrarRecebiveis(server: McpServer): void {
  server.registerTool(
    "rede_recebiveis_resumo",
    {
      title: "Recebiveis — visao sumarizada",
      description:
        "Quanto o PV tem a receber no periodo, somado. Na v3 (padrao) da para agrupar por day, week, month, " +
        "brand, modality ou terminal (minusculo) e filtrar por bandeira, domicilio bancario e status " +
        "(SCHEDULED = agendado, IN_TRANSIT = enviado a CIP). A v1 tem janela de 30 dias; v2 e v3 nao tem limite.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        agrupar_por: z.string().optional().describe("v3: day, week, month, brand, modality, terminal (minusculo). v2: DAY, WEEK, MONTH."),
        bandeiras: pBandeiras,
        contas_bancarias: z.array(z.string()).optional().describe("So na v3 — hash do domicilio bancario."),
        status: z.enum(["SCHEDULED", "IN_TRANSIT"]).optional().describe("So na v3."),
        tipo: z.enum(["DAY", "MONTH"]).optional().describe("So nas v1/v2 — tipo de visao (types)."),
        versao: z.union([z.literal(1), z.literal(2), z.literal(3)]).optional().describe("Padrao 3."),
        tamanho: pTamanho,
        page_key: pPageKey,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const versao = a.versao ?? 3;
      const limite = versao === 1 ? LIMITE.recebiveis_resumo_v1 : undefined;
      const j = validarJanela(a.data_inicio, a.data_fim, limite, `O resumo de recebiveis v${versao}`);

      if (versao === 3) {
        if (a.tipo) throw new Error("O parametro 'tipo' (types) so existe nas versoes 1 e 2. Na v3 use agrupar_por.");
        return {
          pv: pv.nome,
          periodo: j,
          versao: 3,
          resposta: await api(cfg, {
            caminho: "/merchant-statement/v3/receivables/summary",
            merchantIdHeader: pv.numero,
            pv: pv.numero,
            params: {
              startDate: j.inicio,
              endDate: j.fim,
              groupBy: a.agrupar_por ? validarGroupBy("recebiveis_resumo_v3", a.agrupar_por) : undefined,
              brands: bandeiras(a.bandeiras),
              bankAccounts: a.contas_bancarias?.length ? a.contas_bancarias.join(",") : undefined,
              status: a.status,
            } as Params,
          }),
        };
      }

      if (a.status || a.contas_bancarias?.length) {
        throw new Error("status e contas_bancarias so existem na v3. Remova-os ou use versao=3.");
      }
      const params: Params = {
        parentCompanyNumber: pv.numero,
        startDate: j.inicio,
        endDate: j.fim,
        types: a.tipo,
        size: a.tamanho,
        pageKey: a.page_key,
      };
      if (versao === 1) params.subsidiaries = pv.numero;
      if (versao === 2 && a.agrupar_por) params.groupBy = validarGroupBy("recebiveis_v2", a.agrupar_por);

      return {
        pv: pv.nome,
        periodo: j,
        versao,
        resposta: await api(cfg, { caminho: `/merchant-statement/v${versao}/receivables/summary`, params, pv: pv.numero }),
      };
    })
  );

  server.registerTool(
    "rede_recebiveis_calendario",
    {
      title: "Recebiveis — visao calendario",
      description:
        "Recebiveis organizados em blocos diario e mensal ao mesmo tempo, cada um com total e quantidade. " +
        "Bom para montar um calendario de entrada de caixa. Janela maxima de 60 dias.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        tipo: z.enum(["DAY", "MONTH"]).optional().describe("Tipo de visao (types)."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.recebiveis_calendario, "A visao calendario de recebiveis");
      return {
        pv: pv.nome,
        periodo: j,
        resposta: await api(cfg, {
          caminho: "/merchant-statement/v1/receivables/calendar",
          pv: pv.numero,
          params: { parentCompanyNumber: pv.numero, startDate: j.inicio, endDate: j.fim, types: a.tipo } as Params,
        }),
      };
    })
  );

  server.registerTool(
    "rede_recebiveis_diario",
    {
      title: "Recebiveis — visao diaria",
      description:
        "Recebiveis por dia com o detalhe de cada entrada: bandeira, modalidade, domicilio bancario, " +
        "valor liquido, status e tipo de negociacao (gravame, cessao, livre). O PV vai no header Merchant-Id.",
      inputSchema: { pv: pPv, data_inicio: pInicio, data_fim: pFim },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.recebiveis_diario, "A visao diaria de recebiveis");
      return {
        pv: pv.nome,
        periodo: j,
        resposta: await api(cfg, {
          caminho: "/merchant-statement/v1/receivables/daily",
          merchantIdHeader: pv.numero,
          pv: pv.numero,
          params: { startDate: j.inicio, endDate: j.fim } as Params,
        }),
      };
    })
  );

  server.registerTool(
    "rede_recebiveis_parcelas",
    {
      title: "Recebiveis — parcelas detalhadas",
      description:
        "Uma linha por parcela a receber, com NSU, resumo de vendas, hash da venda, data da venda, data do " +
        "recebimento, MDR, flex, valor liquido e domicilio bancario. ATENCAO: a bandeira e OBRIGATORIA nesta " +
        "rota. O PV vai no header Merchant-Id.",
      inputSchema: {
        pv: pPv,
        data_inicio: pInicio,
        data_fim: pFim,
        bandeiras: z
          .array(z.union([z.string(), z.number()]))
          .describe("OBRIGATORIO nesta rota — uma ou mais bandeiras (codigo ou nome)."),
        page_key: pPageKey,
        paginar_tudo: pTudo,
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      if (!a.bandeiras?.length) {
        throw new Error("A rota de parcelas de recebiveis exige ao menos uma bandeira. Ex.: bandeiras: [1, 2] ou ['Mastercard','Visa'].");
      }
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.recebiveis_parcelas, "As parcelas de recebiveis");
      const chamada = {
        caminho: "/merchant-statement/v1/receivables/installments",
        merchantIdHeader: pv.numero,
        pv: pv.numero,
        params: { startDate: j.inicio, endDate: j.fim, brands: bandeiras(a.bandeiras), pageKey: a.page_key } as Params,
      };
      if (!a.paginar_tudo) return { pv: pv.nome, periodo: j, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      const parcelas = juntar(r.paginas, "installments");
      return { pv: pv.nome, periodo: j, total_de_parcelas: parcelas.length, ...resumoPaginacao(r), parcelas };
    })
  );
}
