// Render every entry schematic SVG to png/ with headless Chromium (Playwright).
//
// Usage, from research/schematics/:  node render_png.mjs
// Needs Playwright (npm i playwright && npx playwright install chromium) and,
// for the colour reduction, Python with Pillow. Output: png/entry_NN.png at 1.5x,
// then reduced to 256 colours to keep the files small.
import { chromium } from "playwright";
import { readdirSync, readFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, resolve } from "node:path";

const here = resolve(".");
const out = join(here, "png");
mkdirSync(out, { recursive: true });
const svgs = readdirSync(here).filter((f) => /^entry_.*\.svg$/.test(f)).sort();
const browser = await chromium.launch();
for (const f of svgs) {
  const head = readFileSync(join(here, f), "utf8").slice(0, 400);
  const width = Number(/width="(\d+)"/.exec(head)[1]);
  const height = Number(/height="(\d+)"/.exec(head)[1]);
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1.5 });
  await page.goto("file://" + join(here, f));
  await page.screenshot({ path: join(out, f.replace(/\.svg$/, ".png")) });
  await page.close();
}
await browser.close();
execFileSync("python3", ["-I", "-c", `
from PIL import Image
from pathlib import Path
for f in sorted(Path(${JSON.stringify(out)}).glob("*.png")):
    Image.open(f).convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE).save(f, optimize=True)
`], { stdio: "inherit" });
console.log(`Rendered ${svgs.length} schematics to png/`);
