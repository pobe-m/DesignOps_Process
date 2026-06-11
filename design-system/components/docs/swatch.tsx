import type { ColorToken, PaletteFamily } from "@/lib/design-tokens";

/** Large swatch for a semantic token — shows the exact value from the Figma export. */
export function SemanticSwatch({ token }: { token: ColorToken }) {
  return (
    <div className="overflow-hidden rounded-lg border">
      <div
        className="h-16 w-full border-b"
        style={{ backgroundColor: token.hex, opacity: token.alpha }}
      />
      <div className="space-y-1 p-3">
        <div className="flex items-center justify-between gap-2">
          <span className="font-mono text-sm font-medium">{token.name}</span>
          <span className="text-muted-foreground font-mono text-xs uppercase">
            {token.hex}
          </span>
        </div>
        {token.alias ? (
          <p className="text-muted-foreground text-xs">
            alias: <span className="font-mono">{token.alias}</span>
            {token.alpha < 1 ? ` · ${Math.round(token.alpha * 100)}%` : ""}
          </p>
        ) : null}
        {token.description ? (
          <p className="text-muted-foreground text-xs leading-5">{token.description}</p>
        ) : null}
      </div>
    </div>
  );
}

/** Compact swatch used in palette rows. */
export function PaletteSwatch({
  shade,
  hex,
  alpha,
}: {
  shade: string;
  hex: string;
  alpha: number;
}) {
  return (
    <div className="group flex flex-col gap-1">
      <div
        className="h-12 w-full rounded-md border"
        style={{ backgroundColor: hex, opacity: alpha }}
        title={`${shade} · ${hex}`}
      />
      <div className="px-0.5">
        <div className="text-xs font-medium">{shade}</div>
        <div className="text-muted-foreground font-mono text-[10px] uppercase">{hex}</div>
      </div>
    </div>
  );
}

/** One color family rendered as a row of shade swatches. */
export function PaletteRow({ family }: { family: PaletteFamily }) {
  return (
    <div className="space-y-2">
      <h3 className="font-mono text-sm font-medium capitalize">{family.family}</h3>
      <div className="grid grid-cols-3 gap-2 sm:grid-cols-6 lg:grid-cols-11">
        {family.shades.map((s) => (
          <PaletteSwatch key={s.name} shade={s.shade} hex={s.hex} alpha={s.alpha} />
        ))}
      </div>
    </div>
  );
}
