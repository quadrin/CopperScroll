# Run 22 rule: reverse lookup from well-documented sites to entries

Fixed 27 Oct 2026 before any scoring for this run. Exploratory.

## Idea
Every test so far went from an entry to candidate sites. Here we go the other way: take the best-documented sites in the region and ask which of the 61 entries each one fully satisfies. This can surface matches nobody proposed.

## Sites (fixed now)
Kh. Qumran; the Jericho Hasmonean–Herodian palaces (Tulul Abu el-ʿAlayiq); Hyrcania; Upper and Lower Herodium; Masada (outside the region; scored, marked); Kypros; Alexandrium (Sartaba); the Temple Mount (from published surveys and descriptions only); the City of David / Siloam. Each site's feature inventory comes from its final reports and the repo's extractions; list the inventory per site, with sources, in a file with SHA-256 before step 2.

## Steps
1. **Entry relations:** for all 61 entries, the landmark and relations from text/readings.json and the editions (reuse run 10's and run 20's step-1 files where they exist; otherwise write them now).
2. **Score** every site × entry: pass / unknown / fail on each relation (as run 1); an entry is **satisfied** by a site if every relation passes, and **compatible** if none fails.
3. **Control:** score the same sites against 61 synthetic entries made by shuffling landmark words and relations across entries (10 shuffles). The real-to-shuffled ratio of satisfied pairs shows whether real entries fit real sites better than chance.

## Decision
- **Lead:** a satisfied site–entry pair not proposed in the editions or the repo (check ratings.csv and readings.json).
- **Supported** (exploratory): real entries are satisfied clearly more often than shuffled ones (permutation p < 0.05).
- Report the full site × entry matrix.
