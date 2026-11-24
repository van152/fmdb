#!/usr/bin/env python3
"""t88-fix7: whole-binary scan for the tag-router dispatch idiom.

Idiom (both known clusters, 0x1411f0b61 and 0x140ec02ff):
    lea  eax, [rsi - <base4CC>]        ; 8d 86 disp32  (displacement is NEGATIVE base)
    cmp  eax, <n>                      ; 83 f8 n     or  3d n32
    jcc  <generic/tramp>
    [tramp] lea rcx,[rip+X]; movsxd rax,[rcx+rax*4]; add rax,rcx; jmp rax
    case:  mov rcx,<rec>; mov dl,<rt>; mov r8d,<tag4CC>; jmp <common>

Also records the bitmask variant (mov ecx,imm32; bt ecx,eax; jae ...).

Usage:
  py -V:3.12 -I -B scripts/t88_tagsweep.py [--out F] [--selftest]
Exit: 0 ok / 1 check failed / 2 usage or fatal.
"""
import argparse
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import hashlib
import json
import os
import struct
import sys

import capstone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXE = os.environ.get("FM24_EDITOR_EXE", str(_cfg.EDITOR_EXE))
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")
BASE = 0x140000000
SHA_PREFIX = "b82ebe8e"

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def asc(v):
    return "".join(chr(c) if 32 <= c < 127 else "." for c in v.to_bytes(4, "big"))


def imm(s):
    s = s.strip().rstrip("]")
    try:
        return int(s, 16) if s.startswith("0x") else int(s, 10)
    except ValueError:
        return None


def find_leas(d):
    """All `lea eax,[rsi - K]` sites where K looks like a printable 4CC."""
    out = []
    i = 0
    while True:
        i = d.find(b"\x8d\x86", i)
        if i < 0:
            break
        disp = struct.unpack_from("<i", d, i + 2)[0]
        v = (0 - disp) & 0xFFFFFFFF
        if 0x41000000 <= v <= 0x5A5A5A5A and all(32 <= c < 127 for c in v.to_bytes(4, "big")):
            out.append((i, v))
        i += 1
    return out


def read_n(d, i):
    """cmp eax,<n> right after the lea -> (n, next_off) or None."""
    j = i + 6
    if d[j] == 0x83 and d[j + 1] == 0xF8:
        return d[j + 2], j + 3
    if d[j] == 0x3D:
        return struct.unpack_from("<i", d, j + 1)[0], j + 5
    return None, j


def dis_after(d, fo, n=14):
    return list(md.disasm(d[fo:fo + 80], BASE + fo))[:n]


def find_tramp(d, start_fo, jcc_tgt_fo, limit=14):
    """Return (table_fo, tramp_fo) by locating lea rcx,[rip+X]; movsxd; add; jmp rax."""
    cands = [jcc_tgt_fo] + [i.address - BASE for i in dis_after(d, start_fo, limit)]
    for c in cands:
        if c is None or c < 0:
            continue
        ins = dis_after(d, c, 5)
        if len(ins) < 4:
            continue
        a, b, e, f = ins[0], ins[1], ins[2], ins[3]
        if not (a.mnemonic == "lea" and a.op_str.startswith("rcx, [rip + 0x")):
            continue
        if not (b.mnemonic == "movsxd" and "rax*4" in b.op_str):
            continue
        if not (e.mnemonic == "add" and e.op_str.replace(" ", "") == "rax,rcx"):
            continue
        if not (f.mnemonic == "jmp" and f.op_str == "rax"):
            continue
        disp = int(a.op_str.split("rip + 0x")[1].rstrip("]"), 16)
        return a.address + a.size + disp - BASE, c
    return None, None


def decode_case(d, tgt):
    out = {"tgt": tgt, "rt": None, "tag": None, "kind": "unknown", "seq": []}
    ins = dis_after(d, tgt, 10)
    for i in ins:
        out["seq"].append("%s %s" % (i.mnemonic, i.op_str))
        if i.mnemonic == "mov" and i.op_str.startswith("dl, ") and out["rt"] is None:
            v = imm(i.op_str[4:])
            if v is not None:
                out["rt"] = v
        elif i.mnemonic == "mov" and i.op_str.startswith("r8d, ") and out["tag"] is None:
            v = imm(i.op_str[5:])
            if v is not None:
                out["tag"] = asc(v)
        elif i.mnemonic == "jmp":
            out["kind"] = "case" if out["rt"] is not None or out["tag"] is not None else "defer"
            out["jmp"] = i.op_str
            break
        elif i.mnemonic in ("call", "ret"):
            out["kind"] = "inline"
            break
    return out


