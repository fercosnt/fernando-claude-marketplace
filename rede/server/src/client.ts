/**
 * Client HTTP das APIs de Gestao de Vendas da Rede.
 *
 * Tudo aqui e leitura (a API so expoe GET), entao repetir e sempre seguro: ate 3 tentativas
 * em falha de rede, 429 e 5xx, com espera crescente.
 *
 * Tres particularidades da Rede que este arquivo esconde das tools:
 *  1. O Ponto de Venda viaja em TRES lugares diferentes dependendo da rota — query
 *     (parentCompanyNumber / parentMerchantId), path ({companyNumber} / {merchantId}) ou
 *     header (Merchant-Id). Quem chama informa o PV uma vez; o lugar certo e problema daqui.
 *  2. 204 quer dizer "consulta ok, nenhum registro" — nao e erro e nao pode virar excecao.
 *  3. Paginacao por cursor opaco: a resposta traz cursor.nextKey, que volta como pageKey.
 */
import { BASES, type Config } from "./config.js";
import { accessToken } from "./auth.js";
import { traduzir } from "./dominios.js";

const TIMEOUT_MS = Number(process.env.REDE_TIMEOUT_MS ?? 45000);
const MAX_TENTATIVAS = 3;
const INTERVALO_MIN_MS = Number(process.env.REDE_INTERVALO_MS ?? 200); // ~5 req/s, conservador
const MAX_PAGINAS = Number(process.env.REDE_MAX_PAGINAS ?? 20);

export type Params = Record<string, string | number | boolean | Array<string | number> | undefined | null>;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

let ultimaChamada = 0;
async function respeitarLimite(): Promise<void> {
  const espera = ultimaChamada + INTERVALO_MIN_MS - Date.now();
  ultimaChamada = Math.max(Date.now(), ultimaChamada + INTERVALO_MIN_MS);
  if (espera > 0) await sleep(espera);
}

/**
 * Monta a query string. A Rede usa listas separadas por virgula (?brands=1,2), nunca
 * chaves repetidas — por isso arrays sempre viram join(",").
 */
export function montarQuery(params: Params): string {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "") continue;
    if (Array.isArray(v)) {
      if (!v.length) continue;
      q.append(k, v.join(","));
    } else q.append(k, String(v));
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

export class ErroRede extends Error {
  constructor(message: string, public status: number, public corpo?: unknown) {
    super(message);
  }
}

/**
 * 403 + "Requisicao invalida" e como a Rede diz "esta rota nao esta habilitada para o seu
 * aplicativo". No sandbox e a resposta de toda a familia v2 de vendas, dos resumos, dos
 * recebiveis e dos bloqueios. Serve para decidir um fallback de versao em vez de desistir.
 */
export function rotaNaoHabilitada(e: unknown): boolean {
  if (!(e instanceof ErroRede) || e.status !== 403) return false;
  return /requisi[cç][aã]o inv[aá]lida/i.test(JSON.stringify(e.corpo ?? "") + e.message);
}

/** A Rede tem cinco formatos de erro diferentes. Este extrator cobre todos. */
function mensagemDe(corpo: unknown, textoCru: string): string {
  if (!corpo || typeof corpo !== "object") return textoCru.slice(0, 400);
  const o = corpo as Record<string, unknown>;

  const direta = o.message ?? o.error_message ?? o.error_description ?? o.error;
  if (typeof direta === "string" && direta.trim()) {
    const cod = o.error_code ? ` (codigo ${o.error_code})` : "";
    return `${direta}${cod}`;
  }
  // 422: { campo: ["msg"] } ou { queryStringParameters: { campo: [...] } } ou { pathParameters: {...} }
  // 400: { errors: { Campo: ["msg"] } }
  const alvo = (o.errors ?? o.queryStringParameters ?? o.pathParameters ?? o) as Record<string, unknown>;
  const partes: string[] = [];
  for (const [campo, msgs] of Object.entries(alvo)) {
    if (Array.isArray(msgs)) partes.push(`${campo}: ${msgs.join("; ")}`);
    else if (msgs && typeof msgs === "object") {
      for (const [c2, m2] of Object.entries(msgs as Record<string, unknown>)) {
        if (Array.isArray(m2)) partes.push(`${c2}: ${m2.join("; ")}`);
      }
    }
  }
  return partes.length ? partes.join(" | ") : JSON.stringify(corpo).slice(0, 400);
}

