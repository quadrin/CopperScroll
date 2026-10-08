"""Rough side-by-side comparison of BayHStA BS Pal. 1031 (2 Jul 1918) with EOxCloudless 2024 (Sentinel-2).
Not orthorectified. Scale of 1918 frame estimated from header H.4500 (m) / Br.50 (cm) and IIIF physicalScale."""
import sys, math
sys.path.insert(0, 'scripts')
from geo3857 import ll2px, m_per_px
from PIL import Image, ImageDraw, ImageFont
old = Image.open('downloads/bayhsta/BSPal_1031.jpg').convert('L')
s2 = Image.open('downloads/s2cloudless/s2cloudless-2024_3857_z16_mosaic.png').convert('RGB')
# --- 1918 frame scale estimate
full_w = 10944; dl_w = old.size[0]
plate_px_cm = 0.00140007  # cm per full-res pixel (IIIF physdim service)
H_agl = 4500 + 250        # header altitude 4500 m, ground ~ -250 m (assumption: altitude a.s.l.)
f = 0.50                  # Br.50 = 50 cm focal length
scale = H_agl / f         # ~9500
m_px_old = plate_px_cm/100 * scale * (full_w/dl_w)
m_px_s2 = m_per_px(31.871)
print(f'1918 approx scale 1:{scale:.0f}, {m_px_old:.3f} m/px at download res; S2 mosaic {m_px_s2:.3f} m/px')
# rotate 1918 so the drawn north arrow points up (arrow ~12 deg clockwise of image-up)
rot = 12.3
tell_old = (2150, 1060)   # visually picked tell centre in 4000-px frame (approx.)
oc = (old.size[0]/2, old.size[1]/2)
old_r = old.rotate(rot, resample=Image.BICUBIC, expand=False, center=tell_old, fillcolor=255)
# resample to S2 pixel size
k = m_px_old / m_px_s2
old_rs = old_r.resize((int(old_r.size[0]*k), int(old_r.size[1]*k)), Image.LANCZOS)
tx, ty = tell_old[0]*k, tell_old[1]*k
half_w, half_h = 330, 260   # px at ~2 m/px -> ~1.34 x 1.05 km
A = old_rs.crop((int(tx-half_w), int(ty-half_h), int(tx+half_w), int(ty+half_h))).convert('RGB')
cx, cy = 1898, 1897          # visually picked tell centre in S2 mosaic (approx.)
B = s2.crop((cx-half_w, cy-half_h, cx+half_w, cy+half_h))
Bg = B.convert('L').convert('RGB')
up = 2
A = A.resize((A.size[0]*up, A.size[1]*up)); B = B.resize((B.size[0]*up, B.size[1]*up)); Bg = Bg.resize((Bg.size[0]*up, Bg.size[1]*up))
W = Image.new('RGB', (A.size[0]*2+20, A.size[1]+60), 'white')
W.paste(A, (0, 60)); W.paste(B, (A.size[0]+20, 60))
d = ImageDraw.Draw(W)
d.text((10, 8), 'BayHStA BS Pal. 1031 (Fl.Abt. 304, 2 Jul 1918), CC0 via DDB; rotated ~12 deg to north-up, rescaled ~2 m/px (rough, not orthorectified)', fill='black')
d.text((A.size[0]+30, 8), 'EOxCloudless 2024 (Sentinel-2, 10 m native) CC BY-NC-SA 4.0, EOX IT Services GmbH (contains modified Copernicus Sentinel data 2024)', fill='black')
d.text((10, 30), 'Centred on Tell es-Sultan; width ~%.2f km; north up' % (2*half_w*m_px_s2/1000), fill='black')
W.save('fig_tell_es_sultan_1918_vs_2024.jpg', quality=88)
print('saved', W.size)
