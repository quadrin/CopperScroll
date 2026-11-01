# qum3a, reader A, group Q1: keying log

- Source: Humbert, Chambon & Młynarczyk (eds) 2016, *Khirbet Qumrân et Aïn Feshkha IIIA*, Part 2, ch. 11 "Liste des éléments construits de la fouille" (printed pp. 129–134) and ch. 12 "Liste des loci" (printed pp. 135–138).
- Started 2026-11-01T02:16Z (UTC); finished 2026-11-01T02:32Z (UTC).
- Read: the full text extraction `qum3a_lists_pp129-138.txt` (PDF pp. 129–138; printed page = PDF page). Page images checked: pp. 129, 134, 135 (`render_bucket.py`, 150 dpi). The text layer matched the print on all three, including the odd grids ("(D4" for 258, "G/H/I 4-5" for 951a).
- Figures/plates: none consulted. Plates I–XII are only cited by the lists. `figure` is blank; each element's plate number is in `notes`.
- Nothing was unreadable.

## Output

`keyed/qum3a_A_g1.csv`: 739 rows.
- 542 rows for ch. 11 elements, plus 3 sub-rows for the three segments of 951a (`E951a.a`–`.c`).
- 192 rows for ch. 12 loci (48–49 is one locus), plus 2 sub-rows for the two parts of L. 45 (`L45a`, `L45b`).

Every entry in both lists was keyed. Each has at least a relation or a positional note, and none was dropped.

- Steps: 32 rows. These are 20 `steps`-class rows and 12 loci with steps (stairwell, stepped corridor or passage, stepped basins, or a stair listed as a boundary). `n_steps` is printed for only 4 rows: E214 = 3, E229 = 3, E326 = 3, and E308 = 1 (singular "degré", medium confidence).
- Plaster = yes: 16 rows. Two are explicit "enduit(e)(s)" (E417, E756). The other 14 are basins, vats or floors described "de mortier" (medium confidence). Where mortar is only a binder ("pierres et mortier") or a bench or ridge is made of mortar, plaster was not keyed.
- Size: 4 rows, all lengths from the text: E951a segments a = 49 m, b = 13 m, c = 8 m, and E951b = 22 m. No other dimension is printed.
- Relations: 718 rows. Walls and other numbers between the asterisks of a locus are keyed `next_to:qum3a:E<n>`. Doors listed for a locus are also `next_to`, and their count is in `n_openings` (40 rows, counted as printed). "Opens onto" and "access to" are keyed `leads_to`. "Au-dessus" / "sous" are keyed `above` / `below`. Supplies, spillways and overflows are keyed `fed_by` / `leads_to`. "Traversé par" (crossed by a drain or aqueduct) is keyed `next_to` with a note.
- Other: `opening_dirs` for 4 rows (kiln mouths E317 N and E318 S; E385 "par le sud" S; E399 door in the north front N). `n_pillars` for 4 rows (E789 = 3, E908 = 4, L8 = 1 stair pier, L35 = 1). One natural feature: E710 "faille 3 séisme", keyed as `fissure`.
- `in_window` is `unknown` everywhere except E396–398 (Iron Age wall remnants), which are `no`. Periods are keyed as printed: tardif, post 68, niveau 4, Âge du Fer.

## Conventions and judgement calls

- Grid: the plate cell as printed, with parentheses (`grid_system = unknown`, `position_basis = plan`, "IIIA plate grid" in `notes`).
- Hyphenated locus groups ("L. 1-2", "L. 56-58", "L. 81-88", "L. 129-133") are keyed as the listed loci, not as ranges. The exception is 48–49, which is a single locus. "L. 92-94" (E799) is flagged because it may mean a range.
- Class choices:
  - "Espace à ciel ouvert" → `court`. Couloir, passage locus, secteur and espace → `other`. Chambre, réduit, atelier and partition of a room → `room`. Appentis and hangar → `building`.
  - Bassin à degrés → `pool`. "Bain rituel" L138 → `ritual_bath`. Petit bassin and cuve → `basin`. "Grand réservoir" → `reservoir`. L110 → `cistern`.
  - Bord, bordure and rebord → `wall`.
  - Socle, niche, placard, banquette, four, vanne, margelle and saillant → `other`.
  - Silos L161–164 are classed `other`, following ch. 11 (E514, E515, E525), although ch. 12 calls them partitions.
- Locus classes follow the ch. 12 definition where ch. 11 uses another word (e.g. L117/L118 "bassin à degrés" vs ch. 11 "citerne"). The other word is in `notes`.
- `parent_id`: set when an element is tagged to a single locus ("X, L. n"), to a wall (niche, placard or recess "dans le mur N"), or when a locus is a partition or part of another locus. Parents are repeated as `inside:` in `relations`.

## Cross-list inconsistencies (keyed as printed, flagged in notes)

- Numbers cited in ch. 12 with no ch. 11 entry: 337 (L50, L51), 348 (L3, L81, L82), 386 (L8; ch. 11's stair pier is 248), 587 (L108), 821 (L186), 847 (L77), 956 (L143).
- Loci cited in ch. 11 with no ch. 12 entry: L. 10A (E250, E410, E414) and L. 9A (E413).
- "270" (L5, L152, L190, E277) and "951" (L78, L143, L145, L183) are printed without A/B or a/b.
- Ch. 12 uses some element numbers for a different kind of feature than ch. 11 defines:
  - "porte" 324 (L74), 337 (L51), 415 (L12, L13), 685 (L134) and 854 (L77).
  - "passage" 232 (L17) and 322 (L25).
  - "glacis 252" (L148; E592 also).
  - "four" 535/536 (L116/L115; silos in ch. 11).
  - "renforcement 592" (E706; a drain in ch. 11).
- Locations that look inconsistent:
  - L1 "partagé en L. 2/189" (L191 is the late partition of L1).
  - E270B/E271 "L. 5-16".
  - E341–344 place L191 by L43/52/53, while ch. 12 puts L191 at D3 in L1.
  - E374 "L. 153-154".
  - E518 tagged L. 172.
  - L183 "jouxtant l'empierrement du L. 99".
- E511 has a locus number missing in print. E650 is defined only as "mortier en amont de la vanne 658" but is called aqueduct 650 elsewhere (keyed `conduit`, low confidence).

Confidence: 679 high, 55 medium, 5 low (E650, E774, E875, E913, L183).

Working files (parser, key tables, builder) are in the scratchpad folder `q_A_q1/work/`. Nothing was committed.
