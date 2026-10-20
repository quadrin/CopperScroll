#!/usr/bin/env python3
"""Build the atlas photo gallery from the archived site-photograph sets.

Input:  research/assets/plans/site-photos-2026-10-17/manifest.json and its JPEGs (Commons, LoC Matson);
        research/assets/plans/kidron-field-2026-10-19/manifest.json: the records or video frames that carry
        an "atlasGallery" object (the project owner's own photographs, shown with his permission, no open licence).
Output: atlas/research/assets/plans/<set>/ (byte-identical mirrors),
        atlas/public/dossiers/site-photos/gallery/<id>.webp (long side <= 1600 px, quality 80) and <id>-thumb.webp (240 px),
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
FIELD_SETS = ["kidron-field-2026-10-19"]
WEB = ROOT / "atlas/public/dossiers/site-photos/gallery"
OUT = ROOT / "atlas/app/atlas-site-gallery.json"
DISPLAY = ["id", "placeId", "kind", "web", "thumb", "webWidth", "webHeight", "title", "author", "credit",
           "license", "licenseUrl", "sourceUrl", "date", "alt", "caption", "relevance", "entryIds"]
ALLOWED = ("CC BY", "CC0", "Public domain", "No known restrictions")
# The owner's own photographs: shown with his permission; no open licence is asserted or implied.
OWNER_LICENSE = "Used with permission (no open licence)"
KIND_ORDER = {"project field photograph": 0, "project video frame": 0, "modern photograph": 1}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(jpg: Path, item_id: str) -> dict:
    web = WEB / f"{item_id}.webp"
    with Image.open(jpg) as im:
        im = im.convert("RGB")
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(web, "WEBP", quality=80, method=6)
        w, h = im.size
    thumb = WEB / f"{item_id}-thumb.webp"
    with Image.open(jpg) as im:
        im = im.convert("RGB")
        im.thumbnail((240, 240), Image.LANCZOS)
        im.save(thumb, "WEBP", quality=72, method=6)
    return dict(web=web.name, webWidth=w, webHeight=h, webSha256=sha(web), thumb=thumb.name)


def mirror(src: Path) -> None:
    target = ROOT / "atlas/research/assets/plans" / src.name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target)


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
        item.update(render(jpg, item["id"]))
        gallery.append({k: item[k] for k in DISPLAY})
    (SRC / "manifest.json").write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n")
    mirror(SRC)
    for name in FIELD_SETS:
        src = ROOT / "research/assets/plans" / name
        manifest = json.loads((src / "manifest.json").read_text())
        assert "No open licence" in manifest["rights"], name
        frames = [f for v in manifest.get("videos", []) for f in v["frames"]]
        for record in manifest["records"] + frames:
            item = record.get("atlasGallery")
            if not item:
                continue
            assert item["id"] not in seen, item["id"]
            seen.add(item["id"])
            assert item["placeId"] in known, item["placeId"]
            assert item["author"] == manifest["photographer"], item["id"]
            assert item["license"] == OWNER_LICENSE and item["licenseUrl"] is None, item["id"]
            assert "CC" not in item["credit"] + item["license"] + item["caption"], item["id"]
            jpg = src / record["file"]
            assert sha(jpg) == record["sha256"], f"hash mismatch {jpg}"
            item.update(render(jpg, item["id"]))
            gallery.append({k: item[k] for k in DISPLAY})
        (src / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
        mirror(src)
    stale = {p.name for p in WEB.glob("*.webp")} - {g["web"] for g in gallery} - {g["thumb"] for g in gallery}
    for name in stale:
        (WEB / name).unlink()
    order = {p["id"]: i for i, p in enumerate(json.loads((ROOT / "atlas/app/atlas-data.json").read_text())["places"])}
    gallery.sort(key=lambda g: (order[g["placeId"]], KIND_ORDER.get(g["kind"], 2), g["id"]))
    OUT.write_text(json.dumps(gallery, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(gallery)} photographs, {len({g['placeId'] for g in gallery})} places")
    return 0


if __name__ == "__main__":
    sys.exit(main())
