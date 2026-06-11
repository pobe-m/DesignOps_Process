"use client";

import * as React from "react";
import { Check, Copy, Terminal } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CodeBlock } from "@/components/docs/code-block";

function useCopy() {
  const [copied, setCopied] = React.useState(false);
  const copy = React.useCallback((text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }, []);
  return { copied, copy };
}

function CopyButton({
  value,
  label,
}: {
  value: string;
  label: string;
}) {
  const { copied, copy } = useCopy();
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => copy(value)}
      aria-label={label}
      className="absolute top-3 right-3 z-10 size-7 text-muted-foreground"
    >
      {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
    </Button>
  );
}

export function ComponentPreview({
  preview,
  code,
  install,
}: {
  preview: React.ReactNode;
  code: string;
  /** Items to pass to `shadcn add`. Defaults to none (Installation tab hidden). */
  install?: string;
}) {
  const installCommand = install
    ? `npx shadcn@latest add ${install}`
    : null;

  return (
    <Tabs defaultValue="preview" className="w-full">
      <TabsList>
        <TabsTrigger value="preview">Preview</TabsTrigger>
        <TabsTrigger value="code">Code</TabsTrigger>
        {installCommand && (
          <TabsTrigger value="installation">Installation</TabsTrigger>
        )}
      </TabsList>

      <TabsContent value="preview">
        <div className="flex min-h-[350px] w-full items-center justify-center rounded-lg border p-10">
          {preview}
        </div>
      </TabsContent>

      <TabsContent value="code">
        <div className="relative">
          <CopyButton value={code} label="Copy code" />
          <CodeBlock code={code} />
        </div>
      </TabsContent>

      {installCommand && (
        <TabsContent value="installation">
          <div className="relative">
            <CopyButton value={installCommand} label="Copy install command" />
            <pre className="overflow-auto rounded-lg border bg-muted/50 p-4 pr-12">
              <code className="flex items-center gap-2 font-mono text-sm">
                <Terminal className="size-4 shrink-0 text-muted-foreground" />
                <span>
                  <span className="text-muted-foreground">npx </span>
                  shadcn@latest add{" "}
                  <span style={{ color: "var(--color-chart-1)" }}>
                    {install}
                  </span>
                </span>
              </code>
            </pre>
          </div>
        </TabsContent>
      )}
    </Tabs>
  );
}
