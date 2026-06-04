# Padroes de Qualificacao para Chatbot SDR

## Quando carregar
Fase 1B (analise de scripts SDR) e Fase 3A (compilacao do briefing para prompt-engineer).

---

## 1. Framework BANT Adaptado para Chatbot

### Budget (Investimento)
- NAO perguntar valor direto no inicio — gera resistencia
- Abordagem indireta: "Voce ja pesquisou valores para esse tipo de tratamento/servico?"
- Se lead demonstra preocupacao com preco → classificar como "sensivel a preco" (nao desqualificar)
- Em contexto premium (ex: Beauty Smile): qualificar se lead entende o posicionamento premium

### Authority (Decisor)
- "Essa decisao seria so sua ou voce precisa alinhar com alguem?"
- Se nao e decisor → coletar info e sugerir "convide [pessoa] para a avaliacao"
- NAO desqualificar por nao ser decisor — influenciadores tambem convertem

### Need (Necessidade)
- Pergunta aberta: "O que te motivou a buscar [tratamento/servico]?"
- Mapear: dor funcional (problema real) vs dor emocional (como se sente)
- Urgencia: "Ha quanto tempo voce esta pensando nisso?"
- Evento gatilho: "Tem algum evento proximo que motivou?" (casamento, viagem, reuniao)

### Timeline (Urgencia)
- "Quando voce gostaria de resolver isso?"
- "Voce tem disponibilidade essa semana para uma avaliacao?"
- Lead sem urgencia → nurturing (follow-up em 7-14 dias)
- Lead com evento proximo → fast-track para agendamento

---

## 2. Framework SPIN Adaptado para Chatbot

### Situation (Situacao)
Perguntas de contexto — NAO fazer muitas (max 2-3), chatbot precisa ser agil:
- "Voce ja fez algum tratamento similar antes?"
- "Voce ja tem um profissional de referencia?"
- "Como voce conheceu a [clinica/empresa]?"

### Problem (Problema)
Identificar a dor principal:
- "O que mais te incomoda sobre [situacao atual]?"
- "O que voce mudaria se pudesse?"
- Escuta ativa: repetir o problema do lead para gerar rapport

### Implication (Implicacao)
Ampliar a consequencia de nao agir — usar com moderacao no chat:
- "E como isso tem impactado seu dia a dia?"
- "Voce sente que isso tem afetado sua confianca/produtividade?"
- NAO exagerar — tom empatetico, nao manipulativo

### Need-Payoff (Beneficio)
Fazer o lead visualizar a solucao:
- "Como seria se voce resolvesse isso?"
- "O que mudaria na sua rotina?"
- Conectar o beneficio ao servico oferecido

---

## 3. Arvore Decisoria Conversacional

### Estrutura padrao de qualificacao via chat

```
[Lead entra no chat]
    |
    v
[Saudacao + Identificacao]
    "Oi! Tudo bem? Vi que voce se interessou por [tratamento/servico]."
    "Posso te ajudar! Como voce prefere que eu te chame?"
    |
    v
[Coleta de Nome] → salvar em custom field
    |
    v
[Necessidade Principal]
    "O que te motivou a buscar [tratamento/servico]?"
    |
    v
[Classificacao da Necessidade]
    ├── Necessidade clara → prosseguir para qualificacao
    ├── Explorando opcoes → fornecer info + qualificar
    └── Apenas curiosidade → info rapida + nurturing
    |
    v
[Qualificacao (BANT/SPIN simplificado)]
    - Ja fez tratamento similar?
    - Tem urgencia/evento?
    - Decisao e solo ou compartilhada?
    |
    v
[Lead Scoring]
    ├── Score >= threshold → QUALIFICADO
    │   → "Otimo! Vou te conectar com [consultor] que vai cuidar de tudo pra voce."
    │   → Aplicar tag + mover pipeline + notificar humano
    │
    ├── Score medio → MORNO
    │   → Oferecer conteudo/info adicional
    │   → "Posso te enviar mais detalhes sobre [tratamento]?"
    │   → Follow-up em 24-48h
    │
    └── Score baixo → FRIO/DESQUALIFICADO
        → "Fico a disposicao quando voce quiser saber mais!"
        → Aplicar tag + nurturing sequence
```

