import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm in ["8_56.dat", "8_18.dat", "1000002_18.dat", "8_19.dat", "8_35.dat", "8_47.dat"]:
    e = ent[nm]
    raw = m._decompress_entry(data, base, e)
    n = struct.unpack_from("<I", raw, 8)[0]
    print(nm, "len", len(raw), "count", n, "hdr", raw[:40].hex(" "), "|", raw[12:90])
