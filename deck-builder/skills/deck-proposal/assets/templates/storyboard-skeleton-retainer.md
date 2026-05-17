# STORYBOARD esqueleto — modo `retainer` (servico continuo, 12-18 slides)

Esqueleto para retainer mensal/anual. Termos juridicos BR sao bloco fixo (IPCA + foro Lei 14.879/2024 + multa rescisao 3 meses + LGPD).

---

# Deck: {nome-deck}

## Meta
- Skill geradora: deck-proposal (modo retainer)
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Pyramid Minto + SCQA + 3-tier + SLA P1/P2/P3 + Win Without Pitching + Termos BR
- Modo: retainer
- max_ctas: 1
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

Retainer ancora-se no fee model + SLA + termos BR. Slide 2 e BLUF com a tese "por que retainer vs projeto" (curva de aprendizagem, priority access, custo total 20-30% menor que projetos avulsos). Slides 3-4 desenvolvem SCQA do cliente. Slide 5 e Why Retainer (defesa do modelo recorrente vs projeto). Slide 6 e Escopo com 3 colunas In/Out/Flexible obrigatorias — anti-padrao 2. Slide 7 e SLA matriz P1/P2/P3 com response time + resolution + penalty + compliance targets 99/95/90%. Slide 9 e 3-tier (Essencial / Profissional / Enterprise) com fee model nomeado. Slide 10 e o bloco juridico BR (IPCA + foro SP + multa 2%/mes cap 20% + multa rescisao 3 meses + LGPD). Slide 14 fecha com CTA datado + assinatura via Clicksign.

Tom: Win Without Pitching — posicionamento expert, termos definitivos, equity de mesa.

---

## Slide 1 — Capa
Tipo: capa
Action title: Retainer {servico} pra {cliente} — {periodo} {ano}
Mensagem-chave: {cliente} + {data} + tier proposto + tagline
Speaker notes: Razao social + CNPJ ambas partes em rodape. Tagline curta refletindo Big Idea.
Visual: capa institucional com brand tokens do cliente {marca}.
Prompt de imagem: (deck-image-prompts whitelist — capa)
Tempo estimado: 5s

## Slide 2 — BLUF + Tese Retainer
Tipo: conceitual
Action title: Recomendamos retainer {tier} de {duracao} meses para {resultado mensuravel}
Mensagem-chave: 1 frase + 3 razoes (uma sendo "por que retainer e nao projeto")
Speaker notes:
- Razao 1: {custo-do-nao-ter — quanto se perde por nao ter capacidade dedicada}
- Razao 2: {curva de aprendizagem — valor cresce com tempo}
- Razao 3: {priority access — capacidade reservada do nosso time}

Frase-ancora: "Retainer entrega 20-30% mais valor que projetos avulsos equivalentes pela continuidade do contexto."
Visual: headline + 3 colunas suporte.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 3 — SCQA: Situacao do Cliente
Tipo: problema
Action title: Hoje, {cliente} tem {dado proprio} mas {gap}
Mensagem-chave: Status quo + dado proprio do cliente
Speaker notes: Sem dado proprio do cliente vira teatro. Citar discovery: "Em nossa conversa de {data}, voces mencionaram {fato}."
Visual: 1-2 numeros do cliente.
Prompt de imagem: (deck-image-prompts whitelist — problema)
Tempo estimado: 40s

## Slide 4 — SCQA: Complicacao + Custo-do-Nao-Ter
Tipo: problema
Action title: Sem capacidade dedicada, {cliente} perde {R$ X}/mes em {oportunidade}
Mensagem-chave: Custo do nao-ter retainer, quantificado
Speaker notes: Anti-padrao retainer 5 ("retainer fantasma"): cliente paga sem usar e cancela. Antidoto comeca aqui — mostrar quanto ele perde HOJE por nao ter o servico.

