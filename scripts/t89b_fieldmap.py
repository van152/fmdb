#!/usr/bin/env python3
"""t89b_fieldmap — t9_get_impl / t9_set_impl 4CC dispatch -> container member offset.

Reads (read-only):
  scratch/t89/probe_t9_get_impl.txt   (VA 0x1410668f0; esi = 4CC, big-endian imm)
  scratch/t89/probe_t9_set_impl.txt   (VA 0x141063f30)
  evidence/fm24/reports/editor_schema/master.json (field code -> name)

Dispatch shape (L3, static):
  binary-search tree over the big-endian 4CC immediate; `jg`/`jle`/`ja`/`jbe` are
  tree navigation, `je` opens a case body, `jne` = unknown code -> epilogue.
  Container pointer = `rdi` (from `mov rdi, rcx` in the prologue).
  Case bodies are one of:
    A) container-direct : `movsx/movzx/mov eXX, [rdi + 0xNN]` then a value-sink call
       -> 0xNN is a MEMORY-LAYOUT offset on the T9 object (NOT a wire offset)
    B) forward-to-main  : `mov rcx,rdi; mov edx,esi; mov r8,r14; call 0x1411f1090`
       -> value lives in the nation main row, NOT in the T9 container
    C) wire/collection  : a vtable `call [rax+0x10]/[rax+0x28]` via a temp holder
       -> held: no container offset in the case body

Usage:
  py -V:3.12 -I -B scripts/t89b_fieldmap.py [--out scratch/t89/out/field_map.json]
  py -V:3.12 -I -B scripts/t89b_fieldmap.py --selftest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LINE = re.compile(r"fo=0x([0-9a-f]+) va=0x([0-9a-f]+) ([0-9a-f]+)\s+(.*)$")
CMP4 = re.compile(r"^cmp (e[a-z]+), 0x([0-9a-f]{8})$")
JMP = re.compile(r"^(j[a-z]+)\s+0x([0-9a-f]+)$")
DIRECT = re.compile(r"^(movsx|movzx|mov|movsxd) e?[a-z0-9]+, (byte|word|dword) ptr \[rdi \+ 0x([0-9a-f]+)\]$")
FORWARD = "call 0x1411f1090"


def parse(path: pathlib.Path):
    out = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        m = LINE.search(ln)
        if not m:
            continue
        out.append({"fo": int(m.group(1), 16), "va": int(m.group(2), 16),
                    "txt": m.group(4).strip()})
    out.sort(key=lambda x: x["va"])
    return out


def dec4(v: int) -> str:
    return bytes([(v >> (8 * (3 - i))) & 0xFF for i in range(4)]).decode("latin1")


def cases(ins):
    va2i = {x["va"]: k for k, x in enumerate(ins)}
    out = []
    for i, x in enumerate(ins):
        m = CMP4.match(x["txt"])
        if not m:
            continue
        for j in range(i + 1, min(i + 5, len(ins))):
            mm = JMP.match(ins[j]["txt"])
            if not mm:
                continue
            if mm.group(1) == "je":
                out.append({"code": dec4(int(m.group(2), 16)),
                            "imm": int(m.group(2), 16), "cmp_va": x["va"],
                            "jcc_va": ins[j]["va"], "target_va": int(mm.group(2), 16),
                            "target_i": va2i.get(int(mm.group(2), 16))})
            break
    return out


def body(ins, case, span=48):
    t = case["target_i"]
    if t is None:
        return []
    out = []
    for k in range(t, min(t + span, len(ins))):
        out.append(ins[k])
        if ins[k]["txt"].startswith("jmp ") or ins[k]["txt"].startswith("ret"):
            break
    return out


def classify(b):
    """Return (kind, offsets[], wire_calls, helpers[]).

    vtable slot semantics (L3, from the getter/setter idiom):
      [rax+0x10]  value-holder copy  (NOT wire; the getter writes its result here)
      [rax+0x28]  wire read          (stream reader; Phase 2 entry grid)
      [rax+0x30]  wire write         (stream writer)
    """
    offs, wire, holder, fwd, helpers = [], [], [], False, []
    for x in b:
        t = x["txt"]
        m = DIRECT.match(t)
        if m:
            offs.append({"off": int(m.group(3), 16),
                         "width": {"byte": 1, "word": 2, "dword": 4}[m.group(2)],
                         "va": x["va"], "insn": t})
        if t.startswith(FORWARD):
            fwd = True
        mm = re.match(r"^call qword ptr \[rax \+ 0x(10|28|30)\]$", t)
        if mm:
            slot = int(mm.group(1), 16)
            if slot == 0x10:
                holder.append({"va": x["va"], "insn": t})
            else:
                wire.append({"va": x["va"], "insn": t, "slot": slot})
        md = re.match(r"^call 0x([0-9a-f]+)$", t)
        if md and md.group(1) != "1411f1090":
            helpers.append({"va": x["va"], "target": "0x" + md.group(1)})
    if offs and wire:
        kind = "container_direct_plus_wire"
    elif offs:
        kind = "container_direct"
    elif fwd:
        kind = "forward_to_main_row"
    elif wire:
        kind = "wire_only_held"
    elif helpers:
        kind = "sub_reader_helper"
    else:
        kind = "held_no_offset"
    return kind, offs, wire, helpers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="scratch/t89/out/field_map.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    gi = parse(ROOT / "scratch/t89/probe_t9_get_impl.txt")
    si = parse(ROOT / "scratch/t89/probe_t9_set_impl.txt")
    gc, sc = cases(gi), cases(si)
    if a.selftest:
        assert len(gi) > 2000 and len(si) > 2000, (len(gi), len(si))
        assert len(gc) > 40 and len(sc) > 20, (len(gc), len(sc))
        assert any(c["code"] == "Nflx" for c in gc), "Nflx case missing"
        k, o, w, h = classify(body(gi, next(c for c in gc if c["code"] == "Nflx")))
        assert k == "container_direct" and o and o[0]["off"] == 0x7AD, (k, o)
        print("selftest ok get_ins", len(gi), "set_ins", len(si),
              "get_cases", len(gc), "set_cases", len(sc), "Nflx", k, hex(o[0]["off"]))
        return 0

    master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json")
                        .read_text(encoding="utf-8"))
    nat, allcodes = {}, set()
    for rec in master["entities"]["nation.xml"]:
        for x in rec.get("fields", []):
            c = x.get("field")
            if c:
                allcodes.add(c)
                nat.setdefault(c, x.get("name"))
    for ent, recs in master["entities"].items():
        for rec in recs:
            for x in rec.get("fields", []):
                if x.get("field"):
                    allcodes.add(x["field"])

    gmap, smap = {}, {}
    for c in gc:
        kind, offs, wire, helpers = classify(body(gi, c))
        gmap.setdefault(c["code"], []).append(
            {"case_va": c["target_va"], "cmp_va": c["cmp_va"], "kind": kind,
             "offsets": offs, "wire_calls": wire, "helpers": helpers})
    for c in sc:
        kind, offs, wire, helpers = classify(body(si, c))
        smap.setdefault(c["code"], []).append(
            {"case_va": c["target_va"], "cmp_va": c["cmp_va"], "kind": kind,
             "offsets": offs, "wire_calls": wire, "helpers": helpers})

    fields = []
    for code in sorted(set(gmap) | set(smap)):
        g, s = gmap.get(code, []), smap.get(code, [])
        go = sorted({o["off"] for c in g for o in c["offsets"]})
        so = sorted({o["off"] for c in s for o in c["offsets"]})
        fields.append({
            "code": code,
            "schema_name": nat.get(code),
            "in_nation_xml": code in nat,
            "in_any_schema": code in allcodes,
            "getter": {"kind": g[0]["kind"] if g else None, "cases": g,
                       "container_offsets": go},
            "setter": {"kind": s[0]["kind"] if s else None, "cases": s,
                       "container_offsets": so},
            "layout_agree": bool(go and so and set(go) & set(so)),
        })

    kinds = {}
    for f in fields:
        for side in ("getter", "setter"):
            k = f[side]["kind"]
            if k:
                kinds[k] = kinds.get(k, 0) + 1
    doc = {
        "schema": "t89b.field_map.v1",
        "task": "t89b",
        "inputs": {"get_impl": "scratch/t89/probe_t9_get_impl.txt",
                   "set_impl": "scratch/t89/probe_t9_set_impl.txt",
                   "schema": "evidence/fm24/reports/editor_schema/master.json"},
        "dispatch": {
            "get_entry": "0x1410668f0", "set_entry": "0x141063f30",
            "container_reg": "rdi",
            "get_insns": len(gi), "set_insns": len(si),
            "get_cases": len(gc), "set_cases": len(sc),
            "distinct_codes": len(fields),
            "codes_in_nation_xml": sum(1 for f in fields if f["in_nation_xml"]),
            "codes_elsewhere": sum(1 for f in fields if not f["in_nation_xml"] and f["in_any_schema"]),
            "codes_unknown": sum(1 for f in fields if not f["in_any_schema"]),
            "immediate_encoding": "big-endian ASCII 4CC ('Nrep' = 0x4e726570)",
            "case_kinds": kinds,
        },
        "offset_space": {
            "container_memory_base": "T9 object; data base +0x18, begin/end +0x4a0/+0x4a8",
            "note": "container_offsets are MEMORY-LAYOUT offsets on the T9 object "
                    "([rdi+0xNN] in get_impl). NOT wire offsets — wire offsets are "
                    "in table9_grammar.json entry_grid.",
        },
        "fields": fields,
    }
    p = ROOT / a.out
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    d = doc["dispatch"]
    print("codes", d["distinct_codes"], "nation.xml", d["codes_in_nation_xml"],
          "elsewhere", d["codes_elsewhere"], "unknown", d["codes_unknown"])
    print("kinds", kinds)
    for f in fields:
        if f["getter"]["container_offsets"]:
            print(" ", f["code"], f["schema_name"], f["getter"]["container_offsets"],
                  f["setter"]["container_offsets"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
