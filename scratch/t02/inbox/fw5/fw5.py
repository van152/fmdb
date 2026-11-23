"""t02-f: recover row framework (header/count/stride/closure) for a single table id.

Read-only against the game install DB; no game/editor/IDA launch.
  py -V:3.12 -I scripts/../scratch/t02/inbox/fw5/fw5.py --help
"""
from __future__ import annotations
import argparse
import importlib.util
import struct
import sys

DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
HEADER = bytes.fromhex("03017461 642e f10d")


def load_old():
    spec = importlib.util.spec_from_file_location("oldread", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def grab(old, archive: str, tid: int) -> bytes | None:
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        p = e.get("path", e.get("name", ""))
        if old._table_id(p) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    return None


def framework(raw: bytes) -> dict:
    out: dict = {"payload_len": len(raw), "header": raw[:8].hex()}
    out["header_ok"] = raw[:8] == HEADER
    out["count_at_8"] = struct.unpack_from("<I", raw, 8)[0]
    out["u32_0"] = struct.unpack_from("<I", raw, 0)[0]
    out["u32_12"] = struct.unpack_from("<I", raw, 12)[0]
    tail = len(raw) - 22  # 14 head + 8 tail
    tol = []
    for shift in (0,):
        n = out["count_at_8"]
        if n and tail % n == 0:
            tol.append({"count": n, "stride": tail // n})
    out["closure_candidates"] = tol
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="recover row framework for one table id")
    ap.add_argument("--tid", type=int, default=5)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        raw = HEADER + struct.pack("<I", 2) + b"\x00" * 6 + b"AB" * 2 + b"EFGH"
        print(framework(raw))
        return 0
    old = load_old()
    for archive in ("client_db.dat", "server_db.dat"):
        raw = grab(old, archive, a.tid)
        if raw is None:
            print(f"{archive}: table_{a.tid} NOT FOUND")
            continue
        fw = framework(raw)
        print(archive, {k: v for k, v in fw.items()})
        print("  first 48 bytes:", raw[:48].hex())
        print("  last 16 bytes :", raw[-16:].hex())
    return 0


if __name__ == "__main__":
    sys.exit(main())
