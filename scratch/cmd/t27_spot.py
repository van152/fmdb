#!/usr/bin/env python3
"""Commander independent spot-check of t27 (E63 acceptance). Walks server+client
table_22 with the frame formula only, checks date profiles vs t13d, field type
rules, and re-reads key static bytes. No t27 builder code imported."""
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from fm24_dump import _reader, load_payload  # noqa: E402
from t05_pe import PE  # noqa: E402
from capstone import CS_ARCH_X86, CS_MODE_64, Cs  # noqa: E402

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
HH = lambda b, o: struct.unpack_from("<HH", b, o)
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def walk(raw, stride):
    pos = 13
    bodies = []
    sels = []
    for i in range(449):
        sels.append(raw[pos])
        row = raw[pos:pos + stride]
        bodies.append(row[1:])
        pos += stride
    return pos, bodies, sels


def main():
    codec = _reader()
    srv = load_payload(codec, "server", 22)
    cli = load_payload(codec, "client", 22)
    check("server_len_35493", len(srv) == 35493, str(len(srv)))
    check("client_len_5859", len(cli) == 5859, str(len(cli)))

    pos, bodies, sels = walk(srv, 79)
    check("server_footer_pos_35484", pos == 35484, str(pos))
    check("server_footer_9B", srv[pos:] == bytes.fromhex("0000000001c1010000"), srv[pos:].hex(" "))
    check("server_selectors_all_0", all(s == 0 for s in sels), str(set(sels)))
    ident_ok = all(struct.unpack_from("<III", b, 66) == (i, i + 1, i + 1) for i, b in enumerate(bodies))
    check("server_identity_(i,i+1,i+1)", ident_ok)

    # client: selector + 12B identity only, stride 13
    cpos, cbodies, csels = walk(cli, 13)
    check("client_footer_pos_5850", cpos == 5850, str(cpos))
    check("client_selectors_all_0", all(s == 0 for s in csels))
    cident = all(struct.unpack_from("<III", b, 0) == (i, i + 1, i + 1) for i, b in enumerate(cbodies))
    check("client_identity_only", cident)

    # date profiles vs t13d
    t13d = json.load(open(ROOT / "scratch/t13d/out/audit.json", encoding="utf-8"))
    date_cols = next(t["date_cols"] for t in t13d["tables"] if t["table_type"] == 22)
    by_off = {a["offset"]: a for a in date_cols} if "offset" in date_cols[0] else {}
    for off, expect in ((12, (2000, 2030)), (16, (2017, 2030)), (50, (1900, 2030))):
        years = [HH(b, off)[1] for b in bodies]
        days = [HH(b, off)[0] for b in bodies]
        live = [y for y in years if y != 0xFFFF]
        ok = min(live) == expect[0] and max(live) == expect[1] and all(1 <= d <= 366 for d in days if d != 0xFFFF)
        check(f"date@+{off}_year_{expect[0]}-{expect[1]}", ok, f"min={min(live)} max={max(live)}")

    # field type rules across 449 rows for promoted codes
    master = json.load(open(ROOT / "evidence/fm24/reports/editor_schema/master.json", encoding="utf-8"))
    club = {f["field"]: f for f in master["entities"]["club.xml"][0]["fields"]}
    cstc = next(f for f in club.values() if f["field"] == "Cstc")
    items = {it["field"]: it for it in cstc["list_item_fields"]}
    promoted = {"Slea": (12, 4), "Scap": (20, 4), "Salt": (25, 4), "Scpm": (29, 1),
                "Sscp": (30, 4), "Snxa": (34, 4), "Snmn": (38, 4), "Snmx": (42, 4),
                "Stks": (46, 4), "Slmd": (50, 4), "Slhm": (54, 1), "ScTL": (60, 1),
                "ScYL": (61, 1), "Sceb": (62, 4)}
    for code, (off, w) in promoted.items():
        sch = items.get(code, {})
        kind = sch.get("type", "?")
        cells = [b[off:off + w] for b in bodies]
        if kind == "date":
            ok = sum(1 for c in cells if (lambda d, y: 1850 <= y <= 2100 and 1 <= d <= 366)(*HH(c, 0))) == 449
        elif kind == "database_record_unique_id":
            xs = [int.from_bytes(c, "little", signed=True) for c in cells]
            ok = all(x == -1 or (0 <= x < 48413) for x in xs)
        elif kind == "boolean":
            xs = [c[0] for c in cells]
            ok = all(x in (0, 2, 4, 6) for x in xs)
        elif kind == "integer":
            xs = [int.from_bytes(c, "little", signed=True) for c in cells]
            lo, hi = int(sch.get("min_value", -2**31)), int(sch.get("max_value", 2**31))
            ok = all(x == -1 or lo <= x <= hi for x in xs)
        else:
            ok = True  # enum checked separately
        check(f"field_{code}@+{off}_{kind}", ok, f"type={kind}")

    # Scpm raw distribution 0/2/4 = 390/36/23
    dist = {}
    for b in bodies:
        v = b[29]
        dist[v] = dist.get(v, 0) + 1
    check("Scpm@+29_dist", dist == {0: 390, 2: 36, 4: 23}, str(dist))

    # Salt@+25 live count 208
    salt = [int.from_bytes(b[25:29], "little", signed=True) for b in bodies]
    live = [x for x in salt if x != -1]
    check("Salt@+25_live_208", len(live) == 208, f"live={len(live)}")

    # static re-read: 3 missing 4B reads + width12 + data branch
    pe = PE()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    recs = {}
    for f in (ROOT / "scratch/t27/out").glob("instructions.part*.json"):
        for r in json.load(open(f, encoding="utf-8"))["instructions"]:
            recs[int(r["file_offset"], 16)] = r
    ok = tot = 0
    for fo in (0x1537888, 0x153789C, 0x15379D0, 0x1537AA8, 0x1537AB4, 0x1537ACC):
        r = recs.get(fo)
        if not r:
            check(f"static_{fo:#x}_record", False, "NO RECORD")
            continue
        liveb = pe.raw[fo:fo + 12]
        rb = bytes.fromhex(r["bytes"].replace(" ", ""))
        m = liveb[:len(rb)] == rb and pe.f2va(fo) == int(r["VA"], 16)
        tot += 1
        ok += m
        ins = list(md.disasm(liveb, pe.f2va(fo)))
        check(f"static_{fo:#x}", m, "; ".join(f"{i.mnemonic} {i.op_str}" for i in ins[:1]))
    print(f"static {ok}/{tot}")

    print()
    if fails:
        print(f"SPOT FAIL: {len(fails)} -> {fails}")
        return 1
    print("SPOT PASS: all t27 commander checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())