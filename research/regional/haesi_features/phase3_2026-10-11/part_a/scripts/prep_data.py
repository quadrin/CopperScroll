#!/usr/bin/env python3
"""Turn the hash-only outputs copied back from the Mac into part_a/data CSVs (local_sources.csv, local_spans.csv,
heading_signals.csv). Each copied file was checked against the SHA-256 of the Mac original before use.

usage: prep_data.py SCRATCH_DIR PART_A_DIR
SCRATCH_DIR holds (all outside the repository):
  hc4.tsv            file, PDF pages, raw-text SHA-256, layout-text SHA-256   (from hashcheck.tsv)
  no_text_pages.tsv  base, page count + 1, pages whose text layer has under 50 characters
  jobs_ascii.tsv     the job list sent to the Mac (span_jobs.py): its quote hashes are kept so that the tests can
                     tell whether a quote changed after it was checked
  spans_compact.tsv  report id, raw lines, span SHA-256, PDF pages, quote status (from mac/batch_spans.py)
  sig_compact.tsv    vol, TOC n, heading PDF page, how located (F/W/C/N), map refs in item text, body hits by zone
                     (from mac/signals.py)
"""
import csv, glob, json, sys
S = sys.argv[1]
PART = sys.argv[2]

vols = list(csv.DictReader(open(PART + "/data/volumes.csv", encoding="utf-8")))
part = {r["local_file"]: r["sha256"] for r in csv.DictReader(open(PART + "/../partition.csv", encoding="utf-8")) if r["part"] == "A"}
hc = {}
for l in open(S + "/hc4.tsv", encoding="utf-8"):
    f, pages, raw, lay = l.rstrip("\n").split("\t")
    hc[f] = (pages, raw, lay)


def tf_id(local_file):
    b = local_file[len("IAA_HA_"):-4]
    v, y = b.rsplit("_", 1)
    if v == "029-028":
        return "HA28-29"
    return "HA" + "-".join("%02d" % int(x) for x in v.split("-"))


notext = {}
for l in open(S + "/no_text_pages.tsv", encoding="utf-8"):
    v, n, pages = (l.rstrip("\n").split(" ") + [""])[:3]
    notext["IAA_" + v + ".pdf"] = pages

rows = []
for v in sorted(vols, key=lambda r: tf_id(r["local_file"])):
    f = v["local_file"]
    pages, raw, lay = hc[f]
    # drop the empty tail page that pdftotext adds after the last form feed
    nt = [p for p in notext[f].split(",") if p and int(p) <= int(pages)]
    rows.append(dict(text_file=tf_id(f), series="HA", volume=v["volume"], year=v["year"], portal_item_url=v["item_url"],
                     local_file_name=f, pdf_sha256=part[f], duplicate_file_same_sha256="", text_tool="pdftotext -raw (also -layout)",
                     raw_text_sha256=raw, printed_page_offset="", use="whole volume screened; in-region reports read" +
                     ("; Tier-1 record (extraction only first: tier1_HA28-29_extraction.md)" if f == "IAA_HA_029-028_1969.pdf" else ""),
                     layout_text_sha256=lay, pdf_pages=pages, pdf_pages_without_text_layer=";".join(nt)))
fields = ["text_file", "series", "volume", "year", "portal_item_url", "local_file_name", "pdf_sha256", "duplicate_file_same_sha256",
          "text_tool", "raw_text_sha256", "printed_page_offset", "use", "layout_text_sha256", "pdf_pages", "pdf_pages_without_text_layer"]
with open(PART + "/data/local_sources.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)

reps = {}
for p in sorted(glob.glob(PART + "/data/coding_*.json")):
    for r in json.load(open(p, encoding="utf-8")):
        reps[r["report_id"]] = r
qhash = {}
for l in open(S + "/jobs_ascii.tsv", encoding="ascii"):
    rid, _, _, qs = (l.rstrip("\n").split("\t") + [""])[:4]
    qhash[rid] = qs
srows = []
for l in open(S + "/spans_compact.tsv", encoding="utf-8"):
    rid, lines, sha, pages, st = l.rstrip("\n").split("\t")
    r = reps[rid]
    assert r["text_lines"] == lines, rid
    assert len(st) == len(r["features"]), rid
    nf = [r["features"][i]["quote"] for i, c in enumerate(st) if c == "N"]
    srows.append(dict(report_id=rid, text_file=r["text_file_id"], text_lines=lines, text_sha256=sha, n_quotes=len(st),
                      quotes_not_found=" | ".join(nf), quote_check=st, pdf_pages=pages, quote_hashes=qhash[rid]))
assert set(x["report_id"] for x in srows) == set(reps)
with open(PART + "/data/local_spans.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=["report_id", "text_file", "text_lines", "text_sha256", "n_quotes", "quotes_not_found",
                                       "quote_check", "pdf_pages", "quote_hashes"], lineterminator="\n")
    w.writeheader(); w.writerows(sorted(srows, key=lambda x: x["report_id"]))

short = {}
for v in vols:
    b = v["local_file"][len("IAA_HA_"):-4]
    short[b.rsplit("_", 1)[0]] = "HA_" + b
HOW = {"F": "full title", "W": "one title word", "C": "title after the colon", "N": "not found"}
grows = []
for l in open(S + "/sig_compact.tsv", encoding="utf-8"):
    v, n, pg, how, refs, hits = l.rstrip("\n").split("\t")
    grows.append(dict(vol_file=short[v], toc_n=n, heading_pdf_page=pg, heading_located=HOW[how],
                      map_refs_in_item_text=refs, body_gazetteer_hits_by_zone=hits))
with open(PART + "/data/heading_signals.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(grows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(grows)
print(len(rows), len(srows), len(grows))
