import json, os, struct, sys, hashlib
from pathlib import Path
from collections import Counter

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.append(r"D:\tmp2b\fm24\tools\python")
import numpy as np
import zstandard as zstd

DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
MASTER_PATH = ROOT / "evidence/fm24/reports/editor_schema/master.json"
master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))

# First inspect master.json structure for our 5 entities & enums
print("=== MASTER.JSON ENUMS & FIELDS ===")
enums = master.get("enums", {})
ent_keys = ["award.xml", "language.xml", "weather.xml", "derby.xml", "media source.xml"]
for ek in ent_keys:
    ent = master["entities"][ek]
    print(f"Entity {ek}: type={type(ent).__name__}, len={len(ent)}")
    if isinstance(ent, list):
        fields = ent
    else:
        fields = ent.get("fields", [])
    for f in fields:
        en = f.get("enum") or f.get("enum_id") or f.get("list_id")
        extra = {k: v for k, v in f.items() if k not in ("id", "name", "type", "min", "max", "default", "read_only", "optional", "hidden")}
        if extra:
            s_ex = json.dumps(extra, ensure_ascii=False)
            if len(s_ex) > 160:
                s_ex = s_ex[:160] + "..."
            print(f"  {ek} {f.get('id')} ({f.get('type')}): {s_ex}")
for k in ["foms"]:
    if k in enums:
        print(f"enums[{k}] = {enums[k]}")

# Load FMF archives
def load_fmf(side: str, wanted: list[str]) -> dict[str, bytes]:
    raw = (DB_DIR / f"{side}_db.dat").read_bytes()
    toc_off, base_off = (x + 17 for x in struct.unpack_from("<QQ", raw, 17))
    toc = zstd.ZstdDecompressor().decompressobj().decompress(raw[toc_off + 9:])
    pos = [0]
    entries = {}
    def take(n):
        a = pos[0]; pos[0] += n; return toc[a:a+n]
    def u32(): return struct.unpack("<I", take(4))[0]
    def s(): return take(u32()).decode("utf-8")
    def walk(pfx):
        cur = pfx + s() + "/"
        for _ in range(u32()):
            nm = cur + s() + s()
            off, csz, usz, _, _ = struct.unpack("<5Q", take(40))
            entries[nm] = (base_off + off, base_off + off + csz, usz)
        for _ in range(u32()):
            walk(cur)
    walk("")
    out = {}
    for w in wanted:
        key = f"{side}_db/{w}"
        if key not in entries:
            continue
        lo, hi, usz = entries[key]
        q = lo
        while q < hi:
            dec = zstd.ZstdDecompressor().decompressobj()
            pl = dec.decompress(raw[q:hi])
            used = (hi - q) - len(dec.unused_data)
            if len(pl) == usz:
                out[w] = pl
                break
            q += used
    return out

wanted_tables = [
    "table_0.dat", "table_1.dat", "table_2.dat", "table_3.dat", "table_5.dat",
    "table_7.dat", "table_8.dat", "table_9.dat", "table_10.dat", "table_12.dat",
    "table_18.dat", "table_21.dat", "table_24.dat", "table_25.dat", "table_27.dat",
    "table_30.dat", "table_47.dat",
]
cli = load_fmf("client", wanted_tables)
srv = load_fmf("server", wanted_tables)
print("\nLoaded client:", {k: len(v) for k, v in cli.items()})
print("Loaded server:", {k: len(v) for k, v in srv.items()})

