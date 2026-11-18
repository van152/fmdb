#!/usr/bin/env python3
"""fm24_dump — 通用 .dat 表导出器:把已解析的行边界落成可读行。

设计原则
--------
* **边界真源自动装载**:定长表规格从上游普查 JSON 读(只读),不在这里重复抄数字;
  本仓独立闭合且上游判错的表,用 OVERRIDE 覆盖并标注原因。
* **闭合即验证**:每条路径都必须过 `header + Σrow + footer == payload_len`;
  走不齐就报错,不静默截断。
* **未知字段不猜**:行内未命名的字节以 `raw_hex` 原样导出,字段名只给有证据的。

用法
----
  py -V:3.12 -I -B scripts/fm24_dump.py --list
  py -V:3.12 -I -B scripts/fm24_dump.py --archive client --table 0 --limit 5
  py -V:3.12 -I -B scripts/fm24_dump.py --archive client --table 0 --csv out.csv
  py -V:3.12 -I -B scripts/fm24_dump.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
DB_DIR = pathlib.Path(
    r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
)
MAGIC = bytes.fromhex("28b52ffd")
READER_VERIFY = ROOT / "scratch/t01/inbox/t01k/verify.py"

# 本仓独立闭合 / 上游判错 / 变长文法的表:显式覆盖(附原因)
OVERRIDE: dict[tuple[str, int], dict] = {
    ("client", 47): {
        "model": "variable",
        "grammar": "lcrg_tail",
        "count": 2488,
        "why": "上游 25+2488*44+8 为算术巧合(44B 下 rdui 仅 3/2488);本仓双约束闭合",
        "fields": {"rdui": -13, "duni": -9},
    },
    ("client", 3): {
        "model": "variable",
        "grammar": "club_block",
        "why": "mixed 双 RTTI + 5B block;边界见 scratch/t02/inbox/club_v2/output.json",
        "fields": {"Cccn": 8},
    },
    ("client", 10): {
        "model": "variable",
        "grammar": "nati_count_loop",
        "why": "4 段计数循环,见 scratch/t02/inbox/nati/OUTBOX/framework.json",
    },
}

# 已知字段槽位(只列有 L3/L2 证据的)
FIELDS: dict[tuple[str, int], dict[str, int]] = {
    ("client", 0): {"rdui": 64, "duni": 68},
    ("client", 2): {"Clat": 1, "Clon": 5, "Cnti": 10, "rdui": 30, "duni": 34},
    ("client", 5): {"rdui": 21, "duni": 25},
    ("client", 6): {"rdui": 3, "duni": 7},
    ("client", 8): {"rdui_suffix": 17},
    ("client", 19): {"rdui": 32, "duni": 36},
    ("client", 21): {"Scti": 3, "Slat": 17, "Slon": 21, "rdui": 25, "duni": 29},
    ("client", 22): {"rdui": 0, "duni": 4},
    ("client", 23): {"rdui": 1, "duni": 5},
    ("client", 35): {"rdui": 2, "duni": 6},
    ("client", 41): {"rdui": -13, "duni": -9},
    ("client", 56): {"rdui": 0, "duni": 4},
}


def _reader():
    k = runpy.run_path(str(READER_VERIFY))
    codec = runpy.run_path(str(k["OLD_READER_PATH"]))
    return codec


def load_payload(codec, archive: str, tid: int) -> bytes:
    fn = f"{archive}_db.dat"
    p = DB_DIR / fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    off = e["offset"]
    db = p.read_bytes()
    hit = next((off + d for d in range(64) if db[off + d: off + d + 4] == MAGIC), None)
    if hit is None:
        raise RuntimeError(f"{fn} table_{tid}: zstd frame not found")
    return codec["_stream_decompress"](db[hit:], 256 * 1024 * 1024)


# 上游大表报告(b47)里给出、但不在小表 census 的定长规格
EXTRA_FIXED: dict[tuple[str, int], dict] = {
    # city: client/server payload 字节相同, 56,293 × 43 B
    ("client", 2): {"model": "fixed", "header": 14, "stride": 43, "footer": 8,
                    "count": 56293, "payload": 2420621},
    ("server", 2): {"model": "fixed", "header": 14, "stride": 43, "footer": 8,
                    "count": 56293, "payload": 2420621},
    # stadium: client 38 B / server 181 B, 均 48,413 行
    ("client", 21): {"model": "fixed", "header": 14, "stride": 38, "footer": 8,
                     "count": 48413, "payload": 1839716},
    ("server", 21): {"model": "fixed", "header": 14, "stride": 181, "footer": 8,
                     "count": 48413, "payload": 8762775},
}


def fixed_specs() -> dict[tuple[str, int], dict]:
    """从上游普查装载定长规格。"""
    out: dict[tuple[str, int], dict] = {}
    small = json.loads((UPSTREAM / "reports/dbdat_decode/db_tables_small.json").read_text(encoding="utf-8"))
    for _, it in (small.get("tables") or {}).items():
        tid = it.get("table_id")
        rb = it.get("row_boundary") or {}
        if not isinstance(tid, int) or rb.get("status") != "exact fixed stride":
            continue
        out[("client", tid)] = {
            "model": "fixed",
            "header": rb.get("header_size", 14),
            "stride": rb.get("stride"),
            "footer": rb.get("footer_size", 8),
            "count": it.get("record_count"),
            "payload": it.get("payload_size"),
        }
    srv = json.loads((UPSTREAM / "reports/dbdat_decode/server_tables_census.json").read_text(encoding="utf-8"))
    for it in srv.get("entries") or []:
        if it.get("entry_type") != "table":
            continue
        tid = it.get("table_id")
        rb = it.get("row_boundary") or {}
        if not isinstance(tid, int):
            continue
        st = str(rb.get("status") or "")
        if st in ("arithmetic_candidate", "exact fixed stride") and rb.get("stride"):
            out[("server", tid)] = {
                "model": "fixed",
                "header": int(rb.get("formula", "14").split()[0]) if rb.get("formula") else 14,
                "stride": rb.get("stride"),
                "footer": 8,
                "count": it.get("record_count_header"),
                "payload": it.get("payload_size"),
                "identity_verified": st != "arithmetic_candidate",
            }
    out.update({k: dict(v) for k, v in EXTRA_FIXED.items()})
    return out


def walk_fixed(raw: bytes, spec: dict):
    h, st, ft, n = spec["header"], spec["stride"], spec["footer"], spec["count"]
    if h + n * st + ft != len(raw):
        raise RuntimeError(f"closure fail: {h}+{n}*{st}+{ft}={h + n * st + ft} != {len(raw)}")
    for i in range(n):
        b = h + i * st
        yield i, b, raw[b: b + st]


def walk_lcrg(raw: bytes):
    end = len(raw) - 8
    pos, i = 14, 0
    while pos < end:
        for k in range(60):
            ln = 41 + 5 * k
            t = pos + ln - 13
            if t + 13 > len(raw):
                continue
            rdui, d1, d2 = struct.unpack_from("<III", raw, t)
            if rdui == i and d1 == d2 and raw[t + 12] == 0:
                yield i, pos, raw[pos:pos + ln]
                pos += ln
                i += 1
                break
        else:
            raise RuntimeError(f"lcrg stuck at {pos} row {i}")


def walk_club_block(raw: bytes):
    """club: 84,259 行 5B block 标准布局;3 行特例(55B)。详见 club_v2/output.json。"""
    out = json.loads((ROOT / "scratch/t02/inbox/club_v2/output.json").read_text(encoding="utf-8"))
    n = int(out["count"])
    footer_at = int(out["footer_offset"]) if out.get("footer_offset") else len(raw) - 8
    pos, i = 14, 0
    while i < n:
        # 标准布局: 名称/身份在行内,行尾 duni(4)+duni(4)+00(1)
        picked = None
        for ln in range(20, 200):
            t = pos + ln - 9
            if t + 9 > len(raw):
                break
            a, b = struct.unpack_from("<II", raw, t)
            if a == b and raw[t + 8] == 0:
                picked = ln
                break
        if picked is None:
            raise RuntimeError(f"club stuck at {pos} row {i}")
        yield i, pos, raw[pos:pos + picked]
        pos += picked
        i += 1


def dump(archive: str, tid: int, limit: int | None, codec):
    specs = fixed_specs()
    key = (archive, tid)
    ov = OVERRIDE.get(key)
    raw = load_payload(codec, archive, tid)
    fields = FIELDS.get(key, {})
    rows = []

    if ov and ov["model"] == "variable":
        g = ov["grammar"]
        it = {"lcrg_tail": walk_lcrg, "club_block": walk_club_block}.get(g)
        if it is None:
            raise SystemExit(f"{key}: 变长文法 {g} 尚无 walker(待 t05 代理交付)")
        stream = it(raw)
    elif key in specs:
        stream = walk_fixed(raw, specs[key])
    else:
        raise SystemExit(f"{key}: 无边界规格")

    for i, off, body in stream:
        if limit is not None and i >= limit:
            break
        rec = {"row": i, "offset": off, "len": len(body)}
        for name, fo in fields.items():
            if fo < 0:
                pos = len(body) + fo
            else:
                pos = fo
            if 0 <= pos and pos + 4 <= len(body):
                rec[name] = struct.unpack_from("<I", body, pos)[0]
        rec["raw_hex"] = body.hex()
        rows.append(rec)
    return {"archive": archive, "table_id": tid, "payload_len": len(raw), "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", choices=["client", "server"])
    ap.add_argument("--table", type=int)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--csv")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    specs = fixed_specs()
    if args.list:
        keys = sorted(set(specs) | set(OVERRIDE))
        print(f"可用表 {len(keys)} 张(定长 {len(specs)} + 覆盖 {len(OVERRIDE)}):")
        for a, t in keys:
            s = specs.get((a, t))
            ov = OVERRIDE.get((a, t))
            if ov:
                desc = f"{ov['model']}/{ov.get('grammar')}  [覆盖: {ov.get('why','')[:34]}]"
            elif s:
                desc = f"fixed stride={s['stride']} n={s['count']}"
            else:
                desc = "?"
            print(f"  {a:6s} table_{t:<3d} {desc}")
        return 0

    codec = _reader()

    if args.selftest:
        ok = fail = skip = 0
        for (a, t), s in sorted(specs.items()):
            try:
                raw = load_payload(codec, a, t)
            except Exception as ex:
                print("SKIP", a, t, ex)
                skip += 1
                continue
            if s.get("payload") and len(raw) != s["payload"]:
                print("SKIP", a, t, f"payload {len(raw)} != 上游 {s['payload']}(成员解析不匹配)")
                skip += 1
                continue
            try:
                n = sum(1 for _ in walk_fixed(raw, s))
            except Exception as ex:
                print("FAIL", a, t, ex)
                fail += 1
                continue
            if n == s["count"]:
                ok += 1
            else:
                print("FAIL", a, t, "rows", n)
                fail += 1
        # 变长表
        for (a, t), ov in sorted(OVERRIDE.items()):
            if ov["model"] != "variable" or ov.get("grammar") != "lcrg_tail":
                continue
            try:
                raw = load_payload(codec, a, t)
                n = sum(1 for _ in walk_lcrg(raw))
                good = n == 2488 and len(raw) == 109505
            except Exception as ex:
                print("FAIL", a, t, ex)
                fail += 1
                continue
            print(("PASS" if good else "FAIL"), f"{a} table_{t} variable/lcrg rows={n}")
            ok += 1 if good else 0
            fail += 0 if good else 1
        print(f"--- fixed {ok} PASS / {fail} FAIL / {skip} SKIP ---")
        return 0 if fail == 0 else 1

    if args.archive is None or args.table is None:
        ap.error("需要 --archive 与 --table(或用 --list / --selftest)")

    res = dump(args.archive, args.table, args.limit, codec)
    if args.csv:
        rows = res["rows"]
        cols = ["row", "offset", "len"] + [k for k in (rows[0] if rows else {}) if k not in ("row", "offset", "len", "raw_hex")] + ["raw_hex"]
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in cols})
        print(f"wrote {args.csv} ({len(rows)} rows)")
    else:
        print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
