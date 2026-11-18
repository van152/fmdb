#!/usr/bin/env python3
"""t05 — 行内字节列画像:为字段映射提供数据侧证据。

对一张已解析边界的表,按行内偏移统计每个字节/字宽的解释特征,
帮助判断"这个偏移像什么类型":

  constant      所有行同值(常量/填充)
  zero_ratio    为 0 的行占比
  ff_ratio      为 0xFF(u8)/0xFFFFFFFF(u32) 的占比(空引用特征)
  distinct      唯一值个数
  min/max       数值范围(u8/u16/u32/float32 四种解释)
  monotonic     u32 解释下单调不降的行占比(序号/ID 特征)
  ref_lt_N      值 < N 的占比(引用目标表行数特征)

用法:
  py -V:3.12 -I -B scripts/t05_profile.py --archive client --table 0 \
      --width 77 --header 14 --count 3545 [--refN 56293] [--json out.json]
  py -V:3.12 -I -B scripts/t05_profile.py --archive client --table 0 --auto --refN 56293
"""
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("dmp", ROOT / "scripts/fm24_dump.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rows_of(dmp, archive: str, tid: int, width: int | None):
    import runpy
    codec = dmp._reader()
    specs = dmp.fixed_specs()
    key = (archive, tid)
    raw = dmp.load_payload(codec, archive, tid)
    if width is None:
        s = specs.get(key)
        if not s:
            raise SystemExit(f"{key} 无定长规格,请显式给 --width/--header/--count")
        yield from dmp.walk_fixed(raw, s)
        return
    h = dmp.OVERRIDE.get(key, {}).get("header", 14)
    n = (len(raw) - h - 8) // width
    for i in range(n):
        b = h + i * width
        yield i, b, raw[b:b + width]


def profile(rows, width: int, refN: int | None) -> list[dict]:
    cols: list[dict] = []
    data = [body for _, _, body in rows]
    n = len(data)
    for off in range(width):
        u8 = [r[off] for r in data]
        const = len(set(u8)) == 1
        d: dict = {
            "offset": off,
            "constant": u8[0] if const else None,
            "zero_ratio": round(sum(1 for v in u8 if v == 0) / n, 4),
            "ff_ratio_u8": round(sum(1 for v in u8 if v == 0xFF) / n, 4),
            "distinct_u8": len(set(u8)),
            "min_u8": min(u8), "max_u8": max(u8),
        }
        if off + 2 <= width:
            u16 = [struct.unpack_from("<H", r, off)[0] for r in data]
            d["u16"] = {"distinct": len(set(u16)), "min": min(u16), "max": max(u16),
                        "ff_ratio": round(sum(1 for v in u16 if v == 0xFFFF) / n, 4)}
        if off + 4 <= width:
            u32 = [struct.unpack_from("<I", r, off)[0] for r in data]
            mono = sum(1 for a, b in zip(u32, u32[1:]) if b >= a)
            f32 = [struct.unpack_from("<f", r, off)[0] for r in data]
            fin = [v for v in f32 if v == v and abs(v) != float("inf")]
            d["u32"] = {
                "distinct": len(set(u32)), "min": min(u32), "max": max(u32),
                "ff_ratio": round(sum(1 for v in u32 if v == 0xFFFFFFFF) / n, 4),
                "monotonic": round(mono / max(1, n - 1), 3),
            }
            if refN:
                d["u32"]["ref_lt_N"] = round(sum(1 for v in u32 if v < refN) / n, 4)
            if fin and all(abs(v) < 1e12 for v in fin):
                d["f32"] = {"min": round(min(fin), 4), "max": round(max(fin), 4),
                            "finite_ratio": round(len(fin) / n, 4)}
        cols.append(d)
    return cols


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True, choices=["client", "server"])
    ap.add_argument("--table", type=int, required=True)
    ap.add_argument("--width", type=int)
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--refN", type=int)
    ap.add_argument("--json")
    ap.add_argument("--limit", type=int, default=0, help="只统计前 N 行(0=全量)")
    args = ap.parse_args()

    dmp = load_module()
    rows = list(rows_of(dmp, args.archive, args.table, args.width if not args.auto else None))
    if args.limit:
        rows = rows[:args.limit]
    width = len(rows[0][2])
    cols = profile(rows, width, args.refN)

    print(f"{args.archive} table_{args.table}: {len(rows)} 行 × {width} B")
    print(f"{'off':>4} {'const':>5} {'zero%':>6} {'ff8%':>6} {'dist8':>6} "
          f"{'u32min':>10} {'u32max':>10} {'ff32%':>6} {'mono':>5} {'refN%':>6}  flags")
    for c in cols:
        u = c.get("u32") or {}
        flags = []
        if c["constant"] is not None:
            flags.append(f"CONST={c['constant']:#04x}")
        if u.get("monotonic", 0) > 0.98:
            flags.append("MONO")
        if u.get("ff_ratio", 0) > 0.5:
            flags.append("NULLREF")
        if u.get("ref_lt_N", 0) > 0.98 and u.get("distinct", 0) > 8:
            flags.append(f"REF<{args.refN}")
        print(f"{c['offset']:>4} {str(c['constant']):>5} {c['zero_ratio']:>6.3f} "
              f"{c['ff_ratio_u8']:>6.3f} {c['distinct_u8']:>6} "
              f"{u.get('min', '-'):>10} {u.get('max', '-'):>10} "
              f"{u.get('ff_ratio', 0):>6.3f} {u.get('monotonic', 0):>5.2f} "
              f"{u.get('ref_lt_N', 0):>6.3f}  {' '.join(flags)}")

    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps({"archive": args.archive, "table_id": args.table, "rows": len(rows),
                        "width": width, "columns": cols}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print("wrote", args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
