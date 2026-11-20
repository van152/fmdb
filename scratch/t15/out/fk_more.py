#!/usr/bin/env python3
"""fk_more — t15 收尾交叉:t45/t48 名字与 club/person 空间、t29/t36 值域画像。

用法: py -V:3.12 -I -B scratch/t15/out/fk_more.py [--selftest]
退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch/t15/out"
sys.path.insert(0, str(OUT))
import fk_scan as F  # noqa: E402
import fk_records as R  # noqa: E402

CLUB, COMP, PERSON = 84259, 7047, 658011


def t45_rows():
    raw = F.payload("server", 45)
    end, pos, i, out = len(raw) - 8, 14, 0, []
    while pos < end:
        ln = int.from_bytes(raw[pos + 37:pos + 41], "little")
        out.append((raw[pos:pos + 80], raw[pos + 41:pos + 41 + ln].decode("utf-8", "replace")))
        pos += 80 + ln
        i += 1
    return out


def t48_rows():
    raw = F.payload("server", 48)
    end, pos, out = len(raw) - 8, 14, []
    while pos < end:
        ln = int.from_bytes(raw[pos + 37:pos + 41], "little")
        out.append((raw[pos:pos + 80], raw[pos + 41:pos + 41 + ln].decode("utf-8", "replace")))
        pos += 80 + ln
    return out


def w32(b: bytes, o: int) -> int:
    return int.from_bytes(b[o:o + 4], "little")


def w16(b: bytes, o: int) -> int:
    return int.from_bytes(b[o:o + 2], "little")


def analyze_pair(rows, label) -> dict:
    n = len(rows)
    names = [r[1] for r in rows]
    res = {"rows": n, "named": sum(1 for x in names if x),
           "names_unique": len({x for x in names if x})}
    # 名字首/尾 token 集合
    tok1 = {x.split(" ")[0] for x in names if x}
    tokL = {x.split(" ")[-1] for x in names if x}
    res["first_tokens"] = len(tok1)
    res["last_tokens"] = len(tokL)
    # 逐列在三个 ID 空间内的行命中率
    cols = {}
    for o in range(0, 33):
        v = np.array([w32(b, o) for b, _ in rows], dtype=np.int64)
        m = v != 0xFFFFFFFF
        if not m.any():
            cols[f"@{o}"] = {"all_ff": True}
            continue
        e = {}
        for nm, B in (("club", CLUB), ("comp", COMP), ("person", PERSON)):
            e[nm] = round(float((v[m] < B).mean()), 4)
        e["d"] = int(np.unique(v[m]).size)
        e["min"] = int(v[m].min())
        e["max"] = int(v[m].max())
        cols[f"@{o}"] = e
    res["cols"] = cols
    return res


def t29_prof() -> dict:
    raw = F.payload("server", 29)
    n, st = 13278, 75
    b = np.frombuffer(raw, dtype=np.uint8)[14:14 + st * n].reshape(n, st)
    res = {"rows": n, "stride": st, "cols": {}}
    for o in range(0, st - 3):
        v = (b[:, o].astype(np.int64) | (b[:, o + 1].astype(np.int64) << 8)
             | (b[:, o + 2].astype(np.int64) << 16) | (b[:, o + 3].astype(np.int64) << 24))
        u = np.unique(v)
        if u.size > 600 and u.size < n:
            continue
        e = {"d": int(u.size), "min": int(u.min()), "max": int(u.max()),
             "ff": round(float((v == 0xFFFFFFFF).mean()), 3)}
        for nm, B in (("club", CLUB), ("comp", COMP), ("person", PERSON), ("t29row", n)):
            e[nm] = round(float((v < B).mean()), 4)
        e["contig_row"] = bool(u.size == n and int(u.max() - u.min() + 1) == n)
        res["cols"][f"@{o}"] = e
    return res


def t36_probe() -> dict:
    raw = F.payload("server", 36)
    end = len(raw) - 8
    # 行尾签名: u32@(p-13)==u32@(p-9)==i+1, raw[p-1]==0
    pos, i, lens = 14, 0, []
    while pos < end and i < 6600:
        f = None
        for L in range(20, 400):
            p = pos + L
            if p > end:
                break
            a, c = w32(raw, p - 13), w32(raw, p - 9)
            if a == c == i + 1 and raw[p - 1] == 0:
                f = L
                break
        if f is None:
            return {"ok": False, "rows": i, "stuck_at": pos}
        lens.append(f)
        pos += f
        i += 1
    h = {int(k): int(v) for k, v in zip(*np.unique(np.array(lens), return_counts=True))}
    return {"ok": i == 6535 and pos == end, "rows": i, "end": pos,
            "len": len(raw), "len_hist_top": dict(sorted(h.items(), key=lambda kv: -kv[1])[:10])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r45 = t45_rows()
        assert len(r45) == 84477
        assert r45[0][1] == "Markelian Xhai", r45[0][1]
        print("selftest PASS")
        return 0
    r45, r48 = t45_rows(), t48_rows()
    out = {
        "t45": analyze_pair(r45, "t45"),
        "t48": analyze_pair(r48, "t48"),
        "t45_vs_t48_names": {
            "t45_named": sum(1 for _, n in r45 if n),
            "t48_named": sum(1 for _, n in r48 if n),
            "shared_names": len({n for _, n in r45 if n} & {n for _, n in r48 if n}),
        },
        "t29": t29_prof(),
        "t36": t36_probe(),
    }
    (OUT / "more.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    print("t45 names", out["t45"]["named"], "/", out["t45"]["rows"],
          "t48 names", out["t48"]["named"], "/", out["t48"]["rows"],
          "shared", out["t45_vs_t48_names"]["shared_names"])
    print("t36 walk", json.dumps(out["t36"], ensure_ascii=False)[:220])
    return 0


if __name__ == "__main__":
    sys.exit(main())
