import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def rd(raw, p, end):
    if p + 4 > end: return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xFFFFFFFF: return (4, None)
    if ln > 65536 or p + 4 + ln > end: return None
    try: t = raw[p+4:p+4+ln].decode("utf-8")
    except UnicodeDecodeError: return None
    for ch in t:
        o = ord(ch)
        if (o < 32 and o != 9) or o == 0x7F: return None
    return (4+ln, t)

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
    for nm in ["8_19.dat", "8_35.dat", "1000002_19.dat", "1000002_35.dat", "8_47.dat", "8_5.dat"]:
        if nm not in ent: continue
        raw = m._decompress_entry(data, base, ent[nm])
        n = struct.unpack_from("<I", raw, 8)[0]
        print(label, nm, "count", n, "len", len(raw), "head", raw[12:12+72].hex(" "))
        # dump first row strings+vars
        p = 12
        for i in range(min(2, n)):
            dbid = struct.unpack_from("<I", raw, p)[0]; p += 4
            toks = []
            # generic: consume strings/flags until variant count
            print("   dbid", dbid, "next40", raw[p:p+40].hex(" "))
            break
