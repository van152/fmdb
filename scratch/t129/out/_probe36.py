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

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm in ["8_19.dat", "8_35.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    n = struct.unpack_from("<I", raw, 8)[0]
    print("==", nm, "count", n, "len", len(raw))
    print("  raw:", raw[12:12+80].hex(" "))
    pos = 12
    for i in range(min(3, n)):
        print("  row%d raw:" % i, raw[pos:pos+40].hex(" "))
        # skip u32 dbid then try str
        g = read_str(raw, pos+4, len(raw))
        print("     dbid", struct.unpack_from("<I", raw, pos)[0], "str", None if g is None else g[1])
        pos += 4 + (g[0] if g else 0) + 1
# language ids present
langs = sorted({e["path"].split("/")[1].split("_")[0].replace("person_names","") for e in lay["entries"]}, key=int)
print("langs", langs)
print("n langs", len(langs))
