#!/usr/bin/env node
/**
 * bridge-tokens.mjs
 * Convert poc-delivery/design-system/tokens.json (hex/rgb) → oklch
 * then merge into Hand-off-test/brand.config.json
 *
 * Usage:
 *   node bridge-tokens.mjs \
 *     --tokens  <poc-delivery/design-system/tokens.json> \
 *     --handoff <path/to/Hand-off-test> \
 *     [--brand  <brand-name>]     # default: "poc-brand"
 *     [--dry-run]                 # preview only, don't write files
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs"
import { join, resolve } from "node:path"

// ── parse args ────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const opts = { tokens: null, handoff: null, brand: "poc-brand", dryRun: false }
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--tokens")   opts.tokens  = argv[++i]
    if (argv[i] === "--handoff")  opts.handoff = argv[++i]
    if (argv[i] === "--brand")    opts.brand   = argv[++i]
    if (argv[i] === "--dry-run")  opts.dryRun  = true
  }
  return opts
}

const opts = parseArgs(process.argv.slice(2))

if (!opts.tokens || !opts.handoff) {
  console.error("[bridge-tokens] ERROR: you must provide --tokens <path> and --handoff <path>")
  process.exit(1)
}

// ── load lib-oklch from Hand-off-test ────────────────────────────────────────
const libPath = resolve(opts.handoff, "scripts/lib-oklch.mjs")
if (!existsSync(libPath)) {
  console.error(`[bridge-tokens] ERROR: lib-oklch.mjs not found at ${libPath}`)
  console.error("  Check that --handoff points to the correct Hand-off-test repo")
  process.exit(1)
}
const { toOklch } = await import(`file://${libPath}`)

// ── load tokens.json ──────────────────────────────────────────────────────────
const rawTokens = JSON.parse(readFileSync(resolve(opts.tokens), "utf8"))

// ── flatten W3C DTCG tokens → key/value pairs ────────────────────────────────
// Supports both flat format and nested group format
function flattenTokens(obj, prefix = "") {
  const result = {}
  for (const [key, val] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}-${key}` : key
    if (val && typeof val === "object") {
      if ("$value" in val && "$type" in val) {
        // leaf token
        if (val.$type === "color") result[fullKey] = val.$value
      } else {
        // nested group
        Object.assign(result, flattenTokens(val, fullKey))
      }
    }
  }
  return result
}

const flatTokens = flattenTokens(rawTokens)
const colorTokens = Object.entries(flatTokens)

// ── map token names → semantic brand.config keys ──────────────────────────────
// Try to map a token name → the semantic key that brand.config.json uses
// Add a mapping here if a token name in the TOR output differs from shadcn semantic names
const SEMANTIC_MAP = {
  // W3C token key           → brand.config semantic key
  "color-brand-primary":     "primary",
  "color-brand-secondary":   "secondary",
  "color-background-base":   "background",
  "color-text-primary":      "foreground",
  "color-border-default":    "border",
  "color-status-error":      "destructive",
  // fallback: if the name already matches a semantic key → use it directly
}

function toSemanticKey(tokenKey) {
  if (SEMANTIC_MAP[tokenKey]) return SEMANTIC_MAP[tokenKey]
  // strip the "color-" prefix and try using it directly
  const stripped = tokenKey.replace(/^color-/, "")
  return stripped
}

// ── build light/dark override object ─────────────────────────────────────────
const lightOverride = {}
const conversionLog = []

for (const [key, hexValue] of colorTokens) {
  try {
    const oklchValue = toOklch(hexValue)
    const semanticKey = toSemanticKey(key)
    lightOverride[semanticKey] = oklchValue
    conversionLog.push({ from: key, hex: hexValue, oklch: oklchValue, semantic: semanticKey })
  } catch (e) {
    console.warn(`[bridge-tokens] ⚠ skipped ${key}: ${e.message}`)
  }
}

// ── load + update brand.config.json ──────────────────────────────────────────
const brandConfigPath = resolve(opts.handoff, "brand.config.json")
if (!existsSync(brandConfigPath)) {
  console.error(`[bridge-tokens] ERROR: brand.config.json not found at ${brandConfigPath}`)
  process.exit(1)
}

const brandConfig = JSON.parse(readFileSync(brandConfigPath, "utf8"))

// build the merged light config — white-label base + poc overrides
const mergedLight = { ...brandConfig.light, ...lightOverride }

// ── preview / write ───────────────────────────────────────────────────────────
if (opts.dryRun) {
  console.log("[bridge-tokens] DRY RUN — no files written\n")
  console.log("Tokens to override (light mode):")
  for (const { semantic, hex, oklch } of conversionLog) {
    console.log(`  ${semantic.padEnd(30)} ${hex.padEnd(10)} → ${oklch}`)
  }
  console.log(`\nTotal: ${conversionLog.length} tokens`)
  process.exit(0)
}

// write the updated brand.config.json (light override only — dark still uses the base)
const updatedConfig = {
  ...brandConfig,
  name: opts.brand,
  description: `POC brand generated from designops-pipeline pipeline. Base: White Label.`,
  light: mergedLight,
}

writeFileSync(brandConfigPath, JSON.stringify(updatedConfig, null, 2), "utf8")
console.log(`[bridge-tokens] ✓ brand.config.json updated`)
console.log(`  Brand: ${opts.brand}`)
console.log(`  Tokens injected: ${conversionLog.length}`)
console.log(`  Path: ${brandConfigPath}`)
console.log(`\nNext step: cd ${opts.handoff} && npm run brand:build`)
