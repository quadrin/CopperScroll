#!/usr/bin/env python3
"""Build controls_manifest.csv: candidate control letters for the XII 10 reading calibration.

Run from any directory, with the Python standard library only:

    python3 -I research/text/letter_controls/build_manifest.py
    python3 -I research/text/letter_controls/build_manifest.py --puech2015 PATH   # refresh edition_checks.csv

Inputs are existing repository records (listed in INPUTS). The optional Puech 2015 text is a
local, copyrighted extract that stays outside the repository. Only per-word comparison results
(same / restored / corrected / differs) are stored in edition_checks.csv.

Design rules (see PROTOCOL.md):
- Columns I-X only. Column XI is adjacent to the XII 10 line start and column XII contains the
  segment 21/22 cut, so neither supplies controls.
- A tier A control letter is unflagged in the ETCBC transcription, passes the wave-1 T10
  "candidate undisputed" rule against readings.json, appears in the same word in Puech 2015,
  lies outside the lines of the earlier plate check, and has no exclusion in manual_checks.csv.
- Tier B letters are named in manual_checks.csv: an edition records damage (saw cut, crack, edge
  loss) while all editions keep the same letter.
- A decoy is a restored letter inside a lacuna that both the transcription and Puech 2015 mark.
  Its secure answer is "illegible".
- Each physical letter is used in at most one candidate row.
The output is deterministic for fixed inputs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

INPUTS = {
    'inventory': 'research/agent_review_2026-10-07/wave1/T10_outreach/data/inventory_letters.csv',
    'verified': 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data/labels_verified.csv',
    'registration': 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data/registration.json',
    'plates': 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data/plate_index.csv',
    'plate_check_key': 'registration/plate_check/key.json',
    'edition_checks': 'research/text/letter_controls/edition_checks.csv',
    'manual_checks': 'research/text/letter_controls/manual_checks.csv',
}
OUT = HERE / 'controls_manifest.csv'
SHA_FILE = HERE / 'sealed_key.sha256'

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
COL = {r: i + 1 for i, r in enumerate(ROMAN)}
FINALS = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
MAX_COLUMN = 10
# Puech 2015 printed page where each column's transcription starts (table of contents, p. v).
PUECH2015_PAGE = {'I': 25, 'II': 38, 'III': 43, 'IV': 48, 'V': 54, 'VI': 59, 'VII': 62,
                  'VIII': 68, 'IX': 75, 'X': 85, 'XI': 93, 'XII': 106}
# Caps on tier A candidates per question and class. Tier B rows are always kept.
# The pool is larger than the per-series minimum (PROTOCOL.md) because damage is graded only on the
# series images, and some candidates will be missing from a given series.
CAPS = {('BK', 'ב'): 60, ('BK', 'כ'): 60, ('HH', 'ה'): 60, ('HH', 'ח'): 60, ('HH', 'ת'): 40,
        ('XS', 'present'): 40, ('XS', 'absent'): 45}
FIELDS = ['candidate_id', 'question', 'use', 'tier', 'secure_answer', 'column', 'line', 'ref',
          'word_index', 'etcbc_word', 'char_index', 'slot_letter', 'slot_definition', 'match_level',
          'why_secure', 'edition_notes', 'damage_from_editions', 'crop_box', 'crop_frame',
          'djd3_photo_plate', 'djd3_handcopy_plate', 'puech2006_radiograph_plates',
          'usc_1988_cuts_candidate', 'repo_image_adequate', 'needed_image', 'sealed_key_sha256']


def roman(n: int) -> str:
    vals = [(100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    out = ''
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def norm(word: str) -> str:
    return ''.join(FINALS.get(c, c) for c in word)


def read_csv(rel):
    with (ROOT / rel).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def ref_key(ref: str):
    c, l = ref.split()
    return COL[c], int(l)


# ---------------------------------------------------------------- Puech 2015 comparison

def parse_puech2015(path: Path) -> dict:
    """Return {column: {line: text}} from the Puech 2015 transcription pages (columns I-XII)."""
    lines = path.read_text(encoding='utf-8').split('\n')
    heads = [i for i, l in enumerate(lines) if re.match(r'^Col\. ([IVX]+) \(Figure \d+\)\s*$', l)][:12]
    out = {}
    for h in heads:
        col = re.match(r'^Col\. ([IVX]+)', lines[h]).group(1)
        seq = []
        for l in lines[h + 1:h + 45]:
            if l.startswith('Translation'):
                break
            if not re.search(r'[א-ת]', l):
                continue
            num, body = None, l
            m = re.match(r'^(.*?)(\d{1,2})\s*$', l)
            if m and re.search(r'‬\s*\(?\d*\(?\s*\d{1,2}\s*$', l):
                num, body = int(m.group(2)), m.group(1)
            seq.append([num, body.replace('‫', '').replace('‬', '').strip()])
        for i, (n, _) in enumerate(seq):
            if n is None:
                nxt = next(((j, seq[j][0]) for j in range(i + 1, len(seq)) if seq[j][0] is not None), None)
                prv = next(((j, seq[j][0]) for j in range(i - 1, -1, -1) if seq[j][0] is not None), None)
                seq[i][0] = nxt[1] - (nxt[0] - i) if nxt else (prv[1] + (i - prv[0]) if prv else None)
        out[col] = {str(n): b for n, b in seq if n is not None}
    return out


def compare_word(tokens, word: str) -> str:
    """Compare one transcription word with the tokens of the same Puech 2015 line.

    same                  the same letters with no sigla
    same_adjacent_lacuna  the same letters; a lacuna bracket only touches the word edge from outside
    restored              the same letters, but some of them sit inside lacuna brackets
    corrected             the same letters with correction sigla: ( ) { } < > or [[ ]]
    differs               no token with the same letters
    """
    w = norm(word)
    for t in tokens:
        if re.fullmatch(r'[\u05d0-\u05ea]+', t) and norm(t) == w:
            return 'same'
    for t in tokens:
        if norm(re.sub(r'[^\u05d0-\u05ea]', '', t)) != w:
            continue
        if '[[' in t or ']]' in t or re.search(r'[(){}<>]', t):
            return 'corrected'
        core = re.sub(r'^\]+', '', re.sub(r'\[+$', '', t))
        if '[' not in core and ']' not in core:
            return 'same_adjacent_lacuna'
        return 'restored'
    return 'differs'


def refresh_edition_checks(puech_path: Path, words):
    p15 = parse_puech2015(puech_path)
    rows = []
    for (ref, wi), word in sorted(words.items(), key=lambda kv: (ref_key(kv[0][0]), kv[0][1])):
        col, line = ref.split()
        if COL[col] > MAX_COLUMN:
            continue
        text = p15.get(col, {}).get(line)
        if text is None:
            result, lacuna = 'line_missing', ''
        else:
            tokens = [re.sub(r'^[()\d]+|[()\d]+$', '', t) for t in text.split()]
            result = compare_word(tokens, word)
            lacuna = 'yes' if re.search(r'\[(?!\[)|(?<!\])\]', text.replace('[[', '').replace(']]', '')) else 'no'
        rows.append({'ref': ref, 'word_index': wi, 'etcbc_word': word, 'puech2015': result,
                     'puech2015_line_has_lacuna': lacuna, 'puech2015_page': PUECH2015_PAGE[col]})
    overrides = {(m['ref'], norm(m['etcbc_word'])): m for m in read_csv(INPUTS['manual_checks'])
                 if m['action'] == 'puech_same'}
    for r in rows:
        m = overrides.get((r['ref'], norm(r['etcbc_word'])))
        if m:
            r['puech2015'] = 'same'
            r['puech2015_note'] = f"manual: {m['source']}"
        else:
            r['puech2015_note'] = ''
    with (ROOT / INPUTS['edition_checks']).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    return rows


# ---------------------------------------------------------------- inputs

def load_letters():
    letters = {}
    for r in read_csv(INPUTS['inventory']):
        k = (r['ref'], int(r['word_index']), int(r['char_index']))
        if k in letters:  # lines shared by two entries appear twice; keep the stricter flag
            letters[k]['t10'] = letters[k]['t10'] and r['candidate_undisputed'] == 'True'
            continue
        letters[k] = {'ref': r['ref'], 'wi': k[1], 'ci': k[2], 'letter': r['letter'], 'base': r['base'],
                      'flag': r['flag'], 't10': r['candidate_undisputed'] == 'True'}
    words = defaultdict(list)
    for k in sorted(letters, key=lambda k: (ref_key(k[0]), k[1], k[2])):
        words[(k[0], k[1])].append(letters[k])
    return letters, words


def plate_check_lines():
    key = json.loads((ROOT / INPUTS['plate_check_key']).read_text(encoding='utf-8'))
    out = set()
    for item in key['items'].values():
        m = re.match(r'^([IVX]+)(\d+)$', item['line'])
        out.add(f'{m.group(1)} {int(m.group(2))}')
    return out


def locator_boxes():
    reg = json.loads((ROOT / INPUTS['registration']).read_text(encoding='utf-8'))
    boxes = {}
    for r in read_csv(INPUTS['verified']):
        A = reg[r['col']]['A_fac2photo']
        xs, ys = [], []
        for x in (float(r['fx0']), float(r['fx1'])):
            for y in (float(r['fy0']), float(r['fy1'])):
                xs.append(A[0][0] * x + A[0][1] * y + A[0][2])
                ys.append(A[1][0] * x + A[1][1] * y + A[1][2])
        boxes[(r['ref'], int(r['word_index']), int(r['char_index']))] = (
            round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)))
    return boxes


def plate_refs():
    rad, copy, cuts = defaultdict(list), {}, defaultdict(set)
    for r in read_csv(INPUTS['plates']):
        col = r['column']
        if r['series'] == 'radiograph':
            label = f"pl. {r['plate']} ({r['segment_labels_in_caption']})"
            if label not in rad[col]:
                rad[col].append(label)
            cuts[col].update(int(x) for x in re.findall(r'(?:^|\s)(\d+)', r['segment_labels_in_caption']))
        elif r['series'] == 'copy_photo' and col in COL:
            copy[col] = r['plate']
    return rad, copy, cuts


def load_manual():
    rows = read_csv(INPUTS['manual_checks'])
    for r in rows:
        if r['action'] not in ('damage', 'readmit', 'exclude', 'exclude_decoy', 'analogue', 'decoy_tier_b', 'puech_same'):
            raise ValueError(f"unknown action {r['action']!r} in manual_checks.csv")
    return rows


def manual_matches(row, ref, word, ci=None):
    if row['ref'] != ref:
        return False
    if row['etcbc_word'] != '*' and norm(row['etcbc_word']) != norm(word):
        return False
    if ci is not None and row['char_index'] != '*' and int(row['char_index']) != ci:
        return False
    return True


# ---------------------------------------------------------------- candidates

def build(sealed_sha: str = ''):
    letters, words = load_letters()
    word_text = {k: ''.join(x['letter'] for x in v) for k, v in words.items()}
    ed_path = ROOT / INPUTS['edition_checks']
    if not ed_path.exists():
        raise SystemExit('edition_checks.csv is missing; run once with --puech2015 PATH')
    edition = {(r['ref'], int(r['word_index'])): r for r in read_csv(INPUTS['edition_checks'])}
    manual = load_manual()
    pc_lines = plate_check_lines()
    boxes = locator_boxes()
    rad, copy, cuts = plate_refs()

    def manual_rows(ref, word, ci, actions):
        return [m for m in manual if m['action'] in actions and manual_matches(m, ref, word, ci)]

    def excluded(L, word):
        return bool(manual_rows(L['ref'], word, L['ci'], ('exclude',)))

    def bor_rule(L, ls):
        # Lefkovits 2000 p. 125: the noun בור can also be read כור (bet read as kaf).
        w = ''.join(x['letter'] for x in ls)
        i = w.find('בור')
        return i >= 0 and L['ci'] == ls[i]['ci'] and w[i:] == 'בור'

    def tier_a(L, ls):
        word = ''.join(x['letter'] for x in ls)
        ed = edition.get((L['ref'], L['wi']), {})
        return (L['flag'] == '' and L['t10'] and ed.get('puech2015') in ('same', 'same_adjacent_lacuna')
                and L['ref'] not in pc_lines and not excluded(L, word))

    def evidence(L, ls, tier, extra_note=''):
        word = ''.join(x['letter'] for x in ls)
        col = L['ref'].split()[0]
        ed = edition.get((L['ref'], L['wi']), {})
        parts = []
        parts.append('ETCBC transcription (Abegg, Bowley, Cook): ' + (
            'letter unflagged' if L['flag'] == '' else f"letter flagged '{L['flag']}'"))
        parts.append('readings.json: no letter dispute for this word (T10 rule)' if L['t10']
                     else 'readings.json/T10 rule: word not cleared automatically; admitted by edition note')
        res = ed.get('puech2015', 'not_checked')
        parts.append(f"Puech 2015 p. {PUECH2015_PAGE[col]}: " + {
            'same': 'same word, no sigla', 'same_adjacent_lacuna': 'same word; a lacuna touches the word edge',
            'restored': 'word bracketed as restored',
            'corrected': 'word carries correction sigla', 'differs': 'reads differently or divides differently',
            'line_missing': 'line not parsed'}.get(res, res)
                     + (f" ({ed['puech2015_note']})" if ed.get('puech2015_note') else ''))
        if (L['ref'], L['wi'], L['ci']) in boxes:
            parts.append('Puech 2006 facsimile: a drawn letter sits at this position (W2F alignment, AI review)')
        parts.append('Lefkovits 2000 commentary: no letter alternative found (keyword search, hits reviewed)'
                     if tier == 'A' else
                     'Lefkovits 2000 / Puech 2015 note: identity kept, damage recorded')
        parts.append('Milik 1962: only through readings.json and Lefkovits')
        return '; '.join(parts)

    def plates(col_roman):
        c = COL[col_roman]
        photo, hand = 47 + 2 * c, 46 + 2 * c
        return (f'DJD III pl. {roman(photo)} (PDF p. {photo + 12})',
                f'DJD III pl. {roman(hand)} (PDF p. {hand + 12})',
                '; '.join(rad.get(col_roman, [])),
                ';'.join(str(x) for x in sorted(cuts.get(col_roman, set()))))

    def crop(keys, col_roman):
        bs = [boxes[k] for k in keys if k in boxes]
        if len(bs) != len(keys):
            return '', ''
        x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
        x1, y1 = max(b[2] for b in bs), max(b[3] for b in bs)
        return (f'{x0},{y0},{x1},{y1}',
                f"Puech 2006 vol. II pl. {copy[col_roman]} copy photograph, W2F extraction pixels; "
                'locator only: a copy, not an original image')

    def needed(col_roman):
        cs = ';'.join(str(x) for x in sorted(cuts.get(col_roman, set())))
        c = COL[col_roman]
        return (f'Same series as the target: WSRP 1988 master of cut(s) {cs} recto under the target lighting; '
                f'or an original print/negative of DJD III pl. {roman(47 + 2 * c)} (Manchester 1950s photograph); '
                f'or the EDF radiograph of segment(s) {cs}')

    used = set()
    rows = []

    def add(q, use, tier, answer, L, ls, slot_def, match, keys, note='', damage=''):
        col_roman = L['ref'].split()[0]
        word = ''.join(x['letter'] for x in ls)
        photo, hand, radi, cs = plates(col_roman)
        box, frame = crop(keys, col_roman)
        rows.append({
            'question': q, 'use': use, 'tier': tier, 'secure_answer': answer,
            'column': col_roman, 'line': L['ref'].split()[1], 'ref': L['ref'], 'word_index': L['wi'],
            'etcbc_word': word, 'char_index': L['ci'], 'slot_letter': L['letter'],
            'slot_definition': slot_def, 'match_level': match,
            'why_secure': (evidence(L, ls, tier) if use == 'control' else note),
            'edition_notes': note if use == 'control' else '',
            'damage_from_editions': damage or 'not recorded; grade on the series image',
            'crop_box': box, 'crop_frame': frame,
            'djd3_photo_plate': photo, 'djd3_handcopy_plate': hand,
            'puech2006_radiograph_plates': radi, 'usc_1988_cuts_candidate': cs,
            'repo_image_adequate': 'no (DJD III scan compressed to a 1-bit mask; USC preview about 25 px per letter; '
                                   'Puech plates not in the repository)',
            'needed_image': needed(col_roman), 'sealed_key_sha256': sealed_sha})
        used.update(keys)

    def k(L):
        return (L['ref'], L['wi'], L['ci'])

    in_scope = [(key, ls) for key, ls in words.items() if COL[key[0].split()[0]] <= MAX_COLUMN]

    # Tier B: letters named in manual_checks.csv with damage or readmission.
    for m in manual:
        if m['action'] not in ('damage', 'readmit'):
            continue
        hits = [(key, ls) for key, ls in in_scope if key[0] == m['ref'] and norm(word_text[key]) == norm(m['etcbc_word'])]
        if len(hits) != 1:
            raise ValueError(f"manual row {m['ref']} {m['etcbc_word']} matches {len(hits)} words")
        key, ls = hits[0]
        L = next(x for x in ls if x['ci'] == int(m['char_index']))
        if m['action'] == 'damage' and not tier_a(L, ls):
            raise ValueError(f"manual damage row {m['ref']} {m['etcbc_word']} is not a tier A letter; use readmit")
        note = f"{m['source']}: {m['note']}"
        if m['question'] == 'BK':
            add('BK', 'control', 'B', L['base'], L, ls, 'box letter: bet or kaf', 'damage-matched', [k(L)], note, m['damage'])
        elif m['question'] == 'HH':
            pos = 'word_final' if L is ls[-1] else ('word_initial' if L['ci'] == ls[0]['ci'] else 'medial')
            add('HH', 'control', 'B', L['base'], L, ls, 'roofed letter: he, het or taw', pos + '; damage-matched', [k(L)], note, m['damage'])

    # XS controls: box letter followed by an optional yod/waw and a marked next letter.
    xs = {'present': [], 'absent': []}
    for key, ls in in_scope:
        word = ''.join(x['letter'] for x in ls)
        for i, L in enumerate(ls):
            if i + 1 >= len(ls) or L['letter'] in 'יוך':
                continue
            nxt = ls[i + 1]
            if L['base'] not in 'בכ':
                # Level 3 (present only): another letter + yod/waw + nun, as in the proposed
                # yod-nun sequence. ככרין is skipped: its res-yod group differs between drawings
                # (Lefkovits 2000 pp. 49, 474-475).
                if (nxt['letter'] in 'יו' and i + 2 < len(ls) and ls[i + 2]['letter'] in 'נן'
                        and 'ככרין' not in word and all(tier_a(p, ls) for p in (L, nxt, ls[i + 2]))):
                    xs['present'].append(('other+yw+nun', L, ls, [L, nxt, ls[i + 2]]))
                continue
            if nxt['letter'] in 'יו':
                if i + 2 >= len(ls) or ls[i + 2]['letter'] in 'יו':
                    continue
                parts, cls = [L, nxt, ls[i + 2]], 'present'
                match = 'box+yw+nun' if ls[i + 2]['letter'] in 'נן' else 'box+yw+other'
            else:
                parts, cls = [L, nxt], 'absent'
                match = 'box+nun' if nxt['letter'] in 'נן' else 'box+other'
            if all(tier_a(p, ls) for p in parts):
                xs[cls].append((match, L, ls, parts))

    def column_spread(cands, rank):
        """Order candidates by match rank, then locator availability, then round-robin over columns."""
        by_col = defaultdict(list)
        for c in sorted(cands, key=lambda c: (rank(c), (ref_key(c[1]['ref']), c[1]['wi'], c[1]['ci']))):
            by_col[c[1]['ref'].split()[0]].append(c)
        order = []
        for col, lst in by_col.items():
            for j, c in enumerate(lst):
                order.append((rank(c), j, COL[col], c))
        return [c for *_, c in sorted(order, key=lambda t: (t[0], t[1], t[2]))]

    xs_rank = {'box+yw+nun': 0, 'box+nun': 0, 'box+yw+other': 1, 'box+other': 1, 'other+yw+nun': 2}
    bk = defaultdict(list)
    for key, ls in in_scope:
        for i, L in enumerate(ls):
            if L['base'] in 'בכ' and L['letter'] != 'ך' and tier_a(L, ls) and not bor_rule(L, ls):
                match = 'after_shin' if i > 0 and ls[i - 1]['letter'] == 'ש' else ('word_initial' if i == 0 else 'medial')
                bk[L['base']].append((match, L, ls))
    bk_rank = {'after_shin': 0, 'word_initial': 1, 'medial': 2}
    hh = defaultdict(list)
    for key, ls in in_scope:
        for i, L in enumerate(ls):
            if L['base'] in 'החת' and tier_a(L, ls):
                match = 'word_final' if i == len(ls) - 1 else ('word_initial' if i == 0 else 'medial')
                hh[L['base']].append((match, L, ls))
    hh_rank = {'word_final': 0, 'medial': 1, 'word_initial': 2}
    taken = defaultdict(int)

    def allocate_xs(levels):
        for cls in ('present', 'absent'):
            for match, L, ls, parts in column_spread(xs[cls], lambda c: (xs_rank[c[0]], 0 if k(c[1]) in boxes else 1)):
                keys = [k(p) for p in parts]
                if match not in levels or any(x in used for x in keys) or taken[('XS', cls)] >= CAPS[('XS', cls)]:
                    continue
                mark = parts[-1]['letter']
                first = 'box letter' if L['base'] in 'בכ' else 'marked letter'
                add('XS', 'control', 'A', cls, L, ls,
                    f'between the {first} {L["letter"]} and the next marked letter {mark}: independent yod/waw?',
                    match, keys)
                taken[('XS', cls)] += 1

    def allocate_single(q, pool, rank_map, classes, levels, slot_def):
        for cls in classes:
            for match, L, ls in column_spread(pool[cls], lambda c: (rank_map[c[0]], 0 if k(c[1]) in boxes else 1)):
                if match not in levels or k(L) in used or taken[(q, cls)] >= CAPS[(q, cls)]:
                    continue
                add(q, 'control', 'A', cls, L, ls, slot_def, match, [k(L)])
                taken[(q, cls)] += 1

    # Allocation order keeps the closest matches to the target for each question:
    # XS box+nun first, then BK after shin, then the remaining XS, BK and HH candidates.
    allocate_xs({'box+yw+nun', 'box+nun'})
    allocate_single('BK', bk, bk_rank, ('ב', 'כ'), {'after_shin'}, 'box letter: bet or kaf')
    allocate_xs({'box+yw+other', 'box+other', 'other+yw+nun'})
    allocate_single('BK', bk, bk_rank, ('ב', 'כ'), {'word_initial', 'medial'}, 'box letter: bet or kaf')
    allocate_single('HH', hh, hh_rank, ('ה', 'ח', 'ת'), {'word_final', 'medial', 'word_initial'},
                    'roofed letter: he, het or taw')

    # Decoys: restored letters inside a lacuna shared by the transcription and Puech 2015.
    for key, ls in in_scope:
        ref, wi = key
        restored = [L for L in ls if L['flag'] == 'r']
        if not restored:
            continue
        word = word_text[key]
        if [m for m in manual if m['action'] == 'exclude_decoy' and manual_matches(m, ref, word)]:
            continue
        ed = edition.get(key, {})
        if ed.get('puech2015') == 'restored':
            tier = 'A'
        elif ed.get('puech2015') == 'differs' and ed.get('puech2015_line_has_lacuna') == 'yes':
            tier = 'B'
        else:
            continue
        if [m for m in manual if m['action'] == 'decoy_tier_b' and manual_matches(m, ref, word)]:
            tier = 'B'
        L = restored[0]
        if k(L) in used:
            continue
        q = 'BK' if L['base'] in 'בכ' else ('HH' if L['base'] in 'החת' else 'XS')
        col = ref.split()[0]
        note = (f"Transcription restores this letter (flag r); Puech 2015 p. {PUECH2015_PAGE[col]} "
                + ('brackets the same word' if tier == 'A' else 'has a lacuna in this line with a different restoration')
                + '. Secure answer: no legible letter.')
        add(q, 'decoy', tier, 'illegible', L, ls, f'slot inside a lacuna; question asked as {q}', 'lacuna', [k(L)], note, 'edge_loss')

    # Unkeyed analogues: disputed cases like XII 10, listed for later specialist work, never scored.
    for m in manual:
        if m['action'] != 'analogue':
            continue
        col_roman, line = m['ref'].split()
        photo, hand, radi, cs = plates(col_roman)
        rows.append({'question': m['question'], 'use': 'analogue_unkeyed', 'tier': '', 'secure_answer': '',
                     'column': col_roman, 'line': line, 'ref': m['ref'], 'word_index': '', 'etcbc_word': m['etcbc_word'],
                     'char_index': '', 'slot_letter': '', 'slot_definition': 'disputed in the editions; not a control',
                     'match_level': 'analogue', 'why_secure': 'not secure: ' + m['note'],
                     'edition_notes': m['source'], 'damage_from_editions': m['damage'] or 'not recorded',
                     'crop_box': '', 'crop_frame': '', 'djd3_photo_plate': photo, 'djd3_handcopy_plate': hand,
                     'puech2006_radiograph_plates': radi, 'usc_1988_cuts_candidate': cs, 'repo_image_adequate': 'no',
                     'needed_image': needed(col_roman), 'sealed_key_sha256': sealed_sha})

    # Target slots: filled later from incoming XII 10 images under the frozen protocol.
    for q, d in (('BK', 'XII 10 word 2, second letter: bet or kaf'),
                 ('XS', 'XII 10 word 2, between the box letter and the nun-like letter: independent yod/waw?'),
                 ('HH', 'XII 10 word 2, last letter at the 21/22 cut: he, het or taw')):
        rows.append({'question': q, 'use': 'target_slot', 'tier': '', 'secure_answer': '', 'column': 'XII',
                     'line': '10', 'ref': 'XII 10', 'word_index': '', 'etcbc_word': '', 'char_index': '',
                     'slot_letter': '', 'slot_definition': d, 'match_level': 'target',
                     'why_secure': 'not keyed; filled from incoming images under the frozen XII 10 protocol',
                     'edition_notes': '', 'damage_from_editions': 'saw cut 21/22 and fold per the editions',
                     'crop_box': '', 'crop_frame': 'not opened by this worker', 'djd3_photo_plate': '',
                     'djd3_handcopy_plate': '', 'puech2006_radiograph_plates': '', 'usc_1988_cuts_candidate': '',
                     'repo_image_adequate': 'not applicable', 'needed_image': 'incoming image of XII 10 (frozen protocol)',
                     'sealed_key_sha256': sealed_sha})

    order_q = {'BK': 0, 'XS': 1, 'HH': 2}
    order_use = {'control': 0, 'decoy': 1, 'analogue_unkeyed': 2, 'target_slot': 3}
    order_ans = {'ב': 0, 'כ': 1, 'present': 0, 'absent': 1, 'ה': 0, 'ח': 1, 'ת': 2, 'illegible': 3, '': 4}

    def sort_key(r):
        col = COL.get(r['column'], 99)
        return (order_use[r['use']], order_q.get(r['question'], 9), order_ans.get(r['secure_answer'], 9),
                0 if r['tier'] == 'B' else 1, col, int(r['line']) if r['line'].isdigit() else 0,
                int(r['word_index']) if str(r['word_index']).isdigit() else 0,
                int(r['char_index']) if str(r['char_index']).isdigit() else 0)

    rows.sort(key=sort_key)
    counters = defaultdict(int)
    for r in rows:
        prefix = {'control': 'C', 'decoy': 'D', 'analogue_unkeyed': 'A', 'target_slot': 'T'}[r['use']]
        counters[(prefix, r['question'])] += 1
        r['candidate_id'] = f"LC-{prefix}{r['question']}-{counters[(prefix, r['question'])]:03d}"
    return rows


def candidate_digest(rows) -> str:
    """Hash of the candidate identities and answers, independent of the sealed-key column."""
    h = hashlib.sha256()
    for r in rows:
        h.update('|'.join(str(r[f]) for f in ('candidate_id', 'question', 'use', 'secure_answer', 'ref',
                                               'word_index', 'char_index')).encode('utf-8') + b'\n')
    return h.hexdigest()


def current_sealed_sha() -> str:
    if not SHA_FILE.exists():
        return ''
    lines = [l for l in SHA_FILE.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    return lines[-1].split()[0] if lines else ''


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--puech2015', type=Path, help='local Puech 2015 text extract; refreshes edition_checks.csv')
    ap.add_argument('--check', action='store_true', help='rebuild in memory and report whether the manifest is current')
    args = ap.parse_args(argv)
    if args.puech2015:
        _, words = load_letters()
        wt = {k: ''.join(x['letter'] for x in v) for k, v in words.items()}
        refresh_edition_checks(args.puech2015, wt)
    rows = build(current_sealed_sha())
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=FIELDS, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    text = s.getvalue()
    if args.check:
        same = OUT.exists() and OUT.read_text(encoding='utf-8') == text
        print('manifest current' if same else 'manifest differs from a fresh build')
        return 0 if same else 1
    OUT.write_text(text, encoding='utf-8')
    counts = defaultdict(int)
    for r in rows:
        counts[(r['use'], r['question'], r['secure_answer'], r['tier'])] += 1
    for key in sorted(counts):
        print(*key, counts[key], sep='\t')
    print('candidate digest', candidate_digest(rows))
    return 0


if __name__ == '__main__':
    sys.exit(main())
