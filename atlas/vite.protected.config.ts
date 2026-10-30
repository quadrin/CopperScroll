// Access-controlled build with the WSRP 1988 photographs. Usage (from atlas):
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs decrypt
//   corepack pnpm exec vite build --config vite.protected.config.ts
// Output: dist-protected/, deployed to Cloudflare Pages behind Cloudflare Access
// by .github/workflows/protected-atlas.yml. Never publish it on GitHub Pages.
import { cpSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

const here = fileURLToPath(new URL(".", import.meta.url));
const out = `${here}dist-protected`;
const media = `${here}protected-media/wsrp`;

// The decrypted photographs live outside public/, so the GitHub Pages build can
// never copy them; only this build adds them to its output.
const addPhotographs: Plugin = {
  name: "add-wsrp-photographs",
  apply: "build",
  closeBundle() {
    if (!existsSync(`${media}/frames.json`)) throw new Error("protected-media/wsrp is missing: run scripts/wsrp-media.mjs decrypt first");
    cpSync(media, `${out}/wsrp`, { recursive: true });
  },
};

export default defineConfig({
  root: `${here}pages`,
  base: "/",
  publicDir: `${here}public`,
  plugins: [react(), addPhotographs],
  resolve: { alias: { "@": here.replace(/\/$/, "") } },
  build: { outDir: out, emptyOutDir: true },
});
