"""Entry 25 (VI 1–6): the Cave of the Column, two entrances, facing east; dig at the northern entrance.

Sources: text/translation_en.json VI 1–6; text/readings.json e25-direction;
research/sources/entry25_direction_review_2026-10-02.md (Milik: the cave faces east; stricter model: both mouths);
research/measurements/cycle4/puech_entry25.md (pillar vs Allegro's terrace; deposit under the jar or under the book);
research/feature_workbench/inventory/README.md (depth vs distance; 1.20–1.80 m);
research/assessments/entry25_iv17/README.md; atlas/app/atlas-data.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("25", "the Cave of the Column", "VI 1–6", height=1200,
              subtitle="Schematic plan, north up. One arrangement the text allows; the cave's size and shape "
                       "and the spacing of its two entrances are not given.")
mx, my, mw, mh = L["main"]


def jar(c, x, base, s=1.0, scroll=True):
    """Wide-mouth jar in section, base at (x, base); optional scroll inside. Returns top y."""
    w, h = 22 * s, 40 * s
    c.path(f"M{x - w * 0.45:.1f},{base:.1f} C{x - w:.1f},{base - h * 0.15:.1f} {x - w:.1f},{base - h * 0.8:.1f} "
           f"{x - w * 0.55:.1f},{base - h:.1f} L{x + w * 0.55:.1f},{base - h:.1f} C{x + w:.1f},{base - h * 0.8:.1f} "
           f"{x + w:.1f},{base - h * 0.15:.1f} {x + w * 0.45:.1f},{base:.1f} Z",
           fill="#e2c79c", stroke=P["grave_d"], width=1.2)
    if scroll:
        c.rect(x - 4 * s, base - h * 0.85, 8 * s, h * 0.62, fill="#f6efdc", stroke=P["ochre_d"], width=1, rx=3)
    return base - h


def coins(c, x, y, n=5):
    for k in range(n):
        c.circle(x - (n - 1) * 3.5 + k * 7, y, 3.2, fill="#c9ccd1", stroke="#6f747a", width=0.8)


def cave_plan(c, X, Y0, Y1, depth, gap, pillar=True, terrace=False, lw=1.6, ext=0, pw=None):
    """Cave west of a N–S cliff face at x=X, between Y0 (north) and Y1 (south), with two openings of
    width `gap`. pillar=True: a rock pillar between the openings; False: openings far apart in a plain wall.
    Returns (north_opening_y, south_opening_y)."""
    H, mid = Y1 - Y0, (Y0 + Y1) / 2
    if pillar:
        pw = pw or gap * 0.9
        n1, s0 = mid - pw / 2, mid + pw / 2
        n0, s1 = n1 - gap, s0 + gap
    else:
        n0, n1 = Y0 + 0.12 * H, Y0 + 0.12 * H + gap
        s1, s0 = Y1 - 0.12 * H, Y1 - 0.12 * H - gap
    d = depth
    outer = [(X, n0), (X - 0.25 * d, Y0 + 0.04 * H), (X - 0.8 * d, Y0), (X - d, Y0 + 0.4 * H),
             (X - 0.92 * d, Y1 - 0.2 * H), (X - 0.6 * d, Y1), (X - 0.22 * d, Y1 - 0.04 * H), (X, s1)]
    if pillar:
        pd = 0.22 * d
        back = [(X, s0), (X - pd, s0), (X - pd, n1), (X, n1)]
    else:
        back = [(X, s0), (X - 7, s0 - 6), (X - 7, n1 + 6), (X, n1)]
    c.polyline(outer + back, fill="#f3ece0", stroke="none", close=True)
    if pillar:
        c.rect(X - pd, n1, pd, s0 - n1, fill="url(#rockfill)")
    c.polyline(outer, stroke=P["grave_d"], width=lw)
    c.polyline(back, stroke=P["grave_d"], width=lw)
    # cliff face with gaps at the two openings; hachures fall to the east
    for a, b in ((Y1 + ext, s1), (s0, n1), (n0, Y0 - ext)):
        if a - b > 4:
            S.ridge(c, [(X, a), (X, b)])
    if terrace:
        c.rect(X + 8, n0 - 10, 64, s1 - n0 + 20, fill="#e9dfcc", stroke=P["stone_d"], width=1.4, dash="5 3")
    return (n0 + n1) / 2, (s0 + s1) / 2


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: a pillar cave fronting east, dig at the northern entrance",
    ["Milik 1960 takes “facing east” with the cave as a whole; “northern” picks the northern of",
     "the two mouths, not a north-facing one (entry25_direction_review)."],
    "Project reading (Puech pillar; Milik's eastward cave)", "counted")
X, Y0, Y1 = ix + 470, iy + 70, iy + 450
c.rect(ix + 6, iy + 10, X - ix - 6, 510, fill="url(#rockfill)")
c.rect(X, iy + 10, ix + iw - X - 6, 510, fill="url(#earth)", fill_opacity=0.8)
c.text(ix + 20, iy + 32, "rock", 11, P["sub"], italic=True)
c.text(X + 120, iy + 32, "slope below the cliff", 11, P["sub"], italic=True)
ny, sy_ = cave_plan(c, X, Y0, Y1, depth=300, gap=56, ext=40, pw=70)
c.text(X - 250, (Y0 + Y1) / 2 - 20, "cave · מערה", 13, P["ink"], 700)
c.text(X - 250, (Y0 + Y1) / 2 - 4, "size and shape not given", 10.5, P["muted"])
# pillar label
S.leader(c, X - 40, (Y0 + Y1) / 2, X - 110, (Y0 + Y1) / 2 + 70)
S.label(c, X - 190, (Y0 + Y1) / 2 + 86, ["pillar · העמוד", "between the two entrances"], P["grave_d"], 12, 700)
# facing east: the cave as a whole
c.line(X + 16, (Y0 + Y1) / 2, X + 190, (Y0 + Y1) / 2, P["ochre_d"], 2.2, arrow="ochre")
S.label(c, X + 30, (Y0 + Y1) / 2 - 12, ["the cave faces east · הצופא מזרח"], P["ochre_d"], 12, 700)
c.text(X + 30, (Y0 + Y1) / 2 + 22, "Milik: the cave as a whole, not each mouth", 11, P["ochre_d"])
# openings
S.label(c, X + 14, sy_ + 26, ["southern entrance"], P["ink"], 12, 600)
c.text(X + 14, sy_ + 46, "two entrances · שני הפתחין", 12, P["ink"], 700)
S.deposit(c, X - 8, ny, size=7)
S.label(c, X + 14, ny - 34, ["northern entrance · הפתח הצפוני"], P["ink"], 12, 700)
S.label(c, X + 14, ny - 14, ["dig 3 cubits ≈ 1.5 m: a jar, one scroll,", "42 talents under it"], P["red_d"], 11.5, 700)
S.north_arrow(c, ix + 46, iy + 110)

# section inset at the northern entrance
qx, qy, qw, qh = ix + 8, iy + 536, iw - 16, ih - 540
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section at the northern entrance (schematic), west to the left", 12, P["ink"], 700)
g = qy + 70
c.rect(qx + 16, g, 430, qh - 82, fill="url(#earth)")
c.path(f"M{qx + 16},{g - 46} L{qx + 200},{g - 46} L{qx + 200},{g}", fill="none", stroke=P["grave_d"], width=1.6)
c.text(qx + 24, g - 30, "cave roof", 10.5, P["muted"])
c.line(qx + 16, g, qx + 446, g, P["stone_d"], 1.6)
c.text(qx + 206, g - 6, "threshold", 10.5, P["sub"])
hx, dpx = qx + 260, 90  # 60 px per metre: 3 cubits ≈ 1.5 m
c.rect(hx - 34, g, 68, dpx, fill="#f7f2e8", stroke=P["stone_d"], width=1, dash="4 3")
coins(c, hx, g + dpx - 6)
jar(c, hx, g + dpx - 12, s=1.15)
S.deposit(c, hx + 22, g + dpx - 6, size=4)
S.dim(c, hx + 52, g, hx + 52, g + dpx, "3 cubits ≈ 1.5 m", P["red_d"], offset=-30)
S.label(c, qx + 470, g - 20, ["Down from the northern threshold, whose", "ancient level is not recorded.",
                              "The jar holds one scroll; the 42 talents",
                              "lie under the jar (Puech's preference).",
                              "1 cubit taken as about 0.5 m."], P["sub"], 11.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph = (sh - 3 * gap) / 4

# V1: each mouth faces east
ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Model: each mouth faces east",
                         ["A stricter project model than Milik's; the singular הצופא",
                          "after plural “entrances” does not settle it."],
                         "Project model choice", "neutral")
X1 = ax + 150
nyy, syy = cave_plan(c, X1, ay + 14, ay + ah - 8, depth=110, gap=18, lw=1.3, ext=4, pw=20)
for yy in (nyy, syy):
    c.line(X1 + 4, yy, X1 + 70, yy, P["ochre_d"], 1.6, arrow="ochre")
    c.text(X1 + 76, yy + 4, "east", 11, P["ochre_d"], 600)
S.deposit(c, X1 - 6, nyy)
c.text(X1 + 130, ay + ah / 2 + 4, "Both openings in an east wall,", 11, P["sub"])
c.text(X1 + 130, ay + ah / 2 + 20, "each looking east.", 11, P["sub"])

# V2: terrace / platform
bx, by, bw, bh = S.panel(c, sx, sy + ph + gap, sw, ph, "Variant: a terrace, not a pillar",
                         ["Puech p. 60 records Allegro's “platform or terrace”;",
                          "such a cave need have no pillar between the mouths."],
                         "Not adopted · Allegro, via Puech", "warn")
X2 = bx + 150
nyy, syy = cave_plan(c, X2, by + 14, by + bh - 8, depth=110, gap=18, pillar=False, terrace=True, lw=1.3, ext=4)
S.deposit(c, X2 - 6, nyy)
c.text(X2 + 84, (nyy + syy) / 2 - 4, "terrace in front", 11.5, P["ink"], 700)
c.text(X2 + 84, (nyy + syy) / 2 + 12, "no pillar", 11, P["sub"])

# V3: under the jar or under the scroll
cx_, cy_, cw_, ch_ = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Deposit: under the jar, or under the scroll",
                             ["“Under it” can refer to the jar or to the scroll inside it;",
                              "Puech prefers under the jar. Both kept (puech_entry25)."],
                             "Both readings kept", "neutral")
base = cy_ + ch_ - 8
coins(c, cx_ + 90, base - 4)
jar(c, cx_ + 90, base - 10, s=1.3)
c.text(cx_ + 130, base - 40, "under the jar", 11.5, P["ink"], 700)
c.text(cx_ + 130, base - 24, "Puech's preference", 11, P["sub"])
jar(c, cx_ + 300, base, s=1.3, scroll=False)
coins(c, cx_ + 300, base - 8, n=3)
c.rect(cx_ + 300 - 5, base - 46, 10, 30, fill="#f6efdc", stroke=P["ochre_d"], width=1, rx=3)
c.text(cx_ + 340, base - 40, "under the scroll,", 11.5, P["ink"], 700)
c.text(cx_ + 340, base - 24, "inside the jar", 11, P["sub"])

# V4: depth or distance
dx, dy, dw, dh = S.panel(c, sx, sy + 3 * (ph + gap), sw, ph, "Three cubits: a depth or a distance?",
                         ["Vertical: down from the threshold. Horizontal: 3 cubits",
                          "from the opening, origin and direction unknown."],
                         "Both open (feature workbench)", "neutral")
gy = dy + 34
c.rect(dx + 14, gy, 170, dh - 40, fill="url(#earth)")
c.line(dx + 14, gy, dx + 184, gy, P["stone_d"], 1.4)
c.line(dx + 99, gy, dx + 99, gy + 54, P["red_d"], 1.2, dash="4 3")
S.deposit(c, dx + 99, gy + 54)
S.dim(c, dx + 120, gy, dx + 120, gy + 54, "3 c.", P["red_d"], offset=-22)
c.text(dx + 14, gy - 8, "vertical (section)", 11, P["ink"], 700)
X4, Y4 = dx + 330, dy + dh / 2 + 4
S.ridge(c, [(X4, Y4 + 54), (X4, Y4 + 12)])
S.ridge(c, [(X4, Y4 - 12), (X4, Y4 - 54)])
c.path(f"M{X4},{Y4 - 50} A50,50 0 0,0 {X4},{Y4 + 50}", stroke=P["red_d"], width=1.2, dash="4 3")
c.text(X4 - 120, Y4 - 48, "horizontal (plan)", 11, P["ink"], 700)
c.text(X4 - 130, Y4 + 4, "3 cubits", 11, P["red_d"], 600)
c.text(X4 + 10, Y4 + 4, "opening", 10.5, P["sub"])

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VI 1–6)", "“[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern "
     "entrance, dig three [cu]bits: there is a jar, in it one scroll; under it 42 talents.”"),
    ("What the plan assumes", "A pillar, not a terrace. The cave as a whole fronts east; the northern entrance is the "
     "northern of the pair. Three cubits is a depth; the silver lies under the jar."),
    ("Project placement", "Atlas: possible only, low; Kh. Qumran and its nearby cliff caves. Comparison caves in the "
     "files: Twin Cave near 11Q (Bar-Adon), Abu Saraj IV/17 and IV/11; none is identified."),
    ("What the records show", "IV/17 passes the two-mouth and pillar comparison; mouth bearings, threshold level and "
     "date are unresolved (assessments/entry25_iv17). Twin Cave: both mouths face east; IV/11: an inner pillar only."),
])
print(c.save(S.out_path("25")))
