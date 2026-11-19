#!/usr/bin/env python3
"""t26-A3 — people_db.dat 尾部变体普查(向量化,只读)。

A2 只用 `8x00 + key2 + duni + duni` 拿到 93.45% 覆盖。剩余 43,099 行的尾部
前导零字节更少(4/6/7 个)。本脚本把所有 "N×00 + key2 + duni + duni" 变体
一起枚举,再按 basic_people_db 同 ordinal 的 duni 做独立校验,得到最终覆盖率。

用法:
  py -V:3.12 -I -B scratch/t26/row_sig2.py --help
  py -V:3.12 -I -B scratch/t26/row_sig2.py --selftest
  py -V:3.12 -I -B scratch/t26/row_sig2.py --out scratch/t26/out/people_rowsig2.json

退出码 0/1/2。
"""
from __future__ import annotations

import argparse
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
OUT_DIR = ROOT / "scratch/t26/out"
CL = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}


def _np():
    if str(ZSTD_PATH) not in sys.path:
        sys.path.insert(0, str(ZSTD_PATH))
    import numpy as np
    return np


def payload() -> bytes:
    _np()
    import zstandard as zstd
    import io
    data = (DB_DIR / "people_db.dat").read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[8:]),
                                               read_across_frames=True) as r:
        return r.read(600 * 1024 * 1024)


def basic_people():
    np = _np()
    import zstandard as zstd
    import io
    data = (DB_DIR / "basic_people_db.dat").read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[8:]),
                                               read_across_frames=True) as r:
        bp = r.read(200 * 1024 * 1024)
    cnt = struct.unpack_from("<I", bp, 0)[0]
    pos = 5
    cls = bytearray(cnt)
    duni = np.zeros(cnt, dtype=np.int64)
    for i in range(cnt):
        c = bp[pos + 1]
        cls[i] = c
        ln = CL[c]
        _, dd, _ = struct.unpack_from("<III", bp, pos + ln - 12)
        duni[i] = dd
        pos += ln
    return np.frombuffer(bytes(cls), dtype=np.uint8), duni


def variants(raw: bytes, total: int):
    """对每种前导零数 N in 2..12,枚举 N×00 + key2 + duni + duni。"""
    n = len(raw)
    res = []
    for N in range(2, 13):
        pat = b"\x00" * N
        p = 0
        while True:
            p = raw.find(pat, p)
            if p < 0:
                break
            q = p + N
            if q + 12 <= n:
                k, v, w = struct.unpack_from("<III", raw, q)
                if v == w and 0 < v and k < total:
                    res.append((N, p, k, v))
            p += 1
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="t26-A3 people_db 尾部变体普查(只读)")
    ap.add_argument("--out", default=str(OUT_DIR / "people_rowsig2.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    np = _np()

    if a.selftest:
        raw = b"\x00\x00" + struct.pack("<III", 7, 99, 99)
        r = variants(raw, 100)
        assert (2, 0, 7, 99) in r, r
        print("selftest OK")
        return 0

    raw = payload()
    cls, bduni = basic_people()
    total = struct.unpack_from("<I", raw, 2)[0]
    rows = variants(raw, total)

    by_N = {}
    verified = {}
    dup = 0
    for N, p, k, v in rows:
        by_N[N] = by_N.get(N, 0) + 1
        if bduni[k] == v:
            if k in verified:
                dup += 1
            else:
                verified[k] = (v, N, p)

    vk = np.array(sorted(verified), dtype=np.int64)
    per_class = {}
    for c in sorted(CL):
        m = cls == c
        cov = int(np.isin(np.nonzero(m)[0], vk).sum())
        per_class[str(c)] = {"rows": int(m.sum()), "covered": cov,
                             "pct": round(100 * cov / max(1, int(m.sum())), 2)}
    miss = np.setdiff1d(np.arange(total, dtype=np.int64), vk)
    out = {
        "task": "t26-A3",
        "payload_len": len(raw), "header_count": total,
        "variants": {str(k): v for k, v in sorted(by_N.items())},
        "signature_occurrences": len(rows),
        "verified_distinct_keys": int(len(vk)),
        "verified_pct": round(100 * len(vk) / total, 3),
        "duplicate_key_hits": dup,
        "coverage_by_class": per_class,
        "missing": {"keys": int(len(miss)),
                    "by_class": {str(c): int((cls[miss] == c).sum()) for c in sorted(CL)},
                    "first_12": miss[:12].tolist()},
        "variant_of_choice": {str(k): sum(1 for v in verified.values() if v[1] == k)
                              for k in sorted({v[1] for v in verified.values()})},
        "grade": "L1(尾部签名自洽) + L2(basic_people_db 同 ordinal duni 逐条对齐)",
    }
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    print(f"wrote {a.out}")
    print(f"  variants {out['variants']}")
    print(f"  verified {len(vk)}/{total} ({out['verified_pct']}%)")
    print(f"  by class {per_class}")
    print(f"  missing {out['missing']['keys']} {out['missing']['by_class']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
