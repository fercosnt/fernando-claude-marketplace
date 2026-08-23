---
name: deck-teaching
description: Cria STORYBOARD para aulas, cursos, treinamentos e keynotes inspiracionais. 3 modos (aula-tecnica/workshop-hands-on/keynote-inspirational). Andragogy + Bloom + Mayer + Sparkline Duarte.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/framework-andragogy-bloom-backwards.md
  - references/framework-sparkline-duarte-keynote.md
  - references/eval-cases-teaching.md
assets:
  - assets/templates/storyboard-skeleton-aula-tecnica.md
  - assets/templates/storyboard-skeleton-workshop.md
  - assets/templates/storyboard-skeleton-keynote.md
  - assets/checklists/teaching-checklist.md
---

# deck-teaching

Skill vertical do plugin **deck-builder** para conteudo pedagogico: aulas tecnicas, workshops hands-on e keynotes inspiracionais. Gera STORYBOARD.md aplicando Andragogy (Knowles), Backwards Design (Wiggins/McTighe), Bloom revisada (Anderson/Krathwohl), Multimedia Learning (Mayer 12 principios) e Sparkline (Duarte — somente keynote).

## Quando ativa

Triggers do `deck-orchestrator`: "aula", "curso", "treinamento profissional", "workshop", "ensinar dentistas", "TED", "palestra inspiracional", "keynote inspiracional", "modulo pos-grad", "ministrar".

Modo standalone: `/deck-teaching` ou contexto onde objetivo final e aprendizagem (nao venda, nao captacao, nao pitch interno).

## Modos (3)

| Modo | Quando aplica | Estrutura | Slides tipicos |
|------|--------------|-----------|----------------|
| `aula-tecnica` | Aula 60min-4h conteudo tecnico (pos-grad, treinamento profissional) | Backwards Design + Bloom + chunks ≤7min | 30-60 |
| `workshop-hands-on` | Workshop 4-8h com pratica intercalada | Andragogy + 4 modulos + 2-3 hands-on + caso integrador | 20-40 |
| `keynote-inspirational` | Palestra 12-20min em evento (substitui rotulo "TED-style") | Sparkline Duarte + Big Idea + 1 call provocativo | 12-20 |

**Selecao automatica do modo:**
- T1 = 12-20min E T4=nao E T5=nao → `keynote-inspirational`
- T1 = 4h+ E T4 ≥ 2 hands-on → `workshop-hands-on`
- T1 = 60min-2h E foco tecnico → `aula-tecnica`
- Ambiguidade → perguntar via AskUserQuestion antes de gerar

## Entrevista universal (U1-U6 do SHARED §10.1)

Rodar primeiro. Para keynote, U5 (Big Idea) e CRITICA — destilar em 1 frase ate o usuario aprovar.

## Entrevista vertical (T1-T5, apos U1-U6)

- **T1:** Duracao exata (60min / 4h / 8h / 12-20min keynote)
- **T2:** Objetivo de aprendizagem com verbo Bloom explicito (lembrar / compreender / aplicar / analisar / avaliar / criar). Default sugerido: `aplicar` para aulas tecnicas, `avaliar` para keynote.
- **T3:** Conhecimento previo da audiencia (baixo / medio / alto). Vira pre-avaliacao no slide 3 dos modos `aula-tecnica` e `workshop-hands-on`.
- **T4:** Hands-on previsto? (sim/nao + quantos). Default workshop: 2-3. Default keynote: nao.
- **T5:** Avaliacao final? (quiz / projeto / observacao / caso integrador / nenhum)

## Frameworks aplicados (resumo)

Detalhe completo em [references/framework-andragogy-bloom-backwards.md](references/framework-andragogy-bloom-backwards.md) e [references/framework-sparkline-duarte-keynote.md](references/framework-sparkline-duarte-keynote.md).

### Andragogy (Knowles) — adultos aprendem diferente
Relevancia imediata, experiencia previa ancorada, auto-direcao, motivacao intrinseca.

### Backwards Design (Wiggins/McTighe)
1. Resultado esperado (verbo Bloom em T2) → 2. Evidencia (avaliacao em T5) → 3. Experiencias instrucionais (slides).

### Bloom revisada (Anderson/Krathwohl, 2001)
Lembrar < Compreender < **Aplicar** < Analisar < **Avaliar** < Criar.

### Multimedia Learning (Mayer, 12 principios)
Coerencia, Sinalizacao, Redundancia (NAO ler slide), Contiguidade espacial+temporal, Modalidade, **Segmentacao (chunks ≤7min)**, Pre-treinamento, Multimedia, Personalizacao, Voz, Imagem, Anchoring.

### Sparkline Duarte (Nancy Duarte, *Resonate*) — SO modo `keynote-inspirational`
Comparacao continua "what is" ↔ "what could be"; estrutura contexto → revelacao → tensao → resolucao → call-to-action.

## Protocolo de execucao

