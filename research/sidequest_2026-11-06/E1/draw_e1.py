#!/usr/bin/env python3
"""Reproduce the E1 random draw (side-quest swarm, 6 Nov 2026).

Inputs:
  1. Drive "00 drive_manifest.csv" (file ID 11re7I3lCF4uSl7My6v4V__9Im9VbTSgs, modified 2026-10-30T21:50:47Z),
     downloaded as-is (UTF-8 with BOM, columns path,drive_id,bytes_or_folder,former_name).
  2. live_additions_2026-11-06.csv (this folder): documents found live on 6 Nov in folders 04-09 that are
     not in the manifest. Built from two Drive queries:
       (a) parentId in {04,05,06,07,08,09} and createdTime > '2026-10-30T21:50:00Z'  (depth 1, 20 items)
       (b) parentId in the six new depth-1 subfolders that (a) returned (Reading catalogue (2026-11),
           IAA Mandate archive, Session chunks 2026-10-31, novel reruns 2026-10-31, HEXAGON COG 2026-10-30,
           Albright Jerusalem 1:2000 sheets)  (depth 2, 368 items, 4 pages)
     Deeper levels (e.g. IAA Mandate archive/04 Further archive reading) were NOT listed.
Usage: python3 draw_e1.py drive_manifest.csv live_additions_2026-11-06.csv
"""
import csv, os, random, sys

DOC_EXT = {'.pdf', '.epub', '.docx', '.doc', '.gdoc', '.md', '.txt', '.html', '.htm',
           '.csv', '.tsv', '.xlsx', '.gsheet', '.rtf'}
DOC_MIME = {'application/pdf', 'text/plain', 'text/markdown', 'text/csv', 'text/tab-separated-values',
            'application/vnd.google-apps.document', 'text/html',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.google-apps.spreadsheet'}

man, live = sys.argv[1], sys.argv[2]
pop = {}
for r in csv.DictReader(open(man, encoding='utf-8-sig')):
    if r['bytes_or_folder'] == 'folder' or r['path'].startswith('99 '):
        continue
    if os.path.splitext(r['path'])[1].lower() in DOC_EXT and r['drive_id']:
        pop[r['drive_id']] = ('manifest', r['path'])
for r in csv.DictReader(open(live, encoding='utf-8')):
    if r['mime'] in DOC_MIME and r['drive_id'] not in pop:
        pop[r['drive_id']] = (r['source'], r['title_with_parent'])
ids = sorted(pop)                       # plain Python string sort of Drive file IDs
N = len(ids)
print('population N =', N)              # expected 9902 (9627 manifest + 275 live)
rng = random.Random(20261106)
for k in range(5):                      # document draws 1-5 (no redraws were needed)
    i = rng.randrange(N)
    print(f'draw {k+1}: index {i}  {ids[i]}  {pop[ids[i]]}')
# Draw 3 (Leibner 2018, 669 PDF pages > 300) gets a page draw = the next call on the same RNG:
print('page draw for draw 3:', rng.randrange(669) + 1)   # expected 633 -> book p. 624 -> Chapter 20
