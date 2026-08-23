# clinicorp

Acesso somente-leitura aos dados do **Clinicorp** dentro do Claude Code e do Cowork (Claude Desktop).

Pergunte em portugues — "como foi agosto na Matriz?", "quantas faltas tivemos essa semana?",
"quem tem orcamento aberto acima de 5 mil?" — e o Claude consulta a API e responde com numero real.

## O que vem no plugin

| Componente | O que faz |
|---|---|
| **Servidor MCP** (19 tools) | As chamadas na API: agenda, orcamentos, pagamentos, financeiro, ocupacao, metas, painel |
| **Skill `clinicorp`** | O julgamento: qual tool responde cada pergunta e como ler o resultado sem errar o numero |
| **`references/api-clinicorp.md`** | Documentacao completa dos 49 endpoints, para o que nao tem tool dedicada |

**Somente leitura.** Toda tool faz `GET`. Nada cria, altera ou cancela no Clinicorp — inclusive
`/appointment/change_status`, que a API expoe como `GET` mas altera estado, esta bloqueado.

## Instalacao

### 1. Instalar o plugin

**Claude Code:**

```bash
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install clinicorp@fernando-claude-marketplace
```

Reinicie o Claude Code depois.

**Cowork (Claude Desktop):** Settings → Plugins → Install from GitHub →
`fercosnt/fernando-claude-marketplace` → selecione `clinicorp`.

### 2. Configurar as credenciais

O jeito mais simples e rodar o comando guiado, que conduz o processo passo a passo:

```
/clinicorp-setup
```

Ele leva ate onde ficam usuario e token no Clinicorp, cria o arquivo e valida o acesso —
sem que o token precise ser digitado no chat.

Manualmente, se preferir: crie `~/.clinicorp-mcp.json` com as clinicas as quais voce tem acesso:

```json
[
  {
    "nome": "Matriz",
    "subscriber_id": "...",
    "username": "...",
    "token": "..."
  }
]
```

Depois restrinja a permissao — o token da acesso a dado de paciente:

```bash
chmod 600 ~/.clinicorp-mcp.json
```

Pode listar quantas clinicas quiser. O parametro `clinica` das tools aceita o `nome`
(sem diferenciar acento ou maiuscula) ou o proprio `subscriber_id`.

### 3. Onde achar usuario e token

No Clinicorp: **Gerenciar Assinatura → Acesso Externo e Integracoes → Integracoes**.
Copie **Usuario API** (username) e **Token API** (token).

Cada pessoa usa **as proprias credenciais**, nunca um token compartilhado — e o unico jeito de
haver rastro de quem consultou o que, e permite revogar o acesso de uma pessoa sem derrubar o
de todo mundo.

**Nenhuma credencial vive neste repositorio.** O plugin nao embute token, subscriber_id nem
nome de clinica: tudo vem do arquivo local de cada pessoa. Por isso o plugin serve qualquer
clinica que use Clinicorp, dentro ou fora da sua organizacao — basta cada um apontar para a
propria conta.

### Alternativas de configuracao

Se preferir variaveis de ambiente ao arquivo (precedencia de cima para baixo):

| Variavel | Uso |
|---|---|
| `CLINICORP_CLINICS` | JSON inline com o array de clinicas |
| `CLINICORP_CLINICS_FILE` | Caminho para outro arquivo JSON |
| `~/.clinicorp-mcp.json` | **Padrao recomendado** |
| `CLINICORP_SUBSCRIBER_ID` + `CLINICORP_USERNAME` + `CLINICORP_TOKEN` | Clinica unica |

Opcionais: `CLINICORP_BASE_URL`, `CLINICORP_TIMEOUT_MS`, `CLINICORP_MAX_DAYS`.

## Tools

**Descoberta** — `clinicorp_clinicas` (contas configuradas) · `clinicorp_unidades` (ids das
unidades) · `clinicorp_profissionais`

**Agenda** — `clinicorp_agenda` · `clinicorp_ocupacao` · `clinicorp_kpis_agenda`

**Pacientes** — `clinicorp_buscar_paciente` · `clinicorp_aniversariantes` ·
`clinicorp_agendamentos_paciente`

**Vendas** — `clinicorp_orcamentos` · `clinicorp_orcamento_detalhe` · `clinicorp_conversao`

**Financeiro** — `clinicorp_pagamentos` · `clinicorp_fluxo_caixa` · `clinicorp_inadimplencia` ·
`clinicorp_resumo_financeiro`

**Panorama** — `clinicorp_painel` (a visao de um mes inteiro em uma chamada) · `clinicorp_metas`

**Escape hatch** — `clinicorp_get` (GET cru em qualquer endpoint de leitura da API)

## LGPD

A API trafega dado de saude, CPF e telefone de paciente. O plugin foi desenhado para que o padrao
seja **agregado**, nao lista nominal: as tools resumem por padrao, cortam volume com `limite`, e a
skill orienta a so descer ao nivel do paciente quando a pergunta for sobre uma pessoa especifica.
O token fica no arquivo local com permissao 600 — nunca no repositorio nem no config do Claude.

## Desenvolvimento

O que roda e o bundle `servers/clinicorp-mcp.js` (sem dependencias, para funcionar no Cowork, que
nao executa `npm install`). A fonte fica em `server/`:

```bash
cd server
npm install
npm run build     # typecheck + bundle para ../servers/clinicorp-mcp.js
```

## Notas de campo

- Em ~06/2026 a API migrou de `sistema.clinicorp.com` para `api.clinicorp.com`. O host antigo passou
  a servir a tela de login, entao as chamadas voltavam **HTML** e o erro parecia "token invalido".
  O client detecta isso e diz que o problema e host/URL.
- A API **nao pagina**. Tools de listagem fatiam o periodo em janelas de 31 dias automaticamente;
  tools agregadas (painel, fluxo de caixa, conversao) nunca fatiam — quebrar o periodo quebraria o total.
- Flags booleanas da API sao a string `"X"`. `true`/`1`/`yes` sao ignorados **sem erro**.
- Varios campos de resposta tem typo no proprio spec (`Ocupaccion`, `FirsAppointmentTotal`,
  `AppoinmentsFinished`, `StatusDescrition`). As tools tipadas ja devolvem nome corrigido;
  o `clinicorp_get` devolve cru.
