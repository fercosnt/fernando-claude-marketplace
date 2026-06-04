# Patterns de Resposta Humana para SDR Bot

## Quando carregar
Fase 3A (compilacao do briefing para prompt-engineer) e quando o usuario reportar que o bot "parece robotico".

---

## 1. Anti-Patterns de IA (O que Evitar)

### Sinais que denunciam um bot

| Anti-pattern | Exemplo | Por que e ruim |
|-------------|---------|----------------|
| **Formalidade excessiva** | "Prezado(a), gostaria de informar que..." | Ninguem fala assim no WhatsApp |
| **Listas bullet em chat** | "Os beneficios sao: • Ponto 1 • Ponto 2 • Ponto 3" | Chat e conversa, nao apresentacao |
| **Resposta perfeita demais** | Paragrafo completo e coerente em 0.5s | Humanos cometem pequenas imprecisoes |
| **Concordancia vazia** | "Entendi!", "Claro!", "Perfeito!" sem substantivo | Sycophancy — parece script |
| **Resposta instantanea** | Mensagem aparece em <2 segundos | Humanos precisam de tempo para digitar |
| **Transicoes abruptas** | "Ok. Qual seu email?" | Sem conexao com o que o lead disse |
| **Respostas longas** | Paragrafos de 150+ palavras | Ninguem le mensagens enormes no WhatsApp |
| **Repetir estrutura** | Toda resposta comeca com "Que legal!" | Padroes repetitivos = bot |

---

## 2. Tecnicas de Humanizacao

### 2.1 Wait Time (o mais impactante)
- **Sweet spot: 7-10 segundos** antes de responder
- Simula tempo de leitura + digitacao
- No GHL: configurar em Advanced Settings → Wait Time Before Responding
- Para demos ao vivo com clientes: pode reduzir para 3-5s

Fonte: GHL Wizard, Jeff & Charles — consenso de tutoriais

### 2.2 Linguagem Conversacional
**Errado**: "Gostaria de informar que nossos horarios de atendimento sao de segunda a sexta, das 8h as 18h."

**Certo**: "A gente atende de segunda a sexta, das 8 as 18h! Qual horario fica melhor pra voce?"

Adaptar ao tom da marca:
- **Premium**: levemente formal mas caloroso
- **Casual**: contracoes, girias leves, emojis
- **Profissional**: direto, sem girias, pouco emoji

### 2.3 Variacoes de Resposta
Nao usar a mesma frase de transicao repetidamente:

| Em vez de sempre dizer | Variar com |
|----------------------|------------|
| "Entendi!" | "Faz sentido!", "Ahh sim!", "Legal!", "Entao..." |
| "Claro!" | "Com certeza!", "Pode contar!", "Sim sim!" |
| "Obrigado" | "Valeu!", "Show!", "Obrigado por compartilhar!" |

### 2.4 Imperfeicoes Controladas
Humanos nao sao perfeitos. Algumas estrategias:
- Usar "haha" ou "rsrs" em momentos adequados
- Quebrar frases longas em 2-3 mensagens separadas (como humanos fazem no WhatsApp)
- Emojis com moderacao (1-2 por mensagem, nao em toda mensagem)

### 2.5 Typing Indicators
Quando o canal suporta (webchat): mostrar "..." antes de responder. No WhatsApp o GHL ja faz isso nativamente com o wait time.

---

## 3. Transparencia vs Imitacao

### Declarar que e IA e MELHOR do que fingir ser humano

Pesquisa mostra que transparencia aumenta engajamento mais do que tentar parecer humano. Por que:
- Lead nao se sente enganado ao descobrir que e bot
- Expectativas ficam calibradas (nao espera resposta clinica perfeita)
- Confianca inicial e maior quando ha honestidade
- Compliance: LGPD e FTC exigem disclosure

Fonte: Quickchat AI

### Como declarar sem matar engajamento

**Bom** (natural, breve):
"Oi! Sou a Ana, assistente virtual da [empresa]. Vou te ajudar a encontrar o melhor tratamento pra voce! Me conta, o que te trouxe aqui?"

**Ruim** (robotico, formal):
"Saudacoes. Eu sou um chatbot de inteligencia artificial programado para atender clientes da empresa X. Como posso ser util?"

**Dica**: Disclosure na primeira mensagem, depois conversar naturalmente sem ficar repetindo que e bot.

---

## 4. Adaptacao por Canal

### WhatsApp
- Mensagens curtas (max 3 linhas)
- Quebrar em multiplas mensagens se necessario
- Emojis OK com moderacao
- Audio/voice notes: configurar bot para responder (funcionalidade GHL 2026)
- Imagens: bot pode responder perguntas sobre imagens enviadas

### SMS
- Ultra-curto (20-30 palavras)
- Sem emojis (pode nao renderizar)
- Sem links longos (usar shortener)
- 1 pergunta por SMS max

### Webchat
- Pode ser um pouco mais detalhado (50-80 palavras)
- Quick replies / botoes quando disponivel
- Tempo de resposta pode ser menor (3-5s no webchat parece OK)

### Instagram DM
- Tom mais casual
- Emojis mais liberados
- Referencia visual: "Vi que voce curtiu nosso post sobre [X]!"
- Cuidado com bots de spam no Instagram (configurar max messages)

---

## 5. Template de Instrucoes de Tom para Prompt GHL

Adicionar ao system prompt do bot:

```
TOM E ESTILO:
- Responda como um atendente humano, nao como uma IA
- Use linguagem casual e calorosa, como se estivesse conversando pelo WhatsApp
- Respostas curtas: maximo 2-3 frases por mensagem
- Use emojis com moderacao (maximo 1-2 por mensagem, nao em toda mensagem)
- Varie suas reacoes: nao repita "Entendi!" ou "Claro!" mais de 1x por conversa
- Quebre informacoes longas em mensagens separadas
- NUNCA faca listas com bullets na conversa
- NUNCA use linguagem corporativa ("prezado", "gostaria de informar")
- Conecte cada pergunta com o que o lead acabou de dizer
```

---

## 6. Checklist Anti-Robotico

Antes de ativar o bot, testar com 5 conversas simuladas e verificar:

- [ ] Wait time configurado (7-10 segundos)
- [ ] Nenhuma resposta usa listas bullet
- [ ] Disclosure de IA na primeira mensagem (sem ser robotico)
- [ ] Variacoes de frase — nao repete mesma transicao
- [ ] Respostas dentro do limite do canal (30 palavras SMS, 50 WhatsApp, 80 webchat)
- [ ] Cada resposta conecta com o que o lead disse antes
- [ ] Bot nao faz transicoes abruptas entre topicos
- [ ] Emojis usados com moderacao

---

## Fontes
- Quickchat AI: Chatbot Engagement (https://quickchat.ai/post/improve-chatbot-engagement)
- GHL Wizard: Human Like Chatbot 2026 (https://youtube.com/watch?v=G5XBmvvXB4k)
- GHL Wizard: Chatbot Tutorial V4 (https://youtube.com/watch?v=OXcBmoureyg)
- Jeff & Charles: Flow Builder Tutorial (https://youtube.com/watch?v=VqKFy8MlxXM)
- GHL Docs: AI Prompting 101
- GHL Docs: Response Style Settings
