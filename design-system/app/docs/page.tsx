import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { getNavGroups } from "@/components/docs/registry";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DocsHome() {
  const groups = getNavGroups();
  const total = groups.reduce((n, g) => n + g.items.length, 0);

  return (
    <div className="mx-auto max-w-4xl px-6 py-10 md:py-14">
      <div className="space-y-3">
        <Badge variant="secondary">Next.js 16 · Tailwind v4 · shadcn/ui</Badge>
        <h1 className="text-4xl font-bold tracking-tight">Component Documentation</h1>
        <p className="text-muted-foreground max-w-2xl text-base leading-7">
          A living catalogue of every component in this design system. Each page shows a live
          preview and the code, styled entirely from the {""}
          <span className="text-foreground font-medium">1,804 Figma design tokens</span> —
          colors, spacing, radius, and typography map 1:1 to Tailwind classes.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Button asChild>
            <Link href="/docs/button">
              Browse components <ArrowRight className="size-4" />
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/docs/colors">View design tokens</Link>
          </Button>
        </div>
      </div>

      <div className="mt-12 space-y-8">
        {groups.map((group) => (
          <section key={group.title} className="space-y-4">
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-semibold tracking-tight">{group.title}</h2>
              <Badge variant="outline">{group.items.length}</Badge>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {group.items.map((item) => (
                <Link key={item.slug} href={`/docs/${item.slug}`} className="group">
                  <Card className="hover:border-foreground/20 hover:bg-accent/40 h-full p-0 transition-colors">
                    <CardHeader className="p-4">
                      <CardTitle className="flex items-center justify-between text-base">
                        {item.title}
                        <ArrowRight className="text-muted-foreground size-4 opacity-0 transition-opacity group-hover:opacity-100" />
                      </CardTitle>
                      <CardDescription className="font-mono text-xs">
                        /docs/{item.slug}
                      </CardDescription>
                    </CardHeader>
                  </Card>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>

      <p className="text-muted-foreground mt-12 text-sm">
        {total} documented entries · Add a new one by appending to{" "}
        <code className="font-mono">components/docs/registry.tsx</code>.
      </p>
    </div>
  );
}
