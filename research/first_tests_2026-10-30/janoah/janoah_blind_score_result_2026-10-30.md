# Janoaḥ test: blind score result (30 Oct 2026)

**EXPLORATORY ONLY.** Blinding failed before scoring: the target packet stands out by its structure. The owner chose to score anyway (chat, 29 Oct 2026, about 18:45 PDT). The rule, controls and hashes are in [janoah_controls_and_packets_2026-10-29.md](janoah_controls_and_packets_2026-10-29.md).

## Sequence (UTC)
1. 2026-10-30T01:12:41Z: controls frozen. controls.json sha256 `ebdca1a3…`.
2. 01:35:44Z: key written by a random shuffle (Python `secrets`). key.json sha256 `785f4006…`.
3. A fresh scorer read only the five packets U1–U5, with no names, repo, Drive or web. It locked its answers in answers.json, sha256 `d003ae982e407bc26fce14d2ce964ac3e7a797c467336a26e853e774ba2800eb`.
4. The coordinator re-checked the answer hash on disk (unchanged) and then opened the key.

## Result
| Code | Unit | Role | Scorer's label | Confidence |
|---|---|---|---|---|
| U4 | Kh. Yanun + Yanun village | target | SILENT-IN-ZONE | medium |
| U2 | Kh. Tana el-Fauqa (18-17/55/01) | control 4 | PARTIAL | medium |
| U1 | Kh. er-Risa (18-17/40/01) | control 2 | SILENT | high |
| U3 | Kh. el-Jarayish (18-17/51/01) | control 3 | SILENT | high |
| U5 | Kh. el-Kurum (18-17/21/01) | control 1 | SILENT | high |

- **Target (EVIDENCE, JSP 9 pp. 93–94, as scored):**
  - A plastered rock-cut pit, 38-7 (undated), lies about 5 m from burial cave 38-2.
  - 38-2 was cut in Phase I (late Hellenistic) and was in use in the 1st century CE.
  - The excavated area is about 650 m from Yanun village and about 1,150 m from Kh. Yanun. That is outside the frozen 500 m zone.
  - Inside the zone, the records give only undated "burial caves" near the village.
  - A north-facing opening is recorded only for a different tomb, 39-2.
- **Control U2:** SWP Memoirs II p. 245 lists caves, cisterns and rock-cut tombs with no distances. Hellenistic and Roman pottery is recorded for the site.
- **No unit is NEGATIVE.** Highlands (p. 12) says isolated tombs, cisterns and caves were not published, so its silence shows nothing.

## Verdict under the frozen rule
- The target is not positive, so Janoaḥ is **not supported relative to the controls**.
- It is not rejected either: an unfit zone is silent, not negative.
- Result: **not identifiable from available evidence** for the claim "a pit with tombs at its mouth within 500 m of Kh. Yanun / Yanun village".
- The test is closed. It reopens only for a specified new observation, such as an exact grid for the JSP 9 excavation area or a field record of the zone.

## Exploratory note (not a test result)
- JSP 9's pit 38-7 beside a Hellenistic–1st c. CE burial cave is the closest description in these records to the XII 10 wording.
- It lies about 150 m beyond the zone edge, measured on rounded grids.
- Moving the zone to include it now would be a new exploratory model chosen after exposure, not a rescue of this test.
- Next evidence that could reopen the test: the exact excavation grid (JSP 9 plans and licence record), or GPS from a field visit.

## Limits
- Blinding failed.
- The controls' areas were not checked (size_unverified).
- Only one scorer was used.
- Guérin, the Mandate 1:20,000 sheets and imagery were not applied.
