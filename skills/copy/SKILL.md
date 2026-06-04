---
name: copy
description: Gera copy profissional para redes sociais — carrosseis, reels, legendas, posts estaticos, blogs, LinkedIn, TikTok e newsletters. Usa frameworks reais de copywriting (AIDA, PAS, BAB, PULSE, CopyBoarding, Escala de Schwartz) com selecao automatica por formato e objetivo. Inclui voice cloning, bloqueio de cliches, validacao de hook, 3 criticos adversariais, modo de analise reversa e consultoria interativa. Processo colaborativo: apresenta angulos criativos, discute estrategia e refina com o usuario antes de entregar. Use sempre que o usuario pedir para criar copy, texto para Instagram, legenda, roteiro de reel, carrossel, post, conteudo para redes sociais, newsletter, email marketing, ou qualquer texto persuasivo para plataformas digitais. Tambem ativa quando mencionar copywriting, copy, headline, hook, CTA, ou pedir para escrever para redes sociais, ou tiver duvida sobre copy/estrategia de conteudo. Comandos: /copy [tema], /copy duvida [pergunta], /copy analisar [post], /copy rapido [tema], /copy serie [tema].
intent: Skill colaborativa e interativa de copywriting profissional para redes sociais. Integra frameworks de 2 cursos de formacao (Andre Cia) e pesquisa de 35+ fontes, com fluxo de ideacao (apresenta angulos criativos antes de escrever), geracao (3 hooks + body por framework), adversarial passes (3 criticos: Cetico, Scroller, Editor) e loop de refinamento. Cobre 8 formatos (carrossel, reel, legenda, estatico, blog, LinkedIn, TikTok, newsletter) com reference dedicada por formato e framework. Suporta voice cloning com bloqueio de 140+ cliches de IA, modo consultoria para duvidas, modo reverso para analisar copy existente, modo rapido para legendas simples e modo serie com open loops. NotebookLM opcional como RAG quando reference local nao tem profundidade suficiente.
effort: xhigh
---

# Copy — Geracao Profissional e Colaborativa de Copy para Redes Sociais

Skill de copywriting que combina frameworks profissionais de 2 cursos de formacao (Andre Cia) com pesquisa de 35+ fontes para gerar copy de nivel profissional. O processo e colaborativo: antes de escrever, a skill discute estrategia, apresenta opcoes criativas e refina com o usuario — porque copy boa nasce de dialogo, nao de pipeline automatico.

## Modos de Uso

| Comando | O que faz |
|---------|-----------|
| `/copy [tema]` | Fluxo completo e interativo: entender contexto → apresentar angulos criativos → usuario escolhe → gerar → adversarial → entregar → refinar |
| `/copy duvida [pergunta]` | Consultoria: tira duvidas sobre copy, frameworks, estrategia, hooks, plataformas. Ensina o por que, nao so o como |
| `/copy analisar [post ou URL]` | Modo reverso: analisa copy existente e identifica framework, hook, Schwartz, por que funcionou |
| `/copy rapido [tema]` ou `/copy r [tema]` | Modo rapido: pula ideacao e adversarial. Usa project-context.md se existir. Ideal para legendas simples |
| `/copy serie [tema] [3-5 posts]` | Serializacao com open loops: gera serie conectada onde cada post abre/fecha loops dos anteriores |

## Principios Fundamentais

Estes principios governam toda copy gerada por esta skill. Nao sao opcionais.

1. **Hook e a variavel mais critica** — os primeiros 125 caracteres (legenda) ou 3 segundos (reel) decidem se o conteudo sera consumido. Invista 80% do esforco criativo no hook.
2. **Um CTA unico por peca** — multiplos CTAs dividem atencao e reduzem conversao em qualquer metrica. Escolha um e so um.
3. **Valor antes de pedir** — conteudo organico precisa entregar valor genuino antes de qualquer CTA. Modelo "dar 10x, pedir 1x".
4. **Autenticidade supera perfeicao** — conteudo lo-fi e imperfeito ganha alcance sobre copy polida e publicitaria. 54% dos consumidores identificam conteudo de IA.
5. **Formato dita estrutura** — carrossel, reel, legenda e post estatico tem estruturas radicalmente diferentes. Nunca aplique a mesma copy entre formatos.
6. **Framework guia, nao engessa** — use o framework como esqueleto, nao como formula rigida. A copy precisa soar como conversa, nao como template preenchido.
7. **Colaboracao antes de execucao** — copy boa nasce de dialogo. Apresentar opcoes, discutir angulos e alinhar expectativas ANTES de gerar o texto final. O usuario e co-criador, nao apenas receptor.

