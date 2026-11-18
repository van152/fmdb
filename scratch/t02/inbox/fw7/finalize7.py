"""t02-f: table_7 row framework — exact boundary walk (client + server). Read-only.

Empirical row model (L1):
  payload  = 14B header | body | 8B footer
  body     = row_0 .. row_{count-1}, contiguous, no padding
  row_i    = <variable payload> + 14B trailer
  trailer  = <u8 flag 0|1> <u32 row_id == i> <u32 A> <u32 A> <u8 0x00>

Trailer candidates are disambiguated by lookahead (`next row must start with a
u32-length-prefixed name`), because flag/row_id/A triples can repeat inside
row payloads. No field semantics are decoded here.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import struct
import sys

OLD = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 7
OUT = r"D:\tmp2b\fm24-db\scratch\t02\inbox\fw7\framework.json"
HDR = bytes([0x03, 0x01, 0x74, 0x61, 0x64, 0x2E, 0xF1, 0x0D])
HDR_LEN, FTR_LEN, TRL_LEN = 14, 8, 14

spec = importlib.util.spec_from_file_location("oldread", OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def payload(archive: str, tid: int) -> bytes:
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit(f"table_{tid} not found in {archive}")


def name_ok(body: bytes, p: int) -> bool:
    """A row starts with u32 name_len + UTF-8 name with no control chars
    (structural check only; name charset is irrelevant to framing)."""
    if p + 4 > len(body):
        return False
    L = struct.unpack_from("<I", body, p)[0]
    if not 1 <= L <= 120 or p + 4 + L > len(body):
        return False
    try:
        s = body[p + 4:p + 4 + L].decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(ord(c) >= 32 for c in s)


def is_trailer(body: bytes, p: int, i: int) -> bool:
    if p + TRL_LEN > len(body):
        return False
    if body[p] not in (0, 1) or body[p + TRL_LEN - 1] != 0:
        return False
    if struct.unpack_from("<I", body, p + 1)[0] != i:
        return False
    a, b = struct.unpack_from("<II", body, p + 5)
    return a == b


def walk(body: bytes, count: int):
    pos, bounds, flags = 0, [], []
    for i in range(count):
        p, hit = pos, None
        while p + TRL_LEN <= len(body):
            if is_trailer(body, p, i):
                nxt = p + TRL_LEN
                if i == count - 1:
                    if nxt == len(body):
                        hit = p
                        break
                elif name_ok(body, nxt):
                    hit = p
                    break
            p += 1
        if hit is None:
            return bounds, pos, i, flags
        bounds.append((pos, hit))
        flags.append(body[hit])
        pos = hit + TRL_LEN
    return bounds, pos, None, flags


def side(archive: str) -> dict:
    raw = payload(archive, TID)
    n = len(raw)
    head = raw[:HDR_LEN]
    assert head[:8] == HDR, head.hex()
    count = struct.unpack_from("<I", raw, 8)[0]
    body = raw[HDR_LEN:n - FTR_LEN]
    bounds, end, failed, flags = walk(body, count)
    lens = [b - a for a, b in bounds]
    payload_lens = [b - a for a, b in bounds]
    names = [struct.unpack_from("<I", body, a)[0] for a, _ in bounds]

    info = {
        "member": f"{archive}/table_{TID}.dat",
        "count": count,
        "stride": None,
        "rows_offset": "0xe",
        "payload_len": n,
        "header": head.hex(" "),
        "footer": raw[n - FTR_LEN:].hex(" "),
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
        "variable": len(set(lens)) > 1,
        "row0_offset": HDR_LEN,
        "trailer_len": TRL_LEN,
        "row_trailer": "<u8 flag 0|1> <u32 row_id == row index> <u32 A> <u32 A> <u8 0x00>",
        "row_len_formula": ("row_len = 4 + name_len + rest + 14(trailer); "
                            "no padding, rows are contiguous"),
        "row_len_min": min(lens) if lens else None,
        "row_len_max": max(lens) if lens else None,
        "row_len_distinct": len(set(lens)),
        "name_len_min": min(names) if names else None,
        "name_len_max": max(names) if names else None,
        "trailer_flag_values": sorted(set(flags)),
        "rows_consumed": len(bounds),
        "rows_end": hex(HDR_LEN + end),
    }
    ok = failed is None and end == len(body) and len(bounds) == count
    info["closure"] = (f"14 + sum(row_len_i) + 8 == {n}  "
                       f"(sum={HDR_LEN + end + FTR_LEN}, rows={len(bounds)}/{count})")
    info["closure_ok"] = ok
    if not ok:
        info["failure"] = {"first_unwalked_row": failed,
                           "walk_stopped_at": end, "body_len": len(body)}
    info["first_row_starts"] = [a for a, _ in bounds[:8]]
    info["row0_hex"] = (body[0:bounds[0][1] + TRL_LEN].hex(" ") if bounds else None)
    info["_bounds"] = bounds
    info["_raw"] = raw
    return info


def main() -> int:
    cl = side("client_db.dat")
    sv = side("server_db.dat")
    bc = cl.pop("_bounds")
    bs = sv.pop("_bounds")
    raw_c = cl.pop("_raw")
    raw_s = sv.pop("_raw")

    k = 0
    for a, b in zip(raw_c, raw_s):
        if a != b:
            break
        k += 1
    same_layout = (len(bc) == len(bs) and
                   all((y - x) == (d - c) for (x, y), (c, d) in zip(bc, bs)))
    rel = ("payload byte-identical" if raw_c == raw_s
           else f"common prefix {k} of {len(raw_c)}/{len(raw_s)} bytes")
    if same_layout:
        rel += "; row_len vector identical on both sides"
    else:
        rel += "; row_len vectors differ"

    out = {"type_id": TID, "status": "complete", "client": cl, "server": sv,
           "relation": rel, "payload_identical": raw_c == raw_s,
           "row_layout_identical": same_layout}

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    for tag, s in (("client", cl), ("server", sv)):
        print(tag, {k2: v for k2, v in s.items() if k2 != "row0_hex"})
    print("relation:", rel)
    print("closure_ok:", cl["closure_ok"], sv["closure_ok"])
    if not (cl["closure_ok"] and sv["closure_ok"]):
        print("FAIL", cl.get("failure"), sv.get("failure"))
    return 0 if (cl["closure_ok"] and sv["closure_ok"]) else 1


if __name__ == "__main__":
    sys.exit(main())
