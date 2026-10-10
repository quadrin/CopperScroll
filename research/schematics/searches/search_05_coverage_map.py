"""Past searches 05: where the recorded searches were, against the atlas's candidate places.

Sources (all read when the sheet is built):
- atlas/app/atlas-data.json: 39 places (lat/lon, region, precision) and 61 entries with their
  candidate lists (placeId, status, confidence).
- research/history/salvage_records/searches.csv (27 ledger rows S01-S27) and README.md (coded values;
  "joins should keep near rows separate"; negative rows S03, S10, S17).
- research/models/search_effectiveness/looks.csv (46 looks; looks_v2.csv differs only at non-atlas
  places), results.json (phantom_coverage, plan.phantom_pd_threshold) and README.md section 5
  ("Phantom coverage").
- research/history/devaux1952_cave_points/devaux1952_cave_points.csv, point 8 = 3Q (WGS84 given there).
- research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/grid_conversions_v2.csv, row
  iv17_abu_saraj_group (WGS84 for the Abu Saraj group reference 190300/144150 that S20 cites).

No datum transform is done here. A ledger row is drawn at a WGS84 point the repo gives for it, else at
the atlas point of its place_id; a row with neither is listed as not drawn. The sheet identifies nothing.
"""
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, GREY, REPO, page, out_path  # noqa: E402

KM_PER_DEG = 111.32          # as atlas/app/atlas-geography.ts (111320 m per degree of latitude)
SCROLL = {"scroll_deposit_search", "scroll_motivated", "scroll_find_site"}
PURPOSES = SCROLL | {"manuscript_survey", "excavation_of_named_place", "unknown", "claim_only"}

# ================================================================== data
atlas = json.loads((REPO / "atlas" / "app" / "atlas-data.json").read_text(encoding="utf-8"))
places = {p["id"]: p for p in atlas["places"]}
entry_order = {e["id"]: i for i, e in enumerate(atlas["entries"])}
assert len(places) == 39 and len(atlas["entries"]) == 61
cands = {pid: [] for pid in places}
for e in atlas["entries"]:
    for cd in e["candidates"]:
        cands[cd["placeId"]].append((e["id"], cd["status"]))
for pid in cands:
    cands[pid].sort(key=lambda t: entry_order[t[0]])
assert all(cands[pid] for pid in places), "every atlas place should be some entry's candidate"
assert {st for v in cands.values() for _, st in v} == {"preferred", "possible", "weak"}
NOCOORD = sorted(pid for pid, p in places.items() if p["lat"] is None)
assert NOCOORD == ["jer_shaveh", "jordan_ford", "tekoa_herodium"], NOCOORD

SR = REPO / "research" / "history" / "salvage_records"
with open(SR / "searches.csv", encoding="utf-8", newline="") as fh:
    ledger = sorted(csv.DictReader(fh), key=lambda r: r["search_id"])
L = {r["search_id"]: r for r in ledger}
assert len(ledger) == 27 and sorted(L) == [f"S{i:02d}" for i in range(1, 28)]
for r in ledger:
    assert r["purpose"] in PURPOSES, r["purpose"]
    assert r["place_match"] in ("exact", "near", "none")
    assert (r["place_match"] == "none") == (r["place_id"] == ""), r["search_id"]
    assert r["place_id"] == "" or r["place_id"] in places, r["place_id"]
NEGATIVE = sorted(r["search_id"] for r in ledger if r["result"] == "negative")
assert NEGATIVE == ["S03", "S10", "S17"]

# WGS84 points that the repo itself gives for a ledger row (checked against the row's own text)
pts = {}
with open(REPO / "research" / "history" / "devaux1952_cave_points" / "devaux1952_cave_points.csv",
          encoding="utf-8", newline="") as fh:
    p8 = {r["point"]: r for r in csv.DictReader(fh)}["8"]
assert f"WGS84 {p8['lat']}, {p8['lon']}" in L["S01"]["coords"]
pts["S01"] = (float(p8["lat"]), float(p8["lon"]))
assert L["S02"]["coord_crs"] == "WGS84" and L["S02"]["coords"].startswith("31.741119, 35.459027")
pts["S02"] = (31.741119, 35.459027)
assert "WGS84 31.68216, 35.41991" in L["S05"]["coords"] and L["S06"]["coords"] == "as S05"
pts["S05"] = pts["S06"] = (31.68216, 35.41991)
assert L["S25"]["coord_crs"] == "WGS84" and L["S25"]["coords"].startswith("31.8734, 35.4313")
pts["S25"] = (31.8734, 35.4313)
GC = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/grid_conversions_v2.csv"
with open(GC, encoding="utf-8", newline="") as fh:
    g = {r["id"]: r for r in csv.DictReader(fh)}["iv17_abu_saraj_group"]
