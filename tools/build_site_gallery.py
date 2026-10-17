#!/usr/bin/env python3
"""Build the atlas photo gallery from the archived site-photograph set.

Input:  research/assets/plans/site-photos-2026-10-17/manifest.json and its JPEGs.
Output: atlas/research/assets/plans/site-photos-2026-10-17/ (byte-identical mirror),
        atlas/public/dossiers/site-photos/gallery/<id>.webp (long side <= 1600 px, quality 80),
        atlas/app/atlas-site-gallery.json (display fields only).

Run from the repository root:  python3 -I tools/build_site_gallery.py
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SET = "site-photos-2026-10-17"
SRC = ROOT / "research/assets/plans" / SET
MIRROR = ROOT / "atlas/research/assets/plans" / SET
WEB = ROOT / "atlas/public/dossiers/site-photos/gallery"
OUT = ROOT / "atlas/app/atlas-site-gallery.json"
DISPLAY = ["id", "placeId", "kind", "web", "webWidth", "webHeight", "title", "author", "credit",
           "license", "licenseUrl", "sourceUrl", "date", "alt", "caption", "relevance", "entryIds"]
ALLOWED = ("CC BY", "CC0", "Public domain", "No known restrictions")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    items = json.loads((SRC / "manifest.json").read_text())
    known = {p["id"] for p in json.loads((ROOT / "atlas/app/atlas-data.json").read_text())["places"]}
    WEB.mkdir(parents=True, exist_ok=True)
    seen, gallery = set(), []
    for item in items:
        assert item["id"] not in seen, item["id"]
        seen.add(item["id"])
        assert item["placeId"] in known, item["placeId"]
        assert item["license"].startswith(ALLOWED), (item["id"], item["license"])
        assert "NC" not in item["license"] and "ND" not in item["license"], item["id"]
        jpg = SRC / item["archive"]
        assert sha(jpg) == item["archiveSha256"], f"hash mismatch {jpg}"
        web = WEB / f"{item['id']}.webp"
        with Image.open(jpg) as im:
            im = im.convert("RGB")
            im.thumbnail((1600, 1600), Image.LANCZOS)
            im.save(web, "WEBP", quality=80, method=6)
            w, h = im.size
        item.update(web=web.name, webWidth=w, webHeight=h, webSha256=sha(web))
        gallery.append({k: item[k] for k in DISPLAY})
    (SRC / "manifest.json").write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n")
    stale = {p.name for p in WEB.glob("*.webp")} - {g["web"] for g in gallery}
    for name in stale:
        (WEB / name).unlink()
    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    shutil.copytree(SRC, MIRROR)
    order = {p["id"]: i for i, p in enumerate(json.loads((ROOT / "atlas/app/atlas-data.json").read_text())["places"])}
    gallery.sort(key=lambda g: (order[g["placeId"]], g["kind"] != "modern photograph", g["id"]))
    OUT.write_text(json.dumps(gallery, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(gallery)} photographs, {len({g['placeId'] for g in gallery})} places")
    return 0


if __name__ == "__main__":
    sys.exit(main())
