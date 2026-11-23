"""t02-f fw8: row framework only. Fixed-stride probe for table_8."""
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
OUT = ROOT / "scratch/t02/inbox/fw8/framework.json"
HDR, FTR = 14, 8


def old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def member(mod, archive: str, tid: int) -> tuple[bytes, str]:
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    e = mod._resolve_table(tid, layout["entries"], path.name)
    return mod._decompress_entry(packed, layout["data_base"], e), e["path"]


def side(mod, archive: str, tid: int) -> dict:
    raw, name = member(mod, archive, tid)
    n = len(raw)
    count = int.from_bytes(raw[8:12], "little")
    body = n - HDR - FTR
    d = {
        "member": name,
        "count": count,
        "rows_offset": hex(HDR),
        "payload_len": n,
        "header": raw[:14].hex(" "),
        "footer": raw[-8:].hex(" "),
        "body_len": body,
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
        "count_le4": count <= 4,
    }
    if count:
        q, r = divmod(body, count)
        d["body_div_count"] = {"quotient": q, "remainder": r}
        d["stride"] = q if r == 0 else None
        d["fixed"] = r == 0
        d["closure"] = (
            f"{HDR} + {count}*{q} + {FTR} == {n}" if r == 0
            else f"{HDR} + {count}*stride + {FTR} != {n} (body={body}, rem={r})"
        )
        d["closure_ok"] = r == 0
    else:
        d["closure"] = f"count=0: payload_len={n} (?)"
        d["closure_ok"] = (n == HDR + FTR)
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
        except (KeyError, SystemExit) as e:
            res[key] = {"error": str(e)}
            continue
        if key == "client":
            c = s
        else:
            o = s
        res[key] = {k: v for k, v in s.items() if k != "_raw"}
        if write:
            OUT.write_text(json.dumps(res, indent=1) + "\n")
    if c and o:
        cr, oo = c["_raw"], o["_raw"]
        k = 0
        while k < min(len(cr), len(oo)) and cr[k] == oo[k]:
            k += 1
        res["relation"] = (f"payloads byte-identical={cr == oo}; common prefix {k} of "
                           f"{len(cr)}/{len(oo)} bytes")
        res["payload_identical"] = cr == oo
    if c and o and c.get("closure_ok") and o.get("closure_ok"):
        res["status"] = "complete"
    if write:
        OUT.write_text(json.dumps(res, indent=1) + "\n")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="t02-f row framework probe, read-only")
    ap.add_argument("--tid", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r = run(a.tid, write=False)
        print(json.dumps({k: r[k] for k in ("client", "server", "relation")}, indent=1)[:1500])
        ok = r["client"] is not None and r["server"] is not None
        print("selftest", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    r = run(a.tid, write=not a.no_write)
    print(json.dumps(r, indent=1))
    return 0 if r["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
