---
name: conta-azul-setup
description: Configura o acesso a Conta Azul nesta maquina — credenciais do app (client_id, client_secret, redirect_uri) sem segredo no chat — e conecta a empresa via OAuth. Use quando a pessoa pedir para configurar, instalar, conectar ou reconectar a Conta Azul, perguntar onde colocar as credenciais, ou quando qualquer tool contaazul_* falhar por falta de configuracao, token revogado, invalid_grant ou invalid_refresh_token.
---

Guie a pessoa na configuracao do acesso a **API v2 da Conta Azul** nesta maquina.

## Regras que nao podem ser quebradas

1. **Nunca peca para colar client_secret, access_token ou refresh_token no chat.** Eles ficam
   gravados no historico da conversa. O client_secret vai do Portal direto para o arquivo local.
2. **Nunca imprima o conteudo de `~/.conta-azul-mcp.json` nem da pasta `~/.conta-azul-mcp/`.**
3. O unico dado de autorizacao que pode passar pelo chat e a **URL de retorno com o `code`**:
   ele vale 3 minutos, uso unico, e nao serve para nada sem o client_secret que esta no computador.

## Passo 1 — o que ja existe

Rode `contaazul_status`.
- `configurado: true` e empresa `conectada: true` → rode `contaazul_empresa` para provar que funciona,
  diga o nome da empresa conectada e pare.
- `configurado: true` mas `conectada: false` → pule para o Passo 4.
- Senao, siga.

## Passo 2 — onde estao as credenciais

No **Portal do Desenvolvedor** (https://developers-portal.contaazul.com) → **Minhas aplicacoes** →
a aplicacao de **Producao**:
- **Client ID** e **Client Secret**
- **URL de redirecionamento** cadastrada — o `redirect_uri` precisa ser **identico, byte a byte**
  (inclusive barra final e http/https). Se a aplicacao for de Desenvolvimento, ela usa
  `https://www.contaazul.com` e so enxerga dados ficticios — para a Beauty Smile real precisa ser a de Producao.

Se a pessoa puder cadastrar a URL de redirecionamento, sugira `http://localhost:8765/callback`:
com ela a conexao conclui sozinha, sem copiar URL. Se o Portal nao aceitar localhost, use a que ja existe.

## Passo 3 — criar o arquivo (sem segredo no chat)

Crie `~/.conta-azul-mcp.json` com placeholders e `chmod 600`:

```json
{
  "escrita": false,
  "client_id": "COLE_AQUI",
  "client_secret": "COLE_AQUI",
  "redirect_uri": "COLE_AQUI",
  "empresas": [ { "nome": "Beauty Smile" } ]
}
```

Peca para a pessoa abrir o arquivo no editor, trocar os `COLE_AQUI` e salvar. Diga o caminho completo.
Depois rode `contaazul_status` e confirme `configurado: true` (a config e relida a cada chamada — nao
precisa reiniciar).

## Passo 4 — conectar a empresa

1. Rode `contaazul_conectar` e entregue o link.
2. Avise: entrar com o **login do ERP Conta Azul** (o mesmo do dia a dia), **nao** o do Portal do Desenvolvedor,
   e autorizar.
3. Modo automatico (localhost): espere a pessoa dizer que autorizou e rode `contaazul_status`.
   Modo manual: a pessoa copia a URL inteira da barra de endereco (tem `?code=...&state=...`) e envia;
   chame `contaazul_concluir_conexao` **na hora** — o codigo morre em 3 minutos.

## Passo 5 — validar

Rode `contaazul_empresa` (deve trazer a razao social certa) e `contaazul_resumo_financeiro` do mes atual.

Erros comuns, na ordem:
- `invalid_grant` na troca do codigo → passou de 3 minutos, codigo reutilizado, ou `redirect_uri` diferente do Portal.
- `invalid_client` → client_id/secret com espaco sobrando ou trocados.
- Razao social errada → a pessoa logou numa empresa diferente; conecte de novo.

## Ao terminar

Diga que a escrita ficou **desligada** e que a conexao renova sozinha (o refresh token dura ate 5 anos
enquanto for usado). Se um dia aparecer `invalid_refresh_token` ou `access_revoked`, basta rodar
`contaazul_conectar` de novo.
