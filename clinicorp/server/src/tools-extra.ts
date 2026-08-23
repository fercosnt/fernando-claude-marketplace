/**
 * Tools de leitura complementares (somente GET).
 *
 * Ficam separadas do index apenas por organizacao — sao leitura como as demais.
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

import { apiGet, agregado, listaCacheada, toArray } from "./client.js";
import type { Deps } from "./tools-escrita.js";

const pClinica = z
  .string()
  .optional()
  .describe("Nome da clinica configurada. Opcional se houver so uma.");

const num = (v: unknown) => Number(v) || 0;
const flagX = (v: unknown) => String(v ?? "").toUpperCase() === "X";

export function registrarExtras(server: McpServer, d: Deps): void {
  const { pegarClinica, texto, erro } = d;

  server.registerTool(
    "clinicorp_parcelamento_medio",
    {
      title: "Parcelamento medio",
      description:
        "GET /financial/average_installments — total de pagamentos, total de parcelas e media de parcelas " +
        "por mes. E o numero que explica a distancia entre venda aprovada e dinheiro em caixa numa clinica " +
        "que vende parcelado. Exige unidade_id.",
      inputSchema: {
        clinica: pClinica,
        from: z.string().describe("Data inicial YYYY-MM-DD"),
        to: z.string().describe("Data final YYYY-MM-DD"),
        unidade_id: z.number().int().describe("id da unidade — obrigatorio neste endpoint"),
      },
    },
    async ({ clinica, from, to, unidade_id }) => {
      try {
        const c = pegarClinica(clinica);
        const dados = toArray<Record<string, unknown>>(
          await agregado(c, "financial/average_installments", from, to, {
            business_id: unidade_id,
            group_by: "month",
          })
        );
        return texto({
          clinica: c.nome,
          periodo: { from, to },
          meses: dados.map((m) => ({
            mes: m.month,
            pagamentos: num(m.TotalPayments),
            parcelas: num(m.TotalInstallments),
            parcelamento_medio: num(m.AverageInstallments),
          })),
        });
      } catch (e) {
        return erro(e);
      }
    }
  );

  server.registerTool(
    "clinicorp_assinantes",
    {
      title: "Assinantes e unidades da conta",
      description:
        "GET /group/list_subscribers (+ list_subscribers_clinics) — descobre o subscriber_id de uma conta " +
        "de grupo/franquia e, opcionalmente, a grade de funcionamento e a duracao do slot de cada clinica. " +
        "Use quando nao souber qual subscriber_id preencher na configuracao.",
      inputSchema: {
        clinica: pClinica,
        incluir_horarios: z
          .boolean()
          .default(false)
          .describe("Traz tambem grade de funcionamento e duracao do slot"),
      },
    },
    async ({ clinica, incluir_horarios }) => {
      try {
        const c = pegarClinica(clinica);
        const assinantes = toArray<Record<string, unknown>>(
          await listaCacheada(`assinantes:${c.nome}`, () => apiGet(c, "group/list_subscribers"))
        );

        const saida: Record<string, unknown> = {
          clinica: c.nome,
          assinantes: assinantes.map((a) => ({
            // a API grafa "SubscriberBussinessUID"
            subscriber_id: a.SubscriberBussinessUID ?? null,
            namespace: a.Namespace ?? null,
          })),
        };

        if (incluir_horarios) {
          const grade = toArray<Record<string, unknown>>(
            await listaCacheada(`grade:${c.nome}`, () =>
              apiGet(c, "group/list_subscribers_clinics")
            )
          );
          saida.clinicas = grade.map((g) => ({
            nome: g.Name,
            ativa: flagX(g.Active),
            subscriber_id: g.SubscriberBussinessUID ?? null,
            slot_minutos: num(g.SlotTime),
            endereco: g.Address,
            horarios: g.WorkingDaysHours ?? null,
          }));
        }

        return texto(saida);
      } catch (e) {
        return erro(e);
      }
    }
  );
}
