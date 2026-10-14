#!/usr/bin/env python3
"""Recover the supplied Levy2023 PDF's glyph text without viewing page images.

Some marked-content ActualText replacements suppress entire body paragraphs in
ordinary extraction. Ignore those replacement strings, retaining the underlying
glyph text. This creates a private text derivative, not a repaired PDF, a reading
claim, a physical-leaf completeness check or permission to inspect reserved images.
"""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SHA256 = '08fe807e0550a3e915d5e08f15bdf43e26c855cc6fa2a8809f8c71355305920b'


def main():
    import fitz
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output_json', type=Path)
    args = parser.parse_args()
    source_hash = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SHA256:
        raise SystemExit('Source hash differs; inspect this copy before reusing the extraction method.')
    if not hasattr(fitz, 'TEXT_IGNORE_ACTUALTEXT'):
        raise SystemExit('This PyMuPDF version lacks TEXT_IGNORE_ACTUALTEXT.')
    document = fitz.open(args.pdf)
    rows = []
    for number, page in enumerate(document, 1):
        default = page.get_text(flags=fitz.TEXTFLAGS_TEXT)
        recovered = page.get_text(flags=fitz.TEXTFLAGS_TEXT | fitz.TEXT_IGNORE_ACTUALTEXT)
        rows.append({'viewer_page': number, 'default_chars': len(default),
                     'recovered_chars': len(recovered), 'text': recovered})
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(rows, ensure_ascii=False) + '\n', encoding='utf-8')
    summary = {'source_sha256': source_hash, 'source_pages': len(document),
               'pymupdf_version': fitz.VersionBind,
               'flags': fitz.TEXTFLAGS_TEXT | fitz.TEXT_IGNORE_ACTUALTEXT,
               'default_chars': sum(r['default_chars'] for r in rows),
               'recovered_chars': sum(r['recovered_chars'] for r in rows),
               'pages_with_additional_text': [r['viewer_page'] for r in rows
                                              if r['recovered_chars'] > r['default_chars']],
               'output_sha256': hashlib.sha256(args.output_json.read_bytes()).hexdigest(),
               'limit': 'Text acquisition only; source pages control disputed glyphs, layout and figures.'}
    args.output_json.with_suffix('.metadata.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'pages_with_additional_text'}))


if __name__ == '__main__':
    main()
