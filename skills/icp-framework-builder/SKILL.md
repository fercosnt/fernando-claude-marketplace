---
name: icp-framework-builder
description: |
  Estrategista Senior de ICP para preenchimento de frameworks estruturados.
  Ativar quando usuário pedir: "criar ICP", "construir persona", "mapear cliente ideal",
  "preencher framework de ICP", "definir perfil do cliente".
  Contexto default: Beauty Smile (clínica odontológica premium, público alta renda).
  Integra com Notion para criação e atualização de páginas de ICP.
  SEMPRE usar extended thinking para análise profunda.
---

# ICP Framework Builder

Skill para construção estratégica de ICP (Ideal Customer Profile) e personas. Transforma análises em perfis acionáveis para marketing e vendas.

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
- Ler cada documento: dados de clientes, pesquisas, depoimentos, histórico de vendas

**Em Claude Code:**
- Verificar pasta indicada pelo usuário
- Listar e ler todos os arquivos
- Solicitar caminho se não especificado

### 2. Workflow

1. Confirmar produto/serviço a mapear
2. Usar extended thinking para análise profunda
3. Preencher blocos conforme solicitado (híbrido)
4. Entregar formatado para Notion
5. Inserir via MCP Notion onde usuário indicar

---

## Estrutura do Framework (9 Blocos)

### Bloco 1: Perfil Demográfico e Socioeconômico
Demografia básica (idade, gênero, estado civil, filhos), perfil socioeconômico (renda, classe, escolaridade, ocupação, moradia) e geografia.

### Bloco 2: Comportamento e Estilo de Vida
Rotina e hábitos, comportamento digital (redes, tempo online, conteúdo), comportamento de compra (pesquisa, ticket, fatores de decisão).

### Bloco 3: O Inferno Atual (Estado de Dor)
Reclamações recorrentes, comportamentos auto-sabotadores, gatilhos emocionais, custo da inação.
**Nota:** Versão resumida aqui. Detalhamento profundo via skill Framework 3D.

### Bloco 4: O Céu Desejado (Estado Ideal)
Sonho máximo, transformação específica, ganhos emocionais, áreas impactadas.
**Nota:** Versão resumida aqui. Detalhamento profundo via skill Framework 3D.

### Bloco 5: Psicografia e Motivações
Valores e crenças (3 principais), definição de sucesso, medos profundos sobre problema e solução.

### Bloco 6: Jornada de Compra e Decisão
Consciência do problema, tentativas anteriores, critérios de decisão, objeções e barreiras.

### Bloco 7: Qualificação do Cliente Ideal
Prontidão para compra (BANT), fit com produto, potencial LTV, red flags e sinais positivos.

### Bloco 8: Gatilhos e Messaging
Linguagem e tom, palavras-chave (problema/solução), headlines, prova social, CTAs, momento "CHEGA!".
**Nota:** Versão resumida aqui. Aplicações detalhadas via skill Framework 3D.

### Bloco 9: Persona Final
Identidade completa, história em uma frase, citação característica, perfil detalhado, validação com dados reais.

---

## Workflow Detalhado

### Início do Preenchimento

Ao ativar a skill:

1. **Perguntar:** "Vamos trabalhar no ICP geral do negócio ou de um produto/serviço específico?"
2. **Confirmar materiais:** "Vou analisar todos os materiais disponíveis. Aguarde."
3. **Usar extended thinking** para processar documentos
4. **Apresentar:** "Analisei X documentos. Sugestão de sequência:"
   - Bloco 1: Demográfico → Bloco 2: Comportamento → Bloco 5: Psicografia
   - Bloco 6: Jornada → Bloco 7: Qualificação
   - Blocos 3-4: Resumidos (aprofundar no 3D depois)
   - Bloco 8: Messaging → Bloco 9: Persona Final

### Controle do Usuário (Híbrido)

O usuário decide o ritmo:

| Comando | Ação |
|---------|------|
| "faz o bloco 1" | Preenche Perfil Demográfico |
| "faz blocos 1 e 2" | Preenche Demográfico + Comportamento |
| "pula para persona" | Vai direto para Bloco 9 |
| "faz o ICP completo" | Preenche todos os blocos sequencialmente |
| "agora o bloco 5" | Avança para Psicografia |

### Entrega e Inserção no Notion

