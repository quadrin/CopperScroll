# Encrypted media

Private image sets of the access-controlled atlas. **Every image file is encrypted** (AES-256-GCM; format in `atlas/scripts/wsrp-media.mjs`). Only each folder's `index.json` is plain: file names, sizes and SHA-256.

| Folder | What | Terms |
|---|---|---|
| `wsrp-1988/` | WSRP 1988 colour recto masters, segments 2–8, 10, 11, 16–18, as 1/4-scale previews | Photographs by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary; courtesy the Department of Antiquities, Jordan. Private study copy, not for publication. |
| `allegro-dqcaas/` | John Allegro's photographs of segments 10 and 21–23, 2017 DQCAAS scans of prints | Courtesy of the John Allegro estate © Judith Brown, licensed via DQCAAS. Study copy; publication needs a licence. |

- **Who can see them.** The key is the GitHub Actions secret `WSRP_MEDIA_KEY`. `.github/workflows/protected-atlas.yml` decrypts them, builds the image library with `tools/build_scroll_media.py` (which adds the USC public previews, the EDF facsimile photographs and the DJD III plates already in the repository) and deploys the atlas to Cloudflare Pages behind Cloudflare Access (approved emails only). The public GitHub Pages build never reads these folders, and `atlas/scripts/check-pages-payload.mjs` fails if any `media/`, `wsrp/` or `.enc` file reaches its output. Do not commit decrypted copies; `atlas/protected-media/` and `atlas/dist-protected/` are ignored.
- **Segments 19–23.** Released to the protected atlas on 30 October 2026 by the owner's decision; the XII 10 images are exposed ([record](../research/sources/books_usc_2026-10-30/xii_images_released_2026-10-30.md)). The WSRP masters of 19–23 are not yet added.
- **Add a set.** `WSRP_MEDIA_KEY=… node atlas/scripts/wsrp-media.mjs encrypt <set name> <folder of images>`.
