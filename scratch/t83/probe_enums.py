import json, os, struct, sys
from pathlib import Path
from collections import Counter

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.append(r"D:\tmp2b\fm24\tools\python")
import numpy as np
import zstandard as zstd

DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
enums_map = master["enums"]

def parse_enum_entry(em):
    if not em:
        return None
    out = []
    for x in em.get("values", []):
        v = x.get("enum_id")
        if v is None:
            v = x.get("enum")
        if v is None:
            v = x.get("id")
        try:
            out.append(int(v, 0) if isinstance(v, str) else int(v))
        except Exception:
            out.append(v)
    return out

for ek in ("award.xml", "language.xml", "media source.xml"):
    print(f"\n--- {ek} enum/list fields ---")
    for f in master["entities"][ek][0]["fields"]:
        if f["type"] in ("enum", "list"):
            fid = f["field"]
            eref = f.get("enum_ref")
            em = enums_map.get(eref or fid) or enums_map.get(fid)
            vals = parse_enum_entry(em)
            print(f"  {fid:5s} ({f['type']:4s}) eref={eref} | in_enums={em is not None} n={len(vals) if vals is not None else 0} vals={vals[:14] if vals else vals}" + (f"..{vals[-3:]}" if vals and len(vals)>14 else ""))
            if f["type"] == "list":
                for sf in f.get("list_item_fields", []):
                    sfid = sf["field"]
                    sref = sf.get("enum_ref") or sfid
                    sem = enums_map.get(sref)
                    svals = parse_enum_entry(sem)
                    print(f"    sub {sfid:5s} ({sf['type']:25s}) eref={sf.get('enum_ref')} in_enums={sem is not None} vals={svals}")

# Check ALL enum keys in master["enums"] that exist for award/language/media
print("\n=== ALL master['enums'] matching our 5 entities ===")
for k in sorted(enums_map.keys()):
    em = enums_map[k]
    fn = str(em.get("file", ""))
    if any(k.startswith(p) for p in ("AW", "L", "M", "fom")) or any(w in fn.lower() for w in ("award", "lang", "media")):
        vals = parse_enum_entry(em)
        print(f"  [{k:12s}] n={len(vals) if vals else 0:3d} vals={vals[:12] if vals else []}..{vals[-3:] if vals and len(vals)>12 else ''} | {fn}")

# Now load tables and check EVERY enum field!
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

cli = load_fmf("client", ["table_0.dat", "table_7.dat", "table_8.dat", "table_25.dat"])
srv = load_fmf("server", ["table_0.dat", "table_7.dat", "table_8.dat", "table_25.dat"])

# AWARD
N0 = struct.unpack_from("<I", cli["table_0.dat"], 8)[0]
AB = np.frombuffer(cli["table_0.dat"], dtype=np.uint8, offset=13, count=N0*77).reshape(N0, 77)[:, 1:]
duni0 = AB[:, 68:72].copy().view("<u4").ravel()
af = {f["field"]: f for f in master["entities"]["award.xml"][0]["fields"]}

print("\n=== AWARD FULL ENUM AUDIT ===")
for fid, off, dt in [
    ("AWsc", 2, "i8"), ("AWty", 17, "i8"), ("AWdr", 18, "i8"), ("AWrb", 35, "i8"),
    ("AWfo", 37, "i8"), ("AWbr", 45, "i8"), ("AWsr", 46, "i8"), ("AWss", 47, "i8"),
    ("AWap", 50, "i8"), ("AWrt", 51, "i8"), ("AWvf", 52, "i8"), ("AWpo", 55, "u32"), ("AWnp", 59, "i8"),
]:
    v = AB[:, off].view(np.int8).astype(np.int64) if dt == "i8" else AB[:, off:off+4].copy().view("<u4").ravel().astype(np.int64)
    eref = af[fid].get("enum_ref") or fid
    em = enums_map.get(eref)
    allowed = parse_enum_entry(em)
    if allowed is None:
        print(f"  {fid:5s}@{off:2d}: NO ENUM IN master.enums! hist={dict(Counter(v.tolist()))}")
    else:
        aset = set(x for x in allowed if isinstance(x, int))
        bad = [(i, int(duni0[i]), int(v[i])) for i in range(N0) if int(v[i]) not in aset]
        print(f"  {fid:5s}@{off:2d} enum[{eref}] len={len(aset)} ({min(aset)}..{max(aset)}): bad={len(bad)}, bad_vals={dict(Counter(x[2] for x in bad))}"
              + (f", first={bad[0]}" if bad else " [PASS]"))

# Check AWmi == comp UID 0x5f5e117 (100000023)
# Scan table_25 UIDs
buf25 = cli["table_25.dat"]
n25 = struct.unpack_from("<I", buf25, 8)[0]
st25 = (len(buf25) - 22) // n25
A25 = np.frombuffer(buf25, dtype=np.uint8, offset=13, count=n25*st25).reshape(n25, st25)
u25 = A25[:, st25-8:st25-4].copy().view("<u4").ravel()
hit25 = np.nonzero(u25 == 0x5f5e117)[0].tolist()
print(f"\nCOMP UID 0x5f5e117 (100000023) ordinal in table_25: {hit25}")
if hit25:
    awmi = AB[:, 41:45].copy().view("<i4").ravel()
    rows_h = np.nonzero(awmi == hit25[0])[0].tolist()
    print(f"  AWARD rows referencing that comp: {[(r, int(duni0[r]), int(AB[r,45]), int(AB[r,51])) for r in rows_h]}")

