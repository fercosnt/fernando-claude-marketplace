# Criterios de Qualidade para CLAUDE.md

## Scoring (100 pontos)

| Criterio | Peso | O Que Avaliar |
|----------|------|--------------|
| Comandos documentados | 15 | Build, test, dev, lint, db presentes e copy-paste ready? |
| Arquitetura clara | 15 | Claude entende a estrutura do projeto? 5-10 linhas max? |
| Regras criticas no topo | 15 | Primeiras 5 linhas = constraints mais importantes? |
| Concisao | 15 | < 80 linhas ideal? Sem informacao redundante? |
| Gotchas documentados | 10 | Comportamentos nao-obvios que previnem bugs? |
| Checklist de verificacao | 10 | Lista no final para Claude validar seu trabalho? |
| Positive framing | 5 | Negacoes convertidas para formato positivo? |
| Bullet points | 5 | Formato de lista vs paragrafos longos? |
| Sem linter work | 5 | Zero regras que linter/formatter cobrem? |
| Progressive disclosure | 5 | Info detalhada em rules/skills, nao inflando o CLAUDE.md? |

## Grades

| Grade | Score | Descricao |
|-------|-------|-----------|
| A | 90-100 | Otimo — conciso, acionavel, bem estruturado |
| B | 70-89 | Bom — cobertura adequada, gaps menores |
| C | 50-69 | Basico — faltam secoes importantes |
| D | 30-49 | Fraco — incompleto ou verboso |
| F | 0-29 | Ausente ou inutilizavel |

## Red Flags (Descontar Pontos)

| Red Flag | Penalidade | Motivo |
|----------|-----------|--------|
| > 300 linhas | -20 | Claude ignora partes |
| Snippets de codigo no CLAUDE.md | -10 | Ficam desatualizados |
| Regras de estilo que linter cobre | -10 | LLM nao deve fazer trabalho de linter |
| Instrucoes de personalidade | -5 | System prompt governa |
| Paragrafos longos em vez de bullets | -5 | 40% menos seguidos |
| Negacoes excessivas (5+ "NUNCA") | -5 | Positive framing e mais eficaz |
| Secrets/credenciais | -30 | Risco de seguranca critico |
| @import de arquivos grandes | -10 | Inflam contexto desnecessariamente |

## Checklist Rapido

### Estrutura
- [ ] Nome + descricao + stack nas primeiras linhas
- [ ] Regras criticas logo apos (bias de primazia)
- [ ] Comandos essenciais copy-paste ready
- [ ] Arquitetura em 5-10 linhas
- [ ] Code style APENAS o que linter nao cobre
- [ ] Gotchas documentados
- [ ] Checklist de verificacao no final (bias de recencia)

### Qualidade
- [ ] < 80 linhas (ideal) ou < 200 (aceitavel)
- [ ] Bullet points em vez de paragrafos
- [ ] Positive framing em vez de negacoes
- [ ] Cada regra tem WHY explicito
- [ ] Instrucoes especificas e verificaveis
- [ ] Zero snippets de codigo (usar @references)
- [ ] Zero regras de estilo cobertas por linter
- [ ] Zero secrets ou credenciais

### Infraestrutura
- [ ] `.claude/settings.json` com permissoes do time
- [ ] `.claude/rules/` para regras detalhadas por topico
- [ ] `.gitignore` inclui `.claude/settings.local.json` e `CLAUDE.local.md`
- [ ] @references para docs detalhados (nao inline)
