"""Build the image library of the access-controlled atlas (3D scroll view).

Usage (repository root):
  python3 -I tools/build_scroll_media.py <out folder> [--private <decrypted private-media folder>]

Writes <out>/index.json and every image the 3D view can show:
  wsrp88    WSRP 1988 colour recto masters, 1/4-scale previews (private, decrypted)
  usc       USC Digital Library public previews of the same 1988 photographs:
            all 23 segments, recto and verso, colour and b&w (images/previews)
  allegro   John Allegro's 1955-56 photographs, 2017 DQCAAS scans (private, decrypted)
  facsimile USC 2013 photographs of the EDF metal facsimile, by column (images/previews)
  rti       USC RTI poster images of the facsimile, by column (images/previews)
  djd3      DJD III (1962) plates: Milik's photographs and hand copies, and the
            plates of the object (research/assets/plans/djdIII1962/plates-volume.pdf)
  commons   The Jordan Museum photograph of strip 13 (CC BY-SA 4.0, already public)
  model     Registered model (private, decrypted, set scroll-model): each strip
            unrolled along its surface, with every layer on the same grid. The
            measurements come from research/sources/usc_copper_scroll_images/
            scroll_model_fit.json and are copied into index.json as "model".

Colour recto and verso photographs of segments also get a strip cut-out (WebP
with a transparent background) so the 3D model can carry them.
Needs Pillow, numpy, scipy and poppler (pdftoppm).
"""
import argparse, csv, glob, json, os, re, shutil, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
THUMB = 260
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
USC_LIGHT = {
    "lft top light": "RLT", "ctr top light": "RCT", "rt top light": "RRT",
    "lft bot light": "RLB", "ctr bot light": "RCB", "rt bot light": "RRB",
    "top light": "RT", "bot light": "RB", "edge top light": "RET", "edge top lt": "RET",
    "edge bot light": "REB", "edge bot lt": "REB", "ctr sd light": "RCS",
    "bot ctr": "RBC", "top ctr": "RTC", "fragments": "FRS", "frgs": "FRS",
    "left": "L", "right": "R", "": "",
}
MODEL_LAYERS = {
    "MT": "top light, left, centre and right frames blended", "MB": "bottom light, left, centre and right frames blended",
    "MR": "relief from the top and bottom light", "MN": "black-and-white negative (1988)",
    "MF": "EDF facsimile on the strip", "MA": "Allegro photograph (1955–56) on the strip",
    "MM": "Milik's hand copy on the relief", "MX": "EDF radiograph on the strip",
}
SETS = [
    {"id": "model", "label": "Registered model (all layers on one grid)", "level": "segment", "date": "2026",
     "credit": "Each strip unrolled along its surface from the left, centre and right frames of the WSRP 1988 masters (B. and K. Zuckerman, West Semitic Research; courtesy the Department of Antiquities, Jordan). Further layers on the same grid: USC previews of the 1988 b&w negatives; the EDF facsimile (West Semitic Research 2013 photographs, USC Digital Library); John Allegro's 1955–56 photographs (courtesy of the John Allegro estate © Judith Brown, via DQCAAS); Milik's hand copies (DJD III, 1962); radiographs printed in Brizemeure, Lacoudre and Puech 2006 (STDJ 55). Fitted automatically; private study copy, not for publication."},
    {"id": "wsrp88", "label": "WSRP 1988 masters", "level": "segment", "date": "1988",
     "credit": "Photographs by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary. Courtesy the Department of Antiquities, Jordan. 1/4-scale previews of the drum-scanned colour transparencies; private study copy."},
    {"id": "usc", "label": "USC library previews (1988)", "level": "segment", "date": "1988",
     "credit": "Photographs by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary. Courtesy the Department of Antiquities, Jordan. USC Digital Library public previews (InscriptiFact); educational use only."},
    {"id": "allegro", "label": "Allegro photographs (1955–56)", "level": "segment", "date": "1955–56",
     "credit": "Courtesy of the John Allegro estate © Judith Brown, licensed via the Dispersed Qumran Cave Archives and Archival Sources (DQCAAS) Project. 2017 scans of prints; study copy, not for publication."},
    {"id": "facsimile", "label": "EDF facsimile (2013 photos)", "level": "column", "date": "2013",
     "credit": "Photographs of the EDF metal facsimile by West Semitic Research (USC Digital Library, InscriptiFact); educational use only. A copy of the scroll, not the original."},
    {"id": "rti", "label": "EDF facsimile RTI posters", "level": "column", "date": "2013",
     "credit": "Static poster images of West Semitic Research RTI captures of the EDF facsimile (USC Digital Library)."},
    {"id": "djd3", "label": "DJD III plates (1962)", "level": "column", "date": "1962",
     "credit": "Baillet, Milik and de Vaux, with H. W. Baker, Les 'petites grottes' de Qumrân (DJD III), Oxford 1962, plates volume."},
    {"id": "commons", "label": "Jordan Museum photograph", "level": "segment", "date": "2020",
     "credit": "Osama Shukir Muhammed Amin, 2020, Wikimedia Commons, CC BY-SA 4.0."},
]


