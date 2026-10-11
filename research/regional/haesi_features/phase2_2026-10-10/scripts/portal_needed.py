#!/usr/bin/env python3
"""List the portal volume PDFs (publications.iaa.org.il) that phase 2 could not read in the browser.

The PDFs open in Chrome's viewer (the JavaScript check passes in a real browser), but the viewer's text cannot
be read by the page-text tool, so the brief's route (c) stops here. This script writes portal_pdfs_needed.csv
from phase-1 data/corpus.csv and data/screen_candidates.csv, so the owner can download them in one batch.

Priority (INFERENCE; for ordering the owner's download only):
  A  holds a Tier-1 record (HA 28-29) or >= 5 phase-1 candidates in phase-2 region groups
  B  1-4 phase-1 candidates in region groups
  C  no phase-1 candidate in region groups (still needed for the whole-volume regional screen)
Region groups (phase-1 labels whose places lie in the phase-2 region): JER_ALL, JERICHO_ALL, QUMRAN_ALL,
R_JD_CLIFFS, R_WADI_QELT, mar_saba, hyrcania, buqeia, natuf, tekoa_herodium, gerizim, ein_samiya, kh_yanun,
beth_horon. Outside: beth_shean, carmel_siah, ibziq, kh_salhab, beit_kahil, kuhlah.

Run from the repository root: python3 -I research/regional/haesi_features/phase2_2026-10-10/scripts/portal_needed.py
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
P1 = LANE.parent
REGION_GROUPS = {"JER_ALL", "JERICHO_ALL", "QUMRAN_ALL", "R_JD_CLIFFS", "R_WADI_QELT", "mar_saba", "hyrcania",
                 "buqeia", "natuf", "tekoa_herodium", "gerizim", "ein_samiya", "kh_yanun", "beth_horon"}
SERIES = {"ha_hebrew_series": "HA", "esi_english_series": "ESI", "ha_esi_bilingual_series": "HA-ESI"}
LOCAL_COPIES = {"esi_english_series_15": "ESI 2", "esi_english_series_16": "ESI 3", "esi_english_series_18": "ESI 5",
                "esi_english_series_2": "ESI 6", "esi_english_series_20": "ESI 7-8", "esi_english_series_3": "ESI 9",
                "esi_english_series_8": "ESI 15", "ha_hebrew_series_17": "HA 40", "ha_hebrew_series_76": "HA 45",
                "ha_hebrew_series_28": "HA 59-60"}
TIER1 = {"ha_hebrew_series_64": "HA 28-29 (Tananir): Tier-1 record, arrival register README step 5"}
FIELDS = ["series", "volume", "year", "item_url", "pdf_url", "pdf_size", "phase1_candidates", "phase1_candidates_in_region",
          "phase1_read", "priority", "note"]


def main():
    cands = Counter()
    creg = Counter()
    for r in csv.DictReader(open(P1 / "data" / "screen_candidates.csv", encoding="utf-8")):
        item = r["item_key"].split("#")[0]
        cands[item] += 1
        if {g.strip() for g in r["groups"].split(";")} & REGION_GROUPS:
            creg[item] += 1
    out = []
    for r in csv.DictReader(open(P1 / "data" / "corpus.csv", encoding="utf-8")):
        if not r["pdf_url"]:
            continue
        key = r["item_key"]
        series = SERIES.get(key.rsplit("_", 1)[0], key)
        vol = r["title"].split("/")[0].replace("Hadashot Arkheologiyot", "").replace("Excavations and Surveys in Israel", "")
        vol = vol.replace("Ḥadashot Arkheologiyot חדשות ארכיאולוגיות", "").strip()
        note = []
        if key in TIER1:
            note.append(TIER1[key])
        if key in LOCAL_COPIES:
            note.append(f"also on the owner's Mac ({LOCAL_COPIES[key]}); read in phase 2 from that copy")
        if key == "ha_hebrew_series_2":
            note.append("portal test (plan 3.2): opened in Chrome on 11 Oct 2026; the viewer showed the cover (HA 2-3, 1962) "
                        "but the page-text tool read no text; nothing saved; route stopped")
        prio = "A" if (key in TIER1 or creg[key] >= 5) else ("B" if creg[key] else "C")
        if key in LOCAL_COPIES:
            prio = "local copy"
        out.append(dict(series=series, volume=vol, year=r["year"], item_url=r["item_url"], pdf_url=r["pdf_url"],
                        pdf_size=r["pdf_size"], phase1_candidates=cands[key], phase1_candidates_in_region=creg[key],
                        phase1_read="yes" if r["status"].startswith("read") else "no", priority=prio,
                        note="; ".join(note)))
    order = {"A": 0, "B": 1, "C": 2, "local copy": 3}
    out.sort(key=lambda o: (order[o["priority"]], -int(o["phase1_candidates_in_region"]), o["series"], o["year"]))
    with open(LANE / "portal_pdfs_needed.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(len(out), Counter(o["priority"] for o in out))


if __name__ == "__main__":
    main()
