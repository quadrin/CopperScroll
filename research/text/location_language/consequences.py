#!/usr/bin/env python3
"""Consequences of giving a recurring location expression one meaning.

The Linear B lesson: one assignment must explain every occurrence. This tool
reads occurrences.json (built by build_occurrences.py) and shows, for a choice of
meaning, every occurrence it fixes and every project record (atlas titles and
texts, atlas candidates, exploratory registry branches, the Koḥlit rarity
conditions, workbench predicates, the active questions and the project
translation) that the choice supports, strains or contradicts. It also lists the
other choices it forces, audits the project's own records for inconsistent use,
and ranks expressions by downstream weight.

Strict mode (default) gives every listed member of an expression, including the
conditional members, the same meaning. Split mode lets conditional members (for
example a word that one edition reads with other letters) stand apart.

    python3 -I consequences.py list [EXPR]
    python3 -I consequences.py choose melah=esplanade_temple [--split] [--json]
    python3 -I consequences.py choose "melah=salt_common" "melah@III 8=esplanade_temple" --split
    python3 -I consequences.py audit [--json]
    python3 -I consequences.py rank [--json]
    python3 -I consequences.py report --write

Standard library only. Deterministic. Exploratory: no identification follows.
"""
from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / 'occurrences.json'
CUBIT_M = (0.445, 0.525)  # the exploratory registry's primary cubit range, metres
ORDER = {'supports': 0, 'open': 1, 'tension': 2, 'contradicts': 3}
KIND_LABEL = {
    'atlas_title': 'Atlas titles', 'atlas_text': 'Atlas descriptions and landmarks', 'atlas_candidate': 'Atlas candidate places',
    'registry': 'Exploratory registry branches', 'rarity': 'Koḥlit rarity count (registered conditions)',
    'workbench': 'Feature workbench relationships', 'active_test': 'Active questions (ACTIVE_TEST.md)',
    'translation': 'Project translation', 'analysis': 'Project analyses', 'feature_constraint': 'Feature constraints table',
    'phase5': 'Phase 5 assessments',
}


def load(path=DATA):
    return json.loads(Path(path).read_text(encoding='utf-8'))


