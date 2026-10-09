"""Download OCR text derivatives for QS 1869-1914 issue items from archive.org.
Usage: python3 -I download.py SEARCH_JSON OUTDIR
Text only: _djvu.txt, _hocr_searchtext.txt.gz, _hocr_pageindex.json.gz, _page_numbers.json."""
import json, os, sys, subprocess, time, hashlib

SUFFIXES = ["_djvu.txt", "_hocr_searchtext.txt.gz", "_hocr_pageindex.json.gz", "_page_numbers.json"]

def items(search_json):
    d = json.load(open(search_json))
    out = []
    for x in d["response"]["docs"]:
        i = x["identifier"]
        tail = i.split("_", 1)[1]
        y = tail[:4]
        if not y.isdigit():
            continue
        if not (1869 <= int(y) <= 1914):
            continue
        if "index" in tail or "contents" in tail:
            if tail in ("1869-1892_index", "1893-1910_index"):
                out.append(i)
            continue
        out.append(i)
    return sorted(out)

def fetch(url, dest):
    for k in range(5):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "300", "-o", dest, "-w", "%{http_code}", url], capture_output=True, text=True)
        if r.stdout.strip() == "200" and os.path.getsize(dest) > 0:
            return "200"
        time.sleep(3 + 3 * k)
    return r.stdout.strip() + " " + r.stderr.strip()[:200]

def main():
    sj, outdir = sys.argv[1], sys.argv[2]
    log = []
    for ident in items(sj):
        d = os.path.join(outdir, ident)
        os.makedirs(d, exist_ok=True)
        for suf in SUFFIXES:
            dest = os.path.join(d, ident + suf)
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                continue
            url = "https://archive.org/download/%s/%s%s" % (ident, ident, suf)
            st = fetch(url, dest)
            if st != "200":
                log.append((ident, suf, st))
                print("FAIL", ident, suf, st, flush=True)
        print("ok", ident, flush=True)
    json.dump(log, open(os.path.join(outdir, "_download_failures.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
