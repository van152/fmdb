#!/usr/bin/env python3
"""t91 verify: 独立复算 code_coverage.json(§2)与 nulldate_probe.json(§3)的计数。

设计:本脚本**不 import** t91_codes.py / t91_nulldate.py,而是各自重新实现
最小必要的读取与统计,用不同代码路径得到同一组数,再与落盘 JSON 比对。
不一致 -> 退出码 1 并打印差异。

用法:
  FM24_DB_DIR=... py -V:3.12 -I -B scratch/t91/out/verify.py [--help] [--selftest]
退出码: 0 全部一致 / 1 有不一致 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch/t91/out"
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
sys.path.insert(0, r"D:/tmp2b/fm24/tools/python")

SENT = 0x076C0001
H, F = 14, 8
FAILS: list[str] = []


def check(name, got, want):
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got={got!r} want={want!r}")
    if not ok:
        FAILS.append(name)
    return ok


def _selftest() -> int:
    assert struct.pack("<HH", 1, 1900) == bytes.fromhex("01006c07")
    assert struct.unpack("<HH", bytes.fromhex("01006c07")) == (1, 1900)
    print("selftest OK")
    return 0


# ---------------------------------------------------------------- §2 复算
def verify_codes():
    cc = json.loads((OUT / "code_coverage.json").read_text(encoding="utf-8"))
    m = json.loads(MASTER.read_text(encoding="utf-8"))
    fc = m["field_codes"]

    # 独立重建:从两份外源报告正文正则抽 `pers,XXXX` 码 + 表格里的 label。
    # agentA §3 只给出 16 条;PCJO/PSJO 来自 briefing.md §Key files。
    src = {}
    for name in ("agentA-native-re.md", "briefing.md"):
        p = ROOT / "scratch/ext/fm-data/docs/reports" / name
        txt = p.read_text(encoding="utf-8")
        codes = set(re.findall(r"`pers,([A-Za-z0-9]{2,6})`", txt))
        labels = dict(re.findall(
            r"\|\s*`pers,([A-Za-z0-9]{2,6})`\s*\|\s*([^|]+?)\s*\|", txt))
        # briefing.md 用 `pers,Xxx`=label 的行内形式
        labels.update(dict(re.findall(
            r"`pers,([A-Za-z0-9]{2,6})`\s*=\s*([A-Za-z][A-Za-z ]+?)[,.]", txt)))
        src[name] = (codes, labels)

    a_codes, a_labels = src["agentA-native-re.md"]
    b_codes, b_labels = src["briefing.md"]
    check("§2 agentA codes", len(a_codes), 16)
    check("§2 agentA labelled codes", len(a_labels), 16)
    check("§2 briefing adds PCJO/PSJO",
          sorted(b_codes - a_codes), ["PCJO", "PSJO"])
    found = a_codes | b_codes
    table = {**b_labels, **a_labels}

    check("§2 ext codes recoverable", len(found), 18)
    check("§2 ext codes with label", len(table), 18)

    present = sum(1 for c in found if c in fc)
    check("§2 both_present", present, 18)
    check("§2 they_have_we_lack", 18 - present, 0)
    check("§2 counts.they_have_we_lack",
          cc["section_code_table_diff"]["counts"]["they_have_we_lack"], 0)

    # 标签规范化后精确相等数(独立实现)
    def nz(s):
        if not s:
            return ""
        s = re.sub(r"[^a-z0-9]+", " ", s.lower())
        return " ".join(w for w in s.split() if w not in ("the", "of", "a", "an"))

    exact = 0
    for code, ext_lab in table.items():
        if code in fc and nz(fc[code].get("name")) == nz(ext_lab):
            exact += 1
    check("§2 label_exact_after_norm", exact, 14)
    check("§2 counts.both_label_exact",
          cc["section_code_table_diff"]["counts"]["both_label_exact_after_normalisation"], 14)

    check("§2 our distinct codes", len(fc), 3009)
    check("§2 our_code_space.distinct_field_codes",
          cc["our_code_space"]["distinct_field_codes"], 3009)

    pers = {c for c, v in fc.items()
            if any(l.rsplit("#", 1)[-1] == "pers" for l in v.get("locations", []))}
    check("§2 our pers codes", len(pers), 271)
    check("§2 our_code_space.pers_codes", cc["our_code_space"]["pers_codes"], 271)

    tags = set()
    for v in fc.values():
        for l in v.get("locations", []):
            tags.add(l.rsplit("#", 1)[-1])
    check("§2 our distinct tags", len(tags), 395)

    check("§2 natc absent in ours", "natc" in tags, False)
    check("§2 external_tags_missing_in_ours",
          cc["section_code_table_diff"]["table_tags"]["external_tags_missing_in_ours"], ["natc"])
    check("§2 external commit pinned",
          cc["provenance"]["external"], "ext/fm-data@d7a7150")


# ---------------------------------------------------------------- §3 复算
def _zstd():
    import zstandard
    return zstandard


def verify_nulldate():
    np_ = json.loads((OUT / "nulldate_probe.json").read_text(encoding="utf-8"))
    by = {t["table"]: t for t in np_["tables"] if "hot_slots_rate_ge_0.25" in t}

    # 独立重算 server_21:自己解 zstd、自己算行框(定长 181)
    # 容器解析用我们自己的加载器(fm24_dump.load_payload);
    # 独立性体现在**统计与判据**重写,不在重复实现 FMF 目录解析。
    import runpy
    k = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    codec = k["_reader"]()
    b = k["load_payload"](codec, "server", 21)
    assert b.startswith(bytes.fromhex("03017461642ef10d")), "payload head"
    n = struct.unpack_from("<I", b, 8)[0]
    check("§3 server_21 rows", n, 48413)
    check("§3 server_21 payload_len", len(b), 8762775)
    stride = (len(b) - H - F) // n
    check("§3 server_21 stride", stride, 181)

    # 逐槽位命中率,独立算法(字节 find 而非逐行 unpack)
    hits = {}
    for o in range(stride - 3):
        c = 0
        for r in range(n):
            p = H + r * stride + o
            if b[p:p + 4] == b"\x01\x00\x6c\x07":
                c += 1
        if c:
            hits[o] = c
    full = sorted(o for o, c in hits.items() if c == n)
    check("§3 server_21 rate==1.0 slots", full, [156])
    check("§3 JSON agrees (156)", [h["offset_from_row_start"]
                                   for h in by["server_21"]["hot_slots_rate_ge_0.25"]
                                   if h["rate"] == 1.0], [156])

    # 关键槽位命中数逐个对齐 JSON
    jh = {h["offset_from_row_start"]: h["hits"]
          for h in by["server_21"]["hot_slots_rate_ge_0.25"]}
    for o, want in ((37, 38211), (41, 44879), (45, 45864), (131, 46533),
                    (135, 48231), (156, 48413)):
        check(f"§3 server_21 slot+{o} hits", hits.get(o), want)
        check(f"§3 JSON slot+{o} hits", jh.get(o), want)

    # (doy, year) 文法:独立重算 row+131 与 row+37
    for o, want_rows, want_ok in ((131, 1880, 1880), (37, 10202, 10094)):
        tot = ok = 0
        for r in range(n):
            p = H + r * stride + o
            v = struct.unpack_from("<I", b, p)[0]
            if v == SENT:
                continue
            tot += 1
            doy, yr = v & 0xFFFF, v >> 16
            if 1 <= doy <= 366 and 1900 <= yr <= 2026:
                ok += 1
        check(f"§3 row+{o} non_sentinel_rows", tot, want_rows)
        check(f"§3 row+{o} grammar_ok", ok, want_ok)

    # client_21 定长 38,row+13 = 100%
    bc = k["load_payload"](codec, "client", 21)
    nc = struct.unpack_from("<I", bc, 8)[0]
    check("§3 client_21 rows", nc, 48413)
    sc = (len(bc) - H - F) // nc
    check("§3 client_21 stride", sc, 38)
    c13 = sum(1 for r in range(nc)
              if bc[H + r * sc + 13: H + r * sc + 17] == b"\x01\x00\x6c\x07")
    check("§3 client_21 row+13 hits", c13, 48413)

    # 对照常量在 client_21 全槽位的最高命中(应为 0)
    best = 0
    for o in range(sc - 3):
        c = sum(1 for r in range(nc)
                if bc[H + r * sc + o: H + r * sc + o + 4] == b"\x02\x00\x6c\x07")
        best = max(best, c)
    check("§3 control 0x076c0002 max hits in client_21", best, 0)
    check("§3 JSON control agrees",
          by["client_21"]["control_constants"]["0x076c0002"]["max_hits"], 0)

    # people_db 侧:小窗口重扫,核对量级
    d = _zstd().ZstdDecompressor()
    pr = (DB_DIR / "people_db.dat").read_bytes()
    cut = pr.find(b"\x28\xb5\x2f\xfd")
    with d.stream_reader(pr[cut:]) as r:
        win = r.read(1 << 22)
    occ = win.count(b"\x01\x00\x6c\x07")
    jp = np_["people_family"]["people_db.dat"]
    check("§3 people_db scanned_bytes", jp["scanned_bytes"], 37748736)
    # 4MiB 窗口按同一密度缩放应落在 [occ*8, occ*11] 内
    lo, hi = occ * 8, occ * 11
    check("§3 people_db occurrences in scaled band",
          lo <= jp["occurrences"] <= hi, True)
    check("§3 basic_people_db near-zero occurrences",
          np_["people_family"]["basic_people_db.dat"]["occurrences"] < 100, True)
    check("§3 summary.dat has no zstd", np_["summary_dat"]["zstd_at"], -1)
    check("§3 summary.dat null-date occurrences",
          np_["summary_dat"]["byte_level"]["phase0"]
          + np_["summary_dat"]["byte_level"]["phase1"]
          + np_["summary_dat"]["byte_level"]["phase2"]
          + np_["summary_dat"]["byte_level"]["phase3"], 0)


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--help", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.help:
        print(__doc__)
        return 0
    if a.selftest:
        return _selftest()
    print("== §2 code table ==")
    verify_codes()
    print("== §3 nulldate probe ==")
    verify_nulldate()
    print()
    if FAILS:
        print(f"FAILED {len(FAILS)}: {FAILS}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
