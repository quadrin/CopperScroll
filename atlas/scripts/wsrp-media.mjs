// Encrypt or decrypt the WSRP 1988 photographs for the access-controlled atlas.
//
// The repository holds only ciphertext (../private-media/wsrp-1988/). The key is
// a GitHub Actions secret (WSRP_MEDIA_KEY, 32 random bytes in base64) and is
// never committed. The public GitHub Pages build never reads this folder.
//
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs encrypt <q4 folder> <cut-out folder> [out]
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs decrypt [in] [out]
//
// Format of each .enc file: "CSWSRP1" | 12-byte IV | AES-256-GCM ciphertext | 16-byte tag.
// The file name is the additional authenticated data, so files cannot be swapped.
// Segments 19–23 (columns XI–XII) are reserved for a blind reading and refused.
import { createCipheriv, createDecipheriv, createHash, randomBytes } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ENC = path.resolve(here, "../../private-media/wsrp-1988");
const DEFAULT_OUT = path.resolve(here, "../protected-media/wsrp");
const MAGIC = Buffer.from("CSWSRP1");
const HELD = new Set([19, 20, 21, 22, 23]);
const CREDIT = "Photographs by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary, 1988. Courtesy the Department of Antiquities, Jordan. Private study copy: not for publication or redistribution.";

const sha = buf => createHash("sha256").update(buf).digest("hex");
function key() {
  const raw = process.env.WSRP_MEDIA_KEY;
  if (!raw) throw new Error("WSRP_MEDIA_KEY is not set");
  const k = Buffer.from(raw.trim(), "base64");
  if (k.length !== 32) throw new Error("WSRP_MEDIA_KEY must be 32 bytes in base64");
  return k;
}
function refuseHeld(segment, name) {
  if (!Number.isInteger(segment) || segment < 1 || segment > 23) throw new Error(`no segment number in ${name}`);
  if (HELD.has(segment)) throw new Error(`segment ${segment} is reserved and must not be processed (${name})`);
}
function seal(k, name, plain) {
  const iv = randomBytes(12), c = createCipheriv("aes-256-gcm", k, iv);
  c.setAAD(Buffer.from(name));
  const body = Buffer.concat([c.update(plain), c.final()]);
  return Buffer.concat([MAGIC, iv, body, c.getAuthTag()]);
}
function open(k, name, sealed) {
  if (!sealed.subarray(0, MAGIC.length).equals(MAGIC)) throw new Error(`${name}: not a sealed media file`);
  const iv = sealed.subarray(MAGIC.length, MAGIC.length + 12), tag = sealed.subarray(sealed.length - 16);
  const d = createDecipheriv("aes-256-gcm", k, iv);
  d.setAAD(Buffer.from(name)); d.setAuthTag(tag);
  return Buffer.concat([d.update(sealed.subarray(MAGIC.length + 12, sealed.length - 16)), d.final()]);
}

async function encrypt(q4Dir, cutDir, outDir = DEFAULT_ENC) {
  const k = key();
  const cut = JSON.parse(await readFile(path.join(cutDir, "cutouts.json"), "utf8"));
  await mkdir(outDir, { recursive: true });
  const files = [], frames = [];
  for (const row of cut) {
    refuseHeld(row.segment, row.source);
    const parts = [[`${row.key}_full.jpg`, path.join(q4Dir, row.source)]];
    if (!row.fragments) parts.push([`${row.key}_strip.webp`, path.join(cutDir, `${row.key}_strip.webp`)]);
    for (const [name, from] of parts) {
      const plain = await readFile(from), sealed = seal(k, name, plain);
      await writeFile(path.join(outDir, `${name}.enc`), sealed);
      files.push({ name, bytes: plain.length, sha256: sha(plain), enc_sha256: sha(sealed) });
    }
    if (!row.fragments) frames.push({ segment: row.segment, light: row.light, strip: `wsrp/${row.key}_strip.webp`, full: `wsrp/${row.key}_full.jpg`, aspect: row.aspect });
    else frames.push({ segment: row.segment, light: row.light, full: `wsrp/${row.key}_full.jpg`, fragments: true });
  }
  frames.sort((a, b) => a.segment - b.segment || a.light.localeCompare(b.light));
  const index = { version: 1, cipher: "AES-256-GCM, AAD = file name", source: "WSRP 1988 colour recto drum scans, 1/4-scale previews; strip cut-outs by tools/wsrp_strip_cutouts.py", credit: CREDIT, frames, files };
  await writeFile(path.join(outDir, "index.json"), JSON.stringify(index, null, 1) + "\n");
  console.log(`sealed ${files.length} files for ${frames.length} frames into ${outDir}`);
}

async function decrypt(inDir = DEFAULT_ENC, outDir = DEFAULT_OUT) {
  const k = key();
  const index = JSON.parse(await readFile(path.join(inDir, "index.json"), "utf8"));
  await mkdir(outDir, { recursive: true });
  for (const f of index.frames) refuseHeld(f.segment, f.full);
  for (const f of index.files) {
    const segment = +(f.name.match(/^CT(\d+)_/)?.[1] ?? NaN);
    refuseHeld(segment, f.name);
    const plain = open(k, f.name, await readFile(path.join(inDir, `${f.name}.enc`)));
    if (sha(plain) !== f.sha256) throw new Error(`${f.name}: checksum differs after decryption`);
    await writeFile(path.join(outDir, f.name), plain);
  }
  await writeFile(path.join(outDir, "frames.json"), JSON.stringify({ credit: index.credit, frames: index.frames }) + "\n");
  console.log(`opened ${index.files.length} files into ${outDir}`);
}

const [command, ...args] = process.argv.slice(2);
if (command === "encrypt") await encrypt(...args);
else if (command === "decrypt") await decrypt(...args);
else { console.error("usage: wsrp-media.mjs encrypt <q4 folder> <cut-out folder> [out] | decrypt [in] [out]"); process.exit(2); }