Exemplos por setor:
- Agencia: oportunidades perdidas por velocidade de resposta lenta
- Consultoria: decisoes adiadas que custam EBITDA
- Saude corporativa: absenteismo + custo de internacao evitavel

Visual: chart simples mostrando custo mensal/anual.
Prompt de imagem: (deck-image-prompts whitelist — problema)
Tempo estimado: 40s

## Slide 5 — Why Retainer Over Project
Tipo: comparativo
Action title: Retainer entrega 20-30% mais valor que projetos avulsos
Mensagem-chave: 3 vantagens objetivas: curva, prioridade, custo total
Speaker notes:
| Dimensao | Projeto avulso | Retainer |
|----------|----------------|----------|
| Curva de aprendizagem | Re-aprende a cada projeto | Acumula contexto continuamente |
| Priority access | Fila com outros clientes | Capacidade reservada (SLA P1) |
| Custo total | 100% (baseline) | 70-80% (~20-30% menos) |
| Velocidade resposta | dias-semanas | horas (P1) / dias (P3) |

Visual: tabela comparativa.
Prompt de imagem: skip — comparativo de tabela
Tempo estimado: 50s

## Slide 6 — Escopo: 3 colunas In / Out / Flexible
Tipo: comparativo
Action title: O que esta dentro, fora e flexivel
Mensagem-chave: 3 colunas obrigatorias (anti-scope-creep)
Speaker notes: Anti-padrao 2 (43% projetos sofrem scope creep, custo ate 4× orcamento). Sem coluna "Out" → flag 🔴.

| In Scope (incluso) | Out of Scope (separado) | Flexible (change order) |
|--------------------|--------------------------|--------------------------|
| {items recorrentes} | {items NAO inclusos — ex: producao audiovisual, redesign branding} | {items sob avaliacao caso a caso} |

Anti-padrao retainer 1: scope creep sem governance perde R$ 50-500K/ano em trabalho nao faturado.
Visual: tabela 3 colunas com bordas claras.
Prompt de imagem: skip — comparativo de tabela
Tempo estimado: 60s

## Slide 7 — SLA Matriz P1 / P2 / P3
Tipo: dados
Action title: Compromisso de servico: 99% P1, 95% P2, 90% P3
Mensagem-chave: Matriz P1/P2/P3 com response + resolution + penalty
Speaker notes:
| Nivel | Definicao | Response time | Resolution | Penalty |
|-------|-----------|---------------|------------|---------|
| **P1 Critico** | Operacao parada / reputacional imediato | 15min comercial / 30min fora | 4h | 5% fee/falha, cap 25%/mes |
| **P2 Alto** | Servico degradado, impacto significativo | 1h / 2h | 8-24h | 2% fee/falha, cap 10%/mes |
| **P3 Normal** | Funcionamento normal, melhoria/request menor | 4h comercial | 3-5 dias uteis | Credito 1% se recorrente |
| **Recorrente** | Entregaveis previstos (relatorios, reunioes) | N/A | Conforme calendar | Credito/rollover |

Compliance targets: P1 99% / P2 95% / P3 90%.

Anti-padrao retainer 2: SLA sem metricas mensuraveis ("respondemos rapidamente") nao e SLA, e promessa vazia.

Visual: tabela P1/P2/P3 com codigos de cor.
Prompt de imagem: skip — dados
Tempo estimado: 60s

## Slide 8 — Como Trabalhamos (Operacao)
Tipo: conceitual
Action title: Cadencia weekly + monthly + QBR trimestral
Mensagem-chave: Ritmo operacional definido
Speaker notes:
- **Weekly:** status assincrono (segunda 9h) + sync 30min (quarta 10h)
- **Monthly:** review entregaveis + value report (anti-padrao retainer 5: monthly value report proativo evita "retainer fantasma")
- **Quarterly QBR:** revisao estrategica 90min com sponsor C-level

