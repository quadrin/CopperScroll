// Access-controlled build with the WSRP 1988 photographs. Usage (from atlas):
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs decrypt
//   python3 -I ../tools/build_scroll_media.py protected-media/library --private protected-media
//   corepack pnpm exec vite build --config vite.protected.config.ts
// Output: dist-protected/, deployed to Cloudflare Pages behind Cloudflare Access
// by .github/workflows/protected-atlas.yml. Never publish it on GitHub Pages.
import { cpSync, existsSync, readdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

const here = fileURLToPath(new URL(".", import.meta.url));
// Marks this build as the access-controlled site (import.meta.env.VITE_PROTECTED_BUILD): its navbar keeps Field notes on the same site.
process.env.VITE_PROTECTED_BUILD = "1";
const out = `${here}dist-protected`;
const media = `${here}protected-media/library`;
// Figures of the Field notes page (decrypted set private-media/field-notes-2026-11).
const fieldNotes = `${here}protected-media/field-notes-2026-11`;

// The image library lives outside public/, so the GitHub Pages build can
// never copy them; only this build adds them to its output.
const addPhotographs: Plugin = {
  name: "add-wsrp-photographs",
  apply: "build",
  closeBundle() {
    if (!existsSync(`${media}/index.json`)) throw new Error("protected-media/library is missing: decrypt, then run tools/build_scroll_media.py");
    cpSync(media, `${out}/media`, { recursive: true });
    if (existsSync(fieldNotes)) {
      cpSync(fieldNotes, `${out}/media/field-notes`, { recursive: true });
      const files = readdirSync(fieldNotes).filter(name => name.endsWith(".webp")).sort();
      writeFileSync(`${out}/media/field-notes/index.json`, JSON.stringify({ files }) + "\n");
    }
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