class Model:
    def __init__(self, data):
        self.data = data
        self.expr = {e['id']: e for e in data['expressions']}
        self.occ = {o['id']: o for e in data['expressions'] for o in e['occurrences']}
        self.records = {r['id']: r for r in data['records']}
        self.rules = data['rules']
        self.weights = data['weights']
        self.meanings = {e['id']: [m['id'] for m in e['meanings']] for e in data['expressions']}
        self.line_order = {o['line']: line_key(o['line']) for o in self.occ.values()}
        self.positions = data['atlas_positions']
        self._tiers = None

    # ------------------------------------------------------------------ basics
    def var(self, occ_id, split=False):
        o = self.occ[occ_id]
        return occ_id if split and o['membership'] == 'conditional' else o['expression']

    def assignable(self, expr):
        return [o for o in self.expr[expr]['occurrences'] if o['membership'] in ('certain', 'conditional')]

    def find_occ(self, expr, line):
        hits = [o['id'] for o in self.assignable(expr) if o['line'] == line or o['id'] == f'{expr}@{line}']
        if not hits:
            raise ValueError(f'{expr} has no assignable occurrence at {line}')
        return hits

    def parse_choice(self, items):
        choice, overrides = {}, {}
        for item in items:
            if '=' not in item:
                raise ValueError(f'expected EXPR=MEANING or EXPR@LINE=MEANING, got {item!r}')
            key, meaning = item.split('=', 1)
            expr, _, line = key.partition('@')
            expr, meaning = expr.strip(), meaning.strip()
            if expr not in self.expr:
                raise ValueError(f'unknown expression {expr!r}; try: list')
            if meaning not in self.meanings[expr]:
                raise ValueError(f'unknown meaning {meaning!r} for {expr}; choose from {self.meanings[expr]}')
            if line:
                for oid in self.find_occ(expr, line.replace('_', ' ').strip()):
                    overrides[oid] = meaning
            else:
                choice[expr] = meaning
        return choice, overrides

    def assign(self, choice, overrides=None, split=False):
        overrides = overrides or {}
        assignment, violations, assumptions = {}, [], []
        for expr, meaning in sorted(choice.items()):
            for o in self.assignable(expr):
                if o['membership'] == 'certain' or not split:
                    assignment[o['id']] = meaning
                    if o['membership'] == 'conditional':
                        assumptions.append({'occurrence': o['id'], 'assumes_same_word_despite': o['condition']})
        for oid, meaning in sorted(overrides.items()):
            o = self.occ[oid]
            base = choice.get(o['expression'])
            if base and base != meaning:
                if o['membership'] == 'certain':
                    violations.append({'occurrence': oid, 'meaning': meaning, 'expression_meaning': base,
                                       'why': 'A certain member must share the expression’s meaning (one assignment for every occurrence).'})
                elif not split:
                    violations.append({'occurrence': oid, 'meaning': meaning, 'expression_meaning': base,
                                       'why': 'Strict mode: a conditional member shares the meaning unless you use --split, which accepts: ' + o['condition']})
            assignment[oid] = meaning
        return assignment, violations, assumptions

    # ------------------------------------------------------------------ records
    def evaluate(self, rec, assignment):
        parts = []
        for req in rec['requires']:
            for oid in req['at']:
                meaning = assignment.get(oid)
                if meaning is None:
                    continue
                if meaning in req['allowed']:
                    status, why = 'supports', ''
                elif meaning in req['tension']:
                    status, why = 'tension', req['tension'][meaning]
                else:
                    status, why = 'contradicts', f"needs {' or '.join(req['allowed'])}"
                parts.append({'expr': req['expr'], 'occurrence': oid, 'meaning': meaning, 'status': status, 'why': why})
        if not parts:
            return None
        worst = max(parts, key=lambda p: ORDER[p['status']])['status']
        touched = {(r['expr'], oid) for r in rec['requires'] for oid in r['at']}
        partial = len({(p['expr'], p['occurrence']) for p in parts}) < len(touched)
        return {'status': worst, 'partial': partial, 'parts': parts}

    def tier(self, rec_id):
        if self._tiers is None:
            self._tiers = self._compute_tiers()
        return self._tiers[rec_id]

    def _compute_tiers(self):
        tiers, reg_options = {}, {}
        for r in self.records.values():
            if r['kind'] == 'registry' and r['option']:
                reg_options.setdefault((r['entry'], r['place']), set()).add(r['option'])
        for r in self.records.values():
            at_position = r['entry'] is not None and self.positions.get(r['entry']) == r['place']
            if r['kind'] == 'atlas_candidate':
                tiers[r['id']] = 'position' if at_position else 'alternative'
            elif r['kind'] == 'registry' and r['option']:
                tiers[r['id']] = 'position' if at_position and len(reg_options[(r['entry'], r['place'])]) == 1 else 'alternative'
            elif r['group'] == 'rarity:branch':
                tiers[r['id']] = 'position' if r['option'] == 'A' else 'alternative'
            elif r['group']:
                tiers[r['id']] = 'alternative'
            else:
                tiers[r['id']] = 'statement'
        return tiers

    # ------------------------------------------------------------------ choose
    def choose(self, choice, overrides=None, split=False):
        assignment, violations, assumptions = self.assign(choice, overrides, split)
        occurrences = []
        for expr in sorted(set(choice) | {self.occ[o]['expression'] for o in (overrides or {})}):
            for o in self.expr[expr]['occurrences']:
                row = {'id': o['id'], 'entry': o['entry'], 'line': o['line'], 'hebrew_shown': o['hebrew_shown'],
                       'membership': o['membership'], 'link': o['link'], 'meaning': assignment.get(o['id']),
                       'project_translation': o['translation_project'],
                       'puech2015': o['editions'].get('puech2015', {}).get('rendering'),
                       'lefkovits2000': o['editions'].get('lefkovits2000', {}).get('rendering')}
                if o['membership'] in ('conditional', 'control', 'proposed'):
                    row['condition'] = o['condition']
                if o['number'] is not None and assignment.get(o['id']) in ('depth', 'vertical', 'horizontal', 'distance', 'cubit'):
                    row['metres'] = [round(o['number'] * CUBIT_M[0] + 1e-9, 2), round(o['number'] * CUBIT_M[1] + 1e-9, 2)]
                occurrences.append(row)
        results = []
        for rec in self.records.values():
            ev = self.evaluate(rec, assignment)
            if ev:
                results.append({'id': rec['id'], 'kind': rec['kind'], 'entry': rec['entry'], 'place': rec['place'],
                                'candidate_status': rec['status'], 'tier': self.tier(rec['id']), 'quote': rec['quote'],
                                'source': rec['source'], 'note': rec['note'], **ev})
        results.sort(key=lambda r: (list(KIND_LABEL).index(r['kind']), -ORDER[r['status']], entry_key(r['entry']), r['id']))
        forced = self.forced(choice, assignment)
        counts = {}
        for r in results:
            counts.setdefault(r['kind'], {}).setdefault(r['status'], 0)
            counts[r['kind']][r['status']] += 1
        return {'choice': choice, 'overrides': overrides or {}, 'mode': 'split' if split else 'strict',
                'occurrences': occurrences, 'linear_b_violations': violations, 'membership_assumptions': assumptions,
                'records': results, 'counts': counts, 'forced': forced}

    def forced(self, choice, assignment):
        out = []
        for rule in self.rules:
            if all(choice.get(e) in ms for e, ms in rule['when'].items()):
                item = {'rule': rule['id'], 'kind': rule['kind'], 'why': rule['why'], 'source': rule['source'],
                        'then': rule['then'], 'tension': rule['tension'], 'conflicts': []}
                for e, allowed in rule['then'].items():
                    if e in choice and choice[e] not in allowed:
                        level = 'tension' if choice[e] in rule['tension'] else 'contradicts'
                        item['conflicts'].append({'expr': e, 'chosen': choice[e], 'status': level})
                if item['then']:
                    # What the forced choice itself would do to the records.
                    for e, allowed in item['then'].items():
                        if e not in choice and len(allowed) == 1:
                            sub = self.choose({e: allowed[0]}) if e not in choice else None
                            item.setdefault('forced_effects', {})[f'{e}={allowed[0]}'] = {
                                'contradicts': [r['id'] for r in sub['records'] if r['status'] == 'contradicts'],
                                'tension': [r['id'] for r in sub['records'] if r['status'] == 'tension']}
                out.append(item)
        return out

    # ------------------------------------------------------------------ audit
    def constraints(self, split=False):
        """{var: [(record id, allowed, tension, occurrence ids)]}"""
        out = {}
        for rec in self.records.values():
            for req in rec['requires']:
                by_var = {}
                for oid in req['at']:
                    by_var.setdefault(self.var(oid, split), []).append(oid)
                for v, oids in by_var.items():
                    out.setdefault(v, []).append((rec['id'], frozenset(req['allowed']), frozenset(req['tension']), tuple(sorted(oids))))
        return out

    def relation(self, a, b):
        ra, rb = self.records[a], self.records[b]
        if ra['group'] and ra['group'] == rb['group']:
            return 'internal' if ra['option'] == rb['option'] else 'alternatives_same_group'
        for x, y in ((ra, rb), (rb, ra)):
            if x['kind'] == 'registry' and y['kind'] == 'atlas_candidate' and x['entry'] == y['entry'] and x['place'] == y['place']:
                return 'internal'
        if ra['kind'] == 'registry' and rb['kind'] == 'registry' and ra['entry'] == rb['entry'] and ra['place'] != rb['place'] \
                and ra['option'] and rb['option']:
            return 'alternatives_same_group'
        if ra['kind'] == 'atlas_candidate' and rb['kind'] == 'registry' and ra['entry'] == rb['entry'] and ra['place'] != rb['place']:
            return 'alternatives_same_group'
        if rb['kind'] == 'atlas_candidate' and ra['kind'] == 'registry' and ra['entry'] == rb['entry'] and ra['place'] != rb['place']:
            return 'alternatives_same_group'
        ta, tb = self.tier(a), self.tier(b)
        if ta != 'alternative' and tb != 'alternative':
            return 'project'
        if ta == 'alternative' and tb == 'alternative':
            return 'alternatives'
        return 'alternative_vs_project'

    def conflicts(self):
        strict = self.constraints(False)
        split_vars = {}
        for v, items in self.constraints(True).items():
            for rid, _, _, oids in items:
                for oid in oids:
                    split_vars[(rid, oid)] = v
        found = []
        for v, items in sorted(strict.items()):
            for (a, aa, at, ao), (b, ba, bt, bo) in combinations(sorted(items, key=lambda x: (x[0], x[3])), 2):
                if a == b:
                    continue
                if aa & ba:
                    continue
                level = 'tension' if (aa | at) & (ba | bt) else 'hard'
                rel = self.relation(a, b)
                if rel == 'alternatives_same_group':
                    continue
                va = {split_vars[(a, o)] for o in ao}
                vb = {split_vars[(b, o)] for o in bo}
                strict_only = not (va & vb)
                conds = sorted({self.occ[o]['condition'] for o in ao + bo if self.occ[o]['membership'] == 'conditional'})
                lines_a = sorted({self.occ[o]['line'] for o in ao}, key=self.line_order.get)
                lines_b = sorted({self.occ[o]['line'] for o in bo}, key=self.line_order.get)
                same_line = bool(set(lines_a) & set(lines_b))
                found.append({'expr': v, 'a': a, 'b': b, 'a_allowed': sorted(aa), 'b_allowed': sorted(ba),
                              'a_lines': lines_a, 'b_lines': lines_b, 'same_line': same_line,
                              'level': level, 'relation': rel, 'strict_only': strict_only,
                              'consistent_if': conds if strict_only else [],
                              'soft': not same_line and not self.expr[v].get('uniform', True)})
        return found

    def uneven(self):
        out = []
        strict = self.constraints(False)
        for v, items in sorted(strict.items()):
            opens = [(rid, al, oids) for rid, al, _, oids in items if self.records[rid]['open'] and len(al) > 1]
            fixed = [(rid, al, oids) for rid, al, _, oids in items
                     if not self.records[rid]['open'] and len(al) == 1 and self.tier(rid) != 'alternative']
            for rid, al, oids in opens:
                meanings = sorted({next(iter(f[1])) for f in fixed if not set(f[2]) & set(oids)})
                if len(meanings) == 1 and meanings[0] in al:
                    others = sorted({f[0] for f in fixed if next(iter(f[1])) == meanings[0]})
                    lines = sorted({self.occ[o]['line'] for f in fixed for o in f[2]}, key=self.line_order.get)
                    out.append({'expr': v, 'open_record': rid, 'open_lines': sorted({self.occ[o]['line'] for o in oids}, key=self.line_order.get),
                                'left_open': sorted(al), 'fixed_elsewhere_as': meanings[0], 'fixed_by': others, 'fixed_lines': lines})
        return out

    def rule_conflicts(self):
        out = []
        strict = self.constraints(False)
        for rule in self.rules:
            if not rule['then']:
                continue
            for e, when in rule['when'].items():
                for rid, al, _, _ in strict.get(e, []):
                    if not al <= set(when):
                        continue
                    for te, tallowed in rule['then'].items():
                        for rid2, al2, t2, _ in strict.get(te, []):
                            if al2 & set(tallowed):
                                continue
                            level = 'tension' if al2 & set(rule['tension']) else 'hard'
                            out.append({'rule': rule['id'], 'kind': rule['kind'], 'trigger': rid, 'trigger_tier': self.tier(rid),
                                        'forces': {te: tallowed}, 'against': rid2, 'against_tier': self.tier(rid2),
                                        'against_allowed': sorted(al2), 'level': level, 'why': rule['why']})
        out.sort(key=lambda r: (r['rule'], r['trigger'], r['against']))
        return out

    def candidates(self):
        conflicts = self.conflicts()
        rules = self.rule_conflicts()

        def hits_for(bundle):
            hits = []
            for c in conflicts:
                if c['soft']:
                    continue
                for mine, other in ((c['a'], c['b']), (c['b'], c['a'])):
                    if mine not in bundle:
                        continue
                    if other in bundle and c['relation'] != 'internal':
                        break
                    if other not in bundle and self.tier(other) == 'alternative':
                        break
                    hits.append({'expr': c['expr'], 'mine': mine, 'other': other, 'level': c['level'],
                                 'strict_only': c['strict_only'], 'consistent_if': c['consistent_if'],
                                 'other_entry': self.records[other]['entry']})
                    break
            for r in rules:
                if r['trigger'] in bundle and self.tier(r['against']) != 'alternative':
                    hits.append({'expr': list(r['forces'])[0], 'mine': r['trigger'], 'other': r['against'], 'level': r['level'],
                                 'strict_only': False, 'consistent_if': [], 'other_entry': self.records[r['against']]['entry'],
                                 'rule': r['rule']})
            return sorted(hits, key=lambda h: (h['expr'], h['mine'], h['other']))

        def score(hits):
            return (sum(h['level'] == 'hard' and not h['strict_only'] for h in hits),
                    sum(h['level'] == 'hard' for h in hits), len(hits))

        out = []
        for rec in sorted(self.records.values(), key=lambda r: (entry_key(r['entry']), r['id'])):
            if rec['kind'] != 'atlas_candidate':
                continue
            options = {}
            for r in self.records.values():
                if r['kind'] == 'registry' and r['entry'] == rec['entry'] and r['place'] == rec['place'] and r['option']:
                    options.setdefault(r['option'], set()).add(r['id'])
            trials = [(None, {rec['id']})] if not options else [(o, {rec['id']} | ids) for o, ids in sorted(options.items())]
            evaluated = [(o, b, hits_for(b)) for o, b in trials]
            best_option, bundle, hits = min(evaluated, key=lambda t: (score(t[2]), t[0] or ''))
            needs = {}
            for rid in sorted(bundle):
                for req in self.records[rid]['requires']:
                    cur = needs.get(req['expr'])
                    needs[req['expr']] = set(req['allowed']) if cur is None else cur & set(req['allowed'])
            hard = sorted({h['expr'] for h in hits if h['level'] == 'hard' and not h['strict_only']})
            cond = sorted({h['expr'] for h in hits if h['level'] == 'hard' and h['strict_only']})
            if hard:
                verdict = 'needs choices contradicted elsewhere'
            elif cond:
                verdict = 'consistent only if a conditional member stands apart'
            elif hits:
                verdict = 'tension only'
            else:
                verdict = 'consistent with the project’s other records'
            out.append({'candidate': rec['id'], 'entry': rec['entry'], 'place': rec['place'], 'status': rec['status'],
                        'tier': self.tier(rec['id']), 'registry_branch': best_option,
                        'branches_tried': [o for o, _, _ in evaluated if o], 'bundle': sorted(bundle),
                        'needs': {k: sorted(v) for k, v in sorted(needs.items())}, 'verdict': verdict,
                        'several': len(hard) >= 2, 'conflicting_expressions': hard, 'conditional_expressions': cond,
                        'conflicts': hits})
        return out

    def verdicts(self):
        conflicts, uneven = self.conflicts(), self.uneven()
        out = {}
        for e in self.expr:
            soft = [c for c in conflicts if c['expr'] == e and c['soft'] and c['relation'] in ('project', 'internal')]
            mine = [c for c in conflicts if c['expr'] == e and not c['soft']]
            proj = [c for c in mine if c['relation'] == 'project']
            internal = [c for c in mine if c['relation'] == 'internal']
            hard_proj = [c for c in proj if c['level'] == 'hard']
            hard_int = [c for c in internal if c['level'] == 'hard']
            if any(not c['strict_only'] for c in hard_proj):
                v = 'inconsistent'
            elif hard_proj:
                v = 'consistent only if a conditional member stands apart'
            elif any(not c['strict_only'] for c in hard_int):
                v = 'a candidate branch contradicts itself'
            elif hard_int:
                v = 'consistent only if a conditional member stands apart'
            elif proj or internal:
                v = 'tension'
            elif soft:
                v = 'differs from line to line (allowed for this rule, but not argued in the records)'
            elif any(u['expr'] == e for u in uneven):
                v = 'uneven: fixed in some lines, left open in others'
            elif mine:
                v = 'positions consistent; some alternatives conflict'
            elif any(req['expr'] == e for r in self.records.values() for req in r['requires']):
                v = 'consistent'
            else:
                v = 'no project record depends on it'
            out[e] = v
        return out

    def rank(self):
        rows = []
        for e, meanings in self.meanings.items():
            if len(meanings) < 2:
                continue
            sensitive, entries = [], set()
            for rec in self.records.values():
                if not any(req['expr'] == e for req in rec['requires']):
                    continue
                statuses = []
                for m in meanings:
                    ev = self.evaluate({'requires': [r for r in rec['requires'] if r['expr'] == e]}, self.assign({e: m})[0])
                    statuses.append(ev['status'] if ev else 'open')
                if len(set(statuses)) > 1:
                    key = f"{rec['kind']}:{rec['status']}" if rec['kind'] == 'atlas_candidate' else rec['kind']
                    sensitive.append((rec['id'], self.weights.get(key, 1)))
                    if rec['entry']:
                        entries.add(rec['entry'])
            occs = self.assignable(e)
            entries |= {o['entry'] for o in occs}
            rows.append({'expr': e, 'label': self.expr[e]['label'], 'score': sum(w for _, w in sensitive),
                         'sensitive_records': len(sensitive), 'entries': len(entries), 'occurrences': len(occs),
                         'meanings': len(meanings)})
        rows.sort(key=lambda r: (-r['score'], -r['sensitive_records'], r['expr']))
        for i, r in enumerate(rows, 1):
            r['rank'] = i
        return rows

    def usage(self):
        """Per expression: which meanings the project's statements and current positions need, and where."""
        out = {}
        for v, items in sorted(self.constraints(False).items()):
            groups = {}
            for rid, allowed, tension, oids in items:
                if self.tier(rid) == 'alternative':
                    continue
                key = tuple(sorted(allowed))
                g = groups.setdefault(key, {'allowed': list(key), 'records': [], 'lines': set(), 'entries': set()})
                g['records'].append(rid)
                g['lines'].update(self.occ[o]['line'] for o in oids)
                if self.records[rid]['entry']:
                    g['entries'].add(self.records[rid]['entry'])
            if not groups:
                continue
            feasible = set(self.meanings[v])
            for key in groups:
                feasible &= set(key)
            rows = []
            for key, g in sorted(groups.items()):
                rows.append({'allowed': g['allowed'], 'records': sorted(g['records']),
                             'lines': sorted(g['lines'], key=line_key), 'entries': sorted(g['entries'], key=entry_key)})
            out[v] = {'needs': rows, 'one_meaning_fits_all': sorted(feasible)}
        return out

    def audit(self):
        return {'verdicts': self.verdicts(), 'usage': self.usage(), 'conflicts': self.conflicts(), 'uneven': self.uneven(),
                'rule_conflicts': self.rule_conflicts(), 'candidates': self.candidates(), 'rank': self.rank()}


