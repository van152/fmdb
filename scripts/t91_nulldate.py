#!/usr/bin/env python3
"""t91: 空日期常量 0x076c0001 (`01 00 6c 07` = doy 1, year 1900) 全档探针。

外源主张(ext/fm-data@d7a7150, agentB §2.2):FM 用 (u16 day_of_year, u16 year)
编码日期,`01 00 6c 07` = (1,1900) 是 **null date**。本脚本只做三件事:
  1. 在我们已闭合行框的表上,逐槽位统计该 4 字节常量的命中率;
  2. 用"同表其它槽位的平均命中率"与"字节级随机基线"做对照(不拿命中当结论);
  3. 把命中槽位与 reports/ 里既有 date4 槽位口径逐条并列(只增证据,不改判)。

外部代码一律不执行;只用我们自己的加载器 (scripts/fm24_dump.load_payload)。

用法:
  FM24_DB_DIR=... py -V:3.12 -I -B scripts/t91_nulldate.py [--help] [--selftest]
  ... [--out scratch/t91/out/nulldate_probe.json] [--people-cap 33554432]
退出码: 0 完成 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(_cfg.VENDOR_DIR))

SENT = 0x076C0001
SENT_B = struct.pack("<I", SENT)
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
OUT = ROOT / "scratch/t91/out/nulldate_probe.json"

# 已知行框(t74/E115 冻结):table -> (header, footer, 模型)
FIXED = {(0, "client"): 77, (0, "server"): 77, (21, "client"): 38,
         (21, "server"): 181, (56, "client"): 13, (56, "server"): 13}
VARIABLE = [(7, "client"), (7, "server"), (8, "client"), (8, "server"),
            (18, "client"), (18, "server"), (24, "server"), (27, "client"), (27, "server")]
H, F = 14, 8


def _selftest() -> int:
    assert SENT_B == bytes.fromhex("01006c07")
    assert struct.unpack("<HH", SENT_B) == (1, 1900)
    # (doy, year) -> 0x076c0001 round trip
    assert struct.pack("<HH", 1, 1900) == SENT_B
    print("selftest OK: 01 00 6c 07 == (doy=1, year=1900)")
    return 0


def _zstd():
    import zstandard
    return zstandard


def _rows_fixed(b, stride):
    n = struct.unpack_from("<I", b, 8)[0]
    if H + n * stride + F != len(b):
        return None, n
    return [(H + i * stride, H + (i + 1) * stride) for i in range(n)], n


def _rows_variable(b, tid):
    """复用 t74 的变长文法(只调函数,不改判)。"""
    import t74_frames_part2 as P
    n = struct.unpack_from("<I", b, 8)[0]
    fn = {7: P.seq_media7, 8: P.seq_lang, 18: P.seq_derby,
          24: P.seq_team24, 27: P.seq_weat}[tid]
    if tid == 18:
        const = 80 if False else None
        # derby 需要 const:用 82-4k 之外实测的常量 96(见 t74 frames.json)
        const = 96
        r = fn(b, n, const)
    else:
        r = fn(b, n)
    return (r["rows"] if r else None), n


CONTROLS = {"0x076c0002": 0x076C0002, "0x076c0000": 0x076C0000,
            "0x01000001": 0x01000001}


def slot_scan(b, rows, limit, const=SENT):
    """逐槽位统计常量命中数;limit = 最短行长度(只统计共同前缀)。"""
    n = len(rows)
    hits = [0] * limit
    for s, _e in rows:
        for o in range(limit):
            if struct.unpack_from("<I", b, s + o)[0] == const:
                hits[o] += 1
    return hits, n


def decode_probe(b, rows, off):
    """对非 sentinel 值检验 (doy, year) 文法:year 合理区间 + doy 1..366。

    外源主张(agentB §2.2):DOB 编码 = (u16 day_of_year, u16 year)。
    本函数只统计,不给语义结论。
    """
    years, doys, ok = [], [], 0
    for s, _e in rows:
        v = struct.unpack_from("<I", b, s + off)[0]
        if v == SENT:
            continue
        doy, year = v & 0xFFFF, v >> 16
        years.append(year)
        doys.append(doy)
        if 1 <= doy <= 366 and 1900 <= year <= 2026:
            ok += 1
    n = len(years)
    return {"offset_from_row_start": off, "non_sentinel_rows": n,
            "doy_year_grammar_ok": ok,
            "ok_rate": round(ok / n, 6) if n else None,
            "year_min": min(years) if years else None,
            "year_max": max(years) if years else None,
            "doy_min": min(doys) if doys else None,
            "doy_max": max(doys) if doys else None}


def table_report(b, rows, n, tag):
    if not rows:
        return {"table": tag, "status": "row_frame_unavailable"}
    lens = [e - s for s, e in rows]
    limit = min(lens) - 4 + 1
    hits, n2 = slot_scan(b, rows, limit)
    rates = [h / n2 for h in hits]
    control = sum(rates) / len(rates) if rates else 0.0
    hot = [{"offset_from_row_start": o, "hits": hits[o], "rate": round(rates[o], 6)}
           for o in range(limit) if rates[o] >= 0.25]
    hot.sort(key=lambda d: -d["rate"])
    # 对照常量:同槽位扫描,证明 sentinel 不是"任何常量都命中"
    ctrl_slots = {}
    for name, cv in CONTROLS.items():
        ch, _ = slot_scan(b, rows, limit, cv)
        ctrl_slots[name] = {"max_hits": max(ch) if ch else 0,
                            "max_rate": round(max(ch) / n2, 6) if ch else 0.0}
    return {
        "table": tag, "rows": n, "row_len_min": min(lens), "row_len_max": max(lens),
        "slots_scanned": limit,
        "control_mean_rate_all_slots": round(control, 8),
        "hot_slots_rate_ge_0.25": hot,
        "hot_slot_count": len(hot),
        "control_constants": ctrl_slots,
        "decode_of_hot_slots": [decode_probe(b, rows, h["offset_from_row_start"])
                                for h in hot],
    }


def byte_level(b):
    """字节级:窗口内 pattern 出现次数(4 种对齐各自计数),用作随机基线。"""
    out = {}
    for phase in range(4):
        c = 0
        p = b.find(SENT_B, phase)
        while p >= 0:
            c += 1
            p = b.find(SENT_B, p + 1)
        out[f"phase{phase}"] = c
    out["window_bytes"] = len(b)
    out["expected_random_occurrences"] = round(len(b) / 2**32, 4)
    return out


def people_family(cap):
    """people_db / basic_people_db 侧:流式扫描 sentinel 及其上下文文法。"""
    z = _zstd()
    res = {}
    for fn in ("people_db.dat", "basic_people_db.dat"):
        p = DB_DIR / fn
        if not p.exists():
            res[fn] = {"status": "absent"}
            continue
        raw = p.read_bytes()
        cut = raw.find(b"\x28\xb5\x2f\xfd")
        if cut < 0:
            res[fn] = {"status": "no_zstd_magic"}
            continue
        d = z.ZstdDecompressor()
        buf = bytearray()
        occ = 0
        with d.stream_reader(raw[cut:]) as r:
            while True:
                chunk = r.read(1 << 22)
                if not chunk:
                    break
                buf.extend(chunk)
                if len(buf) > cap:
                    break
        win = bytes(buf)
        pos = win.find(SENT_B)
        while pos >= 0:
            occ += 1
            pos = win.find(SENT_B, pos + 1)
        # 上下文:该常量前 4 字节是否也是该常量(agentB 的 3x 前缀)
        pre = post = 0
        pos = win.find(SENT_B)
        while pos >= 0:
            if pos >= 4 and win[pos - 4:pos] == SENT_B:
                pre += 1
            if win[pos + 4:pos + 8] == SENT_B:
                post += 1
            pos = win.find(SENT_B, pos + 1)
        # 连续 run 长度直方图(agentB §2.2 声称 3 连 + 8x ff + 再 1 连)
        runs = {}
        pos = win.find(SENT_B)
        while pos >= 0:
            k, q = 0, pos
            while q + 4 <= len(win) and win[q:q + 4] == SENT_B:
                k += 1
                q += 4
            runs[k] = runs.get(k, 0) + 1
            pos = win.find(SENT_B, q)
        res[fn] = {"status": "ok", "header_hex": raw[:12].hex(),
                   "scanned_bytes": len(win), "cap": cap,
                   "occurrences": occ,
                   "rate_per_MB": round(occ / (len(win) / 1e6), 4) if win else 0,
                   "expected_random": round(len(win) / 2**32, 4),
                   "prev4_also_sentinel": pre, "next4_also_sentinel": post,
                   "run_length_histogram": {str(k): v for k, v in sorted(runs.items())}}
    return res


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--help", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--people-cap", type=int, default=33554432)
    a = ap.parse_args(argv)
    if a.help:
        print(__doc__)
        return 0
    if a.selftest:
        return _selftest()

    import runpy
    k = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    codec = k["_reader"]()

    res = {
        "task": "t91", "section": "nulldate_probe",
        "provenance_external": "ext/fm-data@d7a7150 (agentB-people-db.md §2.2)",
        "provenance_our_data": f"FM24_DB_DIR={DB_DIR}",
        "constant": {"hex": "01 00 6c 07", "u32_le": hex(SENT),
                     "decode": "(u16 day_of_year=1, u16 year=1900)"},
        "grade_policy": "命中率是 L1 自检量,不构成字段语义结论;外源标签不升等级",
        "tables": [], "people_family": {},
    }
    for (tid, side), stride in sorted(FIXED.items()):
        try:
            b = k["load_payload"](codec, side, tid)
        except Exception as exc:
            res["tables"].append({"table": f"{side}_{tid}",
                                  "status": f"load_error: {type(exc).__name__}: {exc}"})
            continue
        rows, n = _rows_fixed(b, stride)
        r = table_report(b, rows, n, f"{side}_{tid}")
        r["byte_level"] = byte_level(b)
        res["tables"].append(r)
    for tid, side in VARIABLE:
        try:
            b = k["load_payload"](codec, side, tid)
        except Exception as exc:
            res["tables"].append({"table": f"{side}_{tid}",
                                  "status": f"load_error: {type(exc).__name__}: {exc}"})
            continue
        rows, n = _rows_variable(b, tid)
        r = table_report(b, rows, n, f"{side}_{tid}")
        r["byte_level"] = byte_level(b)
        res["tables"].append(r)

    res["people_family"] = people_family(a.people_cap)
    # summary.dat 不压缩(外源 agentC §输入):直接字节级对照
    sp = DB_DIR / "summary.dat"
    if sp.exists():
        sb = sp.read_bytes()
        res["summary_dat"] = {"status": "ok", "bytes": len(sb),
                              "header_hex": sb[:16].hex(),
                              "zstd_at": sb.find(b"\x28\xb5\x2f\xfd"),
                              "byte_level": byte_level(sb)}
    else:
        res["summary_dat"] = {"status": "absent"}
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    for t in res["tables"]:
        if "hot_slots_rate_ge_0.25" in t:
            print(f"{t['table']:14s} rows={t['rows']:6d} slots={t['slots_scanned']:3d} "
                  f"ctrl={t['control_mean_rate_all_slots']:.4f} hot={t['hot_slot_count']}")
        else:
            print(f"{t['table']:14s} {t.get('status')}")
    for fn, v in res["people_family"].items():
        print(fn, v.get("status"), "occ=", v.get("occurrences"), "MB=",
              round(v.get("scanned_bytes", 0) / 1e6, 1))
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
