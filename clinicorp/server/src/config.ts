/**
 * Configuracao das clinicas.
 *
 * Fontes, em ordem de precedencia:
 *  1. CLINICORP_CLINICS       — JSON inline (array de clinicas)
 *  2. CLINICORP_CLINICS_FILE  — caminho para arquivo JSON
 *  3. ~/.clinicorp-mcp.json   — arquivo padrao (recomendado: evita token no config do Claude)
 *  4. CLINICORP_SUBSCRIBER_ID + CLINICORP_USERNAME + CLINICORP_TOKEN — clinica unica
 */
import { readFileSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export interface Clinic {
  nome: string;
  /** Opcional: se ausente, e descoberto via /group/list_subscribers e cacheado. */
  subscriberId?: string;
  username: string;
  token: string;
  businessId?: string;
}

const DEFAULT_FILE = join(homedir(), ".clinicorp-mcp.json");

/** Ligada quando o arquivo de credenciais usa a forma { "escrita": true, "clinicas": [...] }. */
let escritaNaConfig = false;

export function escritaLiberadaNaConfig(): boolean {
  return escritaNaConfig;
}

interface RawClinic {
  nome?: string;
  name?: string;
  subscriber_id?: string;
  subscriberId?: string;
  username?: string;
  token?: string;
  business_id?: string;
  businessId?: string;
}

const PLACEHOLDER = /^(cole_aqui|seu_|nome_da_clinica|\.\.\.|x+)$/i;

function vazio(v?: string): boolean {
  return !v || !v.trim() || PLACEHOLDER.test(v.trim());
}

function normalize(raw: RawClinic, index: number): Clinic {
  const nome = raw.nome ?? raw.name;
  const subscriberId = raw.subscriber_id ?? raw.subscriberId;
  const username = raw.username;
  const token = raw.token;

  const faltando: string[] = [];
  if (vazio(nome)) faltando.push("nome");
  if (vazio(username)) faltando.push("username");
  if (vazio(token)) faltando.push("token");

  if (faltando.length > 0) {
    throw new Error(
      `Clinica #${index + 1} (${nome ?? "sem nome"}) esta incompleta — falta preencher: ${faltando.join(", ")}. ` +
        `O subscriber_id e opcional: se voce nao souber, deixe fora que o servidor descobre sozinho.`
    );
  }

  return {
    nome: nome!,
    subscriberId: vazio(subscriberId ? String(subscriberId) : undefined)
      ? undefined
      : String(subscriberId),
    username: username!,
    token: token!,
    businessId: raw.business_id ?? raw.businessId,
  };
}

function parseList(json: string, origem: string): Clinic[] {
  let parsed: unknown;
  try {
    parsed = JSON.parse(json);
  } catch (e) {
    throw new Error(`Configuracao invalida em ${origem}: JSON malformado — ${(e as Error).message}`);
  }

  // Forma de objeto permite ligar a escrita no proprio arquivo:
  // { "escrita": true, "clinicas": [ ... ] }
  if (!Array.isArray(parsed) && parsed && typeof parsed === "object") {
    escritaNaConfig = (parsed as { escrita?: boolean }).escrita === true;
  }

  const lista = Array.isArray(parsed)
    ? parsed
    : Array.isArray((parsed as { clinicas?: unknown[] }).clinicas)
      ? (parsed as { clinicas: unknown[] }).clinicas
      : null;

  if (!lista) {
    throw new Error(
      `Configuracao invalida em ${origem}: esperado um array de clinicas ou um objeto { "clinicas": [...] }`
    );
  }

  return lista.map((c, i) => normalize(c as RawClinic, i));
}

export function loadClinics(): Clinic[] {
  const inline = process.env.CLINICORP_CLINICS?.trim();
  if (inline) return parseList(inline, "CLINICORP_CLINICS");

  const file = process.env.CLINICORP_CLINICS_FILE?.trim();
  if (file) {
    if (!existsSync(file)) {
      throw new Error(`CLINICORP_CLINICS_FILE aponta para arquivo inexistente: ${file}`);
    }
    return parseList(readFileSync(file, "utf8"), file);
  }

  if (existsSync(DEFAULT_FILE)) {
    return parseList(readFileSync(DEFAULT_FILE, "utf8"), DEFAULT_FILE);
  }

  const { CLINICORP_SUBSCRIBER_ID, CLINICORP_USERNAME, CLINICORP_TOKEN, CLINICORP_BUSINESS_ID } =
    process.env;

  if (CLINICORP_SUBSCRIBER_ID && CLINICORP_USERNAME && CLINICORP_TOKEN) {
    return [
      {
        nome: process.env.CLINICORP_CLINIC_NAME ?? "default",
        subscriberId: CLINICORP_SUBSCRIBER_ID,
        username: CLINICORP_USERNAME,
        token: CLINICORP_TOKEN,
        businessId: CLINICORP_BUSINESS_ID,
      },
    ];
  }

  throw new Error(
    `Nenhuma clinica configurada. Crie ${DEFAULT_FILE} com um array de clinicas ` +
      `[{ "nome": "...", "subscriber_id": "...", "username": "...", "token": "..." }] ` +
      `ou defina CLINICORP_CLINICS / CLINICORP_CLINICS_FILE.`
  );
}

/** Resolve a clinica pelo nome (case/acento-insensitive) ou pelo subscriber_id. */
export function resolveClinic(clinicas: Clinic[], termo?: string): Clinic {
  if (!termo) {
    if (clinicas.length === 1) return clinicas[0];
    throw new Error(
      `Ha ${clinicas.length} clinicas configuradas — informe qual usar em "clinica". ` +
        `Disponiveis: ${clinicas.map((c) => c.nome).join(", ")}`
    );
  }

  const chave = fold(termo);
  const match =
    clinicas.find((c) => fold(c.nome) === chave || c.subscriberId === termo) ??
    clinicas.find((c) => fold(c.nome).includes(chave));

  if (!match) {
    throw new Error(
      `Clinica "${termo}" nao encontrada. Disponiveis: ${clinicas.map((c) => c.nome).join(", ")}`
    );
  }
  return match;
}

function fold(s: string): string {
  return s
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLowerCase();
}
