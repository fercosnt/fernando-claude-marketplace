/** Parametros que se repetem em quase toda tool, definidos uma vez so. */
import { z } from "zod";
import { codigoBandeira, nomeModalidade } from "./dominios.js";

export const pPv = z
  .string()
  .optional()
  .describe("Apelido ou numero do Ponto de Venda. Opcional se houver so um configurado.");

export const pInicio = z.string().describe("Data inicial — YYYY-MM-DD");
export const pFim = z.string().describe("Data final — YYYY-MM-DD");

export const pBandeiras = z
  .array(z.union([z.string(), z.number()]))
  .optional()
  .describe(
    "Bandeiras: codigo ou nome (ex.: [1] ou ['Mastercard','Elo']). Nas rotas detalhadas a Rede " +
      "documenta uma bandeira por chamada; se vierem varias e a API recusar, repita uma a uma."
  );

export const pTamanho = z
  .number()
  .int()
  .positive()
  .max(100)
  .optional()
  .describe("Itens por pagina (limite 100 na Rede).");

export const pPageKey = z
  .string()
  .optional()
  .describe("Chave da proxima pagina (cursor.nextKey da resposta anterior).");

export const pTudo = z
  .boolean()
  .optional()
  .describe("true = segue a paginacao ate o fim (teto de 20 paginas) e devolve a lista ja unida.");

/** Converte a lista de bandeiras para a string separada por virgula que a Rede espera. */
export const bandeiras = (v?: Array<string | number>) =>
  v?.length ? v.map(codigoBandeira).join(",") : undefined;

export const modalidade = (v?: string) => (v ? nomeModalidade(v) : undefined);

/** Resumo padrao de paginacao, igual em todas as tools. */
export function resumoPaginacao(r: { completo: boolean; total_paginas: number; proximo_page_key?: string }) {
  return {
    paginas_lidas: r.total_paginas,
    completo: r.completo,
    ...(r.completo
      ? {}
      : {
          aviso: "Parei no teto de paginas. Passe o page_key abaixo para continuar de onde parou.",
          proximo_page_key: r.proximo_page_key,
        }),
  };
}
