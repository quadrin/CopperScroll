# Colab cell: lane I2 sources (31 Oct 2026). Run in "HEXAGON COG builder v2.ipynb" after cells 1 and 2,
# or alone in a new notebook (it signs in and mounts Drive itself).
# It does two things for each PDF below:
#   A. adds it to the bucket store with hexcog2.do_pdf (one page per PDF + pages.jsonl), then rebuilds index.json;
#   B. writes page-range chunks under 9 MB to Drive "08 Working files/Session chunks 2026-10-31/",
#      so a session without the bucket key can read them through the Drive connector (10 MB limit).
# Restartable: done store units and existing chunk files are skipped.

BUCKET, PROJECT = "copper-scroll-cog-1030", "copper-scroll-cog-1030"
ROOT = "/content/drive/MyDrive/Copper Scroll"
TOOLS = ROOT + "/08 Working files/HEXAGON COG 2026-10-30"
OUT = ROOT + "/08 Working files/Session chunks 2026-10-31"
PDFS = [  # paths relative to ROOT
    "[Erlanger geographische Arbeiten, Sonderband 5] Wolf Dieter Hütteroth, Kamal Abdulfattah - Historical Geography of Palestine, Transjordan and Southern Syria in the Late 16th [sixteenth] Century (1977, Erlangen).pdf",
    "Hebrewbooks_org_32811.pdf",
]
CHUNK_MB = 8.5

import os, sys, json, hashlib, subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pymupdf", "google-cloud-storage"], check=True)
if not os.path.isdir("/content/drive/MyDrive"):
    from google.colab import drive
    drive.mount("/content/drive")
try:
    from google.colab import auth
    auth.authenticate_user()
except Exception as e:
    print("auth skipped:", e)

import pymupdf
sys.path.insert(0, TOOLS)
import hexcog2
hexcog2.ROOT = ROOT


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(16 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_range(doc, a, b, path):
    one = pymupdf.open()
    one.insert_pdf(doc, from_page=a, to_page=b)
    one.save(path, garbage=3, deflate=True)
    one.close()
    return os.path.getsize(path)


def chunk(rel):
    src = os.path.join(ROOT, rel)
    stem = hexcog2.slug(rel)
    man_path = os.path.join(OUT, stem + "__manifest.json")
    if os.path.exists(man_path):
        print("chunks done:", rel)
        return json.load(open(man_path))
    os.makedirs(OUT, exist_ok=True)
    doc = pymupdf.open(src)
    n = doc.page_count
    sizes = []  # single-page sizes, for a first guess at the ranges
    for i in range(n):
        one = pymupdf.open()
        one.insert_pdf(doc, from_page=i, to_page=i)
        sizes.append(len(one.tobytes(garbage=3, deflate=True)))
        one.close()
    ranges, a, tot = [], 0, 0
    for i, s in enumerate(sizes):
        if i > a and tot + s > CHUNK_MB * 1e6:
            ranges.append((a, i - 1))
            a, tot = i, 0
        tot += s
    ranges.append((a, n - 1))
    parts, k = [], 0
    todo = list(ranges)
    while todo:
        a, b = todo.pop(0)
        k += 1
        path = os.path.join(OUT, f"{stem}__part{k:02d}_p{a + 1:04d}-{b + 1:04d}.pdf")
        size = write_range(doc, a, b, path)
        if size > 9.5e6 and b > a:  # too big: split the range in two and redo it
            os.remove(path)
            k -= 1
            m = (a + b) // 2
            todo[:0] = [(a, m), (m + 1, b)]
            continue
        parts.append({"file": os.path.basename(path), "first_page": a + 1, "last_page": b + 1,
                      "bytes": size, "sha256": sha256(path)})
        print(f"  {parts[-1]['file']}  {size / 1e6:.1f} MB")
    text_pages = sum(1 for p in doc if len(p.get_text()) > 50)
    man = {"src": rel, "src_bytes": os.path.getsize(src), "src_sha256": sha256(src), "n_pages": n,
           "text_pages": text_pages, "chunk_limit_mb": CHUNK_MB, "parts": parts}
    doc.close()
    json.dump(man, open(man_path, "w"), indent=1, ensure_ascii=False)
    print(f"chunked {rel}: {n} pages, {text_pages} with text, {len(parts)} parts")
    return man


store = hexcog2.GCSStore(BUCKET, PROJECT)
for rel in PDFS:
    if not os.path.exists(os.path.join(ROOT, rel)):
        print("MISSING:", rel)
        continue
    print("==", rel)
    try:
        hexcog2.do_pdf(rel, store)            # A. bucket store
    except Exception as e:
        print("store FAILED:", repr(e))
    try:
        chunk(rel)                            # B. Drive chunks
    except Exception as e:
        print("chunk FAILED:", repr(e))
hexcog2.build_index(store)
print("ALL DONE")
