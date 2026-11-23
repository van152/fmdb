import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"scratch/data/lang_update_db.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm in ["18_18.dat", "24_18.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    print("==", nm, "len", len(raw), "count", struct.unpack_from("<I", raw, 8)[0])
    for off in range(0, len(raw), 16):
        print(f"{off:04x}", raw[off:off+16].hex(" "), "".join(chr(c) if 32<=c<127 else "." for c in raw[off:off+16]))
