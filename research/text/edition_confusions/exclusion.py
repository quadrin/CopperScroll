"""The hard exclusion for this folder: nothing from column XII lines 8-12, nothing about the 21/22 cut.

Every builder calls these checks. The build stops if a row would break them.
The frozen XII 10 test (research/agent_review_2026-10-07/wave1/T03_T04_registry/
XII10_IMAGE_READING_PROTOCOL.md) must stay clean.
"""
import re

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
EXCLUDED_COLUMN = 'XII'
EXCLUDED_LINES = range(8, 13)  # 8, 9, 10, 11, 12

# Text patterns that point into the excluded zone: "XII 10", "XII:10", "12:10" (Lefkovits),
# "col. XII 9", and any mention of the segment 21/22 cut.
_PATTERNS = [
    r'\bXII\s*[ :.,]\s*(?:8|9|10|11|12)(?!\d)',
    r'(?<![\d.])12\s*:\s*(?:8|9|10|11|12)(?!\d)',
    r'\b21\s*/\s*22\b',
    r'\b21\s*[-–]\s*22\b',
]
_RX = re.compile('|'.join(_PATTERNS))


def is_excluded(column, line) -> bool:
    """True if (column, line) lies in XII 8-12. Unknown lines in column XII count as excluded."""
    if column is None:
        return False
    col = str(column).strip()
    if col.isdigit():
        col = ROMAN[int(col) - 1]
    if col != EXCLUDED_COLUMN:
        return False
    if line is None or str(line).strip() == '':
        return True
    return int(line) in EXCLUDED_LINES


def ref_excluded(ref: str) -> bool:
    """ref like 'XII 10'."""
    if not ref:
        return False
    parts = ref.replace(':', ' ').split()
    if len(parts) < 2:
        return parts[0] == EXCLUDED_COLUMN if parts else False
    return is_excluded(parts[0], parts[1])


def mentions_excluded(text: str) -> bool:
    """True if a free-text field names a position in XII 8-12 or the 21/22 cut."""
    return bool(_RX.search(text or ''))


def assert_clean_rows(rows, col_key='column', line_key='line', text_keys=()):
    """Raise ValueError if any row lies in, or mentions, the excluded zone."""
    for r in rows:
        if is_excluded(r.get(col_key), r.get(line_key)):
            raise ValueError(f'excluded position in data: {r.get(col_key)} {r.get(line_key)}')
        for k in text_keys:
            if mentions_excluded(str(r.get(k, ''))):
                raise ValueError(f'excluded zone mentioned in field {k!r} at {r.get(col_key)} {r.get(line_key)}')
