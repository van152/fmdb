#!/usr/bin/env python3
"""dspot — t15d:D-锚-only 表的轻量列画像(只读)。

目的:给"只有 RTTI D 锚"的表做数据侧抽查——类名语义 ↔ 列画像是否自洽。
不改任何实体裁决(裁决在晨裁);本脚本只产出 `plausible|implausible|silent`
所需的关键数字。

要点
----
1. **载荷定位有坑**:server_db 的 zstd 帧不一定在 table_off+9。t34 在 +9 命中的是
   内层 12 B 空壳,真帧在 +34。所以按 `14 + count*stride + 8` 选帧,不取首个命中。
2. **步长非 4 倍数**:u32 滑窗会跨字段,所以按 width∈{1,2,3,4} 全偏移扫,再按
   "常量 / 行序 / 年份 / 枚举 / ID 贴界 / 金额量级" 打信号分。
3. **E42**:ID 命中只报 max/base 与 d/base,不做裁决;单列值域不足以定案。

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --list
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --table 42 --fields
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --all --json scratch/t15d/out/prof/all.json
  py -V:3.12 -I -B scratch/t15d/out/dspot.py --table 50 --csv scratch/t15d/out/t50.csv

退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import runpy
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15d/out"
DUMP = ROOT / "scripts/fm24_dump.py"

# server 表定长规格(14 + n*stride + 8,见 scratch/t05/COVERAGE.json)
SPEC = {
    34: (7115, 44), 37: (465712, 40), 42: (17721, 26), 43: (535, 46),
    46: (7, 25), 50: (45, 26), 51: (59, 23), 58: (8, 45),
    62: (37214, 42), 64: (6946, 21), 66: (753, 24), 70: (10075, 40),
}
RTTI = {
    34: "STARTING_TEAM_CUP_HISTORY", 37: "STARTING_TEAM_LEAGUE_HISTORY",
    42: "STARTING_RETIREMENT", 43: "STARTING_MONTHLY_INSTALLMENT",
    46: "STARTING_DRAFT_TRANSFER", 50: "STARTING_MLS_TRADED_SLOT",
    51: "STARTING_MLS_GENERAL_ALLOCATION_MONEY",
    58: "STARTING_WEEKLY_WAGE_CONTRIBUTION", 62: "STARTING_RESERVE_TEAM",
    64: "STARTING_CLUB_STAFF_JOB_STATUS", 66: "STARTING_CLUB_TRANSFER_PREFERENCE",
    70: "STARTING_VISION_OBJECTIVE",
}
BASES = {"person": 658011, "club": 84259, "team": 84507, "comp": 7047,
         "injury": 115, "nation": 251, "city": 56293, "award": 3545,
         "curr": 173, "stage": 278}
MAGIC = bytes.fromhex("28b52ffd")
_C: dict = {}


def _codec():
    if "__codec__" not in _C:
        k = runpy.run_path(str(DUMP), run_name="notmain")
        _C["__codec__"] = k["_reader"]()
        _C["__k__"] = k
    return _C["__codec__"], _C["__k__"]


def payload(tid: int, archive: str = "server") -> bytes:
    key = (archive, tid)
    if key in _C:
        return _C[key]
    codec, k = _codec()
    fn = f"{archive}_db.dat"
    p = k["DB_DIR"] / fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    off, db = e["offset"], p.read_bytes()
    want = 14 + SPEC[tid][0] * SPEC[tid][1] + 8 if tid in SPEC else None
    cands, sized = [], []
    for d in range(64):
        if db[off + d: off + d + 4] != MAGIC:
            continue
        try:
            raw = codec["_stream_decompress"](db[off + d:], 256 * 1024 * 1024)
        except Exception:
            continue
        cands.append((d, len(raw)))
        if want is None or len(raw) == want:
            sized.append((d, raw))
    if not sized:
        raise RuntimeError(f"{fn} t{tid}: no frame of size {want}; hits={cands}")
    _C[key] = sized[-1][1]
    _C[("frame_at", tid)] = sized[-1][0]
    return _C[key]


def col(raw: bytes, stride: int, n: int, off: int, w: int) -> np.ndarray:
    a = np.frombuffer(raw, dtype=np.uint8)
    v = np.zeros(n, dtype=np.uint64)
    for k in range(w):
        v |= a[14 + off + k: 14 + off + k + n * stride: stride].astype(np.uint64) << np.uint64(8 * k)
    return v


def fstat(c: np.ndarray, idx: np.ndarray) -> dict:
    v = np.unique(c)
    n = c.size
    st = {"d": int(v.size), "min": int(v[0]), "max": int(v[-1]),
          "zero": round(float((c == 0).mean()), 3),
          "ff": round(float((c == 0xFFFF if c.max() < 65536 else 0xFFFFFFFF) == c).mean()
                      if False else float(((c == 0xFFFFFFFF) | (c == 0xFFFF)).mean()), 3),
          "top": [int(x) for x in v[:6]]}
    sig = []
    if v.size == 1:
        sig.append("const")
    if int(v[0]) == 0 and int(v[-1]) == n - 1 and v.size == n:
        sig.append("ord0")
    elif int(v[0]) == 1 and int(v[-1]) == n and v.size == n:
        sig.append("ord1")
    if v.size >= 5 and int(v[0]) >= 1900 and int(v[-1]) <= 2100:
        sig.append("year")
    if v.size <= 80 and v.size >= 2 and int(v[-1]) - int(v[0]) + 1 == v.size:
        sig.append(f"enum{v.size}")
    # 金额样:整数千元级,且 100/1000 整除比例高
    if int(v[-1]) >= 1000 and v.size > 5:
        big = c[c > 0]
        if big.size and float((big % 1000 == 0).mean()) > 0.9:
            sig.append("k1000")
        elif big.size and float((big % 100 == 0).mean()) > 0.9:
            sig.append("k100")
    # ID 贴界:取最大可容 base
    if int(v[-1]) > 0:
        fit = None
        for name, B in sorted(BASES.items(), key=lambda kv: kv[1]):
            if int(v[-1]) < B:
                fit = (name, B)
                break
        if fit and v.size > 3:
            sig.append(f"<{fit[0]}:{v[-1] / fit[1]:.3f}")
    st["sig"] = sig
    return st


def fields(tid: int, maxw: int = 4) -> dict:
    raw, n, stride = payload(tid), SPEC[tid][0], SPEC[tid][1]
    idx = np.arange(n, dtype=np.uint64)
    out = []
    for off in range(stride):
        for w in range(1, maxw + 1):
            if off + w > stride:
                continue
            c = col(raw, stride, n, off, w)
            st = fstat(c, idx)
            if not st["sig"]:
                continue
            st.update({"off": off, "w": w})
            st.pop("ff", None)
            out.append(st)
    return {"table_type": tid, "rtti_class": RTTI[tid], "count": n, "stride": stride,
            "frame_at": _C.get(("frame_at", tid)), "payload": len(raw),
            "closure": 14 + n * stride + 8 == len(raw), "cands": out}


def brief(tid: int) -> dict:
    raw, n, stride = payload(tid), SPEC[tid][0], SPEC[tid][1]
    bs = {k: round(v, 4) for k, v in
          {"rows": n, "stride": stride, "frame_at": _C.get(("frame_at", tid)),
           "closure": 14 + n * stride + 8 == len(raw)}.items()}
    return {"table_type": tid, "rtti_class": RTTI[tid], **bs}


def write_csv(tid: int, path: pathlib.Path, limit: int = 2000) -> int:
    raw, n, stride = payload(tid), SPEC[tid][0], SPEC[tid][1]
    path.parent.mkdir(parents=True, exist_ok=True)
    m = min(n, limit)
    w = stride // 4
    with path.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["row"] + [f"u32@{4 * j}" for j in range(w)] + [f"b{o}" for o in range(stride - 4 * w)])
        for i in range(m):
            b = 14 + i * stride
            wr.writerow([i] + [int.from_bytes(raw[b + 4 * j: b + 4 * j + 4], "little") for j in range(w)]
                        + [raw[b + 4 * w + o] for o in range(stride - 4 * w)])
    return m


def selftest() -> int:
    cov = json.loads((ROOT / "scratch/t05/COVERAGE.json").read_text(encoding="utf-8"))
    by = {t["table_id"]: t for t in cov["tables"] if t["archive"] == "server"}
    ok = True
    for tid, (n, stride) in SPEC.items():
        want = f"14+{n}*{stride}+8=={by[tid]['payload']}"
        if by[tid]["equation"].replace(" ", "") != want:
            print(f"FAIL t{tid}: {by[tid]['equation']}")
            ok = False
    # 帧定位自检:t34 曾误取 +9 的 12 B 空壳,这里要求 ≠ 首个命中也能取到
    if ok:
        try:
            print(f"  t34 frame_at=+{payload(34) and _C.get(('frame_at', 34))} len={len(payload(34))}")
        except Exception as e:  # noqa: BLE001
            print("  payload load FAIL:", e)
            ok = False
    print("selftest:", "ok" if ok else "MISMATCH", f"({len(SPEC)} tables)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t15d D-锚-only 表轻量画像(只读)")
    ap.add_argument("--table", type=int, action="append")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--fields", action="store_true", help="输出字段候选(width 1..4)")
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--csv", type=pathlib.Path)
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.list:
        for tid in sorted(SPEC):
            print(f"t{tid:>3}  {SPEC[tid][0]:>7} rows x {SPEC[tid][1]:>3} B  {RTTI[tid]}")
        return 0
    tids = sorted(SPEC) if a.all else (a.table or [])
    if not tids:
        ap.print_help()
        return 2
    bad = [t for t in tids if t not in SPEC]
    if bad:
        print(f"unknown table(s): {bad}", file=sys.stderr)
        return 2
    if a.csv:
        if len(tids) != 1:
            print("--csv 需要且仅需一张表", file=sys.stderr)
            return 2
        m = write_csv(tids[0], a.csv, a.limit)
        print(f"csv: {a.csv} ({m} rows)")
    out = [fields(t) if a.fields else brief(t) for t in tids]
    payloadj = out[0] if len(out) == 1 else {"tables": out}
    text = json.dumps(payloadj, ensure_ascii=False, indent=1)
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(text, encoding="utf-8")
        print(f"json: {a.json} ({len(text)} B, {len(out)} tables)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
