"""Local evidence retrieval and source-preserving adapters; standard library only."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sqlite3
import subprocess
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = HERE / 'cache'
BASE = '26871df2e5e673f590b6fdf031489791dd88c38b'
URL = 'https://github.com/quadrin/CopperScroll/blob/'


def read(path, root=ROOT):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def rows(path, root=ROOT):
    with (root / path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def rows_with_lines(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        reader.fieldnames  # Read the header before recording physical line starts.
        while True:
            start = reader.line_num + 1
            try:
                yield start, next(reader)
            except StopIteration:
                return


def dump(value, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def source_link(path, line=None, ref=BASE):
    return URL + ref + '/' + quote(str(path), safe='/') + (f'#L{line}' if line else '')


def repository_ref(root=ROOT):
    """Pin new source links to the checked-out commit, with a non-Git fallback."""
    try:
        ref = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                             check=True, capture_output=True, text=True, timeout=2).stdout.strip()
        if re.fullmatch('[0-9a-f]{40}', ref):
            return ref
    except (OSError, subprocess.SubprocessError):
        pass
    return BASE


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def search_text(value):
    """Normalize accents/vocalization for retrieval, preserving source bytes."""
    return ''.join(c for c in unicodedata.normalize('NFD', value) if not unicodedata.combining(c))


def source_paths(root=ROOT, ocr=False):
    """Deduplicate atlas mirrors and keep raw OCR an explicit local opt-in."""
    prefixes = ('research/', 'registration/', 'tables/', 'text/')
    excluded = ('research/shared_tools/', '/downloads/', '/packets/', '/wave1_copy/')
    suffixes = {'.md', '.json', '.csv'} | ({'.txt'} if ocr else set())
    result = []
    for prefix in prefixes:
        for p in (root / prefix).rglob('*'):
            rel = p.relative_to(root).as_posix()
            if p.is_file() and p.suffix in suffixes and not any(x in rel for x in excluded):
                # Other generated/evaluation outputs are not acquisition records.
                if p.suffix == '.json' and not any(x in rel for x in ('registration/', '/assets/', '/sources/', 'text/')):
                    continue
                if p.suffix == '.csv' and not any(x in rel for x in ('tables/', '/sources/', '/assets/')):
                    continue
                result.append(p)
    return sorted(set(result))


def walk_objects(value, pointer='', inherited=None):
    inherited = dict(inherited or {})
    if isinstance(value, dict):
        for k in ('source_title', 'publication', 'source_url', 'source', 'rights', 'reuse', 'inspection'):
            if k in value and isinstance(value[k], (str, bool)):
                inherited[k] = value[k]
        yield pointer or '/', {**inherited, **value}
        for k, v in value.items():
            yield from walk_objects(v, pointer + '/' + str(k).replace('~', '~0').replace('/', '~1'), inherited)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk_objects(v, pointer + '/' + str(i), inherited)


def locator_record(obj, manifest):
    """Preserve explicit printed/PDF locators; never calculate page offsets."""
    if not any(k in obj for k in ('repository_path', 'pdf_page', 'pdf_page_one_based', 'printed_page', 'figure')):
        return None
    asset = obj.get('repository_path')
    if not isinstance(asset, str):
        file = obj.get('file')
        asset = str(Path(manifest).parent / file) if isinstance(file, str) else None
    # Only repository-relative assets become repository links.
    if asset and (Path(asset).is_absolute() or '..' in Path(asset).parts or asset.startswith(('http:', 'https:'))):
        asset = None
    original = obj.get('original_pdf')
    pdf = str(Path(manifest).parent / original) if isinstance(original, str) else None
    page = obj.get('pdf_page_one_based', obj.get('pdf_page'))
    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        page = None
    printed = obj.get('printed_page')
    if isinstance(printed, (dict, list)):
        printed = json.dumps(printed, ensure_ascii=False)
    title = obj.get('source_title') or obj.get('publication') or obj.get('title') or Path(manifest).parent.name
    label = obj.get('figure') or obj.get('items') or obj.get('caption') or obj.get('file') or 'Source locator'
    return {'title': str(title), 'label': str(label), 'asset_path': asset, 'original_pdf': pdf,
            'printed_page': printed, 'pdf_page_one_based': page,
            'inspection_as_recorded': obj.get('visually_inspected', obj.get('inspection', 'not recorded')),
            'rights_as_recorded': obj.get('rights', obj.get('reuse', 'consult source manifest'))}


def evidence_records(root=ROOT, ocr=False, ref=BASE):
    for p in source_paths(root, ocr):
        rel = p.relative_to(root).as_posix()
        content = p.read_text(encoding='utf-8-sig')
        if p.suffix == '.json':
            objects = list(walk_objects(json.loads(content)))
            document_titles = {str(obj.get('file') or Path(str(obj.get('repository_path', ''))).name):
                               obj.get('source_title') or obj.get('title')
                               for _, obj in objects if obj.get('source_title') or obj.get('title')}
            for pointer, obj in objects:
                if obj.get('original_pdf') in document_titles:
                    obj = {**obj, 'source_title': document_titles[obj['original_pdf']]}
                loc = locator_record(obj, rel)
                if loc:
                    loc['asset_url'] = source_link(loc['asset_path'], ref=ref) if loc['asset_path'] else None
                    body = json.dumps({k: v for k, v in obj.items() if k not in ('direct_image_url',)}, ensure_ascii=False)
                    yield {'id': rel + '#' + pointer, 'kind': 'figure', 'path': rel, 'line': None,
                           'title': loc['title'], 'body': body, 'locator': loc, 'url': source_link(rel, ref=ref)}
        elif p.suffix == '.csv':
            for n, row in rows_with_lines(p):
                clean = {k: v for k, v in row.items() if k != 'direct_image_url'}
                yield {'id': f'{rel}#row{n}', 'kind': 'catalog', 'path': rel, 'line': n,
                       'title': row.get('title') or row.get('constraint') or Path(rel).name,
                       'body': json.dumps(clean, ensure_ascii=False), 'locator': clean, 'url': source_link(rel, n, ref=ref)}
        else:
            title = Path(rel).stem
            section, start, chunk = title, 1, []
            for n, line in enumerate(content.splitlines(), 1):
                if line.startswith('#') or len(chunk) >= 24:
                    if chunk:
                        yield {'id': f'{rel}#L{start}', 'kind': 'ocr' if p.suffix == '.txt' else 'note',
                               'path': rel, 'line': start, 'title': section, 'body': '\n'.join(chunk),
                               'locator': {'inspection_as_recorded': 'project note; consult linked original'},
                               'url': source_link(rel, start, ref=ref)}
                    chunk, start = [], n
                    if line.startswith('#'):
                        section = line.lstrip('# ').strip()
                chunk.append(line)
            if chunk:
                yield {'id': f'{rel}#L{start}', 'kind': 'ocr' if p.suffix == '.txt' else 'note',
                       'path': rel, 'line': start, 'title': section, 'body': '\n'.join(chunk),
                       'locator': {'inspection_as_recorded': 'project note; consult linked original'}, 'url': source_link(rel, start, ref=ref)}


def build_index(root=ROOT, destination=CACHE, ocr=False):
    destination.mkdir(parents=True, exist_ok=True)
    ref = repository_ref(root)
    db = destination / 'evidence.sqlite'
    with tempfile.NamedTemporaryFile(dir=destination, prefix='evidence-', suffix='.sqlite', delete=False) as file:
        staged = Path(file.name)
    try:
        with sqlite3.connect(staged) as con:
            con.executescript('CREATE TABLE records(id TEXT PRIMARY KEY,kind TEXT,path TEXT,line INTEGER,title TEXT,body TEXT,locator TEXT,url TEXT); '
                              'CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED,title,body,tokenize="unicode61 remove_diacritics 2");')
            for item in evidence_records(root, ocr, ref):
                con.execute('INSERT INTO records VALUES(?,?,?,?,?,?,?,?)',
                            [item[k] for k in ('id', 'kind', 'path', 'line', 'title', 'body')] + [json.dumps(item['locator'], ensure_ascii=False), item['url']])
                con.execute('INSERT INTO search VALUES(?,?,?)', (item['id'], search_text(item['title']), search_text(item['body'])))
        staged.replace(db)
    finally:
        staged.unlink(missing_ok=True)
    # Hash the exact bytes used, independent of workspace or wall-clock time.
    inputs = {p.relative_to(root).as_posix(): digest(p) for p in source_paths(root, ocr)}
    dump({'base_commit': ref, 'ocr_opt_in': ocr, 'inputs': inputs, 'builder_sha256': digest(HERE / 'core.py')}, destination / 'index_inputs.json')


def check_index(root=ROOT, destination=CACHE):
    meta = json.loads((destination / 'index_inputs.json').read_text())
    expected = {p.relative_to(root).as_posix(): digest(p) for p in source_paths(root, meta['ocr_opt_in'])}
    if meta['inputs'] != expected or meta.get('builder_sha256') != digest(HERE / 'core.py'):
        raise ValueError('Source index is stale. Rebuild before searching.')


def search(query, kind=None, limit=20, destination=CACHE, root=ROOT):
    check_index(root, destination)
    terms = re.findall(r'[^\W_]+', search_text(query), flags=re.UNICODE)
    if not terms:
        return []
    expr = ' AND '.join('"' + t.replace('"', '""') + '"' for t in terms)
    with sqlite3.connect(destination / 'evidence.sqlite') as con:
        con.row_factory = sqlite3.Row
        sql = ('SELECT r.id,r.kind,r.path,r.line,r.title,r.locator,r.url, '
               'snippet(search,2,"[", "]", " … ",40) AS excerpt '
               'FROM search JOIN records r ON r.id=search.id WHERE search MATCH ?')
        args = [expr]
        if kind:
            sql += ' AND r.kind=?'
            args.append(kind)
        sql += ' ORDER BY bm25(search),r.id LIMIT ?'
        args.append(max(1, min(int(limit), 100)))
        result = [dict(row) for row in con.execute(sql, args)]
    for item in result:
        item['locator'] = json.loads(item['locator'])
        item['excerpt_kind'] = 'accent/vocalization-normalized retrieval text; consult source for exact spelling'
    return result


def manuscript(root=ROOT):
    directory = 'research/sources/usc_copper_scroll_images/'
    acquired = {}
    for file in ('cuts_01_10_preview_manifest.csv', 'remaining_preview_manifest.csv'):
        for row in rows(directory + file, root):
            if row['uc_identifier'] in acquired:
                raise ValueError('Duplicate acquisition identity')
            acquired[row['uc_identifier']] = row
    images = []
    for row in rows(directory + 'index.csv', root):
        a = acquired.get(row['uc_identifier'], {})
        kind = row['item_type']
        substrate = 'original' if kind.startswith('original') else 'replica'
        images.append({'id': row['uc_identifier'], 'title': row['title'], 'substrate': substrate,
                       'item_type': kind, 'column_as_catalogued': int(row['column']) if row['column'] else None,
                       'cut_as_catalogued': int(row['cut']) if row['cut'] else None, 'side': row['side'] or None,
                       'lighting_as_titled': row['lighting_as_titled'] or None,
                       'light_direction_observed': row['light_direction_observed'],
                       'view_transform': None, 'metric_depth_calibration': None,
                       'catalog_url': row['usc_link'], 'asset_path': a.get('filename'),
                       'width_px': int(a['width_px']) if a.get('width_px') else None,
                       'height_px': int(a['height_px']) if a.get('height_px') else None,
                       'sha256_as_recorded': a.get('sha256'), 'rights': row['rights'],
                       'catalog_identity_caveat': a.get('note') or None})
    claims = read('research/shared_tools/mapping_claims.json', root)
    by_id = {i['id']: i for i in images}
    for claim in claims:
        if claim['status'] == 'authenticated' and not all(claim.get(k) for k in ('neighboring_original_hebrew', 'original_roi', 'view_id', 'source')):
            raise ValueError('Authenticated mapping requires an original phrase, ROI, view and source')
        if claim['status'] == 'authenticated':
            view = by_id.get(claim['view_id'])
            if not view or view['substrate'] != 'original':
                raise ValueError('Authenticated original mapping requires an original-object view')
            roi = claim['original_roi']
            if (not isinstance(roi, list) or len(roi) != 4
                    or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in roi)
                    or not view['width_px'] or not view['height_px']
                    or not (0 <= roi[0] < roi[2] <= view['width_px'] and 0 <= roi[1] < roi[3] <= view['height_px'])):
                raise ValueError('Authenticated ROI must be finite and bound to the named original view')
    return {'schema': 1, 'sources': [directory + 'index.csv'], 'images': images, 'locus_claims': claims,
            'limits': ['Catalog cut/column identity and original line registration are separate.',
                       'Rotation, illumination direction and metric depth calibration are separate.',
                       'Acquisition metadata is imported; bytes are not re-inspected by this adapter.']}


def normalize_line(value):
    return re.sub(r'[^A-Z0-9]', '', value.upper())


def image_query(data, line=None, cut=None, column=None, substrate=None):
    claims = [c for c in data['locus_claims'] if not line or normalize_line(c['locus']) == normalize_line(line)]
    if line and not claims:
        return {'locus_claims': [], 'images': [], 'status': 'unregistered'}
    cuts = {n for c in claims for n in c.get('candidate_cuts', [])} if line else None
    cols = {c['column'] for c in claims if c.get('column')} if line else None
    images = [i for i in data['images']
              if (not substrate or i['substrate'] == substrate)
              and (cut is None or i['cut_as_catalogued'] == cut)
              and (column is None or i['column_as_catalogued'] == column)
              and (not line or (i['substrate'] == 'original' and i['cut_as_catalogued'] in cuts)
                   or (i['substrate'] == 'replica' and i['column_as_catalogued'] in cols))]
    return {'locus_claims': claims, 'images': images,
            'status': 'candidate views; consult claim status' if line else 'catalog query'}


def entry_packets(root=ROOT):
    translation = read('text/translation_en.json', root)
    variants = read('text/readings.json', root)
    constraints = rows('tables/feature_constraints.csv', root)
    concordance = rows('tables/entry_concordance.csv', root)
    keys = list(translation)
    ordered = [normalize_line(k) for k in keys]
    entries = []
    for row in concordance:
        entry = row['entry_puech']
        ends = re.split(r'[–—]', row['col_line'])
        start, end = normalize_line(ends[0]), normalize_line(ends[-1])
        window = keys[ordered.index(start):ordered.index(end) + 1]
        entries.append({'entry': entry, 'canonical_lines': row['col_line'],
                        'edition_concordance': row,
                        'translation_context': [{'line': k, 'text': translation[k]} for k in window],
                        'boundary_note': 'Shared boundary lines are context; consult division notes before extracting a predicate.',
                        'variants': [v for v in variants if str(v.get('entry')) == entry],
                        'global_variant_ids': [v['id'] for v in variants if not v.get('entry')],
                        'reviewed_constraint_records': [c for c in constraints if c['entry'] == entry],
                        'formal_constraint_status': 'existing records imported; complete predicate extraction pending review',
                        'measurement_origin': None, 'ancient_reference_surface': None,
                        'source_paths': ['text/translation_en.json', 'text/readings.json', 'tables/entry_concordance.csv', 'tables/feature_constraints.csv']})
    ids = [e['entry'] for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate canonical entry')
    return {'schema': 1, 'entries': entries, 'global_variants': [v for v in variants if not v.get('entry')],
            'limits': 'Edition-based project text and existing constraints; no new manuscript reading or candidate score.'}


def control_packets(root=ROOT):
    caves = read('research/feature_workbench/inventory/catalog.json', root)
    pools = read('research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.json', root)
    register = read('research/feature_workbench/register.json', root)
    return {'schema': 1, 'cave_controls': caves['candidates'], 'cave_sources': caves['sources'],
            'pool_notices': pools['records'], 'pool_sources': pools['sources'],
            'feature_register': register['features'], 'observations': register['observations'],
            'eligible_regional_denominator': None, 'coverage_complete': None,
            'equal_opportunity_rule': 'Apply the same retained branch set to every candidate and control; missing observations stay unknown.',
            'limits': 'Selected reviewed controls and documentary notices; no regional census or inferred physical-feature deduplication.'}


def build(root=ROOT, destination=CACHE, ocr=False):
    build_index(root, destination, ocr)
    dump(manuscript(root), destination / 'manuscript.json')
    dump(entry_packets(root), destination / 'entries.json')
    dump(control_packets(root), destination / 'controls.json')
    dependencies = {
        'manuscript': ['research/shared_tools/mapping_claims.json',
                       'research/sources/usc_copper_scroll_images/index.csv',
                       'research/sources/usc_copper_scroll_images/cuts_01_10_preview_manifest.csv',
                       'research/sources/usc_copper_scroll_images/remaining_preview_manifest.csv'],
        'entries': ['text/translation_en.json', 'text/readings.json', 'tables/entry_concordance.csv', 'tables/feature_constraints.csv'],
        'controls': ['research/feature_workbench/inventory/catalog.json',
                     'research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.json',
                     'research/feature_workbench/register.json']}
    dump({'builder_sha256': digest(HERE / 'core.py'),
          'datasets': {name: {path: digest(root / path) for path in paths} for name, paths in dependencies.items()}},
         destination / 'adapter_inputs.json')
    return {'status': 'built', 'base_commit': repository_ref(root), 'destination': str(destination)}


def cached_dataset(name, root=ROOT, destination=CACHE):
    meta = json.loads((destination / 'adapter_inputs.json').read_text())
    sources = meta['datasets'][name]
    if meta['builder_sha256'] != digest(HERE / 'core.py') or any(digest(root / path) != sha for path, sha in sources.items()):
        raise ValueError('Dataset cache is stale. Rebuild before querying.')
    return json.loads((destination / (name + '.json')).read_text())
