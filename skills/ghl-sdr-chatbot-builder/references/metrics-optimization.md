# Metricas e Otimizacao de SDR Bot

## Quando carregar
Fase pos-deploy (monitoramento), quando o usuario perguntar "como saber se o bot esta bom", e para revisao periodica de performance.

---

## 1. KPIs Primarios

### Metricas de Conversa (qualidade do bot)

| KPI | Benchmark | O que indica | Como medir no GHL |
|-----|-----------|-------------|-------------------|
| **Goal Completion Rate** | ~10% (lead form) | % de leads que completaram o objetivo | Tags de qualificacao / actions triggered |
| **Fallback Rate** | < 10% | % de msgs que o bot nao entendeu | Revisar logs — msgs sem resposta adequada |
| **Human Handoff Rate** | Minimizar | % de conversas escaladas | Dashboard: Human Handover Instances |
| **Avg Messages per Contact** | 5-10 | Eficiencia do fluxo | Dashboard: Average Messages per Contact |
| **Response Latency** | < 10 segundos | Tempo de resposta do bot | Config: Wait Time (controlavel) |

### Metricas de Negocio (resultado do bot)

| KPI | Benchmark | O que indica | Como medir |
|-----|-----------|-------------|------------|
| **Qualified Meetings/mes** | 20-25 (inbound) | Reunioes qualificadas geradas | Pipeline stage: "Agendado" |
| **Meeting Show Rate** | 75% medio, 85% bom | % que comparece a reuniao | Confirmacao no CRM |
| **Reply Rate** | 8-15% excelente, <2% problema | Engajamento dos leads | Msgs respondidas / msgs enviadas |
| **Time-to-First-Touch** | < 5 minutos | Velocidade de resposta ao lead | Timestamp primeira msg do bot |
| **Qualification Rate** | Depende do nicho | % de leads qualificados pelo bot | Tags: qualificado vs total |

---

## 2. Anti-Metricas (o que NAO otimizar isoladamente)

### Bad Deflection
**Deflection Rate alta + CSAT caindo = problema**

O bot "resolve" sem satisfazer. O lead nao volta, nao agenda, nao recomenda.

**Regra**: SEMPRE monitorar deflection rate pareado com CSAT. Nunca otimizar um sem o outro.

### Volume de Conversas
Muitas conversas ≠ bot bom. Se o bot gera volume mas nao qualifica, esta gerando trabalho sem resultado.

### Tempo de Conversa Longo
Conversas longas podem indicar que o bot esta enrolando em vez de qualificar rapido. Avg Messages per Contact alto (>15) e sinal de prompt mal configurado.

---

## 3. Dashboard do GHL — O que Olhar

### Metricas disponiveis nativamente
- Total Unique Contacts
- Total Messages
- Average Messages per Contact
- Total Actions Triggered
- Total Appointments Booked
- Human Handover Instances
- Time Saved
- Bot-to-bot transfers
- Filtros: Date Range, Channel, Agent

### Metricas que o GHL NAO oferece nativamente
- Fallback Rate (precisa revisar logs manualmente)
- CSAT (precisa configurar pesquisa pos-atendimento)
- Qualification Rate (precisa usar tags + filtros)
- Conversion funnel por etapa (precisa de pipeline customizado)
- A/B testing de prompts (nao tem funcionalidade nativa)

### Workarounds
| Metrica ausente | Como medir |
|----------------|------------|
| Fallback Rate | Revisar "Missed Messages" nos logs semanalmente |
| CSAT | Enviar pesquisa rapida apos conversa (workflow) |
| Qualification Rate | Tag "qualificado" vs total de contatos no periodo |
| A/B testing | Alternar prompt semanalmente + comparar metricas |

---

## 4. Loop de Otimizacao

### Ciclo Semanal
1. **Revisar logs de conversa** (30 min/semana)
   - Identificar conversas que falharam (lead desistiu, bot nao entendeu)
   - Listar "Missed Messages" — perguntas que o bot nao soube responder
   - Anotar objecoes recorrentes nao mapeadas

2. **Analisar metricas do dashboard**
   - Avg Messages per Contact subindo? → prompt pode estar prolixo
   - Human Handover Instances subindo? → bot nao esta conseguindo resolver
   - Appointments Booked caindo? → verificar CTA e fluxo de agendamento

### Ciclo Mensal
3. **Retreinar/ajustar prompt** (2-4h/mes)
   - Adicionar objecoes novas ao prompt
   - Ajustar tom se feedback indicar "muito formal" ou "muito informal"
   - Refinar perguntas de qualificacao baseado no que funcionou
   - Atualizar FAQ/base de conhecimento

4. **Analisar "Top Unseen Intents"**
   - O que o bot NAO sabe responder e o input mais valioso para melhoria
   - Priorizar por frequencia: intents que aparecem 3+ vezes/semana

