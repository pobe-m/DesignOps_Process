#!/usr/bin/env node
/**
 * GEOMETRY + UNIVERSAL-DESIGN AUDIT (render-based). Renders a page in headless Chrome and
 * measures the *geometric correctness* the token/contrast/taste audits don't cover — from REAL
 * computed boxes, not static guesses. Complements audit_prototype.py (tokens), taste_audit.mjs
 * (slop), and audit_runtime.mjs (a11y).
 *
 * Grounded (not invented) in three sources so findings trace back:
 *   - 8pt grid        : spacing (margin/padding/gap) should snap to a 4px step.
 *   - WCAG 2.2 §2.5.8 : Target Size (Minimum) — interactive targets ≥ 24×24 CSS px (AA).
 *   - Universal Design: low physical effort + perceptible information (touch reach, min text size).
 *
 * Checks:
 *   - Off-grid spacing   : margin/padding/gap not a multiple of 4px (grid drift)
 *   - Touch targets      : interactive elements < 24px (HIGH, WCAG 2.2 AA) / < 44px (MED, comfort)
 *   - Optical misalign   : sibling left/top edges that differ by 1–3px (should be equal or clearly apart)
 *   - Component drift     : same class, sibling, but differing padding (inconsistent component metrics)
 *   - Tiny text          : rendered font-size < 12px (perceptible-information floor)
 *
 * Usage: node scripts/geometry_audit.mjs <file.html> [--dark] [--strict]
 *   --strict → exit 1 on any HIGH finding (use as a gate). Default: report, exit 0.
 * Degrades gracefully: without Playwright it prints SKIPPED and exits 0 (never blocks default).
 */
import { resolve } from "node:path";

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.log("geometry_audit: playwright not installed — SKIPPED");
  process.exit(0);
}

const argv = process.argv.slice(2);
const strict = argv.includes("--strict");
const dark = argv.includes("--dark");
const files = argv.filter((a) => !a.startsWith("--"));
if (!files.length) {
  console.log("usage: node scripts/geometry_audit.mjs <file.html> [--dark] [--strict]");
  process.exit(0);
}

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
let high = 0;

