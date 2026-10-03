"""Source-neutral whole-corpus attestation extraction, NOT prefix scoring.

Hidden OCR spellings are retained only as unvalidated raw evidence. Every
Greek_form stays null until independent image/OCR review supplies it. Dates and
region hints never establish eligibility by themselves.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import statistics
import fitz

SECTIONS = ((59,238,"biblical_male"),(239,256,"biblical_female"),
    (257,312,"greek_male"),(313,324,"greek_female"),
    (325,341,"latin_male"),(342,345,"latin_female"),
    (346,355,"persian_male"),(356,356,"persian_female"),
    (357,417,"other_hebrew_male"),(418,429,"other_hebrew_female"),
    (430,442,"other_greek_male"),(443,444,"other_greek_female"),
    (445,448,"appendix_ha"),(449,454,"addendum"))
START = re.compile(r"^\s*([\dIl]+)\s*[.)]?\s*(?:[O0o]|\(\))\s*:")
FIELDS = re.compile(r"(?<!\w)(O|0|\(\)|D\s*s|F|S|E|D)\s*:", re.I)
FOOTNOTE = re.compile(r"^\s*(\d+)\s+(?![O0o]\s*:)")


def section(printed):
    return next((name for lo,hi,name in SECTIONS if lo<=printed<=hi), None)


def date_interval(raw):
    """Conservative explicit interval only; never infer dates from book scope."""
    t = re.sub(r"\s+", " ", raw.replace("—","-").replace("–","-")).strip()
    t = re.sub(r"Pre-\s+", "Pre-", t, flags=re.I)
    t = re.sub(r"Post-\s+", "Post-", t, flags=re.I)
    t = re.sub(r"B\s*C\s*E", "BCE", t)
    t = re.sub(r"(?<!B)C\s*E", "CE", t)
    unknown = {"lower":None,"upper":None,"lower_inclusive":None,
               "upper_inclusive":None,"status":"unresolved","raw":raw}
    def result(lo,hi,li=True,ui=True,status="explicit_ocr_unvalidated"):
        return dict(unknown,lower=lo,upper=hi,lower_inclusive=li,
                    upper_inclusive=ui,status=status)
    def year(n,era): return -int(n) if era=="BCE" else int(n)
    m = re.fullmatch(r"(Pre|Post)-(\d+) (BCE|CE)",t,re.I)
    if m:
        y=year(m[2],m[3].upper())
        return result(None,y,None,False,"open_bound_ocr_unvalidated") if m[1].lower()=="pre" else result(y,None,False,None,"open_bound_ocr_unvalidated")
    m = re.fullmatch(r"(\d+)\s*(?:st|nd|rd|th) C (BCE|CE)",t,re.I)
    if m:
        c=int(m[1]);era=m[2].upper()
        return result(-100*c,-100*(c-1)-1) if era=="BCE" else result(100*(c-1)+1,100*c)
    m = re.fullmatch(r"(\d+)s (BCE|CE)",t,re.I)
    if m:
        n=int(m[1]);return result(-n-9,-n) if m[2].upper()=="BCE" else result(n,n+9)
    m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))? (BCE|CE)",t,re.I)
    if m:
        ys=[year(m[1],m[3].upper()),year(m[2] or m[1],m[3].upper())]
        if 0 in ys:return unknown
        return result(min(ys),max(ys))
    m = re.fullmatch(r"(\d+) (BCE|CE)\s*-\s*(\d+) (BCE|CE)",t,re.I)
    if m:
        ys=[year(m[1],m[2].upper()),year(m[3],m[4].upper())]
        return result(min(ys),max(ys))
    return unknown


def split_fields(text):
    matches=list(FIELDS.finditer(text));out={}
    for i,m in enumerate(matches):
        key=re.sub(r"\s+","",m[1]).lower()
        key={"0":"o","()":"o"}.get(key,key)
        value=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
        if key in out:
            return out,["duplicate_field_label"]
        out[key]=value
    return out,(["missing_field_"+k for k in ("o","ds","f","s","e","d") if k not in out])


def page_lines(page, viewer):
    """Two columns, suppress superscript footnote spans but preserve raw spans.

    Merge OCR lines that are the same visual baseline; headings are frequently
    split into original-script and English segments. Ordinary reading order
    cannot be obtained by globally sorting by y across both columns.
    """
    data=page.get_text("dict",flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)
    all_spans=[s for b in data["blocks"] for l in b.get("lines",[]) for s in l["spans"]]
    sizes=[s["size"] for s in all_spans if len(s["text"].strip())>2]
    body=statistics.median(sizes) if sizes else 8
    lines=[]
    for b in data["blocks"]:
        for line in b.get("lines",[]):
            x0,y0,x1,y1=line["bbox"]
            if y0<65 or y0>page.rect.height-24:
                continue
            spans=line["spans"]
            text="".join(s["text"] for s in spans if s["size"]>=body*.75)
            if not text.strip():continue
            lines.append({"viewer":viewer,"printed":viewer-27,
                "column":"left" if x0<page.rect.width/2 else "right",
                "bbox":[x0,y0,x1,y1],"text":text.strip(),
                "raw_text":"".join(s["text"] for s in spans),
                "bold_italic":any("BoldItal" in s["font"] for s in spans),
                "ends_italic":"Ital" in next((s["font"] for s in reversed(spans) if s["text"].strip()),""),
                "superscripts":[s["text"] for s in spans if s["size"]<body*.75]})
    ordered=[]
    for column in ("left","right"):
        group=sorted((l for l in lines if l["column"]==column),key=lambda l:(l["bbox"][1],l["bbox"][0]))
        for line in group:
            if ordered and ordered[-1]["column"]==column and abs(ordered[-1]["bbox"][1]-line["bbox"][1])<2:
                old=ordered[-1]
                pairs=sorted([(old["bbox"][0],old),(line["bbox"][0],line)],key=lambda p:p[0])
                old["text"]=" ".join(p[1]["text"] for p in pairs)
                old["raw_text"]=" ".join(p[1]["raw_text"] for p in pairs)
                old["bold_italic"]|=line["bold_italic"]
                old["ends_italic"]=pairs[-1][1]["ends_italic"]
                old["superscripts"]+=line["superscripts"]
                old["bbox"]=[min(old["bbox"][0],line["bbox"][0]),min(old["bbox"][1],line["bbox"][1]),max(old["bbox"][2],line["bbox"][2]),max(old["bbox"][3],line["bbox"][3])]
            else:ordered.append(line)
    return ordered


def is_heading(line):
    text=line["text"]
    return (line["ends_italic"] and not START.match(text) and not FOOTNOTE.match(text)
        and len(text)<100 and ":" not in text
        and bool(re.search(r"[-–]\s*[A-Z][a-z][A-Za-z'’ -]*$",text)))


def finalize(record):
    text=" ".join(l["text"] for l in record["lines"])
    fields,flags=split_fields(text)
    record.update(raw_text=text,fields_raw=fields,parser_flags=flags,
        greek_form=None,greek_form_status="requires_image_or_greek_ocr_validation",
        date_interval=date_interval(fields.get("d","")),region=None,
        geographic_status="requires_independent_source_localization_audit",
        source_raw=fields.get("s"),find_raw=fields.get("f"),
        description_raw=fields.get("ds"),exceptions_raw=fields.get("e"),
        date_kind="lexicon_D_person_or_event_context_unresolved",
        actual_greek_attestation_date_verified=False,
        eligible_primary=None,eligible_sensitivity=None)
    o_lines=[]
    for line in record["lines"]:
        o_lines.append({k:line[k] for k in ("viewer","printed","column","bbox")})
        if re.search(r"D\s*s\s*:",line["text"],re.I):break
    record["orthography_line_bboxes"]=o_lines
    record["orthography_bbox_scope"]="whole O-bearing line(s), includes adjacent labels; inspect source pixels"
    record["superscript_reference_candidates"]=[s for l in record["lines"] for s in l["superscripts"]]
    if not record.get("entry_id"):flags.append("heading_unresolved")
    flags.append("entry_heading_association_requires_visual_validation")
    if re.search(r"(?:\(\)|0)\s*:",record["lines"][0]["text"]):
        flags.append("ocr_O_label_recovered_from_zero_or_parentheses")
    if any(c in fields.get("o","") for c in "[]{}?"):flags.append("orthography_uncertain_or_restored_markers")
    if re.search(r"3\s*Q\s*15",text,re.I):flags.append("target_derived_source_requires_exclusion")
    if re.search(r"fictitious|doubtful|not a|place|family|nickname|non.?jew",fields.get("e",""),re.I):
        flags.append("source_exception_requires_review")
    if fields.get("o","").strip() in ("—","-",""):
        flags.append("no_distinct_orthography_field_do_not_substitute_headword")
    return record


def parse_document(doc):
    entries=[];records=[];footnotes=[];orphans=[];entry=None;current=None
    def finish():
        nonlocal current
        if current:records.append(finalize(current));current=None
    for viewer in range(86,min(len(doc),481)+1):
        printed=viewer-27; sec=section(printed)
        for line in page_lines(doc[viewer-1],viewer):
            text=line["text"]
            if text.startswith("O: Orthography") or text.startswith("S: Source"):continue
            if is_heading(line):
                finish()
                label=re.split(r"[-–]\s*",text,maxsplit=1)[-1].strip()
                ident=f"ilan2002:{sec}:v{viewer}:{line['column']}:y{round(line['bbox'][1],1)}"
                entry={"entry_id":ident,"section":sec,"heading_raw":text,
                       "english_label_raw":label,"heading_greek_form":None,
                       "heading_status":"raw_hidden_OCR_not_attested_orthography",
                       "locator":line}
                entries.append(entry);continue
            start=START.match(text)
            if start:
                finish()
                number=start[1].replace("I","1").replace("l","1")
                current={"record_id":f"v{viewer}:{line['column']}:y{round(line['bbox'][1],1)}:n{number}",
                    "entry_id":entry["entry_id"] if entry else None,"section":sec,
                    "attestation_number_raw":start[1],"attestation_number":int(number),
                    "lines":[line],"heading_raw":entry["heading_raw"] if entry else None}
                continue
            if FOOTNOTE.match(text):
                finish();footnotes.append({"entry_id":entry["entry_id"] if entry else None,**line});continue
            if current:
                current["lines"].append(line)
            else:
                # Preserve note continuation and unresolved starts; silently
                # dropping them would conceal OCR-driven extraction omissions.
                orphans.append({"entry_id":entry["entry_id"] if entry else None,**line})
    finish()
    return entries,records,footnotes,orphans


def main():
    p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--out",type=Path,required=True)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    doc=fitz.open(args.source);entries,records,notes,orphans=parse_document(doc)
    for name,rows in (("entries_raw",entries),("attestations_raw",records),("footnote_starts_raw",notes),("unassigned_lines_raw",orphans)):
        with (args.out/(name+".jsonl")).open("w",encoding="utf-8") as f:
            for row in rows:f.write(json.dumps(row,ensure_ascii=False)+"\n")
    audit={"source_sha256":sha256(args.source.read_bytes()).hexdigest(),"source_pages":len(doc),
        "scope":"printed59–454/viewer86–481; main corpus, appendix and addendum; no index used as attestations",
        "entry_heading_candidates":len(entries),"attestation_candidates":len(records),
        "attestations_by_section":dict(Counter(r['section'] for r in records)),
        "parser_flags":dict(Counter(flag for r in records for flag in r['parser_flags'])),
        "footnote_start_lines":len(notes),"unassigned_lines":len(orphans),
        "valid_greek_forms":0,"eligible_primary":None,"eligible_sensitivity":None,
        "status":"raw_hidden_OCR_extraction_only_not_a_scoring_corpus",
        "exposure":"Whole-corpus source-neutral extraction; no target-prefix query, matching or scoring."}
    (args.out/"extraction_audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(audit,ensure_ascii=False,indent=2))


if __name__=="__main__":main()
