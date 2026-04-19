---
name: briefing-reuniao
description: Prepara briefings estruturados para reunioes juridicas e de negociacao contratual, e captura action items pos-reuniao. Usar sempre que o usuario mencionar reuniao juridica, preparacao para reuniao de contrato, briefing pre-reuniao, negociacao contratual, revisao de termos com fornecedor, pauta de reuniao legal, ou quiser se preparar para qualquer encontro que envolva discussao de contratos, clausulas ou termos comerciais. Tambem ativar quando o usuario pedir para registrar decisoes, atas, follow-ups ou action items apos uma reuniao de natureza juridica ou contratual — mesmo sem usar a palavra "briefing".
---

# Briefing de Reuniao Juridica

Skill para preparar reunioes de negociacao contratual e revisao de termos, e para capturar action items pos-reuniao de forma estruturada. O foco e dar ao usuario — que nao e advogado — um mapa claro do que discutir, onde ceder, onde nao ceder, e o que registrar depois.

## Jurisdicao e idioma

- Jurisdicao: Brasil (legislacao federal)
- Idioma: portugues brasileiro, sempre
- Citacoes legais: apenas artigos reais — nunca inventar referencia legislativa

## Modos de uso

A skill opera em dois modos complementares:

### 1. Modo Pre-Reuniao: `/briefing-reuniao preparar`

Gera um briefing completo para o usuario se preparar antes de uma reuniao de negociacao contratual ou revisao de termos.

**Fluxo:**

1. Perguntar ao usuario (preencher o que faltar):
   - Qual o objetivo da reuniao?
   - Quem participa? (nomes, cargos, empresa)
   - Qual contrato/acordo sera discutido?
   - Ha historico relevante? (reunioes anteriores, pendencias, conflitos)
   - O usuario tem o contrato ou minuta? (se sim, pedir para colar/anexar)
2. Se houver contrato fornecido, analisar rapidamente os pontos criticos (clausulas RED/YELLOW)
3. Consultar `references/legislacao-base.md` para fundamentacao dos pontos-chave
4. Gerar briefing estruturado

**Formato de saida:**

```
# Briefing Pre-Reuniao
Data da reuniao: [data informada ou a definir]
Preparado em: [data atual]

## Objetivo da Reuniao
[Resumo claro do que se pretende atingir — ex: "Negociar termos do contrato de prestacao de servicos com Fornecedor X"]

## Mapa de Participantes
| Nome | Cargo/Funcao | Empresa | Papel na reuniao |
|------|-------------|---------|-----------------|
| [nome] | [cargo] | [empresa] | [decisor / tecnico / observador] |

**Dinamica esperada:** [Quem decide? Quem pode travar? Quem e aliado?]

## Documentos-Chave
- [Contrato/minuta em discussao — versao e data]
- [Aditivos anteriores, se houver]
- [Propostas comerciais, emails relevantes]
- [Atas de reunioes anteriores]

## Contexto e Historico
[Resumo do relacionamento ate aqui: como chegamos a esta reuniao, o que ja foi acordado, o que esta pendente]

## Pauta Sugerida
1. [Topico 1 — breve descricao]
2. [Topico 2 — breve descricao]
3. [Topico 3 — breve descricao]

## Pontos-Chave para Discussao

### [Ponto 1: ex. Prazo de entrega]
- **Situacao atual:** [o que o contrato/minuta diz]
- **Risco:** [por que este ponto e importante — com base legal se aplicavel]
- **Posicao recomendada:** [o que o usuario deveria buscar]
- **Margem de concessao:** [ate onde pode ceder sem risco critico]

### [Ponto 2: ex. Clausula penal]
[mesma estrutura]

### [Ponto N]
[mesma estrutura]

## Consideracoes Juridicas
- [Artigos de lei relevantes para os pontos em discussao — ex: CC art. 412 sobre clausula penal]
- [Jurisprudencia relevante se conhecida]
- [Limitacoes legais que restringem margem de negociacao]

## Red Lines (linhas inegociaveis)
Pontos que NAO devem ser cedidos porque criam risco juridico ou financeiro critico:
- [Red line 1 — com justificativa legal]
- [Red line 2 — com justificativa legal]

## Talking Points
Frases e argumentos prontos para usar na reuniao:
- Para [ponto X]: "[argumento sugerido]"
- Para [ponto Y]: "[argumento sugerido]"
- Se a outra parte pressionar sobre [Z]: "[resposta sugerida]"

## Perguntas a Levantar
Questoes que o usuario deve fazer durante a reuniao:
1. [Pergunta sobre ponto aberto ou ambiguo]
2. [Pergunta sobre prazo/condicao nao esclarecida]
3. [Pergunta sobre responsabilidades]

## Decisoes Necessarias
Lista de decisoes que precisam sair desta reuniao:
- [ ] [Decisao 1 — ex: aprovar ou rejeitar prazo de 90 dias]
- [ ] [Decisao 2 — ex: aceitar ou contrapropor indice de reajuste]

## Follow-ups de Reunioes Anteriores
[Se o usuario informou historico, listar pendencias de reunioes passadas que devem ser cobradas nesta]
- [Follow-up 1 — status]
- [Follow-up 2 — status]

---
Este briefing nao constitui parecer juridico. Para decisoes criticas, consulte um advogado.
```

