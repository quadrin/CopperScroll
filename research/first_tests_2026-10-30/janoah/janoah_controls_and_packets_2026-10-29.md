# Janoaḥ test: controls frozen, packets cut, scoring held (29–30 Oct 2026)

Rule: the Janoaḥ independent test plan (Claude project note of 26 Oct, approved that day by the owner; not in the repository). Integrator: a subagent of the 29 Oct session. Main session is the coordinator. Nothing has been scored.

## Controls (frozen 2026-10-30T01:12:41Z, before any §4 record was opened)
- **Selection rule.** The universe is every Highlands 1997 entry on map 18-17. Only ruins are eligible. Any ruin less than 1 km from either target is excluded. The rest are ranked by grid distance and the first four taken. The rule uses no described feature.
- **Controls, by distance:**

| Rank | Site | Highlands no. | Distance |
|---|---|---|---|
| 1 | Kh. el-Kurum | 21/01 | 1450 m |
| 2 | Kh. er-Risa | 40/01 | 1836 m |
| 3 | Kh. el-Jarayish | 51/01 | 2202 m |
| 4 | Kh. Tana el-Fauqa | 55/01 | 2239 m |

  The next site, Muwasi, is at 2688 m.
- **controls.json sha256:** `ebdca1a32cfc508fdba4682f61679c72d5253c388d185f7a8511e50c5e5b2bf4`
- **Deviation: size not checked.** The rule requires 0.2–1 ha. No record opened gives an area for any control, so all four are flagged `size_unverified`. The fallback (replace any control whose stated area falls outside the range) was frozen in advance but never triggered.

## Records applied to all five units
- **JSP 9 (2009).** Only the target has a chapter: Kh. Yannun / Itamar East, Hebrew pp. 78–97, English pp. 32*–35*. The Kh. Kurum in JSP 9 is a different site near Sebastia.
- **ASI 1 (1972).** Gophna & Porath has no entries on map 18-17. Kallai's chapter has Tana el-Fauqa only (site 27, p. 167).
- **SWP Memoirs II.** The village (p. 387), Abu Risah (p. 391), Kerum and Kh. Yanun (p. 394), and Tana (p. 245). Nothing for Jarayish.
- **Not applied:** Guérin (*Samarie* vol. II is not on archive.org), the Mandate 1:20,000 maps, and imagery.

## Packets
- Coded units U1–U5: U1 `1e0c35e3…`, U2 `aa7a308c…`, U3 `830d8003…`, U4 `20c78f41…`, U5 `1a830ead…`.
- key.json sha256: `785f400607e475597e791838b182f50385699f6c3eebd056a241be86d578b693`
- The files are kept in the 29 Oct session workspace; they are not uploaded here, to keep the key apart from the packets.

## Why scoring is held (integrator's report; EVIDENCE unless marked)
1. **Blinding cannot be achieved.** The target packet stands out by its structure: two reference points, a full excavation chapter, and a period summary. A scorer can pick it out without names.
2. **The JSP 9 pit falls outside the zone.** JSP 9 describes a plastered pit (38-7) about 5 m from a tomb (38-2). On the published rounded grids, the excavation area is about 650 m from Yanun village and about 1150 m from Kh. Yanun, which is outside the frozen 500 m target zone. INFERENCE: rounding of the printed grids is unlikely to close a 150 m gap, but the grid precision has not been checked.
3. Under AGENTS.md, widening the zone after seeing this would create a new exploratory model. It would not continue the frozen test.

## Exposure
- **Integrator:** has seen everything listed above, plus the repo's Highlands extraction, the SWP stage 1b index and WBADB scripts. A grep printed preregistration file names only; no contents were read.
- **Main session:** knows the two findings above. It has not read the packets.
- **Scoring:** any future scorer must be a fresh agent that has not seen this note.

## Owner decision needed
(a) Score the frozen test as it stands, recording that blinding failed, so it can at most be exploratory.
(b) Close it as **not identifiable from available evidence**: blinding cannot be achieved, and the only pit-and-tomb record lies outside the zone.
(c) Define a new exploratory model with a wider zone, recorded as chosen after this exposure.
