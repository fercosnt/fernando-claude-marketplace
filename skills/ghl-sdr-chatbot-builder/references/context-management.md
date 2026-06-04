# Gestao de Contexto Limitado no GHL

## Quando carregar
Fase 2A (setup do Conversation AI), Fase 3A (compilacao do briefing) e quando o bot perder contexto durante conversas.

---

## 1. O Limite Documentado

O GHL Conversation AI usa as **ultimas 10 mensagens ou ate 800 palavras** de historico (o que vier primeiro). Apos esse limite, mensagens antigas saem da janela de contexto — o bot literalmente "esquece" o inicio da conversa.

Fonte: GHL AI Prompting 101 (docs oficiais)

---

## 2. Implicacoes Praticas

### O que o bot "ve" a cada turno
```
[System Prompt (sempre presente)]
+
[Ultimas 10 mensagens OU 800 palavras do historico]
+
[Mensagem atual do lead]
```

### Consequencias
- Em conversas longas (>10 turnos), o bot perde o nome do lead, a necessidade inicial, e dados coletados no inicio
- Instrucoes no prompt sao permanentes; dados da conversa sao volateis
- Prompts longos (>200 palavras de contexto estatico) consomem espaco da janela

---

## 3. Estrategias de Design para 800 Palavras

### 3.1 Prompt Enxuto
- **Maximo 100-200 palavras de contexto estatico** no prompt
- Cada palavra conta — eliminar redundancias
- Usar delimitadores (`#`, `>`, `<>`) para estruturar sem desperdicar palavras

**Errado** (350 palavras de prompt):
```
Voce e um assistente virtual da clinica odontologica Beauty Smile,
localizada em Brasilia, que oferece tratamentos de alta qualidade
como lentes de contato dental, implantes, harmonizacao facial...
[mais 300 palavras de contexto]
```

**Certo** (80 palavras de prompt):
```
# ROLE
Assistente virtual da Beauty Smile (clinica premium, Brasilia).

# SERVICOS
Lentes de contato, implantes, harmonizacao, clareamento.

# OBJETIVO
Qualificar leads: coletar nome, necessidade, urgencia. Se qualificado, agendar avaliacao.

# REGRAS
- Max 2-3 frases por resposta
- Tom: amigavel e premium
- Se nao souber, transferir para humano
```

### 3.2 Repetir Instrucoes Criticas
Instrucoes fundamentais devem aparecer em **multiplos pontos** do prompt para garantir consistencia mesmo quando a janela desliza:

```
# No inicio do prompt:
"NUNCA invente informacoes. Se nao souber, diga que vai verificar."

# No meio, apos regras de qualificacao:
"Lembre-se: NUNCA invente informacoes."

# No final:
"IMPORTANTE: Em nenhuma hipotese invente dados ou prometa resultados."
```

### 3.3 Respostas Ultra-Curtas
Cada resposta do bot consome contexto. Respostas longas = menos espaco para historico.

| Config GHL | Palavras/resposta | Uso ideal |
|-----------|-------------------|-----------|
| **Concise** | ~30 palavras | SMS, WhatsApp (recomendado para SDR) |
| **Balanced** | ~80 palavras | Webchat |
| **Detailed** | ~200 palavras | FAQ, suporte (NAO usar para SDR) |

**Para SDR**: usar Concise ou Balanced. Detailed consome contexto demais.

### 3.4 Qualificacao em Poucos Turnos
Com 10 mensagens de janela (5 do bot + 5 do lead), o fluxo ideal de qualificacao e:

```
Turno 1: Saudacao + disclosure + pergunta aberta (necessidade)
Turno 2: Validacao + pergunta de urgencia
Turno 3: Dado complementar (nome se nao tem, ou budget indireto)
Turno 4: Resumo + CTA (agendamento ou handoff)
Turno 5: Confirmacao + encerramento
```

5 turnos = 10 mensagens = cabe inteiro na janela.

### 3.5 Skip if Already Filled
No GHL Guided Form: ativar "Skip if Already Filled" para campos de qualificacao. Evita gastar turnos re-perguntando dados ja presentes no CRM.

### 3.6 Bot-to-Bot Transfer
Quando o fluxo e complexo demais para 10 mensagens:
- **Bot 1**: Qualificacao (5 turnos)
- **Bot 2**: Agendamento (3-5 turnos)
- Cada bot tem prompt independente, sem poluir contexto

Configurar via Bot Goals no GHL.

---

## 4. Maximum Message Limit

### Configuracao
GHL Advanced Settings → Maximum Message Limit

### Valores recomendados
| Cenario | Max Messages | Justificativa |
|---------|-------------|---------------|
| SDR qualificacao simples | 10-15 | Suficiente para qualificar e agendar |
| SDR com FAQ | 15-20 | Espaco para perguntas sobre servicos |
| Suporte/FAQ | 20-25 | Conversas mais longas aceitaveis |
| NUNCA | 75 (default GHL) | Custo alto, conversas sem foco, loops |

### O que acontece ao atingir o limite
- Bot para de responder
- Para resetar: usar acao de workflow "Update Conversation AI Bot and Status"
- Util para evitar conversas infinitas e controlar custo

---

## 5. Sleep Mode e Pausa