## Modo Consultoria — `/copy duvida`

Invocacao: `/copy duvida [pergunta]` ou qualquer duvida sobre copywriting.

Este modo transforma a skill em um consultor de copywriting. Nao gera copy — ensina, explica e orienta.

### O que responde

- **Frameworks**: "Qual a diferenca entre PAS e AIDA?", "Quando usar PASTOR?"
- **Estrategia**: "Meu publico e X, qual formato funciona melhor?", "Devo focar em reels ou carrosseis?"
- **Hooks**: "Como melhorar esse hook?", "Por que meus hooks nao param scroll?"
- **Plataformas**: "Qual o melhor horario pra postar no LinkedIn?", "TikTok ou Instagram pra B2B?"
- **Tom e voz**: "Como soar mais autentico?", "Minha copy ta parecendo IA, como resolver?"
- **Metricas**: "O que e um ER bom pro meu nicho?", "Como saber se meu conteudo ta performando?"
- **Conceitos**: "O que e nivel de consciencia de Schwartz?", "Como funciona CopyBoarding?"

### Como responder

1. Responder a duvida de forma clara e pratica, com exemplos concretos
2. Referenciar o framework ou conceito relevante (e explicar de forma acessivel)
3. Se a duvida indicar uma lacuna de conhecimento mais ampla, oferecer contexto adicional proativamente
4. Quando aplicavel, sugerir proximo passo pratico: "Quer que eu gere um exemplo aplicando isso?" ou "Quer que eu analise um post seu usando esse conceito?"
5. Consultar references locais ou NotebookLM quando a pergunta exigir profundidade tecnica

O objetivo e que o usuario saia da conversa entendendo o conceito, nao apenas com uma resposta. Ensinar a pescar, nao dar o peixe — a menos que ele peca o peixe.

## Fluxo de Geracao (completo e interativo)

O fluxo e uma conversa, nao um formulario. Cada passo envolve o usuario na decisao.

