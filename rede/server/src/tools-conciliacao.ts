/**
 * Conciliacao venda x pagamento, mais os utilitarios de escape.
 *
 * O problema que esta tool resolve: a Rede nao tem uma rota que responda "esta venda caiu em
 * qual deposito". A ligacao existe, mas em tres pontas:
 *
 *    venda (saleSummaryNumber)  ->  ordem de credito (saleSummaryNumber + paymentId)  ->  pagamento (paymentId)
 *
 * A rota de vendas traz o saleSummaryNumber; a de pagamentos (v1/payments) NAO traz. A unica
 * rota de pagamento que carrega os dois campos e a de ordens de credito. Por isso a conciliacao
 * passa por ela.
 *
 * Segunda armadilha: as duas pontas usam datas diferentes. Venda e datada pela venda; ordem de
 * credito, pelo pagamento. Debito cai em D+1 e credito em D+30, entao a janela de pagamento
 * precisa ser deslocada para frente — senao a conciliacao "perde" tudo que foi vendido no fim
 * do periodo. O padrao aqui estica a janela de pagamento em 40 dias alem do fim das vendas.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { apenasConfig, contexto, seguro } from "./ctx.js";
import { api, apiPaginado, juntar, rotaNaoHabilitada, type Params } from "./client.js";
import { fatiar, somarDias, validarJanela, LIMITE } from "./periodo.js";

/** Teto de resumos divergentes investigados por chamada — cada um custa ao menos uma consulta. */
const MAX_EXPLICAR = 30;

interface Ajuste {
  codigo: number;
  descricao: string;
  valor: number;
}
import { pPv } from "./comum.js";
import {
  BANDEIRAS, GROUP_BY, MODALIDADES, PRODUTOS, PRODUTO_PT, STATUS_CHARGEBACK, STATUS_PAGAMENTO,
  STATUS_PAGAMENTO_PT, STATUS_PARCELA, STATUS_RECEBIVEL, STATUS_TYPE_VENDA, STATUS_VENDA,
  TIPO_BLOQUEIO, TIPO_COBRANCA, TIPO_NEGOCIACAO, TIPO_PAGAMENTO,
} from "./dominios.js";

const num = (v: unknown) => (typeof v === "number" ? v : Number(v ?? 0) || 0);
const cent = (v: number) => Math.round(v * 100) / 100;

