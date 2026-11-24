#!/usr/bin/env python3
"""t145 — Wave 13+14 Final Master Regression Suite, Protected-File Guardrail Check & Ledger Candidates v2.

Runs --selftest across all 23 core Wave 13+14 verified scripts + t01_anchors, pins SHA-256
manifests of key deliverables, verifies reports/ and scratch/t01/LEDGER.json are 100% untouched,
and emits scratch/t145/out/{regression_matrix.json, ledger_candidates_v2.json, DONE.md}.

Usage:
    py -V:3.12 -B scripts/t145_final_regression.py            # real rerun
    py -V:3.12 -B scripts/t145_final_regression.py --selftest # same real rerun
    py -V:3.12 -B scripts/t145_final_regression.py --cached   # read last matrix only
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scratch" / "t145" / "out"

TESTS = [
    ("t01_anchors", ["scripts/t01_anchors.py"], "Baseline anchor verification"),
    ("t106_special_members", ["scripts/t106_special_members.py", "--selftest"], "13/13 special members + summary.dat (28.4 MB, diff=0)"),
    ("t112_fm24_reader", ["scripts/t112_fm24_reader.py", "--selftest"], "Pure-Python reader v1 (66/79 tables)"),
    ("t119_unicorn_last5", ["scripts/t119_unicorn_last5.py", "--selftest"], "Unicorn last 5 tables closure (79/79)"),
    ("t120_people_unicorn", ["scripts/t120_people_unicorn.py", "--selftest"], "Unicorn people_db 5/5 person classes (3,000/3,000)"),
    ("t121_master_79of79", ["scripts/t121_master_79of79.py", "--selftest"], "79/79 master wire trace + 1,104 L3 join"),
    ("t122_people_l3_schema", ["scripts/t122_people_l3_schema.py", "--selftest"], "5-class virtual base & 177 type-specific 4CC joins"),
    ("t123_basic_people_l3", ["scripts/t123_basic_people_l3.py", "--selftest"], "basic_people_db.dat 658,011 rows (diff=0)"),
    ("t125_big3_gap_closure", ["scripts/t125_big3_gap_closure.py", "--selftest"], "Big-3 L3 v3 (76.2% net persisted)"),
    ("t126_player_attributes_l3", ["scripts/t126_player_attributes_l3.py", "--selftest"], "54/54 PDxx GET==SET + 69B PLAYER_DATA"),
    ("t127_pl_hist", ["scripts/t127_pl_hist.py", "--selftest"], "pl_hist 3-file system (4,515,803 rows, diff=0)"),
    ("t128_non_pl_hist", ["scripts/t128_non_pl_hist.py", "--selftest"], "non_pl_hist 3-file system (3,212,443 rows, diff=0)"),
    ("t130_archive_inventory", ["scripts/t130_archive_inventory.py", "--selftest"], "14-file SHA-256 inventory + 11/11 default-handler proof"),
    ("t133_fm24_reader_v2", ["scripts/t133_fm24_reader_v2.py", "--selftest"], "Pure-Python reader v2 (79/79 tables, 2,846,936 rows, diff=0)"),
    ("t135_star_player_cards", ["scripts/t135_star_player_cards.py", "--selftest"], "21 world superstars live cards (21/21 CA/PA exact)"),
    ("t136_big3_final_closure", ["scripts/t136_big3_final_closure.py", "--selftest"], "Big-3 L3 v4 (85.7% net persisted) + table_extra_9"),
    ("t137_non_player_managers_l3", ["scripts/t137_non_player_managers_l3.py", "--selftest"], "NON_PLAYER 93 own 4CCs + 20/20 managers CA/PA"),
    ("t137d_manager_cards_full", ["scripts/t137d_manager_cards_full.py", "--selftest"], "NON_PLAYER 34 L3 coaching/tactical attrs + 20/20 full cards"),
    ("t138_people_pure_py", ["scripts/t138_people_pure_py.py", "--selftest"], "Pure-Python 400 MB people_db.dat (658,011 rows, diff=0)"),
    ("t139_fm24_db_cli", ["scripts/t139_fm24_db_cli.py", "--selftest"], "Unified 191.7 MB SQLite DB (1,952,416 rows, 0.041ms lookup)"),
    ("t140_fm24_roundtrip", ["scripts/t140_fm24_roundtrip.py", "--selftest"], "S+ 79/79 bit-exact round-trip + editor.exe 10/10 + Kane RAM"),
    ("t141_fm_vs_editor_diff", ["scripts/t141_fm_vs_editor_diff.py", "--selftest"], "491 MB fm.exe vs 74 MB editor.exe (293/293 db:: identical)"),
    ("t142_fk_graph_audit", ["scripts/t142_fk_graph_audit.py", "--selftest"], "84-table FK graph (44 verified edges, 24 col_N, 764 orphans)"),
    ("t143_lang_db", ["scripts/t143_lang_db.py", "--selftest"], "lang_db 704/704 members bit-exact (10,290,726 strings, 22 langs)"),
]

KEY_ARTIFACTS = [
    "scratch/t106/out/special_members_schema.json",
    "scratch/t121/out/wire_traces_79of79.json",
    "scratch/t123/out/basic_people_l3_complete.json",
    "scratch/t126/out/player_69b_attributes_l3.json",
    "scratch/t127/out/pl_hist_schema.json",
    "scratch/t128/out/non_pl_hist_schema.json",
    "scratch/t130/out/archive_inventory.json",
    "scratch/t133/out/reader_v2_verify.json",
    "scratch/t135/out/star_player_cards.json",
    "scratch/t136/out/coverage_summary_v4.json",
    "scratch/t137d/out/non_player_l3_full.json",
    "scratch/t138/out/people_pure_py_verify.json",
    "scratch/t139/out/fm24_core.sqlite",
    "scratch/t140/out/patched_dual_verify.json",
    "scratch/t141/out/fm_vs_editor_diff.json",
    "scratch/t142/out/fk_graph_master.json",
    "scratch/t143/out/lang_db_schema.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def protected_snapshot() -> dict[str, str]:
    """Hash every protected file so pre-existing edits are not blamed on tests."""
    files = sorted((ROOT / "reports").rglob("*.*")) + [ROOT / "scratch/t01/LEDGER.json"]
    return {str(p.relative_to(ROOT)): sha256_file(p) for p in files if p.is_file()}


def check_protected_clean(before: dict[str, str] | None = None) -> dict:
    p = subprocess.run(
        ["git", "status", "--short", "reports/", "scratch/t01/LEDGER.json"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    dirty = [ln for ln in p.stdout.splitlines() if ln.strip()]
    if before is None:
        clean = p.returncode == 0 and not dirty
    else:
        clean = p.returncode == 0 and protected_snapshot() == before
    return {
        "git_rc": p.returncode,
        "protected_clean": clean,
        "dirty_lines": dirty,
        "mode": "snapshot" if before is not None else "git_status",
    }


def check_current_schema() -> dict:
    """Guard the *published* v11.3 schema and its SHA-256 pointers."""
    schema = ROOT / "reports" / "club_nation_subtable_schema.json"
    checks = []
    try:
        doc = json.loads(schema.read_text(encoding="utf-8"))
        checks.append({
            "name": "published_schema_v11_3",
            "passed": doc.get("schema_version") == "11.3"
            and doc.get("generated_by") == "t92"
            and len(doc.get("coverage", {})) > 20,
            "detail": f"version={doc.get('schema_version')} generator={doc.get('generated_by')}",
        })
        for key in ("other_tables_schema", "xml_denominator_coverage"):
            ptr = doc.get("pointer_artifacts", {}).get(key, {})
            target = ROOT / ptr.get("path", "")
            actual = sha256_file(target) if target.is_file() else None
            checks.append({
                "name": f"pointer_sha256_{key}",
                "passed": bool(ptr.get("sha256")) and actual == ptr["sha256"],
                "detail": f"{ptr.get('path')} expected={str(ptr.get('sha256'))[:12]} actual={str(actual)[:12]}",
            })
    except Exception as exc:  # noqa: BLE001 - a broken schema must fail the suite
        checks.append({"name": "schema_readable", "passed": False, "detail": repr(exc)})
    return {
        "checks": checks,
        "all_passed": all(c["passed"] for c in checks),
    }


def run_all() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    before_protected = protected_snapshot()
    results = []
    t0_all = time.perf_counter()
    for name, args, desc in TESTS:
        t0 = time.perf_counter()
        p = subprocess.run(
            ["py", "-V:3.12", "-B", *args],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        dt = round(time.perf_counter() - t0, 2)
        last_line = ""
        for ln in reversed((p.stdout + "\n" + p.stderr).splitlines()):
            if ln.strip():
                last_line = ln.strip()[:140]
                break
        ok = p.returncode == 0
        results.append({
            "name": name,
            "cmd": " ".join(args),
            "description": desc,
            "passed": ok,
            "rc": p.returncode,
            "elapsed_sec": dt,
            "tail": last_line,
        })
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:30s} ({dt:5.2f}s) | {last_line[:70]}")

    manifests = []
    for rel in KEY_ARTIFACTS:
        fp = ROOT / rel
        if fp.is_file():
            manifests.append({"path": rel, "bytes": fp.stat().st_size, "sha256": sha256_file(fp)})
        else:
            manifests.append({"path": rel, "bytes": None, "sha256": None, "missing": True})

    prot = check_protected_clean(before_protected)
    schema_guard = check_current_schema()
    artifacts_ok = all(not m.get("missing") for m in manifests)
    passed = sum(1 for r in results if r["passed"])
    all_ok = (passed == len(results) and prot["protected_clean"]
              and artifacts_ok and schema_guard["all_passed"])
    report = {
        "schema_id": "fm24.t145.final_regression",
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_tests": len(results),
        "passed_tests": passed,
        "failed_tests": len(results) - passed,
        "all_passed": all_ok,
        "tests_all_passed": passed == len(results),
        "artifacts_ok": artifacts_ok,
        "schema_guard": schema_guard,
        "total_elapsed_sec": round(time.perf_counter() - t0_all, 2),
        "protected_guardrail": prot,
        "tests": results,
        "artifact_manifest": manifests,
        "superseded_legacy_scripts": [
            {"script": "scripts/t105_big3_serializers.py", "superseded_by": "scripts/t136_big3_final_closure.py"},
            {"script": "scripts/t115_basic_people_full.py", "superseded_by": "scripts/t123_basic_people_l3.py"},
            {"script": "scripts/t118_people_schema.py", "superseded_by": "scripts/t138_people_pure_py.py"},
        ],
    }
    (OUT / "regression_matrix.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Emit staged ledger_candidates_v2.json (READ-ONLY staging — does NOT touch scratch/t01/LEDGER.json!)
    ledger_v2 = {
        "schema_id": "fm24.t145.ledger_candidates_v2",
        "generated_utc": report["generated_utc"],
        "approval_required": True,
        "note": "Staged update candidates for scratch/t01/LEDGER.json and reports/. DO NOT merge without explicit user approval.",
        "milestones": {
            "dat_files_closed": "13/13 (100.0%, diff=0 pure-Python)",
            "numbered_tables_closed": "79/79 (2,846,936 rows, diff=0, 9.08s pure-Python)",
            "special_members_closed": "13/13 + summary.dat (1,858,739 rows, 28,432,613 B, diff=0)",
            "lang_db_closed": "704/704 members bit-exact (10,290,726 strings, 22 languages)",
            "basic_people_closed": "658,011/658,011 rows (diff=0)",
            "people_db_closed": "658,011/658,011 rows, 400,443,970 B pure-Python (diff=0, 0/3000 Unicorn mismatches)",
            "pl_hist_closed": "515,581 players / 4,515,803 rows / 198,695,332 B (diff=0)",
            "non_pl_hist_closed": "746,543 valid staff / 3,212,443 rows / 77,098,632 B (diff=0)",
            "big3_l3_net_persisted": "568/663 (85.7% net persisted; 568/1034 = 54.9% gross; 95 gaps)",
            "player_pdxx_attributes": "54/54 GET==SET + 21/21 world superstars exact CA/PA",
            "non_player_attributes": "34 L3 coaching/mental/tactical attrs + 20/20 top managers exact CA/PA",
            "roundtrip_engine": "79/79 bit-exact SHA-256 + 10/10 mutated tables + Harry Kane native editor.exe RAM (69/69 PASS)",
            "sqlite_database": "191.7 MB, 1,952,416 rows, 25 indexes, 0.041 ms UID lookup",
            "fk_graph": "84 tables / 4,387,917 rows / 44 verified FK edges / 24 col_N decoded / 764 official orphans",
            "fm_vs_editor_diff": "293/293 db:: classes & 33/33 STARTING_* 100% identical (0 editor-only)",
        },
        "regression_summary": {
            "passed": passed,
            "total": len(results),
            "protected_clean": prot["protected_clean"],
            "artifacts_ok": artifacts_ok,
            "schema_guard_ok": schema_guard["all_passed"],
            "all_passed": all_ok,
        },
    }
    (OUT / "ledger_candidates_v2.json").write_text(json.dumps(ledger_v2, indent=2, ensure_ascii=False), encoding="utf-8")

    (OUT / "DONE.md").write_text(
        "\n".join([
            "DONE type=t145",
            f"regression={passed}/{len(results)} PASS",
            f"protected_clean={prot['protected_clean']}",
            f"artifacts_ok={artifacts_ok}",
            f"schema_guard_ok={schema_guard['all_passed']}",
            f"artifacts_pinned={sum(1 for m in manifests if not m.get('missing'))}/{len(manifests)}",
            f"elapsed_sec={report['total_elapsed_sec']}",
        ]) + "\n",
        encoding="utf-8",
    )
    print(f"\nt145 summary: {passed}/{len(results)} PASS | artifacts_ok={artifacts_ok} | "
          f"schema_guard_ok={schema_guard['all_passed']} | protected_clean={prot['protected_clean']} | "
          f"{report['total_elapsed_sec']}s")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="FM24 final regression suite")
    ap.add_argument("--selftest", action="store_true",
                    help="real rerun of all core tests (same as default)")
    ap.add_argument("--cached", action="store_true",
                    help="fast read-only summary of the last regression_matrix.json")
    args = ap.parse_args()
    if args.cached:
        reg = json.loads((OUT / "regression_matrix.json").read_text(encoding="utf-8"))
        ok = reg.get("all_passed", False)
        print(f"t145 --cached: {'PASS' if ok else 'FAIL'} "
              f"({reg.get('passed_tests')}/{reg.get('total_tests')}, "
              f"generated={reg.get('generated_utc')}, cached only; "
              "protected check skipped — use --selftest for a real run)")
        return 0 if ok else 1
    rep = run_all()
    return 0 if rep["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
