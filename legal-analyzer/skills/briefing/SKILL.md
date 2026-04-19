---
name: briefing
description: Gera briefings juridicos contextuais sobre temas legais, incidentes e pendencias de projeto. Usar sempre que o usuario pedir briefing juridico, resumo de legislacao, analise de incidente legal, panorama de pendencias contratuais, ou quiser entender rapidamente um tema juridico. Tambem ativar quando mencionar "briefing", "resumo juridico", "o que diz a lei sobre", "incidente", "pendencias do projeto", "prazos contratuais", ou qualquer pedido de contextualizacao juridica rapida — mesmo que nao use a palavra "briefing" explicitamente.
---

# Briefing Juridico Contextual

Skill para gerar briefings juridicos rapidos e acionaveis em 3 modos distintos. Cada modo atende um cenario diferente do dia a dia de quem trabalha com contratos e compras.

## Jurisdicao e idioma

- Jurisdicao: Brasil (legislacao federal)
- Idioma: portugues brasileiro, sempre
- Citacoes legais: apenas artigos reais — nunca inventar referencia legislativa

## Modos de uso

### 1. `/briefing topico [query]`

Pesquisa e sintetiza um tema juridico especifico. Ideal para quando o usuario precisa entender rapidamente um assunto antes de tomar uma decisao ou ir a uma reuniao.

**Fluxo:**

1. Receber o topico do usuario
2. Pesquisar na web (WebSearch) por:
   - Legislacao aplicavel (leis, decretos, regulamentos)
   - Jurisprudencia recente relevante (STF, STJ, TRTs)
   - Doutrina e artigos especializados
   - Posicionamentos de orgaos reguladores (ANPD, CADE, etc.)
3. Consultar `references/legislacao-base.md` para artigos-chave relacionados
4. Sintetizar em briefing estruturado

**Formato de saida:**

```
# Briefing: [Topico]
Data: [data atual]

## Resumo Executivo
[2-3 paragrafos com o essencial do tema]

## Legislacao Aplicavel
| Lei/Norma | Artigos | Relevancia |
|-----------|---------|------------|
| [lei]     | [arts.] | [por que importa] |

## Jurisprudencia Relevante
- [Tribunal, numero, data]: [sintese do entendimento]

## Implicacoes Praticas
- [Como isso afeta contratos e operacoes do usuario]

## Riscos e Pontos de Atencao
- [O que pode dar errado se ignorado]

## Next Steps
- [ ] [Acao concreta 1 com responsavel sugerido]
- [ ] [Acao concreta 2]
- [ ] [Acao concreta 3]

## Fontes
- [Links e referencias consultadas]

---
⚠️ Este briefing nao constitui parecer juridico. Para decisoes criticas, consulte um advogado.
```

### 2. `/briefing incidente [situacao]`

Resposta rapida a um incidente ou situacao juridica urgente. Foco em obrigacoes imediatas e proximos passos concretos.

**Fluxo:**

1. Receber descricao da situacao/incidente
2. Identificar:
   - Tipo de incidente (contratual, regulatorio, trabalhista, LGPD, etc.)
   - Partes envolvidas
   - Urgencia e prazos legais aplicaveis
3. Consultar `references/legislacao-base.md` para obrigacoes legais
4. Se envolver dados pessoais, verificar obrigacoes LGPD (notificacao ANPD em 72h, etc.)
5. Mapear contratos potencialmente afetados
6. Gerar briefing de resposta

**Formato de saida:**

