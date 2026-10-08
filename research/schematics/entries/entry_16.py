"""Entry 16 (IV 3–5): the entering conduit, forty-one cubits in.

Sources: text/translation_en.json IV 3–5; text/readings.json e16-goal, e16-distance;
tables/phase5_assessments.csv (entry 16 tell_es_sultan; 16, 29, 35 hyrcania);
research/measurements/cycle6/puech_entry16.md; research/assessments/entry29_hyrcania/reading.md;
research/measurements/cycle7/kohlit_pool.md; atlas record 16.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def goal_box(c, x, y, w, h, text="◦◦"):
    """The lost goal of the conduit: a dashed box with the damaged letters."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#f6f3ee", stroke=P["muted"], width=1.3, dash="5 4", rx=4)
    c.text(x, y + 6, text, 18, P["muted"], 700, anchor="middle")


def walker(c, x, y, length=46):
    """'As you go in': an arrow along the direction of entry."""
    c.line(x, y, x + length, y, P["ochre_d"], 2, arrow="ochre")
    c.circle(x - 6, y, 4, fill=P["ochre_d"])


def fort(c, x, y, s=18):
    """Hilltop fortress (generic)."""
    c.rect(x - s / 2, y - s / 2, s, s, fill=P["stone"], stroke=P["ink"], width=1.6)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        c.rect(x + dx * s / 2 - 3, y + dy * s / 2 - 3, 6, 6, fill=P["stone_d"])


c, L = S.page("16", "the entering conduit", "IV 3–5", height=1200,
              subtitle="Schematic plan; the text gives no direction, so the orientation is arbitrary. "
                       "One arrangement the text allows; not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: in the conduit, forty-one cubits as you go in",
        ["The text gives no direction, so the orientation is arbitrary. The conduit's goal is lost (◦◦).",
         "41 cubits is Milik's restoration (only “four” survives), measured along the conduit from its entrance."])

cub = 12                                   # px per cubit (1 cubit ≈ 0.5 m)
yc = my + 290
xe = mx + 120                              # where one goes in
xd = xe + 41 * cub                         # deposit
c.rect(mx + 16, my + 160, xe - mx - 24, 260, fill="url(#earth)", fill_opacity=0.8)
c.text(mx + 24, my + 182, "outside", 11.5, P["sub"], italic=True)
S.channel(c, [(mx + 40, yc), (xd + 92, yc)], width=16, flow_arrow=False)
c.line(xd + 30, yc, xd + 70, yc, P["water_d"], 1.4, arrow="blue")
goal_box(c, xd + 128, yc, 72, 92)
S.label(c, xd + 128, yc + 72, ["goal lost", "“comes in ◦◦”"], P["muted"], 11.5, 700, anchor="middle")
c.line(xe, yc - 34, xe, yc + 20, P["ochre_d"], 1.4, dash="3 3")
walker(c, xe + 10, yc + 44, 60)
S.label(c, xe - 4, yc + 72, ["“as you go in”", "measured from here"], P["ochre_d"], 11.5, 700)
S.dim(c, xe, yc - 34, xd, yc - 34, "41 cubits ≈ 20.5 m (restored)", P["red_d"])
c.line(xd, yc - 40, xd, yc - 6, P["faint"], 0.8, dash="3 3")
S.deposit(c, xd, yc, size=7)
S.label(c, xd - 6, yc + 30, ["silver, 55 talents"], P["red_d"], 12, 700, anchor="end")
S.label(c, mx + 260, yc - 66, ["conduit · אמא"], P["water_d"], 12, 700)
S.north_arrow(c, mx + mw - 80, my + 130, "N?")
c.text(mx + mw - 80, my + 154, "orientation arbitrary", 10.5, P["muted"], anchor="middle")
S.scale_bar(c, xe, yc + 130, 10 * 2 * cub, "0", "10 m", "Drawn to scale along the conduit: 1 cubit taken as about 0.5 m")

# words that carry the geometry
kx, ky = mx + 16, my + 540
c.rect(kx, ky, mw - 32, 300, fill="#faf8f4", stroke=P["border"], width=1, rx=6)
c.text(kx + 16, ky + 26, "The words that carry the geometry", 13, P["ink"], 700)
rows = [
    ("in the conduit · אמא", "a water conduit or channel (lexicon: high). Open or covered is not stated."),
    ("that comes in ◦◦ · הבאה", "the conduit's goal stood in the lacuna: Puech “to the pool(?)”,"),
    ("", "Eshel “to Hyrcania”, Milik and Lefkovits leave it blank."),
    ("as you go in · בביאתך", "the measure starts where one enters; the entrance is not described."),
    ("forty-one cubits", "only “four” survives: 14 (Puech), 40 (Lefkovits), 41 (Milik 1962, Eshel)."),
    ("", "Distance or depth is also disputed (Milik DJD; Lefkovits p. 161)."),
]
yy = ky + 60
for head, body in rows:
    if head:
        c.text(kx + 16, yy, head, 11.5, P["ink"], 700)
    c.text(kx + 222, yy, body, 11.5, P["sub"])
    yy += 28 if head else 38
c.text(kx + 16, ky + 282, "No place name survives in this entry.", 11.5, P["muted"], italic=True)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 30) / 4

