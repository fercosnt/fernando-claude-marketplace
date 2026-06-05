# Objection Handling para Chat de Texto

## Quando carregar
Fase 1B (analise de scripts SDR), Fase 3A (compilacao do briefing) e quando o usuario pedir ajuda com objecoes.

---

## 1. Framework para Texto Curto

### Acknowledge → Clarify → Value → Confirm (ACVC)

4 passos, cada um em **maximo 1-2 frases**. Adaptado de Gong.io para formato de texto curto.

| Passo | O que faz | Exemplo |
|-------|-----------|---------|
| **Acknowledge** | Validar a objecao sem concordar/discordar | "Entendo perfeitamente sua preocupacao com o investimento." |
| **Clarify** | Entender o real motivo por tras | "O que pesa mais pra voce: o valor total ou o momento?" |
| **Value** | Ancorar em 1 beneficio concreto | "Muitos pacientes dividem em ate 12x e ja saem da avaliacao com um plano." |
| **Confirm** | Verificar se resolveu e oferecer proximo passo | "Faz sentido pra voce? Posso reservar um horario pra conversar melhor?" |

### Regra de Ouro
Em texto, cada step e 1 mensagem separada. Nao colocar os 4 passos na mesma mensagem.

---

## 1.5 Paradigma 2026: Buyer Enablement (prevenir > rebater)

A melhor objecao e a que nao acontece. **61% dos compradores B2B preferem nao falar com um vendedor** — o lead chega com posicao formada, e rebater de forma agressiva perde efeito. A jogada de 2026 (Apollo) e **habilitar a compra antes da objecao surgir**:
- Oferecer **calculadora de ROI, pacote de compliance, timeline** proativamente — antes do lead perguntar o preco.
- **O maior matador de deal em B2B 2026 nao e preco, e desalinhamento interno:** 74% dos times de compra tem conflito interno. Ajudar o lead a "vender internamente" (resumo compartilhavel, material para o decisor) converte mais que contornar objecao de preco.

### "Persistir ate a 2a objecao" — com ressalva de canal
Reps/bots que param na 1a objecao fecham **15–20% menos** do que os que vao ate a 2a. **Mas isso depende do canal:**
- **Webchat / inbound de alta intencao**: ok persistir ate a 2a objecao (1 tentativa de valor extra apos a 1a recusa).
- **WhatsApp**: continuar recuando apos a objecao clara (§4). Insistir vira mensagem nao-solicitada = spam = risco de block e quality-score. A regra anti-spam vence a regra de persistencia.

### Top 5 objecoes (74% de todo o pushback)
1. "Nao tenho interesse"
2. "Caro demais"
3. "Manda por email"
4. "Sem orcamento"
5. "Ja temos solucao"

Cobrir essas 5 no prompt cobre a maioria. Ver banco de respostas abaixo (§3).

---

## 2. Diferenca Fundamental: Chat vs Telefone

| Aspecto | Telefone | Chat/WhatsApp |
|---------|----------|---------------|
| Tom | Voz carrega empatia | Texto e "frio" — precisa compensar com palavras |
| Persistencia | 2-3 tentativas aceitas socialmente | 1 tentativa max — apos "nao", recuar |
| Pressao | Silencio do vendedor cria urgencia | Silencio do bot e percebido como bug |
| Formato | Pode falar 30 segundos | Max 2-3 frases por mensagem |
| Risco | Lead desliga | Lead bloqueia + denuncia (afeta quality score) |
| Tempo | Resposta imediata esperada | Delay de 7-10s aceito e desejavel |

---

## 3. Banco de Objecoes para SDR Bot

### 3.1 Preco / Investimento

**Objecao**: "Esta caro", "Nao tenho orcamento", "Vou pesquisar precos"

**ACVC**:
```
Bot: "Entendo! Investimento e uma preocupacao importante mesmo."
Bot: "Posso perguntar: o que pesa mais, o valor total ou o momento financeiro?"
[Lead responde]
Bot: "Faz sentido. A gente tem opcoes de parcelamento em ate 12x. E na avaliacao o doutor monta um plano personalizado com diferentes opcoes. Que tal conhecer?"
```