ROMAN = {r: i for i, r in enumerate(['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'])}


def line_key(line):
    col, num = line.split()
    return (ROMAN[col], int(num))


def entry_key(entry):
    if not entry:
        return (999, '')
    digits = ''.join(ch for ch in entry if ch.isdigit())
    return (int(digits), entry)


def group_rules(items):
    groups = {}
    for r in items:
        key = (r['rule'], r['kind'], r['level'], json.dumps(r['forces'], ensure_ascii=False))
        g = groups.setdefault(key, {'rule': r['rule'], 'kind': r['kind'], 'level': r['level'], 'forces': r['forces'],
                                    'why': r['why'], 'triggers': set(), 'against': set()})
        g['triggers'].add(f"{r['trigger']} [{r['trigger_tier']}]")
        g['against'].add(f"{r['against']} [{r['against_tier']}]")
    out = []
    for key in sorted(groups):
        g = groups[key]
        g['triggers'] = sorted(g['triggers'])
        g['against'] = sorted(g['against'])
        out.append(g)
    return out


# ---------------------------------------------------------------------- text output
def describe(model, rid):
    r = model.records[rid]
    where = f"entry {r['entry']}" if r['entry'] else 'scroll-wide'
    place = (f", {r['place']} ({r['status']})" if r['status'] else f", branch for {r['place']}") if r['place'] else ''
    return f"{rid} [{where}{place}]: “{r['quote']}”"


