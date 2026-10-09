"""Write volumes.csv: identifier, URL and SHA-256 of every text file read.
usage: python3 -I make_volumes.py DOWNLOADS GETTY_DIR OUT_CSV"""
import csv, gzip, hashlib, json, os, re, sys

dl, getty, out = sys.argv[1:4]
BAD = b"500 Internal Server Error"


def sha(p):
    if not os.path.exists(p):
        return "", 0, False
    b = open(p, "rb").read()
    ok = BAD not in b[:400]
    return hashlib.sha256(b).hexdigest(), len(b), ok


rows = []
for ident in sorted(os.listdir(dl)):
    d = os.path.join(dl, ident)
    if not os.path.isdir(d):
        continue
    tail = ident.split("_", 1)[1]
    role = "general_index (recall check)" if "index" in tail else "searched"
    rec = {"ia_identifier": ident, "role": role, "label": tail,
           "details_url": "https://archive.org/details/" + ident,
           "djvu_txt_url": "https://archive.org/download/%s/%s_djvu.txt" % (ident, ident)}
    notes = []
    for suf, col in (("_djvu.txt", "djvu_txt"), ("_hocr_searchtext.txt.gz", "searchtext"),
                     ("_hocr_pageindex.json.gz", "pageindex"), ("_page_numbers.json", "page_numbers")):
        h, n, ok = sha(os.path.join(d, ident + suf))
        if ok:
            rec[col + "_sha256"] = h
            rec[col + "_bytes"] = n
        else:
            rec[col + "_sha256"] = ""
            rec[col + "_bytes"] = ""
            notes.append("%s: HTTP 500 on every try (9 Oct 2026)" % suf)
    pages = ""
    try:
        pages = len(json.load(gzip.open(os.path.join(d, ident + "_hocr_pageindex.json.gz"))))
    except Exception:
        pass
    rec["leaves"] = pages
    rec["note"] = "; ".join(notes)
    rows.append(rec)
for f in sorted(os.listdir(getty)):
    if not f.endswith("_djvu.txt"):
        continue
    ident = f[:-len("_djvu.txt")]
    h, n, ok = sha(os.path.join(getty, f))
    rows.append({"ia_identifier": ident, "role": "second OCR (recall check only)", "label": "",
                 "details_url": "https://archive.org/details/" + ident,
                 "djvu_txt_url": "https://archive.org/download/%s/%s" % (ident, f),
                 "djvu_txt_sha256": h if ok else "", "djvu_txt_bytes": n if ok else "",
                 "searchtext_sha256": "", "searchtext_bytes": "", "pageindex_sha256": "",
                 "pageindex_bytes": "", "page_numbers_sha256": "", "page_numbers_bytes": "",
                 "leaves": "", "note": "" if ok else "download failed"})
fields = ["ia_identifier", "role", "label", "details_url", "djvu_txt_url", "djvu_txt_sha256", "djvu_txt_bytes",
          "searchtext_sha256", "searchtext_bytes", "pageindex_sha256", "pageindex_bytes",
          "page_numbers_sha256", "page_numbers_bytes", "leaves", "note"]
with open(out, "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print(len(rows))
