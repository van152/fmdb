import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def anchors_greedy(raw):
    n = struct.unpack_from("<I", raw, 8)[0]
    end = len(raw); out = []; pos = 12
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        out.append(pos)
        p = pos + 4
        while True:
            if p + 4 > end: break
            ln = struct.unpack_from("<I", raw, p)[0]
            if ln == 0xffffffff or ln == 0 or ln > 4096 or p+4+ln > end: break
            try: t = raw[p+4:p+4+ln].decode("utf-8")
            except UnicodeDecodeError: break
            if any(ord(c) < 9 for c in t): break
            p += 4 + ln
        found = None
        for q in range(p, min(p + 64, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid:
                ln = struct.unpack_from("<I", raw, q+4)[0] if q+8 <= end else 0
                if 0 < ln < 4096 and q+8+ln <= end:
                    try:
                        t = raw[q+8:q+8+ln].decode("utf-8")
                        if not any(ord(c) < 9 for c in t):
                            found = q; break
                    except UnicodeDecodeError: pass
        if found is None: return out
        pos = found
    return out

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["12_18.dat"])
a = anchors_greedy(raw)
for i in range(4):
    s = a[i]; stop = a[i+1] if i+1 < len(a) else len(raw)
    print(f"row{i} dbid={struct.unpack_from('<I',raw,s)[0]} len={stop-s-4}")
    print("  ", raw[s+4:stop].hex(" "))
