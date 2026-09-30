import { readFile, writeFile, unlink } from "node:fs/promises";

const built = new URL("../../atlas-site/index.html", import.meta.url);
const homepage = new URL("../../index.html", import.meta.url);
const restrictedComparison = new URL("../../atlas-site/research/qumran-video-comparison.html", import.meta.url);

// Pages serves the same built atlas at the repository root and at /atlas-site/.
const html = (await readFile(built, "utf8")).replace('href="./favicon.svg"', 'href="/CopperScroll/atlas-site/favicon.svg"');
await writeFile(homepage, html);
await unlink(restrictedComparison).catch(error => {
  if (error.code !== "ENOENT") throw error;
});
