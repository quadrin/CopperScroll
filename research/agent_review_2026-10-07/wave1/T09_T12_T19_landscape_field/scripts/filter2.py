import csv, sys, re
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
pat = sys.argv[2]; ctxpat = sys.argv[3] if len(sys.argv)>3 else '.'
hits = [r for r in rows if re.search(pat, re.sub(r"^el-Azarije, Jericho-Stra.e.*?usw.:", "", r["title"]), re.I) and re.search(ctxpat, r['context'], re.I)]
print(len(hits))
for r in hits:
    print(f"{r['signature']:<15}|{r['date'][:20]:<20}|{r['title'][:170]}|{r['gda_viewer'][31:]}")
