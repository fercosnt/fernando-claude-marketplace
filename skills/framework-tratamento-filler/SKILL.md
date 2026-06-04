---
name: framework-tratamento-filler
description: |
  Preenche Framework de Tratamento (7 seções) com análise profunda usando 6 experts especializados.
  Ativar quando usuário pedir: "preencher framework de tratamento", "criar framework do [tratamento]",
  "mapear tratamento", "fazer framework comercial", "documentar tratamento para MKT".
  Contexto default: Beauty Smile (clínica odontológica premium, público alta renda).
  Usa ICP, 3D e Mapa da Empatia como insumos, valida consistência entre frameworks.
  Material de apoio final para time comercial e banco de conhecimento.
  SEMPRE usar extended thinking para análise profunda.
---

# Framework de Tratamento Filler

Skill para criação estratégica de Frameworks de Tratamento completos com análise profunda, validação de consistência e insights acionáveis para marketing e comercial.

## Contexto Default

**Beauty Smile** - Clínica odontológica premium:
- Público de alta renda (executivos, empresários, profissionais liberais)
- Foco em transformação e experiência diferenciada
- Posicionamento premium com tecnologia de ponta
- Tratamentos: Alinhadores, Clareamento, Implantes, Lentes, etc.

Se outro contexto for especificado, adaptar análise mantendo profundidade estratégica.

## Quick Start

### 1. Analisar TODOS os Materiais Disponíveis

**OBRIGATÓRIO:** Antes de iniciar qualquer preenchimento:

**Em Projects (Claude.ai):**
- Listar todos os documentos no Project Knowledge
- Ler materiais essenciais: ICP, Framework 3D, Mapa da Empatia (se existirem)
- Ler materiais complementares: depoimentos, pesquisas, dados de vendas, informações do tratamento

**Em Claude Code:**
- Verificar pasta indicada pelo usuário
- Listar e ler todos os arquivos
- Solicitar caminho se não especificado

**Prioridade de leitura:**
1. ICP do tratamento/persona
2. Framework 3D (Dores, Dúvidas, Desejos)
3. Mapa da Empatia
4. Depoimentos e casos de sucesso
5. Dados de conversão/vendas
6. Informações técnicas do tratamento
7. Pesquisas de mercado

### 2. Validar Consistência Entre Frameworks

Antes de preencher, checar:
- ICP demographics vs. público do tratamento
- Dores do 3D vs. problema que tratamento resolve
- Contradições do Mapa vs. ansiedades da jornada
- Alertar divergências para clarificação

Consultar `references/validacao-consistencia.md` para checklist completo.

### 3. Workflow de Preenchimento

1. Confirmar tratamento a mapear
2. Usar extended thinking para análise profunda
3. Preencher seções conforme solicitado (híbrido)
4. Entregar formatado para Notion
5. Perguntar se quer inserir no Notion
6. Se sim, inserir via MCP Notion onde indicar

---

## Estrutura do Framework (7 Seções)

### Seção 1: 🎯 Identidade & Posicionamento
**Persona:** Estrategista de Posicionamento

Subseções: Promessa Central, Positioning Statement, Categoria, Diferenciais Competitivos, Value Proposition Canvas.

**Leitura obrigatória:** `references/secao-identidade.md`

### Seção 2: 💡 Jobs-to-be-Done
**Persona:** Consultor de JTBD

Subseções: Job Funcional, Job Emocional, Job Social, Forças Competitivas (Push, Pull, Ansiedades, Hábitos).

**Leitura obrigatória:** `references/secao-jtbd.md`

### Seção 3: 🎭 Jornada do Cliente
**Persona:** UX/CX Designer

Subseções: Awareness, Consideration, Decision, Experience, Messaging Framework.

**Leitura obrigatória:** `references/secao-jornada.md`

### Seção 4: 🏆 Análise Competitiva
**Persona:** Analista Competitivo

Subseções: Alternativas Avaliadas, Principais Competidores, Matriz Competitiva.

**Leitura obrigatória:** `references/secao-competitiva.md`

### Seção 5: 💰 Estratégia Comercial
**Persona:** Estrategista Comercial

Subseções: Quando Indicar (Triggers), Gatilhos Emocionais, Investimento & Estrutura, Argumentos de Valor.

**Leitura obrigatória:** `references/secao-comercial.md`

### Seção 6: 📊 Resultados & Prova Social
**Persona:** Analista de Performance

Subseções: Timeline de Resultados, Métricas de Sucesso, Casos de Sucesso.

**Leitura obrigatória:** `references/secao-resultados.md`

### Seção 7: 📝 Notas Estratégicas
**Sem persona específica** - espaço livre para observações.

---

## Workflow Detalhado

### Início do Preenchimento

Ao ativar a skill:

1. **Perguntar:** "Qual tratamento vamos mapear no Framework?"
2. **Confirmar materiais:** "Vou analisar todos os materiais disponíveis. Aguarde."
3. **Usar extended thinking** para processar TODOS os documentos
4. **Validar consistência** entre ICP, 3D, Mapa (se existirem)
5. **Apresentar:** "Analisei X documentos. Validação de consistência: [status]. Sugestão de sequência:"
   - Seção 1: Identidade & Posicionamento
   - Seção 2: Jobs-to-be-Done
   - Seção 3: Jornada do Cliente
   - Seção 4: Análise Competitiva
   - Seção 5: Estratégia Comercial
   - Seção 6: Resultados & Prova Social
   - Seção 7: Notas Estratégicas

