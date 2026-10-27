# Run 9 result: Greek architectural loanwords

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit c420100. Step 1 loanword list written before any building was gathered ([out/step1_loanword_entries.md](out/step1_loanword_entries.md), SHA-256 `1444160c…1b13f`, 05:26:24Z); scoring conventions fixed before any pair was scored ([out/scoring_conventions.md](out/scoring_conventions.md)). Exploratory.

## Verdict
**Not useful; no lead.** No loanword entry narrows to ≤3 buildings, and the loanword entries narrow less than the controls fail to.

| Entry | Role | In-region units with no fail (of 23) | All-pass leads |
|---|---|---|---|
| 3 (peristyle, פרסטלין) | loanword | 13 | 0 |
| 51 (stoa אסטאן, exedra אכסדרן) | loanword | 15 | 0 |
| 12-P (Puech's restored δίαιτα) | loanword | 16 | 0 |
| 8 | control (cistern + court) | 22 | 0 |
| 15 | control ("the great cistern") | 22 | 0 |
| 50 | control-alt (court only) | 23 | 12 (only two generic relations) |

- **Closest pairs, both already proposed:** entry 3 at the Temple Mount (3 of 5 pass: peristyle from Josephus BJ 5.190–192; the "Great Sea" cistern No. 8 and its manholes, SWP *Jerusalem* pp. 219–220); entry 51 at the Temple Mount with the Bene Ḥezir tomb (4 of 5; only "Zadok" unknown — the inscription names Ḥezir). Allegro 1960 and Milik 1962 proposed both.
- **Why nothing discriminates:** excavation reports are silent on cisterns under courts and tombs below corners, so most cells are unknown, not fail.
- Informative fails: Jericho Fortified Palace has no cistern on the tell (Netzer 2001 p. 29); Twin Palaces' courts were not colonnaded (p. 16); Alexandrium's only court cistern is "small" (p. 70); Herodium's tomb search failed (Netzer et al. 2010 p. 84).

## Deviations
Only entry 8 names a cistern and a court, so the second control is entry 15; entry 50 run as an alternative. Stoa position for porch tombs reused the tomb lane's frozen 51-S clauses. Hyrcania and Sebaste (feature unconfirmed) and Masada, Machaerus, Kh. el-Muraq (outside the region) in sensitivity lines only; none changes the verdict. Full table: [out/pair_scores.csv](out/pair_scores.csv) (168 rows); [out/summary.json](out/summary.json); [scripts/](scripts/).

## Exploratory follow-ups
- **Hyrcania summit court** lies over four cisterns, "two immense rock-hewn" (Haber & Gutfeld 2024 p. 121*), with Herodian Ionic column fragments; no peristyle reported, the paved court is Byzantine. No one has proposed it for entry 3. Next: the date and plan of the summit court.
- **Upper Herodium:** the SE-corner courtyard cistern (Netzer et al. 2010 p. 103; predates the palace) is the only cistern recorded in a peristyle court in the region. Next: its size in Corbo 1989.
- A post-hoc rule (excavated court with no recorded cistern = fail) cuts entry 3 to ~3 units (Jericho pools complex, Upper Herodium, Temple Mount) but cuts control entry 8 to 3–4 too.

## Not accessible
Netzer 2001 *Palaces* beyond pdf p. 98 and Netzer 2006 (Drive copies over the 10 MB connector limit or without text); Gibson & Jacobson 1996, Corbo 1989, Avigad/Geva Jewish Quarter reports, Crowfoot 1942, Vörös (no copy found).
