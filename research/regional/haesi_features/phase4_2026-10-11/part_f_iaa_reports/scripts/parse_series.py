#!/usr/bin/env python3
"""Parse the saved IAA Reports gallery pages (series page and index.2/index.3) into item records.

Each record: page, no_label, title, authors, landing_url, abstract (the abstract is used only for a hash;
it is not written to the repository). Standard library only.
"""
import html
import re


def parse(paths):
    out = []
    for path in paths:
        t = open(path, encoding="utf-8", errors="replace").read()
        m = re.search(r'<ul id="gallery_items".*?</ul>', t, re.S)
        for li in re.findall(r"<li>(.*?)</li>", m.group(0), re.S):
            h = re.search(r'<h2><a href="([^"]+)"\s*>(.*?)</a></h2>', li, re.S)
            if not h:
                continue
            url, head = h.group(1), html.unescape(re.sub(r"<[^>]+>", "", h.group(2))).strip()
            no, _, title = head.partition("|")
            ps = re.findall(r"<p>(.*?)</p>", li, re.S)
            clean = [" ".join(html.unescape(re.sub(r"<[^>]+>", " ", p)).split()) for p in ps]
            out.append({"page": str(path).rsplit("/", 1)[-1], "no_label": no.strip(), "title": title.strip(),
                        "authors": clean[0] if clean else "", "landing_url": url,
                        "abstract": " ".join(clean[1:])})
    return out
