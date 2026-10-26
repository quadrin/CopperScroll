"""Group x entry match matrix for every test (which entries each string could match)."""
import sys, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/greek_letters_2026-10-27')
import run
T = run.tests()
out = {}
for name, t in T.items():
    out[name] = {}
    for g in run.GROUPS:
        for s, who in run.VARIANTS[g]:
            hits = {}
            for e in run.ENTRIES:
                m = t(s, e)
                if m: hits[e] = m
            out[name][s] = hits
            if 'all_nouns' in name: continue
            print(name, s, {e: (m[0] if 'num' in name else [x[2] for x in m][:3]) for e, m in hits.items()})
json.dump(out, open(f'{run.HERE}/match_matrix.json', 'w'), ensure_ascii=False, indent=1)
for s in ['ΚΕΝ','ΧΑΓ','ΚΑΓ','ΗΝ','ΘΕ','ΞΕ','ΔΙ','ΤΡ','ΤΡΙ','ΣΚ','ΙΣΚ','ΧΚ','ΞΚ']:
    h = out['H-abbr/all_nouns'][s]
    print('all_nouns', s, len(h), 'entries;', sorted({x[2] for v in h.values() for x in v})[:12])
