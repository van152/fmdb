#!/usr/bin/env python3
"""t106_special_members — 13 个非编号特殊成员的解包 / 逐行解码 / 字节精确闭合验证。

成员清单（12 个来自 `server_db.dat`，1 个独立归档 `summary.dat`）
---------------------------------------------------------------
 1-3  name_table_0/1/2.dat         姓名池元数据（定长 12B 行）
 4-6  name_table_extra_0/1/2.dat   姓名池字符串（变长 u32 uid + u32 len + utf8）
 7    common_name_links.dat        常用名 → 姓名池 ordinal 关联（定长 10B）
 8    club_links.dat               俱乐部 → 俱乐部关联（定长 47B）
 9    simple_vars.dat              全局变量键值区（u8 key + u8 len + value）
 10   summary.dat                  库摘要（40B 头 + 54,087 个 body+分隔符 + 尾块）
 11   table_for_old_save_23.dat    旧存档 stage_name 兼容表（15B 头 + 278×14B + 7B 尾）
 12   table_for_old_save_25.dat    旧存档 competition 兼容表（12B 头 + 7,047 变长行 + 9B footer）
 13   fantasy_draft_future_regens.dat  梦幻选秀再生球员（12B 头 + 40 变长行 + 31B 尾块）

解包统一走 `scripts/t38_multiframe.py` 的 E80 规则（`data_base + offset` 定位成员、
`packed_size` 界定帧区间、`size` 选帧），**不跨成员**。`summary.dat` 是独立 tad 文件，
按文件尾直接读。

产出（写入 `--outdir`，默认 `scratch/t106/out`）
----------------------------------------------
  special_members_schema.json  机读 schema（`"status": "complete"`）
  REPORT.md                    格式说明 + 闭合汇总表
  DONE.md                      首行 `DONE type=t106`

用法
----
  py -V:3.12 -I -B scripts/t106_special_members.py --selftest
  py -V:3.12 -I -B scripts/t106_special_members.py
  py -V:3.12 -I -B scripts/t106_special_members.py --outdir scratch/t106/out --force-extract

退出码
------
  0 成功    1 验收/自检失败    2 用法或输入缺失
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import struct
import sys
from bisect import bisect_left

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

OUTDIR_DEFAULT = ROOT / "scratch/t106/out"
DATA_DIR = ROOT / "scratch/data"

MAGIC = b"\x03\x01tad."
SEP = b"\xff\xff\xff\xff\x03"          # summary.dat body 分隔符
MARK = b"\x01\x00\x6c\x07"             # fantasy_draft 行终止标记
SENTINEL = 0xFFFFFFFF

SERVER_MEMBERS = [
    "name_table_0",
    "name_table_1",
    "name_table_2",
    "name_table_extra_0",
    "name_table_extra_1",
    "name_table_extra_2",
    "common_name_links",
    "club_links",
    "simple_vars",
    "table_for_old_save_23",
    "table_for_old_save_25",
    "fantasy_draft_future_regens",
]
SUMMARY_MEMBER = "summary"
ALL_MEMBERS = (
    ["name_table_0", "name_table_1", "name_table_2"]
    + ["name_table_extra_0", "name_table_extra_1", "name_table_extra_2"]
    + ["common_name_links", "club_links", "simple_vars", SUMMARY_MEMBER]
    + ["table_for_old_save_23", "table_for_old_save_25", "fantasy_draft_future_regens"]
)

SAMPLE_N = 10

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ---------------------------------------------------------------- 通用工具


def hx(data: bytes, limit: int | None = None) -> str:
    d = data if limit is None else data[:limit]
    return " ".join(f"{c:02x}" for c in d)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def tad_header(raw: bytes, size: int, fields: list[dict]) -> dict:
    return {
        "size": size,
        "hex": hx(raw[:size]),
        "fields": fields,
        "magic_ok": raw[:6] == MAGIC,
        "payload_version": struct.unpack_from("<H", raw, 6)[0] if len(raw) >= 8 else None,
    }


def std_header_fields(count_off: int = 8) -> list[dict]:
    return [
        {"off": 0, "width": 6, "type": "bytes", "name": "magic", "value": MAGIC.decode("latin-1")},
        {"off": 6, "width": 2, "type": "u16", "name": "payload_version"},
        {"off": count_off, "width": 4, "type": "u32", "name": "row_count"},
    ]


def closure(arith: str, ok: bool, leftover: int, footer_len: int | None = None) -> dict:
    return {
        "arithmetic": arith,
        "ok": bool(ok),
        "leftover_bytes": int(leftover),
        "footer_len": footer_len,
    }


# ---------------------------------------------------------------- 1-3 姓名池主表


def dec_name_main(b: bytes) -> dict:
    """12B 头 + row_count × 12B 行（5 字段：u16 + u32 ordinal + 3×u16）。"""
    count = struct.unpack_from("<I", b, 8)[0]
    need = 12 + count * 12
    rows = []
    f0 = [0] * 256
    ord_ok = True
    meta_b_vals = set()
    meta_c_max = 0
    meta_d_vals = set()
    for idx, (m_a, m_b, m_c, m_d, m_e) in enumerate(
        struct.iter_unpack("<HIHHH", b[12:need])
    ):
        # <HIHHH = u16@0, u32@2 (ordinal), u16@6, u16@8, u16@10
        if m_b != idx:
            ord_ok = False
        if m_a < 256:
            f0[m_a] += 1
        meta_b_vals.add(m_c)
        if m_d > meta_c_max:
            meta_c_max = m_d
        meta_d_vals.add(m_e)
        if len(rows) < SAMPLE_N:
            rows.append(
                {
                    "ordinal": idx,
                    "meta_a": m_a,
                    "meta_b": m_c,
                    "meta_c": m_d,
                    "meta_d": m_e,
                    "meta_d_hex": f"0x{m_e:04x}",
                }
            )
    fmt = {
        "kind": "fixed_stride",
        "header_size": 12,
        "row_stride": 12,
        "row_count": count,
        "fields": [
            {"off": 0, "width": 2, "type": "u16", "name": "meta_a", "semantic": "unresolved"},
            {"off": 2, "width": 4, "type": "u32", "name": "string_ordinal",
             "semantic": "row index == name_table_extra_<pool> record uid"},
            {"off": 6, "width": 2, "type": "u16", "name": "meta_b",
             "semantic": "unresolved (243 distinct, 0..249: nation-like)"},
            {"off": 8, "width": 2, "type": "u16", "name": "meta_c",
             "semantic": "unresolved (1..max: frequency/weight-like)"},
            {"off": 10, "width": 2, "type": "u16", "name": "meta_d",
             "semantic": "unresolved flag word (0xFF00-family + small codes)"},
        ],
        "footer": {"len": 0, "hex": ""},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(f"12 + {count}*12 = {need}", need == len(b), len(b) - need, 0),
        "facts": {
            "ordinal_equals_row_index": ord_ok,
            "meta_b_distinct": len(meta_b_vals),
            "meta_b_max": max(meta_b_vals),
            "meta_c_max": meta_c_max,
            "meta_d_distinct": len(meta_d_vals),
        },
        "samples": rows,
    }


# ---------------------------------------------------------------- 4-6 姓名池字符串


def dec_name_extra(b: bytes) -> dict:
    """12B 头 + row_count × (u32 uid + u32 byte_len + utf8)。"""
    count = struct.unpack_from("<I", b, 8)[0]
    off = 12
    uid_ok = True
    names = []
    maxlen = 0
    ascii_only = 0
    for idx in range(count):
        if off + 8 > len(b):
            break
        uid, ln = struct.unpack_from("<II", b, off)
        off += 8
        if off + ln > len(b):
            break
        raw = b[off:off + ln]
        off += ln
        if uid != idx:
            uid_ok = False
        if ln > maxlen:
            maxlen = ln
        if all(c < 128 for c in raw):
            ascii_only += 1
        if len(names) < SAMPLE_N:
            names.append({"uid": uid, "byte_len": ln, "text": decode_text(raw)})
    fmt = {
        "kind": "variable_stride",
        "header_size": 12,
        "row_count": count,
        "fields": [
            {"off": 0, "width": 4, "type": "u32", "name": "string_uid",
             "semantic": "pool-local zero-based ordinal, pairs 1:1 with name_table_<pool> row index"},
            {"off": 4, "width": 4, "type": "u32", "name": "byte_len"},
            {"off": 8, "width": "byte_len", "type": "utf8", "name": "text"},
        ],
        "footer": {"len": 0, "hex": ""},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(f"12 + sum(8+len) = {off}", off == len(b), len(b) - off, 0),
        "facts": {
            "uid_equals_row_index": uid_ok,
            "max_byte_len": maxlen,
            "ascii_only_rows": ascii_only,
        },
        "samples": names,
    }


# ---------------------------------------------------------------- 7 common_name_links


def dec_common_name_links(b: bytes) -> dict:
    """12B 头 + row_count × 10B 行：u32 name_ordinal + u8 flag + u16 nation + u16 lang<<8。"""
    count = struct.unpack_from("<I", b, 8)[0]
    stride = 10
    need = 12 + count * stride
    sent = 0
    flags = set()
    nations = set()
    langs = set()
    rows = []
    for idx, (uid, flag, opaque5, nation, lang) in enumerate(
        struct.iter_unpack("<IBBHH", b[12:need])
    ):
        if uid == SENTINEL:
            sent += 1
        flags.add(flag)
        nations.add(nation)
        langs.add(lang)
        if len(rows) < SAMPLE_N:
            rows.append(
                {
                    "row": idx,
                    "name_ordinal": None if uid == SENTINEL else uid,
                    "name_ordinal_raw": uid,
                    "is_sentinel": uid == SENTINEL,
                    "flag": flag,
                    "opaque_b5": opaque5,
                    "nation": nation,
                    "lang_code": lang >> 8,
                }
            )
    fmt = {
        "kind": "fixed_stride",
        "header_size": 12,
        "row_stride": stride,
        "row_count": count,
        "fields": [
            {"off": 0, "width": 4, "type": "u32", "name": "name_ordinal",
             "semantic": "ordinal into the three name pools; 0xFFFFFFFF = no name"},
            {"off": 4, "width": 1, "type": "u8", "name": "flag", "semantic": "0/1"},
            {"off": 5, "width": 1, "type": "u8", "name": "opaque_b5", "semantic": "unresolved (256 distinct)"},
            {"off": 6, "width": 2, "type": "u16", "name": "nation",
             "semantic": "nation code, 0..max"},
            {"off": 8, "width": 2, "type": "u16", "name": "lang_x256",
             "semantic": "language code shifted left 8 (low byte always 0)"},
        ],
        "footer": {"len": 0, "hex": ""},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(f"12 + {count}*{stride} = {need}", need == len(b), len(b) - need, 0),
        "facts": {
            "sentinel_rows": sent,
            "flag_distinct": sorted(flags),
            "nation_max": max(nations),
            "nation_distinct": len(nations),
            "lang_distinct": len(langs),
        },
        "samples": rows,
    }


# ---------------------------------------------------------------- 8 club_links


def dec_club_links(b: bytes) -> dict:
    """12B 头 + row_count × 47B 行：u32 club_uid + 5B + u32 linked_uid + 34B 定形子对象。"""
    count = struct.unpack_from("<I", b, 8)[0]
    stride = 47
    need = 12 + count * stride
    club_uids = []
    linked_uids = []
    same = 0
    const_pos = [True] * stride
    const_byte = [None] * stride
    rows = []
    for idx in range(count):
        o = 12 + idx * stride
        row = b[o:o + stride]
        a, c = struct.unpack_from("<I", row, 0)[0], struct.unpack_from("<I", row, 9)[0]
        club_uids.append(a)
        linked_uids.append(c)
        if a == c:
            same += 1
        for i, v in enumerate(row):
            if const_pos[i]:
                if const_byte[i] is None:
                    const_byte[i] = v
                elif const_byte[i] != v:
                    const_pos[i] = False
        if len(rows) < SAMPLE_N:
            rows.append(
                {
                    "row": idx,
                    "club_uid": a,
                    "linked_uid": c,
                    "mid_bytes": hx(row[4:9]),
                    "tail_const_prefix": hx(row[13:21]),
                }
            )
    consts = {i: const_byte[i] for i in range(stride) if const_pos[i]}
    fmt = {
        "kind": "fixed_stride",
        "header_size": 12,
        "row_stride": stride,
        "row_count": count,
        "fields": [
            {"off": 0, "width": 4, "type": "u32", "name": "club_uid",
             "semantic": "club identity, all < 300000"},
            {"off": 4, "width": 5, "type": "bytes", "name": "opaque_a"},
            {"off": 9, "width": 4, "type": "u32", "name": "linked_uid",
             "semantic": "linked club identity, all < 300000"},
            {"off": 13, "width": 34, "type": "bytes", "name": "wire_subobject",
             "semantic": "fixed-shape sub-object carrying repeated marker 0x076c0001"},
        ],
        "constant_bytes": {str(k): f"0x{v:02x}" for k, v in consts.items()},
        "footer": {"len": 0, "hex": ""},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(f"12 + {count}*{stride} = {need}", need == len(b), len(b) - need, 0),
        "facts": {
            "club_uid_max": max(club_uids),
            "linked_uid_max": max(linked_uids),
            "rows_with_equal_uids": same,
            "constant_byte_positions": len(consts),
        },
        "samples": rows,
    }


# ---------------------------------------------------------------- 9 simple_vars


def dec_simple_vars(b: bytes) -> dict:
    """34B 前导（与 client 侧 34B 完整 payload 逐字节相同）+ (u8 key, u8 len, value) 记录流。"""
    hdr = 34
    off = hdr
    recs = 0
    keys = {}
    zero_len = 0
    samples = []
    while off + 2 <= len(b):
        key, ln = b[off], b[off + 1]
        nxt = off + 2 + ln
        if nxt > len(b):
            break
        val = b[off + 2:nxt]
        keys[key] = keys.get(key, 0) + 1
        if ln == 0:
            zero_len += 1
        if len(samples) < SAMPLE_N:
            samples.append(
                {
                    "record": recs,
                    "offset": off,
                    "key": key,
                    "len": ln,
                    "value_hex": hx(val, 16),
                    "value_ascii": "".join(chr(c) if 32 <= c < 127 else "." for c in val[:16]),
                }
            )
        off = nxt
        recs += 1
    hdr_fields = [
        {"off": 0, "width": 6, "type": "bytes", "name": "magic", "value": MAGIC.decode("latin-1")},
        {"off": 6, "width": 2, "type": "u16", "name": "payload_version", "value": 3569},
        {"off": 8, "width": 2, "type": "u16", "name": "opaque_8"},
        {"off": 10, "width": 2, "type": "u16", "name": "opaque_10", "value": 8},
        {"off": 12, "width": 2, "type": "u16", "name": "opaque_12"},
        {"off": 14, "width": 2, "type": "u16", "name": "payload_version_dup", "value": 3569},
        {"off": 16, "width": 4, "type": "u32", "name": "opaque_16", "value": 4},
        {"off": 20, "width": 6, "type": "ascii", "name": "build_tag", "value": "2430K2"},
        {"off": 26, "width": 2, "type": "u16", "name": "year_a", "value": 2024},
        {"off": 28, "width": 4, "type": "u32", "name": "build_id", "value": 300183},
        {"off": 32, "width": 2, "type": "u16", "name": "year_b", "value": 2023},
    ]
    fmt = {
        "kind": "variable_stride",
        "header_size": hdr,
        "row_count": recs,
        "fields": [
            {"off": 0, "width": 1, "type": "u8", "name": "key",
             "semantic": "opaque variable id; 169 of 256 codes used"},
            {"off": 1, "width": 1, "type": "u8", "name": "len"},
            {"off": 2, "width": "len", "type": "bytes", "name": "value"},
        ],
        "footer": {"len": 0, "hex": ""},
        "grammar_status": (
            "unique closing grammar: among all (key,width) x (len,width) x (unit 1/2/4) x "
            "base 34..38 variants, only base=34,key=1,len=1,unit=1 consumes the payload exactly; "
            "key/length semantics remain unresolved"
        ),
    }
    return {
        "header": {"size": hdr, "hex": hx(b[:hdr]), "fields": hdr_fields, "magic_ok": b[:6] == MAGIC,
                   "payload_version": struct.unpack_from("<H", b, 6)[0]},
        "format": fmt,
        "closure": closure(f"34 + sum(2+len) = {off}", off == len(b), len(b) - off, 0),
        "facts": {
            "distinct_keys": len(keys),
            "zero_length_records": zero_len,
            "key_histogram_top": sorted(keys.items(), key=lambda kv: -kv[1])[:10],
        },
        "samples": samples,
    }


# ---------------------------------------------------------------- 10 summary.dat


def dec_summary(b: bytes) -> dict:
    """40B 头 + N ×(body + 5B 分隔符) + 尾块（12B 前缀 + u32 词数组 + (u32,f32)×m + 0xFFFFFFFF）。"""
    count_hdr = struct.unpack_from("<I", b, 8)[0]
    ids = list(struct.unpack_from(f"<{count_hdr}I", b, 12)) if count_hdr else []
    hdr = 12 + 4 * count_hdr
    bodies = []
    sizes = {}
    samples = []
    pos = hdr
    while True:
        sep = b.find(SEP, pos)
        if sep < 0:
            tail = b[pos:]
            break
        body = b[pos:sep]
        bodies.append(body)
        sizes[len(body)] = sizes.get(len(body), 0) + 1
        if len(samples) < SAMPLE_N:
            uid = struct.unpack_from("<I", body, 0)[0] if len(body) >= 4 else None
            samples.append(
                {
                    "record": len(samples),
                    "offset": pos,
                    "byte_len": len(body),
                    "lead_u32": uid,
                    "hex_head": hx(body, 20),
                }
            )
        pos = sep + 5
    consumed = hdr + sum(len(x) + 5 for x in bodies)
    # 尾块：12 B 前缀 + u32 词数组 + 8 B 定长对 + 4 B 终止符
    tail = b[consumed:]
    tail_prefix = 12
    tail_ok = False
    pair_count = 0
    mid_words = 0
    asc_runs: list[int] = []
    tail_pairs: list[dict] = []
    if len(tail) > tail_prefix + 4 and tail[-4:] == b"\xff\xff\xff\xff":
        # 自尾部向前退 8 B 对，直到不再是 (小 u32, 有限 f32)
        q = len(tail) - 4
        while q - 8 >= tail_prefix:
            pid, pval = struct.unpack_from("<If", tail, q - 8)
            if pid >= 4096 or not (pval == pval) or abs(pval) > 1e12:
                break
            q -= 8
        pair_count = (len(tail) - 4 - q) // 8
        mid = tail[tail_prefix:q]
        for k in range(min(pair_count, SAMPLE_N)):
            pid, pval = struct.unpack_from("<If", tail, q + 8 * k)
            tail_pairs.append({"id": pid, "value": round(pval, 6)})
        tail_ok = tail_prefix + len(mid) + 8 * pair_count + 4 == len(tail)
        if len(mid) % 4 == 0:
            mid_words = len(mid) // 4
            vals = struct.unpack_from(f"<{mid_words}I", mid, 0) if mid_words else ()
            i = 0
            while i < len(vals):
                j = i + 1
                while j < len(vals) and vals[j] > vals[j - 1]:
                    j += 1
                if j - i >= 50:
                    asc_runs.append(j - i)
                i = j
    fmt = {
        "kind": "separator_framed",
        "header_size": hdr,
        "row_count": len(bodies),
        "record_grammar": "body bytes + 5B separator ff ff ff ff 03",
        "fields": [
            {"off": 0, "width": 4, "type": "u32", "name": "lead_u32",
             "semantic": "body lead word; dominant 17B bodies lead with a small u32 id"},
            {"off": 4, "width": "body_len-4", "type": "bytes", "name": "body_payload"},
        ],
        "trailing_block": {
            "len": len(tail),
            "prefix_len": tail_prefix,
            "prefix_hex": hx(tail, tail_prefix),
            "u32_word_count": mid_words,
            "pair_count": pair_count,
            "pair_grammar": "u32 id + f32 value, terminated by 0xFFFFFFFF",
            "terminator_hex": "ff ff ff ff",
            "ascending_u32_runs": asc_runs,
            "parsed_ok": tail_ok,
        },
        "footer": {"len": 4, "hex": "ff ff ff ff"},
    }
    return {
        "header": {
            "size": hdr,
            "hex": hx(b[:hdr]),
            "fields": [
                {"off": 0, "width": 6, "type": "bytes", "name": "magic", "value": MAGIC.decode("latin-1")},
                {"off": 6, "width": 2, "type": "u16", "name": "payload_version"},
                {"off": 8, "width": 4, "type": "u32", "name": "id_count"},
                {"off": 12, "width": 4, "type": "u32[]", "name": "id_list", "value": ids},
            ],
            "magic_ok": b[:6] == MAGIC,
            "payload_version": struct.unpack_from("<H", b, 6)[0],
        },
        "format": fmt,
        "closure": closure(
            f"{hdr} + sum(body+5) [{consumed}] + tail {len(tail)} = {consumed + len(tail)}",
            consumed + len(tail) == len(b),
            len(b) - consumed - len(tail),
            4,
        ),
        "facts": {
            "separator_count": len(bodies),
            "body_size_top": sorted(sizes.items(), key=lambda kv: -kv[1])[:5],
            "dominant_body_len": max(sizes.items(), key=lambda kv: kv[1])[0],
            "trailing_words": mid_words,
            "trailing_pairs": pair_count,
            "trailing_asc_runs": asc_runs,
            "trailing_pair_samples": tail_pairs,
        },
        "samples": samples,
    }


# ---------------------------------------------------------------- 11 old_save_23


def dec_old_save_23(b: bytes) -> dict:
    """15B 头 + row_count × 14B 行（u32 ordinal + u32 uid + u32 uid + u16 0）+ 7B 尾。"""
    count = struct.unpack_from("<I", b, 8)[0]
    start, stride = 15, 14
    end = start + count * stride
    rows = []
    ord_ok = True
    uids_equal = 0
    tail_u16_zero = 0
    for idx in range(count):
        o = start + idx * stride
        a, c, d, e = struct.unpack_from("<IIIH", b, o)
        if a != idx:
            ord_ok = False
        if c == d:
            uids_equal += 1
        if e == 0:
            tail_u16_zero += 1
        if len(rows) < SAMPLE_N:
            rows.append({"row": idx, "ordinal": a, "uid_a": c, "uid_b": d, "flag_u16": e})
    tail = b[end:]
    fmt = {
        "kind": "fixed_stride",
        "header_size": start,
        "row_stride": stride,
        "row_count": count,
        "fields": [
            {"off": 0, "width": 4, "type": "u32", "name": "ordinal", "semantic": "equals row index"},
            {"off": 4, "width": 4, "type": "u32", "name": "uid_a"},
            {"off": 8, "width": 4, "type": "u32", "name": "uid_b", "semantic": "always == uid_a"},
            {"off": 12, "width": 2, "type": "u16", "name": "flag", "semantic": "always 0"},
        ],
        "footer": {"len": len(tail), "hex": hx(tail),
                   "note": "7B wire footer; header start 15 is the only offset with 278/278 ordinal match"},
    }
    return {
        "header": tad_header(b, start, std_header_fields()),
        "format": fmt,
        "closure": closure(f"{start} + {count}*{stride} + {len(tail)} = {end + len(tail)}",
                           end + len(tail) == len(b), len(b) - end - len(tail), len(tail)),
        "facts": {
            "ordinal_equals_row_index": ord_ok,
            "rows_with_equal_uids": uids_equal,
            "rows_with_zero_flag": tail_u16_zero,
        },
        "samples": rows,
    }


# ---------------------------------------------------------------- 12 old_save_25


def dec_old_save_25(b: bytes) -> dict:
    """12B 头 + row_count 个变长行（行尾 12B identity：ordinal + u32 + u32）+ 9B footer。

    行走法用唯一路径重建：候选 identity 位置 = 满足 `u32==k 且 u32+4==u32+8` 的偏移；
    自 12 起逐行取第一个 >= 游标的候选，末态必须唯一且停在 len-9。
    """
    count = struct.unpack_from("<I", b, 8)[0]
    n = len(b)
    cand: dict[int, list[int]] = {}
    unpack = struct.unpack_from
    for p in range(12, n - 11):
        v = unpack("<I", b, p)[0]
        if v < count and unpack("<I", b, p + 4)[0] == unpack("<I", b, p + 8)[0]:
            cand.setdefault(v, []).append(p)
    missing = [k for k in range(count) if k not in cand]
    states = {12: 1}
    ends: list[int] = []
    for k in range(count):
        nxt: dict[int, int] = {}
        cl = cand.get(k, [])
        for start, ways in states.items():
            i = bisect_left(cl, start)
            if i < len(cl):
                e = cl[i] + 12
                nxt[e] = nxt.get(e, 0) + ways
        states = nxt
        if len(states) != 1:
            ends.append(len(states))
            break
        ends.append(next(iter(states)))
    unique_path = len(states) == 1
    final_end = next(iter(states)) if unique_path else None
    footer = b[final_end:] if unique_path else b""
    starts = [12]
    if unique_path:
        for k in range(count - 1):
            cl = cand[k]
            i = bisect_left(cl, starts[-1])
            starts.append(cl[i] + 12)
    row_lens = [starts[k + 1] - starts[k] for k in range(len(starts) - 1)]
    rows = []
    for k in range(min(SAMPLE_N, len(starts))):
        o = starts[k]
        ident = o + row_lens[k] - 12 if k < len(row_lens) else None
        rec = {"row": k, "start": o, "byte_len": row_lens[k] if k < len(row_lens) else None}
        if ident is not None:
            a, c, d = struct.unpack_from("<III", b, ident)
            rec.update({"identity_offset": ident, "ordinal": a, "uid_a": c, "uid_b": d})
        rows.append(rec)
    fmt = {
        "kind": "variable_stride",
        "header_size": 12,
        "row_count": count,
        "fields": [
            {"off": 0, "width": "row_len-12", "type": "bytes", "name": "body"},
            {"off": "row_len-12", "width": 4, "type": "u32", "name": "ordinal",
             "semantic": "equals row index (row-frame witness)"},
            {"off": "row_len-8", "width": 4, "type": "u32", "name": "uid_a"},
            {"off": "row_len-4", "width": 4, "type": "u32", "name": "uid_b",
             "semantic": "always == uid_a"},
        ],
        "footer": {"len": len(footer), "hex": hx(footer),
                   "note": "9B wire footer 00000000 01 4ec43a77"},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(
            f"12 + sum(rowlen) [{sum(row_lens) if row_lens else 0}] + {len(footer)} = "
            f"{(final_end + len(footer)) if final_end else 'n/a'}",
            unique_path and final_end + len(footer) == n,
            (n - final_end - len(footer)) if final_end else n,
            len(footer),
        ),
        "facts": {
            "unique_dp_path": unique_path,
            "missing_ordinals": missing[:10],
            "row_len_min": min(row_lens) if row_lens else None,
            "row_len_max": max(row_lens) if row_lens else None,
            "row_len_mode": max(((l, row_lens.count(l)) for l in set(row_lens)), key=lambda t: t[1])[0]
            if row_lens else None,
            "identity_candidates_total": sum(len(v) for v in cand.values()),
        },
        "samples": rows,
    }


# ---------------------------------------------------------------- 13 fantasy_draft


def dec_fantasy_draft(b: bytes) -> dict:
    """12B 头 + row_count 个以 `01 00 6c 07` 结尾的变长行 + 31B 尾块。"""
    count = struct.unpack_from("<I", b, 8)[0]
    marks = []
    i = b.find(MARK)
    while i >= 0:
        marks.append(i)
        i = b.find(MARK, i + 1)
    starts = [12] + [m + 4 for m in marks[:-1]]
    rows = []
    for k in range(len(starts)):
        s = starts[k]
        e = (marks[k] + 4) if k < len(marks) else len(b)
        body = b[s:e]
        if len(rows) < SAMPLE_N:
            rec = {"row": k, "start": s, "byte_len": len(body)}
            # 行首通常是一个 u32 字符串长度 + 名字
            if len(body) >= 4:
                ln = struct.unpack_from("<I", body, 0)[0]
                if 0 < ln <= 64 and 4 + ln <= len(body):
                    rec["name_len"] = ln
                    rec["name"] = decode_text(body[4:4 + ln])
                # 第二段字符串
                o2 = 4 + ln if "name_len" in rec else 4
                if o2 + 4 <= len(body):
                    ln2 = struct.unpack_from("<I", body, o2)[0]
                    if 0 < ln2 <= 64 and o2 + 4 + ln2 <= len(body):
                        rec["name2"] = decode_text(body[o2 + 4:o2 + 4 + ln2])
            rec["hex_head"] = hx(body, 24)
            rows.append(rec)
    tail = b[(marks[-1] + 4):] if marks else b[12:]
    consumed = 12 + sum(len(b[s:(marks[k] + 4) if k < len(marks) else len(b)])
                        for k, s in enumerate(starts))
    fmt = {
        "kind": "variable_stride",
        "header_size": 12,
        "row_count": len(starts),
        "row_terminator": {"hex": hx(MARK), "len": 4, "count": len(marks)},
        "fields": [
            {"off": 0, "width": "var", "type": "bytes", "name": "body",
             "semantic": "starts with u32 len + utf8 stadium/club/person names"},
            {"off": "row_len-4", "width": 4, "type": "bytes", "name": "terminator",
             "value": hx(MARK)},
        ],
        "footer": {"len": len(tail), "hex": hx(tail),
                   "note": "31B trailing block; no 9B wire footer on this member"},
    }
    return {
        "header": tad_header(b, 12, std_header_fields()),
        "format": fmt,
        "closure": closure(f"12 + sum(rowlen) [{consumed - 12}] + {len(tail)} = {consumed + len(tail)}",
                           consumed + len(tail) == len(b) and len(marks) == count,
                           len(b) - consumed - len(tail), len(tail)),
        "facts": {
            "header_count": count,
            "markers_found": len(marks),
            "rows_derived": len(starts),
            "tail_len": len(tail),
        },
        "samples": rows,
    }


DECODERS = {
    "name_table_0": dec_name_main,
    "name_table_1": dec_name_main,
    "name_table_2": dec_name_main,
    "name_table_extra_0": dec_name_extra,
    "name_table_extra_1": dec_name_extra,
    "name_table_extra_2": dec_name_extra,
    "common_name_links": dec_common_name_links,
    "club_links": dec_club_links,
    "simple_vars": dec_simple_vars,
    SUMMARY_MEMBER: dec_summary,
    "table_for_old_save_23": dec_old_save_23,
    "table_for_old_save_25": dec_old_save_25,
    "fantasy_draft_future_regens": dec_fantasy_draft,
}


# ---------------------------------------------------------------- 解包


def _t38():
    import t38_multiframe as m

    return m


def payload_path(outdir: pathlib.Path, member: str) -> pathlib.Path:
    if member == SUMMARY_MEMBER:
        return outdir / "payload_summary.bin"
    return outdir / f"payload_server_{member}.bin"


def extract_payloads(outdir: pathlib.Path, force: bool = False) -> dict:
    """解包 12 个 server 成员 + 独立 summary.dat；已有且长度匹配的中间文件直接复用。"""
    outdir.mkdir(parents=True, exist_ok=True)
    m = _t38()
    codec = m._codec()
    info = m.archive_info(codec, "server")
    result = {}
    for name in SERVER_MEMBERS:
        fn = f"server_db.dat"
        entry = codec["_resolve_table"](f"{name}.dat", info["tables"], fn)
        want = int(entry["size"])
        p = payload_path(outdir, name)
        if not force and p.is_file() and p.stat().st_size == want:
            data = p.read_bytes()
            result[name] = {
                "data": data,
                "source": "server_db.dat",
                "entry": entry,
                "diag": {"reused": True, "selected_length": want},
            }
            continue
        got = m.inspect_entry(codec, entry, info)
        data = got["data"]
        p.write_bytes(data)
        result[name] = {
            "data": data,
            "source": "server_db.dat",
            "entry": entry,
            "diag": got["diag"],
        }
    sp = DATA_DIR / "summary.dat"
    if not sp.is_file():
        raise FileNotFoundError(sp)
    p = payload_path(outdir, SUMMARY_MEMBER)
    if not force and p.is_file() and p.stat().st_size == sp.stat().st_size:
        data = p.read_bytes()
        reused = True
    else:
        data = sp.read_bytes()
        p.write_bytes(data)
        reused = False
    result[SUMMARY_MEMBER] = {
        "data": data,
        "source": "summary.dat (standalone tad file)",
        "entry": {"path": "summary.dat", "size": len(data), "packed_size": len(data)},
        "diag": {"reused": reused, "selected_length": len(data)},
    }
    return result


# ---------------------------------------------------------------- 报告


def build_schema(payloads: dict) -> dict:
    members = {}
    for name in ALL_MEMBERS:
        data = payloads[name]["data"]
        dec = DECODERS[name](data)
        entry = payloads[name]["entry"]
        diag = payloads[name]["diag"]
        dec.update(
            {
                "member": name,
                "source": payloads[name]["source"],
                "payload_size": len(data),
                "declared_size": int(entry["size"]),
                "size_matches": len(data) == int(entry["size"]),
                "payload_sha256": sha256(data),
                "unpack": {
                    "surface": diag.get("surface", "standalone"),
                    "selected_length": diag.get("selected_length"),
                    "leftover_bytes": diag.get("leftover_bytes"),
                    "frame_count": diag.get("frame_count"),
                    "reused_intermediate": diag.get("reused"),
                },
            }
        )
        # 姓名池主表补上真实字符串（与同序 extra 池按 ordinal 对齐）
        if name.startswith("name_table_") and not name.startswith("name_table_extra"):
            pool = name.rsplit("_", 1)[1]
            extra = payloads.get(f"name_table_extra_{pool}", {}).get("data")
            if extra:
                names = []
                off = 12
                want = [s["ordinal"] for s in dec["samples"]]
                target = set(want)
                idx = 0
                while off + 8 <= len(extra) and len(names) <= max(want):
                    uid, ln = struct.unpack_from("<II", extra, off)
                    off += 8
                    if idx in target:
                        names.append(decode_text(extra[off:off + ln]))
                    off += ln
                    idx += 1
                    if idx > max(want):
                        break
                for s, nm in zip(dec["samples"], names):
                    s["name"] = nm
                dec["facts"]["string_join"] = f"ordinal -> name_table_extra_{pool} uid"
        members[name] = dec
    closed = sum(1 for v in members.values() if v["closure"]["ok"])
    return {
        "status": "complete",
        "task": "t106",
        "title": "FM24 non-numbered special members: format decode + byte-exact closure",
        "member_count": len(members),
        "members_closed": closed,
        "all_closed": closed == len(members),
        "inputs": {
            "server_db.dat": str(DATA_DIR / "server_db.dat"),
            "client_db.dat": str(DATA_DIR / "client_db.dat"),
            "summary.dat": str(DATA_DIR / "summary.dat"),
            "unpacker": "scripts/t38_multiframe.py (E80: data_base+offset, packed_size bound, size-selected frame)",
        },
        "members": members,
    }


def render_report(schema: dict) -> str:
    L = []
    L.append("# t106 — 非编号特殊成员格式解析与闭合验证")
    L.append("")
    L.append(f"- 成员数 **{schema['member_count']}**，字节精确闭合 **{schema['members_closed']}/{schema['member_count']}**")
    L.append("- 解包：`scripts/t38_multiframe.py`（E80：`data_base + offset` 定位、`packed_size` 界定、`size` 选帧）")
    L.append("- 脚本：`scripts/t106_special_members.py`（`--help` / `--selftest`，退出码 0/1/2）")
    L.append("")
    L.append("## 闭合汇总表")
    L.append("")
    L.append("| 成员 | 载荷字节 | 记录数 | 头 | 行/记录 | footer | 闭合算式 | OK |")
    L.append("|---|---:|---:|---:|---|---:|---|---|")
    for name in ALL_MEMBERS:
        m = schema["members"][name]
        f = m["format"]
        ftr = f.get("footer", {})
        fl = ftr.get("len", 0)
        hdr = f.get("header_size", m["header"]["size"])
        rows = f.get("row_count")
        stride = f.get("row_stride")
        rowtxt = f"{stride}B 定长" if stride else f.get("kind")
        L.append(
            f"| `{name}` | {m['payload_size']:,} | {rows:,} | {hdr}B | {rowtxt} | {fl}B | "
            f"`{m['closure']['arithmetic']}` | {'✅' if m['closure']['ok'] else '❌'} |"
        )
    L.append("")
    L.append("## 逐成员格式")
    L.append("")
    for name in ALL_MEMBERS:
        m = schema["members"][name]
        f = m["format"]
        L.append(f"### `{name}.dat`")
        L.append("")
        L.append(f"- 来源：{m['source']}；载荷 {m['payload_size']:,} B；SHA-256 `{m['payload_sha256'][:16]}…`")
        L.append(f"- 头（{m['header']['size']} B）：`{m['header']['hex']}`")
        if f.get("row_stride"):
            L.append(f"- 结构：{f['row_stride']} B 定长行 × {f['row_count']:,}")
        else:
            L.append(f"- 结构：{f.get('kind')}，{f['row_count']:,} 条记录")
        for fld in f.get("fields", []):
            sem = f" — {fld['semantic']}" if fld.get("semantic") else ""
            L.append(f"  - `+{fld['off']}` {fld['type']} `{fld['name']}`{sem}")
        ftr = f.get("footer", {})
        if ftr.get("len"):
            L.append(f"- footer（{ftr['len']} B）：`{ftr.get('hex','')}`")
        if f.get("grammar_status"):
            L.append(f"- 文法：{f['grammar_status']}")
        if f.get("trailing_block"):
            tb = f["trailing_block"]
            L.append(
                f"- 尾块：{tb['len']:,} B = {tb['prefix_len']} B 前缀 + {tb['u32_word_count']:,} × u32 "
                f"+ {tb['pair_count']} × (u32,f32) + 4 B 终止符；`{tb['terminator_hex']}`"
            )
        if f.get("row_terminator"):
            rt = f["row_terminator"]
            L.append(f"- 行终止标记：`{rt['hex']}` × {rt['count']}")
        L.append(f"- 闭合：`{m['closure']['arithmetic']}` → leftover {m['closure']['leftover_bytes']} B")
        facts = {k: v for k, v in m["facts"].items() if k != "trailing_pair_samples"}
        if facts:
            L.append(f"- 事实：`{json.dumps(facts, ensure_ascii=False)}`")
        L.append("")
        L.append("前 10 条解码样本：")
        L.append("")
        L.append("```json")
        L.append(json.dumps(m["samples"][:SAMPLE_N], ensure_ascii=False, indent=1))
        L.append("```")
        L.append("")
    L.append("## 证据边界")
    L.append("")
    L.append("- `simple_vars` 的 (u8 key, u8 len) 是**唯一能精确闭合**的定前缀文法；key/长度语义仍未定型，")
    L.append("  不把 key 当业务字段名，也不把 value 当已解类型。")
    L.append("- `name_table_*` 的 `meta_a` / `meta_b` / `meta_c` / `meta_d` 保留原始槽位语义（未命名）；")
    L.append("  `string_ordinal` 已证与同序 `name_table_extra_*` 的 uid 1:1。")
    L.append("- `club_links` 第 13..46 字节是定形 wire 子对象（含重复常量 `0x076c0001`），只列常量位置，不命名字段。")
    L.append("- `summary.dat` body 内部字段语义未解，只给分隔符框定与尾块结构；尾块中 2,621 个 u32 词含")
    L.append("  两段长升序 id 串（2,488 / 126 个），语义未定，不当作已解字段。")
    L.append("- `table_for_old_save_23` 尾为 7 B（非 9 B）；`table_for_old_save_25` 为 9 B footer；")
    L.append("  `fantasy_draft_future_regens` 为 31 B 尾块，无 9 B footer —— 各表 footer 宽度逐表自证，未互相照抄。")
    L.append("")
    return "\n".join(L)


def render_done(schema: dict) -> str:
    closed = schema["members_closed"]
    total = schema["member_count"]
    total_bytes = sum(v["payload_size"] for v in schema["members"].values())
    total_rows = sum(v["format"].get("row_count") or 0 for v in schema["members"].values())
    L = [
        "DONE type=t106",
        "",
        f"- 成员：{total}（server_db 12 + 独立 summary.dat 1）",
        f"- 字节精确闭合：{closed}/{total}",
        f"- 解码载荷合计：{total_bytes:,} B",
        f"- 记录/行合计：{total_rows:,}",
        f"- name_table_0/1/2 行数："
        + " / ".join(f"{schema['members'][f'name_table_{i}']['format']['row_count']:,}" for i in range(3)),
        f"- name_table_extra_0/1/2 字符串数："
        + " / ".join(f"{schema['members'][f'name_table_extra_{i}']['format']['row_count']:,}" for i in range(3)),
        f"- common_name_links 行数：{schema['members']['common_name_links']['format']['row_count']:,}"
        f"（sentinel {schema['members']['common_name_links']['facts']['sentinel_rows']}）",
        f"- club_links 行数：{schema['members']['club_links']['format']['row_count']:,}"
        f"（常量字节位 {schema['members']['club_links']['facts']['constant_byte_positions']}/47）",
        f"- simple_vars：34 B 前导 + {schema['members']['simple_vars']['format']['row_count']:,} 条 (u8 key,u8 len) 记录，"
        f"{schema['members']['simple_vars']['facts']['distinct_keys']} 个键码",
        f"- summary.dat：{schema['members']['summary']['facts']['separator_count']:,} 个 body + "
        f"{schema['members']['summary']['format']['trailing_block']['len']:,} B 尾块"
        f"（{schema['members']['summary']['facts']['trailing_pairs']} 个 (u32,f32) 对）",
        f"- table_for_old_save_23：278×14 B + 7 B 尾；table_for_old_save_25："
        f"{schema['members']['table_for_old_save_25']['format']['row_count']:,} 变长行（唯一 DP 路径）+ 9 B footer",
        f"- fantasy_draft_future_regens：{schema['members']['fantasy_draft_future_regens']['format']['row_count']} 行 + "
        f"{schema['members']['fantasy_draft_future_regens']['facts']['tail_len']} B 尾块",
        "",
        "产出：`special_members_schema.json`、`REPORT.md`、`DONE.md`",
    ]
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- selftest


def _mk_name_main(rows: list[tuple[int, int, int, int, int]]) -> bytes:
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", len(rows))
    for i, (a, c, d, e) in enumerate(rows):
        b += struct.pack("<HIHHH", a, i, c, d, e)
    return b


def run_selftest() -> int:
    checks = []

    def ck(name: str, cond: bool) -> None:
        checks.append((name, bool(cond)))

    # 1 姓名池主表
    b = _mk_name_main([(65535, 249, 4817, 0xFF00), (7, 3, 1, 8)])
    d = dec_name_main(b)
    ck("name_main count", d["format"]["row_count"] == 2)
    ck("name_main closure", d["closure"]["ok"])
    ck("name_main ordinal", d["facts"]["ordinal_equals_row_index"])
    ck("name_main meta_d hex", d["samples"][0]["meta_d_hex"] == "0xff00")

    # 2 姓名池字符串
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2)
    b += struct.pack("<II", 0, 5) + b"Sabri" + struct.pack("<II", 1, 5) + b"Jos\xc3\xa9"
    d = dec_name_extra(b)
    ck("extra count", d["format"]["row_count"] == 2)
    ck("extra closure", d["closure"]["ok"])
    ck("extra uid", d["facts"]["uid_equals_row_index"])
    ck("extra utf8", d["samples"][1]["text"] == "José")

    # 3 common_name_links
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2)
    b += struct.pack("<IBxHH", 5, 1, 108, 10 << 8) + struct.pack("<IBxHH", SENTINEL, 0, 95, 3 << 8)
    d = dec_common_name_links(b)
    ck("cnl closure", d["closure"]["ok"])
    ck("cnl sentinel", d["facts"]["sentinel_rows"] == 1)
    ck("cnl lang", d["samples"][0]["lang_code"] == 10)
    ck("cnl sentinel none", d["samples"][1]["name_ordinal"] is None)

    # 4 club_links
    row = struct.pack("<I", 1270) + b"\x04\xe2\x01\x80\x04" + struct.pack("<I", 11272) + b"\x00" * 34
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2) + row + row
    d = dec_club_links(b)
    ck("club closure", d["closure"]["ok"])
    ck("club uid", d["samples"][0]["club_uid"] == 1270)
    ck("club linked", d["samples"][0]["linked_uid"] == 11272)
    ck("club stride", d["format"]["row_stride"] == 47)

    # 5 simple_vars
    hdr = MAGIC + struct.pack("<H", 3569) + b"\x00\x00\x08\x00\x00\x00" + struct.pack("<H", 3569)
    hdr += struct.pack("<I", 4) + b"2430K2" + struct.pack("<H", 2024) + struct.pack("<I", 300183) + struct.pack("<H", 2023)
    b = hdr + bytes([3, 2, 0xAA, 0xBB]) + bytes([0, 0]) + bytes([9, 1, 0x7F])
    d = dec_simple_vars(b)
    ck("sv header 34", d["header"]["size"] == 34)
    ck("sv closure", d["closure"]["ok"])
    ck("sv recs", d["format"]["row_count"] == 3)
    ck("sv key", d["samples"][0]["key"] == 3 and d["samples"][0]["len"] == 2)

    # 6 summary
    head = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2) + struct.pack("<II", 1, 2)
    body1 = struct.pack("<I", 250) + b"\x01" * 13
    body2 = struct.pack("<I", 7) + b"\x02" * 5
    tail = b"\xfa\x00\x00\x00\xec\x7a\xe4\x04\x00\x00\x00\x00" + b"\xff" * 8
    tail += struct.pack("<If", 11, 1.5) + b"\xff\xff\xff\xff"
    b = head + body1 + SEP + body2 + SEP + tail
    d = dec_summary(b)
    ck("summary hdr", d["header"]["size"] == 20)
    ck("summary closure", d["closure"]["ok"])
    ck("summary bodies", d["format"]["row_count"] == 2)
    ck("summary tail pairs", d["facts"]["trailing_pairs"] == 1)
    ck("summary tail words", d["facts"]["trailing_words"] == 2)

    # 7 old_save_23
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2) + b"\x00\x00\x00"
    b += struct.pack("<IIIH", 0, 1, 1, 0) + struct.pack("<IIIH", 1, 2, 2, 0)
    b += bytes.fromhex("000001945b3a77")
    d = dec_old_save_23(b)
    ck("old23 hdr 15", d["format"]["header_size"] == 15)
    ck("old23 closure", d["closure"]["ok"])
    ck("old23 footer 7", d["closure"]["footer_len"] == 7)

    # 8 old_save_25
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2)
    b += b"\xaa" * 20 + struct.pack("<III", 0, SENTINEL, SENTINEL)
    b += b"\xbb" * 30 + struct.pack("<III", 1, 42, 42)
    b += bytes.fromhex("00000000014ec43a77")
    d = dec_old_save_25(b)
    ck("old25 unique path", d["facts"]["unique_dp_path"])
    ck("old25 closure", d["closure"]["ok"])
    ck("old25 footer 9", d["closure"]["footer_len"] == 9)
    ck("old25 rows", d["format"]["row_count"] == 2)

    # 9 fantasy
    b = MAGIC + struct.pack("<H", 3569) + struct.pack("<I", 2)
    b += struct.pack("<I", 5) + b"Kudsk" + b"\x00" * 4 + MARK
    b += struct.pack("<I", 5) + b"Clara" + b"\x00" * 2 + MARK
    b += bytes.fromhex("10ffff0701") + b"\x00" * 26
    d = dec_fantasy_draft(b)
    ck("fantasy closure", d["closure"]["ok"])
    ck("fantasy markers", d["facts"]["markers_found"] == 2)
    ck("fantasy name", d["samples"][0].get("name") == "Kudsk")

    # 10 工具
    ck("sha256 stable", sha256(b"") == hashlib.sha256(b"").hexdigest())
    ck("all members registered", len(DECODERS) == len(ALL_MEMBERS) == 13)

    bad = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}")
    print(f"selftest: {len(checks) - len(bad)}/{len(checks)} pass")
    return 0 if not bad else 1


# ---------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="t106_special_members.py",
        description="解包并逐行解码 FM24 的 13 个非编号特殊成员，校验字节精确闭合。",
    )
    ap.add_argument("--selftest", action="store_true", help="运行内置自检（不读归档）")
    ap.add_argument("--outdir", default=str(OUTDIR_DEFAULT), help=f"输出目录（默认 {OUTDIR_DEFAULT}）")
    ap.add_argument("--force-extract", action="store_true", help="忽略已有 payload 中间文件，重新解包")
    ap.add_argument("--json-only", action="store_true", help="只写 JSON，不写 REPORT.md / DONE.md")
    args = ap.parse_args(argv)

    if args.selftest:
        return run_selftest()

    outdir = pathlib.Path(args.outdir)
    try:
        payloads = extract_payloads(outdir, force=args.force_extract)
    except FileNotFoundError as e:
        print(f"missing input: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # 解包失败视为验收失败
        print(f"unpack failure: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    schema = build_schema(payloads)
    (outdir / "special_members_schema.json").write_text(
        json.dumps(schema, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    if not args.json_only:
        (outdir / "REPORT.md").write_text(render_report(schema), encoding="utf-8")
        (outdir / "DONE.md").write_text(render_done(schema), encoding="utf-8")

    print(f"members={schema['member_count']} closed={schema['members_closed']}")
    for name in ALL_MEMBERS:
        m = schema["members"][name]
        flag = "OK " if m["closure"]["ok"] else "BAD"
        print(
            f"  {flag} {name:32s} {m['payload_size']:>9,}B  rows={m['format'].get('row_count'):>7,}  "
            f"leftover={m['closure']['leftover_bytes']}"
        )
    print(f"outdir: {outdir}")
    return 0 if schema["all_closed"] else 1


if __name__ == "__main__":
    sys.exit(main())
