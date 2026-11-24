#!/usr/bin/env python3
"""t88-fix5: full RECORD_GET tag -> mem offset map (all 4CC cases).

RECORD_GET @ fo 0x1543ca0 (va 0x1415446a0). Each case: cmp edx, <4CC>; je <target>.
Target block reads the record object via [rdi + disp] (sometimes [rsi + disp]).

Usage: py -V:3.12 -I -B scripts/t88f5_recget.py [--selftest] [--out PATH]
"""
import argparse
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = str(_cfg.EDITOR_EXE)
BO = 0x140000a00
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")

LO, HI = 0x1543ca0, 0x1545400


def cc(v):
    return struct.pack("<I", v)[::-1].decode("latin1")


def is4cc(v):
    return 0x20202020 <= v <= 0x7A7A7A7A and all(32 <= c < 127 for c in struct.pack("<I", v))


def build():
    import capstone
    b = open(EXE, "rb").read()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    ins = list(md.disasm(b[LO:HI], BO + LO))
    addr = {i.address: k for k, i in enumerate(ins)}
    cases = {}
    for k, i in enumerate(ins):
        if i.mnemonic != "cmp" or ", 0x" not in i.op_str:
            continue
        try:
            v = int(i.op_str.split(", 0x")[1], 16)
        except ValueError:
            continue
        if not is4cc(v):
            continue
        nxt = ins[k + 1] if k + 1 < len(ins) else None
        if nxt is None or nxt.mnemonic not in ("je", "jne"):
            continue
        cases.setdefault(i.address, (cc(v), nxt.mnemonic, int(nxt.op_str, 16)))
    # handler blocks: bound by the *next handler entry* (je targets), not the cmp sites
    entries = sorted({t for _, jm, t in cases.values() if jm == "je"})
    out = {}
    for k, (tag, jm, tgt) in sorted(cases.items(), key=lambda kv: kv[1][0]):
        if jm != "je" or tgt not in addr:
            continue
        start = addr[tgt]
        nxt = min([a for a in entries if a > tgt] or [HI])
        end = addr.get(nxt, len(ins))
        blk = ins[start:end]
        reads = []
        for i in blk:
            for m in re.finditer(r"\[(\w+) \+ (0x[0-9a-f]+)\]", i.op_str):
                reads.append((m.group(1), int(m.group(2), 16), i.mnemonic, i.op_str))
        # keep only record-base regs seen with several offsets
        out[tag] = {
            "cmp_fo": "0x%x" % (k - BO), "cmp_va": "0x%x" % k,
            "bytes": b[k - BO:k - BO + 12].hex(),
            "entry_fo": "0x%x" % (tgt - BO), "entry_va": "0x%x" % tgt,
            "n_insn": len(blk),
            "reads": [[r[0], "0x%x" % r[1], r[2], r[3]] for r in reads],
            "offs": sorted({r[1] for r in reads}),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT3, "recget_tagmap.json"))
    a = ap.parse_args()
    m = build()
    if a.selftest:
        ok = "stdb" in m and 0x48 in m.get("stdb", {}).get("offs", [])
        print("selftest tags=%d stdb@0x48=%s" % (len(m), ok))
        return 0 if ok else 1
    os.makedirs(OUT3, exist_ok=True)
    json.dump(m, open(a.out, "w", encoding="utf-8"), indent=0)
    print("tags=%d -> %s" % (len(m), a.out))
    for t in sorted(m):
        print("%-5s entry=%s offs=%s" % (t, m[t]["entry_fo"],
              " ".join("0x%x" % o for o in m[t]["offs"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