```
Usuario invoca /copy ou pede copy para redes sociais
    |
    v
0. CARREGAR CONTEXTO AUTOMATICO
   Se `references/project-context.md` existir, carregar voice profile + brand context.
   Dados do project-context substituem perguntas do passo 1.
    |
    v
1. CONVERSA ESTRATEGICA (substituiu "coletar contexto")
   Em vez de listar perguntas como formulario, conduzir uma conversa curta
   para entender o que o usuario realmente precisa. Fazer 2-4 perguntas
   estrategicas que ajudem o usuario a pensar sobre o conteudo:

   Perguntas essenciais (adaptar ao contexto, nao perguntar todas mecanicamente):
   - "Qual a transformacao que voce quer causar em quem ler isso?"
   - "Seu publico ja sabe que tem esse problema ou precisa acordar pra ele?"
     (isso define Schwartz sem jargao)
   - "Tem algum post ou referencia de tom que voce curtiu recentemente?"
   - "E pra qual plataforma e formato?"

   Se o usuario ja deu contexto suficiente na mensagem inicial, NAO repetir
   perguntas — ir direto para ideacao confirmando o que entendeu:
   "Entendi que voce quer [X] para [publico] no formato [Y]. Antes de escrever,
   deixa eu te mostrar uns angulos..."
    |
    v
2. IDEACAO — APRESENTAR ANGULOS CRIATIVOS (NOVO)
   Antes de escrever qualquer copy, apresentar 2-3 angulos/abordagens diferentes.
   Cada angulo deve ter:
   - Nome curto (2-4 palavras) para facil referencia
   - Qual framework usaria e por que
   - Qual tipo de hook funcionaria melhor
   - Que emocao/reacao busca no leitor
   - Exemplo de como o hook ficaria (1 linha, rascunho)

   Formato de apresentacao:

   **Angulo 1: [nome]** — [framework]
   > [exemplo de hook rascunhado]
   Por que: [1-2 frases explicando a logica estrategica]

   **Angulo 2: [nome]** — [framework]
   > [exemplo de hook rascunhado]
   Por que: [1-2 frases explicando a logica estrategica]

   **Angulo 3: [nome]** — [framework]
   > [exemplo de hook rascunhado]
   Por que: [1-2 frases explicando a logica estrategica]

   Perguntar: "Qual desses angulos te agrada mais? Pode escolher um, misturar
   elementos de varios, ou me pedir outro caminho."

   IMPORTANTE: esperar a resposta do usuario. Nao gerar copy completa sem
   aprovacao do angulo. Esta etapa e o coracao da colaboracao — o usuario
   precisa sentir que participou da direcao criativa.
    |
    v
3. SELECIONAR FRAMEWORK
   Com base no angulo escolhido pelo usuario, confirmar framework e formato.
   Carregar reference correspondente para detalhes.
   Se reference local nao tem profundidade suficiente e NotebookLM esta configurado
   (references/notebooks.json), consultar notebook relevante.
    |
    v
4. GERAR COPY
   - Gerar 3 versoes de hook primeiro (antes de qualquer body copy)
   - Recomendar o hook mais forte usando checklist 4Us
   - Gerar body copy seguindo estrutura do framework + formato
   - Fechar com CTA unico e organico
    |
    v
5. ADVERSARIAL PASSES (3 criticos)
   Rodar 3 criticos ANTES de entregar. Corrigir tudo que encontrarem.
   (Ver secao "Adversarial Passes" abaixo)
    |
    v
6. VALIDAR
   Rodar checklist de qualidade (secao abaixo).
   Corrigir problemas encontrados antes de entregar.
    |
    v
7. ENTREGAR + ABRIR REFINAMENTO
   Copy formatada no template do formato.
   Incluir: copy principal + 3 hooks alternativos + notas de producao.

   Apos entregar, NAO encerrar. Oferecer refinamento ativo:

   "Pronto! Aqui esta a copy. Agora me diz:
   - Ta no tom certo ou quer mais [formal/descontraido/agressivo/sutil]?
   - O hook principal ta forte ou quer testar outro angulo?
   - Alguma parte que nao soa como voce falaria?
   - Quer que eu ajuste o CTA ou mude o foco?

   Pode me pedir quantos ajustes quiser — a copy so ta pronta quando voce
   sentir que e sua."
    |
    v
8. LOOP DE REFINAMENTO (repete ate usuario aprovar)
   Quando o usuario pedir ajuste:
   - Entender O QUE incomodou e POR QUE (nao adivinhar)
   - Explicar o que vai mudar e a logica por tras
   - Gerar versao refinada mantendo o que ja estava bom
   - Mostrar antes/depois se a mudanca for significativa
   - Perguntar se agora ficou melhor

   Quando o usuario aprovar (ex: "ficou otimo", "perfeito", "pode ser"):
   - Confirmar entrega final
   - Oferecer: "Quer que eu salve esse tom/estilo no seu voice profile pra
     proximas vezes?" (se nao tem project-context.md configurado)
```

## Matriz de Selecao: Formato x Objetivo → Framework

