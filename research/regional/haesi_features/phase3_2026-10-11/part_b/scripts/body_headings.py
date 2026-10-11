#!/usr/bin/env python3
"""Body-heading sweep for HA part B (completes the table-of-contents screen).

Some in-volume tables of contents omit reports (HA 76 omits the Judean Desert survey on p. 40). This sweep
lists every short heading-like line of the layout text (1-8 words, a blank line before it, no full stop at the
end) whose words match the frozen gazetteer, the region-wide terms or the A3 variants, and which does not
repeat a heading already in screen_auto.csv for that page range. Each listed line is opened by hand and decided
in data/body_heading_review.csv (same report as a screened heading, sub-heading, caption or running text);
bare group words and imprint lines are classified automatically by the build.

Run: python3 -I .../part_b/scripts/body_headings.py TEXTDIR   (after screen_partb.py)
Writes part_b/data/body_heading_hits.csv. Deterministic.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import screen_partb as S  # noqa: E402

DATA = S.DATA


def toks(s):
    """Hebrew words of two or more letters, normalised (no years, permit numbers or punctuation)."""
    return {w for w in S.textlib.norm_he(S.prenorm(s)).split() if len(w) >= 2 and re.fullmatch(r"[א-ת']+", w)}


def main(textdir):
    params = S.common.plan_params()
    pats = S.patterns(params)
    vols = S.read_csv(DATA / "volumes.csv")
    scr = S.read_csv(DATA / "screen_auto.csv")
    out = []
    for vrow in vols:
        vol = S.textlib.Volume(textdir, vrow["key"])
        toc_pages = {int(x) for x in vrow["toc_pages"].split(";")} if vrow["toc_pages"] else set()
        heads = [r for r in scr if r["volume"] == vrow["label"]]
        for pi, page in enumerate(vol.layout_pages):
            pg = pi + 1
            if pg in toc_pages:
                continue
            prev_blank = True
            for li, l in enumerate(page):
                s = l.strip()
                if not s:
                    prev_blank = True
                    continue
                words = s.split()
                cand = prev_blank and 1 <= len(words) <= 8 and len(s) <= 60 and not s.endswith(".") and \
                    re.search(r"[א-ת]", s) and not re.match(r"^\d", s)
                prev_blank = False
                if not cand:
                    continue
                h = S.hits(s, pats)
                if not h:
                    continue
                # already a screened heading on these pages?
                same = []
                btok = toks(s)
                for r in heads:
                    if not r["pdf_pages"]:
                        continue
                    a, b = (int(x) for x in r["pdf_pages"].split("-"))
                    if a - 1 <= pg <= b:
                        ttok = toks(r["title_he"])
                        if ttok and len(ttok & btok) >= max(1, 0.6 * len(ttok)):
                            same.append(r["screen_id"])
                out.append(dict(volume=vrow["label"], pdf_page=pg, layout_line=li + 1, text=s,
                                title_hits=";".join("%s:%s" % (z, ",".join(x)) for z, x in sorted(h.items())),
                                matches_screen_id=";".join(same)))
    S.write_csv(DATA / "body_heading_hits.csv", ["volume", "pdf_page", "layout_line", "text", "title_hits", "matches_screen_id"], out)
    print(len(out), "heading-like lines with gazetteer hits;", sum(1 for r in out if not r["matches_screen_id"]), "not matching a screened heading")


if __name__ == "__main__":
    main(sys.argv[1])
