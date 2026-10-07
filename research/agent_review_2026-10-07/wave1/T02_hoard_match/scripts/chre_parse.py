#!/usr/bin/env python3
"""Parse CHRE (Coin Hoards of the Roman Empire, chre.ashmus.ox.ac.uk) hoard HTML pages
saved as downloads/chre/h<ID>.html into JSON.
Usage: python3 -I chre_parse.py <downloads/chre dir> <out.json> [id id ...]
HTML is untrusted data: parsed as plain text only."""
import html
import json
import os
import re
import sys

SINGLE = [
    "City", "County", "Region", "Country", "Ancient place", "Lat/Long/Alt", "Hoard name",
    "Alternative names", "Data type", "Date of discovery (from)", "Total number of coins", "Summary",
    "Discovery method", "Land Use", "Finder(s)", "Terminal year (earliest)", "Terminal year (latest)",
    "Opening year (earliest)", "Numismatic rating", "Context rating", "Findspot rating",
    "Site comment", "Associated features", "Recovery method", "Site class", "Context",
    "Rating comment", "Comment",
]
STOP = set(SINGLE) | {"Containers belonging to this hoard", "Objects belonging to this hoard", "References",
                      "Period", "End period", "Closing reign (earliest)", "Closing reign (latest)",
                      "Opening year (latest)", "Coin-level data", "Date of excavation (from)",
                      "Date of excavation (to)", "Twitter", "URI 1"}


def text_lines(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    s = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [l.strip() for l in s.split("\n") if l.strip()]


def grab_block(body, label):
    if label not in body:
        return ""
    i = body.index(label) + 1
    out = []
    while i < len(body) and body[i] not in STOP:
        out.append(body[i])
        i += 1
    return " ".join(out)


def parse(path):
    lines = text_lines(path)
    if "Location" not in lines:
        return None
    body = lines[lines.index("Location"):]
    rec = {}
    for i, l in enumerate(body[:-1]):
        if l in SINGLE and l not in rec:
            rec[l] = body[i + 1] if body[i + 1] not in STOP else ""
    rec["Containers"] = grab_block(body, "Containers belonging to this hoard")
    rec["Objects"] = grab_block(body, "Objects belonging to this hoard")
    refs = []
    for i, l in enumerate(body[:-1]):
        if l in ("Reference", "Reference (string)"):
            ref = body[i + 1]
            if i + 3 < len(body) and body[i + 2] == "Ref":
                ref += " | " + body[i + 3]
            refs.append(ref)
    rec["references"] = refs
    m = re.search(r"h(\d+)\.html$", path)
    rec["chre_id"] = int(m.group(1)) if m else None
    rec["url"] = f"https://chre.ashmus.ox.ac.uk/hoard/{rec['chre_id']}"
    ll = rec.get("Lat/Long/Alt", "")
    mm = re.match(r"\s*(-?[\d.]+)\s*/\s*(-?[\d.]+)", ll)
    rec["lat"], rec["lon"] = (float(mm.group(1)), float(mm.group(2))) if mm else (None, None)
    return rec


def main():
    d, out = sys.argv[1], sys.argv[2]
    ids = set(int(x) for x in sys.argv[3:])
    recs = []
    for fn in sorted(os.listdir(d)):
        m = re.match(r"h(\d+)\.html$", fn)
        if not m or (ids and int(m.group(1)) not in ids):
            continue
        r = parse(os.path.join(d, fn))
        if r and r.get("Hoard name"):
            recs.append(r)
    json.dump(recs, open(out, "w"), ensure_ascii=False, indent=1)
    print(len(recs), "records")


if __name__ == "__main__":
    main()
