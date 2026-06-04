# Spacing Reference

Sistema de espacamento do Beauty Smile Design System.

## Base Unit

**4px** - Todos os valores sao multiplos de 4px.

## Spacing Scale

| Token | Value | Use |
|-------|-------|-----|
| 0 | 0px | Reset |
| 1 | 4px | Minimal gap |
| 2 | 8px | Small gaps |
| 3 | 12px | Tight spacing |
| 4 | 16px | Default/medium |
| 5 | 20px | - |
| 6 | 24px | Large |
| 7 | 28px | - |
| 8 | 32px | Extra large |
| 9 | 36px | - |
| 10 | 40px | - |
| 11 | 44px | - |
| 12 | 48px | 2x large |
| 14 | 56px | - |
| 16 | 64px | Section |
| 20 | 80px | - |
| 24 | 96px | Page |
| 28 | 112px | - |
| 32 | 128px | Hero |

## Semantic Aliases

| Token | Value | Description |
|-------|-------|-------------|
| xs | 4px | Minimal gap |
| sm | 8px | Small gaps between elements |
| md | 16px | Medium spacing, default |
| lg | 24px | Large spacing |
| xl | 32px | Extra large spacing |
| 2xl | 48px | Very large |
| 3xl | 64px | Section level |
| 4xl | 96px | Page level |
| 5xl | 128px | Hero level |

## Component-Specific

| Token | Value | Use |
|-------|-------|-----|
| buttonPadding | 16px | Button internal padding |
| cardPadding | 24px | Card internal padding |
| inputPadding | 12px | Input field padding |
| iconGap | 8px | Gap between icon and text |

## Layout

| Token | Value | Use |
|-------|-------|-----|
| gutter | 16px | Grid gutter |
| container | 24px | Container horizontal padding |
| section | 64px | Vertical section spacing |
| page | 96px | Page vertical padding |

## Border Radius

| Token | Value |
|-------|-------|
| none | 0 |
| sm | 4px |
| DEFAULT | 8px |
| md | 12px |
| lg | 16px |
| xl | 24px |
| 2xl | 32px |
| 3xl | 48px |
| full | 9999px |

## Responsive Breakpoints

| Token | Value | Description |
|-------|-------|-------------|
| xs | 475px | Extra small devices |
| sm | 640px | Small devices |
| md | 768px | Medium devices |
| lg | 1024px | Large devices |
| xl | 1280px | Extra large |
| 2xl | 1536px | 2x large |

## Z-Index Scale

| Token | Value | Use |
|-------|-------|-----|
| base | 0 | Default |
| dropdown | 1000 | Dropdowns |
| sticky | 1100 | Sticky headers |
| fixed | 1200 | Fixed elements |
| modalBackdrop | 1300 | Modal backdrop |
| modal | 1400 | Modals |
| popover | 1500 | Popovers |
| tooltip | 1600 | Tooltips |
| notification | 1700 | Notifications |
| top | 9999 | Always on top |

## Tailwind Classes

```tsx
// Padding
className="p-4"      // 16px all
className="px-6"     // 24px horizontal
className="py-8"     // 32px vertical
className="pt-16"    // 64px top
className="pb-24"    // 96px bottom

// Margin
className="m-4"      // 16px all
className="mx-auto"  // center
className="mt-8"     // 32px top
className="mb-16"    // 64px bottom

// Gap
className="gap-2"    // 8px
className="gap-4"    // 16px
className="gap-6"    // 24px

// Border Radius
className="rounded"      // 8px
className="rounded-sm"   // 4px
className="rounded-md"   // 12px
className="rounded-lg"   // 16px
className="rounded-xl"   // 24px
className="rounded-2xl"  // 32px
className="rounded-full" // 9999px

// Grid
className="grid grid-cols-12 gap-4"
className="col-span-6"
className="col-span-4"
```

## Common Patterns

### Card
```tsx
className="p-6 rounded-lg" // 24px padding, 16px radius
```

### Button
```tsx
className="px-4 py-2 rounded-md" // 16px h, 8px v, 12px radius
```

### Input
```tsx
className="px-3 py-2 rounded-md" // 12px h, 8px v, 12px radius
```

### Section
```tsx
className="py-16 px-6" // 64px vertical, 24px horizontal
```

### Container
```tsx
className="max-w-7xl mx-auto px-6" // centered, 24px padding
```
