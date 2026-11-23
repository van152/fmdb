import sys, struct, time
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

for p in [Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), Path(r"scratch/data/lang_update_db.dat")]:
    data, lay = m._read_archive(p)
    base = lay["data_base"]
    print("==", p.name, "base", base, "entries", len(lay["entries"]))
    for e in lay["entries"][:3]:
        raw = m._decompress_entry(data, base, e)
        print(" ", e["path"], "size", e["size"], "hdr", raw[:14].hex(" "), "ver", struct.unpack_from("<H", raw, 6)[0],
              "count", struct.unpack_from("<I", raw, 8)[0])
    # person_names
    pn = [e for e in lay["entries"] if "person" in e["path"]][0]
    raw = m._decompress_entry(data, base, pn)
    print("  person", pn["path"], pn["size"], raw.hex(" ")[:40])

# base big member timing + grammar walk
data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm, tid in [("1000002_3.dat", 3), ("1000002_21.dat", 21), ("8_9.dat", 9), ("8_25.dat", 25), ("1000002_2.dat", 2), ("1000002_0.dat", 0), ("8_7.dat", 7), ("8_18.dat", 18)]:
    t0 = time.time()
    raw = m._decompress_entry(data, base, ent[nm])
    n = struct.unpack_from("<I", raw, 8)[0]
    rows = L.grammar_walk(raw, tid)
    print(nm, "size", len(raw), "count", n, "walk", None if rows is None else len(rows), "%.2fs" % (time.time() - t0))