def scan_uids(buf: bytes) -> np.ndarray:
    n = struct.unpack_from("<I", buf, 8)[0]
    if n == 0:
        return np.empty(0, dtype=np.uint32)
    if (len(buf) - 22) % n == 0:
        st = (len(buf) - 22) // n
        arr = np.frombuffer(buf, dtype=np.uint8, offset=13, count=n * st).reshape(n, st)
        if np.array_equal(arr[:, st - 12:st - 8].copy().view("<u4").ravel(), np.arange(n, dtype=np.uint32)):
            u1 = arr[:, st - 8:st - 4].copy().view("<u4").ravel()
            u2 = arr[:, st - 4:st].copy().view("<u4").ravel()
            if np.array_equal(u1, u2):
                return u1
    uids = np.empty(n, dtype=np.uint32)
    pos = 13
    for i in range(n):
        pat = struct.pack("<I", i)
        cur = pos
        while True:
            idx = buf.find(pat, cur)
            assert idx != -1 and idx + 12 <= len(buf) - 9, f"scan failed at i={i}"
            u1, u2 = struct.unpack_from("<II", buf, idx + 4)
            if u1 == u2 and u1 not in (0, 0xFFFFFFFF):
                uids[i] = u1
                pos = idx + 12
                break
            cur = idx + 1
    return uids

# Build target UID sets & counts
ref_uids = {}
ref_n = {}
for tid in (0, 2, 3, 5, 7, 8, 9, 10, 12, 18, 21, 24, 25, 27, 30, 47):
    k = f"table_{tid}.dat"
    buf = srv.get(k) or cli.get(k)
    if buf is None:
        continue
    u = scan_uids(buf)
    ref_uids[tid] = set(int(x) for x in u)
    ref_n[tid] = len(u)
print("\nRef table counts:", ref_n)

def fk_report(vals: np.ndarray, tid: int, label: str = ""):
    v = np.asarray(vals, dtype=np.int32)
    n = len(v)
    null_m1 = int((v == -1).sum())
    other_neg = int(((v < 0) & (v != -1)).sum())
    zero_cnt = int((v == 0).sum())
    live = v[v >= 0]
    n_live = len(live)
    in_ord = int((live < ref_n[tid]).sum())
    miss_ord = n_live - in_ord
    uset = ref_uids[tid]
    wrong_uid_hits = sum(1 for x in live.tolist() if x in uset)
    wrong_uid_miss = n_live - wrong_uid_hits
    mn = int(live.min()) if n_live else None
    mx = int(live.max()) if n_live else None
    print(f"  FK {label:12s} -> t{tid:2d} (N={ref_n[tid]:6d}): live={n_live:5d} (0={zero_cnt}), -1={null_m1:5d}, neg!={other_neg}, ord_ok={in_ord}, ord_miss={miss_ord}, min={mn}, max={mx} | wrong_uid_hits={wrong_uid_hits}/{n_live}")

def check_dates(vals: np.ndarray, label: str = "", allow_zero: bool = False):
    v = np.asarray(vals, dtype="<u4")
    y = v >> 16
    d = v & 0x1FF
    rem = (v >> 9) & 0x7F
    leap = (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))
    ok = (rem == 0) & (y >= 1) & (d >= 1) & (d <= 365 + leap)
    if allow_zero:
        ok = ok | (v == 0)
    bad = v[~ok]
    c_1900 = int((v == 0x076c0001).sum())
    c_zero = int((v == 0).sum())
    print(f"  DATE {label:10s}: n={len(v)}, bad={len(bad)}, zero={c_zero}, 1900-01-01={c_1900}, y=[{int(y[ok].min()) if ok.any() else None}..{int(y[ok].max()) if ok.any() else None}]" + (f" bad_sample={[hex(int(x)) for x in bad[:5]]}" if len(bad) else ""))

