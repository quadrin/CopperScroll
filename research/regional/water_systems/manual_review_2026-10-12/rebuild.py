#!/usr/bin/env python3
"""Rebuild an exploratory manual-check overlay without modifying prior lane outputs."""
import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
sys.path.insert(0, str(LANE / 'scripts'))
import common as C
import iaa_view as IV
import phase4_view as PV
import score as S

LEDGERS = ['posthoc_checks.csv', 'iaa_posthoc_checks.csv', 'phase4_posthoc_checks.csv']
FROZEN_MARKER = 'ASI-109/7/48-aqueduct'


def read(path):
    with Path(path).open(encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write(path, rows, fields=None):
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_checks(ledger_names=LEDGERS):
    checks = {}
    for fn in ledger_names:
        for r in read(LANE / fn):
            rid = r.get('id', r.get('row_id'))
            for clause in r['clause'].split(';'):
                key = (rid, clause.strip())
                item = dict(r, id=rid, clause=clause.strip(), ledger=fn)
                if key in checks and checks[key]['verdict'] != item['verdict']:
                    raise ValueError(f'Conflicting ledger verdicts: {key}')
                checks[key] = item
    return checks


def parse_clauses(text):
    return dict(part.split('=', 1) for part in text.split(';') if part)


def repaired_code(check, branch, partial_mode, decision=None):
    if check['verdict'] == 'confirmed':
        return S.M
    if decision:
        return decision['corrected_code']
    if check['verdict'] == 'partly confirmed':
        if check['id'] == FROZEN_MARKER and branch.startswith('S-any|'):
            return S.M
        return S.M if partial_mode == 'retain_partial' else S.U
    if check['verdict'] == 'not confirmed':
        return S.U
    raise ValueError(f"Unknown verdict: {check['verdict']}")


def repair_scores(rows, checks, decisions, partial_mode='verified'):
    out, changes = [], []
    for row in rows:
        r = dict(row)
        codes = parse_clauses(r['clauses'])
        for clause, old in list(codes.items()):
            if old != S.M:
                continue
            alias = 'head' if clause == 'outlet' and r['type'] == 'aqueduct' else clause
            key = (r['id'], alias)
            check = checks.get(key)
            if not check:
                continue
            new = repaired_code(check, r['branch'], partial_mode, decisions.get(key))
            if new != old:
                codes[clause] = new
                changes.append(dict(id=r['id'], entry=r['entry'], branch=r['branch'], clause=clause,
                                    old_code=old, new_code=new, ledger=check['ledger'], verdict=check['verdict'],
                                    reason=check['reason'], decision_reason=decisions.get(key, {}).get('reason', '')))
        dcheck = checks.get((r['id'], 'date'))
        if dcheck and dcheck['verdict'] != 'confirmed' and r['date_code'] != 'undated':
            changes.append(dict(id=r['id'], entry=r['entry'], branch=r['branch'], clause='date',
                                old_code=r['date_code'], new_code='undated', ledger=dcheck['ledger'],
                                verdict=dcheck['verdict'], reason=dcheck['reason'], decision_reason=''))
            r['date_code'] = 'undated'
        r['clauses'] = ';'.join(f'{k}={v}' for k, v in codes.items())
        r['overall'] = S.overall(codes.values())
        out.append(r)
    return out, changes


def aggregate(rows, units):
    per_row = defaultdict(dict)
    dates = {}
    for r in rows:
        per_row[r['id']][(r['entry'], r['branch'])] = parse_clauses(r['clauses'])
        dates[r['id']] = r['date_code']
    detail = []
    for uid, ids in sorted(units.items()):
        keys = set().union(*(per_row[i].keys() for i in ids))
        for entry, branch in sorted(keys):
            members = [per_row[i][(entry, branch)] for i in ids if (entry, branch) in per_row[i]]
            names = sorted({k for m in members for k in m})
            combined = {k: S.combine([m.get(k, S.NS) for m in members]) for k in names}
            dcodes = [dates.get(i, 'undated') for i in ids]
            dc = next((d for d in ('in', 'in_hedged', 'partly', 'undated', 'out') if d in dcodes), 'undated')
            detail.append(dict(unit_id=uid, entry=entry, branch=branch,
                               clauses=';'.join(f'{k}={v}' for k, v in combined.items()),
                               overall=S.overall([S.U if v == 'CONFLICT' else v for v in combined.values()]),
                               date_code=dc, conflicts=';'.join(k for k, v in combined.items() if v == 'CONFLICT')))
    return detail


def count(rows, detail):
    tallies = defaultdict(Counter)
    for records, merged in ((rows, False), (detail, True)):
        for r in records:
            lineage = 'MERGED' if merged else r['lineage'] + ('-unplaced' if r['in_box'] != 'yes' else '')
            for rule, eligible in S.DATE_RULES.items():
                key = (r['entry'], r['branch'], lineage, rule)
                result = S.F if not eligible(r['date_code']) else r['overall']
                tallies[key]['N'] += 1
                tallies[key][result if result in (S.M, S.F) else S.U] += 1
    return [dict(entry=e, branch=b, lineage=l, date_rule=d, N=c['N'],
                 k_match=c[S.M], f_fail=c[S.F], m_unknown=c[S.U])
            for (e, b, l, d), c in sorted(tallies.items())]


def clause_counts(rows, detail):
    tallies = defaultdict(Counter)
    for records, merged in ((rows, False), (detail, True)):
        for r in records:
            lineage = 'MERGED' if merged else r['lineage'] + ('-unplaced' if r['in_box'] != 'yes' else '')
            for rule, eligible in S.DATE_RULES.items():
                if not eligible(r['date_code']):
                    continue
                for clause, code in parse_clauses(r['clauses']).items():
                    tallies[(r['entry'], r['branch'], lineage, rule, clause)][code] += 1
    return [dict(entry=e, branch=b, lineage=l, date_rule=d, clause=k, N=sum(c.values()),
                 k_match=c[S.M], f_fail=c[S.F], m_unknown=c[S.U] + c['CONFLICT'], not_scored=c[S.NS])
            for (e, b, l, d, k), c in sorted(tallies.items())]


def compare(before, after, tag):
    old = {(r['unit_id'], r['entry'], r['branch']): r for r in before}
    out = []
    for r in after:
        o = old[(r['unit_id'], r['entry'], r['branch'])]
        if r['overall'] != o['overall'] or r['date_code'] != o['date_code']:
            out.append(dict(view=tag, unit_id=r['unit_id'], entry=r['entry'], branch=r['branch'],
                            original_overall=o['overall'], corrected_overall=r['overall'],
                            original_date=o['date_code'], corrected_date=r['date_code']))
    return out


def lead_rows(detail, units, water, checks):
    """Complete count-level survivors and dated entry-29 nearest misses; no ranking by exposure."""
    out = []
    for r in detail:
        codes = parse_clauses(r['clauses'])
        dated = r['date_code'] in ('in', 'in_hedged')
        survivor = r['overall'] == S.M and r['date_code'] != 'out'
        nearest29 = r['entry'] == '29' and r['branch'] == 'res|Q-any' and dated \
            and sum(v == S.M for v in codes.values()) >= 3 and S.F not in codes.values()
        if not (survivor or nearest29):
            continue
        members = [water[i] for i in units[r['unit_id']]]
        reviewed = []
        for k, code in codes.items():
            if code == S.M and any(checks.get((m['id'], k), {}).get('verdict') == 'confirmed' for m in members):
                reviewed.append(k)
        unknowns = [k for k, v in codes.items() if v not in (S.M, S.NS)]
        missing, observation = follow_up(r, members, unknowns)
        out.append(dict(r, status='count-level survivor' if survivor else 'dated near miss',
                        names='; '.join(dict.fromkeys(m['name'] for m in members)),
                        types=';'.join(sorted({m['type'] for m in members})),
                        aggregate='yes' if any(m['aggregate'] == 'yes' for m in members) else 'no',
                        member_ids=';'.join(m['id'] for m in members),
                        sources=' || '.join(dict.fromkeys(m['source'] + '; ' + m['locator'] for m in members)),
                        manually_confirmed_clauses=';'.join(reviewed),
                        other_MATCH_clauses=';'.join(k for k, v in codes.items() if v == S.M and k not in reviewed),
                        unknown_clauses=';'.join(unknowns),
                        date_limit='' if dated else 'installation date is not securely within the window',
                        missing_fields=missing, next_discriminating_or_rejecting_observation=observation,
                        evidence_limit='existing coded sources and existing review ledgers; no new PDF inspection'))
    return out


def follow_up(score, members, unknowns):
    entry, branch = score['entry'], score['branch']
    ids = ' '.join(m['id'] for m in members)
    if '#142' in ids and 'ATQ90-' in ids:
        return ('same-phase entrance and feature construction date; exact pool coordinate; Beth ha-Kerem association',
                'A dated L5 construction/access section, with its specific surveyed position. An entrance only after 135 CE rejects the period-compatible entrance; a source-justified 1 km location excludes this 1.94 km candidate under that branch.')
    if '#98' in ids and 'ATQ66-' in ids:
        return ('date of stepped bath phase versus later cistern reuse; exact bath coordinate; admissibility under cistern branch',
                'A section tying the preserved staircase to the dated Cistern 2/bath phase. A later-only staircase rejects the period-compatible access; resolving the source type determines eligibility without using later cistern reuse as ancient bath evidence.')
    if '#57' in ids and 'ATQ54-' in ids:
        return ('late Second Temple bath versus Mamluk cistern phase; phase-specific type; coordinate uncertainty at 2 km edge',
                'A phase-controlled section and feature-specific grid reference for 1I. A Mamluk-only cistern excludes its cistern identity from the date-window claim; bath eligibility requires an explicitly justified text/source-type branch.')
    actions = {
        '21': ('dated conduit head, marker identity and direction, Sekakah association, depth datum',
               'A same-phase head plan and section with the retained reading’s marker and north datum. A contrary marker bearing or water-origin direction rejects that direction branch; undated or absent markers remain unknown.'),
        '29': ('northern relation in the contemporary pool complex, phase-controlled conduit connection, 24-cubit wall/floor datum',
               'A dated whole-complex plan establishing the pool’s northern relation. A contemporary reservoir farther north contradicts the northernmost interpretation; a named north relation alone requires its textual branch to be fixed.'),
        '32': ('installation-specific date, head/outlet identity, wall at that outlet, textual Kozeba association',
               'A dated head/outlet section locating a wall at the mouth itself. A wall along the conduit supplies no outlet-wall support; only a phase relation and fixed interpretation can discriminate competing Qelt heads.'),
        '42': ('same-phase conduit bend, precise waterfall/dam position and separation, date',
               'A surveyed plan of the named feature and contemporary conduit bend. A measured distance beyond the fixed 250 m or 1 km tolerance rejects that spatial branch.'),
        '45': ('one named cistern with same-phase channel supply, wadi catchment and lining, entrance/depth datum',
               'A dated plan and section tying one cistern to its channel and named wadi. An exclusive roof/direct-runoff source rejects the wadi-channel interpretation; an aggregate of separate cisterns cannot discriminate a single target.'),
        '46': ('same-phase access and feature date, feature-specific position, Beth ha-Kerem identification, full textual relation',
               'A dated entrance section and feature-specific position. Access first constructed after 135 CE rejects the period-compatible entrance; a position outside the fixed tolerance rejects only that place-distance branch.'),
    }
    missing, observation = actions[entry]
    if 'B-any' in branch:
        missing += '; B-any has no place constraint and is only a morphology control'
    if unknowns:
        missing = 'unresolved scored clauses: ' + ', '.join(unknowns) + '; ' + missing
    return missing, observation


def main(output=HERE):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    protected = [p for p in LANE.iterdir() if p.is_file()]
    before_sha = {p.name: sha(p) for p in protected}
    inputs = [LANE / fn for fn in LEDGERS] + [LANE / 'phase4_survey_rows.csv', LANE / 'phase4_counts.csv',
             LANE / 'survey_rows.csv', LANE / 'site_points.csv', LANE / 'sources_read.csv', HERE / 'decisions.csv']
    inputs += [LANE / 'scripts' / n for n in ('score.py', 'build_water.py', 'iaa_view.py', 'phase4_view.py',
                                            'literature_data.py', 'literature_data_2.py', 'common.py')]
    inputs += [HERE / 'PLAN.md', HERE / 'rebuild.py', Path(C.PLACES_CSV)]
    inputs += [Path(C.REPO) / p for p in IV.BW.REPO_TEXT.values()]
    for name, h in PV.INPUT_SHA.items():
        p = Path(PV.MERGED) / name
        if sha(p) != h:
            raise ValueError(f'Phase-4 inventory pin differs: {name}')
        inputs.append(p)
    checks = load_checks()
    decisions = {(r['id'], r['clause']): r for r in read(HERE / 'decisions.csv')}
    for key in decisions:
        if key not in checks or checks[key]['verdict'] != 'not confirmed':
            raise ValueError(f'Explicit contradiction must have a not-confirmed review: {key}')
    survey = read(LANE / 'phase4_survey_rows.csv')
    kept = [r for r in read(LANE / 'survey_rows.csv') if r['lineage'] != 'HAESI']
    impacts, result_counts, summary = [], [], {}
    with tempfile.TemporaryDirectory(prefix='water_manual_overlay_') as tmp:
        with contextlib.redirect_stderr(io.StringIO()):
            baseline = IV.run(kept + survey, str(Path(tmp) / 'primary'))
        if sha(baseline['counts.csv']) != sha(LANE / 'phase4_counts.csv'):
            raise ValueError('Rebuilt primary counts do not reproduce the committed phase-4 view')
        baseline_rows = read(baseline['scores.csv'])
        water = {r['id']: r for r in read(baseline['water.csv'])}
        units = {r['unit_id']: r['row_ids'].split(';') for r in read(baseline['merged_units.csv'])}
        uncorrected_detail = aggregate(baseline_rows, units)
        if count(baseline_rows, uncorrected_detail) != [dict(r, **{k: int(r[k]) for k in ('N', 'k_match', 'f_fail', 'm_unknown')})
                                                      for r in read(baseline['counts.csv'])]:
            raise ValueError('Overlay aggregation does not reproduce unchanged scoring')
        p4checks = load_checks(['phase4_posthoc_checks.csv'])
        p4unconfirmed = {k: r for k, r in p4checks.items() if r['verdict'] == 'not confirmed'}
        variants = [('phase4_unconfirmed_only', p4unconfirmed, 'verified'),
                    ('phase4_checks_only', p4checks, 'verified'),
                    ('verified', checks, 'verified'), ('retain_partial', checks, 'retain_partial')]
        for tag, scope, partial in variants:
            rows, changes = repair_scores(baseline_rows, scope, decisions, partial)
            detail = aggregate(rows, units)
            counts = count(rows, detail)
            write(output / f'{tag}_counts.csv', counts)
            impacts += compare(uncorrected_detail, detail, tag)
            result_counts += [dict(r, view=tag) for r in counts]
            summary[tag] = dict(applied_row_clause_pairs=len({(r['id'], r['clause']) for r in changes}),
                                branch_scores_changed=len(changes),
                                merged_branch_changes=len(compare(uncorrected_detail, detail, tag)))
            if tag == 'verified':
                write(output / 'correction_audit.csv', changes)
                write(output / 'verified_merged_scores.csv', detail)
                write(output / 'verified_clause_counts.csv', clause_counts(rows, detail))
                write(output / 'surviving_leads.csv', lead_rows(detail, units, water, checks))
        bracket_rows, _ = IV.bracket(kept, survey, baseline['water.csv'])
        quote_rows, _, _, _ = PV.merged_rows(C.load_places(), subtype=False)
        for tag, inrows in [('bracket_verified', bracket_rows), ('quoteonly_verified', kept + quote_rows)]:
            with contextlib.redirect_stderr(io.StringIO()):
                files = IV.run(inrows, str(Path(tmp) / tag))
            raw = read(files['scores.csv'])
            rows, _ = repair_scores(raw, checks, decisions)
            rununits = {r['unit_id']: r['row_ids'].split(';') for r in read(files['merged_units.csv'])}
            detail = aggregate(rows, rununits)
            counts = count(rows, detail)
            write(output / f'{tag}_counts.csv', counts)
            result_counts += [dict(r, view=tag) for r in counts]
        write(output / 'all_view_counts.csv', result_counts)
    impact_fields = ['view', 'unit_id', 'entry', 'branch', 'original_overall', 'corrected_overall', 'original_date', 'corrected_date']
    write(output / 'merged_match_changes.csv', impacts, impact_fields)
    if before_sha != {p.name: sha(p) for p in protected}:
        raise ValueError('An existing lane file changed')
    summary.update(input_sha256={str(p.relative_to(Path(C.REPO))): sha(p) for p in inputs},
                   note='Separate exploratory review overlay; original lane files remain byte-identical.',
                   date_rule_note='A failed date-only eligibility rule is counted in f_fail; it is not a source contradiction.',
                   inspection_scope='Existing coded rows and manual review ledgers; no new source PDFs or reserved observations opened.')
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k in ('phase4_checks_only', 'verified', 'retain_partial')}))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else HERE)
