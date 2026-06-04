# Components Reference

Biblioteca de componentes React do Beauty Smile Design System.

## UI Atoms (12 components)

### Button
```tsx
import { Button } from '@/components/ui/button'

// Variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="accent">Accent</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button size="icon">Icon</Button>

// With icons
<Button leftIcon={<Plus />}>Add</Button>
<Button rightIcon={<ArrowRight />}>Next</Button>
<Button isLoading>Loading...</Button>
```

### Input
```tsx
import { Input } from '@/components/ui/input'

<Input placeholder="Digite..." />
<Input type="email" />
<Input disabled />
```

### Textarea
```tsx
import { Textarea } from '@/components/ui/textarea'

<Textarea placeholder="Mensagem..." rows={4} />
```

### Label
```tsx
import { Label } from '@/components/ui/label'

<Label htmlFor="email">Email</Label>
```

### Checkbox
```tsx
import { Checkbox } from '@/components/ui/checkbox'

<Checkbox id="terms" />
```

### Badge
```tsx
import { Badge } from '@/components/ui/badge'

<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### Card
```tsx
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card'

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Alert
```tsx
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'

<Alert variant="default">
  <AlertTitle>Info</AlertTitle>
  <AlertDescription>Message</AlertDescription>
</Alert>

<Alert variant="destructive">Error</Alert>
```

### Dialog
```tsx
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'

<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    Content
  </DialogContent>
</Dialog>
```

### Table
```tsx
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table'

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Column</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Value</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### ProgressBar
```tsx
import { ProgressBar } from '@/components/ui/progress-bar'

<ProgressBar value={75} />
<ProgressBar value={50} variant="accent" />
```

### SectionHeader
```tsx
import { SectionHeader } from '@/components/ui/section-header'

<SectionHeader
  title="Section Title"
  subtitle="Optional subtitle"
  action={<Button>Action</Button>}
/>
```

## Glass Morphism Components

### Glass (Base)
```tsx
import { Glass } from '@/components/glass'

<Glass variant="light">Light glass</Glass>
<Glass variant="dark">Dark glass</Glass>
<Glass blur="md" shadow="lg">Custom</Glass>
```

### GlassCard
```tsx
import { GlassCard } from '@/components/glass/glass-card'

<GlassCard>
  <h3>Title</h3>
  <p>Content with glass effect</p>
</GlassCard>
```

### GlassButton
```tsx
import { GlassButton } from '@/components/glass/glass-button'

<GlassButton>Glass Action</GlassButton>
<GlassButton variant="dark">Dark Glass</GlassButton>
```

### GlassPanel
```tsx
import { GlassPanel } from '@/components/glass/glass-panel'

<GlassPanel>
  Panel content with glass morphism
</GlassPanel>
```

### GlassNavbar
```tsx
import { GlassNavbar } from '@/components/glass/glass-navbar'

<GlassNavbar>
  <Logo />
  <Nav />
</GlassNavbar>
```

## Navigation Components

### Sidebar
```tsx
import { Sidebar, SidebarItem, SidebarGroup } from '@/components/navigation/sidebar'

<Sidebar>
  <SidebarGroup label="Menu">
    <SidebarItem icon={<Home />} href="/">Home</SidebarItem>
    <SidebarItem icon={<Settings />} href="/settings">Settings</SidebarItem>
  </SidebarGroup>
</Sidebar>
```

### TopBar
```tsx
import { TopBar } from '@/components/navigation/top-bar'

<TopBar
  logo={<Logo />}
  navigation={<Nav />}
  actions={<Actions />}
/>
```

## Data Display

### MetricCard
```tsx
import { MetricCard } from '@/components/data-display/metric-card'

<MetricCard
  title="Total Revenue"
  value="R$ 125.000"
  change={12.5}
  icon={<TrendingUp />}
/>
```

## Styling Patterns

### CVA Variants
```tsx
import { cva } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
        accent: 'bg-accent text-accent-foreground hover:bg-accent/90',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/90',
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-11 px-8 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)
```

### cn Utility
```tsx
import { cn } from '@/utils/cn'

<div className={cn(
  'base-classes',
  condition && 'conditional-class',
  className
)}>
```

## Accessibility

Todos os componentes:
- Usam Radix UI Primitives para ARIA
- Suportam navegacao por teclado
- Tem focus indicators visiveis
- Sao WCAG 2.1 AA compliant
