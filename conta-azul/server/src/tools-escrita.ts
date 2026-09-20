/**
 * Tools de ESCRITA. Duas travas:
 *  1. escrita desligada por padrao (escrita.ts) -> a tool recusa;
 *  2. cada tool trabalha em dois passos: confirmar=false (padrao) devolve a PREVIA exata do que
 *     sera enviado, sem tocar na Conta Azul; so confirmar=true envia. O modelo mostra a previa
 *     a pessoa e so repete com confirmar=true depois do ok dela.
 * Nenhuma escrita e repetida automaticamente (ver client.ts).
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { contexto, seguro } from "./ctx.js";
import { api, validarData, arred } from "./client.js";
import { exigirEscrita } from "./escrita.js";
import type { Config, Empresa } from "./config.js";

const pEmpresa = z.string().optional().describe("Nome da empresa configurada. Opcional se houver so uma.");
const pConfirmar = z
  .boolean()
  .default(false)
  .describe(
    "false (padrao) = so mostra a previa do que seria enviado, sem alterar nada. " +
      "true = envia de verdade. So use true depois que a pessoa aprovou a previa nesta conversa."
  );

const METODOS = [
  "DINHEIRO", "PIX_PAGAMENTO_INSTANTANEO", "PIX_COBRANCA", "CARTAO_CREDITO", "CARTAO_DEBITO",
  "CARTAO_CREDITO_VIA_LINK", "BOLETO_BANCARIO", "TRANSFERENCIA_BANCARIA", "DEPOSITO_BANCARIO",
  "DEBITO_AUTOMATICO", "CHEQUE", "CARTEIRA_DIGITAL", "CASHBACK", "CREDITO_LOJA", "CREDITO_VIRTUAL",
  "PROGRAMA_FIDELIDADE", "SEM_PAGAMENTO", "VALE_ALIMENTACAO", "VALE_COMBUSTIVEL", "VALE_PRESENTE",
  "VALE_REFEICAO", "OUTRO",
] as const;

function previa(operacao: string, metodo: string, caminho: string, corpo: unknown, avisos: string[] = []) {
  return {
    PREVIA_NADA_FOI_ENVIADO: true,
    operacao,
    requisicao: `${metodo} ${caminho}`,
    corpo,
    avisos,
    proximo_passo: "Mostre esta previa a pessoa. Se ela aprovar, chame a mesma tool com os mesmos argumentos e confirmar=true.",
  };
}

async function acompanharProtocolo(cfg: Config, emp: Empresa, resposta: unknown) {
  const protocolo = (resposta as { protocolo?: string })?.protocolo;
  if (!protocolo) return { resposta };
  let ultimo: unknown = resposta;
  for (let i = 0; i < 5; i++) {
    await new Promise((r) => setTimeout(r, 1500));
    try {
      ultimo = await api(cfg, emp, { caminho: `/v1/protocolo/${protocolo}` });
      const st = (ultimo as { status?: string })?.status;
      if (st && st !== "PENDING") break;
    } catch {
      break;
    }
  }
  return {
    protocolo,
    situacao: ultimo,
    obs: "Se ainda estiver PENDING, consulte depois com contaazul_protocolo — NAO recrie o lancamento.",
  };
}

const parcelaIn = z.object({
  data_vencimento: z.string().describe("YYYY-MM-DD"),
  valor: z.number().positive(),
  descricao: z.string().optional(),
  metodo_pagamento: z.enum(METODOS).optional(),
  nota: z.string().optional(),
});

export function registrarEscrita(server: McpServer) {
  // ------------------------------------------------------------ lancamento receber / pagar
  for (const lado of ["receber", "pagar"] as const) {
    server.registerTool(
      `contaazul_criar_conta_${lado}`,
      {
        title: `ESCRITA — criar conta a ${lado}`,
        description:
          `ESCRITA. Cria um lancamento de contas a ${lado} (evento financeiro) com uma ou mais parcelas. ` +
          `Se 'parcelas' for omitido, cria parcela unica com vencimento = data_vencimento. ` +
          `A soma das parcelas precisa bater com 'valor'. Ids: contato em contaazul_pessoas, conta em ` +
          `contaazul_contas_financeiras, categoria em contaazul_categorias. Processamento assincrono (devolve protocolo).`,
        inputSchema: {
          empresa: pEmpresa,
          descricao: z.string(),
          valor: z.number().positive().describe("Valor total do lancamento"),
          data_competencia: z.string().describe("YYYY-MM-DD"),
          id_contato: z.string().describe(lado === "receber" ? "UUID do cliente" : "UUID do fornecedor"),
          id_conta_financeira: z.string().describe("UUID da conta financeira"),
          id_categoria: z.string().describe("UUID da categoria (rateio 100% nela)"),
          id_centro_custo: z.string().optional().describe("UUID do centro de custo (100% nele)"),
          data_vencimento: z.string().optional().describe("Vencimento da parcela unica (YYYY-MM-DD)"),
          metodo_pagamento: z.enum(METODOS).optional(),
          parcelas: z.array(parcelaIn).optional().describe("Para parcelar; cada uma com vencimento e valor"),
          observacao: z.string().default(""),
          confirmar: pConfirmar,
        },
      },
      seguro(async (a: Record<string, unknown>) => {
        exigirEscrita(`contaazul_criar_conta_${lado}`);
        const { cfg, emp } = contexto(a.empresa as string | undefined);
        const valor = a.valor as number;
        validarData(a.data_competencia as string, "data_competencia");

        let parcelas = a.parcelas as z.infer<typeof parcelaIn>[] | undefined;
        if (!parcelas?.length) {
          if (!a.data_vencimento) throw new Error("Informe data_vencimento (parcela unica) ou a lista 'parcelas'.");
          parcelas = [{ data_vencimento: a.data_vencimento as string, valor, metodo_pagamento: a.metodo_pagamento as never }];
        }
        const soma = arred(parcelas.reduce((s, p) => s + p.valor, 0));
        if (Math.abs(soma - valor) > 0.009) {
          throw new Error(`A soma das parcelas (${soma}) nao bate com o valor total (${valor}).`);
        }
        parcelas.forEach((p, i) => validarData(p.data_vencimento, `parcelas[${i}].data_vencimento`));

        const n = parcelas.length;
        const corpo = {
          data_competencia: a.data_competencia,
          valor,
          observacao: a.observacao ?? "",
          descricao: a.descricao,
          contato: a.id_contato,
          conta_financeira: a.id_conta_financeira,
          rateio: [
            {
              id_categoria: a.id_categoria,
              valor,
              ...(a.id_centro_custo
                ? { rateio_centro_custo: [{ id_centro_custo: a.id_centro_custo, valor }] }
                : {}),
            },
          ],
          condicao_pagamento: {
            parcelas: parcelas.map((p, i) => ({
              descricao: p.descricao ?? (n > 1 ? `${a.descricao} (${i + 1}/${n})` : (a.descricao as string)),
              data_vencimento: p.data_vencimento,
              nota: p.nota ?? "",
              conta_financeira: a.id_conta_financeira,
              detalhe_valor: { valor_bruto: p.valor, valor_liquido: p.valor },
              ...(p.metodo_pagamento ?? a.metodo_pagamento
                ? { metodo_pagamento: p.metodo_pagamento ?? a.metodo_pagamento }
                : {}),
            })),
          },
        };
        const caminho = `/v1/financeiro/eventos-financeiros/contas-a-${lado}`;
        if (!a.confirmar) return previa(`Criar conta a ${lado}`, "POST", caminho, corpo);
        const r = await api(cfg, emp, { metodo: "POST", caminho, corpo });
        return acompanharProtocolo(cfg, emp, r);
      })
    );
  }

  // ------------------------------------------------------------ baixa (quitar parcela)
  server.registerTool(
    "contaazul_baixar_parcela",
    {
      title: "ESCRITA — registrar pagamento (baixa) de parcela",
      description:
        "ESCRITA. Registra o recebimento/pagamento (total ou parcial) de uma parcela. Confira antes com contaazul_parcela " +
        "se ela ja nao esta quitada — baixa duplicada distorce o caixa.",
      inputSchema: {
        empresa: pEmpresa,
        id_parcela: z.string(),
        data_pagamento: z.string().describe("YYYY-MM-DD"),
        valor: z.number().positive().describe("Valor bruto pago"),
        id_conta_financeira: z.string().describe("Conta onde o dinheiro entrou/saiu"),
        metodo_pagamento: z.enum(METODOS).optional(),
        juros: z.number().min(0).optional(),
        multa: z.number().min(0).optional(),
        desconto: z.number().min(0).optional(),
        taxa: z.number().min(0).optional().describe("Taxa de maquininha/boleto"),
        observacao: z.string().optional(),
        nsu: z.string().optional(),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      exigirEscrita("contaazul_baixar_parcela");
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      validarData(a.data_pagamento as string, "data_pagamento");
      const corpo = {
        data_pagamento: a.data_pagamento,
        composicao_valor: {
          valor_bruto: a.valor,
          ...(a.juros !== undefined ? { juros: a.juros } : {}),
          ...(a.multa !== undefined ? { multa: a.multa } : {}),
          ...(a.desconto !== undefined ? { desconto: a.desconto } : {}),
          ...(a.taxa !== undefined ? { taxa: a.taxa } : {}),
        },
        conta_financeira: a.id_conta_financeira,
        ...(a.metodo_pagamento ? { metodo_pagamento: a.metodo_pagamento } : {}),
        ...(a.observacao ? { observacao: a.observacao } : {}),
        ...(a.nsu ? { nsu: a.nsu } : {}),
      };
      const caminho = `/v1/financeiro/eventos-financeiros/parcelas/${a.id_parcela}/baixa`;
      if (!a.confirmar) {
        const atual = (await api(cfg, emp, { caminho: `/v1/financeiro/eventos-financeiros/parcelas/${a.id_parcela}` })) as Record<string, unknown>;
        const avisos = [`Parcela hoje: status ${atual?.status}, nao pago ${atual?.nao_pago}, vencimento ${atual?.data_vencimento}.`];
        if (String(atual?.status) === "QUITADO") avisos.push("ATENCAO: a parcela ja esta QUITADA.");
        return previa("Registrar baixa", "POST", caminho, corpo, avisos);
      }
      return api(cfg, emp, { metodo: "POST", caminho, corpo });
    })
  );

  // ------------------------------------------------------------ editar parcela
  server.registerTool(
    "contaazul_atualizar_parcela",
    {
      title: "ESCRITA — alterar parcela",
      description:
        "ESCRITA. Altera vencimento, valor, descricao, nota, metodo ou conta de uma parcela. A versao atual e buscada " +
        "automaticamente (a API exige). So os campos informados mudam.",
      inputSchema: {
        empresa: pEmpresa,
        id_parcela: z.string(),
        vencimento: z.string().optional().describe("YYYY-MM-DD"),
        valor: z.number().positive().optional().describe("Novo valor bruto"),
        descricao: z.string().optional(),
        nota: z.string().optional(),
        metodo_pagamento: z.enum(METODOS).optional(),
        id_conta_financeira: z.string().optional(),
        data_pagamento_esperado: z.string().optional(),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      exigirEscrita("contaazul_atualizar_parcela");
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      const caminho = `/v1/financeiro/eventos-financeiros/parcelas/${a.id_parcela}`;
      const atual = (await api(cfg, emp, { caminho })) as Record<string, unknown>;
      if (atual?.versao === undefined) throw new Error("Nao consegui ler a versao atual da parcela.");
      if (a.vencimento) validarData(a.vencimento as string, "vencimento");
      const corpo: Record<string, unknown> = { versao: atual.versao };
      for (const [de, para] of [
        ["vencimento", "vencimento"], ["descricao", "descricao"], ["nota", "nota"],
        ["metodo_pagamento", "metodo_pagamento"], ["id_conta_financeira", "id_conta_financeira"],
        ["data_pagamento_esperado", "data_pagamento_esperado"],
      ] as const) if (a[de] !== undefined) corpo[para] = a[de];
      if (a.valor !== undefined) {
        const comp = (atual.valor_composicao ?? {}) as Record<string, unknown>;
        corpo.composicao_valor = { ...comp, valor_bruto: a.valor, valor_liquido: undefined };
      }
      if (Object.keys(corpo).length === 1) throw new Error("Nenhum campo para alterar foi informado.");
      if (!a.confirmar) {
        return previa("Alterar parcela", "PATCH", caminho, corpo, [
          `Hoje: ${atual.descricao} | venc ${atual.data_vencimento} | status ${atual.status} | valor ${JSON.stringify(atual.valor_composicao)}`,
        ]);
      }
      return api(cfg, emp, { metodo: "PATCH", caminho, corpo });
    })
  );

  // ------------------------------------------------------------ pessoas
  server.registerTool(
    "contaazul_criar_pessoa",
    {
      title: "ESCRITA — cadastrar cliente/fornecedor",
      description:
        "ESCRITA. Cadastra pessoa (cliente, fornecedor ou transportadora). Antes, busque com contaazul_pessoas pelo CPF/CNPJ " +
        "para nao duplicar — a previa ja faz essa checagem.",
      inputSchema: {
        empresa: pEmpresa,
        nome: z.string(),
        tipo_pessoa: z.enum(["Física", "Jurídica", "Estrangeira"]),
        perfis: z.array(z.enum(["Cliente", "Fornecedor", "Transportadora"])).min(1).default(["Cliente"]),
        cpf: z.string().optional(),
        cnpj: z.string().optional(),
        email: z.string().optional(),
        telefone_celular: z.string().optional(),
        data_nascimento: z.string().optional().describe("YYYY-MM-DD"),
        nome_fantasia: z.string().optional(),
        observacao: z.string().optional(),
        endereco: z
          .object({
            cep: z.string().optional(), logradouro: z.string().optional(), numero: z.string().optional(),
            complemento: z.string().optional(), bairro: z.string().optional(), cidade: z.string().optional(),
            estado: z.string().optional(),
          })
          .optional(),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      exigirEscrita("contaazul_criar_pessoa");
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      const corpo: Record<string, unknown> = {
        nome: a.nome,
        tipo_pessoa: a.tipo_pessoa,
        perfis: (a.perfis as string[]).map((t) => ({ tipo_perfil: t })),
        ativo: true,
      };
      for (const k of ["cpf", "cnpj", "email", "telefone_celular", "data_nascimento", "nome_fantasia", "observacao"])
        if (a[k]) corpo[k] = a[k];
      if (a.endereco) corpo.enderecos = [{ pais: "Brasil", ...(a.endereco as object) }];
      if (!a.confirmar) {
        const doc = (a.cpf ?? a.cnpj) as string | undefined;
        const avisos: string[] = [];
        if (doc) {
          const achados = await api(cfg, emp, { caminho: "/v1/pessoas", params: { busca: doc.replace(/\D/g, ""), tipos_pessoa: a.tipo_pessoa as string } }).catch(() => null);
          const lista = (achados as { itens?: unknown[] })?.itens ?? [];
          if (lista.length) avisos.push(`ATENCAO: ja existe(m) ${lista.length} cadastro(s) com esse documento: ${JSON.stringify(lista).slice(0, 400)}`);
        } else avisos.push("Sem CPF/CNPJ nao da para checar duplicidade.");
        return previa("Cadastrar pessoa", "POST", "/v1/pessoas", corpo, avisos);
      }
      return api(cfg, emp, { metodo: "POST", caminho: "/v1/pessoas", corpo });
    })
  );

  server.registerTool(
    "contaazul_atualizar_pessoa",
    {
      title: "ESCRITA — atualizar cadastro de pessoa",
      description: "ESCRITA. Atualiza campos do cadastro (PATCH — so o que for informado muda).",
      inputSchema: {
        empresa: pEmpresa,
        id: z.string(),
        campos: z
          .record(z.unknown())
          .describe("Campos a alterar, com os nomes da API: nome, email, telefone_celular, observacao, ativo, cpf, cnpj, enderecos..."),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: { empresa?: string; id: string; campos: Record<string, unknown>; confirmar: boolean }) => {
      exigirEscrita("contaazul_atualizar_pessoa");
      const { cfg, emp } = contexto(a.empresa);
      const caminho = `/v1/pessoas/${a.id}`;
      if (!Object.keys(a.campos).length) throw new Error("Nenhum campo informado.");
      if (!a.confirmar) return previa("Atualizar pessoa", "PATCH", caminho, a.campos);
      return api(cfg, emp, { metodo: "PATCH", caminho, corpo: a.campos });
    })
  );

  // ------------------------------------------------------------ venda
  server.registerTool(
    "contaazul_criar_venda",
    {
      title: "ESCRITA — criar venda",
      description:
        "ESCRITA. Cria uma venda. itens[].id e o UUID do produto OU servico (contaazul_produtos / contaazul_servicos). " +
        "Se 'numero' for omitido, usa o proximo numero livre. condicao: 'À vista', '30, 60, 90' ou '3x'; " +
        "a soma das parcelas deve bater com o total.",
      inputSchema: {
        empresa: pEmpresa,
        id_cliente: z.string(),
        data_venda: z.string().describe("YYYY-MM-DD"),
        situacao: z.enum(["EM_ANDAMENTO", "APROVADO"]).default("EM_ANDAMENTO"),
        itens: z.array(z.object({ id: z.string(), quantidade: z.number().positive(), valor: z.number().min(0), descricao: z.string().optional() })).min(1),
        condicao: z.string().default("À vista").describe("opcao_condicao_pagamento"),
        tipo_pagamento: z.enum(METODOS).optional(),
        id_conta_financeira: z.string().optional(),
        parcelas: z.array(z.object({ data_vencimento: z.string(), valor: z.number().positive(), descricao: z.string().optional() })).optional()
          .describe("Omitido = parcela unica vencendo na data_venda"),
        id_categoria: z.string().optional(),
        id_centro_custo: z.string().optional(),
        id_vendedor: z.string().optional(),
        numero: z.number().int().optional(),
        desconto_valor: z.number().min(0).optional(),
        observacoes: z.string().optional(),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      exigirEscrita("contaazul_criar_venda");
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      validarData(a.data_venda as string, "data_venda");
      const itens = a.itens as Array<{ id: string; quantidade: number; valor: number; descricao?: string }>;
      const bruto = arred(itens.reduce((s, i) => s + i.quantidade * i.valor, 0));
      const total = arred(bruto - ((a.desconto_valor as number) ?? 0));
      const parcelas = (a.parcelas as Array<{ data_vencimento: string; valor: number; descricao?: string }>) ??
        [{ data_vencimento: a.data_venda as string, valor: total }];
      const soma = arred(parcelas.reduce((s, p) => s + p.valor, 0));
      if (Math.abs(soma - total) > 0.009) throw new Error(`Parcelas somam ${soma}, mas o total da venda e ${total}.`);

      let numero = a.numero as number | undefined;
      if (numero === undefined) {
        const r = await api(cfg, emp, { caminho: "/v1/venda/proximo-numero" });
        numero = typeof r === "number" ? r : Number((r as Record<string, unknown>)?.numero ?? (r as Record<string, unknown>)?.proximo_numero ?? r);
        if (!Number.isFinite(numero)) throw new Error(`Nao consegui obter o proximo numero de venda (${JSON.stringify(r)}). Informe 'numero'.`);
      }
      const corpo: Record<string, unknown> = {
        id_cliente: a.id_cliente,
        numero,
        situacao: a.situacao,
        data_venda: a.data_venda,
        itens: itens.map((i) => ({ id: i.id, quantidade: i.quantidade, valor: i.valor, ...(i.descricao ? { descricao: i.descricao } : {}) })),
        condicao_pagamento: {
          opcao_condicao_pagamento: a.condicao,
          ...(a.tipo_pagamento ? { tipo_pagamento: a.tipo_pagamento } : {}),
          ...(a.id_conta_financeira ? { id_conta_financeira: a.id_conta_financeira } : {}),
          parcelas,
        },
      };
      for (const k of ["id_categoria", "id_centro_custo", "id_vendedor", "observacoes"]) if (a[k]) corpo[k] = a[k];
      if (a.desconto_valor) corpo.composicao_de_valor = { desconto: { tipo: "VALOR", valor: a.desconto_valor } };
      if (!a.confirmar) return previa("Criar venda", "POST", "/v1/venda", corpo, [`Total calculado: ${total}`]);
      return api(cfg, emp, { metodo: "POST", caminho: "/v1/venda", corpo });
    })
  );

  // ------------------------------------------------------------ cobranca
  server.registerTool(
    "contaazul_gerar_cobranca",
    {
      title: "ESCRITA — gerar cobranca (boleto / Pix / link)",
      description:
        "ESCRITA. Gera cobranca Conta Azul (BOLETO, PIX_COBRANCA ou LINK_PAGAMENTO) para uma parcela a receber. " +
        "A conta precisa ser do tipo COBRANCAS_CONTA_AZUL. Pode ser enviada ao cliente pela propria Conta Azul.",
      inputSchema: {
        empresa: pEmpresa,
        id_parcela: z.string(),
        id_conta_bancaria: z.string().describe("Conta do tipo COBRANCAS_CONTA_AZUL"),
        tipo: z.enum(["BOLETO", "PIX_COBRANCA", "LINK_PAGAMENTO"]),
        data_vencimento: z.string().describe("YYYY-MM-DD"),
        descricao_fatura: z.string(),
        maximo_parcelas: z.number().int().positive().optional().describe("So para LINK_PAGAMENTO no cartao"),
        confirmar: pConfirmar,
      },
    },
    seguro(async (a: Record<string, unknown>) => {
      exigirEscrita("contaazul_gerar_cobranca");
      const { cfg, emp } = contexto(a.empresa as string | undefined);
      validarData(a.data_vencimento as string, "data_vencimento");
      const corpo = {
        conta_bancaria: a.id_conta_bancaria,
        descricao_fatura: a.descricao_fatura,
        id_parcela: a.id_parcela,
        data_vencimento: a.data_vencimento,
        tipo: a.tipo,
        ...(a.maximo_parcelas ? { maximo_parcelas: a.maximo_parcelas } : {}),
      };
      const caminho = "/v1/financeiro/eventos-financeiros/contas-a-receber/gerar-cobranca";
      if (!a.confirmar) return previa("Gerar cobranca", "POST", caminho, corpo);
      return api(cfg, emp, { metodo: "POST", caminho, corpo });
    })
  );
}
