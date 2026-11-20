#!/usr/bin/env python3
"""Independently verify t13 table/entity anchors from the frozen local artifacts.

Usage: py -V:3.12 -I scratch/t13/out/verify.py [--help|--selftest]
The verifier is read-only; it reads the editor executable and t05/t08/t12 artifacts.
Exit codes: 0 pass, 1 verification failure, 2 usage/fatal error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPECTED = {
    12: 28597, 26: 90128, 29: 13278, 32: 315, 33: 32409, 36: 6535,
    38: 5241, 39: 117, 45: 84477, 48: 5210, 52: 0, 57: 0,
}
GENERIC_CODES = {"duni", "rdui", "ndbc", "fdbc", "dbnm"}
ARTIFACTS = {
    "coverage": ROOT / "scratch/t05/COVERAGE.json",
    "boundaries": ROOT / "scratch/t05/server_bounds/boundaries.json",
    "readers": ROOT / "scratch/t05/reader_widths.json",
    "schema": ROOT / "scratch/t05/schema_inventory.json",
    "chains": ROOT / "scratch/t08/out/chains.json",
    "codes": ROOT / "scratch/t12/out/codes_full.json",
    "stage2": ROOT / "scratch/t01/stage2_three_way.json",
    "exe": Path(r"<OLD_REPO>\input\editor.exe"),
}


class VerifyFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise VerifyFailure(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def norm_instruction(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def entity_tags(stage2: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in stage2.get("rows", []):
        xml = row.get("entity_xml") or ""
        tag = row.get("entity_tag")
        if ".xml#" in xml and tag:
            name = xml.split(".xml#", 1)[0].rsplit("/", 1)[-1]
            out[name] = tag
    return out


def check_selftest() -> None:
    require(set(EXPECTED) == {12, 26, 29, 32, 33, 36, 38, 39, 45, 48, 52, 57},
            "selftest: table coverage set changed")
    require(norm_instruction(" MOV edi,  dword ptr [rdi + 0x80] ") ==
            "mov edi, dword ptr [rdi + 0x80]", "selftest: instruction normalization")
    require(GENERIC_CODES == {"duni", "rdui", "ndbc", "fdbc", "dbnm"},
            "selftest: generic-code exclusion changed")


def run_verify(anchors_path: Path) -> list[str]:
    anchors = load_json(anchors_path)
    require(anchors.get("status", "").startswith("complete_"),
            "anchors.json is not marked complete")
    tables = anchors.get("tables")
    require(isinstance(tables, list), "anchors.json tables must be a list")
    ids = [row.get("table_type") for row in tables]
    require(len(ids) == len(set(ids)), "duplicate table_type")
    require(set(ids) == set(EXPECTED), f"coverage mismatch: got {sorted(ids)}")

    coverage = load_json(ARTIFACTS["coverage"])
    boundary = load_json(ARTIFACTS["boundaries"])
    readers = load_json(ARTIFACTS["readers"])
    schema = load_json(ARTIFACTS["schema"])
    chain_doc = load_json(ARTIFACTS["chains"])
    code_doc = load_json(ARTIFACTS["codes"])
    stage2 = load_json(ARTIFACTS["stage2"])

    cov_by_id = {x["table_id"]: x for x in coverage["tables"]
                 if x.get("archive") == "server"}
    bound_by_id = {x["table_id"]: x for x in boundary["tables"]}
    reader_by_id = {x["type_id"]: x for x in readers["results"]}
    chains_by_id = {x["chain_id"]: x for x in chain_doc["chains"]}
    schema_entities = schema["entities"]
    code_entities: dict[str, set[str]] = {}
    for entity_name, entity in schema_entities.items():
        for field in entity.get("fields", []):
            code_entities.setdefault(field["code"], set()).add(entity_name)
    tag_by_name = entity_tags(stage2)

    exe_hash = hashlib.sha256(ARTIFACTS["exe"].read_bytes()).hexdigest()
    for label in ("readers", "chains", "codes"):
        doc = {"readers": readers, "chains": chain_doc, "codes": code_doc}[label]
        declared_hash = doc.get("exe_sha256")
        require(declared_hash == exe_hash,
                f"{label} exe_sha256 {declared_hash!r} != actual {exe_hash}")

    # Import the project's PE mapper only after determining ROOT explicitly; -I is expected.
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import t05_pe  # type: ignore[import-not-found]
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs  # type: ignore[import-not-found]

    pe = t05_pe.default()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    resolved = 0
    messages: list[str] = []

    for row in tables:
        tid = row["table_type"]
        require(row.get("archive") == "server", f"table {tid}: archive is not server")
        require(row.get("count") == EXPECTED[tid],
                f"table {tid}: anchors count {row.get('count')} != expected {EXPECTED[tid]}")
        require(tid in cov_by_id and cov_by_id[tid].get("count") == EXPECTED[tid],
                f"table {tid}: count not independently present in COVERAGE.json")
        require(row.get("status") in {"resolved", "candidate", "negative", "empty"},
                f"table {tid}: invalid status {row.get('status')!r}")

        status = row["status"]
        if status in {"candidate", "negative"}:
            require(bool(row.get("why_unresolved")),
                    f"table {tid}: {status} requires why_unresolved")
        if status == "empty":
            b = bound_by_id.get(tid, {})
            ee = row.get("empty_evidence", {})
            require(EXPECTED[tid] == 0 and b.get("model") == "empty" and
                    b.get("payload_len") == 22 and b.get("closure") == "14 + 0 + 8 == 22",
                    f"table {tid}: empty payload not verified by boundaries.json")
            require(bool(ee.get("source_file")) and bool(ee.get("claim")),
                    f"table {tid}: empty_evidence is incomplete")
            require(not row.get("anchors"), f"table {tid}: empty table cannot carry a field anchor")
            messages.append(f"table {tid}: empty verified")
            continue

        anchors_list = row.get("anchors")
        require(isinstance(anchors_list, list), f"table {tid}: anchors must be a list")
        if status == "resolved":
            resolved += 1
            require(bool(row.get("entity")), f"table {tid}: resolved entity missing")
            require(any(a.get("kind") in {"A", "B"} for a in anchors_list),
                    f"table {tid}: resolved requires at least one A or B anchor")

        for anchor in anchors_list:
            kind = anchor.get("kind")
            ev = anchor.get("evidence")
            require(kind in {"A", "B", "C"}, f"table {tid}: invalid anchor kind {kind!r}")
            require(isinstance(ev, dict) and bool(ev), f"table {tid}: empty anchor evidence")
            require(bool(anchor.get("claim")) and bool(anchor.get("independence")),
                    f"table {tid}: claim/independence missing")
            if status == "resolved" and kind == "C":
                require(any(a.get("kind") in {"A", "B"} for a in anchors_list),
                        f"table {tid}: C-only evidence cannot resolve")
            if kind != "A":
                continue

            code = ev.get("code")
            require(isinstance(code, str), f"table {tid}: A anchor code missing")
            require(code.lower() not in GENERIC_CODES,
                    f"table {tid}: generic code {code} cannot be an A anchor")
            schema_entity = ev.get("schema_entity")
            owners = code_entities.get(code, set())
            require(len(owners) == 1 and schema_entity in owners,
                    f"table {tid}: {code} schema df is {len(owners)}, expected 1 for {schema_entity}")
            require(ev.get("schema_df") == 1, f"table {tid}: declared schema_df is not 1")
            require(tag_by_name.get(schema_entity) == row.get("entity"),
                    f"table {tid}: schema entity {schema_entity} does not map to tag {row.get('entity')}")

            reader = reader_by_id.get(tid)
            require(reader is not None, f"table {tid}: reader_widths entry missing")
            require(reader.get("reader") == ev.get("reader_file_off"),
                    f"table {tid}: evidence reader does not match type_id reader")
            object_off = ev.get("object_off")
            require(object_off in (reader.get("obj_seq") or []),
                    f"table {tid}: object_off {object_off} is absent from its reader sequence")

            chain_id = ev.get("chain_id")
            chain = chains_by_id.get(chain_id)
            require(chain is not None and chain.get("connectivity", {}).get("status") == "passed",
                    f"table {tid}: missing/failed chain {chain_id}")
            candidates = [p for p in chain.get("candidate_pairs", [])
                          if p.get("code") == code and p.get("object_off") == object_off
                          and p.get("instruction") == ev.get("instruction")
                          and p.get("access_va") == ev.get("access_va")
                          and p.get("file_off") == ev.get("code_site_file_off")]
            require(bool(candidates), f"table {tid}: A anchor not present in declared chain")
            lo, hi = (int(x, 16) for x in chain["file_off_range"])
            reader_off = int(reader["reader"], 16)
            distance = 0 if lo <= reader_off <= hi else min(abs(reader_off - lo), abs(reader_off - hi))
            require(distance <= 0x2000,
                    f"table {tid}: code chain is not near its reader (distance {distance:#x})")

            access_va = int(ev["access_va"], 16)
            file_off = int(ev["file_off"], 16)
            require(pe.va2f(access_va) == file_off,
                    f"table {tid}: access_va does not map to evidence file_off")
            va = pe.f2va(file_off)
            require(va == access_va, f"table {tid}: PE file_off->VA mismatch")
            ins = list(md.disasm(pe.raw[file_off:file_off + 16], va))
            require(bool(ins), f"table {tid}: no instruction at exe file_off {file_off:#x}")
            actual_instruction = f"{ins[0].mnemonic} {ins[0].op_str}".strip()
            require(norm_instruction(actual_instruction) == norm_instruction(ev["instruction"]),
                    f"table {tid}: exe instruction mismatch at {file_off:#x}: {actual_instruction!r}")

        messages.append(f"table {tid}: {status} ({len(anchors_list)} anchor(s))")

    require(resolved >= 4, f"only {resolved} resolved tables have A/B evidence; need >=4")
    require(all(x.get("status") != "in_progress" for x in tables), "unfinished table status")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify t13 entity anchors against local source artifacts and editor.exe.")
    parser.add_argument("--anchors", type=Path, default=HERE / "anchors.json",
                        help="anchors.json path (default: sibling file)")
    parser.add_argument("--selftest", action="store_true", help="run offline verifier self-tests")
    args = parser.parse_args()
    try:
        if args.selftest:
            check_selftest()
            print("SELFTEST PASS")
            return 0
        messages = run_verify(args.anchors.resolve())
        print("VERIFY PASS")
        for message in messages:
            print(message)
        return 0
    except VerifyFailure as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
