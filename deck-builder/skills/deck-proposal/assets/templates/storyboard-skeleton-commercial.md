# STORYBOARD esqueleto — modo `commercial` (one-shot, 12-15 slides)

Esqueleto pronto-pra-copiar. Substituir `{placeholders}` pelos dados da entrevista U1-U6 + P1-P5.

---

# Deck: {nome-deck}

## Meta
- Skill geradora: deck-proposal (modo commercial)
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Pyramid Minto + SCQA + ROI 3-tier + Win Without Pitching
- Modo: commercial
- max_ctas: 1
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

Pyramid invertida: slide 2 (BLUF) entrega a recomendacao em 1 frase + 3 razoes. Slides 3-5 desenvolvem SCQA (situacao do cliente com dado proprio → complicacao com custo-do-nao-agir → resolucao = proposta). Slides 6-9 detalham solucao, escopo (com 3 colunas In/Out/Flexible — anti-padrao 2) e cronograma com dependencias do cliente. Slide 10 apresenta 3 tiers de investimento (Essencial / Profissional / Enterprise) com framing ROI e parcelamento BR. Slides 11-13 fecham com termos, equipe e prova social. Slide 14 e CTA com 3 acoes datadas. Apendice opcional fora do fluxo principal.

Tom: Win Without Pitching — recomendamos, nao suplicamos. Posicionamento expert ("ja diagnosticamos N clinicas similares"), termos definitivos, equity de mesa (cliente escolhe ENTRE 3, nao SE contrata).

---

## Slide 1 — Capa
Tipo: capa
Action title: Proposta {servico} pra {cliente} — {periodo/marco}
Mensagem-chave: {cliente} + {data emissao} + v1
Speaker notes: Identificacao da proposta. Razao social + CNPJ de ambas as partes em rodape, conforme padrao formal BR.
Visual: capa institucional com brand tokens do cliente {marca}.
Prompt de imagem: (deck-image-prompts whitelist — capa)
Tempo estimado: 5s

## Slide 2 — BLUF (Pyramid Minto)
Tipo: conceitual
Action title: Recomendamos {acao} ate {data} pra capturar {resultado mensuravel}
Mensagem-chave: 1 frase de recomendacao + 3 razoes-suporte (MECE)
Speaker notes:
- Razao 1: {dado quantitativo do cliente}
- Razao 2: {capacidade unica nossa relevante}
- Razao 3: {risco mitigado vs status quo}
Esta e a unica conclusao que o C-level vai lembrar. Tudo abaixo suporta.
Visual: 3 colunas suporte abaixo do headline; sem narrativa.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 3 — SCQA: Situacao do Cliente
Tipo: problema
Action title: Hoje, {cliente} {fato verificavel do cliente}
Mensagem-chave: Status quo com dado proprio do cliente (citado em discovery anterior)
Speaker notes: Fato sem julgamento. Dado especifico do cliente (nao generico). Se citacao direta: "Em nossa conversa de {data}, voces mencionaram que..."
Visual: 1-2 graficos/numeros simples do cliente.
Prompt de imagem: (deck-image-prompts whitelist — problema)
Tempo estimado: 40s

## Slide 4 — SCQA: Complicacao + Custo-do-Nao-Agir
Tipo: problema
Action title: Mantido esse cenario, {cliente} {custo quantificado anual/mensal}
Mensagem-chave: O que mudou, por que doi agora, com numero
Speaker notes: Esta e a etapa que gera urgencia. Sem numero do custo, vira teatro. Idealmente, comparar:
- Cenario A: status quo continua → custo X
- Cenario B: status quo + tendencia → custo Y maior
Visual: chart simples mostrando degradacao.
Prompt de imagem: (deck-image-prompts whitelist — problema)
Tempo estimado: 40s

