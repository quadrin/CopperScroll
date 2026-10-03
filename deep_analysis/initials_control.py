"""Finite-corpus exploratory prefix controls. Standard library; no network.

Importing this module does not load or score a corpus. A CLI run requires an
explicit freeze JSON and refuses a non-frozen manifest. No corpus is bundled.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb, sqrt
from pathlib import Path
import random
import unicodedata

ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
VOWELS = "ΑΕΗΙΟΥΩ"
CONSONANTS = "".join(c for c in ALPHABET if c not in VOWELS)
PRIMARY = ("ΚΕΝ", "ΧΑΓ", "ΗΝ", "ΘΕ", "ΔΙ", "ΤΡ", "ΣΚ")
DOCUMENTED_MENU = (("ΚΕΝ",), ("ΧΑΓ",), ("ΗΝ",), ("ΘΕ", "ΞΕ"),
                   ("ΔΙ",), ("ΤΡ", "ΤΡΙ"), ("ΣΚ", "ΧΚ", "ΞΚ"))


def normalize_form(raw: str, *, subscript: str) -> tuple[str, bool]:
    """Strip accents/breathings, merge sigma shapes, handle subscript explicitly.

    NFD before case conversion prevents casefold silently expanding U+0345.
    Spaces/punctuation and letters outside the frozen 24-letter alphabet reject
    the whole form; this function never joins tokens or transliterates names.
    """
    if subscript not in {"omit", "expand", "reject"}:
        raise ValueError("subscript must be omit, expand, or reject")
    text = unicodedata.normalize("NFD", raw.strip())
    has_subscript = "\u0345" in text
    if has_subscript and subscript == "reject":
        raise ValueError("iota subscript needs a declared treatment")
    out = []
    for char in text:
        if char == "\u0345":
            if subscript == "expand":
                out.append("Ι")
            continue
        if unicodedata.category(char).startswith("M"):
            continue
        char = {"ϲ": "Σ", "Ϲ": "Σ", "ς": "Σ", "σ": "Σ"}.get(char, char)
        out.append(char.upper())
    normalized = "".join(out)
    if not normalized or any(c not in ALPHABET for c in normalized):
        raise ValueError("not one Greek form in the declared 24-letter alphabet")
    return normalized, has_subscript


def collapse_nested(menu: tuple[str, ...]) -> tuple[str, ...]:
    """For existence matching, a retained shorter prefix subsumes extensions."""
    unique = set(menu)
    return tuple(sorted(p for p in unique if not any(
        len(q) < len(p) and p.startswith(q) for q in unique)))


def domains(prefix: str, model: str) -> tuple[str, ...]:
    if model == "uniform24":
        return tuple(ALPHABET for _ in prefix)
    if model == "shape":
        return tuple(VOWELS if c in VOWELS else CONSONANTS for c in prefix)
    raise ValueError("unknown null model")


def menu_layout(menu: tuple[str, ...], model: str):
    menu = collapse_nested(menu)
    if not menu or any(any(c not in ALPHABET for c in p) for p in menu):
        raise ValueError("invalid prefix menu")
    base = menu[0]
    if any(len(p) != len(base) or p[1:] != base[1:] for p in menu):
        raise ValueError("supported union menus differ only at first letter")
    ds = domains(base, model)
    if any(domains(p, model) != ds for p in menu):
        raise ValueError("union alternatives must share letter-class pattern")
    return menu, ds, len(menu)


def exact_slot_probability(names: frozenset[str], menu: tuple[str, ...],
                           model: str) -> Fraction:
    """Exact chance of >=1 name hit, preserving menu overlap and C/V shape.

    Sample tail uniformly from its position domains and choose m DISTINCT first
    letters uniformly without replacement. The union has the same first-letter
    ambiguity structure as the documented menu. Longer nested readings are
    subsumed for this statistic, not treated as an independent opportunity.
    """
    menu, ds, m = menu_layout(menu, model)
    length = len(menu[0])
    prefix_set = {name[:length] for name in names if len(name) >= length}
    total = Fraction(0)
    tail_count = 1
    for d in ds[1:]:
        tail_count *= len(d)
    for tail_tuple in product(*ds[1:]):
        tail = "".join(tail_tuple)
        hits = sum(first + tail in prefix_set for first in ds[0])
        failures = comb(len(ds[0]) - hits, m) if len(ds[0]) - hits >= m else 0
        total += 1 - Fraction(failures, comb(len(ds[0]), m))
    return total / tail_count


def poisson_binomial(qs: list[Fraction]) -> list[Fraction]:
    """Exact PMF of independent group-hit count, retaining rational arithmetic."""
    pmf = [Fraction(1)]
    for q in qs:
        nxt = [Fraction(0)] * (len(pmf) + 1)
        for k, p in enumerate(pmf):
            nxt[k] += p * (1 - q)
            nxt[k + 1] += p * q
        pmf = nxt
    return pmf


def score(names: frozenset[str], menus: tuple[tuple[str, ...], ...]) -> int:
    return sum(any(name.startswith(p) for name in names for p in menu)
               for menu in menus)


def exact_result(names, menus, model):
    observed = score(names, menus)
    qs = [exact_slot_probability(names, menu, model) for menu in menus]
    pmf = poisson_binomial(qs)
    p = sum(pmf[observed:], Fraction(0))
    return {"statistic": "groups_with_at_least_one_name_prefix", "observed": observed,
            "slot_hit_probabilities": [float(q) for q in qs],
            "expected": float(sum(qs)), "pmf": [float(q) for q in pmf],
            "upper_tail_exact": str(p), "upper_tail": float(p)}


def sample_menu(menu, model, rng):
    menu, ds, m = menu_layout(menu, model)
    tail = "".join(rng.choice(d) for d in ds[1:])
    return tuple(first + tail for first in rng.sample(ds[0], m))


def monte_carlo(names, menus, model, draws, seed):
    """Optional verification of the SAME null, not an additional hypothesis."""
    if draws < 1:
        raise ValueError("draws must be positive")
    observed = score(names, menus)
    rng = random.Random(seed)
    lengths = {len(p) for menu in menus for p in collapse_nested(menu)}
    support = {length: {n[:length] for n in names if len(n) >= length}
               for length in lengths}
    def drawn_score():
        return sum(any(p in support[len(p)] for p in sample_menu(menu, model, rng))
                   for menu in menus)
    exceed = sum(drawn_score() >= observed for _ in range(draws))
    estimate = (exceed + 1) / (draws + 1)
    return {"draws": draws, "seed": seed, "exceedances": exceed,
            "upper_tail_plus_one": estimate,
            "approximate_mc_standard_error": sqrt(estimate * (1-estimate) / draws)}


def load_corpus(path: Path, subscript: str):
    """CSV must already encode frozen source eligibility and lemma identity.

    Rows need name_id and greek_form. Every row must be one selected attested
    lexical form, not an occurrence or bearer. Extra provenance columns survive
    in the frozen input; this loader does not invent dates/geography/aliases.
    """
    by_id = {}
    rejected = []
    subscript_rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"name_id", "greek_form"}.issubset(reader.fieldnames):
            raise ValueError("CSV header must contain name_id and greek_form")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("duplicate CSV header fields")
        row_count = 0
        for line, row in enumerate(reader, start=2):
            row_count += 1
            if None in row:
                raise ValueError(f"row {line}: more fields than header")
            if not row.get("name_id") or not row.get("greek_form"):
                raise ValueError(f"row {line}: name_id and greek_form required")
            try:
                form, sub = normalize_form(row["greek_form"], subscript=subscript)
            except ValueError as exc:
                rejected.append({"row": line, "reason": str(exc)})
                continue
            by_id.setdefault(row["name_id"], set()).add(form)
            if sub:
                subscript_rows.append(line)
    names = frozenset(form for forms in by_id.values() for form in forms)
    if not row_count:
        raise ValueError("corpus has a header but no data rows")
    if not names:
        raise ValueError("no eligible normalized Greek forms")
    return names, by_id, rejected, subscript_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    args = parser.parse_args()
    freeze = json.loads(args.freeze.read_text(encoding="utf-8"))
    if freeze.get("status") != "frozen_before_scoring":
        raise ValueError("scoring requires explicit frozen_before_scoring manifest")
    if freeze.get("primary_readings") != list(PRIMARY) or freeze.get("reading_menu") != [list(m) for m in DOCUMENTED_MENU]:
        raise ValueError("frozen readings differ from this runner; revise and freeze the method before scoring")
    corpus = args.freeze.parent / freeze["corpus_csv"]
    digest = sha256(corpus.read_bytes()).hexdigest()
    if digest != freeze["corpus_sha256"]:
        raise ValueError("corpus checksum differs from frozen manifest")
    for key in ("source_eligibility", "date_geography_rule", "lemma_alias_rule",
                "exposure_limit", "decision_rule"):
        if not freeze.get(key):
            raise ValueError(f"missing frozen design field: {key}")
    names, by_id, rejected, subs = load_corpus(corpus, freeze["iota_subscript"])
    if not names:
        raise ValueError("no eligible normalized Greek forms")
    output = {"design": freeze, "normalization": {
        "unique_normalized_forms": len(names), "name_ids": len(by_id),
        "rejected_rows": rejected, "iota_subscript_rows": subs}, "results": {}}
    primary = tuple((p,) for p in PRIMARY)
    for label, menus in (("primary", primary), ("documented_union", DOCUMENTED_MENU)):
        output["results"][label] = {}
        for model in ("shape", "uniform24"):
            result = exact_result(names, menus, model)
            if freeze.get("mc_draws", 0):
                result["mc_verification"] = monte_carlo(
                    names, menus, model, freeze["mc_draws"], freeze["seed"])
            output["results"][label][model] = result
    output["branch_sensitivity"] = []
    for readings in product(*DOCUMENTED_MENU):
        menus = tuple((p,) for p in readings)
        output["branch_sensitivity"].append({"readings": readings,
            "shape": exact_result(names, menus, "shape")})
    output["matches"] = [{"entry": entry, "menu": menu,
        "name_ids_by_prefix": {p: sorted(i for i, forms in by_id.items()
                                  if any(n.startswith(p) for n in forms)) for p in menu}}
        for entry, menu in zip(("1", "4", "6", "7", "9", "12a", "15"), DOCUMENTED_MENU)]
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