def cutout(path, loose=False):
    """The strip as the largest tinted, not-black, not-white region near the middle of the frame.
    loose: for versos, whose dark green corrosion fails the tint test; fills larger gaps."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w, _ = im.shape
    v = im.max(axis=2); mn = im.min(axis=2)
    sat = (v - mn) / np.maximum(v, 1)
    if loose:
        metal = (v > 34) & (v < 232) & (sat > .1) & ~((sat > .55) & (v > 150))
    else:
        metal = (v > 48) & (v < 232) & (sat > .07) & ~((sat > .55) & (v > 110))
    metal = ndimage.binary_opening(metal, structure=np.ones((5, 5)))
    k = 17 if loose else 7
    mask = ndimage.binary_closing(metal, structure=np.ones((k, k)))
    labels, _ = ndimage.label(mask)
    best, best_area = None, 0
    for i, sl in enumerate(ndimage.find_objects(labels), 1):
        if sl is None:
            continue
        ys, xs = sl
        if xs.start == 0 or xs.stop == w or (ys.stop - ys.start) < .45 * h:
            continue
        area = int((labels[sl] == i).sum())
        centre = (xs.start + xs.stop) / 2
        score = area * max(.05, 1 - abs(centre - w / 2) / (w / 2))
        if score > best_area:
            best, best_area = (i, sl), score
    if best is None:
        return None
    i, (ys, xs) = best
    region = ndimage.binary_erosion(ndimage.binary_fill_holes(labels == i)[ys, xs], iterations=1)
    rgba = np.dstack([im[ys, xs].astype(np.uint8), (region * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), round((xs.stop - xs.start) / (ys.stop - ys.start), 4)


class Library:
    def __init__(self, out):
        self.out = Path(out); self.images = []
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)

    def add(self, set_id, src, name, strip=False, loose=False, **meta):
        """Copy (or convert) one image, make its thumbnail and optional strip cut-out."""
        folder = self.out / set_id; (folder / "t").mkdir(parents=True, exist_ok=True)
        src = Path(src)
        im = Image.open(src)
        if src.suffix.lower() in (".jpg", ".jpeg") and im.mode in ("RGB", "L"):
            shutil.copyfile(src, folder / f"{name}.jpg")
        else:
            im.convert("RGB").save(folder / f"{name}.jpg", quality=88)
        full = f"{set_id}/{name}.jpg"
        t = im.convert("RGB"); t.thumbnail((THUMB, THUMB * 2)); t.save(folder / "t" / f"{name}.jpg", quality=80)
        item = {"id": f"{set_id}:{name}", "set": set_id, "full": f"media/{full}", "thumb": f"media/{set_id}/t/{name}.jpg", "w": im.width, "h": im.height, **meta}
        if strip:
            got = cutout(folder / f"{name}.jpg", loose)
            if got:
                img, aspect = got
                img.save(folder / f"{name}_strip.webp", "WEBP", quality=86, method=5)
                item.update(strip=f"media/{set_id}/{name}_strip.webp", aspect=aspect)
        self.images.append(item)
        return item

    def add_registered(self, set_id, src, name, **meta):
        """A layer of the registered model: already a strip cut-out, kept as it is."""
        folder = self.out / set_id; (folder / "t").mkdir(parents=True, exist_ok=True)
        im = Image.open(src)
        shutil.copyfile(src, folder / f"{name}.webp")
        t = Image.new("RGB", im.size, (29, 26, 22)); t.paste(im.convert("RGBA"), (0, 0), im.convert("RGBA")); t.thumbnail((THUMB, THUMB * 2)); t.save(folder / "t" / f"{name}.jpg", quality=80)
        path = f"media/{set_id}/{name}.webp"
        item = {"id": f"{set_id}:{name}", "set": set_id, "full": path, "thumb": f"media/{set_id}/t/{name}.jpg", "w": im.width, "h": im.height,
                "strip": path, "aspect": round(im.width / im.height, 4), **meta}
        self.images.append(item)
        return item


def build(out, private):
    lib = Library(out)
    private = Path(private) if private else None

    # WSRP 1988 masters (decrypted). Names: CT<n>_<LIGHT>_full.jpg
    wsrp = private / "wsrp-1988" if private else None
    if wsrp and wsrp.exists():
        for p in sorted(wsrp.glob("CT*_full.jpg")):
            m = re.match(r"CT(\d+)_([A-Z]+)_full\.jpg$", p.name)
            seg, light = int(m.group(1)), m.group(2)
            lib.add("wsrp88", p, f"CT{seg}_{light}", strip=light not in ("FRS", "RFR"),
                    segment=seg, side="recto", light=light, film="colour", title=f"Segment {seg} · recto · {light}")

    # Registered model (decrypted). Names: S<nn>_<LAYER>.webp
    model = private / "scroll-model" if private else None
    fit = None
    if model and model.exists():
        fit_file = ROOT / "research/sources/usc_copper_scroll_images/scroll_model_fit.json"
        for p in sorted(model.glob("S*_M?.webp")):
            m = re.match(r"S(\d+)_(M[A-Z])\.webp$", p.name)
            seg, layer = int(m.group(1)), m.group(2)
            lib.add_registered("model", p, f"S{seg:02d}_{layer}", segment=seg, side="recto", light=layer,
                               film="b&w" if layer in ("MN", "MX", "MA") else "colour", title=f"Segment {seg} · {MODEL_LAYERS.get(layer, layer)}")
        if fit_file.exists() and any(i["set"] == "model" for i in lib.images):
            fit = json.loads(fit_file.read_text(encoding="utf-8"))["strips"]

    # USC public previews of the 1988 photographs, and of the facsimile.
    index = list(csv.DictReader(open(ROOT / "research/sources/usc_copper_scroll_images/index.csv", encoding="utf-8")))
    have = {Path(p).stem: p for p in glob.glob(str(ROOT / "images/previews/*/*.jpg"))}
    for r in index:
        p = have.get(r["uc_identifier"])
        if not p:
            continue
        if r["item_type"].startswith("original"):
            seg, side = int(r["cut"]), r["side"].lower()
            film = "colour" if r["film"] == "colour" else "b&w"
            light = USC_LIGHT.get(r["lighting_as_titled"].strip(), r["lighting_as_titled"].strip().upper())
            lib.add("usc", p, r["uc_identifier"], strip=(film == "colour" and light != "FRS"), loose=(side == "verso"),
                    segment=seg, side=side, light=light, film=film, title=r["title"], link=r["usc_link"])
        elif r["item_type"].startswith("facsimile"):
            col = int(r["column"]) - 1
            lib.add("facsimile", p, r["uc_identifier"], column=col, section=r["section"], shot=r["rti_shot"], title=r["title"], link=r["usc_link"])
        elif r["item_type"].startswith("RTI"):
            col = int(r["column"]) - 1 if r["column"].isdigit() else None
            lib.add("rti", p, r["uc_identifier"], column=col, section=r["section"], title=r["title"], link=r["usc_link"])

    # Allegro / DQCAAS scans (decrypted). Segment(s) from the DQCAAS number: C.21A.3, C.22.1, C.21-23.1, C.10A.2
    allegro = private / "allegro-dqcaas" if private else None
    if allegro and allegro.exists():
        for p in sorted(x for x in allegro.iterdir() if x.suffix.lower() in (".jpg", ".jpeg", ".png", ".tif", ".tiff")):
            m = re.search(r"[Cc]\.?\s*(\d+)(?:\s*-\s*(\d+))?", p.stem)
            segs = list(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1)) if m else []
            name = re.sub(r"[^A-Za-z0-9._-]+", "_", p.stem)
            lib.add("allegro", p, name, segment=segs[0] if segs else None, segments=segs, title=p.stem)

    # DJD III plates: hand copy on the even page, photograph on the odd page of each column.
    pdf = ROOT / "research/assets/plans/djdIII1962/plates-volume.pdf"
    tmp = Path(out) / "_djd"; tmp.mkdir(exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "150", "-jpeg", "-jpegopt", "quality=86", "-f", "55", "-l", "84", str(pdf), str(tmp / "p")], check=True)
    pages = {int(re.search(r"(\d+)$", Path(x).stem).group(1)): x for x in glob.glob(str(tmp / "p-*.jpg"))}
    objects = {55: "Pl. XLIII · the two copper rolls before opening", 56: "Pl. XLIV · the sawing machine and the cut segments",
               57: "Pl. XLV", 58: "Pl. XLVI · photographic montage of the segments of the small roll", 59: "Pl. XLVII · the cutting at Manchester", 84: "Pl. LXXII"}
    for page, src in sorted(pages.items()):
        if page in objects:
            lib.add("djd3", src, f"p{page}", column=None, kind="object", title=objects[page], page=page)
        elif 60 <= page <= 83:
            col = (page - 60) // 2
            kind = "handcopy" if page % 2 == 0 else "photo"
            lib.add("djd3", src, f"p{page}", column=col, kind=kind, page=page,
                    title=f"Col. {ROMAN[col]} · {'Milik hand copy' if kind == 'handcopy' else 'photograph'} (PDF p. {page})")
    shutil.rmtree(tmp)

    # The public Commons photograph of strip 13.
    commons = ROOT / "atlas/public/scroll/strip13.webp"
    if commons.exists():
        lib.add("commons", commons, "strip13", strip=False, segment=13, side="recto", title="Strip 13 in the Jordan Museum (2020)",
                link="https://commons.wikimedia.org/wiki/File:Strip_13,_part_of_the_Copper_Dear_Sea_Scrolls,_from_Qumran_Cave_3,_Jordan_Museum.jpg")

    used = {i["set"] for i in lib.images}
    index_out = {"version": 2, "sets": [s for s in SETS if s["id"] in used], "images": lib.images}
    if fit:
        index_out["model"] = {"strips": {k: {"arc": v["arc_cm"] / 100, "chord": v["chord_cm"] / 100, "height": v["height_cm"] / 100, "measured": v["measured"], "tangent": v["tangent"]} for k, v in fit.items()}}
    (Path(out) / "index.json").write_text(json.dumps(index_out, ensure_ascii=False, separators=(",", ":")))
    counts = {s: sum(1 for i in lib.images if i["set"] == s) for s in used}
    strips = sum(1 for i in lib.images if "strip" in i)
    print(f"{len(lib.images)} images, {strips} strip cut-outs: {counts}")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("out"); a.add_argument("--private")
    args = a.parse_args()
    build(args.out, args.private)
