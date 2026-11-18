"""t05_pe — PE 地址映射基础设施(file offset <-> RVA <-> VA)。

editor.exe 的段布局非标准(section 名是误导的, 代码在 .rdata/.reloc 里),
且各段 file_offset 与 RVA 偏移不同:
    .rdata : VA 0x1000   RawPtr 0x600      -> delta 0xA00
    .reloc : VA 0x1c64000 RawPtr 0x1af8a00 -> delta 0x16B600

任何 thunk 跳转目标 / census 记录的 file_offset 都必须走这张表换算,
否则会落到乱码区(这是 t05_reader_widths 先前 thunk 跟进失败的原因)。
"""
from __future__ import annotations

from pathlib import Path

import pefile

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")


class PE:
    def __init__(self, path: Path = EXE):
        self.path = Path(path)
        self.raw = self.path.read_bytes()
        self.pe = pefile.PE(str(self.path), fast_load=True)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self._secs = []
        for s in self.pe.sections:
            self._secs.append({
                "name": s.Name.rstrip(b"\x00").decode("latin1"),
                "va": s.VirtualAddress,
                "vsize": max(s.Misc_VirtualSize, s.SizeOfRawData),
                "raw": s.PointerToRawData,
                "rawsize": s.SizeOfRawData,
                "exec": bool(s.Characteristics & 0x20000000),
            })

    # ---- 换算 ----
    def f2r(self, off: int) -> int | None:
        for s in self._secs:
            if s["raw"] <= off < s["raw"] + s["rawsize"]:
                return off - s["raw"] + s["va"]
        return None

    def r2f(self, rva: int) -> int | None:
        for s in self._secs:
            if s["va"] <= rva < s["va"] + s["vsize"]:
                return rva - s["va"] + s["raw"]
        return None

    def f2va(self, off: int) -> int | None:
        r = self.f2r(off)
        return None if r is None else self.base + r

    def va2f(self, va: int) -> int | None:
        return self.r2f(va - self.base)

    def section_of(self, off: int) -> str:
        for s in self._secs:
            if s["raw"] <= off < s["raw"] + s["rawsize"]:
                return s["name"]
        return "?"

    def is_code_like(self, off: int, want: int = 12) -> bool:
        """粗略判断该偏移是否是函数/代码起点(前几条指令合法且不是垃圾)。"""
        from capstone import CS_ARCH_X86, CS_MODE_64, Cs

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        ins = list(md.disasm(self.raw[off:off + 24], off))
        if not ins:
            return False
        ok = sum(1 for i in ins[:6] if i.mnemonic not in ("invalid", "db", "(bad)"))
        return ok >= min(4, want) and ins[0].mnemonic not in ("int", "int3", "out")

    def follow_jmp(self, off: int) -> int | None:
        """若 off 处是 `jmp <target>`, 返回 target 的 file offset(已做 PE 换算)。"""
        from capstone import CS_ARCH_X86, CS_MODE_64, Cs

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        va = self.f2va(off)
        if va is None:
            return None
        ins = list(md.disasm(self.raw[off:off + 8], va))
        if not ins or ins[0].mnemonic != "jmp":
            return None
        try:
            target_va = int(ins[0].op_str.replace(" ", ""), 0)
        except ValueError:
            return None
        return self.va2f(target_va)

    def resolve(self, off: int, max_hops: int = 8) -> dict:
        """跟随 jmp 跳板链, 返回 {body, chain, resolved}。"""
        chain = [off]
        cur = off
        for _ in range(max_hops):
            nxt = self.follow_jmp(cur)
            if nxt is None or nxt in chain or not (0 < nxt < len(self.raw)):
                break
            chain.append(nxt)
            cur = nxt
        return {"body": cur, "chain": chain, "resolved": len(chain) > 1}


_DEFAULT: PE | None = None


def default() -> PE:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = PE()
    return _DEFAULT


if __name__ == "__main__":
    import sys

    pe = default()
    print(f"ImageBase {pe.base:#x}  file size {len(pe.raw):#x}")
    print(f"{'name':<10}{'VA':>10}{'VSize':>10}{'RawPtr':>11}{'RawSize':>10}  exec")
    for s in pe._secs:
        print(f"{s['name']:<10}{s['va']:#10x}{s['vsize']:#10x}{s['raw']:#11x}{s['rawsize']:#10x}  {s['exec']}")
    print()
    print("自检: 已知锚点换算")
    for off, want_rva in ((0x157fe70, 0x1580870), (0x3b3f0d0, 0x3d0a6d0)):
        got = pe.f2r(off)
        print(f"  f2r({off:#x}) = {got:#x}  expect {want_rva:#x}  {'OK' if got == want_rva else 'MISMATCH'}")
    print()
    print("thunk 解析测试:")
    for off in (0xed0a40, 0xe54c20, 0xed5d10, 0x10376d0):
        r = pe.resolve(off)
        codish = pe.is_code_like(r["body"])
        print(f"  {off:#x} -> body {r['body']:#x} chain={[hex(x) for x in r['chain']]} "
              f"section={pe.section_of(r['body'])} code_like={codish}")
    sys.exit(0)
