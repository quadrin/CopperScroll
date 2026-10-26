# Run 4 rule: some caches have already been found and catalogued as hoards

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
If the scroll's amounts are in karsh (Method 10: 27 of 30 sums match some hoard's mass), some deposits may already sit in museum catalogues as ordinary hoards. A hoard is a **candidate recovery** of entry E if all four match:
1. **Metal:** the hoard's silver (or gold) matches the entry's silver (or gold); unspecified sums take silver plus gold.
2. **Mass:** the hoard's metal mass is within half to twice the entry's sum at 71 g or 142 g per karsh (talent sums at 21.3 kg / 42.6 kg also run).
3. **Hiding place:** the hoard's recorded context (hoards.csv `context_category`, `setting`, `placement`, `container`) is of the same class as the entry's (scroll_contexts.csv `setting_P`, `placement_P`, `container_P`). Unknown context = no match.
4. **Place:** the findspot is within 5 km of any candidate place for that entry (research/measurements/sequence/places.csv and the ratings.csv candidates), or, for entries with no placed candidate, inside the scroll region (31.40–32.55 N, 35.00–35.60 E).
Also: the hoard closes 63 BCE–135 CE.

## Data
research/comparanda/hoards_full/hoards.csv (204 rows; use `include` = 1); scroll sums from first_tests_2026-10-24/method10_hoards/scroll_sums.json; scroll contexts from research/comparanda/concealment_contexts/scroll_contexts.csv.

## Test
- Count hoard–entry pairs meeting all four conditions (k), and the entries involved.
- **Control:** 10,000 permutations shuffling the entries' sums and contexts together across entries (place kept with the entry); p = share with ≥ k pairs. Also report the count under each condition alone and in pairs, so the bottleneck is visible.
- **Lead:** any pair meeting all four. Report each with the hoard's source and context text. A lead is not an identification.
- If k = 0, report how many pairs fail only on condition 3 (unknown context), which is the AF447-style coverage gap.