def text_choose(model, res):
    out = [f"Choice: {', '.join(f'{k}={v}' for k, v in res['choice'].items()) or '(none)'}"
           + (f"; overrides: {', '.join(f'{k}={v}' for k, v in res['overrides'].items())}" if res['overrides'] else '')
           + f" — {res['mode']} mode", '']
    out.append('Occurrences fixed:')
    for o in res['occurrences']:
        m = o['meaning'] or ('not assigned: ' + o.get('condition', '') if o['membership'] != 'certain' else 'not assigned')
        metres = f" ≈ {o['metres'][0]}–{o['metres'][1]} m" if o.get('metres') else ''
        out.append(f"  {o['line']:<8} entry {o['entry']:<4} {o['hebrew_shown'] or '—':<16} {m}{metres}"
                   f" | project: {o['project_translation'] or '—'} | Puech 2015: {o['puech2015'] or '—'} | Lefkovits: {o['lefkovits2000'] or '—'}")
    if res['membership_assumptions']:
        out += ['', 'Strict mode treats these conditional members as the same word:']
        out += [f"  {a['occurrence']}: {a['assumes_same_word_despite']}" for a in res['membership_assumptions']]
    if res['linear_b_violations']:
        out += ['', 'One-meaning rule violations:']
        out += [f"  {v['occurrence']} = {v['meaning']} (expression = {v['expression_meaning']}): {v['why']}" for v in res['linear_b_violations']]
    for kind, label in KIND_LABEL.items():
        rows = [r for r in res['records'] if r['kind'] == kind]
        if not rows:
            continue
        out += ['', f'{label}:']
        for r in rows:
            bad = [p for p in r['parts'] if p['status'] != 'supports']
            bad.sort(key=lambda p: line_key(model.occ[p['occurrence']]['line']))
            detail = '; '.join(dict.fromkeys(f"{model.occ[p['occurrence']]['line']} {p['status']}" + (f" ({p['why']})" if p['why'] else '')
                                             for p in bad))
            extra = ' (other conditions open)' if r['partial'] and r['status'] == 'supports' else ''
            out.append(f"  {r['status'].upper():<11} {describe(model, r['id'])}{extra}" + (f" — {detail}" if detail else ''))
    if res['forced']:
        out += ['', 'Forced or argued consequences:']
        for f in res['forced']:
            then = ', '.join(f"{e} ∈ {{{', '.join(v)}}}" for e, v in f['then'].items()) or '(no further choice)'
            out.append(f"  [{f['kind']}] {f['rule']}: {f['why']} → {then}. Source: {f['source']}")
            for c in f['conflicts']:
                out.append(f"    conflicts with your choice {c['expr']}={c['chosen']} ({c['status']})")
            for k, eff in sorted(f.get('forced_effects', {}).items()):
                out.append(f"    {k} would contradict {len(eff['contradicts'])} record(s): {', '.join(eff['contradicts']) or 'none'}")
    return '\n'.join(out)


