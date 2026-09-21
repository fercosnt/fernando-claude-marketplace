/**
 * Datas e janelas de consulta.
 *
 * Cada rota da Rede tem um limite proprio de periodo e devolve 422 quando ele estoura.
 * Validar aqui troca um 422 opaco por uma frase que diz exatamente como dividir a consulta.
 *
 * Limites, conforme o swagger oficial:
 *   62 dias -> vendas (v1 e v2), resumos de venda, vendas por NSU
 *   60 dias -> recebiveis visao calendario
 *   30 dias -> vendas parceladas v1, recebiveis v1, pagamentos v1, ordens de credito, debitos
 *   sem limite documentado -> recebiveis v3, pagamentos v2 (resumo e diario), bloqueios
 */

const FORMATO = /^\d{4}-\d{2}-\d{2}$/;
const DIA_MS = 24 * 60 * 60 * 1000;

export function validarData(valor: string, campo: string): string {
  const s = String(valor ?? "").trim();
  if (!FORMATO.test(s)) {
    throw new Error(`${campo} deve estar no formato YYYY-MM-DD (recebi "${valor}").`);
  }
  const d = new Date(`${s}T00:00:00Z`);
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== s) {
    throw new Error(`${campo} "${s}" nao e uma data valida do calendario.`);
  }
  return s;
}

const paraMs = (s: string) => new Date(`${s}T00:00:00Z`).getTime();

/** Dias corridos entre as duas pontas, inclusive (01 a 02 = 2 dias). */
export function diasNoPeriodo(inicio: string, fim: string): number {
  return Math.round((paraMs(fim) - paraMs(inicio)) / DIA_MS) + 1;
}

export function somarDias(data: string, dias: number): string {
  return new Date(paraMs(data) + dias * DIA_MS).toISOString().slice(0, 10);
}

/**
 * Quebra um periodo grande em fatias que cabem no limite da rota.
 * Usado pela conciliacao e por quem pedir explicitamente o periodo inteiro.
 */
export function fatiar(inicio: string, fim: string, maxDias: number): Array<{ inicio: string; fim: string }> {
  const fatias: Array<{ inicio: string; fim: string }> = [];
  let de = inicio;
  while (paraMs(de) <= paraMs(fim)) {
    const ate = somarDias(de, maxDias - 1);
    fatias.push({ inicio: de, fim: paraMs(ate) > paraMs(fim) ? fim : ate });
    de = somarDias(de, maxDias);
  }
  return fatias;
}

export interface Janela {
  inicio: string;
  fim: string;
}

/**
 * Valida as duas datas e, se a rota tiver limite, o tamanho da janela.
 * `maxDias` undefined = rota sem limite documentado.
 */
export function validarJanela(
  inicio: string,
  fim: string,
  maxDias?: number,
  rota = "esta consulta"
): Janela {
  const i = validarData(inicio, "data_inicio");
  const f = validarData(fim, "data_fim");
  if (paraMs(f) < paraMs(i)) {
    throw new Error(`data_fim (${f}) e anterior a data_inicio (${i}).`);
  }
  if (maxDias) {
    const dias = diasNoPeriodo(i, f);
    if (dias > maxDias) {
      const fatias = fatiar(i, f, maxDias);
      const exemplo = fatias.slice(0, 3).map((x) => `${x.inicio} a ${x.fim}`).join(" | ");
      throw new Error(
        `${rota} aceita no maximo ${maxDias} dias por chamada e voce pediu ${dias} (${i} a ${f}). ` +
          `Divida em ${fatias.length} consultas: ${exemplo}${fatias.length > 3 ? " | ..." : ""}`
      );
    }
  }
  return { inicio: i, fim: f };
}

/** Limite de cada rota, em um lugar so — usado pelas tools e documentado nas skills. */
export const LIMITE: Record<string, number | undefined> = {
  vendas: 62,
  vendas_resumo: 62,
  vendas_por_nsu: 62,
  vendas_parceladas: 30,
  pagamentos: 30,
  pagamentos_diario: undefined,
  pagamentos_resumo: undefined,
  ordens_de_credito: 30,
  bloqueios: undefined,
  recebiveis_resumo_v1: 30,
  recebiveis_resumo_v2: undefined,
  recebiveis_resumo_v3: undefined,
  recebiveis_calendario: 60,
  recebiveis_diario: undefined,
  recebiveis_parcelas: undefined,
  debitos: 30,
  debitos_resumo: 30,
};
