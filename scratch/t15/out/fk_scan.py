#!/usr/bin/env python3
"""fk_scan — t15 旁路数据组:逐字节偏移的 u32 列画像 + FK/值域检验。

只读:通过 scripts/fm24_dump.py 的 load_payload 取 server/client 表 payload;
本脚本只写 OUTDIR(默认 scratch/t15/out)。

用法
----
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py --help
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py --selftest
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py scan --table 26
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py scan --table 49 --stride 36 --count 792149
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py walk --table 45 --count 84477
  py -V:3.12 -I -B scratch/t15/out/fk_scan.py cols --table 49 --stride 36 --count 792149 --ncols 20

退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import runpy
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15/out"
DUMP = ROOT / "scripts/fm24_dump.py"

# 实体基数(L2 锚点,见 scratch/t13e/out/baselines.json)
BASES = {
    "comp": 7047, "club": 84259, "person": 658011, "t49rows": 792149,
    "injury": 115, "nation": 251, "city": 56293, "stadium": 48413,
    "lcrg": 2488, "team": 84507, "award": 3545, "region": 28, "stage": 278,
    "weather": 334, "lang": 126, "cont": 7, "curr": 173, "mdso": 208,
    "drbr": 1567, "t26rows": 90128, "t30rows": 72473, "t45rows": 84477,
    "t48rows": 5210, "t29rows": 13278, "t36rows": 6535, "t32rows": 315,
    "t38rows": 5241, "t39rows": 117, "t37rows": 465712,
}

_CACHE: dict[tuple[str, int], bytes] = {}


def payload(archive: str, tid: int) -> bytes:
    key = (archive, tid)
    if key not in _CACHE:
        k = runpy.run_path(str(DUMP), run_name="notmain")
        _CACHE[("__codec__", 0)] = k  # type: ignore[assignment]
        codec = k["_reader"]()
        _CACHE[key] = k["load_payload"](codec, archive, tid)
    return _CACHE[key]


def _k():
    payload("server", 26)  # ensure codec cached
    return _CACHE[("__codec__", 0)]


def u32col(raw: bytes, base: int, stride: int, n: int, off: int) -> np.ndarray:
    """取 offset=off 处的 n 个 little-endian u32(允许非 4 字节对齐)。"""
    a = np.frombuffer(raw, dtype=np.uint8)
    v = np.zeros(n, dtype=np.uint64)
    for k in range(4):
        s = a[base + off + k: base + off + k + n * stride: stride]
        v |= s.astype(np.uint64) << np.uint64(8 * k)
    return v


def colstat(c: np.ndarray, base: int = 0) -> dict:
    n = int(c.size)
    uniq = np.unique(c)
    mn, mx = int(uniq[0]), int(uniq[-1])
    z = int((c == 0).sum())
    ff = int((c == 0xFFFFFFFF).sum())
    st = {
        "distinct": int(uniq.size),
        "min": mn, "max": mx,
        "zero_frac": round(z / n, 4), "ffffffff_frac": round(ff / n, 4),
        "distinct_frac": round(uniq.size / n, 4),
        "contiguous": bool(mx - mn + 1 == uniq.size),
    }
    # FK 值域检验
    fits = {}
    for name, B in BASES.items():
        frac = float((c < B).mean())
        if frac >= 0.98:
            cov = int((uniq < B).sum()) / B
            fits[name] = {"in_range_frac": round(frac, 5),
                          "distinct_covered_of_base": round(cov, 4)}
    if fits:
        st["within"] = fits
    return st


def scan(archive: str, tid: int, base: int, stride: int, n: int) -> dict:
    raw = payload(archive, tid)
    cols = {}
    for off in range(0, stride - 3):
        c = u32col(raw, base, stride, n, off)
        st = colstat(c)
        st["offset"] = off
        cols[f"@{off}"] = st
    return {
        "table_id": tid, "archive": archive, "payload_len": len(raw),
        "header": base, "stride": stride, "count": n,
        "closure": base + n * stride + 8 == len(raw),
        "cols": cols,
    }


def _sig_ok(raw: bytes, p: int) -> bool:
    """行尾签名: u32@(p-9) == u32@(p-5) 且 raw[p-1] == 0。"""
    if p - 9 < 0:
        return False
    a = int.from_bytes(raw[p - 9:p - 5], "little")
    b = int.from_bytes(raw[p - 5:p - 1], "little")
    return a == b and raw[p - 1] == 0


def walk(archive: str, tid: int, expect: int, lo: int = 12, hi: int = 400) -> dict:
    """贪心找行尾签名(与 club/lcrg walker 同一手法),用行数闭合做验收。"""
    raw = payload(archive, tid)
    end = len(raw) - 8
    pos, i = 14, 0
    lens = []
    while pos < end and i < expect + 1:
        for L in range(lo, hi):
            if pos + L > end:
                break
            if _sig_ok(raw, pos + L):
                lens.append(L)
                pos += L
                i += 1
                break
        else:
            return {"ok": False, "stuck_at": pos, "rows": i}
    return {
        "ok": i == expect and pos == end,
        "rows": i, "end_pos": pos, "payload_len": len(raw),
        "expected": expect,
        "len_hist": {int(k): int(v) for k, v in
                     zip(*np.unique(np.array(lens), return_counts=True))},
    }


def cols_csv(archive: str, tid: int, base: int, stride: int, n: int,
             ncols: int, path: pathlib.Path, lens: list[int] | None = None) -> str:
    raw = payload(archive, tid)
    mat = []
    for j in range(ncols):
        off = 4 * j
        if off + 4 > stride:
            break
        mat.append(u32col(raw, base, stride, n, off))
    arr = np.stack(mat, axis=1)
    hdr = ",".join(["row"] + [f"c{j}" for j in range(arr.shape[1])])
    np.savetxt(path, arr, fmt="%d", delimiter=",", header=hdr, comments="")
    return str(path)


def selftest() -> int:
    raw = payload("server", 26)
    assert len(raw) == 6218854, len(raw)
    # 对齐 u32 与非对齐 u32 的一致性
    a = u32col(raw, 14, 69, 10, 0)
    b = np.array([int.from_bytes(raw[14 + i * 69: 14 + i * 69 + 4], "little")
                  for i in range(10)], dtype=np.uint64)
    assert np.array_equal(a, b), (a, b)
    # 非 4 字节对齐偏移也要与逐行 int.from_bytes 一致
    c = u32col(raw, 14, 69, 10, 5)
    d = np.array([int.from_bytes(raw[14 + i * 69 + 5: 14 + i * 69 + 9], "little")
                  for i in range(10)], dtype=np.uint64)
    assert np.array_equal(c, d), (c, d)
    # 签名检测: t49 已知 stride=36,每行结尾签名必须成立
    r49 = payload("server", 49)
    ok = all(_sig_ok(r49, 14 + (i + 1) * 36) for i in range(0, 792149, 997))
    assert ok, "t49 行尾签名不成立"
    print("selftest PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t15 列画像 / FK 值域检验")
    ap.add_argument("cmd", choices=["scan", "walk", "cols", "selftest"], nargs="?")
    ap.add_argument("--archive", default="server", choices=["client", "server"])
    ap.add_argument("--table", type=int)
    ap.add_argument("--base", type=int, default=14)
    ap.add_argument("--stride", type=int)
    ap.add_argument("--count", type=int)
    ap.add_argument("--ncols", type=int, default=20)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or args.cmd == "selftest":
        return selftest()
    if not args.cmd or args.table is None:
        ap.error("需要 cmd 与 --table")
    OUTDIR.mkdir(parents=True, exist_ok=True)

    if args.cmd == "walk":
        if args.count is None:
            ap.error("walk 需要 --count")
        res = walk(args.archive, args.table, args.count)
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0 if res.get("ok") else 1

    if args.stride is None or args.count is None:
        # 从上游 census 读定长规格
        spec = _k()["fixed_specs"]().get((args.archive, args.table))
        if not spec:
            ap.error(f"{args.archive} table_{args.table} 无定长规格,请给 --stride/--count")
        args.stride = args.stride or spec["stride"]
        args.count = args.count or spec["count"]
        args.base = spec.get("header", args.base)

    if args.cmd == "scan":
        res = scan(args.archive, args.table, args.base, args.stride, args.count)
        p = OUTDIR / f"scan_t{args.table}.json"
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {p}  closure={res['closure']} cols={len(res['cols'])}")
        return 0 if res["closure"] else 1

    p = pathlib.Path(args.out) if args.out else OUTDIR / f"t{args.table}_cols.csv"
    print("wrote", cols_csv(args.archive, args.table, args.base, args.stride,
                            args.count, args.ncols, p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
