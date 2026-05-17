# Critico 4 — [VERIFICAR] Auditor (v1.2)

> Quarto critico adversarial do `deck-reviewer`. Adicionado em v1.2 para absorver as marcacoes `[VERIFICAR: descricao]` introduzidas em v1.1 (`shared/verificar-flag.md`).

## Papel

As skills verticais (`deck-fundraising`, `deck-clinical`, etc.) marcam `[VERIFICAR: descricao]` ao lado de qualquer dado especifico que inferiram (nao veio do usuario, nao e dado publico canonicamente conhecido). O Critico 4 do reviewer:

1. **Coleta** todas as marcacoes do STORYBOARD via regex
2. **Mapeia** cada flag para o slide onde aparece
3. **Classifica severidade** baseado no tipo do slide
4. **Gera bloco dedicado** `## Audit [VERIFICAR] flags` no review.md
5. **Contribui para Recommended next action** consolidada com os outros 3 criticos

## Algoritmo

### Passo 1 — Coleta

Regex de busca:

```bash
grep -nE '\[VERIFICAR:[^]]+\]' "$STORYBOARD"
```

Output esperado: linhas com numero + conteudo onde flag aparece. Para cada match:

- `line_n`: numero da linha no STORYBOARD
- `flag_text`: string entre `[VERIFICAR:` e `]`
- `context_line`: linha completa (para extrair contexto do uso)

### Passo 2 — Mapeamento ao slide

Para cada flag, identificar o slide onde aparece:

1. Procurar backward (linhas anteriores) por `^## Slide N — ...` — primeiro match define `slide_n`
2. Procurar backward (linhas anteriores ate antes do `## Slide N`) por `^(\*\*)?Tipo:(\*\*)?[[:space:]]+(.+)$` — extrair `tipo_slide`
3. Identificar `bloco_no_slide` (qual seção do slide a flag aparece):
   - `Action title:` — flag dentro do titulo
   - `Mensagem-chave:` — flag dentro da tese
   - `Conteúdo do slide:` — flag dentro de um bullet visivel
   - `Speaker notes:` — flag dentro da fala do apresentador
   - `Imagens sugeridas:` — flag dentro de prompt de imagem (raro)
   - `Compliance & Disclaimers:` ja flagado no proprio bloco (ignorar)
   - Outro: marcar como `outro`

### Passo 3 — Classificacao de severidade

Regra principal (tipo do slide):

| Tipo do slide | Severidade padrao | Justificativa |
|---------------|-------------------|---------------|
| `CTA` | **🔴 BLOCKER** | Slide decisor — anjo/CEO/comprador toma decisao com base no que esta aqui. Dado nao confirmado vira risco juridico/comercial. |
| `disclaimer` | **🔴 BLOCKER** | Compliance regulatorio. Citar resolucao errada (ex: CVM 160/22 desatualizada) e exposicao. |
| `compliance` (se existir tipo proprio) | **🔴 BLOCKER** | Idem. |
| `financeiro` | **🟡 MAJOR** | Unit economics, ROI, margens. Audiencia pode usar pra decidir, mas raramente sao ASK direto. |
| `dados` | **🟡 MAJOR** | TAM, %, n=, growth rates. Audiencia escrutina. |
| `prova-social` | **🟡 MAJOR** | NPS, cases, depoimentos. Cliente pode questionar metodologia. |
| `problema` | **🟡 MAJOR** se contem numero quantitativo (% / R$ / n=); senao **🟢 MINOR** | Slide gancho — numero fraco quebra o resto. |
| `comparativo` | **🟡 MAJOR** se contem dado vs concorrente; senao **🟢 MINOR** | Risco juridico anti-badmouth + factual. |
| `equipe` | **🟢 MINOR** | Bios — geralmente faceis de corrigir, baixa criticidade. |
| `conceitual` | **🟢 MINOR** | Frameworks raramente tem dado especifico. |
| `contexto` | **🟢 MINOR** | Background/setup. |
| `capa` | **🟢 MINOR** | KPIs no overlay sao auto-referenciados pelo deck. |
| `demo` | **🟢 MINOR** | Demonstracao — texto/numero geralmente ilustrativo. |
| `apêndice` / `apendice` | (ignorado pelo Critico 4 — apendice nao e apresentado) | Apendice e backup; nao classificar pra nao poluir. |
| `agradecimento` | (ignorado) | Slide final relacional. |

**Ajustes contextuais (override):**

1. **Modo_entrega = `enviado-para-leitura`** — se modo Meta indica que deck vai ser lido sem apresentador, ESCALA todas as 🟢 do tipo `problema/comparativo/equipe/conceitual` para 🟡, porque leitor nao tem apresentador pra contextualizar.

2. **Compliance tag = `cfo-cfm` ou `anvisa-laser-classe-iii`** — flags em slide `clinical-style` (peer-facing ou patient-facing) ESCALAM 🟡 para 🔴 se contem termo medico/regulatorio (Anvisa, CFO, CFM, GRADE, RCT).

3. **Multiplas flags no mesmo slide** — agrupa todas as flags do mesmo slide num unico bullet do bloco. Severidade do bullet = maior severidade das flags individuais.

