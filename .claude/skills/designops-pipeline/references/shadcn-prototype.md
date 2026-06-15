# shadcn-skills-design-starter — Prototype Reference

> Source: https://github.com/npsin-oreo/shadcn-skills-design-starter
> Stack: Next.js 16 (App Router) · React 19 · Tailwind CSS v4 · shadcn/ui (radix-nova) · TypeScript

---

## Tech stack required in the prototype

| Layer | Tool | Version |
|-------|------|---------|
| Framework | Next.js App Router | 16 |
| Styling | Tailwind CSS | v4 |
| Components | shadcn/ui owned in `components/ui/` | radix-nova |
| Animation | tw-animate-css | latest |
| Icons | lucide-react | 1.x |
| Forms | react-hook-form + zod | latest |
| Theming | next-themes (class strategy) | 0.4 |
| Fonts | Geist (sans) / Geist Mono (mono) via `next/font` | — |

---

## Design token system

### Semantic tokens (globals.css — always use these)

| Token | Light | Dark | When to use |
|-------|-------|------|-------------|
| `--background` | oklch(1 0 0) | oklch(0.145 0 0) | page background |
| `--foreground` | oklch(0.145 0 0) | oklch(0.985 0 0) | body text |
| `--card` | oklch(1 0 0) | oklch(0.205 0 0) | card surface |
| `--card-foreground` | oklch(0.145 0 0) | oklch(0.985 0 0) | card text |
| `--primary` | oklch(0.205 0 0) | oklch(0.922 0 0) | primary action |
| `--primary-foreground` | oklch(0.985 0 0) | oklch(0.205 0 0) | text on primary |
| `--secondary` | oklch(0.97 0 0) | oklch(0.269 0 0) | secondary surface |
| `--muted` | oklch(0.97 0 0) | oklch(0.269 0 0) | subtle background |
| `--muted-foreground` | oklch(0.556 0 0) | oklch(0.708 0 0) | secondary text |
| `--accent` | oklch(0.97 0 0) | oklch(0.269 0 0) | hover states |
| `--destructive` | oklch(0.577 0.245 27.3) | oklch(0.704 0.191 22.2) | error/danger |
| `--border` | oklch(0.922 0 0) | oklch(1 0 0 / 10%) | borders |
| `--input` | oklch(0.922 0 0) | oklch(1 0 0 / 15%) | input borders |
| `--ring` | oklch(0.708 0 0) | oklch(0.556 0 0) | focus ring |
| `--radius` | 0.625rem | — | base radius |

### Tailwind class map (Figma variable → class)

```
background / foreground      →  bg-background / text-foreground
card / card-foreground       →  bg-card / text-card-foreground
primary / primary-foreground →  bg-primary / text-primary-foreground
secondary                    →  bg-secondary / text-secondary-foreground
muted / muted-foreground     →  bg-muted / text-muted-foreground
accent                       →  bg-accent (hover states)
destructive                  →  text-destructive / bg-destructive
border / input / ring        →  border-border / border-input / ring-ring
sidebar*                     →  bg-sidebar / text-sidebar-foreground / border-sidebar-border
chart-1…5                    →  var(--color-chart-1) … var(--color-chart-5)
```

### Radius scale

```
rounded-sm   →  calc(var(--radius) * 0.6)  →  ~3.75px   — buttons, inputs
rounded-md   →  calc(var(--radius) * 0.8)  →  ~5px      — badges, small cards
rounded-lg   →  var(--radius)              →  10px      — cards
rounded-xl   →  calc(var(--radius) * 1.4)  →  ~8.75px   — dialogs, sheets
rounded-2xl  →  calc(var(--radius) * 1.8)  →  ~11.25px  — modals
rounded-full →  9999px                     —  pills, avatars
```

---

## Component inventory (56 components — all built ✅)

### Form & Input
`button` · `button-group` · `checkbox` · `field` · `input` · `input-group` · `input-otp`
`label` · `native-select` · `radio-group` · `select` · `slider` · `switch`
`textarea` · `toggle` · `toggle-group`

### Navigation
`breadcrumb` · `menubar` · `navigation-menu` · `pagination` · `sidebar` · `tabs`

### Display
`avatar` · `badge` · `card` · `carousel` · `chart` · `empty` · `item` · `kbd`
`progress` · `skeleton` · `spinner` · `table`

### Overlay
`alert-dialog` · `context-menu` · `dialog` · `drawer` · `dropdown-menu`
`hover-card` · `popover` · `sheet` · `tooltip`

### Feedback
`alert` · `sonner`

### Data
`accordion` · `collapsible` · `command` · `separator`

### Utility
`aspect-ratio` · `calendar` · `scroll-area`

### Composition patterns (no separate file — composed from components)
`combobox` (Popover + Command) · `data-table` (Table + Pagination) · `date-picker` (Popover + Calendar)

---

## Coding conventions to follow