def text_audit(model, audit):
    out = ['Verdicts (strict mode):']
    rank = {r['expr']: r for r in audit['rank']}
    for e, v in sorted(audit['verdicts'].items(), key=lambda kv: (rank.get(kv[0], {}).get('rank', 999), kv[0])):
        r = rank.get(e)
        out.append(f"  {e:<16} {v}" + (f"  [weight {r['score']}, rank {r['rank']}]" if r else ''))
    out += ['', 'Conflicts among the project’s own records (statements and current positions):']
    for c in audit['conflicts']:
        if c['relation'] not in ('project', 'internal'):
            continue
        cond = f" — consistent only if: {' / '.join(c['consistent_if'])}" if c['strict_only'] else ''
        where = 'same line' if c['same_line'] else 'different lines'
        out.append(f"  {c['expr']} ({c['level']}, {where}, {c['relation']}): {describe(model, c['a'])} needs {c['a_allowed']} at {c['a_lines']}"
                   f"  ×  {describe(model, c['b'])} needs {c['b_allowed']} at {c['b_lines']}{cond}")
    out += ['', 'Lines the project leaves open although other lines fix the same expression:']
    for u in audit['uneven']:
        out.append(f"  {u['expr']}: {u['open_record']} leaves {u['left_open']} at {u['open_lines']}; "
                   f"{len(u['fixed_by'])} record(s) fix “{u['fixed_elsewhere_as']}” at {u['fixed_lines']}")
    out += ['', 'Rule-based conflicts (a record commits to a rule’s condition; the rule then conflicts with other records):']
    for g in group_rules(audit['rule_conflicts']):
        out.append(f"  {g['rule']} ({g['kind']}, {g['level']}): {len(g['triggers'])} trigger(s) {', '.join(g['triggers'])} "
                   f"force {g['forces']} against {', '.join(g['against'])}")
    out += ['', 'Candidate places that need choices the project contradicts elsewhere:']
    for c in audit['candidates']:
        if c['verdict'] == 'consistent with the project’s other records':
            continue
        flag = ' SEVERAL' if c['several'] else ''
        branch = f"; best registry branch {c['registry_branch']} of {c['branches_tried']}" if c['registry_branch'] else ''
        out.append(f"  {c['candidate']} ({c['status']}, {c['tier']}): {c['verdict']}{flag}{branch}")
        for h in c['conflicts']:
            cond = f" (consistent only if: {' / '.join(h['consistent_if'])})" if h['strict_only'] else ''
            out.append(f"     {h['expr']} {h['level']}: {h['mine']} vs {h['other']} (entry {h['other_entry']}){cond}")
    return '\n'.join(out)


