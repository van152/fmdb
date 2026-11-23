import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
e = [x for x in lay["entries"] if x["path"] == "lang_db/30person_names.dat"][0]
raw = m._decompress_entry(data, base, e)
print("len", len(raw), "count", struct.unpack_from("<I", raw, 8)[0])
out = []
for i in range(8, len(raw)):
    out.append("%d:%02x(%s)" % (i, raw[i], chr(raw[i]) if 32 <= raw[i] < 127 else "."))
print(" ".join(out))