### NEVER
```tsx
// ❌ hardcoded color
className="text-gray-500 bg-[#F8F9FA]"

// ❌ hardcoded hex in style
style={{ color: '#111827' }}

// ❌ w-4 h-4 (Tailwind v4 uses size-4)
<Icon className="w-4 h-4" />

// ❌ forwardRef (not needed in React 19)
const Button = React.forwardRef<...>()

// ❌ tailwindcss-animate (use tw-animate-css instead)
import 'tailwindcss-animate'
```

### ALWAYS
```tsx
// ✅ semantic tokens only
className="text-muted-foreground bg-card"

// ✅ size-4 instead of w-4 h-4
<Icon className="size-4" />

// ✅ React 19 ComponentProps pattern
function Button({ className, ...props }: React.ComponentProps<"button">) {}

// ✅ Server Component by default — "use client" only where there's state/events
// ✅ cn() for className merging
import { cn } from "@/lib/utils"

// ✅ data-slot pattern for compound components
<div data-slot="card-header" />
```

---

## Component usage patterns

### Button
```tsx
import { Button } from "@/components/ui/button"

// variants: default | outline | secondary | ghost | destructive | link
// sizes: xs | sm | md (default) | lg | xl | icon | icon-xs | icon-sm | icon-lg | icon-xl
<Button variant="default" size="md">Save</Button>
<Button variant="outline" size="icon" aria-label="Settings">
  <Settings className="size-4" />
</Button>
```

### Card
```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardAction, CardContent, CardFooter } from "@/components/ui/card"

// size: default | sm
<Card size="default">
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
    <CardAction><Button size="sm">Action</Button></CardAction>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Field + Form
```tsx
import { Field, FieldLabel, FieldDescription, FieldError, FieldGroup } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

// orientation: vertical (default) | horizontal | responsive
<FieldGroup>
  <Field orientation="vertical">
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" type="email" placeholder="you@example.com" />
    <FieldDescription>We'll never share your email.</FieldDescription>
    <FieldError errors={errors.email} />
  </Field>
</FieldGroup>
```

### Dialog
```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"

// always include DialogTitle + DialogDescription (accessibility)
<Dialog>
  <DialogTrigger asChild><Button>Open</Button></DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm action</DialogTitle>
      <DialogDescription>This cannot be undone.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Table (data-table pattern)
```tsx
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {rows.map(row => (
      <TableRow key={row.id}>
        <TableCell>{row.name}</TableCell>
        <TableCell><Badge>{row.status}</Badge></TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Empty state
```tsx
import { Empty, EmptyHeader, EmptyMedia, EmptyTitle, EmptyDescription, EmptyContent } from "@/components/ui/empty"

<Empty>
  <EmptyHeader>
    <EmptyMedia variant="icon"><Inbox className="size-4" /></EmptyMedia>
    <EmptyTitle>No results found</EmptyTitle>
    <EmptyDescription>Try adjusting your filters.</EmptyDescription>
  </EmptyHeader>
  <EmptyContent>
    <Button variant="outline" size="sm">Reset filters</Button>
  </EmptyContent>
</Empty>
```

---

## Page / Screen scaffolding patterns

### Auth screen (Login / Register)
```tsx
// app/(auth)/login/page.tsx
export default function LoginPage() {
  return (
    <main className="flex min-h-svh items-center justify-center bg-background p-4">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Sign in</CardTitle>
          <CardDescription>Enter your credentials to continue</CardDescription>
        </CardHeader>
        <CardContent>
          <LoginForm />  {/* "use client" component */}
        </CardContent>
      </Card>
    </main>
  )
}
```

### Dashboard layout
```tsx
// app/(dashboard)/layout.tsx
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/layout/app-sidebar"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="flex-1 overflow-auto p-6">{children}</main>
    </SidebarProvider>
  )
}
```

### Settings / Form page
```tsx
export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-8 p-6">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="text-muted-foreground">Manage your preferences</p>
      </div>
      <Separator />
      <SettingsForm />  {/* "use client" */}
    </div>
  )
}
```

---

## File structure for prototype screens

```
app/
  (auth)/
    login/page.tsx
    register/page.tsx
  (dashboard)/
    layout.tsx              ← SidebarProvider + AppSidebar
    page.tsx                ← dashboard home
    [feature]/
      page.tsx              ← feature list/index
      [id]/page.tsx         ← detail view
      new/page.tsx          ← create form

components/
  ui/                       ← shadcn components — don't wrap
  layout/
    app-sidebar.tsx         ← nav items from the brief's user flows
    header.tsx
  [feature]/                ← feature-scoped components
    [feature]-form.tsx      ← "use client"
    [feature]-table.tsx     ← "use client" if it has interaction
```

---

## Accessibility checklist (every item must pass)

- [ ] `aria-label` on every icon-only button
- [ ] `<DialogTitle>` + `<DialogDescription>` on every dialog
- [ ] Don't remove `focus-visible:ring-2 focus-visible:ring-ring`
- [ ] Color isn't the only signal — pair it with an icon/text
- [ ] `role="alert"` on error messages
- [ ] `alt` text on every `<img>`

