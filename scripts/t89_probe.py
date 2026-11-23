#!/usr/bin/env python3
"""t89_probe — 探针文本(反汇编转储)程序化抽取层。

只读 scratch/t89/probe_*.txt(单件 25K..259K,禁止整读入会话)。
提供:指令行解析、读/写操作序列抽取(call [rax+0x28] / call [rax+0x18])、
      前导门(gate)上下文、控制流目标索引。

用法:
  py -V:3.12 -I -B scripts/t89_probe.py --list
  py -V:3.12 -I -B scripts/t89_probe.py --ops probe_t9_read
  py -V:3.12 -I -B scripts/t89_probe.py --selftest
"""
from __future__ import annotations

import argparse
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = ROOT / "scratch/t89"

LINE = re.compile(
    r"^\s+fo=(0x[0-9a-f]+)\s+va=(0x[0-9a-f]+)\s+(?:([0-9a-f]{2,})\s+)?(.*)$"
)
SECTION = re.compile(r"^===\s+(\S+):\s+VA=(0x[0-9a-f]+)\.\.(0x[0-9a-f]+)\s+fo=(0x[0-9a-f]+)\.\.(0x[0-9a-f]+)")


def parse(name: str) -> list[dict]:
    """把一件探针文本解析成 [{fo,va,bytes,text}]。"""
    p = PROBE / (name if name.endswith(".txt") else name + ".txt")
    out = []
    with io.open(p, encoding="utf-8", errors="replace") as f:
        for raw in f:
            m = LINE.match(raw.rstrip("\n"))
            if not m:
                continue
            out.append({
                "fo": int(m.group(1), 16),
                "va": int(m.group(2), 16),
                "bytes": (m.group(3) or ""),
                "text": m.group(4).strip(),
            })
    return out


def sections(name: str) -> list[dict]:
    """按 `=== 名字: VA=.. fo=..` 切分多段探针。"""
    p = PROBE / (name if name.endswith(".txt") else name + ".txt")
    out, cur = [], None
    with io.open(p, encoding="utf-8", errors="replace") as f:
        for raw in f:
            s = SECTION.match(raw)
            if s:
                cur = {"name": s.group(1), "va": s.group(2), "fo": s.group(4), "ins": []}
                out.append(cur)
                continue
            m = LINE.match(raw.rstrip("\n"))
            if m and cur is not None:
                cur["ins"].append({"fo": int(m.group(1), 16), "va": int(m.group(2), 16),
                                   "bytes": (m.group(3) or ""), "text": m.group(4).strip()})
    return out


def ops(ins: list[dict]) -> list[dict]:
    """抽 wire 读/写点:call qword ptr [rax + 0x28] (read) / +0x18 / +0x20 (write)。

    返回 {va, fo, bytes, kind, width, dest, gate}
      width = 最近的前导 `mov r8d, imm`
      dest  = 最近的前导 `lea rdx, [..]` / `mov rdx, [..]`
      gate  = 最近的前导条件分支(text 含 `jne`/`je`/`jg`/`jle` 等)
    """
    out = []
    for i, x in enumerate(ins):
        t = x["text"]
        m = re.match(r"^call qword ptr \[(\w+) \+ (0x[0-9a-f]+)\]$", t)
        if not m:
            continue
        slot = int(m.group(2), 16)
        kind = {0x28: "read", 0x18: "write", 0x20: "write"}.get(slot, f"slot{slot:x}")
        width = dest = gate = None
        for j in range(i - 1, max(i - 10, -1), -1):
            tt = ins[j]["text"]
            if width is None and re.match(r"^mov r8d, ", tt):
                width = int(tt.split(",")[1].strip(), 16)
            if dest is None and re.match(r"^(lea|mov) rdx, ", tt):
                dest = tt.split(",", 1)[1].strip()
            if gate is None and re.match(r"^(jne|je|jg|jle|jge|jl|ja|jbe|jb) ", tt):
                gate = tt
        out.append({"va": x["va"], "fo": x["fo"], "bytes": x["bytes"], "kind": kind,
                    "slot": slot, "width": width, "dest": dest, "gate": gate})
    return out


def branches(ins: list[dict]) -> dict:
    """控制流: 目标 VA -> 来源 VA 列表(用于识别循环/条件块)。"""
    g = {}
    for x in ins:
        m = re.match(r"^(?:j\w+|call) (0x[0-9a-f]+)$", x["text"])
        if m:
            g.setdefault(int(m.group(1), 16), []).append(x["va"])
    return g


def selftest() -> int:
    ins = parse("probe_t9_read")
    assert len(ins) > 2000, len(ins)
    assert ins[0]["va"] == 0x14105d510, hex(ins[0]["va"])
    assert ins[0]["text"] == "push r15", ins[0]["text"]
    o = ops(ins)
    assert len(o) == 150, len(o)
    assert o[0]["width"] == 2 and o[0]["dest"] == "[rsi + 0x19c]", o[0]
    s = sections("probe_helpers")
    assert len(s) >= 10, len(s)
    names = [x["name"] for x in s]
    assert "h_839480" in names and "team_container_read" in names, names[:5]
    b = branches(ins)
    assert b, "no branches"
    print("selftest OK", {"t9_read_ins": len(ins), "ops": len(o), "sections": len(s)})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t89 探针抽取层")
    ap.add_argument("--list", action="store_true", help="列出探针文件与体积")
    ap.add_argument("--ops", metavar="NAME", help="打印某探针的 wire 操作序列(紧凑)")
    ap.add_argument("--sections", metavar="NAME", help="列出某探针的分段")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.list:
        for p in sorted(PROBE.glob("probe_*.txt")):
            print(f"{p.name:32s} {p.stat().st_size:>8d}")
        return 0
    if a.sections:
        for s in sections(a.sections):
            print(f"{s['name']:28s} VA={s['va']} fo={s['fo']} ins={len(s['ins'])}")
        return 0
    if a.ops:
        o = ops(parse(a.ops))
        print(f"# {a.ops}: {len(o)} wire ops")
        for x in o:
            print(f"{x['va']:x} {x['kind']:5s} w={x['width']} dst={x['dest']} gate={x['gate']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