# ==========================================================
# 1. TABLE 0 — AWARD (77B fixed, 3545 rows)
# ==========================================================
print("\n==================== TABLE 0: AWARD ====================")
a_cli, a_srv = cli["table_0.dat"], srv["table_0.dat"]
print("client==server:", a_cli == a_srv, "len:", len(a_cli), "hdr_n:", struct.unpack_from("<I", a_cli, 8)[0])
N0 = struct.unpack_from("<I", a_cli, 8)[0]
assert len(a_cli) == 13 + N0 * 77 + 9
# native row: byte 0 = selector, bytes 1..64 = body@0..63, bytes 65..76 = id(ord, duni, rdui)
A = np.frombuffer(a_cli, dtype=np.uint8, offset=13, count=N0 * 77).reshape(N0, 77)
print("sel unique:", np.unique(A[:, 0]).tolist())
AB = A[:, 1:]  # AB[:, off] matches t74/fm24_dump body@off!
ord0 = AB[:, 64:68].copy().view("<u4").ravel()
duni0 = AB[:, 68:72].copy().view("<u4").ravel()
rdui0 = AB[:, 72:76].copy().view("<u4").ravel()
print(f"id: ord==0..N-1: {np.array_equal(ord0, np.arange(N0, dtype=np.uint32))}, duni unique: {len(np.unique(duni0))}, duni==rdui: {int((duni0==rdui0).sum())}/{N0}")

def col_i8(B, off): return B[:, off].view(np.int8)
def col_u8(B, off): return B[:, off]
def col_i16(B, off): return B[:, off:off+2].copy().view("<i2").ravel()
def col_u16(B, off): return B[:, off:off+2].copy().view("<u2").ravel()
def col_i32(B, off): return B[:, off:off+4].copy().view("<i4").ravel()
def col_u32(B, off): return B[:, off:off+4].copy().view("<u4").ravel()

for off, nm, kind in [
    (0, "int_+7e", "u8"), (1, "int_+7f", "u8"), (2, "AWsc", "i8"),
    (3, "int_col0", "u8"), (4, "AWfc", "u16"), (6, "AWbc", "u16"), (8, "AWtc", "u16"),
    (10, "int_col4", "u16"), (12, "int_col6", "u16"), (14, "int_col8", "u8"),
    (15, "AWre", "i16"), (17, "AWty", "i8"), (18, "AWdr", "i8"),
    (35, "AWrb", "i8"), (36, "dSAw", "u8"), (37, "AWfo", "i8"),
    (38, "AWxa", "u8"), (39, "AWwh", "u8"), (40, "AWwr", "u8"),
    (45, "AWbr", "i8"), (46, "AWsr", "i8"), (47, "AWss", "i8"),
    (48, "int_+8c", "u8"), (49, "AWus/op", "u8"),
    (50, "AWap", "i8"), (51, "AWrt", "i8"), (52, "AWvf", "i8"),
    (53, "AWmg", "u8"), (54, "AWma", "u8"), (55, "AWpo", "u32"),
    (59, "AWnp", "i8"),
]:
    v = {"u8": col_u8, "i8": col_i8, "i16": col_i16, "u16": col_u16, "u32": col_u32}[kind](AB, off)
    u, cnt = np.unique(v, return_counts=True)
    if len(u) <= 18:
        hist = {int(k): int(c) for k, c in zip(u, cnt)}
        print(f"  @{off:2d} {nm:8s} ({kind:3s}): min={int(v.min())}, max={int(v.max())}, hist={hist}")
    else:
        print(f"  @{off:2d} {nm:8s} ({kind:3s}): min={int(v.min())}, max={int(v.max())}, uniq={len(u)}, top5={sorted(zip(cnt.tolist(), u.tolist()), reverse=True)[:5]}")

check_dates(col_u32(AB, 19), "AWda@19")
check_dates(col_u32(AB, 60), "AWad@60")
fk_report(col_i32(AB, 23), 5, "AWci@23")
fk_report(col_i32(AB, 27), 10, "AWni@27->10")
fk_report(col_i32(AB, 27), 9, "AWni@27->9")
fk_report(col_i32(AB, 31), 47, "int+68@31")
fk_report(col_i32(AB, 41), 25, "AWmi@41")

