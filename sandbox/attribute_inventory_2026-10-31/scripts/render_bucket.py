"""Render one page of a page-split PDF in the project bucket (pdf/<slug>/pNNNN.pdf).
usage: source /root/.hexcog_env && python3 render_bucket.py <slug> <pdf_page_1based> <out.png> [dpi] [x0 y0 x1 y1]"""
import os, sys, boto3, pymupdf
slug, page, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 150
cache = f"/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/bucket_pages/{slug}"
os.makedirs(cache, exist_ok=True)
local = f"{cache}/p{page:04d}.pdf"
if not os.path.exists(local):
    s = boto3.client('s3', endpoint_url='https://storage.googleapis.com', region_name='auto',
                     aws_access_key_id=os.environ['HEXCOG_HMAC_ID'], aws_secret_access_key=os.environ['HEXCOG_HMAC_SECRET'])
    tmp = f"{local}.{os.getpid()}.part"
    s.download_file(os.environ['HEXCOG_BUCKET'], f"pdf/{slug}/p{page:04d}.pdf", tmp); os.replace(tmp, local)
pg = pymupdf.open(local)[0]
clip = pymupdf.Rect(*map(float, sys.argv[5:9])) if len(sys.argv) > 8 else None
pix = pg.get_pixmap(dpi=dpi, clip=clip); pix.save(out); print(out, pix.width, pix.height, "page size pt:", pg.rect)