assert (g["oig_e"], g["oig_n"]) == ("190300", "144150") and "190300/144150" in L["S20"]["coords"]
pts["S20"] = (float(g["lat"]), float(g["lon"]))

drawn_at = {}      # search_id -> (lat, lon, "own" | "place")
unmapped = []
for r in ledger:
    sid = r["search_id"]
    if sid in pts:
        drawn_at[sid] = (*pts[sid], "own")
    elif r["place_id"] and places[r["place_id"]]["lat"] is not None:
        # no coordinates, or Palestine grid only: drawn at the atlas point of the place
        assert not r["coords"] or r["coords"] == "as S09" or "28191" in r["coord_crs"], sid
        p = places[r["place_id"]]
        drawn_at[sid] = (p["lat"], p["lon"], "place")
    else:
        unmapped.append(sid)
assert unmapped == ["S03", "S04", "S16", "S19", "S24", "S26"], unmapped
assert len(drawn_at) == 21 and all(not L[s]["place_id"] for s in unmapped)

with_search = {}
for r in ledger:
    if r["place_id"]:
        with_search.setdefault(r["place_id"], []).append(r["search_id"])
EXACT = sorted(pid for pid, ss in with_search.items() if any(L[s]["place_match"] == "exact" for s in ss))
NEAR_ONLY = sorted(pid for pid in with_search if pid not in EXACT)
SCROLL_PL = sorted(pid for pid, ss in with_search.items() if any(L[s]["purpose"] in SCROLL for s in ss))
QS_EXACT = [s for s in with_search["kh_qumran"] if L[s]["purpose"] in SCROLL and L[s]["place_match"] == "exact"]
QS_NEAR = [s for s in with_search["kh_qumran"] if L[s]["purpose"] in SCROLL and L[s]["place_match"] == "near"]
assert QS_EXACT == ["S17"] and QS_NEAR == ["S09", "S10", "S11", "S13", "S14", "S15"]

# looks table (search-effectiveness layer)
SE = REPO / "research" / "models" / "search_effectiveness"
NUM = ("coverage", "p_recognise", "p_report", "p_survive")
res = json.loads((SE / "results.json").read_text(encoding="utf-8"))
THR = res["plan"]["phantom_pd_threshold"]
assert THR == 0.2
with open(SE / "looks.csv", encoding="utf-8", newline="") as fh:
    looks = sorted(csv.DictReader(fh), key=lambda r: r["look_id"])
assert len(looks) == 46


def row_pd(r):
    if any(r[k] == "" for k in NUM):
        return None
    return math.prod(float(r[k]) for k in NUM)


looks_at = {}
for r in looks:
    if r["place_id"] in places:
        looks_at.setdefault(r["place_id"], []).append(r)
with open(SE / "looks_v2.csv", encoding="utf-8", newline="") as fh:
    v2 = {r["look_id"]: r for r in csv.DictReader(fh)}
for rs in looks_at.values():          # v2 changes only rows that are not at atlas places
    for r in rs:
        assert v2[r["look_id"]] == r
assert all((row_pd(r) or 0) < THR for rs in looks_at.values() for r in rs)
assert sorted(r["look_id"] for r in looks if (row_pd(r) or 0) >= THR) == ["L03", "L04"]
assert {r["place_id"] for r in looks if r["look_id"] in ("L03", "L04")} == {"ein_feshkha", "ein_ghuweir"}
assert not {"ein_feshkha", "ein_ghuweir"} & set(places)
phantom = sorted({(p["place"], p["look_id"]) for p in res["phantom_coverage"]
                  if p["reading_set"] == res["plan"]["main_reading_set"] and p["place"] in places})
PH = {}
for pid, lid in phantom:
    PH.setdefault(pid, []).append(lid)
assert PH == {"tell_es_sultan": ["L09", "L13", "L25", "L32", "L35", "L36"]}, PH
assert PH["tell_es_sultan"] == [r["look_id"] for r in looks_at["tell_es_sultan"] if r["result"] != "reported"]
REP = {pid: [r["look_id"] for r in rs if r["result"] == "reported"] for pid, rs in looks_at.items()}
assert REP["hyrcania"] == ["L46"] and REP["jericho_palaces"] == ["L45"] and REP["kh_qumran"] == ["L42"]
assert len(REP["tell_es_sultan"]) == 10
LOOKS_ONLY = sorted(pid for pid in looks_at if pid not in with_search)


