#!/usr/bin/env python3
"""dspot_fk — t15d:对 12 张 D-锚-only 表做真实集合交集的人/俱乐部身份检验(只读)。

与 t15 的"值域 < base"不同,这里用**真实集合**:
  * person_duni_all.npy — 646,979 个 person 的 duni(真实存在的 ID 值)
  * person_uid_all.npy  — 0..658,010 全体 ordinal
  * person_ids.npy      — 657,788 个 person 的 id 列
行集命中率 + distinct 命中率 + 单调性,三者一起看。

E42:命中率只报数;不据此升降实体裁决。

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot_fk.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot_fk.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot_fk.py --all
  py -V:3.12 -I -B scratch/t15d/out/dspot_fk.py --table 42 --min 0.5

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

TAIL = 13
SETS: dict[str, np.ndarray] = {}


def sets() -> dict[str, np.ndarray]:
    if not SETS:
        for name in ("person_duni_all", "person_uid_all", "person_ids"):
            p = ROOT / f"scratch/t15/out/{name}.npy"
            SETS[name] = np.unique(np.load(p).astype(np.int64))
    return SETS


def sweep(tid: int, maxw: int = 4, thresh: float = 0.5) -> list[dict]:
    """只把 person_duni 当行集;并计算"小整数白拿"的轴线。

    E42: duni 最小值是 3、1% 分位是 140,270,所以任何 < 1e5 的窄列都会白拿一截命中。
    因此额外报 `artifact`:若列值全落在一个"duni 密度"区间内,命中率可以纯靠密度凑出来。
    真正的引用证据要同时满足 rows≈1、distinct≈1、max > 1e5(或表本身是上层子表)。
    """
    raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    lead = stride - TAIL
    S = sets()
    duni = S["person_duni_all"]
    hits = []
    for off in range(lead):
        for w in range(1, maxw + 1):
            if off + w > lead:
                continue
            c = D.col(raw, stride, n, off, w).astype(np.int64)
            ok = np.isin(c, duni)
            rows = float(ok.mean())
            if rows < thresh:
                continue
            # E42 基线:把 duni 集合看作在 [0,hi] 里的稀疏点集,随机命中的概率 = |duni∩[0,hi]| / hi。
            # (不能用"集合里多少值 <= hi"——那是集合自身的累积占比, hi 一大就趋 1,毫无鉴别力)
            hi = int(c.max())
            base = float((duni <= hi).sum()) / max(1, hi)
            rec = {"off": off, "w": w, "d": int(np.unique(c).size),
                   "min": int(c.min()), "max": hi,
                   "rows": round(rows, 4),
                   "dist": round(float(np.unique(c[ok]).size / max(1, np.unique(c).size)), 4),
                   "base_density": round(base, 6),
                   "lift": round(rows / base, 1) if base > 0 else None,
                   "mono": round(float((np.diff(c) >= 0).mean()), 4) if n > 1 else 1.0}
            hits.append(rec)
    return hits


def selftest() -> int:
    ok = True
    S = sets()
    for k, v in S.items():
        if v.size < 1000:
            print(f"FAIL set {k} size {v.size}")
            ok = False
    # 正控:person 主表的 id 列必须 100% 命中自身集合(用 t42 的 duni 列已验证过)
    raw, n, stride = D.payload(42), D.SPEC[42][0], D.SPEC[42][1]
    c = D.col(raw, stride, n, 0, 4).astype(np.int64)
    frac = float(np.isin(c, S["person_duni_all"]).mean())
    print(f"  positive control t42@0 -> person_duni rows={frac:.4f}")
    if frac < 0.99:
        ok = False
    # 负控:行序号列不应命中人集合
    c2 = D.col(raw, stride, n, stride - TAIL, 4).astype(np.int64)
    f2 = float(np.isin(c2, S["person_duni_all"]).mean())
    duni = S["person_duni_all"]
    # 行序列上限 17720,该区间的 duni 点密度就是 E42 白拿基线
    base = float((duni <= 17720).sum()) / 17720
    print(f"  negative control t42@tail0 -> rows={f2:.4f}, 区间密度 baseline={base:.4f}, "
          f"lift={f2 / base:.2f} (E42:小整数列靠密度白拿,无鉴别力)")
    if f2 / base > 3:
        ok = False
    print("selftest:", "ok" if ok else "MISMATCH")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t15d 真实集合同位检验(只读)")
    ap.add_argument("--table", type=int, action="append")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--min", type=float, default=0.5, help="行命中率阈值")
    ap.add_argument("--maxw", type=int, default=4)
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    tids = sorted(D.SPEC) if a.all else (a.table or [])
    if not tids:
        ap.print_help()
        return 2
    out = {}
    for tid in tids:
        hs = sweep(tid, a.maxw, a.min)
        out[tid] = hs
        print(f"=== t{tid} {D.RTTI[tid]}  ({len(hs)} cols >= {a.min})")
        for r in hs:
            print(f"  @{r['off']:<3}w{r['w']} d={r['d']:<6} duni={r['rows']:<7} dist={r['dist']:<7} "
                  f"base={r['base_density']:<7} lift={r['lift']:<7} mono={r['mono']:<7} "
                  f"[{r['min']}..{r['max']}]")
    if a.json:
        a.json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"json: {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