**No prompt GHL**:
```
Se o lead disser que esta caro ou mencionar preco:
- Valide a preocupacao ("entendo, investimento e importante")
- Pergunte se e o valor total ou o momento
- Mencione opcoes de parcelamento se aplicavel
- Convide para avaliacao sem compromisso
- NAO insista se o lead disser "nao" novamente
```

### 3.2 Timing / "Nao e o momento"

**Objecao**: "Nao e o momento", "Depois eu vejo", "Estou ocupado agora"

**ACVC**:
```
Bot: "Sem problema! Cada um tem seu tempo."
Bot: "Posso te enviar um material sobre [tratamento] pra voce ver quando tiver um tempinho?"
[Se sim]: "Show! Vou enviar. E se quiser, posso te lembrar daqui a [tempo]?"
[Se nao]: "Tranquilo! Fico a disposicao quando voce quiser retomar. 😊"
```

**No prompt**:
```
Se o lead disser que nao e o momento:
- Respeite imediatamente, sem pressionar
- Ofereca conteudo de valor (material, video, caso de sucesso)
- Proponha follow-up futuro com data especifica
- Se recusar follow-up, encerre amigavelmente
```

### 3.3 "Preciso pensar" / Indecisao

**Objecao**: "Vou pensar", "Preciso avaliar", "Deixa eu ver"

**ACVC**:
```
Bot: "Claro! E uma decisao importante mesmo."
Bot: "Tem alguma duvida especifica que eu possa ajudar a esclarecer?"
[Se sim]: responder a duvida
[Se nao]: "Tranquilo! Posso te mandar um resumo do que conversamos pra te ajudar na reflexao?"
```

### 3.4 Competidor / "Ja uso outro"

**Objecao**: "Ja tenho meu dentista", "Ja uso o [competidor]", "Estou satisfeito"

**ACVC**:
```
Bot: "Que bom que voce ja tem uma referencia! Isso mostra que voce se cuida."
Bot: "Muitos dos nossos pacientes vieram de outros profissionais buscando [diferencial]. Voce tem curiosidade sobre [diferencial]?"
[Se sim]: compartilhar diferencial
[Se nao]: "Entendo! Se um dia quiser uma segunda opiniao, estaremos aqui. 😊"
```

### 3.5 "Quero falar com humano"

**Nao e objecao — e handoff imediato**.
```
Bot: "Claro! Vou te conectar com [nome] agora mesmo. Ele(a) vai poder te ajudar com tudo. Um momento! 🙏"
[Trigger: Human Handover Action]
```

### 3.6 Desconfianca / "E bot?"

```
Bot: "Sim, sou a assistente virtual da [empresa]! Consigo responder a maioria das duvidas e agendar sua avaliacao. Se preferir falar direto com alguem da equipe, e so me pedir!"
```

---

## 4. Regras de Escalacao e Recuo

### Quando recuar (OBRIGATORIO)
- Lead disse "nao" explicitamente → 1 tentativa de valor, depois recuar
- Lead pediu para parar → encerrar imediatamente
- Lead demonstrou irritacao → handoff para humano
- Lead repetiu objecao → ja tentou, agora recuar

### Pattern de Recuo Gracioso
```
Bot: "Entendo perfeitamente! Sem pressao nenhuma."
Bot: "Se mudar de ideia, pode me chamar a qualquer hora que eu ajudo! 😊"
[Aplicar tag "recuo_objecao" + workflow de nurturing em 7-14 dias]
```

### Preservar o Lead
Recuar NAO e desistir. E preservar o lead para followup futuro:
1. Aplicar tag especifica da objecao (ex: "objecao_preco", "objecao_timing")
2. Mover para pipeline de nurturing
3. Agendar follow-up automatico em 7-14 dias
4. No follow-up: abordar o assunto de angulo diferente

---

## 5. Como Codificar no Prompt GHL

### Formato recomendado (OmniFusion AI)

Listar objecoes como pares no system prompt, com linguagem flexivel:

