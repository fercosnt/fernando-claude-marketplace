# Typography Reference

Sistema tipografico completo do Beauty Smile Design System.

## Font Families

### Sans (Primary - Inter)
```css
font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
```
Usado para: UI elements, body text, labels

### Heading (Montserrat)
```css
font-family: 'Montserrat', 'Inter', ui-sans-serif, system-ui, sans-serif;
```
Usado para: H1-H6, titles, display text

### Mono (JetBrains Mono)
```css
font-family: 'JetBrains Mono', ui-monospace, monospace;
```
Usado para: Code blocks, technical content

## Font Sizes

| Token | Size | Rem | Line Height |
|-------|------|-----|-------------|
| xs | 12px | 0.75rem | 16px |
| sm | 14px | 0.875rem | 20px |
| base | 16px | 1rem | 24px |
| lg | 18px | 1.125rem | 28px |
| xl | 20px | 1.25rem | 28px |
| 2xl | 24px | 1.5rem | 32px |
| 3xl | 30px | 1.875rem | 36px |
| 4xl | 36px | 2.25rem | 40px |
| 5xl | 48px | 3rem | 1 |
| 6xl | 60px | 3.75rem | 1 |
| 7xl | 72px | 4.5rem | 1 |

## Font Weights

| Token | Weight |
|-------|--------|
| thin | 100 |
| extralight | 200 |
| light | 300 |
| normal | 400 |
| medium | 500 |
| semibold | 600 |
| bold | 700 |
| extrabold | 800 |
| black | 900 |

## Line Heights

| Token | Value |
|-------|-------|
| none | 1 |
| tight | 1.25 |
| snug | 1.375 |
| normal | 1.5 |
| relaxed | 1.625 |
| loose | 2 |

## Letter Spacing

| Token | Value |
|-------|-------|
| tighter | -0.05em |
| tight | -0.025em |
| normal | 0 |
| wide | 0.025em |
| wider | 0.05em |
| widest | 0.1em |

## Heading Styles

### H1
```css
font-family: Montserrat;
font-size: 48px;
font-weight: 700;
line-height: 1;
letter-spacing: -0.025em;
```

### H2
```css
font-family: Montserrat;
font-size: 36px;
font-weight: 600;
line-height: 40px;
letter-spacing: -0.025em;
```

### H3
```css
font-family: Montserrat;
font-size: 30px;
font-weight: 600;
line-height: 36px;
letter-spacing: -0.025em;
```

### H4
```css
font-family: Montserrat;
font-size: 24px;
font-weight: 600;
line-height: 32px;
letter-spacing: 0;
```

### H5
```css
font-family: Montserrat;
font-size: 20px;
font-weight: 600;
line-height: 28px;
letter-spacing: 0;
```

### H6
```css
font-family: Montserrat;
font-size: 18px;
font-weight: 600;
line-height: 28px;
letter-spacing: 0;
```

## Text Styles

### Body
```css
font-family: Inter;
font-size: 16px;
font-weight: 400;
line-height: 24px;
```

### Body Small
```css
font-family: Inter;
font-size: 14px;
font-weight: 400;
line-height: 20px;
```

### Body Large
```css
font-family: Inter;
font-size: 18px;
font-weight: 400;
line-height: 28px;
```

### Label
```css
font-family: Inter;
font-size: 14px;
font-weight: 500;
line-height: 20px;
letter-spacing: 0.025em;
```

### Caption
```css
font-family: Inter;
font-size: 12px;
font-weight: 400;
line-height: 16px;
```

### Button
```css
font-family: Inter;
font-size: 14px;
font-weight: 500;
line-height: 20px;
letter-spacing: 0.025em;
```

## Tailwind Classes

```tsx
// Headings
className="font-heading text-5xl font-bold tracking-tight"
className="font-heading text-4xl font-semibold tracking-tight"
className="font-heading text-3xl font-semibold"

// Body
className="font-sans text-base"
className="font-sans text-sm"
className="font-sans text-lg"

// Code
className="font-mono text-sm"

// Special
className="text-xs uppercase tracking-widest"
className="text-sm font-medium tracking-wide"
```

## Google Fonts Import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Montserrat:wght@100..900&family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet">
```
