# Run 22 result: reverse lookup from well-documented sites

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit ebabf7e. Entry relations (239, all 61 entries) fixed before any site was scored ([out/step1_entry_relations.json](out/step1_entry_relations.json), 06:46:48Z); site inventories fixed before scoring ([out/site_inventory.json](out/site_inventory.json), 06:50:08Z). Exploratory.

## Verdict
**Not supported; no informative lead.** Real entries are satisfied by real sites no more often than shuffled entries.

- Primary (strict dating, base reading, 8 in-region sites × 61 entries): **15 satisfied pairs vs a shuffled mean of 17.1** (range 8–23); ratio 0.88; p = 0.82. With Masada: 18 vs 19.9, p = 0.73.
- **Rule gap:** with 10 shuffles the smallest possible p is 0.091, so p < 0.05 was unreachable. With 1,000 shuffles (deviation): p = 0.40–0.63 across the four scoring modes; ratio 0.91–1.10.
- **Literal "leads"** (satisfied, never proposed): 13 in-region, but 12 are one-relation entries almost every site satisfies (12 and 12a "a court"; 41 "the hollow").
- **The only multi-relation lead: entry 45 at Kh. Qumran** (X 3–4, "the plastered cistern of the channels, watered from the great wadi"): all 6 relations pass on strict scoring — L71 "completely plastered", fed by branches of the central channel, the aqueduct bringing water from Naḥal Qumran (Magen & Peleg 2018 p. 90). It is weak: on lenient scoring Hyrcania and Masada satisfy it too; "plastered" and "channels" are uncertain readings (Milik reads a wheel-well; Lefkovits מיקות); "the great wadi" is a description, not a name; and putting entry 45 at Qumran breaks the IX–X sequence the editors place south of Jerusalem. Earlier placements: Bir Ayyub or the Tekoa–Herodium sector (ratings.csv); ʿAin Fāra in Wadi Qelt (Allegro 1960).

## Informative fails
- Entry 9 at the Temple Mount: no cistern lies within 7–10 m of the Golden Gate; cistern W15 is 25–30 m away (Warren & Conder p. 221; Gibson & Jacobson Fig. 10).
- Entries 3 and 15 at Alexandrium: the only court cistern is "small" (Netzer 2001 *Palaces* pdf p. 74).
- Josephus *BJ* 5.145 puts a "pool of Solomon" at Siloam (so that name passes at the City of David).

## Exploratory notes
- A name-blind lenient variant (1,000 shuffles) gives 79 real vs 56.0 shuffled, p = 0.042; with ≥3 relations 10 vs 3.6 (p = 0.072): 21, 22, 24 at Qumran; 24, 29 at Hyrcania; 29 at Jericho; 43 at Qumran and Jericho; 45 at Qumran and Hyrcania. **Circular**: most are the editions' own assignments, and the site facts were coded from earlier entry-driven runs.
- Known bias: the site facts were coded by someone who knew the entries, which favours real entries. No excess appeared anyway, which strengthens the null.

## Files
[out/matrix.md](out/matrix.md) (full 61 × 9 matrix), [out/pair_scores.csv](out/pair_scores.csv), [out/site_inventory.md](out/site_inventory.md), control summaries, [scripts/](scripts/).
