"""Review queues from unvalidated extraction; no target-prefix operations."""
import csv
import json
from pathlib import Path
import re

folder=Path(__file__).parent/"final-raw"
rows=[json.loads(line) for line in (folder/"attestations_raw.jsonl").read_text().splitlines()]
orphans=[json.loads(line) for line in (folder/"unassigned_lines_raw.jsonl").read_text().splitlines()]
possible=[]
for row in orphans:
    text=row["text"]
    if re.match(r"^\s*[\dIl]+\s*[.)]\s*[^:;]{0,8}[:;]",text) or re.match(r"^\s*[\dIl]+\s+[O0oΟQ]\s*[:;]",text):
        possible.append(dict(row,review_reason="possible_missing_or_corrupted_attestation_start"))
(folder/"possible_orphan_record_starts.json").write_text(json.dumps(possible,ensure_ascii=False,indent=2))
closed=[]
for row in rows:
    f=row["fields_raw"];d=row["date_interval"]
    unsafe=set(row["parser_flags"])-{"entry_heading_association_requires_visual_validation"}
    if d["lower"] is not None and d["upper"] is not None and f.get("e") in {"—","-","Second name"} and not unsafe:
        loc=row["lines"][0]
        closed.append({"record_id":row["record_id"],"entry_id":row["entry_id"],"heading_raw":row["heading_raw"],
            "section":row["section"],"viewer":loc["viewer"],"printed":loc["printed"],
            "column":loc["column"],"orthography_bboxes":json.dumps(row["orthography_line_bboxes"]),
            **{key+"_raw":f.get(key) for key in ("o","ds","f","s","e","d")},
            "D_lower":d["lower"],"D_upper":d["upper"],"date_kind":row["date_kind"],
            "actual_greek_attestation_date_verified":False,"eligible_primary":"unknown"})
with (folder/"closed_D_review_candidates.csv").open("w",newline="",encoding="utf-8") as stream:
    writer=csv.DictWriter(stream,fieldnames=list(closed[0]) if closed else ["record_id"])
    writer.writeheader();writer.writerows(closed)
audit={"possible_orphan_record_starts":len(possible),"closed_D_review_candidates":len(closed),
    "status":"review_candidates_only_not_eligible_names_or_complete_corpus",
    "date_limit":"Lexicon D is person/event/context; an actual Greek attestation date requires source-specific audit.",
    "prefix_queries_or_scores":0}
(folder/"review_queue_audit.json").write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2))
