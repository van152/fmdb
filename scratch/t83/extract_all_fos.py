import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
data = EXE.read_bytes()
pe_off = struct.unpack_from("<I", data, 0x3C)[0]
num_sec = struct.unpack_from("<H", data, pe_off + 6)[0]
opt_sz = struct.unpack_from("<H", data, pe_off + 20)[0]
image_base = struct.unpack_from("<Q", data, pe_off + 24 + 24)[0]
pdata_rva, pdata_sz = struct.unpack_from("<II", data, pe_off + 24 + 112 + 3 * 8)
sections = []
sec_off = pe_off + 24 + opt_sz
for i in range(num_sec):
    o = sec_off + i * 40
    vsz, va, rsz, ra = struct.unpack_from("<IIII", data, o + 8)
    sections.append((va, max(vsz, rsz), ra, rsz))
def rva_to_fo(rva):
    for va, vsz, ra, rsz in sections:
        if va <= rva < va + rsz: return ra + (rva - va)
    raise ValueError(hex(rva))
def fo_to_va(fo):
    for va, vsz, ra, rsz in sections:
        if ra <= fo < ra + rsz: return image_base + va + (fo - ra)
    raise ValueError(hex(fo))
def va_to_fo(va): return rva_to_fo(va - image_base)

pdata_fo = rva_to_fo(pdata_rva)
funcs = []
for o in range(pdata_fo, pdata_fo + pdata_sz, 12):
    b, e, _ = struct.unpack_from("<III", data, o)
    if b == 0 and e == 0: break
    funcs.append((b, e))
import bisect
fstarts = [b for b, _ in funcs]
def fbounds(fo):
    rva = fo_to_va(fo) - image_base
    i = bisect.bisect_right(fstarts, rva) - 1
    b, e = funcs[i]
    return rva_to_fo(b), rva_to_fo(e)

md = Cs(CS_ARCH_X86, CS_MODE_64)

def scan_4cc_cmps(name, entry_fo):
    s, e = fbounds(entry_fo)
    v0 = fo_to_va(s)
    ins_l = list(md.disasm(data[s:e], v0))
    print(f"\n=== 4CC cmps in {name} ({s:#x}..{e:#x}) ===")
    for idx, ins in enumerate(ins_l):
        ifo = s + (ins.address - v0)
        if ins.mnemonic == "cmp" and ", 0x" in ins.op_str:
            try:
                imm = int(ins.op_str.split(", ")[1], 16)
                if 0x20202020 <= imm <= 0x7e7e7e7e:
                    cc = struct.pack(">I", imm).decode("ascii")
                    nxt = ins_l[idx+1] if idx+1 < len(ins_l) else None
                    tgt = ""
                    if nxt and nxt.mnemonic in ("je", "jne"):
                        try: tgt = f" {nxt.mnemonic}->{va_to_fo(int(nxt.op_str,16)):#x}"
                        except Exception: pass
                    print(f"  '{cc}' cmp@{ifo:#x}{tgt}")
            except Exception: pass

def scan_read_sinks(name, entry_fo):
    s, e = fbounds(entry_fo)
    v0 = fo_to_va(s)
    print(f"\n=== Read calls/sinks in {name} ({s:#x}..{e:#x}) ===")
    ins_l = list(md.disasm(data[s:e], v0))
    for idx, ins in enumerate(ins_l):
        ifo = s + (ins.address - v0)
        if (ins.mnemonic == "call" and ("+ 0x28" in ins.op_str or ins.op_str.startswith("0x"))) or (ins.mnemonic == "lea" and any(r in ins.op_str for r in ("[rsi", "[rdi", "[rbx", "[r14", "[r15"))):
            note = ""
            if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
                try: note = f" ; -> {va_to_fo(int(ins.op_str,16)):#x}"
                except Exception: pass
            print(f"  {ifo:#x}: {ins.mnemonic:8s} {ins.op_str}{note}")

for nm, fo in [
    ("AWARD::get", 0xe49a70), ("AWARD::set", 0xe4c240),
    ("LANGUAGE::get", 0x1038a00), ("LANGUAGE::set", 0x1039110),
    ("DERBY::get", 0xffd1b0), ("DERBY::set", 0xffdf50),
    ("WEATHER::get", 0x158e6b0), ("WEATHER::set", 0x15901a0),
    ("MEDIA::get", 0x1546e60), ("MEDIA::set", 0x154a980),
]:
    scan_4cc_cmps(nm, fo)

for nm, fo in [
    ("AWARD::read", 0xe483b0),
    ("LANGUAGE::read", 0x3d546d0),
    ("DERBY::read", 0x3d00950),
    ("WEATHER::read", 0x158b970),
    ("MEDIA::read", 0x15457c0),
]:
    scan_read_sinks(nm, fo)
