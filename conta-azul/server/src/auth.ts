/**
 * OAuth 2.0 da Conta Azul — o ponto mais fragil de qualquer integracao.
 *
 * Regras que este arquivo garante:
 *  1. refresh_token e ROTATIVO: cada renovacao invalida o anterior. O novo par e gravado em disco
 *     (escrita atomica) ANTES de o access_token ser usado.
 *  2. Um unico processo renova por vez. Claude Desktop e Claude Code podem subir cada um o seu
 *     servidor; sem trava, os dois renovam juntos, um recebe invalid_grant e a corrente quebra.
 *     Trava = diretorio criado com mkdir (atomico no POSIX), com expiracao para trava orfa.
 *  3. Depois de pegar a trava, RELE o arquivo: outro processo pode ter acabado de renovar.
 */
import { readFileSync, writeFileSync, renameSync, existsSync, mkdirSync, rmSync, statSync, chmodSync } from "node:fs";
import { join } from "node:path";
import { randomBytes } from "node:crypto";
import { STATE_DIR, garantirDiretorios, type Config, type Empresa } from "./config.js";

export const AUTHORIZE_URL =
  process.env.CONTAAZUL_AUTHORIZE_URL ?? "https://login.contaazul.com/#/oauth/authorize";
export const TOKEN_URL = process.env.CONTAAZUL_TOKEN_URL ?? "https://api-v2.contaazul.com/oauth/token";
export const SCOPE = "openid+profile+aws.cognito.signin.user.admin";

/** Renova quando faltar menos que isso para expirar. */
const MARGEM_MS = 5 * 60 * 1000;
const TRAVA_ORFA_MS = 60 * 1000;
const ESPERA_TRAVA_MS = 30 * 1000;

export interface Tokens {
  access_token: string;
  refresh_token: string;
  /** epoch ms */
  expira_em: number;
  atualizado_em: string;
  empresa_conectada?: { id_empresa?: string; razao_social?: string; documento?: string };
}

const arquivoToken = (e: Empresa) => join(STATE_DIR, "tokens", `${e.slug}.json`);
const dirTrava = (e: Empresa) => join(STATE_DIR, "tokens", `${e.slug}.lock`);
const PENDENTES = () => join(STATE_DIR, "autorizacoes-pendentes.json");

export function lerTokens(e: Empresa): Tokens | null {
  const f = arquivoToken(e);
  if (!existsSync(f)) return null;
  try {
    return JSON.parse(readFileSync(f, "utf8")) as Tokens;
  } catch {
    throw new Error(
      `Arquivo de token corrompido (${f}). Rode contaazul_conectar para autorizar de novo.`
    );
  }
}