# V1: Puech, to the pool, 14 cubits
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: “to the pool(?)”, 14 cubits (Puech)",
                         ["Puech restores the goal as a pool and reads 14 cubits,",
                          "a distance (he excludes depth); Koḥlit from context."],
                         "Puech 2006, 2015 · alternative reading", "neutral")
k = 9
gy = iy + ih / 2 + 4
ex = ix + 40
S.channel(c, [(ix + 8, gy), (ex + 14 * k + 70, gy)], width=8, flow_arrow=False)
S.pool(c, ex + 14 * k + 100, gy, 56, 40)
c.text(ex + 14 * k + 100, gy + 36, "pool", 11, P["water_d"], anchor="middle")
S.dim(c, ex, gy - 20, ex + 14 * k, gy - 20, "14 cubits ≈ 7 m", P["red_d"])
S.deposit(c, ex + 14 * k, gy, size=4.5)
c.line(ex, gy - 26, ex, gy + 8, P["ochre_d"], 1.2, dash="3 3")
S.label(c, ix + 300, iy + 20, ["Puech rejects “Hyrcania”", "as too long for the gap.", "No Koḥlit pool, entrance",
                              "or phase is identified."], P["sub"], 11.5)

# V2: Eshel, to Hyrcania
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: “to Hyrcania” (Eshel 2002)",
                         ["Hyrcania's northern aqueduct; the measure starts where",
                          "the trail meets it, west of Hyrcania. 41 cubits."],
                         "Eshel 2002 · alternative reading", "neutral")
gy = iy + ih / 2 + 4
k = 4.5
ox = ix + 60
S.channel(c, [(ix + 8, gy), (ox + 41 * k + 30, gy)], width=6, flow_arrow=False)
fort(c, ox + 41 * k + 50, gy, 18)
c.text(ox + 41 * k + 50, gy + 26, "Hyrcania", 11, P["ink"], 600, anchor="middle")
c.line(ox, gy - 34, ox, gy + 30, "#9a7b4f", 2, dash="6 4")
c.text(ox - 8, gy + 30, "trail", 11, "#7d6a4a", italic=True, anchor="end")
S.dim(c, ox, gy - 16, ox + 41 * k, gy - 16, "41 cubits", P["red_d"])
S.deposit(c, ox + 41 * k, gy, size=4.5)
S.label(c, ix + 325, iy + 22, ["Eshel: the", "restoration assumes", "a geographical order", "in the list."],
        P["sub"], 11.5)

# V3: the figure
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "The figure: 14, 40 or 41 cubits",
                         ["Only “four” survives; the editions restore the rest.",
                          "Same start, same scale; the deposit moves along the conduit."],
                         "Distance only", "neutral")
k = 9
x0 = ix + 14
for i, (n, who, col) in enumerate(((14, "Puech", P["red_d"]), (40, "Lefkovits", P["water_d"]),
                                   (41, "Milik 1962, Eshel", P["ink"]))):
    y = iy + 12 + i * 36
    c.text(x0, y, f"{n} cubits ≈ {n / 2:g} m · {who}", 11, col, 600)
    S.dim(c, x0, y + 12, x0 + n * k, y + 12, "", col)

# V4: depth or distance
ix, iy, iw, ih = S.panel(c, sx, sy + 3 * (ph + 10), sw, ph, "Depth or distance?",
                         ["Whether a bare number after “as you go in” is a depth is",
                          "disputed (Milik DJD; Lefkovits p. 161); Puech: distance."],
                         "Section, not plan", "neutral")
gl = iy + 26
c.line(ix + 8, gl, ix + 200, gl, P["stone_d"], 2)
c.rect(ix + 8, gl, 192, ih - 26, fill="url(#earth)", fill_opacity=0.7)
c.text(ix + 12, gl - 6, "surface", 10.5, P["muted"])
c.line(ix + 60, gl + 4, ix + 60, iy + ih - 6, P["red_d"], 1.3, arrow="red")
c.text(ix + 70, iy + ih / 2 + 20, "a depth below the entrance?", 11, P["red_d"], 600)
c.text(ix + 230, gl + 4, "If a depth, the deposit lies", 11.5, P["sub"])
c.text(ix + 230, gl + 20, "below, not along, the conduit.", 11.5, P["sub"])
c.text(ix + 230, gl + 36, "The text shown reads distance.", 11.5, P["sub"])

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IV 3–5)", "“In the conduit that comes in ◦◦, as you go in, forty-one cubits: silver, 55 talents.”"),
    ("What the plan assumes", "The goal of the conduit is lost. The 41 cubits (Milik's restoration) run along the "
     "conduit from where one enters it. No direction is given, so the orientation is arbitrary; open or covered is "
     "not stated."),
    ("Project placement", "Possible only, low (atlas). Candidates: Tell es-Sultan (possible, low; Koḥlit by Puech's "
     "context) and Hyrcania / Kh. el-Mird and its aqueducts (possible, low; Eshel). No place name survives here."),
    ("What the records show", "Channels from the spring below Tell es-Sultan are undated; dated Hasmonean–Herodian "
     "conduits served the palaces to the south. Hyrcania's aqueducts are 1st c. BCE, but the link rests on Eshel's "
     "restoration (phase5_assessments.csv)."),
])
print(c.save(S.out_path("16")))