def text_rank(rows):
    out = ['rank  weight  records  entries  occurrences  expression']
    for r in rows:
        out.append(f"{r['rank']:>4}  {r['score']:>6}  {r['sensitive_records']:>7}  {r['entries']:>7}  {r['occurrences']:>11}  {r['expr']} — {r['label']}")
    return '\n'.join(out)


def text_list(model, expr=None):
    out = []
    for e in model.data['expressions']:
        if expr and e['id'] != expr:
            continue
        counts = {}
        for o in e['occurrences']:
            counts[o['membership']] = counts.get(o['membership'], 0) + 1
        out.append(f"{e['id']}: {e['label']} — {', '.join(f'{k} {v}' for k, v in sorted(counts.items()))}")
        for m in e['meanings']:
            who = '; '.join(f"{p['who']} ({p['where']})" for p in m['proposed_by'])
            out.append(f"    {m['id']}: {m['gloss']} — {who}")
        if expr:
            for o in e['occurrences']:
                p15 = o['editions'].get('puech2015', {})
                lef = o['editions'].get('lefkovits2000', {})
                out.append(f"      {o['id']:<22} entry {o['entry']:<4} {o['hebrew_shown'] or '—':<16} {o['link']}/{o['membership']}"
                           f" | Puech 2015 {p15.get('rendering', '—')} ({p15.get('ref', '')}) | Lefkovits {lef.get('rendering', '—')} ({lef.get('ref', '')})")
    return '\n'.join(out)