function explicarStatus(status: number, caminho: string, msg: string, pv?: string): string {
  const base = `Rede GET ${caminho}: ${status}`;

  // Respostas que so aparecem no sandbox, observadas na API real e ausentes do swagger.
  if (/scenario is not available in the sandbox/i.test(msg)) {
    return (
      `${base} — o sandbox da Rede nao tem cenario para esta combinacao de filtros. Nao e erro de ` +
      `configuracao: o ambiente de teste so responde a casos pre-definidos. Em /v1/payments, por exemplo, ` +
      `e preciso mandar um filtro que exista no roteiro de teste: size 1, 5 ou 10, status PENDING, ` +
      `brands 1 ou 2, types DEBIT ou CREDIT — outros valores, e a consulta sem filtro nenhum, sao recusados. ` +
      `A consulta de vendas por NSU so responde no PV 1254405, de 2022-11-22 a 2022-11-28.`
    );
  }
  // Resposta de producao quando o token e valido mas o PV nao foi liberado para o parceiro.
  // Vem como 403 ("Partner not allowed for this company number") ou 401 ("... merchant", codigo 1001).
  if (/partner not allowed/i.test(msg)) {
    return (
      `${base} — o PV${pv ? ` ${pv}` : ""} ainda nao esta liberado para este aplicativo ("${msg}"). ` +
      `O login funcionou; falta a autorizacao do estabelecimento. E preciso uma solicitacao de acesso ` +
      `(pelo portal ou pela API de Gestao de Acessos) e a aprovacao na area logada do lojista no Portal Rede. ` +
      `Ver docs/producao.md, passo 2.`
    );
  }
  if (/insufficient access level/i.test(msg)) {
    return (
      `${base} — nivel de acesso insuficiente para esta funcionalidade ("${msg}"). Se o PV ainda nao foi ` +
      `liberado, resolva isso primeiro. Se ja foi e o erro continua, a permissao concedida na solicitacao de ` +
      `acesso ou o pacote contratado nao inclui esta visao — pedir a inclusao a Rede.`
    );
  }
  if (status === 403 && /requisi[cç][aã]o inv[aá]lida/i.test(msg)) {
    return (
      `${base} — a Rede respondeu "Requisicao invalida", que aqui costuma significar rota nao habilitada ` +
      `para este aplicativo (e nao filtro errado). No sandbox, as rotas de recebiveis, bloqueios, os resumos ` +
      `de venda e a v2 de vendas respondem assim mesmo com credencial correta. Em producao, confira se o ` +
      `pacote contratado inclui esta visao e se o PV${pv ? ` ${pv}` : ""} esta liberado.`
    );
  }

  switch (status) {
    case 400:
      return `${base} — requisicao invalida: ${msg}. Quase sempre e um parametro obrigatorio faltando (nas rotas v2/v3 o PV vai no header Merchant-Id) ou data fora de YYYY-MM-DD.`;
    case 401:
      return `${base} — nao autorizado: ${msg}. O token foi renovado e ainda assim recusou. Duas causas, nesta ordem: (1) o projeto no Portal da Rede nao e do pacote "APIs de Conciliacao" — um projeto de Payment Link autentica normalmente, mas o token sai com escopo "payment-link" e TODA rota de extrato responde 401; rode rede_conectar para ver o escopo do token; (2) o usuario nao tem permissao de extrato para o PV${pv ? ` ${pv}` : ""}, liberada pela Rede na gestao de acessos.`;
    case 403:
      return `${base} — sem permissao para o PV${pv ? ` ${pv}` : ""}: ${msg}. O parceiro precisa ser liberado para este estabelecimento na gestao de acessos da Rede.`;
    case 404:
      return `${base} — rota nao encontrada. Confira a versao (v1/v2/v3) e lembre que a consulta de vendas por NSU roda em uma base diferente no sandbox (ver base_nsu no ~/.rede-mcp.json). ${msg}`;
    case 422:
      return `${base} — dado recusado pela validacao: ${msg}.`;
    case 429:
      return `${base} — limite de chamadas estourado. Espere alguns segundos e repita.`;
    case 500:
    case 502:
    case 503:
      return `${base} — instabilidade do lado da Rede: ${msg}. Repetimos ${MAX_TENTATIVAS}x e nao passou; tente mais tarde.`;
    default:
      return `${base} — ${msg}`;
  }
}

export interface Chamada {
  caminho: string;
  params?: Params;
  /** PV que vai no header Merchant-Id (rotas v2 payments/summary, v3 receivables, charges/cashbacks). */
  merchantIdHeader?: string;
  /** Base diferente da padrao — usada so pela consulta de vendas por NSU no sandbox. */
  base?: string;
  /** Apenas para a mensagem de erro. */
  pv?: string;
}

interface Resposta {
  status: number;
  dados: unknown;
}

