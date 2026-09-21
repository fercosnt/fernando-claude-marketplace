import { carregarConfig, resolverPv, type Config, type Pv } from "./config.js";

export type Conteudo = { content: Array<{ type: "text"; text: string }>; isError?: boolean };

export function texto(valor: unknown): Conteudo {
  return {
    content: [{ type: "text", text: typeof valor === "string" ? valor : JSON.stringify(valor, null, 2) }],
  };
}

export function erro(e: unknown): Conteudo {
  return { isError: true, content: [{ type: "text", text: `Erro: ${(e as Error).message}` }] };
}

/** Rele a config a cada chamada: editar o arquivo nao exige reiniciar o servidor. */
export function contexto(pv?: string): { cfg: Config; pv: Pv } {
  const cfg = carregarConfig();
  return { cfg, pv: resolverPv(cfg, pv) };
}

/** Para as poucas rotas que nao precisam de PV nenhum (ex.: tabela de tipos de ajuste). */
export function apenasConfig(): Config {
  return carregarConfig();
}

/** Envolve o handler para sempre devolver erro legivel em vez de derrubar a chamada. */
export function seguro<A>(fn: (a: A) => Promise<unknown>) {
  return async (a: A): Promise<Conteudo> => {
    try {
      return texto(await fn(a));
    } catch (e) {
      return erro(e);
    }
  };
}