def rep_text(pid):
    """'L45: a feature reported (entry 29)' for a place whose only looks row is one reported row."""
    (lid,) = REP[pid]
    (r,) = [r for r in looks_at[pid] if r["look_id"] == lid]
    return f"{lid}: a feature reported (entry {r['entry_id']})"
NOTHING = sorted(pid for pid in places if pid not in with_search and pid not in looks_at)

# the counts printed on the sheet
N_PL = len(places)
assert N_PL == 39 and N_PL - len(NOCOORD) == 36
assert len(with_search) == 4 and EXACT == ["gerizim", "kh_qumran"] and NEAR_ONLY == ["ain_duk", "doq"]
assert SCROLL_PL == ["kh_qumran"]
assert LOOKS_ONLY == ["hyrcania", "jericho_palaces", "tell_es_sultan"]
assert len(NOTHING) == 32 and len(with_search) + len(LOOKS_ONLY) + len(NOTHING) == N_PL
assert set(NOCOORD) <= set(NOTHING)
assert all(places[p]["region"] == "jerusalem" for p in places if p.startswith("jer_"))
JER = sorted(p for p in places if places[p]["region"] == "jerusalem")
assert len(JER) == 15 and set(JER) <= set(NOTHING)
assert {s for s, (la, lo, h) in drawn_at.items() if la > 32} == {"S07", "S08"}

# short descriptions of the rows (from who / where_name / looked_at); years come from the row itself
DESC = {
    "S01": "cave survey, 3Q point", "S02": "de Vaux excavations", "S05": "Allegro",
    "S06": "Cave Research Center", "S07": "Bull, Tell er-Ras", "S08": "Magen, summit",
    "S09": "Bar-Adon, Twin Cave", "S10": "Twin Cave", "S11": "Cave 3Q",
    "S12": "Patrich, cliff survey", "S13": "Cave 13, juglet", "S14": "Jones's pit",
    "S15": "Jones, Column area", "S17": "Barfield probe", "S18": "Magen and Peleg",
    "S20": "Abu Saraj cliffs (IV/11)", "S21": "Quruntul cliff (V/49)",
    "S22": "Quruntul east cliff", "S23": "escarpment survey", "S25": "Ketef Jericho (no place)",
    "S27": "Gutfeld and Ovadia",
    "S03": "Allegro: trench at Kh. Qumran, monument at Kh. Mird (sheets 02, 03).",
    "S04": "Allegro, Mazin building; not a candidate place. Year disputed.",
    "S16": "Jones, north of Qumran, for Gilgal.",
    "S19": "IAA, Wadi ed-Daliyeh to Nahal Deragot (region rows S20–S25).",
    "S24": "IAA, Kidron outlet (XIV/2); grid ref only; not Mar Saba.",
    "S26": "IAA, Judean Desert cliffs.",
}
assert sorted(DESC) == sorted(L)
assert "Mird" in L["S03"]["where_name"] and "Qumran" in L["S03"]["where_name"]
assert "Mar Saba" in L["S24"]["coverage_notes"] and "Gilgal" in L["S16"]["looked_at"]
assert "Daliyeh" in L["S19"]["looked_at"] and "Mazin" in L["S04"]["where_name"]


def years(r):
    a, b = r["when_start"][:4], r["when_end"][:4]
    if not b or b == a:
        return a
    return f"{a}–{b[2:]}" if a[:2] == b[:2] else f"{a}–{b}"


DISPUTED = {"S04", "S05"}      # the ledger keeps 1960 against Allegro's "winter of 1961" open
assert "Date conflict" in L["S04"]["notes"] and "winter of 1961" in L["S05"]["when_text"]


def chip_text(sid):
    r = L[sid]
    t = f"{DESC[sid]}, {years(r)}" + (" (claim)" if r["kind"] == "CLAIM" else "")
    return t + (" (start year disputed)" if sid in DISPUTED and sid in drawn_at else "")


# ================================================================== drawing helpers
def proj(lat_top, lon_left, x0, y0, s, lat_c):
    kx = KM_PER_DEG * math.cos(math.radians(lat_c)) * s
    ky = KM_PER_DEG * s
    return lambda lat, lon: (x0 + (lon - lon_left) * kx, y0 + (lat_top - lat) * ky)


def rad(pid):
    return 3.0 * math.sqrt(len(cands[pid]))


FILL = "#d8d2c9"


def place_dot(x, y, pid, small=False):
    r = 1.8 if small else rad(pid)
    if not small and pid in looks_at:
        c.circle(x, y, r + 6.5, stroke=GREY, width=1.2, dash="3 2.5")
    c.circle(x, y, r, fill=FILL, stroke=GREY, width=1.0, fill_opacity=0.85)
    if not small and pid in with_search:
        c.circle(x, y, r + 2.6, stroke=BLUE, width=2.0)


