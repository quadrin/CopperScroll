import csv, json
R='/home/claude/copperscroll/'
rows=list(csv.DictReader(open(R+'research/comparanda/concealment_contexts/scroll_contexts.csv',encoding='utf-8')))
res=json.load(open('results.json',encoding='utf-8'))
ci=set(res['cons_inclusive']); cu=set(res['cons_unflagged']); mi=set(res['metal_inclusive']); bi=set(res['bullion_inclusive'])
W={'cistern','pool_reservoir','channel'}
w=csv.writer(open('per_entry.csv','w',encoding='utf-8',newline=''))
w.writerow(['entry','object_type','consecrated_incl','consecrated_unflagged','silver_gold','any_sum','P','Pu','M','L','funerary_P','water_lit_P','water_G1_P'])
for r in rows:
    e=r['entry']
    w.writerow([e,r['object_type'],int(e in ci),int(e in cu),int(e in mi),int(e in bi),r['setting_P'],r['setting_Pu'],r['setting_M'],r['setting_L'],
                int(r['setting_P']=='tomb' or e=='60'),int(r['setting_P'] in W),int(r['setting_P'] in W|{'water_pit'})])
    if e in ci: print(e, r['object_type'], r['setting_P'],r['setting_Pu'],r['setting_M'],r['setting_L'])