```
# Briefing de Incidente
Data: [data atual]
Severidade: [CRITICA / ALTA / MEDIA / BAIXA]

## Situacao
[Resumo objetivo do incidente reportado]

## Classificacao
- Tipo: [contratual / regulatorio / LGPD / trabalhista / outro]
- Urgencia: [imediata / 24h / 72h / 7 dias / 30 dias]
- Prazo legal: [se houver prazo legal obrigatorio, citar com artigo]

## Obrigacoes Imediatas
1. [Obrigacao com prazo e base legal]
2. [Obrigacao com prazo e base legal]

## Contratos Potencialmente Afetados
- [Tipo de contrato]: [como pode ser impactado]
- [Tipo de contrato]: [clausulas relevantes a verificar]

## Riscos se Nao Agir
- [Consequencia juridica com base legal]
- [Consequencia financeira estimada se possivel]

## Next Steps
- [ ] URGENTE: [acao imediata — quem, o que, ate quando]
- [ ] [Acao de curto prazo]
- [ ] [Acao de medio prazo]
- [ ] Consultar advogado sobre: [pontos especificos]

---
⚠️ Este briefing nao constitui parecer juridico. Em incidentes criticos, acione imediatamente seu departamento juridico ou advogado externo.
```

### 3. `/briefing diario`

Panorama de pendencias e prazos do projeto. Consolida o que precisa de atencao no dia.

**Fluxo:**

1. Verificar contexto disponivel:
   - Conversas anteriores na sessao
   - Arquivos do projeto mencionados
   - Contratos em analise recente
2. Identificar:
   - Prazos proximos (vencimentos, renovacoes, notificacoes)
   - Pendencias abertas (respostas aguardadas, documentos faltantes)
   - Riscos identificados em analises anteriores ainda nao resolvidos
3. Se nao houver contexto suficiente, perguntar ao usuario:
   - "Quais contratos estao em andamento?"
   - "Ha prazos proximos que devo considerar?"
   - "Alguma pendencia aberta com fornecedores?"
4. Gerar briefing consolidado

**Formato de saida:**

```
# Briefing Diario
Data: [data atual]

## Prazos Proximos
| Prazo | Contrato/Assunto | Acao Necessaria | Status |
|-------|-----------------|-----------------|--------|
| [data] | [descricao] | [o que fazer] | [pendente/em andamento] |

## Pendencias Abertas
- [Pendencia 1]: [status e proximo passo]
- [Pendencia 2]: [status e proximo passo]

## Alertas
- 🔴 [Item critico que precisa de acao hoje]
- 🟡 [Item que precisa de atencao esta semana]

## Next Steps para Hoje
- [ ] [Acao prioritaria 1]
- [ ] [Acao prioritaria 2]
- [ ] [Acao prioritaria 3]

---
⚠️ Este briefing nao constitui parecer juridico. Para decisoes criticas, consulte um advogado.
```

## Diretrizes gerais

### Pesquisa web
- Modo **topico**: pesquisa web ATIVADA — buscar legislacao, jurisprudencia e doutrina atualizada
- Modo **incidente**: pesquisa web quando necessario para confirmar prazos legais ou obrigacoes regulatorias
- Modo **diario**: sem pesquisa web — foco no contexto local do projeto

### Classificacao de severidade (modo incidente)
- **CRITICA**: prazo legal imediato, risco de sancao, exposicao criminal
- **ALTA**: prazo legal em ate 72h, risco financeiro significativo
- **MEDIA**: prazo em ate 30 dias, risco controlavel
- **BAIXA**: sem prazo legal iminente, risco mitigavel

### Citacoes legais
Citar apenas legislacao real e vigente. Artigos-chave por area:
- Contratos gerais: CC/2002 arts. 104, 421-422, 441-443, 473, 476, 478-480
- LGPD: Lei 13.709/2018 arts. 5, 7, 46-49, 52-54
- Locacao: Lei 8.245/1991 arts. 22-26, 51, 54-57
- Consumidor: CDC arts. 39, 46, 51
- Engenharia: CC arts. 593-626

Na duvida sobre um artigo especifico, consultar `references/legislacao-base.md` antes de citar.

### Qualidade do output
- Next steps sempre concretos e acionaveis — nunca generico como "avaliar a situacao"
- Prazos legais sempre com base legal explicita
- Quando nao souber algo com certeza, dizer explicitamente e recomendar verificacao
- Manter tom profissional mas acessivel — o usuario nao e advogado

### Disclaimer
Todo briefing deve terminar com disclaimer de que nao constitui parecer juridico. Isso e obrigatorio e inegociavel.
