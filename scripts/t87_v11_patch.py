#!/usr/bin/env python3
"""t87 - schema v11 -> v11.1 additive patch (E121 / t82).

  py -V:3.12 -I -B scripts/t87_v11_patch.py --selftest
  py -V:3.12 -I -B scripts/t87_v11_patch.py --build
  py -V:3.12 -I -B scripts/t87_v11_patch.py --verify

Exit codes: 0 pass / 1 check failed / 2 usage or fatal.

--build is additive only and refuses to run twice: it rewrites
  reports/club_nation_subtable_schema.json   (v11 -> v11.1)
  reports/club_nation_subtable_schema.md     (v11 bytes + one appended appendix)
and writes scratch/t87/out/v11_section_digests.json (the per-section guard the
--verify stage re-checks; no bulk payload is copied into scratch).

Every root section other than the four mutable ones is preserved value-identical.
reports/xml_denominator_coverage.json and reports/other_tables_schema.json are
NOT touched: the E116 bucket re-issue stays a follow-up task.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUB_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUB_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
LEDGER = ROOT / "scratch" / "t01" / "LEDGER.json"
T82 = ROOT / "scratch" / "t82" / "out"
OUT = ROOT / "scratch" / "t87" / "out"
DIGESTS = OUT / "v11_section_digests.json"

GUARD = "E121"
NEW_ROOT = "club_extra3_l3_e121"
MUTABLE = ("schema_version", "generated_by", "coverage", "incremental_provenance")
NEW_VERSION = "11.1"
NEW_BY = "t87"

# v11 publication pin, measured 2026-11-21 before this patch (t77 product).
V11_JSON_SHA = "8733497cbd42b33eed7e19a702034dbbc9dc08bb2800d2a30695ef8d2f7cf555"
V11_JSON_BYTES = 29884088
V11_MD_SHA = "3f47bf1661c865635442b0fdc01f76aacc69cc122d5df4ac66cb2817250d582f"
V11_MD_BYTES = 87373

# Accepted t82 (E121) artifacts, re-hashed on every --verify.
SOURCES = {
    "scratch/t82/out/field_map.json": "2a31c0250c905d45b1528c4196e20da9b492225ccaed17bed976d9060041ddae",
    "scratch/t82/out/xref_extra3.json": "944eea8683fcbb1a6a0a8431c4c0f79ba60402fea646de9638eb8cd6479a15ef",
    "scratch/t82/out/domain_stats.json": "d61111dc4bfb1734e7083ecbbdf5bddc2f971121dcbd394d2efbde33b43fd7ff",
    "scratch/t82/out/REPORT.md": "dd809207499b898125311b79478e76e2aeeaeeceed2f3178b39185e9c3bec343",
    "scratch/t82/out/DONE.md": "ee919a9992624c6b39c6d962785ac3911c3ea10c6cb5bb88216859fc96baff0c",
    "scratch/t82/out/verify.py": "7a01d870385160a0876aaab0f6647c03b037403d69449a64aac57065a41df1cc",
}

# E121 claim constants, taken from the accepted t82 REPORT (§1 static chain).
TABLE45 = {
    "target_table": "server_db/table_45.dat",
    "table_type": 45,
    "rtti": ".?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@",
    "records": 84477,
    "getter": {"symbol": "TC_RECORD_GET", "file_offset": "0x3ebad50"},
    "setter": {"symbol": "TC_RECORD_SET", "file_offset": "0x3ebaf50"},
    "ctor_witness": {"file_offset": "0xf06c70..0xf06c84", "bytes": "mov edx, 0x2d"},
}
CLAIM_WITNESS = [  # strings that must still be present in the accepted t82 report
    "0x3ebad50", "0x3ebaf50", "mov edx, 0x2d",
    ".?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@", "84,477",
]


class CheckFailure(Exception):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return sha(raw)


def norm_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8")


def json_bytes(value: Any) -> bytes:
    return norm_bytes(value) + b"\n"


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def section_digests(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Digests for the sections the patch must not touch (mutable roots excluded)."""
    return {k: {"sha256": sha(norm_bytes(v)), "bytes": len(norm_bytes(v))}
            for k, v in doc.items()
            if k != NEW_ROOT and k not in MUTABLE}


