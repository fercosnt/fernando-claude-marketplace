---
name: framework-3d-filler
description: |
  Preenche o Framework 3D (Dores, Dúvidas, Desejos) com profundidade estratégica e concisão. 
  Ativar quando usuário pedir: "preencher framework 3D", "mapear dores, dúvidas e desejos", 
  "criar 3D para [tratamento]", "analisar ICP com framework 3D". 
  Contexto default: Beauty Smile (clínica odontológica premium, público alta renda). 
  Gera conteúdo seção por seção, formatado para Notion, com insights acionáveis para campanhas e criativos.
  SEMPRE usar extended thinking para análise profunda.
---

# Framework 3D Filler

Skill para preenchimento estratégico do Framework 3D (Dores, Dúvidas, Desejos) com foco em qualidade, concisão e aplicabilidade para marketing.

## Contexto Default

**Beauty Smile** - Clínica odontológica premium:
- Público de alta renda (executivos, empresários, profissionais liberais)
- Foco em transformação e experiência diferenciada
- Posicionamento premium com tecnologia de ponta
- Tratamentos: Alinhadores, Clareamento, Implantes, Lentes, etc.

Se outro contexto for especificado, adaptar análise mantendo profundidade estratégica.

## Quick Start

### 1. Analisar TODOS os Materiais Disponíveis

**OBRIGATÓRIO:** Antes de iniciar qualquer preenchimento, identificar e analisar todos os materiais:

**Em Projects (Claude.ai):**
- Listar todos os documentos no Project Knowledge
- Ler cada documento relevante: ICP, depoimentos, FAQs, informações do tratamento, dados da clínica

**Em Claude Code:**
- Verificar pasta indicada pelo usuário
- Listar e ler todos os arquivos da pasta
- Solicitar caminho se não especificado

### 2. Workflow

1. Confirmar tratamento/produto a mapear
2. Usar extended thinking para análise profunda dos materiais
3. Preencher seções conforme solicitado (parte a parte ou completo)
4. Entregar formatado para Notion
5. Inserir via MCP Notion onde usuário indicar

---

## Workflow Detalhado

### Início do Preenchimento

Ao ativar a skill:

1. **Perguntar:** "Qual tratamento/produto vamos mapear no 3D?"
2. **Confirmar materiais:** "Vou analisar todos os materiais disponíveis sobre [tratamento]. Aguarde."
3. **Usar extended thinking** para processar todos os documentos
4. **Apresentar:** "Analisei X documentos. Pronto para preencher. Sugestão de sequência:"
   - Dores (Físicas → Emocionais → Financeiras → Sociais)
   - Dúvidas (Produto → Si Mesmo → Processo → Resultados)
   - Desejos (Explícitos → Implícitos → Transformação → Status)
   - Conexões (Dor→Desejo, Dúvida→Bloqueio)
   - Síntese (3 Maiores Descobertas)
   - Aplicações (Copy, Conteúdo, Argumentos)

### Controle do Usuário

O usuário decide o ritmo:

| Comando | Ação |
|---------|------|
| "faz todas as dores" | Preenche as 4 categorias de Dores |
| "começa pelas dores emocionais" | Preenche só Dores Emocionais |
| "faz o 3D completo" | Preenche todas as seções sequencialmente |
| "agora as dúvidas" | Avança para seção de Dúvidas |
| "pula para síntese" | Vai direto para Síntese |
| "gera a matriz de intensidade" | Cria matriz/tabela específica |

### Entrega e Inserção no Notion

Após cada seção:

1. **Entregar** conteúdo formatado em Markdown (compatível Notion)
2. **Perguntar:** "Quer ajustar algo antes de inserir no Notion?"
3. **Aguardar** indicação de onde inserir (URL ou nome da página)
4. **Inserir** via MCP Notion
5. **Confirmar:** "Inserido. Próxima seção?"

### Perguntas Interativas

Se material insuficiente para uma seção:

1. **Informar:** "Para preencher [seção] com qualidade, preciso de mais informações sobre [aspecto específico]"
2. **Perguntar** de forma específica (não genérica)
3. **Aguardar** resposta antes de preencher
4. **Nunca inventar** dados não fornecidos

Se materiais apresentarem informações conflitantes:

1. **Informar:** "Encontrei informações conflitantes sobre [aspecto]: Material A diz X, Material B diz Y"
2. **Perguntar:** "Qual versão devo considerar?"
3. **Aguardar** resposta antes de preencher

---

## Estrutura do Framework 3D

### 😰 DORES (O que incomoda e precisa ser aliviado)

**4 Categorias:**

