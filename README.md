# fernando-claude-marketplace

Marketplace pessoal de plugins e skills para Claude Code e Cowork (Claude Desktop agent mode).

## Instalacao

### Claude Code (CLI)

```bash
# Adicionar o marketplace
/plugin marketplace add fercosnt/fernando-claude-marketplace

# Listar plugins disponiveis
/plugin marketplace list fernando-claude-marketplace

# Instalar um plugin
/plugin install legal-analyzer@fernando-claude-marketplace

# Reinicie o Claude Code apos instalar
```

### Cowork (Claude Desktop agent mode)

Settings → Plugins → **Install from GitHub** → `fercosnt/fernando-claude-marketplace`

Depois selecione `legal-analyzer` (ou outros plugins) na lista.

## Plugins disponiveis

| Plugin | Descricao | Skills | Versao |
|--------|-----------|--------|--------|
| [legal-analyzer](./legal-analyzer/) | Analise contratual BR — coordenador + 9 skills (revisar, NDA, LGPD, risco, briefings, fornecedor, resposta, assinatura) | 10 | 0.1.0 |

## Roadmap

Fase 2 (proximos):
- `content-suite` — social-media-strategist + copy + elevenlabs-formatter + press-release-writer
- `gsd-essentials` — core do workflow GSD empacotado
- `claude-md-generator` — skill standalone como plugin
- `idea-to-brief` — skill standalone como plugin
- `deep-research` — skill standalone como plugin

## Estrutura

```
claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # Lista todos os plugins
├── legal-analyzer/             # Plugin completo
│   ├── .claude-plugin/plugin.json
│   ├── skills/ (10)
│   ├── references/
│   ├── assets/
│   └── README.md
└── README.md
```

**Convencao:** toda entrada no marketplace e um plugin — mesmo skills standalone viram plugins minimalistas com uma unica skill. Isso padroniza instalacao, versionamento e distribuicao.

## Desenvolvimento local (antes de push)

```bash
# Testar localmente a partir do clone (apos pushar)
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install legal-analyzer@fernando-claude-marketplace
# Restart Claude Code
```

## Licenca

Uso pessoal / interno. Skills contem conhecimento proprietario (playbooks juridicos, frameworks de conteudo) — nao redistribuir sem autorizacao.