async function uma(cfg: Config, c: Chamada): Promise<Resposta> {
  const base = (c.base ?? BASES[cfg.ambiente].api).replace(/\/+$/, "");
  const caminho = "/" + c.caminho.replace(/^\/+/, "");
  const url = `${base}${caminho}${montarQuery(c.params ?? {})}`;

  let tokenRejeitado: string | undefined;
  let jaRenovouPor401 = false;

  for (let tentativa = 1; ; tentativa++) {
    const token = await accessToken(cfg, tokenRejeitado);
    await respeitarLimite();

    let res: Response;
    try {
      res = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
          // Mesmo sem corpo: /v2/payments/installments/{pv} responde 415 sem este cabecalho em
          // producao (confirmado em 2026-09-21). Nas demais rotas ele e inofensivo.
          "Content-Type": "application/json",
          ...(c.merchantIdHeader ? { "Merchant-Id": c.merchantIdHeader } : {}),
        },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
    } catch (e) {
      if (tentativa < MAX_TENTATIVAS) {
        await sleep(800 * tentativa);
        continue;
      }
      throw new ErroRede(`Rede GET ${caminho} — falha de rede apos ${MAX_TENTATIVAS} tentativas: ${(e as Error).message}`, 0);
    }

    // 204 = processou e nao achou registro. Resposta legitima, nao erro.
    if (res.status === 204) return { status: 204, dados: null };

    const texto = await res.text();
    let corpo: unknown = null;
    if (texto.trim()) {
      try {
        corpo = JSON.parse(texto);
      } catch {
        corpo = texto;
      }
    }

    if (res.ok) return { status: res.status, dados: corpo };

    // 401 com token que o relogio dizia valido: renova uma vez e repete.
    if (res.status === 401 && !jaRenovouPor401) {
      jaRenovouPor401 = true;
      tokenRejeitado = token;
      continue;
    }
    if ((res.status === 429 || res.status >= 500) && tentativa < MAX_TENTATIVAS) {
      await sleep(1000 * tentativa);
      continue;
    }
    throw new ErroRede(explicarStatus(res.status, caminho, mensagemDe(corpo, texto), c.pv), res.status, corpo);
  }
}

/** Uma chamada, com os codigos ja traduzidos. */
export async function api(cfg: Config, c: Chamada): Promise<unknown> {
  const r = await uma(cfg, c);
  if (r.status === 204) return { vazio: true, mensagem: "A Rede processou a consulta e nao encontrou nenhum registro no periodo/filtro informado." };
  return traduzir(r.dados);
}

const cursorDe = (d: unknown): { tem: boolean; chave?: string } => {
  const o = d as Record<string, unknown> | null;
  const c = (o?.cursor ?? (o?.content as Record<string, unknown>)?.cursor) as Record<string, unknown> | undefined;
  if (!c) return { tem: false };
  const chave = c.nextKey ? String(c.nextKey) : undefined;
  return { tem: c.hasNextKey === true && !!chave, chave };
};

/**
 * Segue a paginacao por cursor ate acabar ou bater o teto.
 * Devolve as paginas cruas (ja traduzidas) mais um resumo do que aconteceu — quem chama
 * decide como juntar, porque cada rota guarda a lista em um caminho diferente do JSON.
 */
export async function apiPaginado(
  cfg: Config,
  c: Chamada,
  maxPaginas = MAX_PAGINAS
): Promise<{ paginas: unknown[]; completo: boolean; total_paginas: number; proximo_page_key?: string }> {
  const paginas: unknown[] = [];
  let pageKey: string | undefined;
  let completo = true;

  for (let i = 0; i < maxPaginas; i++) {
    const r = await uma(cfg, { ...c, params: { ...(c.params ?? {}), ...(pageKey ? { pageKey } : {}) } });
    if (r.status === 204) break;
    paginas.push(traduzir(r.dados));
    const cur = cursorDe(r.dados);
    if (!cur.tem) {
      pageKey = undefined;
      break;
    }
    pageKey = cur.chave;
    if (i === maxPaginas - 1) completo = false;
  }
  return { paginas, completo, total_paginas: paginas.length, proximo_page_key: completo ? undefined : pageKey };
}

/** Junta a lista que mora em content.<campo> de varias paginas. */
export function juntar(paginas: unknown[], campo: string): unknown[] {
  const fora: unknown[] = [];
  for (const p of paginas) {
    const o = p as Record<string, unknown>;
    const conteudo = (o?.content ?? o) as Record<string, unknown>;
    const lista = conteudo?.[campo] ?? o?.[campo];
    if (Array.isArray(lista)) fora.push(...lista);
  }
  return fora;
}
