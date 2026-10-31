"""B4 pre-freeze preparation (no image score): placement log of every W2F verified letter and the item file.
Writes placements4.csv and items4.json (numbers and edition text only)."""
import csv, json, collections
import b4lib as B, items4 as I

acc = B.a2_accepted()
B.check_cache(sorted({c for c, _ in acc}))
rows, bad = B.w2f_letters()
pl = B.place_letters(rows, acc)
items, dropped, modelled, cnt, tr = I.build(pl)
held = {(i["col"], i["line"]) for i in items if i["split"] == "heldout"}
role = {}
for r in pl:
    k = (r["col"], r["line"])
    role[B.letter_id(r)] = ("target_line" if k in I.TARGETS else "heldout_line" if k in held else "train")
import ps
with open(f"{B.HERE}/placements4.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["letter_id", "column", "line", "word_index", "char_index", "letter", "copy_x", "copy_y", "placed", "cut",
                "frame_ref", "x88", "y88", "lh88", "box_x0", "box_y0", "box_x1", "box_y1", "placement_file",
                "distinctiveness", "local_median_lh", "placement_confidence", "role"])
    for r in pl:
        if r["placed"]:
            ref = ps.load_reg(r["cut"])["ref"]; h = 0.5 * r["lh88"]
            w.writerow([B.letter_id(r), r["column"], r["line"], r["wi"], r["ci"], r["letter"], r["cx"], r["cy"], 1,
                        r["cut"], ref, round(r["x88"], 1), round(r["y88"], 1), round(r["lh88"], 1),
                        round(r["x88"] - h, 1), round(r["y88"] - h, 1), round(r["x88"] + h, 1), round(r["y88"] + h, 1),
                        r["place_file"], round(r["dist"], 3), round(r["local_lh"], 3), r["conf"], role[B.letter_id(r)]])
        else:
            w.writerow([B.letter_id(r), r["column"], r["line"], r["wi"], r["ci"], r["letter"], r["cx"], r["cy"], 0] +
                       [""] * 13 + [role[B.letter_id(r)]])
json.dump({"items": items, "dropped": dropped, "modelled_forms": modelled, "train_counts": cnt,
           "n_train_letters": len(tr), "w2f_etcbc_mismatch": bad},
          open(f"{B.HERE}/items4.json", "w"), ensure_ascii=False, indent=1)
print("placed", sum(r["placed"] for r in pl), "of", len(pl), collections.Counter(role.values()))
print("items", collections.Counter(i["split"] for i in items), "dropped", dropped, "train letters", len(tr))
