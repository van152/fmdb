import sys, struct, collections, json
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

G = {
 0:(["str","s","str","s","CNT"],()), 2:(["str","s","CNT"],()),
 3:(["str","s","str","s","str","str","str","s","str","CNT"],("s","s")),
 5:(["str","s","str","str","str","s","str","s","CNT"],()),
 6:(["str","s","str","s","CNT"],()), 7:(["str","s"],()),
 9:(["str","s","str","s","str","str","CNT"],()),
 18:(["str","str","str","str","s","s","u16","CNT"],()),
 19:(["str","CNT"],()), 21:(["str","str","s","s","CNT"],()),
 23:(["str","s","str","s","str","s","CNT"],()),
 25:(["str","s","str","s","str","CNT"],()), 35:(["s","s","CNT"],()),
 47:(["str","s","str","s","CNT"],()), 56:(["str","s","str","s","s"],()),
}
for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    per_table = collections.defaultdict(lambda: {"rows": 0, "strs": 0, "files": 0, "variants": 0})
    cjk = 0; latin = 0; nonascii = 0; utf16hits = 0
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        raw = m._decompress_entry(data, base, e)
        if "person" in nm:
            continue
        tid = int(nm.split("_")[1])
        n = struct.unpack_from("<I", raw, 8)[0]
        d = per_table[tid]; d["files"] += 1; d["rows"] += n
        # count strings + encoding
        pos = 12; end = len(raw); slots, tail = G[tid]
        for i in range(n):
            p = pos + 4; cnt = None
            for s in slots:
                if s == "CNT": cnt = raw[p]; p += 1
                elif s == "str":
                    g = read_str(raw, p, end); p += g[0]
                    if g[1]:
                        d["strs"] += 1
                        if any(0x4e00 <= ord(c) <= 0x9fff for c in g[1]): cjk += 1
                        elif any(ord(c) > 127 for c in g[1]): nonascii += 1
                        else: latin += 1
                elif s == "u16": p += 2
                else: p += 1
            for k in range(cnt or 0):
                g = read_str(raw, p, end); p += g[0] + 3; d["variants"] += 1
            for t in tail: p += 1
            pos = p
    print(label, "per_table", {k: dict(v) for k, v in sorted(per_table.items())})
    print(label, "charsets: ascii/latin", latin, "other-nonascii", nonascii, "CJK", cjk)
