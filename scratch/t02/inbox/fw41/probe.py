"""t02-f fw41: row framework only. Variable-length rows (table_41)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

ROOT = Path("D:/tmp2b/fm24-db")
OLD = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
DB = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
OUT = ROOT / "scratch/t02/inbox/fw41/framework.json"
HDR, FTR = 14, 8


def old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def member(mod, archive: str, tid: int) -> tuple[bytes, str]:
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    e = mod._resolve_table(tid, layout["entries"], path.name)
    if e is None:
        raise SystemExit(f"table_{tid} absent from {archive}")
    return mod._decompress_entry(packed, layout["data_base"], e), e["path"]


def walk(raw: bytes) -> dict:
    """Variable row: 4*(u32 len + bytes) + f32 + u32 n + n*7 + 13."""
    n = len(raw)
    count = int.from_bytes(raw[8:12], "little")
    pos = HDR
    lens, hist = [], []
    for i in range(count):
        start = pos
        for _ in range(4):
            if pos + 4 > n:
                raise ValueError(f"row {i}: truncated string length at {pos:#x}")
            ln = struct.unpack_from("<I", raw, pos)[0]
            pos += 4
            if ln > 1 << 20 or pos + ln > n:
                raise ValueError(f"row {i}: bad string length {ln} at {pos - 4:#x}")
            pos += ln
        if pos + 8 > n:
            raise ValueError(f"row {i}: truncated rate/count")
        pos += 4                                    # f32 current_rate
        h = struct.unpack_from("<I", raw, pos)[0]
        pos += 4
        if h > 256:
            raise ValueError(f"row {i}: bad history count {h}")
        pos += h * 7
        pos += 13                                   # row trailer
        if pos > n:
            raise ValueError(f"row {i}: overran payload")
        lens.append(pos - start)
        hist.append(h)
    return {
        "count": count,
        "rows_offset": hex(HDR),
        "row_end": pos,
        "footer_len": n - pos,
        "row_len_min": min(lens) if lens else None,
        "row_len_max": max(lens) if lens else None,
        "row_len_distinct": len(set(lens)),
        "row_len_sample_first10": lens[:10],
        "history_counts_first10": hist[:10],
        "row_len_formula": ("4*(4+len(s)) + 4 + 4 + 7*n_hist + 13 "
                            "[4 UTF-8 strings, f32 rate, u32 hist count, 7B items, 13B trailer]"),
    }


def side(mod, archive: str, tid: int) -> dict:
    raw, name = member(mod, archive, tid)
    n = len(raw)
    count = int.from_bytes(raw[8:12], "little")
    d = {"member": name, "count": count, "stride": None, "rows_offset": "0xe",
         "payload_len": n, "header": raw[:14].hex(" "), "footer": raw[-8:].hex(" "),
         "footer_info": {"offset": hex(n - 8), "bytes": raw[-8:].hex(" ")},
         "variable": True, "payload_sha256": hashlib.sha256(raw).hexdigest()}
    try:
        w = walk(raw)
        d.update(w)
        ok = (w["row_end"] + FTR == n) and (w["footer_len"] == FTR)
        d["closure"] = (f"14 + sum(row_len_i) + 8 == {n} "
                        f"(sum={w['row_end']-HDR}, trailing={w['footer_len']})")
        d["closure_ok"] = bool(ok)
    except ValueError as e:
        d["walk_error"] = str(e)
        d["closure"] = f"variable walk failed: {e}"
        d["closure_ok"] = False
    d["_raw"] = raw
    return d


def run(tid: int, write: bool = True) -> dict:
    mod = old()
    res = {"type_id": tid, "status": "in_progress", "client": None, "server": None,
           "relation": None}
    c = o = None
    for key, arch in (("client", "client_db.dat"), ("server", "server_db.dat")):
        try:
            s = side(mod, arch, tid)
        except SystemExit as e:
            res[key] = {"error": str(e)}
            continue
        if key == "client":
            c = s
        else:
            o = s
        res[key] = {k: v for k, v in s.items() if k != "_raw"}
        if write:                                   # write after each side lands
            OUT.write_text(json.dumps(res, indent=1) + "\n")
    if c and o:
        ident = c["_raw"] == o["_raw"]
        cr, oo = c["_raw"], o["_raw"]
        k = 0
        while k < min(len(cr), len(oo)) and cr[k] == oo[k]:
            k += 1
        res["relation"] = (f"payloads byte-identical={ident}; common prefix {k} of "
                           f"{len(cr)}/{len(oo)} bytes")
        res["payload_identical"] = ident
    if c and o and c.get("closure_ok") and o.get("closure_ok"):
        res["status"] = "complete"
    if write:
        OUT.write_text(json.dumps(res, indent=1) + "\n")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="t02-f row framework probe, read-only")
    ap.add_argument("--tid", type=int, default=41)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r = run(41, write=False)
        ok = r["status"] == "complete" and r["client"]["closure_ok"] and r["server"]["closure_ok"]
        print(json.dumps({k: r[k] for k in ("client", "server", "relation")}, indent=1)[:1200])
        print("selftest", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    r = run(a.tid, write=not a.no_write)
    print(json.dumps({k: v for k, v in r.items()}, indent=1))
    return 0 if r["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
