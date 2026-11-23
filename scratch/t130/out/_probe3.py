import sys, pathlib, struct
from collections import Counter
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24-db\scripts")
import zstandard as zstd
import t112_fm24_reader as R

# skippable frame index check
for name in ["pl_hist_dt", "non_pl_hist_dt"]:
    d = (pathlib.Path("scratch/data") / f"{name}.dat").read_bytes()
    body = d[8:]
    dctx = zstd.ZstdDecompressor()
    data = body; consumed = 0; dsum = 0; n = 0
    while data[:4] == bytes.fromhex("28b52ffd"):
        obj = dctx.decompressobj(); chunk = obj.decompress(data)
        c = len(data) - len(obj.unused_data)
        if not obj.eof or c <= 0: break
        consumed += c; dsum += len(chunk); n += 1; data = obj.unused_data
    left = data
    magic, ssize = struct.unpack_from("<II", left, 0)
    pl = left[8:]
    print("==", name, "frames", n, "consumed", consumed, "dsum", dsum, "skipmagic", hex(magic), "ssize", ssize, "len(pl)", len(pl))
    ent = [struct.unpack_from("<III", pl, 12 * i) for i in range(len(pl) // 12)]
    print("   entries(12B)", len(ent), "tail bytes", len(pl) % 12, "sum clen", sum(e[0] for e in ent), "sum dlen", sum(e[1] for e in ent))
    print("   first 4", ent[:4], "last 2", ent[-2:])
    print("   dlen counter", Counter(e[1] for e in ent).most_common(4))

# lang member names
for nm, path in [("lang_update_db", "scratch/data/lang_update_db.dat"), ("lang_db_2400", r"D:\tmp2b\fm24\input\lang_db_2400.dat")]:
    lay = R.archive_layout(pathlib.Path(path).read_bytes())
    names = [pathlib.PurePosixPath(e["path"]).name for e in lay["entries"]]
    ids = sorted({int(x.split("_")[1][:-4]) for x in names if x.endswith(".dat") and x.split("_")[1][:-4].isdigit()})
    print(nm, "members", len(names), "table ids", ids)