| Objetivo | Carrossel | Reel | Legenda | Post Estatico | Blog | LinkedIn | TikTok | Newsletter |
|----------|-----------|------|---------|---------------|------|----------|--------|------------|
| **Educar** | AIDA (slide a slide) | PULSE | Educativa | SCQA | AIDA | SCQA / SAGE | PULSE | Educativa (1 insight) |
| **Empatia/dor** | PAS | PAS | Narrativa | PAS | PAS | PAS + historia | PAS rapido | PAS |
| **Transformacao/case** | BAB | BAB | Behind-the-Scenes | BAB | BAB | BAB + dados | BAB rapido | Storytelling |
| **Debate/opiniao** | TAS | TAS | Humor/Atrevimento | TAS | TAS | TAS (contrarian) | TAS (ousado) | Curadoria com opiniao |
| **Autoridade** | SAGE / 4Ps | SAGE | Educativa | 4Ps | SAGE | 4Ps + social proof | SAGE rapido | SAGE |
| **Venda direta** | AIDA Reversa | PULSE | Fill-in-the-Blank | PAS | PASTOR | AIDA (soft sell) | PULSE (urgencia) | PASTOR |

> Para detalhes de cada framework, ler `references/frameworks-core.md` ou `references/frameworks-avancados.md`.

## Estruturas por Formato

Cada formato tem regras especificas. Ler o reference correspondente para a estrutura completa.

### Carrossel
- **Reference**: `references/formato-carrossel.md`
- Slide 1 = Hook (headline com promessa + numeros). Slides 2-4 = Interest. Slides 5-8 = Desire/Detail. Slide final = CTA unico.
- Cada slide deve "ganhar" o proximo swipe. Uma ideia por slide.
- Mini-headline de 4-7 palavras por slide + 15-30 palavras body.

### Reel (Roteiro)
- **Reference**: `references/formato-reel.md`
- 3 atos: Hook (0-3s) → Desenvolvimento → CTA
- Comecar IN MEDIA RES — sem "Oi gente", sem apresentacao.
- Copy de 3 camadas: verbal (falado) + visual (on-screen text) + textual (legenda). Complementam, nao repetem.
- Framework PULSE para estrutura temporal.

### Legenda
- **Reference**: `references/formato-legenda.md`
- Hook nos primeiros 90-125 caracteres (antes do "ver mais").
- Espacamento entre blocos. Emojis como separadores, nao decoracao.
- 5 formulas: Educativa | Narrativa | Humor | Behind-the-Scenes | Fill-in-the-Blank.

### Post Estatico
- **Reference**: `references/formato-estatico.md`
- Visual headline: hook em ate 7 palavras.
- Legenda: 40-100 palavras. Brevidade supera legendas longas.
- CTA: pergunta ou "Salva pra lembrar".

### Blog
- **Reference**: `references/formato-blog.md`
- Estrutura longa com SEO/AEO. Framework PASTOR ou AIDA expandido.
- Geracao por blocos: secao por secao com validacao entre blocos.

### LinkedIn
- **Reference**: `references/formato-linkedin.md`
- Post longo (1200-1500 chars) com hook nas 2 primeiras linhas.
- Tom: autoridade com vulnerabilidade. Historias pessoais + dados.
- Carrossel PDF (8-12 slides) como formato dominante.
- Sem links no post (algoritmo penaliza) — link no primeiro comentario.

### TikTok
- **Reference**: `references/formato-tiktok.md`
- Hook em 1-2 segundos (mais agressivo que Instagram).
- Tom: ousadia, irreverencia, velocidade. Zero formalidade.
- Pattern interrupts a cada 3-5 segundos.
- Texto on-screen: 5-7 palavras, grande, alto contraste.

### Newsletter (Email)
- **Reference**: `references/formato-newsletter.md`
- Subject line: 30-50 chars. Preview text: 40-90 chars, complementa (nao repete).
- 1 tema por email, 200-500 palavras. CTA unico.
- From name pessoal (nao marca) aumenta open rate.

## Hooks

O hook e o unico copy que importa na primeira leitura. Gerar 3 versoes ANTES de escrever body copy.

### Taxonomia de Hooks

| Tipo | Mecanismo | Quando usar |
|------|-----------|-------------|
| **Curiosity Gap** | Lacuna que o cerebro precisa fechar | Universal, sempre funciona |
| **Contrarian** | Dissonancia cognitiva | Gerar debate, quebrar crencas |
| **Mistake/Vulnerabilidade** | Empatia + prova social | Conexao emocional, cases |
| **Social Proof** | Heuristica de autoridade | Numeros impressionantes |
| **Numbered List** | Numeros impares 3-7 | Educativo, previsibilidade |
| **FOMO** | Urgencia verdadeira | Ofertas reais (nao fabricar) |

