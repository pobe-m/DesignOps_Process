"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

// Static export can't do a server-side redirect, so send the visitor to the
// docs on the client and offer a plain link as a no-JS fallback.
export default function Home() {
  const router = useRouter();

  React.useEffect(() => {
    router.replace("/docs");
  }, [router]);

  return (
    <main className="flex min-h-svh items-center justify-center">
      <p className="text-muted-foreground text-sm">
        Redirecting to the{" "}
        <Link
          href="/docs"
          className="text-foreground underline underline-offset-4"
        >
          documentation
        </Link>
        …
      </p>
    </main>
  );
}