Visual: calendario com cadencia visual.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 9 — Investimento (3 tiers + Fee Model nomeado)
Tipo: comparativo
Action title: 3 opcoes que enderecam o objetivo
Mensagem-chave: Essencial / Profissional / Enterprise + fee model
Speaker notes:
| Tier | Investimento mensal | Inclui | Fee model | Tradeoff |
|------|--------------------:|--------|-----------|----------|
| Essencial | R$ {X} | {pacote basico, SLA P2/P3} | Fixed Monthly | Sem SLA P1, sem QBR |
| **Profissional (recomendado)** | **R$ {Y}** | **{escopo completo, todos SLA, QBR mensal}** | **Fixed + Overflow Rate** | **—** |
| Enterprise | R$ {Z} | {escopo + ativos estrategicos, QBR semanal} | Base + Performance Bonus | (existe pra ancorar) |

Framing 5X opcional: "fee = ~20% do valor mensal gerado pra voce (regra Consulting Success)".

Forma de pagamento BR:
- Boleto mensal vencimento todo dia {N}
- PIX a vista com {5-10}% desconto
- Parcelado anual em N× sem juros

Visual: 3 colunas com destaque visual no tier recomendado.
Prompt de imagem: (deck-image-prompts whitelist — comparativo)
Tempo estimado: 50s

## Slide 10 — Termos Juridicos BR (BLOCO FIXO OBRIGATORIO)
Tipo: dados
Action title: Termos, reajuste, multa e LGPD
Mensagem-chave: IPCA + foro SP + multa 2%/mes cap 20% + multa rescisao 3 meses + LGPD
Speaker notes:

**Reajuste:**
> O valor mensal sera reajustado anualmente, na data de aniversario do contrato, pela variacao positiva do IPCA/IBGE acumulada nos 12 meses anteriores.

**Foro de eleicao (Lei 14.879/2024):**
> Fica eleito o foro da Comarca de Sao Paulo, Capital, com pertinencia com o domicilio de uma das partes contratantes, nos termos da Lei 14.879/2024.

**Multa moratoria (atraso pagamento):**
> Juros 1%/mes + multa 2% + correcao IPCA, limitado a 20% do valor original (STJ).

**Multa compensatoria (rescisao antecipada sem justa causa):**
> Multa equivalente a 3 (tres) meses do valor mensal vigente.
> Notice period: 60 dias.

**LGPD:**
> Contratada = OPERADORA / Contratante = CONTROLADORA. Tratamento limitado a finalidade do contrato. Incidente de seguranca comunicado em 48h. Dados devolvidos/eliminados ao termino.

Anti-padrao retainer 3: fee fixo sem clausula de reajuste → em BR, 24 meses sem IPCA = -10-20% real.
Anti-padrao retainer 4: notice period <15 dias gera churn imprevisto; >90 dias trava cliente.

Visual: bloco de texto formal estruturado em 5 sub-blocos.
Prompt de imagem: skip — dados/disclaimer
Tempo estimado: 45s

## Slide 11 — Renewal Mechanics
Tipo: conceitual
Action title: Auto-renew com opt-out window de 60 dias + escalacao IPCA
Mensagem-chave: Renovacao automatica + janela de saida + reajuste
Speaker notes:
- Contrato de {N} meses com auto-renew por mesmo periodo
- Opt-out window: 60 dias antes do termino (range 30-90)
- Reajuste IPCA aplicado na renovacao
- Possibilidade de re-tier (upgrade/downgrade) na renovacao

Visual: timeline ciclo de renovacao.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 30s

## Slide 12 — Termination & Transition
Tipo: dados
Action title: Saida ordenada com handover obrigatorio
Mensagem-chave: Notice + handover + IP rights
Speaker notes:
- **Notice period:** 60 dias (cliente) / 90 dias (contratada)
- **Handover obrigatorio:** documentacao + transferencia de acessos + briefing para sucessor
- **IP rights:** entregaveis sao do cliente; metodologias/templates internos permanecem da contratada
- **Mediacao previa:** 60 dias antes de litigio (CAM-CCBC / FGV-DIR / CAMARB)

