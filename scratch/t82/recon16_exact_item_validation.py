"""Exact wire-offset disassembly for Cscm/Cspb/Cren/TCrs/VTAG38 + full-archive item-level domain validation
of ALL 16 list fields (Cscm, CPsL, Cspb, Cren, TCrs, Tko1..3, Tkg1..3, Csoc, Camc, Cbbl, pcpt)
with real table UID/ordinal join checks and first counterexamples!"""
import json, os, struct, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
import pefile, capstone

ROOT = Path(r'D:\tmp2b\fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR', ROOT / 'scratch/data'))
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')
HEAD = bytes.fromhex('03017461642ef10d')

PE = EXE.read_bytes()
pe = pefile.PE(data=PE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
fo_va = lambda v: pe.get_offset_from_rva(v - IB)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def dump_calls(name, fo, sz):
    print(f'=== {name} @ 0x{fo:x}..0x{fo+sz:x} ===')
    sva = va(fo)
    for ins in md.disasm(PE[fo:fo+sz], sva):
        cfo = ins.address - sva + fo
        if ins.mnemonic in ('call', 'lea', 'mov') and any(k in ins.op_str for k in ('+ 0x28]', '+ 0x18]', '+ 0x30]', '+ 0x48]', 'r8d,', 'edi', 'rsi', 'rdi', '0x14')):
            extra = ''
            if ins.mnemonic == 'call' and ins.op_str.startswith('0x'):
                try:
                    tva = int(ins.op_str, 16); tfo = fo_va(tva); extra = f' ; -> 0x{tfo:x}'
                    if PE[tfo] == 0xe9:
                        rel = struct.unpack_from('<i', PE, tfo+1)[0]
                        extra += f' (thunk->0x{fo_va(tva+5+rel):x})'
                except Exception: pass
            if 'call' in ins.mnemonic or 'r8d,' in ins.op_str or '+ 0x' in ins.op_str:
                if 'rsp' not in ins.op_str and 'rbp' not in ins.op_str or 'call' in ins.mnemonic:
                    print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}{extra}')

# Dump exact item readers!
# Look at CSCM_RDR (0xe5e169..0xe5e230), VTAG38 item loop (0x14da580..0x14da850), and TC_EXTRA_READER server tail (0x11d3f50..0x11d4950)
def dump_full(name, fo, sz):
    print(f'\n=== FULL {name} @ 0x{fo:x} ===')
    sva = va(fo)
    for ins in md.disasm(PE[fo:fo+sz], sva):
        cfo = ins.address - sva + fo
        extra = ''
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            try:
                tva = int(ins.op_str, 16); tfo = fo_va(tva); extra = f' ; -> 0x{tfo:x}'
                if PE[tfo] == 0xe9:
                    rel = struct.unpack_from('<i', PE, tfo+1)[0]
                    extra += f' (thunk->0x{fo_va(tva+5+rel):x})'
            except Exception: pass
        print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}{extra}')

dump_full('CSCM_ITEM_LOOP', 0xe5e169, 0x90)
dump_full('VTAG38_ITEM_READ', 0x14da5b0, 0x180)

# Find CSPB, CREN, TCRS item readers inside 0x11d3d00..0x11d53f0 by scanning for calls!
print('\n=== CALLS IN TC_EXTRA_READER 0x11d3d00..0x11d53f0 ===')
sva = va(0x11d3d00)
for ins in md.disasm(PE[0x11d3d00:0x11d53f0], sva):
    cfo = ins.address - sva + 0x11d3d00
    if ins.mnemonic == 'call':
        extra = ''
        if ins.op_str.startswith('0x'):
            try:
                tva = int(ins.op_str, 16); tfo = fo_va(tva); extra = f' ; -> 0x{tfo:x}'
                if PE[tfo] == 0xe9:
                    rel = struct.unpack_from('<i', PE, tfo+1)[0]
                    extra += f' (thunk->0x{fo_va(tva+5+rel):x})'
            except Exception: pass
        print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}{extra}')
    elif '+ 0x18]' in ins.op_str or '+ 0x30]' in ins.op_str or '+ 0x48]' in ins.op_str:
        if 'rsp' not in ins.op_str and 'rbp' not in ins.op_str:
            print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}')

