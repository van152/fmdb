from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DEFAULT_EXE = Path(r"<OLD_REPO>\input\editor.exe")
CODES_FILE = OUT / "codes_full.json"
PATHS_FILE = OUT / "club_paths.json"
NAMING_FILE = OUT / "naming_result.json"
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
T07_NAMING = ROOT / "scratch/t07/out/naming_result.json"
UNIVERSAL = {"duni", "rdui", "NDBC", "FDBC", "dbnm"}
INJURY = {
    "icla": (0x4C, 1), "iscl": (0x4D, 1), "Imnd": (0x34, 2), "Iexd": (0x36, 2),
    "Iiar": (0x58, 1), "Irec": (0x59, 1), "Iocr": (0x30, 4), "Imip": (0x50, 1),
    "Iagr": (0x51, 1), "Icms": (0x52, 1), "Icon": (0x53, 1), "inSr": (0x54, 1),
    "Icdp": (0x56, 1),
}
CITY = {"Clat": 0x48, "Clon": 0x4C, "Cnti": 0x20, "Cwea": 0x28, "Clgi": 0x30, "Clri": 0x38}
SCYK_BOUNDARIES = {0x1538637, 0x1538fb8}
BOUNDARY = {"jle", "jl", "jg", "jae", "ja", "jb", "jbe"}
RE_CMP = re.compile(r"^([a-z0-9]+),\s*(-?0x[0-9a-f]+|-?\d+)$", re.I)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_pe_module():
    spec = importlib.util.spec_from_file_location("t12_verify_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def instance_code_at(pe, md, file_off: int):
    va = pe.f2va(file_off)
    if va is None:
        return None, None
    ins = next(md.disasm(pe.raw[file_off:file_off + 16], va, count=1), None)
    if not ins or ins.mnemonic != "cmp":
        return None, ins
    match = RE_CMP.match(ins.op_str.lower())
    if not match:
        return None, ins
    try:
        imm = int(match.group(2), 0) & 0xffffffff
    except ValueError:
        return None, ins
    try:
        code = imm.to_bytes(4, "little")[::-1].decode("ascii")
    except UnicodeDecodeError:
        return None, ins
    return code, ins


def branch_for_cmp(pe, md, file_off: int):
    va = pe.f2va(file_off)
    if va is None:
        return None
    seq = list(md.disasm(pe.raw[file_off:file_off + 24], va, count=5))
    for ins in seq[1:4]:
        if ins.mnemonic == "cmp":
            m = RE_CMP.match(ins.op_str.lower())
            if m:
                try:
                    n = int(m.group(2), 0) & 0xffffffff
                    bytes4 = n.to_bytes(4, "little")[::-1]
                    if all(chr(b).isalnum() and b < 128 for b in bytes4):
                        break
                except (ValueError, OverflowError):
                    pass
        if ins.mnemonic in BOUNDARY | {"je", "jz", "jne", "jnz", "jg", "jge", "jo", "jno", "js", "jns", "jp", "jnp"}:
            return ins
        if ins.mnemonic in {"jmp", "ret", "call"}:
            break
    return None


def branch_route(mnemonic: str):
    mnemonic = mnemonic.lower()
    if mnemonic in BOUNDARY:
        return None
    if mnemonic in {"je", "jz"}:
        return "je_target"
    if mnemonic in {"jne", "jnz"}:
        return "fallthrough"
    return None


def parse_target(ins):
    try:
        return int(ins.op_str.strip(), 0)
    except (ValueError, TypeError):
        return None


def field_codes(field):
    codes = field.get("codes") or []
    if not codes and field.get("field"):
        codes = re.split(r"[+|]", field["field"])
    return [c for c in codes if c]


def check(exe_path: Path):
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs

    failures, warnings = [], []
    full = load(CODES_FILE)
    paths = load(PATHS_FILE)
    naming = load(NAMING_FILE)
    schema = load(SCHEMA)
    pe = load_pe_module().PE(exe_path)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    records = full.get("codes", {})
    shape_names = {"read", "ref_ptr", "write", "path_descend", "remote"}
    instance_count = 0
    code_mismatches = 0
    access_mismatches = 0
    branch_bad = 0
    for code, instances in records.items():
        if not isinstance(instances, list) or not 1 <= len(instances) <= 6:
            failures.append(f"{code}: expected 1..6 instances, got {len(instances) if isinstance(instances,list) else 'non-list'}")
            continue
        for rec in instances:
            instance_count += 1
            shape = rec.get("shape")
            if shape not in shape_names:
                failures.append(f"{code}: unsupported shape {shape!r}")
                continue
            try:
                file_off = int(rec["file_off"], 16)
                access_va = int(rec["access_va"], 16)
            except (KeyError, TypeError, ValueError):
                failures.append(f"{code}: malformed file_off/access_va")
                continue
            decoded_code, cmp_ins = instance_code_at(pe, md, file_off)
            if not cmp_ins or cmp_ins.mnemonic != "cmp" or decoded_code != code:
                code_mismatches += 1
                failures.append(f"{code}@{rec.get('file_off')}: file_off is not cmp immediate for this 4CC (got {decoded_code!r})")
            access_off = pe.va2f(access_va)
            access_ins = next(md.disasm(pe.raw[access_off:access_off + 16], access_va, count=1), None) if access_off is not None else None
            actual = f"{access_ins.mnemonic} {access_ins.op_str}" if access_ins else None
            if actual != rec.get("instruction"):
                access_mismatches += 1
                failures.append(f"{code}@{rec.get('file_off')}: access_va disassembly {actual!r} != instruction {rec.get('instruction')!r}")
            branch = branch_for_cmp(pe, md, file_off)
            if not branch or branch.mnemonic != rec.get("branch"):
                branch_bad += 1
                failures.append(f"{code}@{rec.get('file_off')}: recorded branch {rec.get('branch')!r} not found after cmp")
                continue
            route = rec.get("route")
            expected = branch_route(branch.mnemonic)
            if route == "target_remote":
                if branch.mnemonic not in {"je", "jz"} or shape != "remote":
                    failures.append(f"{code}@{rec.get('file_off')}: remote must be a JE/JZ target")
                target = parse_target(branch)
                if target is None or rec.get("target_va") != hex(target):
                    failures.append(f"{code}@{rec.get('file_off')}: remote target_va mismatch")
            elif expected is None or route != expected:
                failures.append(f"{code}@{rec.get('file_off')}: polarity violation branch={branch.mnemonic}, route={route}")
            if branch.mnemonic in BOUNDARY:
                failures.append(f"{code}@{rec.get('file_off')}: boundary branch {branch.mnemonic} must not carry access")
            if shape == "path_descend":
                if not isinstance(rec.get("descend"), int) or rec.get("object_off") is not None:
                    failures.append(f"{code}@{rec.get('file_off')}: invalid path_descend payload")
                next_off = pe.va2f(access_va)
                second = next(md.disasm(pe.raw[next_off:next_off + 24], access_va, count=2), None) if next_off is not None else None
                if second is None:
                    failures.append(f"{code}@{rec.get('file_off')}: cannot decode path instruction")
                else:
                    seq = list(md.disasm(pe.raw[next_off:next_off + 24], access_va, count=2))
                    if len(seq) < 2 or seq[1].mnemonic not in {"jmp", "call"}:
                        failures.append(f"{code}@{rec.get('file_off')}: path descent is not followed by jmp/call")
            if shape == "remote" and not rec.get("target_va"):
                failures.append(f"{code}@{rec.get('file_off')}: remote target_va missing")

    expected_hash = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
    import hashlib
    digest = hashlib.sha256(pe.raw).hexdigest()
    if digest != expected_hash:
        failures.append(f"editor.exe SHA-256 mismatch: {digest}")
    if full.get("exe_sha256") != digest:
        failures.append("codes_full exe_sha256 does not match current read-only input")

    # Dedicated ScYK boundary-comparison trap test: its JLE is only a range boundary;
    # neither arm may receive an access from this tag. The following ScYL owns its own read.
    trap_checks = 0
    for file_off in sorted(SCYK_BOUNDARIES):
        tag, ins = instance_code_at(pe, md, file_off)
        branch = branch_for_cmp(pe, md, file_off)
        if tag != "ScYK" or branch is None or branch.mnemonic != "jle":
            failures.append(f"ScYK trap @{file_off:#x}: expected cmp ScYK followed by jle")
            continue
        trap_checks += 1
        if any(rec.get("file_off") == hex(file_off) for rec in records.get("ScYK", [])):
            failures.append(f"ScYK trap @{file_off:#x}: boundary access was attached to ScYK")
    scyl_sites = [r for r in records.get("ScYL", []) if r.get("file_off") == "0x1538fc4"]
    if not scyl_sites:
        failures.append("ScYK trap: expected ScYL's own later cmp/access to remain separately attributable")
    if trap_checks != 2:
        failures.append(f"ScYK trap checked {trap_checks}/2 known jle sites")

    # Fixed independent calibrations: injury 13/13 and city 6/6.
    injury_ok = 0
    for code, (off, size) in INJURY.items():
        if any(r.get("object_off") == off and r.get("size") == size
               and r.get("shape") in {"read", "write"} for r in records.get(code, [])):
            injury_ok += 1
    city_ok = 0
    for code, off in CITY.items():
        if any(r.get("object_off") == off and r.get("size") == 4
               and r.get("shape") in {"read", "ref_ptr"} for r in records.get(code, [])):
            city_ok += 1
    if injury_ok != 13:
        failures.append(f"injury calibration {injury_ok}/13")
    if city_ok != 6:
        failures.append(f"city calibration {city_ok}/6")

    # Check every club schema code has exactly one honest classification, retaining unresolved-present
    # as an explicit extension because bytes-present with no supported shape is not truly absent.
    club = paths.get("codes", {})
    club_schema_codes = {f["code"] for f in schema["entities"]["club"].get("fields", []) if f.get("code")}
    if set(club) != club_schema_codes:
        failures.append(f"club_paths code set mismatch: {len(set(club)^club_schema_codes)} missing/extra")
    binary_kinds = Counter(row.get("kind") for row in club.values())
    raw = pe.raw
    for code, row in club.items():
        present = raw.find(code.encode("ascii")[::-1]) >= 0
        if row.get("kind") == "absent" and present:
            failures.append(f"club {code}: marked absent but reversed 4CC bytes are present")
        if row.get("kind") == "unresolved" and not present:
            failures.append(f"club {code}: unresolved-present but reversed 4CC bytes are absent")
        expected_shapes = {"offset": {"read", "ref_ptr", "write"},
                           "path": {"path_descend"}, "remote": {"remote"}}
        kinds = expected_shapes.get(row.get("kind"))
        if kinds and not any(rec.get("shape") in kinds for rec in records.get(code, [])):
            failures.append(f"club {code}: path kind has no corresponding extracted instance")
    path_covered = sum(binary_kinds.get(k, 0) for k in ("offset", "path", "remote"))
    expected_present = 483
    if path_covered < 420:
        failures.append(f"club coverage {path_covered}/{expected_present} below required 420/483")

    # Flat-table naming: no schema-illegal codes; protect the t11 floor and all t07 named slots.
    mapping = {x["type_id"]: x.get("schema_entity") for x in naming.get("schema_map_audit", {}).get("entities", [])}
    illegal = []
    fields = []
    for entity in naming.get("results", []):
        schema_name = mapping.get(entity["type_id"])
        allowed = {f.get("code") for f in schema.get("entities", {}).get(schema_name, {}).get("fields", [])
                   if f.get("code")} | UNIVERSAL
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                fields.append((entity, archive, field))
                for code in field_codes(field) if field.get("field") else []:
                    if code not in allowed:
                        illegal.append((entity["type_id"], archive, field.get("idx"), code, schema_name))
    named_count = sum(bool(f.get("field")) for _, _, f in fields)
    if illegal:
        failures.append(f"schema-illegal={len(illegal)}; first={illegal[:3]}")
    if named_count < 129:
        failures.append(f"naming {named_count}/240 is below t11 baseline 129")
    base = load(T07_NAMING)
    final_lookup = {(e["type_id"], archive, f.get("idx"), f.get("row_off"), f.get("width")): f
                    for e, archive, f in fields}
    t07_named = [(e, archive, f) for e in base.get("results", [])
                 for archive, spec in e.get("archives", {}).items()
                 for f in spec.get("fields", []) if f.get("field")]
    t07_retained = 0
    for e, archive, field in t07_named:
        final = final_lookup.get((e["type_id"], archive, field.get("idx"),
                                  field.get("row_off"), field.get("width")))
        if final and final.get("field") == field.get("field"):
            t07_retained += 1
    if t07_retained != 45:
        failures.append(f"t07 named regression {t07_retained}/45")

    # The three known reference-backed object-member anchors.
    ref_expected = {"Sold": 32, "Snew": 40, "Salt": 72}
    type22 = next((e for e in naming.get("results", []) if e.get("type_id") == 22), None)
    ref_named = {}
    if type22:
        for archive, spec in type22.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("field") in ref_expected:
                    ref_named[field["field"]] = field.get("object_off")
    for code, off in ref_expected.items():
        if ref_named.get(code) != off:
            failures.append(f"type22 ref_ptr anchor {code}: expected object_off {off}, got {ref_named.get(code)}")

    print(f"instances={instance_count}; cmp/immediate mismatches={code_mismatches}; "
          f"instruction-text mismatches={access_mismatches}; branch mismatches={branch_bad}")
    print(f"ScYK trap={trap_checks}/2; injury={injury_ok}/13; city={city_ok}/6")
    print(f"club classifications={dict(sorted(binary_kinds.items()))}; "
          f"offset+path+remote={path_covered}/483; naming={named_count}/240; "
          f"schema-illegal={len(illegal)}; t07 retained={t07_retained}/45; ref_ptr={ref_named}")
    for failure in failures:
        print("FAIL:", failure)
    if failures:
        return 1
    print("PASS: all instruction, branch polarity, regression, and schema checks")
    return 0


def selftest():
    assert len(INJURY) == 13 and len(CITY) == 6
    assert branch_route("je") == "je_target"
    assert branch_route("jz") == "je_target"
    assert branch_route("jne") == "fallthrough"
    assert branch_route("jnz") == "fallthrough"
    for condition in BOUNDARY:
        assert branch_route(condition) is None
    assert "ScYK" != "ScYL"
    assert 0x1538637 in SCYK_BOUNDARIES and 0x1538fb8 in SCYK_BOUNDARIES
    print("verify.py selftest: OK (JE/JNE polarity; all boundary branches excluded; ScYK trap fixture)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Independently verify fresh t12 4CC extraction, naming, and ScYK branch polarity.")
    ap.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        return check(args.exe)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
