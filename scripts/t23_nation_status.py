#!/usr/bin/env python3
"""Reconcile nation evidence scopes without rewriting prior partial results."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t23" / "out"
G2_VERIFY = ROOT / "scratch" / "t02" / "inbox" / "nati" / "OUTBOX" / "verify.py"
G2_PAYLOAD = ROOT / "scratch" / "t02" / "inbox" / "nati" / "client_db_t10.bin"
T19_VERIFY = ROOT / "scratch" / "t19" / "out" / "verify.py"
T19_CURSOR = ROOT / "scratch" / "t19" / "out" / "cursor_nation.json"
T19_REPORT = ROOT / "scratch" / "t19" / "out" / "REPORT.md"
T19_FIELDS = ROOT / "scratch" / "t19" / "out" / "fields_nation.json"
NCPI_SCRIPT = ROOT / "scripts" / "t22_nation_capital.py"
NCPI_REPORT = ROOT / "reports" / "t22_nation_capital.md"
NCPI_DATA = ROOT / "reports" / "t22_nation_capital.json"
EXPECTED_NATION_SHA256 = "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34"
EXPECTED_EDITOR_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_G2_SIZE = 24732
EXPECTED_G2_ROWS = 251


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("_t23_g2_verify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load verifier: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_read_only(command: list[str]) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {"command": command, "returncode": proc.returncode,
            "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}


def check_inputs() -> list[str]:
    required = (G2_VERIFY, G2_PAYLOAD, T19_VERIFY, T19_CURSOR, T19_REPORT,
                T19_FIELDS, NCPI_SCRIPT, NCPI_REPORT, NCPI_DATA)
    return [str(path.relative_to(ROOT)) for path in required if not path.is_file()]


def verify() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    missing = check_inputs()
    if missing:
        return ({"task": "t23", "status": "blocked_missing_inputs", "missing": missing}, missing)

    g2 = load_module(G2_VERIFY)
    g2_hash = file_sha(G2_PAYLOAD)
    if g2_hash != EXPECTED_NATION_SHA256:
        errors.append(f"g2 payload hash mismatch: {g2_hash}")
    if G2_PAYLOAD.stat().st_size != EXPECTED_G2_SIZE:
        errors.append(f"g2 payload size mismatch: {G2_PAYLOAD.stat().st_size}")
    raw = G2_PAYLOAD.read_bytes()
    parsed = g2.parse_payload(raw)
    rows = parsed["rows"]
    if len(rows) != EXPECTED_G2_ROWS:
        errors.append(f"g2 row count mismatch: {len(rows)}")
    if parsed["sum_row_spans"] != 24710 or parsed["footer_start"] != 24724:
        errors.append("g2 full client closure values differ")
    g2_selftest = run_read_only([sys.executable, "-I", str(G2_VERIFY), "--selftest"])
    if g2_selftest["returncode"] != 0:
        errors.append("g2 --selftest failed")

    t19_cursor = load_json(T19_CURSOR)
    nation_state = t19_cursor.get("status")
    t19_full_verify = run_read_only([sys.executable, "-I", str(T19_VERIFY)])
    if nation_state != "partial_prefix_cursor_tail_and_loops_unresolved":
        errors.append(f"t19 nation state changed unexpectedly: {nation_state}")
    if t19_full_verify["returncode"] != 1:
        errors.append(f"t19 full verifier result is {t19_full_verify['returncode']}, expected blocked exit 1")
    manifest = load_json(T19_FIELDS)
    shard_names = manifest.get("shards", [])
    field_rows = []
    for shard_name in shard_names:
        shard = load_json(T19_FIELDS.parent / shard_name)
        if shard.get("entity_tag") != "nati" or shard.get("offset_space") != "dat_row":
            errors.append(f"unexpected nation shard metadata: {shard_name}")
        field_rows.extend(shard.get("fields", []))
    if manifest.get("fields_total") != 441:
        errors.append(f"t19 nation manifest total={manifest.get('fields_total')}, expected 441")
    if len(field_rows) != 441:
        errors.append(f"t19 nation field shards have {len(field_rows)} rows, expected 441")
    nation_named = [row for row in field_rows if row.get("grade") != "unnamed"]
    if len(nation_named) != 7 or manifest.get("named_fields") != 7:
        errors.append(f"t19 inherited named fields={len(nation_named)}, expected 7")

    ncpi = load_json(NCPI_DATA)
    field = ncpi.get("field", {})
    ncpi_status = ncpi.get("status")
    ncpi_check = run_read_only([sys.executable, "-I", str(NCPI_SCRIPT), "--selftest"])
    if ncpi_check["returncode"] != 0:
        errors.append("Ncpi replay --selftest failed")
    if ncpi_status != "complete":
        errors.append(f"Ncpi task status={ncpi_status!r}, expected complete")
    if (field.get("code"), field.get("row_offset"), field.get("width"), field.get("target")) != (
            "Ncpi", 9, 4, "client_db/table_2.dat row ordinal (zero-based)"):
        errors.append("Ncpi mapping tuple changed")
    if ncpi.get("editor_exe", {}).get("sha256") != EXPECTED_EDITOR_SHA256:
        errors.append("Ncpi editor.exe hash differs from the frozen reader binary")
    if ncpi.get("data", {}).get("nation_rows") != EXPECTED_G2_ROWS:
        errors.append("Ncpi nation row count differs from g2 client scope")

    field_offsets = ncpi.get("field", {})
    if (field_offsets.get("code"), field_offsets.get("row_offset"), field_offsets.get("width")) != (
            "Ncpi", 9, 4):
        errors.append("Ncpi field mapping is not recorded at client row+9/4B")

    result = {
        "task": "t23",
        "status": "complete_client_scope_reconciled_with_server_and_schema_coverage_open",
        "scope": "2430 client nation table only; no server grammar or full schema ledger claim",
        "evidence": {
            "g2_client_rows": {
                "payload_sha256": g2_hash,
                "payload_bytes": len(raw),
                "row_count": len(rows),
                "row_span_bytes": parsed["sum_row_spans"],
                "closure": "14 + 24710 + 8 = 24732",
                "count_totals_A_B_C_D": parsed["count_totals"],
                "count_maxima_A_B_C_D": parsed["count_maxima"],
                "identity_all_rows": True,
                "footer_start": parsed["footer_start"],
                "footer_hex": parsed["footer_hex"],
                "verifier": g2_selftest,
            },
            "t19_status_reconciled": {
                "recorded_status": nation_state,
                "full_verifier_exit": t19_full_verify["returncode"],
                "full_verifier_stdout": t19_full_verify["stdout"],
                "meaning": "t19's own expanded cursor ledger remains partial; it does not invalidate the independently closed g2 client grammar",
                "ledger_fields": len(field_rows),
                "inherited_named_fields": len(nation_named),
                "schema_total": 441,
            },
            "ncpi": {
                "status": ncpi_status,
                "code": field.get("code"),
                "name": field.get("name"),
                "row_offset": field.get("row_offset"),
                "width": field.get("width"),
                "target": field.get("target"),
                "evidence_level": field.get("evidence_level"),
                "selftest": ncpi_check,
                "total_nation_fields": 441,
                "named_by_t19_ledger": 7,
                "field_scope_note": "Ncpi is a standalone L3 field mapping, not completion of the remaining nation schema fields",
            },
        },
        "open_items": [
            "server_db table_10 row grammar has only a recorded hash/count; no client formula is extrapolated",
            "434 of 441 nation fields remain unnamed in the t19 row-coordinate ledger; t23 adds only the independently verified Ncpi mapping",
            "the commented XML schema record does not prove UI editability or L4 behavior",
            "alternate arg8!=0 reader path remains unassigned to client/server payload",
        ],
        "errors": errors,
    }
    return result, errors


def selftest() -> bool:
    return (EXPECTED_G2_ROWS == 251 and EXPECTED_G2_SIZE == 24732 and
            len(EXPECTED_NATION_SHA256) == 64 and
            len(EXPECTED_EDITOR_SHA256) == 64)


def write(result: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "nation_status.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence = result.get("evidence", {})
    g2 = evidence.get("g2_client_rows", {})
    t19 = evidence.get("t19_status_reconciled", {})
    ncpi = evidence.get("ncpi", {})
    lines = [
        "# t23 nation client status reconciliation", "",
        f"Status: `{result['status']}`. The client row grammar is closed; the 441-field nation ledger is not.", "",
        "## Reconciled Results", "",
        f"- **Client table_10 framing:** {g2.get('row_count')} rows; `{g2.get('closure')}`; "
        f"A/B/C/D totals `{g2.get('count_totals_A_B_C_D')}`; SHA-256 `{g2.get('payload_sha256')}`.",
        f"- **t19 ledger:** status `{t19.get('recorded_status')}`; its own verifier remains blocked at exit "
        f"{t19.get('full_verifier_exit')}; it contains {t19.get('inherited_named_fields')}/"
        f"{t19.get('schema_total')} named fields. This is consistent with a partial expanded ledger, "
        "not a failed g2 row walk.",
        f"- **Ncpi:** {ncpi.get('code')} ({ncpi.get('name')}) at client body `row+{ncpi.get('row_offset')}`, "
        f"width {ncpi.get('width')}, targeting zero-based city row ordinal; evidence grade `{ncpi.get('evidence_level')}`. "
        "This is one standalone mapping, not completion of the nation schema.",
        "", "## Scope Boundaries", "",
        "- The g2 verifier parses the 2430 client payload only and walks each of the 251 variable rows through identity and footer.",
        "- t01g's original prefix-only negative result remains intact; it did not claim all row starts.",
        "- t19's schema-wide ledger remains partial and its full verifier correctly blocks unresolved row alignment for that ledger.",
        "- No client formula is applied to server table_10; the alternate reader path remains unassigned to client/server.",
        "- The commented Ncpi XML record does not establish current UI editability or L4 behavior.",
        "", "## Still Open", "",
        "- Recover a server table_10 grammar and independently close its rows.",
        "- Map the remaining nation fields using helper/branch-aware row coordinates; the current ledger has 434 unnamed entries.",
        "- Reconcile the alternate arg8!=0 reader path with an actual archive before assigning its role.",
        "", "## Reproduction", "",
        "`py -V:3.12 -I scratch/t02/inbox/nati/OUTBOX/verify.py --selftest`",
        "`py -V:3.12 -I scripts/t22_nation_capital.py --selftest`",
        "`py -V:3.12 -I scratch/t19/out/verify.py` is expected to report BLOCKED for the expanded t19 ledger.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="check immutable scope/hash constants")
    args = parser.parse_args()
    if args.selftest:
        print("t23 verifier selftest: " + ("PASS" if selftest() else "FAIL"))
        return 0 if selftest() else 1
    try:
        result, errors = verify()
        write(result)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print("PASS (partial scope): client nation rows closed; Ncpi verified; server grammar and full field ledger remain open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
