# Recipes de Alto ROI — Implementacao Step-by-Step

Os 5 workflows com maior retorno documentado por agencias reais.

---

## 1. Speed-to-Contact (<5 min)

**Resultado**: +30-50% bookings, +400% conversao vs resposta em 30+ min
**Complexidade**: Baixa (5-8 steps)

### Design

```
Trigger: Form Submitted / Contact Created
  ├─ Wait: 1 minuto (parecer humano)
  ├─ Send SMS: "Oi {{contact.first_name}}, vi que voce se interessou por [X]. Posso te ajudar?"
  ├─ Wait: 3 minutos
  ├─ If/Else: Respondeu?
  │   ├─ SIM → Assign To User (vendedor disponivel)
  │   │       → Add Tag: "lead-quente"
  │   │       → Send Internal Notification
  │   └─ NAO → Send SMS: "Sem problemas! Quando for melhor pra voce, me responde aqui."
  │           → Wait: 2 horas
  │           → Send Email: Follow-up com mais info
  └─ Goal Event: Appointment Status = Booked
```

### Configuracao

1. **Trigger**: Form Submitted (selecionar formulario especifico)
   - Filter: Source = landing page principal
2. **Wait**: 1 minuto (simula tempo humano)
3. **Send SMS**: Usar {{contact.first_name}}, tom conversacional
4. **Wait**: 3 minutos (tempo para responder)
5. **If/Else**: Contact replied = Yes (ultimas 3 min)
6. **Branch SIM**: Assign + Tag + Notification
7. **Branch NAO**: Follow-up SMS + Wait 2h + Email
8. **Goal Event**: Appointment Booked (encerra se agendar)

### Settings

- Re-entry: OFF (lead so entra 1x por form)
- Stop on Response: ON (para de enviar quando responder)
- Time Window: 8h-21h (nao enviar de madrugada)

---

## 2. Missed Call Text-Back

**Resultado**: +20-40% re-engajamento de chamadas perdidas
**Complexidade**: Baixa (4-6 steps)

### Design

```
Trigger: Call Status = Missed / No Answer
  ├─ Wait: 1 minuto
  ├─ Send SMS: "Oi {{contact.first_name}}, vi que tentou nos ligar. Como posso ajudar?"
  ├─ Wait: 30 minutos
  ├─ If/Else: Respondeu?
  │   ├─ SIM → Assign To User
  │   └─ NAO → Send SMS: "Fica a vontade pra responder aqui ou ligar de volta em [horario]"
  └─ Stop
```

### Configuracao

1. **Trigger**: Call Status (selecionar Missed/No Answer)
2. **Wait**: 1 minuto
3. **Send SMS**: Mensagem curta e direta
4. **If/Else**: Contact replied
5. **Assign To User**: Round-robin ou usuario fixo

### Settings

- Re-entry: ON (cada chamada perdida deve triggar)
- Stop on Response: ON

---

## 3. Appointment Reminders 3-Touch

**Resultado**: -40-60% no-shows
**Complexidade**: Media (8-12 steps)

### Design

```
Trigger: Appointment Scheduled
  ├─ If/Else: Appointment > 24h away?
  │   ├─ SIM → Send Email: Confirmacao + detalhes
  │   │       → Wait: Ate 24h antes
  │   │       → Send SMS: "Lembrete: seu agendamento amanha as {{appointment.time}}"
  │   │       → Wait: Ate 1h antes
  │   │       → Send SMS: "Nos vemos em 1 hora! Endereco: [X]"
  │   └─ NAO → Send SMS: "Confirmado! Te esperamos as {{appointment.time}}"
  │           → Wait: Ate 1h antes
  │           → Send SMS: "Nos vemos em 1 hora!"
  └─ Goal Event: Appointment Status = Showed
```

### 3 Touchpoints

| # | Quando | Canal | Conteudo |
|---|--------|-------|----------|
| 1 | Imediato | Email | Confirmacao com data, hora, local, instrucoes |
| 2 | 24h antes | SMS | Lembrete curto + link para reagendar |
| 3 | 1h antes | SMS | "Nos vemos em breve!" + endereco/link |

### Settings

