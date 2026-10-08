# Source-4 addendum: result (8 October 2026 UTC)

**What was added.** The project owner supplied PDFs of 24 first publications that the first run could not read. Source 4 is now read for 25 of the 42 excavated units that have a listed publication (it was 1 in the first run). The procedure ([PROCEDURE.md](PROCEDURE.md)) was committed before any coding (bdcc60f), and `match.py` is unchanged. The first result in [RESULTS.md](../RESULTS.md) stays on record.

- **Coding.** A new coder A coded source 4 for all 24 units. Coder B did the same, blind to coder A, for the 7 units already in coder B's random sample.
- **New matches.** Two units became coder-A matches in some variant: Tell Shiloh (S1492) and Kh. el-Kilya (S1831). Coder B coded both in full ([`coded_B_full/`](coded_B_full/)).
- **Reproduce:** `sh run_addendum.sh PACKETS_DIR OUT_DIR`. Outputs are in [`results/`](results/).

## Result: the headline does not change

Every row of the headline table is the same as in the first run:
- R1, Hellenistic/Roman, branch A survey level: **k = 0, f = 1, m = 332 of 333**.
- Branch B: k = 4, m = 329.
- Text level: all UNKNOWN.

So the reading is also the same: m ≫ k, and rarity is not measurable from the available evidence.

## What changed underneath (primary rules, with Nigro)

| Unit | Change | Source-4 evidence | Coded by |
|---|---|---|---|
| Kh. Qumran (E754), main, R2 | C3 survey: UNKNOWN → **MATCH** | de Vaux 1973 pp. 57–58: a secondary cemetery "on the plateau a little to the north of Khirbet Qumran" | A only |
| Tell Shiloh (S1492), main | C2: UNKNOWN → **MATCH** | Finkelstein 1985 p. 155 and Fig. 11: Iron Age I silos in the northern areas | A and B (B coded the whole unit) |
| Kh. el-Khudriya (S1929), main, R2 | C2: UNKNOWN → **MATCH** | Callaway 1970 p. 10: a storage cave and three large cisterns "on the terrace north of the church" | A only |
| Tananir (E99), main | C2: UNKNOWN → **MATCH** | Boling 1975: Silo B, which the text puts north of the site | A only |

- **Two of three conditions (branch A, survey level).** Three units join the list: Kh. Qumran (C2 and C3 match; C1 UNKNOWN), Kh. el-Khudriya and Tananir. None leaves it.
- **Sensitivity.** One row changes. With C1 at ≤ 2 km, branch B gains Tell Shiloh: 9 → 10 in the R1 main set, 13 → 14 in the pre-70 set. No other sensitivity count changes.
- **Kh. el-Kilya (S1831).** Coder A placed the court cistern to the north (C2 MATCH); coder B did not give it a direction. The merged C2 is therefore UNKNOWN.
- **Coder agreement (62 units coded twice).** C1 1.000 (κ 1.000); C2 0.968 (κ 0.926); C3 survey 0.968 (κ 0.899); C3 text, all UNKNOWN.

## Exposed candidates after the addendum

- **Kh. Qumran.**
  - C2 matches: caves to the north at S3835/E745, 789 m, 338°.
  - C3 survey matches: de Vaux's northern cemetery.
  - C1 stays UNKNOWN. De Vaux places the pools inside the site: the large reservoir 91 to the south-west; loc. 138 near the north-western entrance and loc. 68 in the south-eastern quarter, both on quadrant edges, which give UNKNOWN under position rule 3. No plan could be tied to the unit's recorded point.
  - So Qumran is a branch-A UNKNOWN that matches two of the three conditions.
- **Tell es-Sultan (ESI 15, pp. 68–70).** The 1992 dig exposed only the Early Bronze city wall. There are no water or burial passages, so nothing changes.
- **Kh. Marjame (Zohar 1980, *IEJ* 30: 219–220).** The spring water was collected in a basin beneath the Byzantine crypt. The basin is not open, so it does not count for C1. No burials are mentioned. Nothing changes.
- **Kh. Samiyye (Finkelstein 1990).** The article is about Dhahr Mirzbaneh. It adds shaft-tomb cemeteries, but C3 survey already matched. Nothing changes.

## Limits

- **Single-coded calls.** Three of the four changes rest on one coder's direction call:
  - Qumran's northern cemetery: the direction is the publication's own.
  - Kh. el-Khudriya: "north of the church" was taken as north of the site.
  - Tananir: the text says "north", but the plan's arrows suggest 30–45°.
  - None of these units is a coder-A match in any variant, so the protocol does not send them to coder B.
- **Plans.** No plan could be tied to a unit's recorded centre, because the plans have local grids or none. So every source-4 position comes from words.
- **Still unread (17).** Hizmi 1990 (Kh. el-Beyadat), Tchernov 1994 (Netiv Hagdud), and 15 print-only items: Yeivin 1973 for three sites, *Niqrot Zurim*, JSP 4, 9 and 10, *Teva va-Aretz*, *JSRS* 5, *Qardom*, Garbrecht and Netzer 1991, and two PhD theses.
- **Correction to the first run.** RESULTS.md said four of the publications were free on the IAA site. In fact all eight HA and ESI issues are there. The four extra ones are ESI 5, ESI 9, HA 40 and HA 59–60.
