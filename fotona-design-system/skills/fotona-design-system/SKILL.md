---
name: fotona-design-system
description: |
  Design system da Fotona Brasil — fonte unica de verdade visual para qualquer peca da marca. Cobre os dois registros: o claro (dashboards, LPs, produtos digitais, componentes @fotona/ui) e o escuro de marca (slides 1920x1080, posts do @fotonalaser, capas, campanhas). Inclui tokens CSS prontos, logotipo oficial, fontes embutidas, anatomia de 9 arquetipos de slide, 7 formatos de post e prompts de imagem calibrados.

  Use quando: (1) Construir dashboard, LP, app ou artifact da Fotona, (2) Montar slide ou deck comercial no Canva/Gamma/HTML, (3) Criar post, carrossel ou story do @fotonalaser, (4) Gerar imagens no padrao visual da marca, (5) Precisar de cor, tipografia, logo, medida ou componente Fotona, (6) Revisar se uma peca esta na marca.

  Triggers: "Fotona", "fotona-laser", "@fotonalaser", "design system Fotona", "marca Fotona", "slide Fotona", "deck Fotona", "post Fotona", "carrossel Fotona", "vermelho Fotona", "identidade visual Fotona", "GLP1Tight", "MelasmaRecovery", "Fotona4GLOW", "SP Dynamis", "StarWalker", "choose perfection".
---

# Design System Fotona Brasil

Fonte unica de verdade visual da Fotona Brasil. **Aplique estes tokens antes de qualquer decisao propria de design.**

## Primeiro passo: qual registro?

A marca tem dois registros. Escolher errado e o erro mais caro que existe aqui.

| Registro | Quando | Base visual | Fonte de titulo |
|----------|--------|-------------|-----------------|
| **Claro** — produto digital | Dashboard, LP institucional, app interno, ferramenta de operacao, artifact de trabalho | Branco/off-white, neutros do logotipo, vermelho so na acao primaria | Instrument Serif (display) + Instrument Sans (UI) |
| **Escuro** — marca | Slide, deck comercial, capa, post, story, hero de campanha, imagem gerada | Preto + carmesim com luz de palco vermelha | Montserrat caixa alta (300 + 700) |

Na duvida: **se a peca vai ser usada, e claro; se vai ser mostrada, e escuro.** Um hero de LP pode ser escuro dentro de uma pagina clara — o registro e por peca, nao por projeto.

## Regras de ouro (valem nos dois registros)

1. **Um vermelho vivo por tela.** `#ED1C24` marca a acao primaria, "hoje", "ao vivo", a palavra em destaque. Nada mais. Se tudo e urgente, nada e.
2. **Neutros vem do logotipo** — grafite `#414042` e cinza `#808285`, nunca preto ou cinza puros no registro claro.
3. **Cor pertence ao pilar**, nunca ao responsavel nem ao humor da semana.
4. **Estado nunca so por cor** — sempre cor + forma (pilula, ponto, borda lateral).
5. **Pessoas e fotos reais.** Antes/depois e sempre foto clinica cedida, com credito do medico e numero de sessoes. Nunca gerada.
6. **Nunca**: concorrente citado ou exibido, nome de paciente, valor de procedimento, promessa de resultado, emoji como elemento grafico, dado sem fonte.

## Tokens essenciais

```
--fotona-red      #ED1C24   acao primaria · hoje · ao vivo · destaque. Nada mais.
--fotona-red-deep #CC0000   hover do botao primario
--ink             #414042   grafite do wordmark → texto principal
--ink-muted       #808285   cinza da tagline → rotulos, eixos, metadados
--text            #212121   ·  --text-muted #6E6E6E  ·  --text-faint #9A9895
--surface         #FFFFFF   ·  --surface-alt #F9F9F9 ·  --surface-sunken #F5F4F3
--border          #EBEBEB   ·  --border-strong #DBD9D7 ·  --dark-bg #111111
--radius          5px       controles  ·  --radius-card 6px

REGISTRO ESCURO DE MARCA
--brand-black     #000000   50–60% de todo slide escuro
--crimson-900/800/700/600/500  #1F0003 #3A0009 #5F0503 #7D0000 #9C130D
--brand-gradient  linear-gradient(135deg,#000 0%,#1F0003 40%,#5F0503 75%,#9C130D 100%)
--stage-light     #F5F4F1   fundo dos slides claros (tabelas, antes/depois)

PILARES DE CONTEUDO           claro     escuro
evento                        #ED1C24   #ED1C24
cientifico (tambem link)      #1863DC   #75A7FF
creators                      #0F8377   #43CFBE
comercial                     #9A6B10   #E0AE5E
imprensa                      #55555A   #B0AEAB
```

