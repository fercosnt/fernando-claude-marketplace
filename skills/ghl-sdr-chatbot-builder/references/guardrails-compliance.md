# Guardrails e Compliance para SDR Bot

## Quando carregar
Fase 2A (setup do Conversation AI), Fase 3A (compilacao do briefing para prompt-engineer), e SEMPRE quando o canal for WhatsApp.

---

## 1. Framework de Guardrails (4 Pontos de Intervencao)

| Ponto | Quando atua | O que faz | Exemplo para SDR |
|-------|-------------|-----------|------------------|
| **Pre-input** | Antes do usuario falar | Define politicas e limites | "Max 1 insistencia apos objecao", "Nunca prometa desconto" |
| **Input** | Ao receber mensagem | Filtra requests nocivos | Bloquear prompt injection, detectar spam |
| **Output** | Antes de enviar resposta | Valida contra brand voice | Verificar tom, pressao, promessas |
| **Post-output** | Apos enviar | Loga para auditoria | Detectar patterns de pressao indevida |

Fonte: AltexSoft — AI Guardrails in Agentic Systems

---

## 2. Guardrails Operacionais para SDR Bot

### O que o bot PODE fazer
- Qualificar leads com perguntas conversacionais
- Fornecer informacoes sobre servicos/produtos da base de conhecimento
- Agendar consultas/reunioes
- Coletar dados com consentimento
- Transferir para humano quando necessario

### O que o bot NAO PODE fazer
- Fechar vendas autonomamente (human oversight obrigatorio)
- Prometer resultados especificos
- Dar diagnosticos medicos/financeiros/juridicos
- Pressionar apos objecao direta (max 1 tentativa)
- Inventar informacoes nao presentes na base
- Coletar/armazenar PII sem consentimento explicito
- Responder fora do escopo (politica, religiao, opinioes)

### Relevance Classifiers
Perguntas fora do escopo do bot devem gerar redirecionamento, nao resposta forcada:
- **Errado**: Bot tenta responder sobre politica ou opinioes
- **Certo**: "Essa pergunta foge um pouco do meu escopo! Mas posso te ajudar com [escopo]. Quer saber mais?"

---

## 3. LGPD (Lei 13.709/2018)

### Obrigacoes nao-negociaveis para chatbots de vendas no Brasil

#### 3.1 Disclosure de IA
O bot DEVE informar que e IA **antes de coletar qualquer dado**:
```
"Oi! Sou a [nome], assistente virtual da [empresa]. Vou te ajudar
a encontrar a melhor opcao pra voce! 😊"
```
A palavra "virtual" ou "assistente de IA" deve aparecer na primeira mensagem.

#### 3.2 Consentimento (Opt-in)
Antes de armazenar nome, email, telefone, CPF:
```
"Para te ajudar melhor, preciso do seu nome e email.
Seus dados serao usados apenas para [finalidade]
e armazenados por [periodo]. Tudo bem pra voce?"
```
- Aguardar confirmacao explicita ("sim", "pode", "ok")
- Sem confirmacao = nao coletar

#### 3.3 Finalidade e Retencao
- Comunicar no momento da coleta (nao em link externo)
- Ser especifico: "para agendar sua consulta" > "para fins comerciais"

#### 3.4 Direitos do Titular
O lead pode pedir diretamente no chat:
- "Quais dados meus voces tem?" → bot deve saber responder ou escalar
- "Deletem meus dados" → trigger de workflow para equipe de compliance
- "Corrijam meu email" → bot pode atualizar ou escalar

#### 3.5 Seguranca Tecnica (obrigatorio, nao recomendado)
- Criptografia dos dados em transito e repouso
- Controle de acesso (quem ve os dados do chat)
- Auditoria de logs (registrar interacoes)

### Template de Prompt LGPD
Adicionar ao prompt do bot:
```
REGRAS DE COMPLIANCE:
- Sempre se identifique como assistente virtual na primeira mensagem
- Antes de coletar qualquer dado pessoal, peca consentimento explicito
- Informe a finalidade da coleta na mesma mensagem
- Se o usuario pedir para deletar dados ou falar com humano, transfira imediatamente
- NUNCA repita dados sensiveis do usuario de volta na conversa (CPF, etc.)
```

