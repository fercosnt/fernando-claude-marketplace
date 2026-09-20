/**
 * Trava de escrita. DESLIGADA por padrao.
 *
 * Liga com "escrita": true em ~/.conta-azul-mcp.json (ou CONTAAZUL_ESCRITA=X).
 * O estado e lido UMA vez, quando o servidor sobe: ligar exige reiniciar o cliente de proposito,
 * para que uma edicao acidental do arquivo no meio da conversa nao libere escrita.
 */
import { carregarConfig } from "./config.js";

let ligadaNoBoot = false;
try {
  ligadaNoBoot = carregarConfig().escrita;
} catch {
  ligadaNoBoot = String(process.env.CONTAAZUL_ESCRITA ?? "").toUpperCase() === "X";
}

export const escritaLigada = () => ligadaNoBoot;

export function exigirEscrita(operacao: string): void {
  if (!ligadaNoBoot) {
    throw new Error(
      `"${operacao}" altera dados reais na Conta Azul e a escrita esta DESLIGADA. ` +
        `Para ligar, rode /conta-azul-escrita (ou ponha "escrita": true em ~/.conta-azul-mcp.json) e reinicie o cliente. ` +
        `Enquanto isso, so leitura.`
    );
  }
}
