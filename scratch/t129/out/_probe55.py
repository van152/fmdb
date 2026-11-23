import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"scratch/data/lang_update_db.dat"))
base = lay["data_base"]
e = [x for x in lay["entries"] if x["path"] == "lang_update_db/24person_names.dat"][0]
raw = m._decompress_entry(data, base, e)
print("len", len(raw), "count", struct.unpack_from("<I", raw, 8)[0])
for i in range(8, len(raw)):
    print(f"{i:3d} {raw[i]:02x} {chr(raw[i]) if 32<=raw[i]<127 else '.'}")
