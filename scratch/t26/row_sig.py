#!/usr/bin/env python3
"""t26-A2 — people_db.dat 行签名普查(向量化,只读)。

背景:文法 A(compact)只覆盖 1,193 行(class-5)。全文件其余行用另一套布局:
  ff ff ff ff 00 | u32 name_len | utf8 name | ...body... | 8x00 | u32 key2 | u32 duni | u32 duni
本脚本不猜 body,只用**尾部签名** `8x00 + u32 key2 + u32 duni + u32 duni` 作行锚点,
再用 basic_people_db 的同 ordinal duni 作独立事实校验(key2 与 duni 的配对是否成立),
最后给出按 class 的覆盖率 —— 这是"658,011 条完整 person 库"假设的定量裁决依据。

用法:
  py -V:3.12 -I -B scratch/t26/row_sig.py --help
  py -V:3.12 -I -B scratch/t26/row_sig.py --selftest
  py -V:3.12 -I -B scratch/t26/row_sig.py --out scratch/t26/out/people_rowsig.json

只读 scratch/data/ 与 scratch/t15/out/*.npy;只写 --out。退出码 0/1/2。
"""
from __future__ import annotations

import argparse
import collections
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
CL = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}


def _np():
    if str(ZSTD_PATH) not in sys.path:
        sys.path.insert(0, str(ZSTD_PATH))
    import numpy as np
    return np


def payload() -> bytes:
    _np()                                  # 把 zstandard 所在目录挂到 sys.path
    import zstandard as zstd
    data = (DB_DIR / "people_db.dat").read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[8:]),
                                               read_across_frames=True) as r:
        return r.read(600 * 1024 * 1024)


def basic_people():
    np = _np()
    import zstandard as zstd
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


def trailer_pairs(raw: bytes, max_key: int):
    """枚举 `8x00 + u32 key2 + u32 duni + u32 duni` 签名(全文件,逐字节)。
    bytes.find 是 C 层,不做逐位置 Python 循环以外的运算。"""
    n = len(raw)
    Z8 = b"\x00" * 8
    outs = []
    p = 0
    while True:
        p = raw.find(Z8, p)
        if p < 0:
            break
        q = p + 8
        if q + 12 <= n:
            k, v, w = struct.unpack_from("<III", raw, q)
            if v == w and v > 0 and k <= max_key:
                outs.append((p, k, v))
        p += 1
    return outs


def main() -> int:
    ap = argparse.ArgumentParser(description="t26-A2 people_db 行签名普查(只读)")
    ap.add_argument("--out", default=str(OUT_DIR / "people_rowsig.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    np = _np()

    if a.selftest:
        raw = b"\x00" * 8 + struct.pack("<III", 7, 99, 99) + b"\xff"
        outs = trailer_pairs(raw, 100)
        assert outs == [(0, 7, 99)], outs
        print("selftest OK")
        return 0

    raw = payload()
    cls, bduni = basic_people()
    total = struct.unpack_from("<I", raw, 2)[0]
    out = {"task": "t26-A2", "payload_len": len(raw), "header_count": total}

    outs = trailer_pairs(raw, max_key=total - 1)
    k2 = np.array([o[1] for o in outs], dtype=np.int64)
    dv = np.array([o[2] for o in outs], dtype=np.int64)
    out["signature"] = {
        "layout": "8x00 | u32 key2 | u32 duni | u32 duni  (duni 重复两遍)",
        "occurrences": len(outs),
        "key2_in_range": int((k2 < total).sum()),
        "key2_distinct": int(len(np.unique(k2))),
        "duni_distinct": int(len(np.unique(dv))),
    }

    # 独立事实校验:basic_people_db 同 ordinal 的 duni 是否与签名里的 duni 相等
    ok = dv == bduni[np.clip(k2, 0, total - 1)]
    verified = {}
    for kk, vv, good in zip(k2.tolist(), dv.tolist(), ok.tolist()):
        if good and kk not in verified:
            verified[kk] = vv
    vk = np.array(sorted(verified), dtype=np.int64)
    out["cross_check"] = {
        "claim": "签名行 (key2, duni) 与 basic_people_db 同 ordinal 的 duni 逐条相等",
        "matched_occurrences": int(ok.sum()),
        "matched_pct": round(100 * float(ok.mean()), 3),
        "distinct_verified_keys": int(len(vk)),
        "of_header_count": total,
        "coverage_pct": round(100 * len(vk) / total, 3),
        "grade": "L1(同文件签名自洽) + L2(basic_people_db 独立计数/独立 duni 列逐条对齐)",
    }

    # 按 class 覆盖
    per_class = {}
    for c in sorted(set(CL)):
        m = cls == c
        cov = int(np.isin(np.nonzero(m)[0], vk).sum())
        per_class[str(c)] = {"rows": int(m.sum()), "covered": cov,
                             "pct": round(100 * cov / max(1, int(m.sum())), 2)}
    out["coverage_by_class"] = per_class

    miss = np.setdiff1d(np.arange(total, dtype=np.int64), vk)
    out["missing"] = {
        "keys": int(len(miss)),
        "by_class": {str(c): int((cls[miss] == c).sum()) for c in sorted(set(CL))},
        "sample_keys": miss[:8].tolist(),
    }

    # 缺失行是否以别的形式出现:duni 是否在任何相邻重复 u32 里出现过
    n = len(raw)
    seen = np.zeros(total, dtype=bool)
    for off in range(4):
        m = (n - off) // 4
        w = np.frombuffer(raw[off:off + m * 4], dtype=np.uint32)
        idx = np.nonzero(w[:-1] == w[1:])[0]
        if not len(idx):
            continue
        vals = w[idx].astype(np.int64)
        tgt = bduni[miss]
        pos = np.searchsorted(np.sort(tgt), vals)
        srt = np.sort(tgt)
        pos[pos >= len(srt)] = 0
        hitv = srt[pos] == vals
        if hitv.any():
            got = np.unique(vals[hitv])
            seen[np.isin(bduni, got)] |= True
    out["missing_elsewhere"] = {
        "question": "未命中签名的行,其 duni 是否以'相邻重复 u32'形式出现在别处",
        "missing_total": int(len(miss)),
        "duni_seen_as_adjacent_dup": int(seen[miss].sum()),
        "note": "只说明值出现过,不构成行定位",
    }

    # 间距(签名到签名)分布
    offs = np.sort(np.array([o[0] for o in outs], dtype=np.int64))
    d = np.diff(offs)
    edges = [0, 32, 64, 128, 256, 512, 1024, 4096, 1 << 20]
    hist = np.histogram(d, bins=edges)[0]
    out["row_pitch"] = {
        "median": int(np.median(d)), "p10": int(np.percentile(d, 10)),
        "p90": int(np.percentile(d, 90)), "max": int(d.max()),
        "buckets": {f"{edges[i]}-{edges[i + 1]}": int(hist[i])
                    for i in range(len(hist))},
    }

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    print(f"wrote {a.out}")
    print(f"  signature occurrences {len(outs)}  verified keys {len(vk)}/{total} "
          f"({out['cross_check']['coverage_pct']}%)")
    print(f"  by class {per_class}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