### Ciclo Trimestral
5. **Revisao estrutural**
   - O fluxo de qualificacao ainda faz sentido?
   - Novos servicos/produtos para adicionar?
   - Metricas de negocio (meetings booked, show rate) melhorando?
   - Comparar com baseline do trimestre anterior

---

## 5. Metricas Emergentes de IA (2026)

| Metrica | O que mede | Por que importa |
|---------|-----------|-----------------|
| **Signal Coverage** | % de sinais de intencao capturados pelo bot | Bot detecta interesse mesmo em mensagens ambiguas? |
| **Time-to-First-Touch** | Tempo entre sinal e primeira interacao | Velocidade mata — < 5 min = 21x mais qualificacao |
| **Revenue per Signal** | Receita atribuivel por sinal processado | ROI real do bot |
| **Human Effort per Meeting** | Esforco humano necessario por reuniao | Quanto o bot realmente economiza? |
| **Token Consumption** | Custo por conversa em tokens LLM | Controle de custo operacional |

Fonte: MarketBetter SDR Metrics 2026

---

## 6. A/B Testing de Prompts no GHL

O GHL nao tem A/B testing de prompts built-in, mas ha um workaround funcional usando workflows.

### Metodo Recomendado: Split Action + Update Bot (verificado)

**Passo a passo:**
1. Criar dois bots separados (Bot A e Bot B) com prompts diferentes
2. No workflow de entrada de lead, adicionar **Split Action** (50/50)
3. Em cada path, adicionar **Update Conversation AI Bot and Status** apontando para o bot correspondente
4. Adicionar tag em cada path (`bot_variant_A` / `bot_variant_B`)
5. Rastrear metricas por tag no CRM
6. Usar calculadora de significancia estatistica — meta de **95% de confianca** antes de declarar vencedor

