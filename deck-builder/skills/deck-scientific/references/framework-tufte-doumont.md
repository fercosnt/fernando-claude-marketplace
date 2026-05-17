# Tufte + Doumont — visualizacao de dados e arquitetura de informacao

> Aplicado em **Results** (Tufte) e em **arquitetura narrativa** (Doumont).

## Tufte — principios essenciais

Edward Tufte ("The Visual Display of Quantitative Information"). 5 regras operacionais para slides cientificos:

### 1. Data-ink ratio alto

> Maximize a tinta dedicada aos dados; minimize tinta nao-data.

Aplicacao:
- Sem gradientes 3D em barras
- Sem dropshadow
- Sem grades pesadas (use linhas sutis ou nenhuma)
- Sem moldura ao redor do grafico
- Sem fundo cinza padrao Excel

### 2. Sem chartjunk

Banir:
- **Pizza chart com >5 fatias** (humanos nao distinguem area de setores; use barras horizontais ranqueadas)
- **Eixo Y truncado sem aviso** (exagera diferencas)
- **Cores arco-iris** (sem mapeamento perceptual — use ColorBrewer)
- **Icones decorativos** dentro do plot area (chartjunk classico)
- **Legenda separada do plot** quando rotulos diretos funcionam

### 3. Small multiples

Para comparar trajetorias entre grupos: **multiplas mini-figuras lado-a-lado** com mesmo eixo, em vez de 1 figura entulhada de linhas.

Exemplo: 8 estudos do grupo → 8 mini-plots Kaplan-Meier alinhados em grid 2x4 com mesmo eixo Y, em vez de 1 grafico com 8 curvas sobrepostas.

### 4. Legenda autossuficiente

A figura deve ser entendida **sem ler o slide ao lado** ou o texto do paper. Legenda contem:
- O que e o eixo X / eixo Y (com unidade)
- N por grupo
- Teste estatistico aplicado + p-value
- IC95% reportado ou indicado por barras de erro
- Fonte (se reproducao)

### 5. Sparklines e tabelas densas

Para apresentar **multiplos outcomes secundarios**: tabela densa (Tufte's "supertable") com sparklines inline e bullets visuais, em vez de slide-por-outcome.

## Doumont — Trees, Maps, Theorems

Jean-luc Doumont ("Trees, maps, and theorems"). Arquitetura de informacao para comunicacao tecnica.

### Trees — estrutura hierarquica

Toda apresentacao tem uma arvore:
- **Raiz:** Big Idea (U5) — 1 frase
- **Galhos principais:** 3-5 messages-chave (1 por modulo/ato)
- **Folhas:** evidencias por message

Aplicacao operacional:
- Slide 2 de qualquer apresentacao oral deve mostrar a **arvore** (agenda visual)
- Cada slide subsequente e uma folha que sustenta um galho

### Maps — orientacao espacial

Em apresentacoes longas (oral-long / keynote), use **mapas de progresso**:
- Indicador "voce esta aqui" em cada slide de transicao
- Ato 1 / Ato 2 / Ato 3 visivel
- Slide-numerador discreto no rodape

### Theorems — afirmacao assertiva + evidencia

Cada slide cientifico deve seguir o padrao **theorem**:
- **Action title** (1 frase assertiva — nao titulo descritivo)
- **Evidencia visual** (figura/tabela que sustenta)
- **Speaker notes** com nuance

Exemplo:
- Titulo descritivo (RUIM): "Resultados de profundidade de bolsa"
- Action title (BOM): "Er:YAG reduziu profundidade de bolsa em 1.8 mm (IC95% -2.3 a -1.3, p<0.001, GRADE moderate)"

## Tabela de aplicacao por modo

| Principio | Poster | Oral-short | Oral-long | Keynote |
|-----------|--------|-----------|-----------|---------|
| Data-ink ratio alto | ✅ | ✅ | ✅ | ✅ |
| Sem chartjunk | ✅ | ✅ | ✅ | ✅ |
| Small multiples | quando aplicavel | raro (so 2 slides results) | recomendado | obrigatorio (multi-estudo Ato 2) |
| Legenda autossuficiente | ✅ | ✅ | ✅ | ✅ |
| Tabelas densas (Tufte) | ok no painel direito | evitar (legibilidade plateia) | so em apendice | so em apendice |
| Trees (agenda visual) | nao aplicavel (1 painel) | slide 2 implicito | slide 2 obrigatorio | slide 2 obrigatorio |
| Maps (voce esta aqui) | nao aplicavel | nao precisa | recomendado | obrigatorio |
| Theorems (action titles) | ✅ key finding e theorem | ✅ | ✅ | ✅ |

## Cross-refs

- IMRAD aplicado em arquitetura geral → `framework-imrad-grade.md`
- Better Poster Morrison (modo poster) → `framework-better-poster-morrison.md`
