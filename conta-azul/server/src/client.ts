/**
 * Client HTTP da API v2 da Conta Azul.
 *
 * Base: https://api-v2.contaazul.com   Auth: Bearer <access_token> (OAuth, ver auth.ts)
 * Limite oficial: 600 req/min e 10 req/s por empresa conectada -> aqui, no maximo 8 req/s.
 *
 * Leitura (GET): ate 3 tentativas em rede/429/5xx.
 * Escrita (POST/PUT/PATCH/DELETE): NUNCA repete sozinha — nada disso e idempotente na API.
 */
import type { Config, Empresa } from "./config.js";
import { accessToken } from "./auth.js";

export const BASE_URL = (process.env.CONTAAZUL_BASE_URL ?? "https://api-v2.contaazul.com").replace(/\/+$/, "");
const TIMEOUT_MS = Number(process.env.CONTAAZUL_TIMEOUT_MS ?? 45000);
const MAX_TENTATIVAS = 3;
const INTERVALO_MIN_MS = 125; // ~8 req/s

export type Params = Record<string, string | number | boolean | Array<string | number> | undefined | null>;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

let ultimaChamada = 0;
async function respeitarLimite(): Promise<void> {
  const espera = ultimaChamada + INTERVALO_MIN_MS - Date.now();
  ultimaChamada = Math.max(Date.now(), ultimaChamada + INTERVALO_MIN_MS);
  if (espera > 0) await sleep(espera);
}

/**
 * Monta a query string. Arrays viram chaves repetidas (?status=A&status=B), que e o padrao
 * OpenAPI (style=form, explode=true). Os poucos parametros com explode=false vao em `virgula`.
 */
export function montarQuery(params: Params, virgula: string[] = []): string {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "") continue;
    if (Array.isArray(v)) {
      if (!v.length) continue;
      if (virgula.includes(k)) q.append(k, v.join(","));
      else v.forEach((x) => q.append(k, String(x)));
    } else q.append(k, String(v));
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

export class ErroApi extends Error {
  constructor(message: string, public status: number, public corpo?: unknown) {
    super(message);
  }
}

function mensagemDe(corpo: unknown, textoCru: string): string {
  if (corpo && typeof corpo === "object") {
    const o = corpo as Record<string, unknown>;
    const m = o.message ?? o.error_description ?? o.error ?? o.mensagem ?? o.detail ?? o.title;
    const extras = o.errors ?? o.erros ?? o.fields ?? o.details;
    return [m ? String(m) : "", extras ? JSON.stringify(extras).slice(0, 800) : ""].filter(Boolean).join(" — ");
  }
  return textoCru.slice(0, 500);
}

function explicarStatus(status: number, metodo: string, caminho: string, msg: string): string {
  const base = `Conta Azul ${metodo} ${caminho}: ${status}`;
  switch (status) {
    case 400:
      return `${base} — requisicao recusada: ${msg}. Confira nomes de campos (a API usa id_<coisa>) e formato de data (YYYY-MM-DD).`;
    case 403:
      return `${base} — sem permissao para este recurso na empresa conectada. ${msg}`;
    case 404:
      return `${base} — nao encontrado. Se o caminho foi digitado a mao, lembre que a API mistura singular e plural (/v1/venda, /v1/pessoas). ${msg}`;
    case 429:
      return `${base} — limite de 600 req/min (10/s) estourado. Espere alguns segundos. ${msg}`;
    default:
      return `${base} — ${msg}`;
  }
}

export interface Chamada {
  metodo?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  caminho: string;
  params?: Params;
  virgula?: string[];
  corpo?: unknown;
}

