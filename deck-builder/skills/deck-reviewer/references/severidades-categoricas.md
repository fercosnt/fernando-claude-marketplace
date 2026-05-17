# Severidades Categoricas (D9 — SEM score numerico)

3 niveis. Sem ponderacao. Sem percentual. Sem nota.

| Tier | Significado | Acao do usuario |
|------|-------------|-----------------|
| 🔴 BLOCKER | NAO apresentar antes de resolver | Reescrever ou cortar |
| 🟡 MAJOR | Resolver se sobrar tempo | Polir antes de v2 |
| 🟢 MINOR | Pular se urgente | Backlog |

---

## Por que NAO score numerico

D9 (decisao locked) — riscos de score numerico aplicado por LLM:

1. **Rating theater** — o numero parece objetivo mas e ruido. LLM "calibra" pra um 7-8 default sempre.
2. **Anchoring** — usuario fixa no numero e ignora o conteudo das issues.
3. **Inconsistencia** — mesmo deck recebe 7.2 e 8.4 em runs diferentes.
4. **Falsa precisao** — diferenca entre 8.1 e 8.3 nao tem significado.

Severidades categoricas resolvem: 3 buckets discretos, acao clara associada, mesmo deck recebe classificacoes estaveis.

---

## Guia de classificacao por vertical

### Fundraising

| Issue | Severidade |
|-------|-----------|
| CTA/Ask inexistente | 🔴 |
| Ask sem valuation OU sem ticket OU sem timeline OU sem uso do capital | 🟡 |
| Valuation sem ancora (multiplo, comparavel) | 🟡 |
| TAM/SAM sem fonte | 🟡 |
| Equipe sem exits/anos/empresas anteriores | 🟡 |
| Concorrencia ausente | 🟡 |
| Slide "Use of funds" ausente | 🟡 |
| Disclaimer regulatorio ausente em offering (CVM) | 🔴 |
| Action title fraco em slide Ask | 🟡 |
| Tempo estimado total fora de ±20% da duracao | 🟢 |

### Sales (B2B)

| Issue | Severidade |
|-------|-----------|
| CTA/proxima etapa inexistente | 🔴 |
| ROI sem calculo explicito (payback period) | 🟡 |
| Comparativo concorrente desonesto (cherry-picking obvio) | 🟡 |
| Demo de produto ausente em deck com objetivo demo | 🟡 |
| Prova social ausente (sem case + sem cliente nomeado) | 🟡 |
| Preco oculto no deck que sera enviado pra leitura | 🟢 |
| Pricing comparativo sem incluir desconto/condicao | 🟢 |

### Clinical

| Issue | Severidade |
|-------|-----------|
| Promessa de cura, recuperacao 100%, "sem dor" | 🔴 (CFO Res. 196/2019) |
| "Garante", "elimina", "100% de sucesso" | 🔴 (CFO + CFM 1974/2011) |
| Antes/depois sem TCLE explicito + identificacao | 🔴 (CFO Res. 196/2019 + LGPD) |
| Comparativo clinico sem evidencia (X melhor que Y sem estudo) | 🟡 |
| Imagem de paciente reconhecivel sem TCLE | 🔴 |
| Indicacao off-label apresentada como oficial | 🔴 |
| Tratamento descrito sem possiveis complicacoes/riscos | 🟡 |
| Citacao informal de literatura ("estudos mostram que...") | 🟡 |
| Disclaimer "cada caso e diferente" ausente em prognostico | 🟢 |

### Equipment (lasers, devices)

| Issue | Severidade |
|-------|-----------|
| Claim fora de bula | 🔴 (Anvisa) |
| Parametros tecnicos contradizem manual fabricante | 🔴 |
| Indicacao terapeutica nao autorizada Anvisa | 🔴 |
| Comparativo competitivo sem fonte | 🟡 |
| ROI clinica sem premissas explicitas (cobertura, ticket medio, capacidade) | 🟡 |
| Demo de protocolo sem dosimetria/seguranca | 🟡 |

### Teaching

| Issue | Severidade |
|-------|-----------|
| 0 hands-on em aula tecnica adulta > 2h | 🟡 (Knowles Andragogy) |
| Chunks > 7-10 min sem quebra (regra cognitiva) | 🟡 |
| Sem objetivos de aprendizagem declarados (Bloom) | 🟡 |
| Sem avaliacao ao final (formative ou summative) | 🟡 |
| Ate 4 CTAs (max_ctas=4 default da vertical) | sem issue |
| 5+ CTAs em deck teaching (excede max_ctas=4) | 🟡 |
| Conteudo so teorico em curso pratico | 🟡 |

### Scientific

| Issue | Severidade |
|-------|-----------|
| Metodologia ausente ou vaga | 🟡 |
| Conflito de interesse nao declarado | 🔴 |
| n insuficiente nao reconhecido nas limitacoes | 🟡 |
| Citacoes sem padrao (ABNT/Vancouver/APA) | 🟢 |
| Resultados sem IC95% ou p-valor | 🟡 |
| Ate 3 CTAs (max_ctas=3 default da vertical) | sem issue |
| 4+ CTAs (excede max_ctas=3) | 🟡 |
| Poster sem QR code pro paper completo | 🟢 |

### Proposal

| Issue | Severidade |
|-------|-----------|
| Escopo ambiguo (entregaveis nao listados) | 🟡 |
| Sem prazo final declarado | 🟡 |
| Sem condicao de pagamento | 🟡 |
| Sem clausula de exclusividade/confidencialidade | 🟢 |
| Validade da proposta nao declarada | 🟡 |

### Internal

| Issue | Severidade |
|-------|-----------|
| BLUF (bottom line up front) ausente em slide 2 | 🟡 |
| Ask especifico ausente (politica, decisao, aprovacao) | 🟡 |
| Objecao antecipada ausente em deck "pitch-to-leadership" | 🟡 |
| Backup data ausente (anexo) | 🟢 |

---

## Universais (qualquer vertical)

| Issue | Severidade |
|-------|-----------|
| STORYBOARD malformado (Meta incompleta) | 🔴 |
| Big Idea ausente | 🟡 |
| 0 numeros nos primeiros 5 slides | 🔴 |
| 3+ saltos no horizontal logic test | 🔴 |
| 3+ titles descritivos sistemico | 🟡 |
| Hook fraco no slide 1 (Critico Persuasao) | 🟡 |
| CTA sem O QUE / QUANDO / COMO | 🟡 |
| Tempo total fora de ±20% da duracao | 🟢 |
| Imagens com prompt ausente em slide whitelist | 🟢 |

---

## Regras de dedupe (consolidacao apos 3 passes)

Quando 2 criticos levantam issue similar para o mesmo slide:

1. **Mesma severidade** → manter uma so, listar ambos criticos em `[critico1, critico2]`
2. **Severidades diferentes** → manter a MAIS alta, descartar a outra
3. **Mesmo slide + categorias adjacentes** (ex: "hook fraco" Persuasao + "title descritivo na capa" Clareza) → 1 issue consolidada com `Sugestao:` combinando os dois

Nunca somar severidades. Nunca usar "🔴+🟡" como categoria.
