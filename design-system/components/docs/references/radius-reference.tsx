import { getNumbers } from "@/lib/design-tokens";

const MAIN = new Set([
  "rounded-none",
  "rounded-xs",
  "rounded-sm",
  "rounded-md",
  "rounded-lg",
  "rounded-xl",
  "rounded-2xl",
  "rounded-3xl",
  "rounded-4xl",
  "rounded-full",
]);

export function RadiusReference() {
  const scale = getNumbers("border-radius")
    .filter((t) => MAIN.has(t.name))
    .sort((a, b) => a.value - b.value);

  return (
    <section className="space-y-4">
      <p className="text-muted-foreground text-sm">
        {scale.length} radius steps pulled from the Figma export. Buttons use `rounded-sm`, cards
        `rounded-lg`, dialogs `rounded-xl`.
      </p>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
        {scale.map((t) => (
          <div key={t.name} className="space-y-2">
            <div
              className="bg-muted border-primary/40 flex h-24 items-center justify-center border-2"
              style={{ borderRadius: `${Math.min(t.value, 48)}px` }}
            >
              <span className="text-muted-foreground font-mono text-xs">{t.value}px</span>
            </div>
            <div className="font-mono text-xs font-medium">{t.name}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
