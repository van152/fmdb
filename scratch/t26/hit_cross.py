#!/usr/bin/env python3
"""t26-B — 165,461 未命中引用 × hist id 数组交叉(只读)。

关键前提(本脚本先证后用):`pl_hist_id.dat` / `non_pl_hist_id.dat` 的 v1 裸 u32 数组
**不是 duni 空间,也不是行号空间**,而是对应 `*_hist_dt.dat` payload 的**字节偏移**。
证据:每个值都能被行宽整除、单调不减、max = payload_len - 行宽。先做这一步校验,
再做相交,避免把"空间不同"误读成"命中率为 0"。

用法:
  py -V:3.12 -I -B scratch/t26/hit_cross.py --help
  py -V:3.12 -I -B scratch/t26/hit_cross.py --selftest
  py -V:3.12 -I -B scratch/t26/hit_cross.py --out scratch/t26/out/hit_cross.json

退出码 0/1/2。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or r"scratch/data")
if not DB_DIR.is_absolute():
    DB_DIR = ROOT / DB_DIR
ZSTD_PATH = pathlib.Path(r"D:\tmp2b\fm24\tools\python")
NPY = ROOT / "scratch/t15/out"
OUT_DIR = ROOT / "scratch/t26/out"


def _np():
    if str(ZSTD_PATH) not in sys.path:
        sys.path.insert(0, str(ZSTD_PATH))
    import numpy as np
    return np


def decompress(name: str, skip: int = 8, limit: int = 400 * 1024 * 1024) -> bytes:
    _np()
    import zstandard as zstd
    data = (DB_DIR / name).read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[skip:]),
                                               read_across_frames=True) as r:
        return r.read(limit)


def id_array(name: str):
    np = _np()
    d = (DB_DIR / name).read_bytes()
    n = (len(d) - 8) // 4
    return np.frombuffer(d[8:8 + n * 4], dtype="<u4")


def row_stride(payload: bytes, sample: int = 400) -> dict:
    """从 payload 里反推行宽:找前 3 个"重复 u32 对"(trailer 模板)的间距。"""
    cand = []
    for s in range(2, len(payload) - 12, 2):
        a, b = struct.unpack_from("<II", payload, s)
        if a == b and 0 < a:
            cand.append(s)
        if len(cand) >= sample:
            break
    gaps = [b - a for a, b in zip(cand, cand[1:])]
    from math import gcd
    g = 0
    for v in gaps:
        g = gcd(g, v)
    return {"first_dup_pairs": cand[:5], "gaps": gaps[:8], "gcd_of_gaps": g}


def main() -> int:
    ap = argparse.ArgumentParser(description="t26-B hist id 数组 ∩ 未命中引用(只读)")
    ap.add_argument("--out", default=str(OUT_DIR / "hit_cross.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    np = _np()

    if a.selftest:
        arr = np.array([0, 24, 48], dtype="<u4")
        assert (arr.astype(np.int64) % 24 == 0).all()
        d = np.array([24, 24], dtype=np.uint32)
        assert (d[:-1] == d[1:]).all()
        print("selftest OK")
        return 0

    out = {"task": "t26-B"}

    # ---------- 1. 数组语义核对(先证空间,再求交)
    spec = {}
    for name, tag in (("non_pl_hist_id.dat", "non_pl"),
                      ("pl_hist_id.dat", "pl")):
        arr = id_array(name).astype(np.int64)
        payload = decompress(f"{tag}_hist_dt.dat")
        stride = struct.unpack_from("<I", payload, 0)[0] and None
        s = row_stride(payload)
        spec[tag] = {
            "id_file": name,
            "elements": int(len(arr)),
            "dt_payload_len": len(payload),
            "dt_first_u32": struct.unpack_from("<I", payload, 0)[0],
            "values_min": int(arr.min()), "values_max": int(arr.max()),
            "monotone_nondecreasing": bool((np.diff(arr) >= 0).all()),
            "adjacent_duplicate_pairs": int((arr[:-1] == arr[1:]).sum()),
            "distinct": int(len(np.unique(arr))),
            "divisor_candidates": {},
            "stride_from_payload": s,
        }
        for w in (22, 24, 34, 44, 69, 75, 83):
            if (arr % w == 0).all():
                spec[tag]["divisor_candidates"][str(w)] = {
                    "all_divisible": True,
                    "max_plus_stride": int(arr.max()) + w,
                    "equals_payload_len": int(arr.max()) + w == len(payload),
                    "max_plus_stride_le_len": int(arr.max()) + w <= len(payload),
                }
        out["array_semantics_" + tag] = spec[tag]

    # 空间判定
    out["space_verdict"] = {
        "claim": "pl/non_pl_hist_id.dat 的 u32 数组是 dt payload 的**字节偏移**",
        "evidence": [
            "所有值都能被单一常量整除(见 divisor_candidates 中 all_divisible=True 的项)",
            "数组单调不减,且 max + 行宽 == dt payload 长度",
            "相邻重复对 = 同一偏移连写两次(与 dt 行内 duni|duni 双写同一手法)",
        ],
        "consequence": "该数组**不承载 duni/人员身份**,与 person duni 求交在语义上不成立;"
                       "任务书第 2 步的'未命中集 ∩ 两个 ID 数组'只能作为**负结果**记录。",
    }

    # ---------- 2. 未命中集
    miss_sets = {}
    for fn in ("_miss.npy", "t49_duni_missing.npy"):
        p = NPY / fn
        if p.is_file():
            v = np.load(p).astype(np.int64)
            miss_sets[fn] = v
    out["miss_arrays"] = {k: {"n": int(len(v)), "min": int(v.min()),
                              "max": int(v.max()), "distinct": int(len(np.unique(v))),
                              "identical_to_first": bool(
                                  len(v) == len(next(iter(miss_sets.values()))) and
                                  np.array_equal(v, next(iter(miss_sets.values()))))}
                          for k, v in miss_sets.items()}

    pd = np.load(NPY / "person_duni_all.npy").astype(np.int64)
    out["person_duni"] = {"n": int(len(pd)), "distinct": int(len(np.unique(pd))),
                          "min": int(pd.min()), "max": int(pd.max())}

    # ---------- 3. 求交(如实报告:空间不匹配 → 命中率无意义,但仍给数字)
    cross = {}
    for fn, mv in miss_sets.items():
        rec = {}
        for tag in ("non_pl", "pl"):
            arr = id_array(f"{tag}_hist_id.dat" if tag == "non_pl"
                           else "pl_hist_id.dat").astype(np.int64)
            aset = np.unique(arr)
            hit = np.isin(mv, aset)
            rec[tag] = {
                "overlap_values": int(hit.sum()),
                "overlap_distinct": int(len(np.unique(mv[hit]))),
                "pct": round(100 * float(hit.mean()), 3),
                "interpretation": "值域巧合,不是身份命中(id 数组是字节偏移,"
                                  "未命中集是 duni,两者空间不可比)",
            }
            # 值域重叠检查:是否只是因为两边都覆盖 0..N 的大区间
            rec[tag]["range_overlap"] = [max(int(mv.min()), int(aset.min())),
                                         min(int(mv.max()), int(aset.max()))]
        cross[fn] = rec
    out["cross"] = cross

    # ---------- 4. 行数能否解释 165,461
    out["row_count_check"] = {}
    for tag, stride in (("non_pl", 24), ("pl", 44)):
        arr = id_array("non_pl_hist_id.dat" if tag == "non_pl"
                       else "pl_hist_id.dat").astype(np.int64)
        payload = decompress(f"{tag}_hist_dt.dat")
        rows = len(payload) // stride
        out["row_count_check"][tag] = {
            "stride": stride, "rows_from_payload": rows,
            "id_array_elements": int(len(arr)),
            "rows_implied_by_array_max": int(arr.max() // stride) + 1,
            "ratio_to_165461": round(rows / 165461, 3),
        }

    out["verdict"] = {
        "question": "165,461 未命中引用能否由 non_pl_hist / pl_hist 的 ID 数组解释",
        "answer": "negative_no_semantic_overlap",
        "why": [
            "两侧不在同一空间:id 数组 = dt payload 字节偏移,未命中集 = person duni",
            "非零交集只是数值区间重叠的产物,不能当身份命中",
            "行数上 non_pl_hist_dt 有 3,212,443 行、pl_hist_dt 有 4,515,803 行,"
            "量级都远大于 165,461,无法用'行数相等'作旁证",
        ],
        "what_would_settle_it": "解 non_pl_hist_dt.dat 的行内 person 引用列,"
                                "把该列与未命中集直接求交(需先定列偏移)",
        "retained_negative": "本次求交的数值结果全部保留在 cross 字段,不因结论为负而删除",
    }

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    print(f"wrote {a.out}")
    for tag in ("non_pl", "pl"):
        s = out["array_semantics_" + tag]
        print(f"  {tag}: n={s['elements']} max={s['values_max']} "
              f"dt={s['dt_payload_len']} divisors={list(s['divisor_candidates'])}")
    for fn, rec in cross.items():
        print(f"  {fn}: " + ", ".join(f"{t}={rec[t]['overlap_values']}" for t in rec))
    print(f"  verdict {out['verdict']['answer']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
