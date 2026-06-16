import type { NextConfig } from "next";
import os from "node:os";

// Dev only: allow this machine's LAN IPs so you can open the dev server on a
// phone (http://<lan-ip>:3000). Next 16 blocks cross-origin dev resources (HMR)
// by default, which leaves the client un-hydrated (buttons stay disabled).
// Computed at startup, so it works on any network without hand-editing an IP.
// Ignored by `next build` / static export.
function lanDevOrigins(): string[] {
  const origins = new Set<string>();
  for (const ifaces of Object.values(os.networkInterfaces())) {
    for (const ni of ifaces ?? []) {
      if (ni.family === "IPv4" && !ni.internal) origins.add(ni.address);
    }
  }
  return [...origins];
}

const nextConfig: NextConfig = {
  // Emit a fully static site to `out/` on `next build` so it can be hosted on
  // any static host (GitHub Pages, S3, Netlify…). No server runtime needed.
  output: "export",
  // Required by static export: no on-the-fly image optimization server.
  images: { unoptimized: true },
  // Emit `route/index.html` instead of `route.html` so links work on a plain file host.
  trailingSlash: true,
  // Let a phone on the same Wi-Fi reach the dev server (see lanDevOrigins above).
  allowedDevOrigins: lanDevOrigins(),
};

export default nextConfig;
