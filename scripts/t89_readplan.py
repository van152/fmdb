#!/usr/bin/env python3
"""t89_readplan — 从 t9_read 反汇编抽出 wire 读取计划(有序、带版本门与循环结构)。

输出结构化 plan:每步 {seq, va, kind, width, dest, gate, loop, helper}
  kind: read | vec_count | vec_item | nested | helper
本模块只读 scratch/t89/probe_t9_read.txt(164K,禁止整读入会话)。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _probe():
    spec = importlib.util.spec_from_file_location("p", ROOT / "scripts/t89_probe.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


VERSION_SRC = "[r9 + 0x588]"     # 版本字来源(r15 = r9+0x588)
GATE_RE = re.compile(r"^cmp (eax|ecx), (0x[0-9a-f]+)$")
JCC_RE = re.compile(r"^(ja|jae|jb|jbe|jg|jge|jl|jle|je|jne) (0x[0-9a-f]+)$")
READ_RE = re.compile(r"^call qword ptr \[(\w+) \+ 0x28\]$")


def plan() -> dict:
    P = _probe()
    ins = P.parse("probe_t9_read")
    br = P.branches(ins)

    # 1) 版本门: cmp eax/ecx, IMM 紧随条件跳转
    gates = []
    for i, x in enumerate(ins):
        m = GATE_RE.match(x["text"])
        if not m:
            continue
        nxt = ins[i + 1]["text"] if i + 1 < len(ins) else ""
        j = JCC_RE.match(nxt)
        gates.append({"i": i, "va": x["va"], "cmp": x["text"],
                      "imm": int(m.group(2), 16), "jcc": j.group(1) if j else None,
                      "target": int(j.group(2), 16) if j else None})
    version_imms = sorted({g["imm"] for g in gates})

    # 2) 循环识别:后向跳转(target < 源 va)
    back = []
    for x in ins:
        m = re.match(r"^(j\w+) (0x[0-9a-f]+)$", x["text"])
        if not m:
            continue
        tgt = int(m.group(2), 16)
        if tgt < x["va"]:
            back.append({"from": x["va"], "to": tgt, "jcc": m.group(1)})

    # 3) 有序读取序列(含门上下文)
    steps = []
    for i, x in enumerate(ins):
        t = x["text"]
        m = READ_RE.match(t)
        if not m:
            continue
        width = dest = None
        for j in range(i - 1, max(i - 10, -1), -1):
            tt = ins[j]["text"]
            if width is None and re.match(r"^mov r8d, ", tt):
                width = int(tt.split(",")[1].strip(), 16)
            if dest is None and re.match(r"^(lea|mov) rdx, ", tt):
                dest = tt.split(",", 1)[1].strip()
            if width is not None and dest is not None:
                break
        # 最近的前置版本门(在 40 条内、未被跳转跨越的近似)
        gate = None
        for j in range(i - 1, max(i - 60, -1), -1):
            g = GATE_RE.match(ins[j]["text"])
            if g:
                nxt = ins[j + 1]["text"]
                jm = JCC_RE.match(nxt)
                gate = {"imm": int(g.group(2), 16), "jcc": jm.group(1) if jm else None,
                        "va": ins[j]["va"]}
                break
        loop = None
        for b in back:
            if b["to"] <= x["va"] < b["from"]:
                loop = b["to"]
                break
        steps.append({"i": i, "va": x["va"], "width": width, "dest": dest,
                      "gate": gate, "loop": loop})

    # 4) 辅助子读(嵌套对象/向量)
    helpers = []
    for i, x in enumerate(ins):
        m = re.match(r"^call (0x[0-9a-f]+)$", x["text"])
        if not m:
            continue
        tgt = int(m.group(1), 16)
        if tgt in (0x14083d4f0, 0x1407e58c0, 0x1407e4940, 0x1407e58c0):
            continue
        r8 = None
        for j in range(i - 1, max(i - 8, -1), -1):
            tt = ins[j]["text"]
            if re.match(r"^lea r8, ", tt):
                r8 = tt.split(",", 1)[1].strip()
                break
        helpers.append({"i": i, "va": x["va"], "target": f"0x{tgt:x}", "r8": r8})

    return {"ins": len(ins), "version_imms": version_imms, "gates": gates,
            "back_edges": back, "steps": steps, "helpers": helpers}


def selftest() -> int:
    p = plan()
    assert p["ins"] == 2141
    assert len(p["steps"]) == 150, len(p["steps"])
    assert p["steps"][0]["width"] == 2 and p["steps"][0]["dest"] == "[rsi + 0x19c]"
    assert 0xdc3 in p["version_imms"], p["version_imms"]
    assert p["back_edges"], "no loops"
    hs = {h["target"] for h in p["helpers"]}
    assert "0x140839290" in hs and "0x140839480" in hs, sorted(hs)[:8]
    print("selftest OK", {"steps": len(p["steps"]), "gates": len(p["gates"]),
                          "versions": [hex(v) for v in p["version_imms"]],
                          "helpers": len(p["helpers"]), "loops": len(p["back_edges"])})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t9_read wire 读取计划")
    ap.add_argument("--json", action="store_true", help="完整 plan JSON")
    ap.add_argument("--steps", action="store_true", help="紧凑步骤表")
    ap.add_argument("--versions", action="store_true", help="版本门常量")
    ap.add_argument("--helpers", action="store_true", help="辅助子读")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    p = plan()
    if a.json:
        print(json.dumps(p, indent=1))
        return 0
    if a.versions:
        print("version_imms:", [hex(v) for v in p["version_imms"]])
        for g in p["gates"]:
            print(f"0x{g['va']:x} {g['cmp']} {g['jcc']} -> 0x{(g['target'] or 0):x}")
        return 0
    if a.helpers:
        for h in p["helpers"]:
            print(f"0x{h['va']:x} -> {h['target']} r8={h['r8']}")
        return 0
    if a.steps:
        for k, s in enumerate(p["steps"]):
            g = s["gate"]["imm"] if s["gate"] else None
            print(f"{k:3d} 0x{s['va']:x} w={s['width']} dst={s['dest']} "
                  f"gate={hex(g) if g else '-'} loop={hex(s['loop']) if s['loop'] else '-'}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