# Check AWpo bitmask & AWfo & AWre anomalies explicitly
awre = col_i16(AB, 15)
print("  AWre > 20 count:", int((awre > 20).sum()), "AWre < 0:", int((awre < 0).sum()), "percentiles:", np.percentile(awre, [0, 50, 95, 99, 100]).tolist())
awpo = col_u32(AB, 55)
print("  AWpo unique bits OR:", hex(int(np.bitwise_or.reduce(awpo))), "vals:", {hex(int(k)): int(c) for k, c in zip(*np.unique(awpo, return_counts=True))})

# ==========================================================
# 2. TABLE 8 — LANGUAGE (lstr + 17B suffix + 12B id + 1B sel)
# ==========================================================
print("\n==================== TABLE 8: LANGUAGE ====================")
l_cli, l_srv = cli["table_8.dat"], srv["table_8.dat"]
print("client==server:", l_cli == l_srv, "len:", len(l_cli), "hdr_n:", struct.unpack_from("<I", l_cli, 8)[0])
N8 = struct.unpack_from("<I", l_cli, 8)[0]
pos = 13
lang_names = []
lang_suf = np.empty((N8, 29), dtype=np.uint8)
lang_sels = []
for i in range(N8):
    lang_sels.append(l_cli[pos]); pos += 1
    slen = struct.unpack_from("<I", l_cli, pos)[0]; pos += 4
    lang_names.append(l_cli[pos:pos+slen].decode("utf-8")); pos += slen
    lang_suf[i] = np.frombuffer(l_cli, dtype=np.uint8, offset=pos, count=29); pos += 29
print(f"pos={pos}, expected={len(l_cli)-9}, exact_closure={pos == len(l_cli)-9}, sel_uniq={set(lang_sels)}")
ord8 = lang_suf[:, 17:21].copy().view("<u4").ravel()
duni8 = lang_suf[:, 21:25].copy().view("<u4").ravel()
rdui8 = lang_suf[:, 25:29].copy().view("<u4").ravel()
print(f"id: ord==0..N-1: {np.array_equal(ord8, np.arange(N8, dtype=np.uint32))}, duni==rdui: {int((duni8==rdui8).sum())}/{N8}")
print("sample languages:", list(zip(range(5), lang_names[:5], duni8[:5].tolist())))

for off, nm, kind in [
    (0, "int_+3a", "u8"), (1, "Linf", "i8"), (2, "Ldff", "i8"),
    (3, "Lfam", "i16"), (5, "Lgro", "i16"), (7, "Lsub", "i16"),
    (13, "int_+30", "i32"),
]:
    v = {"u8": col_u8, "i8": col_i8, "i16": col_i16, "i32": col_i32}[kind](lang_suf, off)
    u, cnt = np.unique(v, return_counts=True)
    if len(u) <= 25:
        print(f"  suf+{off:2d} {nm:8s} ({kind:3s}): min={int(v.min())}, max={int(v.max())}, hist={dict(zip(u.tolist(), cnt.tolist()))}")
    else:
        print(f"  suf+{off:2d} {nm:8s} ({kind:3s}): min={int(v.min())}, max={int(v.max())}, uniq={len(u)}, sample_min={u[:5].tolist()}, sample_max={u[-5:].tolist()}")
fk_report(col_i32(lang_suf, 9), 9, "Lnat@suf+9")
# Check int_+30 vs duni8
i30 = col_i32(lang_suf, 13)
print("  int_+30 == duni8:", int((i30.astype(np.int64) == duni8.astype(np.int64)).sum()), "diff rows:",
      [(i, lang_names[i], int(i30[i]), int(duni8[i])) for i in range(N8) if int(i30[i]) != int(duni8[i])][:10])

