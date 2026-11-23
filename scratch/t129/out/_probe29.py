import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["12_18.dat"])
for off in range(0x30, 0xc0):
    pass
seg = raw[0x30:0xc0]
for i, b in enumerate(seg):
    print(f"{0x30+i:04x} {b:02x} {'%02x' % b}")
