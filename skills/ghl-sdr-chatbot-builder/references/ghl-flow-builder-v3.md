# GHL Conversation AI — Flow Builder V3 (Node-Based)

## Quando carregar
Fase 2A quando o usuario opta pela arquitetura **Flow-Based (V3)** em vez do bot Prompt-Based classico. Fase 3 quando desenhar a qualificacao por etapas. Sempre que a duvida envolver nodes, multi-agente, transferencia entre bots ou os pitfalls do V3.

---

## 1. Por que V3 existe (mudanca de paradigma)

O modelo classico do Conversation AI e um **prompt unico** (Personalidade + Objetivo + Info adicional) que o bot interpreta livremente a cada turno. Funciona bem para qualificacao simples, mas em fluxos longos o bot "improvisa": pula etapas, esquece de coletar um campo, ou nao sabe quando transferir.

O **Flow Builder V3** troca o prompt monolitico por um **fluxo de nodes**: cada etapa da qualificacao e um node com objetivo fechado e criterio de saida explicito. O bot deixa de improvisar a estrutura — ela esta desenhada. A logica de roteamento sai do prompt e vira nodes dedicados.

**Regra de escolha:**
- **Prompt-Based** → qualificacao simples (3-5 perguntas, 1 caminho), setup rapido, ainda recomendado para a maioria dos SDR bots.
- **Flow-Based V3** → qualificacao multi-etapa, multiplos caminhos por intencao, ou quando precisa de bots distintos por fase (triagem → closer → agendamento).

**Nao existe migracao automatica legacy → V3.** Um bot prompt-based nao vira flow com um clique — precisa ser reconstruido do zero no Flow Builder. Planejar isso antes de prometer "migracao" ao cliente.

---

## 2. Os Nodes do Flow Builder V3

| Node | O que faz | Config essencial | Cuidado |
|------|-----------|------------------|---------|
| **Chat Initiated** | Trigger unico de entrada do fluxo (canal: SMS/chat) | Canal de origem | E o ponto de partida — so um por fluxo |
| **Capture Information** | Loop autonomo ate cumprir o objetivo ou bater criterio de saida | Objetivo em linguagem natural + campo CRM destino + **max attempts (OBRIGATORIO)** | **Sem max attempts, o node entra em loop** em respostas ambiguas. Sempre definir tentativas maximas |
| **AI Splitter** | Roteia por logica analisando dados JA coletados. **NAO envia mensagem** | Condicoes de roteamento + **branch "No condition met" (OBRIGATORIO)** | **Sem o branch de fallback, o fluxo congela** quando nenhuma condicao bate |
| **Transfer Bot** | Passa a conversa inteira para outro bot. **Sem retorno** | Bot destino (deve estar ativo no mesmo canal em Auto Pilot) | Falha silenciosa se o bot destino estiver em teste/desabilitado. Transcript inteiro e preservado |
| **Book Appointment** | Loop ate agendar ou o lead recusar | Calendario alvo | Timezone pode nao converter para o fuso do lead (nao confirmado — testar) |
| **AI Message** | Gera UMA mensagem e (opcional) aguarda resposta | Texto-base + flag "wait for response" | Execucao unica, nao e loop |
| **Custom Message** | Envia mensagem literal (sem geracao) | Texto fixo | Uso: disclosure, mensagem de transicao |
| **Continue Conversation** | Mantem o fluxo aberto apos cumprir o objetivo | — | Para conversas que continuam pos-qualificacao |
| **End Conversation** | Encerra (opcional: reativacao agendada) | — | Custom triggers so disparam apos nodes [END] |

---

## 3. Limites do V3

| Limite | Valor | Nota |
|--------|-------|------|
| Mensagens por conversa | Configuravel **1–100** | Ao atingir → bot "dorme" + reativacao |
| Custom triggers por fluxo | **Maximo 3** | Disparam so apos nodes [END], com prioridade 1–10 |
| Objetivo (objective) por node | **≤ 500 caracteres** | Vale para Capture e outros nodes com objetivo |
| Acoes de handover por bot | **Maximo 3** (confirmado jun/2026) | Max 2 tentativas antes de escalar |
| Context window do fluxo | **Nao documentado** | Assumir janela efetiva ~15–20 turnos (ver context-management.md) |
| Numero maximo de nodes | **Nao documentado** | — |

