import { PaletteRow, SemanticSwatch } from "@/components/docs/swatch";
import { getColors, getPalette } from "@/lib/design-tokens";

export function ColorsReference() {
  const semantic = getColors("shadcn-ui");
  const tw = getPalette("tw-colors");
  const radix = getPalette("rdx-colors");

  return (
    <div className="space-y-12">
      <section className="space-y-4">
        <div className="space-y-1">
          <h2 className="text-xl font-semibold tracking-tight">Semantic Tokens</h2>
          <p className="text-muted-foreground text-sm">
            The {semantic.length} tokens that drive every component. Values pulled directly from
            the Figma export — these are the variables behind `bg-primary`, `text-muted-foreground`,
            and the rest.
          </p>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {semantic.map((t) => (
            <SemanticSwatch key={t.name} token={t} />
          ))}
        </div>
      </section>

      <section className="space-y-6">
        <div className="space-y-1">
          <h2 className="text-xl font-semibold tracking-tight">Tailwind Palette</h2>
          <p className="text-muted-foreground text-sm">
            {tw.reduce((n, f) => n + f.shades.length, 0)} base colors across {tw.length} families —
            the source palette aliased by the semantic tokens.
          </p>
        </div>
        <div className="space-y-6">
          {tw.map((f) => (
            <PaletteRow key={f.family} family={f} />
          ))}
        </div>
      </section>

      <section className="space-y-6">
        <div className="space-y-1">
          <h2 className="text-xl font-semibold tracking-tight">Radix Palette</h2>
          <p className="text-muted-foreground text-sm">
            {radix.reduce((n, f) => n + f.shades.length, 0)} perceptual scale colors across{" "}
            {radix.length} families — used for chart tokens and overlays.
          </p>
        </div>
        <div className="space-y-6">
          {radix.map((f) => (
            <PaletteRow key={f.family} family={f} />
          ))}
        </div>
      </section>
    </div>
  );
}
