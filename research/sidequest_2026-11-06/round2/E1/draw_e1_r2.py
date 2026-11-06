#!/usr/bin/env python3
"""E1 round-2 draw (6 Nov 2026). Seed string "2026-11-06-r2".
Seed number = first 8 bytes (big-endian) of SHA-256 of the UTF-8 seed string.
Population = round-1 population file (out/E1/population_E1_2026-11-06.csv, N=9902, sorted by Drive ID)
minus the 5 round-1 draws -> N=9897, kept in the same sort order.
Draws: rng.randrange(N) x6 in order. If a drawn file cannot be read (connector + bucket both fail) the
next rng.randrange(N) call replaces it (none recorded unless stated in FINDS.md).
Page draws for books > 300 pp: the next call after the six document draws, rng.randrange(pages)+1, in draw order.
Usage: python3 draw_e1_r2.py population_E1_2026-11-06.csv
"""
import csv, hashlib, random, sys
SEED_STR = "2026-11-06-r2"
seed = int.from_bytes(hashlib.sha256(SEED_STR.encode('utf-8')).digest()[:8], 'big')
R1 = {'149bBe5xYV8Jvw32b7aWE_O277vulC15O', '18O3MGFAX1yppiXtwVYN6ahEfuDDhGarR',
      '1CqSNKvEYJ34zyqdmOkfth9uDHdZo27Qt', '1Nq3DnQhfyvITXpWHnFaVL_tZgHCzpavT',
      '1-qFBKX5KnwEJB58QOG90NBEdTOfpMU2t'}
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding='utf-8')) if r['drive_id'] not in R1]
N = len(rows)
print('seed string', SEED_STR, '-> seed', seed, '; N =', N)
rng = random.Random(seed)
for k in range(int(sys.argv[2]) if len(sys.argv) > 2 else 6):
    i = rng.randrange(N); r = rows[i]
    print(f"draw {k+1}: index {i}  {r['drive_id']}  {r['source']}  {r['path_or_title']}")