4. **Flag em `Speaker notes` quando modo = `enviado-para-leitura`** — DOWNGRADE para 🟢, porque speaker notes nao vao pra leitor em modo enviado-para-leitura. Se modo = hibrido ou apresentado-ao-vivo, mantem severidade base.

### Passo 4 — Geracao do issue

Cada flag classificada vira um issue no formato:

```python
flag_issue = {
  "slide_n": 2,
  "tipo_slide": "problema",
  "bloco_no_slide": "Action title",
  "critico": "verificar",
  "severidade": "🟡",
  "texto_flag": "fonte CFO ou ABO",
  "context_excerpt": "Em 5 anos, 40% das clinicas dentais premium em SP fecharam ou viraram commodity",
  "problema": "Dado fabricado em slide problema (gancho do deck) sem fonte conferida",
  "sugestao": "Confirmar fonte oficial (CFO Conselho Federal de Odontologia OU ABO Associacao Brasileira de Odontologia) antes de apresentar — slide 2 e ponto escrutinado por anjo"
}
```

### Passo 5 — Bloco dedicado no review.md

Apos as issues por severidade, adiciona bloco dedicado:

```markdown
## Audit [VERIFICAR] flags (Critico 4 — v1.2)

> Listagem dedicada das marcacoes [VERIFICAR:] encontradas no STORYBOARD,
> classificadas por slide afetado.

🔴 BLOCKER — dados decisores precisam confirmacao antes da apresentacao:
- **Slide 12 (CTA) — Action title:** "R$500k em SAFE 8% post-money cap R$6M" [VERIFICAR: confirmar estrutura SAFE BR aplicavel]
  Sugestao: consultar advogado tributarista — SAFE no Brasil tem implicacoes especificas vs US

🟡 MAJOR — resolver antes de apresentar:
- **Slide 2 (problema) — Conteudo do slide:** "40% das clinicas dentais premium SP fecharam" [VERIFICAR: fonte CFO/ABO]
  Sugestao: buscar publicacao oficial CFO ou Indicadores ABO 2024
- **Slide 9 (prova-social) — Conteudo do slide:** "NPS 91, n=131" [VERIFICAR: metodologia + datas]
  Sugestao: documentar metodologia Bain + datas Jan-Mar 2026 + protocolo de coleta

🟢 MINOR — resolver se sobrar tempo:
- **Slide 11 (equipe) — Conteudo do slide:** "Dr. Fernando — 12 anos especialização" [VERIFICAR: bio confirmada]
  Sugestao: confirmar bios antes de imprimir material distribuido

Total: 25 flags (3 🔴 / 18 🟡 / 4 🟢)
Densidade: alta — 25 flags em 13 slides = ~2 dados-nao-conferidos por slide. Considere se modo `enviado-para-leitura` aumenta o risco (leitor revisara cada dado sem voce presente).
```

### Passo 6 — Caso especial: nenhuma flag encontrada

Se grep retorna 0 matches, gerar bloco curto + warning:

```markdown
## Audit [VERIFICAR] flags (Critico 4 — v1.2)

Nenhuma flag [VERIFICAR:] encontrada no STORYBOARD.

⚠️ **Atencao:** isso pode significar:
1. Skill geradora aplicou disciplina v1.1 e nao havia dados a inferir (cenario ideal — todos os numeros vieram do usuario ou foram public-domain)
2. OU skill geradora INVENTOU dados sem flagar (risco — over-claiming sem auditoria)

Recomendacao: revisar manualmente o STORYBOARD procurando padroes suspeitos (R$X, N%, n=N, "RCT ano", citacoes a papers) e confirmar se sao dados reais do usuario ou public-domain. Se forem inferidos pela skill, abrir issue na skill geradora.
```

## Integracao com outros criticos

Critico 4 **NAO duplica** issues que ja foram levantadas pelos Criticos 1-3:

- Se Critico 1 (clareza) ja marcou `🔴 BLOCKER: CTA inexistente em slide 13`, e o Critico 4 detecta `[VERIFICAR: confirmar SAFE BR]` no mesmo slide 13 — Critico 4 ADICIONA seu issue ao bloco `## Audit [VERIFICAR]`, mas NAO duplica no bloco `## Issues por severidade` (so apareceria 1x).

- Se Critico 2 (persuasao) sugere reescrever CTA via `/copy`, e a reescrita ainda contem dado `[VERIFICAR]`, Critico 4 mantem a flag no bloco dedicado.

Logica de deduplicacao no consolidador (passo 6 do workflow): se 2 issues mesmo slide + mesmo tipo de problema, mantem o que tem severidade mais alta + agrega contexto dos outros na sugestao.

## Limites

- **NAO valida dados.** Critico 4 detecta flags e classifica severidade. Confirmar dado real e responsabilidade humana (CFO Beauty Smile, advogado, pesquisador, etc.).
- **NAO chama APIs externas** para buscar a fonte real. Apenas sugere onde procurar.
- **NAO atualiza o STORYBOARD original.** Como os outros 3 criticos, gera arquivo `.review.md` paralelo.

## Exemplo de output completo (W1 v1.1 Beauty Smile pitch anjo)

Output `STORYBOARD-beauty-smile-pitch-anjo.review.md` em [evals/reviewer-cases.md case 5](../evals/reviewer-cases.md).
