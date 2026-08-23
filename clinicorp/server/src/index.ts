/**
 * Servidor MCP do Clinicorp.
 *
 * Leitura sempre disponivel. Escrita (agendar, confirmar, cancelar, cadastrar paciente,
 * lead no CRM, anexo, ordem de compra) fica DESLIGADA por padrao — ligue com
 * { "escrita": true, "clinicas": [...] } no arquivo de credenciais, ou CLINICORP_ESCRITA=X.
 * Ver src/tools-escrita.ts.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { loadClinics, resolveClinic, type Clinic } from "./config.js";
import {
  apiGet,
  agregado,
  listarPeriodo,
  listaCacheada,
  subscriberDe,
  toArray,
  validarPeriodo,
  BASE_URL,
  MAX_DAYS_PER_REQUEST,
} from "./client.js";
import type { ClinicorpEstimate, ClinicorpPayment } from "./types.js";
import { registrarEscrita } from "./tools-escrita.js";
import { registrarExtras } from "./tools-extra.js";
import { escritaLiberada } from "./escrita.js";

let clinicas: Clinic[] = [];
let erroConfig: string | null = null;

try {
  clinicas = loadClinics();
} catch (e) {
  erroConfig = (e as Error).message;
}

function pegarClinica(nome?: string): Clinic {
  if (erroConfig) throw new Error(erroConfig);
  return resolveClinic(clinicas, nome);
}

type Conteudo = { content: Array<{ type: "text"; text: string }> };

function texto(valor: unknown): Conteudo {
  return {
    content: [
      { type: "text" as const, text: typeof valor === "string" ? valor : JSON.stringify(valor, null, 2) },
    ],
  };
}

function erro(e: unknown) {
  return { isError: true, content: [{ type: "text" as const, text: `Erro: ${(e as Error).message}` }] };
}

const brl = (n: number) =>
  (Number(n) || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const num = (v: unknown) => Number(v) || 0;
const flagX = (v: unknown) => String(v ?? "").toUpperCase() === "X";
/** Flags booleanas da API sao a string "X" — true/1/yes sao ignorados sem erro. */
const X = (ligado?: boolean) => (ligado ? "X" : undefined);

const server = new McpServer(
  { name: "clinicorp", version: "0.1.0" },
  {
    instructions:
      "Acesso a API do Clinicorp (gestao de clinicas odontologicas). Leitura sempre disponivel; " +
      "as tools marcadas ESCRITA alteram dados reais e so funcionam se a escrita estiver ligada. " +
      "Antes de qualquer escrita, confirme com a pessoa o que sera alterado. " +
      "Datas sempre YYYY-MM-DD. Use clinicorp_clinicas para descobrir os nomes aceitos em 'clinica' " +
      "e clinicorp_unidades para descobrir os ids de unidade. Para uma visao geral de um mes, " +
      "clinicorp_painel resolve em uma chamada. Endpoints sem tool dedicada: clinicorp_get.",
  }
);

const pClinica = z
  .string()
  .optional()
  .describe("Nome da clinica configurada (ou subscriber_id). Opcional se houver so uma configurada.");
const pFrom = z.string().describe("Data inicial YYYY-MM-DD (inclusive)");
const pTo = z.string().describe("Data final YYYY-MM-DD (inclusive)");
const pUnidade = z
  .number()
  .int()
  .optional()
  .describe("id da unidade/clinica fisica (ver clinicorp_unidades). Omitido = todas do assinante.");
const pLimite = z.number().int().positive().max(500).default(100).describe("Maximo de registros");
const pFormato = z
  .enum(["resumo", "detalhado"])
  .default("resumo")
  .describe("resumo = campos principais; detalhado = payload cru da API");

function recorte<T>(itens: T[], limite: number) {
  return {
    total_encontrado: itens.length,
    exibindo: Math.min(itens.length, limite),
    truncado:
      itens.length > limite
        ? `mostrando ${limite} de ${itens.length} — aumente "limite" ou reduza o periodo`
        : null,
    lista: itens.slice(0, limite),
  };
}

// ============================================================== DESCOBERTA

