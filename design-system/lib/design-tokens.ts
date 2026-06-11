import "server-only";

import fs from "node:fs";
import path from "node:path";

// Single source of truth — the Figma export shipped with the design-system skill.
const TOKENS_FILE = path.join(
  process.cwd(),
  ".claude/skills/shadcn-ui-design/assets/variables-export.json",
);

type RawColor = { r: number; g: number; b: number; a?: number };
type RawMode = { value: RawColor | number; alias?: string; aliasCollection?: string };
type RawVar = {
  name: string;
  resolvedType: "COLOR" | "FLOAT" | "STRING" | string;
  description?: string;
  collectionName: string;
  valuesByMode: Record<string, RawMode>;
};
type RawFile = {
  collections: { name: string; variableCount: number }[];
  variables: RawVar[];
};

let cache: RawFile | null = null;
function load(): RawFile {
  if (!cache) cache = JSON.parse(fs.readFileSync(TOKENS_FILE, "utf8")) as RawFile;
  return cache;
}

function firstMode(v: RawVar): RawMode {
  return v.valuesByMode[Object.keys(v.valuesByMode)[0]];
}

function toHex(c: RawColor): string {
  const h = (n: number) => Math.round(n * 255).toString(16).padStart(2, "0");
  return `#${h(c.r)}${h(c.g)}${h(c.b)}`;
}

export type ColorToken = {
  name: string;
  hex: string;
  alpha: number;
  alias?: string;
  description?: string;
};

export type PaletteFamily = {
  family: string;
  shades: { name: string; shade: string; hex: string; alpha: number }[];
};

export type NumberToken = { name: string; value: number; alias?: string };

/** Flat list of color tokens for a collection (e.g. "shadcn-ui"). */
export function getColors(collection: string): ColorToken[] {
  return load()
    .variables.filter((v) => v.collectionName === collection && v.resolvedType === "COLOR")
    .map((v) => {
      const m = firstMode(v);
      const c = m.value as RawColor;
      return {
        name: v.name,
        hex: toHex(c),
        alpha: c.a ?? 1,
        alias: m.alias,
        description: v.description?.trim() || undefined,
      };
    });
}

/** Color tokens grouped by family (e.g. slate, gray, blue) for a palette collection. */
export function getPalette(collection: string): PaletteFamily[] {
  const families = new Map<string, PaletteFamily>();
  for (const v of load().variables) {
    if (v.collectionName !== collection || v.resolvedType !== "COLOR") continue;
    const [family, shade = ""] = v.name.split("/");
    const c = firstMode(v).value as RawColor;
    if (!families.has(family)) families.set(family, { family, shades: [] });
    families.get(family)!.shades.push({
      name: v.name,
      shade: shade || family,
      hex: toHex(c),
      alpha: c.a ?? 1,
    });
  }
  return [...families.values()];
}

/** Numeric tokens (spacing, radius, etc.) for a collection. */
export function getNumbers(collection: string): NumberToken[] {
  return load()
    .variables.filter(
      (v) => v.collectionName === collection && typeof firstMode(v).value === "number",
    )
    .map((v) => {
      const m = firstMode(v);
      return { name: v.name, value: m.value as number, alias: m.alias };
    });
}

/** font collection grouped by prefix (size, weight, leading, tracking, family). */
export function getFontTokens(): Record<string, { name: string; value: number | string }[]> {
  const groups: Record<string, { name: string; value: number | string }[]> = {};
  for (const v of load().variables) {
    if (v.collectionName !== "font") continue;
    const group = v.name.includes("/") ? v.name.split("/")[0] : "other";
    (groups[group] ??= []).push({
      name: v.name,
      value: firstMode(v).value as number | string,
    });
  }
  return groups;
}

export function getTotals(): { collection: string; count: number }[] {
  return load().collections.map((c) => ({ collection: c.name, count: c.variableCount }));
}