### Formula de Hook em 3 Passos (Kallaway)

1. **Context Lean-In** — Topico + identificacao com dor/beneficio
2. **Scroll Stop** — Linha de contraste (mas, porem, no entanto)
3. **Contrarian Snapback** — Revelacao na direcao oposta da expectativa

> Banco completo de hooks: `references/hooks-banco.md`

### Checklist 4Us (validar hook)

Antes de aprovar um hook, validar contra os 4Us:
- [ ] **Util** — resolve um problema ou entrega valor?
- [ ] **Urgente** — por que agora e nao depois?
- [ ] **Unico** — diferente do que o publico ja viu?
- [ ] **Ultra-especifico** — numeros, prazos, detalhes concretos?

Se menos de 3 dos 4Us ativados, reescrever o hook.

## Frameworks Avancados (dos cursos)

Estes frameworks vem da formacao profissional e sao o diferencial desta skill.

### Escala de Consciencia de Schwartz

O publico esta em um de 5 niveis. O nivel determina o tipo de lead/hook:

| Nivel | Estado | Tipo de Lead | Exemplo de Hook |
|-------|--------|-------------|-----------------|
| 1. Inconsciente | Nao sabe que tem o problema | Lead indireto: historia, curiosidade, choque | "O que 90% das pessoas fazem todo dia sem saber que esta destruindo..." |
| 2. Consciente do Problema | Sabe da dor mas nao da solucao | Lead de empatia: PAS, agitacao | "Cansado de postar todo dia e nao ver resultado?" |
| 3. Consciente da Solucao | Sabe que existe solucao mas nao qual | Lead educativo: demonstracao | "Existe um framework que triplicou meu alcance" |
| 4. Consciente do Produto | Conhece a solucao mas nao decidiu | Lead de prova: depoimentos, dados | "1.247 alunos ja usam esse metodo" |
| 5. Totalmente Consciente | Pronto para agir | Lead direto: oferta, CTA | "Ultimas vagas. Comeca segunda." |

> Detalhes completos: `references/frameworks-avancados.md`

### CopyBoarding

Framework de planejamento ANTES de escrever. Mapeia:
1. **Avatar** — Quem e o publico? Dores, desejos, objecoes
2. **Produto** — O que resolve? Beneficios vs features
3. **Promessa** — Qual transformacao? De onde → para onde
4. **Objecoes** — 5 objecoes universais a quebrar
5. **Prova** — Evidencias de que funciona

> Aplicar CopyBoarding antes de gerar qualquer copy longa (carrossel 8+ slides, blog, pagina de vendas).
> Detalhes: `references/frameworks-avancados.md`

### 5 Objecoes Universais

Toda copy deve antecipar e responder:
1. "Nao tenho tempo"
2. "Nao tenho dinheiro"
3. "Isso nao funciona pra mim"
4. "Nao confio em voce"
5. "Nao preciso disso agora"

### PASTOR (Macro-estrutura)

Para copy longa (blog, pagina de vendas, carrossel denso):
- **P**roblema — Identifique a dor
- **A**mplificacao — Agrave as consequencias
- **S**olucao — Apresente a saida
- **T**estimunho — Prova social
- **O**ferta — O que esta incluido
- **R**esposta — CTA claro

## Voice Cloning (Personalizacao de Tom)

Se o usuario quiser calibrar a voz da marca/perfil:

1. **Coletar amostras** — Pedir 3-5 textos que representam o tom desejado (posts anteriores, textos do site, transcricoes)
2. **Analisar padroes** — Extrair: nivel de formalidade, uso de humor, vocabulario recorrente, tamanho de frases, uso de emojis, girias
3. **Criar voice profile** — Documento com os padroes identificados
4. **Aplicar na geracao** — Usar o voice profile como restricao ao gerar copy
5. **Bloqueio de cliches** — Lista de frases PROIBIDAS que soam como IA generica

