"""Exploratory: place every W2F verified letter (numbers only)."""
import collections, json
import b4lib as B
acc = B.a2_accepted()
print(sorted(acc))
B.check_cache(sorted({c for c, _ in acc}))
rows, bad = B.w2f_letters()
print("w2f rows", len(rows), "mismatch with ETCBC", bad)
pl = B.place_letters(rows, acc)
P = [r for r in pl if r["placed"]]
print("placed", len(P), "of", len(pl))
print(collections.Counter((r["column"], r["cut"]) for r in P))
print(collections.Counter(r["column"] for r in pl))
