#!/usr/bin/env python3
"""Partial decoder for the custom Greek font in the CIIP I part 2 PDF text layer (lower-case
Greek only; capitals are NOT extracted by pdftotext and cannot be recovered). Mapping derived
from known words in the volume (e.g. 'Ä¸Éº¸ÉĕË' = μαργαρίς, 'ÎįÉ¸Ä¸' = φύραμα).
usage: ciip1b_decode.py ciip1b.txt OUT.txt   (run on the device copy; used only for scanning)"""
import sys
base = {0xB8:'α',0xB9:'β',0xBA:'γ',0xBB:'δ',0xBC:'ε',0xBD:'ζ',0xBE:'η',0xBF:'θ',0xC0:'ι',0xC1:'κ',0xC2:'λ',
        0xC4:'μ',0xC5:'ν',0xC6:'ξ',0xC7:'ο',0xC8:'π',0xC9:'ρ',0xCA:'σ',0xCB:'ς',0xCC:'τ',0xCD:'υ',0xCE:'φ',
        0xCF:'χ',0xD0:'ψ',0xD1:'ω',0x115:'ι',0x120:'ο',0x12F:'υ',0xF1:'ε',0xDA:'α',0x13E:'ω',0xF7:'η',
        0xEC:'ε',0x163:'ι',0xFC:'η'}
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
open(sys.argv[2], 'w', encoding='utf-8').write(''.join(base.get(ord(c), c) for c in t))
