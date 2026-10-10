"""Past searches 01: the March 1952 cliff survey around Cave 3 (3Q), drawn to scale.

Sources: research/history/devaux1952_cave_points/ (RB 60 pl. XX digitized; ±30 m 1σ);
research/history/djd3_text_cave_list_extracted.md (DJD III Textes pp. 4–16);
research/history/devaux1953_cave_list_extracted.md (RB 60 pp. 541–555);
research/history/salvage_records/README.md (Patrich & Arubas Cave 13, Twin Cave locator).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, page, load_points, out_path, bullets  # noqa: E402

pts = load_points()
c = page("01", "the 1952 cave survey around Cave 3 (3Q)",
         "Plan to scale on the Palestine grid (km), grid north up. Points as de Vaux plotted them in 1953, "
         "digitized to about ±30 m (1σ).")

TOP, BOTTOM = 100, 810
KHQ = (193.592, 127.604)          # Kh. Qumran square on pl. XX
TWIN = (193.700, 129.300)         # Twin Cave locator (IAA rec. 709, ±100 m)
PA_FIG = (193.477, 130.008)       # Patrich & Arubas Cave 13 as plotted on their Fig. 1
PA_TEXT_N = 130.445               # their text: 2.8 km N of Kh. Qumran (no easting given)

CONTENT = {   # DJD III Textes pp. 6–9 (short paraphrase)
    "1": ["1: large cave; pottery, then ash", "0.75 m thick down to bedrock"],
    "2": ["2: not a cave; pottery heap", "under fallen rocks"],
    "3": ["3: cave c. 3 m deep, roof fallen;", "finds at or just below the surface"],
    "4": ["4: large cave; mostly Arab sherds"],
    "7": ["7: very small cave (2 × 1.5 m);", "one lid, jar fragments"],
    "9": ["9: crevice walled with dry stone;", "a lamp"],
    "10": ["10: large cave, wide entrance;", "fragments of 2 jars"],
}

# ---------------- overview (to scale) ----------------
ox, oy, ow, oh = S.panel(c, 40, TOP, 390, BOTTOM - TOP, "Overview, to scale",
                         ["27 legible points of 40 on de Vaux's map (pl. XX).",
                          "Points 35–40 lie further south (not shown)."])
E0, E1, N0, N1 = 192.85, 193.95, 127.00, 130.65
k = min((ow - 70) / (E1 - E0), (oh - 40) / (N1 - N0))
gx0 = ox + 50 + ((ow - 70) - k * (E1 - E0)) / 2
gy0 = oy + 20


def XY(e, n):
    return gx0 + (e - E0) * k, gy0 + (N1 - n) * k


# grid
for e in (193.0, 193.5):
    x, _ = XY(e, N0)
    c.line(x, gy0, x, gy0 + (N1 - N0) * k, P["faint"], 0.8, dash="3 4")
    c.text(x, gy0 + (N1 - N0) * k + 14, f"{e:.1f}", 10, P["muted"], anchor="middle")
for n in (127.5, 128.0, 128.5, 129.0, 129.5, 130.0, 130.5):
    _, y = XY(E0, n)
    c.line(gx0, y, gx0 + (E1 - E0) * k, y, P["faint"], 0.8, dash="3 4")
    c.text(gx0 - 6, y + 4, f"{n:.1f}", 10, P["muted"], anchor="end")
c.rect(gx0, gy0, (E1 - E0) * k, (N1 - N0) * k, stroke=P["border"], width=1)

# inset frame
IE0, IE1, IN0, IN1 = 193.05, 193.78, 129.60, 130.28
x0, y0 = XY(IE0, IN1)
x1, y1 = XY(IE1, IN0)
c.rect(x0, y0, x1 - x0, y1 - y0, fill=P["grey_l"], stroke=P["ochre_d"], width=1.2, dash="4 3", fill_opacity=0.5)
c.text(x1 + 4, y0 + 10, "enlarged", 10.5, P["ochre_d"], 600)
c.text(x1 + 4, y0 + 23, "at right →", 10.5, P["ochre_d"])

# Kh. Qumran, Twin Cave, P&A text line
qx, qy = XY(*KHQ)
S.site(c, qx, qy, r=9)
c.text(qx + 12, qy + 4, "Kh. Qumran", 11.5, P["ink"], 700)
tx, ty = XY(*TWIN)
c.circle(tx, ty, 0.100 * k, stroke=GREY, width=0.9, dash="2 2")
c.path(f"M{tx},{ty - 5} L{tx + 5},{ty} L{tx},{ty + 5} L{tx - 5},{ty} Z", fill=P["paper"], stroke=GREY, width=1.3)
c.text(tx + 9, ty + 4, "Twin Cave (locator ±100 m)", 10, P["muted"])
lx0, ly = XY(193.15, PA_TEXT_N)
lx1, _ = XY(193.85, PA_TEXT_N)
c.line(lx0, ly, lx1, ly, RED, 1.2, dash="5 3")
c.text(lx0, ly - 6, "Cave 13 by its text", 10, P["red_d"])
c.text(lx0, ly + 13, "(2.8 km N of Kh. Qumran)", 10, P["red_d"])

LAB = {"14": (8, -2, "14 = 1Q"), "19": (-8, 12, "19 = 2Q"), "15": (-8, -2, "15"), "17": (8, 16, "17"),
       "18": (8, 6, "18"), "21": (8, 4, "21"), "12": (8, 4, "12"), "22": (8, 4, "22"), "26": (8, 4, "26"),
       "27": (-8, 4, "27"), "28": (-8, 8, "28"), "29": (8, 0, "29"), "30": (8, 10, "30"), "31": (-8, 6, "31"),
       "32": (8, 8, "32")}
for p, r in pts.items():
    e, n = float(r["pal_e_km"]), float(r["pal_n_km"])
    if not (E0 <= e <= E1 and N0 <= n <= N1):
        continue
    x, y = XY(e, n)
    inset = IE0 <= e <= IE1 and IN0 <= n <= IN1
    c.circle(x, y, 3.2, fill=P["ochre"] if p == "8" else P["ink"], stroke=P["paper"], width=0.8)
    if not inset and p in LAB:
        dx, dy, s = LAB[p]
        c.text(x + dx, y + dy, s, 10, P["ink"], 600 if "Q" in s else None, anchor="end" if dx < 0 else None)
S.north_arrow(c, XY(E1 - 0.12, 128.7)[0], XY(E1, 128.7)[1], "grid N")
S.scale_bar(c, XY(193.38, 128.2)[0], XY(193.38, 128.2)[1], 0.5 * k, "0", "500 m")

# ---------------- inset (to scale) ----------------
ix, iy, iw, ih = S.panel(c, 450, TOP, 530, BOTTOM - TOP, "Around 3Q (point 8), enlarged",
                         ["Circles show the ±30 m (1σ) position error of each point.",
                          "Notes give what DJD III (1962) pp. 6–9 records for each site."])
ki = min((iw - 20) / (IE1 - IE0), (ih - 40) / (IN1 - IN0))
ix0 = ix + 10 + ((iw - 20) - ki * (IE1 - IE0)) / 2
iy0 = iy + 14


def IXY(e, n):
    return ix0 + (e - IE0) * ki, iy0 + (IN1 - n) * ki


for e in (193.1, 193.2, 193.3, 193.4, 193.5, 193.6, 193.7):
    x, _ = IXY(e, IN0)
    c.line(x, iy0, x, iy0 + (IN1 - IN0) * ki, P["grey_l"], 1)
for n in (129.7, 129.8, 129.9, 130.0, 130.1, 130.2):
    _, y = IXY(IE0, n)
    c.line(ix0, y, ix0 + (IE1 - IE0) * ki, y, P["grey_l"], 1)
    c.text(ix0 + 3, y - 3, f"{n:.1f}", 9.5, P["faint"])

ILAB = {"1": (12, -4, "start"), "2": (12, 4, "start"), "3": (-12, -14, "end"), "4": (10, -24, "start"),
        "7": (-30, -40, "end"), "9": (-14, 4, "end"), "10": (-12, 30, "end")}
for p in ("1", "2", "3", "4", "7", "9", "10", "8"):
    r = pts[p]
    x, y = IXY(float(r["pal_e_km"]), float(r["pal_n_km"]))
    c.circle(x, y, 0.030 * ki, fill=P["ochre"] if p == "8" else P["grey_l"], stroke=P["ochre_d"] if p == "8" else GREY,
             width=1, fill_opacity=0.25 if p == "8" else 0.6)
    c.circle(x, y, 4, fill=P["ochre"] if p == "8" else P["ink"], stroke=P["paper"], width=1)
    if p == "8":
        S.leader(c, x + 5, y + 3, x + 24, y + 70, P["ochre_d"])
        S.label(c, x - 60, y + 84, ["8 = 3Q, the Copper Scroll cave",
                                    "c. 10 m wide; roof fallen except over a",
                                    "rear chamber c. 3 × 2 m; jar-and-lid layer",
                                    "30–40 cm thick in front; dug out completely",
                                    "in c. 10 days (de Contenson)"], P["ochre_d"], 11, 700)
    else:
        dx, dy, anc = ILAB[p]
        if p == "7":
            S.leader(c, x - 4, y - 4, x + dx + 4, y + dy + 16, P["sub"])
        S.label(c, x + dx, y + dy, CONTENT[p], P["ink"], 10.5, 600, anchor=anc if anc == "end" else None)

# Patrich & Arubas Cave 13 as plotted on their figure
fx, fy = IXY(*PA_FIG)
c.path(f"M{fx},{fy - 7} L{fx + 7},{fy + 5} L{fx - 7},{fy + 5} Z", fill=P["paper"], stroke=RED, width=1.6)
S.label(c, fx + 10, fy - 2, ["Cave 13 (Patrich & Arubas 1989),", "as plotted on their Fig. 1"], P["red_d"], 10.5, 600)
ax_, _ = IXY(193.42, IN1)
c.line(ax_, iy0 + 40, ax_, iy0 + 6, RED, 1.2, arrow="red", dash="4 3")
S.label(c, ax_ + 6, iy0 + 22, ["Cave 13 by their text: c. 0.17 km", "north of this frame (2.8 km N", "of Kh. Qumran; no easting given)"],
        P["red_d"], 10, None)

S.north_arrow(c, ix + 30, iy + ih - 70, "grid N")
S.scale_bar(c, ix + 16, iy + ih - 26, 0.1 * ki, "0", "100 m")
c.text(ix + 120, iy + ih - 6, "Caves A and B (1956), across 3Q's ravine c. 20 m apart: not plotted.", 10.5, P["muted"])

# ---------------- side: what the record says ----------------
sx, sy, sw, sh = S.panel(c, 1000, TOP, 360, BOTTOM - TOP, "What the 1952 record says",
                         ["DJD III Textes (1962) and RB 60 (1953)."])
y = sy + 14
y = bullets(c, sx + 8, y, [
    "40 numbered sites, listed on pp. 6–12; 26 had Qumran-type pottery.",
    "230 soundings found nothing. They are not located anywhere (p. 4).",
    "Map positions were plotted by eye (p. 6).",
    "The list does not say which sites were only sounded. Deposits were not removed everywhere (p. 16).",
    "Depths are given only for cave 1 (ash to bedrock, 0.75 m), cave 3 (finds near the surface) "
    "and 3Q (the jar layer).",
    "Not searched: the marl terrace below the cliff, which de Vaux calls \"une erreur\" (4Q and 5Q "
    "were found there). One large cave was sounded but not finished (not named).",
    "Cave 5 is \"just above the roof of cave 8\" in the text (p. 7), but the 1962 map plots it "
    "elsewhere; it is not legible on the 1953 map.",
], 50, 11.2, 7)
y += 8
c.text(sx + 8, y, "Distance from 3Q (point 8), on the map", 12.5, P["ink"], 700)
y += 20
for p, lab in (("7", "7"), ("10", "10"), ("4", "4"), ("9", "9"), ("3", "3"), ("2", "2"), ("1", "1"),
               ("14", "14 = 1Q"), ("19", "19 = 2Q")):
    d = int(pts[p]["dist_to_8_m"])
    c.text(sx + 14, y, lab, 11.5, P["ink"], 600)
    c.text(sx + 120, y, f"{d:,} m", 11.5, P["sub"], anchor="end")
    c.rect(sx + 132, y - 9, min(d, 1100) / 1100 * 190, 9, fill=GREY, fill_opacity=0.45)
    y += 17

# ---------------- footer ----------------
S.footer(c, 830, [
    ("Sources", "R. de Vaux, RB 60 (1953) 540–561, pl. XX (map, digitized here); DJD III, Textes (1962) pp. 4–16 "
     "(the numbered list). Patrich & Arubas, IEJ 39 (1989) pp. 43–44 and Fig. 1."),
    ("How it was drawn", "Affine fit on 24 grid crossings (RMS 5.4 m). Each point ±30 m (1σ), about ±60 m at 95%: "
     "drafting, base map and datum, fit and measurement. Grid north of the 1953 map."),
    ("What it shows", "Which 1952 sites lie near 3Q and what was recorded there. Only 3Q is said to have been dug "
     "out completely; for the others the record gives contents, not how deep anyone dug."),
    ("What it does not show", "No site is identified by distance alone. Patrich & Arubas's Cave 13 stays "
     "unidentified (their figure and text differ by c. 0.4 km). The 230 empty soundings cannot be drawn."),
])
print(c.save(out_path("search_01_qumran_caves_1952")))
