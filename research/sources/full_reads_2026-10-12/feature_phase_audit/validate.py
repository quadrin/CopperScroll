"""Validate source identity, phase separation, exposure, joins and output agreement."""
import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def row_digest(row):
    return hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def pages(text):
    out = set()
    for a, b in re.findall(r"(\d+)(?:\s*[–-]\s*(\d+))?", text):
        out.update(range(int(a), int(b or a) + 1))
    return out


def validate():
    data = json.loads((HERE / "audit.json").read_text())
    manifest = json.loads((HERE / "input_manifest.json").read_text())
    assert data["baseline_commit"] == manifest["baseline_commit"]
    for pin in manifest["files"]:
        if pin.get("validation_mode") == "context_only":
            continue  # Context files may gain integrator links; the pin records the inspected baseline.
        content = (ROOT / pin["path"]).read_bytes()
        assert len(content) == pin["bytes"], pin["path"]
        assert hashlib.sha256(content).hexdigest() == pin["sha256"], pin["path"]
    records = data["rows"]
    assert 15 <= len(records) <= 25
    assert len({r["audit_id"] for r in records}) == len(records)
    sources = set()
    for record in records:
        assert record["exposure"].startswith("exploratory")
        assert record["confirmatory_support"] is False
        for field in ("construction", "use", "fill", "alteration", "relationship", "consequence", "next_observation"):
            assert isinstance(record[field], str) and record[field].strip(), (record["audit_id"], field)
        for ref in record["refs"]:
            sources.add(ref["source"])
            source_path = ROOT / ref["observation_file"]
            source_row = next(r for r in rows(source_path) if (r.get("observation_id") or r.get("id")) == ref["observation_id"])
            assert source_row == ref["observation_row"], ref["observation_id"]
            assert row_digest(source_row) == ref["observation_row_sha256"]
            page_spec = source_row.get("pdf_pages") or source_row.get("pdf_page") or source_row.get("viewer_page")
            assert set(ref["viewer_pages"]).issubset(pages(page_spec)), ref["observation_id"]
            for coverage in ref["coverage_rows"] + ref["figure_coverage_rows"]:
                assert coverage["status"] in {"read", "reviewed", "complete", "read_visual"}, (ref["source"], coverage)
            assert len(ref["figure_ids"]) == len(ref["figure_access_rows"])
            for fig in ref["figure_access_rows"]:
                assert (fig.get("figure_id") or fig.get("locator")) in ref["figure_ids"]
                fig_page = int(fig.get("pdf_page") or fig.get("viewer_page"))
                assert not (ref["source"] == "dalman_institute" and fig_page == 116)
            assert not (ref["source"] == "dalman_institute" and 116 in ref["viewer_pages"])
        for link in record["inventory_links"]:
            path = ROOT / link["file"]
            if path.suffix == ".csv":
                linked = next(r for r in rows(path) if r[link["id_field"]] == link["id"])
                assert linked == link["baseline_row"]
                assert row_digest(linked) == link["baseline_row_sha256"]
            else:
                assert link["id"] in path.read_text(), link["id"]
    assert sources == {"benjamin1993", "highlands1997", "kloner_zissu2003", "hirschfeld1992", "finkelstein1988", "dalman_institute", "netzer1981"}
    csv_rows = rows(HERE / "audit.csv")
    assert len(csv_rows) == len(records)
    for csv_row, record in zip(csv_rows, records):
        for key, value in csv_row.items():
            expected = json.dumps(record[key], ensure_ascii=False, separators=(",", ":")) if isinstance(record[key], (list, bool)) else record[key]
            assert value == expected, (record["audit_id"], key)
    # Domain checks prevent construction-date inheritance and proxy substitution in key applied joins.
    by_id = {r["audit_id"]: r for r in records}
    assert by_id["FP05"]["construction"].startswith("Unknown")
    assert by_id["FP05"]["inventory_links"][0]["baseline_row"]["date_code"] == "undated"
    assert by_id["FP20"]["inventory_links"][0]["baseline_row"]["date_code"] == "in"
    assert by_id["FP20"]["construction"].startswith("Independent absolute date unavailable")
    assert "not discovered" in by_id["FP20"]["observed"]
    assert "original access south" in by_id["FP17"]["observed"]
    assert "later breach west" in by_id["FP17"]["observed"]
    assert "Later/modern stairs" in by_id["FP07"]["alteration"]
    assert "shared reports as dependent" in by_id["FP07"]["consequence"]
    assert "Lining dates" in by_id["FP14"]["relationship"]
    assert "separate grave" in by_id["FP06"]["relationship"]
    return {"result": "pass", "scope": "Input hashes; exact observation, source page and figure joins; missing/reserved page exclusions; inventory identity; CSV/JSON agreement; phase-transfer and access-proxy regressions. This validates provenance and data discipline, not the archaeological truth of every source interpretation."}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, ensure_ascii=False))