---

## 4. Dois modelos de arquitetura multi-agente

### Modelo A — Flow Builder + Transfer Bot encadeado
Varios bots especializados, cada um Auto Pilot no mesmo canal, ligados por nodes Transfer Bot.
```
Bot Triagem (qualifica BANT) → Transfer Bot → Bot Closer (objecoes + agendamento)
```
Mais simples de raciocinar; cada bot tem prompt e objetivo proprios. O transcript passa adiante na transferencia.

### Modelo B — Agent Studio com AI Agent Node
Agentes dentro do Agent Studio compartilham **variaveis globais** que persistem entre eles. Mais flexivel e mais complexo — usar quando os agentes precisam ler/escrever estado compartilhado durante a conversa.

**Para SDR comum, comecar pelo Modelo A.** Modelo B so quando a complexidade justificar.

---

## 5. Sequencia recomendada para qualificacao SDR (V3)

Desenho de referencia para um fluxo BANT por nodes (ver conversation-design.md para o detalhamento):

```
Chat Initiated
  → Custom Message (disclosure de IA — compliance)
  → AI Message (ice-breaker + necessidade)
  → Capture (necessidade/dor → campo)         [max attempts: 3]
  → Capture (autoridade/decisor → campo)        [max attempts: 2]
  → Capture (timeline → campo)                  [max attempts: 2]
  → AI Splitter (qualificado?)                  [fallback: re-Capture]
       ├── SQL  → Book Appointment → Transfer Bot (SDR humano)
       ├── Morno → End Conversation (nurturing agendado)
       └── No condition met → AI Message (esclarece) → volta ao Splitter
```

**Tecnica-chave:** escrever o criterio de saida DENTRO do campo "objective" de cada Capture. Ex: *"Coletar o principal desafio do lead. Se nao responder apos 3 tentativas, encerre esta etapa e siga."* Isso evita loop sem depender de logica externa.

Ordem das perguntas: usar **N→A→T→B** (necessidade primeiro, budget por ultimo). Ver qualification-patterns.md §1.

---

## 6. Pitfalls do V3 (checklist anti-erro)

- [ ] **AI Splitter** tem branch "No condition met"? (sem ele, congela)
- [ ] **Capture** tem max attempts definido? (sem ele, loopa em resposta ambigua)
- [ ] Captura de email/telefone testada em **chat/SMS real**, nao no trial (falha silenciosa no preview)
- [ ] **Transfer Bot** aponta para bot **ativo em Auto Pilot no mesmo canal**? (falha silenciosa se destino estiver em teste)
- [ ] Booking confirma conversao de timezone para o fuso do lead? (testar)
- [ ] Disclosure de IA esta como primeiro node antes de qualquer Capture? (compliance — ver guardrails-compliance.md)
- [ ] Lembrou que **nao ha migracao automatica** legacy→V3? (reconstruir do zero)

---

## 7. Tres tipos de bot — visao consolidada

| Tipo | Melhor para | Trade-off |
|------|-------------|-----------|
| **Guided Form** | Iniciantes, FAQ, formularios | Simples demais para qualificacao de vendas |
| **Prompt-Based** | Maioria dos SDR bots; melhor resultado com menos setup | Bot improvisa a estrutura em fluxos longos |
| **Flow-Based (V3)** | Qualificacao multi-etapa, multi-agente, multiplos caminhos | Setup mais trabalhoso; exige desenho de nodes |

---

## Fontes
- GHL Help: Conversation AI Flow Builder (https://help.gohighlevel.com/support/solutions/articles/155000006515)
- GHL Help: Transfer Bot e multi-agente
- Jeff & Charles: Flow Builder Tutorial (https://youtube.com/watch?v=VqKFy8MlxXM)
- Para a AI Agent action (workflow premium), ver `ghl-ai-agent-action.md`
