#!/usr/bin/env python3
"""Parse the cached portal item pages (portal/ha<item>.html) into toc.tsv: vol, n, pages, title, author.
The same items are in ../../data/portal_toc_items.csv. Copied from the Mac scratch copy."""
import re, html, os
M = "HA_029-028_1969:64 HA_10_1964:57 HA_11_1964:58 HA_12_1964:59 HA_13_1965:60 HA_14_1965:6 HA_15_1965:55 HA_16_1965:56 HA_17_1966:61 HA_18-19_1966:7 HA_1_1961:1 HA_2-3_1962:2 HA_20_1966:8 HA_21_1967:9 HA_22-23_1967:62 HA_24_1967:10 HA_25_1968:63 HA_26_1968:11 HA_27_1968:12 HA_30_1969:13 HA_31-32_1969:14 HA_33_1970:15 HA_34-35_1970:16 HA_36_1970:65 HA_37_1971:66 HA_38_1971:67 HA_39_1971:68 HA_41-42_1972:75 HA_43_1972:18 HA_46_1973:19 HA_47_1973:20 HA_48-49_1974:21 HA_4_1962:51 HA_50_1974:22 HA_51-52_1974:23 HA_53_1975:24 HA_54-55_1975:25 HA_56_1975:26 HA_57-58_1976:27 HA_5_1963:52 HA_61-62_1977:29 HA_63-64_1977:30 HA_65-66_1978:31 HA_67-68_1978:32 HA_69-71_1979:33 HA_6_1963:53 HA_72_1979:34 HA_7_1963:4 HA_8_1963:5 HA_9_1964:54"
base = os.path.expanduser("~/p3a_scratch/")
out = open(base + "toc.tsv", "w", encoding="utf-8")
tot = 0
for pair in M.split():
    v, n = pair.split(":")
    t = open(base + "portal/ha%s.html" % n, encoding="utf-8", errors="replace").read()
    i = t.find("Description</h2>")
    seg = t[i:t.find("</div>", i)]
    body = re.search(r"<p>(.*)</p>", seg, re.S).group(1)
    items = re.findall(r"<strong>(.*?)</strong>(.*?)\[\s*([0-9]+(?:\s*[–-]\s*[0-9]+)?)\s*\]", body, re.S)
    for k, (ti, au, pg) in enumerate(items, 1):
        ti = html.unescape(re.sub("<[^>]+>", "", ti)).strip(); au = html.unescape(re.sub("<[^>]+>", "", au)).strip().lstrip(",").strip()
        out.write("%s\t%d\t%s\t%s\t%s\n" % (v, k, pg.replace(" ", ""), ti, au)); tot += 1
print(tot)