def glyph(x, y, scroll, filled, k=4.4):
    f = BLUE if filled else P["panel"]
    if scroll:
        k += 0.9
        c.path(f"M{x:.1f},{y - k:.1f} L{x + k:.1f},{y:.1f} L{x:.1f},{y + k:.1f} L{x - k:.1f},{y:.1f} Z",
               fill=f, stroke=BLUE, width=1.5)
    else:
        c.rect(x - k + 0.6, y - k + 0.6, 2 * k - 1.2, 2 * k - 1.2, fill=f, stroke=BLUE, width=1.5)


LH = 14.0
CW = 5.25      # rough text width per character at 10.5 px (layout only; measured on the render)


def chips(x, y, sids, size=10.5):
    """Chips, one row per search, first baseline at y. Returns [(y_mid, x_end)] per row."""
    out = []
    for i, sid in enumerate(sids):
        r = L[sid]
        yy = y + i * LH
        glyph(x + 5, yy - 3.8, r["purpose"] in SCROLL, r["place_match"] == "exact")
        c.text(x + 14, yy, sid, size, P["ink"], 700)
        t = chip_text(sid)
        c.text(x + 39, yy, t, size, P["sub"])
        out.append((yy - 3.8, x + 39 + len(t) * CW))
    return out


def search_point(x, y):
    c.circle(x, y, 2.7, fill=BLUE, stroke=P["panel"], width=0.8)


def lbl(x, y, lines, anchor=None, size=10.5, weight=None, col=None, lh=None):
    lines = [lines] if isinstance(lines, str) else lines
    for i, s in enumerate(lines):
        c.text(x, y + i * (lh or size * 1.24), s, size, col or P["sub"], weight if i == 0 else None, anchor=anchor)


def pname(pid, x, y, anchor=None, extra=None, size=10.5, split=False):
    """Place name: ink if the place has a ledger search or a look, else grey; bold if a ledger search."""
    col = P["ink"] if (pid in with_search or pid in looks_at) else P["sub"]
    lines = places[pid]["shortName"].split(" · ") if split else [places[pid]["shortName"]]
    for i, s in enumerate(lines):
        c.text(x, y + 12.5 * i, s, size, col, 600 if pid in with_search else None, anchor=anchor)
    for i, s in enumerate(extra or []):
        c.text(x, y + 12.5 * (i + len(lines)), s, 10, P["sub"], anchor=anchor)