1. **Receber input** do `deck-orchestrator` (rota detectada) ou modo standalone.
2. **Auto-detect marca** (§10.5 SHARED). Se Fotona detectada, considerar invocar `laser-physics` para formulas.
3. **Rodar entrevista U1-U6 + T1-T5.**
4. **Selecionar modo** (aula-tecnica / workshop-hands-on / keynote-inspirational).
5. **Consultar NB1** apenas se houver duvida especifica. Query exemplo:
   ```bash
   notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
   notebooklm ask "Mayer segmentacao chunks 7min retrieval practice adult dental {tema}" --max-citations 5
   ```
   Falha de NB nao bloqueia — segue com defaults da pesquisa.
6. **Aplicar Backwards Design**: partir de T2 (Bloom) → T5 (evidencia) → planejar slides reversamente.
7. **Gerar STORYBOARD** seguindo skeleton do modo (em `assets/templates/`).
8. **Invocar `deck-image-prompts`** para slides whitelisted (capa, problema, conceitual, comparativo, demo, prova-social).
9. **Validar via checklist** [assets/checklists/teaching-checklist.md](assets/checklists/teaching-checklist.md).
10. **Output** em `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md` (§10.4).

## Output STORYBOARD — regras especificas teaching

Schema base §10.2. **`max_ctas: 4` DEVE ser declarado explicitamente na Meta** (override D14 — objetivos pedagogicos: pratica + leitura + quiz + caso proprio). Para `keynote-inspirational`, usar `max_ctas: 1`.

**Meta obrigatoria adicional para teaching:**
```markdown
- Modo: aula-tecnica | workshop-hands-on | keynote-inspirational
- max_ctas: 4  (ou 1 para keynote-inspirational)
- Verbo Bloom alvo: {T2 — aplicar|analisar|avaliar|criar}
- Duracao total: {T1} min
- Chunks totais: {N}  (so modos aula/workshop)
- Hands-on totais: {N}  (so modos aula/workshop)
- Avaliacao final: {T5}
```

### Slide 2 — Objetivos visiveis (REGRA INVIOLAVEL)

Em TODOS os 3 modos, o slide 2 lista os objetivos de aprendizagem com **verbo Bloom explicito** no inicio de cada bullet. Exemplo:

```
## Slide 2 — Objetivos
Tipo: conceitual
Action title: Ao final desta aula voce vai APLICAR dosimetria Er:YAG em casos reais
Mensagem-chave: 3 objetivos mensuraveis
Bullets:
- APLICAR formula de fluence (J/cm²) em 5 casos de clareamento
- CALCULAR energia cumulativa em sessao multi-pulso
- AJUSTAR parametros conforme tipo de tecido
```

Sem verbo Bloom no slide 2 → falha critica do reviewer.

### Modo `aula-tecnica` — chunks ≤7min (regra Mayer segmentacao)

Estrutura segmentada obrigatoria. Cada chunk = 5min explicacao + 2min retrieval practice (quiz / pergunta retorica / pause-and-discuss). Slides estimados por chunk: 4-7. Quiz formativo entre chunks. Avaliacao somativa no final + 4 CTAs (proxima leitura / quiz online / 5 casos proprios para tentar / proximo modulo).

Skeleton em [assets/templates/storyboard-skeleton-aula-tecnica.md](assets/templates/storyboard-skeleton-aula-tecnica.md).

### Modo `workshop-hands-on` — modulos + pratica intercalada

4 modulos conceito + 2-3 hands-on + 1 caso integrador final. Cada hands-on com worksheet impresso (referenciar em apendice). Avaliacao = caso integrador (Bloom-aplicar ou analisar). Hands-on contado e estruturado: tempo, materiais, criterio de sucesso. 4 CTAs.

Skeleton em [assets/templates/storyboard-skeleton-workshop.md](assets/templates/storyboard-skeleton-workshop.md).

### Modo `keynote-inspirational` — Sparkline Duarte

12-20 slides em arco narrativo: capa → contexto (what is) → promessa (what could be) → tensao 1 → resolucao 1 → tensao 2 (mais profunda) → resolucao 2 (revelacao) → Big Idea reforcada → 1 call provocativo. **Sparkline so se aplica neste modo** — nao usar em aula/workshop. Sem hands-on, sem quiz, sem chunks ≤7min. `max_ctas: 1`.

Skeleton em [assets/templates/storyboard-skeleton-keynote.md](assets/templates/storyboard-skeleton-keynote.md).

## Whitelist deck-image-prompts (D5)

- **Preencher prompt:** capa, problema, conceitual (esquemas pedagogicos), comparativo, demo, prova-social
- **Skip:** dados, financeiro (raro em teaching), CTA, disclaimer, agradecimento, apendice

## Defaults

- Verbo Bloom default: `aplicar` (aula/workshop), `avaliar` (keynote)
- Hands-on default workshop: 2-3 (criticar se T4=0 em workshop ≥4h → 🟡 MAJOR)
- Chunks default aula 60min: 6-8 (60min / 7min)
- Engines default delegadas a `deck-image-prompts`: Higgsfield + Imagen 4 + Nano Banana Pro
- `max_ctas`: 4 (aula/workshop), 1 (keynote)
- Aspect ratio: 16:9

## Limites (D8 SHARED)