# ---------------------------------------------------------------------- report
def md_escape(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def report_markdown(model, audit):
    d = model.data
    s = d['summary']
    rank = {r['expr']: r for r in audit['rank']}
    out = ['# Location-language audit (generated)', '',
           f"Generated by `consequences.py report --write` from `occurrences.json` (base commit {d['base_commit']}). "
           'Do not edit by hand. Strict mode: every listed member of an expression shares one meaning.', '',
           f"{s['expressions']} expressions, {s['occurrences']} listed occurrences "
           f"({s['by_link']['explicit']} explicit, {s['by_link']['restored']} restored, {s['by_link']['proposed']} proposed), "
           f"{s['records']} project records, {s['rules']} rules.", '',
           '## Verdicts and downstream weight', '',
           '| Rank | Expression | Verdict | Weight | Records that change | Entries |', '|---|---|---|---|---|---|']
    for e, v in sorted(audit['verdicts'].items(), key=lambda kv: (rank.get(kv[0], {}).get('rank', 999), kv[0])):
        r = rank.get(e, {})
        out.append(f"| {r.get('rank', '—')} | `{e}` {md_escape(model.expr[e]['label'])} | {v} | {r.get('score', '—')} | "
                   f"{r.get('sensitive_records', '—')} | {r.get('entries', '—')} |")
    out += ['', '## How the project’s current records use each expression', '',
            'Statements (atlas titles and texts, translation, registered conditions, analyses) and current positions '
            '(preferred or sole atlas candidates and their single registry branch). Alternatives are left out here.', '',
            '| Expression | Meanings needed → lines (records) | One meaning that fits all |', '|---|---|---|']
    for e, u in audit['usage'].items():
        if len(model.meanings[e]) < 2:
            continue
        needs = '<br>'.join(md_escape(f"{' or '.join(n['allowed'])} → {', '.join(n['lines'])} ({len(n['records'])})") for n in u['needs'])
        fits = ', '.join(u['one_meaning_fits_all']) or '**none**'
        out.append(f"| `{e}` | {needs} | {fits} |")
    out += ['', '## Conflicts among the project’s own records', '',
            'Each row pairs two current project records that need different meanings for one expression. '
            '“Different lines” means the one-meaning rule is what makes them conflict.', '',
            '| Expression | Level | Lines | Record A | Needs | Record B | Needs | Consistent only if |', '|---|---|---|---|---|---|---|---|']
    for c in audit['conflicts']:
        if c['relation'] not in ('project', 'internal'):
            continue
        soft = ' (soft: rule may differ by line)' if c['soft'] else ''
        out.append(f"| `{c['expr']}` | {c['level']}{' (internal)' if c['relation'] == 'internal' else ''}{soft} | "
                   f"{'same line' if c['same_line'] else 'different lines'} | {md_escape(describe(model, c['a']))} | {', '.join(c['a_allowed'])} "
                   f"({', '.join(c['a_lines'])}) | {md_escape(describe(model, c['b']))} | {', '.join(c['b_allowed'])} ({', '.join(c['b_lines'])}) | "
                   f"{md_escape(' / '.join(c['consistent_if'])) if c['strict_only'] else '—'} |")
    out += ['', '## Lines left open although the same expression is fixed elsewhere', '',
            '| Expression | Open record | Open lines | Fixed elsewhere as | Fixed by |', '|---|---|---|---|---|']
    for u in audit['uneven']:
        out.append(f"| `{u['expr']}` | {u['open_record']} | {', '.join(u['open_lines'])} | {u['fixed_elsewhere_as']} | "
                   f"{len(u['fixed_by'])} records at {', '.join(u['fixed_lines'])} |")
    out += ['', '## Rule-based conflicts', '', '| Rule | Kind | Level | Why | Triggered by | Forces | Against |', '|---|---|---|---|---|---|---|']
    for g in group_rules(audit['rule_conflicts']):
        out.append(f"| {g['rule']} | {g['kind']} | {g['level']} | {md_escape(g['why'])} | {md_escape(', '.join(g['triggers']))} | "
                   f"{md_escape(json.dumps(g['forces'], ensure_ascii=False))} | {md_escape(', '.join(g['against']))} |")
    out += ['', '## Candidate places', '',
            'A candidate “needs choices contradicted elsewhere” when it, or its registry branch, needs a meaning that another entry’s current record rules out.', '',
            '| Candidate | Status | Verdict | Expressions in conflict | Conflicting records |', '|---|---|---|---|---|']
    for c in audit['candidates']:
        if c['verdict'] == 'consistent with the project’s other records':
            continue
        others = sorted({h['other'] for h in c['conflicts']})
        out.append(f"| {c['candidate']} | {c['status']} ({c['tier']}) | {c['verdict']}{' (several)' if c['several'] else ''} | "
                   f"{', '.join(sorted({h['expr'] for h in c['conflicts']}))} | {md_escape(', '.join(others))} |")
    out += ['', '## Occurrences', '',
            'Hebrew as shown in `data/scroll-text.js`: [ ] restored, { } cancelled, < > supplied by the modern editor, ° damaged letter. '
            'Renderings are short phrases; pages are printed pages.', '']
    for e in d['expressions']:
        out += [f"### `{e['id']}`: {md_escape(e['label'])}", '']
        for m in e['meanings']:
            who = '; '.join(f"{p['who']} ({p['where']})" for p in m['proposed_by'])
            out.append(f"- **{m['id']}**: {md_escape(m['gloss'])}. Proposed by: {md_escape(who)}.")
        if e['note']:
            out.append(f"- Note: {md_escape(e['note'])}")
        out += ['', '| Line | Entry | Hebrew shown | Link | Membership | Project | Puech 2015 | Puech 2006 | Lefkovits 2000 |', '|---|---|---|---|---|---|---|---|---|']
        for o in e['occurrences']:
            def ed(k):
                v = o['editions'].get(k)
                if not v:
                    return '—'
                return md_escape(f"{v['rendering']} ({v['ref']})" + (f" [{v['reading']}]" if v.get('reading') else ''))
            link = o['link'] + (f": {o['proposer']}" if o['proposer'] else '')
            mem = o['membership'] + (f": {o['condition']}" if o['membership'] != 'certain' else '')
            out.append(f"| {o['line']} | {o['entry']} | {md_escape(o['hebrew_shown'] or '—')} | {md_escape(link)} | {md_escape(mem)} | "
                       f"{md_escape(o['translation_project'] or o['link_note'] or '—')} | {ed('puech2015')} | {ed('puech2006')} | {ed('lefkovits2000')} |")
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Consequences of one meaning per recurring location expression.')
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('list')
    p.add_argument('expr', nargs='?')
    p = sub.add_parser('choose')
    p.add_argument('items', nargs='+', help='EXPR=MEANING or "EXPR@LINE=MEANING"')
    p.add_argument('--split', action='store_true', help='let conditional members stand apart')
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('audit')
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('rank')
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('report')
    p.add_argument('--write', action='store_true', help='write report.md and audit.json next to this script')
    p.add_argument('--data', default=str(DATA), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    model = Model(load(getattr(args, 'data', DATA)))
    if args.cmd == 'list':
        print(text_list(model, args.expr))
    elif args.cmd == 'choose':
        try:
            choice, overrides = model.parse_choice(args.items)
        except ValueError as exc:
            print(f'error: {exc}', file=sys.stderr)
            return 2
        res = model.choose(choice, overrides, args.split)
        print(json.dumps(res, ensure_ascii=False, indent=1) if args.json else text_choose(model, res))
    elif args.cmd == 'audit':
        audit = model.audit()
        print(json.dumps(audit, ensure_ascii=False, indent=1) if args.json else text_audit(model, audit))
    elif args.cmd == 'rank':
        rows = model.rank()
        print(json.dumps(rows, ensure_ascii=False, indent=1) if args.json else text_rank(rows))
    elif args.cmd == 'report':
        audit = model.audit()
        md = report_markdown(model, audit)
        if args.write:
            (HERE / 'report.md').write_text(md, encoding='utf-8')
            (HERE / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            print('wrote report.md and audit.json')
        else:
            print(md)
    return 0


if __name__ == '__main__':
    sys.exit(main())