Fonte: lgpdbrasil.com.br — Chatbot e LGPD

---

## 4. WhatsApp Business API — Restricoes Criticas

### 4.1 Opt-in Obrigatorio (3 elementos)
1. Nome do negocio identificado
2. Declaracao de que o usuario recebera mensagens
3. Coleta explicita do numero de telefone

Atualizacao de novembro 2024 consolidou essa exigencia.
Fonte: WuSeller

### 4.2 Proibicao de AI General-Purpose (Outubro 2025)
A Meta proibiu chatbots de IA general-purpose na API do WhatsApp. Apenas **task-oriented automation flows** sao permitidos:
- Qualificacao de leads (OK — e task-oriented)
- Agendamento (OK)
- Suporte/FAQ (OK)
- Conversa aberta tipo ChatGPT (PROIBIDO)

**Implicacao para SDR bot**: desenhar como bot de qualificacao com escopo definido, nao como "assistente que conversa sobre tudo".

Fonte: TechCrunch / Respond.io

### 4.3 Tipos de Mensagem e Custo
| Tipo | Quando usar | Custo relativo |
|------|-------------|----------------|
| Utility | Confirmacoes, atualizacoes | Mais barato |
| Marketing | Promocoes, outreach | Mais caro |
| Authentication | Verificacao de identidade | Medio |

### 4.4 Consequencias de Violacao
- Quality score degradado → alcance reduzido
- Suspensao temporaria da conta
- **Banimento permanente** em casos graves
- Denuncias de usuarios afetam quality score diretamente

### 4.5 Regra Anti-Spam para SDR Bot
- Nao insistir apos objecao (1 tentativa max no WhatsApp)
- Oferecer opt-out claro em toda interacao
- Respeitar horarios (nao enviar de madrugada)
- Nao reenviar a mesma mensagem se nao houve resposta

---

## 5. FTC e Tendencias Regulatorias Globais

### 5 Don'ts da FTC para AI Chatbots
1. NAO fazer claims falsos sobre capacidades da IA
2. NAO ocultar natureza artificial do agente
3. NAO usar tacticas manipulativas de pressao
4. NAO coletar dados sem transparencia
5. NAO tratar dados de menores sem consentimento parental

Maine (EUA) tornou disclosure obrigatoria em setembro 2025. Tendencia global.

Fonte: Fenwick/FTC

### Disclosure-First Framework
1. Bot se identifica como IA no inicio
2. Explica proposito do contato
3. Oferece opt-out e escalation para humano de forma inequivoca
4. Opt-outs propagam para todos os canais em segundos

Fonte: Close-O-Matic

---

## 6. Checklist de Compliance para Deploy

Antes de ativar o bot em producao:

- [ ] Primeira mensagem inclui disclosure de IA
- [ ] Opt-in antes de coletar dados pessoais
- [ ] Finalidade de coleta informada na mensagem
- [ ] Bot nao repete dados sensiveis de volta
- [ ] Handoff para humano funciona quando solicitado
- [ ] Opt-out disponivel e funcional
- [ ] Bot nao faz claims de resultados garantidos
- [ ] Bot nao pressiona apos objecao direta
- [ ] Logs de conversa armazenados com seguranca
- [ ] Horarios de envio configurados (nao madrugada)
- [ ] WhatsApp: bot e task-oriented, nao general-purpose
- [ ] WhatsApp: opt-in com 3 elementos presente

---

## 7. LGPD: Bases Legais Alternativas ao Consentimento

### Interesse Legitimo (Art. 10 LGPD)
Valido para chatbots SDR quando o lead ja demonstrou interesse (visitou site, preencheu formulario). Requer Teste de Proporcionalidade documentado:

1. **Legitimidade**: documentar por que o uso serve ao negocio sem violar direitos
2. **Necessidade**: coletar apenas o estritamente necessario
3. **Balanceamento**: a abordagem nao e invasiva? O prospect esperaria esse contato?
4. **Salvaguardas**: aviso de privacidade + opt-out + seguranca

**PROIBIDO**: listas compradas para outreach via chatbot — nao existe base legal.

**Dados sensiveis (saude, biometria)**: NAO podem usar Interesse Legitimo — exigem consentimento explicito.

