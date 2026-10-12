"""Join authored audit judgments to the pinned source and inventory evidence."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = HERE.parent
ROOT = FULL.parents[2]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def digest_row(row):
    return hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def viewer(row):
    return int(row.get("pdf_page") or row.get("viewer_page"))


def build():
    data = json.loads((HERE / "audit.json").read_text())
    source_ids = sorted({r["source"] for a in data["rows"] for r in a["refs"]})
    files = []
    sources = {}
    for source in source_ids:
        folder = FULL / source
        manifest = json.loads((folder / "source_manifest.json").read_text())
        observations = read_csv(folder / "observations.csv")
        obs_index = {r.get("observation_id") or r.get("id"): r for r in observations}
        coverage = {viewer(r): r for r in read_csv(folder / "page_coverage.csv")}
        figures = {r.get("figure_id") or r.get("locator"): r for r in read_csv(folder / "figures_access.csv")}
        sources[source] = (manifest, obs_index, coverage, figures)
        files.extend(folder / f for f in ("observations.csv", "page_coverage.csv", "figures_access.csv", "source_manifest.json"))
    for audit in data["rows"]:
        for ref in audit["refs"]:
            manifest, obs, coverage, figures = sources[ref["source"]]
            evidence = obs[ref["observation_id"]]
            ref["observation_file"] = str((FULL / ref["source"] / "observations.csv").relative_to(ROOT))
            ref["printed_locator"] = evidence.get("printed_pages") or evidence.get("printed_page") or evidence.get("printed_label")
            ref["source_pdf_sha256"] = manifest.get("sha256") or manifest["source_sha256"]
            ref["source_url"] = manifest.get("source_url") or manifest.get("stable_url") or manifest["stable_source_url"]
            ref["observation_row_sha256"] = digest_row(evidence)
            ref["observation_row"] = evidence
            ref["coverage_rows"] = [coverage[p] for p in ref["viewer_pages"]]
            ref["figure_access_rows"] = [figures[f] for f in ref["figure_ids"]]
            ref["figure_coverage_rows"] = [coverage[viewer(figures[f])] for f in ref["figure_ids"]]
        for link in audit["inventory_links"]:
            path = ROOT / link["file"]
            files.append(path)
            if path.suffix == ".csv":
                row = next(r for r in read_csv(path) if r[link["id_field"]] == link["id"])
                link["baseline_row"] = row
                link["baseline_row_sha256"] = digest_row(row)
    (HERE / "audit.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    fields = ["audit_id", "feature", "role", "entries", "observed", "construction", "use", "fill", "alteration", "function_status", "relationship", "consequence", "next_observation", "audit_disposition", "phase_eligibility", "exposure", "confirmatory_support", "refs", "inventory_links"]
    with (HERE / "audit.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in data["rows"]:
            w.writerow({k: json.dumps(row[k], ensure_ascii=False, separators=(",", ":")) if isinstance(row[k], (list, bool)) else row[k] for k in fields})
    files.extend(ROOT / p for p in ("AGENTS.md", "research/ACTIVE_TEST.md", "research/regional/caves_entry25/README.md", "research/regional/tombs/README.md", "research/regional/water_systems/README.md"))
    pinned = {"baseline_commit": data["baseline_commit"], "files": [{"path": str(p.relative_to(ROOT)), "bytes": len(p.read_bytes()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "validation_mode": "context_only" if p.suffix == ".md" else "content_pin"} for p in sorted(set(files))]}
    (HERE / "input_manifest.json").write_text(json.dumps(pinned, ensure_ascii=False, indent=2) + "\n")
    return data


if __name__ == "__main__":
    build()
