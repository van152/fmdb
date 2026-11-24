#!/usr/bin/env python3
"""t89_scan — editor.exe 只读静态扫描(VA/fo/指令字节三件套)。

能力:
  --refs VA[,VA...]     在全部节里找 8 字节 LE 指针 == VA(即 vtable 槽),
                        以及 4 字节 rel32 call 目标 == VA(即调用点)
  --vtable VA           以 VA 为锚,向两侧扩展连续 qword 指针,给出槽序号
  --bytes VA,LEN        打印原始字节
  --selftest

不改任何输入;不联网;只读 D:/tmp2b/fm24/input/editor.exe。
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import pathlib
import struct
import sys

EXE = pathlib.Path(str(_cfg.EDITOR_EXE))
SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
IMAGE_BASE = 0x140000000

# 由 pefile 读出的节表(固定,便于无依赖自检)
SECTIONS = [
    (".rdata", 0x1000, 0x1758000, 0x600),
    (".debug", 0x1759000, 0x325000, 0x1758600),
    (".sbss", 0x1A7E000, 0xE9000, 0x1A7D000),
    (".code", 0x1B67000, 0x93000, 0x1ABC600),
    (".data", 0x47EB000, 0x4142C, 0x467F200),
]


def load() -> bytes:
    return EXE.read_bytes()


def va_to_fo(va: int) -> int | None:
    rva = va - IMAGE_BASE
    for name, vsz_or_va, size, fo in SECTIONS:
        if vsz_or_va <= rva < vsz_or_va + size:
            return fo + (rva - vsz_or_va)
    return None


def fo_to_va(fo: int) -> int | None:
    for name, sva, size, sfo in SECTIONS:
        if sfo <= fo < sfo + size:
            return IMAGE_BASE + sva + (fo - sfo)
    return None


def sec_of_fo(fo: int) -> str:
    for name, sva, size, sfo in SECTIONS:
        if sfo <= fo < sfo + size:
            return name
    return "?"


def scan_ptr(db: bytes, va: int, secs=None) -> list[dict]:
    """8 字节 LE 指针命中(默认全文件,含 .debug——实测 vtable 槽落在 .debug 区)。"""
    pat = struct.pack("<Q", va)
    out = []
    for name, sva, size, sfo in SECTIONS:
        if secs is not None and name not in secs:
            continue
        blob = db[sfo:sfo + size]
        i = blob.find(pat)
        while i >= 0:
            out.append({"sec": name, "fo": sfo + i, "va": IMAGE_BASE + sva + i})
            i = blob.find(pat, i + 1)
    return out


def scan_call(db: bytes, va: int) -> list[dict]:
    """E8 rel32 调用点(.rdata/.code 皆可),返回 fo/va/bytes。"""
    out = []
    for name, sva, size, sfo in SECTIONS:
        if name not in (".rdata", ".code"):
            continue
        blob = db[sfo:sfo + size]
        for i in range(0, len(blob) - 5):
            if blob[i] != 0xE8:
                continue
            src = IMAGE_BASE + sva + i
            rel = struct.unpack_from("<i", blob, i + 1)[0]
            if src + 5 + rel == va:
                out.append({"sec": name, "fo": sfo + i, "va": src,
                            "bytes": blob[i:i + 5].hex()})
    return out


def vtable_run(db: bytes, va: int, span: int = 40) -> dict:
    """以 va 所在槽为中心,向两侧扩展连续 `.rdata` 内指针,给槽号。"""
    hits = scan_ptr(db, va)
    res = []
    for h in hits:
        fo = h["fo"]
        lo = fo
        while lo - 8 >= 0x600:
            q = struct.unpack_from("<Q", db, lo - 8)[0]
            if not (IMAGE_BASE + 0x1000 <= q < IMAGE_BASE + 0x47EB000):
                break
            lo -= 8
        hi = fo + 8
        while hi + 8 <= len(db):
            q = struct.unpack_from("<Q", db, hi)[0]
            if not (IMAGE_BASE + 0x1000 <= q < IMAGE_BASE + 0x47EB000):
                break
            hi += 8
        slots = []
        for k in range(lo, min(hi, lo + 8 * span), 8):
            q = struct.unpack_from("<Q", db, k)[0]
            slots.append({"i": (k - lo) // 8, "va": f"0x{q:x}", "self": k == fo})
        res.append({"slot_fo": h["fo"], "slot_va": f"0x{h['va']:x}",
                    "run_start_fo": lo, "run_start_va": f"0x{IMAGE_BASE + 0x1000 + (lo - 0x600):x}",
                    "n_slots": (hi - lo) // 8, "index_of_va": (fo - lo) // 8,
                    "slots": slots})
    return {"va": f"0x{va:x}", "hits": len(hits), "runs": res}


def selftest() -> int:
    db = load()
    assert len(db) == 74807296, len(db)
    assert va_to_fo(0x14105d510) == 0x105cb10, hex(va_to_fo(0x14105d510))
    assert fo_to_va(0x105cb10) == 0x14105d510
    assert va_to_fo(0x141042f1e) == 0x104251e
    c = scan_call(db, 0x14105a430)
    assert c, "t9_ctor 无调用点"
    p = scan_ptr(db, 0x14105d510)
    assert p and p[0]["fo"] == 0x1888f70, p
    print("selftest OK", {"t9_ctor_calls": len(c), "t9_read_slots": len(p)})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t89 editor.exe 静态扫描")
    ap.add_argument("--refs", help="逗号分隔 VA,列指针槽+调用点")
    ap.add_argument("--vtable", help="VA,给 vtable 槽号")
    ap.add_argument("--bytes", help="VA,LEN 十六进制打印")
    ap.add_argument("--bytesfo", help="FO,LEN 十六进制打印")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    db = load()
    if a.refs:
        for s in a.refs.split(","):
            va = int(s.strip(), 16)
            print(f"## 0x{va:x} fo=0x{(va_to_fo(va) or 0):x}")
            for h in scan_ptr(db, va):
                print(f"   ptr {h['sec']} fo=0x{h['fo']:x} va=0x{h['va']:x}")
            for h in scan_call(db, va):
                print(f"   call {h['sec']} fo=0x{h['fo']:x} va=0x{h['va']:x} {h['bytes']}")
        return 0
    if a.vtable:
        print(__import__("json").dumps(vtable_run(db, int(a.vtable, 16)), indent=1))
        return 0
    if a.bytes:
        va, n = a.bytes.split(",")
        fo = va_to_fo(int(va, 16))
        if fo is None:
            print(f"va={va} 不在已收录节内", file=sys.stderr)
            return 2
        print(f"va={va} fo=0x{fo:x} {db[fo:fo + int(n, 0)].hex(' ')}")
        return 0
    if a.bytesfo:
        fo, n = a.bytesfo.split(",")
        fo = int(fo, 0)
        print(f"fo=0x{fo:x} {db[fo:fo + int(n, 0)].hex(' ')}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
