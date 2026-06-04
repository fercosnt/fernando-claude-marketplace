# Conversation Design para Vendas em Chat

## Quando carregar
Fase 1B (analise de scripts SDR), Fase 3A (compilacao do briefing) e quando o usuario pedir ajuda com fluxo conversacional.

---

## 1. Principios de Pacing

### Progressive Disclosure
Cada pergunta de qualificacao deve ser construida sobre a resposta anterior, nunca em burst. O bot revela informacao e coleta dados gradualmente, como uma conversa natural.

**Regra de ouro**: 1 pergunta por mensagem. Nunca 2+ perguntas na mesma mensagem.

### Limite de Perguntas
- **Maximo 3-5 perguntas de qualificacao por sessao**
- Acima disso: drop-off aumenta significativamente
- Se precisar de mais dados: coletar nos follow-ups, nao na primeira interacao

### Pacing Natural
| Situacao | Comportamento do bot |
|----------|---------------------|
| Lead responde rapido | Manter ritmo — responder apos delay natural (7-10s) |
| Lead responde devagar | Nao pressionar — aguardar; follow-up apos 1h se silencio |
| Lead da resposta curta | Fazer pergunta de follow-up, nao avançar topico |
| Lead da resposta longa | Reconhecer o que disse, resumir, depois avançar |

---

## 2. Engagement Loops

### O que mantém o lead na conversa

1. **Validacao emocional antes de proxima pergunta**
   - "Entendo perfeitamente! E muito comum sentir isso."
   - Depois: proxima pergunta

2. **Micro-compromissos progressivos**
   - Cada "sim" pequeno prepara para o "sim" grande (agendamento)
   - "Posso te fazer uma pergunta rapida?" → "sim" → pergunta de qualificacao

3. **Quick replies / botoes** (quando o canal suporta)
   - Reduzem fricao cognitiva
   - Aumentam flow adherence
   - Diminuem bounce rate
   - Ex: "O que mais te interessa? 1) Tratamento X  2) Tratamento Y  3) Outro"

4. **Informacao de valor intercalada**
   - Nao so perguntar — oferecer algo entre perguntas
   - "Interessante! Sabia que [dado relevante]? E sobre [proxima pergunta]..."

### O que mata o engajamento

- Burst de perguntas (2+ na mesma mensagem)
- Respostas genericas sem personalização ("Entendi!")
- Resposta instantanea (sem delay)
- Pressao para agendamento antes de rapport
- Proactive triggers agressivos (popup imediato)

---

## 3. Branching Dinamico

### Anti-pattern: Script Linear
Scripts rigidos quebram quando o lead foge do esperado. O bot deve recalibrar sem reiniciar.

### Conversation Repair
Quando o lead muda de topico ou da input incompleto:

```
Lead: "Quanto custa?"
Bot: "Vou te passar os valores! Antes, posso saber o que te motivou a buscar [tratamento]? Assim consigo te indicar a melhor opcao."
```

O bot nao ignora a pergunta — reconhece, redireciona gentilmente, e volta ao fluxo.

### Context Retention
- Referenciar inputs anteriores SEMPRE que possivel
- **Maior frustracao**: bot re-pergunta algo ja respondido
- Usar "Skip if Already Filled" no GHL para campos ja coletados

### Fall-Forward Pattern
Quando o bot nao entende:
- **Errado**: "Desculpe, nao entendi. Pode repetir?"
- **Certo**: "Hmm, nao tenho certeza se entendi. Voce quis dizer [opcao A] ou [opcao B]?"

Oferecer alternativas concretas em vez de pedir repeticao.

---

## 4. Estrutura de Mensagem

### Anatomia de uma boa resposta do bot SDR

```
[Validacao/reconhecimento — 1 frase]
[Informacao/valor — 1-2 frases OU pular se nao aplicavel]
[Proxima pergunta OU CTA — 1 frase]
```

### Exemplos

**Bom:**
"Que legal que voce ta pensando nisso! Muitos pacientes nos procuram por esse mesmo motivo. Posso saber ha quanto tempo voce tem pensado em resolver isso?"

**Ruim:**
"Entendi. Qual seu nome? Qual sua idade? Voce tem disponibilidade essa semana?"

### Tamanho por canal

| Canal | Tamanho ideal | Config GHL |
|-------|---------------|------------|
| SMS | 20-30 palavras | Response Style: Concise |
| WhatsApp | 30-50 palavras | Response Style: Concise ou Balanced |
| Webchat | 50-80 palavras | Response Style: Balanced |
| Email | 80-150 palavras | Response Style: Detailed |

---

## 5. Two-Way Conversation

### Nao e interrogatorio
A qualificacao deve parecer conversa, nao formulario. Cada resposta do lead e informacao valiosa que o bot deve reconhecer.

### Cada resposta e pesquisa competitiva
- Ferramentas que o lead usa → anotar no CRM
- Decisores mencionados → registrar
- Timeline de compra → classificar urgencia
- Objecoes levantadas → feeding para melhoria do prompt

### Progressao natural

```
[Rapport] → [Necessidade] → [Qualificacao leve] → [Valor] → [CTA]
```

Nao pular etapas. Se o lead pede agendamento direto, otimo — aceitar. Mas nao forcar a progressao.

---

## Fontes
- Rasa Blog: Chatbot Flow Examples (https://rasa.com/blog/chatbot-flow-examples)
- Quickchat AI: Chatbot Engagement (https://quickchat.ai/post/improve-chatbot-engagement)
- SpurNow: Lead Qualification Guide (https://www.spurnow.com/en/blogs/how-do-chatbots-qualify-leads)
- OmniFusion AI: AI Sales Agents Tutorial (https://youtube.com/watch?v=aPsoYnirlgM)
- SalesTechStar: Conversational Sales Technologies
