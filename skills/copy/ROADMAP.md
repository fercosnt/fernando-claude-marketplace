# Copy Skill — Roadmap

## v1 (atual) — Instalada 2026-04-01

**Status:** Funcional, testada, 100% pass rate (20/20 assertions), +40% vs baseline.

**O que tem:**
- SKILL.md principal (~280 linhas) com fluxo de geracao completo
- 10 references: frameworks-core, frameworks-avancados, 5 formatos, hooks-banco, voice-cloning, anti-patterns
- Frameworks embarcados: AIDA, PAS, BAB, PULSE, SAGE, SCQA, TAS, 4Ps, 4Us, CopyBoarding (6 passos), CPPB, PASTOR, Schwartz (5 niveis), 5 Objecoes Universais, Promessas Poderosas (5 tipos), 10 Perguntas Chaves, Liminal Thinking, Sofisticacao de Mercado
- Voice cloning com workflow de 5 passos + bloqueio de cliches
- 3 evals com 20 assertions

**Fontes:** 35+ fontes web (deep-research) + 3 notebooks NotebookLM (pesquisa, formacao copy Andre Cia, IA+Copy Andre Cia)

---

## v1.1 — Enriquecimento de Conteudo

**Status:** Concluida 2026-04-01. Instalada em ~/.claude/skills/copy/.

### Tarefas

- [x] Sintetizar curso IA+Copy — Tecnicas por formato (Modulo 2) extraidas via NotebookLM e integradas em frameworks-avancados.md
  - Modulo 3 parcialmente extraido (paginas de captura, lancamento ao vivo) em v1.1
  - Modulo 4 (Empresario da Copy) — conteudo de negocios, nao de copy. Descartado.
- [x] Extrair frameworks da formacao copy via NotebookLM:
  - Carta de Vendas (42 passos) ✓
  - Video de Vendas / VSL (26 passos) ✓
  - Pagina de Vendas (9 blocos + mapa CTAs) ✓
  - Palavras Gravidas (conceito + exemplos + tecnica de desengravidamento) ✓
  - Gerador de Clareza (4 etapas + exemplos) ✓
- [x] Extrair PDFs faltantes da formacao copy via NotebookLM
  - CopyBoarding PDF = template em branco (7 campos). Conteudo pratico ja extraido dos audios. Adicionada nota de processo Pre-CopyBoarding (post-its) em frameworks-avancados.md
  - Perguntas Chaves PDF = formulario em branco (10 perguntas). Versao expandida ja extraida do audio M2.6
  - Avatar Material de Apoio = novo reference `avatar-briefing.md` (9 campos, pesquisa invisivel, mineracao dados)
  - Carta de Vendas exemplo real = padroes praticos adicionados em `formatos-vendas.md` (adaptacao por ticket, FAQ como trator, provas logicas vs emocionais)
  - Paginas de Captura (M3.2-3.3) = novo reference `formatos-vendas.md` (3 blocos recompensa, 5 blocos lancamento)
  - Lancamento ao Vivo (M3.8-3.12) = estrutura completa em `formatos-vendas.md` (Causa, 4 aulas, pitch 14 passos, disparos WhatsApp)
- [x] Enriquecer `references/frameworks-avancados.md` com estruturas de vendas + Insights Transversais
- [x] Expandir AI-tell database: novo `references/ai-tells-database.md` com 140+ substituicoes em 16 categorias
  - Organizado por contexto: texto, video, thumbnail, plataforma (TikTok, LinkedIn, Reddit, Email)
  - Fonte: create-viral-content (aaaronmiller)
- [x] Expandir `references/anti-patterns.md` com 5 passes adversariais + hooks avancados (Tribal Identity Split, etc.) + stats
- [x] Expandir `references/hooks-banco.md` com 5 novas categorias (Story, Value/How-To, Question, Relatable, Timely) + limites por plataforma + checklist de verificacao
  - Fonte: social-ai-team (stevenflanagan1)
- [x] Rodar evals: 20/20 assertions (100% pass rate) — 3 test cases (carrossel, reel, legenda storytelling)

