/**
 * Servidor MCP da Conta Azul (API v2) — roda localmente via stdio.
 *
 * Leitura sempre disponivel. Escrita desligada por padrao e, quando ligada, em dois passos
 * (previa -> confirmar=true). Ver escrita.ts e tools-escrita.ts.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer, type Server } from "node:http";
import { z } from "zod";

import { carregarConfig, resolverEmpresa, CONFIG_FILE, STATE_DIR } from "./config.js";
import { lerTokens, novaAutorizacao, consumirState, extrairCode, trocarCode, gravarTokens } from "./auth.js";
import { api } from "./client.js";
import { contexto, seguro } from "./ctx.js";
import { escritaLigada } from "./escrita.js";
import { registrarLeitura } from "./tools-leitura.js";
import { registrarEscrita } from "./tools-escrita.js";

const VERSAO = "0.1.0";

const server = new McpServer(
  { name: "conta-azul", version: VERSAO },
  {
    instructions:
      "Acesso a API v2 do ERP Conta Azul. Comece por contaazul_status se houver qualquer duvida de conexao. " +
      "Datas SEMPRE YYYY-MM-DD. Para visao geral de um periodo use contaazul_resumo_financeiro; para listas, " +
      "contaazul_contas_receber / contaazul_contas_pagar (filtram por VENCIMENTO). Ids (UUID) de pessoas, contas, " +
      "categorias e centros de custo saem das tools de listagem — nunca invente um id. " +
      "Tools marcadas ESCRITA alteram dados reais: primeiro chame com confirmar=false, mostre a previa a pessoa e " +
      "so repita com confirmar=true depois do ok explicito dela. Nunca repita uma escrita que falhou por rede sem " +
      "antes conferir se ela foi aplicada. Endpoints sem tool dedicada: contaazul_get.",
  }
);

// ================================================================ conexao
server.registerTool(
  "contaazul_status",
  {
    title: "Status da configuracao e da conexao",
    description:
      "Mostra se o arquivo de configuracao esta ok, quais empresas estao configuradas, quais ja foram conectadas " +
      "(e ate quando o token vale), e se a escrita esta ligada. Nao expoe segredos.",
    inputSchema: {},
  },
  seguro(async () => {
    let cfg;
    try {
      cfg = carregarConfig();
    } catch (e) {
      return { configurado: false, problema: (e as Error).message, arquivo: CONFIG_FILE };
    }
    return {
      configurado: true,
      arquivo: CONFIG_FILE,
      redirect_uri: cfg.redirectUri,
      escrita: escritaLigada() ? "LIGADA (com previa + confirmar=true)" : "DESLIGADA",
      empresas: cfg.empresas.map((e) => {
        const t = lerTokens(e);
        return {
          nome: e.nome,
          conectada: !!t,
          empresa_na_conta_azul: t?.empresa_conectada ?? null,
          access_token_valido_ate: t ? new Date(t.expira_em).toISOString() : null,
          ultima_renovacao: t?.atualizado_em ?? null,
          obs: t ? "O token renova sozinho; o refresh_token vale ate 5 anos enquanto for usado." : "Rode contaazul_conectar.",
        };
      }),
      versao_servidor: VERSAO,
    };
  })
);

let ouvinte: Server | null = null;

server.registerTool(
  "contaazul_conectar",
  {
    title: "Conectar (autorizar) uma empresa",
    description:
      "Gera o link de autorizacao OAuth da Conta Azul. A pessoa abre o link, entra com o login do ERP (nao o do Portal " +
      "do Desenvolvedor) e autoriza. Se o redirect_uri configurado for http://localhost:PORTA, a conexao conclui sozinha; " +
      "senao, a pessoa copia a URL da barra de endereco apos o redirecionamento e voce chama contaazul_concluir_conexao " +
      "com ela — em ate 3 minutos (validade do codigo).",
    inputSchema: { empresa: z.string().optional() },
  },
  seguro(async (a: { empresa?: string }) => {
    const cfg = carregarConfig();
    const emp = resolverEmpresa(cfg, a.empresa);
    const { url, state } = novaAutorizacao(cfg, emp);

    const redir = new URL(cfg.redirectUri);
    const local = redir.protocol === "http:" && ["localhost", "127.0.0.1"].includes(redir.hostname);
    if (local) {
      ouvinte?.close();
      const porta = Number(redir.port || 80);
      ouvinte = createServer(async (req, res) => {
        const u = new URL(req.url ?? "/", cfg.redirectUri);
        if (u.pathname !== redir.pathname || !u.searchParams.get("code")) {
          res.writeHead(404).end();
          return;
        }
        let msg: string;
        try {
          if (consumirState(u.searchParams.get("state") ?? "") !== emp.slug) throw new Error("state invalido (possivel CSRF) — gere um link novo.");
          await trocarCode(cfg, emp, u.searchParams.get("code")!);
          await registrarEmpresaConectada(emp.nome);
          msg = `Conta Azul conectada (${emp.nome}). Pode fechar esta aba e voltar ao Claude.`;
        } catch (e) {
          msg = `Falhou: ${(e as Error).message}`;
        }
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }).end(`<p style="font-family:sans-serif">${msg}</p>`);
        ouvinte?.close();
        ouvinte = null;
      });
      ouvinte.listen(porta, redir.hostname);
      setTimeout(() => { ouvinte?.close(); ouvinte = null; }, 10 * 60 * 1000).unref();
    }

    return {
      empresa: emp.nome,
      link_de_autorizacao: url,
      modo: local ? "automatico (ouvindo o retorno por 10 minutos)" : "manual",
      instrucoes: local
        ? "Abra o link, entre com o login do ERP Conta Azul e autorize. A conexao conclui sozinha; depois rode contaazul_status."
        : "Abra o link, entre com o login do ERP Conta Azul e autorize. O navegador vai para " +
          `${cfg.redirectUri}?code=...&state=... — copie a URL inteira da barra de endereco e me envie em ate 3 minutos. ` +
          "O codigo e de uso unico e so funciona junto com o client_secret que esta no seu computador.",
      state,
    };
  })
);

async function registrarEmpresaConectada(nome: string) {
  const { cfg, emp } = contexto(nome);
  try {
    const info = (await api(cfg, emp, { caminho: "/v1/pessoas/conta-conectada" })) as Record<string, string>;
    const t = lerTokens(emp);
    if (t) {
      t.empresa_conectada = { id_empresa: info?.id_empresa, razao_social: info?.razao_social ?? info?.nome_fantasia, documento: info?.documento };
      gravarTokens(emp, t);
    }
    return info;
  } catch (e) {
    return { aviso: `Tokens salvos, mas a consulta de teste falhou: ${(e as Error).message}` };
  }
}

server.registerTool(
  "contaazul_concluir_conexao",
  {
    title: "Concluir conexao com o codigo recebido",
    description:
      "Recebe a URL para onde a Conta Azul redirecionou (ou so o code) e troca pelos tokens, gravando-os localmente. " +
      "Use logo apos a pessoa autorizar — o codigo expira em 3 minutos e so vale uma vez.",
    inputSchema: {
      url_ou_codigo: z.string().describe("URL completa da barra de endereco apos autorizar, ou o valor de code"),
      empresa: z.string().optional(),
    },
  },
  seguro(async (a: { url_ou_codigo: string; empresa?: string }) => {
    const cfg = carregarConfig();
    const { code, state } = extrairCode(a.url_ou_codigo);
    let slugDoState: string | null = null;
    if (state) {
      slugDoState = consumirState(state);
      if (!slugDoState) {
        throw new Error("Esse link de autorizacao nao foi gerado por este computador ou ja foi usado (state desconhecido). Rode contaazul_conectar de novo.");
      }
    }
    const emp = (slugDoState && cfg.empresas.find((e) => e.slug === slugDoState)) || resolverEmpresa(cfg, a.empresa);
    await trocarCode(cfg, emp, code);
    const info = await registrarEmpresaConectada(emp.nome);
    return {
      conectado: true,
      empresa_configurada: emp.nome,
      empresa_na_conta_azul: info,
      tokens_em: `${STATE_DIR}/tokens/ (permissao 600, fora do chat)`,
      proximo_passo: "Teste com contaazul_resumo_financeiro do mes atual.",
    };
  })
);

registrarLeitura(server);
registrarEscrita(server);

const transport = new StdioServerTransport();
await server.connect(transport);

let resumo = "sem configuracao";
try {
  const cfg = carregarConfig();
  resumo = `${cfg.empresas.length} empresa(s): ${cfg.empresas.map((e) => `${e.nome}${lerTokens(e) ? "" : " (nao conectada)"}`).join(", ")}`;
} catch (e) {
  resumo = (e as Error).message;
}
console.error(`conta-azul-mcp ${VERSAO} pronto — ${resumo} | escrita: ${escritaLigada() ? "LIGADA" : "desligada"}`);
