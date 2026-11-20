#!/usr/bin/env python3
"""t05 — 生成夹具真值文件(fixtures_truth.json):给对齐器的硬约束。

对每个夹具表:
  * 精确 closure 等式
  * 已验锚点(偏移/宽度/期望值)
  * 3 条样例行的 hex + 锚点实际值(便于逐字节对照)
  * 身份槽验证率(全表扫描)

用法:
  py -V:3.12 -I -B scripts/t05_fixtures_truth.py
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t05/fixtures_truth.json"

# (archive, tid, 名称, 锚点{field:(offset,width)}, 特殊检查)
FIXTURES = [
    ("client", 0, "award", {"rdui": (64, 4), "duni_lo": (68, 4), "duni_hi": (72, 4)},
     {"marker_offset": 76, "marker_expect": 0}),
    ("client", 2, "city", {"Clat": (1, 4), "Clon": (5, 4), "Cnti": (10, 1),
                           "rdui": (30, 4), "duni_lo": (34, 4), "duni_hi": (38, 4)},
     {"named_rows": {"Liverpool": (1061, {"rdui": 1061, "Cnti": 139, "duni_lo": 100047}),
                     "Manchester": (1075, {"rdui": 1075, "Cnti": 139, "duni_lo": 100062}),
                     "Madrid": (316, {"rdui": 316, "Cnti": 170, "duni_lo": 341}),
                     "München": (540, {"rdui": 540, "Cnti": 145, "duni_lo": 592})}}),
    ("client", 21, "stadium", {"Scti": (3, 4), "Slat": (17, 4), "Slon": (21, 4),
                               "rdui": (25, 4), "duni_lo": (29, 4), "duni_hi": (33, 4)},
     {"note": "client 38B;server 181B 的前 38B 与之逐字节相同"}),
    ("client", 6, "injury", {"rdui": (3, 4), "duni_lo": (7, 4), "duni_hi": (11, 4)},
     {"marker_offset": 15, "marker_expect": 0}),
]


def load_dmp():
    spec = importlib.util.spec_from_file_location("dmp", ROOT / "scripts/fm24_dump.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rows_iter(raw: bytes, h: int, stride: int, count: int):
    for i in range(count):
        b = h + i * stride
        yield i, raw[b:b + stride]


def main() -> int:
    dmp = load_dmp()
    codec = dmp._reader()
    specs = dmp.fixed_specs()
    out = {"generated_by": "scripts/t05_fixtures_truth.py",
           "note": "所有锚点均由指挥官独立逐字节验证;对齐器必须复现这些偏移与值。",
           "fixtures": []}

    for archive, tid, name, anchors, extra in FIXTURES:
        s = specs[(archive, tid)]
        raw = dmp.load_payload(codec, archive, tid)
        h, st, n = s["header"], s["stride"], s["count"]
        assert h + n * st + 8 == len(raw), (name, "closure")
        body_rows = list(rows_iter(raw, h, st, n))

        # 身份验证率
        ok_rdui = sum(1 for i, r in body_rows
                      if struct.unpack_from("<I", r, anchors["rdui"][0])[0] == i)
        ok_duni = sum(1 for i, r in body_rows
                      if struct.unpack_from("<I", r, anchors["duni_lo"][0])[0]
                      == struct.unpack_from("<I", r, anchors["duni_hi"][0])[0])

        samples = []
        for idx in (0, 1, 2):
            r = body_rows[idx][1]
            rec = {"row": idx, "hex": r.hex()}
            for fld, (off, w) in anchors.items():
                if w == 4:
                    rec[fld] = struct.unpack_from("<I", r, off)[0]
                elif w == 1:
                    rec[fld] = r[off]
            if "marker_offset" in extra:
                rec["marker"] = r[extra["marker_offset"]]
            samples.append(rec)

        named = []
        for label, (idx, exp) in (extra.get("named_rows") or {}).items():
            r = body_rows[idx][1]
            got = {}
            for fld, ev in exp.items():
                off, w = anchors[fld]
                got[fld] = struct.unpack_from("<I", r, off)[0] if w == 4 else r[off]
            named.append({"label": label, "row": idx,
                          "expected": exp, "actual": got,
                          "match": all(got[k] == v for k, v in exp.items())})

        out["fixtures"].append({
            "archive": archive, "table_id": tid, "name": name,
            "count": n, "payload_len": len(raw), "stride": st, "header": h,
            "closure": f"{h} + {n}*{st} + 8 = {len(raw)}",
            "anchors": {k: {"offset": v[0], "width": v[1]} for k, v in anchors.items()},
            "identity": {"rdui_equals_row_index": f"{ok_rdui}/{n}",
                         "duni_repeated": f"{ok_duni}/{n}"},
            "extra": extra, "samples": samples, "named_rows_check": named,
        })
        print(f"{name:<10} {n:>6} rows  closure OK  rdui {ok_rdui}/{n}  duni {ok_duni}/{n}"
              + ("  named_rows ALL MATCH" if named and all(x["match"] for x in named) else ""))

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