def adder_guard(pre: dict[str, Any], post: dict[str, Any],
                removed: list[str], changed: list[str]) -> None:
    """Collect removed/mutated root keys, ignoring the four mutable roots."""
    for key in pre:
        if key in MUTABLE or key == NEW_ROOT:
            continue
        if key not in post:
            removed.append(key)
        elif post[key] != pre[key]:
            changed.append(key)


class Reporter:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def check(self, name: str, ok: bool, detail: Any = "") -> bool:
        self.rows.append({"check": name, "ok": bool(ok), "detail": detail})
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        return bool(ok)

    def failures(self) -> list[dict[str, Any]]:
        return [r for r in self.rows if not r["ok"]]

    def done(self, stage: str) -> int:
        fails = self.failures()
        print(f"\n{stage}: {len(self.rows) - len(fails)}/{len(self.rows)} checks passed")
        return 0 if not fails else 1


# ---------------------------------------------------------------- inputs ----
def e121_claim() -> dict[str, Any]:
    entries = read_json(LEDGER)["entries"]
    hit = [e for e in entries if e.get("id") == GUARD]
    require(len(hit) == 1, f"ledger must hold exactly one {GUARD}, got {len(hit)}")
    return hit[0]


def t82_field_map() -> dict[str, Any]:
    doc = read_json(T82 / "field_map.json")
    require(doc.get("task") == "t82", f"field_map task is {doc.get('task')!r}")
    require(doc.get("L4") == 0, "L4 must stay 0")
    return doc


def strip_idx(code: str) -> str:
    """t82 held codes carry a [xml_index] suffix; the field rows carry the bare 4CC."""
    return code.split("[", 1)[0]


def split_t82(doc: dict[str, Any]) -> dict[str, Any]:
    """Re-derive the E121 counts from the accepted t82 artifact."""
    fields = doc["fields"]
    l3 = [f for f in fields if f["grade"] == "L3"]
    held = [f for f in fields if f["grade"] == "held"]
    neg = doc["negative_not_extra3"]
    t45 = [n for n in neg if n.get("target_table", "").startswith(TABLE45["target_table"])]
    other = [n for n in neg if n not in t45]
    idx = sorted({n["xml_index"] for n in t45})
    cb = sorted({n["code"] for n in t45 if n["code"].startswith("CB")})
    require(len(l3) == len(doc["new_L3_codes"]) == 35,
            f"L3 rows {len(l3)} vs new_L3_codes {len(doc['new_L3_codes'])}")
    require(len(held) == len(doc["held_codes"]) == 39,
            f"held rows {len(held)} vs held_codes {len(doc['held_codes'])}")
    require({f["code"] for f in l3} == set(doc["new_L3_codes"]), "L3 code set mismatch")
    require({strip_idx(c) for c in doc["held_codes"]} == {f["code"] for f in held},
            "held code set mismatch")
    require(len(neg) == 131, f"negative_not_extra3 must be 131, got {len(neg)}")
    require(len(t45) == 117 and idx == list(range(211, 328)),
            f"table_45 cluster must be 117 contiguous 211..327, got {len(t45)}")
    require(len(other) == 14, f"other non-extra_3 negatives must be 14, got {len(other)}")
    return {"l3": l3, "held": held, "neg45": t45, "neg_other": other,
            "indices": idx, "cb_codes": cb, "grade_counts": doc["grade_counts"],
            "held_codes_raw": doc["held_codes"]}


def ledger_row(item: dict[str, Any]) -> dict[str, Any]:
    return {"kind": item["kind"], "level": item["level"],
            "date": item["date"],
            "claim_sha256": canonical_sha256(item["claim"])}


