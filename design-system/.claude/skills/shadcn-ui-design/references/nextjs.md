# Next.js App Router Conventions

Reference for building UI in a Next.js App Router project. Load when working on
routing, layouts, data fetching, or deciding Server vs Client components.

---

## Reserved File Conventions

| File | Purpose | Client? |
|---|---|---|
| `layout.tsx` | Shared UI wrapping child routes | Server (default) |
| `page.tsx` | Route's unique UI; makes route accessible | Server (default) |
| `loading.tsx` | Instant loading state (Suspense boundary) | Server |
| `error.tsx` | Error boundary for segment | **Must be `"use client"`** |
| `not-found.tsx` | 404 UI for `notFound()` throws | Server |
| `template.tsx` | Like layout but re-mounts on navigation | Server |

```tsx
// app/(dashboard)/loading.tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="p-6 space-y-4">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
    </div>
  )
}
```

```tsx
// app/(dashboard)/error.tsx — error boundaries MUST be client
"use client"
import { Button } from "@/components/ui/button"

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-16">
      <p className="text-lg font-semibold">Something went wrong</p>
      <p className="text-sm text-muted-foreground">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

---

## Server Component vs Client Component

**Default = Server Component.** Add `"use client"` only when the component needs:

| Needs | Use |
|---|---|
| `useState`, `useReducer` | `"use client"` |
| `useEffect`, lifecycle | `"use client"` |
| Browser APIs (`window`, `document`) | `"use client"` |
| Event handlers (`onClick`, `onChange`) | `"use client"` |
| `useRouter`, `usePathname`, `useSearchParams` | `"use client"` |
| `useContext` | `"use client"` |
| `async`/`await` data fetching | Server Component |
| Database / filesystem access | Server Component |
| No interactivity | Server Component |

**Placement rule:** push `"use client"` as deep as possible — wrap the interactive leaf, not the page.

```tsx
// ✓ Good — page stays a Server Component, only FilterBar is client
// app/(dashboard)/page.tsx
import { DataTable } from "@/components/dashboard/data-table"
import { FilterBar } from "@/components/dashboard/filter-bar"  // "use client"

export default async function DashboardPage() {
  const data = await fetchData()        // runs on the server
  return (
    <div>
      <FilterBar />
      <DataTable data={data} />
    </div>
  )
}

// ✗ Bad — entire page becomes client-side for one widget
"use client"
export default function DashboardPage() { /* ... */ }
```

`"use client"` goes at the very top of the file, before all imports.

---

## Route Groups

`(groupName)` folders organize routes without adding a URL segment.

```
app/
  (auth)/            # URL: /login (not /auth/login)
    layout.tsx       # centered auth layout
    login/page.tsx
    register/page.tsx
  (dashboard)/       # URL: /dashboard
    layout.tsx       # sidebar layout
    dashboard/page.tsx
    settings/page.tsx
```

```tsx
// app/(auth)/layout.tsx
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted">
      <div className="w-full max-w-sm">{children}</div>
    </div>
  )
}
```

---

## Dynamic Segments & Params

In Next.js 15+, `params` and `searchParams` are Promises — await them.

```tsx
// app/posts/[id]/page.tsx
interface Props {
  params: Promise<{ id: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export default async function PostPage({ params }: Props) {
  const { id } = await params
  const post = await fetchPost(id)
  return <article>{post.content}</article>
}

export async function generateStaticParams() {
  const posts = await fetchAllPosts()
  return posts.map((p) => ({ id: p.id }))
}
```

---

## Metadata API

```tsx
import type { Metadata } from "next"

// Static
export const metadata: Metadata = {
  title: "Dashboard",
  description: "Manage your workspace",
}

// Dynamic
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params
  const post = await fetchPost(id)
  return { title: post.title }
}
```

---

## Image Handling

```tsx
import Image from "next/image"

// Fixed dimensions
<Image
  src="/hero.png"
  alt="Hero image"
  width={1200}
  height={600}
  priority                       // for above-the-fold images
  className="rounded-lg object-cover"
/>

// Fill parent (unknown dimensions)
<div className="relative aspect-video">
  <Image src={url} alt={alt} fill className="object-cover rounded-lg" />
</div>
```

Never use a bare `<img>` — always `next/image`.

---

## Font Setup

Fonts load via `next/font` and expose CSS variables consumed by `globals.css`.
See `assets/fonts.ts`. Wire the variables onto `<body>` in the root layout:

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes"
import { googleSans, geistMono } from "@/lib/fonts"
import "@/app/globals.css"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${googleSans.variable} ${geistMono.variable} font-sans antialiased bg-background text-foreground`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```
