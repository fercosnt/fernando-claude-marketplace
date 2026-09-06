# Principios de Engenharia de Contexto para CLAUDE.md

Compilado de 60+ fontes: documentacao oficial Anthropic, blog posts, showcases e gists reais.

## 1. Concisao Acima de Tudo

LLMs frontier seguem ~150-200 instrucoes com consistencia razoavel. O system prompt do Claude Code consome ~50 instrucoes. Isso deixa ~100-150 para o CLAUDE.md.

**Teste definitivo**: "Remover esta linha faria Claude cometer erros?" Se NAO, corte.

**Tamanhos recomendados:**

| Categoria | Linhas |
|-----------|--------|
| Ideal | 50-80 |
| Aceitavel | < 200 |
| Maximo | < 300 (com .claude/rules/) |
| Refatorar | > 300 |

Acima de 80 linhas, Claude comeca a ignorar partes. Performance degrada uniformemente (nao so as ultimas instrucoes).

## 2. Positive Framing

Estudos da comunidade mostram que inverter negacoes para positivas reduz violacoes pela metade.

**Por que funciona**: LLMs ativam o conceito independente do "nao". Ao dizer "nao use semicolons", o conceito "semicolons" fica ativado.

Exemplos de conversao:

| Negacao | Positive framing |
|---------|-----------------|
| "Do NOT use semicolons" | "Use no-semicolon style" |
| "NUNCA use any" | "Use tipos explicitos em todas as funcoes" |
| "NAO use CSS customizado" | "Use apenas classes Tailwind para estilos" |
| "NUNCA use CommonJS" | "Use ES modules (import/export) em todo o projeto" |
| "NAO faca queries pesadas" | "Leia dados de tabelas pre-calculadas para dashboards" |

## 3. Bias de Posicionamento

LLMs dao mais atencao ao INICIO e FIM do prompt:

- **Primeiras 5 linhas**: regras mais criticas (REGRAS INVIOLAVEIS)
- **Ultimas linhas**: checklist de verificacao, gotchas criticos
- **Meio**: regras de menor prioridade

## 4. Bullet Points > Paragrafos

Instrucoes em formato de bullet point tem ~40% mais chance de serem seguidas vs paragrafos longos. Usar listas sempre que possivel.

## 5. Especificidade > Generalidade

Instrucoes vagas sao ignoradas. Instrucoes concretas e verificaveis sao seguidas.

| Vago (ignorado) | Especifico (seguido) |
|-----------------|---------------------|
| "Formate o codigo corretamente" | "Use 2 espacos de indentacao" |
| "Escreva codigo limpo" | "Use ES modules (import/export), nunca CommonJS" |
| "Siga boas praticas" | "TypeScript strict mode, sem tipos any" |
| "Teste adequadamente" | "Rode `npm test` apos cada mudanca. Coverage minimo: 80%" |

## 6. Motivacao > Imposicao

Explicar WHY junto com a regra. Claude generaliza melhor quando entende a razao:

```markdown
# Bom (com motivacao)
- Valores monetarios: DECIMAL(12,2) — float causa erros de arredondamento em calculos financeiros
- RLS ativo em TODAS as tabelas multi-tenant — isolamento no banco, nao no codigo

# Ruim (imposicao sem razao)
- IMPORTANTE: SEMPRE use DECIMAL(12,2) para valores monetarios
- NUNCA esqueca de ativar RLS
```

## 7. Framework WHY-WHAT-HOW

Organizar CLAUDE.md em tres blocos:

1. **WHY** (1-2 linhas): Qual o proposito do projeto? Que problema resolve?
2. **WHAT** (bulk): Stack, arquitetura, padroes, constraints
3. **HOW** (final): Comandos, workflows, verificacao

## 8. Forma Imperativa

Instrucoes verbosas diluem a atencao. Forma imperativa e mais eficaz e consome menos tokens:

- Ruim: "Por favor, o desenvolvedor deve garantir que o codigo esteja formatado..."
- Bom: "Formatacao: Prettier padrao"

## 9. "Prefer X over Y"

Mais confiavel que "Do not use Y":

- "Prefer named exports over default exports"
- "Prefer Server Components over client components"
- "Prefer Supabase client over raw SQL"

## 10. Funcao Cognitiva por Secao

