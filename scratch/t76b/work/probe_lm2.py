"""t76b scratch: exact byte dumps for media(7) row0 and language(8) prefix values."""
import runpy, sys, struct
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


raw7 = load(7)
row = raw7[14:204]
print("media row0 len", len(row))
for i in range(0, len(row), 8):
    seg = row[i:i + 8]
    print(f"{i:3d}: {seg.hex(' ')}")
print()
print("hashtag candidates: u32 at 66 =", u32(row, 66), " at 67 =", u32(row, 67))
print("u32 chain from 66:", [u32(row, o) for o in range(66, 100, 1)][:20])
print()
raw8 = load(8)
pos = 14
vals = []
for j in range(126):
    k = u32(raw8, pos)
    name = raw8[pos + 4:pos + 4 + k].decode("utf-8", "replace")
    pre = raw8[pos + 4 + k:pos + 4 + k + 17]
    vals.append((j, name, pre, u32(pre, 13)))
    pos += 4 + k + 30
print("language pre13 values (all 126):")
for j, nm, pre, v in vals:
    print(f"  {j:3d} {nm[:20]:20s} pre13_u32={v:>12d} pre13_hex={pre[13:17].hex()} pre0_13={pre[:13].hex()}")
