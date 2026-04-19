# legal-analyzer

Plugin de analise contratual brasileira para Claude Code. Reune um coordenador mestre + 9 skills especializadas que aceleram a triagem de contratos de compras, servicos, locacao, engenharia e NDAs, aplicando verificacao numerica automatica, classificacao tricolor (GREEN/YELLOW/RED) e protocolo de playbook.

> **Aviso Legal:** Este plugin auxilia na revisao contratual mas NAO constitui parecer juridico. Sempre consulte um advogado qualificado antes de tomar decisoes juridicas vinculantes.

## O que tem dentro

### Coordenador (auto-trigger)
- **coordenador-legal** — Regras transversais (disclaimer, verificacao numerica das 7 regras, tricolor, playbook protocol) e roteamento para a skill especialista correta. Ativa automaticamente em qualquer trabalho contratual.

### 9 Skills especializadas
| Skill | Quando ativa |
|-------|--------------|
| **revisar-contrato** | Revisao clausula por clausula, checklist legal, deteccao de inconsistencias numericas |
| **triagem-nda** | Triagem rapida de NDAs em 10 dimensoes (detecta non-compete embutido) |
| **compliance** | Checklist LGPD (7 itens) + conformidade com Codigo Civil |
| **avaliacao-risco** | Matriz 5x5 severidade x probabilidade com memo estruturado |
| **briefing** | Briefings juridicos (topico/incidente/diario) |
| **briefing-reuniao** | Preparacao pre-reuniao e captura de action items pos-reuniao |
| **checar-fornecedor** | Status de fornecedor, gaps documentais, timeline de vencimentos |
| **resposta-juridica** | Templates de respostas formais + gatilhos de escalacao |
| **assinatura** | Checklist pre-assinatura, consistencia corpo x anexos, testemunhas BR |

### Recursos compartilhados
- `references/` — Checklists por tipo de contrato (compras, servicos, locacao, engenharia), LGPD, red flags, legislacao base
- `assets/` — Playbook `legal.local.md` exemplo + templates de relatorio/memo/perguntas
- `skills/*/evals/` — Casos de teste para cada skill

## Instalacao (dev local)

```bash
# 1. Adicionar o marketplace local
/plugin marketplace add "/Users/fernando/Cursor Repo/Skill Prompt/plugins/legal-analyzer"

# 2. Instalar o plugin
/plugin install legal-analyzer@legal-analyzer-dev

# 3. Reiniciar Claude Code (obrigatorio apos instalacao)
```

Teste rapido sem instalar:
```bash
claude --plugin-dir "/Users/fernando/Cursor Repo/Skill Prompt/plugins/legal-analyzer"
```

Hot-reload apos edicoes:
```bash
/reload-plugins
```

## Como usar

O coordenador ativa automaticamente quando voce menciona contrato/clausula/NDA/fornecedor/compliance/assinatura. Exemplos:

```
Analisa esse contrato de servicos: [cola texto]
```
→ Ativa `coordenador-legal` + `revisar-contrato`

```
Esse NDA ta ok? [cola texto]
```
→ Ativa `coordenador-legal` + `triagem-nda`

```
Checklist pre-assinatura pra esse contrato
```
→ Ativa `coordenador-legal` + `assinatura`

## Playbook da empresa

Para aplicar posicoes personalizadas (em vez dos defaults brasileiros), coloque um arquivo `legal.local.md` no contexto da conversa ou no project knowledge. Veja exemplo em `assets/legal.local.md`.

## Estrutura

```
legal-analyzer/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── coordenador-legal/
│   ├── revisar-contrato/
│   ├── triagem-nda/
│   ├── compliance/
│   ├── avaliacao-risco/
│   ├── briefing/
│   ├── briefing-reuniao/
│   ├── checar-fornecedor/
│   ├── resposta-juridica/
│   └── assinatura/
├── references/
├── assets/
└── README.md
```

## Jurisdicao

Brasil — Codigo Civil 2002, LGPD 13.709/2018, Lei 8.245/91 (locacao), CDC 8.078/90. Portugues brasileiro em todas as saidas.

## Versao

0.1.0 — primeiro release local (2026-04-19)
