# shadcn/ui Component Patterns

Copy-paste usage patterns. Load when composing UI from shadcn/ui components.
Add components with `npx shadcn@latest add <name>`.

---

## Button

```tsx
import { Button } from "@/components/ui/button"

<Button>Save Changes</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost" size="icon" aria-label="Close">
  <X className="size-4" />
</Button>
<Button variant="link" asChild><a href="/docs">Read Docs</a></Button>

// Async / loading
<Button disabled={isPending}>
  {isPending && <Loader2 className="size-4 animate-spin" />}
  {isPending ? "Saving..." : "Save"}
</Button>
```

Variants: `default` `secondary` `destructive` `outline` `ghost` `link`
Sizes: `default` `sm` `lg` `icon`

---

## Card

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Supporting text</CardDescription>
  </CardHeader>
  <CardContent>content</CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="outline">Cancel</Button>
    <Button>Confirm</Button>
  </CardFooter>
</Card>
```

---

## Form (react-hook-form + zod)

```tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({ email: z.string().email() })
type Values = z.infer<typeof schema>

export function EmailForm() {
  const form = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { email: "" } })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-4">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input placeholder="you@example.com" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

---

## Dialog

```tsx
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild><Button variant="outline">Open</Button></DialogTrigger>
  <DialogContent className="sm:max-w-md">
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    <div className="py-4">{/* content */}</div>
    <DialogFooter><Button>Confirm</Button></DialogFooter>
  </DialogContent>
</Dialog>
```

Always include `<DialogTitle>` + `<DialogDescription>` for accessibility.

---

## Data Table

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {rows.map((row) => (
      <TableRow key={row.id}>
        <TableCell className="font-medium">{row.name}</TableCell>
        <TableCell>
          <Badge variant={row.status === "active" ? "default" : "secondary"}>{row.status}</Badge>
        </TableCell>
        <TableCell className="text-right">{row.amount}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

---

## Toast (Sonner)

```tsx
// app/layout.tsx — add once at root
import { Toaster } from "@/components/ui/sonner"
<Toaster />

// anywhere
import { toast } from "sonner"
toast.success("Saved")
toast.error("Failed")
toast.promise(save(), { loading: "Saving...", success: "Done!", error: "Error" })
```

---

## Dropdown Menu

```tsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon"><MoreHorizontal className="size-4" /></Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuLabel>Actions</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem onClick={handleEdit}>Edit</DropdownMenuItem>
    <DropdownMenuItem className="text-destructive" onClick={handleDelete}>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

---

## Composition Patterns

### Page Shell with Sidebar

```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden">
      <AppSidebar />
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto p-6 max-w-7xl">{children}</div>
      </main>
    </div>
  )
}
```

### Section Header

```tsx
function SectionHeader({ title, description, action }: {
  title: string; description?: string; action?: React.ReactNode
}) {
  return (
    <div className="flex items-start justify-between gap-4 mb-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </div>
      {action}
    </div>
  )
}
```

### Empty State

```tsx
function EmptyState({ title, description, action }: {
  title: string; description: string; action?: React.ReactNode
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16 text-center">
      <p className="text-lg font-medium">{title}</p>
      <p className="text-sm text-muted-foreground max-w-sm">{description}</p>
      {action}
    </div>
  )
}
```

### Loading Skeleton

```tsx
import { Skeleton } from "@/components/ui/skeleton"

<Card>
  <CardHeader>
    <Skeleton className="h-5 w-1/2" />
    <Skeleton className="h-4 w-3/4" />
  </CardHeader>
  <CardContent className="space-y-2">
    <Skeleton className="h-4 w-full" />
    <Skeleton className="h-4 w-5/6" />
  </CardContent>
</Card>
```

---

## Customizing Components

Edit `components/ui/*.tsx` directly — never wrap to override. Use React 19 patterns (no `forwardRef`).

```tsx
// Add a Button variant — edit components/ui/button.tsx
const buttonVariants = cva("...", {
  variants: {
    variant: {
      default: "...",
      brand: "bg-violet-600 text-white hover:bg-violet-700",  // custom
    },
  },
})

// Input — React 19, ComponentProps not forwardRef
function Input({ className, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      data-slot="input"
      className={cn("flex h-9 w-full rounded-sm border border-input ...", className)}
      {...props}
    />
  )
}
```

---

## Component Catalogue

**Form & Input:** `button` `button-group` `checkbox` `combobox` `field` `input` `input-group` `input-otp` `label` `native-select` `radio-group` `select` `slider` `switch` `textarea` `toggle` `toggle-group`

**Display:** `avatar` `badge` `card` `carousel` `chart` `empty` `item` `kbd` `progress` `skeleton` `spinner` `table`

**Navigation:** `breadcrumb` `menubar` `navigation-menu` `pagination` `sidebar` `tabs`

**Overlay:** `alert-dialog` `context-menu` `dialog` `drawer` `dropdown-menu` `hover-card` `popover` `sheet` `tooltip`

**Data:** `accordion` `collapsible` `command` `data-table` `separator`

**Feedback:** `alert` `sonner`

**Utility:** `aspect-ratio` `calendar` `date-picker` `resizable` `scroll-area`

> `resizable` is a valid shadcn/ui component but has no page in the current Figma file —
> kept here as a shadcn capability; add a Figma page if the design needs it.
