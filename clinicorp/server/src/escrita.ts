/**
 * Primitivas de ESCRITA na API Clinicorp.
 *
 * Regra que vale para tudo neste arquivo: **nenhum retry automatico**.
 * Nenhum POST da API e idempotente — repetir por conta propria cria paciente
 * duplicado, agendamento duplicado ou lead duplicado. Em caso de falha de rede,
 * o certo e conferir no Clinicorp antes de tentar de novo.
 */
import type { Clinic } from "./config.js";
import { escritaLiberadaNaConfig } from "./config.js";
import {
  BASE_URL,
  TIMEOUT_MS,
  authHeader,
  limpar,
  descreverMensagem,
  extrairMensagem,
} from "./client.js";

/**
 * Escrita fica DESLIGADA por padrao. Duas formas de ligar:
 *  - no arquivo de credenciais: { "escrita": true, "clinicas": [ ... ] }
 *  - por ambiente: CLINICORP_ESCRITA=X
 */
export function escritaLiberada(): boolean {
  return (
    String(process.env.CLINICORP_ESCRITA ?? "").toUpperCase() === "X" ||
    escritaLiberadaNaConfig()
  );
}

export function exigirEscrita(operacao: string): void {
  if (!escritaLiberada()) {
    throw new Error(
      `"${operacao}" altera dados reais no Clinicorp e a escrita esta DESLIGADA neste servidor. ` +
        `Para ligar, troque o arquivo ~/.clinicorp-mcp.json para a forma ` +
        `{ "escrita": true, "clinicas": [ ...as clinicas de hoje... ] } e reinicie o cliente. ` +
        `Enquanto isso, so leitura e permitida.`
    );
  }
}

/** POST na API. Sucesso e 200 OU 201 (products/orders responde 201). */
export async function apiPost(clinic: Clinic, path: string, body: unknown): Promise<unknown> {
  const clean = path.replace(/^\/+/, "");

  let res: Response;
  try {
    res = await fetch(`${BASE_URL}/${clean}`, {
      method: "POST",
      headers: {
        Authorization: authHeader(clinic),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
  } catch (e) {
    throw new Error(
      `Clinicorp POST ${clean} — falha de rede: ${(e as Error).message}. ` +
        `NAO repita a chamada sem antes conferir no Clinicorp se o registro foi criado: ` +
        `a requisicao pode ter chegado antes de a conexao cair.`
    );
  }

  const corpo = await res.text().catch(() => "");
  let dados: unknown = null;
  if (corpo.trim()) {
    try {
      dados = JSON.parse(corpo);
    } catch {
      dados = corpo;
    }
  }

  if (!res.ok) {
    throw new Error(
      `Clinicorp POST ${clean}: ${res.status} — ${extrairMensagem(corpo) ?? res.statusText}`
    );
  }

  // /crm/add_leads devolve Error DENTRO de um 200 — status HTTP nao basta.
  if (dados && typeof dados === "object" && !Array.isArray(dados)) {
    const o = dados as Record<string, unknown>;
    if (o.Error) {
      throw new Error(
        `Clinicorp POST ${clean}: a API recusou dentro de um 200 — ${descreverMensagem(o.Message)}`
      );
    }
  }

  return dados;
}

/**
 * GET que ALTERA estado — so /appointment/change_status.
 * Sem retry e nunca em prefetch/cache, pelo mesmo motivo dos POSTs.
 */
export async function apiGetEscrita(
  clinic: Clinic,
  path: string,
  params: Record<string, string | number | undefined | null>
): Promise<unknown> {
  const clean = path.replace(/^\/+/, "");
  const qs = new URLSearchParams(limpar(params)).toString();

  const res = await fetch(`${BASE_URL}/${clean}?${qs}`, {
    headers: { Authorization: authHeader(clinic), Accept: "application/json" },
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });

  const corpo = await res.text().catch(() => "");
  if (!res.ok) {
    throw new Error(`Clinicorp ${clean}: ${res.status} — ${extrairMensagem(corpo) ?? res.statusText}`);
  }
  try {
    return corpo.trim() ? JSON.parse(corpo) : [];
  } catch {
    return corpo;
  }
}
