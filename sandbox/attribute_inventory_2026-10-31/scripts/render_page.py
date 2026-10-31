"""Render one page of an 'Atiqot 41 (English issue) article PDF from the project bucket.
usage: python3 render_page.py <article_id> <page_index_1based> <out.png> [dpi]
       python3 render_page.py <article_id> info      # page count
Needs: source /root/.hexcog_env first (read-only bucket key)."""
import os, sys, glob, boto3, fitz
aid, page = sys.argv[1], sys.argv[2]
cache = f"/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/atq41_pdfcache"
os.makedirs(cache, exist_ok=True)
hit = glob.glob(f"{cache}/{aid}_*.pdf")
if not hit:
    s = boto3.client('s3', endpoint_url='https://storage.googleapis.com', region_name='auto',
                     aws_access_key_id=os.environ['HEXCOG_HMAC_ID'], aws_secret_access_key=os.environ['HEXCOG_HMAC_SECRET'])
    keys = [o['Key'] for o in s.list_objects_v2(Bucket=os.environ['HEXCOG_BUCKET'], Prefix='atiqot/pdf/vol-041/iss-2/')['Contents'] if os.path.basename(o['Key']).startswith(aid + '_')]
    dst = f"{cache}/{os.path.basename(keys[0])}"
    s.download_file(os.environ['HEXCOG_BUCKET'], keys[0], dst + '.part'); os.replace(dst + '.part', dst); hit = [dst]
doc = fitz.open(hit[0])
if page == 'info':
    print(hit[0], doc.page_count); sys.exit()
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 150
pix = doc[int(page) - 1].get_pixmap(dpi=dpi); pix.save(sys.argv[3]); print(sys.argv[3], pix.width, pix.height)