```
# OBJECTION HANDLING
Quando o lead levantar objecoes, use estas orientacoes:

> Objecao sobre PRECO:
Valide a preocupacao, pergunte se e valor total ou momento,
mencione parcelamento, convide para avaliacao sem compromisso.
Exemplo: "Entendo! O investimento e uma preocupacao real.
Posso perguntar: pesa mais o valor total ou o momento?"

> Objecao sobre TIMING:
Respeite, ofereca material de valor, proponha follow-up com data.
Exemplo: "Sem problema! Posso te enviar um material pra ver no seu tempo?"

> Objecao sobre COMPETIDOR:
Reconheca, destaque diferencial unico, nao deprecie o concorrente.
Exemplo: "Que bom que voce ja se cuida! Nosso diferencial e [X]."

> REGRA GERAL: Se o lead disser "nao" 2 vezes, recue
amigavelmente e encerre sem pressionar.
```

### NAO fazer
- Nao dar script rigido de resposta (o modelo precisa de flexibilidade)
- Nao usar "NUNCA diga X" excessivamente (consome contexto)
- Nao listar 20 objecoes (5-8 mais frequentes e suficiente)

---

## 6. Sentiment Analysis e Handoff Preventivo

### Sinais de frustacao no texto
- Respostas cada vez mais curtas ("ok", "tanto faz", "sei")
- Uso de capslock ("JA DISSE QUE NAO")
- Emojis negativos ou ausencia total de emojis quando antes usava
- Tempo de resposta aumentando (lead perdendo interesse)

### Acao
O bot deve detectar frustacao e acionar handoff ANTES que a objecao escale:
```
Se o lead demonstrar frustacao:
- NAO tente mais uma objecao
- Diga: "Percebi que talvez eu nao esteja conseguindo te ajudar
  da melhor forma. Vou te conectar com [nome] que vai poder
  conversar com mais detalhes!"
- Trigger: Human Handover
```

---

## 7. Templates Curtos (<280 chars) para Clinica/Saude

### Banco expandido em portugues B2C

| Objecao | Resposta (<280 chars) |
|---------|----------------------|
| "Ta caro" | "Entendo! E o valor total ou a parcela que preocupa? Me conta que te mando a opcao que encaixa melhor no seu bolso." |
| "Vou pensar" | "Claro! So me diz: o que ainda te deixa em duvida? Assim consigo te ajudar melhor antes de voce decidir." |
| "Nao tenho tempo" | "Tudo bem! Quando seria melhor — semana que vem ou em duas semanas? A avaliacao e so 20 min." |
| "Ja faco em outro lugar" | "Faz sentido! O que te faria considerar experimentar aqui pelo menos uma vez?" |
| "Nao estou interessada" | "Tudo bem! E so timing ou o procedimento nao faz sentido pra voce agora?" |
| Sem resposta | "Oi [Nome], tudo bem? Sua avaliacao ainda esta reservada ate [data]. Confirma ou prefere outro dia?" |
| "Preciso falar com meu marido/esposa" | "Super normal! Quer que eu mande um resumo pra voce compartilhar? Assim fica mais facil decidir juntos." |
| "Tenho medo" | "Entendo! Muitos pacientes tinham o mesmo receio e ficaram surpresos com o conforto. Quer que eu te conte como funciona?" |

### Principios para texto curto (pesquisa aprofundada)
- **CTAs de duas opcoes** ("A ou B?") em vez de perguntas abertas aumentam resposta significativamente
- Mensagens ideais ficam em **~153 caracteres** — "uma tela"
- Texto e canal de **micro-compromisso**: confirmar, escolher horario, responder UMA pergunta
- Pitch longo vai para a ligacao/reuniao, nao para o chat
- **SPIN adaptado para texto**: perguntas binarias situacionais ("Voce usa X?") em vez de abertas

Fonte: Prospeo.io (https://prospeo.io/s/sales-text-message), SalesMessage, Simplegram

---

## Fontes
- Gong.io: Handling Sales Objections with AI (https://www.gong.io/blog/handling-sales-objections-with-ai)
- Close-O-Matic: AI Sales Compliance (https://www.close-o-matic.com/ai-sales-blog/ai-sales-ethics-and-compliance/ai-sales-outreach-compliance-guide)
- OmniFusion AI: AI Sales Agents Tutorial (https://youtube.com/watch?v=aPsoYnirlgM)
- SaaS Inspection: Astra by Wati BANT (https://youtube.com/watch?v=ITiFtR9D5-w)
