# Effects Reference

Sombras, animacoes e transicoes do Beauty Smile Design System.

## Box Shadows

### Standard Shadows
```css
/* sm - Minimal elevation */
box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);

/* DEFAULT - Standard (cards, buttons) */
box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);

/* md - Moderate (floating panels) */
box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);

/* lg - High (modals, dialogs) */
box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

/* xl - Maximum */
box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);

/* 2xl - Dramatic */
box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);

/* inner - Inset depth */
box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
```

### Glass Morphism Shadows
Para uso sobre gradientes:
```css
glass-sm: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
glass: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
glass-md: 0 8px 24px 0 rgba(0, 0, 0, 0.2);
glass-lg: 0 12px 32px 0 rgba(0, 0, 0, 0.25);
glass-xl: 0 16px 48px 0 rgba(0, 0, 0, 0.3);
```

### Colored Shadows
```css
/* Primary (Deep Blue) */
primary-sm: 0 2px 8px 0 rgba(0, 16, 158, 0.2);
primary: 0 4px 16px 0 rgba(0, 16, 158, 0.25);
primary-lg: 0 8px 24px 0 rgba(0, 16, 158, 0.3);

/* Accent (Turquoise) */
accent-sm: 0 2px 8px 0 rgba(53, 191, 173, 0.2);
accent: 0 4px 16px 0 rgba(53, 191, 173, 0.25);
accent-lg: 0 8px 24px 0 rgba(53, 191, 173, 0.3);

/* Secondary (Gold) */
secondary-sm: 0 2px 8px 0 rgba(187, 150, 91, 0.2);
secondary: 0 4px 16px 0 rgba(187, 150, 91, 0.25);
secondary-lg: 0 8px 24px 0 rgba(187, 150, 91, 0.3);
```

### Focus Rings
```css
focus-primary: 0 0 0 3px rgba(0, 16, 158, 0.3);
focus-accent: 0 0 0 3px rgba(53, 191, 173, 0.3);
focus-error: 0 0 0 3px rgba(239, 68, 68, 0.3);
focus-success: 0 0 0 3px rgba(16, 185, 129, 0.3);
```

### Glow Effects
```css
glow-primary: 0 0 20px rgba(0, 16, 158, 0.4);
glow-accent: 0 0 20px rgba(53, 191, 173, 0.4);
glow-success: 0 0 20px rgba(16, 185, 129, 0.4);
glow-error: 0 0 20px rgba(239, 68, 68, 0.4);
```

## Animations

### Keyframes

```css
/* Fade */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }

/* Slide */
@keyframes slideInUp { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes slideInDown { from { transform: translateY(-10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* Scale */
@keyframes scaleIn { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes zoomIn { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }

/* Feedback */
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
@keyframes bounce { 0%, 100% { transform: translateY(-25%); } 50% { transform: translateY(0); } }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-4px); } 75% { transform: translateX(4px); } }

/* Dialog */
@keyframes dialogContentShow {
  from { opacity: 0; transform: translate(-50%, -48%) scale(0.96); }
  to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}
```

### Durations
```
fastest: 100ms
fast: 150ms
normal: 200ms (default)
slow: 300ms
slower: 400ms
slowest: 500ms
```

### Timing Functions (Easing)
```css
linear: linear;
ease: ease;
ease-in: ease-in;
ease-out: ease-out;
ease-in-out: ease-in-out;
spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
smooth: cubic-bezier(0.4, 0, 0.2, 1);
swift: cubic-bezier(0.4, 0, 0.6, 1);
snappy: cubic-bezier(0, 0, 0.2, 1);
```

### Animation Delays
```
none: 0ms
xs: 50ms
sm: 100ms
md: 150ms
lg: 200ms
xl: 300ms
```

## Transitions

### Pre-configured
```css
/* All properties */
transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
transition: all 150ms ease; /* fast */
transition: all 300ms ease; /* slow */

/* Specific */
transition: opacity 200ms ease;
transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
transition: color 200ms ease, background-color 200ms ease;
transition: box-shadow 200ms ease;

/* Component-specific */
button: color 150ms ease, background-color 150ms ease, border-color 150ms ease;
link: color 150ms ease, text-decoration-color 150ms ease;
input: border-color 150ms ease, box-shadow 150ms ease;
```

## Backdrop Blur

```css
backdrop-blur-xs: blur(2px);
backdrop-blur-sm: blur(4px);
backdrop-blur: blur(8px);
backdrop-blur-md: blur(12px);
backdrop-blur-lg: blur(16px);
backdrop-blur-xl: blur(24px);
backdrop-blur-2xl: blur(40px);
backdrop-blur-3xl: blur(64px);
```

## Tailwind Classes

```tsx
// Shadows
className="shadow-sm"
className="shadow"
className="shadow-md"
className="shadow-lg"
className="shadow-xl"
className="shadow-2xl"

// Glass shadows
className="shadow-glass"
className="shadow-glass-lg"

// Colored shadows
className="shadow-primary"
className="shadow-accent"

// Animations
className="animate-fadeIn"
className="animate-slideInUp"
className="animate-pulse"
className="animate-spin"
className="animate-bounce"

// Transitions
className="transition-all"
className="transition-colors"
className="transition-transform"
className="duration-150"
className="duration-200"
className="duration-300"
className="ease-out"
className="ease-in-out"

// Backdrop blur
className="backdrop-blur-sm"
className="backdrop-blur-md"
className="backdrop-blur-lg"
```

## Glass Morphism Pattern
```tsx
<div className={cn(
  // Background
  "bg-white/15",
  // Backdrop blur
  "backdrop-blur-md",
  // Border
  "border border-white/20",
  // Border radius
  "rounded-2xl",
  // Shadow
  "shadow-glass",
  // Transition
  "transition-all duration-200",
  // Hover
  "hover:bg-white/25 hover:shadow-glass-lg"
)}>
```
