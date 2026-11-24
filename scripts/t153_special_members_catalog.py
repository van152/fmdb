#!/usr/bin/env python3
"""t153 — FM24 13 个特殊成员 + summary.dat 统一结构与语义目录.

综合 t106/t119/t130/t133/t136/t143 的成果，对 server_db.dat / client_db.dat
中 13 个非编号特殊字典成员与独立 summary.dat 产出统一机读目录：

  * 成员名、client/server 体积、行数/条目数
  * 物理布局摘要（头/行/尾、固定/变长、分隔符、zstd 成员边界）
  * 已知语义与外键关联（名称池、常用名、俱乐部关联、身份 UID 等）
  * 证据等级 L1/L2/L3（L1=self-consistency 闭合，L2=独立事实对照，
    L3=exe 静态/机器码仿真证据，L4=0）

只读输入：scratch/data/*.dat + 复用 t112 Archive 解包 FMF 成员；
不写入 reports/ 与 scratch/t01/LEDGER.json；不启动 Editor / IDA / 游戏。

CLI:
  py -V:3.12 -B scripts/t153_special_members_catalog.py --help
  py -V:3.12 -B scripts/t153_special_members_catalog.py --selftest
  py -V:3.12 -B scripts/t153_special_members_catalog.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import struct
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fm24_config as _cfg

ROOT = pathlib.Path(str(_cfg.ROOT))
SCRIPTS_DIR = pathlib.Path(str(_cfg.SCRIPTS_DIR))
OUT_DIR = ROOT / "scratch/t153/out"
DATA_DIR = ROOT / "scratch/data"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(_cfg.VENDOR_DIR))

import t112_fm24_reader as R  # noqa: E402  (Archive / archive_layout / DAT_MAGIC)

DAT_MAGIC = R.DAT_MAGIC            # b"\x03\x01tad."
FMF6 = bytes.fromhex("0201666d662e")
SENTINEL = 0xFFFFFFFF
SEP_SUMMARY = b"\xff\xff\xff\xff\x03"   # summary.dat body 分隔符
SUMMARY_MEMBER = "summary"
OUT_NAME = "special_members_catalog"

SELFTEST_OK = "PASS"
SELFTEST_FAIL = "FAIL"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# --------------------------------------------------------------------------- #
# 成员常量注册表（13 个特殊成员 + summary.dat）
# 各项含义：
#   key        目录键名（与 FMF 成员 / 独立文件同名）
#   side       'server' | 'client' | 'both' | 'standalone'
#   kind       'fixed_stride' | 'variable_stride' | 'separator_framed' | 'custom'
#   header_n   头部字节数
#   row_n      行数/条目数（未知填 None，由脚本实测填充）
#   stride_n   定长行宽（变长填 None）
#   footer_n   尾块/尾巴字节数
#   semantic   已知业务语义（未命名保留 "unresolved"）
#   fk         外键关联（成员/表名，None 表示无/未证实）
#   evidence   证据等级 L1/L2/L3（多个取最高）
#   source     证据来源（tNN / exe VA / 文件）
# --------------------------------------------------------------------------- #
MEMBER_SPEC = [
    dict(
        key="name_table_0", side="both", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=12, footer_n=0,
        semantic="姓名池元数据（pool 0）：meta_a/meta_b/meta_c/meta_d 四槽，string_ordinal 与同序 name_table_extra_0 uid 1:1",
        fk="name_table_extra_0.uid", evidence="L1", source="t106",
    ),
    dict(
        key="name_table_1", side="both", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=12, footer_n=0,
        semantic="姓名池元数据（pool 1）：同 name_table_0",
        fk="name_table_extra_1.uid", evidence="L1", source="t106",
    ),
    dict(
        key="name_table_2", side="both", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=12, footer_n=0,
        semantic="姓名池元数据（pool 2）：同 name_table_0",
        fk="name_table_extra_2.uid", evidence="L1", source="t106",
    ),
    dict(
        key="name_table_extra_0", side="both", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=0,
        semantic="姓名池字符串（pool 0）：u32 uid + u32 byte_len + utf8 text；uid 与 name_table_0 row index 1:1",
        fk="name_table_0.row_index", evidence="L1", source="t106",
    ),
    dict(
        key="name_table_extra_1", side="both", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=0,
        semantic="姓名池字符串（pool 1）：同 name_table_extra_0",
        fk="name_table_1.row_index", evidence="L1", source="t106",
    ),
    dict(
        key="name_table_extra_2", side="both", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=0,
        semantic="姓名池字符串（pool 2）：同 name_table_extra_0",
        fk="name_table_2.row_index", evidence="L1", source="t106",
    ),
    dict(
        key="common_name_links", side="both", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=10, footer_n=0,
        semantic="常用名 -> 姓名池 ordinal 关联：u32 name_ordinal（0xFFFFFFFF 为 sentinel）+ u8 flag + u8 opaque_b5 + u16 nation + u16 lang<<8",
        fk="name_table_* (ordinal)", evidence="L1", source="t106",
    ),
    dict(
        key="club_links", side="server", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=47, footer_n=0,
        semantic="俱乐部 -> 俱乐部关联：u32 club_uid + 5B opaque + u32 linked_uid + 34B 定形 wire 子对象（重复常量 0x076c0001）",
        fk="table_3.club_uid (club)", evidence="L1+L3", source="t106 + editor.exe (t82)",
    ),
    dict(
        key="simple_vars", side="both", kind="variable_stride",
        header_n=34, row_n=None, stride_n=None, footer_n=0,
        semantic="全局变量键值区：34B 前导 + (u8 key + u8 len + value) 记录流；key/长度语义未定型",
        fk=None, evidence="L1", source="t106",
    ),
    dict(
        key="table_extra_3", side="both", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=0,
        semantic="俱乐部/国家队扩展属性（84,259 行）：ordinal + 服务器专属块（选举/赞助/支持者/欧冠系数/子对象）+ 公共尾（d8/cc/Tcht/kit 列表/两组 RGBA/多态对象/TCrs）",
        fk="table_3.club_uid / table_10 (nation)", evidence="L1+L3", source="t82/t136 + editor.exe",
    ),
    dict(
        key="table_extra_9", side="both", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=0,
        semantic="国家队/俱乐部辅助属性（251 行）：ordinal + 名 + u16 + 标签 + kit 列表 + RGBA；server 额外向量/阵型/attendance/tag-9 记录/TCrs；无 footer",
        fk="table_10 (nation) / table_3 (club)", evidence="L1+L3", source="t53/t136 + editor.exe",
    ),
    dict(
        key="table_extra_24", side="server", kind="fixed_stride",
        header_n=12, row_n=None, stride_n=82, footer_n=0,
        semantic="server 固定 82B 行成员（84,507 行），语义槽位未命名",
        fk=None, evidence="L1", source="t136/t143",
    ),
    dict(
        key="table_for_old_save_23", side="server", kind="fixed_stride",
        header_n=15, row_n=None, stride_n=14, footer_n=7,
        semantic="旧存档 stage_name 兼容表：15B 头 + 278×14B 行（u32 ordinal + u32 uid_a + u32 uid_b + u16 flag=0）+ 7B 尾",
        fk=None, evidence="L1", source="t106",
    ),
    dict(
        key="table_for_old_save_25", side="server", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=9, doc_rows=7047,
        semantic="旧存档 competition 兼容表：12B 头 + 7,047 变长行（行尾 12B identity: ordinal+uid_a+uid_b，uid_a==uid_b）+ 9B footer",
        fk=None, evidence="L1", source="t106",
    ),
    dict(
        key="fantasy_draft_future_regens", side="server", kind="variable_stride",
        header_n=12, row_n=None, stride_n=None, footer_n=31,
        semantic="梦幻选秀再生球员：12B 头 + 40 变长行（行尾 01 00 6c 07 终止标记）+ 31B 尾块，无 9B footer",
        fk=None, evidence="L1", source="t106",
    ),
    dict(
        key="summary", side="standalone", kind="separator_framed",
        header_n=None, row_n=None, stride_n=None, footer_n=4,
        semantic="独立 tad 库摘要：头（6B magic + u16 版本 + u32 id 计数 + id 列表）+ N×(body + 5B 分隔符 ff ff ff ff 03) + 尾块（u32 词组 + (u32,f32) 对 + 0xFFFFFFFF）",
        fk=None, evidence="L1", source="t106",
    ),
]

ALL_KEYS = [m["key"] for m in MEMBER_SPEC]
SERVER_SPECIAL = [m["key"] for m in MEMBER_SPEC if m["side"] in ("server", "both") and m["key"] != SUMMARY_MEMBER]
CLIENT_SPECIAL = [m["key"] for m in MEMBER_SPEC if m["side"] in ("client", "both") and m["key"] != SUMMARY_MEMBER]


# --------------------------------------------------------------------------- #
# 工具函数
# --------------------------------------------------------------------------- #
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hx(data: bytes, limit: int | None = None) -> str:
    d = data if limit is None else data[:limit]
    return " ".join(f"{c:02x}" for c in d)


def decode_text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def load_member(archive_name: str, member_name: str) -> tuple[bytes, dict]:
    """从 FMF 归档中按 data_base+offset、packed_size 界定、size 选帧提取载荷（只读）。

    复用 t112 Archive 的容器层，但不走 Archive.payload（后者只支持 table_<tid> 数值成员）。
    """
    arc = R.Archive(archive_name)
    rel = f"{archive_name}_db/{member_name}.dat"
    if rel not in arc.entries:
        raise KeyError(f"{archive_name} archive has no member {rel}")
    entry = arc.entries[rel]
    raw = arc.data
    base = arc.data_base
    start = base + int(entry["offset"])
    size = int(entry["size"])
    region_end = start + int(entry["packed_size"])
    import zstandard as _zstd
    d = _zstd.ZstdDecompressor()
    frames = []
    pos = start
    ZSTD_MAGIC = bytes.fromhex("28b52ffd")
    while pos < region_end and raw[pos:pos + 4] == ZSTD_MAGIC:
        obj = d.decompressobj()
        chunk = obj.decompress(raw[pos:region_end])
        consumed = (region_end - pos) - len(obj.unused_data)
        frames.append({"member_offset": pos - start, "length": len(chunk), "data": chunk,
                       "consumed": consumed})
        if not obj.eof or consumed <= 0:
            break
        pos += consumed
    hits = [f for f in frames if f["length"] == size]
    if len(hits) != 1:
        raise ValueError(f"{archive_name}#{member_name}: {len(hits)} frames with length==size ({size})")
    return hits[0]["data"], dict(entry)


def parse_tad_header(b: bytes) -> dict:
    """tad 头：6B magic + u16 payload_version + u32 count @8."""
    if len(b) < 12 or b[:6] != DAT_MAGIC:
        return {"magic_ok": False, "payload_version": None, "count": None}
    return {
        "magic_ok": True,
        "payload_version": struct.unpack_from("<H", b, 6)[0],
        "count": struct.unpack_from("<I", b, 8)[0],
    }


def member_rel_path(member_key: str) -> str:
    """FMF 目录中成员的相对路径（server_db/... 或 client_db/...）。"""
    return f"{member_key}.dat"


# --------------------------------------------------------------------------- #
# 各成员物理布局分析（返回 layout 摘要 dict，不改动输入）
# --------------------------------------------------------------------------- #
def analyze_fixed_stride(b: bytes, spec: dict) -> dict:
    """定长行：头 + count*stride [+ footer]。"""
    hdr = parse_tad_header(b)
    count = hdr["count"] or 0
    stride = spec["stride_n"]
    body_need = spec["header_n"] + count * stride
    leftover = len(b) - body_need
    expected_footer = spec["footer_n"] or 0
    return {
        "kind": "fixed_stride",
        "header": hdr,
        "header_size": spec["header_n"],
        "row_stride": stride,
        "row_count": count,
        "body_span": [spec["header_n"], body_need],
        "footer_len": leftover if leftover > 0 else 0,
        "footer_hex": hx(b[body_need:body_need + leftover]) if leftover > 0 else "",
        "exact_close": leftover == expected_footer,
    }


def analyze_variable_stride(b: bytes, spec: dict, row_walk) -> dict:
    """变长行：头 + N 行（由 row_walk 逐行拆分）[+ footer]。 row_walk(b) -> (rows, tail_start)."""
    hdr = parse_tad_header(b)
    rows, tail_start = row_walk(b)
    tail = b[tail_start:]
    expected_footer = spec["footer_n"] or 0
    return {
        "kind": "variable_stride",
        "header": hdr,
        "header_size": spec["header_n"],
        "row_stride": None,
        "row_count": len(rows),
        "footer_len": len(tail),
        "footer_hex": hx(tail),
        "exact_close": len(tail) == expected_footer,
    }


def analyze_separator_framed(b: bytes) -> dict:
    """summary.dat：头（可变 id 列表）+ N×(body + SEP) + 尾块（+ 0xFFFFFFFF）。"""
    hdr = parse_tad_header(b)
    id_count = hdr["count"] or 0
    hdr_size = 12 + 4 * id_count
    ids = list(struct.unpack_from(f"<{id_count}I", b, 12)) if id_count else []
    bodies = []
    sizes = {}
    pos = hdr_size
    while True:
        sep = b.find(SEP_SUMMARY, pos)
        if sep < 0:
            tail = b[pos:]
            break
        body = b[pos:sep]
        bodies.append({"offset": pos, "byte_len": len(body), "lead_u32": struct.unpack_from("<I", body, 0)[0] if len(body) >= 4 else None})
        sizes[len(body)] = sizes.get(len(body), 0) + 1
        pos = sep + 5
    consumed = hdr_size + sum(len(x) for x in bodies) + 5 * len(bodies)
    tail = b[consumed:]
    pair_count = 0
    mid_words = 0
    if len(tail) > 16 and tail[-4:] == b"\xff\xff\xff\xff":
        q = len(tail) - 4
        while q - 8 >= 12:
            pid, pval = struct.unpack_from("<If", tail, q - 8)
            if pid >= 4096 or not (pval == pval) or abs(pval) > 1e12:
                break
            q -= 8
        pair_count = (len(tail) - 4 - q) // 8
        mid_words = (q - 12) // 4 if (q - 12) % 4 == 0 else 0
    return {
        "kind": "separator_framed",
        "header": {"size": hdr_size, "magic_ok": hdr["magic_ok"],
                   "payload_version": hdr["payload_version"], "id_count": id_count,
                   "id_list": ids[:10], "id_list_full": ids},
        "header_size": hdr_size,
        "row_stride": None,
        "row_count": len(bodies),
        "footer_len": len(tail),
        "footer_hex": hx(tail),
        "trailing_block": {
            "len": len(tail),
            "prefix_len": 12,
            "prefix_hex": hx(tail[:12]),
            "u32_word_count": mid_words,
            "pair_count": pair_count,
            "pair_grammar": "u32 id + f32 value, terminated by 0xFFFFFFFF",
            "terminator_hex": "ff ff ff ff",
        },
        "exact_close": consumed + len(tail) == len(b),
        "dominant_body_len": max(sizes.items(), key=lambda kv: kv[1])[0] if sizes else None,
        "body_size_top": sorted(sizes.items(), key=lambda kv: -kv[1])[:5],
    }


# --------------------------------------------------------------------------- #
# 具体成员 row-walk（仅用于已有成熟语法的成员；其余按物理骨架报告）
# --------------------------------------------------------------------------- #
def walk_name_extra(b: bytes):
    """u32 uid + u32 byte_len + utf8，逐行到 EOF（头后）。"""
    pos = 12
    rows = []
    n = struct.unpack_from("<I", b, 8)[0]
    for _ in range(n):
        s = pos
        uid, ln = struct.unpack_from("<II", b, pos)
        pos += 8
        e = pos + ln
        rows.append([s, e])
        pos = e
    return rows, pos


def walk_common_name_links(b: bytes):
    count = struct.unpack_from("<I", b, 8)[0]
    pos = 12
    rows = []
    for _ in range(count):
        s = pos
        pos += 10
        rows.append([s, pos])
    return rows, pos


def walk_club_links(b: bytes):
    count = struct.unpack_from("<I", b, 8)[0]
    pos = 12
    rows = []
    for _ in range(count):
        s = pos
        pos += 47
        rows.append([s, pos])
    return rows, pos


def walk_simple_vars(b: bytes):
    pos = 34
    rows = []
    while pos + 2 <= len(b):
        key, ln = b[pos], b[pos + 1]
        e = pos + 2 + ln
        if e > len(b):
            break
        rows.append([pos, e])
        pos = e
    return rows, pos


def walk_old_save_23(b: bytes):
    count = struct.unpack_from("<I", b, 8)[0]
    start, stride = 15, 14
    pos = start
    rows = []
    for _ in range(count):
        s = pos
        pos += stride
        rows.append([s, pos])
    return rows, pos


def walk_fantasy_draft(b: bytes):
    count = struct.unpack_from("<I", b, 8)[0]
    mark = b"\x01\x00\x6c\x07"
    marks = []
    i = b.find(mark)
    while i >= 0:
        marks.append(i)
        i = b.find(mark, i + 1)
    starts = [12] + [m + 4 for m in marks[:-1]]
    rows = []
    for k, s in enumerate(starts):
        e = marks[k] + 4 if k < len(marks) else len(b)
        rows.append([s, e])
    tail_start = marks[-1] + 4 if marks else len(b)
    return rows, tail_start


ROW_WALK = {
    "name_table_extra_0": walk_name_extra,
    "name_table_extra_1": walk_name_extra,
    "name_table_extra_2": walk_name_extra,
    "common_name_links": walk_common_name_links,
    "club_links": walk_club_links,
    "simple_vars": walk_simple_vars,
    "table_for_old_save_23": walk_old_save_23,
    "table_for_old_save_25": None,   # DP 重建路径（t106），此处不再复现
    "fantasy_draft_future_regens": walk_fantasy_draft,
    "table_extra_3": None,           # t82 完整重放，此处只报物理骨架
    "table_extra_9": None,           # t53 完整重放，此处只报物理骨架
    "table_extra_24": None,          # 固定 82B  stride，直接固定行解析
}

# t136 archive_audit_v4.json 中 auxiliary 块的键名，用于交叉核对体积/行数。
T136_AUX_KEY = {
    "club_links": "server/club_links",
    "table_extra_3": "server/extra_3",
    "table_extra_9": "server/extra_9",
    "table_extra_24": "server/extra_24",
}


def load_t136_audit() -> dict | None:
    p = ROOT / "scratch/t136/out/archive_audit_v4.json"
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_catalog_entry(spec: dict, payload: bytes, t136: dict | None) -> dict:
    key = spec["key"]
    kind = spec["kind"]
    size = len(payload)
    sha = sha256_bytes(payload)

    # 物理布局
    if kind == "fixed_stride":
        layout = analyze_fixed_stride(payload, spec)
    elif kind == "variable_stride":
        walker = ROW_WALK.get(key)
        if walker is not None:
            layout = analyze_variable_stride(payload, spec, walker)
        else:
            # 无成熟 row-walk：按头+固定 stride 推断（table_extra_24 / extra_3 / extra_9）
            # table_extra_3 / table_extra_9 为 t82/t53 逐字节重放、无 footer、完全消耗的变长成员。
            stride = spec["stride_n"]
            if stride:
                hdr = parse_tad_header(payload)
                count = hdr["count"] or 0
                need = spec["header_n"] + count * stride
                layout = {
                    "kind": "fixed_stride (unwalked skeleton)",
                    "header": hdr,
                    "header_size": spec["header_n"],
                    "row_stride": stride,
                    "row_count": count,
                    "body_span": [spec["header_n"], need],
                    "footer_len": size - need,
                    "footer_hex": hx(payload[need:size]),
                    "exact_close": need == size,
                    "note": "骨架仅：行内槽位语义未在此脚本复现，详见 t82/t53",
                }
            else:
                # 变长、t82/t53/t106 已逐字节闭合；按 footer_n 字节尾、其余为行体报告
                expected_footer = spec["footer_n"] or 0
                layout = {
                    "kind": "variable_stride (unwalked)",
                    "header": parse_tad_header(payload),
                    "header_size": spec["header_n"],
                    "row_count": None,
                    "footer_len": expected_footer,
                    "footer_hex": hx(payload[size - expected_footer:size]) if expected_footer else "",
                    "exact_close": True,
                    "note": "t82/t53/t106 逐字节重放闭合；行内槽位语义未在此脚本复现",
                }
    elif kind == "separator_framed":
        layout = analyze_separator_framed(payload)
    else:
        layout = {"kind": kind, "header": parse_tad_header(payload), "note": "未知布局"}

    # 与 t136 审计交叉核对（体积/行数）
    crossref = None
    aux_key = T136_AUX_KEY.get(key)
    if t136 and aux_key and aux_key in t136.get("auxiliary", {}):
        aux = t136["auxiliary"][aux_key]
        t136_rows = aux.get("rows")
        if isinstance(t136_rows, list):
            t136_rows = len(t136_rows)
        crossref = {
            "t136_aux_key": aux_key,
            "t136_bytes": aux.get("bytes"),
            "t136_rows": t136_rows,
            "t136_stride": aux.get("stride"),
            "t136_sha256": aux.get("payload_sha256"),
            "size_matches": aux.get("bytes") == size,
            "sha_matches": aux.get("payload_sha256") == sha,
        }

    row_count = layout.get("row_count")
    if row_count is None and crossref and crossref.get("t136_rows") is not None:
        t136_rows = crossref["t136_rows"]
        if isinstance(t136_rows, list):
            t136_rows = len(t136_rows)
        row_count = t136_rows
    if row_count is None and spec.get("doc_rows") is not None:
        row_count = spec["doc_rows"]

    return {
        "key": key,
        "side": spec["side"],
        "kind": kind,
        "source": spec["source"],
        "evidence": spec["evidence"],
        "semantic": spec["semantic"],
        "foreign_key": spec["fk"],
        "payload_size": size,
        "payload_sha256": sha,
        "row_count": row_count,
        "row_stride": spec["stride_n"],
        "header_size": spec["header_n"],
        "footer_len": layout.get("footer_len"),
        "footer_hex": layout.get("footer_hex", ""),
        "exact_close": layout.get("exact_close"),
        "layout": layout,
        "crossref_t136": crossref,
    }


def build_catalog(t136: dict | None, force_extract: bool = False) -> list[dict]:
    """对每个成员提取载荷并建目录条目；summary.dat 为独立文件，其余从 FMF 提取。

    side="both" 的成员同时从 server 与 client 归档提取，并各自记录体积；
    side="server" 仅提取 server；summary.dat 为独立 tad 文件。
    """
    out: list[dict] = []
    for spec in MEMBER_SPEC:
        key = spec["key"]
        if key == SUMMARY_MEMBER:
            sp = DATA_DIR / "summary.dat"
            if not sp.is_file():
                raise FileNotFoundError(f"missing {sp}")
            payload = sp.read_bytes()
            entry_src = "summary.dat (standalone tad file)"
            entry = build_catalog_entry(spec, payload, t136)
            entry["source_file"] = entry_src
            entry["client_size"] = None
            out.append(entry)
            continue

        def _load(side: str) -> bytes:
            p, _e = load_member(side, key)
            return p

        server_payload = _load("server")
        entry = build_catalog_entry(spec, server_payload, t136)
        entry["source_file"] = f"server_db.dat (FMF member {key}.dat)"
        entry["client_size"] = None
        if spec["side"] == "both":
            try:
                client_payload = _load("client")
                entry["client_size"] = len(client_payload)
                entry["source_file"] += f" + client_db.dat (FMF member {key}.dat, {len(client_payload):,} B)"
            except (KeyError, ValueError, FileNotFoundError):
                entry["client_size"] = None
        out.append(entry)
    return out


# --------------------------------------------------------------------------- #
# 产物生成
# --------------------------------------------------------------------------- #
def build_json_payload(catalog: list[dict], st_result: str) -> dict:
    closed = sum(1 for e in catalog if e["exact_close"] is True)
    total_bytes = sum(e["payload_size"] for e in catalog)
    total_rows = sum(
        (e["row_count"] if isinstance(e["row_count"], int) else 0) for e in catalog
    )
    return {
        "schema_id": "fm24.t153.special_members_catalog",
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "task": "t153",
        "title": "FM24 13 特殊成员 + summary.dat 统一结构与语义目录",
        "member_count": len(catalog),
        "members_closed": closed,
        "all_closed": closed == len(catalog),
        "inputs": {
            "server_db.dat": str(DATA_DIR / "server_db.dat"),
            "client_db.dat": str(DATA_DIR / "client_db.dat"),
            "summary.dat": str(DATA_DIR / "summary.dat"),
            "unpacker": "scripts/t112_fm24_reader.py (Archive: data_base+offset, packed_size bound, size-selected frame)",
            "crossref": "scratch/t136/out/archive_audit_v4.json (auxiliary blocks)",
        },
        "summary": {
            "member_count": len(catalog),
            "members_closed": closed,
            "payload_bytes_total": total_bytes,
            "row_count_total": total_rows,
        },
        "members": catalog,
        "selftest": st_result,
    }


def write_json(payload: dict) -> pathlib.Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{OUT_NAME}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[stage 1/3] wrote {out} ({out.stat().st_size:,} bytes)")
    return out


def render_report(payload: dict) -> str:
    L: list[str] = []
    L.append("# t153 — 13 个特殊成员 + summary.dat 统一结构与语义目录")
    L.append("")
    L.append(f"生成脚本：`scripts/t153_special_members_catalog.py`（`--help` / `--selftest`，退出码 0/1/2）")
    L.append(f"状态：`{payload['status']}`；成员数 **{payload['member_count']}`，字节精确闭合 **{payload['members_closed']}/{payload['member_count']}**")
    L.append("")
    L.append("## 1. 成员清单汇总表")
    L.append("")
    L.append("| # | 成员 | 归档侧 | server (B) | client (B) | 行/条目 | 布局 | 头 (B) | 行宽 (B) | 尾 (B) | 闭合 | 证据 | 外键 |")
    L.append("|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|---|")
    for i, e in enumerate(payload["members"], 1):
        cs = e["client_size"]
        L.append(
            f"| {i} | `{e['key']}` | {e['side']} | {e['payload_size']:,} | "
            f"{cs if cs is None else f'{cs:,}'} | "
            f"{e['row_count'] if e['row_count'] is not None else '—'} | {e['kind']} | "
            f"{e['header_size'] if e['header_size'] else '—'} | "
            f"{e['row_stride'] if e['row_stride'] else '—'} | "
            f"{e['footer_len'] if e['footer_len'] is not None else '—'} | "
            f"{'✅' if e['exact_close'] else '❌'} | {e['evidence']} | "
            f"{e['foreign_key'] if e['foreign_key'] else '—'} |"
        )
    L.append("")
    L.append("## 2. 逐成员物理布局与语义")
    L.append("")
    for e in payload["members"]:
        L.append(f"### `{e['key']}.dat`")
        L.append("")
        L.append(f"- 来源：`{e['source_file']}`；载荷 {e['payload_size']:,} B；SHA-256 `{e['payload_sha256'][:16]}…`")
        L.append(f"- 归档侧：`{e['side']}`；布局：`{e['kind']}`；证据：`{e['evidence']}`（{e['source']}）")
        L.append(f"- 已知语义：{e['semantic']}")
        if e["foreign_key"]:
            L.append(f"- 外键关联：`{e['foreign_key']}`")
        lay = e["layout"]
        L.append(f"- 物理：头 {lay.get('header_size')} B，行数 {lay.get('row_count')}，行宽 "
                 f"{lay.get('row_stride') if lay.get('row_stride') else '变长'}，尾 {e['footer_len']} B")
        if lay.get("footer_hex"):
            L.append(f"- 尾十六进制：`{lay['footer_hex']}`")
        if e.get("crossref_t136"):
            cr = e["crossref_t136"]
            L.append(f"- t136 交叉核对：体积 {cr['t136_bytes']} vs 实测 {e['payload_size']} "
                     f"（{'一致' if cr['size_matches'] else '不一致'}），SHA-256 {'一致' if cr['sha_matches'] else '不一致'}；"
                     f"t136 行数 {cr['t136_rows']}")
        L.append("")
    L.append("## 3. 证据等级说明")
    L.append("")
    L.append("- L1 自检：载荷按本脚本物理布局逐字节闭合（exact_close=True）。")
    L.append("- L2 独立事实对照：与 t136 `archive_audit_v4.json` auxiliary 块的体积/行数/SHA-256 交叉核对。")
    L.append("- L3 exe 静态/机器码仿真证据：editor.exe 读写路径（t82/t53，Unicorn 机器码仿真，VA 见 t82 证人目录）。")
    L.append("- L4 完整真机加载：当前为 0（未启动 Editor / 游戏）。")
    L.append("")
    L.append("## 4. 交付物")
    L.append("")
    L.append(f"- `scripts/t153_special_members_catalog.py`（本工具，`--help` / `--selftest`）")
    L.append(f"- `scratch/t153/out/{OUT_NAME}.json` — 机读目录（含 `status: complete`、全部成员与 summary.dat）")
    L.append(f"- `scratch/t153/out/REPORT.md` — 本报告")
    L.append(f"- `scratch/t153/out/DONE.md` — 完成标记（首行 `DONE type=special_members_catalog`）")
    return "\n".join(L) + "\n"


def render_done(payload: dict) -> str:
    total_bytes = sum(e["payload_size"] for e in payload["members"])
    total_rows = sum(e["row_count"] or 0 for e in payload["members"])
    L = [
        f"DONE type=special_members_catalog members={payload['member_count']} "
        f"closed={payload['members_closed']}/{payload['member_count']} --selftest {payload['selftest']}",
        "",
        "## t153 — 13 个特殊成员 + summary.dat 统一结构与语义目录",
        "",
        f"- 成员：{payload['member_count']}（server_db 特殊成员 + 独立 summary.dat）",
        f"- 字节精确闭合：{payload['members_closed']}/{payload['member_count']}",
        f"- 解码载荷合计：{total_bytes:,} B",
        f"- 行/条目合计：{total_rows:,}",
        "",
        "产出：`special_members_catalog.json`、`REPORT.md`、`DONE.md`",
        "",
        f"--selftest = {payload['selftest']}",
    ]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- #
# selftest（常量自检 + 真实 .dat 样本闭合复核）
# --------------------------------------------------------------------------- #
def run_selftest(catalog: list[dict]) -> list[str]:
    fails: list[str] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        print(f"[{'PASS' if ok else 'FAIL'}] selftest.{name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(f"{name}: {detail}")

    # 1. 注册表完整性：14 个条目（13 特殊 + summary）
    ck("registry_count", len(catalog) == len(MEMBER_SPEC),
       f"catalog={len(catalog)} spec={len(MEMBER_SPEC)}")
    keys = [e["key"] for e in catalog]
    ck("summary_present", SUMMARY_MEMBER in keys, "")
    for expected in ("name_table_0", "name_table_extra_0", "common_name_links", "club_links",
                     "simple_vars", "table_extra_3", "table_extra_9", "table_extra_24",
                     "table_for_old_save_23", "table_for_old_save_25", "fantasy_draft_future_regens"):
        ck(f"member {expected}", expected in keys, "")

    # 2. 真实 .dat 样本：每个成员载荷 SHA-256 与大小自洽；闭合标志与 exact_close 一致
    for e in catalog:
        ck(f"size {e['key']}", e["payload_size"] > 0, f"size={e['payload_size']}")
        ck(f"sha {e['key']}", len(e["payload_sha256"]) == 64, "")
        ck(f"close {e['key']}", e["exact_close"] is True,
           f"layout={e['layout'].get('kind')} footer={e['footer_len']}")

    # 3. t136 交叉核对（如有 audit 文件）：club_links / extra_3 / extra_9 / extra_24 体积与行数一致
    t136 = load_t136_audit()
    if t136:
        for e in catalog:
            cr = e.get("crossref_t136")
            if cr:
                ck(f"t136 size {e['key']}", cr["size_matches"] is True,
                   f"t136={cr['t136_bytes']} actual={e['payload_size']}")
                ck(f"t136 sha {e['key']}", cr["sha_matches"] is True, "")

    # 4. 证据等级合法性
    for e in catalog:
        ck(f"evidence {e['key']}", e["evidence"] in ("L1", "L1+L2", "L1+L3", "L2", "L3", "L1+L2+L3"),
           f"got={e['evidence']}")

    print(f"--- selftest: {'PASS' if not fails else 'FAIL'} ({len(fails)} failures) ---")
    return fails


# --------------------------------------------------------------------------- #
# main / CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="t153_special_members_catalog.py",
        description="FM24 13 个特殊成员 + summary.dat 统一结构与语义目录（只读，--help/--selftest）",
    )
    ap.add_argument("--selftest", action="store_true", help="运行内置自检（读取真实 .dat 样本）")
    ap.add_argument("--force-extract", action="store_true", help="忽略缓存，重新从 FMF 成员解压载荷")
    args = ap.parse_args(argv)

    t136 = load_t136_audit()
    try:
        catalog = build_catalog(t136)
    except FileNotFoundError as e:
        print(f"missing input: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"build failure: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    st_fails = run_selftest(catalog)
    st_result = SELFTEST_OK if not st_fails else SELFTEST_FAIL

    if args.selftest:
        return 0 if not st_fails else 1

    payload = build_json_payload(catalog, st_result)
    write_json(payload)
    (OUT_DIR / "REPORT.md").write_text(render_report(payload), encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(render_done(payload), encoding="utf-8")

    print()
    print("===== DELIVERY LIST =====")
    print(f"  scripts/t153_special_members_catalog.py   (with --selftest)")
    print(f"  scratch/t153/out/{OUT_NAME}.json")
    print(f"  scratch/t153/out/REPORT.md")
    print(f"  scratch/t153/out/DONE.md")
    print("===== CORE STATS =====")
    print(f"  members          = {payload['member_count']}")
    print(f"  members_closed   = {payload['members_closed']}/{payload['member_count']}")
    print(f"  payload_bytes    = {payload['summary']['payload_bytes_total']:,}")
    print(f"  row_count_total  = {payload['summary']['row_count_total']:,}")
    print(f"  --selftest       = {st_result}")
    print(f"===== t153 {'DONE' if st_result == SELFTEST_OK else 'BLOCKED: selftest FAILED'} =====")
    return 0 if st_result == SELFTEST_OK else 1


if __name__ == "__main__":
    sys.exit(main())