/** Escrita atomica: tmp + rename, permissao 600. */
function gravarAtomico(caminho: string, dados: unknown): void {
  garantirDiretorios();
  const tmp = `${caminho}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(tmp, JSON.stringify(dados, null, 2), { mode: 0o600 });
  renameSync(tmp, caminho);
  try {
    chmodSync(caminho, 0o600);
  } catch {
    /* ignore */
  }
}

export function gravarTokens(e: Empresa, t: Tokens): void {
  gravarAtomico(arquivoToken(e), t);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function comTrava<T>(e: Empresa, fn: () => Promise<T>): Promise<T> {
  garantirDiretorios();
  const trava = dirTrava(e);
  const inicio = Date.now();
  for (;;) {
    try {
      mkdirSync(trava);
      break;
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code !== "EEXIST") throw err;
      try {
        if (Date.now() - statSync(trava).mtimeMs > TRAVA_ORFA_MS) {
          rmSync(trava, { recursive: true, force: true });
          continue;
        }
      } catch {
        continue;
      }
      if (Date.now() - inicio > ESPERA_TRAVA_MS) {
        throw new Error(
          "Outro processo esta renovando o token da Conta Azul ha mais de 30s. Tente de novo em instantes."
        );
      }
      await sleep(150);
    }
  }
  try {
    return await fn();
  } finally {
    rmSync(trava, { recursive: true, force: true });
  }
}

function basic(cfg: Config): string {
  return "Basic " + Buffer.from(`${cfg.clientId}:${cfg.clientSecret}`).toString("base64");
}

async function postToken(cfg: Config, corpo: Record<string, string>): Promise<Tokens> {
  let res: Response;
  try {
    res = await fetch(TOKEN_URL, {
      method: "POST",
      headers: {
        Authorization: basic(cfg),
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/json",
      },
      body: new URLSearchParams(corpo).toString(),
      signal: AbortSignal.timeout(30000),
    });
  } catch (e) {
    throw new Error(`Falha de rede ao falar com o servidor de tokens da Conta Azul: ${(e as Error).message}`);
  }
  const texto = await res.text();
  let j: Record<string, unknown> = {};
  try {
    j = JSON.parse(texto);
  } catch {
    /* corpo nao-JSON */
  }
  if (!res.ok || !j.access_token) {
    throw new Error(explicarErroToken(res.status, j, texto, corpo.grant_type));
  }
  return {
    access_token: String(j.access_token),
    refresh_token: String(j.refresh_token ?? corpo.refresh_token ?? ""),
    expira_em: Date.now() + Number(j.expires_in ?? 3600) * 1000,
    atualizado_em: new Date().toISOString(),
  };
}

function explicarErroToken(status: number, j: Record<string, unknown>, texto: string, grant: string): string {
  const sub = String(j.error_subtype ?? "");
  const desc = String(j.error_description ?? j.message ?? texto.slice(0, 300));
  const reconectar = "Rode contaazul_conectar para autorizar de novo no navegador.";
  if (sub === "access_revoked")
    return `A empresa revogou o acesso deste app na Conta Azul (access_revoked). ${reconectar}`;
  if (sub === "invalid_refresh_token")
    return `O refresh_token gravado ja foi usado ou nao existe mais (invalid_refresh_token) — a corrente de renovacao quebrou. ${reconectar}`;
  if (sub === "invalid_client")
    return `client_id/client_secret invalidos ou mal copiados (invalid_client). Confira o ~/.conta-azul-mcp.json.`;
  if (grant === "authorization_code" && j.error === "invalid_grant")
    return (
      `A Conta Azul recusou o codigo (invalid_grant). Causas, em ordem: o codigo tem mais de 3 minutos, ` +
      `ja foi usado uma vez, ou o redirect_uri do arquivo nao e identico (byte a byte) ao cadastrado no Portal. ` +
      `Gere um codigo novo com contaazul_conectar. Detalhe: ${desc}`
    );
  return `Servidor de tokens da Conta Azul respondeu ${status}: ${j.error ?? ""} ${desc}`.trim();
}

// ------------------------------------------------------------------ fluxo de autorizacao

interface Pendente {
  state: string;
  empresa: string;
  criado_em: number;
}

function lerPendentes(): Pendente[] {
  try {
    const l = JSON.parse(readFileSync(PENDENTES(), "utf8")) as Pendente[];
    return l.filter((p) => Date.now() - p.criado_em < 30 * 60 * 1000);
  } catch {
    return [];
  }
}

export function novaAutorizacao(cfg: Config, e: Empresa): { url: string; state: string } {
  const state = randomBytes(16).toString("hex");
  gravarAtomico(PENDENTES(), [...lerPendentes(), { state, empresa: e.slug, criado_em: Date.now() }]);
  const url =
    `${AUTHORIZE_URL}?response_type=code` +
    `&client_id=${encodeURIComponent(cfg.clientId)}` +
    `&redirect_uri=${encodeURIComponent(cfg.redirectUri)}` +
    `&state=${state}` +
    `&scope=${SCOPE}`;
  return { url, state };
}

/** Confere o state (CSRF) e devolve a empresa a que ele pertence. */
export function consumirState(state: string): string | null {
  const l = lerPendentes();
  const p = l.find((x) => x.state === state);
  if (!p) return null;
  gravarAtomico(PENDENTES(), l.filter((x) => x.state !== state));
  return p.empresa;
}

/** Aceita a URL inteira para onde o navegador foi redirecionado, ou so o code. */
export function extrairCode(entrada: string): { code: string; state?: string } {
  const s = entrada.trim();
  if (/^https?:\/\//i.test(s) || s.includes("code=")) {
    const q = s.includes("?") ? s.slice(s.indexOf("?") + 1) : s;
    const p = new URLSearchParams(q.split("#")[0]);
    const code = p.get("code");
    if (!code) throw new Error("Nao achei o parametro code nessa URL. Copie a URL completa da barra de endereco.");
    return { code, state: p.get("state") ?? undefined };
  }
  return { code: s };
}

export async function trocarCode(cfg: Config, e: Empresa, code: string): Promise<Tokens> {
  const t = await postToken(cfg, {
    grant_type: "authorization_code",
    code,
    redirect_uri: cfg.redirectUri,
  });
  gravarTokens(e, t);
  return t;
}

// ------------------------------------------------------------------ uso diario

/**
 * Devolve um access_token valido, renovando se preciso.
 * `forcar` = a API acabou de responder 401 com `tokenRejeitado`.
 */
export async function accessToken(cfg: Config, e: Empresa, tokenRejeitado?: string): Promise<string> {
  const atual = lerTokens(e);
  if (!atual) {
    throw new Error(
      `A empresa "${e.nome}" ainda nao foi conectada a Conta Azul. Rode contaazul_conectar.`
    );
  }
  const valido = (t: Tokens) =>
    t.access_token !== tokenRejeitado && t.expira_em - MARGEM_MS > Date.now();
  if (valido(atual)) return atual.access_token;

  return comTrava(e, async () => {
    // Rele dentro da trava: outro processo pode ter renovado enquanto esperavamos.
    const agora = lerTokens(e)!;
    if (valido(agora)) return agora.access_token;
    const novo = await postToken(cfg, { grant_type: "refresh_token", refresh_token: agora.refresh_token });
    gravarTokens(e, { ...novo, empresa_conectada: agora.empresa_conectada }); // grava ANTES de usar
    return novo.access_token;
  });
}
