"""t02-f: table_24 row framework probe (read-only).

Restores only the row frame: payload header, count, row start/stride or variable
row boundary rule, and closure. No field decoding.

Run:  py -V:3.12 -I probe24.py [--tid N] [--selftest] [--no-write]
Exit: 0 = framework complete (closure holds), 1 = check failed, 2 = usage/fatal
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
OLD = Path(r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
DB = Path(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm")
OUTDIR = ROOT / "scratch/t02/inbox/fw24"
HDR, ROW_ID_LEN = 14, 4
MAGIC = bytes([0x03, 0x01, 0x74, 0x61, 0x64, 0x2E, 0xF1, 0x0D])


def load_old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def member(mod, archive: str, tid: int):
    """Return (payload_bytes, member_path) or (None, None) when absent."""
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    for e in layout["entries"]:
        if mod._table_id(e["path"]) == tid:
            return mod._decompress_entry(packed, layout["data_base"], e), e["path"]
    return None, None


def split_rows(raw: bytes, count: int) -> dict:
    """Row boundary rule for table_24: each row starts with u32 row_index,
    then a u32 duplicate at +4/+8, then a shape byte at +12.

    Several positions can carry the same index, so candidate chains are built
    from every candidate start for row 0 and the one that covers all rows is kept.
    """
    n = len(raw)
    cand = {}
    for p in range(HDR, n - 13):
        v = raw[p] | raw[p + 1] << 8 | raw[p + 2] << 16 | raw[p + 3] << 24
        if v >= count:
            continue
        if raw[p + 4:p + 8] != raw[p + 8:p + 12]:
            continue
        cand.setdefault(v, []).append(p)

    # rows 0..count-2 carry a shape byte in {0x01, 0x0a, 0x0b} at +12;
    # the final entry (id count-1) is a short terminator with shape 0x00.
    shaped = {v: [p for p in ps if raw[p + 12] in (0x01, 0x0A, 0x0B)]
              for v, ps in cand.items()}
    runner = count - 1 if count > 1 else 0

    best = None
    for first in shaped.get(0, []):
        starts, expected, cur = [first], 1, first
        while expected < runner:
            nxt = [p for p in shaped.get(expected, []) if p > cur]
            if not nxt:
                break
            cur = nxt[0]
            starts.append(cur)
            expected += 1
        if expected == runner:
            tail = [p for p in cand.get(count - 1, []) if p > cur]
            if tail:
                starts.append(tail[0])
                if best is None or len(starts) > len(best):
                    best = starts
    if best is None or len(best) != count:
        got = len(best) if best else 0
        return {"ok": False,
                "reason": f"found {got} of {count} row starts"}
    starts = best

    lens = [starts[i + 1] - starts[i] for i in range(count - 1)]
    tail_len = n - starts[-1]
    shapes = {}
    for i in range(count):
        L = lens[i] if i < count - 1 else tail_len
        shapes.setdefault(raw[starts[i] + 12], []).append(L)
    runner_len = lens[:-1] if len(lens) > 1 else []
    summary = {
        hex(t): {"rows": len(v), "len_min": min(v), "len_max": max(v),
                 "len_distinct": len(set(v)),
                 "len_top": sorted(((v.count(x), x) for x in set(v)), reverse=True)[:5]}
        for t, v in shapes.items()
    }
    return {
        "ok": True,
        "row0_offset": starts[0],
        "prefix_len": starts[0] - HDR,
        "prefix_hex": raw[HDR:starts[0]].hex(" "),
        "row_len_sum": n - starts[0],
        "runner_rows": count - 1,
        "runner_len_min": min(runner_len) if runner_len else None,
        "runner_len_max": max(runner_len) if runner_len else None,
        "terminator_len": tail_len,
        "shape_byte_summary": summary,
        "row_len_ctr": {"min": min(lens), "max": max(lens)},
    }


def side(mod, archive: str, tid: int) -> dict:
    raw, name = member(mod, archive, tid)
    if raw is None:
        return {"member": None,
                "absent": True,
                "note": f"table_{tid}.dat not present in {archive} member directory"}
    n = len(raw)
    head = raw[:HDR]
    count = struct.unpack_from("<I", raw, 8)[0]
    body = n - HDR
    d = {
        "member": name,
        "count": count,
        "stride": None,
        "rows_offset": "0xe",
        "payload_len": n,
        "header": head.hex(" "),
        "header_magic_ok": head[:8] == MAGIC,
        "footer": raw[n - 8:].hex(" "),
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
        "variable": True,
    }
    if count and body % count == 0:
        d["variable"] = False
        d["stride"] = body // count
    rows = split_rows(raw, count)
    d["rows"] = rows
    if rows.get("ok"):
        d["closure"] = (f"14 + {rows['prefix_len']}(prefix) + {rows['row_len_sum']}"
                        f"(sum of {count} variable rows) == {n}")
        d["closure_ok"] = HDR + rows["prefix_len"] + rows["row_len_sum"] == n
    else:
        d["closure"] = f"row split failed: {rows.get('reason')}"
        d["closure_ok"] = False
    d["_raw"] = raw
    return d


def run(tid: int, write: bool = True) -> dict:
    mod = load_old()
    res = {"type_id": tid, "status": "in_progress", "client": None, "server": None,
           "relation": None}
    if write:
        OUTDIR.mkdir(parents=True, exist_ok=True)
        (OUTDIR / "framework.json").write_text(json.dumps(res, indent=1) + "\n")

    got = {}
    for key, archive in (("client", "client_db.dat"), ("server", "server_db.dat")):
        s = side(mod, archive, tid)
        got[key] = s
        res[key] = {k: v for k, v in s.items() if k != "_raw"}
        if write:                      # rewrite as soon as each side lands
            (OUTDIR / "framework.json").write_text(json.dumps(res, indent=1) + "\n")

    c, sv = got["client"].get("_raw"), got["server"].get("_raw")
    if c is not None and sv is not None:
        k = 0
        while k < min(len(c), len(sv)) and c[k] == sv[k]:
            k += 1
        res["relation"] = (f"payloads byte-identical={c == sv}; "
                           f"common prefix {k} of {len(c)}/{len(sv)} bytes")
        res["payload_identical"] = c == sv
    elif c is None or sv is None:
        missing = "client" if c is None else "server"
        present = "server" if c is None else "client"
        res["relation"] = (f"{missing} member absent (server-only table): "
                           f"no cross-side comparison possible")

    ok = all(got[k].get("closure_ok") for k in got if got[k].get("member"))
    res["status"] = "complete" if ok else "in_progress"
    if write:
        (OUTDIR / "framework.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="t02-f row framework probe (read-only)")
    ap.add_argument("--tid", type=int, default=24)
    ap.add_argument("--selftest", action="store_true",
                    help="re-derive table_24 in memory and assert closure")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    res = run(a.tid, write=not a.no_write)
    for k in ("client", "server"):
        s = res[k] or {}
        print(k, {kk: s.get(kk) for kk in ("member", "count", "stride", "payload_len",
                                           "closure", "closure_ok")})
        if s.get("rows", {}).get("ok"):
            r = s["rows"]
            print("   row0_offset", r["row0_offset"], "prefix_len", r["prefix_len"],
                  "row_len_sum", r["row_len_sum"])
            print("   shapes", json.dumps(r["shape_byte_summary"]))
    print("relation:", res["relation"])
    print("status:", res["status"])
    if a.selftest:
        sv = res["server"]
        ok = (res["status"] == "complete" and sv["closure_ok"]
              and sv["count"] == 84507 and sv["rows"]["row0_offset"] == 122 + 14
              and sv["rows"]["prefix_len"] == 122
              and sv["rows"]["shape_byte_summary"].get("0xa", {}).get("rows") == 84256
              and sv["rows"]["terminator_len"] == 21)
        print("selftest", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    return 0 if res["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
