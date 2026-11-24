#!/usr/bin/env python3
"""t88_pe — 从 editor.exe 真 PE 头解析全部节表,建立 fo<->VA 映射(只读)。

用法:
  py -V:3.12 -I -B scripts/t88_pe.py --sections
  py -V:3.12 -I -B scripts/t88_pe.py --va 0x1411f0ca7 --len 0x40
  py -V:3.12 -I -B scripts/t88_pe.py --dump-json scratch/t88/out3/pe_sections.json
  py -V:3.12 -I -B scripts/t88_pe.py --selftest

退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import hashlib
import json
import pathlib
import struct
import sys

EXE = pathlib.Path(str(_cfg.EDITOR_EXE))


class PE:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.db = path.read_bytes()
        db = self.db
        pe = struct.unpack_from("<I", db, 0x3C)[0]
        if db[pe:pe + 4] != b"PE\0\0":
            raise SystemExit(f"非 PE: {db[pe:pe+4]!r}")
        self.pe_off = pe
        self.machine, self.nsec = struct.unpack_from("<HH", db, pe + 4)
        optsz = struct.unpack_from("<H", db, pe + 20)[0]
        opt = pe + 24
        self.magic = struct.unpack_from("<H", db, opt)[0]
        if self.magic == 0x20B:
            self.image_base = struct.unpack_from("<Q", db, opt + 24)[0]
            self.size_of_image = struct.unpack_from("<I", db, opt + 56)[0]
            self.entry_rva = struct.unpack_from("<I", db, opt + 16)[0]
        elif self.magic == 0x10B:
            self.image_base = struct.unpack_from("<I", db, opt + 28)[0]
            self.size_of_image = struct.unpack_from("<I", db, opt + 56)[0]
            self.entry_rva = struct.unpack_from("<I", db, opt + 16)[0]
        else:
            raise SystemExit(f"未知 optional magic 0x{self.magic:x}")
        secoff = opt + optsz
        self.sections = []
        for i in range(self.nsec):
            b = secoff + 40 * i
            name = db[b:b + 8].rstrip(b"\0").decode("ascii", "replace")
            vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", db, b + 8)
            chars = struct.unpack_from("<I", db, b + 36)[0]
            self.sections.append({
                "idx": i, "name": name,
                "rva": vaddr, "va": self.image_base + vaddr,
                "vsize": vsize, "fo": rawptr, "rawsize": rawsize,
                "fo_end": rawptr + rawsize,
                "chars": chars,
                "exec": bool(chars & 0x20000000),
                "readable": bool(chars & 0x40000000),
                "writable": bool(chars & 0x80000000),
            })
        self.sha256 = hashlib.sha256(db).hexdigest()

    def rva_to_fo(self, rva: int) -> int | None:
        for s in self.sections:
            span = max(s["vsize"], s["rawsize"])
            if s["rva"] <= rva < s["rva"] + span:
                delta = rva - s["rva"]
                if delta >= s["rawsize"]:
                    return None  # 未初始化尾部(虚拟 > 原始)
                return s["fo"] + delta
        return None

    def va_to_fo(self, va: int) -> int | None:
        if va < self.image_base:
            return None
        return self.rva_to_fo(va - self.image_base)

    def section_of_va(self, va: int) -> dict | None:
        rva = va - self.image_base
        for s in self.sections:
            if s["rva"] <= rva < s["rva"] + max(s["vsize"], s["rawsize"]):
                return s
        return None

    def read(self, va: int, n: int) -> bytes:
        fo = self.va_to_fo(va)
        if fo is None:
            raise KeyError(f"VA 0x{va:x} 无文件映射")
        return self.db[fo:fo + n]


def disasm(pe: PE, va: int, n: int) -> list[dict]:
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    code = pe.read(va, n)
    out = []
    for ins in md.disasm(code, va):
        out.append({"va": f"0x{ins.address:x}", "bytes": ins.bytes.hex(),
                    "mn": ins.mnemonic, "op": ins.op_str,
                    "text": f"{ins.mnemonic} {ins.op_str}".strip()})
    return out


def selftest() -> int:
    pe = PE(EXE)
    assert pe.magic == 0x20B and pe.image_base == 0x140000000, (hex(pe.magic), hex(pe.image_base))
    names = [s["name"] for s in pe.sections]
    assert len(names) >= 5, names
    assert any(s["exec"] for s in pe.sections), "无可执行节"
    # 入口点可解析
    assert pe.rva_to_fo(pe.entry_rva) is not None
    # 反向自洽:每节首字节 fo 可回读
    for s in pe.sections:
        if s["rawsize"]:
            assert pe.va_to_fo(s["va"]) == s["fo"], s["name"]
    # 已知锚点:0x1408386A0 首字节 0x55 (push rbp)
    assert pe.read(0x1408386A0, 1) == b"\x55"
    # 5 个任务地址:4 个须有文件映射
    for va in (0x1411F0CA7, 0x1411F0CB6, 0x143EBAD50, 0x141543CA0):
        assert pe.va_to_fo(va) is not None, hex(va)
    # 0x141B60190 落 .sbss 未初始化区(BSS 全局指针,无静态初值)→ 无文件映射是正确结论
    sec = pe.section_of_va(0x141B60190)
    assert sec is not None and sec["name"] == ".sbss", sec
    assert pe.va_to_fo(0x141B60190) is None
    # 真节表必须多于旧硬编码 5 节
    assert len(pe.sections) > 5, len(pe.sections)
    print("selftest OK", {"nsec": len(names), "names": names,
                          "sha256": pe.sha256[:8]})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="editor.exe 真 PE 节表 / fo-VA 映射")
    ap.add_argument("--sections", action="store_true")
    ap.add_argument("--va")
    ap.add_argument("--len", default="0x40")
    ap.add_argument("--dump-json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    pe = PE(EXE)
    if a.sections:
        print(f"image_base=0x{pe.image_base:x} nsec={pe.nsec} sha={pe.sha256[:8]}")
        for s in pe.sections:
            print(f"{s['idx']:2d} {s['name']:10s} rva=0x{s['rva']:08x} "
                  f"vsize=0x{s['vsize']:07x} fo=0x{s['fo']:08x} raw=0x{s['rawsize']:07x} "
                  f"{'X' if s['exec'] else '-'}{'R' if s['readable'] else '-'}"
                  f"{'W' if s['writable'] else '-'}")
        return 0
    if a.dump_json:
        obj = {"exe": str(EXE), "sha256": pe.sha256,
               "sha256_prefix": pe.sha256[:8],
               "image_base": pe.image_base, "entry_rva": pe.entry_rva,
               "size_of_image": pe.size_of_image,
               "nsec": pe.nsec, "sections": pe.sections}
        p = pathlib.Path(a.dump_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=1), encoding="utf-8")
        print("wrote", p, len(pe.sections), "sections")
        return 0
    if a.va:
        va = int(a.va, 16)
        fo = pe.va_to_fo(va)
        if fo is None:
            print(f"VA 0x{va:x} 不在任何节", file=sys.stderr)
            return 1
        sec = pe.section_of_va(va)
        print(f"VA=0x{va:x} fo=0x{fo:x} section={sec['name']}")
        for ins in disasm(pe, va, int(a.len, 0)):
            print(f"{ins['va']} {ins['bytes']:<22s} {ins['text']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
