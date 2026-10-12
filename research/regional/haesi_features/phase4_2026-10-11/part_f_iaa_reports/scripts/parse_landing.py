#!/usr/bin/env python3
"""Parse saved IAA Reports landing pages (publications.iaa.org.il/iaareports/<id>/) into records.

Fields: landing_id, heading, authors, pdf_url, pdf_size, files [{label, size, url}], abstract,
publication_date, identifier (EISBN), keywords, comments, recommended_citation. Standard library only.
"""
import html
import re
from pathlib import Path


def text(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def element(t, eid):
    m = re.search(r"<div id='%s' class='element'>(.*?)</div>\s*<div class='clear'>" % eid, t, re.S)
    if not m:
        return ""
    v = re.sub(r"<h[1-6][^>]*class=['\"][^'\"]*(visually-hidden|field-heading)[^'\"]*['\"][^>]*>.*?</h[1-6]>",
               " ", m.group(1), flags=re.S)
    v = re.sub(r"^\s*<h4>.*?</h4>", " ", v, flags=re.S)
    return v


def parse_one(p):
    t = Path(p).read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<(script|style)\b.*?</\1>", "", t, flags=re.S | re.I)
    rec = {"landing_id": int(Path(p).stem)}
    rec["heading"] = text(element(t, "title"))
    rec["authors"] = [text(a) for a in re.findall(r"<li>(.*?)</li>", element(t, "authors"), re.S)]
    fl = element(t, "file_list")
    m = re.search(r'id="alpha-pdf" href="([^"]+)"', fl)
    rec["pdf_url"] = html.unescape(m.group(1)) if m else ""
    m = re.search(r"Download Full Text <span class='size'>\(([^)]+)\)", fl)
    rec["pdf_size"] = html.unescape(m.group(1)).replace("\xa0", " ") if m else ""
    rec["files"] = []
    for a in re.finditer(r'<a class="btn btn-small" href="([^"]+)" title="[^"]*">Download</a>\s*(.*?)'
                         r'<span class="size">\(([^)]+)\)</span>', fl, re.S):
        rec["files"].append({"label": text(a.group(2)), "size": html.unescape(a.group(3)).replace("\xa0", " "),
                             "url": html.unescape(a.group(1))})
    for key in ("abstract", "publication_date", "identifier", "keywords", "comments", "recommended_citation"):
        rec[key] = text(element(t, key))
    return rec


def parse(landing_dir):
    return [parse_one(p) for p in sorted(Path(landing_dir).glob("*.html"), key=lambda x: int(x.stem))]
