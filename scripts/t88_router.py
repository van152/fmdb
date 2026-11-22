#!/usr/bin/env python3
"""t88-fix7: tag-router (0x11f0b61) jump-table extraction + case-body decode.

Two dispatchers are involved in table_45 field reads:
  * RECORD_GET  0x141543ca0 : cmp edx,<tag4CC>  -> case body reads [rdi+off]
  * TAG_ROUTER  0x1411f0b61 : lea eax,[rsi-<base4CC>] / cmp eax,n / jmp table
                              -> case body emits (dl=record-type, r8d=tag4CC)

Usage:
  py -V:3.12 -I -B scripts/t88_router.py --router    [--out scratch/t88/out3/router.json]
  py -V:3.12 -I -B scripts/t88_router.py --recget    [--out scratch/t88/out3/recget.json]
  py -V:3.12 -I -B scripts/t88_router.py --selftest
Exit: 0 ok / 1 check failed / 2 usage or fatal.
"""
import argparse
import hashlib
import json
import os
import struct
import sys

import capstone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXE = os.environ.get("FM24_EDITOR_EXE", r"D:/tmp2b/fm24/input/editor.exe")
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")
BASE = 0x140000000
EXE_SHA_PREFIX = "b82ebe8e"

ROUTER_START = 0x11f0b00
ROUTER_END = 0x11f2f00
RECGET_START = 0x1543ca0
RECGET_END = 0x1546a00

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False


def load():
    d = open(EXE, "rb").read()
    sha = hashlib.sha256(d).hexdigest()
    return d, sha


def asc(v):
    """4CC immediates are packed big-endian (cmp edx,0x636f6d70 == 'comp')."""
    b = v.to_bytes(4, "big")
    return "".join(chr(c) if 32 <= c < 127 else "." for c in b)


def dis(d, fo, n=0x40):
    return list(md.disasm(d[fo:fo + n], BASE + fo))


# ---------------------------------------------------------------- router ----
def parse_router(d):
    """Walk 0x11f0b61 region: find (base4CC, n, trampoline, table) triples.

    Shape:
        lea  eax, [rsi - <base4CC>]
        cmp  eax, <n>
        ja   <generic>        ; or jbe <tramp>
        <tramp>: lea rcx,[rip+X]; movsxd rax,[rcx+rax*4]; add rax,rcx; jmp rax
    """
    insns = dis(d, ROUTER_START, ROUTER_END - ROUTER_START)
    # pass 1: trampolines (lea rcx,[rip+X] + movsxd rax,[rcx+rax*4] + add + jmp rax)
    tramp = {}
    for n, i in enumerate(insns):
        if i.mnemonic != "lea" or not i.op_str.startswith("rcx, [rip + 0x"):
            continue
        disp = int(i.op_str.split("rip + 0x")[1].rstrip("]"), 16)
        tbl = i.address + i.size + disp - BASE
        nxt = insns[n + 1:n + 4]
        if len(nxt) < 3:
            continue
        if not ("movsxd" in nxt[0].mnemonic and "rax*4" in nxt[0].op_str):
            continue
        if not (nxt[1].mnemonic == "add" and nxt[1].op_str.replace(" ", "") == "rax,rcx"):
            continue
        if not (nxt[2].mnemonic == "jmp" and nxt[2].op_str == "rax"):
            continue
        tramp[i.address - BASE] = tbl
    tables = []
    for idx, i in enumerate(insns):
        if i.mnemonic != "lea" or not i.op_str.startswith("eax, [rsi - 0x"):
            continue
        try:
            k = int(i.op_str.split("- 0x")[1].rstrip("]"), 16)
        except ValueError:
            continue
        n_val = None
        jcc = None
        jcc_tgt = None
        for j in insns[idx + 1:idx + 4]:
            if j.mnemonic == "cmp" and j.op_str.startswith("eax, 0x") and n_val is None:
                n_val = int(j.op_str.split("0x")[1], 16)
            elif j.mnemonic in ("jbe", "ja", "jae", "jb", "jne", "je") and jcc is None:
                jcc = j.mnemonic
                jcc_tgt = int(j.op_str, 16) - BASE
                break
        if n_val is None or jcc is None:
            continue
        # trampoline is either the jcc target or the fallthrough address
        fall = jcc_tgt
        cand = None
        if jcc in ("jbe", "ja"):
            cand = jcc_tgt
        else:
            cand = None
        # also allow fallthrough trampoline
        ft = None
        for j in insns[idx + 1:idx + 5]:
            if j.address - BASE in tramp:
                ft = j.address - BASE
                break
        tbl = None
        tramp_at = None
        for c in (cand, ft):
            if c in tramp:
                tbl = tramp[c]
                tramp_at = c
                break
        if tbl is None:
            continue
        ents = []
        for e in range(n_val + 1):
            rel = struct.unpack_from("<i", d, tbl + 4 * e)[0]
            ents.append({"idx": e, "code": asc(k + e), "rel": rel, "tgt": tbl + rel})
        tables.append({
            "base4cc": k, "base_code": asc(k), "n": n_val, "table_fo": tbl,
            "lea_fo": i.address - BASE, "tramp_fo": tramp_at, "guard": jcc,
            "guard_tgt": jcc_tgt, "entries": ents,
        })
    seen = {}
    for t in tables:
        seen.setdefault(t["base4cc"], t)
    return [seen[k] for k in sorted(seen)]


