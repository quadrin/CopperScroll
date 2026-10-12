#!/usr/bin/env python3
"""Turn the saved portal pages (scratch folder, outside the repository) into the part-F data tables.

Writes data/volumes.csv (one row per portal item), data/files.csv (one row per downloadable file listed on a
landing page; none of them fetched) and data/fetched_pages.csv (every portal page fetched, with SHA-256).
Abstracts are not written; only their SHA-256 (whitespace collapsed) and their gazetteer hits.
The abstract of a held unit is not screened (HELD_NOS).

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/scripts/prep_data.py <scratch_part_f_dir>
"""
import csv
import datetime
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
sys.path.insert(0, str(HERE))
import common_f  # noqa: E402
import parse_landing  # noqa: E402
import parse_series  # noqa: E402

HELD_NOS = {"5"}  # decided from the title and the abstract's first line only (see NOTES.md)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(scratch):
    scratch = Path(scratch)
    pages = [scratch / "html" / n for n in ("series.html", "series_index.2.html", "series_index.3.html")]
    items = parse_series.parse([str(p) for p in pages])
    landing = {r["landing_id"]: r for r in parse_landing.parse(scratch / "html" / "landing")}
    pats = common_f.patterns()
    vol_rows, file_rows = [], []
    for it in items:
        lid = int(it["landing_url"].rstrip("/").rsplit("/", 1)[1])
        lp = landing.get(lid)
        no = it["no_label"]
        row = {"no_label": no, "title": it["title"], "authors": it["authors"],
               "landing_url": it["landing_url"] + "/", "landing_id": lid, "series_page": it["page"]}
        if lp is None:
            row.update({"landing_fetched": "no (already read elsewhere; not fetched)", "year": "", "pdf_url": "",
                        "pdf_size": "", "n_files": "", "keywords": "", "eisbn": "", "doi": "",
                        "abstract_sha256": "", "abstract_hits": ""})
        else:
            assert lp["heading"].split("|")[0].strip() == no, (lid, lp["heading"])
            ab = " ".join(lp["abstract"].split())
            doi = lp["recommended_citation"].split("DOI:")[-1].split()[0] if "DOI:" in lp["recommended_citation"] else ""
            hits = "" if no in HELD_NOS else common_f.fmt_hits(common_f.hits(ab, pats))
            row.update({"landing_fetched": "yes", "year": lp["publication_date"].split("-")[-1],
                        "pdf_url": lp["pdf_url"], "pdf_size": lp["pdf_size"], "n_files": len(lp["files"]),
                        "keywords": lp["keywords"], "eisbn": lp["identifier"], "doi": doi,
                        "abstract_sha256": sha(ab.encode("utf-8")) if ab else "",
                        "abstract_hits": "(held: not screened)" if no in HELD_NOS else hits})
            for i, f in enumerate(lp["files"]):
                file_rows.append({"no_label": no, "landing_id": lid, "file_index": i, "label": f["label"],
                                  "size": f["size"], "url": f["url"],
                                  "label_hits": common_f.fmt_hits(common_f.hits(f["label"], pats))})
        vol_rows.append(row)
    fetched = []
    for p in pages + sorted((scratch / "html" / "landing").glob("*.html"), key=lambda x: int(x.stem)):
        b = p.read_bytes()
        url = ("https://publications.iaa.org.il/iaareports/" if p.name == "series.html" else
               "https://publications.iaa.org.il/iaareports/" + p.name.replace("series_", "") if p.name.startswith("series_")
               else "https://publications.iaa.org.il/iaareports/%s/" % p.stem)
        fetched.append({"url": url, "http_status": 200, "bytes": len(b), "sha256": sha(b),
                        "saved_utc": datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ")})
    for name, rows in (("volumes.csv", vol_rows), ("files.csv", file_rows), ("fetched_pages.csv", fetched)):
        with open(PART / "data" / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    print(len(vol_rows), len(file_rows), len(fetched))


if __name__ == "__main__":
    main(sys.argv[1])
