# Colab cell B (lane I2, 31 Oct 2026). Run after cell A in the same runtime.
# The Drive connector cannot return files of about 8 MB. This writes, for each PDF:
#   text/<slug>__text_pXXXX-YYYY.jsonl  the text layer, one JSON line per page, files under 250 kB;
#   small/<slug>__sNN_pXXXX-YYYY.pdf  page-range chunks under 2 MB.
import os, json, hashlib, pymupdf
SMALL_MB = 1.8
SMALL = os.path.join(OUT, "small")
os.makedirs(SMALL, exist_ok=True)
for rel in PDFS:
    src = os.path.join(ROOT, rel)
    if not os.path.exists(src):
        print("MISSING:", rel)
        continue
    stem = hexcog2.slug(rel)
    doc = pymupdf.open(src)
    TXT = os.path.join(OUT, "text")
    os.makedirs(TXT, exist_ok=True)
    buf, first, n = [], 1, 0
    def flush(buf, first, last):
        p = os.path.join(TXT, f"{stem}__text_p{first:04d}-{last:04d}.jsonl")
        if not os.path.exists(p):
            open(p, "w").write("".join(buf))
    for i, p in enumerate(doc):
        line = json.dumps({"page": i + 1, "label": p.get_label() or None, "text": p.get_text()}, ensure_ascii=False) + "\n"
        if buf and sum(len(b.encode()) for b in buf) + len(line.encode()) > 250000:
            flush(buf, first, i); n += 1
            buf, first = [], i + 1
        buf.append(line)
    flush(buf, first, doc.page_count); n += 1
    print("text chunks:", stem, n)
    sizes = []
    for i in range(doc.page_count):
        one = pymupdf.open()
        one.insert_pdf(doc, from_page=i, to_page=i)
        sizes.append(len(one.tobytes(garbage=3, deflate=True)))
        one.close()
    ranges, a, tot = [], 0, 0
    for i, s in enumerate(sizes):
        if i > a and tot + s > SMALL_MB * 1e6:
            ranges.append((a, i - 1))
            a, tot = i, 0
        tot += s
    ranges.append((a, doc.page_count - 1))
    parts = []
    for k, (a, b) in enumerate(ranges, 1):
        path = os.path.join(SMALL, f"{stem}__s{k:03d}_p{a + 1:04d}-{b + 1:04d}.pdf")
        if not os.path.exists(path):
            write_range(doc, a, b, path)
        parts.append({"file": os.path.basename(path), "first_page": a + 1, "last_page": b + 1,
                      "bytes": os.path.getsize(path), "sha256": sha256(path)})
    json.dump({"src": rel, "n_pages": doc.page_count, "limit_mb": SMALL_MB, "parts": parts},
              open(os.path.join(SMALL, stem + "__small_manifest.json"), "w"), indent=1, ensure_ascii=False)
    print("small chunks:", stem, len(parts), "parts, max", round(max(p["bytes"] for p in parts) / 1e6, 2), "MB")
    doc.close()
print("CELL B DONE")
