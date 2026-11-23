import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
pns = [(e["path"], e["size"], e["packed_size"]) for e in lay["entries"] if "person" in e["path"]]
print("person members:", pns)
for nm, sz, pk in pns:
    if sz > 1_000_000:
        e = [x for x in lay["entries"] if x["path"] == nm][0]
        raw = m._decompress_entry(data, base, e)
        n = struct.unpack_from("<I", raw, 8)[0]
        print(nm, "size", len(raw), "count", n, "hdr", raw[:16].hex(" "))
        print("  body0", raw[12:12+80].hex(" "))
        print("  text", raw[12:12+120])
        break