export function registrarConciliacao(server: McpServer): void {
  server.registerTool(
    "rede_conciliar",
    {
      title: "Conciliar vendas com pagamentos",
      description:
        "Cruza as vendas do periodo com as ordens de credito pelo numero do resumo de vendas " +
        "(saleSummaryNumber) e diz, resumo a resumo: quanto foi vendido no bruto, quanto entrou de liquido " +
        "e em qual paymentId. Separa o que ainda nao apareceu em nenhum pagamento do que apareceu sem venda " +
        "correspondente no periodo. Divergencias explicadas por debito do deposito (aluguel, estorno de outra venda) " +
        "viram 'ajuste no repasse', com o ajuste e, para estorno, a venda de origem. " +
        "Faz o fatiamento das janelas (62 dias para vendas, 30 para ordens) sozinho, " +
        "entao pode pedir alguns meses de uma vez — leva mais tempo e mais chamadas.",
      inputSchema: {
        pv: pPv,
        venda_inicio: z.string().describe("Inicio do periodo de VENDA — YYYY-MM-DD"),
        venda_fim: z.string().describe("Fim do periodo de VENDA — YYYY-MM-DD"),
        pagamento_inicio: z
          .string()
          .optional()
          .describe("Inicio do periodo de PAGAMENTO. Padrao: igual ao inicio das vendas."),
        pagamento_fim: z
          .string()
          .optional()
          .describe("Fim do periodo de PAGAMENTO. Padrao: fim das vendas + 40 dias, para alcancar o credito em D+30."),
        detalhar: z
          .boolean()
          .optional()
          .describe("true = devolve a lista completa de resumos de venda. Padrao: so os totais e uma amostra."),
        limite_amostra: z.number().int().positive().max(200).optional().describe("Tamanho da amostra (padrao 20)."),
        explicar_divergencias: z
          .boolean()
          .optional()
          .describe(
            "Padrao true. Para cada resumo divergente, consulta os debitos do deposito; se explicarem a diferenca, " +
              "reclassifica como 'ajuste no repasse'. Quando o ajuste e estorno, procura a venda estornada nos 6 meses " +
              "anteriores. Custa chamadas extras so quando ha divergencia."
          ),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const { cfg, pv } = contexto(a.pv);
      const venda = validarJanela(a.venda_inicio, a.venda_fim, undefined, "A conciliacao");
      const pagIni = a.pagamento_inicio ?? venda.inicio;
      const pagFim = a.pagamento_fim ?? somarDias(venda.fim, 40);
      const pagamento = validarJanela(pagIni, pagFim, undefined, "A janela de pagamento da conciliacao");
      const amostra = a.limite_amostra ?? 20;

      // ---------------- vendas (fatiadas em 62 dias)
      // Mesma regra de rede_vendas: tenta a v2 e cai para a v1 se ela nao estiver habilitada.
      const buscarVendas = async (f: { inicio: string; fim: string }, usarV2: boolean) =>
        apiPaginado(cfg, {
          caminho: `/merchant-statement/v${usarV2 ? 2 : 1}/sales`,
          pv: pv.numero,
          params: {
            // parentCompanyNumber vale nas duas versoes; a v2 tambem leva o nome do swagger.
            parentCompanyNumber: pv.numero,
            ...(usarV2 ? { parentMerchantId: pv.numero } : {}),
            subsidiaries: pv.numero,
            startDate: f.inicio,
            endDate: f.fim,
            size: 100,
          } as Params,
        });

      const vendas: Record<string, unknown>[] = [];
      let versaoVendas = 2;
      for (const f of fatiar(venda.inicio, venda.fim, LIMITE.vendas!)) {
        let r;
        try {
          r = await buscarVendas(f, versaoVendas === 2);
        } catch (e) {
          if (versaoVendas !== 2 || !rotaNaoHabilitada(e)) throw e;
          versaoVendas = 1;
          r = await buscarVendas(f, false);
        }
        vendas.push(...(juntar(r.paginas, "transactions") as Record<string, unknown>[]));
      }

      // ---------------- ordens de credito (fatiadas em 30 dias)
      const ordens: Record<string, unknown>[] = [];
      for (const f of fatiar(pagamento.inicio, pagamento.fim, LIMITE.ordens_de_credito!)) {
        const r = await apiPaginado(cfg, {
          caminho: "/merchant-statement/v1/payments/credit-orders",
          pv: pv.numero,
          params: {
            parentCompanyNumber: pv.numero,
            subsidiaries: pv.numero,
            startDate: f.inicio,
            endDate: f.fim,
            size: 100,
          } as Params,
        });
        ordens.push(...(juntar(r.paginas, "paymentsCreditOrders") as Record<string, unknown>[]));
      }

      // ---------------- cruzamento por saleSummaryNumber
      interface Linha {
        resumo_de_vendas: string;
        vendas: number;
        valor_bruto_vendido: number;
        valor_liquido_previsto: number;
        ordens_de_credito: number;
        valor_liquido_pago: number;
        payment_ids: string[];
        datas_de_pagamento: string[];
        /** Maior quantidade de parcelas entre as vendas do resumo (1 = a vista). */
        parcelas: number;
        parcelas_pagas?: number;
        falta_receber?: number;
        /** Debitos do deposito que explicam a diferenca. */
        ajustes?: Ajuste[];
        /** Debitos existentes que NAO fecham a conta — pista, nao explicacao. */
        ajustes_no_pagamento?: Ajuste[];
        provavel_origem?: Record<string, unknown>;
        candidatos_de_origem?: Record<string, unknown>[];
        situacao: string;
      }
      const linhas = new Map<string, Linha>();
      const nova = (k: string): Linha => ({
        resumo_de_vendas: k, vendas: 0, valor_bruto_vendido: 0, valor_liquido_previsto: 0,
        ordens_de_credito: 0, valor_liquido_pago: 0, payment_ids: [], datas_de_pagamento: [],
        parcelas: 1, situacao: "",
      });

      let vendasSemResumo = 0;
      for (const v of vendas) {
        const k = String(v.saleSummaryNumber ?? "");
        if (!k || k === "undefined") {
          vendasSemResumo++;
          continue;
        }
        const l = linhas.get(k) ?? nova(k);
        l.vendas++;
        l.valor_bruto_vendido = cent(l.valor_bruto_vendido + num(v.amount));
        l.valor_liquido_previsto = cent(l.valor_liquido_previsto + num(v.netAmount));
        l.parcelas = Math.max(l.parcelas, num(v.installmentQuantity) || 1);
        linhas.set(k, l);
      }

      for (const o of ordens) {
        const k = String(o.saleSummaryNumber ?? "");
        if (!k || k === "undefined") continue;
        const l = linhas.get(k) ?? nova(k);
        l.ordens_de_credito++;
        l.valor_liquido_pago = cent(l.valor_liquido_pago + num(o.netAmount));
        const pid = o.paymentId ? String(o.paymentId) : "";
        if (pid && !l.payment_ids.includes(pid)) l.payment_ids.push(pid);
        const d = o.paymentDate ? String(o.paymentDate) : "";
        if (d && !l.datas_de_pagamento.includes(d)) l.datas_de_pagamento.push(d);
        linhas.set(k, l);
      }

      const TOLERANCIA = 0.02; // centavos de arredondamento nao sao divergencia

      /**
       * Venda parcelada paga pela metade NAO e divergencia. Credito parcelado cai uma parcela por mes,
       * entao uma janela de pagamento de ~40 dias so enxerga a primeira. Visto no primeiro teste em
       * producao: previsto 10.270,05 e pago 2.054,01 — exatamente 1/5. Aqui o pago e comparado com
       * multiplos inteiros da parcela; a tolerancia cresce com o numero de parcelas porque cada uma
       * e arredondada separadamente pela Rede.
       */
      const parcelasPagas = (l: Linha, pago = l.valor_liquido_pago): number | null => {
        if (l.parcelas < 2 || pago <= 0) return null;
        const parcela = l.valor_liquido_previsto / l.parcelas;
        const k = Math.round(pago / parcela);
        if (k < 1 || k >= l.parcelas) return null;
        return Math.abs(pago - k * parcela) <= 0.05 * k + TOLERANCIA ? k : null;
      };

      for (const l of linhas.values()) {
        if (!l.ordens_de_credito) l.situacao = "sem pagamento na janela consultada";
        else if (!l.vendas) l.situacao = "pago, mas a venda esta fora do periodo consultado";
        else if (Math.abs(l.valor_liquido_pago - l.valor_liquido_previsto) <= TOLERANCIA) l.situacao = "conciliado";
        else {
          const k = parcelasPagas(l);
          if (k) {
            l.situacao = "parcelado em andamento";
            l.parcelas_pagas = k;
            l.falta_receber = cent(l.valor_liquido_previsto - l.valor_liquido_pago);
          } else l.situacao = "valor divergente";
        }
      }

      // ---------------- explicar divergencias pelos debitos do deposito
      /**
       * A Rede desconta ajustes (aluguel, estorno, chargeback) do proximo deposito, seja qual for a
       * venda que ele paga. Entao a diferenca de um resumo quase sempre e um debito — muitas vezes de
       * OUTRA venda. Caso real que motivou este bloco: deposito R$ 526,32 menor porque levou o estorno
       * parcial de uma venda 10x de outra data. Aqui a conta e fechada automaticamente.
       */
      const explicar = a.explicar_divergencias !== false;
      const tiposAjuste = new Map<number, string>();
      const debitosCache = new Map<string, Ajuste[]>();
      const debitosDoPagamento = async (pid: string): Promise<Ajuste[]> => {
        if (debitosCache.has(pid)) return debitosCache.get(pid)!;
        let lista: Ajuste[] = [];
        try {
          const r = (await api(cfg, {
            caminho: `/merchant-statement/v1/payments/charges/${encodeURIComponent(pid)}`,
            merchantIdHeader: pv.numero,
            pv: pv.numero,
          })) as { charges?: Record<string, unknown>[] };
          lista = (r?.charges ?? []).map((c) => {
            const codigo = num(c.adjustmentTypeCode);
            return { codigo, descricao: tiposAjuste.get(codigo) ?? `ajuste ${codigo}`, valor: cent(num(c.debitAmount)) };
          });
        } catch {
          lista = []; // sem debitos legiveis: a linha continua divergente, sem inventar explicacao
        }
        debitosCache.set(pid, lista);
        return lista;
      };

      const divergentes = [...linhas.values()].filter((l) => l.situacao === "valor divergente");
      const investigados = divergentes.slice(0, MAX_EXPLICAR);
      if (explicar && investigados.length) {
        try {
          const t = await api(cfg, { caminho: "/merchant-statement/v1/charges/adjustment-types" });
          if (Array.isArray(t)) for (const x of t as Record<string, unknown>[]) tiposAjuste.set(num(x.code), String(x.description));
        } catch {
          /* sem nomes: os ajustes saem so com o codigo */
        }
        for (const l of investigados) {
          const ajustes: Ajuste[] = [];
          for (const pid of l.payment_ids) ajustes.push(...(await debitosDoPagamento(pid)));
          if (!ajustes.length) continue;
          const diferenca = cent(l.valor_liquido_previsto - l.valor_liquido_pago);
          const total = cent(ajustes.reduce((t, x) => t + x.valor, 0));
          const fecha = (v: number) => Math.abs(v - diferenca) <= 0.05;
          const explicam = fecha(total) ? ajustes : ajustes.filter((x) => fecha(x.valor)).slice(0, 1);
          if (explicam.length) {
            l.situacao = "ajuste no repasse";
            l.ajustes = explicam;
            continue;
          }
          // Parcelado pago em parte E com desconto no mesmo deposito.
          const k = parcelasPagas(l, l.valor_liquido_pago + total);
          if (k) {
            l.situacao = "parcelado em andamento";
            l.parcelas_pagas = k;
            l.falta_receber = cent(l.valor_liquido_previsto - l.valor_liquido_pago - total);
            l.ajustes = ajustes;
            continue;
          }
          l.ajustes_no_pagamento = ajustes;
        }
      }

      // ---------------- estorno: qual venda foi estornada?
      /**
       * O debito de estorno nao diz a venda de origem. O rastreio (tracking) da venda estornada tem
       * um evento CANCELLED/PARTIAL_CANCELLED dias antes do deposito que levou o desconto. Busca nos 6
       * meses anteriores — cobre parcelado de ate 6x com folga; parcelado mais longo pode escapar.
       */
      const ehEstorno = (x: Ajuste) => x.codigo === 18 || /cancel|estorno/i.test(x.descricao);
      const comEstorno = [...linhas.values()].filter((l) => (l.ajustes ?? []).some(ehEstorno));
      if (explicar && comEstorno.length) {
        const datas = comEstorno.flatMap((l) => l.datas_de_pagamento).filter(Boolean).sort();
        const historico: Record<string, unknown>[] = [];
        for (const f of fatiar(somarDias(datas[0], -186), datas[datas.length - 1], LIMITE.vendas!)) {
          let r;
          try {
            r = await buscarVendas(f, versaoVendas === 2);
          } catch (e) {
            if (versaoVendas !== 2 || !rotaNaoHabilitada(e)) throw e;
            versaoVendas = 1;
            r = await buscarVendas(f, false);
          }
          historico.push(...(juntar(r.paginas, "transactions") as Record<string, unknown>[]));
        }
        for (const l of comEstorno) {
          const ate = [...l.datas_de_pagamento].sort().pop()!;
          const de = somarDias(ate, -7);
          const candidatos = historico.flatMap((v) => {
            const ev = ((v.tracking as Record<string, unknown>[]) ?? []).find(
              (t) => /CANCEL/i.test(String(t.status)) && String(t.date) >= de && String(t.date) <= ate
            );
            return ev
              ? [{
                  nsu: v.nsu,
                  data_da_venda: v.saleDate,
                  valor_da_venda: v.amount,
                  parcelas: v.installmentQuantity,
                  bandeira: v.bandeira,
                  evento: ev.status,
                  data_do_evento: ev.date,
                  // No caso verificado em producao (venda de 6.000 com evento de 5.400, parcelas caindo
                  // para 10%), o valor do evento era o ESTORNADO, nao o que sobrou. Nome neutro de proposito.
                  valor_do_evento: ev.amount,
                }]
              : [];
          });
          if (candidatos.length === 1) l.provavel_origem = candidatos[0];
          else if (candidatos.length > 1) l.candidatos_de_origem = candidatos.slice(0, 5);
        }
      }

      const todas = [...linhas.values()];
      const por = (s: string) => todas.filter((l) => l.situacao === s);
      const soma = (ls: Linha[], campo: keyof Linha) => cent(ls.reduce((t, l) => t + num(l[campo]), 0));

      const grupos = {
        conciliado: por("conciliado"),
        parcelado_em_andamento: por("parcelado em andamento"),
        ajuste_no_repasse: por("ajuste no repasse"),
        valor_divergente: por("valor divergente"),
        sem_pagamento: por("sem pagamento na janela consultada"),
        pago_sem_venda: por("pago, mas a venda esta fora do periodo consultado"),
      };

      return {
        pv: pv.nome,
        periodo_de_venda: venda,
        periodo_de_pagamento: {
          ...pagamento,
          observacao:
            a.pagamento_fim || a.pagamento_inicio
              ? "janela informada por voce"
              : "janela padrao: fim das vendas + 40 dias, para alcancar o credito pago em D+30",
        },
        versao_da_rota_de_vendas: versaoVendas,
        totais: {
          vendas_lidas: vendas.length,
          ordens_de_credito_lidas: ordens.length,
          resumos_de_venda: todas.length,
          valor_bruto_vendido: soma(todas, "valor_bruto_vendido"),
          valor_liquido_previsto: soma(todas, "valor_liquido_previsto"),
          valor_liquido_pago: soma(todas, "valor_liquido_pago"),
          ...(vendasSemResumo ? { vendas_sem_resumo_de_vendas: vendasSemResumo } : {}),
        },
        situacao: {
          conciliado: { resumos: grupos.conciliado.length, valor_pago: soma(grupos.conciliado, "valor_liquido_pago") },
          parcelado_em_andamento: {
            resumos: grupos.parcelado_em_andamento.length,
            pago_ate_agora: soma(grupos.parcelado_em_andamento, "valor_liquido_pago"),
            falta_receber: soma(grupos.parcelado_em_andamento, "falta_receber"),
          },
          ajuste_no_repasse: {
            resumos: grupos.ajuste_no_repasse.length,
            descontado: cent(grupos.ajuste_no_repasse.reduce((t, l) => t + (l.ajustes ?? []).reduce((u, x) => u + x.valor, 0), 0)),
          },
          valor_divergente: { resumos: grupos.valor_divergente.length, previsto: soma(grupos.valor_divergente, "valor_liquido_previsto"), pago: soma(grupos.valor_divergente, "valor_liquido_pago") },
          sem_pagamento: { resumos: grupos.sem_pagamento.length, previsto: soma(grupos.sem_pagamento, "valor_liquido_previsto") },
          pago_sem_venda: { resumos: grupos.pago_sem_venda.length, pago: soma(grupos.pago_sem_venda, "valor_liquido_pago") },
        },
        como_ler:
          "'parcelado em andamento' e normal: venda parcelada cujas parcelas seguintes vencem depois da janela " +
          "(uma por mes) — o pago e um multiplo exato da parcela, e falta_receber diz o restante. " +
          "'valor_liquido_pago' nos totais inclui parcelas de vendas ANTERIORES ao periodo (grupo 'pago sem venda'), " +
          "por isso pode ser maior que o vendido. " +
          "'sem pagamento' costuma ser venda recente que ainda nao venceu (credito cai em D+30) ou parcela bloqueada — " +
          "confira em rede_parcelas_da_venda. 'pago sem venda' quase sempre e venda anterior ao periodo: estique venda_inicio. " +
          "'ajuste no repasse' e diferenca ja explicada por um debito do deposito — o campo ajustes diz qual; se for " +
          "estorno, provavel_origem aponta a venda estornada (pode ser de outra data e outro resumo). " +
          "'valor divergente' e o que sobrou SEM explicacao nos debitos: esse sim merece olhar humano." +
          (divergentes.length > MAX_EXPLICAR
            ? ` Atencao: ${divergentes.length} divergencias, so as ${MAX_EXPLICAR} primeiras foram investigadas.`
            : ""),
        ...(a.detalhar
          ? { resumos_de_venda: todas }
          : {
              amostra: {
                valor_divergente: grupos.valor_divergente.slice(0, amostra),
                parcelado_em_andamento: grupos.parcelado_em_andamento.slice(0, amostra),
                ajuste_no_repasse: grupos.ajuste_no_repasse.slice(0, amostra),
                sem_pagamento: grupos.sem_pagamento.slice(0, amostra),
                pago_sem_venda: grupos.pago_sem_venda.slice(0, amostra),
                conciliado: grupos.conciliado.slice(0, Math.min(5, amostra)),
              },
              dica: "Passe detalhar=true para receber a lista completa de resumos de venda.",
            }),
      };
    })
  );

  // ------------------------------------------------------------ tabelas de dominio
  server.registerTool(
    "rede_dominios",
    {
      title: "Tabelas de codigos da Rede",
      description:
        "Devolve as tabelas de dominio usadas pela API: bandeiras, modalidades, produtos, status de venda, " +
        "de pagamento, de parcela e de recebivel, tipos de bloqueio, chargeback, cobranca e negociacao, e os " +
        "valores de groupBy aceitos em cada rota. Nao chama a Rede — e consulta local, instantanea.",
      inputSchema: {
        tabela: z
          .string()
          .optional()
          .describe("Nome de uma tabela especifica (ex.: bandeiras, status_pagamento, group_by). Sem isso, devolve todas."),
      },
    },
    seguro(async (a: { tabela?: string }) => {
      const tabelas: Record<string, unknown> = {
        bandeiras: BANDEIRAS,
        modalidades: MODALIDADES,
        produtos: PRODUTOS,
        produtos_descricao: PRODUTO_PT,
        status_venda: STATUS_VENDA,
        status_tipo_venda: STATUS_TYPE_VENDA,
        status_pagamento: STATUS_PAGAMENTO,
        status_pagamento_descricao: STATUS_PAGAMENTO_PT,
        tipo_pagamento: TIPO_PAGAMENTO,
        status_parcela_de_venda: STATUS_PARCELA,
        status_recebivel: STATUS_RECEBIVEL,
        tipo_bloqueio: TIPO_BLOQUEIO,
        status_chargeback: STATUS_CHARGEBACK,
        tipo_cobranca: TIPO_COBRANCA,
        tipo_negociacao: TIPO_NEGOCIACAO,
        group_by: GROUP_BY,
      };
      if (!a.tabela) {
        return {
          tabelas,
          notas: [
            "Parcela de VENDA usa SCHEDULLED (dois L); recebivel usa SCHEDULED (um L). Nao e erro de digitacao.",
            "groupBy e MAIUSCULO no resumo de vendas v1 e minusculo em pagamentos v2, recebiveis v3 e bloqueios.",
            "A bandeira 3 aparece como 'Dinners' em partes da doc da Rede e 12 como 'Mais!'; aqui sao Diners e Credsystem.",
          ],
        };
      }
      const k = a.tabela.trim().toLowerCase();
      if (!(k in tabelas)) {
        throw new Error(`Tabela "${a.tabela}" nao existe. Disponiveis: ${Object.keys(tabelas).join(", ")}.`);
      }
      return { tabela: k, valores: tabelas[k] };
    })
  );

  // ------------------------------------------------------------ escape hatch
  server.registerTool(
    "rede_get",
    {
      title: "GET livre em qualquer rota da Rede",
      description:
        "Chama qualquer endpoint da API de Gestao de Vendas que ainda nao tenha tool propria, ja com token, " +
        "retentativa e traducao de codigos. Informe o caminho a partir da barra, ex.: " +
        "/merchant-statement/v1/charges/adjustment-types. Use as tools dedicadas sempre que existirem — " +
        "elas validam janela de data e colocam o PV no lugar certo.",
      inputSchema: {
        caminho: z.string().describe("Caminho da rota, comecando com /."),
        params: z.record(z.union([z.string(), z.number(), z.boolean()])).optional().describe("Query string."),
        merchant_id_header: z
          .string()
          .optional()
          .describe("PV para o header Merchant-Id, exigido pelas rotas v2/payments/summary, v3/receivables e charges/cashbacks."),
        paginar_tudo: z.boolean().optional().describe("true = segue o cursor ate o fim (teto de 20 paginas)."),
      },
    },
    seguro(async (a: Record<string, any>) => {
      const cfg = apenasConfig();
      const chamada = {
        caminho: a.caminho,
        params: (a.params ?? {}) as Params,
        merchantIdHeader: a.merchant_id_header,
      };
      if (!a.paginar_tudo) return { caminho: a.caminho, resposta: await api(cfg, chamada) };
      const r = await apiPaginado(cfg, chamada);
      return { caminho: a.caminho, paginas_lidas: r.total_paginas, completo: r.completo, proximo_page_key: r.proximo_page_key, paginas: r.paginas };
    })
  );
}
