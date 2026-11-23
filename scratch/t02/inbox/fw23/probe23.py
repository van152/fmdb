"""t02-f: table_23 row framework probe (client + server). Read-only."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import struct
import sys

OLD = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 23
OUT = r"D:\tmp2b\fm24-db\scratch\t02\inbox\fw23\framework.json"

spec = importlib.util.spec_from_file_location("oldread", OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def payload(archive: str, tid: int) -> bytes:
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        t = old._table_id(e.get("path", e.get("name", "")))
        if t == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit(f"table_{tid} not found in {archive}")


def side(archive: str) -> dict:
    raw = payload(archive, TID)
    n = len(raw)
    head = raw[:14]
    assert head[:8] == bytes([0x03, 0x01, 0x74, 0x61, 0x64, 0x2E, 0xF1, 0x0D]), head.hex()
    count = struct.unpack_from("<I", raw, 8)[0]
    info = {
        "member": f"{archive}/table_{TID}.dat",
        "count": count,
        "stride": None,
        "rows_offset": "0xe",
        "payload_len": n,
        "header": head.hex(" "),
        "footer": raw[n - 8:].hex(" "),
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
    }
    body = n - 14 - 8
    if count > 0 and body % count == 0:
        stride = body // count
        info["stride"] = stride
        info["variable"] = False
        info["closure"] = f"14 + {count}*{stride} + 8 == {n}"
        info["closure_ok"] = 14 + count * stride + 8 == n
        info["_rows"] = raw[14:14 + count * stride]
    else:
        info["variable"] = True
        info["closure"] = f"body={body} not divisible by count={count} (variable-length rows)"
        info["closure_ok"] = False
        info["_rows"] = raw[14:n - 8]
    info["_raw"] = raw
    return info


def main() -> int:
    cl = side("client_db.dat")
    sv = side("server_db.dat")
    rows_c = cl.pop("_rows")
    rows_s = sv.pop("_rows")
    raw_c = cl.pop("_raw")
    raw_s = sv.pop("_raw")

    same = raw_c == raw_s
    k = 0
    for a, b in zip(raw_c, raw_s):
        if a != b:
            break
        k += 1
    rel = (f"payloads byte-identical=True; len {len(raw_c)}/{len(raw_s)}"
           if same else f"common prefix {k} of {len(raw_c)}/{len(raw_s)} bytes")

    out = {"type_id": TID, "status": "complete", "client": cl, "server": sv,
           "relation": rel, "payload_identical": same}

    # row-shape diagnostics on client (helps a follow-up, not a field decode)
    if cl["stride"]:
        s = cl["stride"]
        out["client"]["row0_hex"] = rows_c[:s].hex(" ")
        out["client"]["u32_at_row0_every4"] = [
            struct.unpack_from("<I", rows_c, i)[0] for i in range(0, s - 3, 4)
        ]
        # monotone ordinal check: which 4-byte slot equals row index for first 40 rows
        hits = []
        for off in range(0, s - 3):
            ok = True
            for i in range(min(40, cl["count"])):
                if struct.unpack_from("<I", rows_c, i * s + off)[0] != i:
                    ok = False
                    break
            if ok:
                hits.append(off)
        out["client"]["ordinal_u32_offsets_first40"] = hits

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("client", "server")}, ensure_ascii=False))
    print("client:", {k: v for k, v in cl.items() if k != "row0_hex"})
    print("server:", {k: v for k, v in sv.items() if k != "row0_hex"})
    return 0 if (cl["closure_ok"] and sv["closure_ok"]) else 1


if __name__ == "__main__":
    sys.exit(main())
