/**
 * OAuth 2.0 da Rede.
 *
 * Basic <client_id:client_secret> no header, corpo x-www-form-urlencoded. Dois grants:
 *
 *   client_credentials -> so client_id e client_secret. NAO esta na doc oficial, mas e o que
 *                         o sandbox realmente aceita, e o token sai com o escopo
 *                         "merchant-statement". E o padrao aqui quando nao ha usuario/senha.
 *   password           -> o unico documentado; exige usuario e senha que o time de Integracoes
 *                         da Rede envia por e-mail.
 *
 * Em ambos, a resposta traz access_token de vida curta (expires_in 1440s = 24 minutos, exatamente
 * o que a doc manda renovar) e refresh_token de 24 horas.
 *
 * Consequencia pratica: TODA sessao de mais de um dia perde o refresh_token. Como as credenciais
 * ficam no arquivo local, este modulo refaz o login sozinho quando o refresh morre — a pessoa nao
 * precisa reconectar nada. E o principal motivo de este arquivo existir em vez de um fetch solto
 * no client.
 *
 * Tres garantias:
 *  1. O par novo e gravado em disco (escrita atomica, permissao 600) ANTES de ser usado.
 *  2. Um unico processo renova por vez. Claude Desktop e Claude Code podem subir cada um o
 *     seu servidor; sem trava, os dois renovam juntos e um invalida o token do outro.
 *     Trava = diretorio criado com mkdir (atomico no POSIX), com expiracao para trava orfa.
 *  3. Depois de pegar a trava, RELE o arquivo: outro processo pode ter acabado de renovar.
 */
import { readFileSync, writeFileSync, renameSync, existsSync, mkdirSync, rmSync, statSync, chmodSync } from "node:fs";
import { join } from "node:path";
import { BASES, STATE_DIR, garantirDiretorios, type Ambiente, type Config } from "./config.js";

/** Renova quando faltar menos que isso para o access_token expirar. */
const MARGEM_MS = 3 * 60 * 1000;
/** A Rede da 24h de vida ao refresh_token; paramos antes para nao tentar um morto. */
const VIDA_REFRESH_MS = 23 * 60 * 60 * 1000;
const TRAVA_ORFA_MS = 60 * 1000;
const ESPERA_TRAVA_MS = 30 * 1000;

export interface Tokens {
  access_token: string;
  refresh_token: string;
  /** epoch ms — quando o access_token expira */
  expira_em: number;
  /** epoch ms — quando o refresh_token nasceu (vale 24h a partir dai) */
  refresh_desde: number;
  atualizado_em: string;
  /** Como o par atual foi obtido, so para diagnostico. */
  origem: "password" | "client_credentials" | "refresh_token";
  escopo?: string;
}

const arquivoToken = (amb: Ambiente) => join(STATE_DIR, "tokens", `${amb}.json`);
const dirTrava = (amb: Ambiente) => join(STATE_DIR, "tokens", `${amb}.lock`);

export function lerTokens(amb: Ambiente): Tokens | null {
  const f = arquivoToken(amb);
  if (!existsSync(f)) return null;
  try {
    return JSON.parse(readFileSync(f, "utf8")) as Tokens;
  } catch {
    // Token corrompido nao e fatal aqui: o proximo acesso refaz o grant password.
    return null;
  }
}

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

export function gravarTokens(amb: Ambiente, t: Tokens): void {
  gravarAtomico(arquivoToken(amb), t);
}

