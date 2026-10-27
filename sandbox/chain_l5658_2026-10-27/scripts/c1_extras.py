"""Label-point distances for non-stone heaps (refuse dumps, modern spoil pile) to L56/58 and the channels."""
import sys, json, math
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
import importlib.util
spec = importlib.util.spec_from_file_location('c1', sys.argv[0].rsplit('/', 1)[0] + '/c1_distances.py')
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf): c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
items = {'Eastern Refuse Dump (Fig. 9 label)': (59.14, 56.82), 'Southern Refuse Dump (label)': (28.38, 64.48),
         'Northern Refuse Dump (label)': (40.56, -40.61), 'Northwestern Refuse Dump (label)': (-13.68, -50.53)}
spoil = [c1.r2t(p) for p in [(531, 372), (545, 362), (555, 385), (552, 425), (540, 428), (526, 395)]]  # Reeder 2002 'Outline of January 2002 Spoil Pile' (modern)
out = {}
for k, p in items.items():
    out[k] = {'d_L56_58': round(c1.dL(p), 1), 'd_T1': round(min(c1.dpoly(p, c1.CH[c]) for c in c1.MAIN), 1), 'd_T2': round(min(c1.dpoly(p, c1.CH[c]) for c in c1.NARROW), 1)}
P = c1.dense(spoil + [spoil[0]])
out['Jan 2002 spoil pile outline (modern; Reeder map)'] = {'d_L56_58': round(min(c1.dL(p) for p in P), 1), 'd_T1': round(min(min(c1.dpoly(p, c1.CH[c]) for c in c1.MAIN) for p in P), 1),
    'd_T2': round(min(min(c1.dpoly(p, c1.CH[c]) for c in c1.NARROW) for p in P), 1)}
for k, v in out.items(): print(k, v)
json.dump(out, open('out/c1_extras.json', 'w'), indent=1)
