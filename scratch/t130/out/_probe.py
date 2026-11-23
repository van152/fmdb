import sys, pathlib, struct, time
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24-db\scripts")
import zstandard as zstd
import t112_fm24_reader as R

for name in ["server_db", "client_db", "lang_update_db"]:
    t0 = time.time()
    p = pathlib.Path("scratch/data") / f"{name}.dat"
    d = p.read_bytes()
    lay = R.archive_layout(d)
    ents = lay["entries"]
    print(name, "members", len(ents), "data_base", lay["data_base"], "toc", lay["toc_offset"], "%.2fs" % (time.time() - t0))
    tids = []
    for e in ents:
        nm = pathlib.PurePosixPath(e["path"]).name
        tids.append(nm)
    print("  first 8:", tids[:8])
    print("  sum declared size", sum(e["size"] for e in ents), "sum packed", sum(e["packed_size"] for e in ents))
    table_ids = sorted(int(n[len("table_"):-4]) for n in tids if n.startswith("table_") and n.endswith(".dat") and n[6:-4].isdigit())
    print("  table ids:", table_ids)

p = pathlib.Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat")
d = p.read_bytes()
lay = R.archive_layout(d)
ents = lay["entries"]
print("lang_db_2400 members", len(ents), "data_base", lay["data_base"], "toc", lay["toc_offset"])
print("  sum declared", sum(e["size"] for e in ents))
print("  sample paths", [e["path"] for e in ents[:10]])
