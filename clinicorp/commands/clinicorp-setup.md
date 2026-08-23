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
4. Precisa tambem do **subscriber_id** da conta. Se a pessoa nao souber qual e, oriente a
   perguntar a quem administra a conta Clinicorp da clinica.

Se a pessoa nao encontrar a secao, o mais provavel e que o usuario dela nao tenha permissao de
administrador — nesse caso quem administra a conta precisa gerar o acesso.

## Passo 3 — criar o arquivo (sem o token passar pelo chat)

Crie `~/.clinicorp-mcp.json` com **placeholders**, nao com valores reais:

```json
[
  {
    "nome": "Matriz",
    "subscriber_id": "COLE_AQUI",
    "username": "COLE_AQUI",
    "token": "COLE_AQUI"
  }
]
```

Aplique `chmod 600` no arquivo.

Depois peca para a pessoa **abrir o arquivo no editor dela** e substituir os tres `COLE_AQUI`
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

## Ao terminar

Confirme o que ficou disponivel: consultas de faturamento, orcamentos, agenda, ocupacao,
pagamentos e inadimplencia — tudo **somente leitura**, nada e alterado no Clinicorp.
Avise tambem que o arquivo de credenciais e local: nao vai para o GitHub nem e compartilhado.
