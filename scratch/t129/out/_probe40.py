import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
for nm in ["lang_db/30person_names.dat", "lang_db/1000004person_names.dat", "lang_db/21person_names.dat", "lang_db/19person_names.dat", "lang_db/24person_names.dat", "lang_db/7person_names.dat"]:
    e = [x for x in lay["entries"] if x["path"] == nm][0]
    raw = m._decompress_entry(data, base, e)
    print("==", nm, "len", len(raw), "hdr", raw[:12].hex(" "), "count", struct.unpack_from("<I", raw, 8)[0])
    for off in range(0, min(len(raw), 240), 16):
        chunk = raw[off:off+16]
        print(f"  {off:04x}", chunk.hex(" "), "".join(chr(c) if 32<=c<127 else "." for c in chunk))
