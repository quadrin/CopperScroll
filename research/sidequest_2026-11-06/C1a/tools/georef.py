"""Fit a homography from a HEXAGON/CORONA overview (stored orientation) to an Esri mosaic.
usage: python3 georef.py OV.png OVSCALE ESRI.png Z ORIGX ORIGY OUT.json [X0 Y0]
OV.png is a box/overview read at OVSCALE whose top-left is stored pixel (X0, Y0).
Output: H mapping stored full-res px -> Esri mosaic px, and helpers to lat/lon.
"""
import json, sys
import cv2, numpy as np

ov, s, es, z, ox, oy, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
X0, Y0 = (float(sys.argv[8]), float(sys.argv[9])) if len(sys.argv) > 9 else (0.0, 0.0)
A = cv2.imread(ov, 0); B = cv2.imread(es, 0)
cl = cv2.createCLAHE(3.0, (8, 8)); A2 = cl.apply(A); B2 = cl.apply(B)
sift = cv2.SIFT_create(8000)
ka, da = sift.detectAndCompute(A2, (A > 5).astype(np.uint8))
kb, db = sift.detectAndCompute(B2, None)
m = cv2.BFMatcher().knnMatch(da, db, k=2)
good = [a for a, b in m if a.distance < 0.8 * b.distance]
pa = np.float32([ka[g.queryIdx].pt for g in good]); pb = np.float32([kb[g.trainIdx].pt for g in good])
# to stored full-res
pa_full = pa / s + np.float32([X0, Y0])
Hm, inl = cv2.findHomography(pa_full, pb, cv2.RANSAC, 4.0, maxIters=20000)
inl = inl.ravel().astype(bool)
res = cv2.perspectiveTransform(pa_full[inl][None], Hm)[0] - pb[inl]
r = np.sqrt((res ** 2).sum(1))
print("matches", len(good), "inliers", int(inl.sum()), "median resid esri px", float(np.median(r)), "p90", float(np.percentile(r, 90)))
json.dump({"H_stored_to_esri_px": Hm.tolist(), "esri_z": z, "esri_origin_tiles": [ox, oy], "n_inl": int(inl.sum()),
           "median_resid_esri_px": float(np.median(r)), "src": ov, "src_scale": s, "src_offset": [X0, Y0],
           "inlier_pairs_full": np.hstack([pa_full[inl], pb[inl]]).tolist()}, open(out, "w"))
