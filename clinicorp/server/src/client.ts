/**
 * Client HTTP da API Clinicorp.
 *
 * Base: https://api.clinicorp.com/rest/v1
 * Auth: HTTP Basic (usuario_api:token_api) — NUNCA Bearer, apesar do spec
 *       declarar o esquema como "bearerAuth".
 */
import type { Clinic } from "./config.js";

export const BASE_URL = process.env.CLINICORP_BASE_URL ?? "https://api.clinicorp.com/rest/v1";

const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1000;
export const TIMEOUT_MS = Number(process.env.CLINICORP_TIMEOUT_MS ?? 45000);

/** Janela de seguranca por request nos endpoints de LISTAGEM (a API nao pagina). */
export const MAX_DAYS_PER_REQUEST = Number(process.env.CLINICORP_MAX_DAYS ?? 31);

export function authHeader(c: Clinic): string {
  return `Basic ${Buffer.from(`${c.username}:${c.token}`).toString("base64")}`;
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** Remove chaves vazias — a API trata "" como valor e alguns filtros quebram. */
export function limpar(params: Record<string, string | number | undefined | null>): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "") continue;
    out[k] = String(v);
  }
  return out;
}

export async function apiGet(
  clinic: Clinic,
  path: string,
  params: Record<string, string | number | undefined | null> = {}
): Promise<unknown> {
  const clean = path.replace(/^\/+/, "");
  const qs = new URLSearchParams(limpar(params)).toString();
  const url = `${BASE_URL}/${clean}${qs ? `?${qs}` : ""}`;

  let ultimoErro = "";

  for (let tentativa = 1; tentativa <= MAX_RETRIES; tentativa++) {
    let res: Response;
    try {
      res = await fetch(url, {
        headers: { Authorization: authHeader(clinic), Accept: "application/json" },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
    } catch (e) {
      ultimoErro = `falha de rede: ${(e as Error).message}`;
      if (tentativa < MAX_RETRIES) {
        await sleep(RETRY_DELAY_MS * tentativa);
        continue;
      }
      throw new Error(`Clinicorp GET ${clean} — ${ultimoErro}`);
    }

    if (res.ok) {
      const texto = await res.text();
      const tipo = res.headers.get("content-type") ?? "";
      if (tipo.includes("text/html") || texto.trimStart().startsWith("<")) {
        throw new Error(
          `Clinicorp GET ${clean} devolveu HTML em vez de JSON — quase sempre e host/URL errado, ` +
            `NAO token invalido. BASE_URL atual: ${BASE_URL}`
        );
      }
      if (!texto.trim()) return [];
      let dados: unknown;
      try {
        dados = JSON.parse(texto);
      } catch {
        throw new Error(`Clinicorp GET ${clean}: resposta nao e JSON — ${texto.slice(0, 300)}`);
      }
      // Alguns endpoints devolvem erro DENTRO de um 200.
      if (dados && typeof dados === "object" && !Array.isArray(dados)) {
        const o = dados as Record<string, unknown>;
        if (o.Error) {
          throw new Error(
            `Clinicorp GET ${clean}: erro ${o.Error} dentro de um 200 — ${descreverMensagem(o.Message)}`
          );
        }
      }
      return dados;
    }

    const corpo = await res.text().catch(() => "");
    const mensagem = extrairMensagem(corpo) ?? res.statusText;

    if (res.status === 401 || res.status === 403) {
      throw new Error(
        `Clinicorp GET ${clean}: ${res.status} — acesso negado para a clinica "${clinic.nome}". ` +
          `Causas: usuario/token da API errados, OU conta de grupo/franquia sem subscriber_id valido.`
      );
    }
    if (res.status === 404) {
      throw new Error(`Clinicorp GET ${clean}: 404 — endpoint ou recurso inexistente. ${mensagem}`);
    }
    if (res.status === 400) {
      // 400 e erro de parametro — retry nao resolve.
      throw new Error(`Clinicorp GET ${clean}: 400 — ${mensagem}`);
    }
    if (res.status >= 500 && tentativa < MAX_RETRIES) {
      ultimoErro = `${res.status} ${res.statusText}`;
      await sleep(RETRY_DELAY_MS * tentativa);
      continue;
    }

    throw new Error(`Clinicorp GET ${clean}: ${res.status} — ${mensagem}`);
  }

  throw new Error(`Clinicorp GET ${clean}: esgotou as tentativas — ultimo erro: ${ultimoErro}`);
}

/** `Message` pode ser string OU array de erros de validacao (estilo Zod). */
export function descreverMensagem(msg: unknown): string {
  if (Array.isArray(msg)) {
    return msg
      .map((e) => {
        const err = e as { path?: unknown[]; message?: string };
        const campo = Array.isArray(err.path) ? err.path.join(".") : "?";
        return `${campo}: ${err.message ?? "invalido"}`;
      })
      .join("; ");
  }
  return typeof msg === "string" ? msg : JSON.stringify(msg ?? "");
}

export function extrairMensagem(corpo: string): string | null {
  try {
    const o = JSON.parse(corpo) as { Message?: unknown };
    return o.Message !== undefined ? descreverMensagem(o.Message) : null;
  } catch {
    return corpo ? corpo.slice(0, 300) : null;
  }
}

/**
 * Resolve o subscriber_id da clinica. Se nao veio na configuracao, descobre via
 * /group/list_subscribers (que nao exige subscriber_id) e cacheia pela sessao.
 */
const cacheSubscriber = new Map<string, string | undefined>();

export async function subscriberDe(clinic: Clinic): Promise<string | undefined> {
  if (clinic.subscriberId) return clinic.subscriberId;
  if (cacheSubscriber.has(clinic.nome)) return cacheSubscriber.get(clinic.nome);

  // 1) Conta de grupo/franquia: os assinantes vem listados aqui.
  //    Em conta unica esse endpoint responde vazio — por isso o passo 2.
  let achados: Array<Record<string, unknown>> = [];
  try {
    achados = toArray<Record<string, unknown>>(await apiGet(clinic, "group/list_subscribers"));
  } catch {
    achados = [];
  }

  const ids = achados
    .map((a) => a.SubscriberBussinessUID ?? a.Namespace)
    .filter((v): v is string => typeof v === "string" && v.length > 0);

  if (ids.length > 1) {
    throw new Error(
      `A conta "${clinic.nome}" e de grupo/franquia e tem ${ids.length} assinantes: ${ids.join(", ")}. ` +
        `Escolha um e preencha "subscriber_id" no arquivo de credenciais.`
    );
  }

  if (ids.length === 1) {
    cacheSubscriber.set(clinic.nome, ids[0]);
    return ids[0];
  }

  // 2) Em conta unica, o id do assinante e o proprio Usuario API.
  //    (Confirmado contra a API: /business/list responde com subscriber_id = username.)
  cacheSubscriber.set(clinic.nome, clinic.username);
  return clinic.username;
}

/** Cache de listas estaveis (unidades, status) — evita repetir a chamada a cada pergunta. */
const cacheLista = new Map<string, unknown>();

export async function listaCacheada<T>(chave: string, buscar: () => Promise<T>): Promise<T> {
  if (cacheLista.has(chave)) return cacheLista.get(chave) as T;
  const valor = await buscar();
  cacheLista.set(chave, valor);
  return valor;
}

/** A API ora devolve array puro, ora { data: [...] }. */
export function toArray<T>(payload: unknown): T[] {
  if (Array.isArray(payload)) return payload as T[];
  if (payload && typeof payload === "object") {
    const obj = payload as Record<string, unknown>;
    for (const chave of ["data", "items", "results", "list"]) {
      if (Array.isArray(obj[chave])) return obj[chave] as T[];
    }
    // /procedures/list devolve um objeto agrupado por tabela de preco:
    // { "Tabela A": [...], "Tabela B": [...] } — achata mantendo a ordem.
    const valores = Object.values(obj);
    if (valores.length > 0 && valores.every((v) => Array.isArray(v))) {
      return (valores as unknown[][]).flat() as T[];
    }
  }
  return [];
}

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

export function validarData(rotulo: string, valor: string): void {
  if (!DATE_RE.test(valor)) {
    throw new Error(`${rotulo} deve estar no formato YYYY-MM-DD (recebido: "${valor}")`);
  }
  if (Number.isNaN(new Date(`${valor}T00:00:00Z`).getTime())) {
    throw new Error(`${rotulo} nao e uma data valida: "${valor}"`);
  }
}

export function validarPeriodo(from: string, to: string): void {
  validarData("from", from);
  validarData("to", to);
  if (new Date(`${from}T00:00:00Z`) > new Date(`${to}T00:00:00Z`)) {
    throw new Error(`Periodo invalido: "from" (${from}) e posterior a "to" (${to})`);
  }
}

/** Quebra o periodo em janelas — SO para endpoints de listagem. */
export function janelas(
  from: string,
  to: string,
  maxDias = MAX_DAYS_PER_REQUEST
): Array<{ from: string; to: string }> {
  validarPeriodo(from, to);

  const inicio = new Date(`${from}T00:00:00Z`);
  const fim = new Date(`${to}T00:00:00Z`);
  const out: Array<{ from: string; to: string }> = [];
  const DIA = 86_400_000;
  let cursor = inicio;

  while (cursor <= fim) {
    const candidato = new Date(cursor.getTime() + (maxDias - 1) * DIA);
    const janelaFim = candidato > fim ? fim : candidato;
    out.push({ from: iso(cursor), to: iso(janelaFim) });
    cursor = new Date(janelaFim.getTime() + DIA);
  }
  return out;
}

function iso(d: Date): string {
  return d.toISOString().slice(0, 10);
}

/**
 * LISTAGEM: percorre o periodo em janelas e concatena.
 * Use apenas onde a resposta e uma lista de registros — nunca em endpoint agregado,
 * senao o total sai quebrado em pedacos e a leitura fica errada.
 */
export async function listarPeriodo<T>(
  clinic: Clinic,
  path: string,
  from: string,
  to: string,
  extra: Record<string, string | number | undefined | null> = {}
): Promise<T[]> {
  const todos: T[] = [];
  for (const j of janelas(from, to)) {
    const payload = await apiGet(clinic, path, {
      subscriber_id: await subscriberDe(clinic),
      from: j.from,
      to: j.to,
      ...extra,
    });
    todos.push(...toArray<T>(payload));
  }
  return todos;
}

/** AGREGADO: uma unica chamada, periodo intacto. */
export async function agregado(
  clinic: Clinic,
  path: string,
  from: string,
  to: string,
  extra: Record<string, string | number | undefined | null> = {}
): Promise<unknown> {
  validarPeriodo(from, to);
  return apiGet(clinic, path, {
    subscriber_id: await subscriberDe(clinic),
    from,
    to,
    ...extra,
  });
}
