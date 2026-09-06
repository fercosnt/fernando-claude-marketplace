# Registro claro — produtos digitais

Dashboards, LPs institucionais, apps internos, ferramentas de operacao e artifacts de trabalho.
Superficie branca, neutros do logotipo, vermelho reservado a acao primaria.

## Setup

**Projeto React/Next.js** (stack oficial: Next.js 15 App Router + TypeScript + Tailwind + shadcn/ui, Supabase para dados/realtime, Vercel para deploy):

```tsx
import '@fotona/ui/styles.css';           // tokens + fontes + componentes
import { Button, Chip, Metric } from '@fotona/ui';
```

**Qualquer outro contexto** (artifact, HTML solto, Canva embed, e-mail): cole `assets/tokens.css` e `assets/components.css` no `<style>` e use as classes `.ftn-*` direto no HTML. Nao precisa de React.

**Artifact ou pagina standalone**: embuta as tres fontes como `@font-face` com `src: url(data:font/woff2;base64,...)`. CDN de fonte e bloqueado e cai em fallback sem avisar.

Aplique `.ftn` no container raiz para herdar familia, tamanho 15px, `line-height` 1.6 e cor de texto.

## Tema escuro

Os tokens sao redefinidos em `[data-theme="dark"]`. Coloque o atributo no `<html>` ou em qualquer container:

```html
<html data-theme="dark">
```

Estruture sempre por tokens, nunca estilize componente dentro da media query:

1. Palette completa em `:root`
2. Redefinir **so os tokens** em `@media (prefers-color-scheme: dark)`
3. Redefinir de novo em `:root[data-theme="dark"]` **e** `:root[data-theme="light"]` — o toggle precisa vencer a media query nos dois sentidos

`assets/tokens.css` traz o bloco `[data-theme="dark"]` pronto (tema escuro opt-in). Se a peca precisar seguir a preferencia do sistema, duplique esse bloco dentro de `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }`.

## Componentes `@fotona/ui`

Vocabulario CSS: `.ftn-<componente>`, `.ftn-<componente>__<parte>`, `.ftn-<componente>--<variante>`.
Cada componente le `--pilar` e `--pilar-wash`, injetados pela classe `.ftn-pilar-<nome>` (helper `pillarClass(pillar)`).

### Acoes

| Componente | Props | Regra |
|------------|-------|-------|
| `Button` | `variant?: 'primary' \| 'secondary' \| 'ghost'` · `size?: 'sm' \| 'md' \| 'lg'` · `icon?` | **Um unico `primary` (vermelho) por tela.** `md` 32px (padrao dashboard), `sm` 26px (toolbar densa), `lg` 40px (LP). Icone SVG 16px stroke 1.6 |
| `SegmentedControl` | `options: {value,label}[]` · `value` · `onChange?` | Alterna visoes (Semana/Mes/Agenda). Ativo ganha `--surface-sunken` + peso 600. **Nunca usa vermelho** — ele e do botao primario |
| `FilterPill` | `pillar: Pillar` · `active?` | Filtro por pilar. Ponto de 6px na cor do pilar; borda cinza inativa, fundo sunken ativa. Texto em caixa baixa |
| `IconButton` | `current?` | 34×34, rail lateral. Estados: padrao cinza · hover fundo sunken · atual fundo surface + anel · foco outline vermelho |

### Classificacao

| Componente | Props | Regra |
|------------|-------|-------|
| `Chip` | `pillar: Pillar` | A que pilar o item pertence. Fundo = wash do pilar (~10%), texto na cor cheia, ponto 6px. **Raio 4px, nunca pilula** |
| `StatusPill` | `status: 'ao-vivo' \| 'publicado' \| 'pendente' \| 'rascunho'` | Pilula raio 999. Estado por cor **e** forma. Vermelho so em `ao-vivo` — a unica excecao ao "um vermelho por tela", porque significa "agora" |

### Dados

