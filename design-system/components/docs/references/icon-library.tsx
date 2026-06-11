"use client";

import * as React from "react";
import { icons, Copy, Search } from "lucide-react";
import { toast } from "sonner";

import { Input } from "@/components/ui/input";

// PascalCase export name → kebab-case display name (matches the Figma "Lucide
// - Outline" page and lucide.dev): "AArrowDown" → "a-arrow-down".
const toKebab = (name: string) =>
  name
    .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
    .replace(/([A-Z])([A-Z][a-z])/g, "$1-$2")
    .toLowerCase();

// Built once from the installed lucide-react registry — the real source of
// truth, so the gallery never drifts from the package version.
const ALL_ICONS = Object.entries(icons).map(([name, Icon]) => ({
  name,
  kebab: toKebab(name),
  Icon,
}));

export function IconLibrary() {
  const [query, setQuery] = React.useState("");
  const q = query.trim().toLowerCase();

  const list = React.useMemo(
    () =>
      q
        ? ALL_ICONS.filter(
            (i) => i.kebab.includes(q) || i.name.toLowerCase().includes(q),
          )
        : ALL_ICONS,
    [q],
  );

  function copy(name: string) {
    navigator.clipboard.writeText(`<${name} />`);
    toast.success("Copied to clipboard", {
      description: `<${name} />`,
    });
  }

  return (
    <section className="space-y-5">
      <p className="text-muted-foreground text-sm leading-7">
        {ALL_ICONS.length.toLocaleString()} outline icons from{" "}
        <a
          href="https://lucide.dev/icons"
          target="_blank"
          rel="noreferrer"
          className="text-foreground underline underline-offset-4"
        >
          lucide-react
        </a>
        . Import by name —{" "}
        <code className="bg-muted rounded px-1.5 py-0.5 font-mono text-xs">
          {`import { Camera } from "lucide-react"`}
        </code>{" "}
        — then click any icon below to copy its JSX.
      </p>

      <div className="relative">
        <Search className="text-muted-foreground pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2" />
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={`Search ${ALL_ICONS.length.toLocaleString()} icons…`}
          aria-label="Search icons"
          className="pl-9"
        />
      </div>

      <p className="text-muted-foreground text-xs">
        {list.length.toLocaleString()}{" "}
        {list.length === 1 ? "icon" : "icons"}
        {q ? ` matching “${query.trim()}”` : ""}
      </p>

      {list.length === 0 ? (
        <div className="text-muted-foreground flex flex-col items-center gap-2 py-16 text-center text-sm">
          <Search className="size-6 opacity-40" />
          <span>No icons match “{query.trim()}”.</span>
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-2 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10">
          {list.map(({ name, kebab, Icon }) => (
            <button
              key={name}
              type="button"
              onClick={() => copy(name)}
              title={kebab}
              aria-label={`Copy ${name}`}
              className="group bg-card text-card-foreground hover:bg-accent hover:text-accent-foreground focus-visible:ring-ring relative flex aspect-square items-center justify-center rounded-md border transition-colors focus-visible:ring-2 focus-visible:outline-none"
            >
              <Icon className="size-5" />
              <Copy className="text-muted-foreground absolute top-1 right-1 size-3 opacity-0 transition-opacity group-hover:opacity-100" />
            </button>
          ))}
        </div>
      )}
    </section>
  );
}
