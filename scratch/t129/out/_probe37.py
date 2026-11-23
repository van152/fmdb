import sys, struct, re, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

for p in [Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), Path(r"scratch/data/lang_update_db.dat")]:
    data, lay = m._read_archive(p)
    names = [e["path"].split("/")[1][:-4] for e in lay["entries"]]
    langs = sorted({int(re.sub(r"person_names$", "", n).split("_")[0]) for n in names})
    print(p.name, "langs", langs, len(langs))
    # entry order check
    print("  first 17:", names[:17])
    # sizes
    tot_packed = sum(e["packed_size"] for e in lay["entries"])
    tot_size = sum(e["size"] for e in lay["entries"])
    print("  packed", tot_packed, "unpacked", tot_size, "file", len(data), "toc", lay["toc_offset"], "base", lay["data_base"], "dirsize", lay["directory_size"])
    # person_names sizes
    pn = [(e["path"], e["size"], e["packed_size"]) for e in lay["entries"] if "person" in e["path"]]
    print("  person_names", pn[:2], "n", len(pn), "sizes", set(x[1] for x in pn))
