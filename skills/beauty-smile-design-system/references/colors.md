# Colors Reference

Paleta de cores completa do Beauty Smile Design System.

## Brand Colors

### Primary (Deep Blue)
Usado em: Admin theme, CTAs primarios, headers, navegacao
```
DEFAULT: #00109E
hover:   #000C7A
active:  #000958
```

### Secondary (Gold)
Usado em: Acentos premium, destaques especiais (usar com moderacao)
```
DEFAULT: #BB965B
hover:   #A68350
active:  #917045
```

### Accent (Turquoise)
Usado em: Public theme, elementos interativos, tech moderno
```
DEFAULT: #35BFAD
hover:   #2DA89A
active:  #259187
```

## Neutral Colors

Escala de cinzas do branco ao preto.

```
white: #FFFFFF
50:    #F8F9F9
100:   #F1F2F2
200:   #E8E9E8
300:   #D6D7D5
400:   #BFC0BE
500:   #A5A7A9
600:   #86898C
700:   #6B6D70
800:   #4A4C4E
900:   #2D2E30
black: #000000
```

## Semantic Colors

### Success (Green)
```
DEFAULT: #10B981
700:     #047857
```

### Warning (Orange)
```
DEFAULT: #F59E0B
700:     #D97706
```

### Error (Red)
```
DEFAULT: #EF4444
700:     #DC2626
```

### Info (Turquoise)
```
DEFAULT: #35BFAD
```

## Chart Colors

Para graficos e visualizacao de dados:
```
1: #00109E (Primary)
2: #35BFAD (Accent)
3: #BB965B (Secondary)
4: #10B981 (Success)
5: #F59E0B (Warning)
```

## Admin Theme

```css
--primary: #00109E;
--background: #00109E;
--sidebar: #2D2E30;
--sidebar-foreground: #FFFFFF;
--sidebar-accent: #4A4C4E;
--sidebar-border: #6B6D70;
--sidebar-ring: #35BFAD;
```

## Public Theme

```css
--primary: #35BFAD;
--background: linear-gradient(135deg, #35BFAD 0%, #00109E 100%);
--overlay: rgba(0, 0, 0, 0.15);
```

## Glass Morphism

```css
/* Light glass */
background: rgba(255, 255, 255, 0.15);

/* Light glass hover */
background: rgba(255, 255, 255, 0.25);

/* Dark glass */
background: rgba(0, 0, 0, 0.30);
```

## Tailwind Classes

```tsx
// Primary
className="bg-primary text-primary-foreground"
className="bg-primary/hover"
className="bg-primary/active"

// Accent
className="bg-accent text-accent-foreground"

// Secondary
className="bg-secondary text-secondary-foreground"

// Semantic
className="text-success"
className="text-warning"
className="text-error"
className="text-info"

// Neutral
className="bg-neutral-50"
className="text-neutral-700"
className="border-neutral-200"
```

## CSS Variables

```css
:root {
  --primary: 240 100% 31%;
  --primary-foreground: 0 0% 100%;
  --accent: 170 55% 48%;
  --accent-foreground: 0 0% 100%;
  --secondary: 35 39% 55%;
  --secondary-foreground: 0 0% 100%;

  --success: 160 84% 39%;
  --warning: 38 92% 50%;
  --error: 0 84% 60%;
  --info: 170 55% 48%;

  --background: 0 0% 100%;
  --foreground: 240 4% 16%;
  --card: 0 0% 100%;
  --card-foreground: 240 4% 16%;
  --border: 240 3% 90%;
  --ring: 170 55% 48%;
}
```
