"use client";

import * as React from "react";

import { cn } from "@/lib/utils";

type TokenType = "plain" | "comment" | "string" | "tag" | "attr" | "punct";
type Token = { value: string; type: TokenType };

const isIdentStart = (c: string) => /[A-Za-z_$]/.test(c);
const isIdentPart = (c: string) => /[\w$.-]/.test(c);

/**
 * Tiny dependency-free tokenizer, good enough for the short JSX/TSX snippets in
 * the docs registry. Colours come from the chart design tokens so the theme
 * stays in sync — no hardcoded hex.
 */
function tokenize(code: string): Token[] {
  const tokens: Token[] = [];
  const n = code.length;
  let i = 0;
  let prev = ""; // last significant marker: "<", "</", "{" or "ident"

  while (i < n) {
    const c = code[i];

    if (/\s/.test(c)) {
      let j = i + 1;
      while (j < n && /\s/.test(code[j])) j++;
      tokens.push({ value: code.slice(i, j), type: "plain" });
      i = j;
      continue;
    }

    // line comment
    if (c === "/" && code[i + 1] === "/") {
      let j = i + 2;
      while (j < n && code[j] !== "\n") j++;
      tokens.push({ value: code.slice(i, j), type: "comment" });
      i = j;
      continue;
    }

    // string (single, double, template)
    if (c === '"' || c === "'" || c === "`") {
      let j = i + 1;
      while (j < n && code[j] !== c) {
        if (code[j] === "\\") j++;
        j++;
      }
      j = Math.min(j + 1, n);
      tokens.push({ value: code.slice(i, j), type: "string" });
      i = j;
      continue;
    }

    // identifier
    if (isIdentStart(c)) {
      let j = i + 1;
      while (j < n && isIdentPart(code[j])) j++;
      const word = code.slice(i, j);
      let k = j;
      while (k < n && /\s/.test(code[k])) k++;
      let type: TokenType = "plain";
      if (prev === "<" || prev === "</") type = "tag";
      else if (code[k] === "=") type = "attr";
      else if (/^[A-Z]/.test(word)) type = "tag";
      tokens.push({ value: word, type });
      i = j;
      prev = "ident";
      continue;
    }

    // punctuation — track <, </ and { for tag detection
    tokens.push({ value: c, type: "punct" });
    if (c === "<") prev = "<";
    else if (c === "/" && prev === "<") prev = "</";
    else if (c === "{") prev = "{";
    else prev = c;
    i++;
  }

  return tokens;
}

const STYLES: Partial<Record<TokenType, React.CSSProperties>> = {
  string: { color: "var(--color-chart-2)" },
  tag: { color: "var(--color-chart-1)" },
  attr: { color: "var(--color-chart-4)" },
};

const CLASSES: Partial<Record<TokenType, string>> = {
  comment: "text-muted-foreground italic",
  punct: "text-muted-foreground",
};

export function CodeBlock({
  code,
  className,
}: {
  code: string;
  className?: string;
}) {
  const tokens = React.useMemo(() => tokenize(code), [code]);

  return (
    <pre
      className={cn(
        "max-h-[450px] overflow-auto rounded-lg border bg-muted/50 p-4",
        className,
      )}
    >
      <code className="font-mono text-sm leading-relaxed">
        {tokens.map((t, idx) => (
          <span key={idx} className={CLASSES[t.type]} style={STYLES[t.type]}>
            {t.value}
          </span>
        ))}
      </code>
    </pre>
  );
}
