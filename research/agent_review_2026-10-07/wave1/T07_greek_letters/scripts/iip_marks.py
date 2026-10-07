"""Extract short Greek 'mark' tokens (1-4 letters, standalone) from all IIP editions,
within the extended window (overlapping 200 BCE-250 CE), plus target-group hits.

Token sources: every <w>, <orig>, <num>, <abbr> element of the transcription_segmented
and transcription editions, plus whitespace tokens of the diplomatic edition.
Outputs: data/iip_short_marks.csv, data/iip_mark_hits.csv, data/iip_mark_baseline.json
"""
import sys, json, re, csv, collections, os
sys.path.insert(0, os.path.dirname(__file__))
from iip_search import gnorm, overlap, ALLG, GROUPS, TEI, parse, text_of

CORE_PREFIX = {'jeru','masa','jeri','hero','qumr','akld','hebr','mare','idum','beth','bleh','emma',
               'geze','jmon','moli','ksus','susi','naar','tjez','beit','sepp','tibe'}

def tokens_of(ins):
    toks = []
    for e in ins['editions']:
        et = e['edition_type']
        if et == 'translation':
            continue
        root = parse(e['raw_xml'])
        if root is None:
            continue
        if et in ('transcription_segmented', 'transcription'):
            for tag in ('w', 'orig', 'num', 'abbr'):
                for el in root.iter(TEI + tag):
                    t = gnorm(text_of(el))
                    if t:
                        toks.append((et, tag, t, text_of(el).strip()))
        txt = text_of(root)
        for raw in re.split(r'[\s\.\·\,\;\:\-\|/\[\]\(\)]+', txt):
            t = gnorm(raw)
            if t:
                toks.append((et, 'split', t, raw))
    return toks

def main(path, outdir):
    d = json.load(open(path, encoding='utf8'))
    short = []
    hits = []
    n_ins_window = 0
    for ins in d:
        ext = overlap(ins, -200, 250)
        core_t = overlap(ins, -200, 135)
        fn = ins['filename']
        city = (ins.get('city') or {}).get('placename')
        title = re.sub(r'\s+', ' ', ins.get('title') or '')
        desc = re.sub(r'\s+', ' ', ins.get('description') or '')
        toks = tokens_of(ins)
        seen = set()
        for (et, tag, t, raw) in toks:
            key = (t,)
            if 1 <= len(t) <= 4 and ext and tag in ('orig', 'num', 'abbr', 'split', 'w'):
                if (t, tag) not in seen:
                    seen.add((t, tag))
                    short.append(dict(file=fn, city=city, nb=ins.get('not_before'), na=ins.get('not_after'),
                                      core_time=core_t, core_region=fn[:4] in CORE_PREFIX, tag=tag, token=t,
                                      raw=raw, title=title[:120]))
            for g in ALLG:
                if t == g:
                    hits.append(dict(group=g, file=fn, city=city, nb=ins.get('not_before'), na=ins.get('not_after'),
                                     core_time=core_t, ext=ext, tag=tag, edition=et, raw=raw, title=title[:120], desc=desc[:300]))
        if ext:
            n_ins_window += 1
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, 'iip_short_marks.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=list(short[0].keys()))
        w.writeheader(); w.writerows(short)
    # dedupe hits per (group, file)
    dd = {}
    for h in hits:
        dd.setdefault((h['group'], h['file']), h)
    with open(os.path.join(outdir, 'iip_mark_hits.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=list(hits[0].keys()))
        w.writeheader(); w.writerows(sorted(dd.values(), key=lambda h: (ALLG.index(h['group']), h['file'])))
    # baseline: inscriptions in window whose WHOLE Greek token set consists of short marks only
    perfile = collections.defaultdict(set)
    for s in short:
        perfile[s['file']].add(s['token'])
    c23 = collections.Counter(s['token'] for s in short if 2 <= len(s['token']) <= 3 and s['tag'] in ('orig', 'split'))
    print('inscriptions in ext window', n_ins_window)
    print('distinct short-token occurrences (file,token,tag) in window:', len(short))
    print('2-3 letter tokens (orig/split), total occurrences', sum(c23.values()), 'distinct', len(c23))
    json.dump(dict(n_ins_window=n_ins_window, n_short=len(short), c23_total=sum(c23.values()),
                   c23_top=c23.most_common(100)), open(os.path.join(outdir, 'iip_mark_baseline.json'), 'w', encoding='utf8'),
              ensure_ascii=False, indent=1)
    for k in sorted(dd.values(), key=lambda h: (ALLG.index(h['group']), h['file'])):
        if k['ext']:
            print(k['group'], k['file'], k['city'], k['nb'], k['na'], k['tag'], k['edition'], '|', k['raw'][:40], '|', k['title'][:80], '|', k['desc'][:150])

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
