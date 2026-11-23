"""Disasm helper via pefile VA->FO (covers all sections incl .reloc)."""
import sys
import pefile
import capstone

PE = r"D:\tmp2b\fm24\input\editor.exe"


def va_to_fo(pe, va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            if s.PointerToRawData == 0:
                return None
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None


def disasm(va, before=0x40, after=0x80):
    pe = pefile.PE(PE, fast_load=True)
    raw = open(PE, "rb").read()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    start = va - before
    fo = va_to_fo(pe, start)
    if fo is None:
        print(f"VA 0x{va:x}: no file backing (bss/virtual)")
        return
    n = before + after
    for ins in md.disasm(raw[fo : fo + n], start):
        mark = " <<" if ins.address == va else ""
        print(f"0x{ins.address:x}  {ins.bytes.hex():<24s} {ins.mnemonic} {ins.op_str}{mark}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    va = int(sys.argv[1], 0)
    b = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x40
    a = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x80
    disasm(va, b, a)
