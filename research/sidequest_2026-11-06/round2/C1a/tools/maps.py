"""maps.py NAME LAT LON HALF_M layer:z [layer:z ...] -> pv/NAME_maps.png (north-up, same box, 700 px each)"""
import sys, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tiles as T
name, lat, lon, half = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
dlat = half / 111320; dlon = half / (111320 * np.cos(np.radians(lat)))
ims = []
for spec in sys.argv[5:]:
    L, z = spec.split(":"); z = int(z)
    im, org = T.mosaic(L, z, lat - dlat, lon - dlon, lat + dlat, lon + dlon)
    a = cv2.resize(np.array(im), (700, 700), interpolation=cv2.INTER_AREA)
    a = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    cv2.line(a, (340, 350), (360, 350), (0, 0, 255), 1); cv2.line(a, (350, 340), (350, 360), (0, 0, 255), 1)
    cv2.putText(a, spec, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    ims.append(a); ims.append(np.full((700, 6, 3), 255, np.uint8))
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pv"), exist_ok=True)
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pv", f"{name}_maps.png"), np.hstack(ims[:-1]))
print("ok", 2 * half, "m box")
