import sys, struct, time, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

for p in [Path(r"scratch/data/lang_update_db.dat"), Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat")]:
    data, lay = m._read_archive(p)
    base = lay["data_base"]
    t0 = time.time()
    ok = fail = 0
    sizes = collections.Counter()
    tot = 0
    fails = []
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm:
            continue
        tid = int(nm.split("_")[1])
        raw = m._decompress_entry(data, base, e)
        tot += len(raw)
        rows = L.grammar_walk(raw, tid)
        if rows is None:
            fail += 1; fails.append(nm)
        else:
            ok += 1
    print(p.name, "ok", ok, "fail", fail, "bytes", tot, "%.1fs" % (time.time() - t0))
    print("  fails", fails[:10], len(fails))
