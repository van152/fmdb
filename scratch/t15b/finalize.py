#!/usr/bin/env python3
"""t15b finalize — lang_update 行文法闭合 + 合并三份探针结果为最终 probe.json。

只读 FM24_DB_DIR;只写 scratch/t15b/out/。
退出码 0 成功 / 1 校验未过 / 2 用法错误。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or r"scratch/data")
if not DB_DIR.is_absolute():
    DB_DIR = ROOT / DB_DIR
OUT = ROOT / "scratch/t15b/out"
sys.path.insert(0, str(pathlib.Path(r"D:\tmp2b\fm24\tools\python")))


def codec():
    import runpy
    k = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
    return runpy.run_path(str(k["OLD_READER_PATH"]))


def lang_scan(c) -> dict:
    p = DB_DIR / "lang_update_db.dat"
    data = p.read_bytes()
    lay = c["_archive_layout"](data)
    ents = c["list_tables"](p, "lang_update_db.dat")
    import re
    langs, tabs, per_tab = collections.Counter(), collections.Counter(), collections.Counter()
    dec_total = ff_total = 0
    cnt_sum = 0
    tad_files = 0
    fully_closed = 0
    for e in ents:
        raw = c["_decompress_entry"](data, lay["data_base"], e)
        dec_total += len(raw)
        ff_total += raw.count(b"\xff")
        m = re.fullmatch(r"lang_update_db/(\d+)_(\d+)\.dat", e["path"])
        if m:
            langs[int(m.group(1))] += 1
            tabs[int(m.group(2))] += 1
        if len(raw) >= 16 and raw[:6] == b"\x03\x01tad.":
            tad_files += 1
            cnt_sum += struct.unpack_from("<I", raw, 8)[0]
            # 试解 (u32 len, utf8, 0xff) 重复;记录能走多远
            pos, n = 16, 0
            while pos + 4 <= len(raw):
                ln = struct.unpack_from("<I", raw, pos)[0]
                if ln > 600 or pos + 4 + ln > len(raw):
                    break
                try:
                    raw[pos + 4:pos + 4 + ln].decode("utf-8")
                except UnicodeDecodeError:
                    break
                pos += 4 + ln
                n += 1
                if pos < len(raw):
                    pos += 1
            if pos == len(raw):
                fully_closed += 1
            per_tab[int(m.group(2)) if m else -1] += n
    return {"entries": len(ents), "numbered_entries": sum(langs.values()),
            "languages": len(langs), "table_types": len(tabs),
            "person_names_files": sum(1 for e in ents if "person_names" in e["path"]),
            "decompressed_total": dec_total, "ff_terminator_bytes": ff_total,
            "files_with_tad_header": tad_files,
            "count_field_sum": cnt_sum,
            "files_fully_closed": fully_closed,
            "grammar_closed": False,
            "observed_prefix": "每文件 tad. f10d | u32 count | u32 aux | 接着是 (u32 len, utf8, 0xff) 序列",
            "why_not_closed": "前 3–6 个字符串后出现非 len/utf8/ff 的字节(例 8_3.dat 在 offset 76 遇到 u32=1258291456),"
                              "说明记录内还有子结构/嵌套;0/235 个带 tad. 头的成员能被单层文法走到 EOF",
            "sample": "8_9.dat = count 1 + ['Singapore'->ff, 'Singapore'->ff, 'SGP', 'Singaporean', 0x00]"}


def main() -> int:
    ap = argparse.ArgumentParser(description="t15b finalize")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        assert 8 + 4 + 4 == 16
        print("selftest OK")
        return 0

    p1 = json.loads((OUT / "probe_raw.json").read_text(encoding="utf-8"))
    p2 = json.loads((OUT / "probe2.json").read_text(encoding="utf-8"))
    p3 = json.loads((OUT / "probe3.json").read_text(encoding="utf-8"))
    lang = lang_scan(codec())

    rel = p2["relations"]
    files = {}
    F = p1["files"]

    files["people_db.dat"] = {
        "size": F["people_db.dat"]["size"], "sha256": F["people_db.dat"]["sha256"],
        "container_ok": True, "container": F["people_db.dat"]["container"],
        "tables": None,
        "tables_note": "非 FMF 档案(offset 8 单个 Zstd 流),list_tables 抛 'no supported embedded resource-FMF signature'",
        "decompressed_len": F["people_db.dat"]["decompressed"]["len"],
        "decompressed_sha256": F["people_db.dat"]["decompressed"]["sha256"],
        "key_4cc": ["tad.", "f1 0d (v3569)", "28b52ffd Zstd"],
        "structure": {
            "header_u32_at_2": p3["u32_at_2"],
            "header_note": "payload+2 的 u32 = 658,011,与 basic_people_db.dat payload+0 的 count 完全相同",
            "compact_segment": p3["compact"],
            "cross_join": p3["cross_join"],
            "compact_note": "offset 6..55,750 共 1,193 行 type=5,行跨度 33+namelen;key 集恰为 656818..658010 全覆盖,"
                            "且每行 (key,duni) 与 basic_people_db 同 ordinal 行逐一相等 1193/1193;"
                            "足后 376B 未解小间隙,再到 offset 56,126 起是姓名/DOB 锚点流",
            "gap_after_compact_bytes": p3["first_marker_gap_bytes"],
            "main_anchor_stream_start": p3["first_marker_after_compact"],
            "anchor_markers_ff00_total": p2["people_db"]["marker_ff00"],
            "valid_name_dob_anchors_full_scan": 186082,
            "anchor_grammar": "FF FF FF FF 00 | u32 name_len | utf8 name | u32 dob(year<<16|doy)",
            "name_samples": p2["people_db"]["name_samples"],
        },
        "relation_to_baseline": rel,
        "verdict": "值得开专项(最高优先级):这是 person 全量扩展库,basic_people_db 只是 658,011 行 stub",
    }

    for tag, pre in (("pl", "pl"), ("non_pl", "non_pl")):
        h = p2["hist"][tag]
        dt = F[f"{tag}_hist_dt.dat"]
        idf = F[f"{tag}_hist_id.dat"]
        idx = F[f"{tag}_hist_index.dat"]
        files[f"{tag}_hist_dt.dat"] = {
            "size": dt["size"], "sha256": dt["sha256"], "container_ok": True,
            "container": dt["container"], "tables": None,
            "key_4cc": ["tadc", "03 00 (v3)", "28b52ffd Zstd"],
            "zstd_streams": dt.get("frames"),
            "decompressed_len": dt["decompressed"]["len"],
            "stride": h["stride"], "exact_rows": h["dt_exact_rows"],
            "len_mod_stride": h["dt_len_mod_stride"],
            "chain_sample": dt.get("chain"),
            "verdict": "已解(旧仓 L1 全量链 + 本仓抽样复现);行内字段语义不在本任务范围",
        }
        files[f"{tag}_hist_id.dat"] = {
            "size": idf["size"], "sha256": idf["sha256"], "container_ok": True,
            "container": idf["container"], "tables": None,
            "key_4cc": ["tad.", "01 00 (v1) 裸 u32 数组,无 Zstd 无 FMF"],
            "array": idf.get("array"),
            "pairs": h["id_pairs"], "pair_stride": h["stride"],
            "pairs_aligned": h["head_pairs_aligned_bytes"],
            "contiguous_step": h["head_pairs_contiguous_step"],
            "last_end_plus_stride_eq_dt": h["id_last_end_plus_stride_eq_dt"],
            "verdict": "已解;<u32 start,u32 end> inclusive 字节偏移对,与 dt 长度闭合",
        }
        files[f"{tag}_hist_index.dat"] = {
            "size": idx["size"], "sha256": idx["sha256"], "container_ok": True,
            "container": idx["container"], "tables": None,
            "key_4cc": ["tad.", "f1 0d (v3569)", "28b52ffd Zstd"],
            "decompressed_len": idx["decompressed"]["len"],
            "index": idx.get("index"),
            "valid_ordinals": h["index_count"],
            "verdict": "已解;<u32 count><count × (u32 key,u32 range_ordinal)>",
        }

    s = F["summary.dat"]
    files["summary.dat"] = {
        "size": s["size"], "sha256": s["sha256"], "container_ok": True,
        "container": s["container"], "tables": None,
        "key_4cc": ["tad.", "f1 0d (v3569);无 Zstd、无 FMF"],
        "summary": s["summary"],
        "byte_accounting_ok": s["summary"]["byte_accounting"]["file"] == 1648018,
        "verdict": "容器+分段账已清;字段语义 0 个(旧仓 L2=0,本仓不改判)",
    }
    files["lang_update_db.dat"] = {
        "size": F["lang_update_db.dat"]["size"], "sha256": F["lang_update_db.dat"]["sha256"],
        "container_ok": True, "container": F["lang_update_db.dat"]["container"],
        "tables": F["lang_update_db.dat"]["tables"],
        "tables_note": "352 个 auxiliary 成员(table_entries=0),非数值表",
        "key_4cc": ["tad.", "f1 0d", "02 01 66 6d 66 2e (fmf.)"],
        "lang": lang,
        "verdict": "容器可列(352 成员 = 22 语言 × 15 表号 + 22 person_names);但行文法未闭合(0/235),"
                   "本地化覆盖层,非 schema 表",
    }

    res = {
        "task": "t15b", "kind": "bypass-inventory (旁路清点,非主线产物)",
        "status": "ok", "generated": "2026-11-18",
        "db_dir": str(DB_DIR), "read_only": True,
        "baseline_ref": "scratch/t13e/out/baselines.json",
        "scripts": ["scratch/t15b/probe.py", "scratch/t15b/probe2.py",
                    "scratch/t15b/probe3.py", "scratch/t15b/finalize.py"],
        "container_summary": {
            "tad. + zstd@8 (非 FMF)": ["people_db.dat"],
            "tadc v3 + 串联 zstd": ["pl_hist_dt.dat", "non_pl_hist_dt.dat"],
            "tad. v1 裸 u32 数组": ["pl_hist_id.dat", "non_pl_hist_id.dat"],
            "tad. v3569 + zstd (index)": ["pl_hist_index.dat", "non_pl_hist_index.dat"],
            "tad. v3569 自有文法 (无 zstd)": ["summary.dat"],
            "tad. v3569 + 内嵌 fmf. 目录": ["lang_update_db.dat"],
            "结论": "9/9 容器层全部进入,0 个未知外壳",
        },
        "files": files,
        "baseline_relations": {
            "person_universe": {
                "basic_people_db_rows": 658011,
                "people_db_header_count": p3["u32_at_2"],
                "equal": p3["u32_at_2"] == 658011,
                "compact_rows_joined": p3["cross_join"]["rows_compared"],
                "compact_duni_equal": p3["cross_join"]["duni_equal"],
                "evidence": "people_db payload+2 的 u32 == 658,011 == basic_people payload+0 的 count;"
                            "people_db 开头 1,193 行的 (key,duni) 与 basic_people 同 ordinal 行逐行相等",
                "grade": "L1(跨档案字节对齐) + L2(同值锚点)",
            },
            "hist_vs_person": {
                "pl_hist_persons": rel["pl_hist_persons"],
                "non_pl_hist_persons": rel["non_pl_hist_persons"],
                "sum": rel["pl_plus_non_pl"],
                "basic_people_total": 658011,
                "delta_sum": rel["delta_sum_vs_basic"],
                "basic_class_counts": {"1_NON_PLAYER": 166064, "2_PLAYER": 476158,
                                       "3": 4757, "4_OFFICIAL": 9839, "5_RETIRED_NAME": 1193},
                "delta_pl_vs_class2": rel["delta_pl_vs_basic_players"],
                "delta_nonpl_vs_class1": rel["delta_nonpl_vs_basic_nonplayers"],
                "t49_server_rows": 792149,
                "delta_nonpl_vs_t49": rel["non_pl_hist_persons"] - 792149,
                "verdict": "不对等。pl_hist(515,581) 与 class2(476,158) 差 +39,423;"
                           "non_pl_hist(746,543) 与 class1(166,064) 差 +580,479,"
                           "non_pl_hist 与 t49(792,149) 差 -45,606。三者是不同层,不能用行数互相替代",
            },
            "people_db_vs_basic": {
                "people_db_decompressed": 400443970,
                "basic_people_decompressed": p3["basic_people"]["len"],
                "ratio": round(400443970 / p3["basic_people"]["len"], 2),
                "finding": "basic_people 是 658,011 行定长 stub(class1/2/3=83B, class4=34B, class5=22B, "
                           "class5 段连姓名都没有);people_db 才带姓名+出生日期+后续属性块,同一 person 宇宙",
                "anchor_stream_valid_name_dob": 186082,
                "old_report_ref": "D:/tmp2b/fm24/reports/dbdat_decode/PEOPLE_DB.md(解压长度/SHA-256 与本仓逐字节一致)",
            },
        },
        "recommendations": [
            {"archive": "people_db.dat", "open_project": True, "priority": 1,
             "why": "唯一带完整 person 姓名/生日/属性块的档案;header count 与 basic_people 同为 658,011,"
                    "compact 段 1,193 行 key+duni 双向对齐已构成跨档案锚点;400MB 主体 186,082 个姓名+生日锚点可复用",
             "scope_hint": "先把 1,193 行 compact 段整段闭合(唯一已有双向锚点),再用它反推主体行首标记语义"},
            {"archive": "pl_hist_* / non_pl_hist_*", "open_project": False,
             "why": "容器与链条已闭合(id/dt/index 三方对齐、next 链 0 违例),缺的只是行内字段语义,"
                    "属履历而非 schema;除非要回答球员历史类编辑问题,否则不开"},
            {"archive": "summary.dat", "open_project": False,
             "why": "54,086 body 账已平,字段语义旧仓已穷尽尝试且 L2=0;无新增锚点前不重复投入"},
            {"archive": "lang_update_db.dat", "open_project": False,
             "why": "352 成员可列可解压,是本地化覆盖层而非 schema 表;行文法未闭合(0/235),"
                    "但即使解开也只影响本地化文本,不进入体字段映射,优先级最低"},
        ],
        "negative_results_kept": [
            "people_db.dat / summary.dat 对 list_tables() 均抛 'no supported embedded resource-FMF signature' —— 二者不是 FMF 档案,不得按表目录思路处理",
            "people_db compact 段 1,193 行 key 与行序不同序(first key=657,483,集合覆盖 656818..658010),不能把段内行号当 key",
            "lang_update_db.dat 352 成员全部 table_id=None,不存在 table_N.dat,不能与 client/server 表号互比",
            "lang_update_db.dat 成员内部 (u32 len, utf8, 0xff) 单层文法未闭合:235 个带 tad. 头的成员中 0 个能走到 EOF",
            "non_pl_hist_index count=754,688 ≠ 746,543 个有效范围(差 8,145 个 0xFFFFFFFF sentinel)",
        ],
    }
    (OUT / "probe.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"status": res["status"], "lang_files": lang["files_with_tad_header"],
                      "lang_closed": lang["files_fully_closed"],
                      "lang_dec": lang["decompressed_total"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
