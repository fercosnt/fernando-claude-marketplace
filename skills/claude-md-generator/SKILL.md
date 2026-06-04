---
name: claude-md-generator
description: Cria ou melhora CLAUDE.md + estrutura .claude/ completa. Use ao iniciar projeto, configurar Claude Code, melhorar CLAUDE.md, ou mencionar "CLAUDE.md", "setup do projeto".
intent: >
  CLAUDE.md e o unico mecanismo de contexto persistente entre sessoes do Claude Code.
  Sem ele, voce repete instrucoes a cada conversa. Esta skill aplica pesquisa de 60+ fontes
  (documentacao oficial Anthropic, blog posts, showcases, gists reais) para gerar CLAUDE.md
  otimizado e toda a infraestrutura .claude/ necessaria. Foco no stack padrao de Fernando
  (Next.js + Supabase + TypeScript + Tailwind + n8n + @beautysmile/design-system).
---

# Claude MD Generator

Gera ou melhora CLAUDE.md e a estrutura completa `.claude/` para projetos, aplicando melhores praticas de engenharia de contexto.

## Deteccao de Modo

Antes de comecar, detecte o modo de operacao:

| Modo | Sinal | Fluxo |
|------|-------|-------|
| **Criar** | Projeto novo, sem CLAUDE.md, "iniciar projeto", "setup" | Entrevista -> Gerar tudo |
| **Melhorar** | CLAUDE.md existe, "melhorar", "revisar", "atualizar" | Auditar -> Diagnosticar -> Corrigir |

Confirme: "Vou [criar/melhorar] o CLAUDE.md. Certo?"

---

## Modo Criar: Gerar do Zero

### Passo 1: Entrevista Rapida

Colete apenas o que NAO da para inferir do codigo:

1. **O que e o projeto?** (uma frase)
2. **Stack principal?** (framework, banco, deploy) — se nao informar, assumir stack padrao
3. **Tem multi-tenancy?** Se sim, qual coluna de tenant?
4. **Automacao?** (n8n, cron, webhooks)
5. **Algo que Claude erra frequentemente?** (gotchas)

Se o usuario ja forneceu contexto suficiente na conversa, pule perguntas redundantes.

### Passo 2: Explorar o Projeto

Se ja existe codigo:
- Ler `package.json` para stack e comandos
- Ler estrutura de diretorios (`ls` nos principais)
- Verificar `supabase/migrations/` para schema SQL
- Verificar `.env.example` para variaveis
- Verificar `tsconfig.json` para config TypeScript
- Ler qualquer README existente

### Passo 3: Gerar CLAUDE.md

Aplicar os principios abaixo na geracao. O CLAUDE.md deve ter **50-80 linhas** (maximo absoluto: 200). Ver [references/principios.md](references/principios.md) para detalhes.

**Estrutura obrigatoria (nesta ordem):**

```markdown
# [Nome do Projeto]

[Uma frase: o que e, stack, problema que resolve]
Stack: [stack]

## REGRAS INVIOLAVEIS
[3-7 constraints criticas — as mais importantes primeiro]

## Comandos Essenciais
[dev, build, test, lint, db — copy-paste ready]

## Arquitetura
[5-10 linhas de estrutura de diretorios, apenas niveis relevantes]

## Code Style
[APENAS o que linter NAO cobre e difere do padrao]

## [Secao Especifica do Dominio]
[Ex: Supabase, Auth, Multi-tenancy — so se relevante]

## Gotchas
[Comportamentos nao-obvios que causam bugs]

## Verificacao Antes de Concluir
[Checklist para Claude validar antes de considerar tarefa completa]
```

### Passo 4: Gerar Estrutura .claude/

Criar os arquivos complementares:

```
.claude/
├── settings.json          # Permissoes do time
├── rules/                 # Regras auto-carregadas por topico
│   ├── sql-conventions.md # Se usa banco de dados
│   └── security.md        # Regras de seguranca
└── commands/              # Slash commands uteis
    └── review.md          # Code review rapido
```