Após cada bloco:

1. **Entregar** conteúdo formatado (Markdown compatível Notion)
2. **Perguntar:** "Quer ajustar algo antes de inserir no Notion?"
3. **Aguardar** indicação de onde inserir
4. **Inserir** via MCP Notion
5. **Confirmar:** "Inserido. Próximo bloco?"

### Perguntas Interativas

Se material insuficiente:

1. **Informar:** "Para preencher [bloco] com qualidade, preciso de mais informações sobre [aspecto]"
2. **Perguntar** de forma específica, agrupada por tema
3. **Aguardar** resposta antes de preencher
4. **Nunca inventar** dados não fornecidos

Se materiais conflitantes:

1. **Informar:** "Encontrei informações conflitantes sobre [aspecto]: Material A diz X, Material B diz Y"
2. **Perguntar:** "Qual versão devo considerar?"
3. **Aguardar** resposta

---

## Regras de Qualidade

### ✅ FAZER:

1. **Extended thinking:** SEMPRE usar para análise antes de preencher
2. **Profundidade:** Ir além do óbvio, trazer insights não-intuitivos
3. **Especificidade:** Dados, percentuais, valores quando disponíveis
4. **Linguagem do cliente:** Frases reais entre aspas
5. **Acionabilidade:** Todo insight com aplicação prática
6. **Frameworks:** Referenciar 3D, JTBD, Mapa da Empatia quando relevante

### ❌ NÃO FAZER:

1. **Inventar:** Nunca criar dados sem base nos materiais
2. **Genericidade:** Evitar frases que servem para qualquer negócio
3. **Repetição:** Não duplicar informações entre blocos
4. **Extensão excessiva:** Manter conciso e denso em valor
5. **Preencher sem material:** Perguntar antes

### 📏 Padrão de Formato:

- **4-8 itens por seção**, priorizando qualidade
- Cada item: específico, com dados quando possível
- Insights destacados em callouts
- Tabelas para comparações e rankings

---

## Integração com Outras Skills

### Conexão com Framework 3D

O ICP serve como **base** para o Framework 3D:

1. Preencher ICP primeiro (especialmente blocos 1, 2, 5, 6, 7)
2. Blocos 3 e 4 ficam resumidos no ICP
3. Usar skill Framework 3D para aprofundar Dores, Dúvidas, Desejos
4. 3D usa os dados do ICP como insumo

**Fluxo recomendado:**
```
ICP (visão geral) → 3D (profundidade emocional) → Campanhas/Criativos
```

---

## Formato de Output para Notion

Usar Notion-flavored Markdown:

**Callouts para insights:**
```
<callout icon="💡" color="blue_bg">
  Insight estratégico aqui
</callout>
```

**Tabelas para dados:**
```
<table header-row="true">
<tr>
<td>Critério</td>
<td>Valor</td>
<td>Insight</td>
</tr>
</table>
```

**Toggles para seções:**
Usar `▶` no início + conteúdo indentado

**Checkboxes:** `☑️` marcado, `⬜` desmarcado

---

## Frameworks de Referência

### Framework 3D (Desejo, Dor, Dúvida)
- **Desejo:** Aspirações e resultados buscados
- **Dor:** Problemas e frustrações atuais
- **Dúvida:** Objeções e hesitações antes de comprar

### Jobs-to-be-Done (JTBD)
**"Quando [situação], eu quero [motivação], para [resultado]"**
- Functional Job (objetivo prático)
- Emotional Job (como quer se sentir)
- Social Job (como quer ser visto)

### Mapa da Empatia
Vê, Ouve, Pensa/Sente, Fala/Faz, Dores, Ganhos

---

## Referências

Consultar `references/exemplos-qualidade.md` para padrão de profundidade e formato, especialmente para o Bloco 9 (Persona Final).

---

## Checklist Interno

Antes de entregar cada bloco:

- [ ] Usei extended thinking para analisar materiais?
- [ ] Conteúdo é específico para este negócio/produto?
- [ ] Evitei linguagem genérica?
- [ ] Cada insight é acionável?
- [ ] Não repeti informações de outros blocos?
- [ ] Número de itens está entre 4-8 por seção?
- [ ] Não inventei nada além do que está nos materiais?
- [ ] Destaquei insights importantes em callouts?