Visual: bloco de texto + diagrama handover.
Prompt de imagem: skip — dados
Tempo estimado: 30s

## Slide 13 — Equipe Responsavel
Tipo: prova-social
Action title: {Lead, N anos no setor} + {Apoios nomeados}
Mensagem-chave: Quem executa, com nome
Speaker notes: Pessoas nomeadas (anti-padrao 7). Foto + linha-de-credencial. Tier Essencial: time menor. Tier Enterprise: senior nomeado + backup.
Visual: 2-4 fotos + credencial.
Prompt de imagem: (deck-image-prompts whitelist — prova-social)
Tempo estimado: 50s

## Slide 14 — Caso Retainer de Longa Data
Tipo: prova-social
Action title: {Cliente} renovou {N} vezes; resultado em {X} meses: {R$/percentual}
Mensagem-chave: Caso real de retainer longo
Speaker notes:
- Before: contexto do cliente similar
- After: resultado mensuravel apos N meses retainer
- Because: mecanismo (curva de aprendizagem, priority access)

Anti-padrao retainer 5: monthly value report. Mostrar exemplo de value report mensal entregue.

Visual: caso visual + value report exemplo.
Prompt de imagem: (deck-image-prompts whitelist — prova-social)
Tempo estimado: 40s

## Slide 15 — CTA (Proximos Passos)
Tipo: CTA
Action title: Decisao recomendada ate {data} para inicio em {data}
Mensagem-chave: 3 acoes com data + dono
Speaker notes:
1. **Call de duvidas:** {data} {hora} — link {Google Meet} — owner {nome lead}
2. **Decisao recomendada ate:** {data} (assinatura Clicksign)
3. **Inicio retainer:** {data}, primeiro fee {data+15}

Frase-ancora: "Os proximos passos sao..." NUNCA "Aguardamos retorno".
Visual: 3 caixas numeradas data + dono.
Prompt de imagem: skip — CTA
Tempo estimado: 20s

## Apendice (slides opcionais)
- A: Templates de value report mensal
- B: Casos adicionais de retainer
- C: Certidoes negativas + qualificacao tecnica
- D: Curriculo completo do time

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1 (capa)
- Slide 2 (conceitual): BLUF + tese retainer
- Slide 3-4 (problema): situacao + complicacao
- Slide 8 (conceitual): cadencia operacional
- Slide 9 (comparativo): 3-tier
- Slide 11 (conceitual): renewal cycle
- Slide 13 (prova-social): equipe
- Slide 14 (prova-social): caso retainer longo

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] BLUF no slide 2 (Pyramid Minto)
- [ ] SCQA com dado proprio do cliente nos slides 3-4
- [ ] Why Retainer over Project (defesa do modelo)
- [ ] Escopo com 3 colunas In/Out/Flexible
- [ ] SLA matriz P1/P2/P3 com targets 99/95/90%
- [ ] 3 tiers (Essencial/Profissional/Enterprise) com fee model nomeado
- [ ] **Bloco juridico BR completo:**
  - [ ] IPCA reajuste anual
  - [ ] Foro SP com pertinencia (Lei 14.879/2024)
  - [ ] Multa moratoria 2%/mes cap 20% (STJ)
  - [ ] Multa rescisao 3 meses fee
  - [ ] LGPD controlador/operador
- [ ] Notice period 30-90 dias (default 60)
- [ ] Monthly value report mencionado (anti-padrao 5)
- [ ] CTA com 3 acoes datadas
- [ ] Tom Win Without Pitching (frases banidas ausentes)

## Compliance & Disclaimers
🔴 Issues bloqueantes:
- {se aplicavel}

🟡 Verificar antes:
- {se aplicavel}

✅ OK:
- {confirmacoes}