def bearing_km(a, b):
    la, lb = places[a], places[b]
    dy = (lb["lat"] - la["lat"]) * KM_PER_DEG
    dx = (lb["lon"] - la["lon"]) * KM_PER_DEG * math.cos(math.radians(la["lat"]))
    ang = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    words = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return math.hypot(dx, dy), words[int((ang + 11.25) // 22.5) % 16]


def lead(x1, y1, x2, y2, col=None):
    c.line(x1, y1, x2, y2, col or P["muted"], 0.8)


# ================================================================== page
c = page("05", "where the recorded searches were, against the atlas's candidate places",
         "Three maps to scale, north up, from WGS84 lat/lon (equirectangular, x scaled by cos latitude). "
         "No base map: the repo has no Dead Sea or Jordan outline.")
TOP, BOTTOM = 100, 810

# ------------------------------------------------------------------ panel 1: whole area
ox, oy, ow, oh = S.panel(c, 40, TOP, 290, BOTTOM - TOP, "Whole area",
                         ["36 places with coordinates; in A and B, dots only."])
s1 = 2.4
P1 = proj(32.555, 34.60, ox, oy + 8, s1, 32.08)
A_BOX = (31.917, 35.323, 31.645, 35.5636)         # inset A extent (lat_top, lon_left, lat_bottom, lon_right)
B_BOX = (31.7825, 35.2310, 31.7660, 35.2430)      # inset B extent
in_box = lambda b, p: b[2] <= p["lat"] <= b[0] and b[1] <= p["lon"] <= b[3]  # noqa: E731
xa1, ya1 = P1(A_BOX[0], A_BOX[1])
xa2, ya2 = P1(A_BOX[2], A_BOX[3])
c.rect(xa1, ya1, xa2 - xa1, ya2 - ya1, stroke=P["sub"], width=1.0, dash="4 3")
c.text(xa2 + 5, ya1 + 10, "A", 12, P["ink"], 700)
jl = [places[p] for p in JER if places[p]["lat"] is not None]
xb1, yb1 = P1(max(p["lat"] for p in jl) + 0.012, min(p["lon"] for p in jl) - 0.016)
xb2, yb2 = P1(min(p["lat"] for p in jl) - 0.012, max(p["lon"] for p in jl) + 0.016)
c.rect(xb1, yb1, xb2 - xb1, yb2 - yb1, stroke=P["sub"], width=1.0, dash="4 3")
c.text(xb1 - 5, yb2 - 1, "B", 12, P["ink"], 700, anchor="end")
c.text(xb1 - 18, yb2 - 1, "Jerusalem", 10.5, P["sub"], anchor="end")
for pid in sorted(places):
    p = places[pid]
    if p["lat"] is None:
        continue
    x, y = P1(p["lat"], p["lon"])
    place_dot(x, y, pid, small=in_box(A_BOX, p) or p["region"] == "jerusalem")
OV = {  # pid: (dx, dy, anchor, split)
    "beth_shean": (-8, 4, "end", False), "ibziq": (8, -2, None, False), "kh_salhab": (-7, 6, "end", False),
    "beth_horon": (-6, -17, "end", True), "tell_el_ful": (-7, 0, "end", False), "natuf": (-7, 0, "end", True),
}
for pid, (dx, dy, an, sp) in sorted(OV.items()):
    x, y = P1(places[pid]["lat"], places[pid]["lon"])
    pname(pid, x + dx, y + dy, an, split=sp)
gx, gy = P1(places["gerizim"]["lat"], places["gerizim"]["lon"])
pname("gerizim", gx + 11, gy + 4)
rows = chips(gx - 70, gy + 30, ["S07", "S08"])
lead(gx, gy + rad("gerizim") + 3, gx, rows[0][0] - 8, BLUE)
S.north_arrow(c, ox + 16, oy + 60)
S.scale_bar(c, ox + 36, oy + 62, 20 * s1, "0", "20 km")

# ------------------------------------------------------------------ B: Jerusalem enlarged
by0 = oy + 268
c.rect(ox, by0, ow, oy + oh - by0, fill=P["panel"], stroke=P["border"], width=1.0, rx=4)
c.text(ox + 8, by0 + 18, "B — Jerusalem, enlarged", 12.5, P["ink"], 700)
c.text(ox + 8, by0 + 34, "No ledger search, no look.", 10.5, P["sub"])
s2 = 128.0
P2 = proj(B_BOX[0], B_BOX[1], ox + 70, by0 + 52, s2, 31.776)
B_WEST = {"jer_bethesda": ["Bethesda ·", "St Anne’s"], "jer_temple": ["Temple", "enclosure"],
          "jer_tyropoeon": ["Tyropoeon", "valley"], "jer_south_wall": ["Southern", "Temple wall"],
          "jer_siloam": ["Silwan pool &", "tunnel outlet"], "jer_bir_ayyub": ["Bir Ayyub /", "En-Rogel"]}
B_EAST = {"jer_gethsemane": ["Gethsemane"], "jer_east_gate": ["Eastern gate", "& wall"],
          "jer_kidron_mon": ["Kidron", "monuments"], "jer_se_corner": ["Southeastern", "Temple slope"],
          "jer_kidron_east": ["Silwan", "necropolis"]}
for d in (B_WEST, B_EAST):
    for pid, lines in d.items():
        assert in_box(B_BOX, places[pid]) and " ".join(lines) == places[pid]["shortName"], pid
for pid in sorted(set(B_WEST) | set(B_EAST)):
    x, y = P2(places[pid]["lat"], places[pid]["lon"])
    place_dot(x, y, pid)


def column(items, xcol, anchor, gap=3.0, lh=12.0):
    """Stack labels in a column near their points' heights, without overlap; draw leaders."""
    items = sorted(items, key=lambda t: t[1])
    ycur = -1e9
    for px, py, lines, r in items:
        h = len(lines) * lh
        top = max(py - lh / 2 - 2, ycur + gap)
        ycur = top + h
        lbl(xcol, top + lh - 3, lines, anchor, 10, None, P["sub"], lh)
        ex = xcol + (4 if anchor == "end" else -4)
        sx = px + (-r - 1 if anchor == "end" else r + 1)
        lead(sx, py, ex, top + lh / 2 - 1)


west_x = min(P2(places[p]["lat"], places[p]["lon"])[0] for p in B_WEST) - 22
column([(*P2(places[p]["lat"], places[p]["lon"]), B_WEST[p], rad(p)) for p in B_WEST], west_x, "end")
east_x = max(P2(places[p]["lat"], places[p]["lon"])[0] for p in B_EAST) + 18
column([(*P2(places[p]["lat"], places[p]["lon"]), B_EAST[p], rad(p)) for p in B_EAST], east_x, None)
off = [p for p in JER if places[p]["lat"] is not None and not in_box(B_BOX, places[p])]
assert sorted(off) == ["jer_baqa", "jer_tombs_kings", "ramat_rahel"]
yb = oy + oh - 58
c.text(ox + 8, yb, "Off this frame (from the Temple enclosure):", 10, P["sub"])
for pid in sorted(off, key=lambda q: bearing_km("jer_temple", q)[0]):
    d, w = bearing_km("jer_temple", pid)
    yb += 14
    c.circle(ox + 14, yb - 3.5, rad(pid), fill=FILL, stroke=GREY, width=1.0)
    c.text(ox + 24, yb, f"{places[pid]['shortName']}, {d:.1f} km {w}", 10, P["sub"])
S.scale_bar(c, ox + ow - 52, by0 + 14, 0.25 * s2, "0", "250 m")
S.north_arrow(c, ox + ow - 20, by0 + 84)

# ------------------------------------------------------------------ panel 2: inset A
ax, ay, aw, ah = S.panel(c, 346, TOP, 664, BOTTOM - TOP, "A — Jericho, Qumran and the desert, enlarged",
                         ["Every ledger search that can be placed lies here, except S07 and S08 at Mount Gerizim."])
mx0 = ax + 170
c.rect(mx0, ay, ax + aw - mx0, ah, stroke=P["border"], width=1.0)
s3 = 21.0
P3 = proj(A_BOX[0], A_BOX[1], mx0, ay, s3, 31.78)
xr, yb3 = P3(A_BOX[2], A_BOX[3])
assert abs(xr - (ax + aw)) < 1.5 and abs(yb3 - (ay + ah)) < 15, (xr, yb3)
for pid in sorted(places):
    p = places[pid]
    if p["lat"] is not None and in_box(A_BOX, p):
        place_dot(*P3(p["lat"], p["lon"]), pid)
assert {p for p in places if places[p]["lat"] is not None and in_box(A_BOX, places[p])} == {
    "ain_duk", "nuweimeh", "doq", "tell_es_sultan", "jericho_area", "tell_el_qos", "jericho_palaces", "choziba",
    "kuteif", "asla", "kh_qumran", "wadi_qumran", "hyrcania", "buqeia", "mar_saba"}
for sid, (la, lo, how) in sorted(drawn_at.items()):
    if how == "own":
        search_point(*P3(la, lo))
xy = {pid: P3(places[pid]["lat"], places[pid]["lon"]) for pid in places if places[pid]["lat"] is not None}
spt = {sid: P3(la, lo) for sid, (la, lo, how) in drawn_at.items() if la < 32}

# north of Jericho: Ain Duk, IV/11 group, Wadi Nuweimeh
x, y = xy["ain_duk"]
pname("ain_duk", x - 12, y + 4, "end")
rows = chips(mx0 + 8, y + 24, ["S21", "S20"])
lead(rows[0][1] + 3, rows[0][0], x - 5, y + 6, BLUE)
lead(rows[1][1] + 3, rows[1][0], spt["S20"][0] - 3, spt["S20"][1] + 2, BLUE)
x, y = xy["nuweimeh"]
pname("nuweimeh", x - 4, y - 10)
# Doq and Ketef Jericho
x, y = xy["doq"]
pname("doq", x - 10, y + 4, "end")
rows = chips(mx0 + 8, y + 22, ["S22", "S25"])
lead(rows[0][1] + 3, rows[0][0], x - 4, y + 5, BLUE)
lead(rows[1][1] + 3, rows[1][0], spt["S25"][0] - 1, spt["S25"][1] + 3, BLUE)
# Tell es-Sultan (looks only)
x, y = xy["tell_es_sultan"]
tx = x + 86
lead(x + 14, y - 3, tx - 4, y - 12)
pname("tell_es_sultan", tx, y - 12,
      extra=["6 silent looks, pd null or 0:", " ".join(PH["tell_es_sultan"]),
             f"and {len(REP['tell_es_sultan'])} reported looks"])
# Jericho oasis and Tell el-Qos
x, y = xy["jericho_area"]
pname("jericho_area", x + 13, y - 1)
x, y = xy["tell_el_qos"]
lead(x + 3, y + 3, x + 9, y + 9)
pname("tell_el_qos", x + 11, y + 14)
# Jericho palaces (looks only)
x, y = xy["jericho_palaces"]
lead(x + 2, y + 10, x + 6, y + 22)
pname("jericho_palaces", x - 2, y + 34, extra=[rep_text("jericho_palaces")])
# Choziba, Kuteif, Asla, Wadi Qumran
for pid, dx, dy in (("choziba", -9, 4), ("kuteif", -9, 4), ("asla", -9, 4), ("wadi_qumran", -6, 17)):
    x, y = xy[pid]
    pname(pid, x + dx, y + dy, "end")
# 3Q and Kh. Qumran
x, y = spt["S01"]
chips(x + 12, y + 4, ["S01"])
x, y = xy["kh_qumran"]
pname("kh_qumran", x + 18, y + 2, extra=[rep_text("kh_qumran")])
QB = [s for s in with_search["kh_qumran"] if s != "S01"]
QB = sorted(QB, key=lambda s: (L[s]["place_match"] != "exact", L[s]["purpose"] not in SCROLL, s))
assert len(QB) == 12 and spt["S02"] == P3(*pts["S02"])
bx0 = ax + aw - 266
c.rect(bx0, y + 26, 260, len(QB) * LH + 8, fill=P["panel"], stroke=P["border"], width=1.0, rx=3)
rows = chips(bx0 + 6, y + 40, QB)
lead(x, y + rad("kh_qumran") + 3, x, y + 26, BLUE)
# Hyrcania, Buqeia, Mar Saba
x, y = xy["hyrcania"]
lead(x, y - 13, x, y - 24)
c.text(x - 68, y - 64, places["hyrcania"]["shortName"], 10.5, P["ink"])
lbl(x - 68, y - 51.5, [rep_text("hyrcania") + ".", "S03 names Kh. Mird but has", "no place_id (see left)."],
    None, 10.5, None, P["sub"], 12.5)
x, y = xy["buqeia"]
pname("buqeia", x, y + 20, "middle")
x, y = xy["mar_saba"]
pname("mar_saba", x - 10, y + 22, split=False)
# Christmas Cave (no candidate place)
x, y = spt["S05"]
lbl(x - 8, y - 14, ["Christmas Cave", "(not a candidate place)"], "end", 10.5, None, P["ink"], 12.5)
rows = chips(mx0 + 6, y + 73, ["S05", "S06"])
lead(x - 2, y + 3, mx0 + 70, rows[0][0] - 9, BLUE)
# north arrow and scale
S.north_arrow(c, mx0 + 22, ay + 52)
S.scale_bar(c, ax + aw - 125, ay + 20, 5 * s3, "0", "5 km")

# ------------------------------------------------------------------ panel 2, left column: key and unplaced rows
kx, ky = ax + 6, ay + 14
c.text(kx, ky, "Key (all maps)", 12.5, P["ink"], 700)
ky += 20
for i, n in enumerate((1, 4, 8)):
    c.circle(kx + 6 + i * 22 + (3.0 * math.sqrt(n)), ky, 3.0 * math.sqrt(n), fill=FILL, stroke=GREY, width=1.0)
c.text(kx + 76, ky + 4, "1, 4, 8 entries", 10.5, P["sub"])
ky = c.wrap(kx, ky + 22, "Candidate place; circle area = entries that name it", 30, 10.5) + 8


def key_item(draw, text):
    global ky
    draw(kx + 8, ky - 4)
    ky = c.wrap(kx + 22, ky, text, 26, 10.5) + 5


key_item(lambda x, y: (c.circle(x, y, 4, fill=FILL, stroke=GREY), c.circle(x, y, 6.6, stroke=BLUE, width=2)),
         "a ledger row has this place_id")
key_item(lambda x, y: glyph(x, y, True, True), "scroll-motivated, exact place")
key_item(lambda x, y: glyph(x, y, True, False), "scroll-motivated, near or none")
key_item(lambda x, y: glyph(x, y, False, True), "other search, exact place")
key_item(lambda x, y: glyph(x, y, False, False), "other search, near or none")
key_item(lambda x, y: search_point(x, y), "point the repo gives")
key_item(lambda x, y: (c.circle(x, y, 3, fill=FILL, stroke=GREY), c.circle(x, y, 8, stroke=GREY, width=1.2,
                                                                         dash="3 2.5")),
         "in the looks table; no look has a detection probability")
ky += 14
c.text(kx, ky, "Not drawn (6 rows)", 12.5, P["ink"], 700)
ky = c.wrap(kx, ky + 16, "No place_id and no WGS84 point in the repo:", 27, 10.5) + 4
for sid in unmapped:
    r = L[sid]
    scroll = r["purpose"] in SCROLL
    glyph(kx + 5, ky - 3.8, scroll, False)
    c.text(kx + 14, ky, f"{sid}, {years(r)}", 10.5, P["ink"], 700)
    ky = c.wrap(kx + 14, ky + 13, DESC[sid] + (" (claim)" if r["kind"] == "CLAIM" else ""), 26, 10, lh=12.4) + 4

# ------------------------------------------------------------------ panel 3: counts and the unsearched list
sx, sy, sw, sh = S.panel(c, 1026, TOP, 334, BOTTOM - TOP, "Coverage of the record",
                         ["Counted from the three tables when the sheet is built."])
CNT = [
    (N_PL, f"candidate places ({N_PL - len(NOCOORD)} with coordinates)"),
    (len(with_search), f"with a ledger search (place_id): {len(EXACT)} exact, {len(NEAR_ONLY)} near only"),
    (len(SCROLL_PL), "with a scroll-motivated search: Kh. Qumran"),
    (len(LOOKS_ONLY), "looks only, none with a detection probability"),
    (len(NOTHING), "with nothing in either table"),
]
y = sy + 12
for n, text in CNT:
    c.text(sx + 30, y + 1, str(n), 14, P["ink"], 700, anchor="end")
    c.text(sx + 40, y, text, 10.5, P["sub"])
    y += 18
y += 8
c.text(sx + 6, y, f"The {len(NOTHING)} places with nothing recorded", 12.5, P["ink"], 700)
y = c.wrap(sx + 6, y + 15, "Entries that name each place. * = the atlas's preferred candidate; "
           "† = no coordinates.", 56, 10, fill=P["sub"]) + 4
GROUPS = [("jerusalem", "Jerusalem"), ("jericho", "Jericho and Qumran"), ("region", "Other regions")]
assert {places[p]["region"] for p in NOTHING} == {g for g, _ in GROUPS}


def ent_list(pid):
    out = []
    for eid, st in cands[pid]:
        out.append(eid + ("*" if st == "preferred" else " (weak)" if st == "weak" else ""))
    return ", ".join(out)


for reg, head in GROUPS:
    ps = sorted((p for p in NOTHING if places[p]["region"] == reg), key=lambda p: (-len(cands[p]), places[p]["shortName"]))
    c.text(sx + 6, y + 2, f"{head} ({len(ps)})", 11, P["ink"], 700)
    y += 15
    for pid in ps:
        nm = places[pid]["shortName"] + (" †" if pid in NOCOORD else "")
        c.text(sx + 12, y, nm, 10, P["sub"])
        c.text(sx + sw - 6, y, ent_list(pid), 10, P["ink"], anchor="end")
        y += 12.0
    y += 3
y = c.wrap(sx + 6, y + 8, "Scroll-motivated: purpose coded scroll_deposit_search, scroll_motivated or "
           "scroll_find_site; other: surveys and digs of named places. Near: the ledger matched only the "
           "nearest place. (claim): row graded CLAIM.", 58, 10, fill=P["sub"], lh=12.4)
assert y - 12.4 < sy + sh - 8, y   # last baseline inside the panel

# ------------------------------------------------------------------ footer
S.footer(c, 830, [
    ("Sources", f"atlas/app/atlas-data.json (snapshot {atlas['snapshot'][:7]}); "
     "research/history/salvage_records/searches.csv and README; research/models/search_effectiveness/looks.csv, "
     "results.json and README §5; WGS84 points from devaux1952_cave_points (S01) and W2B grid_conversions_v2 (S20)."),
    ("How it was drawn", "WGS84 lat/lon, 111.32 km per degree, x scaled by cos latitude at each map's centre; a bar "
     "on each map. Rows with no WGS84 point in the repo sit at their place's atlas point. No datum transform."),
    ("What it shows", f"Of {N_PL} candidate places, {len(with_search)} have a ledger search; {len(NEAR_ONLY)} of those are "
     f"“near” matches only. Only Kh. Qumran has a scroll-motivated one. {len(NOTHING)} places, all of Jerusalem "
     "among them, have nothing. No look at any candidate place has a detection probability."),
    ("What it does not show", "This sheet identifies nothing; it shows coverage of the record only. A marker does not "
     "mean the place was covered: no row has a target volume, and the negative rows (S03, S10, S17) have "
     "unknown or tiny footprints."),
])
print(c.save(out_path("search_05_coverage_map")))
print(f"places {N_PL}; with search {len(with_search)} (exact {EXACT}, near only {NEAR_ONLY}); scroll {SCROLL_PL}; "
      f"looks only {LOOKS_ONLY}; nothing {len(NOTHING)}; not drawn {unmapped}")