| Componente | Props | Regra |
|------------|-------|-------|
| `Card` | `title?` · `variant?: 'default' \| 'compact' \| 'elevated'` | Superficie branca, borda 1px, raio 6px, padding 20×22. **Sem sombra em repouso** — `elevated` so no container principal do dashboard. Corpo 13.5px em `--text-muted` |
| `Metric` | `name` · `value` · `delta?` · `progress?` · `hit?` · `flat?` · `size?: 'md' \| 'lg'` | Valor em Instrument Serif (24px / 38px em `lg`). **Nunca sozinha**: sempre com `delta` e `progress` contra a meta do baseline nov/2025. Barra 3px; `hit` pinta de teal |
| `Alert` | `tone?: 'evento' \| 'pendente' \| 'publicado' \| 'neutro'` · `title` | Lista lateral: ponto 6px + titulo + descricao. `evento` (vermelho) so para o que acontece hoje |
| `EventItem` | `pillar?` · `time?` · `ghost?` | Item de calendario: borda esquerda 2px na cor do pilar + fundo wash. `ghost` = slot vazio, chip vazado em italico — **vazio e informacao, nao ausencia** |
| `SectionHeading` | `label?` · `title` · `lede?` · `neutral?` | Rotulo caixa baixa + ponto vermelho 7px + titulo serifado. Um ponto vermelho por secao e o unico vermelho decorativo permitido; `neutral` troca por cinza |
| `Heading` | `variant?: 'display' \| 'section' \| 'card'` · `as?: h1..h4` | `display` e `section` em Instrument Serif 400; `card` em Instrument Sans 600. Sempre `text-wrap: balance` |

### Formulario

| Componente | Props | Regra |
|------------|-------|-------|
| `TextField` | `label` · `hint?` · `error?` | 34px, borda `--border-strong`, raio 5px, foco outline vermelho. **O erro e a unica outra situacao em que o vermelho aparece fora do botao primario** |
| `Label` | `error?` · `as?: 'label' \| 'span'` | 11px, peso 500, `letter-spacing: .16em`, caixa baixa — ecoa "choose perfection". Nomes de campo, titulos de bloco lateral, eixos de grafico |

### Marca

| Componente | Props | Regra |
|------------|-------|-------|
| `Logo` | `variant?: 'positive' \| 'negative' \| 'mono'` · `height?` (46) | `positive` grafite/cinza/ponto vermelho · `negative` branco + ponto vermelho · `mono` tudo branco (so sobre o vermelho da marca) |

### Pilares

```ts
type Pillar = 'evento' | 'cientifico' | 'creators' | 'comercial' | 'imprensa';
pillarClass('cientifico')  // → 'ftn-pilar-cientifico'
```

A cor pertence ao pilar — nunca ao responsavel, nunca ao "humor da semana".

## Layout e forma

| Regra | Detalhe |
|-------|---------|
| Raio | 5px em controles, 6px em cards. Nada de `rounded-lg` em card |
| Sombra | So no container principal (`Card variant="elevated"`). Cards internos sem sombra em repouso |
| Foco de teclado | `outline: 2px solid var(--fotona-red); outline-offset: 2px` — ja embutido nos componentes. No botao primario o outline vira `--text` (contraste sobre o vermelho) |
| Conteudo largo | Tabela ou grade de calendario rola dentro do proprio container (`overflow-x: auto`). **O body nunca rola na horizontal** |
| Evento multi-dia | Faixa continua sobre a semana, **nunca** o mesmo chip repetido em cada celula |
| Slot vazio | `EventItem ghost` — nunca deixe a celula em branco |
| Icones | SVG stroke 1.6, grade 16/20/24. **Nunca emoji** |
| Medida de linha | Maximo 65 caracteres |
| Numeros | `font-variant-numeric: tabular-nums` em qualquer coluna |

## Estados semanticos

| Estado | Cor | Quando |
|--------|-----|--------|
| ao vivo | vermelho `#ED1C24` | Acontecendo hoje |
| publicado | teal `#0F8377` | Entregue e no ar |
| pendente | ambar `#9A6B10` | Depende de aprovacao ou de terceiro |
| rascunho | cinza `#9A9895` | Reservado, sem conteudo |

## Hero escuro dentro de produto claro

LP institucional costuma abrir com hero no **registro escuro de marca**: fundo `--brand-black` com `--brand-gradient`, halo radial `--brand-halo` vindo de um canto, texto branco, titulo em `--font-brand` (Montserrat) caixa alta 300 + 700, barra `--fotona-red` de `--brand-bar` (8px em web) rente a borda inferior do bloco. O resto da pagina segue o registro claro. Detalhes em `references/slides.md` e `references/prompts-imagem.md`.

## Exemplo aplicado

`assets/exemplo-dashboard.html` — o sistema inteiro num dashboard de calendario real (rail lateral, filtros por pilar, grade semanal, metricas, alertas, tema escuro). **152KB: abra no browser ou consulte trechos com `grep`, nunca leia o arquivo inteiro.**