# LANGUAGE
buf = cli["table_8.dat"]
N8 = struct.unpack_from("<I", buf, 8)[0]
pos = 13
l_names = []; l_suf = np.empty((N8, 29), dtype=np.uint8)
for i in range(N8):
    pos += 1
    sl = struct.unpack_from("<I", buf, pos)[0]; pos += 4
    l_names.append(buf[pos:pos+sl].decode("utf-8")); pos += sl
    l_suf[i] = np.frombuffer(buf, dtype=np.uint8, offset=pos, count=29); pos += 29
duni8 = l_suf[:, 21:25].copy().view("<u4").ravel()
lf = {f["field"]: f for f in master["entities"]["language.xml"][0]["fields"]}
print("\n=== LANGUAGE FULL ENUM AUDIT ===")
for fid, off in [("Lfam", 3), ("Lgro", 5), ("Lsub", 7)]:
    v = l_suf[:, off:off+2].copy().view("<i2").ravel().astype(np.int64)
    eref = lf[fid].get("enum_ref") or fid
    em = enums_map.get(eref)
    allowed = parse_enum_entry(em)
    if allowed is None:
        print(f"  {fid:5s}@suf+{off}: NO ENUM IN master.enums! min={int(v.min())}, max={int(v.max())}, uniq={len(set(v.tolist()))}")
    else:
        aset = set(x for x in allowed if isinstance(x, int))
        bad = [(i, l_names[i], int(duni8[i]), int(v[i])) for i in range(N8) if int(v[i]) not in aset]
        print(f"  {fid:5s}@suf+{off} enum[{eref}] len={len(aset)} ({min(aset)}..{max(aset)}): bad={len(bad)}, bad_vals={dict(Counter(x[3] for x in bad))}"
              + (f", first={bad[0]}" if bad else " [PASS]"))

# MEDIA_SOURCE
def parse_media_srv(buf):
    N7 = struct.unpack_from("<I", buf, 8)[0]
    pos = 13
    rows = []
    for i in range(N7):
        pos += 1
        def rd_lstr():
            nonlocal pos; l = struct.unpack_from("<I", buf, pos)[0]; pos += 4; s = buf[pos:pos+l].decode("utf-8"); pos += l; return s
        def rd_u8():
            nonlocal pos; v = buf[pos]; pos += 1; return v
        def rd_i32():
            nonlocal pos; v = struct.unpack_from("<i", buf, pos)[0]; pos += 4; return v
        def rd_u32():
            nonlocal pos; v = struct.unpack_from("<I", buf, pos)[0]; pos += 4; return v
        def rd_vec():
            c = rd_u32(); return [rd_i32() for _ in range(c)]
        Mnam = rd_lstr(); _ = rd_u8(); c_t = rd_u32(); Mtyp = [rd_u8() for _ in range(c_t)]
        Murl = rd_lstr(); Mhtg = rd_lstr(); Misf = rd_u8(); Msty = rd_u8()
        Mcmi = rd_vec(); Mcyi = rd_i32(); Mrgi = rd_vec(); Mnti = rd_vec(); Mcti = rd_i32()
        c_cl = rd_u32()
        for _ in range(c_cl): rd_u32(); rd_u32(); rd_lstr()
        Mper = rd_u8(); Mscp = rd_u8(); Mdlp = rd_u32(); c_j = rd_u8()
        for _ in range(c_j): rd_i32()
        Mlnm = rd_vec(); Mapc = rd_u8()
        o_i = rd_u32(); d_i = rd_u32(); r_i = rd_u32()
        rows.append((Mnam, d_i, Mtyp, Misf, Msty, Mper, Mscp, Mdlp, Mapc))
    return rows

mf = {f["field"]: f for f in master["entities"]["media source.xml"][0]["fields"]}
m_rows = parse_media_srv(srv["table_7.dat"])
print("\n=== MEDIA FULL ENUM AUDIT ===")
for fid, getter in [("Mtyp", lambda r: r[2]), ("Msty", lambda r: [r[4]]), ("Mper", lambda r: [r[5]]), ("Mscp", lambda r: [r[6]])]:
    f = mf[fid]
    eref = f.get("enum_ref") or fid
    em = enums_map.get(eref)
    allowed = parse_enum_entry(em)
    if allowed is None:
        print(f"  {fid:5s}: NO ENUM IN master.enums! hist={dict(Counter(v for r in m_rows for v in getter(r)))}")
    else:
        aset = set(x for x in allowed if isinstance(x, int))
        bad = [(i, r[0], r[1], v) for i, r in enumerate(m_rows) for v in getter(r) if v not in aset]
        print(f"  {fid:5s} enum[{eref}] len={len(aset)} ({min(aset)}..{max(aset)}): bad={len(bad)}, bad_vals={dict(Counter(x[3] for x in bad))}"
              + (f", first={bad[0]}" if bad else " [PASS]"))
