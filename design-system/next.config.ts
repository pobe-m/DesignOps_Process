import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Emit a fully static site to `out/` on `next build` so the docs can be
  // hosted on any static host (GitHub Pages, S3, Netlify…). The docs are all
  // statically generated, so no server runtime is needed.
  output: "export",
  // Required by static export: no on-the-fly image optimization server.
  images: { unoptimized: true },
  // Emit `docs/button/index.html` instead of `docs/button.html` so links work
  // when served from a plain file host.
  trailingSlash: true,
};

export default nextConfig;
