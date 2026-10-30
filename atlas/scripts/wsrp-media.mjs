// Encrypt or decrypt the private image sets of the access-controlled atlas.
//
// The repository holds them only as ciphertext, one folder per set under
// ../private-media/ (wsrp-1988, allegro-dqcaas). The key is the GitHub Actions
// secret WSRP_MEDIA_KEY (32 random bytes in base64) and is never committed.
// The public GitHub Pages build never reads these folders.
//
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs encrypt <set name> <source folder>
//   WSRP_MEDIA_KEY=... node scripts/wsrp-media.mjs decrypt [out folder]
//
// Each .enc file: "CSWSRP1" | 12-byte IV | AES-256-GCM ciphertext | 16-byte tag.
// The file name is the additional authenticated data, so files cannot be swapped.
import { createCipheriv, createDecipheriv, createHash, randomBytes } from "node:crypto";
import { mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const PRIVATE = path.resolve(here, "../../private-media");
const DEFAULT_OUT = path.resolve(here, "../protected-media");
const MAGIC = Buffer.from("CSWSRP1");
const IMAGE = /\.(jpe?g|png|tiff?|webp)$/i;

const sha = buf => createHash("sha256").update(buf).digest("hex");
function key() {
  const raw = process.env.WSRP_MEDIA_KEY;
  if (!raw) throw new Error("WSRP_MEDIA_KEY is not set");
  const k = Buffer.from(raw.trim(), "base64");
  if (k.length !== 32) throw new Error("WSRP_MEDIA_KEY must be 32 bytes in base64");
  return k;
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

async function encrypt(set, source) {
  if (!/^[a-z0-9-]+$/.test(set ?? "")) throw new Error("set name: lower case, digits and hyphens");
  const k = key(), outDir = path.join(PRIVATE, set);
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });
  const files = [];
  for (const name of (await readdir(source)).filter(n => IMAGE.test(n)).sort()) {
    const plain = await readFile(path.join(source, name)), sealed = seal(k, name, plain);
    await writeFile(path.join(outDir, `${name}.enc`), sealed);
    files.push({ name, bytes: plain.length, sha256: sha(plain), enc_sha256: sha(sealed) });
  }
  await writeFile(path.join(outDir, "index.json"), JSON.stringify({ version: 2, set, cipher: "AES-256-GCM, AAD = file name", files }, null, 1) + "\n");
  console.log(`sealed ${files.length} files into ${outDir}`);
}

async function decrypt(outRoot = DEFAULT_OUT) {
  const k = key();
  for (const set of (await readdir(PRIVATE, { withFileTypes: true })).filter(d => d.isDirectory()).map(d => d.name)) {
    const inDir = path.join(PRIVATE, set), indexFile = path.join(inDir, "index.json");
    if (!existsSync(indexFile)) continue;
    const index = JSON.parse(await readFile(indexFile, "utf8")), outDir = path.join(outRoot, set);
    await mkdir(outDir, { recursive: true });
    for (const f of index.files) {
      const plain = open(k, f.name, await readFile(path.join(inDir, `${f.name}.enc`)));
      if (sha(plain) !== f.sha256) throw new Error(`${set}/${f.name}: checksum differs after decryption`);
      await writeFile(path.join(outDir, f.name), plain);
    }
    console.log(`opened ${index.files.length} files of ${set}`);
  }
}

const [command, ...args] = process.argv.slice(2);
if (command === "encrypt") await encrypt(...args);
else if (command === "decrypt") await decrypt(...args);
else { console.error("usage: wsrp-media.mjs encrypt <set name> <source folder> | decrypt [out folder]"); process.exit(2); }
