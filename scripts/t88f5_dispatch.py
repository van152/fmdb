#!/usr/bin/env python3
"""t88-fix5: TC_GET2 4CC -> (rec_type, tag) full dispatch table.

For each `cmp edx,<4CC>` in TC_GET2, follow the je target block and extract
`mov dl, 0xNN` (rec_type) and `mov r8d, <4CC>` (inner tag).

Usage: py -V:3.12 -I -B scripts/t88f5_dispatch.py [--selftest] [--out PATH]
"""
import argparse
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = str(_cfg.EDITOR_EXE)
BO = 0x140000a00
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")

# NOTE: these are FILE OFFSETS. va = BO + fo (verified: fo 0x11f0ca7 -> va 0x1411f16a7).
LO, HI = 0x11F0690, 0x11F2A00


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
    out = {}
    for k, i in enumerate(ins):
        if i.mnemonic != "cmp" or ", 0x" not in i.op_str:
            continue
        try:
            v = int(i.op_str.split(", 0x")[1], 16)
        except ValueError:
            continue
        if not is4cc(v):
            continue
        tag = cc(v)
        if tag in out:
            continue
        nxt = ins[k + 1] if k + 1 < len(ins) else None
        if nxt is None or nxt.mnemonic not in ("je", "jne"):
            continue
        tgt = int(nxt.op_str, 16)
        if nxt.mnemonic != "je" or tgt not in addr:
            out[tag] = {"cmp_fo": "0x%x" % (k - BO), "bytes": b[k - BO:k - BO + 12].hex(),
                        "rec_type": None, "inner_tag": None, "note": "jne/ unresolved"}
            continue
        st = addr[tgt]
        rt = it = None
        for j in range(st, min(st + 24, len(ins))):
            o = ins[j]
            if rt is None and o.mnemonic == "mov" and o.op_str.startswith("dl, 0x"):
                rt = int(o.op_str.split(", ")[1], 16)
            if it is None and o.mnemonic == "mov" and o.op_str.startswith("r8d, 0x"):
                vv = int(o.op_str.split(", ")[1], 16)
                if is4cc(vv):
                    it = cc(vv)
            if rt is not None and it is not None:
                break
        out[tag] = {"cmp_fo": "0x%x" % (k - BO), "bytes": b[k - BO:k - BO + 12].hex(),
                    "entry_fo": "0x%x" % (tgt - BO), "entry_va": "0x%x" % tgt,
                    "rec_type": rt, "inner_tag": it}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT3, "tcget2_dispatch.json"))
    a = ap.parse_args()
    m = build()
    if a.selftest:
        hit = [t for t, v in m.items() if v.get("rec_type") is not None]
        print("selftest tags=%d resolved=%d" % (len(m), len(hit)))
        return 0 if hit else 1
    os.makedirs(OUT3, exist_ok=True)
    json.dump(m, open(a.out, "w", encoding="utf-8"), indent=0)
    print("tags=%d -> %s" % (len(m), a.out))
    got = [(t, v) for t, v in m.items() if v.get("rec_type") is not None]
    print("resolved=%d unresolved=%d" % (len(got), len(m) - len(got)))
    for t, v in sorted(got, key=lambda x: (x[1]["rec_type"], x[0])):
        print("  %-5s rt=%-3d tag=%-5s entry=%s" % (t, v["rec_type"], v["inner_tag"], v["entry_fo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
