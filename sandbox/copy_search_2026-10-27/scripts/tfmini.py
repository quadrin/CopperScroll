"""Minimal Text-Fabric .tf reader (node features, oslots edge, otype)."""
import os


def _body(path):
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines) and lines[i].startswith('@'):
        i += 1
    # blank separator line
    if i < len(lines) and lines[i] == '':
        i += 1
    return lines[i:]


def _nodes(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def load_feature(tfdir, name):
    d = {}
    n = 0
    for line in _body(os.path.join(tfdir, name + '.tf')):
        if line == '' and False:
            continue
        if '\t' in line:
            spec, val = line.split('\t', 1)
            ns = _nodes(spec)
            for x in ns:
                d[x] = val
            n = ns[-1]
        else:
            n += 1
            d[n] = line
    return d


def load_otype(tfdir):
    """returns list of (start, end, type) ranges"""
    rng = []
    for line in _body(os.path.join(tfdir, 'otype.tf')):
        if not line:
            continue
        spec, val = line.split('\t')
        a, b = (spec.split('-') + [spec])[:2]
        rng.append((int(a), int(b), val))
    return rng


def load_oslots(tfdir):
    d = {}
    n = 0
    for line in _body(os.path.join(tfdir, 'oslots.tf')):
        if not line:
            continue
        if '\t' in line:
            spec, val = line.split('\t', 1)
            n = int(spec)
        else:
            n += 1
            val = line
        d[n] = val
    return d


def slot_ranges(val):
    out = []
    for part in val.split(','):
        if '-' in part:
            a, b = part.split('-')
            out.append((int(a), int(b)))
        else:
            out.append((int(part), int(part)))
    return out