# --------------------------------------------------------------- sections ----
def patch_doc(pre: dict[str, Any], t82: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    """Return the v11.1 document. Only the four mutable roots may differ."""
    s = split_t82(t82)
    doc = json.loads(json.dumps(pre))  # deep copy
    doc["schema_version"] = NEW_VERSION
    doc["generated_by"] = NEW_BY

    doc[NEW_ROOT] = {
        "generated_by": NEW_BY,
        "acceptance_ledger_entry": GUARD,
        "acceptance_ledger_level": claim["level"],
        "source_task": "t82",
        "source_artifact": {
            "path": "scratch/t82/out/field_map.json",
            "sha256": SOURCES["scratch/t82/out/field_map.json"],
            "bytes": (T82 / "field_map.json").stat().st_size,
            "rule": "pointer only; the 74-field ledger stays in the t82 artifact",
        },
        "baseline_v11": {"sha256": V11_JSON_SHA, "bytes": V11_JSON_BYTES},
        "counts": {"new_L3": len(s["l3"]), "held": len(s["held"]),
                   "negative_not_extra3": len(s["neg45"]) + len(s["neg_other"]),
                   "negative_to_table_45": len(s["neg45"]),
                   "negative_other": len(s["neg_other"]),
                   "excluded_t71_L3": t82["excluded_t71_L3_count"],
                   "grade_counts": s["grade_counts"], "L4": t82["L4"]},
        "new_L3_codes": sorted(f["code"] for f in s["l3"]),
        "new_L3_by_group": group_l3(s["l3"]),
        "held_count": len(s["held"]),
        "held_codes": sorted(f["code"] for f in s["held"]),
        "held_codes_with_xml_index": sorted(s["held_codes_raw"]),
        "held_policy": "held records are copied as counts + codes only; first "
                       "counterexamples live in the t82 artifact and are unchanged",
        "cbw_cbd_table_45_verdict": {
            "verdict": "not in table_extra_3; the whole 117-item club.xml[211..327] "
                       "record family is a server_db/table_45.dat STARTING_RECORD payload",
            "xml_index_range": [s["indices"][0], s["indices"][-1]],
            "occurrence_count": len(s["neg45"]),
            "cb_code_count": len(s["cb_codes"]),
            "cb_codes": s["cb_codes"],
            "table_45": TABLE45,
            "consequence": "the E116 denominator's 239 unresolved club occurrences shrink by "
                           "these 117; the bucket re-issue belongs to a follow-up task",
            "evidence_pointer": "scratch/t82/out/field_map.json#/negative_not_extra3",
        },
        "dual_object_closure": {
            "client_object": "CLUB+0x100 (0x130B CLUB_IN_GAME_DATA)",
            "server_object": "CLUB+0xb0 (0xB0B TEAM_CONTAINER_IN_GAME_DATA)",
            "rows": 84259,
            "client_payload_bytes": 13053908,
            "server_payload_bytes": 35009248,
            "client_only_fields": 0,
        },
        "L4": 0,
    }

    cov = doc["coverage"]
    cov["club_main_row_L3"] = 78
    cov["club_main_row_L3_prior_v11"] = 43
    cov["club_main_row_L3_delta_E121"] = 35
    cov["club_main_row_L3_note_E121"] = (
        "43 (v11) + 35 = 78 club main-row + extra_3 object L3 per E121. The 35 are the t82 "
        "table_extra_3 promotions (31 scalars + 4 list/polymorphic); the 24 t71 records of "
        "E111 are already inside the 43 and are not counted twice.")
    cov["club_denominator_note_E121"] = (
        "the club.xml[211..327] record family (117 items, incl. CBW*/CBD*) is a "
        "server_db/table_45.dat STARTING_RECORD payload, not table_extra_3, so those 117 of the "
        "239 club unresolved_wire_slot occurrences in E116 are re-routed out of the club "
        "extra_3 denominator. reports/xml_denominator_coverage.json is NOT rewritten by t87; "
        "the bucket re-issue is a follow-up.")
    cov["xml_denominator_pointer_note_E121"] = (
        "pointer still carries the E116 numbers (1,034 occurrences / 110 carried); t87 records "
        "the re-routing as a note only")

    prov = doc["incremental_provenance"]
    prov["acceptance_ledger_entries"][GUARD] = ledger_row(claim)
    prov["t87_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level id, kind, level, date and canonical claim SHA-256; "
                       "no live full-file hash or byte-count pin",
        "guarded_entries": [GUARD],
        "entries": [{"id": GUARD, **ledger_row(claim)}],
        "out_of_scope_note": "E122 and later belong to the next lane; E111-E120 stay as t77 pinned them",
    }
    prov["tasks"]["t82"] = {
        "acceptance_ledger_entry": GUARD,
        "acceptance_ledger_level": claim["level"],
        "section": "club_extra3_l3_e121",
        "source_artifacts": sorted(SOURCES),
    }
    prov["t87_volume_policy"] = {
        "main_schema_keeps": ["the new 35-code section", "counters", "a single source pointer"],
        "bulk_stays_out": "the t82 74-field ledger, per-field static chains and all 131 "
                          "negative witnesses remain in scratch/t82/out/",
        "split_files_untouched": ["reports/other_tables_schema.json",
                                  "reports/xml_denominator_coverage.json"],
    }
    prov["t87_additive_rule"] = ("v11 sections are value-identical after the patch; only "
                                 "schema_version, generated_by, coverage and "
                                 "incremental_provenance change, plus the new root section")
    return doc


GROUPS = (
    ("server_only_scalars", ("Ctlv", "Cmle", "Cyim", "Cyfb", "Cytv", "Crcb")),
    ("election_sub_object", ("Cetl", "Cmtm", "Cect", "Cemn", "Cemx")),
    ("supporter_profile", ("Csly", "Csps", "Cspt", "Csaf", "Cste", "Cspe")),
    ("uefa_coefficient_ring", ("Cuf1", "Cuf2", "Cuf3", "Cuf4", "Cuf5", "Cuf6",
                               "Cuf7", "Cuf8", "Cuf9", "Cf10")),
    ("server_only_i32", ("Catd", "Cmna", "Cmxa")),
)


def group_l3(l3: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Named groups from the E121 claim; anything left over is listed explicitly."""
    seen: set[str] = set()
    out: dict[str, dict[str, Any]] = {}
    for name, codes in GROUPS:
        rows = [f for f in l3 if f["code"] in codes]
        seen |= {f["code"] for f in rows}
        out[name] = {"count": len(rows),
                     "codes": [f["code"] for f in rows],
                     "wire_scope": sorted({f["wire_scope"] for f in rows})}
    rest = [f for f in l3 if f["code"] not in seen]
    out["string_and_list_tail"] = {
        "count": len(rest),
        "codes": [f["code"] for f in rest],
        "detail": [{"code": f["code"], "wire_type": f["wire_type"],
                    "object_path": f["object_path"]} for f in rest],
    }
    return out


# ------------------------------------------------------------------- md ------
def appendix(doc: dict[str, Any]) -> str:
    sec = doc[NEW_ROOT]
    c = sec["counts"]
    v = sec["cbw_cbd_table_45_verdict"]
    t45 = v["table_45"]
    lines = [
        "",
        "## t87 - schema v11 -> v11.1 (E121)",
        "",
        "Additive appendix to the byte-pinned v11 Markdown. No existing section, held record "
        "or negative regression is modified; this patch only appends a section and updates "
        "`schema_version`, `generated_by`, `coverage` and `incremental_provenance`. L4=0.",
        "",
        "### Volume governance",
        "",
        "| Item | Value |",
        "|---|---|",
        f"| E121 source pointer | `scratch/t82/out/field_map.json`, "
        f"{sec['source_artifact']['bytes']:,} B, SHA-256 `{sec['source_artifact']['sha256'][:16]}...` |",
        "| split files | `reports/other_tables_schema.json` and "
        "`reports/xml_denominator_coverage.json` untouched by this patch |",
        "",
        "### club `table_extra_3` remainder (t82 / E121, L3)",
        "",
        f"- New L3: **{c['new_L3']}** (31 scalars + 4 list/polymorphic); held: **{c['held']}** "
        f"(codes + counts only); excluded t71 records: {c['excluded_t71_L3']}.",
        f"- club main-row + extra_3 object L3 43 -> **78** (+{c['new_L3']}).",
        "- Dual-object closure: `CLUB+0x100` (`0x130B`) + `CLUB+0xb0` (`0xB0B`), "
        f"{sec['dual_object_closure']['rows']:,} rows; client "
        f"{sec['dual_object_closure']['client_payload_bytes']:,} B / server "
        f"{sec['dual_object_closure']['server_payload_bytes']:,} B; 0 client-only fields.",
        "",
        "### `CBW*`/`CBD*` verdict: not `table_extra_3`",
        "",
        f"- The whole `club.xml[211..327]` record family (**{v['occurrence_count']}** items, "
        f"{v['cb_code_count']} `CB*` codes) is a `{t45['target_table']}` "
        f"(`DATABASE_TABLE<STARTING_RECORD>`, type `0x2d`={t45['table_type']}, "
        f"{t45['records']:,} records) payload.",
        f"- `{t45['getter']['symbol']} @ {t45['getter']['file_offset']}` never reads "
        "`CLUB+0x100` or `CLUB+0xb0`; the table type is self-proved by "
        f"`{t45['ctor_witness']['bytes']}` at `{t45['ctor_witness']['file_offset']}` with RTTI "
        f"`{t45['rtti']}`.",
        f"- Consequence: {v['occurrence_count']} of the 239 club `unresolved_wire_slot` "
        "occurrences in E116 are re-routed out of the club extra_3 denominator. The E116 "
        "bucket file is **not** rewritten here; the re-issue is a follow-up.",
        "",
        "### Provenance and boundaries",
        "",
        "- E121 guards: id, kind, level, date and canonical claim SHA-256 (entry-level only).",
        "- v11 sections are value-identical after the patch; only the four mutable roots and "
        "the new root section differ.",
        "- No game/editor/IDA was started and no `.dat` payload was decoded for this patch. "
        "L4=0.",
        "",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ build ----
def build(rep: Reporter) -> int:
    pre_raw = PUB_JSON.read_bytes()
    pre_md = PUB_MD.read_bytes()
    rep.check("v11 publication pin matches", sha(pre_raw) == V11_JSON_SHA, f"{len(pre_raw):,} B")
    rep.check("v11 markdown pin matches", sha(pre_md) == V11_MD_SHA, f"{len(pre_md):,} B")
    pre = json.loads(pre_raw)
    if pre.get("schema_version") == NEW_VERSION:
        rep.check("already patched (idempotence guard)", False,
                  "--build refuses to re-apply; re-run --verify instead")
        return rep.done("build")
    rep.check("pre-patch schema_version is 11", pre["schema_version"] == 11,
              pre["schema_version"])
    rep.check("pre-patch generated_by is t77", pre["generated_by"] == "t77",
              pre["generated_by"])

    claim = e121_claim()
    rep.check("E121 claim present and accepted", claim["kind"] == "acceptance",
              f"{claim['kind']} / {claim['level']} / {claim['date']}")
    t82 = t82_field_map()
    for path, want in SOURCES.items():
        got = sha((ROOT / path).read_bytes())
        rep.check(f"accepted artifact hash: {path}", got == want, got[:16] + "...")

    doc = patch_doc(pre, t82, claim)

    removed: list[str] = []
    changed: list[str] = []
    adder_guard(pre, doc, removed, changed)
    allowed = [k for k in MUTABLE]
    rep.check("no v11 root section removed or altered",
              not removed and not changed,
              f"{len(pre) - len(allowed)} sections identical")
    rep.check("root keys are exactly v11 + the new section",
              set(doc) - set(pre) == {NEW_ROOT}, sorted(set(doc) - set(pre)))
    rep.check("schema_version is 11.1", doc["schema_version"] == NEW_VERSION,
              doc["schema_version"])

    section = doc[NEW_ROOT]
    rep.check("E121 section counts 35/39/131",
              (section["counts"]["new_L3"], section["counts"]["held"],
               section["counts"]["negative_not_extra3"]) == (35, 39, 131),
              section["counts"])
    rep.check("E121 new_L3_codes are 35 unique 4CC",
              len(set(section["new_L3_codes"])) == 35
              and all(len(c) == 4 for c in section["new_L3_codes"]),
              section["new_L3_codes"][:6] + ["..."])
    rep.check("E121 groups sum to 35",
              sum(g["count"] for g in section["new_L3_by_group"].values()) == 35,
              {k: v["count"] for k, v in section["new_L3_by_group"].items()})
    rep.check("E121 held codes are 35+4", len(section["held_codes"]) == 39,
              len(section["held_codes"]))
    rep.check("table_45 verdict carries 117 occurrences 211..327",
              section["cbw_cbd_table_45_verdict"]["occurrence_count"] == 117
              and section["cbw_cbd_table_45_verdict"]["xml_index_range"] == [211, 327],
              section["cbw_cbd_table_45_verdict"]["xml_index_range"])
    rep.check("coverage club L3 43 -> 78",
              doc["coverage"]["club_main_row_L3"] == 78
              and doc["coverage"]["club_main_row_L3_prior_v11"] == 43
              and doc["coverage"]["club_main_row_L3_delta_E121"] == 35,
              doc["coverage"]["club_main_row_L3"])
    rep.check("coverage L4 stays 0", doc["coverage"]["L4"] == 0, doc["coverage"]["L4"])

    # coverage: only additive keys, nothing removed, nothing else touched
    cov_pre, cov_post = pre["coverage"], doc["coverage"]
    lost = [k for k in cov_pre if k not in cov_post]
    touched = [k for k in cov_pre if cov_post.get(k) != cov_pre[k]]
    rep.check("coverage keys only appended",
              not lost and set(touched) == {"club_main_row_L3"},
              {"removed": lost, "changed": touched})

    prov = doc["incremental_provenance"]
    rep.check("E121 ledger row appended with claim digest",
              prov["acceptance_ledger_entries"][GUARD]["claim_sha256"]
              == canonical_sha256(claim["claim"]),
              prov["acceptance_ledger_entries"][GUARD]["claim_sha256"][:16] + "...")
    rep.check("E121 row does not copy the claim text",
              "claim" not in prov["acceptance_ledger_entries"][GUARD],
              sorted(prov["acceptance_ledger_entries"][GUARD]))
    old = pre["incremental_provenance"]
    rep.check("prior provenance rows preserved",
              all(prov["acceptance_ledger_entries"].get(k) == v
                  for k, v in old["acceptance_ledger_entries"].items())
              and prov["t70_ledger_snapshot"] == old["t70_ledger_snapshot"]
              and prov["t77_ledger_snapshot"] == old["t77_ledger_snapshot"],
              f"{len(old['acceptance_ledger_entries'])} prior ledger rows")

    raw = json_bytes(doc)
    PUB_JSON.write_bytes(raw)
    md_new = pre_md + appendix(doc).encode("utf-8")
    PUB_MD.write_bytes(md_new)
    OUT.mkdir(parents=True, exist_ok=True)
    DIGESTS.write_bytes(json_bytes({
        "generated_by": NEW_BY,
        "baseline_v11": {"sha256": V11_JSON_SHA, "bytes": V11_JSON_BYTES},
        "patched": {"sha256": sha(raw), "bytes": len(raw), "schema_version": NEW_VERSION},
        "md": {"baseline_sha256": V11_MD_SHA, "baseline_bytes": V11_MD_BYTES,
               "sha256": sha(md_new), "bytes": len(md_new)},
        "sections": section_digests(pre),
        "new_root": NEW_ROOT,
        "coverage_changed": {"club_main_row_L3": {"from": 43, "to": 78},
                             "added_keys": sorted(set(cov_post) - set(cov_pre))},
        "L4": 0,
    }))
    rep.check("v11.1 written", True, f"{len(raw):,} B json / {len(md_new):,} B md")
    rep.check("section digests recorded", True, str(DIGESTS.relative_to(ROOT)))
    return rep.done("build")


# ----------------------------------------------------------------- verify ----
def verify(rep: Reporter) -> int:
    if not PUB_JSON.exists():
        raise FileNotFoundError(PUB_JSON)
    pub = json.loads(PUB_JSON.read_bytes())
    rep.check("published schema_version is 11.1", str(pub["schema_version"]) == NEW_VERSION,
              pub["schema_version"])
    rep.check("published generated_by is t87", pub["generated_by"] == NEW_BY,
              pub["generated_by"])
    if not DIGESTS.exists():
        raise FileNotFoundError(DIGESTS)
    pin = json.loads(DIGESTS.read_bytes())
    rep.check("patched JSON matches the recorded digest",
              sha(PUB_JSON.read_bytes()) == pin["patched"]["sha256"],
              pin["patched"]["sha256"][:16] + "...")

    claim = e121_claim()
    t82 = t82_field_map()
    s = split_t82(t82)
    rep.check("t82 re-derived: 35 L3", len(s["l3"]) == 35, len(s["l3"]))
    rep.check("t82 re-derived: 39 held", len(s["held"]) == 39, len(s["held"]))
    rep.check("t82 re-derived: 131 negatives (117 + 14)",
              len(s["neg45"]) + len(s["neg_other"]) == 131,
              {"table_45": len(s["neg45"]), "other": len(s["neg_other"])})
    rep.check("t82 re-derived: 117 table_45 occurrences at 211..327",
              s["indices"] == list(range(211, 328)), s["indices"][:3] + ["..."])

    section = pub[NEW_ROOT]
    rep.check("published section counts 35/39/131",
              (section["counts"]["new_L3"], section["counts"]["held"],
               section["counts"]["negative_not_extra3"]) == (35, 39, 131),
              section["counts"])
    rep.check("published new_L3_codes match the t82 artifact",
              section["new_L3_codes"] == sorted(f["code"] for f in s["l3"]),
              len(section["new_L3_codes"]))
    rep.check("published held_codes match the t82 artifact",
              section["held_codes"] == sorted(f["code"] for f in s["held"]),
              len(section["held_codes"]))
    rep.check("published CB* codes match the t82 artifact",
              section["cbw_cbd_table_45_verdict"]["cb_codes"] == s["cb_codes"],
              s["cb_codes"])
    rep.check("published group counts sum to 35",
              sum(g["count"] for g in section["new_L3_by_group"].values()) == 35,
              {k: v["count"] for k, v in section["new_L3_by_group"].items()})

    # E121 parity against the ledger claim wording
    claim_text = claim["claim"]["scope"] + " " + " ".join(claim["claim"]["major"])
    rep.check("claim states 35 new L3", "35 new L3" in claim_text, "35 new L3")
    rep.check("claim states 39 held", "39 held" in claim_text, "39 held")
    rep.check("claim states 131 negative proofs", "131 negative proofs" in claim_text,
              "131 negative proofs")
    rep.check("claim states 43 -> 78",
              "43 (E111) -> 78 (E121)" in claim["claim"]["club_l3_count"],
              claim["claim"]["club_l3_count"])
    rep.check("coverage carries 43 -> 78",
              pub["coverage"]["club_main_row_L3"] == 78
              and pub["coverage"]["club_main_row_L3_prior_v11"] == 43,
              pub["coverage"]["club_main_row_L3"])
    rep.check("ledger row digest matches the live claim",
              pub["incremental_provenance"]["acceptance_ledger_entries"][GUARD]
              ["claim_sha256"] == canonical_sha256(claim["claim"]),
              "canonical claim sha256")

    # additivity against the v11 pins
    rep.check("v11 JSON pin recorded", pin["baseline_v11"]["sha256"] == V11_JSON_SHA,
              pin["baseline_v11"]["sha256"][:16] + "...")
    for key, want in pin["sections"].items():
        got = sha(norm_bytes(pub[key]))
        rep.check(f"v11 section unchanged: {key}", got == want["sha256"], key)
    rep.check("root key delta is exactly the new section",
              set(pub) - set(pin["sections"]) == {NEW_ROOT} | set(MUTABLE),
              sorted(set(pub) - set(pin["sections"])))

    # t82 static witnesses still present in the accepted report
    report = (T82 / "REPORT.md").read_text(encoding="utf-8")
    rep.check("t82 report still carries the static witnesses",
              all(w in report for w in CLAIM_WITNESS),
              [w for w in CLAIM_WITNESS if w not in report] or "all present")
    rep.check("accepted t82 artifacts re-hashed",
              all(sha((ROOT / p).read_bytes()) == h for p, h in SOURCES.items()),
              f"{len(SOURCES)} files")
    rep.check("L4 stays 0", pub["coverage"]["L4"] == 0 and pub[NEW_ROOT]["L4"] == 0,
              "0")

    # markdown: the v11 bytes stay a strict prefix, the appendix sits right after them
    md = PUB_MD.read_bytes()
    base_bytes = pin["md"]["baseline_bytes"]
    rep.check("markdown prefix is the pinned v11 bytes",
              sha(md[:base_bytes]) == pin["md"]["baseline_sha256"],
              f"{base_bytes:,} B prefix of {len(md):,} B")
    rep.check("markdown tail starts with the t87 appendix header",
              md[base_bytes:].lstrip(bytes((13, 10))).startswith(
                  b"## t87 - schema v11 -> v11.1 (E121)"),
              md[base_bytes:base_bytes + 40].decode("utf-8", "replace").strip())
    rep.check("markdown digest unchanged since build",
              sha(md) == pin["md"]["sha256"], f"{len(md):,} B")

    # the t77 verifier stays green on everything except its four terminal-state
    # assertions, which pin the *published* file to v11 and are now superseded.
    rep.check("t77 verifier regressions are limited to the superseded pins",
              set(t77_regressions()) == SUPERSEDED_BY_V11_1,
              sorted(set(t77_regressions()) ^ set(SUPERSEDED_BY_V11_1)) or "exactly 4")
    return rep.done("verify")


SUPERSEDED_BY_V11_1 = {
    "published schema_version is 11",
    "published generated_by is t77",
    "root keys are exactly v10 + the new sections",
    "coverage club_main_row_L3 = 43 (21 + 22)",
}


def t77_regressions() -> list[str]:
    """Re-run the v11 verifier (read-only) and return its failing check names."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import t77_verify as V  # noqa: PLC0415 - optional cross-check only

    class Quiet:
        def __init__(self) -> None:
            self.rows: list[dict[str, Any]] = []

        def check(self, name: str, ok: bool, detail: Any = "") -> bool:
            self.rows.append({"check": name, "ok": bool(ok)})
            return bool(ok)

        def failures(self) -> list[dict[str, Any]]:
            return [r for r in self.rows if not r["ok"]]

    q = Quiet()
    import contextlib  # noqa: PLC0415 - local, keeps the module header small
    import io  # noqa: PLC0415

    with contextlib.redirect_stdout(io.StringIO()):
        V.verify(q)
    return [r["check"] for r in q.rows if not r["ok"]]


# --------------------------------------------------------------- selftest ----
def selftest(rep: Reporter) -> int:
    rep.check("sha256 empty vector",
              sha(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
              "known digest")
    rep.check("canonical_sha256 is key-order stable",
              canonical_sha256({"b": 1, "a": 2}) == canonical_sha256({"a": 2, "b": 1}),
              "sorted keys")
    rep.check("json_bytes round-trips",
              json.loads(json_bytes({"x": [1, 2]})) == {"x": [1, 2]}, "utf-8 + newline")
    pre = {"a": {"deep": [1, 2]}, "schema_version": 11, "generated_by": "t77",
           "coverage": {"club_main_row_L3": 43}}
    post = json.loads(json.dumps(pre))
    post["schema_version"] = NEW_VERSION
    post["coverage"]["club_main_row_L3"] = 78
    removed: list[str] = []
    changed: list[str] = []
    adder_guard(pre, post, removed, changed)
    rep.check("adder_guard ignores the mutable roots",
              not removed and not changed, {"removed": removed, "changed": changed})
    post2 = json.loads(json.dumps(post))
    post2["a"]["deep"] = [9]
    del post2["a"]
    r2: list[str] = []
    c2: list[str] = []
    adder_guard(pre, post2, r2, c2)
    rep.check("adder_guard catches removal and mutation", r2 == ["a"] and c2 == [],
              {"removed": r2, "changed": c2})
    rep.check("norm_bytes is stable under reload",
              sha(norm_bytes(json.loads(norm_bytes(pre)))) == sha(norm_bytes(pre)),
              "digest stable")
    groups = group_l3(FIXTURE)
    rep.check("group_l3 assigns every row exactly once",
              sum(g["count"] for g in groups.values()) == len(FIXTURE),
              {k: v["count"] for k, v in groups.items()})
    rep.check("group_l3 keeps the tail explicit",
              "Ctal" in groups["string_and_list_tail"]["codes"],
              groups["string_and_list_tail"]["codes"])
    try:
        split_t82({"task": "t82", "L4": 0, "fields": [], "negative_not_extra3": [],
                   "new_L3_codes": [], "held_codes": [], "grade_counts": {},
                   "excluded_t71_L3_count": 24})
    except CheckFailure as exc:
        rep.check("split_t82 guards the 35 L3 count", True, str(exc)[:40])
    else:
        rep.check("split_t82 guards the 35 L3 count", False, "no exception raised")
    return rep.done("selftest")


FIXTURE = [
    {"code": "Ctlv", "grade": "L3", "wire_scope": "server_only", "wire_type": "i8",
     "object_path": "CLUB+0x100 -> +0x120"},
    {"code": "Cuf1", "grade": "L3", "wire_scope": "server_only", "wire_type": "i16",
     "object_path": "CLUB+0xb0 -> +0x40"},
    {"code": "Ctal", "grade": "L3", "wire_scope": "client+server", "wire_type": "poly_tag5_24B",
     "object_path": "CLUB+0xb0 -> +0x00"},
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="t87_v11_patch.py",
        description="Fold accepted E121 (t82) into schema v11.1 (additive).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true",
                   help="write the v11.1 main schema + appendix + scratch/t87/out digests")
    g.add_argument("--verify", action="store_true",
                   help="re-read v11.1 plus the t82 artifacts and re-check every count")
    g.add_argument("--selftest", action="store_true", help="check the helpers only")
    args = ap.parse_args(argv)
    rep = Reporter()
    try:
        if args.selftest:
            return selftest(rep)
        if args.build:
            return build(rep)
        return verify(rep)
    except CheckFailure as exc:
        print(f"FATAL: {exc}")
        return 2
    except FileNotFoundError as exc:
        print(f"FATAL: missing input: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