- NAO gera slides finais sem pedido explicito (D15) — default e STORYBOARD.md. Render e exclusividade de `deck-render-canva`, opt-in e so com MCP do Canva conectado. PPTX/Google Slides/Figma/Gamma seguem proibidos.
- NAO ministra a aula — so estrutura
- NAO produz materiais didaticos impressos (worksheet/apostila/quiz com gabarito) — so referencia em apendice
- NAO faz design visual — `deck-image-prompts` gera prompts
- NAO substitui pedagogo/instructional designer profissional para conteudo regulado (CME oficial com creditos)

## Handoff: render no Canva (v2.0.0 — opt-in, D16)

Ao entregar o `STORYBOARD.md`, **se e somente se** o MCP do Canva estiver conectado, ofereca via `AskUserQuestion`:

> "Gero a base deste deck no Canva a partir do storyboard?"
> - Sim → `deck-render-canva`
> - Nao → encerra normalmente

Invioláveis:
- **Nunca** chama `deck-render-canva` automaticamente (D16).
- MCP do Canva desconectado → **nao oferece**. Sem aviso e sem opcao quebrada (D15).
- Recusa encerra o fluxo normalmente — nao insiste, nao repergunta.
- Sem brand template para a marca, o render reporta e pula. Nunca cai para geracao livre (D19).

## Cross-skill

- **Auto-detect Fotona** → invoca `laser-physics` para formulas/dosimetria nos slides conceituais.
- **Auto-detect Beauty Smile** → carrega `beauty-smile-design-system` tokens (se instalado).
- **Sempre** invoca `deck-image-prompts` para slides whitelisted ao final.
- **`deck-reviewer`** valida ao final (opt-in mas recomendado) — checa chunks ≤7min, max_ctas, verbo Bloom slide 2, hands-on contado.

## Eval cases

3 cases em [references/eval-cases-teaching.md](references/eval-cases-teaching.md):
1. **Aula 60min "Dosimetria Er:YAG"** (dentistas pos-grad) — modo `aula-tecnica`, 8 chunks, 2 hands-on, quiz final, invoca `laser-physics`
2. **Workshop 4h "Implantodontia basica"** — modo `workshop-hands-on`, 4 modulos, 2 hands-on, caso integrador
3. **Keynote 18min "O futuro da odontologia premium"** — modo `keynote-inspirational`, Sparkline Duarte, Big Idea, 1 call, `max_ctas: 1`

## DoD

- [x] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1
- [x] 3 modos implementados (aula-tecnica / workshop-hands-on / keynote-inspirational)
- [x] Chunks ≤7min em `aula-tecnica` (Mayer segmentacao)
- [x] **`max_ctas: 4` declarado na Meta** (override D14) — `max_ctas: 1` em keynote
- [x] Verbo Bloom explicito no slide 2 (regra inviolavel)
- [x] Hands-on contado e estruturado em modos relevantes
- [x] Sparkline Duarte SO em `keynote-inspirational`
- [x] Schema §10.2 valido
- [x] 3 eval cases cobrindo os 3 modos
- [x] Instalada Code + Cowork

## v1.1 — Adendo: `modo_entrega` + `[VERIFICAR]` + Layout sugerido

A partir de v1.1 do plugin, esta skill aplica 4 disciplinas adicionais ao gerar STORYBOARD. Detalhes canônicos em `../../shared/storyboard-schema.md` e `../../shared/verificar-flag.md`.

**1. `modo_entrega` adapta densidade do slide** (regra 7 do schema):
- `apresentado-ao-vivo` (U4=1/2): slides minimalistas (2-3 bullets) + speaker notes RICOS
- `enviado-para-leitura` (U4=3): slides DENSOS (4-6 bullets + dados inline + 1 quote curto) + speaker notes opcionais ou curtos
- `hibrido` (U4=4): meio-termo, ambos preenchidos

Preencher bloco `Conteúdo do slide (visível na projeção)` em cada slide, calibrado ao `modo_entrega`.

**2. `Layout sugerido` em cada slide** (regra 8 do schema): grid + tipografia + componentes visuais + animação. Sem isso, designer/Gamma/Claude Design/PowerPoint recebe o deck "no escuro".

**3. `[VERIFICAR]` em dados fabricados** (regra 9 do schema + `verificar-flag.md`): todo R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa que a skill **inferir** (não veio do usuário; não é público canonicamente conhecido) recebe `[VERIFICAR: descrição]` inline ou em footnote. Lint v1.1 emite WARN quando ausente. Reviewer converte em 🟡 ou 🔴 no segundo passe.

**4. Bold opcional nos rótulos:** preferir `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` para facilitar leitura visual. Lint aceita ambos formatos.

**Checklist v1.1 ao gerar cada slide:**
- [ ] `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` em bold
- [ ] Bloco `Conteúdo do slide (visível na projeção)` preenchido com densidade adaptada ao `modo_entrega`
- [ ] Bloco `Layout sugerido` com grid + tipografia + componentes
- [ ] Dados específicos inferidos marcados com `[VERIFICAR: ...]`
- [ ] `Imagens sugeridas` no formato v1.1 (Quantidade explícita + variações em blocos separados)
