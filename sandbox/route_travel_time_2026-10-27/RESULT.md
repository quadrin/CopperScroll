# Run 8 result: the entry order as a walking route

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit c420100, SHA-256 `2c3137d9…`. Anchor list written before any path was computed ([out/anchors.csv](out/anchors.csv), SHA-256 `4f09abb4…6449`, 2026-10-27T05:25:10Z). Exploratory.

## Verdict
**Not supported as written.** The anchors' scroll order is short (p ≈ 0.01–0.02), but **walking time does not beat straight distance**. Relief adds little or nothing, so this gives no new evidence that the list follows a walked route.

- **Anchors (7):** entries 9, 10 (East Gate and wall), 35 (Kidron gorge, Mar Saba), 49 (Siloam), 51 (Zadok's tomb), 57 (Gerizim), 58 (Beth-shean). Out: 48 (Absalom, low confidence); 30, 59 (medium only in `entries_possible`). Four of the seven lie within 0.7 km of each other, so the test really involves four locations.
- **Scroll order:** T = 27.17 h walking (Tobler on Copernicus GLO-30, 30 m, 8 neighbours); 111.7 km straight.

| Control | p walking | p straight | Rule met? |
|---|---|---|---|
| 10,000 orders, first anchor free | 0.0142 | 0.0228 | no (p ≥ 0.01) |
| 10,000 orders, first fixed | 0.0090 | 0.0088 | no (walk not smaller) |
| Exact, first fixed (deviation) | 6/720 = 0.0083 | 7/720 = 0.0097 | passes by one ordering; ties at 90 m / 16 neighbours |
| Exact, free (deviation) | 78/5040 = 0.0155 | 120/5040 = 0.0238 | no |

Deviation sets (fixed in the anchor file): D0 without entry 10 (p 0.03); D1 adding Doq, Kozeba, Naṭof, Bethesda (11 anchors, p ≈ 0.0003–0.0009, walking not smaller); D2 all medium placements (circular: Secacah = Qumran rests on the order itself; not a valid test).

## Exploratory follow-ups (outside the rule)
- **The scroll departs from the optimal route** by a 6.2 h Jerusalem → Mar Saba → Jerusalem round trip (entry 35) in the middle of the Jerusalem group. Scroll order ranks 6th of 720 (first fixed), 77th of 5,040 (free). The forward direction is ~2% quicker than the reverse.
- **1-hour detour corridors** ([out/corridors_90m_n16.json](out/corridors_90m_n16.json)): for the corridor Jerusalem → Mar Saba bracketing entries 11–34, every Jericho and Qumran placement in the project falls **4.1–7.4 h outside** it (Hyrcania 1.26 h). INFERENCE: if entry 35 really is Mar Saba and the list is one walked route, the project's Jericho/Qumran placements for entries 11–34 need a ≥4 h detour. Either the list is not a single route, or entry 35 is not at Mar Saba, or the middle block is not in the Jericho/Qumran area.

## Caveats
GLO-30 is a modern surface (buildings, cuts); no water or barrier costs; anchors are areas of ~50–500 m; readings for 9, 10, 49 partly assume a Jerusalem tour (W2B circularity note). Large path and cost files kept in the scratch folder only. Scripts: [scripts/](scripts/).
