/**
 * Servidor MCP das APIs de Gestao de Vendas da Rede — roda localmente via stdio.
 *
 * A API da Rede e somente leitura: nao existe rota que altere dado do estabelecimento.
 * Por isso este servidor nao tem camada de escrita nem confirmacao em dois passos.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { BASES, carregarConfig, CONFIG_FILE, STATE_DIR } from "./config.js";
import { esquecerTokens, lerTokens, login } from "./auth.js";
import { api } from "./client.js";
import { seguro } from "./ctx.js";
import { registrarVendas } from "./tools-vendas.js";
import { registrarPagamentos } from "./tools-pagamentos.js";
import { registrarRecebiveis } from "./tools-recebiveis.js";
import { registrarDebitos } from "./tools-debitos.js";
import { registrarConciliacao } from "./tools-conciliacao.js";

const VERSAO = "0.1.2";

const server = new McpServer(
  { name: "rede", version: VERSAO },
  {
    instructions:
      "Acesso as APIs de Gestao de Vendas da Rede (adquirente de cartao). Tudo aqui e LEITURA — a API nao " +
      "altera nada. Comece por rede_status se houver duvida de conexao. Datas SEMPRE YYYY-MM-DD. " +
      "Entenda a diferenca antes de escolher a tool: VENDA e valor bruto na data da compra (rede_vendas); " +
      "PAGAMENTO e o deposito liquido, ja com MDR e debitos descontados, na data do repasse (rede_pagamentos); " +
      "RECEBIVEL e o que ainda vai cair (rede_recebiveis_resumo). Debito cai em D+1 e credito em D+30, entao " +
      "venda e pagamento quase nunca estao no mesmo periodo. Para ligar os dois use rede_conciliar, que cruza " +
      "pelo saleSummaryNumber via ordens de credito. Cada rota tem limite de janela (62, 60 ou 30 dias) e as " +
      "tools validam isso antes de chamar. Os codigos (bandeira, status, produto) ja vem traduzidos na resposta; " +
      "a tabela completa esta em rede_dominios. Endpoints sem tool dedicada: rede_get.",
  }
);

// ================================================================ conexao
server.registerTool(
  "rede_status",
  {
    title: "Status da configuracao e da conexao",
    description:
      "Mostra se o arquivo de configuracao esta ok, em qual ambiente (sandbox ou producao) o plugin esta, " +
      "quais PVs estao configurados e ate quando o token atual vale. Nao expoe segredos.",
    inputSchema: {},
  },
  seguro(async () => {
    let cfg;
    try {
      cfg = carregarConfig();
    } catch (e) {
      return { configurado: false, problema: (e as Error).message, arquivo: CONFIG_FILE };
    }
    const t = lerTokens(cfg.ambiente);
    const agora = Date.now();
    return {
      configurado: true,
      arquivo: CONFIG_FILE,
      ambiente: cfg.ambiente,
      base_da_api: BASES[cfg.ambiente].api,
      ...(cfg.baseNsu ? { base_vendas_por_nsu: cfg.baseNsu } : {}),
      grant: cfg.grant,
      ...(cfg.usuario ? { usuario: cfg.usuario } : {}),
      client_id_final: `...${cfg.clientId.slice(-6)}`,
      pvs: cfg.pvs.map((p) => `${p.nome} (${p.numero})`),
      conexao: t
        ? {
            conectado: true,
            access_token_valido_ate: new Date(t.expira_em).toISOString(),
            access_token_expirado: t.expira_em <= agora,
            refresh_token_nasceu_em: new Date(t.refresh_desde).toISOString(),
            refresh_token_expira_em: new Date(t.refresh_desde + 24 * 3600 * 1000).toISOString(),
            obtido_por: t.origem,
            escopo: t.escopo ?? null,
            obs: "O token renova sozinho. Quando o refresh de 24h vence, o login e refeito automaticamente.",
          }
        : { conectado: false, obs: "Nenhum token gravado ainda — a primeira consulta faz o login sozinha. Para testar agora, rode rede_conectar." },
      tokens_em: `${STATE_DIR}/tokens/ (permissao 600, fora do chat)`,
      versao_servidor: VERSAO,
    };
  })
);

server.registerTool(
  "rede_conectar",
  {
    title: "Testar as credenciais e conectar",
    description:
      "Faz o login na Rede com as credenciais do arquivo de configuracao e confirma com uma consulta real " +
      "(a tabela de tipos de ajuste). Mostra o ESCOPO do token — e ele que denuncia projeto criado no pacote " +
      "errado no Portal da Rede. Use depois de preencher ou trocar credenciais. Nao e obrigatorio no dia a " +
      "dia: qualquer tool ja faz o login quando precisa.",
    inputSchema: {
      recomecar: z
        .boolean()
        .optional()
        .describe("true = descarta o token gravado antes de logar (use se desconfiar do token em disco)."),
    },
  },
  seguro(async (a: { recomecar?: boolean }) => {
    const cfg = carregarConfig();
    if (a.recomecar) esquecerTokens(cfg.ambiente);
    const t = await login(cfg);

    let teste: unknown;
    try {
      const r = (await api(cfg, { caminho: "/merchant-statement/v1/charges/adjustment-types" })) as unknown[];
      teste = Array.isArray(r)
        ? { ok: true, rota: "/merchant-statement/v1/charges/adjustment-types", tipos_de_ajuste_retornados: r.length }
        : { ok: true, rota: "/merchant-statement/v1/charges/adjustment-types", resposta: r };
    } catch (e) {
      teste = {
        ok: false,
        aviso:
          `O login funcionou, mas a consulta de teste falhou: ${(e as Error).message} ` +
          `Token valido + consulta recusada costuma ser falta de liberacao do PV para este usuario na Rede.`,
      };
    }

    const escopoOk = !t.escopo || /merchant-statement/i.test(t.escopo);
    return {
      conectado: true,
      ambiente: cfg.ambiente,
      grant: cfg.grant,
      access_token_valido_ate: new Date(t.expira_em).toISOString(),
      refresh_token_expira_em: new Date(t.refresh_desde + 24 * 3600 * 1000).toISOString(),
      escopo: t.escopo ?? null,
      ...(escopoOk
        ? {}
        : {
            ALERTA:
              `O token veio com escopo "${t.escopo}", sem "merchant-statement". Este projeto do Portal da Rede ` +
              `nao e do pacote "APIs de Conciliacao" — provavelmente e de Payment Link. O login funciona, mas ` +
              `toda rota de extrato vai responder 401. Crie um projeto no pacote certo em "Meus Projetos".`,
          }),
      consulta_de_teste: teste,
      proximo_passo: `Experimente rede_vendas com um periodo curto em um dos PVs: ${cfg.pvs.map((p) => p.numero).join(", ")}.`,
    };
  })
);

registrarVendas(server);
registrarPagamentos(server);
registrarRecebiveis(server);
registrarDebitos(server);
registrarConciliacao(server);

const transport = new StdioServerTransport();
await server.connect(transport);

let resumo: string;
try {
  const cfg = carregarConfig();
  const t = lerTokens(cfg.ambiente);
  resumo = `${cfg.ambiente} | ${cfg.pvs.length} PV(s): ${cfg.pvs.map((p) => p.numero).join(", ")} | ${t ? "token em disco" : "sem token (loga na primeira consulta)"}`;
} catch (e) {
  resumo = (e as Error).message;
}
console.error(`rede-mcp ${VERSAO} pronto — ${resumo}`);