Fonte: RD Station (https://www.rdstation.com/blog/marketing/legitimo-interesse/)

### Nota Tecnica ANPD 12/2025 — Decisoes Automatizadas
A ANPD publicou em maio/2025 orientacao sobre bots de IA:
- Decisoes automatizadas (qualificacao de lead, recusa) ativam Art. 20 LGPD — direito a revisao humana
- Bot DEVE informar criterios e procedimentos de forma clara
- Bases legais alternativas ao consentimento sao reconhecidas com salvaguardas
- Prioridades de fiscalizacao ANPD 2026-2027: transparencia, vies, seguranca

Fonte: Lefosse/ANPD (https://lefosse.com/noticias/inteligencia-artificial-anpd-publica-nota-tecnica-sobre-decisoes-automatizadas/)

### Casos de Sancao ANPD (referencia)
- **Telekall (2023)**: R$ 14.400 — uso de dados sem base legal
- **Meta (2024)**: R$ 50 mil/dia — IA sem disclosure, sem salvaguardas, sem respeito a direitos
- Nenhum caso especifico de chatbot de vendas ate 2025 — enforcement incipiente mas crescendo

Fonte: ANPD (https://www.gov.br/anpd/pt-br/assuntos/noticias/)

---

## 8. Templates de Disclosure LGPD (em Portugues)

### Template minimo (consentimento)
```
Ola! Sou um assistente virtual da [Empresa].
Para continuar, preciso coletar: nome, telefone e interesse.
Seus dados sao tratados conforme a LGPD e nossa Politica de Privacidade.
Voce concorda? (Sim / Nao quero continuar)
```

### Template com Interesse Legitimo (lead quente)
```
Ola! Vi seu interesse em [servico] no nosso site.
Sou assistente virtual da [Empresa] — posso tirar suas duvidas?
Qualquer dado compartilhado e tratado conforme a LGPD.
Quer continuar? (Sim / Prefiro nao)
```

### Template para prompt GHL (compliance)
```
REGRAS DE COMPLIANCE (OBRIGATORIO):
- Sempre se identifique como assistente virtual na primeira mensagem
- Antes de coletar dado pessoal, peca consentimento explicito
- Informe a finalidade na mesma mensagem da coleta
- Se pedirem para deletar dados ou falar com humano, transfira imediatamente
- NUNCA repita dados sensiveis de volta (CPF, etc.)
- Se o lead pedir explicacao sobre decisao do bot, transfira para humano (Art. 20 LGPD)
```

Fontes adicionais:
- InBot: Como adequar chatbot a LGPD (https://inbot.com.br/chatbots/como-adequar-seu-chatbot-a-lgpd/)
- Blip.ai: LGPD no contexto dos chatbots (https://www.blip.ai/blog/chatbots/lgpd-no-contexto-dos-chatbots/)
- Botmaker: LGPD e privacidade (https://botmaker.com/pt/publicacoes/lgpd-importancia-privacidade-usuarios/)
- Confidata: ANPD regulacao IA 2026-2027 (https://confidata.com.br/blog/anpd-regulacao-ia-brasil-2026-2027)

---

## Fontes
- LGPD Brasil: Chatbot e LGPD (https://www.lgpdbrasil.com.br/como-garantir-que-o-uso-do-chatbot-nao-viole-a-lgpd/)
- WuSeller: WhatsApp Opt-In Rules (https://www.wuseller.com/whatsapp-business-knowledge-hub/whatsapp-business-opt-in-rules-prevent-bans-grow-lists/)
- Respond.io: WhatsApp AI Policy (https://respond.io/blog/whatsapp-general-purpose-chatbots-ban)
- Fenwick/FTC: AI Chatbot Don'ts (https://www.fenwick.com/insights/publications/ftc-outlines-five-donts-for-ai-chatbots)
- Close-O-Matic: AI Sales Compliance (https://www.close-o-matic.com/ai-sales-blog/ai-sales-ethics-and-compliance/ai-sales-outreach-compliance-guide)
- AltexSoft: AI Guardrails (https://www.altexsoft.com/blog/ai-guardrails/)
- Salesforce Trailhead: Agentforce Guardrails
