#!/usr/bin/env python3
"""fk_records — t15:t45/t48 行提取(80B+nameLen@37,+41)与列画像;t32/t36 通用值域扫描。

用法
----
  py -V:3.12 -I -B scratch/t15/out/fk_records.py --selftest
  py -V:3.12 -I -B scratch/t15/out/fk_records.py --table 45 --csv
  py -V:3.12 -I -B scratch/t15/out/fk_records.py --all
  py -V:3.12 -I -B scratch/t15/out/fk_records.py --scan 32
退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15/out"
sys.path.insert(0, str(OUTDIR))
import fk_scan as F  # noqa: E402

EXPECT = {45: 84477, 48: 5210}
HEAD, LENOFF, NAMEOFF, UCOLS = 80, 37, 41, 9  # 安全 u32 区: 0..32


def walk80(raw: bytes, expect: int) -> dict:
    end, pos, i, lens = len(raw) - 8, 14, 0, []
    while pos < end:
        ln = int.from_bytes(raw[pos + LENOFF:pos + LENOFF + 4], "little")
        if ln > 300 or pos + HEAD + ln > end:
            return {"ok": False, "rows": i, "stuck_at": pos, "bad_len": ln}
        lens.append(ln)
        pos += HEAD + ln
        i += 1
    return {"ok": i == expect and pos == end, "rows": i, "end": pos,
            "len": len(raw), "expected": expect,
            "named_rows": int(sum(1 for x in lens if x)),
            "len_hist": {int(k): int(v) for k, v in
                         zip(*np.unique(np.array(lens), return_counts=True))} if lens else {}}


def prof(raw: bytes, expect: int) -> dict:
    end, pos, i = len(raw) - 8, 14, 0
    cols = [[] for _ in range(UCOLS)]
    names = []
    while pos < end and i < expect:
        ln = int.from_bytes(raw[pos + LENOFF:pos + LENOFF + 4], "little")
        if ln > 300 or pos + HEAD + ln > end:
            break
        b = raw[pos:pos + HEAD]
        for j in range(UCOLS):
            cols[j].append(int.from_bytes(b[4 * j:4 * j + 4], "little"))
        names.append(raw[pos + NAMEOFF:pos + NAMEOFF + ln].decode("utf-8", "replace"))
        pos += HEAD + ln
        i += 1
    out = {"rows": i, "closed": pos == end == 14 + sum(
        HEAD + len(n.encode("utf-8")) for n in names)}
    prof_c = {}
    for j, c in enumerate(cols):
        a = np.array(c, dtype=np.int64)
        u = np.unique(a)
        prof_c[f"@{4 * j}"] = {"d": int(u.size), "min": int(u.min()), "max": int(u.max()),
                               "zero": round(float((a == 0).mean()), 4),
                               "ff": round(float((a == 0xFFFFFFFF).mean()), 4),
                               "sample": [int(x) for x in u[:4]]}
    out["cols"] = prof_c
    out["names_sample"] = [n for n in names[:6] if n]
    out["names_unique"] = len({n for n in names if n})
    out["_names"] = names
    out["_cols"] = cols
    return out


def gen_scan(tid: int, refs: dict[str, np.ndarray]) -> dict:
    """行边界未闭合的表:全 payload 逐字节 4B 窗口,统计落在各身份集合的比例。"""
    raw = F.payload("server", tid)
    body = np.frombuffer(raw, dtype=np.uint8)[14:len(raw) - 8]
    n = body.size - 3
    v = (body[:-3].astype(np.uint64)
         | (body[1:-2].astype(np.uint64) << np.uint64(8))
         | (body[2:-1].astype(np.uint64) << np.uint64(16))
         | (body[3:].astype(np.uint64) << np.uint64(24))).astype(np.int64)
    u = np.unique(v)
    res = {"table_id": tid, "payload_body": int(body.size),
           "window4": int(n), "distinct4": int(u.size)}
    for nm, ref in refs.items():
        hit = np.isin(u, ref)
        res[nm] = {"distinct_hits": int(hit.sum()),
                   "distinct_frac": round(float(hit.mean()), 5),
                   "window_hits": int(np.isin(v, ref).sum())}
    # 4 字节对齐子集(u32 读法)对照
    m = (body.size // 4) * 4
    va = np.frombuffer(body[:m].tobytes(), dtype="<u4").astype(np.int64)
    ua = np.unique(va)
    res["aligned_u32"] = {"count": int(va.size), "distinct": int(ua.size),
                          "min": int(ua.min()), "max": int(ua.max())}
    for nm, ref in refs.items():
        res["aligned_u32"][nm + "_distinct_hits"] = int(np.isin(ua, ref).sum())
    return res


def refs() -> dict[str, np.ndarray]:
    base = ROOT / "scratch/t05/people"
    c1 = np.load(base / "cls1.npy"); c2 = np.load(base / "cls2.npy")
    c3 = np.load(base / "cls3.npy"); c4 = np.load(base / "cls4.npy")
    c5 = np.load(base / "cls5.npy")
    a123 = np.concatenate([c1, c2, c3])
    return {
        "person_ordinal": np.unique(np.concatenate([
            a123[:, 71:75].copy().view("<u4").ravel(),
            c4[:, 22:26].copy().view("<u4").ravel(),
            c5[:, 10:14].copy().view("<u4").ravel()]).astype(np.int64)),
        "person_duni": np.unique(a123[:, 75:79].copy().view("<u4").ravel().astype(np.int64)),
        "club_ordinal": np.arange(84259, dtype=np.int64),
        "comp_ordinal": np.arange(7047, dtype=np.int64),
    }


def selftest() -> int:
    for tid, exp in EXPECT.items():
        r = walk80(F.payload("server", tid), exp)
        assert r["ok"], (tid, r)
    # t45 首行名字必须与 payload 中的字符串一致
    raw = F.payload("server", 45)
    ln = int.from_bytes(raw[14 + LENOFF:14 + LENOFF + 4], "little")
    nm = raw[14 + NAMEOFF:14 + NAMEOFF + ln].decode("utf-8")
    assert nm.strip(), nm
    print("selftest PASS", nm)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t15 t45/t48 行提取 / t32,t36 值域扫描")
    ap.add_argument("--table", type=int, choices=[45, 48])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--scan", type=int, choices=[32, 36])
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    if a.scan:
        r = gen_scan(a.scan, refs())
        (OUTDIR / f"scan_gen_t{a.scan}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print("scan t%d" % a.scan, json.dumps({k: v for k, v in r.items() if k != "aligned_u32"}, ensure_ascii=False)[:500])
        return 0
    tids = [45, 48] if a.all else ([a.table] if a.table else [])
    if not tids:
        ap.error("需要 --table/--all/--scan")
    for tid in tids:
        raw = F.payload("server", tid)
        w = walk80(raw, EXPECT[tid])
        p = prof(raw, EXPECT[tid])
        cols, names = p.pop("_cols"), p.pop("_names")
        out = {"table_id": tid, "walk": {k: v for k, v in w.items() if k != "len_hist"},
               "len_hist_top": dict(sorted(w.get("len_hist", {}).items(),
                                           key=lambda kv: -kv[1])[:12]),
               "profile": p}
        (OUTDIR / f"prof_t{tid}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        if a.csv:
            with (OUTDIR / f"t{tid}_cols.csv").open("w", newline="", encoding="utf-8") as f:
                cw = csv.writer(f)
                cw.writerow(["row", "nameLen"] + [f"u32@{4 * j}" for j in range(UCOLS)] + ["name"])
                for i in range(len(names)):
                    cw.writerow([i, len(names[i].encode("utf-8"))]
                                + [cols[j][i] for j in range(UCOLS)] + [names[i]])
        print(f"t{tid}: closed={w['ok']} rows={w['rows']} named={w.get('named_rows')} "
              f"end={w.get('end')} len={w.get('len')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
