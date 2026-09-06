# fernando-claude-marketplace

Marketplace pessoal de plugins e skills para Claude Code e Cowork (Claude Desktop agent mode).

O repositorio guarda dois tipos de artefato:

- **Plugins** — instalaveis via marketplace (`/plugin install`). Ficam em pastas-plugin na raiz.
- **Skills avulsas** — ficam em [`skills/`](./skills/) e sao instaladas por copia manual (nao viram plugin).

## Instalacao

### Plugins — Claude Code (CLI)

```bash
# Adicionar o marketplace
/plugin marketplace add fercosnt/fernando-claude-marketplace

# Listar plugins disponiveis
/plugin marketplace list fernando-claude-marketplace

# Instalar um plugin
/plugin install deck-builder@fernando-claude-marketplace

# Reinicie o Claude Code apos instalar
```

### Plugins — Cowork (Claude Desktop agent mode)

Settings → Plugins → **Install from GitHub** → `fercosnt/fernando-claude-marketplace`, depois selecione o plugin na lista.

### Skills avulsas — copia manual

Skills nao sao instaladas pelo marketplace; copie a pasta para o destino:

```bash
# Claude Code
cp -r skills/<nome>/ ~/.claude/skills/<nome>/

# Claude Desktop (Cowork)
cp -r skills/<nome>/ "~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<sessao>/skills/<nome>/"
```

Skills com `scripts/` (ex.: `deep-research`, `presentation-text-extractor`) trazem `requirements.txt` — recrie o `.venv` localmente (o ambiente virtual nao e versionado).

## Plugins disponiveis

| Plugin | Descricao | Skills | Versao |
|--------|-----------|--------|--------|
| [deck-builder](./deck-builder/) | STORYBOARD de apresentacoes em 8 verticais + 2 auxiliares + orquestrador. Entry: `/deck`. Auto-detect de marca, NotebookLM-aware | 11 | 1.2.0 |
| [legal-analyzer](./legal-analyzer/) | Analise contratual BR — coordenador + 9 skills (revisar, NDA, LGPD, risco, briefings, fornecedor, resposta, assinatura) | 10 | 0.1.0 |
| [skill-prd](./skill-prd/) | Criacao, validacao e melhoria de PRDs estruturados — 4 modos, 3 niveis, scorecard 5D, Deep Modules, vertical slicing (tracer bullets) | 1 | 0.3.0 |
| [fotona-design-system](./fotona-design-system/) | Design system da Fotona Brasil — os dois registros da marca (claro de produto, escuro de marca), tokens, logo, fontes, 14 componentes, 9 arquetipos de slide, 7 formatos de post e prompts de imagem | 1 | 1.0.0 |

## Skills avulsas

Em [`skills/`](./skills/) — instalacao por copia manual.

### Criacao de skills, plugins e prompts
| Skill | Descricao |
|-------|-----------|
| [idea-to-brief](./skills/idea-to-brief/) | Transforma ideias em briefs estruturados com pesquisa automatica |
| [grill-me](./skills/grill-me/) | Entrevista 1-pergunta-por-vez antes do PRD (Matt Pocock) |
| [skill-creator](./skills/skill-creator/) | Cria, melhora e avalia skills (com evals) |
| [skill-analyzer](./skills/skill-analyzer/) | Avalia qualquer skill com scorecard de 4 dimensoes |
| [plugin-builder](./skills/plugin-builder/) | Constroi plugins para Claude Code e Cowork |
| [prompt-engineer](./skills/prompt-engineer/) | Cria, melhora e analisa prompts (tecnicas Anthropic) |
| [claude-md-generator](./skills/claude-md-generator/) | Cria/melhora CLAUDE.md + estrutura .claude/ |

### Pesquisa e conhecimento
| Skill | Descricao |
|-------|-----------|
| [deep-research](./skills/deep-research/) | Pesquisa profunda com subagentes paralelos + sync NotebookLM |
| [notebook-source-auditor](./skills/notebook-source-auditor/) | Reconcilia NotebookLM com manifesto e pesquisas |
| [knowledge-optimizer](./skills/knowledge-optimizer/) | Transforma conteudo em base RAG-otimizada |
| [presentation-text-extractor](./skills/presentation-text-extractor/) | Extrai texto de PDFs de apresentacoes (OCR hibrido) |

### Conteudo e marketing
| Skill | Descricao |
|-------|-----------|
| [copy](./skills/copy/) | Copy profissional para redes sociais (frameworks reais) |
| [social-media-strategist](./skills/social-media-strategist/) | Estrategia de conteudo e calendario editorial |
| [press-release-writer](./skills/press-release-writer/) | Press releases e titulos jornalisticos |
| [elevenlabs-formatter](./skills/elevenlabs-formatter/) | Formata scripts para ElevenLabs TTS |

### GoHighLevel
| Skill | Descricao |
|-------|-----------|
| [ghl-sdr-chatbot-builder](./skills/ghl-sdr-chatbot-builder/) | Chatbot SDR no GoHighLevel Conversation AI |
| [ghl-workflow-expert](./skills/ghl-workflow-expert/) | Analisa, cria e otimiza workflows GoHighLevel |

### Produtividade e nicho
| Skill | Descricao |
|-------|-----------|
| [handoff](./skills/handoff/) | Compacta conversa em handoff doc para outro agente (Matt Pocock) |
| [laser-physics](./skills/laser-physics/) | Calculos de fisica do laser + dosimetria (odontologia) |

### Beauty Smile / business
| Skill | Descricao |
|-------|-----------|
| [beauty-smile-design-system](./skills/beauty-smile-design-system/) | Design system Beauty Smile (cores, tipografia, componentes, logos) |
| [skill-cenografia](./skills/skill-cenografia/) | Equipe criativa (ARCHI/DECOR/VISION) para eventos e stands |
| [framework-3d-filler](./skills/framework-3d-filler/) | Preenche Framework 3D (Dores, Duvidas, Desejos) |
| [framework-tratamento-filler](./skills/framework-tratamento-filler/) | Preenche Framework de Tratamento (7 secoes) |
| [mapa-empatia-filler](./skills/mapa-empatia-filler/) | Preenche Mapa da Empatia (6 quadrantes) |
| [matriz-implicacao-filler](./skills/matriz-implicacao-filler/) | Preenche Matriz de Implicacao (SPIN Selling) |
| [objecoes-filler](./skills/objecoes-filler/) | Preenche Framework de Objecoes (14-20 objecoes) |
| [icp-framework-builder](./skills/icp-framework-builder/) | Estrategista de ICP para frameworks estruturados |

## Estrutura

```
fernando-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # Lista os PLUGINS (skills avulsas nao entram aqui)
├── deck-builder/               # Plugin (11 skills + shared/ + templates/)
├── legal-analyzer/             # Plugin (10 skills + references/)
├── skill-prd/                  # Plugin (1 skill)
├── skills/                     # Skills avulsas (copia manual, nao viram plugin)
│   ├── idea-to-brief/
│   ├── deep-research/
│   └── ... (27 skills)
└── README.md
```

**Convencao:** o que ja e plugin fica plugin (instalavel via marketplace); o que e skill avulsa fica em `skills/` e e instalado por copia manual — nao e transformado em plugin.

## Licenca

Uso pessoal / interno. Skills contem conhecimento proprietario (playbooks juridicos, frameworks de conteudo, design system) — nao redistribuir sem autorizacao.
