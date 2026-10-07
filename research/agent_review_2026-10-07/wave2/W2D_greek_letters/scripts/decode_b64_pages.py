#!/usr/bin/env python3
"""Decode '=====name' + base64-line blocks from a saved device_bash output into image files.
usage: decode_b64_pages.py SAVED_OUTPUT OUTDIR PREFIX"""
import base64, sys, os
src, outdir, prefix = sys.argv[1:4]
name = None
for line in open(src).read().split("\n"):
    if line.startswith("====="):
        name = line[5:].strip(); continue
    if name and len(line) > 1000:
        s = line.strip()
        try:
            b = base64.b64decode(s + "=" * (-len(s) % 4))
            open(os.path.join(outdir, prefix + name), "wb").write(b)
            print("ok", name, len(b))
        except Exception as e:
            print("FAIL", name, e)
        name = None
