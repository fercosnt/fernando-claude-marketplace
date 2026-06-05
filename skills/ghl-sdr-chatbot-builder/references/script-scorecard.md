# Scorecard de Auditoria de Script/Bot SDR (53 itens)

## Quando carregar
No **modo Auditoria** (quando o usuario pede para avaliar um bot/script SDR ja pronto, proprio ou de terceiro) e como checklist de qualidade final antes de colocar um bot gerado em producao (Fase 3 → deploy).

---

## Como pontuar

- Cada item: **✅ = 1.0 ponto · ⚠️ = 0.5 · ❌ = 0**.
- Score global = soma / 53, em %.
- **Itens 🔴 sao blockers**: um unico 🔴 em aberto (❌) **condena o script**, independente do score global.

### Criterio de aprovacao
> **Aprovado = score global ≥ 80% E zero blocker 🔴 em aberto.**

Os dois precisam ser verdadeiros. 95% com um 🔴 aberto = reprovado.

---

## Os 5 erros que condenam (verificar primeiro)

Antes do scorecard completo, cheque os 5 kill-errors mais comuns — cada um e um 🔴:

1. 🔴 **Budget perguntado primeiro** (deveria ser por ultimo — N→A→T→B)
2. 🔴 **2+ perguntas na mesma mensagem** (deveria ser 1 por mensagem)
3. 🔴 **AI Splitter sem fallback** "No condition met" (V3 — congela o fluxo)
4. 🔴 **Sem disclosure de IA** na primeira mensagem
5. 🔴 **Resposta instantanea** (sem delay de 7-10s — denuncia o bot)

---

## Dimensao 1 — Qualificacao BANT (8 itens · 2 🔴)

- [ ] 🔴 **Ordem N→A→T→B**: necessidade primeiro, budget por ultimo
- [ ] 🔴 **Criterio de qualificado definido** (score/threshold) antes do handoff
- [ ] Need explorado com pergunta aberta + consequencia ("o que acontece se continuar?")
- [ ] Authority abordado de forma natural ("voce decide ou alinha com alguem?")
- [ ] Timeline ancorado em evento/prazo, nao so "quando?"
- [ ] Budget apresentado com **ancora de faixa** ("a maioria investe entre R$X e R$Y") antes de perguntar
- [ ] Scoring atribui ~25pts por dimensao forte → **Hot ≥75 / Warm 50–74 / Cold <50**
- [ ] Alto ticket (>R$50k): nunca pergunta orcamento a frio; quantifica custo-de-inacao primeiro

## Dimensao 2 — Estrutura do Prompt (6 itens)

- [ ] Prompt enxuto (≤100–200 palavras de contexto estatico)
- [ ] 3 blocos do GHL preenchidos (Personalidade / Objetivo / Info adicional) ou nodes equivalentes no V3
- [ ] Instrucoes criticas repetidas em 2-3 pontos
- [ ] Output limitado (~70-90 tokens / Response Style Concise ou Balanced)
- [ ] Variaveis do CRM injetadas ({{contact.first_name}}, custom fields)
- [ ] Sem overprompting (nao lista 20 objecoes nem regras redundantes)

## Dimensao 3 — Conversation Design (9 itens · 1 🔴)

- [ ] 🔴 **1 pergunta por mensagem** (nunca burst de 2+)
- [ ] Max 3-5 perguntas de qualificacao por sessao
- [ ] Progressive disclosure (cada pergunta sobre a resposta anterior)
- [ ] Validacao emocional antes da proxima pergunta
- [ ] Conversation repair (redireciona sem reiniciar quando o lead foge do fluxo)
- [ ] Fall-forward (oferece opcoes em vez de "nao entendi, repita")
- [ ] Referencia inputs anteriores (nao re-pergunta o que ja foi respondido)
- [ ] CTA de duas opcoes ("A ou B?") em vez de pergunta aberta no fechamento
- [ ] (V3) AI Splitter com branch de fallback + Capture com max attempts

## Dimensao 4 — Objecoes (8 itens · 1 🔴)

- [ ] 🔴 **Recua apos objecao clara no WhatsApp** (anti-spam — nao insiste e vira block/quality-score)
- [ ] Framework Acknowledge → Clarify → Value → Confirm (1-2 frases cada)
- [ ] Buyer enablement: oferece ROI/material/timeline antes da objecao surgir
- [ ] Cobre as top 5 objecoes (sem interesse / caro / manda email / sem orcamento / ja temos)
- [ ] Cada step da objecao e 1 mensagem separada (nao bloco unico)
- [ ] Templates curtos (~153 chars, "uma tela")
- [ ] Persiste ate a 2a objecao em canais de alta intencao (webchat/inbound) — com a ressalva WhatsApp acima
- [ ] Recuo gracioso aplica tag + nurturing (preserva o lead, nao descarta)

## Dimensao 5 — Humanizacao (7 itens · 2 🔴)

- [ ] 🔴 **Wait time 7-10s** configurado (nao resposta instantanea)
- [ ] 🔴 **Assume ser IA quando perguntado diretamente** (nao finge ser humano)
- [ ] Sem listas bullet na conversa
- [ ] Sem linguagem corporativa ("prezado", "gostaria de informar")
- [ ] Varia frases de transicao (nao repete "Entendi!")
- [ ] Respostas dentro do limite do canal (30 SMS / 50 WhatsApp / 80 webchat palavras)
- [ ] Split de 40 palavras (2 mensagens de ~40 > 1 bloco de 80)

## Dimensao 6 — Guardrails & Compliance (8 itens · 2 🔴)

- [ ] 🔴 **Disclosure de IA na primeira mensagem** (LGPD + EU AI Act Art. 50)
- [ ] 🔴 **Opt-in explicito antes de coletar PII** (nome/email/telefone/CPF)
- [ ] Finalidade da coleta informada na mesma mensagem (nao em link externo)
- [ ] Opt-out claro em toda interacao proativa ("responda PARAR")
- [ ] Nao repete dados sensiveis de volta (CPF etc.)
- [ ] Bot nao fecha venda, nao da diagnostico, nao promete resultado garantido
- [ ] Handoff para humano funciona quando solicitado / em frustacao
- [ ] WhatsApp: bot e task-oriented com opt-in de 3 elementos (nome do negocio + aviso + coleta do numero)

## Dimensao 7 — Mensurabilidade (7 itens)

- [ ] Tags de qualificacao aplicadas (qualificado/desqualificado/inativo)
- [ ] Custom fields de qualificacao preenchidos durante a conversa
- [ ] Pipeline movido conforme o resultado
- [ ] Evento de handoff rastreavel (instancia registrada)
- [ ] Time-to-first-touch < 5 min (config de wait/trigger compativel)
- [ ] Export auditavel disponivel (Generations API para QA/compliance)
- [ ] Metricas-alvo definidas (qualification rate, show rate, avg messages)

---

## Saida da auditoria

Ao auditar, produzir:
1. **Veredito**: Aprovado / Reprovado + score global (%).
2. **Blockers 🔴 em aberto** (lista — qualquer um reprova).
3. **Itens ⚠️/❌ por dimensao**, com a correcao especifica.
4. **Top 3 fixes priorizados** por impacto.

Benchmark de referencia BR para contextualizar: ver metrics-optimization.md (Leadster: 79,2% qualificado→reuniao, 18,5 msgs/conversa).
