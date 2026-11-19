#!/usr/bin/env python3
"""dspot_an — t15d 逐表字段级判读辅助(只读)。

在 dspot.py 已确认 `14 + n*stride + 8` 闭合 + 尾 13 B 固定尾的前提下,做三件事:

1. `grid`:对 lead 区(0..stride-13)按 width 1..4 全偏移扫,输出"有语义信号"的列
   (常量 / 行序 / 年份 / 枚举≤64 / 与前一 4B 字段完全同值 / 金额样 / ID 贴界)。
2. `hex`:打印前若干行 + 任意行的逐字节偏移视图(人读布局)。
3. `fk`:对指定列做真实集合交集——person_duni_all.npy(646,979 个真实 duni)
   与 person_uid_all.npy(0..658,010);这是超出"值域 < base"的独立检验。

E42:交集比例只报数,不据此升降实体裁决。

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot_an.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot_an.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot_an.py grid --table 34
  py -V:3.12 -I -B scratch/t15d/out/dspot_an.py hex --table 34 --rows 0:3
  py -V:3.12 -I -B scratch/t15d/out/dspot_an.py fk --table 42 --off 0 --w 4

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

BASES = D.BASES
TAIL = 13


def _sets() -> dict:
    if "s" not in _sets.__dict__:
        s = {}
        for name in ("person_duni_all", "person_uid_all", "person_duni"):
            p = ROOT / f"scratch/t15/out/{name}.npy"
            s[name] = np.load(p) if p.exists() else None
        _sets.s = s
    return _sets.s


def grid(tid: int, maxw: int = 4) -> list[dict]:
    raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    lead = stride - TAIL
    out = []
    for off in range(lead):
        for w in range(1, maxw + 1):
            if off + w > lead:
                continue
            c = D.col(raw, stride, n, off, w)
            v = np.unique(c)
            d, mn, mx = int(v.size), int(v[0]), int(v[-1])
            sig = []
            if d == 1:
                sig.append(f"const={mn}")
            if d == n and mn == 0:
                sig.append("ord0")
            if d == n and mn == 1:
                sig.append("ord1")
            if 5 <= d <= 80 and mn >= 1900 and mx <= 2100:
                sig.append(f"YEAR[{mn}..{mx}]")
            if 2 <= d <= 64 and mx - mn + 1 == d:
                sig.append(f"enum{d}")
            if d >= 2 and mx <= 366 and w <= 2:
                sig.append(f"day?[{mn}..{mx}]")
            # 与下一个 4B 字段同值(重复对)
            if w == 4 and off + 8 <= lead:
                c2 = D.col(raw, stride, n, off + 4, 4)
                if bool((c == c2).all()):
                    sig.append("DUP@+4")
                elif float((c == c2).mean()) > 0.98:
                    sig.append(f"DUP@+4[{float((c == c2).mean()):.3f}]")
            # 金额样:1e3..1e11 且 1000 整除率高、离散度高
            if d > 20 and 1000 <= mx <= 10 ** 11:
                big = c[c > 0]
                if big.size and float((big % 1000 == 0).mean()) > 0.5:
                    sig.append("money/k1000")
                elif big.size and float((big % 100 == 0).mean()) > 0.9:
                    sig.append("money/k100")
            # ID 贴界
            if d > 3 and mx > 0:
                for name, B in sorted(BASES.items(), key=lambda kv: kv[1]):
                    if mx < B:
                        ratio = mx / B
                        if ratio > 0.05:
                            sig.append(f"<{name} {mx}/{B}={ratio:.3f}")
                        break
            if sig:
                out.append({"off": off, "w": w, "d": d, "min": mn, "max": mx,
                            "zero": round(float((c == 0).mean()), 3),
                            "sig": sig, "top": [int(x) for x in v[:5]]})
    return out


def hexrows(tid: int, rows: str) -> list[str]:
    raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    a, _, b = rows.partition(":")
    lo = int(a)
    hi = min(int(b) if b else lo + 1, n)
    lines = []
    for i in range(lo, hi):
        r = raw[14 + i * stride: 14 + (i + 1) * stride]
        lines.append(f"r{i:<6} " + " ".join(f"{x:02x}" for x in r))
    return lines


def fk(tid: int, off: int, w: int) -> dict:
    raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    c = D.col(raw, stride, n, off, w).astype(np.int64)
    s = _sets()
    out = {"table": tid, "off": off, "w": w, "d": int(np.unique(c).size),
           "min": int(c.min()), "max": int(c.max())}
    duni = s.get("person_duni_all")
    if duni is not None:
        ds = np.unique(duni)
        ok = np.isin(c, ds)
        out["person_duni_exact"] = {"rows_hit": round(float(ok.mean()), 4),
                                    "distinct_hit": int(np.unique(c[ok]).size),
                                    "distinct_hit_of_table": round(
                                        float(np.unique(c[ok]).size / max(1, np.unique(c).size)), 4)}
    uid = s.get("person_uid_all")
    if uid is not None:
        us = np.unique(uid)
        ok2 = np.isin(c, us)
        out["person_uid_exact"] = {"rows_hit": round(float(ok2.mean()), 4)}
    return out


def selftest() -> int:
    ok = True
    for tid in sorted(D.SPEC):
        raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
        c4 = D.col(raw, stride, n, stride - TAIL, 4)
        b = np.frombuffer(raw, dtype=np.uint8)[14 + stride - 1: 14 + stride - 1 + n * stride: stride]
        # 尾 13 B 首 u32 恒等于 0-based 行序,末字节恒 0(t34/t37 中间两个 u32 是组内计数,
        # 其余表是 ord+1 的复制,不作为判据)
        good = bool((c4 == np.arange(n)).all()) and bool((b == 0).all())
        if not good:
            print(f"FAIL tail t{tid}")
            ok = False
    print("selftest:", "ok" if ok else "MISMATCH", "(tail 13B starts with row ordinal, ends with 0)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t15d 字段级判读辅助(只读)")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("grid")
    g.add_argument("--table", type=int, required=True)
    g.add_argument("--maxw", type=int, default=4)
    h = sub.add_parser("hex")
    h.add_argument("--table", type=int, required=True)
    h.add_argument("--rows", default="0:3")
    f = sub.add_parser("fk")
    f.add_argument("--table", type=int, required=True)
    f.add_argument("--off", type=int, required=True)
    f.add_argument("--w", type=int, default=4)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "grid":
        for r in grid(a.table, a.maxw):
            print(f"  @{r['off']:<3}w{r['w']} d={r['d']:<6} min={r['min']:<12} max={r['max']:<12} "
                  f"z={r['zero']:<5} {';'.join(r['sig'])}  top={r['top']}")
        return 0
    if a.cmd == "hex":
        print("\n".join(hexrows(a.table, a.rows)))
        return 0
    if a.cmd == "fk":
        print(json.dumps(fk(a.table, a.off, a.w), ensure_ascii=False))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
