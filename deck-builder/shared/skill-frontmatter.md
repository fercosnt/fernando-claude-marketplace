# §10.7 Frontmatter Padrão SKILL.md

> Contrato LOCKED — todas as 11 skills usam o mesmo formato de frontmatter.
> Chaves no topo do frontmatter fora do spec Agent Skills fazem o upload para claude.ai/Cowork **falhar com erro** (`Unexpected key(s) in SKILL.md frontmatter`). Por isso as convenções internas do plugin (`intent`, `nb_ids`, `references`, `assets`) vivem dentro de `metadata:` — o único campo livre do spec. Atualizado em 2026-09-29.

## Template

```yaml
---
name: deck-{vertical}
description: >-
  {1-2 frases — quando ativa + o que faz}
effort: high            # low / medium / high / xhigh / max (extensao do Claude Code)
metadata:
  intent: action        # ou knowledge / orchestration
  nb_ids:
    - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da   # NB1 Core (sempre)
    - {NB2 ou NB3 conforme vertical}
  references:
    - references/framework-{vertical}.md
    - references/eval-cases-{vertical}.md
  assets:
    - assets/templates/storyboard-skeleton.md
    - assets/checklists/{vertical}-checklist.md
---
```

## Campos obrigatórios (Anthropic spec)

- `name` — slug kebab-case, único, igual ao nome do diretório
- `description` — terceira pessoa, "Use quando..." + lista de trigger phrases. **Sempre como bloco `>-`**: texto com `: ` (ex.: "Triggers: paper") numa linha plain e YAML invalido — o Claude Code tolera, mas validadores estritos (upload claude.ai, Cowork) falham

## Campos opcionais

| Campo | Tipo | Quando usar |
|-------|------|-------------|
| `metadata.intent` | `action` / `knowledge` / `orchestration` | Sempre (convenção do plugin; não afeta discovery) |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` | Extensão do Claude Code — sobrepõe o effort da sessão |
| `context` | string | Domain hint (raramente necessário) |
| `agent` | string | Skill exposta como agente |
| `hooks` | array | Hooks específicos da skill |
| `disable-model-invocation` | bool | Skill só via slash command |
| `user-invocable` | bool | Aparece em `/<slash-name>` |
| `allowed-tools` | array | Whitelist de ferramentas |

**`metadata.nb_ids`, `metadata.references`, `metadata.assets`** são convenção interna do plugin (não são lidos pela Anthropic, mas documentam dependências).

## Intent por skill do plugin

| Skill | `metadata.intent` |
|-------|----------|
| `deck-orchestrator` | `orchestration` (único — entry point) |
| `deck-fundraising` / `deck-sales` / `deck-clinical` / `deck-equipment` / `deck-teaching` / `deck-proposal` / `deck-scientific` / `deck-internal` | `action` |
| `deck-image-prompts` / `deck-reviewer` | `action` |

## Effort por skill

| Skill | `effort` |
|-------|----------|
| Todas 8 verticais + orchestrator | `high` |
| Auxiliares (`deck-image-prompts`, `deck-reviewer`) | `medium` |

## Description — checklist (combate undertriggering)

A description é o que decide se a skill é invocada. Cheque:

- [ ] Terceira pessoa (não "I will...")
- [ ] Começa com "Use when..." ou "Quando..."
- [ ] Lista 4-6 trigger phrases concretas
- [ ] Menciona Big Idea, U1-U6 ou STORYBOARD
- [ ] Distingue da skill irmã mais próxima (ex: deck-sales vs deck-equipment)

## Cross-references

- `entrevista-universal-u1-u6.md` — sempre referenciada na description
- `nb-query-template.md` — `nb_ids:` declarado segue esse formato
- `fronteiras-explicitas.md` — `description` deve declarar o que NÃO faz
