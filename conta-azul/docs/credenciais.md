# Onde ficam as credenciais

Tudo fica **no seu computador**. Nada vai para o repositório, para o chat ou para servidor de terceiros.

| Arquivo | Quem escreve | O que tem |
|---|---|---|
| `~/.conta-azul-mcp.json` | **Você** (uma vez) | `client_id`, `client_secret`, `redirect_uri`, lista de empresas, chave `escrita` |
| `~/.conta-azul-mcp/tokens/<empresa>.json` | **O servidor** (sozinho) | `access_token` e `refresh_token`. Renova a cada hora; não edite |
| `~/.conta-azul-mcp/autorizacoes-pendentes.json` | O servidor | `state` dos links de autorização abertos (proteção CSRF), apagados ao usar |

`~` é a sua pasta de usuário: no Mac, `/Users/fernando/.conta-azul-mcp.json`. O arquivo começa com ponto, então fica
oculto no Finder (`Cmd + Shift + .` mostra).

## Passo a passo

1. No **Portal do Desenvolvedor** (https://developers-portal.contaazul.com) → **Minhas aplicações** → aplicação de
   **Produção**, copie **Client ID**, **Client Secret** e a **URL de redirecionamento** cadastrada.
   A aplicação de Desenvolvimento só enxerga dados fictícios.
2. Crie `~/.conta-azul-mcp.json` (ou peça ao Claude: `/conta-azul-setup`, que cria o arquivo com `COLE_AQUI`):

   ```json
   {
     "escrita": false,
     "client_id": "cole aqui o Client ID",
     "client_secret": "cole aqui o Client Secret",
     "redirect_uri": "exatamente a URL cadastrada no Portal",
     "empresas": [ { "nome": "Beauty Smile" } ]
   }
   ```

3. Proteja o arquivo: `chmod 600 ~/.conta-azul-mcp.json`
4. No Claude: "conecta a Conta Azul". Ele gera o link; você entra com o **login do ERP** (não o do Portal) e autoriza.
   - Se o `redirect_uri` for `http://localhost:8765/callback` (e o Portal aceitar), a conexão termina sozinha.
   - Senão, copie a URL da barra de endereço depois de autorizar (tem `?code=...`) e cole no chat **em até 3 minutos**.
     O código é de uso único e inútil sem o `client_secret`, que não sai do seu computador.
5. Confira: "qual empresa está conectada na Conta Azul?"

## Regras

- `redirect_uri` precisa ser **idêntico, caractere por caractere**, ao cadastrado no Portal (barra final, http/https).
- Nunca cole `client_secret` ou tokens no chat.
- Mais de uma empresa: acrescente `{ "nome": "..." }` em `empresas` e conecte cada uma. As tools passam a pedir o
  parâmetro `empresa`.
- Trocou de computador (MacBook Air ↔ Mac Mini): copie `~/.conta-azul-mcp.json` e **reconecte** na máquina nova.
  Não copie a pasta de tokens entre máquinas: duas máquinas renovando o mesmo `refresh_token` quebram a conexão
  das duas (o token é rotativo).
- Deu `invalid_refresh_token` ou `access_revoked`? É só reconectar.

## Escrita

Desligada por padrão. Para ligar: `/conta-azul-escrita` (ou `"escrita": true` no arquivo) e **reinicie o Claude**.
Mesmo ligada, cada alteração mostra uma prévia e só é enviada depois do seu "pode".
