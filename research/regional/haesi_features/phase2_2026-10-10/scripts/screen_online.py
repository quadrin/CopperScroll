#!/usr/bin/env python3
"""Screen the HA-ESI online report lists (vols 116-137) against the frozen gazetteer (PLAN.md section 4).

Input:  data/online_titles.csv (every report listed on the 22 volume pages; transcription checked against
        the SHA-256 computed in the browser, data/online_lists.csv)
        data/screen_amendment_A2.csv (post-freeze manual additions, labelled exploratory; AMENDMENTS.md A2)
Output: data/online_candidates.csv (one row per candidate, with screen, zone by title, tier and reading order)

Run from the repository root: python3 -I research/regional/haesi_features/phase2_2026-10-10/scripts/screen_online.py
Deterministic.
"""
import csv
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402

DATA = HERE.parent / "data"
FIELDS = ["report_id", "volume", "year", "list_position", "title", "url", "screen", "title_hits", "zone_by_title",
          "tier", "order_key"]


def tier_of(zone, title):
    if zone in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "REGION_WIDE"):
        return "T1"
    if zone == "Z4_JERUSALEM_HILLS":
        return "T3" if common.norm(title).startswith(" jerusalem ") else "T2"
    return ""


def main():
    pats = common.gazetteer_patterns()
    titles = list(csv.DictReader(open(DATA / "online_titles.csv", encoding="utf-8")))
    amend = {r["report_id"]: r for r in csv.DictReader(open(DATA / "screen_amendment_A2.csv", encoding="utf-8"))}
    out = []
    for t in titles:
        hits = common.title_hits(t["title"], pats)
        screen = ""
        if hits:
            screen = "S-ON1"
            # Zone by title: a specific zone beats the region-wide term; Z1-Z3 beat Z4 (desert names inside
            # Jerusalem titles, e.g. "Jerusalem, Survey of Nahal Darga").
            zs = [z for z in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS") if z in hits]
            zone = zs[0] if zs else "REGION_WIDE"
        elif t["report_id"] in amend:
            screen = "S-ON2 (amendment A2, exploratory)"
            zone = amend[t["report_id"]]["zone_by_title"]
        else:
            continue
        tier = tier_of(zone, t["title"])
        out.append(dict(report_id=t["report_id"], volume=t["volume"], year=t["year"], list_position=t["list_position"],
                        title=t["title"],
                        url=f"https://hadashot.iaa.org.il/report_detail_eng.aspx?id={t['report_id']}",
                        screen=screen,
                        title_hits="; ".join(f"{z}:{'/'.join(h)}" for z, h in sorted(hits.items())) if hits else
                        amend[t["report_id"]]["reason"],
                        zone_by_title=zone, tier=tier,
                        order_key=hashlib.sha256(t["report_id"].encode()).hexdigest()))
    missing = set(amend) - {o["report_id"] for o in out}
    assert not missing, f"amendment ids not in the lists: {missing}"
    out.sort(key=lambda r: (r["tier"], r["order_key"]))
    with open(DATA / "online_candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(len(titles), "titles;", len(out), "candidates;", dict(Counter(o["tier"] for o in out)),
          dict(Counter(o["screen"][:5] for o in out)))


if __name__ == "__main__":
    main()
