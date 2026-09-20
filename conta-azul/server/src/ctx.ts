import { carregarConfig, resolverEmpresa, type Config, type Empresa } from "./config.js";

export type Conteudo = { content: Array<{ type: "text"; text: string }>; isError?: boolean };

export function texto(valor: unknown): Conteudo {
  return {
    content: [{ type: "text", text: typeof valor === "string" ? valor : JSON.stringify(valor, null, 2) }],
  };
}

export function erro(e: unknown): Conteudo {
  return { isError: true, content: [{ type: "text", text: `Erro: ${(e as Error).message}` }] };
}

/** Rele a config a cada chamada: editar o arquivo nao exige reiniciar (exceto a flag escrita, ver escrita.ts). */
export function contexto(empresa?: string): { cfg: Config; emp: Empresa } {
  const cfg = carregarConfig();
  return { cfg, emp: resolverEmpresa(cfg, empresa) };
}

/** Envolve o handler para sempre devolver erro legivel em vez de derrubar a chamada. */
export function seguro<A>(fn: (a: A) => Promise<unknown>) {
  return async (a: A): Promise<Conteudo> => {
    try {
      const r = await fn(a);
      return texto(r);
    } catch (e) {
      return erro(e);
    }
  };
}