1. **Físicas/Tangíveis:** Problemas práticos, desconforto físico, processos difíceis
2. **Emocionais/Psicológicas:** Sentimentos negativos, ansiedade, vergonha, autoestima
3. **Financeiras:** Gastos sem resultado, custo de oportunidade, medo de investir errado
4. **Sociais/Relacionais:** Impacto em relacionamentos, julgamentos, oportunidades perdidas

**Para cada categoria:** Lista de dores + Intensidade (Baixa/Média/Alta/Insuportável)

### ❓ DÚVIDAS (O que paralisa e precisa ser esclarecido)

**4 Categorias:**

1. **Sobre o Produto/Serviço:** Funcionamento, segurança, diferencial, eficácia
2. **Sobre Si Mesmo:** Capacidade, disciplina, adequação ao tratamento
3. **Sobre o Processo:** Passo a passo, tempo, complexidade, erros
4. **Sobre Resultados:** Prazo, permanência, garantia, expectativa

**Para cada categoria:** Lista de dúvidas + Criticidade (Baixa/Média/Alta/Bloqueadora)

### ✨ DESEJOS (O que move e precisa ser alcançado)

**4 Categorias:**

1. **Explícitos (Conscientes):** O que dizem querer abertamente
2. **Implícitos (Subconscientes):** Motivações profundas não verbalizadas
3. **De Transformação:** Quem querem se tornar, mudança de identidade
4. **De Status:** Como querem ser vistos, imagem projetada

**Para cada categoria:** Lista de desejos + Força (Fraco/Moderado/Forte/Obsessivo)

### 🔄 CONEXÕES (sob demanda)

- **Dor → Desejo:** Cada dor tem um desejo oposto correspondente
- **Dúvida → Bloqueio:** Cada dúvida bloqueia um desejo específico

### 📈 SÍNTESE (sob demanda)

- Maior Dor Identificada (com impacto e contexto)
- Maior Dúvida Bloqueadora (com análise do medo por trás)
- Maior Desejo Motivador (com força e manifestação)
- Insights Cruzados e Narrativa Completa

### 💡 APLICAÇÕES (sob demanda)

- Headlines baseadas em Dores
- Headlines baseadas em Desejos
- Respostas para Dúvidas (FAQ/Objeções)
- Estratégia de Conteúdo por estágio
- Argumentos de Venda

---

## Regras de Qualidade

### ✅ FAZER:

1. **Profundidade específica:** Insights não-óbvios, viscerais, contextualizados
2. **Concisão:** Cada item denso em significado, sem enrolação
3. **Linguagem do cliente:** Usar termos e expressões reais do público
4. **Acionabilidade:** Todo insight deve ser aplicável em campanhas/criativos
5. **Conexão emocional:** Tocar nas motivações profundas, não superficiais
6. **Extended thinking:** SEMPRE usar para análise antes de preencher

### ❌ NÃO FAZER:

1. **Inventar:** Nunca criar dados, depoimentos ou insights sem base nos materiais
2. **Genericidade:** Evitar frases que servem para qualquer produto/público
3. **Repetição:** Não duplicar informações entre seções
4. **Extensão desnecessária:** Não encher linguiça para parecer completo
5. **Preencher sem material:** Se faltar info, perguntar antes

### 📏 Padrão de Formato:

- **4-8 itens por categoria**, priorizando qualidade sobre quantidade
- Cada item: frase completa e específica, não genérica
- Intensidade/Criticidade/Força: sempre indicar
- Matrizes e tabelas: só quando solicitadas

---

## Referências

Consultar arquivos em `references/`:

- **exemplo-qualidade.md** - Padrão de profundidade e formato esperado
- **estrutura-3d.md** - Estrutura completa com perguntas orientadoras

---

## Formato de Output para Notion

Usar Notion-flavored Markdown:

**Callouts:**
```
<callout icon="🎯" color="purple_bg">
  Conteúdo do callout
</callout>
```

**Tabelas:**
```
<table header-row="true">
<tr>
<td>Coluna 1</td>
<td>Coluna 2</td>
</tr>
<tr>
<td>Dado 1</td>
<td>Dado 2</td>
</tr>
</table>
```

**Toggles:** Usar `▶` no início + conteúdo indentado

**Outros:** `---` para separadores, `☑️`/`⬜` para checks

---

## Checklist Interno

Antes de entregar cada seção, verificar:

- [ ] Usei extended thinking para analisar materiais?
- [ ] Conteúdo é específico para este tratamento/público?
- [ ] Evitei linguagem genérica de marketing?
- [ ] Cada item é acionável para campanhas?
- [ ] Não repeti informações de outras seções?
- [ ] Intensidade/Criticidade/Força está indicada?
- [ ] Número de itens está entre 4-8 por categoria?
- [ ] Não inventei nada além do que está nos materiais?
