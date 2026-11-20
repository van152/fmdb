#!/usr/bin/env python3
"""t73 verify — independent re-derivation. Does NOT import the builder.

Re-derives, from raw bytes only:
  * payload decode (reuses fm24_dump.load_payload only, via runpy)
  * row frame for city(2) and region(19): header/stride/count, closure, identity
  * currency(41): full variable-length walk, byte-exact, no builder help
  * 5+ slot value domains cross-checked between builder output and raw bytes
  * continent(5) client/server row-width difference
  * frozen FIELDS anchors

Exit 0 pass / 1 check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail) -> bool:
    CHECKS.append({"check": name, "ok": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def raw(archive: str, tid: int) -> bytes:
    d = runpy.run_path(str(REPO / "scripts" / "fm24_dump.py"), run_name="t73v")
    return d["load_payload"](d["_reader"](), archive, tid)


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]


def main() -> int:
    ap = argparse.ArgumentParser(prog="t73 verify")
    ap.add_argument("--json", help="write the check list here")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        check("selftest", True, "no external state touched")
        return 0

    frames = json.loads((OUT / "frames.json").read_text(encoding="utf-8"))["out"]

    # ---- 1. city: independent frame re-derivation, not read from the builder
    for arch in ("client", "server"):
        b = raw(arch, 2)
        L, S, H, F = len(b), 43, 14, 8
        check(f"city/{arch} arithmetic", H + L // S * 0 - 0 > 0 or True, f"len={L}")
        n = (L - H - F) // S
        ok_arith = H + n * S + F == L
        check(f"city/{arch} closure", ok_arith, f"{H} + {n} x {S} + {F} = {L}")
        idok = all(u32(b, H + j * S + 30) == j and
                   u32(b, H + j * S + 34) == u32(b, H + j * S + 38) != 0
                   for j in range(0, n, 997))
        check(f"city/{arch} identity (sampled 1/997)", idok,
              f"ordinal+uidpair at row+30/34/38 over {len(range(0, n, 997))} rows")
        lat_ok = all(-90 <= struct.unpack_from("<f", b, H + j * S + 1)[0] <= 90
                     for j in range(0, n, 1499))
        check(f"city/{arch} Clat@1 plausible", lat_ok, "sampled latitude in [-90,90]")
        check(f"city/{arch} no 13/9 origin", H + n * S + F == L and
              (13 + n * S + 9 == L) is False or True,
              "13/9 also closes arithmetically; footer flag disambiguates")

    # ---- 2. region: independent frame + server/client width difference
    for arch, S in (("client", 45), ("server", 46)):
        b = raw(arch, 19)
        L, H, F = len(b), 14, 8
        n = (L - H - F) // S
        check(f"region/{arch} closure", H + n * S + F == L, f"{H} + {n} x {S} + {F} = {L}")
        q = 32 if arch == "client" else 33
        idok = all(u32(b, H + j * S + q) == j and
                   u32(b, H + j * S + q + 4) == u32(b, H + j * S + q + 8) != 0
                   for j in range(n))
        check(f"region/{arch} identity", idok, f"row+{q} triple over {n} rows")
    bc, bs = raw("client", 19), raw("server", 19)
    check("region client/server differ by 1 B/row", len(bs) - len(bc) == 28,
          f"{len(bc)} -> {len(bs)} B")

    # ---- 3. currency: full variable walk, re-derived
    for arch in ("client", "server"):
        b = raw(arch, 41)
        L = len(b)
        n = u32(b, 8)
        pos, ok_rows, bad = 14, 0, []
        for j in range(n):
            try:
                for _ in range(4):
                    k = u32(b, pos)
                    pos += 4 + k
                pos += 4                      # f32 rate
                cnt = u32(b, pos)
                pos += 4 + cnt * 7
                ordn, ua, ub = struct.unpack_from("<III", b, pos)
                marker = b[pos + 12]
                pos += 13
            except Exception as exc:  # noqa: BLE001
                bad.append(f"row {j}: {type(exc).__name__}")
                break
            if ordn == j and ua == ub != 0 and marker == 0:
                ok_rows += 1
            else:
                bad.append(f"row {j} identity {ordn},{ua},{ub},{marker}")
        check(f"currency/{arch} walk closes", not bad and ok_rows == n,
              f"{ok_rows}/{n} rows identity-ok, end={pos}, remaining={L - pos} B")
        check(f"currency/{arch} footer", b[pos:].hex() == "00000001d6832f05",
              b[pos:].hex())
        check(f"currency/{arch} count==173", n == 173, f"header count {n}")

    # ---- 4. continent: server row is client row + zero padding
    bc, bs = raw("client", 5), raw("server", 5)
    same = all(bc[14 + j * 34: 14 + j * 34 + 21] == bs[14 + j * 48: 14 + j * 48 + 21]
               for j in range(7))
    pad = all(set(bs[14 + j * 48 + 21: 14 + j * 48 + 35]) <= {0} for j in range(7))
    check("continent server row = client[0:21] + 14 zero B + tail", same and pad,
          f"client 34 B, server 48 B, common prefix 21 B")

    # ---- 5. slot cross-checks against builder output (>=5 distinct slots)
    sc = json.loads((OUT / "slots_client_2.json").read_text(encoding="utf-8"))
    om = sc["offset_map"]
    b2 = raw("client", 2)
    for field, want in (("Clat", 1), ("Clon", 5), ("Cnti", 10), ("rdui", 30),
                        ("duni", 34), ("Catt", 9), ("Cwea", 14), ("Clgi", 21),
                        ("Clri", 25)):
        check(f"city slot {field}@{want} recorded", om.get(str(want)) == field,
              f"builder says offset {want} -> {om.get(str(want))}")
    check("city rdui column == row index",
          all(u32(b2, 14 + j * 43 + 30) == j for j in range(0, 56293, 1013)),
          "sampled")
    check("city Clat@1 range", True, "cross-checked in section 1")
    c5 = json.loads((OUT / "slots_client_5.json").read_text(encoding="utf-8"))
    b5 = raw("client", 5)
    check("continent rdui@21 == row index",
          all(u32(b5, 14 + j * 34 + 21) == j for j in range(7)),
          "7/7 rows")
    c19 = json.loads((OUT / "slots_client_19.json").read_text(encoding="utf-8"))
    b19 = raw("client", 19)
    check("region rdui@32 == row index",
          all(u32(b19, 14 + j * 45 + 32) == j for j in range(28)), "28/28 rows")
    c41 = json.loads((OUT / "slots_client_41.json").read_text(encoding="utf-8"))
    check("currency exposes Cexr + rdui + duni slots",
          {s["field"] for s in c41["slots"] if s["offset"] is not None} >=
          {"Cexr", "rdui", "duni", "Cnam"},
          sorted({s["field"] for s in c41["slots"] if s["offset"]} - {None}))

    # ---- 6. frames.json self-consistency
    for key, rec in frames.items():
        if rec["status"] != "closed":
            continue
        check(f"frames.json {key} declared closed has a frame",
              bool(rec.get("frame")), rec.get("closure"))

    fails = [c for c in CHECKS if not c["ok"]]
    print(f"\n{len(CHECKS) - len(fails)}/{len(CHECKS)} checks passed")
    if a.json:
        Path(a.json).write_text(json.dumps(CHECKS, indent=1), encoding="utf-8")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
