# Eval Cases — `deck-orchestrator`

> **6 cases** (5 base obrigatorios + 1 smoke test extra com 3 rotas ambiguas).
> Orchestrator e critico para qualidade do plugin — TODOS devem passar antes de declarar DoD.

---

## Case 1: Routing direto (3+ keywords mesma rota — caminho 90%)

**Input:** `/deck preciso pitchar Beauty Smile pra anjo do Iguatemi, R$500k`

**Comportamento esperado:**

1. Auto-detection §10.5 nivel 1 → regex `\bBeauty Smile\b` casa → marca = `Beauty Smile`
2. `design_system_skill = beauty-smile-design-system` → tenta carregar
3. Contagem keywords:
   - fundraising: "pitchar"(1) + "anjo"(1) + "R$500k"(1) = **3**
   - outras rotas: 0
4. Algoritmo D10 → `top[0].score=3, top[1].score=0` → **routing direto SEM perguntar U1-U3**
5. Output ao usuario:
   ```
   [Auto-detection: Beauty Smile via input regex — design system carregado]
   [Keywords fundraising: "pitchar"(1) + "anjo"(1) + "R$500k"(1) = 3]
   
   Routing → `deck-fundraising`
   
   Vou te passar para a entrevista universal U1-U6 + F1-F5 fundraising.
   Compliance tags: odontologia-br, cfo-cfm
   ```
6. Handoff context completo com `respostas_pre_coletadas: null`

**Assercoes:**
- [ ] NAO chamou AskUserQuestion (routing direto)
- [ ] `vertical_destino == "deck-fundraising"`
- [ ] `marca_detectada == "Beauty Smile"`
- [ ] `marca_origem == "input_regex"`
- [ ] `design_system_skill == "beauty-smile-design-system"`
- [ ] `compliance_tags` inclui `odontologia-br` e `cfo-cfm`
- [ ] `respostas_pre_coletadas == null`
- [ ] `algoritmo_branch == "2+_mesma_rota_direto"`

---

## Case 2: Ambiguidade rotas (2+ keywords de 2 rotas distintas)

**Input:** `/deck vou dar aula de Er:YAG pra dentistas em curso`

**Comportamento esperado:**

1. Auto-detection §10.5 nivel 1 → regex `Er:YAG` casa → marca = `Fotona`
2. Contagem keywords:
   - teaching: "aula"(1) + "curso"(1) = **2**
   - clinical: "dentistas"(1) = **1**
   - equipment: "Er:YAG"(1) = **1**
3. Empate clinical/equipment (1 cada) + teaching (2) — mas teaching domina

   **Ajuste:** "dentistas" e ambiguo entre clinical/teaching (audiencia clinica em aula). Re-interpretacao do PRD eval case sugere que dentistas+Er:YAG conta como sinal clinical/equipment forte. Algoritmo conservador:
   - teaching: 2 ("aula", "curso")
   - clinical/equipment: 2 ("Er:YAG", "dentistas")
   - **Empate 2-vs-2** → T1 (ambiguidade)
4. AskUserQuestion T1.a:
   ```
   question: "Detectei sinais de aula tecnica E apresentacao clinica. É mais aula de dosimetria/protocolo Er:YAG, ou apresentacao do protocolo clinico ja consolidado?"
   options:
     - "Aula tecnica (deck-teaching)" — Ensino estruturado, chunks ≤7min, hands-on
     - "Apresentacao clinica (deck-clinical)" — Peer-facing, EBM/GRADE, casos
   ```
5. Apos resposta usuario "Aula tecnica" → delega `deck-teaching` modo `aula-tecnica`
6. Handoff inclui `keywords_matched` de AMBAS rotas (auditoria) + `algoritmo_branch: "2+_empate_AskUserQuestion"`

**Assercoes:**
- [ ] Chamou AskUserQuestion T1 (NAO chutou rota)
- [ ] AskUserQuestion teve **2 opcoes** (rotas empatadas)
- [ ] `marca_detectada == "Fotona"` (independente da rota escolhida)
- [ ] `compliance_tags` inclui `anvisa-laser-classe-iii` (injetada de Fotona)
- [ ] Apos resposta → delegou rota escolhida pelo usuario
- [ ] `algoritmo_branch == "2+_empate_AskUserQuestion"`

---

## Case 3: Delegacao externa (NAO e deck)

**Input:** `/deck tem como voce criar um carrossel sobre tratamento?`

**Comportamento esperado:**