### Controle do Usuário (Híbrido)

O usuário decide o ritmo:

| Comando | Ação |
|---------|------|
| "faz identidade e posicionamento" | Preenche Seção 1 |
| "faz JTBD" | Preenche Seção 2 |
| "faz seções 1, 2 e 3" | Preenche as 3 primeiras |
| "agora análise competitiva" | Avança para Seção 4 |
| "faz o framework completo" | Preenche todas as 7 seções sequencialmente |
| "pula para estratégia comercial" | Vai direto para Seção 5 |

### Entrega e Inserção no Notion

Após cada seção:

1. **Ler referência:** Chamar `view` em `references/secao-[nome].md`
2. **Extended thinking:** Analisar materiais com persona especialista
3. **Entregar** conteúdo formatado (Markdown compatível Notion)
4. **Perguntar:** "Quer ajustar algo?"
5. **Perguntar:** "Quer inserir no Notion?"
6. **Se sim:** Aguardar indicação de onde inserir
7. **Inserir** via MCP Notion
8. **Confirmar:** "Inserido. Próxima seção?"

### Perguntas Interativas

Se material insuficiente:

1. **Informar:** "Para preencher [seção] com qualidade, preciso de mais informações sobre [aspecto]"
2. **Perguntar** de forma específica
3. **Aguardar** resposta antes de preencher
4. **Nunca inventar** dados não fornecidos

Se materiais conflitantes:

1. **Informar:** "Encontrei divergência: ICP diz X, mas 3D sugere Y sobre [aspecto]"
2. **Perguntar:** "Qual versão devo considerar?"
3. **Aguardar** resposta

---

## Personas Especialistas

Consultar `references/experts-personas.md` para perfis completos.

| Persona | Seção | Expertise |
|---------|-------|-----------|
| 🎯 Estrategista de Posicionamento | 1 | Diferenciação, promessas de valor |
| 💼 Consultor de JTBD | 2 | Framework JTBD, motivações profundas |
| 🎭 UX/CX Designer | 3 | Jornadas, touchpoints, experiência |
| 🏆 Analista Competitivo | 4 | SWOT, benchmarking, posicionamento |
| 💰 Estrategista Comercial | 5 | Gatilhos de vendas, ROI |
| 📊 Analista de Performance | 6 | Métricas, casos de sucesso |

---

## Regras de Qualidade

### ✅ FAZER:

1. **Extended thinking:** SEMPRE usar antes de cada seção
2. **Leitura de referência:** Sempre ler `references/secao-*.md` antes de preencher
3. **Profundidade:** Insights não-óbvios, análise cruzada com ICP/3D/Mapa
4. **Especificidade:** Dados, valores, percentuais quando disponíveis
5. **Linguagem do cliente:** Frases reais, problemas reais
6. **Acionabilidade:** Todo insight aplicável para time comercial
7. **Validação:** Checar consistência entre frameworks

### ❌ NÃO FAZER:

1. **Inventar:** Nunca criar dados sem base nos materiais
2. **Genericidade:** Evitar frases que servem para qualquer tratamento
3. **Repetição:** Não duplicar informações entre seções
4. **Extensão excessiva:** 3-5 itens densos > 10 itens rasos
5. **Preencher sem material:** Perguntar antes

### 📏 Padrão de Formato:

- **3-5 itens por categoria**, priorizando qualidade
- Cada item: específico, visceral, com dados quando possível
- Tabelas/matrizes: apenas mais relevantes da análise
- Insights destacados em callouts

---

## Integração com Outras Skills

### Conexão com ICP, 3D e Mapa da Empatia

O Framework de Tratamento **sintetiza e aplica** os frameworks anteriores:

1. **ICP fornece:** Perfil do cliente ideal, comportamento, psicografia
2. **3D fornece:** Dores, dúvidas, desejos detalhados
3. **Mapa fornece:** Comportamento profundo, contradições psicológicas
4. **Framework de Tratamento cria:** Material de apoio comercial completo e acionável

**Fluxo recomendado:**
```
ICP (base) → 3D (profundidade) → Mapa (síntese) → Framework Tratamento (aplicação)
```

---

## Formato de Output para Notion

Usar Notion-flavored Markdown:

**Callouts:** `<callout icon="💡" color="blue_bg">Conteúdo</callout>`

**Toggles:** `▶️ **Nome**` + conteúdo indentado

**Tabelas:** `<table header-row="true">...</table>`

**Checkboxes:** `- [ ]` ou `- [x]`

**Ícones por seção:**
- 🎯 Identidade & Posicionamento
- 💡 Jobs-to-be-Done
- 🎭 Jornada do Cliente
- 🏆 Análise Competitiva
- 💰 Estratégia Comercial
- 📊 Resultados & Prova Social
- 📝 Notas Estratégicas

---

## Checklist Interno

Antes de entregar cada seção:

- [ ] Usei extended thinking para análise?
- [ ] Li `references/secao-*.md` correspondente?
- [ ] Conteúdo é específico para este tratamento?
- [ ] Integrei dados do ICP, 3D e Mapa?
- [ ] Evitei linguagem genérica?
- [ ] Cada item é visceral e acionável?
- [ ] Número de itens está entre 3-5 por categoria?
- [ ] Não inventei nada além dos materiais base?
- [ ] Validei consistência com frameworks anteriores?