export function esquecerTokens(amb: Ambiente): void {
  try {
    rmSync(arquivoToken(amb), { force: true });
  } catch {
    /* ignore */
  }
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function comTrava<T>(amb: Ambiente, fn: () => Promise<T>): Promise<T> {
  garantirDiretorios();
  const trava = dirTrava(amb);
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
        throw new Error("Outro processo esta renovando o token da Rede ha mais de 30s. Tente de novo em instantes.");
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
  const url = BASES[cfg.ambiente].token;
  let res: Response;
  try {
    res = await fetch(url, {
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
    throw new Error(`Falha de rede ao falar com o servidor de tokens da Rede (${url}): ${(e as Error).message}`);
  }
  const texto = await res.text();
  let j: Record<string, unknown> = {};
  try {
    j = JSON.parse(texto);
  } catch {
    /* corpo nao-JSON */
  }
  if (!res.ok || !j.access_token) {
    throw new Error(explicarErroToken(res.status, j, texto, corpo.grant_type, cfg));
  }
  const agora = Date.now();
  const grant = corpo.grant_type as Tokens["origem"];
  return {
    access_token: String(j.access_token),
    refresh_token: String(j.refresh_token ?? corpo.refresh_token ?? ""),
    expira_em: agora + Number(j.expires_in ?? 1440) * 1000,
    // O refresh so "nasce de novo" no grant password; o refresh_token grant devolve o mesmo relogio.
    refresh_desde: agora,
    atualizado_em: new Date(agora).toISOString(),
    origem: grant,
    escopo: j.scope ? String(j.scope) : undefined,
  };
}

function explicarErroToken(
  status: number,
  j: Record<string, unknown>,
  texto: string,
  grant: string,
  cfg: Config
): string {
  const err = String(j.error ?? j.status ?? "");
  const desc = String(j.error_description ?? j.message ?? texto.slice(0, 300));
  const onde = `Portal do Desenvolvedor da Rede (ambiente ${cfg.ambiente})`;

  // "Bad credentials" e a resposta padrao da Rede quando o Basic (client) nao confere.
  if (/bad credentials/i.test(desc) || err === "UNAUTHORIZED" || status === 401) {
    if (grant === "refresh_token") {
      return `refresh_token recusado (${desc}). Ele vale 24h; vou refazer o login do zero.`;
    }
    return (
      `A Rede recusou as credenciais (${status} ${desc}). Nessa ordem, confira: ` +
      `(1) client_id e client_secret sao dois valores DIFERENTES copiados do projeto em ${onde}; ` +
      `(2) o projeto foi criado no pacote "APIs de Conciliacao" — credencial de um projeto de ` +
      `Payment Link autentica, mas o token sai com escopo "payment-link" e as rotas de extrato ` +
      `respondem 401; ` +
      (cfg.grant === "password"
        ? `(3) usuario e senha sao os que o time de Integracoes enviou por e-mail, nao o login do portal; `
        : `(3) `) +
      `o ambiente do arquivo ("${cfg.ambiente}") e o mesmo em que as credenciais foram geradas — ` +
      `credencial de sandbox nao funciona em producao e vice-versa.`
    );
  }
  if (err === "invalid_client")
    return `client_id/client_secret invalidos ou mal copiados (invalid_client). Confira o ~/.rede-mcp.json.`;
  if (err === "unsupported_grant_type")
    return `A Rede nao aceitou o grant "${grant}". Este plugin usa grant_type=password, como manda a doc oficial.`;
  if (err === "invalid_grant")
    return `Usuario ou senha recusados pela Rede (invalid_grant): ${desc}. Confira "usuario" e "senha" no ~/.rede-mcp.json.`;
  return `Servidor de tokens da Rede respondeu ${status}: ${err} ${desc}`.trim();
}

/** Corpo do grant configurado — o unico lugar que sabe a diferenca entre os dois. */
function corpoDoLogin(cfg: Config): Record<string, string> {
  if (cfg.grant === "password") {
    return { grant_type: "password", username: cfg.usuario ?? "", password: cfg.senha ?? "" };
  }
  return { grant_type: "client_credentials" };
}

/** Faz o login do zero e grava. E o que rede_conectar chama. */
export async function login(cfg: Config): Promise<Tokens> {
  return comTrava(cfg.ambiente, async () => {
    const t = await postToken(cfg, corpoDoLogin(cfg));
    gravarTokens(cfg.ambiente, t);
    return t;
  });
}

const refreshVivo = (t: Tokens) => !!t.refresh_token && Date.now() - t.refresh_desde < VIDA_REFRESH_MS;

/**
 * Devolve um access_token valido, renovando se preciso — sem pedir nada a pessoa.
 * `tokenRejeitado` = a API acabou de responder 401 com esse token, entao ele nao serve
 * mesmo que o relogio diga que ainda vale.
 */
export async function accessToken(cfg: Config, tokenRejeitado?: string): Promise<string> {
  const atual = lerTokens(cfg.ambiente);
  const valido = (t: Tokens) => t.access_token !== tokenRejeitado && t.expira_em - MARGEM_MS > Date.now();
  if (atual && valido(atual)) return atual.access_token;

  return comTrava(cfg.ambiente, async () => {
    // Rele dentro da trava: outro processo pode ter renovado enquanto esperavamos.
    const agora = lerTokens(cfg.ambiente);
    if (agora && valido(agora)) return agora.access_token;

    if (agora && refreshVivo(agora)) {
      try {
        const novo = await postToken(cfg, { grant_type: "refresh_token", refresh_token: agora.refresh_token });
        // O refresh_token grant nao reinicia a janela de 24h: preserva o nascimento do par.
        gravarTokens(cfg.ambiente, { ...novo, refresh_desde: agora.refresh_desde });
        return novo.access_token;
      } catch {
        // Refresh morreu antes da hora (rotacao, revogacao, reinicio do lado da Rede).
        // Cair para o login com senha e o comportamento certo aqui, nao um erro a mostrar.
      }
    }
    const novo = await postToken(cfg, corpoDoLogin(cfg));
    gravarTokens(cfg.ambiente, novo);
    return novo.access_token;
  });
}