1. Auto-detection §10.5 → nenhum match (sem mencao de marca) → marca = `generico`
2. Contagem keywords:
   - copy (delegacao externa): "carrossel"(1) = **1**
   - clinical: "tratamento"(1) = **1**
   - **Empate** entre delegacao externa e vertical
3. **Casos de borda — routing direto + delegacao externa empate** (routing-matrix.md): pergunta T1
   ```
   question: "Detectei 'carrossel' (post social = /copy) E 'tratamento' (deck clinico). É mais carrossel Instagram ou apresentacao do tratamento?"
   options:
     - "Carrossel Instagram (/copy)" — post de redes sociais
     - "Deck clinico do tratamento (deck-clinical)" — apresentacao peer/paciente
   ```
4. Usuario escolhe "Carrossel" → orchestrator delega `/copy`
5. Mensagem final:
   ```
   Isso nao e um deck — carrossel Instagram e da skill `/copy`. Delegando.
   ```

**OBS:** caso o PRD original entenda "carrossel sobre tratamento" como delegacao direta (sem AskUserQuestion porque "carrossel" e termo dominante de social media), a implementacao admite dois caminhos validos:
- **Caminho A (conservador, respeita matriz):** T1 desambigua
- **Caminho B (heuristica peso semantico):** delega direto `/copy` (carrossel e o substantivo principal; "tratamento" e tema secundario)

Para garantir reprodutibilidade, **a implementacao usa Caminho A** (T1 desambigua quando externa empata com vertical).

**Assercoes:**
- [ ] Detectou "carrossel" → delegacao externa
- [ ] Resolveu para `/copy` (com ou sem T1 dependendo do caminho A/B)
- [ ] Mensagem clara "isso NAO e deck — delegando para /copy"
- [ ] NAO chamou `deck-clinical` mesmo com keyword "tratamento" presente

---

## Case 4: Input vago + sugestao /idea-to-brief (D12)

**Input:** `/deck preciso de slides`

**Comportamento esperado:**

1. Auto-detection §10.5 → nenhum match → marca = `generico`
2. Contagem keywords:
   - todas rotas = 0
3. Algoritmo D10 → `top[0].score == 0` → **AskUserQuestion T2 (U1-U3)**
4. Usuario responde:
   - U1: "tipo, alguma coisa pra mostrar pro time" (VAGO)
   - U2: "minha equipe"
   - U3: "15-20min"
5. Re-roda algoritmo com input + respostas:
   - "time" + "equipe" → leve sinal internal (1)
   - Mas U1 ainda vago — sem objetivo concreto (acao da audiencia)
6. **Detecta U1 vago** (heuristica: <10 palavras OU sem verbo de acao OU sem sujeito da decisao):
   - Sem palavras-chave de acao ("decidir", "aprovar", "comprar", "investir", "aprender", "alinhar")
   - "alguma coisa pra mostrar" e meta-vago
7. **AskUserQuestion T3 (sugere /idea-to-brief — D12)**:
   ```
   question: "Seu input ainda esta vago para escolher uma vertical especifica. Recomendo rodar `/idea-to-brief` primeiro... Quer fazer isso?"
   options:
     - "Sim, rodar /idea-to-brief primeiro (Recomendado)"
     - "Nao, segue com deck-builder mesmo assim"
     - "Cancelar"
   ```
8. **NUNCA auto-delega** (D12) — espera confirmacao

**Cenarios pos-T3:**
- Se "Sim" → delega `/idea-to-brief` com input + respostas pre-coletadas
- Se "Nao, segue" → orchestrator pergunta U4 + U5 e roteia `deck-internal all-hands` como melhor palpite
- Se "Cancelar" → sai limpo, sem delegacao

**Assercoes:**
- [ ] Chamou AskUserQuestion T2 (U1-U3) **antes** de qualquer routing
- [ ] Apos U1 vago, chamou AskUserQuestion T3 (sugerir /idea-to-brief)
- [ ] **NAO chamou `/idea-to-brief` automaticamente** (D12)
- [ ] So delega `/idea-to-brief` se usuario explicitamente escolhe opcao 1
- [ ] `algoritmo_branch == "0-1_kw_perguntou_U1-U3"` ou `"apos_U1_sugeriu_idea_to_brief"`

---

## Case 5: Concept-reveal pipeline D3

**Input:** `/deck queria apresentar o conceito da sala VIP do Carnaval 360 pro board`

**Comportamento esperado:**