Arquivo completo pronto para colar: **`assets/tokens.css`** (inclui washes, estados semanticos, sombra e o tema escuro). Copie-o inteiro no `globals.css` do projeto ou dentro do `<style>` do artifact.

## Tipografia

| Papel | Fonte | Especificacao |
|-------|-------|---------------|
| Interface / corpo | Instrument Sans 400–700 | 15px / 1.6 · maximo 65 caracteres por linha |
| Display / numeros | Instrument Serif 400 | Titulos e numeros de resultado — conversa com o wordmark serifado |
| Rotulo | Instrument Sans 500 | 11px · `letter-spacing: .16em` · **caixa baixa** (ecoa "choose perfection") |
| Titulo de marca | Montserrat 300 + 700 | Slides, posts e campanhas: caixa alta, duas batidas na mesma frase |
| Frase emocional (social) | Serifa italica | + complemento em Montserrat 700 |

- Numeros em coluna sempre com `font-variant-numeric: tabular-nums`; titulos com `text-wrap: balance`.
- **Em artifact ou pagina standalone: embuta as fontes como `@font-face` data URI (woff2 base64).** CDN de fonte e bloqueado e cai em fallback silencioso sem avisar. Os tres arquivos estao em `assets/fonts/` e o `@font-face` de referencia em `assets/fonts.css`.
- Fallback: `Segoe UI, Helvetica Neue, sans-serif`.

## Logotipo

Wordmark serifado "Fotona" em grafite + **ponto vermelho** + tagline "choose perfection" em sans caixa baixa espacada. Arquivo: **`assets/fotona-logo.svg`** (viewBox `0 0 120 56`).

| Item | Valor |
|------|-------|
| Cores internas | wordmark `#414042` · tagline `#808285` · ponto `#ED1C24` |
| Negativa | `#414042` → `#FFFFFF` e `#808285` → `#9C9A97`, **manter o ponto vermelho** |
| Monocromatica | tudo `#FFFFFF` (inclusive o ponto) quando sobre o vermelho da marca |
| Altura minima em tela | 28px · em slide 1920×1080: 150–240px de largura |
| Area de respiro | igual a altura do ponto, em todos os lados |
| Marca reduzida | so o ponto vermelho (rail lateral, favicon, avatar) |

**Recolorir em HTML**: inline o SVG e troque os `fill` fixos por variaveis CSS. Se inlinar o mesmo SVG mais de uma vez na pagina, **renomeie os `id` do `clipPath`** em cada copia — ids duplicados quebram a renderizacao silenciosamente.

**Nunca**: recolorir o ponto, gradiente no wordmark, logo sobre foto sem camada solida, lockup com marca de terceiro dentro do produto.

## Onde continuar

Carregue **apenas** o arquivo do registro que a tarefa pede:

| Tarefa | Arquivo |
|--------|---------|
| Dashboard, LP, app, artifact, componente | `references/produtos-digitais.md` — 14 componentes `@fotona/ui`, classes CSS, temas, layout |
| Slide, deck, capa, apresentacao | `references/slides.md` — grade 1920×1080 e 9 arquetipos com anatomia e copy |
| Post, carrossel, story, feed | `references/posts-social.md` — 7 formatos, regras de grade e legenda |
| Gerar imagem (Higgsfield, Midjourney, Flux, Imagen) | `references/prompts-imagem.md` — prompt-base, 6 variacoes prontas, negativo |

Assets de apoio:

- `assets/tokens.css` — todos os tokens, claro + escuro + registro de marca
- `assets/components.css` — CSS dos 14 componentes (vocabulario `.ftn-*`), funciona sem React
- `assets/fonts.css` + `assets/fonts/*.woff2` — as tres fontes
- `assets/fotona-logo.svg` — logotipo vetorial oficial
- `assets/exemplo-dashboard.html` — o sistema claro aplicado num dashboard real. **152KB: abra no browser ou consulte trechos com `grep`, nunca leia inteiro.**

## Checklist antes de entregar

- [ ] Registro certo para a peca (claro = usar, escuro = mostrar)
- [ ] Um unico vermelho vivo na tela
- [ ] Neutros do logotipo, nunca preto/cinza puros (registro claro)
- [ ] Fontes embutidas se for artifact/standalone
- [ ] Estado com cor **e** forma
- [ ] Nenhum concorrente, nome de paciente, valor ou promessa de resultado
- [ ] Dado com fonte; protocolo com ® e metade em bold (`GLP1**TIGHT**®`)
- [ ] Antes/depois com foto real, credito do medico e numero de sessoes

## O que evitar sempre

Gradiente roxo/azul · cream com serif + terracota · luz azul, roxa ou teal na fotografia · tudo centralizado · emoji como marcador de secao · cantos muito arredondados em card · metrica sozinha sem meta · body rolando na horizontal · ilustracao ou stock no lugar de gente real.
