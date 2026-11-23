"""t76b scratch: award(0) 64B business-region deep probe."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def rows_fixed(raw, H, S, n):
    return [raw[H + j * S:H + (j + 1) * S] for j in range(n)]


def doms():
    """Reference UID domains from their own identity trailers (data side)."""
    out = {}
    for tid, H, S, off in ((5, 14, 34, 21), (25, 14, 127, 114), (23, 14, 14, 1),
                           (2, 14, 43, 30), (19, 14, 45, 32), (21, 14, 38, 25)):
        raw = load(tid)
        n = (len(raw) - H - 8) // S
        out[tid] = [u32(raw, H + j * S + off + 4) for j in range(n)]
    return out


def main():
    raw = load(0)
    H, S, n = 14, 77, 3545
    rows = rows_fixed(raw, H, S, n)
    print("payload", len(raw), "rows", n)
    # identity recheck
    ok = sum(1 for j, r in enumerate(rows)
             if u32(r, 64) == j and u32(r, 68) == u32(r, 72) != 0 and r[76] == 0)
    print("identity rows ok", ok)

    ref = doms()
    print({k: (len(v), len(set(v))) for k, v in ref.items()})

    def col32(off):
        return [u32(r, off) for r in rows]

    print("\n== FK sweep (u32 col, off 0..60) ==")
    for off in range(0, 61):
        vals = col32(off)
        nff = vals.count(0xFFFFFFFF)
        nz = vals.count(0)
        s = set(vals)
        hits = []
        for tid, d in ref.items():
            ds = set(d)
            h = sum(1 for v in vals if v in ds)
            if h >= n * 0.5:
                hits.append((tid, h))
        if hits or nff > n * 0.3:
            print(f" off{off:2d} ff={nff:4d} zero={nz:4d} d={len(s):4d} "
                  f"hits={hits} sample={vals[:4]}")

    print("\n== u16 sweep ==")
    for off in range(0, 62):
        vals = [int.from_bytes(r[off:off + 2], "little") for r in rows]
        s = set(vals)
        if len(s) <= 40:
            print(f" off{off:2d} u16 d={len(s):3d} min={min(s)} max={max(s)} {sorted(s)[:22]}")

    print("\n== per-byte enum-domain fits (1B) ==")
    sch = json.loads(Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
    fields = sch["entities"]["award.xml"][0]["fields"]
    enums = sch["enums"]
    enum_dom = {}
    for f in fields:
        if f.get("type") == "enum":
            key = f.get("enum_ref") or f["field"]
            enum_dom[f["field"]] = {int(v["enum"]) for v in enums.get(key, {}).get("values", [])
                                    if str(v["enum"]).lstrip("-").isdigit()}
    for off in range(0, 64):
        vals = {r[off] for r in rows}
        fits = [f for f, d in enum_dom.items() if vals <= d and len(vals) >= 2]
        if fits:
            print(f" off{off:2d} vals={sorted(vals)} fits={fits}")


if __name__ == "__main__":
    main()