1. Auto-detection §10.5 nivel 1 → regex `\bCarnaval 360\b` casa → marca = `Carnaval 360`
2. Contagem keywords:
   - concept-reveal: "apresentar conceito"(1) + "sala VIP"(1) = **2**
   - internal: "board"(1) = **1**
   - **Concept-reveal domina** (2 > 1)
3. Algoritmo D10 → rota = `deck-internal` modo `concept-reveal` (rotas 9 da matriz)
4. **AskUserQuestion T4 (pipeline cenografia D3)**:
   ```
   question: "Detectei pipeline cenografia. Modo `concept-reveal` consome artefatos da `skill-cenografia`. Voce ja gerou esses artefatos?"
   options:
     - "Sim, tenho os paths/JSONs prontos"
     - "Nao, ainda preciso gerar"
     - "Quero apresentar SEM os artefatos visuais"
   ```
5. Pos-resposta:
   - Opcao 1 → orchestrator pede paths e delega com artefatos no handoff
   - Opcao 2 → orchestrator PAUSA, mostra mensagem: "Rode `/skill-cenografia` primeiro com tema 'sala VIP Carnaval 360' e me chame de volta com os paths."
   - Opcao 3 → delega com warning `sem_artefatos_warning`

**Assercoes:**
- [ ] Detectou concept-reveal → rota `deck-internal` modo `concept-reveal`
- [ ] Chamou AskUserQuestion T4 ANTES de delegar
- [ ] Handoff inclui `pipeline_cenografia.status` apropriado
- [ ] Se opcao 2 (gerar primeiro) → orchestrator NAO delega, PAUSA
- [ ] `marca_detectada == "Carnaval 360"`
- [ ] Mensagem clara mencionando `skill-cenografia` como pre-requisito

---

## Case 6 (SMOKE TEST EXTRA): 3 rotas ambiguas

**Input:** `/deck preciso de um pitch tecnico-comercial pra investidor em congresso clinico semana que vem`

**Comportamento esperado:**

1. Auto-detection → marca = `generico` (sem match)
2. Contagem keywords:
   - fundraising: "pitch"(1) + "investidor"(1) = **2**
   - sales: "comercial"(1) = **1**
   - clinical: "clinico"(1) = **1**
   - scientific: "congresso"(1) = **1**
   - **3 rotas empatam-ish**: fundraising(2), depois sales/clinical/scientific(1 cada)
3. **Caso especial:** fundraising domina com 2, mas o input descreve uma situacao hibrida (pitch comercial + cenario clinico/congresso).

   **Algoritmo conservador:** quando top[0]=2 e ha 3+ rotas com score 1 (cenario hibrido obvio), promove T1 com top 3 rotas (3 opcoes) em vez de routing direto.
4. **AskUserQuestion T1.b** (3 opcoes max 4):
   ```
   question: "Detectei um cruzamento de 3 verticais (captacao + vendas + cientifico). Qual e o foco principal do pitch?"
   options:
     - "Captacao (deck-fundraising)" — pedir dinheiro, mostrar tese, ask + uso de capital
     - "Vendas/parceria (deck-sales)" — propor produto/parceria comercial
     - "Apresentacao cientifica (deck-scientific)" — congresso, GRADE, evidencia"
   ```
5. Apos resposta usuario → delega a rota escolhida com handoff completo

**Assercoes:**
- [ ] Detectou 3 rotas competindo (mesmo com 1 dominante)
- [ ] Chamou AskUserQuestion T1.b com 3 opcoes
- [ ] NAO chutou fundraising so porque tinha score=2
- [ ] Handoff preserva `keywords_matched` das 3 rotas
- [ ] `algoritmo_branch == "2+_empate_AskUserQuestion"` (mesmo nao sendo empate estrito, e cenario hibrido obvio)

---

## Resumo das assercoes por LOCKED

| LOCKED | Garantido por case |
|--------|--------------------|
| D10 routing-first (2+ kw → direto) | Case 1 |
| D10 empate → AskUserQuestion | Case 2, Case 6 |
| D12 NUNCA auto-delega /idea-to-brief | Case 4 |
| D3 concept-reveal → deck-internal + sinaliza cenografia | Case 5 |
| Delegacao externa clara (NAO e deck) | Case 3 |
| Auto-detection §10.5 (5 niveis) | Cases 1, 2, 5 |
| Handoff context completo | Todos |
| NUNCA tenta gerar deck sem rotear | Todos (orchestrator nunca emite STORYBOARD) |
