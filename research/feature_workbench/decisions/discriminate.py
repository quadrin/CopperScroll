"""Find the smallest sets of queued records that separate the surviving models.

Planning only. A model survives an outcome unless a recorded or derived
consequence of that outcome contradicts one of its required predicates. The
search is exact over the seven record dependencies. It computes no probability,
likelihood, prior, expected value or information gain. Effort and access are the
categories recorded in plans.json; they are listed, never weighted or summed.

A task can carry a recorded outcome (plans.json ``recorded_outcome``): an outcome
row that an obtained record actually showed. Classes are formed before recorded
outcomes are applied, so class names stay the names used when the rows were
planned and registered. The classes that a recorded row excludes then leave the
search. Current evidence and the recorded row must agree on those classes.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable


MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_REPO = MODULE_DIR.parents[2]
SPEC_PATH = MODULE_DIR / "discrimination.json"
PLANS_PATH = MODULE_DIR / "plans.json"
ROW_KINDS = ("decisive", "partial", "not_obtained")
MEMBER_LIST_LIMIT = 24  # larger classes are described exactly by their composition
STATUS_OVERRIDES = {"compatible", "contradicted"}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_evaluator(repo_root: Path, name: str):
    """Load another module's evaluator read-only; its inputs are never written."""
    path = repo_root / "research/feature_workbench" / name / "evaluate.py"
    spec = importlib.util.spec_from_file_location(f"decisions_discriminate_{name}", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Generic logic. These functions take plain dictionaries so tests can use
# synthetic families with a known answer.
# ---------------------------------------------------------------------------

def collapse(model_ids: Iterable[str], survivors: dict[str, dict[str, frozenset]]) -> list[list[str]]:
    """Group models whose survival is identical on every outcome of every record.

    ``survivors[task][row]`` is the set of model IDs that survive that row.
    Classes are ordered by their smallest member ID, so input order is irrelevant.
    """
    ordered = sorted(model_ids)
    keys = [(task, row) for task in sorted(survivors) for row in sorted(survivors[task])]
    groups: dict[tuple, list[str]] = {}
    for model in ordered:
        signature = tuple(model in survivors[task][row] for task, row in keys)
        groups.setdefault(signature, []).append(model)
    return sorted(groups.values(), key=lambda members: members[0])


def predictions(classes: dict[str, list[str]], survivors: dict[str, dict[str, frozenset]]) -> dict[str, dict[str, frozenset]]:
    """P[class][task]: the outcomes of that record under which the class survives."""
    result = {}
    for class_id, members in classes.items():
        representative = members[0]
        result[class_id] = {
            task: frozenset(row for row, alive in rows.items() if representative in alive)
            for task, rows in survivors.items()
        }
    return result


def separated_pairs(class_ids: list[str], pred: dict, tasks: Iterable[str]) -> list[tuple[str, str]]:
    """Pairs that some outcome of some record in ``tasks`` separates (in principle)."""
    tasks = list(tasks)
    return [
        (a, b) for a, b in itertools.combinations(sorted(class_ids), 2)
        if any(pred[a][task] != pred[b][task] for task in tasks)
    ]


def guaranteed_pairs(class_ids: list[str], pred: dict, tasks: Iterable[str], allowed: dict[str, frozenset] | None = None) -> list[tuple[str, str]]:
    """Pairs separated whatever outcome each record returns (worst case).

    A pair is guaranteed only when some record has no permitted outcome that
    both classes survive. ``allowed`` restricts the outcomes considered, for
    example to decisive outcomes; ``None`` admits every outcome.
    """
    tasks = list(tasks)
    found = []
    for a, b in itertools.combinations(sorted(class_ids), 2):
        for task in tasks:
            shared = pred[a][task] & pred[b][task]
            if allowed is not None:
                shared &= allowed[task]
            if not shared:
                found.append((a, b))
                break
    return found


def blocks(class_ids: list[str], pred: dict, tasks: Iterable[str]) -> int:
    tasks = list(tasks)
    return len({tuple(pred[c][task] for task in tasks) for c in class_ids})


def minimal_sets(universe: Iterable[str], test: Callable[[tuple[str, ...]], bool]) -> list[tuple[str, ...]]:
    """Exact search: every smallest subset that passes ``test``; [] if none does."""
    items = sorted(universe)
    for size in range(len(items) + 1):
        hits = [combo for combo in itertools.combinations(items, size) if test(combo)]
        if hits:
            return hits
    return []


def reachable_survivor_sets(class_ids: list[str], row_survivors: dict[str, list[frozenset]], tasks: Iterable[str]) -> set[frozenset]:
    """All survivor sets some combination of outcomes can leave (best and worst cases)."""
    current = {frozenset(class_ids)}
    for task in tasks:
        options = set(row_survivors[task])
        current = {alive & option for alive in current for option in options}
    return current


# ---------------------------------------------------------------------------
# Model families
# ---------------------------------------------------------------------------

def _kohlit_models(snapshot: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Return surviving models, excluded-model summaries and the full excluded models.

    The full excluded models keep their checks, so a recorded outcome can be
    matched to the contradiction it caused.
    """
    results = {result["id"]: result for result in snapshot["results"]}
    models, excluded, excluded_full = [], [], []
    for branch in snapshot["data"]["branches"]:
        result = results[branch["result_id"]]
        checks = [
            {
                "predicate": check["value"]["predicate_id"],
                "subject": check["value"]["resolved_subject"],
                "object": check["value"]["resolved_object"],
                "required": check["value"]["required"],
                "status": check["status"],
                "observation_ids": list(check["value"].get("observation_ids", [])),
            }
            for check in result["checks"]
        ]
        model = {
            "id": branch["id"],
            "family": "kohlit",
            "kind": "relationships",
            "dims": {"assignment": branch["assignment_id"], "reading": branch["reading_id"], "window": branch["window_id"]},
            "status": result["status"],
            "checks": checks,
        }
        if result["status"] == "contradicted":
            excluded.append({
                "id": model["id"],
                "dims": model["dims"],
                "contradicted_predicates": sorted(c["predicate"] for c in checks if c["status"] == "contradicted"),
            })
            excluded_full.append(model)
        else:
            models.append(model)
    return models, excluded, excluded_full


def _entry25_models(snapshot: dict, query_id: str) -> tuple[list[dict], list[dict]]:
    query = next(item for item in snapshot["data"]["queries"] if item["id"] == query_id)
    choices = {branch["id"]: branch["choices"] for branch in query["branches"]}
    models, excluded = [], []
    for candidate in query["candidate_results"]:
        for outcome in candidate["branches"]:
            suffix = outcome["branch_id"][len(query_id) + 2:]
            model = {
                "id": f"entry25-{candidate['candidate_id']}--{suffix}",
                "family": "entry25",
                "kind": "inventory",
                "dims": {"candidate": candidate["candidate_id"], **choices[outcome["branch_id"]]},
                "status": outcome["status"],
                "checks": [{"check": check["id"], "required": True, "status": check["status"]} for check in outcome["checks"]],
            }
            if outcome["status"] == "contradicted":
                excluded.append({"id": model["id"], "dims": model["dims"], "contradicted_checks": sorted(c["check"] for c in model["checks"] if c["status"] == "contradicted")})
            else:
                models.append(model)
    return models, excluded


def _letter_models(spec: dict) -> list[dict]:
    return [
        {"id": string["id"], "family": "xii10", "kind": "letter_strings", "dims": {"string": f"{string['id']} {string['sequence']}"},
         "status": "unknown", "components": string["components"], "checks": []}
        for string in spec["letter_strings"]["strings"]
    ]


def _single_branch_model(family: dict) -> dict:
    return {"id": family["id"] + "-named-branch", "family": family["id"], "kind": "single_branch",
            "dims": {"branch": family["label"]}, "status": "unknown",
            "checks": [{"check": "named-branch", "required": True, "status": "unknown"}]}


def _effect_matches(effect: dict, model: dict, check: dict) -> bool:
    if effect["family"] != model["family"] or "status" not in effect:
        return False
    if model["kind"] == "relationships":
        if check["predicate"] != effect["predicate"] or check["subject"] != effect["subject"]:
            return False
        if "object" in effect and check["object"] != effect["object"]:
            return False
        if "windows" in effect and model["dims"]["window"] not in effect["windows"]:
            return False
        return "readings" not in effect or model["dims"]["reading"] in effect["readings"]
    if model["kind"] == "inventory":
        return (model["dims"]["candidate"] == effect["candidate"] and check["check"] == effect["check"]
                and all(model["dims"].get(key) == value for key, value in effect.get("where", {}).items()))
    return model["kind"] == "single_branch"


def survives(model: dict, effects: list[dict]) -> bool:
    """Conjunction semantics shared by the source modules: one contradiction fails a branch."""
    for effect in effects:
        if effect["family"] == model["family"] and effect.get("exclude_reading") == model["dims"].get("reading"):
            return False
    for check in model["checks"]:
        if not check["required"]:
            continue
        overrides = {effect["status"] for effect in effects if _effect_matches(effect, model, check)}
        status = "contradicted" if "contradicted" in overrides else "compatible" if "compatible" in overrides else check["status"]
        if status == "contradicted":
            return False
    return True


# ---------------------------------------------------------------------------
# Recorded outcomes
# ---------------------------------------------------------------------------

def _recorded_rows(tasks: dict, rows: dict[str, list[dict]]) -> dict[str, dict]:
    """The refined row that each task's recorded outcome names."""
    out = {}
    for task_id in sorted(tasks):
        record = tasks[task_id].get("recorded_outcome")
        if record is None:
            continue
        row = next((item for item in rows[task_id] if item["id"] == record["row_id"]), None)
        if row is None or row["plans_outcome_id"] != record["outcome_id"]:
            raise ValueError(f"Recorded outcome of {task_id} names no refined row of outcome {record['outcome_id']}")
        out[task_id] = {"task_id": task_id, "row": row, "record": record}
    return out


def _conjunction(statuses: list[str]) -> str:
    if "contradicted" in statuses:
        return "contradicted"
    if "mixed" in statuses:
        return "mixed"
    return "unknown" if not statuses or "unknown" in statuses else "compatible"


def _recorded_exclusions(families: dict[str, dict], recorded: dict[str, dict]) -> dict[str, list[dict]]:
    """Excluded models whose every contradiction comes from a recorded outcome.

    Each returned model has those checks set back to unknown, their state before
    the record. Classes are formed with these models, so recorded outcomes keep
    the planned class names. A model with any other contradiction stays outside.
    """
    effects = [(item["task_id"], effect) for item in recorded.values()
               for effect in item["row"]["effects"] if effect.get("status") == "contradicted"]
    observations = {item["task_id"]: set(item["record"].get("observation_ids", [])) for item in recorded.values()}
    out: dict[str, list[dict]] = {fid: [] for fid in families}
    for fid, family in families.items():
        for model in family.get("excluded_full", []):
            restored, by_tasks, explained = copy.deepcopy(model), set(), True
            for check in restored["checks"]:
                if not check["required"] or check["status"] != "contradicted":
                    continue
                cause = set(check.get("observation_ids", []))
                hits = {task_id for task_id, effect in effects
                        if _effect_matches(effect, model, check) and cause and cause <= observations[task_id]}
                if not hits:
                    explained = False
                    break
                check["status"] = "unknown"
                by_tasks |= hits
            if explained and by_tasks:
                restored["status"] = _conjunction([c["status"] for c in restored["checks"] if c["required"]])
                restored["recorded_by"] = sorted(by_tasks)
                out[fid].append(restored)
    return out


# ---------------------------------------------------------------------------
# Outcome rows
# ---------------------------------------------------------------------------

def _matches_when(when: dict, values: dict) -> bool:
    return all(values[key] in allowed for key, allowed in when.items())


def _component_rows(task: dict, observation: dict) -> list[dict]:
    components = observation["components"]
    rows = []
    for picked in itertools.product(*(component["values"] for component in components)):
        values = {component["id"]: value["id"] for component, value in zip(components, picked)}
        if any(_matches_when(rule, values) for rule in observation.get("inconsistent", [])):
            continue
        rule = next(rule for rule in observation["rules"] if _matches_when(rule["when"], values))
        derivations = [(f"{task['id']}#{component['id']}={value['id']}", value["derivation"])
                       for component, value in zip(components, picked) if value.get("derived")]
        if rule.get("derived"):
            derivations.append((f"{task['id']}#rule-{observation['rules'].index(rule) + 1}", rule["derivation"]))
        unresolved = any(value.get("unresolved") for value in picked)
        rows.append({
            "id": rule["plans_outcome_id"] + ":" + "+".join(values[c["id"]] for c in components),
            "plans_outcome_id": rule["plans_outcome_id"],
            "label": "; ".join(value["label"] for value in picked),
            "row_kind": "partial" if unresolved else "decisive",
            "basis": "derived" if derivations else "recorded",
            "derivations": derivations,
            "components": values,
            "effects": [effect for value in picked for effect in value["effects"]],
        })
    not_obtained = observation["not_obtained_outcome"]
    rows.append({
        "id": not_obtained["id"], "plans_outcome_id": not_obtained["plans_outcome_id"],
        "label": not_obtained["label"], "row_kind": "not_obtained", "basis": "recorded",
        "derivations": [], "components": None, "effects": [],
    })
    return rows


def _plans_rows(task: dict, observation: dict) -> list[dict]:
    rows = []
    for outcome in task["outcomes"]:
        row = observation["rows"][outcome["id"]]
        rows.append({
            "id": outcome["id"], "plans_outcome_id": outcome["id"], "label": outcome["label"],
            "row_kind": row["row_kind"], "basis": "recorded", "derivations": [],
            "components": None, "effects": row["effects"],
        })
    return rows


def _cubes(vectors: list[tuple], names: list[str]) -> list[str]:
    """Describe a set of component vectors exactly as a union of products.

    Each product is one string, for example ``box=ב; middle=ינ|unresolved``.
    """
    vector_set = set(vectors)
    values = [sorted({vector[i] for vector in vectors}, key=lambda value: (value == "unresolved", value)) for i in range(len(names))]
    if len(vector_set) == len(list(itertools.product(*values))):
        return ["; ".join(f"{name}={'|'.join(value)}" for name, value in zip(names, values))]
    split = next(i for i, options in enumerate(values) if len(options) > 1)
    cubes = []
    for option in values[split]:
        cubes.extend(_cubes([vector for vector in vectors if vector[split] == option], names))
    return cubes


def _letter_rows(spec: dict, observation: dict) -> list[dict]:
    letters = spec["letter_strings"]
    unresolved = letters["unresolved_value"]
    names = [component["id"] for component in letters["components"]]
    mapping = letters["plans_mapping"]
    groups: dict[tuple, dict] = {}
    for vector in itertools.product(*(component["values"] + [unresolved] for component in letters["components"])):
        values = dict(zip(names, vector))
        alive = tuple(s["id"] for s in letters["strings"] if all(values[n] in (unresolved, s["components"][n]) for n in names))
        decisive = unresolved not in vector
        plans_outcome = mapping["rejected_all"] if not alive else mapping["single_decisive"] if decisive and len(alive) == 1 else mapping["otherwise"]
        effects = []
        for dependency in letters["string_dependencies"]:
            if not set(dependency["requires_any_of"]) & set(alive):
                effects.append({"family": dependency["family"], "exclude_reading": dependency["reading"]})
        key = (plans_outcome, decisive, alive)
        group = groups.setdefault(key, {"vectors": [], "effects": effects})
        group["vectors"].append(vector)
    rows = []
    for (plans_outcome, decisive, alive), group in sorted(groups.items(), key=lambda item: (item[0][0], item[0][2], not item[0][1])):
        suffix = "+".join(alive) if alive else "none"
        open_suffix = "" if decisive or plans_outcome == mapping["otherwise"] else ":open-components"
        derivations = [(f"{observation['task_id']}#decomposition", letters["decomposition_note"])]
        for dependency in letters["string_dependencies"]:
            if any(effect.get("exclude_reading") == dependency["reading"] for effect in group["effects"]):
                derivations.append((f"{observation['task_id']}#requires-{dependency['reading']}", dependency["derivation"]))
        rows.append({
            "id": f"{plans_outcome}:{suffix}{open_suffix}",
            "plans_outcome_id": plans_outcome,
            "label": ("Surviving strings: " + ", ".join(alive)) if alive else "No registered string survives",
            "row_kind": "decisive" if decisive else "partial",
            "basis": "derived",
            "derivations": derivations,
            "components": {"vector_count": len(group["vectors"]), "cubes": _cubes(sorted(group["vectors"]), names)},
            "effects": group["effects"],
            "string_survivors": list(alive),
        })
    gate = observation["not_obtained_outcome"]
    rows.append({
        "id": gate["id"], "plans_outcome_id": gate["plans_outcome_id"], "label": gate["label"],
        "row_kind": "not_obtained", "basis": "recorded", "derivations": [], "components": None,
        "effects": [], "string_survivors": [s["id"] for s in letters["strings"]],
    })
    return rows


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(spec: dict, plans: dict, repo_root: Path, families: dict[str, dict], rows: dict[str, list[dict]],
             restored: dict[str, list[dict]] | None = None) -> None:
    # The planned roster: surviving models plus models excluded only by a recorded outcome.
    restored = restored or {}
    roster = {fid: family["models"] + restored.get(fid, []) for fid, family in families.items()}
    if spec.get("mode") != "planning_only":
        raise ValueError("Discrimination must be planning_only")
    plan_sources = {source["id"] for source in plans["sources"]}
    spec_sources = [source["id"] for source in spec["sources"]]
    if len(spec_sources) != len(set(spec_sources)) or set(spec_sources) & plan_sources:
        raise ValueError("Duplicate discrimination source ID")
    for source in spec["sources"]:
        if not source["id"].startswith("decisions-"):
            raise ValueError("Discrimination source ID must be module-prefixed")
        if not (repo_root / source["repo_path"]).is_file():
            raise ValueError(f"Missing source record: {source['repo_path']}")
        if source["inspection"] not in {"already_inspected", "not_inspected", "derived"}:
            raise ValueError("Unknown source inspection state")
    known_sources = plan_sources | set(spec_sources)
    for family in spec["families"]:
        if not set(family["source_ids"]) <= known_sources:
            raise ValueError(f"Unknown source in family {family['id']}")
    for item in spec["supplementary_observations"]:
        if not item["id"].startswith("decisions-") or not set(item["source_ids"]) <= known_sources or item["effects"]:
            raise ValueError("Supplementary observations are prefixed, sourced and outside the search")
    for dependency in spec["letter_strings"]["string_dependencies"]:
        if not set(dependency["source_ids"]) <= known_sources:
            raise ValueError("Unknown string-dependency source")

    tasks = {task["id"]: task for task in plans["tasks"]}
    observed = [observation["task_id"] for observation in spec["observations"]]
    if sorted(observed) != sorted(tasks) or len(observed) != len(set(observed)):
        raise ValueError("Every plans.json task needs exactly one discrimination observation")
    for task_id, task_rows in rows.items():
        plan_outcomes = {outcome["id"] for outcome in tasks[task_id]["outcomes"]}
        mapped = {row["plans_outcome_id"] for row in task_rows}
        if mapped != plan_outcomes:
            raise ValueError(f"Refined outcomes of {task_id} must map onto exactly its plans.json outcomes")
        row_ids = [row["id"] for row in task_rows]
        if len(row_ids) != len(set(row_ids)):
            raise ValueError(f"Duplicate outcome row in {task_id}")
        if not any(row["row_kind"] == "not_obtained" for row in task_rows):
            raise ValueError(f"{task_id} needs a not-obtained outcome")
        for row in task_rows:
            if row["row_kind"] not in ROW_KINDS or row["basis"] not in {"recorded", "derived"}:
                raise ValueError("Invalid outcome row kind or basis")
            if row["basis"] == "derived" and not row["derivations"]:
                raise ValueError("A derived outcome must state its derivation")
            for effect in row["effects"]:
                if effect["family"] not in families:
                    raise ValueError(f"Unknown effect family {effect['family']}")
                if "status" in effect and effect["status"] not in STATUS_OVERRIDES:
                    raise ValueError("An effect sets a check to compatible or contradicted only")

    strings = {string["id"] for string in spec["letter_strings"]["strings"]}
    for dependency in spec["letter_strings"]["string_dependencies"]:
        readings = {model["dims"].get("reading") for model in roster[dependency["family"]]}
        if dependency["reading"] not in readings or not set(dependency["requires_any_of"]) <= strings:
            raise ValueError(f"String dependency refers to an unknown reading or string: {dependency['reading']}")

    # Every declared effect must reach an existing check; stale references fail.
    for observation in spec["observations"]:
        declared = [effect for component in observation.get("components", []) for value in component["values"] for effect in value["effects"]]
        declared += [effect for row in observation.get("rows", {}).values() for effect in row["effects"]]
        for effect in declared:
            models = roster[effect["family"]]
            if not any(_effect_matches(effect, model, check) for model in models for check in model["checks"]):
                raise ValueError(f"Effect in {observation['task_id']} matches no model check: {effect}")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _class_label(members: list[dict], dimensions: list[str]) -> str:
    parts = []
    for dimension in dimensions:
        values = sorted({str(model["dims"][dimension]) for model in members})
        parts.append(f"{dimension}: {' / '.join(values)}")
    return "; ".join(parts)


def _varying(members: list[dict], dimensions: list[str]) -> dict[str, list[str]]:
    return {
        dimension: values for dimension in dimensions
        if len(values := sorted({str(model["dims"][dimension]) for model in members})) > 1
    }


def _profile(tasks: dict, subset: Iterable[str]) -> dict:
    subset = list(subset)
    return {
        "records": len(subset),
        "request_status": {status: sum(tasks[t]["request"]["status"] == status for t in subset) for status in sorted({tasks[t]["request"]["status"] for t in subset})},
        "access_status": {status: sum(tasks[t]["access"]["status"] == status for t in subset) for status in sorted({tasks[t]["access"]["status"] for t in subset})},
        "effort_level": {level: sum(tasks[t]["effort"]["level"] == level for t in subset) for level in sorted({tasks[t]["effort"]["level"] for t in subset})},
    }


def analyse(repo_root: Path = DEFAULT_REPO, plans: dict | None = None, spec: dict | None = None) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    plans = plans if plans is not None else _read_json(PLANS_PATH)
    spec = spec if spec is not None else _read_json(SPEC_PATH)
    tasks = {task["id"]: task for task in plans["tasks"]}
    task_ids = sorted(tasks)

    relationships = _load_evaluator(repo_root, "relationships").build(repo_root)
    inventory = _load_evaluator(repo_root, "inventory").build(repo_root)

    families: dict[str, dict] = {}
    for family in spec["families"]:
        excluded_full: list[dict] = []
        if family["kind"] == "relationships":
            models, excluded, excluded_full = _kohlit_models(relationships)
        elif family["kind"] == "inventory":
            models, excluded = _entry25_models(inventory, family["query_id"])
        elif family["kind"] == "letter_strings":
            models, excluded = _letter_models(spec), []
        elif family["kind"] == "single_branch":
            models, excluded = [_single_branch_model(family)], []
        else:
            raise ValueError(f"Unknown family kind {family['kind']}")
        families[family["id"]] = {**family, "models": sorted(models, key=lambda m: m["id"]), "excluded": sorted(excluded, key=lambda m: m["id"]),
                                  "excluded_full": sorted(excluded_full, key=lambda m: m["id"])}
    family_ids = [family["id"] for family in spec["families"]]

    rows: dict[str, list[dict]] = {}
    observations = {observation["task_id"]: observation for observation in spec["observations"]}
    if sorted(observations) != task_ids or len(observations) != len(spec["observations"]):
        raise ValueError("Every plans.json task needs exactly one discrimination observation")
    for task_id in task_ids:
        observation = observations[task_id]
        if observation["kind"] == "letter_components":
            rows[task_id] = _letter_rows(spec, observation)
        elif observation["kind"] == "component_product":
            rows[task_id] = _component_rows(tasks[task_id], observation)
        elif observation["kind"] == "plans_outcomes":
            rows[task_id] = _plans_rows(tasks[task_id], observation)
        else:
            raise ValueError(f"Unknown observation kind {observation['kind']}")
    recorded = _recorded_rows(tasks, rows)
    restored = _recorded_exclusions(families, recorded)
    validate(spec, plans, repo_root, families, rows, restored)
    # The planned roster: surviving models plus models that only a recorded outcome excludes.
    roster = {fid: sorted(families[fid]["models"] + restored[fid], key=lambda m: m["id"]) for fid in family_ids}

    # Model-level survival for every outcome row.
    model_survivors: dict[str, dict[str, dict[str, frozenset]]] = {fid: {} for fid in family_ids}
    for fid in family_ids:
        family = families[fid]
        for task_id in task_ids:
            per_row = {}
            for row in rows[task_id]:
                if family["kind"] == "letter_strings":
                    alive = frozenset(row["string_survivors"]) if task_id == family["task_id"] else frozenset(m["id"] for m in roster[fid])
                else:
                    alive = frozenset(m["id"] for m in roster[fid] if survives(m, row["effects"]))
                per_row[row["id"]] = alive
            model_survivors[fid][task_id] = per_row

    # 1. Equivalence classes. They are formed on the planned roster, so recorded
    # outcomes keep the class names used when the rows were planned.
    family_out, class_pred, class_ids, class_rows = {}, {}, {}, {}
    recorded_out: dict[str, dict] = {task_id: {"task_id": task_id, "outcome_id": item["record"]["outcome_id"],
                                               "row_id": item["row"]["id"], "recorded_utc": item["record"]["recorded_utc"],
                                               "excluded_classes": {}} for task_id, item in recorded.items()}
    for fid in family_ids:
        family = families[fid]
        by_id = {model["id"]: model for model in roster[fid]}
        groups = collapse(by_id, model_survivors[fid])
        planned = {f"{fid}-c{index:02d}": members for index, members in enumerate(groups, start=1)}
        gone_by: dict[str, list[str]] = {}
        for task_id, item in recorded.items():
            alive = model_survivors[fid][task_id][item["row"]["id"]]
            for cid, members in planned.items():
                if members[0] not in alive:
                    gone_by.setdefault(cid, []).append(task_id)
                    recorded_out[task_id]["excluded_classes"].setdefault(fid, []).append(cid)
        restored_ids = {model["id"] for model in restored[fid]}
        if {m for cid in gone_by for m in planned[cid]} != restored_ids:
            raise ValueError(f"Recorded outcomes and current evidence disagree on the excluded {fid} models")
        classes = {cid: members for cid, members in planned.items() if cid not in gone_by}
        class_ids[fid] = sorted(classes)
        class_pred[fid] = predictions(classes, model_survivors[fid])
        class_rows[fid] = {
            task_id: [frozenset(cid for cid in classes if classes[cid][0] in alive) for alive in model_survivors[fid][task_id].values()]
            for task_id in task_ids
        }
        dims = family["dimensions"]
        within_pairs = sum(len(members) * (len(members) - 1) // 2 for members in classes.values())
        family_out[fid] = {
            "id": fid, "label": family["label"], "kind": family["kind"], "active_test": family["active_test"],
            "claim": family["claim"], "source_ids": family["source_ids"], "roster_note": family["roster_note"],
            "surviving_models": len(family["models"]), "excluded_models": family["excluded"],
            "class_count": len(classes),
            "recorded_exclusions": [
                {
                    "class_id": cid, "label": _class_label([by_id[m] for m in planned[cid]], dims),
                    "member_count": len(planned[cid]), "members": planned[cid],
                    "task_ids": sorted(gone_by[cid]),
                    "row_ids": sorted(recorded[t]["row"]["id"] for t in gone_by[cid]),
                }
                for cid in sorted(gone_by)
            ],
            "classes": [
                {
                    "id": cid, "label": _class_label([by_id[m] for m in members], dims),
                    "member_count": len(members),
                    "composition": _cubes(sorted(tuple(str(by_id[m]["dims"][d]) for d in dims) for m in members), dims),
                    "identical_on": _varying([by_id[m] for m in members], dims),
                    **({"members": members} if len(members) <= MEMBER_LIST_LIMIT else {}),
                }
                for cid, members in sorted(classes.items())
            ],
            "model_pairs_no_record_separates": within_pairs,
        }

    for task_id, item in recorded.items():
        computed = {fid: sorted(cids) for fid, cids in recorded_out[task_id]["excluded_classes"].items()}
        recorded_out[task_id]["excluded_classes"] = computed
        if item["record"].get("excluded_classes", {}) != computed:
            raise ValueError(f"Recorded outcome of {task_id} declares excluded classes {item['record'].get('excluded_classes')}; the search finds {computed}")

    # 2. Observation table at class level.
    derivations: dict[str, str] = {}
    table = []
    for task_id in task_ids:
        task = tasks[task_id]
        observation = observations[task_id]
        affected = [fid for fid in family_ids
                    if any(row["id"] not in class_pred[fid][cid][task_id] for row in rows[task_id] for cid in class_ids[fid])]
        out_rows = []
        for row in rows[task_id]:
            excluded, surviving = {}, {}
            for fid in family_ids:
                gone = [cid for cid in class_ids[fid] if row["id"] not in class_pred[fid][cid][task_id]]
                if gone:
                    excluded[fid] = gone
                if fid in affected:
                    surviving[fid] = [cid for cid in class_ids[fid] if row["id"] in class_pred[fid][cid][task_id]]
            for derivation_id, text in row["derivations"]:
                if derivations.setdefault(derivation_id, text) != text:
                    raise ValueError(f"Conflicting derivation text for {derivation_id}")
            out_rows.append({
                "id": row["id"], "plans_outcome_id": row["plans_outcome_id"], "label": row["label"],
                "row_kind": row["row_kind"], "basis": row["basis"],
                "derivation_ids": [derivation_id for derivation_id, _ in row["derivations"]],
                "components": row["components"], "surviving_classes": surviving, "excluded_classes": excluded,
                "every_class_survives": not excluded,
                **({"recorded": True, "recorded_utc": recorded[task_id]["record"]["recorded_utc"],
                    "excluded_before_search": recorded_out[task_id]["excluded_classes"]}
                   if task_id in recorded and recorded[task_id]["row"]["id"] == row["id"] else {}),
            })
        table.append({
            "task_id": task_id, "title": task["title"], "question_types": observation["question_types"],
            "scope_note": observation.get("scope_note"),
            "non_discriminating_components": observation.get("non_discriminating_components", []),
            "request_status": task["request"]["status"], "access_status": task["access"]["status"],
            "effort_level": task["effort"]["level"], "freeze_status": task["freeze"]["status"],
            "historical_priority": task["priority"],
            "recorded_outcome": recorded_out[task_id]["row_id"] if task_id in recorded_out else None,
            "families_affected": affected,
            "outcomes": out_rows,
        })

    # 3. Search.
    multi = [fid for fid in family_ids if len(class_ids[fid]) > 1]
    active = [fid for fid in multi if families[fid]["active_test"]]
    decisive_rows = {t: frozenset(row["id"] for row in rows[t] if row["row_kind"] == "decisive") for t in task_ids}
    all_survive_rows = {t: [row["id"] for row in rows[t] if all(row["id"] in class_pred[f][c][t] for f in family_ids for c in class_ids[f])] for t in task_ids}

    def full_in_principle(fid: str) -> Callable[[tuple], bool]:
        return lambda subset: blocks(class_ids[fid], class_pred[fid], subset) == len(class_ids[fid])

    def full_guarantee(fid: str, allowed: dict | None) -> Callable[[tuple], bool]:
        total = len(class_ids[fid]) * (len(class_ids[fid]) - 1) // 2
        return lambda subset: len(guaranteed_pairs(class_ids[fid], class_pred[fid], subset, allowed)) == total

    per_family_search = {}
    for fid in family_ids:
        cids = class_ids[fid]
        pred = class_pred[fid]
        principle_sets = minimal_sets(task_ids, full_in_principle(fid)) if len(cids) > 1 else [()]
        necessary = sorted(set.intersection(*(set(s) for s in principle_sets))) if principle_sets and len(cids) > 1 else []
        reachable = reachable_survivor_sets(cids, class_rows[fid], task_ids)
        sole = sorted({next(iter(s)) for s in reachable if len(s) == 1})
        sole_sets = {
            cid: [list(s) for s in minimal_sets(task_ids, lambda subset, cid=cid: frozenset([cid]) in reachable_survivor_sets(cids, class_rows[fid], subset))]
            for cid in sole
        }
        pair_records = []
        for a, b in itertools.combinations(cids, 2):
            records = [t for t in task_ids if pred[a][t] != pred[b][t]]
            pair_records.append({"pair": [a, b], "separating_records": records})
        never_excludable = [cid for cid in cids if all(pred[cid][t] == frozenset(r["id"] for r in rows[t]) for t in task_ids)]
        total_pairs = len(cids) * (len(cids) - 1) // 2
        per_family_search[fid] = {
            "class_pair_count": total_pairs,
            "worst_case_all_outcomes": {
                "guaranteed_pairs_with_all_records": len(guaranteed_pairs(cids, pred, task_ids)),
                "minimal_sets": [list(s) for s in minimal_sets(task_ids, full_guarantee(fid, None))] if total_pairs else [[]],
            },
            "worst_case_decisive_outcomes": {
                "guaranteed_pairs_with_all_records": len(guaranteed_pairs(cids, pred, task_ids, decisive_rows)),
                "minimal_sets": [list(s) for s in minimal_sets(task_ids, full_guarantee(fid, decisive_rows))] if total_pairs else [[]],
            },
            "in_principle": {
                "separated_pairs_with_all_records": len(separated_pairs(cids, pred, task_ids)),
                "minimal_sets": [list(s) for s in principle_sets],
                "necessary_records": necessary,
            },
            "best_case": {
                "classes_that_can_remain_alone": sole,
                "minimal_sets_to_leave_each_alone": sole_sets,
                "all_classes_can_be_excluded": frozenset() in reachable,
            },
            "classes_no_record_can_exclude": never_excludable,
            "class_pairs": pair_records,
            "class_pairs_with_one_separating_record": [p["pair"] for p in pair_records if len(p["separating_records"]) == 1],
            "class_pairs_no_record_separates": [p["pair"] for p in pair_records if not p["separating_records"]],
        }

    union_sets = minimal_sets(task_ids, lambda subset: all(full_in_principle(fid)(subset) for fid in multi))

    # 4. Per-record metrics and queue rank.
    record_metrics = []
    for task_id in task_ids:
        per_family = {}
        for fid in family_ids:
            cids = class_ids[fid]
            reach = [cid for cid in cids if class_pred[fid][cid][task_id] != frozenset(r["id"] for r in rows[task_id])]
            per_family[fid] = {
                "separated_pairs": len(separated_pairs(cids, class_pred[fid], [task_id])),
                "blocks": blocks(cids, class_pred[fid], [task_id]),
                "classes_it_can_exclude": reach,
                "guaranteed_pairs_all_outcomes": len(guaranteed_pairs(cids, class_pred[fid], [task_id])),
                "guaranteed_pairs_decisive_outcomes": len(guaranteed_pairs(cids, class_pred[fid], [task_id], decisive_rows)),
                "necessary": task_id in per_family_search[fid]["in_principle"]["necessary_records"],
            }
        key = {
            "necessary_for_active_families": sum(per_family[f]["necessary"] for f in active),
            "necessary_for_families": sum(per_family[f]["necessary"] for f in multi),
            "active_separated_pairs": sum(per_family[f]["separated_pairs"] for f in active),
            "all_separated_pairs": sum(per_family[f]["separated_pairs"] for f in multi),
        }
        record_metrics.append({"task_id": task_id, "rank_key": key, "per_family": {f: v for f, v in per_family.items() if f in multi or v["classes_it_can_exclude"]},
                               "outcomes_where_every_class_survives": all_survive_rows[task_id],
                               "profile": _profile(tasks, [task_id])})
    ordering = sorted(record_metrics, key=lambda m: (tuple(-v for v in m["rank_key"].values()), m["task_id"]))
    rank, previous = 0, None
    for item in ordering:
        signature = tuple(item["rank_key"].values())
        if signature != previous:
            rank += 1
            previous = signature
        item["rank"] = rank
        item["reasons"] = _reasons(item, tasks[item["task_id"]], families)

    # 5. Sets that separate the most class pairs for each number of records.
    frontiers = {"active_families": _frontier(task_ids, active, class_ids, class_pred, tasks),
                 "all_families": _frontier(task_ids, multi, class_ids, class_pred, tasks)}

    # 6. Predicates no queued record can contradict.
    contradicting = [effect for t in task_ids for row in rows[t] for effect in row["effects"]]
    unqueued = _unqueued(families, contradicting)

    supplementary = [
        {key: item[key] for key in ("id", "title", "origin", "question_type", "derivation", "source_ids")} | {"excluded_classes": {}}
        for item in spec["supplementary_observations"]
    ]

    every_record_can_leave_all = all(all_survive_rows[t] for t in task_ids)
    result = {
        "schema_version": 1,
        "mode": "planning_only",
        "as_of_utc": spec["as_of_utc"],
        "method": spec["method"],
        "definitions": DEFINITIONS,
        "limits": spec["limits"],
        "question_types": spec["question_types"],
        "display_order": spec["display_order"],
        "families": [family_out[f] for f in family_ids],
        "recorded_outcomes": [recorded_out[t] for t in sorted(recorded_out)],
        "observation_table": table,
        "derivations": dict(sorted(derivations.items())),
        "supplementary_observations": supplementary,
        "search": {
            "records": task_ids,
            "families_with_alternatives": multi,
            "active_families": active,
            "every_record_has_an_outcome_leaving_every_class": every_record_can_leave_all,
            "per_family": per_family_search,
            "minimal_in_principle_sets_all_families": [list(s) for s in union_sets],
            "frontier_by_record_count": frontiers,
        },
        "queue_rank": [{key: item[key] for key in ("rank", "task_id", "rank_key", "reasons", "per_family", "outcomes_where_every_class_survives", "profile")} for item in ordering],
        "unqueued_predicates": unqueued,
    }
    result["question_summary"] = _question_summary(spec, rows, table, family_ids, class_ids, class_pred)
    result["findings"] = _findings(result, families)
    return result


def _question_summary(spec: dict, rows: dict, table: list[dict], family_ids: list[str], class_ids: dict, class_pred: dict) -> list[dict]:
    """What each question can exclude when it is the only component resolved."""
    by_task = {item["task_id"]: item for item in table}
    out = []

    def summarise(task_id: str, row_ids: list[str]) -> tuple[dict, dict]:
        excluded, pairs = {}, {}
        for fid in family_ids:
            gone = sorted({cid for row in by_task[task_id]["outcomes"] if row["id"] in row_ids for cid in row["excluded_classes"].get(fid, [])})
            if gone:
                excluded[fid] = gone
                restricted = {cid: {task_id: class_pred[fid][cid][task_id] & frozenset(row_ids)} for cid in class_ids[fid]}
                pairs[fid] = len(separated_pairs(class_ids[fid], restricted, [task_id]))
        return excluded, pairs

    for observation in spec["observations"]:
        task_id = observation["task_id"]
        if observation["kind"] == "component_product":
            unresolved = {c["id"]: next(v["id"] for v in c["values"] if v.get("unresolved")) for c in observation["components"]}
            for component in observation["components"]:
                selected = [row["id"] for row in rows[task_id] if row["components"]
                            and all(row["components"][other] == unresolved[other] for other in unresolved if other != component["id"])]
                excluded, pairs = summarise(task_id, selected)
                out.append({"question_type": component["question_type"], "task_id": task_id, "component": component["id"],
                            "label": component["label"], "in_queue": True, "can_exclude": excluded, "separated_pairs": pairs})
            for extra in observation.get("non_discriminating_components", []):
                out.append({"question_type": extra["question_type"], "task_id": task_id, "component": extra["id"],
                            "label": extra["label"], "in_queue": True, "can_exclude": {}, "separated_pairs": {}, "detail": extra["detail"]})
        else:
            excluded, pairs = summarise(task_id, [row["id"] for row in rows[task_id]])
            label = spec["letter_strings"]["components"] if observation["kind"] == "letter_components" else None
            out.append({"question_type": observation["question_types"][0], "task_id": task_id, "component": "whole record",
                        "label": by_task[task_id]["title"], "in_queue": True, "can_exclude": excluded, "separated_pairs": pairs,
                        **({"components": [c["label"] for c in label]} if label else {})})
    for item in spec["supplementary_observations"]:
        out.append({"question_type": item["question_type"], "task_id": item["id"], "component": "supplementary",
                    "label": item["title"], "in_queue": False, "can_exclude": {}, "separated_pairs": {}, "detail": item["derivation"]})
    order = [q["id"] for q in spec["question_types"]]
    return sorted(out, key=lambda item: (order.index(item["question_type"]), not item["in_queue"], item["task_id"], item["component"]))


def _frontier(task_ids: list[str], family_ids: list[str], class_ids: dict, class_pred: dict, tasks: dict) -> list[dict]:
    """For each number of records, the sets that separate the most class pairs."""
    total = sum(len(class_ids[f]) * (len(class_ids[f]) - 1) // 2 for f in family_ids)
    frontier = []
    for size in range(1, len(task_ids) + 1):
        scored = {subset: sum(len(separated_pairs(class_ids[f], class_pred[f], subset)) for f in family_ids)
                  for subset in itertools.combinations(task_ids, size)}
        best = max(scored.values())
        frontier.append({
            "records": size,
            "max_separated_pairs": best,
            "class_pairs": total,
            "sets": [{"tasks": list(subset), "profile": _profile(tasks, subset)} for subset in sorted(s for s, v in scored.items() if v == best)],
        })
        # Larger sets only add records that separate nothing more.
        if best == total:
            break
    best_ratio = max(Fraction(item["max_separated_pairs"], item["records"]) for item in frontier)
    for item in frontier:
        item["best_pairs_per_record"] = Fraction(item["max_separated_pairs"], item["records"]) == best_ratio
        item["separates_every_pair"] = item["max_separated_pairs"] == total
    return frontier


def _findings(result: dict, families: dict) -> list[str]:
    """Plain sentences generated from the computed result."""
    search = result["search"]
    out = []
    for item in result["recorded_outcomes"]:
        gone = "; ".join(f"{fid}: {', '.join(cids)}" for fid, cids in sorted(item["excluded_classes"].items())) or "no class"
        out.append(f"Recorded outcome ({item['recorded_utc']}): {item['task_id']} row {item['row_id']} excluded {gone}. "
                   "These classes left the search; the other classes keep their planned names.")
    if search["every_record_has_an_outcome_leaving_every_class"]:
        out.append("Every record has an inconclusive, partial or not-obtained outcome under which every class survives. No set of records guarantees any separation in the worst case.")
    for family in result["families"]:
        fid = family["id"]
        if family["class_count"] < 2:
            continue
        per = search["per_family"][fid]
        out.append(f"{family['label']}: {family['surviving_models']} surviving models collapse into {family['class_count']} classes.")
        sets = per["in_principle"]["minimal_sets"]
        if sets:
            out.append(f"{family['label']}: the smallest record set that can separate every class is " + " or ".join("{" + ", ".join(s) + "}" for s in sets)
                       + "; necessary records: " + (", ".join(per["in_principle"]["necessary_records"]) or "none") + ".")
        decisive = per["worst_case_decisive_outcomes"]["minimal_sets"]
        out.append(f"{family['label']}: " + ("if every record returns a decisive outcome, " + " or ".join("{" + ", ".join(s) + "}" for s in decisive) + " guarantees separation of every class." if decisive
                   else "even decisive outcomes guarantee no separation, because a compatible verdict never excludes another branch."))
        if per["classes_no_record_can_exclude"]:
            out.append(f"{family['label']}: no queued record can exclude " + ", ".join(per["classes_no_record_can_exclude"]) + "; at best the queue narrows the roster to it.")
    top = [item["task_id"] for item in result["queue_rank"] if item["rank"] == 1]
    out.append("Rank 1: " + ", ".join(top) + ".")
    return out


DEFINITIONS = {
    "survives": "A class survives an outcome unless the outcome's recorded or derived consequence contradicts a required predicate of every model in it.",
    "class": "Models with identical survival on every outcome of every queued record. Collapsing them stops duplicated parameter choices from counting twice.",
    "in_principle": "A record set separates a pair in principle if some outcome of some record in it excludes one class of the pair and not the other.",
    "worst_case_all_outcomes": "A record set guarantees a pair if, for some record in it, no outcome (including inconclusive, partial and not-obtained ones) leaves both classes alive.",
    "worst_case_decisive_outcomes": "The same guarantee, counting only decisive outcomes: the record is obtained and every component it tests is resolved.",
    "best_case": "Classes that some combination of outcomes can leave as the only survivor.",
    "frontier": "For each number of records, the record sets that separate the most class pairs in principle. The unit is one record dependency; access and effort categories are listed, not weighted.",
    "rank": "Lexicographic: necessary for active-test families, necessary for any family, class pairs separated in active-test families, class pairs separated in all families. Equal keys share a rank.",
    "recorded_outcome": "An outcome row that an obtained record actually showed (plans.json recorded_outcome). Classes are formed before it is applied, so class names stay as planned and registered; the classes it excludes leave the search.",
}


def _reasons(item: dict, task: dict, families: dict) -> list[str]:
    reasons = []
    record = task.get("recorded_outcome")
    if record:
        gone = "; ".join(f"{fid}: {', '.join(cids)}" for fid, cids in sorted(record.get("excluded_classes", {}).items())) or "no class"
        reasons.append(f"Outcome recorded {record['recorded_utc']}: row {record['row_id']}. It excluded {gone} before the search.")
        if not any(m["separated_pairs"] or m["classes_it_can_exclude"] for m in item["per_family"].values()):
            reasons.append("It now separates no remaining class.")
    for fid, metrics in sorted(item["per_family"].items()):
        label = families[fid]["label"]
        if metrics["necessary"]:
            reasons.append(f"Necessary: every smallest record set that separates the {label} classes includes it.")
        if metrics["separated_pairs"]:
            reasons.append(f"Separates {metrics['separated_pairs']} class pairs in {label} in principle; it can exclude {len(metrics['classes_it_can_exclude'])} classes.")
        elif metrics["classes_it_can_exclude"]:
            reasons.append(f"Can exclude only its own named branch ({label}); no alternative is modelled beside it.")
        if metrics["guaranteed_pairs_decisive_outcomes"]:
            reasons.append(f"If its outcome is decisive, it is guaranteed to separate {metrics['guaranteed_pairs_decisive_outcomes']} class pairs in {label}.")
    if item["outcomes_where_every_class_survives"]:
        reasons.append(f"{len(item['outcomes_where_every_class_survives'])} of its outcomes leave every class alive, so it guarantees nothing in the worst case.")
    reasons.append(f"Recorded access: request {task['request']['status']}, access {task['access']['status']}, effort {task['effort']['level']}, freeze {task['freeze']['status']}.")
    return reasons


def _unqueued(families: dict, effects: list[dict]) -> dict[str, list[dict]]:
    """Unknown required checks that no queued outcome can contradict."""
    out = {}
    contradictions = [effect for effect in effects if effect.get("status") == "contradicted"]
    for fid, family in families.items():
        if family["kind"] not in {"relationships", "inventory"}:
            continue
        found: dict[tuple, int] = {}
        for model in family["models"]:
            for check in model["checks"]:
                if not check["required"] or check["status"] != "unknown":
                    continue
                if any(_effect_matches(effect, model, check) for effect in contradictions):
                    continue
                key = (check["predicate"], check["subject"] or "unassigned role") if family["kind"] == "relationships" else (check["check"], model["dims"]["candidate"])
                found[key] = found.get(key, 0) + 1
        label = ("predicate", "subject") if family["kind"] == "relationships" else ("check", "candidate")
        out[fid] = [{label[0]: k[0], label[1]: k[1], "models": n} for k, n in sorted(found.items())]
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--summary", action="store_true", help="Print the rank and minimal sets only")
    args = parser.parse_args()
    result = analyse(args.repo_root)
    if args.summary:
        result = {
            "queue_rank": [{"rank": r["rank"], "task_id": r["task_id"], "rank_key": r["rank_key"]} for r in result["queue_rank"]],
            "classes": {f["id"]: f["class_count"] for f in result["families"]},
            "minimal_in_principle_sets_all_families": result["search"]["minimal_in_principle_sets_all_families"],
            "per_family": {fid: {k: v for k, v in s.items() if k not in {"class_pairs"}} for fid, s in result["search"]["per_family"].items()},
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
