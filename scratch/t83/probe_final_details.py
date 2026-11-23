import json, os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.append(r"D:\tmp2b\fm24\tools\python")
import numpy as np
import zstandard as zstd

# 1. t79 all-zero bool / constant L3 fields check
fm79 = json.loads((ROOT / "scratch/t79/out/field_map.json").read_text(encoding="utf-8"))
print("=== t79 constant/bool/date L3 fields ===")
for tbl in ("stadium_21", "team_24"):
    for f in fm79[tbl]["schema_fields"]:
        d = f.get("domain") or {}
        if f["grade"] == "L3" and (f["schema_type"] in ("boolean", "date", "string") or d.get("uniq") == 1):
            print(f"  {tbl}.{f['field']} ({f['schema_type']}): dom={str(d)[:140]}")

# 2. Check LEDGER t57 / t63 entries specifically
ledger = json.loads((ROOT / "scratch/t01/LEDGER.json").read_text(encoding="utf-8"))
entries = ledger if isinstance(ledger, list) else ledger.get("entries", [])
print("\n=== LEDGER t57 / t63 / t74 / t76b / t76c ===")
for e in entries:
    s = json.dumps(e, ensure_ascii=False)
    if any(k in s for k in ("t57", "t63", "t74", "t76b", "t76c", "E115", "E118")):
        print(f"  {e.get('id')}: {s[:350]}")

# 3. Static: 0x43e7e10 (WEATHER normalizer), 0xfe3520 (DATABASE_RECORD::get dAPw/dbnm/duni/rdui),
#    MEDIA_SOURCE::get exact 4CC dispatches, and AWARD::set / LANGUAGE::set / DERBY::set / WEATHER::set / MEDIA_SOURCE::set summary
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

print("\n=== WEATHER normalizer 0x43e7e10 ===")
s, e = fbounds(0x43e7e10)
v0 = fo_to_va(s)
for ins in md.disasm(data[s:e], v0):
    ifo = s + (ins.address - v0)
    print(f"  {ifo:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== DATABASE_RECORD::get 0xfe3520 4CC comparisons ===")
s, e = fbounds(0xfe3520)
v0 = fo_to_va(s)
for ins in md.disasm(data[s:e], v0):
    ifo = s + (ins.address - v0)
    if ins.mnemonic == "cmp" and ", 0x" in ins.op_str:
        try:
            imm = int(ins.op_str.split(", ")[1], 16)
            if 0x20202020 <= imm <= 0x7e7e7e7e:
                cc = struct.pack(">I", imm).decode("ascii")
                print(f"  {ifo:#x}: {ins.mnemonic} {ins.op_str}  ; '{cc}'")
        except Exception: pass

print("\n=== MEDIA_SOURCE::get (0x1546e60) 4CC comparisons ===")
s, e = fbounds(0x1546e60)
v0 = fo_to_va(s)
ins_l = list(md.disasm(data[s:e], v0))
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
                    try: tgt = f" -> {nxt.mnemonic} {va_to_fo(int(nxt.op_str,16)):#x}"
                    except Exception: pass
                print(f"  {ifo:#x}: '{cc}'{tgt}")
        except Exception: pass

# 4. Concrete named anchors in all 5 tables + verify table_9 vs table_10 nation mapping!
DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
def load_fmf(side, wanted):
    raw = (DB_DIR / f"{side}_db.dat").read_bytes()
    toc_off, base_off = (x + 17 for x in struct.unpack_from("<QQ", raw, 17))
    toc = zstd.ZstdDecompressor().decompressobj().decompress(raw[toc_off + 9:])
    pos = [0]; entries = {}
    def take(n): a = pos[0]; pos[0] += n; return toc[a:a+n]
    def u32(): return struct.unpack("<I", take(4))[0]
    def s(): return take(u32()).decode("utf-8")
    def walk(pfx):
        cur = pfx + s() + "/"
        for _ in range(u32()):
            nm = cur + s() + s()
            off, csz, usz, _, _ = struct.unpack("<5Q", take(40))
            entries[nm] = (base_off + off, base_off + off + csz, usz)
        for _ in range(u32()): walk(cur)
    walk("")
    out = {}
    for w in wanted:
        key = f"{side}_db/{w}"
        if key not in entries: continue
        lo, hi, usz = entries[key]
        q = lo
        while q < hi:
            dec = zstd.ZstdDecompressor().decompressobj()
            pl = dec.decompress(raw[q:hi])
            used = (hi - q) - len(dec.unused_data)
            if len(pl) == usz: out[w] = pl; break
            q += used
    return out

cli = load_fmf("client", ["table_0.dat", "table_5.dat", "table_7.dat", "table_8.dat", "table_9.dat", "table_10.dat", "table_18.dat", "table_27.dat"])
srv = load_fmf("server", ["table_7.dat", "table_18.dat"])

def scan_uids(buf):
    n = struct.unpack_from("<I", buf, 8)[0]
    uids = []
    pos = 13
    for i in range(n):
        pat = struct.pack("<I", i)
        cur = pos
        while True:
            idx = buf.find(pat, cur)
            u1, u2 = struct.unpack_from("<II", buf, idx + 4)
            if u1 == u2 and u1 not in (0, 0xFFFFFFFF):
                uids.append(u1); pos = idx + 12; break
            cur = idx + 1
    return uids

