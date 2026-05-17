# Skeleton STORYBOARD — Modo `pitch-to-leadership`

Aplica Pyramid Minto (BLUF slide 2) + Raskin (Status Quo → New World) + adaptacao Brasil (slide 1 relacional).

Anexo OBRIGATORIO: 6-pager Amazon em arquivo separado `.6pager.md`.

---

```markdown
# Deck: {slug}

## Meta
- Skill geradora: deck-internal
- Objetivo unico: {U1}
- Audiencia: {U2 — CEO/board, 1-10 executivos}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Pyramid Minto + Raskin
- Modo: pitch-to-leadership
- max_ctas: 1
- Anexo 6-pager: sim → STORYBOARD-{slug}-{HHmm}.6pager.md
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

Pyramid Minto SCQA com BLUF no slide 2 (adaptacao BR: slide 1 capa relacional ANTES do BLUF).
Status Quo (Raskin slide 3) ancora urgencia; recomendacao do BLUF e a ponte para New World.
Anti-padroes banidos: enterrar o lede; ask invisivel; business case sem numeros; deck sem 6-pager anexo.

## Slide 1 — Capa
Tipo: capa
Action title: {assertivo, NAO descritivo — relacional pre-BLUF (Hofstede BR)}
Mensagem-chave: {1 frase de abertura — reciprocidade + situacao compartilhada}
Speaker notes: 30-60s de abertura — agradecer o tempo + situar contexto compartilhado + transicionar para BLUF
Visual: {descricao neutra — brand-safe}
Prompt de imagem: {preencher via deck-image-prompts — whitelist D5}
Tempo estimado: 30-60s

## Slide 2 — BLUF (Pyramid Minto)
Tipo: conceitual
Action title: {recomendacao em 1 sentenca}
Mensagem-chave: "Recomendo {recomendacao}, investindo {valor}, esperando {retorno mensuravel} ate {prazo}, pedindo {ask especifico} {quando}"
Speaker notes: 60-90s — entregar a recomendacao COM TODOS os 5 elementos (recomendacao + investimento + retorno + prazo + ask). NAO enrolar.
Visual: minimalista — eventualmente sem visual (so texto)
Prompt de imagem: {preencher OU skip se decisao por minimalismo}
Tempo estimado: 60-90s

## Slide 3 — Problema/Status Quo (Raskin)
Tipo: problema
Action title: {custo de inacao quantificado em 1 frase}
Mensagem-chave: {Grande Mudanca + Status Quo desconfortavel + custo}
Speaker notes: 60-90s — nomear a mudanca (Raskin 5 elementos #1), mostrar perdedores (cases reais), custo de inacao em R$ ou tempo
Visual: representacao do problema (sem cliches stock — ver deck-image-prompts anti-cliches)
Prompt de imagem: {preencher — whitelist D5}
Tempo estimado: 60-90s

## Slide 4 — Solucao proposta
Tipo: conceitual
Action title: {nome da solucao + verbo de acao}
Mensagem-chave: {a Terra Prometida Raskin em 7-10 palavras vividas}
Speaker notes: 60s — recursos como "presentes magicos" (Raskin #4), NAO specs tecnicas
Visual: {ilustrar a solucao}
Prompt de imagem: {preencher}
Tempo estimado: 60s

## Slide 5 — Business case
Tipo: financeiro
Action title: {ROI/payback em 1 frase}
Mensagem-chave: {tabela com numeros — payback liderado vs NPV (Brasil)}
Speaker notes: 90s — apresentar numeros + premissas explicitas + cenarios (otimista/realista/pessimista)
Visual: tabela com 4 colunas (cenario / investimento / retorno / payback)
Prompt de imagem: — (skip — tipo financeiro fora whitelist D5)
Tempo estimado: 90s

## Slide 6 — Friccao mitigada (objecao antecipada)
Tipo: comparativo
Action title: {endereca I5 diretamente}
Mensagem-chave: {ANTES vs DEPOIS com mitigacao explicita}
Speaker notes: 60s — reconhecer a preocupacao + mostrar mitigacao concreta + nao defender, ENGAJAR
Visual: comparativo lado-a-lado
Prompt de imagem: {preencher — whitelist D5}
Tempo estimado: 60s

## Slide 7 — Ask especifico
Tipo: CTA
Action title: {VERBO + numero + prazo + decisao}
Mensagem-chave: "Aprovar {politica/projeto} + liberar R$ {valor} + decisao {hoje/data} + sponsor {nome}"
Speaker notes: 30s — dizer exatamente o que precisa AGORA. NAO vago. SEM "vamos discutir", SIM "preciso da sua aprovacao formal hoje"
Visual: — (silencio textual)
Prompt de imagem: — (skip — tipo CTA fora whitelist D5)
Tempo estimado: 30s + SILENCIO

## Slide 8 — Proximos passos
Tipo: CTA (continuacao)
Action title: Cronograma de implementacao
Mensagem-chave: {3-5 marcos temporais com owners}
Speaker notes: 30s — implementacao real + primeira revisao + criterio de continuidade
Visual: timeline simples
Prompt de imagem: — (skip)
Tempo estimado: 30s

## Slide 9 — Q&A backup
Tipo: apendice
Action title: Perguntas antecipadas
Mensagem-chave: {3-5 perguntas previsiveis com respostas prontas}
Speaker notes: usar apenas se perguntado — slide oculto durante apresentacao linear
Visual: —
Prompt de imagem: — (skip — tipo apendice fora whitelist D5)
Tempo estimado: variavel

## Apendice (opcional)
- Slide A1 — Detalhe financeiro completo
- Slide A2 — Premissas detalhadas
- Slide A3 — Riscos top 5

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1: {brief capa relacional}
- Slide 3: {brief problema — anti-cliches stock}
- Slide 4: {brief solucao — Terra Prometida vivida}
- Slide 6: {brief comparativo ANTES/DEPOIS}

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] BLUF e slide 2 (NAO enterrar o lede)
- [ ] BLUF tem 5 elementos (recomendacao + investimento + retorno + prazo + ask)
- [ ] Slide 1 = capa relacional (Hofstede BR)
- [ ] Action titles em todos os slides (NAO titulos descritivos)
- [ ] 1 ideia por slide
- [ ] Slide 6 enderaca I5 explicitamente
- [ ] Slide 7 = Ask ESPECIFICO (valor + prazo + decisao + sponsor)
- [ ] Anexo 6-pager existe em arquivo separado
- [ ] ROI/payback explicito em slide 5
- [ ] CTA unico (max_ctas: 1)

## Compliance & Disclaimers
{aplicar 3 tiers §10.2 SHARED.md conforme marca/contexto}

🔴 Issues bloqueantes:
- {se houver}

🟡 Verificar antes:
- {se houver}

✅ OK:
- {confirmacoes}
```
