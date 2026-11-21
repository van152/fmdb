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

def get_allowed_enum(f):
    if f.get("enum_values"):
        return sorted(int(x.get("enum_id", x.get("enum"))) for x in f["enum_values"])
    eref = f.get("enum_ref")
    if eref and eref in enums_map:
        vals = enums_map[eref].get("values", [])
        return sorted(int(x.get("enum_id", x.get("enum"))) for x in vals)
    return None

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

cli = load_fmf("client", ["table_0.dat", "table_7.dat", "table_8.dat", "table_18.dat", "table_27.dat"])
srv = load_fmf("server", ["table_0.dat", "table_7.dat", "table_8.dat", "table_18.dat", "table_27.dat"])

# Helper to get schema field dict
def fdict(ek):
    return {f["field"]: f for f in master["entities"][ek][0]["fields"]}

# 1. AWARD
af = fdict("award.xml")
N0 = struct.unpack_from("<I", cli["table_0.dat"], 8)[0]
AB = np.frombuffer(cli["table_0.dat"], dtype=np.uint8, offset=13, count=N0*77).reshape(N0, 77)[:, 1:]
duni0 = AB[:, 68:72].copy().view("<u4").ravel()

print("=== AWARD ENUM & RANGE VIOLATIONS ===")
aw_cols = [
    ("AWsc", 2, "i8", False),
    ("AWre", 15, "i16", False),
    ("AWty", 17, "i8", False),
    ("AWdr", 18, "i8", False),
    ("AWrb", 35, "i8", False),
    ("AWfo", 37, "i8", False),
    ("AWxa", 38, "u8", True),  # getter suppresses <=0
    ("AWwh", 39, "u8", True),  # getter suppresses ==0
    ("AWwr", 40, "u8", True),  # getter suppresses ==0
    ("AWbr", 45, "i8", False),
    ("AWsr", 46, "i8", False),
    ("AWss", 47, "i8", False),
    ("AWap", 50, "i8", False),
    ("AWrt", 51, "i8", False),
    ("AWvf", 52, "i8", False),
    ("AWmg", 53, "u8", True),  # getter suppresses <=0
    ("AWma", 54, "u8", True),  # getter suppresses <=0
    ("AWpo", 55, "u32", False),
    ("AWnp", 59, "i8", False),
]
for fid, off, dt, sup0 in aw_cols:
    f = af[fid]
    if dt == "i8": v = AB[:, off].view(np.int8).astype(np.int64)
    elif dt == "u8": v = AB[:, off].astype(np.int64)
    elif dt == "i16": v = AB[:, off:off+2].copy().view("<i2").ravel().astype(np.int64)
    elif dt == "u32": v = AB[:, off:off+4].copy().view("<u4").ravel().astype(np.int64)
    allowed = get_allowed_enum(f)
    mn = int(f["min_value"]) if "min_value" in f else None
    mx = int(f["max_value"]) if "max_value" in f else None
    live_mask = (v > 0) if sup0 else np.ones(N0, dtype=bool)
    bad_idx = []
    if allowed is not None:
        aset = set(allowed)
        bad_idx = [i for i in range(N0) if live_mask[i] and int(v[i]) not in aset]
        bad_vals = Counter(int(v[i]) for i in bad_idx)
        print(f"  {fid:5s}@{off:2d} enum(len={len(allowed)}, {allowed[:6]}..{allowed[-3:]}): bad={len(bad_idx)}, bad_vals={dict(bad_vals)}"
              + (f", first=(row={bad_idx[0]}, duni={int(duni0[bad_idx[0]])}, val={int(v[bad_idx[0]])})" if bad_idx else " [PASS]"))
    elif mn is not None or mx is not None:
        bad_idx = [i for i in range(N0) if live_mask[i] and ((mn is not None and int(v[i]) < mn) or (mx is not None and int(v[i]) > mx))]
        bad_vals = Counter(int(v[i]) for i in bad_idx)
        print(f"  {fid:5s}@{off:2d} range[{mn}..{mx}] sup0={sup0}: live={int(live_mask.sum())}, bad={len(bad_idx)}, bad_vals={dict(bad_vals)}"
              + (f", first=(row={bad_idx[0]}, duni={int(duni0[bad_idx[0]])}, val={int(v[bad_idx[0]])})" if bad_idx else " [PASS]"))

# Note on AWbr/AWrt fixup: check if any award has AWmi pointing to comp UID 0x5f5e117 (100000023)!
# 2. LANGUAGE
lf = fdict("language.xml")
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
print("\n=== LANGUAGE ENUM & RANGE VIOLATIONS ===")
for fid, off, dt in [("Linf", 1, "i8"), ("Ldff", 2, "i8"), ("Lfam", 3, "i16"), ("Lgro", 5, "i16"), ("Lsub", 7, "i16")]:
    f = lf[fid]
    v = l_suf[:, off].view(np.int8).astype(np.int64) if dt == "i8" else l_suf[:, off:off+2].copy().view("<i2").ravel().astype(np.int64)
    allowed = get_allowed_enum(f)
    mn = int(f["min_value"]) if "min_value" in f else None
    mx = int(f["max_value"]) if "max_value" in f else None
    if allowed is not None:
        aset = set(allowed)
        bad_idx = [i for i in range(N8) if int(v[i]) not in aset]
        bad_vals = Counter(int(v[i]) for i in bad_idx)
        print(f"  {fid:5s}@suf+{off} enum(len={len(allowed)}, {allowed[:5]}..{allowed[-3:]}): bad={len(bad_idx)}, bad_vals={dict(bad_vals)}"
              + (f", first=(row={bad_idx[0]}, name={l_names[bad_idx[0]]!r}, duni={int(duni8[bad_idx[0]])}, val={int(v[bad_idx[0]])})" if bad_idx else " [PASS]"))
    else:
        bad_idx = [i for i in range(N8) if int(v[i]) < mn or int(v[i]) > mx]
        print(f"  {fid:5s}@suf+{off} range[{mn}..{mx}]: bad={len(bad_idx)} [PASS]" if not bad_idx else f"  {fid} bad={len(bad_idx)}")

# 3. MEDIA_SOURCE
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

mf = fdict("media source.xml")
m_rows = parse_media_srv(srv["table_7.dat"])

print("\n=== MEDIA ENUM & BOOL VIOLATIONS ===")
for fid, getter in [
    ("Msty", lambda r: [r[4]]),
    ("Mper", lambda r: [r[5]]),
    ("Mscp", lambda r: [r[6]]),
    ("Mtyp", lambda r: r[2]),
    ("Misf", lambda r: [r[3]]),
    ("Mapc", lambda r: [r[8]]),
]:
    f = mf[fid]
    allowed = get_allowed_enum(f)
    if fid == "Mtyp":
        # Mtyp is a list of subfields? Let's inspect f!
        print(f"  Mtyp schema keys={list(f.keys())}, sub={str(f.get('fields') or f.get('list_fields') or f.get('enum_values'))[:220]}")
    if allowed is not None:
        aset = set(allowed)
        bad = [(i, r[0], r[1], v) for i, r in enumerate(m_rows) for v in getter(r) if v not in aset]
        print(f"  {fid:5s} enum({allowed}): bad={len(bad)}, bad_vals={dict(Counter(x[3] for x in bad))}"
              + (f", first={bad[0]}" if bad else " [PASS]"))
    elif f["type"] == "boolean":
        bad = [(i, r[0], r[1], v) for i, r in enumerate(m_rows) for v in getter(r) if v not in (0, 1)]
        print(f"  {fid:5s} bool: bad={len(bad)} [PASS]")
