# Skeleton POSTER.md — schema D8 (modo poster, NAO STORYBOARD)

> **D8:** modo `poster` do `deck-scientific` gera arquivo `POSTER-{slug}-{HHmm}.md` com schema proprio. NUNCA usar §10.2 STORYBOARD em modo poster.

Path default: `$DECKS_DIR/{YYYY-MM}/POSTER-{slug}-{HHmm}.md`

```markdown
# Poster: {titulo-paper}

## Meta
- Skill geradora: deck-scientific (modo poster)
- Congresso: {X1}
- Tipo de estudo: {X2}
- Outcome primario: {X3}
- Outcomes secundarios: {lista}
- COI: {X4 — se vazio, "Nenhum a declarar"}
- Big Idea: {U5}
- Marca/grupo: {U6}
- Authors: {lista com afiliacoes}
- ORCID autor responsavel: {se aplicavel}
- Tamanho painel: A0 (84.1 x 118.9 cm) | A1 (59.4 x 84.1 cm) | custom
- Estilo: Better Poster Morrison
- max_ctas: 3 (override scientific D14 — read paper / replicate / contact author)
- Reporting guideline: CONSORT | STROBE | PRISMA | CARE (conforme X2)
- Gerado em: {ISO date}
- Versao: v1
- Poster ID: POSTER-{slug}-{YYYYMMDD-HHmm}

---

## Estrutura Visual (Better Poster Morrison)

### CABECALHO (topo do painel — fonte 60 pt)
**Titulo do estudo:** {titulo conciso, assertivo, action-oriented}
**Authors:** {lista com numero de afiliacao em sobrescrito}
**Affiliations:** {1. instituicao A; 2. instituicao B}
**COI:** {X4 — declaracao explicita visivel no cabecalho}
**Congresso:** {X1}

---

### CENTRO — Key Finding GRANDE (fonte ≥ 100 pt em A0)
**Achado principal em 1 frase + 1 numero chave:**
{ex: "Er:YAG sustenta clareamento por 6 meses em 92% dos casos (n=50)"}

**Sub-achado (fonte intermediaria, opcional):**
{ex: "Delta E medio = 4.8 (IC95% 4.2-5.4, p<0.001)"}

---

### PAINEL ESQUERDO — Background

**Contexto (1-2 paragrafos curtos, fonte 24-32 pt):**
{2-3 frases sobre o problema clinico + relevancia + estado atual da literatura}

**Research question (destaque):**
> {pergunta de pesquisa em 1 frase, em quote ou caixa}

---

### PAINEL INFERIOR ESQUERDO — Methods (small, fonte 18-22 pt)

- **Design:** {X2}
- **Sample:** {n + criterios inclusao/exclusao + recrutamento}
- **Intervention/Exposure:** {protocolo operacionalizado e reproduzivel}
- **Outcome primario:** {X3 operacionalizado + metrica}
- **Outcomes secundarios:** {lista breve}
- **Tempo de seguimento:** {periodo}
- **Analise estatistica:** {testes + software}
- **Reporting per {CONSORT|STROBE|PRISMA|CARE}** — checklist QR no rodape
- **Ethics approval:** {comite + numero}
- **Pre-registration:** {OSF / ClinicalTrials.gov / PROSPERO se aplicavel}

---

### PAINEL DIREITO — Results (figuras Tufte)

**Figura 1 — {nome operacional}**
- Tipo: {forest plot | Kaplan-Meier | scatter | small multiples | linha temporal}
- Tufte aplicado: data-ink ratio alto, sem chartjunk, legenda autossuficiente
- Conteudo: {effect size + IC95% sombreado/barras + p-value visivel}
- N por grupo: {explicito na figura}

**Figura 2 — {nome operacional}** (opcional, se necessario)
- Tipo: {tabela densa Tufte com sparklines | small multiples}
- Conteudo: outcomes secundarios — TODOS reportados (nao cherry-picking)

**Tabela resumida:**
| Outcome | Effect size | IC95% | p-value | n | GRADE |
|---------|-------------|-------|---------|---|-------|
| {X3 primario} | {valor} | {intervalo} | {p} | {n} | {nivel} |
| Secundario 1 | {valor} | {intervalo} | {p} | {n} | {nivel} |
| Secundario 2 | {valor} | {intervalo} | {p} | {n} | {nivel} |

---

### PAINEL INFERIOR DIREITO — Conclusion (small, fonte 18-22 pt)

**Discussion destilada (1-2 paragrafos):**
- Restatement do achado principal
- Comparacao com literatura existente
- Implicacoes clinicas / praticas

**Limitacoes:**
- {limitacao 1 — interna}
- {limitacao 2 — externa}
- {se p>0.05 outcome primario} Erro tipo II: poder = {valor}

**Implicacoes para pratica:**
{1-2 frases acionaveis}

---

### RODAPE — References + COI + Acknowledgments + QR Code + CTAs

**References (5 papers principais):**
1. {Autor et al., Journal, Year, DOI}
2. {Autor et al., Journal, Year, DOI}
3. ...

**COI (declaracao explicita):**
{X4 — copiar do cabecalho para reforco visivel}

**Acknowledgments:**
- Financiamento: {grants + numero}
- Instituicao: {agradecimento}

**ORCID autor responsavel:** {ID}

---

## CTAs (max 3 — D14 override scientific)

1. **Read paper completo:** [QR code grande centralizado] → DOI ou OSF preprint
2. **Replicate o estudo:** [QR menor] → Protocolo + dataset/codigo (OSF / Zenodo / Figshare)
3. **Contact author:** {email ou ORCID + LinkedIn}

---

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de imprimir o poster):
- {ex: "Centro do poster: 'reducao de 80%' sem n nem GRADE — adicionar"}
- {ex: "COI Fotona nao explicitado no cabecalho"}

🟡 Verificar antes:
- {ex: "QR code testado? Link estavel?"}
- {ex: "Tabela secundarios inclui outcomes negativos?"}
- {ex: "Pre-registration mencionada (OSF)?"}

✅ OK:
- COI declarado cabecalho + rodape
- Key finding centralizado com numero chave (n explicito)
- Reporting per {CONSORT|STROBE|PRISMA|CARE} citado em Methods
- GRADE level por outcome na tabela
- Tufte aplicado (data-ink alto, sem chartjunk)
- 3 CTAs (read paper / replicate / contact author)
- QR code para paper completo presente
- Big Idea (U5) = key finding centro

---

## NAO faz (anti-patterns Better Poster Morrison)

- Muro de texto em todos os paineis (densidade alta = ninguem le)
- Key finding pequeno + detalhe grande (inverte a tese)
- Sem QR code (quem se interessa nao tem como aprofundar)
- Logo institucional gigante (ego sobre ciencia)
- Cor decorativa (gradientes, fundos azuis institucionais)
- >3 figuras (perde foco)
- Pizza chart (Tufte)
- Mais de 3 CTAs (D14 override scientific)
- STORYBOARD §10.2 (modo poster usa este schema D8, NUNCA STORYBOARD)
```

---

## Testes de validacao (Better Poster — 4 testes)

1. **Teste de 5 segundos:** leitor a 3 metros entende o key finding (centro grande)?
2. **Teste de QR code:** scan funciona e chega no paper completo?
3. **Teste de COI:** COI declarado e visivel sem zoom?
4. **Teste de GRADE:** outcome primario tem GRADE level explicito na tabela?

Se algum falha, o POSTER.md nao esta pronto.

---

## Fluxo apos gerar POSTER.md

1. Usuario revisa POSTER.md
2. Designer humano (ou IA) executa o layout visual em InDesign / Figma / Adobe Illustrator (escala A0 ou A1)
3. Figuras do paper sao referenciadas diretamente (Tufte aplicado pelo autor; **NAO invoca `deck-image-prompts`** — poster usa figuras do paper)
4. Validar com `deck-reviewer` (opcional)
5. Imprimir