for (const f of files) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.goto("file://" + resolve(f), { waitUntil: "networkidle" }).catch(() => {});
  await page.addStyleTag({ content: "*{transition:none!important;animation:none!important}" });
  if (dark) await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
  await page.waitForTimeout(300);

  const data = await page.evaluate(() => {
    const vis = (el) => {
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 1 && r.height > 1 && s.visibility !== "hidden" && +s.opacity !== 0;
    };
    const px = (v) => parseFloat(v) || 0;
    const offGrid = (v) => { const n = px(v); return n > 0 && Math.abs(n - Math.round(n / 4) * 4) > 0.5; };

    let spacingTotal = 0, spacingOff = 0;
    const tinyText = [];
    const targets = [];
    const drift = [];
    const misalign = [];

    for (const el of document.querySelectorAll("body *")) {
      if (["SCRIPT", "STYLE", "SVG", "PATH"].includes(el.tagName) || !vis(el)) continue;
      const s = getComputedStyle(el);

      // off-grid spacing (8pt grid → 4px step)
      for (const prop of ["marginTop", "marginBottom", "marginLeft", "marginRight",
                          "paddingTop", "paddingBottom", "paddingLeft", "paddingRight", "gap", "rowGap", "columnGap"]) {
        const v = s[prop];
        if (!v || v === "0px" || v === "normal") continue;
        spacingTotal++;
        if (offGrid(v)) spacingOff++;
      }

      // tiny text (perceptible information)
      const direct = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
      if (direct && px(s.fontSize) < 12) tinyText.push(Math.round(px(s.fontSize)));

      // touch targets (WCAG 2.2 §2.5.8)
      const interactive = ["A", "BUTTON", "INPUT", "SELECT", "TEXTAREA"].includes(el.tagName) ||
        ["button", "link", "checkbox", "radio", "switch", "tab", "menuitem"].includes(el.getAttribute("role") || "");
      if (interactive) {
        const r = el.getBoundingClientRect();
        if (r.width > 1 && r.height > 1) targets.push({ w: Math.round(r.width), h: Math.round(r.height), tag: el.tagName });
      }
    }

    // per-component drift + optical misalignment among same-class siblings
    const cls = (el) => (typeof el.className === "string" ? el.className : (el.getAttribute && el.getAttribute("class")) || "").split(" ").filter(Boolean)[0] || "";
    for (const parent of document.querySelectorAll("body *")) {
      const kids = [...parent.children].filter((k) => vis(k) && cls(k));
      const byClass = {};
      for (const k of kids) (byClass[k.tagName + "." + cls(k)] ||= []).push(k);
      for (const [key, arr] of Object.entries(byClass)) {
        if (arr.length < 2) continue;
        const pads = arr.map((k) => getComputedStyle(k).paddingLeft);
        if (new Set(pads).size > 1) drift.push(key);
        // optical misalignment: left edges 1–3px apart (a real misalignment reads as sloppy)
        const lefts = arr.map((k) => k.getBoundingClientRect().left);
        for (let a = 0; a < lefts.length; a++)
          for (let b = a + 1; b < lefts.length; b++) {
            const d = Math.abs(lefts[a] - lefts[b]);
            if (d >= 1 && d <= 3) { misalign.push(key); a = lefts.length; break; }
          }
      }
    }

    return { spacingTotal, spacingOff, tinyText, targets, drift: [...new Set(drift)], misalign: [...new Set(misalign)] };
  });
  await page.close();

  const findings = [];
  const offPct = data.spacingTotal ? Math.round((data.spacingOff / data.spacingTotal) * 100) : 0;
  if (offPct > 15) findings.push(["MED", `${offPct}% of spacing values are off the 4px grid (${data.spacingOff}/${data.spacingTotal}) — snap margins/padding/gap to the spacing scale.`]);
  const tooSmall = data.targets.filter((t) => t.w < 24 || t.h < 24);
  const smallish = data.targets.filter((t) => (t.w < 44 || t.h < 44) && !(t.w < 24 || t.h < 24));
  if (tooSmall.length) findings.push(["HIGH", `${tooSmall.length} interactive target(s) < 24×24px (WCAG 2.2 §2.5.8 AA fail) — e.g. ${tooSmall.slice(0, 3).map((t) => `${t.tag} ${t.w}×${t.h}`).join(", ")}.`]);
  if (smallish.length) findings.push(["MED", `${smallish.length} target(s) < 44×44px (below comfortable touch/Universal-Design reach).`]);
  if (data.tinyText.length) findings.push(["MED", `${data.tinyText.length} text node(s) render < 12px (perceptible-information floor) — smallest ${Math.min(...data.tinyText)}px.`]);
  if (data.misalign.length) findings.push(["MED", `Optical misalignment: sibling edges 1–3px apart in ${data.misalign.length} group(s) (${data.misalign.slice(0, 2).join(", ")}) — align to the same edge or space them clearly.`]);
  if (data.drift.length) findings.push(["MED", `Component metric drift: same-class siblings with differing padding in ${data.drift.length} group(s) (${data.drift.slice(0, 2).join(", ")}).`]);

  const mode = dark ? " [dark]" : "";
  if (!findings.length) console.log(`OK   ${f}${mode} — geometry clean (grid ${100 - offPct}% on, ${data.targets.length} targets ≥24px)`);
  else {
    console.log(`\n${f}${mode}:`);
    for (const [sev, msg] of findings) { console.log(`  ${sev}  ${msg}`); if (sev === "HIGH") high++; }
  }
}
await browser.close();
if (strict && high) { console.log(`\n${high} HIGH geometry finding(s).`); process.exit(1); }
console.log("\n(geometry is measured, but taste calls the final cut — pair with human visual review.)");
process.exit(0);