# ==========================================================
# 3. TABLE 18 — DERBY (4 lstr + 36/42B num + 12B id + 1B sel)
# ==========================================================
print("\n==================== TABLE 18: DERBY ====================")
def parse_derby(buf: bytes, is_server: bool):
    n = struct.unpack_from("<I", buf, 8)[0]
    pos = 13
    sels = []
    strs = [[], [], [], []]
    nlen = 42 if is_server else 36
    nums = np.empty((n, nlen + 12), dtype=np.uint8)
    for i in range(n):
        sels.append(buf[pos]); pos += 1
        for k in range(4):
            sl = struct.unpack_from("<I", buf, pos)[0]; pos += 4
            strs[k].append(buf[pos:pos+sl].decode("utf-8")); pos += sl
        nums[i] = np.frombuffer(buf, dtype=np.uint8, offset=pos, count=nlen + 12); pos += nlen + 12
    assert pos == len(buf) - 9, f"derby closure fail {pos} vs {len(buf)-9}"
    return sels, strs, nums

ds_c, dstr_c, dnum_c = parse_derby(cli["table_18.dat"], False)
ds_s, dstr_s, dnum_s = parse_derby(srv["table_18.dat"], True)
N18 = len(ds_c)
print(f"DERBY N={N18}, sel_c={set(ds_c)}, sel_s={set(ds_s)}")
print("strings client==server:", dstr_c == dstr_s)
print("non-empty counts [Dnam, Dsnm, Dasn, Danm]:", [sum(1 for x in s if x) for s in dstr_c])
print("num[0:28] client==server:", np.array_equal(dnum_c[:, :28], dnum_s[:, :28]))
print("num[28:36] client == num[34:42] server:", np.array_equal(dnum_c[:, 28:36], dnum_s[:, 34:42]))
print("id client==server:", np.array_equal(dnum_c[:, 36:48], dnum_s[:, 42:54]))
ord18 = dnum_s[:, 42:46].copy().view("<u4").ravel()
duni18 = dnum_s[:, 46:50].copy().view("<u4").ravel()
rdui18 = dnum_s[:, 50:54].copy().view("<u4").ravel()
print(f"id: ord==0..N-1: {np.array_equal(ord18, np.arange(N18, dtype=np.uint32))}, duni==rdui: {int((duni18==rdui18).sum())}/{N18}")

check_dates(col_u32(dnum_s, 0), "Dfmd@0")
fk_report(col_i32(dnum_s, 4), 24, "Dtm1@4->t24")
fk_report(col_i32(dnum_s, 8), 24, "Dtm2@8->t24")
fk_report(col_i32(dnum_s, 4), 3, "Dtm1@4->t3!")
fk_report(col_i32(dnum_s, 12), 25, "Dfmc@12")
fk_report(col_i32(dnum_s, 16), 21, "Dfms@16")
for off, nm, kind in [
    (20, "Dfma", "i32"), (24, "rpdr", "i32"),
    (28, "D1tw(s)", "i16"), (30, "D1td(s)", "i16"), (32, "D1tl(s)", "i16"),
    (34, "Dfg1", "i8"), (35, "Dfg2", "i8"),
    (36, "int36", "u8"), (37, "int37", "u8"), (38, "int38", "u8"), (39, "int39", "u8"),
    (40, "Dwdr", "u8"), (41, "Dntr", "u8"),
]:
    v = {"u8": col_u8, "i8": col_i8, "i16": col_i16, "i32": col_i32}[kind](dnum_s, off)
    neg = int((v < 0).sum())
    live = v[v >= 0]
    u, cnt = np.unique(v, return_counts=True)
    if len(u) <= 12:
        print(f"  s@{off:2d} {nm:8s} ({kind:3s}): hist={dict(zip(u.tolist(), cnt.tolist()))}")
    else:
        print(f"  s@{off:2d} {nm:8s} ({kind:3s}): neg={neg} (m1={int((v==-1).sum())}), live={len(live)}, live_min={int(live.min()) if len(live) else None}, live_max={int(live.max()) if len(live) else None}, uniq={len(u)}")

