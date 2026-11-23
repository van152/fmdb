import sys, pathlib, struct
from collections import Counter
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
import zstandard as zstd

Z = bytes.fromhex("28b52ffd")

def frames(body):
    dctx = zstd.ZstdDecompressor()
    data = body; out = []; consumed = 0
    while data[:4] == Z:
        obj = dctx.decompressobj()
        chunk = obj.decompress(data)
        c = len(data) - len(obj.unused_data)
        if not obj.eof or c <= 0:
            break
        out.append(len(chunk)); consumed += c; data = obj.unused_data
    return out, consumed, data

for name in ["pl_hist_dt", "non_pl_hist_dt"]:
    d = (pathlib.Path("scratch/data") / f"{name}.dat").read_bytes()
    body = d[8:]
    lens, consumed, left = frames(body)
    print("==", name, "frames", len(lens), "consumed", consumed, "leftover", len(left))
    print("   head", left[:32].hex())
    u = [struct.unpack_from("<I", left, 4 * i)[0] for i in range(6)]
    print("   u32s", u, hex(u[0]), hex(u[1]))
    # hypothesis: [u32 magic][u32 n][n*(u32 clen,u32 dlen)]
    n = struct.unpack_from("<I", left, 4)[0]
    print("   n", n, "expected bytes", 8 + 8 * n, "actual", len(left))
    if 8 + 8 * n == len(left):
        ents = [struct.unpack_from("<II", left, 8 + 8 * i) for i in range(min(n, 5))]
        print("   sample entries", ents)
        tot_c = sum(struct.unpack_from("<I", left, 8 + 8 * i)[0] for i in range(n))
        tot_d = sum(struct.unpack_from("<I", left, 8 + 8 * i + 4)[0] for i in range(n))
        print("   sum clen", tot_c, "sum dlen", tot_d)
    else:
        print("   not a flat table; tail", left[-32:].hex())

for name in ["pl_hist_id", "non_pl_hist_id"]:
    d = (pathlib.Path("scratch/data") / f"{name}.dat").read_bytes()
    body = d[8:]
    n = len(body) // 4
    v = struct.unpack_from("<%dI" % min(n, 8), body, 0)
    print("==", name, "body", len(body), "u32 count", n, "rem", len(body) % 4, "first", v)
    asc = all(struct.unpack_from("<I", body, 4 * i)[0] <= struct.unpack_from("<I", body, 4 * (i + 1))[0] for i in range(min(n, 200000) - 1))
    print("   first 200k ascending:", asc)
    print("   last u32", struct.unpack_from("<I", body, len(body) - 4)[0])

for name in ["people_db", "basic_people_db", "pl_hist_index", "non_pl_hist_index"]:
    d = (pathlib.Path("scratch/data") / f"{name}.dat").read_bytes()
    lens, consumed, left = frames(d[8:])
    print("==", name, "frames", len(lens), "decomp", sum(lens), "leftover", len(left), "tail", d[-8:].hex())
