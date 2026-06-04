# Scorecard de 4 Dimensoes — Rubricas Detalhadas (16 Sub-Metricas)

## Indice

1. [Dimensao 1: Arquitetura da Skill (25%)](#dimensao-1-arquitetura-da-skill-25)
2. [Dimensao 2: Qualidade das Instrucoes (30%)](#dimensao-2-qualidade-das-instrucoes-30)
3. [Dimensao 3: Cobertura Funcional (25%)](#dimensao-3-cobertura-funcional-25)
4. [Dimensao 4: Ecossistema e Manutencao (20%)](#dimensao-4-ecossistema-e-manutencao-20)
5. [Formula de Calculo](#formula-de-calculo)
6. [Penalidades](#penalidades)
7. [Classificacao Final](#classificacao-final)

---

## Dimensao 1: Arquitetura da Skill (25%)

Avalia a qualidade estrutural da skill como artefato de software.

**Por que 25%:** A arquitetura determina eficiencia em tokens (custo direto), facilidade de manutencao, e aderencia ao principio de progressive disclosure que o Claude Code espera.

### 1.1 Estrutura de Arquivos (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Progressive disclosure exemplar. SKILL.md enxuto (<500 linhas). References para conteudo pesado. Scripts/assets quando necessario. Cada arquivo tem proposito claro e nome descritivo. |
| 7-8 | Boa organizacao com desvios menores. Algum conteudo que deveria estar em reference esta inline. |
| 5-6 | Funcional mas monolitico. Tudo no SKILL.md ou references mal organizados. |
| 3-4 | Estrutura confusa. Arquivos sem proposito claro ou nomes genericos. |
| 1-2 | Arquivo unico sem qualquer estrutura. |

**O que verificar:**
- SKILL.md contem apenas workflow e instrucoes essenciais?
- References contem detalhamento que seria caro manter inline?
- Scripts existem apenas para operacoes deterministicas/frageis?
- Cada arquivo tem nome descritivo (nao ref1.md, ref2.md)?

**Red flags:**
- README.md dentro da skill (para humanos, nao para AI)
- CHANGELOG.md (documentacao nao lida pelo Claude)
- Arquivos orfaos nao referenciados no SKILL.md
- References sem TOC ou organizacao interna

**Benchmark (baseado em 17+ skills analisadas):**
- Mediana de arquivos: 3-5 (SKILL.md + 2-4 references)
- Skills com scripts: ~30% (apenas quando necessario)
- Skills com assets: ~15% (imagens de referencia, templates)

---

### 1.2 Metadata e Trigger (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Description cobre TODOS os triggers possiveis com sinonimos. Name e slug-friendly. Description < 1024 chars mas exaustiva em triggers. |
| 7-8 | Description boa mas faltam 1-2 triggers obvios. |
| 5-6 | Description descreve workflow (errado) em vez de triggers. |
| 3-4 | Description vaga, skill dificilmente sera ativada automaticamente. |
| 1-2 | Frontmatter ausente ou malformado. |

**O que verificar:**
- Frontmatter YAML valido com `name` e `description`?
- `name` e slug-friendly (kebab-case, sem espacos)?
- `description` < 1024 caracteres?
- Description lista QUANDO usar (triggers), nao O QUE faz (workflow)?
- Sinonimos cobertos? (ex: "analisar", "avaliar", "revisar", "pontuar")

**Como testar acuracia do trigger:**
1. Imaginar 5 formas diferentes que um usuario pediria essa funcionalidade
2. Verificar se a description contem palavras-chave de cada forma
3. Verificar se a description NAO aciona para pedidos nao relacionados

**Anatomia de description eficaz:**
```
[VERBO + O QUE FAZ] + [QUANDO USAR com lista exaustiva de triggers]
```

**Exemplo bom:**
```
Analisa qualquer skill do Claude Code usando scorecard de 4 dimensoes.
Ativar quando usuario pedir para analisar skill, avaliar skill, revisar
skill, pontuar skill, diagnosticar skill, comparar skills, checklist
rapido de skill, ou verificar qualidade de skill.
```

**Exemplo ruim:**
```
Framework de analise que usa 16 metricas ponderadas para gerar scores
e planos de melhoria com tasklists priorizadas.
```
(Descreve o que faz, nao quando usar. Usuario que diz "avalia essa skill" nao vai ativar.)

---

### 1.3 Tamanho e Eficiencia (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Cada linha justifica seu custo em tokens. Sem repeticao. Conteudo no lugar certo. |
| 7-8 | Leve repeticao ou conteudo que poderia ser movido para reference. |
| 5-6 | SKILL.md inchado (>500 linhas) com conteudo que deveria ser reference. |
| 3-4 | Desperdicando contexto com conteudo irrelevante ou redundante. |
| 1-2 | Massivamente ineficiente (>800 linhas monoliticas). |

**Benchmark de tamanho (17+ skills):**

| Metrica | Valor |
|---------|-------|
| Mediana SKILL.md | ~250 linhas |
| Range saudavel | 93-500 linhas |
| Maximo com references | ~750 linhas total |
| Acima de 800 sem references | Penalidade x0.95 |

**O que verificar:**
- Linhas do SKILL.md vs benchmark?
- Conteudo repetido entre SKILL.md e references?
- Tabelas/listas que poderiam ser mais concisas?
- Conteudo que deveria estar em reference (detalhamento pesado)?
- Tokens gastos em comentarios/explicacoes para humanos vs instrucoes para AI?

**Calculo do subtotal Dimensao 1:**
```
subtotal = (estrutura × 3 + metadata × 2.5 + tamanho × 2) / (3 + 2.5 + 2)
subtotal = (estrutura × 3 + metadata × 2.5 + tamanho × 2) / 7.5
```

---

## Dimensao 2: Qualidade das Instrucoes (30%)

Avalia quao bem a skill instrui o Claude a executar a tarefa.

**Por que 30% (maior peso):** Instrucoes sao o core da skill. Uma skill com arquitetura perfeita mas instrucoes ruins produz resultados ruins.

### 2.1 Clareza e Naturalidade (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Linguagem natural, imperativa, zero jargao desnecessario. Tabelas e listas para decisao rapida. Escaneavel na primeira leitura. |
| 7-8 | Claro e direto, ocasionalmente tecnico demais ou verboso. |
| 5-6 | Funcional mas robotico. Paredes de texto sem hierarquia visual. |
| 3-4 | Confuso, instrucoes enterradas em prosa. |
| 1-2 | Incompreensivel ou contraditorio. |

**O que verificar:**
- Usa forma imperativa? ("Faca X" vs "Voce deveria fazer X")
- Tom apropriado e consistente ao longo da skill?
- Tabelas para decisoes rapidas (sinais -> acoes)?
- Headers e listas para escaneabilidade?
- Livre de jargao desnecessario?
- Paragrafos curtos (max 3-4 linhas)?

**Checklist de escaneabilidade:**
- [ ] Headers hierarquicos (H2 > H3 > H4)?
- [ ] Listas para itens sequenciais?
- [ ] Tabelas para dados estruturados?
- [ ] Negrito para termos-chave?
- [ ] Secoes com tamanho uniforme?

---

### 2.2 Contexto e Justificativas (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Toda instrucao tem PORQUE. Zero numeros arbitrarios sem justificativa. |
| 7-8 | Maioria tem justificativa. Poucas regras sem contexto. |
| 5-6 | Instrucoes claras mas sem contexto do porque. |
| 3-4 | Instrucoes vagas. Regras arbitrarias. |
| 1-2 | Instrucoes contraditorias ou ausentes. |

**O que verificar:**
- Cada instrucao tem justificativa (o PORQUE)?
- Numeros arbitrarios sao justificados? (ex: "max 5" — por que 5?)
- Contexto suficiente para decisoes em edge cases?
- Principios sobre numeros? ("pare quando clareza >= 80%" > "maximo 5 perguntas")

**Metrica concreta:** Contar % de instrucoes com justificativa.
- >= 80% = score 9+
- >= 60% = score 7-8
- >= 40% = score 5-6
- < 40% = score 3-4

**Exemplo bom:**
> "Maximo 3 perguntas na fase de contexto — porque a skill sob analise ja fornece contexto suficiente e mais perguntas causam fadiga"

**Exemplo ruim:**
> "Maximo 5 perguntas" (por que 5 e nao 4 ou 6?)

---

### 2.3 Especificidade vs Liberdade (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Equilibrio perfeito: detalhado onde operacao e fragil, flexivel onde Claude pode decidir. Graus de liberdade explicitamente calibrados. |
| 7-8 | Bom balanco com leves excessos em um sentido. |
| 5-6 | Muito vago OU muito prescritivo. |
| 3-4 | Claramente sub ou super especificado. |
| 1-2 | Totalmente aberto OU microgerencia cada decisao. |

**Framework de graus de liberdade (analogia da ponte):**

| Grau | Mecanismo | Quando usar | Exemplo |
|------|-----------|-------------|---------|
| **Alta liberdade** | Instrucoes textuais | Decisoes onde multiplas abordagens sao validas | "Escolha o tom adequado ao contexto" |
| **Media liberdade** | Pseudocodigo com parametros | Processos que precisam de estrutura mas permitem variacao | "Se input > 500 linhas, resuma primeiro" |
| **Baixa liberdade** | Scripts exatos | Operacoes frageis onde desvio = erro | Script bash para validacao de YAML |

**O que verificar:**
- Onde a skill e prescritiva, faz sentido? (operacoes frageis, formatos exatos)
- Onde a skill e flexivel, faz sentido? (decisoes criativas, adaptacao ao contexto)
- Existe mistura? (prescritivo onde deveria ser flexivel ou vice-versa)

---

### 2.4 Anti-Patterns e Guardas (peso 1.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Triade DO/DON'T/VERIFY completa e especifica. Anti-patterns nomeados com justificativa. |
| 7-8 | DO e DON'T presentes, sem VERIFY explicito. |
| 5-6 | Apenas instrucoes positivas (sem anti-patterns). |
| 3-4 | Anti-patterns obvios nao mencionados. |
| 1-2 | Sem qualquer guideline de qualidade ou guarda. |

**Triade DO/DON'T/VERIFY:**
- **DO:** O que fazer (instrucoes positivas)
- **DON'T:** O que NAO fazer (anti-patterns nomeados)
- **VERIFY:** Como verificar se fez certo (checklist de qualidade)

**O que verificar:**
- Tem instrucoes negativas explicitas (DON'T)?
- Anti-patterns sao nomeados e justificados?
- Existe mecanismo de verificacao (VERIFY)?
- Guardas previnem erros comuns do dominio?

**Calculo do subtotal Dimensao 2:**
```
subtotal = (clareza × 3 + contexto × 2.5 + especificidade × 2 + antipatterns × 1.5) / (3 + 2.5 + 2 + 1.5)
subtotal = (clareza × 3 + contexto × 2.5 + especificidade × 2 + antipatterns × 1.5) / 9.0
```

---

## Dimensao 3: Cobertura Funcional (25%)

Avalia se a skill cobre o que precisa cobrir para cumprir seu proposito.

**Por que 25%:** Uma skill pode ser bem escrita mas incompleta — faltando modos, exemplos ou tratamento de edge cases.

### 3.1 Workflow e Modos (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Workflow completo de inicio a fim. Deteccao automatica de modo. Arvores de decisao para branching. Cada passo com acao clara. |
| 7-8 | Workflow solido com minor gaps. Deteccao de modo presente mas incompleta. |
| 5-6 | Passos basicos presentes, faltam ramificacoes ou modos alternativos. |
| 3-4 | Descricao de conceitos sem workflow acionavel. |
| 1-2 | Sem workflow identificavel. |

**O que verificar:**
- Workflow tem inicio definido (primeiro passo claro)?
- Passos sao sequenciais e acionaveis?
- Fim/entrega esta definido?
- Transicoes entre passos sao claras?
- Deteccao de modo e automatica (tabela de sinais)?
- Branching para cenarios diferentes?

**Checklist de completude de workflow:**
- [ ] Trigger -> primeiro passo definido?
- [ ] Cada passo tem acao + output?
- [ ] Transicoes entre passos sao explicitas?
- [ ] Modos alternativos cobertos?
- [ ] Passo final com entrega definida?

---

### 3.2 Exemplos e Demonstracoes (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | 3+ exemplos concretos e completos cobrindo modos principais. Pares before/after quando aplicavel. Anotados com "por que e bom". |
| 7-8 | Exemplos presentes e uteis, sem anotacao ou cobrindo so 1 modo. |
| 5-6 | 1 exemplo basico ou exemplos com placeholders genericos. |
| 3-4 | Exemplos irrelevantes ou mal formulados. |
| 1-2 | Sem exemplos em skill que claramente precisa. |

**O que verificar:**
- Exemplos sao concretos (dados reais, nao "[placeholder]")?
- Exemplos cobrem modos diferentes da skill?
- Exemplos sao anotados (explicam POR QUE sao bons)?
- Pares before/after quando a skill transforma algo?
- Exemplos de edge cases, nao so happy path?

**Inventario de exemplos (template):**

| # | Tipo | Concreto? | Anotado? | Modo coberto |
|---|------|-----------|----------|-------------|
| 1 | [tipo] | [sim/nao] | [sim/nao] | [modo] |

---

### 3.3 Edge Cases e Fallbacks (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Fallbacks para inputs inesperados. Instrucoes para ambiguidade. Limites de escopo definidos. O que fazer quando a skill nao se aplica. |
| 7-8 | Cobre casos principais, faltam edge cases raros. |
| 5-6 | Funciona para happy path, quebra em variantes. |
| 3-4 | Funciona so para o cenario exato imaginado. |
| 1-2 | Nenhuma consideracao de variantes. |

**Edge cases universais que toda skill deveria tratar:**
- Input vazio ou incompleto
- Input fora do escopo da skill
- Ambiguidade que requer clarificacao
- Erros durante execucao
- Output que nao atende expectativas

**O que verificar:**
- Skill define limites de escopo (o que NAO faz)?
- Tem fallback para input inesperado?
- Instrui o Claude sobre quando pedir clarificacao?
- Define comportamento para erros?

---

### 3.4 Output e Entrega (peso 1.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Formato de saida definido com template. Checklist de verificacao pre-entrega. Metadata no output (data, versao, metodo). |
| 7-8 | Formato definido sem template ou checklist. |
| 5-6 | Formato implicito, nao especificado. |
| 3-4 | Sem definicao de output. |
| 1-2 | Output ambiguo que confunde o usuario. |

**O que verificar:**
- Formato de saida esta definido explicitamente?
- Existe template de output?
- Checklist de verificacao pre-entrega?
- Metadata no output (data, metodo, versao)?
- Output e consistente entre execucoes?

**Calculo do subtotal Dimensao 3:**
```
subtotal = (workflow × 3 + exemplos × 2.5 + edge_cases × 2 + output × 1.5) / (3 + 2.5 + 2 + 1.5)
subtotal = (workflow × 3 + exemplos × 2.5 + edge_cases × 2 + output × 1.5) / 9.0
```

---

## Dimensao 4: Ecossistema e Manutencao (20%)

Avalia integracao com o ambiente e viabilidade a longo prazo.

**Por que 20%:** Uma skill isolada e fragil. Integracao com o ecossistema Claude Code e consistencia interna determinam vida util.

### 4.1 References e Recursos (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | References tematicos com proposito claro. Cada um cobrindo um dominio. TOC para navegabilidade. Sem arquivo orfao. Todos referenciados no SKILL.md. |
| 7-8 | References uteis com minor gaps de cobertura. |
| 5-6 | Poucos references ou references genericos. |
| 3-4 | References confusos ou irrelevantes. |
| 1-2 | Sem references em skill que claramente precisa. |

**O que verificar:**
- Cada reference tem proposito claro e distinto?
- Todos sao referenciados no SKILL.md?
- Existem arquivos orfaos (nao referenciados)?
- References tem TOC interno para navegabilidade?
- Conteudo dos references e complementar (sem sobreposicao)?

**Template de inventario:**

| Reference | Linhas | Proposito | Referenciado? |
|-----------|--------|-----------|--------------|
| [arquivo] | [N] | [proposito] | [sim/nao] |

---

### 4.2 Integracao com Plataforma (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Usa features do Claude Code quando relevante (TodoWrite para tracking, MCP para integracoes, Bash para operacoes de sistema, Task para paralelismo). Nao reinventa o que a plataforma oferece. |
| 7-8 | Integracoes principais presentes, faltam oportunidades. |
| 5-6 | Funcional mas ignora capabilities da plataforma. |
| 3-4 | Poderia ser para qualquer LLM, nao aproveita o Claude Code. |
| 1-2 | Conflita com convencoes da plataforma. |

**Features do Claude Code disponiveis:**

| Feature | Quando usar |
|---------|------------|
| TodoWrite | Tracking de progresso em tarefas multi-step |
| Task (subagents) | Paralelizar pesquisa ou trabalho independente |
| Read/Glob/Grep | Explorar codebase |
| Bash | Operacoes de sistema, git, builds |
| MCP servers | Integracoes com servicos externos |
| Edit/Write | Modificar/criar arquivos |
| WebFetch/WebSearch | Pesquisa na web |
| AskUserQuestion | Clarificacao estruturada |

**O que verificar:**
- Skill instrui uso de tools relevantes?
- Nao reinventa funcionalidades existentes?
- Integra com hooks/CLAUDE.md quando apropriado?
- Usa TodoWrite para workflows multi-step?

---

### 4.3 Consistencia Interna (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Pratica o que prega. Estrutura segue as regras que ensina. Cross-references todos validos. Zero contradicoes. |
| 7-8 | Consistente com minor desvios. |
| 5-6 | Inconsistencias visiveis (ex: ensina XML mas usa markdown puro). |
| 3-4 | Contradicoes que confundem o Claude. |
| 1-2 | Totalmente inconsistente. |

**O que verificar:**
- Skill pratica o que prega? (estrutura segue as regras que define)
- Cross-references entre SKILL.md e references sao validos?
- Terminologia consistente em todos os arquivos?
- Sem contradicoes entre secoes?
- Numeros/scores consistentes (mesma escala em todo lugar)?

---

### 4.4 Evolucao (peso 1.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Facil de iterar: secoes modulares, references substituiveis, workflow extensivel. |
| 7-8 | Razoavelmente modular, algumas secoes acopladas. |
| 5-6 | Mudancas exigem reescrever secoes grandes. |
| 3-4 | Monolitico, dificil de modificar sem quebrar. |
| 1-2 | Qualquer mudanca exige reescrever tudo. |

**O que verificar:**
- Secoes sao modulares (podem ser editadas independentemente)?
- References podem ser substituidos sem quebrar o SKILL.md?
- Workflow pode ser estendido com novos passos/modos?
- Formato permite versionamento (git-friendly)?

**Calculo do subtotal Dimensao 4:**
```
subtotal = (references × 3 + plataforma × 2.5 + consistencia × 2 + evolucao × 1.5) / (3 + 2.5 + 2 + 1.5)
subtotal = (references × 3 + plataforma × 2.5 + consistencia × 2 + evolucao × 1.5) / 9.0
```

---

## Formula de Calculo

### Score Bruto

```
raw = (dim1_arquitetura × 0.25) + (dim2_instrucoes × 0.30) + (dim3_cobertura × 0.25) + (dim4_ecossistema × 0.20)
```

### Subtotal por Dimensao

```
subtotal_dim = Sigma(score_sub_metrica × peso) / Sigma(pesos)
```

**Exemplo Dimensao 1:**
```
subtotal = (estrutura × 3 + metadata × 2.5 + tamanho × 2) / 7.5
subtotal = (8 × 3 + 9 × 2.5 + 7 × 2) / 7.5
subtotal = (24 + 22.5 + 14) / 7.5 = 8.07
```

---

## Penalidades

Penalidades sao multiplicativas e acumulam:

| Condicao | Penalidade | Justificativa |
|----------|------------|---------------|
| Sub-metrica critica < 5.0 | x 0.85 (-15%) | Falha grave que invalida o conjunto |
| Reference ausente para funcionalidade core | x 0.90 (-10%) | Viola progressive disclosure |
| Description nao aciona corretamente | x 0.90 (-10%) | Skill inacessivel = skill inexistente |
| SKILL.md > 800 linhas sem references | x 0.95 (-5%) | Monolito desperdicando tokens |

**Sub-metricas criticas (disparam -15% se < 5.0):**
- Clareza e Naturalidade (sem clareza, nada funciona)
- Contexto e Justificativas (sem contexto, Claude nao generaliza)
- Workflow e Modos (sem workflow, skill nao executa)
- Metadata e Trigger (sem trigger, skill nao ativa)

---

## Classificacao Final

| Score | Classificacao | Significado |
|-------|---------------|-------------|
| >= 9.0 | **Elite** | Pronto para producao, excelencia. Referencia para outras skills. |
| >= 8.0 | **Profissional** | Alta qualidade. Gaps menores que nao impedem uso eficaz. |
| >= 7.0 | **Competente** | Solido, funcional. Iteracao recomendada para gaps identificados. |
| >= 6.0 | **Em desenvolvimento** | Iteracao obrigatoria. Gaps significativos que afetam qualidade. |
| < 6.0 | **Inadequado** | Revisao major necessaria. Fundamentos precisam ser reconstruidos. |

### Thresholds de Acao

| Condicao | Acao |
|----------|------|
| Score >= 8.5 + todas metricas >= 7.0 | Aprovacao — skill pronta |
| Score >= 7.5 | Aprovada com sugestoes opcionais |
| Score < 7.5 | Iteracao obrigatoria antes de uso |
| Qualquer metrica critica < 5.0 | BLOQUEADO — corrigir antes de qualquer outra coisa |
