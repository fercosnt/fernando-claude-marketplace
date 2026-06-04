---
name: beauty-smile-design-system
description: |
  Design system completo da Beauty Smile para criar aplicacoes com identidade visual consistente. Inclui paleta de cores, tipografia, espacamento, sombras, animacoes, componentes React, glass morphism, emojis, icones Lucide e 50+ logos SVG.

  Use quando: (1) Criar componentes ou paginas Beauty Smile, (2) Estilizar artefatos (slides, docs, HTML, dashboards) com a marca, (3) Aplicar efeitos glass morphism, (4) Implementar tema admin ou public, (5) Precisar de cores, fontes, espacamentos, logos ou icones da marca, (6) Criar landing pages ou sistemas internos.

  Triggers: "Beauty Smile", "design system", "brand colors", "glass effect", "admin theme", "public theme", "turquoise", "deep blue", "dental clinic", "healthcare UI", "isotipo", "logo Beauty Smile".
---

# Beauty Smile Design System

Design system completo para criar interfaces consistentes com a identidade visual Beauty Smile.

## Quick Reference

### Cores Principais
```
Primary (Deep Blue):  #00109E  - Admin theme, CTAs, headers
Accent (Turquoise):   #35BFAD  - Public theme, interativo
Secondary (Gold):     #BB965B  - Premium, destaques
Success:              #10B981  - Confirmacoes
Warning:              #F59E0B  - Alertas
Error:                #EF4444  - Erros
```

### Fontes
- **Headings**: Montserrat (semibold/bold)
- **Body**: Inter (regular/medium)
- **Code**: JetBrains Mono

### Temas

**Admin** (Ferramentas internas):
```css
background: #00109E;
sidebar: #2D2E30;
foreground: #FFFFFF;
```

**Public** (Landing pages):
```css
background: linear-gradient(135deg, #35BFAD 0%, #00109E 100%);
```

### Glass Morphism
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 16px;
```

### Espacamento (base 4px)
```
xs: 4px   sm: 8px   md: 16px   lg: 24px   xl: 32px
```

### Border Radius
```
sm: 4px   default: 8px   md: 12px   lg: 16px   xl: 24px   full: 9999px
```

## Referencias Detalhadas

Carregue conforme necessidade:

| Necessidade | Arquivo |
|-------------|---------|
| Cores completas, estados, semanticas | [colors.md](references/colors.md) |
| Fontes, tamanhos, pesos, hierarquia | [typography.md](references/typography.md) |
| Componentes React, variantes, props | [components.md](references/components.md) |
| Espacamento, border-radius, layout | [spacing.md](references/spacing.md) |
| Sombras, animacoes, transicoes | [effects.md](references/effects.md) |
| Voz da marca, personalidade, valores | [brand-guidelines.md](references/brand-guidelines.md) |
| Icones Lucide e Emojis | [icons-emojis.md](references/icons-emojis.md) |
| Logos SVG, variacoes, uso | [logos.md](references/logos.md) |

## Logos (Quick Reference)

### Variacoes
- **Horizontal**: Headers, materiais digitais
- **Vertical**: Espacos quadrados, impressos
- **Isotipo**: Favicon, icones de app
- **Tipografico**: Apenas o nome

### Cores Disponiveis
Azul (#00109E), Branco, Cinza (#6B6D70), Dourado (#BB965B), Preto (#2D2E30), Turquesa (#35BFAD)

### Paths SVG
```
/logos/svg/horizontal/BS_Horizontal_{Cor}.svg
/logos/svg/vertical/BeautySmile_Vertical_{Cor}.svg
/logos/svg/isotipo/BS_Isotipo_{Cor}.svg
/logos/svg/tipografico/BS_Tipografico_{Cor}.svg
```

## Icones (Lucide React)

```tsx
import { Moon, Sparkles, Zap, Heart, Smile } from 'lucide-react'

// Beauty Sleep
<Moon size={24} className="text-primary" />

// Clareamento
<Sparkles size={24} className="text-secondary" />

// Laser Fotona
<Zap size={24} className="text-primary" />
```

### Icones por Tratamento
| Tratamento | Icone | Import |
|------------|-------|--------|
| Beauty Sleep | Moon | `lucide-react` |
| Clareamento | Sparkles | `lucide-react` |
| Limpeza Laser | Droplet | `lucide-react` |
| Sensibilidade | AlertCircle | `lucide-react` |
| Laser Fotona | Zap | `lucide-react` |

## Emojis da Marca

### Tratamentos
- Beauty Sleep: `moon`
- Clareamento: `sparkles`
- Limpeza: `tooth`
- Tecnologia: `zap` `microscope`

### Status
- Sucesso: `white_check_mark`
- Aviso: `warning`
- Erro: `x`
- Info: `information_source`

## Variantes de Button

```tsx
// Primary (Deep Blue)
<Button variant="primary">Agendar</Button>

// Accent (Turquoise)
<Button variant="accent">Saiba Mais</Button>

// Secondary (Gold)
<Button variant="secondary">Premium</Button>

// Destructive
<Button variant="destructive">Cancelar</Button>
```

## Personalidade da Marca

Aplique estes tracos em UI e copy:

1. **Transformadora** - Mostrar antes/depois, resultados dramaticos
2. **Acolhedora** - Linguagem calorosa, cuidado
3. **Vanguardista** - Moderna, tecnologia de ponta
4. **Sofisticada** - Premium, estetica elegante
5. **Confiavel** - Construir confianca com expertise

## Checklist para Novos Componentes

- [ ] Usa tokens de cor corretos (nao hex hardcoded)
- [ ] Tipografia segue hierarquia (Montserrat headings, Inter body)
- [ ] Espacamento usa grid de 4px
- [ ] Tem estados hover/active/focus
- [ ] Suporta temas admin e public
- [ ] Acessivel (contraste, focus indicators)
- [ ] Usa icones Lucide consistentemente