### Quando usar
- Apos handoff para humano: bot deve parar para nao interferir
- Config: Advanced Settings → Send Bot to Sleep (dias, horas, minutos)
- Ativar via workflow tambem e possivel

### Pattern recomendado
```
[Bot qualifica lead]
  → [Handoff para humano]
    → [Workflow: Sleep bot por 24h]
      → [Humano responde]
        → [Se humano nao responder em 24h: bot reativa automaticamente]
```

---

## 6. Contexto entre Sessoes

### Gap documentado
O GHL NAO tem documentacao clara sobre persistencia de contexto entre conversas distintas do mesmo contato. Na pratica:

- **Custom fields**: persistem entre sessoes (dados salvos via workflow ficam no contato)
- **Historico de chat**: a janela de contexto do bot provavelmente reinicia por sessao
- **Workaround**: salvar dados criticos em custom fields durante a conversa, e referencia-los no prompt via variaveis do GHL

### Template de prompt com variaveis
```
# CONTEXTO DO LEAD
Nome: {{contact.first_name}}
Interesse: {{contact.custom_field_interesse}}
Score: {{contact.custom_field_lead_score}}
Ultima interacao: {{contact.custom_field_ultimo_contato}}
```

Isso garante que o bot "lembra" de sessoes anteriores sem depender do historico de chat.

---

## 7. Checklist de Otimizacao de Contexto

- [ ] Prompt tem no maximo 200 palavras de contexto estatico
- [ ] Instrucoes criticas repetidas em 2-3 pontos do prompt
- [ ] Response Style configurado como Concise ou Balanced
- [ ] Maximum Message Limit entre 10-20 (nao 75)
- [ ] Skip if Already Filled ativado para campos ja preenchidos
- [ ] Dados criticos salvos em custom fields (nao dependem do historico)
- [ ] Bot-to-bot transfer configurado se fluxo > 5 turnos
- [ ] Sleep mode ativo apos handoff para humano

---

## 8. Persistencia de Contexto entre Sessoes

### Comportamento atual do GHL
O bot reseta o contexto entre sessoes. Em nova sessao, o historico anterior NAO e injetado automaticamente no prompt. Confirmado pela comunidade GHL e feature requests.

### Workaround: Custom Fields como Memoria Externa

**Passo a passo:**
1. Durante a conversa, usar GPT Action em workflow para extrair dados chave (nome, interesse, objecao, etapa)
2. Salvar em custom fields especificos (ex: `interesse_principal`, `objecao_ultima`, `etapa_funil`)
3. No prompt do bot, injetar via variaveis: `{{contact.interesse_principal}}`, `{{contact.objecao_ultima}}`
4. Usar bloco contextual no prompt: "O contato ja informou que: {{contact.resumo_conversa_anterior}}"
5. Atualizar o campo de resumo ao final de cada sessao (trigger: bot inativado ou timeout)

### AI Memory Key (Labs)
O GHL tem feature em Labs chamada "AI Memory Key" que persiste historico entre execucoes de GPT Actions em workflows:
- Escopos: This Sub Account, This Workflow, Per Execution, This Step, Custom
- Aplica-se a GPT Actions em workflows, NAO ao bot nativo
- Precisa ativar em Labs

Fonte: GHL Help Portal (https://help.gohighlevel.com/support/solutions/articles/155000003026-history-for-gpt-actions-ai-memory-key-)

### Variaveis no Prompt do Bot
Variaveis disponiveis no prompt editor do Conversation AI:
- `{{contact.name}}`, `{{contact.phone}}`, `{{contact.email}}`
- Custom fields via botao "Add Custom Values" no editor
- Permite injetar dados de sessoes anteriores se salvos em custom fields

Fonte: GHL Help Portal (https://help.gohighlevel.com/support/solutions/articles/155000002255-customize-your-ai-responses-using-prompts)

### Tecnicas avancadas de gestao de contexto
- **Sliding window + rolling summary**: manter ultimas 3-6 trocas verbatim + resumo comprimido das anteriores
- **State machine no prompt**: definir estado atual e transicoes possiveis para manter coerencia sem memoria
- **Compressao de prompt**: ferramentas como LLMLingua (Microsoft) comprimem ate 20x com perda minima

Fontes:
- Anthropic: Context Engineering (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- GetMaxim: Context Window Management (https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- HighLevel Techie: Custom Fields (https://highleveltechie.com/post/how-to-capture-and-update-custom-fields-using-gohighlevel-conversational-ai)

---

## Fontes
- GHL Docs: AI Prompting 101 (https://help.gohighlevel.com/support/solutions/articles/155000002254-ai-prompting-101)
- GHL Docs: Advanced Settings (https://help.gohighlevel.com/support/solutions/articles/155000004415-advanced-settings-overview-conversation-ai)
- GHL Docs: Bot Goals (https://help.gohighlevel.com/support/solutions/articles/155000004095-bot-goals-feature-complete-guide)
- GHL Docs: Response Style Settings (https://help.gohighlevel.com/support/solutions/articles/155000007421-configure-response-settings-in-conversation-ai)
- OmniFusion AI: Buffer window de 5-10 trocas (https://youtube.com/watch?v=aPsoYnirlgM)
- GHL Wizard: Max messages 10-15 (https://youtube.com/watch?v=G5XBmvvXB4k)