---

## 4. Triggers de Handoff para Humano

### Handoff IMEDIATO (bot para de responder e passa para humano)
- Lead pede explicitamente para falar com humano
- Lead demonstra irritacao ou insatisfacao com o bot
- Assunto medico/clinico que exige avaliacao profissional
- Lead menciona emergencia ou urgencia real
- Bot nao entende a mensagem apos 2 tentativas
- Lead faz pergunta sobre precos especificos (se a politica for nao informar via bot)

### Handoff QUALIFICADO (bot completa qualificacao e passa)
- Todos os campos obrigatorios preenchidos
- Lead score >= threshold definido
- Lead demonstra interesse ativo em agendar/comprar
- Lead tem urgencia/timeline definido

### Handoff PROGRAMADO (bot agenda follow-up humano)
- Lead interessado mas sem urgencia
- Lead precisa consultar outra pessoa
- Lead pediu para retornar em outro momento

---

## 5. Criterios de Desqualificacao

### Desqualificacao SOFT (nurturing — nao descarta)
- Sem urgencia definida
- Apenas pesquisando precos
- Localizacao fora da area de atendimento (verificar antes de desqualificar)
- Budget declaradamente incompativel (com cuidado — nao assumir)

### Desqualificacao HARD (encerrar interacao)
- Spam ou mensagens sem sentido
- Lead nao e pessoa real (bot/automacao)
- Solicitacao de servico que a empresa nao oferece
- Comportamento abusivo ou assedio

---

## 6. Regras de Conversa para WhatsApp

### Tom e formato
- Mensagens curtas (max 3 linhas por bloco)
- Linguagem conversacional, nao corporativa
- Emojis com moderacao (1-2 por mensagem max)
- Nunca enviar paredes de texto
- Usar quebra de linha entre blocos de informacao

### Tempo de resposta
- Resposta instantanea na primeira mensagem
- Delay simulado de 2-5 segundos em mensagens subsequentes (parecer humano)
- Se lead demora para responder: follow-up em 1h, depois 24h, depois 72h

### O que o bot NAO deve fazer
- Inventar informacoes que nao possui
- Dar diagnosticos medicos ou financeiros
- Prometer resultados especificos
- Pressionar excessivamente para agendamento
- Enviar audio ou imagens nao autorizados
- Responder fora do escopo (politica, religiao, etc.)

---

## 7. Integracao com Frameworks Beauty Smile

Quando o contexto for Beauty Smile, a qualificacao se enriquece com:

### Do ICP
- Validar se lead corresponde ao perfil demografico (renda, localizacao, faixa etaria)
- Adaptar linguagem ao nivel socioeconomico do ICP

### Do Framework 3D
- **Dores**: usar as dores mapeadas para gerar rapport ("entendo que [dor] e muito desconfortavel...")
- **Duvidas**: antecipar as duvidas mais comuns nos scripts do bot
- **Desejos**: conectar o tratamento ao desejo mapeado ("imagina [desejo realizado]...")

### Da Matriz de Objecoes
- Quando lead apresentar objecao conhecida → usar o script de contorno mapeado
- Priorizar objecoes de alta frequencia nos fluxos do bot

### Da Matriz de Implicacao
- Usar perguntas de implicacao mapeadas para ampliar consciencia do problema
- Conectar argumentos validados ao fechamento

---

## 8. Metricas de Qualificacao

### KPIs do bot SDR
- **Taxa de qualificacao**: % de leads que passam pelo fluxo completo
- **Taxa de handoff**: % de leads passados para humano (qualificados)
- **Taxa de agendamento** (v2): % de leads que agendam via bot
- **Tempo medio de qualificacao**: minutos do primeiro contato ao handoff
- **Taxa de desistencia**: % de leads que param de responder em cada etapa
- **NPS do atendimento bot**: satisfacao pos-interacao (pesquisa rapida)

### Pontos de otimizacao
- Etapa com maior taxa de desistencia → simplificar ou remover
- Perguntas que geram silencio → reformular ou tornar opcional
- Objecoes recorrentes nao mapeadas → adicionar ao fluxo