## Slide 5 — Solucao recomendada (resposta SCQA)
Tipo: conceitual
Action title: Recomendamos {acao especifica} para {resultado especifico}
Mensagem-chave: 3-4 componentes nucleares da solucao
Speaker notes: Diagrama: hoje → trabalho de {duracao} → futuro. Foco no que muda, nao em features.
Visual: diagrama hoje/transformacao/futuro.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 6 — Como executamos (metodologia)
Tipo: conceitual
Action title: Em {N} fases ao longo de {periodo}
Mensagem-chave: Fases nomeadas + entregavel-chave por fase
Speaker notes: Metodologia DEPOIS de provar valor (anti-padrao 7). Nomear framework proprietario se existe. Sem jargao gratuito.
Visual: timeline com fases.
Prompt de imagem: (deck-image-prompts whitelist — conceitual)
Tempo estimado: 45s

## Slide 7 — Escopo: 3 colunas In / Out / Flexible
Tipo: comparativo
Action title: O que esta dentro, fora e flexivel
Mensagem-chave: 3 colunas obrigatorias — coluna "Out" anti-scope-creep
Speaker notes: 43% projetos sofrem scope creep, custo ate 4× orcamento. Coluna "Out" e o campo mais omitido. Sem ela → flag 🔴.
Visual:
| In Scope | Out of Scope | Flexible (change order) |
|----------|--------------|--------------------------|
| {items} | {items} | {items} |
Prompt de imagem: (skip — comparativo de tabela e melhor sem imagem)
Tempo estimado: 60s

## Slide 8 — Cronograma com Dependencias do Cliente
Tipo: dados
Action title: Inicio {data}, conclusao {data} ({N} semanas)
Mensagem-chave: Gantt simples + premissas/dependencias do cliente
Speaker notes: Premissas explicitas (anti-padrao 5): aprovacoes, dados, acessos, disponibilidade de stakeholders. Sem isso, atraso do cliente vira disputa.
Visual: Gantt + boxes de dependencia destacados.
Prompt de imagem: skip — tipo dados fora da whitelist
Tempo estimado: 40s

## Slide 9 — Equipe Responsavel
Tipo: prova-social
Action title: {Lead, N anos no setor} + {Apoios nomeados}
Mensagem-chave: Quem executa, com nome (DocSend: 1m02s atencao media)
Speaker notes: Pessoas nomeadas, NAO "time alocado". Foto + linha-de-credencial relevante (anos no setor, casos similares, posts publicos). Anti-padrao 7: pessoas > empresa generica.
Visual: 2-4 fotos + linha curta de credencial.
Prompt de imagem: (deck-image-prompts whitelist — prova-social)
Tempo estimado: 62s

## Slide 10 — Investimento (3 tiers Essencial / Profissional / Enterprise)
Tipo: comparativo
Action title: 3 opcoes que enderecam o objetivo
Mensagem-chave: Essencial / Profissional / Enterprise (recomendado destacado)
Speaker notes:
| Tier | Investimento | Inclui | Tradeoff |
|------|-------------:|--------|----------|
| Essencial | R$ {X} | {entregaveis basicos} | {sem suporte premium / SLA frouxo} |
| **Profissional (recomendado)** | **R$ {Y}** | **{escopo completo}** | **—** |
| Enterprise | R$ {Z} | {escopo + ativos extras} | (existe pra ancorar) |

Framing 5X opcional: "fee = ~20% do valor mensal gerado pra voce (regra Consulting Success)".

Visual: tabela 3 colunas, destaque visual no tier recomendado.
Prompt de imagem: (deck-image-prompts whitelist — comparativo)
Tempo estimado: 50s