Fonte: GHL Help Portal — Split Action (https://help.gohighlevel.com/support/solutions/articles/155000001717-split-action) + Update Bot Action (https://help.gohighlevel.com/support/solutions/articles/155000003821-update-conversation-ai-bot-and-status-workflow-action)

### Metodo Simples: "Semana A / Semana B"
1. **Semana 1**: Prompt versao A (ex: tom mais casual)
2. **Semana 2**: Prompt versao B (ex: tom mais profissional)
3. Comparar metricas: Qualification Rate, Avg Messages, Handoff Rate
4. Manter a versao vencedora
5. Menos preciso (variaveis externas mudam entre semanas)

### Metodologia de teste (best practices)
- Definir **Goal Metrics** (o que quer melhorar) E **Guardrail Metrics** (o que nao pode regredir)
- Comecar com 1-5% do trafego no variant, escalar gradualmente
- 20-50 conversas representativas sao suficientes para avaliacao inicial
- Feature flags permitem desativar variante imediatamente se guardrail regredir

Fonte: Braintrust (https://www.braintrust.dev/articles/ab-testing-llm-prompts), GrowthBook (https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)

### O que testar
| Variavel | Hipotese | Metrica para medir |
|----------|----------|-------------------|
| Tom (casual vs profissional) | Casual converte mais no WhatsApp | Qualification Rate |
| Numero de perguntas (3 vs 5) | Menos perguntas = menos drop-off | Avg Messages + Qualification Rate |
| CTA (agendamento vs material) | Material primeiro gera mais confianca | Handoff Rate + Meeting Show Rate |
| Wait time (5s vs 10s) | 10s parece mais humano | Reply Rate + CSAT |
| Disclosure (inicio vs atrasado) | Inicio gera mais confianca | CSAT + Reply Rate |

---

## 7. Benchmarks por Setor

### Internacional (US/Europa)
| Setor | Resolution Rate | Show Rate | Qualification Rate |
|-------|----------------|-----------|-------------------|
| Saude/Clinicas | 60-70% | 80-85% | 15-25% |
| SaaS B2B | 65-75% | 70-80% | 10-20% |
| E-commerce | 75-80% | N/A | 20-30% |
| Financeiro | 70-75% | 75-85% | 10-15% |
| Educacao | 65-75% | 65-75% | 15-20% |

### Baseline BR — estudo Leadster (chatbot SDR real)

Estudo de **635 conversas** (dez/2025–jan/2026) de um chatbot de qualificacao BR:

| Metrica | Valor | Leitura |
|---------|-------|---------|
| Qualificado → reuniao | **79,2%** (57 de 72 leads qualificados) | Conversao pos-qualificacao alta |
| 1a resposta (mediana) | **0,8 min** (82% < 5 min) | Speed-to-lead na pratica |
| Mensagens / conversa qualificada | **18,5** | ≈ janela efetiva ~15–20 turnos |
| Conversas simultaneas sem degradar | 31+ | ≈ 10–15 SDRs humanos |
| Rapport na 1a resposta | 68,2% vs 25,4% humano | 2,7x |

> **Ressalva de amostra:** a base qualificada e pequena (72 leads → 57 reunioes). Os 79,2% sao robustos para **conversao pos-qualificacao**, mas a amostra limita extrapolacao. Saude/estetica aparecem no estudo sem caso com metrica publicada. Tratar como baseline indicativo, nao como garantia por nicho.

### Leadster vs GHL — complementam, nao competem
- **Leadster** = captura/qualificacao no **site** (topo de funil; precos BRL: Free 15 leads · Starter R$142 · Pro R$154/mes). Sem CRM nativo — exporta via webhook/Zapier.
- **GHL** = CRM + nurturing + follow-up + agendamento + WhatsApp Conversation AI nativo (desde jan/2025).
- **Stack recomendada:** Leadster (captura no site) → GHL (CRM e operacao). Nao e ou-um-ou-outro.

### Brasil (dados verificados)

| Metrica | Valor Brasil | Fonte |
|---------|-------------|-------|
| Taxa abertura WhatsApp | 97-98% | DisparoPro, AiSensy |
| Melhor horario envio | 10h-15h | DisparoPro |
| Frequencia ideal | Max 3x/semana | DisparoPro |
| Conversao WhatsApp vs e-commerce | 6x maior | OmniChat 2025 |
| Conversao leads via chatbot WhatsApp | 28% | OmniChat 2025 |
| IA resolve sem humano | 80% | OmniChat 2025 |
| IA gera vendas fora do horario | 23% das vendas | OmniChat 2025 |
| SDR outbound conversao | 17% | Meetime |
| SDR inbound conversao | 23% | Meetime |
| Reunioes/mes SDR outbound | 12-15 | Meetime |
| Reunioes/mes SDR inbound | ~15 SALs | Meetime |
| No-show rate benchmark | <15% | Meetime |
| Leads abordados/mes por SDR | 63 | Meetime |
| Salario SDR Brasil | R$ 2.500-4.500 + comissoes | Exact Sales |
| Times que nao bateram meta 2024 | 72% | RD Station |
| Times que integram WhatsApp ao CRM | 31% | RD Station |
| Times usando IA em vendas | 58% | RD Station |

Fontes:
- OmniChat: Chat Commerce Report 2025 (https://omni.chat/pesquisa-omnichat-2025/)
- Meetime: Inside Sales Benchmark Brasil (https://lp.meetime.com.br/tofu-inside-sales-benchmark-brasil)
- RD Station: Panorama Marketing e Vendas 2025 (https://www.rdstation.com/pesquisas/panoramas-rdstation-2025/)
- DisparoPro: Relatorio WhatsApp 2026 (https://disparopro.com.br/relatorio-whatsapp-marketing/)
- Exact Sales: Agendamento (https://www.exactsales.com.br/agendamento-de-reuniao-online/)

Fonte: Quickchat AI, MarketBetter

---

## 8. Checklist de Monitoramento

### Diario (5 min)
- [ ] Verificar se o bot esta ativo e respondendo
- [ ] Checar se houve handovers inesperados

### Semanal (30 min)
- [ ] Revisar 5-10 conversas completas nos logs
- [ ] Listar Missed Messages / perguntas sem resposta
- [ ] Anotar objecoes novas que apareceram
- [ ] Verificar Avg Messages per Contact (benchmark: 5-10)

### Mensal (2-4h)
- [ ] Atualizar prompt com objecoes novas
- [ ] Ajustar FAQ/base de conhecimento
- [ ] Analisar Top Unseen Intents
- [ ] Comparar Qualification Rate vs mes anterior
- [ ] Comparar Meeting Show Rate vs mes anterior

### Trimestral (meio dia)
- [ ] Revisao estrutural do fluxo
- [ ] A/B test de uma variavel
- [ ] Comparar ROI: custo do bot vs SDR humano equivalente
- [ ] Decidir: manter, ajustar ou redesenhar o fluxo

---

## Fontes
- Quickchat AI: Chatbot Analytics (https://quickchat.ai/post/chatbot-analytics)
- MarketBetter: SDR Metrics 2026 (https://marketbetter.ai/blog/sdr-metrics-kpis-benchmarks-2026/)
- Dialzara: KPI Chatbot 2025 (https://dialzara.com/blog/ai-chatbot-kpis-what-to-track-in-2025)
- GHL Docs: Dashboard (https://help.gohighlevel.com/support/solutions/articles/155000005427-conversation-ai-agents-dashboard)
- GHL Wizard: Max messages e configuracoes (https://youtube.com/watch?v=G5XBmvvXB4k)
