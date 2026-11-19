#!/usr/bin/env python3
"""dspot_ids — t15d:构建 club/team/comp 的真实 ID 集合(只读)。

动机:12 张抽查表里大量列是 4B/2B 的"看起来像 ID"的整数。用值域 < base 判命中
毫无鉴别力(E42),必须用**真实集合成员**才能算 lift。

集合来源(全部只读、可复算):
  comp  —— server table 25, straight-line 7047 x ?;用 t14 D 锚已定的 comp 主表,
           取首列 u32 作为 comp id 集合(需闭合校验)。
  club  —— server table 3,前 69,705 行 4B 首列(db_id)已由
           scratch/t02/club_partial.json 逐行验证;取该区间的 u32@0。
  team  —— server table 24 边界未闭合(COVERAGE 明确写"未建立"),不构建,
           只在报告里标 unavailable。

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot_ids.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot_ids.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot_ids.py --build --json scratch/t15d/out/idset.json

退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15d/out"
sys.path.insert(0, str(OUTDIR))
import dspot as D  # noqa: E402

CACHE = ROOT / "scratch/t15d/out/idset"


def comp_set() -> dict:
    """t25 是 straight-line 7047 行;stride 由 payload 求。"""
    raw = D.payload(25)
    n = D.SPEC.get(25, (7047, None))[0]
    stride = (len(raw) - 22) // 7047
    assert 14 + 7047 * stride + 8 == len(raw), f"t25 closure {len(raw)} stride {stride}"
    c = D.col(raw, stride, 7047, 0, 4).astype(np.int64)
    return {"n": 7047, "stride": stride, "d": int(np.unique(c).size),
            "min": int(c.min()), "max": int(c.max()), "vals": np.unique(c)}


def club_set() -> dict:
    """t3 变长;只用 club_partial.json 已验证的 69,705 行 4B 首列。"""
    part = json.loads((ROOT / "scratch/t02/club_partial.json").read_text(encoding="utf-8"))
    verified = int(part["row_framework"]["verified_rows"])
    raw = D.payload(3)
    # 首列固定 4B @0,前 verified 行的行起点需逐行推:用 club_partial 的 row_offset_map
    # 若拿不到行长,退化为"从 payload 头部按 4B 步长取前 verified 个"——不采用。
    # 这里只调用上游已给出的 samples(若存在),否则返回 unavailable。
    samples = part.get("samples") or []
    ids = [s.get("db_id") for s in samples if isinstance(s, dict) and isinstance(s.get("db_id"), int)]
    if len(ids) < 50:
        return {"status": "unavailable", "why": "club_partial.json 未给足 db_id 样本",
                "verified_rows": verified, "payload": len(raw)}
    return {"status": "partial", "n": len(ids), "vals": np.unique(np.array(ids, dtype=np.int64))}


def build() -> dict:
    out = {}
    CACHE.mkdir(parents=True, exist_ok=True)
    try:
        c = comp_set()
        np.save(CACHE / "comp.npy", c.pop("vals"))
        out["comp"] = c
    except Exception as e:  # noqa: BLE001
        out["comp"] = {"status": "error", "err": str(e)}
    try:
        cl = club_set()
        if "vals" in cl:
            np.save(CACHE / "club.npy", cl.pop("vals"))
        out["club"] = cl
    except Exception as e:  # noqa: BLE001
        out["club"] = {"status": "error", "err": str(e)}
    out["team"] = {"status": "unavailable",
                   "why": "server t24 行边界未闭合(COVERAGE: 未建立)"}
    return out


def selftest() -> int:
    ok = True
    r = build()
    c = r.get("comp") or {}
    if c.get("status") in ("error",) or "n" not in c:
        print("FAIL comp set:", c)
        ok = False
    else:
        print(f"  comp: n={c['n']} stride={c['stride']} distinct={c['d']} "
              f"range=[{c['min']}..{c['max']}] (base 7047)")
        if not (c["d"] <= 7047 and c["max"] < 7047):
            print("FAIL comp id set 未落在 [0,7047)")
            ok = False
    print("  club:", {k: v for k, v in (r.get("club") or {}).items()})
    print("selftest:", "ok" if ok else "MISMATCH")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t15d 真实 ID 集合构建(只读)")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.build:
        ap.print_help()
        return 2
    r = build()
    text = json.dumps(r, ensure_ascii=False, indent=1, default=str)
    if a.json:
        a.json.write_text(text, encoding="utf-8")
        print(f"json: {a.json}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
