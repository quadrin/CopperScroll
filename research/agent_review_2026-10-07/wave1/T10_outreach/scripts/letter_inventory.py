"""Count candidate training letters per class in the 3Q15 transcription.

Inputs (project files, trusted local copies):
  atlas_text.json : Abegg/Bowley/Cook ETCBC dss 2.0.1 transcription with per-segment flags
                    ('' = plain, 'u' = uncertain, 'x' = ?, 'r' = reconstructed, 'c' = corrected,
                     's' = supralinear, 'g' = Greek)  [flag meanings as used by the project atlas]
  readings.json   : project apparatus of edition disputes (Milik / Lefkovits / Puech ...)

A letter is a *candidate undisputed training letter* if
  (1) its segment flag is '' (no uncertainty / reconstruction / correction mark), and
  (2) its word is not the subject of a letter-level dispute in readings.json.
Rule (2): for each apparatus note whose 'reading' fields contain >=2 different consonantal
variants, every Hebrew word in those readings and in the note label is marked disputed *within
that note's entry*; a transcription word is excluded if it (or it minus 1-2 prefix letters)
matches, or contains a disputed string of >=3 letters. Meaning-only notes are ignored.
This is an approximation; a human pass over the excluded/included lists is still required.

Usage: python3 -I letter_inventory.py atlas_text.json readings.json OUT_PREFIX
"""
import sys, json, re, collections, csv

atlas = json.load(open(sys.argv[1]))
readings = json.load(open(sys.argv[2]))
out = sys.argv[3]
HEB = re.compile(r"[א-ת]+")
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}

disputed = collections.defaultdict(set)   # entry -> set of disputed consonantal words
for note in readings:
    texts = [r.get("reading", "") for r in note.get("readings", [])]
    variants = {"".join(HEB.findall(t)) for t in texts if HEB.findall(t)}
    if len(variants) < 2:
        continue                     # meaning-only note, or a single printed reading
    entry = note.get("entry", "")
    for t in texts + [note.get("label", "")]:
        for w in HEB.findall(t):
            if len(w) >= 2:
                disputed[entry].add(w)
rows = []
for entry, lines in atlas["entries"].items():
    for line in lines:
        ref = line["ref"]
        for wi, w in enumerate(line["w"]):
            word = "".join(seg for seg, fl in w["h"])
            word_heb = "".join(HEB.findall(word))
            ds = disputed.get(entry, set())
            # strip common one-letter prefixes (b, h, w, l, m, sh, k) when comparing
            stems = {word_heb, word_heb[1:], word_heb[2:]} if len(word_heb) > 3 else {word_heb}
            word_disputed = any(st and st in ds for st in stems) or any(len(d) >= 3 and d in word_heb for d in ds)
            pos = 0
            for seg, fl in w["h"]:
                for ch in seg:
                    if HEB.fullmatch(ch):
                        rows.append({
                            "ref": ref, "entry": entry, "word_index": wi, "word": word_heb,
                            "char_index": pos, "letter": ch, "base": FINALS.get(ch, ch),
                            "final_form": ch in FINALS, "flag": fl,
                            "word_disputed": word_disputed,
                            "candidate_undisputed": (fl == "" and not word_disputed),
                        })
                    pos += 1

with open(out + "_letters.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wr.writeheader(); wr.writerows(rows)

tot = collections.Counter(r["letter"] for r in rows)
cand = collections.Counter(r["letter"] for r in rows if r["candidate_undisputed"])
flagged = collections.Counter(r["letter"] for r in rows if r["flag"] != "")
summary = []
for ch in sorted(tot, key=lambda c: -tot[c]):
    summary.append({"letter": ch, "all": tot[ch], "flagged": flagged[ch], "candidate_undisputed": cand[ch]})
with open(out + "_class_counts.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=["letter", "all", "flagged", "candidate_undisputed"])
    wr.writeheader(); wr.writerows(summary)
print("letters total", len(rows), "flagged", sum(flagged.values()),
      "candidate undisputed", sum(cand.values()), "disputed-word letters",
      sum(1 for r in rows if r["word_disputed"]))
for s in summary:
    print(s["letter"], s["all"], s["flagged"], s["candidate_undisputed"])
