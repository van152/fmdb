"""t76b scratch: media(7) full-row byte map for chosen rows."""
import runpy, sys, struct
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def media_rows(arch):
    raw = D["load_payload"](C, arch, 7)
    n = u32(raw, 8)
    hi = len(raw) - 8
    pos, rows = 14, []
    for j in range(n):
        k = u32(raw, pos)
        best = None
        for e in range(pos + 13 + 4 + k, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o != j or u1 != u2 or u1 == 0 or m != 0:
                continue
            if e < hi:
                k2 = u32(raw, e)
                if k2 > 64:
                    continue
                try:
                    nm = raw[e + 4:e + 4 + k2].decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if not nm or any(ord(c) < 0x20 for c in nm):
                    continue
            best = e
        rows.append((pos, best))
        pos = best
    return raw, rows


raw, rows = media_rows("client")
for j in (6, 0):
    s, e = rows[j]
    body = raw[s:e]
    print(f"=== row{j} start={s} end={e} len={len(body)}")
    for i in range(0, len(body), 16):
        chunk = body[i:i + 16]
        txt = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        print(f"  {i:3d}: {chunk.hex(' '):<48} {txt}")