### Lista de Cliches Proibidos

Nunca usar estas frases (soam sinteticas, 54% dos consumidores identificam IA):
- "Desbloqueie seu potencial"
- "Transforme sua vida"
- "Leve para o proximo nivel"
- "Descubra o segredo"
- "Nao vai acreditar"
- "Revolucionario"
- "Game changer"
- "Potencialize seus resultados"
- "Jornada de transformacao"
- "Conteudo de valor"

> Workflow completo de voice cloning: `references/voice-cloning.md`

## Anti-Patterns

Erros que destroem performance. Verificar TODA copy contra esta lista.

- **Multiplos CTAs** — dividem atencao. Um por peca, sempre.
- **Copy identica entre plataformas** — Instagram penaliza links, LinkedIn favorece; adaptar.
- **Hook neutro/generico** — hooks devem gerar concordancia, discordancia ou curiosidade. Neutralidade = scroll.
- **Panfletagem digital** — posts puramente promocionais tem queda de alcance organico.
- **Clickbait/overpromise** — hooks devem ser intrigantes E verdadeiros.
- **Comecar Reel com "Oi gente"** — perde os 3 segundos criticos.
- **30 hashtags genericas** — 3-5 especificas de nicho superam em alcance.
- **Cliches de IA** — ver lista acima. Substituir por linguagem real.
- **Repetir copy nas 3 camadas do Reel** — verbal, visual e textual devem se COMPLEMENTAR.
- **Legenda sem espacamento** — blocos de texto denso reduzem legibilidade e tempo de permanencia.

## Adversarial Passes (3 Criticos)

Antes de entregar qualquer copy, rodar 3 criticos internos. Cada um avalia uma dimensao diferente. Corrigir TUDO que encontrarem antes de entregar.

| Critico | O que avalia | Exemplo de feedback |
|---------|-------------|-------------------|
| **O Cetico** | Promessas fracas, claims sem prova, logica furada, exageros | "Slide 3 afirma '3x mais alcance' sem dado — adicionar fonte ou remover" |
| **O Scroller** | Hook fraco, retencao, pattern interrupts, ritmo, motivo para continuar lendo | "Hook atual e informativo mas nao para scroll — testar versao contrarian" |
| **O Editor** | Cliches de IA (ver ai-tells-database.md), tom sintetico, redundancia, naturalidade | "Frase 'jornada de transformacao' no slide 5 — substituir por linguagem real" |

### Fluxo dos Adversarial Passes

1. Gerar copy completa (passos 1-4 do fluxo)
2. **Pass 1 — O Cetico**: Avaliar claims, promessas, dados. Marcar tudo sem prova.
3. **Pass 2 — O Scroller**: Avaliar hook (4Us), retencao por bloco, pattern interrupts, CTA. Marcar onde o leitor desistiria.
4. **Pass 3 — O Editor**: Rodar contra `references/ai-tells-database.md`. Substituir toda frase sintetica. Verificar tom vs voice profile.
5. Corrigir todos os problemas encontrados.
6. Prosseguir para checklist de qualidade.

> Em modo `/copy rapido`, os adversarial passes sao PULADOS para velocidade.

## Modo Reverso — Analise de Copy Existente

Invocacao: `/copy analisar [colar post ou URL]`

Quando o usuario colar um post que performou bem, analisar:

1. **Framework identificado** — Qual framework foi usado (AIDA, PAS, BAB, etc.)
2. **Tipo de hook** — Classificar (curiosity gap, contrarian, numbered list, etc.)
3. **Nivel de Schwartz** — Em que nivel de consciencia o publico esta sendo abordado
4. **Breakdown estrutural** — Por que funcionou: dissecar cada bloco e sua funcao
5. **Padrao replicavel** — Como replicar o padrao em outros temas/nichos

### Formato de Entrega (Analise)

