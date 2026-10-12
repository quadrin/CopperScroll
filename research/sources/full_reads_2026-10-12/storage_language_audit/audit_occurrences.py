#!/usr/bin/env python3
"""Rebuild the bounded occurrence audit from the repository's displayed text.
Ancient-text/transcription provenance: ETCBC DSS TF2.0.1, Abegg/Bowley/Cook;
display conversion Jacobs/Naaijer/Roorda; CC BY-NC4.0.
"""
import argparse, hashlib, json, re
from pathlib import Path
ROMAN = ["", "I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
ENTRY_BY_LINE = {(5,6):22,(7,4):29,(10,5):46,(11,12):55,(1,15):5,(3,7):12}
def build(source):
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    data = json.loads(text.split("window.SCROLL_TEXT = ",1)[1].rstrip().removesuffix(";"))
    water, root_hits, numbers = [], [], []
    for col in data["columns"]:
        for line in col["lines"]:
            loc = f'{ROMAN[col["c"]]} {line["l"]}'
            context = " ".join("".join(s[0] for s in w["h"]) if "n" not in w else f'[{w["n"]}]' for w in line["w"])
            for i,w in enumerate(line["w"]):
                rendered = "".join(s[0] for s in w["h"])
                morph = [m[0] for m in w.get("m",[])]
                if any(term in rendered for term in ["אשיח","אשוח"]):
                    water.append(dict(entry=ENTRY_BY_LINE.get((col["c"],line["l"])),line=loc,word_index_zero_based=i,rendered=rendered,segments=w["h"],surface_morphology=morph,context=context))
                if "טמר" in rendered or "מטמר" in rendered or any("טמר" in m or "מטמר" in m for m in morph):
                    root_hits.append(dict(line=loc,rendered=rendered,surface_morphology=morph))
                if w.get("n") in [35,40]:
                    numbers.append(dict(entry=ENTRY_BY_LINE.get((col["c"],line["l"])),line=loc,value=w["n"],notation=w.get("ns"),context=context))
    return dict(schema_version=1,source_path="data/scroll-text.js",source_sha256=hashlib.sha256(raw).hexdigest(),scope="one derivative displayed transcription; not a manuscript/edition-variant exhaustive audit",searched_roots=["טמר","מטמר"],root_matches=root_hits,water_forms=water,water_token_count=len(water),water_line_count=len({x["line"] for x in water}),number_35_or_40_tokens=numbers,numeric_role_note="the recorded 40 tokens stand beside ככר/ככ quantities; modern entry35/40 numbers are editorial labels")
def main():
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,default=Path("data/scroll-text.js"));p.add_argument("--output",type=Path,default=Path(__file__).with_name("corpus_occurrences.json"));p.add_argument("--check",action="store_true");a=p.parse_args()
    result=build(a.source)
    if a.check:
        assert result == json.loads(a.output.read_text()), "Saved occurrence audit differs"
        assert result["water_token_count"]==5 and result["water_line_count"]==4
        assert not result["root_matches"]
        print("Occurrence audit rebuilds exactly:5 water tokens/4 lines; no bounded טמר matches.")
    else:a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__":main()

