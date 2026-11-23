import sys, struct
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
    if any(ord(c) < 32 or ord(c) == 0x7F for c in t): return None
    return (4+ln, t)

def anchors(raw):
    n = struct.unpack_from("<I", raw, 8)[0]
    end = len(raw); out = []; pos = 12
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        out.append(pos)
        p = pos + 4
        while True:
            g = read_str(raw, p, end)
            if g is None: break
            p += g[0]
        found = None
        for q in range(p, min(p + 40, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and read_str(raw, q + 4, end) is not None:
                found = q; break
        if found is None: return out
        pos = found
    return out

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["12_18.dat"])
a = anchors(raw)
print("anchors", len(a))
for i in range(4):
    s = a[i]; stop = a[i+1] if i+1 < len(a) else len(raw)
    print(f"row{i} off={s} dbid={struct.unpack_from('<I',raw,s)[0]} bodylen={stop-s-4}")
    print("   body:", raw[s+4:stop].hex(" "))