```
## Analise de Copy

**Framework detectado**: [nome]
**Tipo de hook**: [tipo] — [por que funciona]
**Nivel Schwartz**: [nivel] — [evidencia]

### Breakdown Estrutural
- [Bloco 1]: [funcao] — [por que funciona]
- [Bloco 2]: [funcao] — [por que funciona]
- ...

### Pontos Fortes
- [o que esta excelente e por que]

### Pontos de Melhoria
- [o que poderia ser melhor e como]

### Padrao Replicavel
- Template: [estrutura abstraida do post]
- Aplicacao: [como usar em 2-3 outros temas]
```

## Quick Mode — Legendas Rapidas

Invocacao: `/copy rapido [tema]` ou `/copy r [tema]`

Modo simplificado para legendas e posts simples sem workflow completo.

**O que PULA**: conversa estrategica (usa project-context.md), ideacao de angulos, adversarial passes, loop de refinamento.

**O que MANTEM**: selecao de framework, 3 hooks, checklist basico, bloqueio de cliches.

**Requisito**: funciona melhor com `references/project-context.md` configurado. Sem ele, assume tom neutro e publico generico.

**Mesmo no modo rapido**, se o usuario pedir ajuste apos entrega, entrar no loop de refinamento normalmente.

## Serializacao com Open Loops

Invocacao: `/copy serie [tema] [3-5 posts]`

Gera series conectadas onde cada post abre e fecha loops dos anteriores.

### Mecanica de Open Loops

- **Post 1**: Faz promessa nao resolvida no final → cria expectativa
- **Post 2**: Resolve promessa do Post 1, abre nova promessa → mantem engajamento
- **Post 3**: Resolve promessa do Post 2, fecha arco → satisfacao + CTA final
- Cada post funciona standalone (quem nao viu o anterior ainda entende)
- Alcance cumulativo: engajamento de um alimenta alcance do proximo

### Regras de Serializacao

1. **Apresentar 2-3 arcos tematicos** antes de gerar — cada arco com angulo diferente e preview do open loop central. Usuario escolhe qual arco seguir.
2. Cada post usa framework independente (pode variar entre posts)
3. Open loop = pergunta sem resposta, revelacao prometida, ou "parte 2 amanha"
4. Nunca depender 100% do post anterior — cada um entrega valor solo
5. Ultimo post fecha todos os loops abertos e tem CTA mais forte
6. Apos gerar a serie, oferecer refinamento por post individual ("Quer ajustar algum post especifico?")

## Project Context (Contexto Automatico)

Se o arquivo `references/project-context.md` existir, a skill carrega automaticamente e usa como contexto padrao, eliminando perguntas repetitivas.

### Estrutura do project-context.md

```markdown
## Brand
- Nome: [marca]
- Nicho: [nicho]
- Tom: [descricao do tom]
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
- Newsletter: [sim/nao] — ferramenta: [Substack/Mailchimp/etc]
```

> Criar este arquivo com `/copy` respondendo as perguntas de contexto, ou manualmente.

## NotebookLM Integration (RAG opcional)

Configuracao em `references/notebooks.json`. Se habilitado e NotebookLM autenticado, a skill consulta notebooks quando references locais nao tem profundidade suficiente.

**Comportamento:**
- Se `enabled: true` e NotebookLM autenticado → consulta notebook relevante via `/notebooklm ask`
- Se `enabled: false` ou nao autenticado → usa references locais normalmente (fallback transparente)
- Consulta apenas quando necessario (framework nao completo nos references, voice cloning avancado, dados de benchmark)

**Notebooks disponiveis:**
- `pesquisa` — 35+ fontes de pesquisa sobre copy para redes sociais
- `formacao_copy` — Curso Formacao Copywriter Andre Cia (frameworks avancados)
- `ia_copy` — Curso Metodo CIA 2.0 (tecnicas de IA para copy)

## Checklist de Qualidade

Antes de entregar qualquer copy, validar:

- [ ] Hook ativa pelo menos 3 dos 4Us?
- [ ] CTA e unico e organico (nao link externo)?
- [ ] Framework aplicado corretamente ao formato?
- [ ] Nenhum cliche da lista proibida?
- [ ] Tom alinhado com voice profile (se configurado)?
- [ ] Espacamento e formatacao adequados ao formato?
- [ ] Copy entrega valor antes de pedir acao?
- [ ] Nenhuma repeticao entre camadas (se reel)?
- [ ] Hashtags: 3-5 especificas de nicho (se aplicavel)?
- [ ] Tamanho adequado ao formato (legenda estatico: 40-100 palavras; carrossel: 15-30 por slide)?

