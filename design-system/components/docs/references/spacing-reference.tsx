import { getNumbers } from "@/lib/design-tokens";

export function SpacingReference() {
  // The gap scale, excluding directional gap-x / gap-y duplicates.
  const scale = getNumbers("gap")
    .filter((t) => !t.name.includes("-x-") && !t.name.includes("-y-"))
    .sort((a, b) => a.value - b.value);

  return (
    <section className="space-y-4">
      <p className="text-muted-foreground text-sm">
        {scale.length} steps on a 4px base unit. Values pulled from the Figma export — these back
        every `p-*`, `m-*`, and `gap-*` utility.
      </p>
      <div className="divide-y rounded-lg border">
        {scale.map((t) => (
          <div key={t.name} className="flex items-center gap-4 px-4 py-2.5">
            <span className="w-20 shrink-0 font-mono text-sm">{t.name}</span>
            <span className="text-muted-foreground w-16 shrink-0 font-mono text-xs">
              {t.value}px
            </span>
            <div className="flex-1">
              <div
                className="bg-primary h-3 rounded-sm"
                style={{ width: `${Math.min(t.value, 384)}px` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
