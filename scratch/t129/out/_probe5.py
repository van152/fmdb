import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
fails = collections.Counter()
for e in lay["entries"]:
    nm = e["path"].split("/")[1][:-4]
    if "person" in nm:
        continue
    tid = int(nm.split("_")[1])
    raw = m._decompress_entry(data, base, e)
    if L.grammar_walk(raw, tid) is None:
        fails[tid] += 1
print("base fails by table:", dict(fails), "total", sum(fails.values()))

# t18 / t56 grammar inference on base via joint solver
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm in ["8_18.dat", "8_56.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    n = struct.unpack_from("<I", raw, 8)[0]
    # anchors: rows are increasing dbid then string; use LIS
    anchors = L._anchor_scan(raw, None)
    print(nm, "count", n, "anchors", None if anchors is None else len(anchors))
    if anchors:
        bodies = [b for _, b in L._row_slices(raw, anchors)]
        lay_out = L.infer_layout(bodies, max_rows=200)
        print("  inferred", lay_out)
