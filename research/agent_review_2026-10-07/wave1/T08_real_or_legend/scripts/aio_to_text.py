"""Convert downloaded AIO inscription HTML pages to plain text (translation + notes).
Usage: python3 -I aio_to_text.py <html> [<html> ...]  -> writes .txt next to each html"""
import re, html, sys
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    t = re.sub(r'<br\s*/?>', '\n', t); t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t)
    t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n', t)
    open(p[:-5] + '.txt', 'w', encoding='utf-8').write(t)
    print(p, len(t))
