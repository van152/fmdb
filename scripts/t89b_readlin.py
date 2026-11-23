#!/usr/bin/env python3
"""t89b_readlin — linearize t9_read (VA=0x14105d510) into a wire-read program.

Parses scratch/t89/probe_t9_read.txt (read-only) in VA order and emits, for each
wire read (`call qword ptr [rax+0x28]`, rdx=dest, r8d=width), the static context:

  width     bytes consumed from the wire
  dest      `rsi + 0xNNN`  -> container member (memory layout offset)
            `rsp + 0xNN`   -> temp slot (used for counts / dynamic payloads)
            other/None     -> indirect (rbp/rbx based) => loop-strided or dynamic
  loops     containing loops, each {head_va, back_va, trip_src}
  gate      nearest enclosing `cmp e.., imm` + jcc whose skip target is after the
            read => version gate (imm is the version threshold, 3523/3524/3535/999)

Usage:
  py -V:3.12 -I -B scripts/t89b_readlin.py [--out scratch/t89/out/read_lin.json]
  py -V:3.12 -I -B scripts/t89b_readlin.py --selftest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = ROOT / "scratch/t89/probe_t9_read.txt"
LINE = re.compile(r"fo=0x([0-9a-f]+) va=0x([0-9a-f]+) ([0-9a-f]+)\s+(.*)$")
TGT = re.compile(r"0x(14[0-9a-f]{7,9})")
CMP = re.compile(r"cmp (e[a-z]+|word ptr \[[^\]]+\]|dword ptr \[[^\]]+\]), (0x[0-9a-f]+)$")
JCC = re.compile(r"^(j[a-z]+)\s")


def parse(path: pathlib.Path):
    ins = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        m = LINE.search(ln)
        if not m:
            continue
        by = m.group(3)
        ins.append({"fo": int(m.group(1), 16), "va": int(m.group(2), 16),
                    "bytes": by, "len": len(by) // 2, "txt": m.group(4).strip()})
    ins.sort(key=lambda x: x["va"])
    return ins


def jtargets(txt: str):
    return [int(t, 16) for t in TGT.findall(txt)]


def find_loops(ins):
    """Real loops only: backward branch AND an incremented counter that the loop
    compares against a bound, AND a short span (error-epilogue `jne` hops reuse
    earlier addresses and are excluded by the span + counter test)."""
    va2i = {x["va"]: k for k, x in enumerate(ins)}
    loops = []
    for i, x in enumerate(ins):
        t = x["txt"]
        m = re.match(r"^(j[a-z]+)\s+0x([0-9a-f]+)$", t)
        if not m:
            continue
        tg = int(m.group(2), 16)
        if tg >= x["va"]:
            continue
        if x["va"] - tg > 0x200:  # span filter
            continue
        h = va2i.get(tg)
        if h is None:
            continue
        # counter: an increment inside the span and a `cmp` on the same register
        regs = set()
        for j in range(h, i):
            mm = re.match(r"(inc|dec) ([a-z][a-z0-9]*)$", ins[j]["txt"])
            if mm:
                regs.add(mm.group(2))
        reg = None
        for r in sorted(regs):
            if any(re.match(r"^cmp %s," % r, ins[j]["txt"]) for j in range(h, i)):
                reg = r
                break
        if not reg:
            continue
        loops.append({"head_va": tg, "back_va": x["va"], "back_i": i,
                      "jcc": m.group(1), "counter": reg, "head_i": h})
    return loops


def trip_src(ins, head_va):
    """Loop trip count source: `mov e.., dword ptr [rsi+X]` just before the head,
    or the `cmp rXX, rYY` bound register's last load."""
    lo = max(0, next(k for k, x in enumerate(ins) if x["va"] >= head_va) - 12)
    for j in range(next(k for k, x in enumerate(ins) if x["va"] >= head_va) - 1, lo - 1, -1):
        t = ins[j]["txt"]
        m = re.match(r"mov (e[a-z]+), dword ptr \[(rsi \+ 0x[0-9a-f]+|rsp \+ 0x[0-9a-f]+)\]$", t)
        if m:
            return {"reg": m.group(1), "src": m.group(2), "va": ins[j]["va"]}
        m = re.match(r"mov (e[a-z]+), dword ptr \[(rsp \+ 0x[0-9a-f]+)\]$", t)
        if m:
            return {"reg": m.group(1), "src": m.group(2), "va": ins[j]["va"]}
    return None


def gate_for(ins, i):
    """Nearest preceding version cmp+jcc whose skip target is after this insn."""
    va = ins[i]["va"]
    for j in range(i - 1, max(i - 60, -1), -1):
        m = CMP.match(ins[j]["txt"])
        if not m:
            continue
        k = j + 1
        if k >= len(ins) or not JCC.match(ins[k]["txt"]):
            continue
        tg = jtargets(ins[k]["txt"])
        if not tg:
            continue
        if tg[0] > va:
            return {"imm": int(m.group(2), 16), "reg": m.group(1),
                    "jcc": ins[k]["txt"].split()[0], "va": ins[k]["va"],
                    "skip_to": tg[0], "cmp_va": ins[j]["va"]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="scratch/t89/out/read_lin.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    ins = parse(PROBE)
    if a.selftest:
        assert len(ins) > 2000, len(ins)
        assert ins[0]["va"] == 0x14105D510, hex(ins[0]["va"])
        print("selftest ok insns", len(ins), "span",
              hex(ins[0]["va"]), hex(ins[-1]["va"]))
        return 0
    loops = find_loops(ins)
    for lp in loops:
        lp["trip_src"] = trip_src(ins, lp["head_va"])
    reads = []
    for i, x in enumerate(ins):
        if not x["txt"].startswith("call qword ptr [rax + 0x28]"):
            continue
        w = dst = None
        for j in range(i - 1, max(i - 9, -1), -1):
            tt = ins[j]["txt"]
            if w is None:
                m = re.match(r"mov r8d, (\w+)$", tt)
                if m:
                    w = int(m.group(1), 0)
            if dst is None:
                m = re.match(r"lea rdx, \[(.+)\]$", tt)
                if m:
                    dst = m.group(1)
            if w is not None and dst is not None:
                break
        if w is None or dst is None:
            # indirect dest: `mov rdx, rbp` / `mov rdx, rbx` / lea via reg
            for j in range(i - 1, max(i - 9, -1), -1):
                m = re.match(r"mov rdx, (\w+)$", ins[j]["txt"])
                if m and dst is None:
                    dst = "indirect:" + m.group(1)
        enclosing = [lp for lp in loops if lp["head_va"] <= x["va"] <= lp["back_va"]]
        enclosing.sort(key=lambda l: l["head_va"] - l["back_va"])
        reads.append({"i": i, "va": x["va"], "fo": x["fo"], "width": w, "dest": dst,
                      "loops": [{k: l[k] for k in ("head_va", "back_va", "jcc", "trip_src")}
                                for l in enclosing],
                      "gate": gate_for(ins, i)})
    doc = {"schema": "t89b.read_lin.v1",
           "probe": str(PROBE.relative_to(ROOT)),
           "va_range": [hex(ins[0]["va"]), hex(ins[-1]["va"])],
           "insns": len(ins), "loops": loops, "reads": reads}
    p = ROOT / a.out
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("insns", len(ins), "loops", len(loops), "reads", len(reads), "->", a.out)
    ungated = [r for r in reads if not r["gate"] and not r["loops"]]
    print("ungated&unlooped reads:", len(ungated),
          "sum width", sum(r["width"] or 0 for r in ungated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
