import csv, json, sys
rows = list(csv.DictReader(open(sys.argv[1])))
T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
out = {}
for reading in ['strict', 'lenient']:
    for incl_b in [False, True]:
        key = f"{reading}{'+B' if incl_b else ''}"
        res = {'members': {}, 'leads': []}
        for cls in ['A', 'ctrl']:
            mem = [r for r in rows if r['reading'] == reading and (r['class'] == cls or (incl_b and cls == 'A' and r['class'] == 'B'))]
            p = sum(r[t] == 'pass' for r in mem for t in T)
            f = sum(r[t] == 'fail' for r in mem for t in T)
            u = sum(r[t] == 'unknown' for r in mem for t in T)
            n = len(mem)
            res['members'][cls] = {'n': n, 'pass': p, 'fail': f, 'unknown': u,
                                   'pass_per': round(p / n, 2), 'fail_per': round(f / n, 2)}
            if cls == 'A':
                for r in mem:
                    if all(r[t] == 'pass' for t in ['T1', 'T3', 'T4']) and not any(r[t] == 'fail' for t in T):
                        res['leads'].append(r['id'])
        a, c = res['members']['A'], res['members']['ctrl']
        better = a['pass_per'] > c['pass_per'] and a['fail_per'] <= c['fail_per']
        res['class_scores_better'] = better
        res['lead'] = bool(res['leads'])
        res['class_supported'] = better and bool(res['leads'])
        out[key] = res
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out, indent=1))