- Re-entry: ON (cada agendamento gera nova sequencia)
- Stop on Response: OFF (nao parar — reminders sao importantes)
- Goal Event: Appointment Showed (encerra se compareceu)

---

## 4. Review Request Post-Service

**Resultado**: 3-5x mais reviews em 90 dias
**Complexidade**: Media (6-10 steps)

### Design

```
Trigger: Appointment Status = Showed (ou Tag "servico-concluido")
  ├─ Wait: 2 horas (tempo para experiencia decantar)
  ├─ Send SMS: "Oi {{contact.first_name}}! Como foi sua experiencia? Responda de 1 a 5"
  ├─ Wait: 24 horas
  ├─ If/Else: Respondeu com 4 ou 5?
  │   ├─ SIM → Send SMS: "Que otimo! Nos ajudaria muito se deixasse um review: [link Google]"
  │   │       → Wait: 48h
  │   │       → If/Else: Clicou no link?
  │   │           ├─ SIM → Add Tag: "review-enviado"
  │   │           └─ NAO → Send Email: Lembrete gentil
  │   └─ NAO/Sem resposta → Add Tag: "feedback-negativo"
  │                        → Send Internal Notification (alerta para gestor)
  └─ Stop
```

### Logica

O segredo e filtrar: so pedir review publico para quem deu nota alta. Notas baixas vao para alerta interno (oportunidade de recuperacao).

### Settings

- Re-entry: ON (cada servico gera novo pedido)
- Stop on Response: OFF (a logica interna gerencia)
- Time Window: 9h-20h

---

## 5. Database Reactivation (AI-Assisted)

**Resultado**: Requalifica 5-15% de uma lista fria
**Complexidade**: Alta (10-15 steps)

### Design

```
Trigger: Tag Added = "reativacao-batch-[data]"
  ├─ Wait: Random 1-5 min (distribuir envios)
  ├─ If/Else: Last Activity > 90 dias?
  │   ├─ SIM → Send SMS: "Oi {{contact.first_name}}, tudo bem? Faz tempo que nao conversamos. Ainda tem interesse em [X]?"
  │   │       → Wait: 24h
  │   │       → If/Else: Respondeu?
  │   │           ├─ SIM → AI Intent Detection: Interesse/Sem interesse
  │   │           │       → If/Else: Interesse?
  │   │           │           ├─ SIM → Add Tag: "lead-reativado" → Speed-to-Contact
  │   │           │           └─ NAO → Add Tag: "sem-interesse" → Remove do proximo batch
  │   │           └─ NAO → Wait: 7 dias
  │   │                   → Send Email: Conteudo de valor (nao venda)
  │   │                   → Wait: 3 dias
  │   │                   → Send SMS: Ultima tentativa
  │   └─ NAO → Skip (contato recente, nao reativar)
  └─ Stop
```

### Dicas

- **Usar AI Intent Detection** para classificar respostas automaticamente
- **Batch por tags** para controlar volume (nao enviar 5000 SMS de uma vez)
- **Conteudo de valor primeiro** — nao vender logo; re-engajar
- **3 tentativas max** — respeitar quem nao quer ser contactado
- **Monitorar DND** — se contato pedir para parar, DND imediatamente

### Settings

- Re-entry: OFF (1x por campanha)
- Stop on Response: ON
- Time Window: 10h-18h (horario mais conservador para lista fria)

---

## Bonus: Comment Automation (Instagram/Facebook)

### Design (Instagram)

```
Trigger: Instagram Comment (post especifico)
  ├─ Send Instagram Reply: "Acabei de te mandar no DM!"
  ├─ Wait: 30 segundos
  ├─ Send Instagram DM: Mensagem interativa com botoes
  │   → Botao 1: "Quero saber mais" → Entrega link/recurso
  │   → Botao 2: "Agendar" → Generate Booking Link
  ├─ Wait: 24h
  ├─ If/Else: Clicou em algum botao?
  │   ├─ SIM → Tag + Pipeline
  │   └─ NAO → DM follow-up simples
  └─ Stop
```

Este recipe combina engajamento social com captura de lead. Funciona especialmente bem para lead magnets e agendamentos.
