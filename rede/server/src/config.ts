/**
 * Configuracao do plugin rede.
 *
 * Dois arquivos, com donos diferentes:
 *  - ~/.rede-mcp.json          -> escrito pela PESSOA (ambiente, credenciais do app, usuario, PVs)
 *  - ~/.rede-mcp/tokens/*.json -> escrito pelo SERVIDOR (access/refresh token, expiram rapido)
 *
 * Separar os dois evita que o servidor reescreva a cada 20 minutos o arquivo que a pessoa edita.
 *
 * A Rede tem DOIS ambientes com credenciais diferentes e bases diferentes. Trocar de ambiente
 * sem trocar as credenciais e o erro numero 1 da integracao, entao o ambiente fica gravado no
 * nome do arquivo de token: sandbox e producao nunca compartilham token.
 */
import { readFileSync, existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export type Ambiente = "sandbox" | "producao";

export interface Pv {
  /** Nome amigavel usado no parametro "pv" das tools. */
  nome: string;
  /** Numero do Ponto de Venda (ate 9 digitos), como a Rede o conhece. */
  numero: string;
}

/**
 * Como pedir o token. A doc oficial da Rede so descreve "password", mas o sandbox aceita
 * "client_credentials" com client_id/secret apenas — e e assim que um projeto criado em
 * "Meus Projetos" funciona, sem esperar o e-mail do time de Integracoes.
 */
export type Grant = "client_credentials" | "password";

export interface Config {
  ambiente: Ambiente;
  clientId: string;
  clientSecret: string;
  /** So no grant "password". */
  usuario?: string;
  senha?: string;
  grant: Grant;
  pvs: Pv[];
  /**
   * Base alternativa so para a consulta de vendas por NSU. A doc do sandbox aponta
   * https://payments-apisandbox.useredecloud.com.br para essa rota, diferente de todas as
   * outras. Fica opcional: so preencha se a rota der 404 na base padrao.
   */
  baseNsu?: string;
  origem: string;
}

/**
 * Bases oficiais. REDE_BASE_URL e REDE_TOKEN_URL sobrescrevem as duas — e assim que o teste de
 * integracao aponta o servidor para a API simulada sem mexer no codigo.
 */
const semBarra = (u: string) => u.replace(/\/+$/, "");

export const BASES: Record<Ambiente, { api: string; token: string }> = {
  sandbox: {
    api: semBarra(process.env.REDE_BASE_URL?.trim() || "https://rl7-sandbox-api.useredecloud.com.br"),
    token:
      process.env.REDE_TOKEN_URL?.trim() ||
      `${semBarra(process.env.REDE_BASE_URL?.trim() || "https://rl7-sandbox-api.useredecloud.com.br")}/oauth/token`,
  },
  producao: {
    api: semBarra(process.env.REDE_BASE_URL?.trim() || "https://api.userede.com.br/redelabs"),
    token:
      process.env.REDE_TOKEN_URL?.trim() ||
      `${semBarra(process.env.REDE_BASE_URL?.trim() || "https://api.userede.com.br/redelabs")}/oauth/token`,
  },
};

export const CONFIG_FILE = process.env.REDE_CONFIG_FILE?.trim() || join(homedir(), ".rede-mcp.json");
export const STATE_DIR = process.env.REDE_STATE_DIR?.trim() || join(homedir(), ".rede-mcp");

export function garantirDiretorios(): void {
  mkdirSync(join(STATE_DIR, "tokens"), { recursive: true, mode: 0o700 });
}

const PLACEHOLDER = /^(cole_aqui|seu_|xxx+|\.\.\.)/i;
const vazio = (v?: unknown) => typeof v !== "string" || !v.trim() || PLACEHOLDER.test(v.trim());

export function fold(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").trim().toLowerCase();
}

export function slugify(s: string): string {
  return fold(s).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "pv";
}

function normalizarAmbiente(v: unknown): Ambiente {
  const k = fold(String(v ?? "sandbox"));
  if (["producao", "production", "prod", "prd"].includes(k)) return "producao";
  if (["sandbox", "sbx", "homologacao", "teste"].includes(k)) return "sandbox";
  throw new Error(`ambiente "${v}" nao reconhecido em ${CONFIG_FILE}. Use "sandbox" ou "producao".`);
}

/** Numero de PV: so digitos, ate 9. Erra cedo em vez de virar 422 la na frente. */
export function normalizarNumeroPv(v: unknown, onde: string): string {
  const s = String(v ?? "").replace(/\D/g, "");
  if (!s) throw new Error(`${onde}: numero do PV vazio ou sem digitos.`);
  if (s.length > 9) throw new Error(`${onde}: numero do PV "${s}" tem ${s.length} digitos; a Rede aceita ate 9.`);
  return s;
}

export function carregarConfig(): Config {
  if (!existsSync(CONFIG_FILE)) {
    throw new Error(`Arquivo de configuracao nao encontrado: ${CONFIG_FILE}. Rode /rede-setup para criar.`);
  }
  let raw: Record<string, unknown>;
  try {
    raw = JSON.parse(readFileSync(CONFIG_FILE, "utf8"));
  } catch (e) {
    throw new Error(`${CONFIG_FILE} nao e um JSON valido — ${(e as Error).message}`);
  }

  const clientId = raw.client_id ?? raw.clientId;
  const clientSecret = raw.client_secret ?? raw.clientSecret;
  const usuario = raw.usuario ?? raw.username;
  const senha = raw.senha ?? raw.password;

  const faltando: string[] = [];
  if (vazio(clientId)) faltando.push("client_id");
  if (vazio(clientSecret)) faltando.push("client_secret");
  if (faltando.length) {
    throw new Error(
      `${CONFIG_FILE} esta incompleto — falta preencher: ${faltando.join(", ")}. ` +
        `Os dois saem do projeto criado em "Meus Projetos" no Portal do Desenvolvedor da Rede, ` +
        `no pacote "APIs de Conciliacao" (um projeto de Payment Link gera credencial que NAO abre estas rotas).`
    );
  }

  // Sem usuario/senha o caminho e client_credentials, que e o que o sandbox usa de fato.
  const temUsuario = !vazio(usuario) && !vazio(senha);
  const grantPedido = vazio(raw.grant) ? undefined : fold(String(raw.grant));
  let grant: Grant;
  if (grantPedido === "password") {
    if (!temUsuario) {
      throw new Error(
        `${CONFIG_FILE} pede grant "password", mas "usuario" e "senha" estao vazios. ` +
          `Preencha os dois (o time de Integracoes da Rede os envia por e-mail) ou remova o campo "grant" ` +
          `para usar client_credentials so com client_id e client_secret.`
      );
    }
    grant = "password";
  } else if (grantPedido === "client_credentials") {
    grant = "client_credentials";
  } else {
    grant = temUsuario ? "password" : "client_credentials";
  }
  if (String(clientId).trim() === String(clientSecret).trim()) {
    throw new Error(
      `client_id e client_secret estao iguais em ${CONFIG_FILE} — provavelmente o mesmo valor foi colado duas vezes. ` +
        `No Portal da Rede eles sao dois valores diferentes; o secret so aparece na tela do projeto.`
    );
  }

  const lista = Array.isArray(raw.pvs) ? raw.pvs : Array.isArray(raw.pontos_de_venda) ? raw.pontos_de_venda : [];
  if (!lista.length) {
    throw new Error(
      `${CONFIG_FILE} nao tem nenhum PV em "pvs". Informe ao menos um: ` +
        `[{ "nome": "Loja 1", "numero": "13381369" }]. No sandbox da Rede so existem 13381369 e 22523510.`
    );
  }
  const pvs: Pv[] = lista.map((p: unknown, i: number) => {
    const nome = typeof p === "string" ? p : (p as { nome?: string })?.nome;
    const numero = typeof p === "string" ? p : (p as { numero?: unknown })?.numero;
    const rotulo = `PV #${i + 1} em ${CONFIG_FILE}`;
    const num = normalizarNumeroPv(numero, rotulo);
    return { nome: vazio(nome) ? num : String(nome).trim(), numero: num };
  });

  return {
    ambiente: normalizarAmbiente(raw.ambiente),
    clientId: String(clientId).trim(),
    clientSecret: String(clientSecret).trim(),
    usuario: temUsuario ? String(usuario).trim() : undefined,
    senha: temUsuario ? String(senha) : undefined,
    grant,
    pvs,
    baseNsu: vazio(raw.base_nsu) ? undefined : String(raw.base_nsu).trim().replace(/\/+$/, ""),
    origem: CONFIG_FILE,
  };
}

/**
 * Resolve o PV a partir do que a pessoa disse: o apelido, o numero, ou nada
 * (se so houver um configurado). Tambem aceita um numero que nao esta na lista,
 * porque a permissao de leitura e concedida por PV do lado da Rede, nao aqui.
 */
export function resolverPv(cfg: Config, termo?: string): Pv {
  if (!termo) {
    if (cfg.pvs.length === 1) return cfg.pvs[0];
    throw new Error(
      `Ha ${cfg.pvs.length} PVs configurados — informe "pv". Disponiveis: ` +
        cfg.pvs.map((p) => `${p.nome} (${p.numero})`).join(", ")
    );
  }
  const k = fold(termo);
  const digitos = termo.replace(/\D/g, "");
  const achou =
    cfg.pvs.find((p) => p.numero === digitos) ??
    cfg.pvs.find((p) => fold(p.nome) === k) ??
    cfg.pvs.find((p) => fold(p.nome).includes(k));
  if (achou) return achou;
  if (digitos && digitos.length <= 9) return { nome: digitos, numero: digitos };
  throw new Error(
    `PV "${termo}" nao configurado e nao parece um numero de PV. Disponiveis: ` +
      cfg.pvs.map((p) => `${p.nome} (${p.numero})`).join(", ")
  );
}
