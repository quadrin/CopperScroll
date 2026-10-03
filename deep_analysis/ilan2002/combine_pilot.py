"""Merge the fixed pilot's explicit visual validations. NO prefix matching.

The scoring-compatible name_id denotes a normalized orthographic FORM, not a
lexical lemma, a person or a source occurrence. Occurrences are separate rows.
"""
import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata

ALPHABET="ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
UNCERTAIN_FLAGS=re.compile(r"unknown|uncertain|doubt|restor|fragment|ambig|target.?derived|3q15|unverified",re.I)


def normalize(raw):
    text=unicodedata.normalize("NFD",raw.strip())
    if "\u0345" in text:raise ValueError("iota subscript rejected by fixed policy")
    out=[]
    for c in text:
        if unicodedata.category(c).startswith("M"):continue
        c={"ϲ":"Σ","Ϲ":"Σ","ς":"Σ","σ":"Σ"}.get(c,c)
        out.append(c.upper())
    form="".join(out)
    if not form or any(c not in ALPHABET for c in form):
        raise ValueError("not one complete Greek token in the frozen alphabet")
    return form


def form_id(form):
    return "ilan2002:reported_greek_form:"+sha256(form.encode("utf-8")).hexdigest()


def index_unique(rows,label):
    result={}
    for row in rows:
        key=row.get("record_id")
        if not key:raise ValueError(label+": missing record_id")
        if key in result:raise ValueError(label+": duplicate record_id "+key)
        result[key]=row
    return result


def combine(pilot,raw,validated,expected_count=198):
    selected=index_unique(pilot,"pilot");metadata=index_unique(raw,"raw")
    validations=index_unique(validated,"validation")
    if len(selected)!=expected_count:
        raise ValueError(f"fixed pilot count must be {expected_count}, got {len(selected)}")
    if set(validations)!=set(selected):
        raise ValueError("validation coverage mismatch: missing="+
            str(sorted(set(selected)-set(validations)))+" extra="+
            str(sorted(set(validations)-set(selected))))
    if not set(selected).issubset(metadata):
        raise ValueError("fixed pilot contains IDs absent from raw metadata")
    decisions=[];occurrences=[]
    for key,p in selected.items():
        r=metadata[key];v=validations[key];status=v.get("status")
        if status not in {"accepted","excluded","unknown"}:
            raise ValueError(key+": explicit accepted/excluded/unknown status required")
        reason=v.get("reason","");flags=v.get("flags",[])
        if not isinstance(flags,list):raise ValueError(key+": flags must be a list")
        effective=status;gates=[]
        source_raw=r.get("fields_raw",{}).get("s",p.get("s_raw",""))
        if re.search(r"3\s*Q\s*15",source_raw,re.I) or "target_derived_source_requires_exclusion" in r.get("parser_flags",[]):
            effective="excluded";gates.append("target_derived_source")
        if v.get("source_independent") is not True:
            effective="unknown" if effective!="excluded" else effective
            gates.append("source_independence_not_verified")
        if any(UNCERTAIN_FLAGS.search(str(f)) for f in flags):
            effective="unknown" if effective!="excluded" else effective
            gates.append("unresolved_validation_flags")
        if status=="accepted" and v.get("image_checked") is not True:
            effective="unknown" if effective!="excluded" else effective
            gates.append("source_image_not_verified")
        if v.get("source_page") is not None and int(v["source_page"])!=int(p["printed"]):
            raise ValueError(key+": validation printed page differs from selected row")
        forms=v.get("greek_forms",[])
        if not isinstance(forms,list) or any(not isinstance(f,str) for f in forms):
            raise ValueError(key+": greek_forms must be a list of strings")
        if effective=="accepted" and not forms:
            raise ValueError(key+": accepted row has no attested Greek forms")
        cleaned=[]
        if effective=="accepted":
            for source_form in forms:
                try:normalized=normalize(source_form)
                except ValueError as exc:
                    effective="unknown";gates.append("normalization_rejected: "+str(exc));break
                cleaned.append((source_form,normalized))
        decision={"record_id":key,"validator_status":status,"effective_status":effective,
            "reason":reason,"flags":flags,"gates":gates,"validation":v}
        decisions.append(decision)
        if effective!="accepted":continue
        seen=set()
        for source_form,normalized in cleaned:
            if normalized in seen:continue
            seen.add(normalized)
            fid=form_id(normalized)
            fields=r.get("fields_raw",{})
            occurrences.append({"occurrence_id":key+":"+fid.rsplit(":",1)[-1],
                "record_id":key,"name_id":fid,"id_unit":"normalized_orthographic_form",
                "greek_form":normalized,"source_form":source_form,
                "printed":p["printed"],"viewer":p["viewer"],"column":p["column"],
                "orthography_bboxes":p.get("orthography_bboxes",json.dumps(r.get("orthography_line_bboxes",[]))),
                "source_ref":fields.get("s",p.get("s_raw","")),
                "description_raw":fields.get("ds",p.get("ds_raw","")),
                "find_raw":fields.get("f",p.get("f_raw","")),
                "exceptions_raw":fields.get("e",p.get("e_raw","")),
                "book_D_raw":p.get("d_raw",fields.get("d","")),
                "book_D_lower":p.get("D_lower"),"book_D_upper":p.get("D_upper"),
                "date_kind":"reported_person_or_event_period_pilot",
                "actual_attestation_primary_eligible":"unresolved_not_this_pilot",
                "source_independent":True,"image_checked":True,
                "validation_reason":reason,"validation_flags":json.dumps(flags,ensure_ascii=False),
                "parser_heading_id_unvalidated":r.get("entry_id"),
                "heading_used_for_form_identity":False})
    groups=defaultdict(list)
    for row in occurrences:groups[row["name_id"]].append(row)
    forms=[{"name_id":fid,"greek_form":rows[0]["greek_form"],
        "id_unit":"normalized_orthographic_form","occurrence_count":len(rows),
        "record_ids":json.dumps(sorted({r["record_id"] for r in rows})),
        "source_forms":json.dumps(sorted({r["source_form"] for r in rows}),ensure_ascii=False)}
        for fid,rows in sorted(groups.items())]
    audit={"fixed_pilot_records":len(selected),"validation_records":len(validations),
        "all_selected_records_have_explicit_validation":True,
        "validator_status_counts":dict(Counter(d["validator_status"] for d in decisions)),
        "effective_status_counts":dict(Counter(d["effective_status"] for d in decisions)),
        "accepted_form_occurrences":len(occurrences),"unique_normalized_forms":len(forms),
        "name_id_semantics":"normalized orthographic form; NOT unique onomastic lemma or bearer",
        "date_claim":"New exploratory reported-person-period pilot; original actual-attestation branch not replaced",
        "population_limit":"Fixed source-audited pilot, NOT complete eligible Ilan corpus",
        "target_prefix_queries_or_scores":0,"freeze_status":"not_frozen_by_this_helper"}
    return forms,occurrences,decisions,audit


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_csv(path,rows,fallback):
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]) if rows else fallback, lineterminator="\n")
        writer.writeheader();writer.writerows(rows)