### 2. Modo Pos-Reuniao: `/briefing-reuniao registrar`

Captura decisoes e action items apos a reuniao. O usuario pode descrever o que aconteceu em texto livre — a skill organiza e estrutura.

**Fluxo:**

1. Perguntar ao usuario (ou extrair do texto fornecido):
   - O que foi decidido?
   - Quais acoes ficaram pendentes?
   - Quem ficou responsavel por cada acao?
   - Quais prazos foram definidos?
   - Houve pontos nao resolvidos que precisam de nova reuniao?
2. Se o usuario fornecer texto corrido ou notas informais, extrair e organizar as informacoes
3. Classificar prioridade dos action items
4. Gerar registro estruturado

**Formato de saida:**

```
# Registro Pos-Reuniao
Data da reuniao: [data]
Registrado em: [data atual]

## Participantes
| Nome | Cargo/Funcao | Empresa |
|------|-------------|---------|
| [nome] | [cargo] | [empresa] |

## Resumo da Reuniao
[3-5 frases com o essencial do que aconteceu e o tom geral da discussao]

## Decisoes Tomadas
1. [Decisao 1 — com contexto breve]
2. [Decisao 2 — com contexto breve]

## Action Items

| # | Acao | Responsavel | Prazo | Prioridade |
|---|------|------------|-------|------------|
| 1 | [descricao da acao] | [nome/area] | [data] | [ALTA/MEDIA/BAIXA] |
| 2 | [descricao da acao] | [nome/area] | [data] | [ALTA/MEDIA/BAIXA] |

### Criterios de prioridade:
- **ALTA**: bloqueante para assinatura ou proxima etapa; prazo <= 7 dias
- **MEDIA**: importante mas nao bloqueante; prazo ate 30 dias
- **BAIXA**: desejavel, pode ser tratado em paralelo; sem prazo critico

## Pontos Nao Resolvidos
Questoes que ficaram em aberto e precisam de nova discussao ou analise:
- [Ponto 1 — por que nao foi resolvido, proximo passo]
- [Ponto 2 — por que nao foi resolvido, proximo passo]

## Alteracoes no Contrato/Minuta
[Se houve acordo sobre mudancas especificas no texto contratual]
- Clausula [X]: [mudanca acordada]
- Clausula [Y]: [mudanca acordada]

## Proxima Reuniao
- Data prevista: [se definida]
- Pauta preliminar: [topicos para proxima rodada]

---
Este registro nao constitui parecer juridico. Para decisoes criticas, consulte um advogado.
```

## Diretrizes gerais

### Analise de contrato no modo pre-reuniao

Se o usuario fornecer o contrato ou minuta, fazer uma analise rapida focada nos pontos de negociacao — nao uma revisao completa (para isso existe `/revisar-contrato`). Identificar:
- Clausulas com risco (RED/YELLOW) que serao discutidas na reuniao
- Pontos ambiguos que precisam de esclarecimento
- Valores, prazos e condicoes que podem ser negociados

### Citacoes legais

Citar apenas legislacao real e vigente. Artigos-chave frequentes em negociacoes:
- Clausula penal: CC art. 412 (limite ao valor da obrigacao)
- Boa-fe objetiva: CC arts. 421-422
- Resolucao por onerosidade: CC arts. 478-480
- Vicios: CC arts. 441-443
- Excecao de contrato nao cumprido: CC art. 476
- Locacao comercial: Lei 8.245/1991 arts. 51, 54-57
- LGPD: Lei 13.709/2018 arts. 46-49

Na duvida sobre um artigo especifico, consultar `references/legislacao-base.md` antes de citar.

### Talking points e red lines

Os talking points devem ser praticos e adaptados ao contexto da reuniao — nao frases genericas. Cada um deve poder ser dito literalmente pelo usuario.

Red lines devem ter justificativa legal ou financeira clara. Se uma concessao criaria risco juridico real (ex: clausula penal acima do limite do CC art. 412), isso e uma red line. Se e apenas preferencia comercial, e um ponto de negociacao — nao red line.

### Action items pos-reuniao

Cada action item deve ser:
- **Especifico**: "Enviar minuta revisada com clausula 5.2 alterada" — nao "Revisar contrato"
- **Atribuido**: sempre com responsavel nomeado
- **Com prazo**: data concreta quando possivel, ou referencia ("ate proxima reuniao")
- **Priorizado**: ALTA/MEDIA/BAIXA com criterio objetivo

### Qualidade do output

- Manter tom profissional mas acessivel — o usuario nao e advogado
- Talking points em linguagem natural, como o usuario falaria numa reuniao
- Red lines com fundamentacao solida, nunca alarmismo sem base
- Se nao souber algo com certeza, recomendar que o usuario verifique antes da reuniao
- Perguntas a levantar devem ser estrategicas, nao obvias

### Exportacao

Oferecer exportacao em Word (.docx) quando o usuario precisar compartilhar o briefing ou o registro com colegas.

## Disclaimer

Todo output — pre ou pos-reuniao — deve terminar com disclaimer de que nao constitui parecer juridico. Isso e obrigatorio e inegociavel.
