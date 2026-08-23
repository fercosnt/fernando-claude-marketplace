---
description: Liga ou desliga as tools que alteram dados no Clinicorp
---

Liga ou desliga a escrita no Clinicorp para esta maquina, editando `~/.clinicorp-mcp.json`
com seguranca. A pessoa nao precisa mexer em JSON na mao.

## Regras que nao podem ser quebradas

1. **Nunca imprima o conteudo do arquivo**, nem em trecho, nem em diff. Ele contem tokens de
   acesso a dado de paciente. Fale sobre o arquivo, nao mostre o arquivo.
2. **Nunca ligue a escrita sem a pessoa pedir explicitamente nesta conversa.** Se ela rodou o
   comando so para consultar o estado, informe e pare.
3. **Faca backup antes de escrever** e restaure se a validacao falhar. Perder as credenciais
   significa a pessoa ter que buscar tudo de novo no Clinicorp.

## Passo 1 — ler o estado atual

Leia `~/.clinicorp-mcp.json`. Se nao existir, a configuracao ainda nao foi feita: aponte
`/clinicorp-setup` e pare.

O arquivo tem dois formatos possiveis:

- **Lista** `[ {...}, {...} ]` — escrita DESLIGADA
- **Objeto** `{ "escrita": true|false, "clinicas": [ {...} ] }` — escrita conforme o campo

Diga a pessoa em uma frase qual e o estado atual e quantas clinicas estao configuradas
(numero e nomes, nunca credenciais).

## Passo 2 — confirmar a intencao

Se a pessoa nao deixou claro se quer ligar ou desligar, pergunte. Ao **ligar**, diga antes o que
isso passa a permitir: agendar, confirmar, cancelar, cadastrar paciente, lead no CRM, anexo e
ordem de compra — alteracoes reais na base da clinica, sem desfazer pela API.

Se o estado desejado ja for o atual, diga isso e pare. Nao reescreva o arquivo a toa.

## Passo 3 — aplicar

1. Copie o arquivo para `~/.clinicorp-mcp.json.bak`.
2. Carregue o JSON, converta preservando **todos** os campos de cada clinica:
   - ligando: `{ "escrita": true, "clinicas": [ ...os mesmos blocos... ] }`
   - desligando: mantenha o objeto e troque para `"escrita": false`
3. Escreva o arquivo com indentacao de 2 espacos e aplique `chmod 600`.

## Passo 4 — validar (obrigatorio)

Confira, sem imprimir conteudo:

- o arquivo volta a fazer parse como JSON;
- o numero de clinicas e o mesmo de antes;
- cada clinica ainda tem `nome`, `username` e `token` preenchidos;
- o campo `escrita` esta no estado pedido.

Se qualquer item falhar, **restaure o backup** e diga o que aconteceu. Nao tente consertar na
tentativa e erro.

Se tudo passou, apague o backup.

## Passo 5 — reiniciar e confirmar

O servidor MCP le esse arquivo ao subir, entao a mudanca **so vale depois de reiniciar** o
Claude Code (e o Claude Desktop, se a pessoa usa nos dois — o arquivo e o mesmo para ambos).

Avise para reiniciar e diga como conferir: ao subir, o servidor loga

```
clinicorp-mcp pronto — N clinica(s): ... | escrita: LIGADA
```

Se preferir conferir sem reiniciar, rode uma tool de escrita qualquer e veja se ela recusa.

## Ao terminar

Se ligou, lembre em uma linha: toda alteracao sera confirmada com a pessoa antes de acontecer, e
o caminho seguro para testar e `clinicorp_alterar_status` (reversivel), nao cancelamento.
