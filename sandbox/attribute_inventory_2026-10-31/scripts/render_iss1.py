"""Render pages of an 'Atiqot 41 part 1 (Hebrew) article PDF from the local cache.
usage: python3 render_iss1.py <article_id> info                      -> page count
       python3 render_iss1.py <article_id> <page_1based> <out.png> [dpi] [x0 y0 x1 y1]
The optional box crops the page (in PDF points, page size printed by 'info') for a close-up."""
import glob, sys, pymupdf
aid = sys.argv[1]
doc = pymupdf.open(glob.glob(f"/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/atq41_iss1_pdf/{aid}_*.pdf")[0])
if sys.argv[2] == "info":
    print(doc.page_count, "pages; page size (pt):", doc[0].rect); sys.exit()
pg = doc[int(sys.argv[2]) - 1]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 150
clip = pymupdf.Rect(*map(float, sys.argv[5:9])) if len(sys.argv) > 8 else None
pix = pg.get_pixmap(dpi=dpi, clip=clip); pix.save(sys.argv[3]); print(sys.argv[3], pix.width, pix.height)
