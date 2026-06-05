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

### 4.2 Ban de AI General-Purpose — SUSPENSO pelo CADE (jan/2026)

**Correcao importante:** o ban que a Meta anunciou em out/2025 (proibindo chatbots de IA general-purpose de terceiros na API do WhatsApp) foi **SUSPENSO**. Em **13/jan/2026 o CADE ordenou a Meta suspender** essa restricao, por entender que era **conduta exclusionaria** favorecendo a propria Meta AI (questao antitruste). Processos paralelos foram abertos na UE e na Italia.

**Estado atual:** **bots SDR de terceiros voltaram a operar legalmente no WhatsApp BR** durante a investigacao. A orientacao da Respond.io de out/2025 esta **desatualizada**.

**Mas as boas praticas continuam valendo** (independente do ban):
- Desenhar o bot como **task-oriented** (qualificacao/agendamento/FAQ) e nao "ChatGPT que fala de tudo" — reduz risco de quality-score e de spam.
- O opt-in de 3 elementos (§4.1) e as regras anti-spam/quality-score **continuam ativos** e independem do ban.

Fonte: CADE (decisao 13/jan/2026) — substitui a leitura anterior de TechCrunch/Respond.io

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

## 5. EU AI Act, FTC e Tendencias Regulatorias Globais

### EU AI Act — Artigo 50 (em vigor 2/ago/2026)
Se o bot conversa com **qualquer lead na UE**, o Art. 50 exige disclosure de IA **"clara e distinta" antes/no inicio da primeira interacao** — nao no rodape nem nos T&C.
- Multa: ate **€7,5M ou 1% do faturamento global**.
- Exemplo compativel: exibir "Voce esta interagindo com IA" **antes** da primeira mensagem.
- A Comissao Europeia publicou diretrizes de transparencia (rascunho, mai/2026).

**Implicacao pratica:** o disclosure na primeira mensagem (§3.1) ja atende LGPD **e** EU AI Act — manter isso como passo nao-negociavel do fluxo, V3 incluido (primeiro node = disclosure).

### Novas leis estaduais nos EUA (alcance comercial)
- **Maine** (set/2025): disclosure de chatbot obrigatoria.
- **Nebraska** Conversational AI Safety Act (em vigor jul/2027, escopo amplo).
- **Washington** HB 2225 (em vigor jan/2027).
- **Maine + New Jersey**: disclosure exigido se o bot "puder enganar". (Maioria das leis estaduais foca companion-chatbots, fora do escopo de vendas — mas elevam a regua.)

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
- [ ] WhatsApp: bot e task-oriented (boa pratica; o ban de terceiros esta suspenso pelo CADE desde jan/2026)
- [ ] WhatsApp: opt-in com 3 elementos presente
- [ ] Opt-in registrado com timestamp + IP + canal + texto aceito (ANPD NT 1/2026)
- [ ] Se ha leads na UE: disclosure de IA antes da 1a interacao (EU AI Act Art. 50)

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

### Nota Tecnica ANPD nº 1/2026 — Output de IA = dado pessoal (a mais recente)
Publicada com MPF + SENACON (caso Grok/X), e o **unico documento normativo de IA da ANPD em 2026**. Pontos centrais para SDR bot:
- **A saida gerada pela IA E dado pessoal** quando referenciavel a pessoa identificavel.
- **O ciclo inteiro — input → processamento → output → distribuicao — e "tratamento de dados" sob a LGPD.** Cada mensagem gerada pelo LLM para um lead precisa de **base legal** (consentimento ou interesse legitimo documentado).
- Regulacao do Art. 20 (decisoes automatizadas) ainda pendente (roadmap 2026–2027).
- O PL 2338/2023 (Marco Legal da IA) **ainda nao e lei** (aprovado no Senado em dez/2024, aguarda a Camara).

**Implicacao pratica:** tratar toda mensagem do bot como tratamento de dados — disclosure + base legal + opt-out funcionam como salvaguarda. Registrar o opt-in com **timestamp + IP + canal + texto aceito**.

Fonte: ANPD Nota Tecnica nº 1/2026 (MPF/SENACON)

### Nota Tecnica ANPD 12/2025 — Decisoes Automatizadas (contexto anterior)
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
