/**
 * Tools de ESCRITA — alteram dados reais no Clinicorp.
 *
 * Todas exigem a escrita ligada — no arquivo de credenciais ({ "escrita": true, ... })
 * ou por CLINICORP_ESCRITA=X. Sem isso o servidor e somente leitura.
 * Nenhuma faz retry: os POSTs da API nao sao idempotentes.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

import type { Clinic } from "./config.js";
import { apiGet, subscriberDe, toArray } from "./client.js";
import { apiPost, apiGetEscrita, exigirEscrita } from "./escrita.js";

type Conteudo = { content: Array<{ type: "text"; text: string }> };

export interface Deps {
  pegarClinica: (nome?: string) => Clinic;
  texto: (valor: unknown) => Conteudo;
  erro: (e: unknown) => { isError: boolean; content: Array<{ type: "text"; text: string }> };
}

const pClinica = z
  .string()
  .optional()
  .describe("Nome da clinica configurada. Opcional se houver so uma.");

export function registrarEscrita(server: McpServer, d: Deps): void {
  const { pegarClinica, texto, erro } = d;

  // ------------------------------------------------ apoio (leitura, mas so serve pra escrita)

  server.registerTool(
    "clinicorp_status_agendamento",
    {
      title: "Status de agendamento disponiveis",
      description:
        "GET /appointment/status_list — lista os status e seus ids. Necessario antes de " +
        "clinicorp_alterar_status. Case sempre pelo campo 'tipo' (CONFIRMED, MISSED...), nunca pela " +
        "descricao, que a clinica edita livremente.",
      inputSchema: { clinica: pClinica },
    },
    async ({ clinica }) => {
      try {
        const c = pegarClinica(clinica);
        const dados = toArray<Record<string, unknown>>(
          await apiGet(c, "appointment/status_list", { subscriber_id: await subscriberDe(c) })
        );
        return texto({
          clinica: c.nome,
          status: dados.map((s) => ({
            id: s.id,
            tipo: s.Type,
            descricao: s.Description,
            ativo: String(s.Active ?? "").toUpperCase() === "X",
          })),
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_campanhas",
    {
      title: "Campanhas ativas do CRM",
      description:
        "GET /crm/list_active_campaigns — nomes das campanhas. Rode antes de clinicorp_adicionar_lead: " +
        "a campanha e casada pelo NOME exato, e nome errado nao gera erro claro.",
      inputSchema: { clinica: pClinica },
    },
    async ({ clinica }) => {
      try {
        const c = pegarClinica(clinica);
        const dados = toArray<Record<string, unknown>>(
          await apiGet(c, "crm/list_active_campaigns", { subscriber_id: await subscriberDe(c) })
        );
        return texto({ clinica: c.nome, campanhas: dados });
      } catch (e) {
        return erro(e);
      }
    }
  );

  // ------------------------------------------------------------------ agendamento

  server.registerTool(
    "clinicorp_alterar_status",
    {
      title: "ESCRITA — alterar status de agendamentos",
      description:
        "Altera o status de um ou varios agendamentos (confirmado, faltou, atendido). " +
        "Pegue os ids de status em clinicorp_status_agendamento. Base da rotina de confirmacao. " +
        "ALTERA DADOS: confirme com a pessoa antes de chamar, e nunca repita a chamada automaticamente.",
      inputSchema: {
        clinica: pClinica,
        agendamento_ids: z
          .array(z.union([z.number().int(), z.string()]))
          .min(1)
          .max(200)
          .describe("Ids dos agendamentos a alterar"),
        status_id: z.union([z.number().int(), z.string()]).describe("id do status (ver clinicorp_status_agendamento)"),
      },
    },
    async ({ clinica, agendamento_ids, status_id }) => {
      try {
        exigirEscrita("clinicorp_alterar_status");
        const c = pegarClinica(clinica);
        const r = await apiGetEscrita(c, "appointment/change_status", {
          id: agendamento_ids.join(","),
          status_id,
        });
        // Verificado contra a API em 08/2026: ao alterar UM agendamento a resposta e um
        // OBJETO unico, nao o array que a doc mostra. Aceita as duas formas — senao um
        // write bem-sucedido e reportado como "0 alterados".
        const lista =
          r && typeof r === "object" && !Array.isArray(r) && "id" in (r as Record<string, unknown>)
            ? [r as Record<string, unknown>]
            : toArray<Record<string, unknown>>(r);

        return texto({
          clinica: c.nome,
          alterados: lista.length,
          resultado: lista.map((a) => ({
            id: a.id,
            paciente: a.PatientName,
            data: a.Date,
            // a doc avisa do typo "StatusDescrition", mas esta rota devolveu a grafia
            // correta — aceite as duas.
            status: a.StatusDescrition ?? a.StatusDescription,
          })),
          aviso:
            lista.length === 0
              ? "A API respondeu sem identificar o agendamento — confira por leitura se a alteracao valeu."
              : null,
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_confirmar_agendamento",
    {
      title: "ESCRITA — confirmar agendamento",
      description:
        "POST /appointment/confirm_appointment — registra a confirmacao do paciente. ALTERA DADOS.",
      inputSchema: { clinica: pClinica, agendamento_id: z.union([z.number().int(), z.string()]) },
    },
    async ({ clinica, agendamento_id }) => {
      try {
        exigirEscrita("clinicorp_confirmar_agendamento");
        const c = pegarClinica(clinica);
        const r = await apiPost(c, "appointment/confirm_appointment", {
          subscriber_id: await subscriberDe(c),
          id: agendamento_id,
        });
        const item = toArray<Record<string, unknown>>(r)[0] ?? {};
        return texto({
          clinica: c.nome,
          confirmado: String(item.PatientConfirm ?? "").toUpperCase() === "X",
          paciente: item.PatientName,
          data: item.Date,
          status: item.StatusDescription,
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_cancelar_agendamento",
    {
      title: "ESCRITA — cancelar agendamento",
      description:
        "POST /appointment/cancel_appointment — cancela o agendamento. ALTERA DADOS e nao tem desfazer " +
        "pela API. Sempre confirme paciente, data e horario com a pessoa antes de chamar.",
      inputSchema: { clinica: pClinica, agendamento_id: z.union([z.number().int(), z.string()]) },
    },
    async ({ clinica, agendamento_id }) => {
      try {
        exigirEscrita("clinicorp_cancelar_agendamento");
        const c = pegarClinica(clinica);
        const r = await apiPost(c, "appointment/cancel_appointment", {
          subscriber_id: await subscriberDe(c),
          id: agendamento_id,
        });
        const item = toArray<Record<string, unknown>>(r)[0] ?? {};
        return texto({
          clinica: c.nome,
          cancelado: String(item.Deleted ?? "").toUpperCase() === "X",
          paciente: item.PatientName,
          bruto: item,
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_criar_agendamento",
    {
      title: "ESCRITA — criar agendamento na agenda",
      description:
        "POST /appointment/create_appointment_by_api — cria o agendamento DIRETO na agenda, ja valendo, " +
        "sem passar por aprovacao. Para automacao (bot, formulario), prefira " +
        "clinicorp_solicitar_agendamento, que entra na fila de aprovacao da clinica. " +
        "Confira horario livre antes (clinicorp_agenda). ALTERA DADOS.",
      inputSchema: {
        clinica: pClinica,
        paciente_id: z.number().int().describe("id do paciente ja cadastrado"),
        paciente_nome: z.string(),
        data: z.string().describe("Data do agendamento em ISO 8601 UTC. Ex.: 2026-09-12T03:00:00.000Z = 12/09 00:00 em BRT"),
        hora_inicio: z.string().describe("HH:MM"),
        hora_fim: z.string().describe("HH:MM"),
        unidade_id: z.number().int().describe("id da clinica (Clinic_BusinessId)"),
        profissional_id: z.number().int().describe("id do profissional (Dentist_PersonId)"),
        procedimentos: z.string().optional().describe("Procedimentos separados por virgula"),
        celular: z.string().optional(),
        email: z.string().optional(),
        recurso_id: z.number().int().optional().describe("id da cadeira, se agendar por cadeira"),
        recurso_tipo: z.string().optional().describe('Tipo do recurso. Ex.: "CHAIR"'),
        categoria: z.string().optional().describe("Descricao da categoria"),
        categoria_cor: z.string().optional().describe("Cor da categoria em hex"),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_criar_agendamento");
        const c = pegarClinica(a.clinica);
        if (!/^\d{4}-\d{2}-\d{2}T/.test(a.data)) {
          throw new Error(
            `"data" precisa ser ISO 8601 com hora e fuso (ex.: 2026-09-12T03:00:00.000Z). Recebido: "${a.data}"`
          );
        }
        const r = await apiPost(c, "appointment/create_appointment_by_api", {
          Patient_PersonId: a.paciente_id,
          PatientName: a.paciente_nome,
          MobilePhone: a.celular,
          Email: a.email,
          fromTime: a.hora_inicio,
          toTime: a.hora_fim,
          date: a.data,
          Clinic_BusinessId: a.unidade_id,
          Dentist_PersonId: a.profissional_id,
          ScheduleToId: a.recurso_id,
          ScheduleToType: a.recurso_tipo,
          Procedures: a.procedimentos,
          CategoryColor: a.categoria_cor,
          CategoryDescription: a.categoria,
        });
        const item = toArray<Record<string, unknown>>(r)[0] ?? {};
        return texto({ clinica: c.nome, status: item.Status ?? "?", agendamento_id: item.id ?? null });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_solicitar_agendamento",
    {
      title: "ESCRITA — criar solicitacao de agendamento (fila de aprovacao)",
      description:
        "POST /appointment/create_online_scheduling — entra como PEDIDO para a clinica aprovar, nao como " +
        "agendamento confirmado. E a opcao segura para bot, site e formulario. " +
        "Precisa do code_link (codigo do link publico de agendamento).",
      inputSchema: {
        clinica: pClinica,
        code_link: z.number().int().describe("Codigo do link publico de agendamento"),
        paciente_nome: z.string(),
        motivo: z.string().describe("Razao da consulta"),
        celular: z.string(),
        data: z.string().describe("Data desejada em ISO 8601 UTC"),
        hora_inicio: z.string().describe("HH:MM"),
        hora_fim: z.string().describe("HH:MM"),
        unidade_id: z.number().int(),
        profissional_id: z.number().int(),
        email: z.string().optional(),
        cpf_3_primeiros: z
          .string()
          .max(3)
          .optional()
          .describe("APENAS os 3 primeiros digitos do CPF — a API so aceita isso aqui"),
        observacoes: z.string().optional(),
        ja_e_paciente: z.boolean().default(false),
        origem: z.string().default("CLOUDIA").describe("Origem da solicitacao"),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_solicitar_agendamento");
        const c = pegarClinica(a.clinica);
        if (a.cpf_3_primeiros && a.cpf_3_primeiros.length > 3) {
          throw new Error("cpf_3_primeiros aceita no maximo 3 digitos — a API nao quer o CPF inteiro aqui.");
        }
        const r = await apiPost(c, "appointment/create_online_scheduling", {
          CodeLink: a.code_link,
          PatientName: a.paciente_nome,
          SchedulingReason: a.motivo,
          MobilePhone: a.celular,
          Email: a.email,
          OtherDocumentId: a.cpf_3_primeiros,
          NotesPatient: a.observacoes,
          fromTime: a.hora_inicio,
          toTime: a.hora_fim,
          IsOnlineScheduling: true,
          date: a.data,
          Type: a.origem,
          Dentist_PersonId: a.profissional_id,
          Clinic_BusinessId: a.unidade_id,
          AlreadyPatient: a.ja_e_paciente,
        });
        const item = toArray<Record<string, unknown>>(r)[0] ?? {};
        return texto({
          clinica: c.nome,
          status: item.Status ?? "?",
          solicitacao_id: item.id ?? null,
          observacao: "Entrou na fila de aprovacao da clinica — ainda nao e um agendamento confirmado.",
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  // --------------------------------------------------------------------- paciente

  server.registerTool(
    "clinicorp_criar_paciente",
    {
      title: "ESCRITA — cadastrar paciente",
      description:
        "POST /patient/create — cria paciente. Busca por CPF antes para nao duplicar: se ja existir, " +
        "devolve o existente e NAO cria. O POST nao e idempotente, entao nunca repita a chamada as cegas. " +
        "ALTERA DADOS.",
      inputSchema: {
        clinica: pClinica,
        nome: z.string(),
        cpf: z.string().optional().describe("CPF — usado para nao duplicar. Sem ele a checagem nao acontece."),
        nascimento: z.string().optional().describe("YYYY-MM-DD"),
        sexo: z.enum(["M", "F"]).optional(),
        email: z.string().optional(),
        celular: z.string().optional(),
        documento: z.string().optional().describe("RG"),
        observacoes: z.string().optional(),
        criar_mesmo_com_duplicata: z
          .boolean()
          .default(false)
          .describe("Cria mesmo havendo paciente com mesmo nome/CPF. Use so com confirmacao explicita."),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_criar_paciente");
        const c = pegarClinica(a.clinica);
        const sub = await subscriberDe(c);

        if (a.cpf && !a.criar_mesmo_com_duplicata) {
          const achado = (await apiGet(c, "patient/get", {
            subscriber_id: sub,
            OtherDocumentId: a.cpf,
          })) as Record<string, unknown> | null;

          if (achado?.PatientId) {
            return texto({
              clinica: c.nome,
              criado: false,
              motivo: "Ja existe paciente com esse CPF — nada foi criado.",
              paciente_id: achado.PatientId,
              nome: achado.Name,
            });
          }
        }

        const r = (await apiPost(c, "patient/create", {
          subscriber_id: sub,
          Name: a.nome,
          BirthDate: a.nascimento,
          Sex: a.sexo,
          Email: a.email,
          MobilePhone: a.celular,
          DocumentId: a.documento,
          OtherDocumentId: a.cpf,
          Notes: a.observacoes,
          IgnoreSameName: a.criar_mesmo_com_duplicata ? "X" : undefined,
          IgnoreSameDoc: a.criar_mesmo_com_duplicata ? "X" : undefined,
        })) as Record<string, unknown> | null;

        return texto({
          clinica: c.nome,
          criado: true,
          paciente_id: r?.PatientId ?? r?.id ?? null,
          retorno: r,
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  // -------------------------------------------------------------------------- crm

  server.registerTool(
    "clinicorp_adicionar_lead",
    {
      title: "ESCRITA — inserir lead em campanha do CRM",
      description:
        "POST /crm/add_leads — joga um lead externo (site, Meta Ads, WhatsApp) no funil do Clinicorp. " +
        "A campanha e casada pelo NOME exato: rode clinicorp_campanhas antes e use o nome de la. " +
        "A API pode recusar dentro de um 200 — o servidor ja trata isso como erro. ALTERA DADOS.",
      inputSchema: {
        clinica: pClinica,
        nome: z.string().describe("Nome do lead"),
        campanha: z.string().describe("Nome EXATO da campanha (ver clinicorp_campanhas)"),
        email: z.string().optional(),
        telefone: z.string().optional(),
        observacoes: z.string().optional(),
        validar_campanha: z
          .boolean()
          .default(true)
          .describe("Confere o nome da campanha na lista antes de enviar"),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_adicionar_lead");
        const c = pegarClinica(a.clinica);
        const sub = await subscriberDe(c);

        if (a.validar_campanha) {
          const campanhas = toArray<Record<string, unknown>>(
            await apiGet(c, "crm/list_active_campaigns", { subscriber_id: sub })
          );
          const nomes = campanhas
            .map((x) => x.Name)
            .filter((n): n is string => typeof n === "string");
          if (nomes.length > 0 && !nomes.includes(a.campanha)) {
            throw new Error(
              `Campanha "${a.campanha}" nao existe na lista de campanhas ativas. ` +
                `Disponiveis: ${nomes.join(", ")}. Nome errado faz o lead sumir sem erro claro.`
            );
          }
        }

        const r = await apiPost(c, "crm/add_leads", {
          subscriber_id: sub,
          Name: a.nome,
          Email: a.email,
          Phone: a.telefone,
          BoardName: a.campanha,
          Notes: a.observacoes,
        });
        return texto({ clinica: c.nome, inserido: true, campanha: a.campanha, retorno: r });
      } catch (e) {
        return erro(e);
      }
    }
  );

  // ---------------------------------------------------------------------- arquivos

  server.registerTool(
    "clinicorp_anexar_arquivo",
    {
      title: "ESCRITA — anexar arquivo ao paciente",
      description:
        "POST /file/upload — anexa foto, documento ou arquivo ao paciente. O upload e POR URL: o arquivo " +
        "precisa estar acessivel publicamente (ou por URL assinada) no momento da chamada. " +
        "O processamento e assincrono — informe webhook_url para saber quando terminou. ALTERA DADOS.",
      inputSchema: {
        clinica: pClinica,
        paciente_id: z.number().int(),
        paciente_nome: z.string(),
        url: z.string().describe("URL publica do arquivo a importar"),
        destino: z
          .enum(["Person.Profile", "Person.Photo", "Person.Document", "Person.File"])
          .default("Person.File")
          .describe("Onde anexar: foto de perfil, galeria, documentos ou arquivos gerais"),
        webhook_url: z.string().optional().describe("URL que recebe o callback com o resultado"),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_anexar_arquivo");
        const c = pegarClinica(a.clinica);
        const r = await apiPost(c, "file/upload", [
          {
            ResponseWebhookUrl: a.webhook_url,
            Url: a.url,
            LocalFile: a.destino,
            PatientName: a.paciente_nome,
            // NAO corrigir: o campo de envio e grafado "PatinetId" no spec.
            // Escrever "PatientId" faz o vinculo com o paciente falhar em silencio.
            PatinetId: a.paciente_id,
          },
        ]);
        const item = toArray<Record<string, unknown>>(r)[0] ?? {};
        return texto({ clinica: c.nome, status: item.Status ?? "?", destino: a.destino, retorno: item });
      } catch (e) {
        return erro(e);
      }
    }
  );

  // ---------------------------------------------------------------------- produtos

  server.registerTool(
    "clinicorp_criar_ordem_compra",
    {
      title: "ESCRITA — criar ordem de compra de produtos",
      description:
        "POST /products/orders — registra ordem de compra de insumos para uma clinica. " +
        "Erro de validacao vem como lista de campos, ja tratada pelo servidor. ALTERA DADOS.",
      inputSchema: {
        clinica: pClinica,
        unidade: z.string().describe("Identificador da clinica no campo 'clinic' da API"),
        codigo_ordem: z.string().describe("Codigo da ordem no seu sistema"),
        data_ordem: z.string().describe("YYYY-MM-DD"),
        produtos: z
          .array(
            z.object({
              codigo: z.string(),
              nome: z.string(),
              quantidade: z.number(),
              preco_unitario: z.number(),
              descricao: z.string().optional(),
              unidade_medida: z.string().optional().describe("Ex.: UN, CX, ML"),
              validade: z.string().optional().describe("YYYY-MM-DD"),
              lote: z.string().optional(),
              marca: z.string().optional(),
              fornecedor: z.string().optional(),
              local_armazenamento: z.string().optional(),
              observacoes: z.string().optional(),
            })
          )
          .min(1),
      },
    },
    async (a) => {
      try {
        exigirEscrita("clinicorp_criar_ordem_compra");
        const c = pegarClinica(a.clinica);
        const r = await apiPost(c, "products/orders", {
          clinic: a.unidade,
          orderCode: a.codigo_ordem,
          orderDate: a.data_ordem,
          products: a.produtos.map((p) => ({
            code: p.codigo,
            name: p.nome,
            description: p.descricao,
            quantity: p.quantidade,
            unitPrice: p.preco_unitario,
            unitOfMeasurement: p.unidade_medida,
            expirationDate: p.validade,
            lot: p.lote,
            brand: p.marca,
            supplier: p.fornecedor,
            storageLocation: p.local_armazenamento,
            notes: p.observacoes,
          })),
        });
        return texto({ clinica: c.nome, criado: true, itens: a.produtos.length, retorno: r });
      } catch (e) {
        return erro(e);
      }
    }
  );
}