export async function api(cfg: Config, empresa: Empresa, c: Chamada): Promise<unknown> {
  const metodo = c.metodo ?? "GET";
  const caminho = "/" + c.caminho.replace(/^\/+/, "");
  const url = `${BASE_URL}${caminho}${montarQuery(c.params ?? {}, c.virgula)}`;
  const leitura = metodo === "GET";

  let tokenRejeitado: string | undefined;
  let jaRenovouPor401 = false;

  for (let tentativa = 1; ; tentativa++) {
    const token = await accessToken(cfg, empresa, tokenRejeitado);
    await respeitarLimite();

    let res: Response;
    try {
      res = await fetch(url, {
        method: metodo,
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
          ...(c.corpo !== undefined ? { "Content-Type": "application/json" } : {}),
        },
        body: c.corpo !== undefined ? JSON.stringify(c.corpo) : undefined,
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
    } catch (e) {
      if (leitura && tentativa < MAX_TENTATIVAS) {
        await sleep(800 * tentativa);
        continue;
      }
      throw new Error(
        leitura
          ? `Conta Azul GET ${caminho} — falha de rede: ${(e as Error).message}`
          : `Conta Azul ${metodo} ${caminho} — falha de rede: ${(e as Error).message}. ` +
            `NAO repita sem antes conferir na Conta Azul se o registro foi criado/alterado: ` +
            `a requisicao pode ter chegado antes de a conexao cair.`
      );
    }

    // 401: token expirado/rejeitado -> renova UMA vez e repete (seguro inclusive para escrita:
    // a API recusou antes de processar).
    if (res.status === 401 && !jaRenovouPor401) {
      jaRenovouPor401 = true;
      tokenRejeitado = token;
      continue;
    }

    const texto = await res.text().catch(() => "");
    let corpo: unknown = null;
    if (texto.trim()) {
      try {
        corpo = JSON.parse(texto);
      } catch {
        corpo = texto;
      }
    }

    if (res.ok) {
      if (typeof corpo === "string" && corpo.trimStart().startsWith("<")) {
        throw new Error(`Conta Azul ${metodo} ${caminho} devolveu HTML em vez de JSON — URL/host errado.`);
      }
      return corpo ?? { ok: true, status: res.status };
    }

    const podeRepetir = leitura && (res.status === 429 || res.status >= 500) && tentativa < MAX_TENTATIVAS;
    if (podeRepetir) {
      const retryAfter = Number(res.headers.get("retry-after"));
      await sleep(retryAfter > 0 ? retryAfter * 1000 : 1000 * 2 ** (tentativa - 1));
      continue;
    }
    if (res.status === 401) {
      throw new ErroApi(
        `Conta Azul recusou o token mesmo apos renovar (401). A conexao pode ter sido revogada — rode contaazul_conectar.`,
        401,
        corpo
      );
    }
    throw new ErroApi(explicarStatus(res.status, metodo, caminho, mensagemDe(corpo, texto)), res.status, corpo);
  }
}

// ------------------------------------------------------------------ utilidades de dados

/** A API devolve data como YYYY-MM-DD em alguns lugares e DD/MM/AAAA em outros. Normaliza para ISO. */
export function dataIso(v: unknown): string | null {
  if (typeof v !== "string" || !v) return null;
  const br = v.match(/^(\d{2})\/(\d{2})\/(\d{4})/);
  if (br) return `${br[3]}-${br[2]}-${br[1]}`;
  const iso = v.match(/^(\d{4}-\d{2}-\d{2})/);
  return iso ? iso[1] : null;
}

export function validarData(v: string, campo: string): string {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v) || isNaN(Date.parse(v))) {
    throw new Error(`${campo} deve estar no formato YYYY-MM-DD (recebi "${v}").`);
  }
  return v;
}

/** Extrai a lista de itens das varias formas de envelope da API. */
export function itensDe(r: unknown): Record<string, unknown>[] {
  if (Array.isArray(r)) return r as Record<string, unknown>[];
  if (r && typeof r === "object") {
    const o = r as Record<string, unknown>;
    for (const k of ["itens", "items", "data", "content", "resultado", "lista"]) {
      if (Array.isArray(o[k])) return o[k] as Record<string, unknown>[];
    }
  }
  return [];
}

export function totalDe(r: unknown): number | null {
  if (r && typeof r === "object") {
    const o = r as Record<string, unknown>;
    for (const k of ["itens_totais", "total_itens", "totalItems", "total"]) {
      if (typeof o[k] === "number") return o[k] as number;
    }
  }
  return null;
}

/**
 * Busca todas as paginas de um endpoint paginado, ate `maxItens`.
 * Para quando a pagina vem menor que o tamanho pedido ou quando o total informado e atingido.
 */
export async function todasPaginas(
  cfg: Config,
  empresa: Empresa,
  c: Chamada,
  opts: { tamanho?: number; maxItens?: number; nomePagina?: string; nomeTamanho?: string } = {}
): Promise<{ itens: Record<string, unknown>[]; total_informado: number | null; truncado: boolean; ultima: unknown }> {
  const tamanho = opts.tamanho ?? 100;
  const max = opts.maxItens ?? 2000;
  const kp = opts.nomePagina ?? "pagina";
  const kt = opts.nomeTamanho ?? "tamanho_pagina";
  const itens: Record<string, unknown>[] = [];
  let total: number | null = null;
  let ultima: unknown = null;
  for (let pagina = 1; pagina <= 200; pagina++) {
    const r = await api(cfg, empresa, { ...c, params: { ...(c.params ?? {}), [kp]: pagina, [kt]: tamanho } });
    ultima = r;
    const lote = itensDe(r);
    total = totalDe(r) ?? total;
    itens.push(...lote);
    if (itens.length >= max) return { itens: itens.slice(0, max), total_informado: total, truncado: true, ultima };
    if (lote.length < tamanho) break;
    if (total !== null && itens.length >= total) break;
  }
  return { itens, total_informado: total, truncado: false, ultima };
}

export const num = (v: unknown) => (typeof v === "number" ? v : Number(String(v ?? "").replace(",", ".")) || 0);
export const brl = (n: number) => n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
export const arred = (n: number) => Math.round(n * 100) / 100;
