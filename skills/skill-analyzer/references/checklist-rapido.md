# Checklist Rapido — 10 Pontos de Verificacao

## Quando Usar

Use este checklist para avaliacao rapida de skills quando:
- Precisa de uma primeira impressao em < 5 minutos
- Quer validar melhorias apos iteracao
- Nao precisa de analise completa com scores detalhados

## Interpretacao

| Resultado | Classificacao | Acao |
|-----------|---------------|------|
| 9-10 OK | Aprovada | Pronta para uso |
| 7-8 OK | Ajustes menores | Corrigir itens FALHA e usar |
| 5-6 OK | Revisao necessaria | Analise completa recomendada |
| < 5 OK | Revisao major | Analise completa obrigatoria |

---

## Os 10 Pontos

### 1. Frontmatter Valido

**O que verificar:** Arquivo comeca com bloco YAML valido contendo `name` e `description`.

**Criterio OK:**
- Bloco `---` no inicio e fim do frontmatter
- Campo `name` presente, kebab-case, sem espacos
- Campo `description` presente, < 1024 caracteres
- YAML valido (sem erros de sintaxe)

**Criterio FALHA:**
- Frontmatter ausente ou malformado
- name ou description faltando
- description > 1024 caracteres

---

### 2. Description Aciona Corretamente

**O que verificar:** Description lista triggers (quando usar), nao workflow (o que faz).

**Criterio OK:**
- Description contem verbos que o usuario usaria ("analisar", "criar", "revisar")
- Cobre pelo menos 3 sinonimos do trigger principal
- Frase "Ativar quando..." ou equivalente presente
- Testando 5 formas diferentes de pedir a funcionalidade, >= 3 acionariam

**Criterio FALHA:**
- Description descreve workflow ("Executa 7 passos...")
- Faltam sinonimos obvios
- Apenas jargao tecnico sem termos coloquiais

---

### 3. Tamanho Adequado

**O que verificar:** SKILL.md dentro do range saudavel com conteudo pesado em references.

**Criterio OK:**
- SKILL.md < 500 linhas
- Se > 300 linhas, conteudo pesado esta em references
- Sem repeticao de conteudo entre SKILL.md e references
- Cada linha justifica seu custo em tokens

**Criterio FALHA:**
- SKILL.md > 500 linhas sem references
- SKILL.md > 800 linhas (penalidade no scorecard)
- Conteudo pesado inline que deveria ser reference

---

### 4. Forma Imperativa

**O que verificar:** Instrucoes usam forma imperativa direta.

**Criterio OK:**
- >= 80% das instrucoes em forma imperativa ("Faca X", "Leia Y", "Avalie Z")
- Voz ativa predominante
- Tom consistente ao longo da skill

**Criterio FALHA:**
- Predominancia de voz passiva ("Deve ser feito", "Os arquivos sao lidos")
- Linguagem condicional excessiva ("Voce poderia talvez considerar...")
- Tom inconsistente (alterna entre formal e informal)

---

### 5. Instrucoes com PORQUE

**O que verificar:** Instrucoes incluem justificativa (Context > Configuration).

**Criterio OK:**
- >= 70% das instrucoes com justificativa explicitada
- Numeros arbitrarios justificados ("max 3 — porque...")
- Principios priorizados sobre numeros fixos

**Criterio FALHA:**
- < 50% das instrucoes com justificativa
- Numeros sem explicacao (por que 5 e nao 4 ou 6?)
- Regras arbitrarias sem contexto

---

### 6. Progressive Disclosure

**O que verificar:** Conteudo pesado esta em references, nao inline no SKILL.md.

**Criterio OK:**
- SKILL.md contem workflow e instrucoes essenciais
- References contem detalhamento, rubricas, catalogos, templates
- Cada reference tem proposito claro e nome descritivo
- SKILL.md referencia explicitamente os references ("Consulte `references/X`")

**Criterio FALHA:**
- Todo conteudo no SKILL.md sem references
- References existem mas nao sao referenciados
- Conteudo duplicado entre SKILL.md e references
- Arquivos orfaos sem referencia

---

### 7. Workflow Completo

**O que verificar:** Skill define workflow de inicio a fim com passos acionaveis.

**Criterio OK:**
- Primeiro passo claro (o que fazer quando ativada)
- Passos sequenciais com acoes definidas
- Transicoes entre passos explicitas
- Passo final com entrega definida
- Deteccao de modo se skill tem multiplos modos

**Criterio FALHA:**
- Sem workflow identificavel
- Passos vagos ("analisar o conteudo")
- Sem passo de entrega final
- Modos existem mas sem deteccao automatica

---

### 8. Exemplos Concretos

**O que verificar:** Pelo menos 1 exemplo concreto e completo (nao placeholder).

**Criterio OK:**
- Pelo menos 1 exemplo com dados reais (nao "[placeholder]")
- Exemplo demonstra o padrao esperado de output
- Se skill tem multiplos modos, pelo menos 1 exemplo por modo principal
- Exemplos anotados explicando por que sao bons (bonus)

**Criterio FALHA:**
- Sem exemplos em skill que claramente precisa
- Apenas placeholders genericos ("[insira aqui]")
- Exemplos irrelevantes ou desatualizados

---

### 9. Anti-Patterns / Guardas

**O que verificar:** Skill inclui instrucoes negativas e mecanismos de verificacao.

**Criterio OK:**
- DO: Instrucoes positivas presentes
- DON'T: Anti-patterns nomeados (o que NAO fazer)
- VERIFY: Mecanismo de verificacao de qualidade (bonus para score alto)
- Anti-patterns tem justificativa

**Criterio FALHA:**
- Apenas instrucoes positivas, nenhuma guarda
- Anti-patterns obvios do dominio nao mencionados
- Sem qualquer mecanismo de verificacao

---

### 10. Consistencia Interna

**O que verificar:** Skill pratica o que prega. Sem contradicoes.

**Criterio OK:**
- Estrutura da skill segue as regras que ensina
- Terminologia consistente em todos os arquivos
- Cross-references validos (arquivos referenciados existem)
- Sem contradicoes entre secoes

**Criterio FALHA:**
- Hipocrisia: ensina X mas faz Y
- Cross-references quebrados
- Contradicoes entre secoes
- Terminologia inconsistente

---

## Template de Resultado Rapido

```
CHECKLIST RAPIDO: [nome-da-skill]
Data: [YYYY-MM-DD]

 1. Frontmatter valido:          [OK/FALHA] — [nota breve]
 2. Description aciona:          [OK/FALHA] — [nota breve]
 3. Tamanho adequado:            [OK/FALHA] — [N linhas SKILL.md]
 4. Forma imperativa:            [OK/FALHA] — [nota breve]
 5. Instrucoes com PORQUE:       [OK/FALHA] — [~N% com justificativa]
 6. Progressive disclosure:      [OK/FALHA] — [N references]
 7. Workflow completo:            [OK/FALHA] — [nota breve]
 8. Exemplos concretos:          [OK/FALHA] — [N exemplos]
 9. Anti-patterns/guardas:       [OK/FALHA] — [DO/DON'T/VERIFY?]
10. Consistencia interna:        [OK/FALHA] — [nota breve]

RESULTADO: [N]/10 OK — [Classificacao]

TOP 3 MELHORIAS:
1. [Melhoria mais impactante]
2. [Segunda melhoria]
3. [Terceira melhoria]
```
