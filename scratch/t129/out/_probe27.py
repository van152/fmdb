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

def anchor_rows(raw):
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
        for q in range(p, min(p + 96, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and read_str(raw, q + 4, end) is not None:
                found = q; break
        if found is None: return out, False
        pos = found
    return out, pos == end

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["12_18.dat"])
a, closed = anchor_rows(raw)
print("rows", len(a), "closed", closed)
lines = []
for i in range(6):
    s = a[i]; stop = a[i+1] if i+1 < len(a) else len(raw)
    body = raw[s+4:stop]
    p = 0; strs = []
    while True:
        g = read_str(body, p, len(body))
        if g is None: break
        strs.append(g[1]); p += g[0]
    lines.append(f"row{i} dbid={struct.unpack_from('<I',raw,s)[0]} len={len(body)} strs={strs} tail={body[p:].hex(' ')}")
Path(r"scratch/t129/out/_t18.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