# ==========================================================
# 4. TABLE 27 — WEATHER (lstr + 3B + 4*23B + 12B id + 1B sel)
# ==========================================================
print("\n==================== TABLE 27: WEATHER ====================")
w_cli, w_srv = cli["table_27.dat"], srv["table_27.dat"]
print("client==server:", w_cli == w_srv, "len:", len(w_cli), "hdr_n:", struct.unpack_from("<I", w_cli, 8)[0])
N27 = struct.unpack_from("<I", w_cli, 8)[0]
pos = 13
w_sels = []
w_names = []
w_mid = np.empty((N27, 95 + 12), dtype=np.uint8)
for i in range(N27):
    w_sels.append(w_cli[pos]); pos += 1
    sl = struct.unpack_from("<I", w_cli, pos)[0]; pos += 4
    w_names.append(w_cli[pos:pos+sl].decode("utf-8")); pos += sl
    w_mid[i] = np.frombuffer(w_cli, dtype=np.uint8, offset=pos, count=107); pos += 107
print(f"pos={pos}, expected={len(w_cli)-9}, exact_closure={pos == len(w_cli)-9}, sel_uniq={set(w_sels)}")
ord27 = w_mid[:, 95:99].copy().view("<u4").ravel()
duni27 = w_mid[:, 99:103].copy().view("<u4").ravel()
rdui27 = w_mid[:, 103:107].copy().view("<u4").ravel()
print(f"id: ord==0..N-1: {np.array_equal(ord27, np.arange(N27, dtype=np.uint32))}, duni==rdui: {int((duni27==rdui27).sum())}/{N27}")
print("mid[0:3] unique:", np.unique(w_mid[:, :3]).tolist())
for b in range(4):
    base = 3 + 23 * b
    sd = col_i16(w_mid, base)
    w_arr = w_mid[:, base+2:base+7].view(np.int8)
    p_arr = w_mid[:, base+7:base+12].view(np.int8)
    te = w_mid[:, base+12].view(np.int8)
    tv = w_mid[:, base+13].view(np.int8)
    t_arr = w_mid[:, base+14:base+22].view(np.int8)
    dn = w_mid[:, base+22].view(np.int8)
    dn_live = dn[dn != 100]
    wsum = w_arr.sum(axis=1)
    psum = p_arr.sum(axis=1)
    tsum = t_arr.sum(axis=1)
    print(f"  season {b} (base={base:2d}): sd=[{int(sd.min())}..{int(sd.max())}] (>365:{int((sd>365).sum())}, <0:{int((sd<0).sum())}), "
          f"win=[{int(w_arr.min())}..{int(w_arr.max())}] sum!=100:{int((wsum!=100).sum())}, "
          f"pre=[{int(p_arr.min())}..{int(p_arr.max())}] sum!=100:{int((psum!=100).sum())}, "
          f"te=[{int(te.min())}..{int(te.max())}], tv=[{int(tv.min())}..{int(tv.max())}], "
          f"t0..7=[{int(t_arr.min())}..{int(t_arr.max())}] sum!=100:{int((tsum!=100).sum())}, "
          f"dn: 100(null)={int((dn==100).sum())}, live={len(dn_live)} [{int(dn_live.min()) if len(dn_live) else None}..{int(dn_live.max()) if len(dn_live) else None}]")
# Check all-4-sd-equal rows (triggering 55/145/230/300 default in read)
sds = np.column_stack([col_i16(w_mid, 3 + 23*b) for b in range(4)])
all_eq = (sds[:,0]==sds[:,1]) & (sds[:,1]==sds[:,2]) & (sds[:,2]==sds[:,3])
print("  all 4 sd equal count:", int(all_eq.sum()), "sd>365 rows:", [(i, w_names[i], sds[i].tolist()) for i in range(N27) if (sds[i]>365).any()][:5])

