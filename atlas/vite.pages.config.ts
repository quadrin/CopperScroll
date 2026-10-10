// Static build for GitHub Pages. Usage (from atlas):
//   corepack pnpm exec vite build --config vite.pages.config.ts
// Output: ../atlas-site/, served at https://quadrin.github.io/CopperScroll/atlas-site/
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { createReadStream, existsSync, statSync } from "node:fs";

const here = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  root: `${here}pages`,
  base: "/CopperScroll/atlas-site/",
  publicDir: `${here}public`,
  plugins: [react(), {
    name: "local-source-film",
    configureServer(server) {
      // The owner's source stays outside the repository and public build.
      const filmPath = process.env.COPPER_SCROLL_FILM_PATH;
      if (!filmPath || !existsSync(filmPath)) return;
      server.middlewares.use((request, response, next) => {
        if (request.url?.split("?")[0] !== "/__source-film.mp4") return next();
        const size = statSync(filmPath).size;
        const range = request.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
        const start = range ? Number(range[1]) : 0;
        const end = range && range[2] ? Math.min(Number(range[2]), size - 1) : size - 1;
        if (start >= size || start > end) {
          response.writeHead(416, { "Content-Range": `bytes */${size}` });
          return response.end();
        }
        response.writeHead(range ? 206 : 200, {
          "Content-Type": "video/mp4", "Accept-Ranges": "bytes",
          "Content-Length": end - start + 1, "Cache-Control": "private, no-store",
          ...(range ? { "Content-Range": `bytes ${start}-${end}/${size}` } : {}),
        });
        if (request.method === "HEAD") return response.end();
        createReadStream(filmPath, { start, end }).on("error", () => response.destroy()).pipe(response);
      });
    },
  }],
  resolve: { alias: { "@": here.replace(/\/$/, "") } },
  build: { outDir: process.env.ATLAS_SITE_OUT ?? `${here}../atlas-site`, emptyOutDir: true },
});
