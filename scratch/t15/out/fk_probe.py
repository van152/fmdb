#!/usr/bin/env python3
"""fk_probe — t15 补充:变长表(t45/t48/t36/t32)行边界 + person/non-pl 身份空间交叉。

只读 server_db.dat / *_hist_*.dat;只写 scratch/t15/out/。

用法
----
  py -V:3.12 -I -B scratch/t15/out/fk_probe.py --help
  py -V:3.12 -I -B scratch/t15/out/fk_probe.py --selftest
  py -V:3.12 -I -B scratch/t15/out/fk_probe.py walk --table 45
  py -V:3.12 -I -B scratch/t15/out/fk_probe.py people
退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15/out"
DATA = ROOT / "scratch/data"
sys.path.insert(0, str(OUTDIR))
import fk_scan as F  # noqa: E402

EXPECT = {32: 315, 36: 6535, 45: 84477, 48: 5210}


def walk45(raw: bytes) -> dict:
    """t45 行 = 80B 头 + nameLen(name 在 +41);闭合 14+Σ+8==len。"""
    end, pos, i, names = len(raw) - 8, 14, 0, []
    while pos < end:
        if pos + 41 > end:
            return {"ok": False, "stuck_at": pos, "rows": i}
        ln = int.from_bytes(raw[pos + 37:pos + 41], "little")
        if not (0 <= ln <= 120) or pos + 80 + ln > end:
            return {"ok": False, "stuck_at": pos, "rows": i, "bad_len": ln}
        nm = raw[pos + 41:pos + 41 + ln]
        # 名字为 UTF-8,允许高位字节;只排除控制字符(允许 0x09/0x0a)
        if ln and any(c < 9 for c in nm):
            return {"ok": False, "stuck_at": pos, "rows": i, "bad_name": nm[:20].hex()}
        names.append(nm.decode("utf-8", "replace"))
        pos += 80 + ln
        i += 1
    return {"ok": i == EXPECT[45] and pos == end, "rows": i, "end": pos,
            "len": len(raw), "names_sample": names[:6], "names_total": len(names)}


def walk48(raw: bytes) -> dict:
    """t48 试探:行尾 u32@(p-13)==u32@(p-9) 且 u32@(p-17)==1 且 raw[p-1]==0。"""
    end, pos, i = len(raw) - 8, 14, 0
    lens = []
    while pos < end:
        for L in range(20, 400):
            p = pos + L
            if p > end:
                return {"ok": False, "stuck_at": pos, "rows": i}
            a = int.from_bytes(raw[p - 13:p - 9], "little")
            b = int.from_bytes(raw[p - 9:p - 5], "little")
            c = int.from_bytes(raw[p - 17:p - 13], "little")
            if a == b and c == 1 and raw[p - 1] == 0:
                lens.append(L)
                pos += L
                i += 1
                break
        else:
            return {"ok": False, "stuck_at": pos, "rows": i}
    hist = {int(k): int(v) for k, v in
            zip(*np.unique(np.array(lens), return_counts=True))} if lens else {}
    return {"ok": i == EXPECT[48] and pos == end, "rows": i, "end": pos,
            "len": len(raw), "expected": EXPECT[48], "len_hist": hist}


def id_cols(raw: bytes, base: int, stride: int, n: int, offsets) -> dict:
    out = {}
    for o in offsets:
        v = F.u32col(raw, base, stride, n, o).astype(np.int64)
        out[o] = v
    return out


def people() -> dict:
    c1 = np.load(str(OUTDIR.parents[1] / "t05/people/cls1.npy"))
    c2 = np.load(str(OUTDIR.parents[1] / "t05/people/cls2.npy"))
    c3 = np.load(str(OUTDIR.parents[1] / "t05/people/cls3.npy"))
    c4 = np.load(str(OUTDIR.parents[1] / "t05/people/cls4.npy"))
    c5 = np.load(str(OUTDIR.parents[1] / "t05/people/cls5.npy"))
    a123 = np.concatenate([c1, c2, c3])
    ordinal = np.concatenate([a123[:, 71:75].copy().view("<u4").ravel(),
                              c4[:, 22:26].copy().view("<u4").ravel(),
                              c5[:, 10:14].copy().view("<u4").ravel()]).astype(np.int64)
    duni = a123[:, 75:79].copy().view("<u4").ravel().astype(np.int64)

    # t49 的 @4
    raw = F.payload("server", 49)
    n, st = 792149, 36
    v49 = F.u32col(raw, 14, st, n, 4).astype(np.int64)
    u49 = np.unique(v49)

    # 未解析的非球员历史 id 文件(tad. 明文,非 zstd)
    def plain_ids(fn: str) -> np.ndarray:
        b = (DATA / fn).read_bytes()
        return np.frombuffer(b, dtype="<u4", offset=12).copy()

    pl = plain_ids("pl_hist_id.dat")
    npl = plain_ids("non_pl_hist_id.dat")

    res = {
        "role": "t49 的 @4 引用列 vs basic_people_db 身份空间",
        "person_rows_total": int(ordinal.size),
        "person_ordinal": {"distinct": int(np.unique(ordinal).size),
                           "min": int(ordinal.min()), "max": int(ordinal.max()),
                           "contiguous_0_to_max": bool(np.unique(ordinal).size == ordinal.max() + 1)},
        "person_duni": {"distinct": int(np.unique(duni).size),
                        "min": int(duni.min()), "max": int(duni.max()),
                        "rows_sharing_duni": int(duni.size - np.unique(duni).size)},
        "t49_col4": {"rows": int(v49.size), "distinct": int(u49.size),
                     "min": int(u49.min()), "max": int(u49.max()),
                     "rows_per_distinct": round(v49.size / u49.size, 4)},
        "t49_col4_in_person_duni": {"distinct_hits": int(np.isin(u49, duni).sum()),
                                    "row_hits": int(np.isin(v49, duni).sum()),
                                    "tag": "C"},
        "t49_col4_in_person_ordinal": {"distinct_hits": int(np.isin(u49, ordinal).sum()),
                                       "row_hits": int(np.isin(v49, ordinal).sum()),
                                       "caveat": "ordinal 空间 0..658010 连续,任何 <658011 的值都算命中,单测无鉴别力"},
        "t49_col4_excess": {},
        "plain_id_files": {
            "pl_hist_id.dat": {"u32": int(pl.size), "distinct": int(np.unique(pl).size),
                               "min": int(pl.min()), "max": int(pl.max())},
            "non_pl_hist_id.dat": {"u32": int(npl.size), "distinct": int(np.unique(npl).size),
                                   "min": int(npl.min()), "max": int(npl.max())},
        },
    }
    miss = u49[~np.isin(u49, duni)]
    res["t49_col4_excess"] = {
        "distinct_not_in_duni": int(miss.size),
        "rows_not_in_duni": int((~np.isin(v49, duni)).sum()),
        "missing_min": int(miss.min()), "missing_max": int(miss.max()),
        "missing_lt_658011": int((miss < 658011).sum()),
        "missing_ge_658011": int((miss >= 658011).sum()),
        "missing_in_pl_hist_id": int(np.isin(miss, pl).sum()),
        "missing_in_non_pl_hist_id": int(np.isin(miss, npl).sum()),
        "missing_in_pl_or_npl": int(np.isin(miss, np.concatenate([pl, npl])).sum()),
        "missing_in_neither": int(miss.size - np.isin(miss, np.concatenate([pl, npl])).sum()),
    }
    # 整数分档直方(以 2^k 为界)
    bins = [0, 65536, 658011, 1 << 20, 1 << 24, 1 << 28, 1 << 31, 1 << 32]
    h = {}
    for lo, hi in zip(bins, bins[1:]):
        h[f"{lo}-{hi}"] = int(((miss >= lo) & (miss < hi)).sum())
    res["t49_col4_excess"]["missing_hist"] = h
    return res


def selftest() -> int:
    raw = F.payload("server", 45)
    assert len(raw) == 7608748, len(raw)
    ln = int.from_bytes(raw[14 + 37:14 + 41], "little")
    assert 0 < ln < 40, ln
    print("selftest PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t15 变长表边界 + person 空间交叉")
    ap.add_argument("cmd", choices=["walk", "people", "selftest"], nargs="?")
    ap.add_argument("--table", type=int)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest or args.cmd == "selftest":
        return selftest()
    if args.cmd == "people":
        r = people()
        OUTDIR.mkdir(parents=True, exist_ok=True)
        (OUTDIR / "people_probe.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote people_probe.json", r["t49_col4"]["distinct"], r["t49_col4_excess"]["distinct_not_in_duni"])
        return 0
    if args.cmd == "walk" and args.table in (45, 48):
        raw = F.payload("server", args.table)
        r = walk45(raw) if args.table == 45 else walk48(raw)
        (OUTDIR / f"walk_t{args.table}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print("t%d" % args.table, json.dumps({k: v for k, v in r.items() if k != "names_sample"}, ensure_ascii=False)[:400])
        return 0 if r.get("ok") else 1
    ap.error("需要 cmd(--table 45|48)")
    return 2


if __name__ == "__main__":
    sys.exit(main())