def main():
    p=argparse.ArgumentParser();p.add_argument("--pilot",type=Path,required=True)
    p.add_argument("--raw",type=Path,required=True);p.add_argument("--validated",type=Path,nargs="+",required=True)
    p.add_argument("--out",type=Path,required=True);args=p.parse_args()
    pilot=json.loads(args.pilot.read_text());raw=read_jsonl(args.raw)
    validated=[dict(r,validator_input=str(path)) for path in args.validated for r in read_jsonl(path)]
    forms,occurrences,decisions,audit=combine(pilot,raw,validated)
    # Only write after every selected status and schema/ID gate succeeds.
    args.out.mkdir(parents=True,exist_ok=True)
    write_csv(args.out/"pilot_forms.csv",forms,["name_id","greek_form","id_unit"])
    write_csv(args.out/"pilot_form_occurrences.csv",occurrences,["record_id","name_id","greek_form"])
    (args.out/"pilot_validation_decisions.json").write_text(json.dumps(decisions,ensure_ascii=False,indent=2))
    audit["inputs"]=[{"path":str(path),"sha256":sha256(path.read_bytes()).hexdigest()}
        for path in [args.pilot,args.raw,*args.validated]]
    audit["outputs"]=[{"path":str(args.out/name),"sha256":sha256((args.out/name).read_bytes()).hexdigest()}
        for name in ["pilot_forms.csv","pilot_form_occurrences.csv","pilot_validation_decisions.json"]]
    (args.out/"pilot_merge_audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print(json.dumps(audit,ensure_ascii=False,indent=2))


if __name__=="__main__":main()
