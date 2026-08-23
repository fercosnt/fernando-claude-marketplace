# API Clinicorp — Documentação Completa

> Referência não-oficial, gerada a partir do OpenAPI 3.0 publicado em
> <https://api.clinicorp.com/api-docs/> (spec `API Clinicorp v1.0.0`).
> 49 endpoints em 17 grupos funcionais.

---

## Sumário

1. [Visão geral](#1-visão-geral)
2. [Autenticação](#2-autenticação)
3. [Convenções da API](#3-convenções-da-api)
4. [Erros](#4-erros)
5. [Clients prontos (cURL / JavaScript / Python)](#5-clients-prontos)
6. [Índice de endpoints](#6-índice-de-endpoints)
7. [Referência de endpoints](#7-referência-de-endpoints)
   - [7.1 users](#71-users) · [7.2 group](#72-group) · [7.3 business](#73-business)
   - [7.4 professional](#74-professional) · [7.5 procedures](#75-procedures)
   - [7.6 patient](#76-patient) · [7.7 appointment](#77-appointment)
   - [7.8 estimates](#78-estimates) · [7.9 sales](#79-sales)
   - [7.10 payment](#710-payment) · [7.11 financial](#711-financial)
   - [7.12 analytics](#712-analytics) · [7.13 operational](#713-operational)
   - [7.14 crm](#714-crm) · [7.15 products](#715-products)
   - [7.16 upload](#716-upload) · [7.17 migration](#717-migration)
8. [Receitas — fluxos completos](#8-receitas--fluxos-completos)
9. [Pegadinhas e inconsistências conhecidas](#9-pegadinhas-e-inconsistências-conhecidas)

---

## 1. Visão geral

| Item | Valor |
|---|---|
| **Base URL** | `https://api.clinicorp.com/rest/v1` |
| **Base URL alternativa** | `{url}/rest/v1` — para instâncias com host próprio |
| **Versão do spec** | `1.0.0` (OpenAPI 3.0) |
| **Protocolo** | HTTPS |
| **Formato** | JSON (`Content-Type: application/json`) |
| **Autenticação** | HTTP Basic (ver §2) |
| **Documentação interativa** | <https://api.clinicorp.com/api-docs/> |

A API é **REST-like**, mas com particularidades importantes:

- Quase tudo é `GET` com **query string**, inclusive operações que alteram estado
  (`/appointment/change_status` é `GET`).
- Os `POST` recebem o payload em `application/json` no corpo.
- Não há paginação. A janela de tempo (`from` / `to`) é o único mecanismo de
  limitação de volume — use períodos curtos em clínicas grandes.
- Não há webhooks documentados no spec (exceto o campo `ResponseWebhookUrl` de
  `/file/upload`). Integrações precisam de **polling**.

---

## 2. Autenticação

Todas as chamadas usam **HTTP Basic Authentication**.

> ⚠️ O spec declara o esquema com o nome `bearerAuth`, mas o `scheme` real é
> `basic`. **Não** use `Authorization: Bearer <token>` — não funciona.

| Campo Basic | O que informar |
|---|---|
| **Username** | ID de acesso ao sistema (**Usuário API**) |
| **Password** | **Token API** |

### Onde encontrar as credenciais

1. Fazer login no sistema Clinicorp.
2. Clicar em **Gerenciar Assinatura**.
3. Clicar em **Acesso Externo e Integrações**.
4. Seção **Integrações** → copiar **Usuário API** (username) e **Token API** (password).

### Header resultante

```
Authorization: Basic base64(USUARIO_API:TOKEN_API)
```

```bash
# cURL monta o header automaticamente
curl -u "$CLINICORP_USER:$CLINICORP_TOKEN" \
  "https://api.clinicorp.com/rest/v1/business/list?subscriber_id=SEU_ID"
```

```bash
# Ou manualmente
AUTH=$(printf '%s:%s' "$CLINICORP_USER" "$CLINICORP_TOKEN" | base64)
curl -H "Authorization: Basic $AUTH" \
  "https://api.clinicorp.com/rest/v1/business/list?subscriber_id=SEU_ID"
```

> 🔐 Guarde o Token API como segredo (variável de ambiente / secret manager).
> Ele dá acesso a dados de pacientes — dado pessoal sensível sob a LGPD.

---

## 3. Convenções da API

### 3.1 `subscriber_id`

Identifica o assinante (a conta Clinicorp). É obrigatório na maioria dos
endpoints. Duas exceções relevantes em `/appointment/list`:

| Tipo de conta | `subscriber_id` |
|---|---|
| Conta única | Opcional — o assinante é inferido do token |
| Conta de grupo / franquia | **Obrigatório** — seleciona a unidade. Sem ele, retorna `401` |

Use `/group/list_subscribers` para descobrir os `subscriber_id` de uma franquia.

### 3.2 `business_id` / `businessId` / `Clinic_BusinessId`

Identificam a **clínica** (unidade física). O mesmo conceito aparece com três
grafias diferentes dependendo do endpoint — confira a tabela de cada rota.
Quando opcional e omitido, a resposta agrega todas as clínicas do assinante.

Descubra os ids em `/business/list` ou `/group/list_subscribers_clinics`.

### 3.3 Formatos de data

A API mistura **quatro** formatos. Esta é a principal fonte de bugs:

| Formato | Exemplo | Onde aparece |
|---|---|---|
| `YYYY-MM-DD` | `2026-08-01` | Maioria dos filtros `from` / `to` / `date` |
| `YYYYMMDD` (string) | `20260801` | `/business/list_available_times` (`fromDate`, `toDate`) |
| `YYYYMMDD` (inteiro) | `20260801` | Campo `AtomicDate` nas respostas |
| ISO 8601 UTC | `2026-08-01T03:00:00.000Z` | Campo `date` de agendamentos, corpo dos `POST` |

Regras práticas:

- **Agendamentos** (`ItemType: APPOINTMENT`) trazem data/hora em **UTC** no campo
  `date`, mais `fromTime`/`toTime`.
- **Eventos e compromissos** (`EVENT`, `ASSIGN`) trazem `AtomicDate`
  (inteiro `YYYYMMDD`) e horários **no fuso da clínica**.
- Ao criar agendamento via `POST`, envie `date` em ISO com o offset correto
  (ex.: `"2026-04-12T03:00:00.000Z"` = 12/04 00:00 em BRT/UTC-3).
- Períodos `from`/`to` são **inclusivos** nas duas pontas.

### 3.4 A flag `"X"`

Vários parâmetros booleanos usam a convenção interna do Clinicorp: o valor é a
**string `X`** (maiúscula ou minúscula), não `true`/`1`/`yes`.

```
?includeAssigns=X&includeCanceled=X
```

Qualquer outro valor **mantém a opção desligada silenciosamente** — não gera erro.

A mesma convenção aparece em respostas: campos como `Deleted`, `Canceled`,
`Active`, `PatientConfirm`, `AllDay` vêm com `"X"` quando verdadeiros e
vazios/ausentes quando falsos.

### 3.5 `group_by`

Endpoints analíticos aceitam `group_by=month` para quebrar o resultado por mês
dentro do período. Só o valor `month` é suportado. Em alguns endpoints o
parâmetro é marcado obrigatório no spec (`/appointment/schedule_occupation`,
`/financial/average_installments`, `/sales/estimates_and_conversion`).

### 3.6 `isAPI`

Os endpoints de metas (`/operational/*`) exigem `isAPI=X` para retornar o JSON no
formato da API em vez do formato interno da tela.

---

## 4. Erros

Formato padrão de erro:

```json
{
  "Error": 400,
  "Message": "Parâmetro obrigatório não informado"
}
```

| Código | Significado | Causa típica |
|---|---|---|
| `400` | Parâmetro obrigatório não informado / dados inválidos | Falta `subscriber_id`, `from`, `to`; formato de data errado |
| `401` | Unauthorized | Credenciais Basic inválidas, ou conta de grupo sem `subscriber_id` |
| `404` | Recurso não encontrado | `clinic` inexistente em `/products/orders` |
| `500` | Erro interno | Falha no servidor — reenviar com backoff |

Em `/products/orders` o campo `Message` do `400` é um **array de erros de
validação** (formato Zod), não uma string:

```json
{
  "Error": 400,
  "Message": [
    {
      "code": "invalid_type",
      "expected": "string",
      "received": "undefined",
      "path": ["products", 0, "code"],
      "message": "Required"
    }
  ]
}
```

> ⚠️ Trate `Message` como `string | array` no seu parser de erro.

### Boas práticas de resiliência

- Retry com backoff exponencial em `500` e timeouts; **não** faça retry em `400`.
- Sem paginação: se um período retornar volume muito grande ou estourar timeout,
  **quebre em janelas menores** (ex.: mês → semanas).
- `POST /patient/create` e `POST /crm/add_leads` **não são idempotentes** —
  guarde o id retornado e faça deduplicação do seu lado.

---

## 5. Clients prontos

### 5.1 Bash / cURL

```bash
#!/usr/bin/env bash
set -euo pipefail

CLINICORP_BASE="https://api.clinicorp.com/rest/v1"
: "${CLINICORP_USER:?defina CLINICORP_USER}"
: "${CLINICORP_TOKEN:?defina CLINICORP_TOKEN}"

cc_get() {  # cc_get "/business/list" "subscriber_id=meuid"
  curl -sS -u "$CLINICORP_USER:$CLINICORP_TOKEN" \
       -H "Accept: application/json" \
       "$CLINICORP_BASE$1?${2:-}"
}

cc_post() { # cc_post "/patient/create" '{"Name":"..."}'
  curl -sS -u "$CLINICORP_USER:$CLINICORP_TOKEN" \
       -H "Content-Type: application/json" \
       -X POST -d "$2" \
       "$CLINICORP_BASE$1"
}

cc_get "/business/list" "subscriber_id=meuid" | jq .
```

### 5.2 JavaScript / Node (fetch nativo, Node 18+)

```js
// clinicorp.js
const BASE = "https://api.clinicorp.com/rest/v1";

const auth = "Basic " + Buffer.from(
  `${process.env.CLINICORP_USER}:${process.env.CLINICORP_TOKEN}`
).toString("base64");

async function request(path, { method = "GET", query, body } = {}) {
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(query ?? {})) {
    if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, v);
  }

  const res = await fetch(url, {
    method,
    headers: {
      Authorization: auth,
      Accept: "application/json",
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const msg = Array.isArray(data?.Message)
      ? JSON.stringify(data.Message)          // erro de validação (products/orders)
      : data?.Message ?? res.statusText;
    throw new Error(`Clinicorp ${res.status}: ${msg}`);
  }
  return data;
}

export const clinicorp = {
  get:  (path, query)      => request(path, { query }),
  post: (path, body, query) => request(path, { method: "POST", body, query }),
};

// uso
// const clinicas = await clinicorp.get("/business/list", { subscriber_id: "meuid" });
```

### 5.3 Python (requests)

```python
# clinicorp.py
import os
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://api.clinicorp.com/rest/v1"


class ClinicorpError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(f"Clinicorp {status}: {message}")


class Clinicorp:
    def __init__(self, user=None, token=None, timeout=60):
        self.auth = HTTPBasicAuth(
            user or os.environ["CLINICORP_USER"],
            token or os.environ["CLINICORP_TOKEN"],
        )
        self.timeout = timeout
        self.session = requests.Session()

    def _call(self, method, path, params=None, json=None):
        params = {k: v for k, v in (params or {}).items() if v not in (None, "")}
        r = self.session.request(
            method, BASE + path,
            params=params, json=json,
            auth=self.auth, timeout=self.timeout,
            headers={"Accept": "application/json"},
        )
        try:
            data = r.json() if r.content else None
        except ValueError:
            data = None

        if not r.ok:
            msg = (data or {}).get("Message", r.text) if isinstance(data, dict) else r.text
            raise ClinicorpError(r.status_code, msg)
        return data

    def get(self, path, **params):
        return self._call("GET", path, params=params)

    def post(self, path, payload, **params):
        return self._call("POST", path, params=params, json=payload)


# uso
# cc = Clinicorp()
# clinicas = cc.get("/business/list", subscriber_id="meuid")
```

> Os exemplos por endpoint abaixo usam `cc_get`/`cc_post` (bash),
> `clinicorp` (JS) e `cc` (Python) definidos aqui.

---

## 6. Índice de endpoints

| # | Método | Rota | Grupo | O que faz |
|---|---|---|---|---|
| 1 | GET | `/security/list_users` | users | Lista usuários do assinante |
| 2 | GET | `/group/list_subscribers_clinics` | group | Clínicas do assinante com horários de trabalho |
| 3 | GET | `/group/list_subscribers` | group | Unidades da franquia |
| 4 | GET | `/business/list` | business | Clínicas do assinante |
| 5 | GET | `/business/list_chairs` | business | Cadeiras da clínica |
| 6 | GET | `/business/list_available_times` | business | Slots livres por profissional/clínica |
| 7 | GET | `/professional/list_all_professionals` | professional | Profissionais do sistema |
| 8 | GET | `/procedures/list` | procedures | Procedimentos das tabelas de preço |
| 9 | GET | `/procedures/list_specialties` | procedures | Especialidades |
| 10 | GET | `/patient/get` | patient | Busca 1 paciente |
| 11 | GET | `/patient/birthdays` | patient | Aniversariantes do dia |
| 12 | POST | `/patient/create` | patient | Cria paciente |
| 13 | GET | `/patient/list_appointments` | patient | Agendamentos do paciente |
| 14 | GET | `/patient/list_estimates` | patient | Soma de orçamentos por status |
| 15 | GET | `/appointment/list` | appointment | Agenda do período (agend./eventos/compromissos) |
| 16 | GET | `/appointment/list_categories` | appointment | Categorias de agendamento |
| 17 | GET | `/appointment/list_info` | appointment | KPIs de agendamento |
| 18 | GET | `/appointment/schedule_occupation` | appointment | Ocupação da agenda |
| 19 | GET | `/appointment/status_list` | appointment | Status de agendamento |
| 20 | GET | `/appointment/change_status` | appointment | Altera status (1..n agendamentos) |
| 21 | POST | `/appointment/create_appointment_by_api` | appointment | Cria agendamento na agenda |
| 22 | POST | `/appointment/create_online_scheduling` | appointment | Cria solicitação de agendamento online |
| 23 | GET | `/appointment/get_avaliable_days` | appointment | Dias com horários livres (link público) |
| 24 | GET | `/appointment/get_avaliable_times_calendar` | appointment | Horários livres de uma data (link público) |
| 25 | GET | `/appointment/get_appointment` | appointment | Detalha agendamento/solicitação |
| 26 | POST | `/appointment/confirm_appointment` | appointment | Confirma agendamento |
| 27 | POST | `/appointment/cancel_appointment` | appointment | Cancela agendamento |
| 28 | GET | `/estimates/list` | estimates | Orçamentos do período |
| 29 | GET | `/estimates/get` | estimates | Orçamento por `treatment_id` |
| 30 | GET | `/sales/estimates_and_conversion` | sales | Orçamentos, ticket médio e conversão |
| 31 | GET | `/sales/expertise_revenue` | sales | Vendas por especialidade |
| 32 | GET | `/payment/list` | payment | Pagamentos do período |
| 33 | GET | `/payment/list_reconcile_claim` | payment | Faturamento por plano de saúde |
| 34 | GET | `/financial/list_summary` | financial | Resumo financeiro do período |
| 35 | GET | `/financial/list_cash_flow` | financial | Fluxo de caixa |
| 36 | GET | `/financial/list_payments` | financial | Totais de pagamentos/inadimplência |
| 37 | GET | `/financial/list_invoices` | financial | Pagamentos com nota fiscal |
| 38 | GET | `/financial/list_receipt` | financial | Recibos |
| 39 | GET | `/financial/average_installments` | financial | Parcelamento médio |
| 40 | GET | `/analytics/list_results` | analytics | Painel consolidado por clínica |
| 41 | GET | `/operational/list_sales_goals` | operational | Metas de venda vs. realizado |
| 42 | GET | `/operational/list_misses_goals` | operational | Metas de falta vs. realizado |
| 43 | POST | `/crm/add_leads` | crm | Insere lead em campanha |
| 44 | GET | `/crm/list_active_campaigns` | crm | Campanhas ativas |
| 45 | POST | `/products/orders` | products | Cria ordem de compra de produtos |
| 46 | POST | `/file/upload` | upload | Envia arquivo/imagem/documento |
| 47 | POST | `/migration/file/upload` | migration | Gera URL assinada para upload de base |
| 48 | POST | `/migration/file` | migration | Cria migrações a partir de arquivo |
| 49 | POST | `/migration/connection` | migration | Cria migrações por conexão a banco |

---

## 7. Referência de endpoints

Legenda: **✱** = parâmetro obrigatório.

---

### 7.1 users

#### `GET /security/list_users`

Lista todos os usuários do sistema para o assinante.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |

**200 — resposta**

```json
[
  { "id": 0, "UserName": "string", "FullName": "string" }
]
```

```bash
cc_get "/security/list_users" "subscriber_id=$SUB"
```

```js
const users = await clinicorp.get("/security/list_users", { subscriber_id: SUB });
```

```python
users = cc.get("/security/list_users", subscriber_id=SUB)
```

---

### 7.2 group

#### `GET /group/list_subscribers_clinics`

Dados das clínicas do assinante: nome, tipo, horários de trabalho, duração do slot.
Útil para montar grade de horários e calcular capacidade instalada.

Sem parâmetros (o assinante vem do token).

**200 — resposta**

```json
[
  {
    "Name": "string",
    "Email": "string",
    "NoLimitAptSameTime": "string",
    "Address": "string",
    "Active": "string",
    "OtherLandline": 0,
    "WorkingDaysHours": {},
    "Landline": 0,
    "SubscriberBussinessUID": "string",
    "SlotTime": 0,
    "CompanyId": 0
  }
]
```

| Campo | Observação |
|---|---|
| `WorkingDaysHours` | Objeto com a grade de funcionamento por dia da semana |
| `SlotTime` | Duração do slot da agenda, em minutos |
| `NoLimitAptSameTime` | `"X"` = permite agendamentos simultâneos sem limite |
| `Active` | `"X"` = clínica ativa |
| `SubscriberBussinessUID` | ⚠️ grafia com dois "s" no spec |

```bash
cc_get "/group/list_subscribers_clinics"
```

```js
const clinicas = await clinicorp.get("/group/list_subscribers_clinics");
```

```python
clinicas = cc.get("/group/list_subscribers_clinics")
```

#### `GET /group/list_subscribers`

Lista as unidades da franquia. É o ponto de partida em contas de grupo: devolve
os `SubscriberBussinessUID` que você usará como `subscriber_id` nos demais endpoints.

Sem parâmetros.

**200 — resposta**

```json
{ "SubscriberBussinessUID": "string", "Namespace": "string" }
```

```bash
cc_get "/group/list_subscribers"
```

---

### 7.3 business

#### `GET /business/list`

Lista as clínicas do assinante.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |

**200 — resposta**

```json
[
  {
    "id": 0,
    "CompanyId": 0,
    "BusinessName": "string",
    "Name": "string",
    "Address": "string",
    "Email": "string"
  }
]
```

O campo `id` é o valor que vai em `business_id` / `businessId` / `Clinic_BusinessId`
nos outros endpoints.

**400** — parâmetro obrigatório não informado.

```bash
cc_get "/business/list" "subscriber_id=$SUB"
```

```js
const clinicas = await clinicorp.get("/business/list", { subscriber_id: SUB });
const idPorNome = Object.fromEntries(clinicas.map(c => [c.Name, c.id]));
```

```python
clinicas = cc.get("/business/list", subscriber_id=SUB)
id_por_nome = {c["Name"]: c["id"] for c in clinicas}
```

#### `GET /business/list_chairs`

Lista as cadeiras **ativas** da clínica. Necessário quando você agenda por cadeira
(`ScheduleToType: "CHAIR"`).

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `Clinic_BusinessId` | query | integer | ✱ | id da Clínica |

**200 — resposta**

```json
[
  { "id": 0, "BusinessId": 0, "Name": "string" }
]
```

**400** — parâmetro obrigatório não informado.

```bash
cc_get "/business/list_chairs" "subscriber_id=$SUB&Clinic_BusinessId=$CLINICA"
```

```python
cadeiras = cc.get("/business/list_chairs",
                  subscriber_id=SUB, Clinic_BusinessId=CLINICA)
```

#### `GET /business/list_available_times`

Slots de horário **disponíveis** para um par profissional/clínica em um intervalo.

> ⚠️ Este endpoint usa datas no formato **`YYYYMMDD`** (sem hífens), diferente do
> resto da API.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `professionalId` | query | integer | ✱ | id do profissional |
| `clinicId` | query | integer | ✱ | id da clínica |
| `fromDate` | query | string `YYYYMMDD` | ✱ | Data inicial |
| `toDate` | query | string `YYYYMMDD` | ✱ | Data final |

**200 — resposta**

```json
[
  {
    "date": "YYYYMMDD",
    "slots": [
      { "slotTime": "YYYYMMDD", "toTime": "10:00", "fromTime": "10:30" }
    ]
  }
]
```

> ⚠️ No exemplo do spec `toTime` vem **antes** de `fromTime` e com valor menor —
> inconsistência do exemplo, não confie na ordem dos campos; leia por nome.

```bash
cc_get "/business/list_available_times" \
  "professionalId=$PROF&clinicId=$CLINICA&fromDate=20260901&toDate=20260930"
```

```js
const slots = await clinicorp.get("/business/list_available_times", {
  professionalId: PROF,
  clinicId: CLINICA,
  fromDate: "20260901",
  toDate:   "20260930",
});
```

```python
from datetime import date

def ymd(d: date) -> str:
    return d.strftime("%Y%m%d")

slots = cc.get("/business/list_available_times",
               professionalId=PROF, clinicId=CLINICA,
               fromDate=ymd(date(2026, 9, 1)), toDate=ymd(date(2026, 9, 30)))
```

---

### 7.4 professional

#### `GET /professional/list_all_professionals`

Lista todos os profissionais do assinante.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `fromOnlineScheduling` | query | boolean | — | `true` para trazer apenas profissionais habilitados no agendamento online |

**200 — resposta**

```json
[
  { "id": 0, "name": "string", "cpf": "string" }
]
```

```bash
cc_get "/professional/list_all_professionals"
cc_get "/professional/list_all_professionals" "fromOnlineScheduling=true"
```

```js
const profs = await clinicorp.get("/professional/list_all_professionals",
                                  { fromOnlineScheduling: true });
```

```python
profs = cc.get("/professional/list_all_professionals", fromOnlineScheduling="true")
```

---

### 7.5 procedures

#### `GET /procedures/list`

Procedimentos válidos das tabelas de preço da clínica.

Sem parâmetros.

**200 — resposta**

```json
[
  {
    "id": 0,
    "PriceListId": 0,
    "ProcedureExpertiseName": "string",
    "ProcedureName": "string",
    "Type": "string",
    "PriceListName": "string"
  }
]
```

```bash
cc_get "/procedures/list"
```

#### `GET /procedures/list_specialties`

Especialidades cadastradas.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |

**200 — resposta**

```json
[
  {
    "id": 0,
    "Active": "string",
    "Description": "string",
    "Language": "string",
    "Type": "string",
    "z_LastChange_Date": "2026-08-23",
    "z_LastChange_UserId": 0
  }
]
```

```bash
cc_get "/procedures/list_specialties" "subscriber_id=$SUB"
```

```python
esp = cc.get("/procedures/list_specialties", subscriber_id=SUB)
ativas = [e for e in esp if e.get("Active") == "X"]
```

---

### 7.6 patient

#### `GET /patient/get`

Busca **um** paciente. Além de `subscriber_id`, informe **pelo menos um** critério
de busca. Se mais de um for enviado, funcionam como filtros combinados.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `PatientId` | query | integer | — | id do Paciente |
| `Name` | query | string | — | Nome do Paciente |
| `OtherDocumentId` | query | string | — | CPF do Paciente |
| `Phone` | query | string | — | Telefone ou celular |
| `Email` | query | string | — | E-mail |

**200 — resposta**

```json
{
  "PatientId": 0,
  "Name": "string",
  "Email": "string",
  "Phone": "string",
  "OtherDocumentId": "string",
  "Status": "string",
  "BirthDate": "string"
}
```

> Retorna **objeto**, não array. Se nada for encontrado o retorno vem vazio —
> trate ausência de `PatientId` como "não existe".

```bash
cc_get "/patient/get" "subscriber_id=$SUB&OtherDocumentId=12345678900"
```

```js
const p = await clinicorp.get("/patient/get", {
  subscriber_id: SUB,
  OtherDocumentId: "12345678900",
});
if (!p?.PatientId) console.log("paciente não encontrado");
```

```python
p = cc.get("/patient/get", subscriber_id=SUB, OtherDocumentId="12345678900")
if not (p or {}).get("PatientId"):
    print("paciente não encontrado")
```

#### `GET /patient/birthdays`

Pacientes aniversariantes de uma data. Base típica para automação de mensagem
de aniversário.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `date` | query | `YYYY-MM-DD` | — | Data alvo. Omitido = hoje |

**200 — resposta**

```json
[
  {
    "PatientId": 0,
    "Name": "string",
    "BirthDate": "2026-08-23",
    "Age": 0,
    "Email": "string",
    "MobilePhone": "string",
    "OtherDocumentId": "string"
  }
]
```

```bash
cc_get "/patient/birthdays" "subscriber_id=$SUB&date=2026-09-15"
```

```python
from datetime import date
niver = cc.get("/patient/birthdays", subscriber_id=SUB, date=date.today().isoformat())
```

#### `POST /patient/create`

Cria um paciente.

**Request body** (`application/json`)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `subscriber_id` | string | ✱ | id do Assinante |
| `Name` | string | ✱ | Nome do paciente |
| `BirthDate` | `YYYY-MM-DD` | — | Data de nascimento |
| `Sex` | string | — | `M` / `F` |
| `Email` | string | — | E-mail |
| `MobilePhone` | string/number | — | Celular |
| `DocumentId` | string/number | — | Documento (RG) |
| `OtherDocumentId` | string/number | — | CPF |
| `Notes` | string | — | Observações |
| `IgnoreSameName` | `"X"` | — | Cria mesmo havendo paciente com o mesmo nome |
| `IgnoreSameDoc` | `"X"` | — | Cria mesmo havendo paciente com o mesmo CPF |

```json
{
  "subscriber_id": "clinicorp",
  "Name": "Maria Souza",
  "BirthDate": "1988-04-22",
  "Sex": "F",
  "Email": "maria@exemplo.com",
  "MobilePhone": "47990000000",
  "OtherDocumentId": "12345678900",
  "Notes": "Indicada pela Dra. Ana"
}
```

**200 — resposta**: eco dos dados do paciente criado.

> ⚠️ Sem `IgnoreSameName`/`IgnoreSameDoc`, a criação é **bloqueada** quando existe
> duplicata. O fluxo seguro é: `GET /patient/get` por CPF → se não achar, criar.

```bash
cc_post "/patient/create" '{
  "subscriber_id":"'"$SUB"'",
  "Name":"Maria Souza",
  "BirthDate":"1988-04-22",
  "Sex":"F",
  "OtherDocumentId":"12345678900"
}'
```

```js
const novo = await clinicorp.post("/patient/create", {
  subscriber_id: SUB,
  Name: "Maria Souza",
  BirthDate: "1988-04-22",
  Sex: "F",
  OtherDocumentId: "12345678900",
});
```

```python
novo = cc.post("/patient/create", {
    "subscriber_id": SUB,
    "Name": "Maria Souza",
    "BirthDate": "1988-04-22",
    "Sex": "F",
    "OtherDocumentId": "12345678900",
})
```

#### `GET /patient/list_appointments`

Todos os agendamentos de um paciente (sem recorte de período).

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `PatientId` | query | integer | ✱ | id do Paciente |

**200 — resposta**

```json
[
  {
    "id": 4791226171916288,
    "AtomicDate": 20250501,
    "date": "2025-05-01T18:02:36.132Z",
    "PatientName": "Nome do Paciente",
    "fromTime": "10:00",
    "toTime": "10:30"
  }
]
```

```bash
cc_get "/patient/list_appointments" "PatientId=$PACIENTE"
```

#### `GET /patient/list_estimates`

Soma dos orçamentos do período, quebrada por status. É o agregado — para a lista
detalhada use `/estimates/list`.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |

**200 — resposta**

```json
{
  "From": "2026-08-01",
  "To": "2026-08-31",
  "BusinessId": 0,
  "ApprovedQuantity": 0,
  "ApprovedTotalAmount": 0,
  "FollowUpQuantity": 0,
  "FollowUpTotalAmount": 0,
  "OpenQuantity": 0,
  "OpenTotalAmount": 0,
  "RejectedQuantity": 0,
  "RejectedTotalAmount": 0
}
```

```bash
cc_get "/patient/list_estimates" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

```python
tot = cc.get("/patient/list_estimates", subscriber_id=SUB,
             **{"from": "2026-08-01", "to": "2026-08-31"})
conversao = tot["ApprovedTotalAmount"] / max(
    tot["ApprovedTotalAmount"] + tot["OpenTotalAmount"] + tot["RejectedTotalAmount"], 1)
```

> 💡 Em Python, `from` é palavra reservada — passe via `**{"from": ...}`.

---

### 7.7 appointment

O grupo mais rico da API. Divide-se em três frentes:

- **Leitura da agenda**: `list`, `list_categories`, `status_list`, `list_info`, `schedule_occupation`
- **Escrita**: `create_appointment_by_api`, `change_status`, `confirm_appointment`, `cancel_appointment`
- **Agendamento online público** (fluxo com `code_link`): `get_avaliable_days`,
  `get_avaliable_times_calendar`, `create_online_scheduling`, `get_appointment`

#### `GET /appointment/list`

**O endpoint central.** Lista os itens da agenda do assinante no período.

Por padrão retorna **apenas agendamentos de pacientes**. Para a agenda completa —
necessária para cálculo de ocupação e capacidade instalada — envie `includeAssigns=X`.

##### Tipos de item

Todo item traz o campo `ItemType`:

| `ItemType` | O que é | Como incluir |
|---|---|---|
| `APPOINTMENT` | Agendamento de paciente | sempre retornado |
| `ASSIGN` | Compromisso na agenda | `includeAssigns=X` |
| `EVENT` | Evento ou bloqueio da agenda | `includeAssigns=X` |

Compromissos e eventos ocupam a agenda da mesma forma e vêm pelo mesmo parâmetro.
A distinção é histórica: a agenda atual cria apenas **compromissos** (`ASSIGN`);
itens `EVENT` vêm da agenda antiga.

##### Parâmetros

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `from` | query | `string($date)` | ✱ | Data inicial do período (inclusive) |
| `to` | query | `string($date)` | ✱ | Data final do período (inclusive) |
| `subscriber_id` | query | string | condicional | **Conta única**: pode ser omitido (assinante vem do token). **Conta de grupo**: obrigatório — seleciona a unidade; sem ele retorna `401` |
| `businessId` | query | integer | — | Filtra uma clínica. Omitido = todas as clínicas do assinante |
| `patientId` | query | integer | — | Filtra agendamentos de um paciente |
| `includeAssigns` | query | `"X"` | — | Inclui compromissos e eventos (`ASSIGN` e `EVENT`) |
| `includeCanceled` | query | `"X"` | — | Inclui agendamentos desmarcados |
| `includeDeleted` | query | `"X"` | — | Inclui agendamentos excluídos |

##### Datas e horários

- **Agendamentos** trazem data e hora em **UTC** no campo `date`, e os horários em
  `fromTime` / `toTime`.
- **Eventos e compromissos** trazem a data em `AtomicDate` (inteiro `YYYYMMDD`) e
  os horários em `fromTime` / `toTime` **no fuso da clínica**. Quando ocupam o dia
  inteiro, `AllDay` vem preenchido.

##### Observações

- Os parâmetros de inclusão são ativados **somente pelo valor `X`** (maiúsculo ou
  minúsculo). Qualquer outro valor mantém a opção desligada.
- Agendamentos excluídos não são retornados a menos que `includeDeleted` seja enviado.
- Eventos e compromissos **não têm vínculo com paciente** — o filtro `patientId`
  não se aplica a eles.
- Evento **sem** `Dentist_PersonId` é um evento da clínica (não de um profissional).

**200 — resposta**

```json
[
  {
    "ItemType": "APPOINTMENT",
    "id": 0,
    "date": "2026-08-23T03:05:52.641Z",
    "AtomicDate": 20260801,
    "fromTime": "09:00",
    "toTime": "09:30",
    "AllDay": "string",
    "Name": "string",
    "Clinic_BusinessId": 0,
    "Dentist_PersonId": 0,
    "PatientName": "string",
    "MobilePhone": "string",
    "Email": "string",
    "StatusId": 0,
    "Canceled": "string",
    "Deleted": "string",
    "Notes": "string",
    "Session": 0,
    "Sequence": 0,
    "CreateUserId": 0,
    "CreateUserName": "string",
    "z_LastChange_Date": "2026-08-23T03:05:52.641Z"
  }
]
```

Os campos variam conforme o `ItemType`: agendamentos trazem os dados do paciente;
eventos e compromissos trazem título em `Name` e, quando aplicável,
`Dentist_PersonId`.

**400** — parâmetro obrigatório não informado · **401** — Unauthorized
(inclusive conta de grupo sem `subscriber_id`).

```bash
# agenda completa de agosto, incluindo compromissos e eventos
cc_get "/appointment/list" "from=2026-08-01&to=2026-08-31&includeAssigns=X"
```

```js
const agenda = await clinicorp.get("/appointment/list", {
  from: "2026-08-01",
  to:   "2026-08-31",
  subscriber_id: SUB,        // obrigatório em conta de grupo
  includeAssigns: "X",
});

const porTipo = agenda.reduce((acc, i) => {
  (acc[i.ItemType] ??= []).push(i);
  return acc;
}, {});

console.log(
  "agendamentos:", porTipo.APPOINTMENT?.length ?? 0,
  "compromissos:", porTipo.ASSIGN?.length ?? 0,
  "eventos:",      porTipo.EVENT?.length ?? 0,
);
```

```python
from collections import defaultdict

agenda = cc.get("/appointment/list", subscriber_id=SUB,
                includeAssigns="X",
                **{"from": "2026-08-01", "to": "2026-08-31"})

por_tipo = defaultdict(list)
for item in agenda:
    por_tipo[item["ItemType"]].append(item)

# agendamentos ativos (nem cancelados nem excluídos)
ativos = [a for a in por_tipo["APPOINTMENT"]
          if a.get("Canceled") != "X" and a.get("Deleted") != "X"]
```

#### `GET /appointment/list_categories`

Categorias de agendamento cadastradas (com cor).

Sem parâmetros.

**200 — resposta**

```json
[
  { "id": 0, "Description": "string", "Color": "string" }
]
```

```bash
cc_get "/appointment/list_categories"
```

#### `GET /appointment/status_list`

Lista os status de agendamento do assinante — necessário para saber quais
`status_id` passar em `/appointment/change_status`.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |

**200 — resposta**

```json
[
  {
    "Description": "1-Confirmado",
    "Color": "#009688",
    "z_LastChange_UserId": 0,
    "Type": "CONFIRMED",
    "Reference": "Appointment",
    "Active": "X",
    "ReferenceType": "",
    "z_LastChange_Date": "2020-12-01T20:00:00.000Z",
    "id": 8888888888888888
  }
]
```

O campo `Type` é a chave semântica estável (ex.: `CONFIRMED`); `Description` é
livre e editável pela clínica — **não faça matching por `Description`**.

```bash
cc_get "/appointment/status_list" "subscriber_id=$SUB"
```

```python
status = cc.get("/appointment/status_list", subscriber_id=SUB)
id_confirmado = next(s["id"] for s in status if s["Type"] == "CONFIRMED")
```

#### `GET /appointment/change_status`

Atualiza o status de **um ou vários** agendamentos.

> ⚠️ É um `GET` que **altera estado**. Não é idempotente do ponto de vista de
> auditoria e não deve ser colocado atrás de cache/prefetch.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `id` | query | string | ✱ | id do agendamento. Para vários: `id1, id2, id3,...` |
| `status_id` | query | integer | ✱ | id do Status (ver `/appointment/status_list`) |

**200 — resposta**

```json
[
  {
    "id": 4791226171916288,
    "Date": "2025-01-30T18:02:36.132Z",
    "PatientName": "Nome do Paciente",
    "StatusId": 5609543400816640,
    "StatusDescrition": "1-Confirmado"
  }
]
```

> ⚠️ O campo vem grafado `StatusDescrition` (sem o "p"), não `StatusDescription`.

```bash
cc_get "/appointment/change_status" "id=4791226171916288&status_id=5609543400816640"

# vários de uma vez (URL-encode a vírgula+espaço)
cc_get "/appointment/change_status" "id=111,222,333&status_id=5609543400816640"
```

```js
await clinicorp.get("/appointment/change_status", {
  id: [111, 222, 333].join(","),
  status_id: 5609543400816640,
});
```

```python
cc.get("/appointment/change_status",
       id=",".join(map(str, [111, 222, 333])),
       status_id=5609543400816640)
```

#### `GET /appointment/list_info`

KPIs de agendamento do período: total agendado, primeiras consultas, faltas e
quebra por categoria.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |
| `group_by` | query | `"month"` | — | Agrupa por mês |

**200 — resposta**

```json
{
  "From": "2026-08-01",
  "To": "2026-08-31",
  "ClinicId": 0,
  "ScheduledTotal": 0,
  "FirsAppointmentTotal": 0,
  "MissedAppointmentTotal": 0,
  "Category": [ { "categoria_do_cliente": "string" } ]
}
```

> ⚠️ `FirsAppointmentTotal` — grafia sem o "t" de "First".

```bash
cc_get "/appointment/list_info" \
  "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31&group_by=month"
```

```python
info = cc.get("/appointment/list_info", subscriber_id=SUB, group_by="month",
              **{"from": "2026-01-01", "to": "2026-12-31"})
taxa_falta = info["MissedAppointmentTotal"] / max(info["ScheduledTotal"], 1)
```

#### `GET /appointment/schedule_occupation`

Ocupação da agenda no período: tempo disponível, tempo agendado, percentual de
ocupação, tempo de eventos e tempo em que os profissionais não estão disponíveis.
Todos os tempos em **minutos**.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |
| `group_by` | query | `"month"` | ✱ | Agrupamento (passe `month`) |

**200 — resposta**

```json
[
  {
    "TotalValidScheduleTime": 0,
    "TotalAppointmentTime": 0,
    "TotalEvent": "string",
    "TotalBusy": 0,
    "month": "string",
    "Ocupaccion": "string"
  }
]
```

| Campo | Significado |
|---|---|
| `TotalValidScheduleTime` | Tempo total que a clínica teve disponível (min) |
| `TotalAppointmentTime` | Tempo total de agendamentos (min) |
| `TotalEvent` | Tempo total de eventos na agenda (min) |
| `TotalBusy` | Tempo em que os profissionais não estão disponíveis (min) |
| `Ocupaccion` | Ocupação da agenda em **percentual** ⚠️ grafia com dois "c" |

```bash
cc_get "/appointment/schedule_occupation" \
  "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31&group_by=month"
```

```js
const oc = await clinicorp.get("/appointment/schedule_occupation", {
  subscriber_id: SUB, from: "2026-01-01", to: "2026-12-31", group_by: "month",
});
oc.forEach(m => console.log(m.month, m.Ocupaccion));
```

#### `POST /appointment/create_appointment_by_api`

Cria um agendamento **direto na agenda** do sistema (diferente da solicitação
online, que entra como pedido a aprovar).

**Request body** (`application/json`)

| Campo | Tipo | Descrição |
|---|---|---|
| `Patient_PersonId` | integer | id do paciente já cadastrado |
| `PatientName` | string | Nome do paciente |
| `MobilePhone` | string | Celular |
| `Email` | string | E-mail |
| `fromTime` | `HH:MM` | Hora de início |
| `toTime` | `HH:MM` | Hora de término |
| `date` | ISO 8601 | Data do agendamento |
| `Clinic_BusinessId` | integer | id da clínica |
| `Dentist_PersonId` | integer | id do profissional |
| `ScheduleToId` | integer | id do recurso de destino (ex.: cadeira) |
| `ScheduleToType` | string | Tipo do recurso — ex.: `"CHAIR"` |
| `Procedures` | string | Procedimentos, separados por vírgula |
| `CategoryColor` | string | Cor da categoria (hex) |
| `CategoryDescription` | string | Descrição da categoria |

```json
{
  "Patient_PersonId": 333333333333,
  "PatientName": "João da Silva",
  "MobilePhone": "(11) 91234-5678",
  "Email": "email@dominio.com",
  "fromTime": "10:00",
  "toTime": "11:00",
  "date": "2025-04-12T03:00:00.000Z",
  "Clinic_BusinessId": 111111111111,
  "Dentist_PersonId": 222222222222,
  "ScheduleToId": 1234567890124,
  "ScheduleToType": "CHAIR",
  "Procedures": "Limpeza, Obturação",
  "CategoryColor": "#FF5733",
  "CategoryDescription": "Consulta odontológica de rotina"
}
```

**200 — resposta**

```json
[ { "Status": "CREATED", "id": 987654321 } ]
```

**400** — requisição inválida ou recurso não encontrado (sem corpo padronizado).

```bash
cc_post "/appointment/create_appointment_by_api" '{
  "Patient_PersonId": 333333333333,
  "PatientName": "João da Silva",
  "fromTime": "10:00",
  "toTime": "11:00",
  "date": "2026-09-12T03:00:00.000Z",
  "Clinic_BusinessId": 111111111111,
  "Dentist_PersonId": 222222222222,
  "Procedures": "Limpeza"
}'
```

```js
const [criado] = await clinicorp.post("/appointment/create_appointment_by_api", {
  Patient_PersonId: pacienteId,
  PatientName: "João da Silva",
  fromTime: "10:00",
  toTime: "11:00",
  date: new Date(Date.UTC(2026, 8, 12, 3, 0, 0)).toISOString(),
  Clinic_BusinessId: CLINICA,
  Dentist_PersonId: PROF,
  Procedures: "Limpeza",
});
console.log(criado.Status, criado.id);
```

```python
from datetime import datetime, timezone

criado = cc.post("/appointment/create_appointment_by_api", {
    "Patient_PersonId": paciente_id,
    "PatientName": "João da Silva",
    "fromTime": "10:00",
    "toTime": "11:00",
    "date": datetime(2026, 9, 12, 3, 0, tzinfo=timezone.utc)
              .isoformat().replace("+00:00", "Z"),
    "Clinic_BusinessId": CLINICA,
    "Dentist_PersonId": PROF,
    "Procedures": "Limpeza",
})[0]
```

#### `POST /appointment/create_online_scheduling`

Cria uma **solicitação** de agendamento (fluxo de agendamento online / chatbot).
Entra na fila de aprovação da clínica — não é um agendamento confirmado.

**Request body** (`application/json`)

| Campo | Tipo | Descrição |
|---|---|---|
| `CodeLink` | integer | Código de acesso do link público de agendamento |
| `PatientName` | string | Nome do paciente |
| `SchedulingReason` | string | Razão da consulta |
| `MobilePhone` | string | Celular |
| `OtherPhones` | string | Outros telefones |
| `OtherDocumentId` | string | CPF — **apenas os 3 primeiros dígitos** |
| `Email` | string | E-mail |
| `NotesPatient` | string | Observações do paciente |
| `fromTime` | `HH:MM` | Hora de início |
| `toTime` | `HH:MM` | Hora de término |
| `IsOnlineScheduling` | boolean | `true` para agendamento online |
| `date` | ISO 8601 | Data desejada |
| `Type` | string | Origem da solicitação — ex.: `"CLOUDIA"` |
| `Dentist_PersonId` | integer | id do profissional |
| `Clinic_BusinessId` | integer | id da clínica |
| `AlreadyPatient` | boolean | `true` se já é paciente da clínica |

```json
{
  "CodeLink": 27478,
  "PatientName": "Nome do paciente",
  "SchedulingReason": "Razao da consulta",
  "MobilePhone": "(47) 90000-0000",
  "OtherPhones": "(47) 90000-0000",
  "OtherDocumentId": "567 (apenas 3 primeiros dígitos)",
  "Email": "joaosilva@yahoo.com",
  "NotesPatient": "preciso dessa consulta urgente",
  "fromTime": "14:30",
  "toTime": "15:30",
  "IsOnlineScheduling": true,
  "date": "2021-07-15T03:00:00.000Z",
  "Type": "CLOUDIA",
  "Dentist_PersonId": 0,
  "Clinic_BusinessId": 0,
  "AlreadyPatient": true
}
```

**200 — resposta**

```json
[ { "Status": "CREATED", "id": 0 } ]
```

```js
const [sol] = await clinicorp.post("/appointment/create_online_scheduling", {
  CodeLink: 27478,
  PatientName: "Maria Souza",
  SchedulingReason: "Avaliação",
  MobilePhone: "(47) 90000-0000",
  OtherDocumentId: "123",          // só 3 dígitos
  Email: "maria@exemplo.com",
  fromTime: "14:30",
  toTime: "15:30",
  IsOnlineScheduling: true,
  date: "2026-09-15T03:00:00.000Z",
  Type: "CLOUDIA",
  Dentist_PersonId: PROF,
  Clinic_BusinessId: CLINICA,
  AlreadyPatient: false,
});
```

#### `GET /appointment/get_avaliable_days`

Dias com horários disponíveis para o link público de agendamento.

> ⚠️ A rota tem o typo `avaliable` (correto seria `available`). Use como está.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `code_link` | query | string | ✱ | Código de acesso |
| `from` | query | `YYYY-MM-DD` | — | Data inicial |
| `to` | query | `YYYY-MM-DD` | — | Data final |
| `includeHolidays` | query | `"X"` | — | Incluir feriados na listagem |
| `showAvailableTimes` | query | `"X"` | — | Trazer também a lista de horários |

**200 — resposta**

```json
[
  {
    "Date": "YYYY-MM-DD",
    "Week": "Quarta-Feira",
    "DayWeek": "3 (Quarta-Feira)",
    "day": 31,
    "month": 12,
    "year": 2024,
    "jsonDate": "2024-12-31",
    "AvailableTimes": [
      {
        "from": "08:00",
        "to": "08:30",
        "isSelectable": true,
        "isAvailable": true,
        "isFirstActivate": "X",
        "isSelected": true,
        "professionalId": 1234567890
      }
    ]
  }
]
```

`AvailableTimes` só vem preenchido com `showAvailableTimes=X`.

```bash
cc_get "/appointment/get_avaliable_days" \
  "subscriber_id=$SUB&code_link=27478&from=2026-09-01&to=2026-09-30&showAvailableTimes=X"
```

```python
dias = cc.get("/appointment/get_avaliable_days",
              subscriber_id=SUB, code_link="27478",
              showAvailableTimes="X",
              **{"from": "2026-09-01", "to": "2026-09-30"})
livres = [d for d in dias if any(t["isAvailable"] for t in d.get("AvailableTimes", []))]
```

#### `GET /appointment/get_avaliable_times_calendar`

Horários disponíveis de **uma data específica** no link público.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `date` | query | `YYYY-MM-DD` | ✱ | Data selecionada |
| `code_link` | query | string | ✱ | Código de acesso |

**200 — resposta**

```json
[
  {
    "From": "9:00",
    "To": "10:00",
    "DayWeek": 1,
    "BusinessId": 123456789,
    "ProfessionalId": 2345512
  }
]
```

```bash
cc_get "/appointment/get_avaliable_times_calendar" \
  "subscriber_id=$SUB&date=2026-09-15&code_link=27478"
```

#### `GET /appointment/get_appointment`

Detalhes de um agendamento **ou** de uma solicitação de agendamento, pelo id.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `code_link` | query | string | ✱ | Código de acesso |
| `id` | query | integer | ✱ | id do agendamento |

**200 — resposta**

```json
[
  {
    "OtherPhones": "(47) 99999-9999",
    "ShedulingReason": "Dor de dente",
    "AtomicDate": 20210713,
    "CreateUserId": -1,
    "Date": "2021-07-15T18:02:36.132Z",
    "Id": 4791226171916288,
    "Type": "CLOUDIA",
    "MobilePhone": "(47) 98870-0805",
    "SK_DateFirstTime": 920210713,
    "Deleted": "Se tiver com 'X', é porque o agendamento foi deletado ou a solicitação de agendamento recusada",
    "OtherDocumentId": 12345678900,
    "ToTime": "13:00",
    "FromTime": "14:00",
    "Email": "joaosilva@gmail.com",
    "Clinic_BusinessId": 5759793708400640,
    "Dentist_PersonId": 5670262998564864,
    "NotesPatient": "Obs do paciente",
    "PatientName": "Gustavo Blasius",
    "IsOnlineScheduling": true,
    "ShedulingAccepted": false
  }
]
```

| Campo | Leitura |
|---|---|
| `Deleted` = `"X"` | Agendamento deletado **ou** solicitação recusada |
| `ShedulingAccepted` | `true` = solicitação aprovada pela clínica ⚠️ grafia sem o "c" |
| `ShedulingReason` | Motivo da consulta ⚠️ mesma grafia |
| `Id` (maiúsculo) | Aqui o id vem como `Id`, não `id` |

```bash
cc_get "/appointment/get_appointment" \
  "subscriber_id=$SUB&code_link=27478&id=4791226171916288"
```

```python
sol = cc.get("/appointment/get_appointment",
             subscriber_id=SUB, code_link="27478", id=4791226171916288)[0]

if sol.get("Deleted") == "X":
    estado = "recusado/deletado"
elif sol.get("ShedulingAccepted"):
    estado = "aprovado"
else:
    estado = "aguardando aprovação"
```

#### `POST /appointment/confirm_appointment`

Confirma o agendamento (equivale à confirmação do paciente).

**Request body**

```json
{ "subscriber_id": "clinicorp", "id": 5778927598043136 }
```

**200 — resposta**

```json
[
  {
    "Date": "2025-01-30T18:02:36.132Z",
    "AtomicDate": 20250130,
    "PatientName": "Lucas Gonçalves",
    "FromTime": "14:00",
    "ToTime": "13:00",
    "MobilePhone": "(47) 98870-0805",
    "OtherDocumentId": "01234567890",
    "PatientConfirm": "X",
    "PatientMessage": "CONFIRMAR",
    "Email": "lucas.goncalves@gmail.com",
    "CreateUserId": -1,
    "Type": "CLOUDIA",
    "Clinic_BusinessId": 5759793708400640,
    "Dentist_PersonId": 5670262998564864,
    "IsOnlineScheduling": true,
    "OtherPhones": "(47) 99999-9999",
    "ShedulingReason": "Dor de dente",
    "StatusId": 5609543400816640,
    "StatusDescription": "1-Confirmado",
    "id": 4791226171916288
  }
]
```

```bash
cc_post "/appointment/confirm_appointment" \
  '{"subscriber_id":"'"$SUB"'","id":5778927598043136}'
```

```js
const [conf] = await clinicorp.post("/appointment/confirm_appointment", {
  subscriber_id: SUB, id: 5778927598043136,
});
console.log(conf.PatientConfirm === "X" ? "confirmado" : "pendente");
```

#### `POST /appointment/cancel_appointment`

Cancela o agendamento.

**Request body**

```json
{ "subscriber_id": "clinicorp", "id": 5778927598043136 }
```

**200 — resposta**: mesmo formato de `/appointment/get_appointment`.
Após o cancelamento, `Deleted` vem com `"X"`.

```bash
cc_post "/appointment/cancel_appointment" \
  '{"subscriber_id":"'"$SUB"'","id":5778927598043136}'
```

```python
cc.post("/appointment/cancel_appointment",
        {"subscriber_id": SUB, "id": 5778927598043136})
```

---

### 7.8 estimates

#### `GET /estimates/list`

Lista os orçamentos do período, com status, profissional, valor e lista de
procedimentos.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `clinic_id` | query | integer | — | Clínica específica (multiclínicas na mesma unidade) |

> ⚠️ Aqui o filtro de clínica se chama `clinic_id` — não `business_id`.

**200 — resposta**

```json
[
  {
    "PatientId": 0,
    "CreateDate": "2026-08-23",
    "SearchDate": "2026-08-23",
    "Date": "2026-08-23",
    "LastChange_Date": "2026-08-23",
    "BusinessId": 0,
    "ProfessionalId": 0,
    "ProfessionalName": "string",
    "PatientName": "string",
    "PatientMobilePhone": "string",
    "Amount": 0,
    "Status": "string",
    "TreatmentId": 0,
    "id": 0,
    "ProcedureList": [ {} ]
  }
]
```

`TreatmentId` é a chave para buscar o detalhe em `/estimates/get`.

```bash
cc_get "/estimates/list" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

```js
const orcs = await clinicorp.get("/estimates/list", {
  subscriber_id: SUB, from: "2026-08-01", to: "2026-08-31",
});
const porStatus = orcs.reduce((a, o) => {
  a[o.Status] = (a[o.Status] ?? 0) + o.Amount;
  return a;
}, {});
```

```python
orcs = cc.get("/estimates/list", subscriber_id=SUB,
              **{"from": "2026-08-01", "to": "2026-08-31"})
por_prof = {}
for o in orcs:
    por_prof.setdefault(o["ProfessionalName"], 0)
    por_prof[o["ProfessionalName"]] += o["Amount"]
```

#### `GET /estimates/get`

Detalhe de um orçamento específico.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `treatment_id` | query | integer | ✱ | id do orçamento (`TreatmentId` de `/estimates/list`) |

**200 — resposta**

```json
{
  "Patient_PersonId": 0,
  "CreateDate": "2026-08-23",
  "PaymentTypePlan": "string",
  "BusinessId": 0,
  "Dentist_PersonId": 0,
  "CurrentChargePaymentPlanId": 0,
  "Status": "string",
  "id": 0,
  "ProcedureList": [ {} ]
}
```

```bash
cc_get "/estimates/get" "subscriber_id=$SUB&treatment_id=7777777777777777"
```

```python
# hidratar todos os orçamentos aprovados do mês
orcs = cc.get("/estimates/list", subscriber_id=SUB,
              **{"from": "2026-08-01", "to": "2026-08-31"})
detalhes = [cc.get("/estimates/get", subscriber_id=SUB, treatment_id=o["TreatmentId"])
            for o in orcs if o["Status"] == "APPROVED"]
```

---

### 7.9 sales

#### `GET /sales/estimates_and_conversion`

Orçamentos por status, quantidade, valor total, ticket médio e taxa de conversão.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | ✱ | id da clínica |
| `group_by` | query | `"month"` | ✱ | Agrupamento |

**200 — resposta**

```json
[
  {
    "month": "string",
    "Status": {
      "TotalEstimates": 0,
      "TotalEstimatesAmount": 0,
      "AverageTicket": 0
    },
    "Conversion": "string"
  }
]
```

```bash
cc_get "/sales/estimates_and_conversion" \
  "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31&business_id=$CLINICA&group_by=month"
```

```js
const serie = await clinicorp.get("/sales/estimates_and_conversion", {
  subscriber_id: SUB, from: "2026-01-01", to: "2026-12-31",
  business_id: CLINICA, group_by: "month",
});
serie.forEach(m => console.log(m.month, m.Status.AverageTicket, m.Conversion));
```

#### `GET /sales/expertise_revenue`

Vendas por especialidade (mês de referência e valor total por especialidade).

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `businessId` | query | integer | — | id da clínica ⚠️ camelCase aqui |
| `patientId` | query | integer | — | id do paciente |

**200 — resposta**

```json
[
  { "month": "string", "Expertise": "string" }
]
```

```bash
cc_get "/sales/expertise_revenue" "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31"
```

```python
rev = cc.get("/sales/expertise_revenue", subscriber_id=SUB, businessId=CLINICA,
             **{"from": "2026-01-01", "to": "2026-12-31"})
```

---

### 7.10 payment

#### `GET /payment/list`

Lista analítica de todos os pagamentos do período. É a fonte mais detalhada de
recebimentos da API.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `include_total_amount` | query | `"X"` | — | Traz o valor total (`TotalPostAmount`) |
| `get_amount_with_discounts` | query | `"X"` | — | Traz o valor líquido de taxas (`AmountWithDiscounts`) |
| `date_type` | query | string | — | Qual data filtrar (ver abaixo) |

##### `date_type`

| Valor | Filtra por |
|---|---|
| *(vazio / omitido)* | **Data de recebimento** — comportamento padrão |
| `postDate` | Data de criação do lançamento |
| `checkoutDate` | Data de pagamento (checkout) |

Essa escolha muda completamente o resultado. Para conciliação contábil por regime
de caixa, use o padrão (recebimento); para acompanhar vendas, `checkoutDate`.

**200 — resposta**

```json
[
  {
    "id": 0,
    "PaymentReceived": "string",
    "DueDateAtomic": 0,
    "CheckOutDate": "2026-08-23",
    "Amount": 0,
    "DueDate": "2026-08-23",
    "ReceiverBusinessId": 0,
    "CheckOutAtomicTime": 0,
    "PaymentDate": "2026-08-23",
    "PaymentConfirmed": "string",
    "ConfirmedDate": "2026-08-23",
    "ConfirmedDateAtomic": 0,
    "InstallmentsCount": "2026-08-23",
    "z_LastChange_UserId": 0,
    "CheckOutUserId": 0,
    "InstallmentNumber": "string",
    "PostDate": "2026-08-23",
    "CheckOutDateAtomic": "string",
    "PatientId": 0,
    "PaymentHeaderId": 0,
    "ReceivedDateAtomic": 0,
    "ReceivedDate": "2026-08-23",
    "PostDateAtomic": "string",
    "z_LastChange_Date": "2026-08-23",
    "PaymentForm": "string",
    "PatientName": "string",
    "TreatmentId": 0,
    "TotalPostAmount": 0,
    "AmountWithDiscounts": 0
  }
]
```

| Campo | Leitura |
|---|---|
| `PaymentReceived` | `"X"` = recebido |
| `PaymentConfirmed` | `"X"` = confirmado |
| `InstallmentNumber` / `InstallmentsCount` | Parcela N de M |
| `PaymentForm` | Forma de pagamento (dinheiro, cartão, boleto…) |
| `TreatmentId` | Liga o pagamento ao orçamento |
| `AmountWithDiscounts` | Só vem com `get_amount_with_discounts=X` |

```bash
cc_get "/payment/list" \
  "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31&include_total_amount=X&get_amount_with_discounts=X"
```

```js
const pags = await clinicorp.get("/payment/list", {
  subscriber_id: SUB,
  from: "2026-08-01",
  to:   "2026-08-31",
  include_total_amount: "X",
  get_amount_with_discounts: "X",
  date_type: "checkoutDate",
});

const liquido = pags
  .filter(p => p.PaymentReceived === "X")
  .reduce((s, p) => s + (p.AmountWithDiscounts ?? p.Amount), 0);
```

```python
pags = cc.get("/payment/list", subscriber_id=SUB,
              include_total_amount="X", get_amount_with_discounts="X",
              **{"from": "2026-08-01", "to": "2026-08-31"})

por_forma = {}
for p in pags:
    if p.get("PaymentReceived") == "X":
        por_forma[p["PaymentForm"]] = por_forma.get(p["PaymentForm"], 0) + p["Amount"]
```

#### `GET /payment/list_reconcile_claim`

Faturamentos por plano de saúde (convênio), com status de glosa/recurso.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | data | ✱ | Data início |
| `to` | query | data | ✱ | Data fim |
| `type` | query | enum | ✱ | Status do faturamento |

##### Valores de `type`

| Valor | Significado |
|---|---|
| `ALL` | Todos |
| `OPEN` | Em aberto |
| `DISPUTE` | Recurso |
| `REJECT` | Glosa |
| `PARTIAL_PAID` | Pagamento parcial *(no spec: "Pagsmento Parcial" — typo)* |
| `PAID` | Pago |

**200 — resposta**

```json
[
  {
    "id": 6666666666666666,
    "AtomicDate": 20220101,
    "Amount": 99.99,
    "ClaimNumber": 222,
    "PersonId": 8888888888888888,
    "PatientName": "João da Silva",
    "TreatmentId": 7777777777777777,
    "ProcedureName": "Restauração coroa",
    "PriceListName": "Tabela de preço 1"
  }
]
```

```bash
cc_get "/payment/list_reconcile_claim" \
  "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31&type=REJECT"
```

```python
glosas = cc.get("/payment/list_reconcile_claim", subscriber_id=SUB, type="REJECT",
                **{"from": "2026-08-01", "to": "2026-08-31"})
total_glosado = sum(g["Amount"] for g in glosas)
```

---

### 7.11 financial

Todos os endpoints deste grupo compartilham a mesma assinatura de período.
A diferença está em `business_id` ser obrigatório ou não — atenção.

| Endpoint | `business_id` |
|---|---|
| `/financial/list_summary` | opcional |
| `/financial/list_invoices` | opcional |
| `/financial/list_receipt` | opcional |
| `/financial/list_cash_flow` | **obrigatório** |
| `/financial/list_payments` | **obrigatório** |
| `/financial/average_installments` | **obrigatório** |

#### `GET /financial/list_summary`

Resumo financeiro do período: total de vendas, receitas, despesas, formas de
pagamento e lista detalhada de lançamentos.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |

**200 — resposta**

```json
{
  "From": "2026-08-01",
  "To": "2026-08-31",
  "BusinessId": 0,
  "TotalSales": 0,
  "TotalIncome": 0,
  "TotalExpenses": 0,
  "Type": "string",
  "values": [ {} ]
}
```

`values` traz os lançamentos detalhados (descrição, valor, forma de pagamento).

```bash
cc_get "/financial/list_summary" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

```python
res = cc.get("/financial/list_summary", subscriber_id=SUB,
             **{"from": "2026-08-01", "to": "2026-08-31"})
margem = (res["TotalIncome"] - res["TotalExpenses"]) / max(res["TotalIncome"], 1)
```

#### `GET /financial/list_cash_flow`

Fluxo de caixa: entradas, saídas, previsões e quebra por meio de pagamento.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | ✱ | id da clínica |

**200 — resposta**

```json
{
  "in": 0,
  "out": 0,
  "in_forecast": 0,
  "out_forecast": 0,
  "month": "string",
  "cash": 0,
  "bank_slip": 0,
  "credit_card": 0,
  "debit_card": 0,
  "check": 0,
  "transfer": 0,
  "debit": 0
}
```

| Campo | Significado |
|---|---|
| `in` / `out` | Entradas e saídas realizadas |
| `in_forecast` / `out_forecast` | Previsto a receber / a pagar |
| `cash`, `bank_slip`, `credit_card`, `debit_card`, `check`, `transfer` | Recebido por meio de pagamento (dinheiro, boleto, crédito, débito, cheque, transferência) |
| `debit` | Saldo devedor |

```bash
cc_get "/financial/list_cash_flow" \
  "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31&business_id=$CLINICA"
```

```js
const fc = await clinicorp.get("/financial/list_cash_flow", {
  subscriber_id: SUB, from: "2026-08-01", to: "2026-08-31", business_id: CLINICA,
});
console.log("saldo realizado:", fc.in - fc.out);
console.log("saldo projetado:", (fc.in + fc.in_forecast) - (fc.out + fc.out_forecast));
```

#### `GET /financial/list_payments`

Totais consolidados de pagamentos: previsto, recebido e inadimplência.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | ✱ | id da clínica |

**200 — resposta**

```json
{
  "totalInForecastAmount": 0,
  "totalPaymentsAmount": 0,
  "totalDebitAmount": 0
}
```

```bash
cc_get "/financial/list_payments" \
  "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31&business_id=$CLINICA"
```

```python
p = cc.get("/financial/list_payments", subscriber_id=SUB, business_id=CLINICA,
           **{"from": "2026-08-01", "to": "2026-08-31"})
inadimplencia = p["totalDebitAmount"] / max(p["totalInForecastAmount"], 1)
```

#### `GET /financial/list_invoices`

Pagamentos com nota fiscal emitida.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |

**200 — resposta**

```json
[
  {
    "ReferenceId": 0,
    "Amount": 0,
    "Description": "string",
    "PatientName": "string",
    "PatientId": 0,
    "Date": "2026-08-23",
    "InvoiceId": 0,
    "Status": "string",
    "PaymentReceived": "string",
    "PaymentConfirmed": "string",
    "InstallmentNumber": 0,
    "ReceiverBusinessId": 0
  }
]
```

```bash
cc_get "/financial/list_invoices" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

#### `GET /financial/list_receipt`

Recibos emitidos no período.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |

**200 — resposta**

```json
[
  {
    "id": 0,
    "ReferenceId": 0,
    "Amount": 0,
    "Description": "string",
    "PatientName": "string",
    "PatientId": 0,
    "ReceiptDate": "2026-08-23",
    "ReceiverBusinessId": 0
  }
]
```

```bash
cc_get "/financial/list_receipt" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

#### `GET /financial/average_installments`

Parcelamento médio: total de pagamentos, total de parcelas e média.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | ✱ | id da clínica |
| `group_by` | query | `"month"` | ✱ | Agrupamento por mês |

**200 — resposta**

```json
[
  {
    "month": "string",
    "TotalPayments": 0,
    "TotalInstallments": 0,
    "AverageInstallments": 0
  }
]
```

```bash
cc_get "/financial/average_installments" \
  "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31&business_id=$CLINICA&group_by=month"
```

```python
serie = cc.get("/financial/average_installments", subscriber_id=SUB,
               business_id=CLINICA, group_by="month",
               **{"from": "2026-01-01", "to": "2026-12-31"})
```

---

### 7.12 analytics

#### `GET /analytics/list_results`

Painel consolidado por clínica — o endpoint mais denso da API. Um único
`GET` devolve orçamentos por status, receita, despesas, agendamentos, conversão
e ticket médio. Ideal como base de um dashboard.

> Inclui **clínicas inativas** que tiveram movimento no período.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |

**200 — resposta** (um objeto por clínica)

```json
[
  {
    "TotalRevenueAmount": 0,
    "EstimatesTotalAmount": 0,
    "EstimatesTotalQuantity": 0,
    "EstimatesApprovedAmount": 0,
    "EstimatesApprovedQuantity": 0,
    "EstimatesOpenAmount": 0,
    "EstimatesOpenQuantity": 0,
    "EstimatesFollowUpAmount": 0,
    "EstimatesFollowUpQuantity": 0,
    "EstimatesRejectedAmount": 0,
    "EstimatesRejectedQuantity": 0,
    "ApprovedTicketAverage": 0,
    "BusinessId": 0,
    "ConversionRate": 0,
    "TotalReceivedAmount": 0,
    "TotalExpenses": 0,
    "AppointmentsTotal": 0,
    "AppoinmentsFinished": 0,
    "AppointmentsMissed": 0,
    "AppointmentsNewPatients": 0,
    "AppointmentsExistingPatients": 0,
    "WithoutCategory": 0,
    "UnityName": "string"
  }
]
```

| Grupo de campos | Leitura |
|---|---|
| `Estimates*Amount` / `Estimates*Quantity` | Orçamentos por status: total, aprovado, aberto, follow-up, rejeitado |
| `ApprovedTicketAverage` | Ticket médio dos aprovados |
| `ConversionRate` | Taxa de conversão de orçamento |
| `TotalRevenueAmount` / `TotalReceivedAmount` | Vendas x efetivamente recebido |
| `TotalExpenses` | Despesas |
| `Appointments*` | Agendados, finalizados, faltas, novos e recorrentes |
| `UnityName` | Nome da unidade |

> ⚠️ `AppoinmentsFinished` — grafia sem o "t".

```bash
cc_get "/analytics/list_results" "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31"
```

```js
const painel = await clinicorp.get("/analytics/list_results", {
  subscriber_id: SUB, from: "2026-08-01", to: "2026-08-31",
});

painel
  .sort((a, b) => b.TotalRevenueAmount - a.TotalRevenueAmount)
  .forEach(u => console.log(
    u.UnityName,
    "receita", u.TotalRevenueAmount,
    "conv", (u.ConversionRate * 100).toFixed(1) + "%",
    "faltas", u.AppointmentsMissed,
  ));
```

```python
painel = cc.get("/analytics/list_results", subscriber_id=SUB,
                **{"from": "2026-08-01", "to": "2026-08-31"})

for u in sorted(painel, key=lambda x: -x["TotalRevenueAmount"]):
    taxa_falta = u["AppointmentsMissed"] / max(u["AppointmentsTotal"], 1)
    print(f'{u["UnityName"]:<25} R$ {u["TotalRevenueAmount"]:>12,.2f}  '
          f'conv {u["ConversionRate"]:.1%}  falta {taxa_falta:.1%}')
```

---

### 7.13 operational

Ambos os endpoints exigem `isAPI=X` para devolver o JSON no formato da API.

#### `GET /operational/list_sales_goals`

Metas de venda configuradas por mês, total vendido e projeção.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | ✱ | id da clínica |
| `isAPI` | query | `"X"` | ✱ | Formata a resposta para a API |

**200 — resposta**

```json
[
  {
    "month": "string",
    "From": "string",
    "To": "string",
    "Goal": 0,
    "TotalRevenueAmount": 0,
    "Projection": 0
  }
]
```

```bash
cc_get "/operational/list_sales_goals" \
  "subscriber_id=$SUB&from=2026-01-01&to=2026-12-31&business_id=$CLINICA&isAPI=X"
```

```python
metas = cc.get("/operational/list_sales_goals", subscriber_id=SUB,
               business_id=CLINICA, isAPI="X",
               **{"from": "2026-01-01", "to": "2026-12-31"})

for m in metas:
    atingimento = m["TotalRevenueAmount"] / max(m["Goal"], 1)
    print(m["month"], f"{atingimento:.0%}", "projeção:", m["Projection"])
```

#### `GET /operational/list_misses_goals`

Metas de falta do período e total de faltas realizadas.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |
| `from` | query | `YYYY-MM-DD` | ✱ | Data inicial |
| `to` | query | `YYYY-MM-DD` | ✱ | Data final |
| `business_id` | query | integer | — | Clínica específica |
| `isAPI` | query | `"X"` | ✱ | Formata a resposta para a API |

**200 — resposta**

```json
{
  "From": "2026-08-01",
  "To": "2026-08-31",
  "month": "string",
  "Goal": 0,
  "Misses": 0
}
```

```bash
cc_get "/operational/list_misses_goals" \
  "subscriber_id=$SUB&from=2026-08-01&to=2026-08-31&isAPI=X"
```

---

### 7.14 crm

#### `POST /crm/add_leads`

Insere um lead externo em uma campanha do CRM. É o gancho para conectar
formulários de site, Meta Ads, WhatsApp ou landing pages ao funil do Clinicorp.

**Request body**

| Campo | Tipo | Descrição |
|---|---|---|
| `subscriber_id` | string | id do assinante |
| `Name` | string | Nome do lead |
| `Email` | string | E-mail |
| `Phone` | string | Telefone |
| `BoardName` | string | **Nome** da campanha (não o id) |
| `Notes` | string | Observações do lead |

```json
{
  "subscriber_id": "id do assinante",
  "Name": "Nome do lead",
  "Email": "paciente_teste@gmail.com",
  "Phone": "(47) 90000-0000",
  "BoardName": "Nome da campanha",
  "Notes": "Observações do lead"
}
```

> ⚠️ `BoardName` é o **nome** da campanha, casado por string. Busque o nome exato
> em `/crm/list_active_campaigns` antes de enviar — nome errado não gera erro claro.

**200 — resposta**

```json
{ "Message": "string", "Error": "string" }
```

> ⚠️ Este endpoint devolve `Error` **dentro de um `200`**. Verifique o corpo, não
> apenas o status HTTP.

```bash
cc_post "/crm/add_leads" '{
  "subscriber_id":"'"$SUB"'",
  "Name":"Maria Souza",
  "Email":"maria@exemplo.com",
  "Phone":"(47) 90000-0000",
  "BoardName":"Campanha Setembro",
  "Notes":"Veio do formulário do site"
}'
```

```js
const r = await clinicorp.post("/crm/add_leads", {
  subscriber_id: SUB,
  Name: "Maria Souza",
  Email: "maria@exemplo.com",
  Phone: "(47) 90000-0000",
  BoardName: "Campanha Setembro",
  Notes: "Veio do formulário do site",
});
if (r.Error) throw new Error(`Lead não inserido: ${r.Message}`);
```

```python
r = cc.post("/crm/add_leads", {
    "subscriber_id": SUB,
    "Name": "Maria Souza",
    "Email": "maria@exemplo.com",
    "Phone": "(47) 90000-0000",
    "BoardName": "Campanha Setembro",
    "Notes": "Veio do formulário do site",
})
if r.get("Error"):
    raise RuntimeError(r.get("Message"))
```

#### `GET /crm/list_active_campaigns`

Lista as campanhas ativas do CRM.

> A descrição no spec está errada ("Lista todos os usuários do sistema") —
> o endpoint retorna campanhas.

| Parâmetro | Local | Tipo | Obrig. | Descrição |
|---|---|---|---|---|
| `subscriber_id` | query | string | ✱ | id do Assinante |

**200 — resposta**

```json
[
  { "Name": "string", "Status": "string", "Description": "string" }
]
```

```bash
cc_get "/crm/list_active_campaigns" "subscriber_id=$SUB"
```

```python
camps = cc.get("/crm/list_active_campaigns", subscriber_id=SUB)
nomes = [c["Name"] for c in camps]   # use um destes em BoardName
```

---

### 7.15 products

#### `POST /products/orders`

Cria uma ordem de compra de produtos/insumos para uma clínica. Único endpoint da
API com validação estruturada (estilo Zod) e códigos `404`/`500` documentados.

**Request body**

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `clinic` | string | ✱ | Identificador da clínica |
| `orderCode` | string | ✱ | Código da ordem no seu sistema |
| `orderDate` | `YYYY-MM-DD` | ✱ | Data da ordem |
| `products` | array | ✱ | Itens da ordem (ver abaixo) |

**Item de `products`**

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `code` | string | ✱ | Código do produto |
| `name` | string | ✱ | Nome |
| `description` | string | — | Descrição |
| `quantity` | number | ✱ | Quantidade |
| `unitPrice` | number | ✱ | Preço unitário |
| `unitOfMeasurement` | string | — | Unidade (ex.: `UN`, `CX`, `ML`) |
| `expirationDate` | `YYYY-MM-DD` | — | Validade |
| `lot` | string | — | Lote |
| `brand` | string | — | Marca |
| `supplier` | string | — | Fornecedor |
| `storageLocation` | string | — | Local de armazenamento |
| `notes` | string | — | Observações |

```json
{
  "clinic": "12345678901234",
  "orderCode": "ORDER123",
  "orderDate": "2024-10-24",
  "products": [
    {
      "code": "PROD001",
      "name": "Seringa 10ml",
      "description": "Seringa descartável de 10ml",
      "quantity": 100,
      "unitPrice": 3.5,
      "unitOfMeasurement": "UN",
      "expirationDate": "2025-12-31",
      "lot": "LOT2023A",
      "brand": "Becton Dickinson",
      "supplier": "Fornecedor A",
      "storageLocation": "Depósito 1",
      "notes": "Manter em temperatura ambiente"
    }
  ]
}
```

**Respostas**

| Código | Corpo |
|---|---|
| `201` | `{ "success": true }` |
| `400` | `{ "Error": 400, "Message": [ …erros de validação… ] }` |
| `404` | `{ "Error": 404, "Message": "Clínica não encontrada." }` |
| `500` | `{ "Error": 500, "Message": "Erro interno do servidor." }` |

> ⚠️ Sucesso aqui é **`201`**, não `200`.

```bash
cc_post "/products/orders" '{
  "clinic":"12345678901234",
  "orderCode":"ORDER123",
  "orderDate":"2026-08-23",
  "products":[{"code":"PROD001","name":"Seringa 10ml","quantity":100,"unitPrice":3.5,"unitOfMeasurement":"UN"}]
}'
```

```js
try {
  const r = await clinicorp.post("/products/orders", {
    clinic: "12345678901234",
    orderCode: "ORDER123",
    orderDate: "2026-08-23",
    products: [
      { code: "PROD001", name: "Seringa 10ml", quantity: 100,
        unitPrice: 3.5, unitOfMeasurement: "UN" },
    ],
  });
  console.log(r.success);
} catch (e) {
  // Message pode ser array de erros de validação
  console.error(e.message);
}
```

```python
try:
    r = cc.post("/products/orders", {
        "clinic": "12345678901234",
        "orderCode": "ORDER123",
        "orderDate": "2026-08-23",
        "products": [{
            "code": "PROD001", "name": "Seringa 10ml",
            "quantity": 100, "unitPrice": 3.5, "unitOfMeasurement": "UN",
        }],
    })
except ClinicorpError as e:
    if isinstance(e.message, list):
        for err in e.message:
            print("campo", ".".join(map(str, err["path"])), "→", err["message"])
    raise
```

---

### 7.16 upload

#### `POST /file/upload`

Envia arquivos, imagens e documentos para o sistema, vinculando-os a um paciente.
O corpo é um **array** — permite lote.

**Request body** (array de objetos)

| Campo | Tipo | Descrição |
|---|---|---|
| `ResponseWebhookUrl` | string | URL que receberá o callback com o resultado |
| `Url` | string | URL pública do arquivo a ser baixado e importado |
| `LocalFile` | enum | Onde anexar (ver abaixo) |
| `PatientName` | string | Nome do paciente |
| `PatinetId` | integer | id do paciente ⚠️ **grafia com typo no spec** |

##### Valores de `LocalFile`

| Valor | Destino |
|---|---|
| `Person.Profile` | Foto de perfil |
| `Person.Photo` | Galeria de fotos |
| `Person.Document` | Documentos |
| `Person.File` | Arquivos gerais |

```json
[
  {
    "ResponseWebhookUrl": "https://webhook...",
    "Url": "https://image...",
    "LocalFile": "Person.Profile",
    "PatientName": "Patient Name",
    "PatinetId": 92302392323
  }
]
```

**200 — resposta**

```json
[
  {
    "PatientName": "Patient Name",
    "Url": "https://image...",
    "LocalFile": "Person.Profile",
    "Status": "SUCCESS"
  }
]
```

> ⚠️ O upload é **por URL**, não multipart. O arquivo precisa estar acessível
> publicamente (ou por URL assinada) no momento da chamada.
> `ResponseWebhookUrl` é o único mecanismo de callback da API — use-o para saber
> quando o processamento terminou.

```bash
cc_post "/file/upload" '[{
  "ResponseWebhookUrl":"https://meusistema.com/hooks/clinicorp",
  "Url":"https://cdn.meusistema.com/raiox/123.jpg",
  "LocalFile":"Person.Document",
  "PatientName":"Maria Souza",
  "PatinetId":92302392323
}]'
```

```js
const r = await clinicorp.post("/file/upload", [{
  ResponseWebhookUrl: "https://meusistema.com/hooks/clinicorp",
  Url: "https://cdn.meusistema.com/raiox/123.jpg",
  LocalFile: "Person.Document",
  PatientName: "Maria Souza",
  PatinetId: pacienteId,          // typo é do spec, mantenha
}]);
```

```python
r = cc.post("/file/upload", [{
    "ResponseWebhookUrl": "https://meusistema.com/hooks/clinicorp",
    "Url": "https://cdn.meusistema.com/raiox/123.jpg",
    "LocalFile": "Person.Document",
    "PatientName": "Maria Souza",
    "PatinetId": paciente_id,     # typo é do spec, mantenha
}])
```

---

### 7.17 migration

Grupo usado na **migração de dados** de outro software para o Clinicorp. Fluxo
típico: obter URL assinada → subir o arquivo → registrar a migração.

#### `POST /migration/file/upload`

Retorna uma URL assinada para upload do arquivo de banco de dados.

**Request body** (array)

```json
[
  {
    "SubscriptionId": "clinicorp",
    "DataAccess": { "FileName": "database.fdb" }
  }
]
```

**200 — resposta**

```json
[
  {
    "SubscriptionId": "clinicorp",
    "UploadSignedUrl": "https://google.com/clinicorp"
  }
]
```

Envie o arquivo para `UploadSignedUrl` com um `PUT` (fora da API Clinicorp).

```bash
RESP=$(cc_post "/migration/file/upload" \
  '[{"SubscriptionId":"clinicorp","DataAccess":{"FileName":"database.fdb"}}]')
URL=$(echo "$RESP" | jq -r '.[0].UploadSignedUrl')
curl -X PUT --upload-file ./database.fdb "$URL"
```

#### `POST /migration/file`

Cria uma ou várias migrações a partir de arquivos já enviados.

**Request body** (array)

| Campo | Descrição |
|---|---|
| `SubscriptionId` | id da assinatura de destino |
| `DataAccess.FileName` | Nome do arquivo enviado |
| `DataAccess.DatabaseType` | Tipo do banco — ex.: `firebird` |
| `DataAccess.MigrationType` | Tipo de migração — ex.: `migration A` |

```json
[
  {
    "SubscriptionId": "clinicorp",
    "DataAccess": {
      "FileName": "database.fdb",
      "DatabaseType": "firebird",
      "MigrationType": "migration A"
    }
  }
]
```

**200 — resposta**

```json
[ { "SubscriptionId": "clinicorp", "Status": "SUCCESS" } ]
```

#### `POST /migration/connection`

Cria migrações conectando diretamente ao banco de origem.

**Request body** (array)

| Campo | Descrição |
|---|---|
| `SubscriptionId` | id da assinatura de destino |
| `DataAccess.DatabaseType` | Ex.: `mariaDB` |
| `DataAccess.MigrationType` | Ex.: `migration B` |
| `DataAccess.Host` | Host do banco |
| `DataAccess.Database` | Nome do banco |
| `DataAccess.User` | Usuário |
| `DataAccess.Password` | Senha |

```json
[
  {
    "SubscriptionId": "clinicorp",
    "DataAccess": {
      "DatabaseType": "mariaDB",
      "MigrationType": "migration B",
      "Host": "183.254...",
      "Password": "myPassword",
      "Database": "My Database",
      "User": "admin"
    }
  }
]
```

**200 — resposta**

```json
[ { "SubscriptionId": "clinicorp", "Status": "SUCCESS" } ]
```

> 🔐 Este payload trafega **credenciais de banco em texto claro**. Use apenas em
> ambiente controlado, prefira usuário somente-leitura com escopo mínimo, e
> revogue as credenciais assim que a migração terminar.

---

## 8. Receitas — fluxos completos

### 8.1 Bootstrap: descobrir os ids da conta

Antes de qualquer integração, colete os identificadores.

```python
cc = Clinicorp()

# 1. Franquia? descubra as unidades
unidades = cc.get("/group/list_subscribers")          # → SubscriberBussinessUID

SUB = "seu_subscriber_id"

# 2. Clínicas do assinante
clinicas = cc.get("/business/list", subscriber_id=SUB)
CLINICA = clinicas[0]["id"]

# 3. Profissionais
profs = cc.get("/professional/list_all_professionals")

# 4. Status de agendamento (para change_status)
status = cc.get("/appointment/status_list", subscriber_id=SUB)
STATUS = {s["Type"]: s["id"] for s in status}

# 5. Grade de funcionamento e slot
grade = cc.get("/group/list_subscribers_clinics")
```

### 8.2 Agendamento online ponta a ponta (link público)

```js
const CODE_LINK = "27478";

// 1. Dias com vaga no mês
const dias = await clinicorp.get("/appointment/get_avaliable_days", {
  subscriber_id: SUB,
  code_link: CODE_LINK,
  from: "2026-09-01",
  to:   "2026-09-30",
  showAvailableTimes: "X",
});

// 2. Horários de um dia escolhido
const horarios = await clinicorp.get("/appointment/get_avaliable_times_calendar", {
  subscriber_id: SUB, code_link: CODE_LINK, date: "2026-09-15",
});

const slot = horarios[0];   // { From, To, BusinessId, ProfessionalId }

// 3. Criar a solicitação
const [sol] = await clinicorp.post("/appointment/create_online_scheduling", {
  CodeLink: Number(CODE_LINK),
  PatientName: "Maria Souza",
  SchedulingReason: "Avaliação inicial",
  MobilePhone: "(47) 90000-0000",
  OtherDocumentId: "123",                 // só os 3 primeiros dígitos do CPF
  Email: "maria@exemplo.com",
  NotesPatient: "Preferência pela manhã",
  fromTime: slot.From,
  toTime:   slot.To,
  IsOnlineScheduling: true,
  date: "2026-09-15T03:00:00.000Z",
  Type: "CLOUDIA",
  Dentist_PersonId: slot.ProfessionalId,
  Clinic_BusinessId: slot.BusinessId,
  AlreadyPatient: false,
});

// 4. Acompanhar (polling — não há webhook)
const [det] = await clinicorp.get("/appointment/get_appointment", {
  subscriber_id: SUB, code_link: CODE_LINK, id: sol.id,
});

const estado = det.Deleted === "X"
  ? "recusado"
  : det.ShedulingAccepted ? "aprovado" : "aguardando";
```

### 8.3 Cadastrar paciente sem duplicar + agendar

```python
def upsert_paciente(cc, sub, cpf, nome, **extra):
    achado = cc.get("/patient/get", subscriber_id=sub, OtherDocumentId=cpf)
    if (achado or {}).get("PatientId"):
        return achado["PatientId"]

    novo = cc.post("/patient/create", {
        "subscriber_id": sub,
        "Name": nome,
        "OtherDocumentId": cpf,
        **extra,
    })
    return novo.get("PatientId") or novo.get("id")


paciente_id = upsert_paciente(
    cc, SUB, "12345678900", "Maria Souza",
    BirthDate="1988-04-22", Sex="F", MobilePhone="47990000000",
)

cc.post("/appointment/create_appointment_by_api", {
    "Patient_PersonId": paciente_id,
    "PatientName": "Maria Souza",
    "fromTime": "10:00",
    "toTime": "11:00",
    "date": "2026-09-15T03:00:00.000Z",
    "Clinic_BusinessId": CLINICA,
    "Dentist_PersonId": PROF,
    "Procedures": "Avaliação",
})
```

### 8.4 Confirmação de consultas do dia seguinte (rotina diária)

```python
from datetime import date, timedelta

amanha = (date.today() + timedelta(days=1)).isoformat()

agenda = cc.get("/appointment/list", subscriber_id=SUB,
                **{"from": amanha, "to": amanha})

pendentes = [
    a for a in agenda
    if a["ItemType"] == "APPOINTMENT"
    and a.get("Canceled") != "X" and a.get("Deleted") != "X"
    and a.get("StatusId") != STATUS.get("CONFIRMED")
]

for a in pendentes:
    enviar_whatsapp(a["MobilePhone"], a["PatientName"], a["fromTime"])

# depois que o paciente responder:
# cc.get("/appointment/change_status", id=a["id"], status_id=STATUS["CONFIRMED"])
```

### 8.5 Ocupação real da agenda (com compromissos e eventos)

Para capacidade instalada, `includeAssigns=X` é obrigatório — sem ele os
bloqueios de agenda ficam invisíveis e a ocupação sai subestimada.

```python
agenda = cc.get("/appointment/list", subscriber_id=SUB,
                includeAssigns="X",
                **{"from": "2026-08-01", "to": "2026-08-31"})

def minutos(item):
    h1, m1 = map(int, item["fromTime"].split(":"))
    h2, m2 = map(int, item["toTime"].split(":"))
    return (h2 * 60 + m2) - (h1 * 60 + m1)

ocupado = sum(minutos(i) for i in agenda
              if i.get("AllDay") != "X"
              and i.get("Canceled") != "X" and i.get("Deleted") != "X")

# comparar com o cálculo oficial do Clinicorp:
oficial = cc.get("/appointment/schedule_occupation", subscriber_id=SUB,
                 group_by="month",
                 **{"from": "2026-08-01", "to": "2026-08-31"})
print(oficial[0]["Ocupaccion"], "|", ocupado, "min calculados")
```

### 8.6 Dashboard mensal em uma chamada

```js
async function dashboardMensal(sub, from, to) {
  const [painel, ocupacao, agendamentos] = await Promise.all([
    clinicorp.get("/analytics/list_results", { subscriber_id: sub, from, to }),
    clinicorp.get("/appointment/schedule_occupation",
      { subscriber_id: sub, from, to, group_by: "month" }),
    clinicorp.get("/appointment/list_info", { subscriber_id: sub, from, to }),
  ]);

  return painel.map(u => ({
    unidade:      u.UnityName,
    receita:      u.TotalRevenueAmount,
    recebido:     u.TotalReceivedAmount,
    despesas:     u.TotalExpenses,
    ticketMedio:  u.ApprovedTicketAverage,
    conversao:    u.ConversionRate,
    agendamentos: u.AppointmentsTotal,
    faltas:       u.AppointmentsMissed,
    novosPacientes: u.AppointmentsNewPatients,
    ocupacao:     ocupacao[0]?.Ocupaccion,
    primeiras:    agendamentos.FirsAppointmentTotal,
  }));
}
```

### 8.7 Sincronização incremental (sem webhooks)

A API não notifica mudanças. O padrão viável é polling com janela deslizante,
usando `z_LastChange_Date` para detectar alterações retroativas.

```python
from datetime import date, timedelta

def sincronizar(cc, sub, dias_retroativos=7):
    """Reprocessa uma janela para capturar edições em registros antigos."""
    hoje = date.today()
    inicio = (hoje - timedelta(days=dias_retroativos)).isoformat()
    fim = (hoje + timedelta(days=60)).isoformat()

    agenda = cc.get("/appointment/list", subscriber_id=sub,
                    includeAssigns="X", includeCanceled="X", includeDeleted="X",
                    **{"from": inicio, "to": fim})

    for item in agenda:
        upsert_local(item)          # chave: (ItemType, id)
        # z_LastChange_Date permite pular o que não mudou
```

> Regras de ouro:
> - Traga `includeCanceled=X` e `includeDeleted=X` na sincronização, senão
>   cancelamentos ficam "fantasmas" na sua base.
> - Use `z_LastChange_Date` para decidir o que reescrever.
> - Janelas de no máximo 1–3 meses por chamada em clínicas de alto volume.

---

## 9. Pegadinhas e inconsistências conhecidas

Lista de armadilhas reais do spec. Todas foram verificadas contra a documentação
publicada — **use os nomes como estão**, mesmo quando parecerem errados.

### 9.1 Autenticação

| Problema | O que fazer |
|---|---|
| O security scheme se chama `bearerAuth` mas o `scheme` é `basic` | Use `Authorization: Basic`, nunca `Bearer` |

### 9.2 Typos nas rotas

| Rota publicada | Grafia "correta" |
|---|---|
| `/appointment/get_avaliable_days` | ~~available~~ |
| `/appointment/get_avaliable_times_calendar` | ~~available~~ |

### 9.3 Typos em campos de resposta

| Campo publicado | Onde | Esperado |
|---|---|---|
| `SubscriberBussinessUID` | `/group/*` | ~~Business~~ |
| `FirsAppointmentTotal` | `/appointment/list_info` | ~~First~~ |
| `AppoinmentsFinished` | `/analytics/list_results` | ~~Appointments~~ |
| `Ocupaccion` | `/appointment/schedule_occupation` | ~~Occupation~~ |
| `StatusDescrition` | `/appointment/change_status` | ~~Description~~ |
| `ShedulingReason` | `/appointment/get_appointment` | ~~Scheduling~~ |
| `ShedulingAccepted` | `/appointment/get_appointment` | ~~Scheduling~~ |
| `PatinetId` | `/file/upload` (**request**) | ~~Patient~~ |

`PatinetId` é o mais perigoso: é campo de **envio**. Escrever "PatientId"
faz o vínculo com o paciente falhar silenciosamente.

### 9.4 O mesmo conceito com nomes diferentes

| Conceito | Grafias em uso |
|---|---|
| id da clínica | `business_id`, `businessId`, `Clinic_BusinessId`, `clinic_id`, `BusinessId`, `ReceiverBusinessId`, `clinic` |
| id do paciente | `PatientId`, `patientId`, `Patient_PersonId`, `PersonId`, `PatinetId` |
| id do profissional | `professionalId`, `ProfessionalId`, `Dentist_PersonId` |
| id do orçamento | `treatment_id`, `TreatmentId` |
| id do agendamento | `id`, `Id` |

Recomendação: crie uma camada de normalização no seu client e **não** compartilhe
o mesmo objeto de parâmetros entre endpoints diferentes.

### 9.5 Semântica HTTP

| Comportamento | Detalhe |
|---|---|
| `GET /appointment/change_status` altera estado | Não colocar atrás de cache, prefetch ou retry automático |
| `POST /products/orders` responde `201` | Não trate só `200` como sucesso |
| `POST /crm/add_leads` devolve `Error` dentro de `200` | Sempre inspecione o corpo |
| `Message` do `400` de `/products/orders` é array | Trate `string \| array` |
| `400` de `/appointment/create_appointment_by_api` não tem corpo padronizado | Faça fallback para `statusText` |

### 9.6 Datas

| Armadilha | Detalhe |
|---|---|
| `/business/list_available_times` usa `YYYYMMDD` | Todo o resto usa `YYYY-MM-DD` |
| `date` de agendamentos vem em **UTC** | Converta para o fuso da clínica antes de exibir |
| `AtomicDate` de eventos usa o fuso **da clínica** | Não converta |
| Exemplo de `list_available_times` traz `toTime` < `fromTime` | Erro do exemplo; leia por nome do campo |
| `InstallmentsCount` é tipado como data no schema | É um contador de parcelas |

### 9.7 Booleanos

| Armadilha | Detalhe |
|---|---|
| Flags usam a string `"X"` | `true`, `1`, `yes` são ignorados **sem erro** |
| `fromOnlineScheduling` é boolean de verdade | Exceção à regra do `"X"` |
| `IsOnlineScheduling`, `AlreadyPatient`, `ShedulingAccepted` são boolean | Também exceções |

### 9.8 Obrigatoriedade inconsistente

| Endpoint | Detalhe |
|---|---|
| `/financial/list_cash_flow`, `/financial/list_payments`, `/financial/average_installments` | `business_id` **obrigatório** |
| `/financial/list_summary`, `/list_invoices`, `/list_receipt` | `business_id` opcional |
| `/appointment/schedule_occupation`, `/sales/estimates_and_conversion`, `/financial/average_installments` | `group_by` marcado obrigatório |
| `/operational/*` | Exigem `isAPI=X` |
| `/appointment/list` | `subscriber_id` opcional em conta única, obrigatório em conta de grupo (senão `401`) |

### 9.9 Descrições erradas no spec

| Endpoint | Descrição publicada | Realidade |
|---|---|---|
| `/crm/list_active_campaigns` | "Lista todos os usuários do sistema" | Lista campanhas |
| `/crm/list_active_campaigns` (200) | "mudar descrição" | Placeholder esquecido |
| `/payment/list_reconcile_claim` | "Pagsmento Parcial" | Pagamento Parcial (`PARTIAL_PAID`) |

### 9.10 Limitações estruturais

| Limitação | Consequência prática |
|---|---|
| Sem paginação | Quebre períodos longos em janelas menores |
| Sem webhooks (salvo `/file/upload`) | Integrações dependem de polling |
| Sem rate limit documentado | Implemente throttling defensivo do seu lado |
| Sem `ETag` / `If-Modified-Since` | Use `z_LastChange_Date` para diffs |
| Sem endpoint de "listar todos os pacientes" | Descoberta de pacientes só via agenda, orçamentos ou pagamentos |
| `POST` não são idempotentes | Guarde ids retornados e deduplique |

### 9.11 LGPD

A API trafega **dados pessoais sensíveis de saúde** (nome, CPF, telefone, e-mail,
data de nascimento, procedimentos, motivo da consulta). Ao integrar:

- Armazene o Token API em secret manager, nunca no código ou no front-end.
- Não exponha endpoints da Clinicorp diretamente ao navegador — o Basic Auth
  vazaria o token. Sempre passe por um backend intermediário.
- Colete apenas os campos necessários; `/patient/get` permite busca por CPF,
  o que é um vetor de enumeração se exposto sem controle.
- Registre logs de acesso e defina retenção.

---

## Anexo — checklist de integração

- [ ] Token API guardado como secret (não no repositório)
- [ ] Client com Basic Auth (não Bearer)
- [ ] Backend intermediário — API nunca chamada do browser
- [ ] `subscriber_id` resolvido (conta única vs. grupo)
- [ ] Mapa de `business_id` por clínica em cache
- [ ] Mapa de `status_id` por `Type` em cache
- [ ] Conversão de fuso UTC ↔ clínica implementada
- [ ] Flags `"X"` (não `true`) em todos os parâmetros booleanos
- [ ] `includeAssigns=X` nos cálculos de ocupação
- [ ] `includeCanceled=X` + `includeDeleted=X` na sincronização
- [ ] Janelas de data curtas (sem paginação)
- [ ] Retry com backoff em `5xx`, sem retry em `4xx`
- [ ] Parser de erro que aceita `Message` como string **ou** array
- [ ] `201` tratado como sucesso em `/products/orders`
- [ ] Corpo verificado em `/crm/add_leads` (erro dentro de `200`)
- [ ] Deduplicação de pacientes por CPF antes de `POST /patient/create`
- [ ] Polling agendado (não há webhooks)

---

*Documento gerado a partir do spec OpenAPI 3.0 público da Clinicorp
(`API Clinicorp v1.0.0`, 49 endpoints, 17 grupos), consultado em 23/08/2026.
Referência não-oficial — em caso de divergência, o spec em
<https://api.clinicorp.com/api-docs/> prevalece.*
