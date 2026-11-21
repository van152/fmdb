"""t76b scratch: language prefix + media body alignment probes."""
import runpy, sys, struct
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


print("=== language(8): 126 rows, name + 17B prefix + 13B trailer ===")
raw = load(8)
pos = 14
L = []
for j in range(126):
    k = u32(raw, pos)
    name = raw[pos + 4:pos + 4 + k]
    pre = raw[pos + 4 + k:pos + 4 + k + 17]
    tr = raw[pos + 4 + k + 17:pos + 4 + k + 30]
    L.append({"j": j, "start": pos, "k": k, "name": name, "pre": pre, "tr": tr})
    pos += 4 + k + 30
print("end", pos, "payload", len(raw), "footer", raw[pos:].hex())
for o in range(0, 17):
    vals = [r["pre"][o] for r in L]
    print(f"  pre{o:2d}: {len(set(vals)):3d} distinct, min={min(vals)} max={max(vals)}, first8={vals[:8]}")
print("  prefix+13 u32 values:", [u32(r["pre"], 13) for r in L][:20], "...")
tail = [u32(r["pre"], 13) for r in L]
print("  prefix+13: d=%d, rows where ==j+1: %d, values>=1000: %d" %
      (len(set(tail)), sum(1 for j, v in enumerate(tail) if v == j + 1),
       sum(1 for v in tail if v >= 1000)))
print("  rows 110..125 prefix+13:", [(j, tail[j]) for j in range(110, 126)])
print("  trailer check:", all(u32(r["tr"], 0) == r["j"] and u32(r["tr"], 4) == u32(r["tr"], 8) != 0
                              and r["tr"][12] == 0 for r in L))

print()
print("=== media(7): body alignment of row 0/1 (client) ===")
raw7 = load(7)
for j in (0, 1):
    H, S = 14, None
    # derive row bounds by scanning identity trailers just to print alignment
    pass
# row0 fixed from t74: payload [14,204)
body = raw7[14:204]
k = u32(body, 0)
print("namelen", k, body[4:4 + k])
print("6B prefix", body[4 + k:10 + k].hex())
ul = u32(body, 10 + k)
print("urllen", ul, body[14 + k:14 + k + ul])
off = 14 + k + ul
print("body len", len(body), "after url at", off)
for i in range(off, len(body), 4):
    print(f"  {i:3d} {body[i:i + 4].hex()} u32={u32(body, i) if i + 4 <= len(body) else None}")
print("last 13 as identity:", struct.unpack_from("<IIIB", body, len(body) - 13))