# ==========================================================
# 5. TABLE 7 — MEDIA_SOURCE (exact MEDIA_SOURCE::read grammar!)
# ==========================================================
print("\n==================== TABLE 7: MEDIA_SOURCE ====================")
def parse_media(buf: bytes, is_server: bool):
    n = struct.unpack_from("<I", buf, 8)[0]
    pos = 13
    rows = []
    for i in range(n):
        row_start = pos
        sel = buf[pos]; pos += 1
        def rd_lstr():
            nonlocal pos
            l = struct.unpack_from("<I", buf, pos)[0]; pos += 4
            s = buf[pos:pos+l].decode("utf-8"); pos += l
            return s
        def rd_u8():
            nonlocal pos
            v = buf[pos]; pos += 1; return v
        def rd_i32():
            nonlocal pos
            v = struct.unpack_from("<i", buf, pos)[0]; pos += 4; return v
        def rd_u32():
            nonlocal pos
            v = struct.unpack_from("<I", buf, pos)[0]; pos += 4; return v
        def rd_i32_vec():
            cnt = rd_u32()
            return [rd_i32() for _ in range(cnt)]

        Mnam = rd_lstr()
        int_d1 = rd_u8()
        cnt_typ = rd_u32()
        Mtyp_raw = [rd_u8() for _ in range(cnt_typ)]
        Murl = rd_lstr()
        Mhtg = rd_lstr()
        Misf = rd_u8()
        Msty = rd_u8()
        Mcmi = rd_i32_vec()
        Mcyi = rd_i32()
        Mrgi = rd_i32_vec()
        Mnti = rd_i32_vec()
        Mcti = rd_i32()
        cnt_cli = rd_u32()
        Mcli = []
        for _ in range(cnt_cli):
            c_u1 = rd_u32(); c_u2 = rd_u32()
            c_url = rd_lstr()
            Mcli.append((c_u1, c_u2, c_url))
        if is_server:
            srv_start = pos
            Mper = rd_u8()
            Mscp = rd_u8()
            Mdlp = rd_u32()
            cnt_jor = rd_u8()
            Mjor = [rd_i32() for _ in range(cnt_jor)]
            srv_bytes = buf[srv_start:pos]
        else:
            Mper = Mscp = Mdlp = None
            Mjor = None
            srv_bytes = b""
        Mlnm = rd_i32_vec()
        Mapc = rd_u8()
        pre5 = buf[pos-5:pos]
        ord_i = rd_u32()
        duni_i = rd_u32()
        rdui_i = rd_u32()
        rows.append({
            "sel": sel, "Mnam": Mnam, "int_d1": int_d1, "Mtyp_raw": Mtyp_raw,
            "Murl": Murl, "Mhtg": Mhtg, "Misf": Misf, "Msty": Msty,
            "Mcmi": Mcmi, "Mcyi": Mcyi, "Mrgi": Mrgi, "Mnti": Mnti, "Mcti": Mcti,
            "Mcli": Mcli, "Mper": Mper, "Mscp": Mscp, "Mdlp": Mdlp, "Mjor": Mjor,
            "Mlnm": Mlnm, "Mapc": Mapc, "pre5": pre5.hex(),
            "ord": ord_i, "duni": duni_i, "rdui": rdui_i,
            "row_len": pos - row_start, "srv_len": len(srv_bytes),
        })
    assert pos == len(buf) - 9, f"MEDIA closure failed: pos={pos}, expected={len(buf)-9}"
    return rows

m_cli = parse_media(cli["table_7.dat"], False)
m_srv = parse_media(srv["table_7.dat"], True)
print(f"MEDIA 100% CLOSED BOTH ARCHIVES! N_cli={len(m_cli)}, N_srv={len(m_srv)}")
print("sel_c:", set(r["sel"] for r in m_cli), "sel_s:", set(r["sel"] for r in m_srv))
# Check client==server on all shared fields!
shared_keys = ["sel","Mnam","int_d1","Mtyp_raw","Murl","Mhtg","Misf","Msty","Mcmi","Mcyi","Mrgi","Mnti","Mcti","Mcli","Mlnm","Mapc","ord","duni","rdui"]
eq_all = all(all(rc[k] == rs[k] for k in shared_keys) for rc, rs in zip(m_cli, m_srv))
print("ALL shared fields client==server:", eq_all)
print("srv_len hist:", Counter(r["srv_len"] for r in m_srv))
print("row_len delta (srv-cli) hist:", Counter(rs["row_len"] - rc["row_len"] for rc, rs in zip(m_cli, m_srv)))
print("id ord==0..N-1:", [r["ord"] for r in m_srv] == list(range(len(m_srv))),
      "duni==rdui:", sum(1 for r in m_srv if r["duni"] == r["rdui"]), "/", len(m_srv))