**Rules files** — mover para ca tudo que exceder o limite de 80 linhas do CLAUDE.md. Cada rule file deve ter **um topico** e ser conciso.

**Rules com path-scoping** — usar YAML frontmatter para carregar condicionalmente:

```yaml
---
paths:
  - "supabase/migrations/**/*.sql"
---
```

### Passo 5: Gerar MEMORY.md (se aplicavel)

Se o projeto e novo, criar `MEMORY.md` inicial com ponteiros para memorias relevantes. Manter como indice puro (links + descricoes de 1 linha).

### Passo 6: Gerar .gitignore entries

Garantir que `.gitignore` inclua:
```
.claude/settings.local.json
CLAUDE.local.md
.env
.env.*
```

---

## Modo Melhorar: Auditar e Corrigir

### Passo 1: Ler CLAUDE.md Existente

Ler o arquivo completo e todos os arquivos em `.claude/rules/`.

### Passo 2: Diagnosticar

Avaliar contra os criterios de qualidade (ver [references/quality-criteria.md](references/quality-criteria.md)):

| Criterio | Peso | Verificacao |
|----------|------|-------------|
| Tamanho | Alto | < 80 linhas ideal, < 200 aceitavel, > 300 refatorar |
| Comandos | Alto | Build/test/dev/lint presentes e funcionais? |
| Regras criticas no topo | Alto | Primeiras 5 linhas = regras mais importantes? |
| Checklist no final | Alto | Bias de recencia — gotchas/verificacao no fim? |
| Positive framing | Medio | Negacoes convertidas para positivo? |
| Bullet points | Medio | Formato de lista vs paragrafos? |
| Specificidade | Medio | Instrucoes concretas e verificaveis? |
| Sem linter work | Medio | Zero regras que linter/formatter cobrem? |
| Sem snippets | Medio | Zero codigo copiado (usar @references)? |
| Sem personalidade | Baixo | Zero instrucoes de tom/personalidade? |
| Progressive disclosure | Medio | Info detalhada em rules/skills, nao no CLAUDE.md? |

### Passo 3: Gerar Relatorio

```markdown
## Diagnostico CLAUDE.md

**Score: XX/100 (Grade: X)**
**Linhas: XX (alvo: 50-80)**

### Problemas Encontrados
1. [problema] — [impacto] — [solucao]

### Melhorias Sugeridas
1. [melhoria] — [por que ajuda]

### Acoes Recomendadas
- [ ] [acao concreta 1]
- [ ] [acao concreta 2]
```

### Passo 4: Aplicar Correcoes

Apos aprovacao do usuario, aplicar mudancas com Edit tool. Preservar conteudo existente que esta bom.

---

## Principios de Engenharia de Contexto

Estes principios governam TODA geracao. Ver [references/principios.md](references/principios.md) para detalhes completos.

### Concisao (Principio #1)

> "Para cada linha, pergunte: 'Remover isso causaria Claude a cometer erros?' Se nao, corte."

- LLMs seguem ~150-200 instrucoes com consistencia. System prompt do Claude Code consome ~50.
- Isso deixa ~100-150 instrucoes uteis para CLAUDE.md.
- Performance degrada UNIFORMEMENTE conforme instrucoes aumentam.

### Positive Framing (Principio #2)

Reduz violacoes pela metade vs negacoes:

| Negacao (evitar) | Positive framing (usar) |
|------------------|-------------------------|
| "NUNCA use any" | "Use tipos explicitos em todas as funcoes" |
| "NAO use CSS customizado" | "Use apenas classes Tailwind para estilos" |
| "NUNCA use CommonJS" | "Use ES modules (import/export) em todo o projeto" |

### Bias de Posicionamento (Principio #3)

- **Primeiras 5 linhas**: regras mais criticas (REGRAS INVIOLAVEIS)
- **Ultimas 5 linhas**: checklist de verificacao / gotchas criticos
- **Meio**: regras de menor prioridade

### Bullet Points > Paragrafos (Principio #4)

Bullet points tem ~40% mais chance de serem seguidos vs paragrafos longos.

### Especificidade > Generalidade (Principio #5)

