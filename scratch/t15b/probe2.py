#!/usr/bin/env python3
"""t15b addendum — people_db 内部锚点抽样 + hist id/dt 偏移算术 + 基数关系。

只读 FM24_DB_DIR;输出 JSON 到 --out。
退出码 0 / 1 校验失败 / 2 用法错误。
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
MAGIC = bytes.fromhex("28b52ffd")
sys.path.insert(0, str(pathlib.Path(r"D:\tmp2b\fm24\tools\python")))


def dec(path: pathlib.Path, skip: int = 8) -> bytes:
    import io
    import zstandard as zstd
    data = path.read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[skip:]), read_across_frames=True) as r:
        return r.read(600 * 1024 * 1024)


def people_probe() -> dict:
    raw = dec(DB_DIR / "people_db.dat")
    out = {"len": len(raw), "first_48_hex": raw[:48].hex()}
    u32 = list(struct.unpack_from("<12I", raw, 0))
    out["header_u32_12"] = u32
    # 候选头部计数字段:找 1e4..1e7 且能被后续检查命中的 u32(仅前 4KB)
    cands = []
    for off in range(0, 4096, 1):
        if off + 4 > 4096:
            break
        v = struct.unpack_from("<I", raw, off)[0]
        if 100000 <= v <= 2000000:
            cands.append([off, v])
    out["u32_candidates_100k_2m_in_first4k"] = cands[:24]
    # 全量 marker 计数(不解析字段)
    out["marker_ff00"] = raw.count(b"\xff\xff\xff\xff\x00")
    out["marker_ff"] = raw.count(b"\xff\xff\xff\xff")
    # 抽样 8 个 1MB 窗口:合法 "FF FF FF FF 00 | u32 len | utf8 name | u32 dob" 密度
    win = 1 << 20
    step = max(1, (len(raw) - win) // 8)
    per = []
    for i in range(8):
        s = i * step
        blob = raw[s:s + win]
        good = 0
        p = blob.find(b"\xff\xff\xff\xff\x00")
        while p != -1:
            if p + 9 <= len(blob):
                ln = struct.unpack_from("<I", blob, p + 5)[0]
                e = p + 9 + ln
                if 3 <= ln <= 60 and e + 4 <= len(blob):
                    try:
                        nm = blob[p + 9:e].decode("utf-8")
                    except UnicodeDecodeError:
                        nm = None
                    if nm and all((c.isprintable() or c in " -'.") for c in nm):
                        dob = struct.unpack_from("<I", blob, e)[0]
                        yr, doy = dob >> 16, dob & 0xFFFF
                        if 1900 <= yr <= 2012 and 1 <= doy <= 366:
                            good += 1
            p = blob.find(b"\xff\xff\xff\xff\x00", p + 5)
        per.append({"win_off": s, "markers": blob.count(b"\xff\xff\xff\xff\x00"), "valid_name_dob": good})
    tot_valid = sum(x["valid_name_dob"] for x in per)
    tot_mark = sum(x["markers"] for x in per)
    out["windows"] = per
    out["est_valid_anchors_full"] = round(tot_valid / tot_mark * out["marker_ff00"]) if tot_mark else 0
    # 名字样本(只取 3 个)
    samples = []
    p = raw.find(b"\xff\xff\xff\xff\x00")
    while p != -1 and len(samples) < 3:
        ln = struct.unpack_from("<I", raw, p + 5)[0]
        if 3 <= ln <= 60:
            try:
                nm = raw[p + 9:p + 9 + ln].decode("utf-8")
                if all((c.isprintable() or c == " ") for c in nm):
                    samples.append({"off": p, "name": nm})
            except UnicodeDecodeError:
                pass
        p = raw.find(b"\xff\xff\xff\xff\x00", p + 5)
    out["name_samples"] = samples
    return out


def hist_probe() -> dict:
    out = {}
    for tag, stride, dt in (("pl", 44, "pl_hist_dt.dat"), ("non_pl", 24, "non_pl_hist_dt.dat")):
        ids = (DB_DIR / f"{tag}_hist_id.dat").read_bytes()
        n = (len(ids) - 8) // 4
        k = min(n, 400)
        h = list(struct.unpack_from(f"<{k}I", ids, 8))
        t = min(n, 400)
        tail = list(struct.unpack_from(f"<{t}I", ids, 8 + 4 * (n - t)))
        pairs = [(h[i], h[i + 1]) for i in range(0, k - 1, 2)]
        al = sum(1 for p in pairs if p[0] % stride == 0 and p[1] % stride == 0)
        inc = all(pairs[i + 1][0] - pairs[i][1] == stride for i in range(len(pairs) - 1))
        dtraw = dec(DB_DIR / dt)
        idx = dec(DB_DIR / f"{tag}_hist_index.dat")
        icount = struct.unpack_from("<I", idx, 0)[0]
        out[tag] = {
            "id_u32": n, "id_pairs": n // 2, "stride": stride,
            "head_pairs": [list(p) for p in pairs[:3]],
            "head_pairs_aligned_bytes": f"{al}/{len(pairs)}",
            "head_pairs_contiguous_step": inc,
            "id_tail_u32_8": tail[-8:],
            "dt_decompressed_len": len(dtraw),
            "dt_exact_rows": len(dtraw) // stride,
            "dt_len_mod_stride": len(dtraw) % stride,
            "index_count": icount,
            "index_count_eq_id_pairs": icount == n // 2,
            "id_last_end": tail[-1] if tail else None,
            "id_last_end_plus_stride_eq_dt": (tail[-1] + stride == len(dtraw)) if tail else None,
        }
    # 后面再看看两路同一 person 集是否互斥:比较 id 文件里的 start 偏移(不是 id)
    return out


def relations(people: dict, hist: dict) -> dict:
    return {
        "basic_people_db_rows": 658011,
        "people_db_valid_name_dob_est": people.get("est_valid_anchors_full"),
        "people_db_header_u32_12": people.get("header_u32_12"),
        "pl_hist_persons": hist["pl"]["id_pairs"],
        "non_pl_hist_persons": hist["non_pl"]["id_pairs"],
        "pl_plus_non_pl": hist["pl"]["id_pairs"] + hist["non_pl"]["id_pairs"],
        "delta_pl_vs_basic_players": hist["pl"]["id_pairs"] - 476158,
        "delta_nonpl_vs_basic_nonplayers": hist["non_pl"]["id_pairs"] - 166064,
        "delta_sum_vs_basic": hist["pl"]["id_pairs"] + hist["non_pl"]["id_pairs"] - 658011,
        "t49_server_rows": 792149,
        "note": "差值只作为量级线索,不构成实体同一性证明",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="t15b addendum: people_db / hist 偏移算术")
    ap.add_argument("--out", default=str(ROOT / "scratch/t15b/out/probe2.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        assert 8 + 3 * 44 == 140
        print("selftest OK")
        return 0
    res = {"task": "t15b-addendum", "generated": "2026-11-18"}
    res["people_db"] = people_probe()
    res["hist"] = hist_probe()
    res["relations"] = relations(res["people_db"], res["hist"])
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res["relations"], ensure_ascii=False, indent=1))
    print("people est anchors:", res["people_db"]["est_valid_anchors_full"])
    print("hist:", json.dumps({k: {kk: vv for kk, vv in v.items() if kk in
                                  ("id_pairs", "dt_exact_rows", "index_count", "index_count_eq_id_pairs",
                                   "head_pairs_aligned_bytes", "id_last_end_plus_stride_eq_dt")}
                               for k, v in res["hist"].items()}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
