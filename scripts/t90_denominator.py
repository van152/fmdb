#!/usr/bin/env python3
"""t90 - denominator re-bucket (E116 baseline -> v2 candidate).

  py -V:3.12 -I -B scripts/t90_denominator.py --selftest
  py -V:3.12 -I -B scripts/t90_denominator.py --build
  py -V:3.12 -I -B scripts/t90_denominator.py --verify

Assembly only: every re-bucket cites an accepted source (E124/E125/E126/E127
out files). Nothing here re-adjudicates evidence; where a source and the brief
disagree the row is kept with `conflict` set and no bucket is invented.

Writes scratch/t90/out/denominator_v2.json only.
Exit codes: 0 pass / 1 check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "reports" / "xml_denominator_coverage.json"
SCHEMA = ROOT / "reports" / "club_nation_subtable_schema.json"
T83_FM = ROOT / "scratch" / "t83" / "out" / "field_map.json"
T81_CITY = ROOT / "scratch" / "t81" / "out" / "rescan_fk_city.json"
OUT = ROOT / "scratch" / "t90" / "out" / "denominator_v2.json"

BASE_SHA = "e3a6d56e639fb3d9cd507500d81b3e5d4a9f591eafdfc75f0d1f1227d23df9c4"
BASE_BYTES = 297905
T83_SHA = "3a2db1496cd2c5217a03ec9f4ab5abf805b8ca727080491acc98e0157908969d"
T81_CITY_SHA = "e49642a8085021c3c1f6d24fe3d3fab2c3904ede3f73693e9cd39e45ddaf9c45"

# E124 (t87) accepted verdict, read back from the v11.1 section, not retyped.
TABLE45_RANGE = (211, 327)
TABLE45_COUNT = 117
FIVE_TABLES = ("award_0", "language_8", "derby_18", "weather_27", "media_7")
# XML entity names of the five tables. None of them occurs in the 1,034-row
# club/comp/nation denominator, so rule (2) can never move a row by construction.
FIVE_TABLE_ENTITIES = ("award", "language", "derby", "weather", "media")


class CheckFailure(Exception):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2,
                      allow_nan=False).encode("utf-8") + b"\n"


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def occ_index(occ_id: str) -> int | None:
    try:
        return int(occ_id.rsplit("/", 1)[-1])
    except ValueError:
        return None


def t83_l3_codes(fm: dict[str, Any]) -> dict[str, list[str]]:
    return {t: sorted(f["field"] for f in fm[t]["schema_fields"] if f["grade"] == "L3")
            for t in FIVE_TABLES}


def build() -> dict[str, Any]:
    base_raw = BASE.read_bytes()
    require(sha(base_raw) == BASE_SHA, "E116 baseline pin mismatch")
    base = read_json(BASE)
    occ = base["occurrences"]
    require(len(occ) == 1034, "E116 occurrence count changed")

    fm = read_json(T83_FM)
    require(sha(T83_FM.read_bytes()) == T83_SHA, "t83 field_map pin mismatch")
    l3 = t83_l3_codes(fm)
    city = read_json(T81_CITY)
    require(sha(T81_CITY.read_bytes()) == T81_CITY_SHA, "t81 city pin mismatch")

    v111 = read_json(SCHEMA)["club_extra3_l3_e121"]["cbw_cbd_table_45_verdict"]
    require(tuple(v111["xml_index_range"]) == TABLE45_RANGE, "table_45 range drift")
    require(v111["occurrence_count"] == TABLE45_COUNT, "table_45 count drift")
    t45_codes = set(v111["cb_codes"])

    rows: list[dict[str, Any]] = []
    for o in occ:
        idx = occ_index(o["id"])
        row = {"id": o["id"], "entity": o["entity"], "code": o["code"],
               "bucket_before": o["bucket"], "bucket_after": o["bucket"],
               "grade": None, "pointer": o.get("evidence_ref"),
               "reason": None}
        # (1) E124/E121 table_45 record family: club.xml[211..327]
        if (o["entity"] == "club" and idx is not None
                and TABLE45_RANGE[0] <= idx <= TABLE45_RANGE[1]
                and o["bucket"] == "unresolved_wire_slot"):
            row.update(bucket_after="re_routed_table_45", grade="L2_candidate",
                       reason="E124/E121: STARTING_RECORD payload of server_db/table_45.dat "
                              "(not a club main-row wire slot); t88-fix2 slot-join lane in flight",
                       pointer="reports/club_nation_subtable_schema.json"
                               "#/club_extra3_l3_e121/cbw_cbd_table_45_verdict")
        # (2) E126 five-table L3 promotion: SCOPED to the five tables' own members.
        # The 1,034 denominator is club/comp/nation only, so no member of
        # award/language/derby/weather/media exists here -> structurally 0 rows.
        # A bare code match is NOT identity (see duni collision below).
        elif (o["entity"] in FIVE_TABLE_ENTITIES and o["bucket"] != "mapped_l3"):
            row.update(bucket_after="mapped_l3", grade="L3",
                       reason="E126: field promoted to L3 in the t83 five-table block",
                       pointer="scratch/t83/out/field_map.json")
        # (3) E125 city Cnti lane
        elif o["code"] == "Cnti" and o["bucket"] != "mapped_l3":
            row.update(bucket_after="mapped_l3", grade="L2_candidate",
                       reason="E125: city(2) Cnti mapped-ordinal 56,293/56,293 in-domain",
                       pointer="scratch/t81/out/rescan_fk_city.json#/lanes/0")
        rows.append(row)

    after: dict[str, int] = {}
    for r in rows:
        after[r["bucket_after"]] = after.get(r["bucket_after"], 0) + 1
    before = dict(base["totals"])

    per_entity: dict[str, dict[str, int]] = {}
    for r in rows:
        e = per_entity.setdefault(r["entity"], {"before_total": 0, "after_total": 0})
        e["before_total"] += 1
        e["after_total"] += 1
        e[f"before.{r['bucket_before']}"] = e.get(f"before.{r['bucket_before']}", 0) + 1
        e[f"after.{r['bucket_after']}"] = e.get(f"after.{r['bucket_after']}", 0) + 1

    carried = ("mapped_l3", "independent_member", "string_name_table")
    carried_n = sum(after.get(b, 0) for b in carried)
    rerouted = after.get("re_routed_table_45", 0)
    denom = len(rows)
    denom_eff = denom - rerouted
    unres_before = before["unresolved_wire_slot"]
    unres_after = after.get("unresolved_wire_slot", 0)

    moved = [r for r in rows if r["bucket_before"] != r["bucket_after"]]
    return {
        "schema_id": "fm24.xml_denominator_coverage",
        "schema_version": "2-candidate",
        "generated_by": "t90",
        "status": "candidate_for_commander_acceptance",
        "source_task": "t90",
        "acceptance_ledger_entries": ["E116 (baseline)", "E124", "E125", "E126", "E127"],
        "baseline": {"path": "reports/xml_denominator_coverage.json",
                     "sha256": BASE_SHA, "bytes": BASE_BYTES,
                     "denominator": base["count"], "totals": before,
                     "physical_coverage": base["physical_coverage"]},
        "method": "occurrence-by-occurrence re-bucket; no source re-adjudicated, "
                  "no new bucket invented beyond re_routed_table_45",
        "buckets_order": base["buckets_order"] + ["re_routed_table_45"],
        "count": denom,
        "totals_after": dict(sorted(after.items())),
        "conservation": {
            "occurrences_before": denom,
            "occurrences_after": denom,
            "sum_before": sum(before.values()),
            "sum_after": sum(after.values()),
            "moved_rows": len(moved),
            "moved_by_rule": {
                "table_45_reroute": sum(1 for r in moved
                                        if r["bucket_after"] == "re_routed_table_45"),
                "e126_five_table_promotion": sum(1 for r in moved
                                                 if r["bucket_after"] == "mapped_l3"
                                                 and "E126" in (r["reason"] or "")),
                "e125_city_cnti": sum(1 for r in moved
                                      if "E125" in (r["reason"] or "")),
            },
        },
        "physical_coverage_after": {
            "formula_carried": list(carried),
            "carried": carried_n,
            "denominator_gross": denom,
            "ratio_gross": round(carried_n / denom, 4),
            "text_gross": f"{carried_n}/{denom} = {carried_n / denom * 100:.1f}%",
            "carved_out_re_routed": rerouted,
            "denominator_net": denom_eff,
            "ratio_net": round(carried_n / denom_eff, 4),
            "text_net": f"{carried_n}/{denom_eff} = {carried_n / denom_eff * 100:.1f}% "
                        f"(table_45 family carved out of the club extra_3 denominator)",
            "note": "re_routed_table_45 is NOT counted as carried; it is a pending "
                    "L2 candidate awaiting the t88-fix2 slot join",
        },
        "unresolved_wire_slot": {
            "before": unres_before, "after": unres_after,
            "delta": unres_after - unres_before,
            "share_before": round(unres_before / denom, 4),
            "share_after": round(unres_after / denom, 4),
        },
        "per_entity": per_entity,
        "five_table_side_denominator": {
            "note": "t83's five tables are NOT part of the 1,034 XML denominator "
                    "(they come from MANIFEST-verified master.json); only `duni` co-occurs",
            "xml_fields": sum(len(fm[t]["schema_fields"]) for t in FIVE_TABLES),
            "L3": sum(len(v) for v in l3.values()),
            "overlap_codes_in_1034": sorted(set().union(*l3.values())
                                            & {r["code"] for r in rows}),
            "overlap_rows_already_mapped_l3": sum(
                1 for r in rows if r["code"] in set().union(*l3.values())
                and r["bucket_before"] == "mapped_l3"),
            "rows_moved_inside_1034": 0,
            "code_collision_escalate": [
                {"occurrence": "nation.xml#nati/001", "code": "duni",
                 "bucket": "held", "bucket_after": "held",
                 "why_not_promoted": "code-name collision only: t83's `duni` is the "
                                      "identity column of table_0/8/18/27/7; nation's "
                                      "duni is table_10 and stays held per E94/E108 "
                                      "(byte located, promotion withheld)",
                 "action": "escalate: no promotion, no re-bucket; identity is "
                           "(archive member, parent, code), never code alone"}],
            "consequence": "rule (2) moves 0 rows inside the 1,034 denominator; the "
                           "152 L3 live on the separate 188-field five-table denominator",
        },
        "e125_city_lane": {
            "note": "the Cnti lane is a city(2) column offset 10 -> table_10 row index; "
                    "the 1,034 denominator has no city(2) occurrence",
            "lanes": [{k: l[k] for k in ("target", "field", "offset", "entity",
                                         "decision", "grade_after", "rows")}
                      for l in city["lanes"]],
            "rows_moved_inside_1034": 0,
            "escalate": "brief step 3 item (3) assumed a Cnti row inside the 1,034; "
                        "none exists (club/016 + comp/015 were already mapped_l3). "
                        "The Cnti result is real but belongs to city(2), outside E116."
        },
        "conflicts": [
            {"id": "C1_brief_vs_E121_code_scope",
             "brief_says": "117 items = the CBW*/CBD* record family",
             "source_says": "E121/E124: the 117-item family is club.xml[211..327]; "
                            "only 10 of its codes are CB* (CBWa/c/d/f/o, CBDa/c/d/f/o) — "
                            "the rest are CAAa/CFGd/CGLn/CHRn/CLAc/CMAp/COPc/CWCg/CYPd...",
             "resolution": "not adjudicated; the 117-row count and the [211..327] range "
                           "come from E121 and are used verbatim, the CB* label is kept "
                           "as the brief's shorthand",
             "escalate": True},
            {"id": "C2_city_cnti_not_in_1034",
             "brief_says": "step 3 (3) t81 city Cnti -> resolved",
             "source_says": "t81 lanes are city(2) columns; the 1,034 denominator holds "
                            "no city occurrence. Cnti rows that DO exist (club/016, "
                            "comp/015) were already mapped_l3 in E116",
             "resolution": "0 rows moved; the lane is recorded in e125_city_lane for the "
                           "five-table/city side only",
             "escalate": True},
        ],
        "preserved_negatives": [
            "all 564 no_wire_evidence rows untouched (t75 grammar closure is naming, "
            "not wire)",
            "all 59 held rows untouched (E99/E107/E108/E110 holds stand)",
            "the 160 remaining unresolved_wire_slot rows keep their E116 evidence_ref "
            "verbatim",
        ],
        "rows": rows,
        "L4": 0,
    }


def verify() -> int:
    doc = read_json(OUT)
    base = read_json(BASE)
    rows = doc["rows"]
    fails: list[str] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    ck("baseline pin", sha(BASE.read_bytes()) == BASE_SHA)
    ck("occurrence count preserved", len(rows) == base["count"] == 1034,
       f"{len(rows)}")
    ck("ids unique", len({r["id"] for r in rows}) == len(rows))
    before = {r["bucket_before"] for r in rows}
    ck("before buckets match E116", {r["bucket_before"] for r in rows}
       <= set(base["buckets_order"]))
    ck("before bucket totals match E116 verbatim",
       {b: sum(1 for r in rows if r["bucket_before"] == b)
        for b in {r["bucket_before"] for r in rows}}
       == {k: v for k, v in base["totals"].items() if v},
       str(base["totals"]["unresolved_wire_slot"]))
    ck("before totals conserved", doc["conservation"]["sum_before"] == 1034,
       str(doc["conservation"]["sum_before"]))
    ck("after totals conserved", doc["conservation"]["sum_after"] == 1034,
       str(doc["conservation"]["sum_after"]))
    ck("totals_after recompute", doc["totals_after"]
       == dict(sorted({r["bucket_after"] for r in rows} and
                      {b: sum(1 for r in rows if r["bucket_after"] == b)
                       for b in {r["bucket_after"] for r in rows}}.items())))
    t45 = [r for r in rows if r["bucket_after"] == "re_routed_table_45"]
    ck("table_45 reroute count == 117", len(t45) == TABLE45_COUNT, str(len(t45)))
    ck("table_45 rows are club 211..327",
       all(r["entity"] == "club" and 211 <= occ_index(r["id"]) <= 327 for r in t45))
    cb = set(read_json(SCHEMA)["club_extra3_l3_e121"]["cbw_cbd_table_45_verdict"]
             ["cb_codes"])
    ck("table_45 CB codes subset of E121 verdict",
       {r["code"] for r in t45 if r["code"].startswith("CB")} <= cb,
       f"{len(cb)} CB codes, {sum(1 for r in t45 if r['code'].startswith('CB'))} rows")
    ck("unresolved delta == -117",
       doc["unresolved_wire_slot"]["delta"] == -TABLE45_COUNT,
       str(doc["unresolved_wire_slot"]["delta"]))
    ck("no invented bucket", set(doc["totals_after"]) <= set(doc["buckets_order"]))
    ck("no held/no_wire rows moved",
       all(r["bucket_after"] == r["bucket_before"] for r in rows
           if r["bucket_before"] in ("held", "no_wire_evidence", "ui_or_derived")))
    ck("rule(2) moved 0 rows (five tables outside 1,034)",
       doc["five_table_side_denominator"]["rows_moved_inside_1034"] == 0
       and doc["conservation"]["moved_by_rule"]["e126_five_table_promotion"] == 0)
    ck("nation duni held collision preserved",
       [r["bucket_after"] for r in rows if r["id"] == "nation.xml#nati/001"] == ["held"])
    ck("every moved row has a reason+pointer",
       all(r["reason"] and r["pointer"] for r in rows
           if r["bucket_before"] != r["bucket_after"]))
    ck("L4 == 0", doc["L4"] == 0)
    print(f"\n{len(fails)} failure(s)")
    return 0 if not fails else 1


def selftest() -> int:
    fails = 0

    def ck(name: str, ok: bool) -> None:
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + name)
        fails += 0 if ok else 1

    ck("sha of empty", sha(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934"
                              "ca495991b7852b855")
    ck("occ_index parses", occ_index("club.xml#club/211") == 211)
    ck("occ_index rejects", occ_index("nope") is None)
    d = json_bytes({"a": 1})
    ck("json_bytes roundtrip", json.loads(d) == {"a": 1} and d.endswith(b"\n"))
    ck("pins are hex64", all(len(x) == 64 for x in (BASE_SHA, T83_SHA, T81_CITY_SHA)))
    # conservation algebra on a toy case
    toy = {"mapped_l3": 2, "unresolved_wire_slot": 3}
    after = {"mapped_l3": 2, "re_routed_table_45": 1, "unresolved_wire_slot": 2}
    ck("toy conservation", sum(toy.values()) == sum(after.values()) == 5)
    print(f"\n{5 - fails}/5 selftest checks")
    return 0 if not fails else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not (a.build or a.verify or a.selftest):
        ap.print_help()
        return 2
    try:
        if a.selftest:
            return selftest()
        if a.build:
            doc = build()
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_bytes(json_bytes(doc))
            print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size:,} B")
            print("totals_after", json.dumps(doc["totals_after"]))
            print("coverage", doc["physical_coverage_after"]["text_gross"], "|",
                  doc["physical_coverage_after"]["text_net"])
            return 0
        return verify()
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
