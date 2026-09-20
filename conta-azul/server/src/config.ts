/**
 * Configuracao do plugin conta-azul.
 *
 * Dois arquivos, com donos diferentes:
 *  - ~/.conta-azul-mcp.json         -> escrito pela PESSOA (credenciais do app + empresas + escrita)
 *  - ~/.conta-azul-mcp/tokens/*.json -> escrito pelo SERVIDOR (access/refresh token, rotacionam)
 *
 * Separar os dois evita que o servidor reescreva a cada hora o arquivo que a pessoa edita.
 */
import { readFileSync, existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export interface Empresa {
  /** Nome amigavel usado no parametro "empresa" das tools. */
  nome: string;
  /** Slug usado no nome do arquivo de token. */
  slug: string;
}

export interface Config {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  escrita: boolean;
  empresas: Empresa[];
  origem: string;
}

export const CONFIG_FILE =
  process.env.CONTAAZUL_CONFIG_FILE?.trim() || join(homedir(), ".conta-azul-mcp.json");

export const STATE_DIR =
  process.env.CONTAAZUL_STATE_DIR?.trim() || join(homedir(), ".conta-azul-mcp");

export function garantirDiretorios(): void {
  mkdirSync(join(STATE_DIR, "tokens"), { recursive: true, mode: 0o700 });
}

const PLACEHOLDER = /^(cole_aqui|seu_|xxx+|\.\.\.)/i;
const vazio = (v?: unknown) => typeof v !== "string" || !v.trim() || PLACEHOLDER.test(v.trim());

export function slugify(s: string): string {
  return fold(s).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "empresa";
}

export function fold(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").trim().toLowerCase();
}

export function carregarConfig(): Config {
  if (!existsSync(CONFIG_FILE)) {
    throw new Error(
      `Arquivo de configuracao nao encontrado: ${CONFIG_FILE}. Rode /conta-azul-setup para criar.`
    );
  }
  let raw: Record<string, unknown>;
  try {
    raw = JSON.parse(readFileSync(CONFIG_FILE, "utf8"));
  } catch (e) {
    throw new Error(`${CONFIG_FILE} nao e um JSON valido — ${(e as Error).message}`);
  }

  const clientId = raw.client_id ?? raw.clientId;
  const clientSecret = raw.client_secret ?? raw.clientSecret;
  const redirectUri = raw.redirect_uri ?? raw.redirectUri;

  const faltando: string[] = [];
  if (vazio(clientId)) faltando.push("client_id");
  if (vazio(clientSecret)) faltando.push("client_secret");
  if (vazio(redirectUri)) faltando.push("redirect_uri");
  if (faltando.length) {
    throw new Error(
      `${CONFIG_FILE} esta incompleto — falta preencher: ${faltando.join(", ")}. ` +
        `Os tres ficam em Portal do Desenvolvedor Conta Azul -> Minhas aplicacoes.`
    );
  }

  const lista = Array.isArray(raw.empresas) ? raw.empresas : [{ nome: "Principal" }];
  const empresas: Empresa[] = lista.map((e: unknown, i: number) => {
    const nome = typeof e === "string" ? e : (e as { nome?: string })?.nome;
    if (vazio(nome)) throw new Error(`Empresa #${i + 1} em ${CONFIG_FILE} esta sem "nome".`);
    return { nome: nome!.trim(), slug: slugify(nome!) };
  });

  return {
    clientId: String(clientId).trim(),
    clientSecret: String(clientSecret).trim(),
    redirectUri: String(redirectUri).trim(),
    escrita: raw.escrita === true || String(process.env.CONTAAZUL_ESCRITA ?? "").toUpperCase() === "X",
    empresas,
    origem: CONFIG_FILE,
  };
}

/** Resolve a empresa pelo nome (sem diferenciar acento/maiuscula). */
export function resolverEmpresa(cfg: Config, termo?: string): Empresa {
  if (!termo) {
    if (cfg.empresas.length === 1) return cfg.empresas[0];
    throw new Error(
      `Ha ${cfg.empresas.length} empresas configuradas — informe "empresa". ` +
        `Disponiveis: ${cfg.empresas.map((e) => e.nome).join(", ")}`
    );
  }
  const k = fold(termo);
  const achou =
    cfg.empresas.find((e) => fold(e.nome) === k || e.slug === k) ??
    cfg.empresas.find((e) => fold(e.nome).includes(k));
  if (!achou) {
    throw new Error(
      `Empresa "${termo}" nao configurada. Disponiveis: ${cfg.empresas.map((e) => e.nome).join(", ")}`
    );
  }
  return achou;
}