u9 = scan_uids(cli["table_9.dat"])
u10 = scan_uids(cli["table_10.dat"])
print(f"\ntable_9 vs table_10: len9={len(u9)}, len10={len(u10)}, exact_equal={u9==u10}, diff_count={sum(a!=b for a,b in zip(u9,u10))}")
print("  England ord 139: t9_uid=", u9[139], "t10_uid=", u10[139])
print("  China PR ord 55: t9_uid=", u9[55], "t10_uid=", u10[55])
# Check English language -> Lnat == 139? Chinese language -> Lnat == 55?
buf = cli["table_8.dat"]; N8 = struct.unpack_from("<I", buf, 8)[0]; pos = 13
print("\n=== LANGUAGE NAMED ANCHORS ===")
for i in range(N8):
    pos += 1; sl = struct.unpack_from("<I", buf, pos)[0]; pos += 4
    nm = buf[pos:pos+sl].decode("utf-8"); pos += sl
    suf = buf[pos:pos+29]; pos += 29
    if nm in ("English", "Chinese", "Spanish", "French", "German", "Japanese", "Korean", "Hausa", "Dzongkha"):
        linf, ldff = struct.unpack_from("<bb", suf, 1)
        lfam, lgro, lsub = struct.unpack_from("<hhh", suf, 3)
        lnat, l30, o_i, d_i = struct.unpack_from("<iiII", suf, 9)
        print(f"  row={i:3d} {nm:10s} duni={d_i:3d} Linf={linf:2d} Ldff={ldff:2d} Lfam={lfam:3d} Lgro={lgro:2d} Lsub={lsub:2d} Lnat={lnat:3d} +0x30={l30}")

# Check DERBY named anchors (North London, Manchester, El Clásico, Old Firm, etc.)
buf = srv["table_18.dat"]; N18 = struct.unpack_from("<I", buf, 8)[0]; pos = 13
print("\n=== DERBY NAMED ANCHORS ===")
for i in range(N18):
    pos += 1
    ss = []
    for _ in range(4):
        sl = struct.unpack_from("<I", buf, pos)[0]; pos += 4
        ss.append(buf[pos:pos+sl].decode("utf-8")); pos += sl
    nb = buf[pos:pos+54]; pos += 54
    if any(k in ss[0] for k in ("North London", "Manchester", "Old Firm", "El Cl", "Merseyside", "Milan", "Supercl")):
        dfmd, dtm1, dtm2, dfmc, dfms, dfma, rpdr = struct.unpack_from("<Iiiiiii", nb, 0)
        w, d, l = struct.unpack_from("<hhh", nb, 28)
        g1, g2 = struct.unpack_from("<bb", nb, 34)
        wd, nt = struct.unpack_from("<BB", nb, 40)
        o_i, d_i = struct.unpack_from("<II", nb, 42)
        print(f"  row={i:4d} {ss} duni={d_i} y={dfmd>>16} dtm=({dtm1},{dtm2}) dfmc={dfmc} dfms={dfms} att={dfma} WDL=({w},{d},{l}) G=({g1},{g2}) rep=({wd},{nt})")

# Check MEDIA named anchors
buf = srv["table_7.dat"]; N7 = struct.unpack_from("<I", buf, 8)[0]; pos = 13
print("\n=== MEDIA NAMED ANCHORS ===")
for i in range(N7):
    pos += 1
    def rl():
        global pos; l = struct.unpack_from("<I", buf, pos)[0]; pos += 4; s = buf[pos:pos+l].decode("utf-8"); pos += l; return s
    mn = rl(); _ = buf[pos]; pos += 1
    ct = struct.unpack_from("<I", buf, pos)[0]; pos += 4; mt = list(buf[pos:pos+ct]); pos += ct
    mu = rl(); mh = rl(); misf, msty = buf[pos], buf[pos+1]; pos += 2
    cc = struct.unpack_from("<I", buf, pos)[0]; pos += 4; mcmi = list(struct.unpack_from(f"<{cc}i", buf, pos)); pos += 4*cc
    mcyi = struct.unpack_from("<i", buf, pos)[0]; pos += 4
    cr = struct.unpack_from("<I", buf, pos)[0]; pos += 4; mrgi = list(struct.unpack_from(f"<{cr}i", buf, pos)); pos += 4*cr
    cn = struct.unpack_from("<I", buf, pos)[0]; pos += 4; mnti = list(struct.unpack_from(f"<{cn}i", buf, pos)); pos += 4*cn
    mcti = struct.unpack_from("<i", buf, pos)[0]; pos += 4
    ccl = struct.unpack_from("<I", buf, pos)[0]; pos += 4
    mcli = []
    for _ in range(ccl):
        u1, u2 = struct.unpack_from("<II", buf, pos); pos += 8; cu = rl(); mcli.append((u1, cu))
    mper, mscp = buf[pos], buf[pos+1]; pos += 2
    mdlp = struct.unpack_from("<I", buf, pos)[0]; pos += 4
    cj = buf[pos]; pos += 1 + 4*cj
    cln = struct.unpack_from("<I", buf, pos)[0]; pos += 4; mlnm = list(struct.unpack_from(f"<{cln}i", buf, pos)); pos += 4*cln
    mapc = buf[pos]; pos += 1
    o_i, d_i, r_i = struct.unpack_from("<III", buf, pos); pos += 12
    if i < 5 or any(k in mn for k in ("BBC", "Sky Sports", "Equipe", "Marca", "Gazzetta", "ESPN", "Cofina", "Stoke")):
        print(f"  row={i:3d} {mn!r:28s} duni={d_i} url={mu!r} typ={mt} sty={msty} per={mper} scp={mscp} apc={mapc} nti={mnti} cti={mcti} cyi={mcyi} rgi={mrgi} cmi={mcmi[:3]} cli_n={len(mcli)} lnm={mlnm}")
