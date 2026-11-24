#!/usr/bin/env python3
"""t89_pe — 从 editor.exe PE 头解析真实节表(替代 t89_scan 里的硬编码表)。

用法:
  py -V:3.12 -I -B scripts/t89_pe.py --sections
  py -V:3.12 -I -B scripts/t89_pe.py --va 0x143779990 --len 0x40
  py -V:3.12 -I -B scripts/t89_pe.py --selftest
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
IMAGE_BASE = 0x140000000


def sections() -> list[dict]:
    db = EXE.read_bytes()
    pe = struct.unpack_from("<I", db, 0x3C)[0]
    assert db[pe:pe + 4] == b"PE\0\0", db[pe:pe + 4]
    nsec = struct.unpack_from("<H", db, pe + 6)[0]
    optsz = struct.unpack_from("<H", db, pe + 20)[0]
    opt = pe + 24
    magic = struct.unpack_from("<H", db, opt)[0]
    assert magic == 0x20B, hex(magic)          # PE32+
    imgbase = struct.unpack_from("<Q", db, opt + 24)[0]
    secoff = opt + optsz
    out = []
    for i in range(nsec):
        b = secoff + 40 * i
        name = db[b:b + 8].rstrip(b"\0").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", db, b + 8)
        out.append({"name": name, "va": vaddr, "vsize": vsize,
                    "fo": rawptr, "rawsize": rawsize,
                    "image_base": imgbase})
    return out


def va_to_fo(va: int) -> int | None:
    rva = va - IMAGE_BASE
    for s in sections():
        if s["va"] <= rva < s["va"] + max(s["vsize"], s["rawsize"]):
            return s["fo"] + (rva - s["va"])
    return None


def disasm(va: int, n: int) -> list[dict]:
    import capstone
    db = EXE.read_bytes()
    fo = va_to_fo(va)
    if fo is None:
        raise SystemExit(f"VA 0x{va:x} 不在任何节")
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    out = []
    for ins in md.disasm(db[fo:fo + n], va):
        out.append({"va": ins.address, "bytes": ins.bytes.hex(),
                    "mn": ins.mnemonic, "op": ins.op_str,
                    "text": f"{ins.mnemonic} {ins.op_str}".strip()})
    return out


def selftest() -> int:
    sec = sections()
    names = [s["name"] for s in sec]
    assert ".text" in names or ".code" in names, names
    # 条目读取器应落在可执行节
    fo = va_to_fo(0x1408386A0)
    assert fo is not None and EXE.read_bytes()[fo] == 0x55, (fo,)
    assert va_to_fo(0x143779990) is not None, "0x143779990 应可解析"
    print("selftest OK", {"sections": len(sec), "names": names})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="editor.exe PE 节表解析")
    ap.add_argument("--sections", action="store_true")
    ap.add_argument("--va")
    ap.add_argument("--len", default="0x40")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.sections:
        for s in sections():
            print(f"{s['name']:10s} va=0x{s['va']+IMAGE_BASE:x} "
                  f"vsize=0x{s['vsize']:x} fo=0x{s['fo']:x} raw=0x{s['rawsize']:x}")
        return 0
    if a.va:
        va = int(a.va, 16)
        fo = va_to_fo(va)
        if fo is None:
            print(f"VA 0x{va:x} 不在任何节", file=sys.stderr)
            return 1
        db = EXE.read_bytes()
        n = int(a.len, 0)
        import capstone
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        for ins in md.disasm(db[fo:fo + n], va):
            print(f"0x{ins.address:x} {ins.bytes.hex():<20s} {ins.mnemonic} {ins.op_str}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
