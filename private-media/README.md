# Encrypted media

`wsrp-1988/` holds the 1988 West Semitic Research Project colour recto frames of the Copper Scroll (segments 2–8, 10, 11, 16–18), as 1/4-scale previews and strip cut-outs. **Every image file is encrypted** (AES-256-GCM; format in `atlas/scripts/wsrp-media.mjs`). Only `index.json` is plain: segment, light code, strip aspect, sizes and SHA-256 of each file.

- **Rights.** Photographs by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary. Courtesy the Department of Antiquities, Jordan. They were supplied as a private study copy and are not for publication. Do not commit decrypted copies; `atlas/protected-media/` and `atlas/dist-protected/` are ignored.
- **Who can see them.** The key is the GitHub Actions secret `WSRP_MEDIA_KEY`. The workflow `.github/workflows/protected-atlas.yml` decrypts them and deploys the access-controlled atlas to Cloudflare Pages behind Cloudflare Access (approved emails only). The public GitHub Pages build never reads this folder, and `atlas/scripts/check-pages-payload.mjs` fails if any of it reaches the public output.
- **Not here.** Segments 19–23 (columns XI–XII) are reserved, unopened, for the blind reading of XII 10; both scripts refuse them. Segments 1, 9 and 12–15 were not in the delivery.
- **Rebuild.** `python3 -I tools/wsrp_strip_cutouts.py <q4 folder> <cut-out folder>`, then `WSRP_MEDIA_KEY=… node atlas/scripts/wsrp-media.mjs encrypt <q4 folder> <cut-out folder>`. The q4 previews are in Drive, "WSRP previews 2026-10-29/previews_q4".