def imm(s):
    """Parse capstone immediate operand (hex or decimal)."""
    s = s.strip().rstrip("]")
    return int(s, 16) if s.startswith("0x") else int(s, 10)


def decode_case(d, tgt, depth=0):
    """Decode a case body: returns {rt, tag, kind}."""
    out = {"tgt": tgt, "rt": None, "tag": None, "kind": "unknown", "insn": []}
    if tgt == 0x11f2a95:
        out["kind"] = "router_generic"
        return out
    if tgt == 0x11f2a5a:
        out["kind"] = "router_otht"
        out["tag"] = "otht"
        return out
    if tgt == 0x11f2a60:
        out["kind"] = "router_case"
        return out
    insns = dis(d, tgt, 0x30)
    for i in insns[:8]:
        out["insn"].append("%s %s" % (i.mnemonic, i.op_str))
        if i.mnemonic == "mov" and i.op_str.startswith("dl, ") and out["rt"] is None:
            out["rt"] = imm(i.op_str[4:])
        elif i.mnemonic == "mov" and i.op_str.startswith("r8d, ") and out["tag"] is None:
            out["tag"] = asc(imm(i.op_str[5:]))
        elif i.mnemonic == "jmp":
            t = i.op_str
            if t == "0x1411f2a60":
                out["kind"] = "router_case"
            elif t == "0x1411f2a5a":
                out["kind"] = "router_otht"
                out["tag"] = "otht"
            elif t == "0x1411f2a95":
                out["kind"] = "router_generic"
            elif t.startswith("0x1411f0"):
                out["kind"] = "router_defer"
            else:
                out["kind"] = "jmp_other"
            out["jmp"] = t
            break
    return out


# --------------------------------------------------------------- recget ----
def parse_recget(d):
    """0x1543ca0: cmp edx,<tag> ... je <body>; body reads [rdi+off]."""
    insns = dis(d, RECGET_START, RECGET_END - RECGET_START)
    addr = {i.address: n for n, i in enumerate(insns)}
    cases = []
    for n, i in enumerate(insns):
        if i.mnemonic == "cmp" and i.op_str.startswith("edx, "):
            v = imm(i.op_str[5:])
            if not (0x20202020 <= v <= 0x7e7e7e7e):
                continue
            # find je within next 2 insns
            for j in insns[n + 1:n + 3]:
                if j.mnemonic == "je":
                    cases.append({"tag": asc(v), "cmp_fo": i.address - BASE,
                                  "body_fo": int(j.op_str, 16) - BASE})
                    break
    out = {}
    for c in cases:
        body = dis(d, c["body_fo"], 0x60)
        reads = []
        for i in body[:24]:
            if i.mnemonic in ("mov", "movsx", "movzx", "movsxd") and "ptr [rdi + 0x" in i.op_str:
                off = int(i.op_str.split("[rdi + 0x")[1].split("]")[0], 16)
                width = 1 if "byte" in i.op_str else 2 if "word" in i.op_str else 4
                reads.append({"off": off, "w": width, "insn": "%s %s" % (i.mnemonic, i.op_str)})
            if i.mnemonic.startswith("jmp") or i.mnemonic == "ret":
                break
        rec = {"tag": c["tag"], "cmp_fo": c["cmp_fo"], "body_fo": c["body_fo"], "reads": reads}
        out.setdefault(c["tag"], []).append(rec)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--router", action="store_true")
    ap.add_argument("--recget", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if not (a.router or a.recget or a.selftest):
        ap.print_help()
        return 2
    d, sha = load()
    if not sha.startswith(EXE_SHA_PREFIX):
        print("FATAL editor.exe sha mismatch", sha)
        return 2
    os.makedirs(OUT3, exist_ok=True)
    if a.selftest or a.router:
        tabs = parse_router(d)
        print("tables=%d" % len(tabs))
        for t in tabs:
            ks = [decode_case(d, e["tgt"]) for e in t["entries"]]
            kinds = {}
            for k in ks:
                kinds[k["kind"]] = kinds.get(k["kind"], 0) + 1
            print("  %-4s n=%2d tbl=%#x guard=%s %s" %
                  (t["base_code"], t["n"], t["table_fo"], t["guard"], kinds))
        if a.out or a.router:
            dst = a.out or os.path.join(OUT3, "router.json")
            for t in tabs:
                t["cases"] = [decode_case(d, e["tgt"]) for e in t["entries"]]
            json.dump({"meta": {"task": "t88-fix7", "exe_sha256_prefix": sha[:8],
                                "router_va": hex(BASE + ROUTER_START)},
                       "tables": tabs}, open(dst, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print("wrote", dst)
    if a.selftest or a.recget:
        rg = parse_recget(d)
        print("recget tags=%d" % len(rg))
        print("  " + " ".join(sorted(rg)))
        if a.recget:
            dst = a.out or os.path.join(OUT3, "recget.json")
            json.dump({"meta": {"task": "t88-fix7", "exe_sha256_prefix": sha[:8],
                                "recget_va": hex(BASE + RECGET_START)},
                       "cases": rg}, open(dst, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