print("int_d1 hist:", Counter(r["int_d1"] for r in m_srv))
print("Mtyp len hist:", Counter(len(r["Mtyp_raw"]) for r in m_srv),
      "vals hist:", Counter(x for r in m_srv for x in r["Mtyp_raw"]))
print("Murl non-empty:", sum(1 for r in m_srv if r["Murl"]), "Mhtg non-empty:", sum(1 for r in m_srv if r["Mhtg"]))
print("Misf hist:", Counter(r["Misf"] for r in m_srv))
print("Msty hist:", Counter(r["Msty"] for r in m_srv))
print("Mper hist:", Counter(r["Mper"] for r in m_srv))
print("Mscp hist:", Counter(r["Mscp"] for r in m_srv))
print("Mapc hist:", Counter(r["Mapc"] for r in m_srv))
print("Mjor len hist:", Counter(len(r["Mjor"]) for r in m_srv))
check_dates(np.array([r["Mdlp"] for r in m_srv], dtype="<u4"), "Mdlp")

fk_report(np.array([x for r in m_srv for x in r["Mcmi"]], dtype=np.int32), 25, "Mcmi_flat")
fk_report(np.array([r["Mcyi"] for r in m_srv], dtype=np.int32), 2, "Mcyi")
fk_report(np.array([x for r in m_srv for x in r["Mrgi"]], dtype=np.int32), 47, "Mrgi_flat")
fk_report(np.array([x for r in m_srv for x in r["Mnti"]], dtype=np.int32), 9, "Mnti_flat")
fk_report(np.array([r["Mcti"] for r in m_srv], dtype=np.int32), 5, "Mcti")
fk_report(np.array([x for r in m_srv for x in r["Mlnm"]], dtype=np.int32), 7, "Mlnm_flat")

# Mcli: check u1, u2 vs CLUB UIDs (table 3)!
mcli_flat = [item for r in m_srv for item in r["Mcli"]]
print(f"Mcli total items={len(mcli_flat)} across {sum(1 for r in m_srv if r['Mcli'])} rows")
if mcli_flat:
    u1s = [x[0] for x in mcli_flat]
    u2s = [x[1] for x in mcli_flat]
    curls = [x[2] for x in mcli_flat]
    club_uids = ref_uids[3]
    in_uid = sum(1 for u in u1s if u in club_uids)
    in_ord = sum(1 for u in u1s if u < ref_n[3])
    print(f"  Mcli u1==u2: {sum(1 for a,b in zip(u1s,u2s) if a==b)}/{len(mcli_flat)}, u2==0: {sum(1 for b in u2s if b==0)}, u1 in club UIDs: {in_uid}/{len(mcli_flat)}, u1 < club N: {in_ord}/{len(mcli_flat)}, non-empty curl: {sum(1 for c in curls if c)}")
    print("  Mcli sample:", mcli_flat[:5])

# Explain t74's 16 distinct 5B prefixes before identity!
pre5_c = Counter(r["pre5"] for r in m_cli)
print(f"pre5 distinct count: {len(pre5_c)} (cnt_lnm==0 rows={sum(1 for r in m_cli if len(r['Mlnm'])==0)}, cnt_lnm>0 rows={sum(1 for r in m_cli if len(r['Mlnm'])>0)})")
print("  pre5 top 10:", pre5_c.most_common(10))
print("  Mlnm len hist:", Counter(len(r["Mlnm"]) for r in m_cli))