---

## v2 — Features Novas + Integracao NotebookLM

**Status:** Concluida 2026-04-01. Instalada em ~/.claude/skills/copy/.

### Tarefas

- [x] Adversarial Passes: 3 criticos (O Cetico, O Scroller, O Editor) integrados no fluxo antes da entrega
- [x] Analise de Copy Existente: modo reverso `/copy analisar [post]` com breakdown estrutural
- [x] NotebookLM Integration: `references/notebooks.json` com config de 3 notebooks como RAG opcional
- [x] project-context.md: auto-inject de brand/voice profile, elimina perguntas repetitivas
- [x] Quick Mode: `/copy rapido [tema]` pula CopyBoarding e adversarial para legendas simples
- [x] Platform Benchmarks: `references/benchmarks.md` com ER, horarios, tamanhos por plataforma
- [x] Novos Formatos: `references/formato-linkedin.md`, `formato-tiktok.md`, `formato-newsletter.md`
- [x] Serializacao com Open Loops: `/copy serie [tema]` gera series conectadas com open/close loops
- [x] Matriz de selecao expandida: 8 formatos (adicionados LinkedIn, TikTok, Newsletter)
- [x] 4 modos de uso documentados: /copy, /copy analisar, /copy rapido, /copy serie

---

### Detalhes de Implementacao (referencia)

#### Adversarial Passes (inspirado em create-viral-content)

Adicionar etapa de validacao com 3 criticos nomeados ANTES de entregar a copy:

| Critico | O que avalia | Exemplo de feedback |
|---------|-------------|-------------------|
| **O Cetico** | Promessas fracas, claims sem prova, logica furada | "Slide 3 afirma '3x mais alcance' sem dado — adicionar fonte ou remover" |
| **O Scroller** | Hook fraco, retencao, pattern interrupts | "Hook atual e informativo mas nao para scroll — testar versao contrarian" |
| **O Editor** | Cliches de IA, tom sintetico, redundancia | "Frase 'jornada de transformacao' no slide 5 — substituir por linguagem real" |

Fluxo: Gerar copy → rodar 3 criticos → corrigir → entregar.

#### Analise de Copy Existente (modo reverso)

Novo modo: usuario cola um post que performou bem → skill analisa:
- Qual framework foi usado (AIDA, PAS, BAB, etc.)
- Qual tipo de hook (curiosity gap, contrarian, numbered list)
- Nivel de Schwartz do publico
- Por que funcionou (breakdown estrutural)
- Como replicar o padrao em outros temas

Invocacao: `/copy analisar [colar post ou URL]`

#### NotebookLM Integration (consulta opcional como RAG)

**Arquivo de config:** `references/notebooks.json`

```json
{
  "enabled": true,
  "notebooks": {
    "pesquisa": {
      "id": "cb5704d8-123a-4f60-b692-b1bb45bdca0d",
      "description": "35+ fontes de pesquisa sobre copy para redes sociais",
      "use_when": "Precisa de dados, estatisticas ou tendencias atualizadas"
    },
    "formacao_copy": {
      "id": "89aaef0b-0577-4a42-b576-a8f49f1d9b3d",
      "description": "Curso Formacao Copywriter Andre Cia — CopyBoarding, Schwartz, CPPB, PASTOR, 42 passos carta de vendas",
      "use_when": "Precisa de detalhes profundos de frameworks avancados que excedem o reference local"
    },
    "ia_copy": {
      "id": "fb5f80d7-b67f-4a6c-926b-fd7edf21d149",
      "description": "Curso Metodo CIA 2.0 — tecnicas de IA para copy, voice cloning, programacao de prompts por formato",
      "use_when": "Precisa de tecnicas especificas de geracao de copy com IA ou templates do Metodo CIA"
    }
  }
}
```