## Formato de Entrega

Toda copy entregue deve seguir este formato:

```
## [Formato] — [Tema]

**Framework**: [nome do framework usado]
**Objetivo**: [educar/empatia/transformacao/debate/autoridade/venda]
**Nivel de consciencia**: [nivel Schwartz]

---

### Hook Principal
[o hook escolhido]

### Hooks Alternativos
1. [hook alternativo 1]
2. [hook alternativo 2]

### Copy Principal
[a copy completa no formato adequado]

### CTA
[o CTA unico]

### Hashtags (se aplicavel)
[3-5 hashtags especificas]

### Notas de Producao
- [observacoes sobre visual, timing, tom]
- [sugestoes de melhoria ou variacao]
```

## References Disponiveis

| Arquivo | Conteudo | Quando carregar |
|---------|----------|-----------------|
| `references/frameworks-core.md` | AIDA, PAS, BAB, PULSE, SAGE, SCQA, TAS, 4Ps, 4Us | Ao gerar qualquer copy |
| `references/frameworks-avancados.md` | CopyBoarding, CPPB, PASTOR, Schwartz, 5 Objecoes, Carta Vendas 42 passos, VSL 26 passos, Pagina Vendas 9 blocos, Palavras Gravidas, Gerador Clareza, Tecnicas por formato | Copy longa, vendas ou avancada |
| `references/formato-carrossel.md` | Estrutura slide a slide, CTAs, metricas | Ao gerar carrossel |
| `references/formato-reel.md` | Roteiro 3 atos, PULSE, copy 3 camadas | Ao gerar roteiro de reel |
| `references/formato-legenda.md` | 5 formulas, 125 chars, espacamento | Ao gerar legenda |
| `references/formato-estatico.md` | Visual headline, brevidade | Ao gerar post estatico |
| `references/formato-blog.md` | Estrutura longa, SEO, AEO, PASTOR | Ao gerar blog |
| `references/formato-linkedin.md` | Posts longos, carrosseis PDF, artigos, boas praticas LinkedIn | Ao gerar copy para LinkedIn |
| `references/formato-tiktok.md` | Roteiro TikTok, texto on-screen, trends, tom irreverente | Ao gerar copy para TikTok |
| `references/formato-newsletter.md` | Subject line, preview text, estrutura de email, tipos de newsletter | Ao gerar newsletter/email |
| `references/hooks-banco.md` | Banco de hooks por tipo psicologico + exemplos | Ao gerar hooks |
| `references/voice-cloning.md` | Workflow de calibracao, bloqueio de cliches | Ao configurar tom |
| `references/avatar-briefing.md` | Briefing do Avatar (9 campos), pesquisa invisivel, mineracao de dados, 5 Porques | Antes de copy de venda, carrosseis longos |
| `references/formatos-vendas.md` | Paginas de captura (3 e 5 blocos), lancamento ao vivo (4 aulas + pitch 14 passos), padroes de carta de vendas, FAQ como trator de objecoes | Copy de venda, lancamentos, paginas de captura |
| `references/ai-tells-database.md` | 140+ substituicoes AI-tell organizadas por contexto (texto, video, thumbnail, plataforma) | Revisao anti-IA, adversarial pass 3 |
| `references/anti-patterns.md` | O que NAO fazer, erros comuns, 5 passes adversariais, hooks avancados, stats | Revisao de qualidade |
| `references/benchmarks.md` | ER por plataforma, engagement monetization, horarios, tamanho ideal | Ao definir plataforma, validar metricas |
| `references/notebooks.json` | Config NotebookLM: IDs dos notebooks, quando consultar | Quando reference local insuficiente |
| `references/project-context.md` | Brand, voice profile, plataformas ativas (criado pelo usuario) | Auto-carregado se existir |