def sweep(d):
    sites = find_leas(d)
    tabs = []
    for fo, k in sites:
        n, nxt = read_n(d, fo)
        if n is None or not (0 < n < 64):
            continue
        ins = dis_after(d, nxt, 6)
        jcc = None
        jtgt = None
        for i in ins:
            if i.mnemonic in ("ja", "jbe", "jae", "jb", "jg", "jle", "je", "jne"):
                jcc, jtgt = i.mnemonic, int(i.op_str, 16) - BASE
                break
            if i.mnemonic == "bt":
                jcc = "bt"
                break
        if jcc is None:
            continue
        if jcc == "bt":
            mask = None
            for i in ins:
                if i.mnemonic == "mov" and i.op_str.startswith("ecx, "):
                    mask = imm(i.op_str[5:])
            tabs.append({"base4cc": k, "base_code": asc(k), "n": n, "lea_fo": fo,
                         "guard": "bt", "mask": mask, "table_fo": None, "entries": [],
                         "cases": []})
            continue
        tbl, tramp = find_tramp(d, nxt, jtgt)
        if tbl is None:
            tabs.append({"base4cc": k, "base_code": asc(k), "n": n, "lea_fo": fo,
                         "guard": jcc, "guard_tgt": jtgt, "table_fo": None,
                         "entries": [], "cases": []})
            continue
        ents, cases = [], []
        for e in range(n + 1):
            rel = struct.unpack_from("<i", d, tbl + 4 * e)[0]
            tgt = tbl + rel
            ents.append({"idx": e, "code": asc(k + e), "tgt": tgt})
            cases.append(decode_case(d, tgt))
        tabs.append({"base4cc": k, "base_code": asc(k), "n": n, "lea_fo": fo,
                     "guard": jcc, "guard_tgt": jtgt, "tramp_fo": tramp,
                     "table_fo": tbl, "entries": ents, "cases": cases})
    seen = {}
    for t in tabs:
        seen.setdefault((t["base4cc"], t["lea_fo"]), t)
    return [seen[k] for k in sorted(seen)]


def sweep_inline(d):
    """Inline variant: cmp <r32>,<4CC> ; jcc ; [body: mov dl,rt ; mov r8d,tag ; jmp common]

    je -> body at target; jne -> body at fallthrough.
    Two register flavours exist: cmp esi (0xec0xxx cluster) and cmp ebx (0xe8axxx cluster).
    """
    out = []
    for reg, name in ((b"\x81\xfe", "esi"), (b"\x81\xfb", "ebx"),
                      (b"\x81\xfa", "edx"), (b"\x81\xf9", "ecx"),
                      (b"\x81\xff", "edi")):
        i = 0
        while True:
            i = d.find(reg, i)
            if i < 0:
                break
            v = struct.unpack_from("<I", d, i + 2)[0]
            if not (0x41000000 <= v <= 0x5A5A5A5A):
                i += 1
                continue
            raw = v.to_bytes(4, "big")
            if not all(32 <= c < 127 for c in raw):
                i += 1
                continue
            code = raw.decode("ascii")
            ins = dis_after(d, i + 6, 2)
            if not ins or ins[0].mnemonic not in ("je", "jne", "jg", "jle", "ja", "jbe"):
                i += 1
                continue
            j = ins[0]
            body = (int(j.op_str, 16) - BASE) if j.mnemonic == "je" else (j.address - BASE + j.size)
            case = decode_case(d, body)
            if case["rt"] is None and case["tag"] is None:
                i += 1
                continue
            case["code"] = code
            case["cmp_fo"] = i
            case["reg"] = name
            case["via"] = j.mnemonic
            out.append(case)
            i += 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(OUT3, "tagsweep.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    d = open(EXE, "rb").read()
    sha = hashlib.sha256(d).hexdigest()
    if not sha.startswith(SHA_PREFIX):
        print("FATAL editor.exe sha mismatch", sha)
        return 2
    tabs = sweep(d)
    inline = sweep_inline(d)
    withtbl = [t for t in tabs if t["table_fo"] is not None]
    print("lea sites=%d tables=%d (with jumptable %d)" %
          (len(find_leas(d)), len(tabs), len(withtbl)))
    hit = sum(1 for t in withtbl for c in t["cases"] if c["rt"] is not None)
    print("cases with rt=%d  with tag=%d" %
          (hit, sum(1 for t in withtbl for c in t["cases"] if c["tag"])))
    print("inline cmp-esi cases=%d (distinct codes=%d)" %
          (len(inline), len({c["code"] for c in inline})))
    clusters = {}
    for t in tabs:
        clusters.setdefault(t["lea_fo"] >> 16, []).append(t["base_code"])
    for k in sorted(clusters):
        print("  cluster %#x: %d tables" % (k << 16, len(clusters[k])))
    json.dump({"meta": {"task": "t88-fix7", "exe_sha256_prefix": sha[:8],
                        "note": "case.rt = record type byte (dl), case.tag = 4CC (r8d)"},
               "tables": tabs, "inline": inline},
              open(a.out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
