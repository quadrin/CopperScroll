#!/usr/bin/env python3
"""Select WBADB rows (PLAN.md S10) inside the box whose name, components or comments contain a cave word.

Run: python3 -I wbadb_extract.py WBADB_data1.xlsx OUT_JSON
The workbook is not committed (third-party data). Its SHA-256 must equal the frozen value.
X/Y are Old Israel Grid metres without the false northing (EPSG:28191), as PLAN.md 4.5 states.
Each selected row carries a 'cites_inventoried' list: the inventoried sources (S1-S9, S11) its survey reference
or bibliography names, by the patterns below; rows citing any of them are crosswalks only (PLAN.md 4.2).
"""
import hashlib
import json
import re
import sys

import pandas as pd

SHA = "3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b"
BOX = (180000, 197000, 91000, 150000)
CAVE = re.compile(r"\bcaves?\b|\bgrott|\bcavern|\bmugh?ar|\bm['ʿ]?gh?arat|\bme['ʿ]?ar(a|at)\b", re.I)
PERIOD_FLAGS = {"LP", "MP", "UP", "EP", "Natufian", "Neo", "PPN", "PN", "Chal", "EB", "EB1", "EB2_3", "IB", "MB", "MB2a", "MB2b_c",
                "LB", "IA", "IA1", "IA2", "Per", "Hel", "Rom", "Byz", "EIs", "Med", "Ott"}
INVENTORIED = {
    "S1-S3 de Vaux / DJD III / Reed": r"de ?Vaux|Baillet|DJD|Reed",
    "S4 Atiqot 41 (1993 survey)": r"Atiqot 41|'Atiqot 41|Atiqot XLI|\b(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV)/\d+\b|Sion 2002|Eshel and Zissu 2002|Yattah|Dahari 2002|Wexler"
                                  r"|(Barshad and Shaked|Hirschfeld and Riklin|Itah et al\.?|Baruch et al\.?|Abeles|Aronshtam|Tal and Oron|Tal et al\.?|Ibrahim|Cohen and Yisrael|Peleg and Hameiri|Eisenberg|Weiss|Nahlieli|Feig|Melamed|Segal) 2002|Operation Scroll",
    "S5 ESI cave survey (Patrich)": r"ESI 6|ESI 7|ESI 3: ?6|Patrich 198[5-9]|Patrich and Arubas|Arubas",
    "S7 Bar-Adon 1989": r"Bar-?Adon 1989",
    "S9 ASI maps": r"Patrich 1994a|Map of Deir Mar Saba|Map of 'Ein Gedi|Map of Wadi Qelt|Map of Kalia|Goldfus|Golani|Hadas|Sion 2013|Sion 199[3-7]|Map of Wadi el-Makokh",
    "S11 Zissu 2023": r"Zissu 2023",
}


def main(xlsx, out):
    h = hashlib.sha256(open(xlsx, "rb").read()).hexdigest()
    if h != SHA:
        sys.exit(f"hash mismatch {h}")
    rows = []
    for sheet in ("Surveyed", "Excavations"):
        d = pd.read_excel(xlsx, sheet_name=sheet)
        for r in d.to_dict("records"):
            try:
                x, y = float(r["X"]), float(r["Y"])
            except (TypeError, ValueError):
                continue
            if not (BOX[0] <= x <= BOX[1] and BOX[2] <= y <= BOX[3]):
                continue
            txt = " ; ".join(str(r.get(k, "")) for k in ("Site_Name", "Other_Names", "Site_Components", "More_Components", "Comments", "More_Comments"))
            if not CAVE.search(txt):
                continue
            refs = " ; ".join(str(r.get(k, "")) for k in ("Survey_Ref", "Publication_Bibliography", "More_Bibliography", "Comments", "More_Comments", "Site_Components"))
            cites = [k for k, pat in INVENTORIED.items() if re.search(pat, refs)]
            rows.append({"sheet": sheet, "index": int(r["Index"]), "X": x, "Y": y,
                         **{k: (None if (isinstance(v, float) and v != v) else v) for k, v in r.items() if k not in PERIOD_FLAGS},
                         "cites_inventoried": cites})
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(len(rows), sum(1 for r in rows if not r["cites_inventoried"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