| Ruim | Bom |
|------|-----|
| "Formate o codigo corretamente" | "Use 2 espacos de indentacao" |
| "Escreva codigo limpo" | "Use ES modules (import/export), nunca CommonJS" |
| "Siga boas praticas" | "TypeScript strict mode, sem tipos any" |

### Motivacao > Imposicao (Principio #6)

Explicar o WHY junto com a regra. Claude generaliza melhor quando entende a razao:

```markdown
# Bom
- Valores monetarios: DECIMAL(12,2) — float causa erros de arredondamento em calculos financeiros

# Ruim
- IMPORTANTE: SEMPRE use DECIMAL(12,2) para valores monetarios
```

---

## Stack Padrao (Default)

Quando o usuario nao especificar stack, assumir:

| Camada | Tecnologia |
|--------|-----------|
| Framework | Next.js 14+ (App Router) |
| Linguagem | TypeScript (strict mode) |
| UI | @beautysmile/design-system + Tailwind CSS |
| Componentes base | Radix UI |
| Auth | Supabase Auth (Email + Senha) |
| Banco | Supabase PostgreSQL |
| Multi-tenancy | Row Level Security (RLS) |
| Graficos | Recharts |
| Validacao | Zod + React Hook Form |
| Icons | Lucide React |
| Deploy | Vercel |
| Automacao | n8n (self-hosted) |
| Notificacoes | Telegram via n8n |
| Testes | Jest + Testing Library + Playwright |

Ver [references/stack-padrao.md](references/stack-padrao.md) para detalhes de cada tecnologia.

---

## O Que INCLUIR vs EXCLUIR

### INCLUIR (Claude NAO consegue inferir)

- Comandos Bash especificos do projeto
- Regras que DIFEREM do padrao da linguagem
- Decisoes arquiteturais nao-obvias
- Quirks do ambiente
- Gotchas que causam bugs
- Glossario de dominio
- Constraints de negocio

### EXCLUIR (Claude JA sabe ou linter resolve)

- Convencoes padrao da linguagem
- Regras de estilo detalhadas (Prettier/ESLint cobrem)
- Documentacao de API (usar @references)
- Descricoes arquivo-por-arquivo
- Info que muda frequentemente
- Instrucoes de personalidade/tom
- Snippets de codigo (ficam desatualizados)

---

## Anti-Patterns a Evitar

| Anti-Pattern | Problema | Solucao |
|--------------|----------|---------|
| Kitchen Sink | Tudo no CLAUDE.md | < 80 linhas + .claude/rules/ + skills |
| LLM como Linter | Regras de estilo | Prettier/ESLint + hooks |
| /init sem curar | Generico demais | Curar cada linha |
| Negacao excessiva | "NUNCA X" repetido | Positive framing |
| @import massivo | Docs grandes always-loaded | Referencia lazy |
| Snippets de codigo | Ficam desatualizados | @references |
| Personality override | "Be a senior engineer" | System prompt governa |

---

## Progressive Disclosure

Organizar informacao em camadas:

```
Sempre carregado (CLAUDE.md ~80 linhas)
  └── Auto-carregado (.claude/rules/ — sem paths:)
       └── Sob demanda (.claude/rules/ — com paths:)
            └── Sob demanda (.claude/skills/)
                 └── Referenciado com @ (docs/, migrations/)
```

Regra: se a informacao e necessaria em TODA sessao, vai no CLAUDE.md. Se e necessaria apenas ao trabalhar com certo tipo de arquivo, vai em rules com path-scoping. Se e conhecimento especializado, vai em skills.

---

## Arquivos de Referencia

Para detalhes que nao precisam estar no contexto principal:

- [references/principios.md](references/principios.md) — Principios completos de engenharia de contexto
- [references/quality-criteria.md](references/quality-criteria.md) — Criterios de qualidade e scoring
- [references/stack-padrao.md](references/stack-padrao.md) — Stack tecnologico padrao detalhado
- [references/templates-por-tipo.md](references/templates-por-tipo.md) — Templates para 10 tipos de projeto