## Slide 11 — Termos
Tipo: dados
Action title: Termos, condicoes e validade
Mensagem-chave: Pagamento + validade proposta + impostos
Speaker notes:
- Forma de pagamento: 50% inicio + 50% conclusao (default; ajustar por modo). Boleto / PIX / TED.
- Alternativa parcelado: {N}× R$ {valor} sem juros.
- Validade desta proposta: 30 dias da emissao ({data limite}).
- Tributacao: {Simples Nacional / Lucro Real} — {valor total} {liquido / + impostos}.
- Foro: Comarca de Sao Paulo, Capital, conforme Lei 14.879/2024.
Visual: bloco de texto formal estruturado.
Prompt de imagem: skip — tipo dados fora da whitelist
Tempo estimado: 30s

## Slide 12 — Caso (Before / After / Because)
Tipo: prova-social
Action title: {Cliente similar} entregou {resultado} em {tempo}
Mensagem-chave: Caso de cliente brasileiro conhecido (BR prefere BR)
Speaker notes:
- Before: {situacao identica ao cliente atual}
- After: {resultado mensuravel — R$/percentual/tempo}
- Because: {mecanismo especifico que fez a transformacao}
Stanford 2024: informacao em formato historia e lembrada 22× melhor que fatos isolados.
Visual: 3 caixas before/after/because.
Prompt de imagem: (deck-image-prompts whitelist — prova-social)
Tempo estimado: 25s

## Slide 13 — CTA (Proximos Passos)
Tipo: CTA
Action title: Decisao recomendada ate {data} para inicio em {data}
Mensagem-chave: 3 acoes com data e dono
Speaker notes:
1. **Call de duvidas:** {data} {hora} — link {Google Meet/Zoom} — owner {nome}.
2. **Decisao recomendada ate:** {data} (assinatura via Clicksign).
3. **Inicio dos trabalhos:** {data}, condicionado a assinatura ate {data-anterior}.

Frase-ancora: "Os proximos passos sao..." NUNCA "Aguardamos retorno".
Visual: 3 caixas numeradas com data + dono.
Prompt de imagem: skip — tipo CTA fora da whitelist
Tempo estimado: 20s

## Slide 14 — Agradecimento
Tipo: agradecimento
Action title: Obrigado, {cliente}
Mensagem-chave: {nome do lead} + email + telefone direto
Speaker notes: Contato direto do lead da proposta, nao "comercial@empresa.com".
Visual: contato + logo cliente + logo nossa.
Prompt de imagem: skip
Tempo estimado: 10s

## Apendice (slides opcionais, FORA do fluxo principal)
- Apendice A: Metodologia detalhada
- Apendice B: Cases adicionais
- Apendice C: Certidoes negativas, qualificacao tecnica
- Apendice D: Curriculo do time (longo)

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1 (capa): {brief}
- Slide 2 (conceitual): {brief BLUF 3-suporte}
- Slide 3 (problema): {brief situacao cliente}
- Slide 4 (problema): {brief complicacao + custo}
- Slide 5 (conceitual): {brief solucao diagrama}
- Slide 6 (conceitual): {brief metodologia}
- Slide 9 (prova-social): {brief equipe nomeada}
- Slide 10 (comparativo): {brief 3-tier visual}
- Slide 12 (prova-social): {brief caso before/after}

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] BLUF no slide 2 (Pyramid Minto)
- [ ] Action titles sao conclusao, NAO tema
- [ ] 1 ideia por slide
- [ ] Exec summary ≤250 palavras
- [ ] Escopo com 3 colunas In/Out/Flexible
- [ ] 3 tiers de investimento com tier premium ancorando
- [ ] CTA com 3 acoes datadas (NAO "aguardamos retorno")
- [ ] Cronograma com dependencias do cliente
- [ ] Equipe nomeada (nao "time alocado")
- [ ] Frases banidas Win Without Pitching ausentes
- [ ] Caso brasileiro conhecido (BR prefere BR)
- [ ] Foro Lei 14.879/2024
- [ ] Tom expert (recomendamos, nao suplica)

## Compliance & Disclaimers
🔴 Issues bloqueantes:
- {se aplicavel}

🟡 Verificar antes:
- {se aplicavel}

✅ OK:
- {confirmacoes}