**Comportamento:**
- Se `enabled: true` e NotebookLM autenticado → skill consulta notebook relevante quando reference local nao tem profundidade suficiente
- Se `enabled: false` ou nao autenticado → usa references locais normalmente (fallback transparente)
- Consulta via: `notebooklm ask "pergunta" --notebook <id> --json`
- Cache: respostas do NotebookLM podem ser salvas como notes no notebook para consultas futuras mais rapidas

**Casos de uso:**
1. Usuario pede framework que nao esta completo nos references (ex: "usa o modelo de 42 passos da carta de vendas do Andre Cia") → consulta notebook formacao_copy
2. Voice cloning avancado com exemplos do curso → consulta notebook ia_copy
3. Dados de benchmark ou tendencia especifica → consulta notebook pesquisa

#### project-context.md (inspirado em kostja94/marketing-skills)

Padronizar voice profile + contexto de marca num arquivo auto-injetado:

```
references/project-context.md

## Brand
- Nome: [marca]
- Nicho: [nicho]
- Tom: [descricao]
- Publico: [avatar resumido]

## Voice Profile
- Formalidade: [1-5]
- Humor: [tipo + frequencia]
- Vocabulario: [palavras que usa / palavras proibidas]
- Emojis: [quais + onde]

## Plataformas Ativas
- Instagram: [sim/nao] — foco em [formatos]
- LinkedIn: [sim/nao]
- TikTok: [sim/nao]
```

Skill carrega automaticamente se existir. Substitui perguntas do fluxo de coleta de contexto.

#### Quick Mode

Modo rapido para legendas simples sem workflow completo:

Invocacao: `/copy rapido [tema]` ou `/copy r [tema]`

Pula: deteccao de formato (assume legenda), coleta de contexto (usa project-context.md), CopyBoarding, adversarial passes.
Mantem: selecao de framework, 3 hooks, checklist basico, bloqueio de cliches.

#### Platform Benchmarks

Novo reference: `references/benchmarks.md`

| Plataforma | ER medio | ER excelente | Formato dominante |
|-----------|----------|-------------|-------------------|
| Instagram Feed | 1.22% | >6% | Carrosseis |
| Instagram Reels | 0.50% | >3% | Video curto |
| TikTok | 5.96% | >15% | Video curto |
| LinkedIn | 2.0% | >5% | Posts longos + carrosseis |
| Facebook | 0.07% | >1% | Video |
| Twitter/X | 0.05% | >0.5% | Thread |

Engagement monetization: Like $0.50, Comment $2.00, Share $5.00, Save $3.00.

#### Novos Formatos

- `references/formato-linkedin.md` — posts longos, tom de autoridade, carrosseis PDF
- `references/formato-tiktok.md` — ousadia, irreverencia, velocidade, sem formalidade
- `references/formato-newsletter.md` — subject line, preview text, estrutura de email

#### Serializacao com Open Loops

Modo de geracao de series conectadas (3-5 posts):
- Post 1 faz promessa nao resolvida → Post 2 resolve e abre nova → Post 3 resolve e fecha
- Cada post funciona standalone mas conecta com os outros
- Alcance cumulativo: engajamento de um alimenta alcance do proximo

---

## Fontes de Referencia (repos pesquisados)

| Repo | O que aproveitar | Para versao |
|------|-----------------|-------------|
| [social-ai-team](https://github.com/stevenflanagan1/social-ai-team) | Hook library (40+ formulas), Visual Direction field, file-based state machine | v1.1 (hooks), v2 (visual direction) |
| [create-viral-content](https://github.com/aaaronmiller/create-viral-content) | 6 adversarial passes, AI-tell database (100+ substituicoes), Tribal Identity Split hook | v1.1 (AI-tells), v2 (adversarial passes) |
| [ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) | Quick mode (60s snapshot), parallel subagent audit, PDF reports | v2 (quick mode) |
| [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) | project-context.md auto-inject, "skip intro" shortcuts, breadth de templates | v2 (project-context) |
| [social-media-analyzer](https://github.com/alirezarezvani/claude-skills) | Platform benchmarks (ER/CTR), engagement monetization ($0.50-$5.00), confidence tagging | v2 (benchmarks) |
