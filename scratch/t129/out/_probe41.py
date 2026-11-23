import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def read_str(raw, p, end):
    if p + 4 > end: return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xFFFFFFFF: return (4, None)
    if ln > 8192 or p + 4 + ln > end: return None
    try: t = raw[p+4:p+4+ln].decode("utf-8")
    except UnicodeDecodeError: return None
    for ch in t:
        o = ord(ch)
        if (o < 32 and o != 9) or o == 0x7F: return None
    return (4+ln, t)

def walk_pn(raw):
    pos = 12; end = len(raw); n = 0; ids = collections.Counter()
    while pos < end:
        if pos + 8 > end: return None, ("hdr", pos, n)
        a = read_str(raw, pos, end)
        if a is None: return None, ("str1", pos, n)
        p = pos + a[0]
        if p + 4 > end: return None, ("pad1", pos, n)
        pad1 = struct.unpack_from("<I", raw, p)[0]; p += 4
        b = read_str(raw, p, end)
        if b is None: return None, ("str2", pos, n)
        p += b[0]
        if p + 4 > end: return None, ("pad2", pos, n)
        pad2 = struct.unpack_from("<I", raw, p)[0]; p += 4
        if p + 4 > end: return None, ("alias", pos, n)
        alias = struct.unpack_from("<I", raw, p)[0]; p += 4
        if alias != 0xFFFFFFFF:
            g = read_str(raw, p, end)
            if g is None: return None, ("aliasstr", pos, n)
            p += g[0]
        if p + 3 > end: return None, ("tail", pos, n)
        ids[(struct.unpack_from("<H", raw, p)[0], raw[p+2])] += 1
        p += 3
        n += 1
        pos = p
    return (n, ids), None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"], err))
        else: ok += 1; tot += r[0]
    print(label, "person_names ok", ok, "bad", bad, "records", tot)