| Secao | Funcao | Exemplo |
|-------|--------|---------|
| Comandos | Memoria Procedural | `npm test -- --watch --coverage` |
| Arquitetura | Modelo Mental | "Backend: Supabase. Frontend: App Router." |
| Estilo | Restricoes Sintaticas | "TypeScript Strict. Named exports." |
| Workflow | Governanca | "Novas tabelas: 1. Migration. 2. RLS. 3. Types." |
| Glossario | Desambiguacao | "User = Paciente. Session = Consulta." |

## 11. CLAUDE.md e User Message, NAO System Prompt

CLAUDE.md e injetado como mensagem de usuario APOS o system prompt. Implicacoes:

- Instrucoes de personalidade/tom sao ignoradas (system prompt governa)
- Instrucoes de estilo de raciocinio ("pense passo a passo") nao funcionam
- Funciona melhor para regras especificas, aditivas, no nivel do projeto
- NAO tente sobrescrever comportamento core do Claude

## 12. O Que INCLUIR vs EXCLUIR

### INCLUIR (Claude NAO consegue inferir)

| Categoria | Exemplos |
|-----------|----------|
| Comandos Bash especificos | `npm run test:e2e -- --headed`, `npx supabase db reset` |
| Regras que diferem do padrao | "Named exports apenas", "ES modules, nunca CommonJS" |
| Decisoes arquiteturais | "Multi-tenancy via RLS, nao filtro de aplicacao" |
| Quirks do ambiente | "PORT 3000 ja usado, use 3001" |
| Gotchas nao-obvios | "Supabase RLS exige SECURITY DEFINER" |
| Glossario de dominio | "User = Paciente. Session = Consulta." |
| Constraints de negocio | "Valores monetarios: DECIMAL(12,2)" |

### EXCLUIR (Claude JA sabe ou linter resolve)

| Categoria | Motivo |
|-----------|--------|
| Convencoes padrao | Claude ja conhece PEP 8, ESLint defaults |
| Regras de estilo detalhadas | Prettier/ESLint + hooks |
| Documentacao de API | Linke com @, nao copie |
| Descricoes arquivo-por-arquivo | Claude pode ler o codigo |
| Info que muda frequentemente | Fica desatualizada |
| Personalidade/tom | System prompt governa |
| Snippets de codigo | Ficam desatualizados — use @references |

## 13. Hierarquia de Carregamento

| Nivel | Localizacao | Carregamento |
|-------|-------------|-------------|
| Enterprise Policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Automatico, imutavel |
| User Global | `~/.claude/CLAUDE.md` | Automatico |
| User Rules | `~/.claude/rules/*.md` | Automatico |
| Project Root | `./CLAUDE.md` | Automatico |
| Project Rules | `./.claude/rules/*.md` | Automatico (sem paths) ou sob demanda (com paths) |
| Subdirectory | `./subdir/CLAUDE.md` | Sob demanda |

Resolucao de conflitos: mais especifico vence.

## 14. Progressive Disclosure

Nao diga ao Claude tudo que ele PODERIA precisar. Diga como ENCONTRAR informacao quando precisar.

```
Sempre carregado (CLAUDE.md ~80 linhas)
  └── Auto-carregado (.claude/rules/)
       └── Sob demanda (.claude/rules/ com paths:)
            └── Sob demanda (.claude/skills/)
                 └── Referenciado com @ (docs/, migrations/)
```

## 15. CLAUDE.local.md esta Deprecated

Recomendacao oficial: usar @imports para arquivos pessoais no home directory:

```markdown
# No CLAUDE.md do projeto
@~/.claude/my-project-overrides.md
```

Funciona melhor com git worktrees.

## 16. Path-Scoped Rules

Rules em `.claude/rules/` suportam YAML frontmatter com globs:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Rules
- Todos os endpoints incluem validacao de input
```

Carregam apenas quando Claude trabalha com arquivos que matcham o pattern.

## 17. Manutencao

**Frequencia de revisao:**
- A cada 2-4 semanas: revisao com Claude
- A cada mudanca arquitetural: atualizar na mesma PR
- Quando Claude erra repetidamente: adicionar regra
- Quando Claude faz algo certo sem instrucao: REMOVER a regra redundante

**Ciclo virtuoso:**
```
Claude erra → adicionar regra → Claude nao repete
Claude segue sem instrucao → remover regra → CLAUDE.md mais conciso
```
