import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["32_18.dat"])
c = struct.unpack_from("<I", raw, 8)[0]
print("count", c, "len", len(raw))
for off in range(7990, 8250, 16):
    print(f"{off:06x}", raw[off:off+16].hex(" "), "".join(chr(ch) if 32<=ch<127 else "." for ch in raw[off:off+16]))
