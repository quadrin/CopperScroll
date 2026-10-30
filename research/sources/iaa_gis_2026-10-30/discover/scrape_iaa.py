#!/usr/bin/env python3
"""Scrape cave-related survey records from the IAA National Archaeological Database.

The public SPA at https://discover.iaa.org.il is backed by a plain JSON API.
Two endpoints matter here:

    GET /api/surveys                 -> all 3,709 survey stubs
    GET /api/api/SurveyPage/<id>     -> full survey record (note the doubled /api)

The second path is doubled because the frontend's backend base URL already
includes "/api". Full records include permit numbers, excavator/institution
groups and the survey polygon as WKT.

Guest access is enough for most records. A handful return HTTP 403
("You do not have permission to view this survey."); those are recorded with
their status rather than silently dropped.

Outputs (in data/):
    surveys.json          combined dataset, each record flagged judean_desert/cave
    survey_licenses.csv   one row per survey permit
    manifest.json         run metadata and per-record fetch status
"""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://discover.iaa.org.il"
OUT = Path(__file__).resolve().parent / "data"
UA = "Mozilla/5.0 (compatible; CopperScroll research intake)"  # repository copy: honest user agent (Drive copy differs)

CAVE_RE = re.compile(r"מער(?:ה|ות|ת)(?![א-ת])|\bcaves?\b", re.IGNORECASE)
JUDEAN_RE = re.compile(r"מדבר\s*יהודה|judean\s+desert|judea\s+desert|midbar\s+yehuda", re.IGNORECASE)


def get(path: str, timeout: int = 60) -> tuple[int, bytes]:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def name_blob(survey: dict) -> str:
    name = survey.get("surveyName") or {}
    return f"{name.get('hebrew', '')} {name.get('english', '')}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    status, body = get("/api/surveys")
    if status != 200:
        raise SystemExit(f"/api/surveys returned {status}")
    surveys = json.loads(body)["surveys"]

    candidates = []
    for survey in surveys:
        blob = name_blob(survey)
        is_cave = bool(CAVE_RE.search(blob))
        is_judean = bool(JUDEAN_RE.search(blob))
        if is_cave or is_judean:
            candidates.append({**survey, "_cave": is_cave, "_judean": is_judean})

    candidates.sort(key=lambda s: s["entitySurveyId"])
    print(f"{len(surveys)} surveys, {len(candidates)} cave/Judean Desert candidates")

    records, manifest = [], []
    for i, survey in enumerate(candidates, 1):
        sid = survey["entitySurveyId"]
        code, payload = get(f"/api/api/SurveyPage/{sid}")
        detail = None
        if code == 200:
            try:
                detail = json.loads(payload)
            except json.JSONDecodeError:
                code = -1
        manifest.append(
            {
                "entitySurveyId": sid,
                "surveyId": survey.get("surveyId"),
                "name_en": survey["surveyName"].get("english"),
                "http_status": code,
            }
        )
        records.append(
            {
                "entitySurveyId": sid,
                "surveyId": survey.get("surveyId"),
                "name_he": survey["surveyName"].get("hebrew"),
                "name_en": survey["surveyName"].get("english"),
                "is_cave": survey["_cave"],
                "is_judean_desert": survey["_judean"],
                "licenseIds": survey.get("licenseIds", []),
                "detail": detail,
            }
        )
        print(f"  [{i}/{len(candidates)}] {sid} {code} {survey['surveyName'].get('english')}")
        time.sleep(0.25)

    (OUT / "surveys.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (OUT / "survey_licenses.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "entity_survey_id",
                "survey_id",
                "name_en",
                "name_he",
                "is_cave",
                "is_judean_desert",
                "license_id",
                "license_short_name",
                "license_long_name",
                "years",
                "responsible_person_en",
                "survey_type",
                "survey_subtype",
                "institutions",
                "excavators",
            ]
        )
        for rec in records:
            detail = rec["detail"] or {}
            licenses = detail.get("licenses") or []
            base = [
                rec["entitySurveyId"],
                rec["surveyId"],
                rec["name_en"],
                rec["name_he"],
                rec["is_cave"],
                rec["is_judean_desert"],
            ]
            tail = [
                detail.get("years"),
                (detail.get("responsiblePerson") or {}).get("nameEnglish"),
                detail.get("surveyTypeName"),
                detail.get("surveySubtypeName"),
            ]
            if not licenses:
                writer.writerow(base + ["", "", "", *tail, "", ""])
                continue
            for lic in licenses:
                groups = lic.get("excavatorGroups") or []
                institutions = sorted(
                    {g.get("institutionEnglish") for g in groups if g.get("institutionEnglish")}
                )
                excavators = sorted(
                    {
                        p.get("nameEnglish")
                        for g in groups
                        for p in (g.get("excavators") or [])
                        if p.get("nameEnglish")
                    }
                )
                writer.writerow(
                    base
                    + [
                        lic.get("licenseId"),
                        lic.get("licenseShortName"),
                        lic.get("licenseLongName"),
                    ]
                    + tail
                    + ["; ".join(institutions), "; ".join(excavators)]
                )

    manifest_doc = {
        "source": BASE,
        "scraped_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_surveys": len(surveys),
        "candidates": len(candidates),
        "fetched_ok": sum(1 for m in manifest if m["http_status"] == 200),
        "forbidden": sum(1 for m in manifest if m["http_status"] == 403),
        "records": manifest,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest_doc, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
