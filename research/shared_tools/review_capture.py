"""Prepare anonymous review and acquisition records without sending correspondence."""
from __future__ import annotations
import csv
import hashlib
import json
import re
from pathlib import Path
from core import ROOT, HERE, dump, manuscript, image_query, digest

CAPTURE_FIELDS = ['asset_id', 'local_file', 'sha256', 'object_or_document_id', 'custodian',
                  'capture_date', 'source_url', 'printed_page', 'pdf_page_one_based',
                  'figure', 'view_id', 'substrate', 'side', 'lighting_label', 'rotation_label',
                  'scale_description', 'north_kind', 'coordinate_frame', 'phase_basis',
                  'derivative_of', 'reuse_permission', 'notes']


def export_review(destination, root=ROOT):
    """IDs and source provenance live only in the separate coordinator key."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Use a new export directory; preserve previous reader packets.')
    (destination / 'reviewer').mkdir(parents=True)
    (destination / 'coordinator').mkdir()
    data = manuscript(root)
    # Only recorded candidate views; this export does not reopen their reading test.
    selected = image_query(data, line='VII 11', substrate='original')['images']
    selected += image_query(data, line='XII 10', substrate='original')['images']
    selected = sorted({i['id']: i for i in selected}.values(), key=lambda i: i['id'])
    key, items = [], []
    for n, image in enumerate(selected, 1):
        code = f'R{n:03}'
        key.append({'code': code, **image})
        items.append({'code': code, 'file': None, 'task': 'Describe visible strokes and physical anchors; use uncertain when unresolved.',
                      'status': 'needs_source_asset_and_verified_target_crop'})
    dump(items, destination / 'reviewer' / 'items.json')
    dump(key, destination / 'coordinator' / 'source_key.json')
    (destination / 'reviewer' / 'INSTRUCTIONS.md').write_text(
        '# Independent image review\n\nRecord the item code, view code, visible strokes, legible neighboring characters, '
        'damage, proposed alternatives and confidence. Mark unreadable areas explicitly. '
        'Finish the stroke description before proposing a word.\n\n'
        'The coordinator must supply anonymous, authorized images with verified target placement '
        'and legible original-letter controls before distributing this packet. '
        'Keep the source key outside the reviewer folder.\n', encoding='utf-8')
    with (destination / 'reviewer' / 'responses.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['code', 'view_code', 'visible_strokes', 'neighboring_characters', 'damage', 'alternatives', 'confidence_0_to_1', 'unreadable'])
        writer.writerows([[i['code'], '', '', '', '', '', '', ''] for i in items])
    dump({'status': 'prepared_metadata_only', 'dispatch': 'not_sent',
          'gates': ['authorized source images', 'registered target and neighboring original Hebrew',
                    'independently established original-letter controls', 'independent readers'],
          'interpretation': 'Preparing this packet gives no new reading vote.'}, destination / 'coordinator' / 'readiness.json')
    return {'status': 'prepared_metadata_only', 'directory': str(destination)}


def capture_template(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / 'capture.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CAPTURE_FIELDS)
    (destination / 'CAPTURE.md').write_text(
        '# Archive and object capture\n\n'
        '1. Record the custodian, object/document identifier and reuse terms.\n'
        '2. Capture the complete page/object and its labels before detail views. Preserve captions, scale and north arrows.\n'
        '3. Record printed and one-based PDF pages separately. Photograph foldouts and their attachment context.\n'
        '4. Give each view a stable code. Record lighting and object rotation separately. Preserve original bytes.\n'
        '5. Describe scales and coordinate frames. Record whether north means true, grid, magnetic or unspecified.\n'
        '6. Keep observed contacts, excavator phase assignments and later interpretations separate in the notes.\n'
        '7. Record derivatives against their original asset. Run the validator to compute hashes and flag missing metadata.\n\n'
        'Use blank cells for unrecorded fields. A blank field remains unknown. A scale bar establishes planar scale; '
        'depth requires its own calibration. Acquisition records establish neither an ancient phase nor a textual reading.\n', encoding='utf-8')
    return {'status': 'template_created', 'directory': str(destination)}


def validate_capture(path):
    path = Path(path).resolve()
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != CAPTURE_FIELDS:
            raise ValueError('Capture columns differ from the template')
        records = list(reader)
    ids, result = set(), []
    for row in records:
        errors, missing = [], []
        identity = row['asset_id']
        if not identity or identity in ids:
            errors.append('asset_id is missing or duplicated')
        ids.add(identity)
        file = (path.parent / row['local_file']).resolve() if row['local_file'] else None
        if file and not file.is_relative_to(path.parent):
            errors.append('local_file leaves the capture directory')
        elif file and file.is_file():
            actual = digest(file)
            if row['sha256'] and row['sha256'] != actual:
                errors.append('sha256 mismatch')
            row['computed_sha256'] = actual
        else:
            missing.append('local asset bytes')
        if row['pdf_page_one_based'] and (not row['pdf_page_one_based'].isdigit() or int(row['pdf_page_one_based']) < 1):
            errors.append('pdf_page_one_based must be a positive integer')
        if row['north_kind'] and row['north_kind'] not in ('true', 'grid', 'magnetic', 'unspecified', 'not_applicable'):
            errors.append('north_kind is unrecognized')
        for field in ('object_or_document_id', 'custodian', 'view_id', 'substrate', 'reuse_permission'):
            if not row[field] or row[field].strip().lower() in ('unknown', 'unrecorded', 'unspecified', 'none', 'n/a'):
                missing.append(field)
        result.append({'record': row, 'status': 'invalid' if errors else ('incomplete' if missing else 'complete_capture_metadata'),
                       'errors': errors, 'unknowns': missing})
    return {'records': result, 'status': 'invalid' if any(r['errors'] for r in result) else ('empty_template' if not result else 'validated'),
            'limits': 'Complete capture metadata is independent of scientific calibration and ancient-phase authentication.'}
