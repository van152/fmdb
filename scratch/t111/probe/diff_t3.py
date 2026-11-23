"""Diff CLUB row3 behavior: isolated vs after-t0, dump globals + reads divergence."""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
import t96c_unicorn_master as M  # noqa: E402


def load_specific(pairs):
    import t38_multiframe as mf
    codec = mf._codec()
    out = {}
    for arch, tid in pairs:
        info = mf.archive_info(codec, arch)
        target = f"{arch}_db/table_{tid}.dat"
        for e in info["entries"]:
            if e["path"] == target:
                start, _ = mf.member_bounds(e, info["data_base"])
                frames = mf.decode_frames_unbounded(info["data"], start)
                for f in frames:
                    if f["length"] == int(e["size"]):
                        out[(arch, tid)] = f["data"]
                        break
                break
    return out


GLOBALS = [0x141AA7808, 0x141B59FA0, 0x141B59EE0, 0x141B5FDA8, 0x141B5FDC8, 0x141B5FDD0, 0x141B5FE00, 0x141B60320, 0x141BF7E10]


def dump_globals(emu, tag):
    vals = {}
    for g in GLOBALS:
        vals[g] = struct.unpack("<Q", bytes(emu.mu.mem_read(g, 8)))[0]
    print(tag, {hex(k): hex(v) for k, v in vals.items()})
    return vals


def run_rows(ut, emu, tid, payload, nrows, tag, dump_from=None):
    pos = 13
    rows = []
    for r in range(nrows):
        flag = payload[pos]
        pos += 1
        obj, vt, s19, err = M.construct_via_factory(ut, emu, tid, flag)
        res = M.run_one_row(ut, emu, obj, s19, payload[pos:pos + 65536], 0x0DF1, 1, a3_ptr=0)
        print(f"{tag} row{r} flag={flag:#x} ok={res['ok']} cons={res['bytes_consumed']} err={str(res['error'])[:60]}")
        if dump_from is not None and r >= dump_from:
            return res
        pos += res["bytes_consumed"]
        rows.append(res)
        if not res["ok"]:
            break
    return rows


def main():
    tabs = load_specific([("server", 0), ("server", 3)])
    p0, p3 = tabs[("server", 0)], tabs[("server", 3)]

    # Scenario A: isolated t3
    ut, emu, _ = M.setup_emulator()
    dump_globals(emu, "A-start")
    resA = run_rows(ut, emu, 3, p3, 4, "A", dump_from=3)
    dump_globals(emu, "A-end")
    readsA = resA["reads"]

    # Scenario B: t0 (1 row + crash row) then t3
    ut2, emu2, _ = M.setup_emulator()
    dump_globals(emu2, "B-start")
    run_rows(ut2, emu2, 0, p0, 2, "B-t0")
    dump_globals(emu2, "B-after-t0")
    resB = run_rows(ut2, emu2, 3, p3, 4, "B", dump_from=3)
    dump_globals(emu2, "B-end")
    readsB = resB["reads"]

    # find divergence
    n = min(len(readsA), len(readsB))
    div = None
    for i in range(n):
        a, b = readsA[i], readsB[i]
        key = ("wire_pos", "n", "dst", "caller")
        if any(a.get(k) != b.get(k) for k in key):
            div = i
            break
    print("readsA", len(readsA), "readsB", len(readsB), "first divergence at", div)
    if div is not None:
        for i in range(max(0, div - 3), min(n, div + 6)):
            print(" A", readsA[i])
            print(" B", readsB[i])
    (ROOT / "scratch/t111/probe/readsA.json").write_text(json.dumps(readsA))
    (ROOT / "scratch/t111/probe/readsB.json").write_text(json.dumps(readsB))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
