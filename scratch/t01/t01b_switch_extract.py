"""t01-b step 3: extract the XML->object field dispatch switch in editor.exe.

Finds `cmp esi, <4CC-be>` + `je <handler>` pairs in a region, disassembles each
handler, classifies:
  direct   : call helperB(0x83d4f0 RVA) then `add rax, N` -> field at obj+N
  delegate : `mov rcx,[r12+X]; mov rdx,r14; call <setter>` -> record setter RVA
  complex  : anything else (record first 12 insns)

Output: scratch/t01/t01b_switch_cases.json + stdout table.
Run: py -V:3.12 -I scratch/t01/t01b_switch_extract.py
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

import capstone

ROOT = Path(__file__).resolve().parents[2]
EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
OUT = ROOT / "scratch" / "t01" / "t01b_switch_cases.json"

REGION_LO, REGION_HI = 0xEC0000, 0xEC6000  # file offsets
HELPER_B_RVA = 0x83D4F0
DELTA = 0xA00  # RVA = fileoff + DELTA within .rdata


def rva(off: int) -> int:
    return off + DELTA


def code_from_imm(imm: int) -> str:
    return struct.pack(">I", imm).decode("ascii", errors="replace")


def main() -> int:
    data = EXE.read_bytes()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    # 1) find cmp esi, imm32 followed by je
    cases = []
    pos = REGION_LO
    while pos < REGION_HI:
        i = data.find(b"\x81\xfe", pos)
        if i < 0 or i >= REGION_HI:
            break
        pos = i + 1
        try:
            insns = list(md.disasm(data[i:i + 24], rva(i)))
        except Exception:
            continue
        if not insns or insns[0].mnemonic != "cmp" or not insns[0].op_str.startswith("esi, 0x"):
            continue
        imm = int(insns[0].op_str.split(",")[1].strip(), 16)
        je = next((x for x in insns[1:3] if x.mnemonic == "je"), None)
        if je is None:
            continue
        tgt_rva = int(je.op_str, 16)
        if tgt_rva == 0xEC51FE:  # default/not-handled chain
            continue
        cases.append({"code": code_from_imm(imm), "cmp_off": i, "handler_off": tgt_rva - DELTA})

    # 2) dedupe by code (keep first cmp per code)
    seen: dict[str, dict] = {}
    for c in cases:
        seen.setdefault(c["code"], c)

    # 3) classify handlers
    results = []
    for code, c in sorted(seen.items()):
        hoff = c["handler_off"]
        try:
            insns = list(md.disasm(data[hoff:hoff + 160], rva(hoff)))
        except Exception:
            results.append({**c, "kind": "disasm_fail"})
            continue
        entry = {**c, "kind": "complex", "notes": []}
        for idx, ins in enumerate(insns[:24]):
            ops = f"{ins.mnemonic} {ins.op_str}"
            if ins.mnemonic == "call" and ins.op_str == hex(HELPER_B_RVA):
                nxt = insns[idx + 1] if idx + 1 < len(insns) else None
                if nxt is not None and nxt.mnemonic == "add" and nxt.op_str.startswith("rax, "):
                    entry["kind"] = "direct"
                    entry["offset"] = int(nxt.op_str.split(",")[1].strip(), 16)
                    # value source/type hint: scan backwards for the last r12 read
                    for back in reversed(insns[:idx]):
                        if back.op_str.startswith("r12 +") or "r12" in back.op_str and ("movsx" in back.mnemonic or "movzx" in back.mnemonic or back.mnemonic == "mov"):
                            entry["value_src"] = f"{back.mnemonic} {back.op_str}"
                            break
                break
            if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
                tgt = int(ins.op_str, 16)
                if tgt not in (HELPER_B_RVA,):
                    # look for rcx=[r12+X] before the call
                    node = next((p.op_str for p in reversed(insns[:idx]) if p.op_str.startswith("r12 +")), None)
                    if node is not None and "r12 + 0x" in node:
                        entry["kind"] = "delegate"
                        entry["setter_rva"] = hex(tgt)
                        entry["node_off"] = node
                    break
            if ins.mnemonic == "jmp":
                break
        results.append(entry)

    # 4) entity match vs master.json comp codes
    master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
    comp_codes = set(master["entity_summary"].get("comp.xml#comp", {}).get("codes", []))
    all_codes = {}
    for ent, s in master["entity_summary"].items():
        for cd in s["codes"]:
            all_codes.setdefault(cd, []).append(ent)
    matched = [r for r in results if r["code"] in comp_codes]
    other = [r for r in results if r["code"] not in comp_codes and r["code"] in all_codes]
    unknown = [r for r in results if r["code"] not in all_codes]

    out = {
        "region": [hex(REGION_LO), hex(REGION_HI)],
        "helperB_rva": hex(HELPER_B_RVA),
        "case_count": len(results),
        "comp_matched": matched,
        "codes_of_other_entities": [{"code": r["code"], "entities": all_codes[r["code"]], "kind": r["kind"], "offset": r.get("offset"), "setter_rva": r.get("setter_rva")} for r in other],
        "codes_not_in_schema": [{"code": r["code"], "kind": r.get("kind"), "cmp_off": hex(r["cmp_off"])} for r in unknown],
        "direct_offsets": sorted({r["offset"] for r in results if r.get("offset") is not None}),
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"cases: {len(results)} (comp-matched {len(matched)}, other-entity {len(other)}, unknown {len(unknown)})")
    print(f"direct-offset distribution: {out['direct_offsets']}")
    print("\ncomp-matched cases:")
    for r in matched:
        print(f"  {r['code']:<6} {r['kind']:<9} off={r.get('offset')} setter={r.get('setter_rva','-')} src={r.get('value_src','-')}")
    print("\nsample non-comp codes:", [r["code"] for r in other][:15])
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
