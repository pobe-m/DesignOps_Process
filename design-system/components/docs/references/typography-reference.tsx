import { getFontTokens } from "@/lib/design-tokens";

export function TypographyReference() {
  const font = getFontTokens();
  const sizes = (font.size ?? []).filter((t) => typeof t.value === "number");
  const weights = (font.weight ?? []).filter((t) => typeof t.value === "number");
  const leading = font.leading ?? [];
  const tracking = font.tracking ?? [];
  const family = font.family ?? [];

  return (
    <div className="space-y-12">
      <section className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Font Families</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          {family.map((f) => (
            <div key={f.name} className="rounded-lg border p-4">
              <div className="text-muted-foreground font-mono text-xs">{f.name}</div>
              <div className="mt-1 text-lg">{String(f.value)}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Font Sizes</h2>
        <div className="divide-y rounded-lg border">
          {sizes.map((s) => (
            <div key={s.name} className="flex items-baseline justify-between gap-6 px-4 py-3">
              <span
                className="truncate font-semibold"
                style={{ fontSize: `${s.value as number}px`, lineHeight: 1.1 }}
              >
                The quick brown fox
              </span>
              <span className="text-muted-foreground shrink-0 font-mono text-xs">
                {s.name.replace("size/", "")} · {s.value as number}px
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">Font Weights</h2>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {weights.map((w) => (
            <div
              key={w.name}
              className="flex items-center justify-between rounded-lg border px-4 py-3"
            >
              <span className="text-lg" style={{ fontWeight: w.value as number }}>
                {w.name.replace("weight/", "")}
              </span>
              <span className="text-muted-foreground font-mono text-xs">
                {w.value as number}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-8 sm:grid-cols-2">
        <div className="space-y-3">
          <h2 className="text-xl font-semibold tracking-tight">Line Height</h2>
          <div className="divide-y rounded-lg border">
            {leading.map((l) => (
              <div key={l.name} className="flex justify-between px-4 py-2.5 text-sm">
                <span className="font-mono">{l.name.replace("leading/", "leading-")}</span>
                <span className="text-muted-foreground font-mono">{l.value as number}px</span>
              </div>
            ))}
          </div>
        </div>
        <div className="space-y-3">
          <h2 className="text-xl font-semibold tracking-tight">Letter Spacing</h2>
          <div className="divide-y rounded-lg border">
            {tracking.map((t) => (
              <div key={t.name} className="flex justify-between px-4 py-2.5 text-sm">
                <span className="font-mono">{t.name.replace("tracking/", "tracking-")}</span>
                <span className="text-muted-foreground font-mono">{t.value as number}px</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
