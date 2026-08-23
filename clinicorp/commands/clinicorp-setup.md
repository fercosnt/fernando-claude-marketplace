---
description: Configura as credenciais pessoais de acesso ao Clinicorp
---

Guie a pessoa na configuracao das **credenciais dela** de acesso a API do Clinicorp.
Cada pessoa usa usuario e token proprios — nunca um token compartilhado.

## Regra que nao pode ser quebrada

**Nunca peca para a pessoa colar o token no chat.** O token da acesso a dado de paciente e
ficaria gravado no historico da conversa. O fluxo abaixo existe justamente para o token ir do
Clinicorp direto para o arquivo local, sem passar pela conversa.

## Passo 1 — verificar o que ja existe

Cheque se `~/.clinicorp-mcp.json` ja existe. Se existir, rode a tool `clinicorp_clinicas`:
se ela listar as clinicas, esta tudo certo — diga isso e pare. Se der erro de credencial,
siga para o passo 2 avisando que vai substituir o conteudo.

## Passo 2 — onde a pessoa pega usuario e token

Instrua, nessa ordem:

1. Entrar no Clinicorp pelo navegador.
2. **Gerenciar Assinatura** -> **Acesso Externo e Integracoes** -> secao **Integracoes**.
3. Ali estao **Usuario API** e **Token API**.
4. O **subscriber_id** e opcional — nao mande a pessoa procurar. O servidor descobre sozinho na
   primeira chamada. So sera necessario se a conta for de grupo com mais de um assinante, e nesse
   caso o proprio erro lista as opcoes (ou rode `clinicorp_assinantes`).

Se a pessoa nao encontrar a secao, o mais provavel e que o usuario dela nao tenha permissao de
administrador — nesse caso quem administra a conta precisa gerar o acesso.

## Passo 3 — criar o arquivo (sem o token passar pelo chat)

Crie `~/.clinicorp-mcp.json` com **placeholders**, nao com valores reais:

```json
[
  {
    "nome": "Matriz",
    "username": "COLE_AQUI",
    "token": "COLE_AQUI"
  }
]
```

Aplique `chmod 600` no arquivo.

Depois peca para a pessoa **abrir o arquivo no editor dela** e substituir os `COLE_AQUI`
pelos valores reais, salvando em seguida. Diga o caminho completo do arquivo.

Se a pessoa tem acesso a mais de uma clinica, explique que basta repetir o bloco dentro do
array, um por clinica, cada um com seu `nome` — e esse `nome` que ela vai usar nas perguntas
("como foi o mes na Matriz?").

## Passo 4 — validar

Depois que a pessoa confirmar que salvou:

1. Rode `clinicorp_clinicas` e confirme que as clinicas aparecem.
2. Rode uma consulta real e barata para provar que a credencial funciona de ponta a ponta —
   `clinicorp_unidades` serve bem.
3. Se der erro de acesso negado, os suspeitos, nessa ordem: token ou usuario copiados com
   espaco sobrando, `subscriber_id` errado, ou conta de grupo/franquia em que o
   `subscriber_id` precisa ser o da unidade especifica, nao o da rede.

Se o servidor MCP nao aparecer, lembre que o Claude Code precisa ser reiniciado depois de
instalar o plugin.

## Passo 5 — escrita (so se a pessoa pedir)

Por padrao o acesso e somente leitura. Se — e apenas se — a pessoa pedir para tambem agendar,
confirmar, cancelar ou cadastrar pelo Claude, explique que isso altera a base real da clinica e,
com o ok dela, troque o arquivo para a forma com objeto:

```json
{
  "escrita": true,
  "clinicas": [ ...os mesmos blocos de antes... ]
}
```

Reinicie o cliente depois. Quem so consulta nao precisa disso e nao deve ligar.

## Ao terminar

Confirme o que ficou disponivel: consultas de faturamento, orcamentos, agenda, ocupacao,
pagamentos e inadimplencia. Diga tambem se a escrita ficou ligada ou nao — e, se ficou, que toda
alteracao sera confirmada com ela antes de acontecer.
Avise tambem que o arquivo de credenciais e local: nao vai para o GitHub nem e compartilhado.