server.registerTool(
  "clinicorp_clinicas",
  {
    title: "Clinicas configuradas neste servidor",
    description:
      "Lista as contas Clinicorp disponiveis (nome e subscriber_id) para usar no parametro 'clinica'. Nao expoe tokens.",
    inputSchema: {},
  },
  async () => {
    if (erroConfig) return erro(new Error(erroConfig));
    return texto({
      base_url: BASE_URL,
      janela_maxima_listagem_dias: MAX_DAYS_PER_REQUEST,
      clinicas: await Promise.all(
        clinicas.map(async (c) => ({
          nome: c.nome,
          subscriber_id: (await subscriberDe(c).catch(() => null)) ?? "(nao definido — descoberto na 1a chamada)",
          business_id_padrao: c.businessId ?? null,
        }))
      ),
    });
  }
);

server.registerTool(
  "clinicorp_unidades",
  {
    title: "Unidades (clinicas fisicas) do assinante",
    description:
      "GET /business/list — devolve o id de cada unidade. Esse id e o que vai em 'unidade_id' nas demais tools.",
    inputSchema: { clinica: pClinica },
  },
  async ({ clinica }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await apiGet(c, "business/list", { subscriber_id: await subscriberDe(c) })
      );
      return texto({
        clinica: c.nome,
        unidades: dados.map((u) => ({
          id: u.id,
          nome: u.Name,
          razao_social: u.BusinessName,
          endereco: u.Address,
          email: u.Email,
        })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_profissionais",
  {
    title: "Profissionais do assinante",
    description: "GET /professional/list_all_professionals — id, nome e CPF dos profissionais.",
    inputSchema: {
      clinica: pClinica,
      apenas_agendamento_online: z
        .boolean()
        .default(false)
        .describe("So profissionais habilitados no agendamento online"),
    },
  },
  async ({ clinica, apenas_agendamento_online }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await apiGet(c, "professional/list_all_professionals", {
          // excecao a regra do "X": aqui e boolean de verdade
          fromOnlineScheduling: apenas_agendamento_online ? "true" : undefined,
        })
      );
      return texto({ clinica: c.nome, total: dados.length, profissionais: dados });
    } catch (e) {
      return erro(e);
    }
  }
);

// =================================================================== AGENDA

server.registerTool(
  "clinicorp_agenda",
  {
    title: "Agenda do periodo",
    description:
      "GET /appointment/list — itens da agenda. Por padrao traz SO agendamentos de paciente; " +
      "para ocupacao real ative 'incluir_compromissos' (bloqueios e eventos ocupam a agenda e ficam " +
      "invisiveis sem isso). Para auditoria/sync ative tambem cancelados e excluidos. " +
      "Periodos longos sao fatiados automaticamente.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: pUnidade,
      paciente_id: z.number().int().optional().describe("Filtra um paciente (nao se aplica a eventos)"),
      incluir_compromissos: z
        .boolean()
        .default(false)
        .describe("Inclui compromissos e eventos (ASSIGN/EVENT) — obrigatorio para calcular ocupacao"),
      incluir_cancelados: z.boolean().default(false).describe("Inclui desmarcados"),
      incluir_excluidos: z.boolean().default(false).describe("Inclui excluidos"),
      formato: pFormato,
      limite: pLimite,
    },
  },
  async (a) => {
    try {
      const c = pegarClinica(a.clinica);
      const dados = await listarPeriodo<Record<string, unknown>>(c, "appointment/list", a.from, a.to, {
        businessId: a.unidade_id,
        patientId: a.paciente_id,
        includeAssigns: X(a.incluir_compromissos),
        includeCanceled: X(a.incluir_cancelados),
        includeDeleted: X(a.incluir_excluidos),
      });

      const porTipo: Record<string, number> = {};
      for (const i of dados) {
        const t = String(i.ItemType ?? "?");
        porTipo[t] = (porTipo[t] ?? 0) + 1;
      }

      const r = recorte(dados, a.limite);
      return texto({
        clinica: c.nome,
        periodo: { from: a.from, to: a.to },
        incluiu_compromissos: a.incluir_compromissos,
        por_tipo: porTipo,
        total_encontrado: r.total_encontrado,
        exibindo: r.exibindo,
        truncado: r.truncado,
        itens:
          a.formato === "detalhado"
            ? r.lista
            : r.lista.map((i) => ({
                tipo: i.ItemType,
                id: i.id,
                data: i.date ?? i.AtomicDate,
                de: i.fromTime,
                ate: i.toTime,
                dia_inteiro: flagX(i.AllDay),
                paciente: i.PatientName ?? null,
                titulo: i.Name ?? null,
                unidade_id: i.Clinic_BusinessId,
                profissional_id: i.Dentist_PersonId ?? null,
                status_id: i.StatusId ?? null,
                cancelado: flagX(i.Canceled),
                excluido: flagX(i.Deleted),
              })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_ocupacao",
  {
    title: "Ocupacao da agenda (calculo oficial do Clinicorp)",
    description:
      "GET /appointment/schedule_occupation — tempo disponivel, agendado e percentual de ocupacao, por mes. Tempos em minutos.",
    inputSchema: { clinica: pClinica, from: pFrom, to: pTo, unidade_id: pUnidade },
  },
  async ({ clinica, from, to, unidade_id }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await agregado(c, "appointment/schedule_occupation", from, to, {
          business_id: unidade_id,
          group_by: "month",
        })
      );
      return texto({
        clinica: c.nome,
        periodo: { from, to },
        meses: dados.map((m) => ({
          mes: m.month,
          tempo_disponivel_min: num(m.TotalValidScheduleTime),
          tempo_agendado_min: num(m.TotalAppointmentTime),
          tempo_eventos_min: m.TotalEvent,
          tempo_indisponivel_min: num(m.TotalBusy),
          // a API grafa "Ocupaccion"
          ocupacao_pct: m.Ocupaccion,
        })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_kpis_agenda",
  {
    title: "KPIs de agendamento",
    description:
      "GET /appointment/list_info — total agendado, primeiras consultas, faltas e quebra por categoria no periodo.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: pUnidade,
      por_mes: z.boolean().default(false).describe("Quebra o resultado por mes"),
    },
  },
  async ({ clinica, from, to, unidade_id, por_mes }) => {
    try {
      const c = pegarClinica(clinica);
      const d = (await agregado(c, "appointment/list_info", from, to, {
        business_id: unidade_id,
        group_by: por_mes ? "month" : undefined,
      })) as Record<string, unknown>;

      const agendados = num(d.ScheduledTotal);
      const faltas = num(d.MissedAppointmentTotal);
      return texto({
        clinica: c.nome,
        periodo: { from, to },
        agendamentos: agendados,
        // a API grafa "FirsAppointmentTotal"
        primeiras_consultas: num(d.FirsAppointmentTotal),
        faltas,
        taxa_falta_pct: agendados ? Number(((faltas / agendados) * 100).toFixed(1)) : 0,
        categorias: d.Category ?? null,
      });
    } catch (e) {
      return erro(e);
    }
  }
);

// ================================================================ PACIENTES

server.registerTool(
  "clinicorp_buscar_paciente",
  {
    title: "Buscar um paciente",
    description:
      "GET /patient/get — busca por id, nome, CPF, telefone ou e-mail (pelo menos um). Retorna UM paciente. " +
      "Dado pessoal sensivel: use so quando a pergunta for realmente sobre uma pessoa especifica.",
    inputSchema: {
      clinica: pClinica,
      paciente_id: z.number().int().optional(),
      nome: z.string().optional(),
      cpf: z.string().optional().describe("CPF (campo OtherDocumentId na API)"),
      telefone: z.string().optional(),
      email: z.string().optional(),
    },
  },
  async ({ clinica, paciente_id, nome, cpf, telefone, email }) => {
    try {
      const c = pegarClinica(clinica);
      if (!paciente_id && !nome && !cpf && !telefone && !email) {
        throw new Error("Informe pelo menos um criterio: paciente_id, nome, cpf, telefone ou email.");
      }
      const d = (await apiGet(c, "patient/get", {
        subscriber_id: await subscriberDe(c),
        PatientId: paciente_id,
        Name: nome,
        OtherDocumentId: cpf,
        Phone: telefone,
        Email: email,
      })) as Record<string, unknown> | null;

      if (!d || !d.PatientId) {
        return texto({ clinica: c.nome, encontrado: false, mensagem: "Nenhum paciente com esses criterios." });
      }
      return texto({ clinica: c.nome, encontrado: true, paciente: d });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_aniversariantes",
  {
    title: "Aniversariantes do dia",
    description: "GET /patient/birthdays — pacientes que fazem aniversario na data (omitida = hoje).",
    inputSchema: {
      clinica: pClinica,
      data: z.string().optional().describe("YYYY-MM-DD. Omitido = hoje"),
      limite: pLimite,
    },
  },
  async ({ clinica, data, limite }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await apiGet(c, "patient/birthdays", { subscriber_id: await subscriberDe(c), date: data })
      );
      const r = recorte(dados, limite);
      return texto({
        clinica: c.nome,
        data: data ?? "hoje",
        total_encontrado: r.total_encontrado,
        truncado: r.truncado,
        aniversariantes: r.lista.map((p) => ({
          id: p.PatientId,
          nome: p.Name,
          idade: p.Age,
          celular: p.MobilePhone,
          email: p.Email,
        })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_agendamentos_paciente",
  {
    title: "Agendamentos de um paciente",
    description: "GET /patient/list_appointments — historico completo de agendamentos de um paciente (sem recorte de periodo).",
    inputSchema: { clinica: pClinica, paciente_id: z.number().int(), limite: pLimite },
  },
  async ({ clinica, paciente_id, limite }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await apiGet(c, "patient/list_appointments", { PatientId: paciente_id })
      );
      const r = recorte(dados, limite);
      return texto({
        clinica: c.nome,
        paciente_id,
        total_encontrado: r.total_encontrado,
        truncado: r.truncado,
        agendamentos: r.lista,
      });
    } catch (e) {
      return erro(e);
    }
  }
);

// ================================================================== VENDAS

server.registerTool(
  "clinicorp_orcamentos",
  {
    title: "Orcamentos do periodo",
    description:
      "GET /estimates/list — paciente, valor, status (APPROVED/OPEN/FOLLOW_UP/REJECTED), profissional e " +
      "procedimentos. Traz tambem o agregado por status. Periodos longos sao fatiados automaticamente.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: pUnidade,
      status: z.enum(["APPROVED", "OPEN", "FOLLOW_UP", "REJECTED"]).optional(),
      formato: pFormato,
      limite: pLimite,
    },
  },
  async (a) => {
    try {
      const c = pegarClinica(a.clinica);
      let dados = await listarPeriodo<ClinicorpEstimate>(c, "estimates/list", a.from, a.to, {
        // atencao: aqui a API chama de clinic_id, nao business_id
        clinic_id: a.unidade_id,
      });

      const porStatus: Record<string, { quantidade: number; valor: number }> = {};
      for (const o of dados) {
        const s = String(o.Status ?? "?");
        porStatus[s] ??= { quantidade: 0, valor: 0 };
        porStatus[s].quantidade += 1;
        porStatus[s].valor += num(o.Amount);
      }

      if (a.status) dados = dados.filter((o) => o.Status === a.status);
      const r = recorte(dados, a.limite);
      const valor = dados.reduce((s, o) => s + num(o.Amount), 0);

      return texto({
        clinica: c.nome,
        periodo: { from: a.from, to: a.to },
        filtro_status: a.status ?? null,
        por_status: porStatus,
        valor_filtrado: valor,
        valor_filtrado_formatado: brl(valor),
        total_encontrado: r.total_encontrado,
        exibindo: r.exibindo,
        truncado: r.truncado,
        orcamentos:
          a.formato === "detalhado"
            ? r.lista
            : r.lista.map((o) => ({
                id: o.id,
                treatment_id: o.TreatmentId,
                paciente: o.PatientName,
                valor: o.Amount,
                status: o.Status,
                data: o.CreateDate,
                profissional: o.ProfessionalName,
                procedimentos: (o.ProcedureList ?? []).map((p) => p.ProcedureName),
              })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_orcamento_detalhe",
  {
    title: "Detalhe de um orcamento",
    description: "GET /estimates/get — detalhe pelo treatment_id (campo TreatmentId de clinicorp_orcamentos).",
    inputSchema: { clinica: pClinica, treatment_id: z.number().int() },
  },
  async ({ clinica, treatment_id }) => {
    try {
      const c = pegarClinica(clinica);
      const d = await apiGet(c, "estimates/get", {
        subscriber_id: await subscriberDe(c),
        treatment_id,
      });
      return texto({ clinica: c.nome, treatment_id, orcamento: d });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_conversao",
  {
    title: "Conversao de orcamentos e ticket medio",
    description:
      "GET /sales/estimates_and_conversion — quantidade, valor, ticket medio e taxa de conversao por mes. Exige unidade_id.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: z.number().int().describe("id da unidade — obrigatorio neste endpoint"),
    },
  },
  async ({ clinica, from, to, unidade_id }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await agregado(c, "sales/estimates_and_conversion", from, to, {
          business_id: unidade_id,
          group_by: "month",
        })
      );
      return texto({ clinica: c.nome, periodo: { from, to }, unidade_id, meses: dados });
    } catch (e) {
      return erro(e);
    }
  }
);

// ============================================================== FINANCEIRO

server.registerTool(
  "clinicorp_pagamentos",
  {
    title: "Pagamentos e parcelas do periodo",
    description:
      "GET /payment/list — a fonte mais detalhada de recebimentos. ATENCAO: 'base_data' muda completamente " +
      "o resultado — 'recebimento' (padrao) para regime de caixa, 'checkoutDate' para acompanhar venda, " +
      "'postDate' para data de lancamento. Periodos longos sao fatiados automaticamente.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      base_data: z
        .enum(["recebimento", "postDate", "checkoutDate"])
        .default("recebimento")
        .describe("Qual data o periodo filtra"),
      apenas_recebidos: z.boolean().default(false).describe("So parcelas com PaymentReceived = X"),
      valor_liquido: z
        .boolean()
        .default(false)
        .describe("Traz AmountWithDiscounts (valor liquido de taxas)"),
      formato: pFormato,
      limite: pLimite,
    },
  },
  async (a) => {
    try {
      const c = pegarClinica(a.clinica);
      let dados = await listarPeriodo<ClinicorpPayment>(c, "payment/list", a.from, a.to, {
        // vazio = data de recebimento (comportamento padrao da API)
        date_type: a.base_data === "recebimento" ? undefined : a.base_data,
        include_total_amount: "X",
        get_amount_with_discounts: X(a.valor_liquido),
      });

      if (a.apenas_recebidos) dados = dados.filter((p) => flagX(p.PaymentReceived));

      const porForma: Record<string, { quantidade: number; valor: number }> = {};
      for (const p of dados) {
        const f = String(p.PaymentForm ?? "?");
        porForma[f] ??= { quantidade: 0, valor: 0 };
        porForma[f].quantidade += 1;
        porForma[f].valor += num(p.Amount);
      }

      const total = dados.reduce((s, p) => s + num(p.Amount), 0);
      const r = recorte(dados, a.limite);

      return texto({
        clinica: c.nome,
        periodo: { from: a.from, to: a.to, base_data: a.base_data },
        valor_total: total,
        valor_total_formatado: brl(total),
        por_forma_pagamento: porForma,
        total_encontrado: r.total_encontrado,
        exibindo: r.exibindo,
        truncado: r.truncado,
        pagamentos:
          a.formato === "detalhado"
            ? r.lista
            : r.lista.map((p) => ({
                id: p.id,
                treatment_id: p.TreatmentId,
                paciente: p.PatientName,
                valor: p.Amount,
                valor_liquido: p.AmountWithDiscounts ?? null,
                forma: p.PaymentForm,
                parcela: `${p.InstallmentNumber}/${p.InstallmentsCount}`,
                vencimento: p.DueDate,
                recebido: flagX(p.PaymentReceived),
                confirmado: flagX(p.PaymentConfirmed),
              })),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_fluxo_caixa",
  {
    title: "Fluxo de caixa",
    description:
      "GET /financial/list_cash_flow — entradas, saidas, previsto a receber/pagar e quebra por meio de pagamento. Exige unidade_id.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: z.number().int().describe("id da unidade — obrigatorio neste endpoint"),
    },
  },
  async ({ clinica, from, to, unidade_id }) => {
    try {
      const c = pegarClinica(clinica);
      const d = (await agregado(c, "financial/list_cash_flow", from, to, {
        business_id: unidade_id,
      })) as Record<string, unknown>;

      const entrou = num(d.in);
      const saiu = num(d.out);
      return texto({
        clinica: c.nome,
        periodo: { from, to },
        realizado: { entradas: entrou, saidas: saiu, saldo: entrou - saiu, saldo_formatado: brl(entrou - saiu) },
        previsto: { a_receber: num(d.in_forecast), a_pagar: num(d.out_forecast) },
        saldo_projetado: entrou + num(d.in_forecast) - (saiu + num(d.out_forecast)),
        por_meio: {
          dinheiro: num(d.cash),
          boleto: num(d.bank_slip),
          credito: num(d.credit_card),
          debito: num(d.debit_card),
          cheque: num(d.check),
          transferencia: num(d.transfer),
        },
        saldo_devedor: num(d.debit),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_inadimplencia",
  {
    title: "Previsto x recebido x inadimplencia",
    description: "GET /financial/list_payments — totais consolidados do periodo. Exige unidade_id.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: z.number().int().describe("id da unidade — obrigatorio neste endpoint"),
    },
  },
  async ({ clinica, from, to, unidade_id }) => {
    try {
      const c = pegarClinica(clinica);
      const d = (await agregado(c, "financial/list_payments", from, to, {
        business_id: unidade_id,
      })) as Record<string, unknown>;

      const previsto = num(d.totalInForecastAmount);
      const devedor = num(d.totalDebitAmount);
      return texto({
        clinica: c.nome,
        periodo: { from, to },
        previsto,
        recebido: num(d.totalPaymentsAmount),
        em_aberto: devedor,
        em_aberto_formatado: brl(devedor),
        inadimplencia_pct: previsto ? Number(((devedor / previsto) * 100).toFixed(1)) : 0,
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_resumo_financeiro",
  {
    title: "Resumo financeiro (vendas, receitas, despesas)",
    description:
      "GET /financial/list_summary — total de vendas, receitas, despesas e lancamentos detalhados do periodo.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: pUnidade,
      incluir_lancamentos: z.boolean().default(false).describe("Inclui a lista detalhada de lancamentos"),
      limite: pLimite,
    },
  },
  async ({ clinica, from, to, unidade_id, incluir_lancamentos, limite }) => {
    try {
      const c = pegarClinica(clinica);
      const d = (await agregado(c, "financial/list_summary", from, to, {
        business_id: unidade_id,
      })) as Record<string, unknown>;

      const receita = num(d.TotalIncome);
      const despesa = num(d.TotalExpenses);
      const lancamentos = Array.isArray(d.values) ? (d.values as unknown[]) : [];

      return texto({
        clinica: c.nome,
        periodo: { from, to },
        vendas: num(d.TotalSales),
        receitas: receita,
        despesas: despesa,
        resultado: receita - despesa,
        resultado_formatado: brl(receita - despesa),
        margem_pct: receita ? Number((((receita - despesa) / receita) * 100).toFixed(1)) : 0,
        total_lancamentos: lancamentos.length,
        lancamentos: incluir_lancamentos ? lancamentos.slice(0, limite) : null,
      });
    } catch (e) {
      return erro(e);
    }
  }
);

// =============================================================== PANORAMA

server.registerTool(
  "clinicorp_painel",
  {
    title: "Painel consolidado por unidade",
    description:
      "GET /analytics/list_results — a visao mais completa em UMA chamada: orcamentos por status, receita, " +
      "recebido, despesas, ticket medio, conversao, agendamentos, faltas e novos pacientes, por unidade. " +
      "Use isto para 'como foi o mes'. Inclui unidades inativas que tiveram movimento.",
    inputSchema: { clinica: pClinica, from: pFrom, to: pTo },
  },
  async ({ clinica, from, to }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await agregado(c, "analytics/list_results", from, to)
      );

      return texto({
        clinica: c.nome,
        periodo: { from, to },
        unidades: dados
          .map((u) => {
            const agendados = num(u.AppointmentsTotal);
            const faltas = num(u.AppointmentsMissed);
            return {
              unidade: u.UnityName,
              unidade_id: u.BusinessId,
              receita: num(u.TotalRevenueAmount),
              receita_formatada: brl(num(u.TotalRevenueAmount)),
              recebido: num(u.TotalReceivedAmount),
              despesas: num(u.TotalExpenses),
              orcamentos: {
                total_valor: num(u.EstimatesTotalAmount),
                total_qtd: num(u.EstimatesTotalQuantity),
                aprovados_valor: num(u.EstimatesApprovedAmount),
                aprovados_qtd: num(u.EstimatesApprovedQuantity),
                abertos_valor: num(u.EstimatesOpenAmount),
                follow_up_valor: num(u.EstimatesFollowUpAmount),
                rejeitados_valor: num(u.EstimatesRejectedAmount),
              },
              ticket_medio_aprovado: num(u.ApprovedTicketAverage),
              conversao: u.ConversionRate,
              agendamentos: agendados,
              // a API grafa "AppoinmentsFinished"
              finalizados: num(u.AppoinmentsFinished),
              faltas,
              taxa_falta_pct: agendados ? Number(((faltas / agendados) * 100).toFixed(1)) : 0,
              novos_pacientes: num(u.AppointmentsNewPatients),
              pacientes_recorrentes: num(u.AppointmentsExistingPatients),
            };
          })
          .sort((a, b) => b.receita - a.receita),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "clinicorp_metas",
  {
    title: "Metas de venda x realizado",
    description:
      "GET /operational/list_sales_goals — meta, realizado e projecao por mes. Exige unidade_id.",
    inputSchema: {
      clinica: pClinica,
      from: pFrom,
      to: pTo,
      unidade_id: z.number().int().describe("id da unidade — obrigatorio neste endpoint"),
    },
  },
  async ({ clinica, from, to, unidade_id }) => {
    try {
      const c = pegarClinica(clinica);
      const dados = toArray<Record<string, unknown>>(
        await agregado(c, "operational/list_sales_goals", from, to, {
          business_id: unidade_id,
          isAPI: "X", // sem isso a resposta vem no formato interno da tela
        })
      );
      return texto({
        clinica: c.nome,
        periodo: { from, to },
        meses: dados.map((m) => {
          const meta = num(m.Goal);
          const realizado = num(m.TotalRevenueAmount);
          return {
            mes: m.month,
            meta,
            realizado,
            atingimento_pct: meta ? Number(((realizado / meta) * 100).toFixed(1)) : null,
            projecao: num(m.Projection),
          };
        }),
      });
    } catch (e) {
      return erro(e);
    }
  }
);

// ============================================================ ESCAPE HATCH

server.registerTool(
  "clinicorp_get",
  {
    title: "GET cru em qualquer endpoint da API",
    description:
      "Para os endpoints de leitura sem tool dedicada (ex.: procedures/list, appointment/status_list, " +
      "payment/list_reconcile_claim, financial/list_invoices, business/list_available_times). " +
      `Base: ${BASE_URL}. O subscriber_id e injetado automaticamente. Somente GET. ` +
      "Flags booleanas da API usam a string 'X'. Campos de resposta podem vir com os typos do proprio " +
      "spec (Ocupaccion, FirsAppointmentTotal, StatusDescrition, ShedulingAccepted).",
    inputSchema: {
      clinica: pClinica,
      path: z.string().describe("Path relativo sem barra inicial. Ex.: 'procedures/list'"),
      params: z.record(z.string()).optional().describe("Query params adicionais (todos como string)"),
      limite: z.number().int().positive().max(500).default(50),
    },
  },
  async ({ clinica, path, params, limite }) => {
    try {
      const c = pegarClinica(clinica);
      if (/^https?:\/\//i.test(path)) {
        throw new Error("Informe apenas o path relativo (ex.: 'procedures/list'), nao a URL completa.");
      }
      if (/change_status/i.test(path)) {
        throw new Error(
          "Bloqueado: /appointment/change_status e um GET que ALTERA estado. Este servidor e somente leitura."
        );
      }
      const payload = await apiGet(c, path, { subscriber_id: await subscriberDe(c), ...(params ?? {}) });
      const lista = toArray<unknown>(payload);

      if (lista.length > 0) {
        const r = recorte(lista, limite);
        return texto({
          clinica: c.nome,
          endpoint: path,
          total_encontrado: r.total_encontrado,
          exibindo: r.exibindo,
          truncado: r.truncado,
          registros: r.lista,
        });
      }
      return texto({ clinica: c.nome, endpoint: path, resposta: payload });
    } catch (e) {
      return erro(e);
    }
  }
);

// ======================================================= EXTRAS E ESCRITA

registrarExtras(server, { pegarClinica, texto, erro });
registrarEscrita(server, { pegarClinica, texto, erro });

// =================================================================== START

const transport = new StdioServerTransport();
await server.connect(transport);
console.error(
  erroConfig
    ? `clinicorp-mcp SEM configuracao valida — ${erroConfig}`
    : `clinicorp-mcp pronto — ${clinicas.length} clinica(s): ${clinicas.map((c) => c.nome).join(", ")} ` +
        `| escrita: ${escritaLiberada() ? "LIGADA" : "desligada (ligue em ~/.clinicorp-mcp.json)"}`
);
