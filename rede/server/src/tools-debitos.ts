/**
 * Gestao de Debitos — ajustes a debito previstos para o estabelecimento (aluguel de maquininha,
 * cancelamentos, chargebacks, pacotes). Sao eles que explicam a diferenca entre o valor bruto
 * das vendas e o que efetivamente cai na conta.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { apenasConfig, contexto, seguro } from "./ctx.js";
import { api, apiPaginado, juntar, type Params } from "./client.js";
import { validarJanela, LIMITE } from "./periodo.js";
import { pFim, pInicio, pPageKey, pPv, pTamanho, pTudo, resumoPaginacao } from "./comum.js";

export function registrarDebitos(server: McpServer): void {
  server.registerTool(
    "rede_debitos",
    {
      title: "Debitos — visao detalhada",
      description:
        "Cada ajuste a debito do periodo: tipo do ajuste, valor, valor ja compensado, valor a compensar, " +
        "data de pagamento e de compensacao, resumo de vendas e ordem de credito relacionados, e o tipo de " +
        "cobranca (NET desconta do repasse, NET_EXTERNO debita da conta). Janela maxima de 30 dias.",
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
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.debitos, "A consulta de debitos");
      const chamada = {
        caminho: "/merchant-statement/v1/charges",
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
      const debitos = juntar(r.paginas, "charges");
      return { pv: pv.nome, periodo: j, total_de_debitos: debitos.length, ...resumoPaginacao(r), debitos };
    })
  );

  server.registerTool(
    "rede_debitos_resumo",
    {
      title: "Debitos — visao sumarizada",
      description:
        "Debitos do periodo somados por tipo de ajuste, com valor previsto e valor efetivamente compensado. " +
        "Use para responder 'o que a Rede me cobrou neste mes e por que'. Janela maxima de 30 dias.",
      inputSchema: { pv: pPv, data_inicio: pInicio, data_fim: pFim },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const j = validarJanela(a.data_inicio, a.data_fim, LIMITE.debitos_resumo, "O resumo de debitos");
      return {
        pv: pv.nome,
        periodo: j,
        resposta: await api(cfg, {
          caminho: "/merchant-statement/v1/charges/summary",
          pv: pv.numero,
          params: {
            parentCompanyNumber: pv.numero,
            subsidiaries: pv.numero,
            startDate: j.inicio,
            endDate: j.fim,
          } as Params,
        }),
      };
    })
  );

  server.registerTool(
    "rede_tipos_de_ajuste",
    {
      title: "Tabela de tipos de ajuste de debito",
      description:
        "Lista codigo e descricao de todos os tipos de ajuste a debito da Rede. E a tabela que da nome ao " +
        "adjustmentTypeCode que aparece em rede_debitos e rede_debitos_do_pagamento. Nao precisa de PV nem periodo.",
      inputSchema: {},
    },
    seguro(async () => {
      const cfg = apenasConfig();
      return { resposta: await api(cfg, { caminho: "/merchant-statement/v1/charges/adjustment-types" }) };
    })
  );
}