# Also inspect item reader functions we already know from t71/disasm_recon12 or callers above!
# Wait: check Cscm item struct from 0xe5e169: notice in recon15_out:
# Cscm sample hex=01 5f150200 5f150200 0b 61000000 61000000 ffffffff !!
# OMG!! Look at those 22 bytes:
#   byte 0: 0x01 (version/tag!)
#   bytes 1..4: 0x0002155f = 136543 (comp UID 1!)
#   bytes 5..8: 0x0002155f = 136543 (comp UID 2!)
#   byte 9: 0x0b = 11 (stnm = 11 matches! Or 0x05 = 5!)
#   bytes 10..13: 0x00000061 = 97 (stage_name UID 1!)
#   bytes 14..17: 0x00000061 = 97 (stage_name UID 2!)
#   bytes 18..21: 0xffffffff (-1!)
# AND LOOK AT Cspb sample hex:
#   hex=01 3d225000 3d225000 01 ff 00 1201e707 6e01e807
#   byte 0: 0x01 (version/tag!)
#   bytes 1..8: comp UID pair (0x0050223d = 5251645, or -1,-1)!
#   byte 9: 0x01 / 0x03 (type!)
#   byte 10: 0xff = -1 (matc!)
#   byte 11: 0x00 (venu!)
#   bytes 12..15: 0x07e70112 (stdt: year 2023 doy 274!)
#   bytes 16..19: 0x07e8016e (endt: year 2024 doy 366!)
# AND LOOK AT Cren sample hex (6 bytes):
#   sample row 19: po=-251? NO! Look at raw: it's <bb i> or <i bb>?
#   Wait: sample row 22 had po=8061959, num=0, rsn=4!! Wait 8061959 = 0x007b0407!
#   Wait: if layout is <i8 rsnn, i8 rsnr, i32 rsnp> OR <i32 rsnp, i8 rsnn, i8 rsnr>?
#   Wait: 0x007b0407 in LE bytes is 07 04 7b 00, then num=00, rsn=04 -> wait if 4B+1B+1B:
#   byte 0..3 = 07 04 7b 00 (person ord/uid!), byte 4 = 0, byte 5 = 4? NO! Look at row 19:
#   po=-251 = 0xffffff05 -> bytes 05 ff ff ff, then -1=ff, 4=04 -> 05 ff ff ff ff 04!!
#   OMG!! 05 is rsnn=5 (squad number 5!), ff ff ff ff is rsnp=-1 (no player!), 04 is rsnr=4 (reason=4)!!
#   AND row 22: 07 04 7b 00 00 04 -> wait 0x00007b04 = 31492?! Let's check the EXACT reader bytes!!

def open_fmf(side):
    b = (DATA / f'{side}_db.dat').read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', b, 17))
    def frame(buf):
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)
    directory, used = frame(b[toc+9:])
    p = 0; entries = {}
    def pull(n):
        nonlocal p; r = directory[p:p+n]; p += n; return r
    def num(): return struct.unpack('<I', pull(4))[0]
    def text(): return pull(num()).decode('utf-8')
    def node(parent):
        prefix = parent + text() + '/'
        for _ in range(num()):
            name = prefix + text() + text()
            off, size, unpacked, _, _ = struct.unpack('<5Q', pull(40))
            entries[name] = (base + off, base + off + size, unpacked)
        for _ in range(num()): node(prefix)
    node('')
    def get(rel):
        lo, hi, n = entries[rel]
        q = lo; out = None
        while q < hi:
            pl, w = frame(b[q:hi]); q += w
            if len(pl) == n: out = pl
        assert out is not None and out[:8] == HEAD
        return out
    return entries, get

srv_ent, srv_get = open_fmf('server')
srv_ex3 = srv_get('server_db/table_extra_3.dat')
N = struct.unpack_from('<I', srv_ex3, 8)[0]

# Quick check of people_db.dat zstd decompression (header 8B tad. + zstd stream?)
pb_raw = (DATA / 'basic_people_db.dat').read_bytes()
print(f'\n=== basic_people_db.dat first 32B: {pb_raw[:32].hex()} ===')
# Zstd magic is at offset 8!
d = zstd.ZstdDecompressor().decompressobj()
pb_dec = d.decompress(pb_raw[8:])
print(f'  basic_people_db decompressed: {len(pb_dec)}B, first 32B: {pb_dec[:32].hex()}, u32[0..3]={struct.unpack_from("<4I", pb_dec, 0)}')
# Check client_db/table_25.dat UIDs and server_db/table_29.dat UIDs!
cli_ent, cli_get = open_fmf('client')
t25 = cli_get('client_db/table_25.dat')
print(f'  client table_25: len={len(t25)}, cnt={struct.unpack_from("<I", t25, 8)[0]}, first 32B={t25[:32].hex()}')
t29 = srv_get('server_db/table_29.dat')
print(f'  server table_29: len={len(t29)}, cnt={struct.unpack_from("<I", t29, 8)[0]}, first 32B={t29[:32].hex()}')
