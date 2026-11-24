#!/usr/bin/env python3
"""t112_fm24_reader — FM24 数据库纯 Python 高速只读多表解析库.

把前期逆向成果（t96c Unicorn wire traces + t110 L3 4CC 总账 + t98 STARTING_RECORD
行走）落地成一个不依赖 Unicorn / IDA 的实用解码器：

  * 容器层：FMF 归档（data_base + zstd 帧，成员边界 = 帧边界，size 选帧）。
  * payload 层：13 字节头（magic 6B + version u16 + row_count u32 + 保留 1B）
    + 每行 [1 字节 flag + 行体] + 尾部 9 字节闭合窗（末行 identity 终止符 0x00
    + 8 字节文件 footer）。
  * 行层：两类解码器 ——
      fixed   : t96c 实测 row0 读序列在 `13 + nrows*(1+rowlen) == footer_off`
                方程成立时泛化为全行定长布局（struct 一次解一行，秒级跑百万行；
                每行全字段 unpack，仅样例行物化成 dict）。
      variable: 从 t95/funcs slot19 C 逆向手写的行程序（字符串 u32 长度前缀、
                向量 u32/u8/u16 计数、a7 服务器门、identity 12B），逐行解释执行。
  * 命名层：t110 L3 4CC 按 row0 线偏移绑定字段名；无 4CC 处诚实命名
    `col_<row0_off>`；每行尾部 12B identity 解出 ordinal/uid/dbid。

CLI（退出码 0 成功 / 1 校验失败 / 2 用法或致命错误）:
  py -V:3.12 -I -B scripts/t112_fm24_reader.py --list
  py -V:3.12 -I -B scripts/t112_fm24_reader.py --dump server 45 --limit 5
  py -V:3.12 -I -B scripts/t112_fm24_reader.py --verify-all [--out DIR]
  py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest

只读输入：scratch/data/*_db.dat、scratch/t96c/out/wire_traces_master.json、
scratch/t110/out/master_67tables_l3.json。不修改 reports/ 与 LEDGER.json。
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import pathlib
import struct
import sys
import time
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "scratch/data"
TRACE_JSON = ROOT / "scratch/t96c/out/wire_traces_master.json"
L3_JSON = ROOT / "scratch/t110/out/master_67tables_l3.json"
DEFAULT_OUT = ROOT / "scratch/t112/out"

UPSTREAM_ZSTD = pathlib.Path(str(_cfg.VENDOR_DIR))

DAT_MAGIC = b"\x03\x01tad."
FMF_MAGIC = bytes.fromhex("0201666d662e080000")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")
MAX_PAYLOAD = 256 * 1024 * 1024
HEADER_END = 13          # 头 13 字节：0..6 magic, 6..8 version, 8..12 count, 12 保留
FOOTER_SIZE = 9          # [末行 identity 终止符 0x00][8B 文件 footer]
IDENTITY_SIZE = 12       # [ordinal u32][uid u32][dbid u32]

IDENTITY_CALLERS = {"0x143dcb71c"}  # t96c traces 里 identity 读的调用点

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ---------------------------------------------------------------- zstd
def _zstd():
    import importlib.util

    spec = importlib.util.find_spec("zstandard")
    if spec is None and UPSTREAM_ZSTD.is_dir():
        sys.path.insert(0, str(UPSTREAM_ZSTD))
        spec = importlib.util.find_spec("zstandard")
    if spec is None:
        raise RuntimeError("vendored zstandard not found (D:\\tmp2b\\fm24\\tools\\python)")
    return importlib.import_module("zstandard")


# ---------------------------------------------------------------- FMF 归档层
class _DirectoryReader:
    """FMF 目录树读取（与上游 modding_read_dbdat 同构，只读）。"""

    MAX_STRING = 1024 * 1024

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0
        self.entries: list[dict] = []

    def _take(self, n: int) -> bytes:
        if self.pos + n > len(self.data):
            raise ValueError(f"truncated FMF directory at 0x{self.pos:x}")
        v = self.data[self.pos : self.pos + n]
        self.pos += n
        return v

    def u32(self) -> int:
        return struct.unpack("<I", self._take(4))[0]

    def string(self) -> str:
        n = self.u32()
        if n > self.MAX_STRING:
            raise ValueError(f"oversized FMF directory string: {n}")
        return self._take(n).decode("utf-8")

    def directory(self, parent: str = "", depth: int = 0) -> None:
        if depth > 40:
            raise ValueError("FMF directory nesting exceeds 40")
        folder = self.string()
        current = f"{parent}{folder}/"
        for _ in range(self.u32()):
            name, ext = self.string(), self.string()
            offset, packed, size, _t1, _t2 = struct.unpack("<5Q", self._take(40))
            self.entries.append(
                {
                    "path": current + name + ext,
                    "offset": offset,
                    "packed_size": packed,
                    "size": size,
                }
            )
        for _ in range(self.u32()):
            self.directory(current, depth + 1)


def archive_layout(data: bytes) -> dict:
    start = 8 if data.startswith(DAT_MAGIC) and data[8:17] == FMF_MAGIC else 0
    if data[start : start + 9] != FMF_MAGIC:
        raise ValueError("no embedded resource-FMF signature")
    toc = start + 9 + struct.unpack_from("<Q", data, start + 9)[0]
    base = start + 9 + struct.unpack_from("<Q", data, start + 17)[0]
    if not (start + 26 <= base <= toc < len(data)):
        raise ValueError(f"FMF offsets outside file: base={base}, toc={toc}")
    if data[toc : toc + 9] != FMF_MAGIC:
        raise ValueError(f"missing secondary FMF header at 0x{toc:x}")
    zstd = _zstd()
    d = zstd.ZstdDecompressor()
    obj = d.decompressobj()
    dir_bytes = obj.decompress(data[toc + 9 :])
    if not obj.eof:
        raise ValueError("FMF directory frame not closed")
    reader = _DirectoryReader(dir_bytes)
    reader.directory()
    if reader.pos != len(dir_bytes):
        raise ValueError(f"unparsed FMF directory bytes: {len(dir_bytes) - reader.pos}")
    return {"data_base": base, "toc_offset": toc, "entries": reader.entries}


def _decode_frames(region: bytes) -> list[dict]:
    """在字节区间内逐帧解压，绝不越过区间（成员边界 = 帧边界）。"""
    zstd = _zstd()
    d = zstd.ZstdDecompressor()
    frames: list[dict] = []
    data = region
    pos = 0
    while data[:4] == ZSTD_MAGIC:
        obj = d.decompressobj()
        chunk = obj.decompress(data)
        consumed = len(data) - len(obj.unused_data)
        frames.append({"member_offset": pos, "length": len(chunk), "data": chunk})
        if not obj.eof or consumed <= 0:
            break
        pos += consumed
        data = obj.unused_data
    return frames


class Archive:
    """一个 *_db.dat 归档的只读句柄：TOC 定位 + 按表取 payload。"""

    def __init__(self, name: str):
        self.name = name
        path = DB_DIR / f"{name}_db.dat"
        if not path.is_file():
            raise FileNotFoundError(path)
        self.path = path
        self.data = path.read_bytes()
        layout = archive_layout(self.data)
        self.data_base = layout["data_base"]
        self.entries = {e["path"]: e for e in layout["entries"]}

    def entry(self, tid: int) -> dict:
        path = f"{self.name}_db/table_{tid}.dat"
        if path not in self.entries:
            raise KeyError(f"{self.name} archive has no table_{tid}.dat")
        return self.entries[path]

    def payload(self, tid: int) -> bytes:
        """成员定位（data_base+offset）→ 帧枚举（packed_size 有界）→ size 选帧。

        P1 失败（截断/无 size 命中）时扩到下一成员起点重试一次（t38 P2 策略）。
        """
        entry = self.entry(tid)
        base = self.data_base
        start = base + entry["offset"]
        size = int(entry["size"])

        def _attempt(end: int) -> tuple[list[dict], list[dict]]:
            frames = _decode_frames(self.data[start:end])
            hits = [f for f in frames if f["length"] == size]
            return frames, hits

        frames, hits = _attempt(start + int(entry["packed_size"]))
        if len(hits) != 1:
            nxt = sorted(
                base + e["offset"] for e in self.entries.values() if e["offset"] > entry["offset"]
            )
            if nxt:
                frames, hits = _attempt(nxt[0])
        if not frames:
            raise ValueError(f"{self.name}#{tid}: no zstd frame in member")
        if len(hits) != 1:
            raise ValueError(f"{self.name}#{tid}: {len(hits)} frames with length==size ({size})")
        raw = hits[0]["data"]
        if len(raw) > MAX_PAYLOAD:
            raise ValueError(f"{self.name}#{tid}: payload over safety limit")
        return raw


# ---------------------------------------------------------------- 行程序 VM
# op = ('u', n) 定宽无符号整数 | ('s',) u32 长度前缀字符串 | ('id',) 12B identity
#      ('v', count_op, elem_ops) 向量 | ('rep', n, ops) 固定次数重复块
_P1, _P2, _P4, _P8 = ("u", 1), ("u", 2), ("u", 4), ("u", 8)
_STR, _ID = ("s",), ("id",)

PROG_T7_SERVER = [
    _STR, _P1,
    ("v", _P4, [_P1]),
    _STR, _STR, _P1, _P1,
    ("v", _P4, [_P4]), _P4,
    ("v", _P4, [_P4]),
    ("v", _P4, [_P4]),
    _P4,
    ("v", _P4, [_P4, _P4, _STR]),
    # --- a7 != 0（server_db）专属块 ---
    _P1, _P1, _P4, ("v", _P1, [_P4]),
    ("v", _P4, [_P4]), _P1, _ID,
]
PROG_T7_CLIENT = [
    _STR, _P1,
    ("v", _P4, [_P1]),
    _STR, _STR, _P1, _P1,
    ("v", _P4, [_P4]), _P4,
    ("v", _P4, [_P4]),
    ("v", _P4, [_P4]),
    _P4,
    ("v", _P4, [_P4, _P4, _STR]),
    ("v", _P4, [_P4]), _P1, _ID,
]
PROG_T8 = [_STR, _P1, _P1, _P1, _P2, _P2, _P2, _P4, _P4, _ID]
PROG_T12_SERVER = [
    _P4, _P2, _P4, _P4, _P4, _P2, _P2, _P2, _P2, _P2, _P2, _P4, _P4, _P4,
    _STR, _STR, _STR, _P8, _P8, _P8, _P4, _P4, _P4, _P1, _P1, _P1, _P1, _P1, _ID,
]
_PROG_T18_HEAD = [_STR, _STR, _STR, _STR, _P4, _P4, _P4, _P4, _P4, _P4, _P4]
_PROG_T18_TAIL = [_P1, _P1, _P1, _P1, _P1, _P1, _P1, _P1, _ID]
PROG_T18_SERVER = _PROG_T18_HEAD + [_P2, _P2, _P2] + _PROG_T18_TAIL
PROG_T18_CLIENT = _PROG_T18_HEAD + _PROG_T18_TAIL
_T27_ITER = [_P2] + [_P1] * 21
PROG_T27 = [_STR, _P1, _P1, _P1, ("rep", 4, _T27_ITER), _ID]
PROG_T41 = [_STR, _STR, _STR, _STR, _P4, ("v", _P4, [_P1, _P2, _P4]), _ID]
PROG_T47 = [_P4, _P4] + [_P1] * 11 + [_P2, _P1, ("v", _P2, [_P4, _P1]), _P4, _ID]
PROG_T59 = [_P4, _P1, ("v", _P4, [_P1, _P8, _P1]), _ID]
# t45/t48 STARTING_RECORD：17 列前缀 + u32 namelen + 名字 + 26B 尾 + identity 12B
# （rowlen == 80 + namelen，含 flag 字节；t98 已证 84,477/5,210 行全闭合）
PROG_T45 = [
    _P4, _P1, _P8, _P8, _P8, _P8,
    _STR,
    _P4, _P4, _P4, _P4, _P2, _P2, _P2, _P1, _P1, _P1, _P1,
    _ID,
]

VARIABLE_PROGRAMS: dict[tuple[str, int], list] = {
    ("server", 7): PROG_T7_SERVER,
    ("client", 7): PROG_T7_CLIENT,
    ("server", 8): PROG_T8,
    ("client", 8): PROG_T8,
    ("server", 12): PROG_T12_SERVER,
    ("server", 18): PROG_T18_SERVER,
    ("client", 18): PROG_T18_CLIENT,
    ("server", 27): PROG_T27,
    ("client", 27): PROG_T27,
    ("server", 41): PROG_T41,
    ("client", 41): PROG_T41,
    ("server", 45): PROG_T45,
    ("server", 48): PROG_T45,
    ("server", 47): PROG_T47,
    ("client", 47): PROG_T47,
    ("server", 59): PROG_T59,
}

# t10 NATION —— 头/尾按 a7 分块（Unicorn row0 实测 + slot19 C 逆向 1410404C0）。
# 三个缺 .c 的元素解析器（sub_1415CFD70 / sub_141072F60 / sub_1415CFEA0）的线格式
# 由全表 251 行字节记账 + identity 序号锚定穷举求解：CFD70=[u8,str,str,7×u32]
# （变长、含人名双字符串）、72F60=14B、CFEA0=7×u32（28B，slot5/6 为 DATE 型值）；
# 605B0=[u32,DATE,DATE] 由 client 全表闭合独立证实（12B）。
_T10_25B = [_P1, _P4, _P4, _P4, _P2, _P1, _P1, _P4, _P1, _P1, _P2]  # sub_14144C6A0
_T10_12B = [_P4, _P4, _P4]                                          # u32 + 2×DATE
_T10_CFD70 = [_P1, _STR, _STR, _P4, _P4, _P4, _P4, _P4, _P4, _P4]   # sub_1415CFD70
_T10_72F60 = [_P1, _P4, _P4, _P1, _P1, _P2, _P1]                    # sub_141072F60 (14B)
_T10_CFEA0 = [_P4, _P4, _P4, _P4, _P4, _P4, _P4]                    # sub_1415CFEA0 (28B)
PROG_T10_SERVER = [
    _P4,
    ("v", _P2, [_P4]),
    ("v", _P4, [_P4]),
    ("v", _P2, _T10_CFD70),
    _P4, _P4, _P4, _P4, _P4, _P4,
    ("v", _P4, _T10_25B),
    ("v", _P4, _T10_12B),
    ("v", _P4, _T10_72F60),
    _P1, _P4, _P4, _P4, _P4, _P1, _P1, _P4, _P1,
    ("v", _P1, [_P4, _P1]),
    ("v", _P4, _T10_CFEA0),
    ("v", _P4, _T10_CFEA0),
    ("v", _P4, _T10_12B),
    _P4, _P4, _P4, _P4, _P4, _P4, _P4, _P4, _P4, _P4, _P2, _P1,
    _ID,
]
PROG_T10_CLIENT = [
    _P1, _P4, _P4, _P4, _P4, _P1, _P1, _P4, _P1,
    ("v", _P1, [_P4, _P1]),
    ("v", _P4, _T10_CFEA0),
    ("v", _P4, _T10_CFEA0),
    ("v", _P4, _T10_12B),
    _ID,
]
VARIABLE_PROGRAMS[("server", 10)] = PROG_T10_SERVER
VARIABLE_PROGRAMS[("client", 10)] = PROG_T10_CLIENT


class WireError(ValueError):
    """行解码越界/结构不符（诚实失败，不吞错）。"""


def decode_row(mv: memoryview, start: int, limit: int, prog: list) -> tuple[list, list, int]:
    """解释一行程序（读上界 limit=footer_off，防越界进 footer）。

    返回 (值列表, [(槽位|None, 行内偏移, 宽)], 行尾绝对位置)。
    槽位 None 的 touched 项是向量计数读取，不是独立字段。
    """
    pos = start
    touched: list[tuple[int | None, int, int]] = []
    values: list = []

    def walk(ops: list) -> None:
        nonlocal pos
        for op in ops:
            kind = op[0]
            off0 = pos - start
            if kind == "u":
                n = op[1]
                if pos + n > limit:
                    raise WireError(f"u{n} read at {pos} beyond limit {limit}")
                values.append(int.from_bytes(mv[pos : pos + n], "little"))
                touched.append((len(values) - 1, off0, n))
                pos += n
            elif kind == "s":
                if pos + 4 > limit:
                    raise WireError(f"string len at {pos} beyond limit {limit}")
                ln = int.from_bytes(mv[pos : pos + 4], "little")
                if pos + 4 + ln > limit:
                    raise WireError(f"string len {ln} at {pos} beyond limit {limit}")
                values.append(bytes(mv[pos + 4 : pos + 4 + ln]).decode("utf-8", errors="replace"))
                touched.append((len(values) - 1, off0, 4 + ln))
                pos += 4 + ln
            elif kind == "id":
                if pos + IDENTITY_SIZE > limit:
                    raise WireError(f"identity at {pos} beyond limit {limit}")
                ordinal, uid, dbid = struct.unpack_from("<III", mv, pos)
                values.append({"ordinal": ordinal, "uid": uid, "dbid": dbid})
                touched.append((len(values) - 1, off0, IDENTITY_SIZE))
                pos += IDENTITY_SIZE
            elif kind == "v":
                count_kind, elem = op[1], op[2]
                cn = count_kind[1]
                if pos + cn > limit:
                    raise WireError(f"vector count at {pos} beyond limit {limit}")
                cnt = int.from_bytes(mv[pos : pos + cn], "little")
                touched.append((None, off0, cn))
                pos += cn
                for _ in range(cnt):
                    walk(elem)
            elif kind == "rep":
                for _ in range(op[1]):
                    walk(op[2])
            else:  # pragma: no cover
                raise WireError(f"unknown op {op}")

    walk(prog)
    if pos > limit:
        raise WireError(f"row end {pos} beyond limit {limit}")
    return values, touched, pos


# ---------------------------------------------------------------- L3 命名
def _l3_name_map(l3: dict | None, table_type: int, archive: str) -> dict[int, str]:
    """row0 线偏移（wire_off + in_slot）→ 4CC。direct_field 优先，DELE 最后。"""
    if not l3:
        return {}
    rec = next((t for t in l3.get("tables", []) if t.get("table_type") == table_type), None)
    if not rec:
        return {}
    rank = {"direct_field": 0, "subobj_deref": 1, "resolved_via_helper": 2, "bitfield": 3}
    best: dict[int, tuple[int, int, str]] = {}
    for j in rec.get("joined_l3_fourccs", []):
        if j.get("archive") != archive:
            continue
        pos = int(j["wire_off_row0"]) + int(j.get("in_slot_off") or 0)
        fourcc = j["fourcc"]
        pri = (rank.get(j.get("access_kind"), 4), 0 if fourcc != "DELE" else 1)
        cur = best.get(pos)
        if cur is None or pri < (cur[0], cur[1]):
            best[pos] = (pri[0], pri[1], fourcc)
    return {pos: v[2] for pos, v in best.items()}


def _dedup(names: list[str]) -> list[str]:
    """同名冲突：保持首个，后续加 #序号。"""
    seen: Counter = Counter()
    out: list[str] = []
    for nm in names:
        if not nm:
            out.append(nm)
            continue
        seen[nm] += 1
        out.append(nm if seen[nm] == 1 else f"{nm}#{seen[nm]}")
    return out


def rows_to_dict(values: list, names: list[str]) -> dict:
    row: dict = {}
    for slot, nm in enumerate(names):
        if nm and slot < len(values):
            row[nm] = values[slot]
    return row


# ---------------------------------------------------------------- 表注册
class TableSpec:
    def __init__(self, archive: str, tid: int, klass: str, kind: str):
        self.archive = archive
        self.tid = tid
        self.klass = klass
        self.kind = kind          # fixed | variable | empty
        self.rowlen: int | None = None
        self.prog: list | None = None
        self.row0_reads: list[dict] | None = None
        self.unsupported_reason: str | None = None

    @property
    def key(self) -> str:
        return f"{self.archive}/{self.tid}"


def _skip(spec: TableSpec, reason: str) -> dict:
    return {"archive": spec.archive, "table_id": spec.tid, "class": spec.klass, "reason": reason}


def build_registry(traces: dict) -> tuple[list[TableSpec], list[dict]]:
    """由 t96c traces + 手写变量程序生成可解码表注册表。

    fixed 判据：row_len 唯一 && 13 + nrows*(1+rowlen) == footer_off
               && row0 读序列恰好覆盖整个行体（含末尾 identity 12B）。
    """
    specs: list[TableSpec] = []
    skipped: list[dict] = []
    for t in traces["tables"]:
        arch, tid = t["archive"], int(t["table_id"])
        spec = TableSpec(arch, tid, t["class"], "?")
        footer_off = int(t["footer_off"])
        nrows = int(t["rows_header"])
        rowlen = t.get("row_len_min")
        reads = t.get("row0_reads") or []

        if nrows == 0:
            if footer_off == HEADER_END and t.get("closed_to_footer"):
                spec.kind = "empty"
                specs.append(spec)
            else:
                spec.unsupported_reason = "0-row but header/footer inconsistent"
                skipped.append(_skip(spec, spec.unsupported_reason))
            continue

        width_sum = sum(r["n"] if isinstance(r["n"], int) else 0 for r in reads)
        identity_like = bool(reads) and reads[-1]["n"] == IDENTITY_SIZE and (
            reads[-1].get("caller") in IDENTITY_CALLERS
            or reads[-1]["wire_pos"] + IDENTITY_SIZE == rowlen
        )
        fixed_ok = (
            rowlen is not None
            and t.get("row_len_max") == rowlen
            and HEADER_END + nrows * (1 + rowlen) == footer_off
            and width_sum == rowlen
            and identity_like
            and tid not in (45, 48)
        )
        if fixed_ok:
            spec.kind = "fixed"
            spec.rowlen = int(rowlen)
            spec.row0_reads = reads
            specs.append(spec)
            continue

        if (arch, tid) in VARIABLE_PROGRAMS:
            spec.kind = "variable"
            spec.prog = VARIABLE_PROGRAMS[(arch, tid)]
            specs.append(spec)
            continue

        reason = "no wire closure equation / no hand-written program"
        if (arch, tid) == ("server", 29):
            reason = "slot19 C (sub_1445195D0 chain) incomplete in scratch/t95/funcs"
        spec.unsupported_reason = reason
        skipped.append(_skip(spec, reason))
    return specs, skipped


# ---------------------------------------------------------------- 解码器
class TableReader:
    """单表解码器：一次命名绑定，整表跑行（fixed 走 struct 快路径）。"""

    def __init__(self, spec: TableSpec, l3: dict | None):
        self.spec = spec
        self.l3map = _l3_name_map(l3, spec.tid, spec.archive)
        self.names: list[str] | None = None
        self.l3_named = 0
        self._fixed_fmt: struct.Struct | None = None
        self._fixed_fields: list[tuple[str, int, int, str | None]] = []

    # ---- 命名绑定 ----
    def _count_named(self, names: list[str]) -> int:
        return sum(
            1 for nm in names
            if nm and not nm.startswith("col_") and nm != "identity" and "#" not in nm
        )

    def _bind_variable(self, values: list, touched: list) -> list[str]:
        names: list[str] = []
        for slot, off, _w in touched:
            if slot is None:
                names.append("")
                continue
            v = values[slot]
            if isinstance(v, dict) and set(v) == {"ordinal", "uid", "dbid"}:
                names.append("identity")
            else:
                names.append(self.l3map.get(off) or f"col_{off}")
        names = _dedup(names)
        self.names = names
        self.l3_named = self._count_named(names)
        return names

    def _fixed_setup(self) -> None:
        """把 row0 读序列编译成覆盖整行的 struct（空隙补 col_<off> 原始字节）。

        identity 12B 读拆成 3×u32（ordinal/uid/dbid），物化为 row['identity']。
        """
        reads = self.spec.row0_reads or []
        rowlen = self.spec.rowlen or 0
        covered = bytearray(rowlen)
        fields: list[tuple[str, int, int, str | None]] = []
        for r in reads:
            off, width = r["wire_pos"], r["n"]
            if off + width > rowlen:
                continue
            for b in range(off, off + width):
                covered[b] = 1
            if width == IDENTITY_SIZE and (
                r.get("caller") in IDENTITY_CALLERS or off + width == rowlen
            ):
                for sub, dw in (("ordinal", 0), ("uid", 4), ("dbid", 8)):
                    fields.append(("identity", off + dw, 4, sub))
            else:
                nm = self.l3map.get(off) or f"col_{off}"
                fields.append((nm, off, width, None))
        for off in range(rowlen):
            if not covered[off]:
                fields.append((f"col_{off}", off, 1, None))
        fields.sort(key=lambda f: f[1])
        parts = []
        for f in fields:
            if f[2] in (1, 2, 4, 8):
                parts.append({1: "B", 2: "H", 4: "I", 8: "Q"}[f[2]])
            else:  # 非标宽读（如 CITY 的 3 字节 Calt 跨度）：按原始字节保真
                parts.append(f"{f[2]}s")
        self._fixed_fmt = struct.Struct("<" + "".join(parts))
        names = _dedup([f[0] if f[3] is None else "identity" for f in fields])
        self._fixed_fields = [(nm, f[1], f[2], f[3]) for nm, f in zip(names, fields)]
        flat_names = [nm for nm in names]
        self.l3_named = sum(
            1 for nm, f in zip(flat_names, fields)
            if nm and not nm.startswith("col_") and nm != "identity" and "#" not in nm
            and f[3] is None
        )

    # ---- 单行解码 ----
    def decode_row_into(self, mv: memoryview, start: int, limit: int) -> tuple[dict, int]:
        """解码一行；返回 (行字典, 行尾绝对位置)。仅用于样例行/小表。"""
        if self.spec.kind == "fixed":
            vals = self._fixed_fmt.unpack_from(mv, start)
            row: dict = {}
            ident: dict | None = None
            for (nm, _off, _w, sub), v in zip(self._fixed_fields, vals):
                if sub is not None:
                    ident = ident or {}
                    ident[sub] = v
                elif isinstance(v, (bytes, bytearray)):
                    row[nm] = v.hex()
                else:
                    row[nm] = v
            if ident is not None:
                row["identity"] = ident
            return row, start + (self.spec.rowlen or 0)
        values, touched, end = decode_row(mv, start, limit, self.spec.prog)
        if self.names is None:
            self._bind_variable(values, touched)
        return rows_to_dict(values, self.names), end

    def decode_row_fast(self, mv: memoryview, start: int, limit: int) -> tuple[list, int]:
        """整表跑行用的快路径：解出全部字段值但不物化 dict。"""
        if self.spec.kind == "fixed":
            return list(self._fixed_fmt.unpack_from(mv, start)), start + (self.spec.rowlen or 0)
        values, _touched, end = decode_row(mv, start, limit, self.spec.prog)
        return values, end

    # ---- 整表校验 ----
    def verify(self, payload: bytes, sample_limit: int = 3) -> dict:
        t0 = time.perf_counter()
        mv = memoryview(payload)
        nrows = struct.unpack_from("<I", payload, 8)[0]
        footer_off = len(payload) - FOOTER_SIZE
        flags: Counter = Counter()
        row_lens: Counter = Counter()
        samples: list[dict] = []
        err: str | None = None
        pos = HEADER_END
        count = 0
        try:
            if self.spec.kind == "fixed":
                rowlen = self.spec.rowlen or 0
                step = 1 + rowlen
                if HEADER_END + nrows * step != footer_off:
                    raise WireError("footer equation mismatch")
                self._fixed_setup()
                for i in range(nrows):
                    p = HEADER_END + i * step
                    flags[payload[p]] += 1
                    if i < sample_limit:
                        row, _ = self.decode_row_into(mv, p + 1, footer_off)
                        samples.append(row)
                    else:
                        _, end = self.decode_row_fast(mv, p + 1, footer_off)
                        if end != p + 1 + rowlen:
                            raise WireError(f"row {i} end {end} != expected {p + 1 + rowlen}")
                    count += 1
                pos = footer_off
                row_lens[rowlen] += nrows
            elif self.spec.kind == "variable":
                if self.names is None and nrows:
                    # 先解 row0 完成命名绑定（同时产出样例行）
                    flags[payload[pos]] += 1
                    row0, end0 = self.decode_row_into(mv, pos + 1, footer_off)
                    samples.append(row0)
                    row_lens[end0 - (pos + 1)] += 1
                    pos, count = end0, 1
                for i in range(count, nrows):
                    if pos >= footer_off:
                        raise WireError(f"row {i}: pos {pos} >= footer {footer_off}")
                    flags[payload[pos]] += 1
                    if i < sample_limit:
                        row, end = self.decode_row_into(mv, pos + 1, footer_off)
                        samples.append(row)
                    else:
                        _, end = self.decode_row_fast(mv, pos + 1, footer_off)
                    row_lens[end - (pos + 1)] += 1
                    pos = end
                    count += 1
            else:  # empty
                if nrows or footer_off != HEADER_END:
                    raise WireError("0-row table with non-empty body")
                pos = footer_off
        except WireError as exc:
            err = f"row {count}: {exc}"
        except (struct.error, UnicodeDecodeError) as exc:
            err = f"row {count}: {type(exc).__name__}: {exc}"
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "archive": self.spec.archive,
            "table_id": self.spec.tid,
            "class": self.spec.klass,
            "kind": self.spec.kind,
            "rows_header": nrows,
            "rows_decoded": count,
            "elapsed_ms": round(elapsed_ms, 1),
            "footer_closed": err is None and pos == footer_off and count == nrows,
            "footer9_hex": bytes(payload[footer_off:]).hex(),
            "flags_seen": {hex(k): v for k, v in sorted(flags.items())},
            "row_len_min": min(row_lens) if row_lens else None,
            "row_len_max": max(row_lens) if row_lens else None,
            "l3_named_fields": self.l3_named,
            "error": err,
            "sample_rows": samples,
        }


# ---------------------------------------------------------------- 校验驱动
def load_traces() -> dict:
    return json.loads(TRACE_JSON.read_text(encoding="utf-8"))


def load_l3() -> dict | None:
    if L3_JSON.is_file():
        return json.loads(L3_JSON.read_text(encoding="utf-8"))
    return None


def verify_all(out_dir: pathlib.Path, sample_limit: int = 3) -> tuple[dict, list]:
    traces = load_traces()
    l3 = load_l3()
    specs, skipped = build_registry(traces)
    archives: dict[str, Archive] = {}
    results: list[dict] = []
    t_start = time.perf_counter()
    for spec in specs:
        try:
            arc = archives.get(spec.archive)
            if arc is None:
                arc = Archive(spec.archive)
                archives[spec.archive] = arc
            payload = arc.payload(spec.tid)
        except Exception as exc:  # 归档层失败也诚实记录
            results.append(
                {
                    "archive": spec.archive, "table_id": spec.tid, "class": spec.klass,
                    "kind": spec.kind, "rows_header": 0, "rows_decoded": 0, "elapsed_ms": 0.0,
                    "footer_closed": False, "footer9_hex": "", "flags_seen": {},
                    "row_len_min": None, "row_len_max": None, "l3_named_fields": 0,
                    "error": f"archive: {exc}", "sample_rows": [],
                }
            )
            continue
        results.append(TableReader(spec, l3).verify(payload, sample_limit=sample_limit))
    total_ms = (time.perf_counter() - t_start) * 1000.0

    closed = [r for r in results if r["footer_closed"]]
    failed = [r for r in results if not r["footer_closed"]]
    verify = {
        "status": "complete" if not failed else "partial",
        "schema_id": "fm24.t112.reader_verify",
        "schema_version": 1,
        "inputs": {
            "traces": str(TRACE_JSON.relative_to(ROOT)),
            "l3_master": str(L3_JSON.relative_to(ROOT)),
            "db_dir": str(DB_DIR),
        },
        "elapsed_total_ms": round(total_ms, 1),
        "summary": {
            "tables_supported": len(results),
            "tables_closed": len(closed),
            "tables_failed": len(failed),
            "tables_skipped": len(skipped),
            "rows_decoded_total": sum(r["rows_decoded"] for r in results),
            "fixed_tables": sum(1 for r in results if r["kind"] == "fixed"),
            "variable_tables": sum(1 for r in results if r["kind"] == "variable"),
            "empty_tables": sum(1 for r in results if r["kind"] == "empty"),
            "l3_named_field_total": sum(r["l3_named_fields"] for r in results),
        },
        "tables": {f"{r['archive']}/{r['table_id']}": r for r in results},
        "skipped_tables": skipped,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "reader_verify.json").write_text(
        json.dumps(verify, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return verify, results


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    fails: list[str] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        if not ok:
            fails.append(f"{name}: {detail}")
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))

    # --- 1 VM 单元（合成字节，不依赖数据文件） ---
    body = (
        b"\x08\x00\x00\x00Albanian"          # string 'Albanian'
        + b"\x00\x0f\x01"                    # 3 × u8
        + b"\x2c\x00\x01\x00\x14\x00"        # 3 × u16
        + b"\x7e\x00\x00\x00\x01\x00\x00\x00"  # 2 × u32
        + b"\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00"  # identity 12B
    )
    payload = (
        DAT_MAGIC + struct.pack("<H", 0xDF1) + struct.pack("<I", 1) + b"\x00"
        + b"\x00" + body                      # flag + body
        + b"\x00\x00\x00\x00\x01\x00\x00\x00\x00"  # 9B footer (term 00 + footer8)
    )
    spec = TableSpec("unit", 8, "LANGUAGE", "variable")
    spec.prog = PROG_T8
    res = TableReader(spec, None).verify(payload, sample_limit=3)
    ck("vm t8 1-row closure", res["footer_closed"] and res["error"] is None, str(res["error"]))
    ck("vm t8 identity", res["sample_rows"][0]["identity"]["uid"] == 1, "")
    ck("vm t8 fallback col names", any(k.startswith("col_") for k in res["sample_rows"][0]), "")

    # 越界负结果：字符串长度越过 footer 必须报错而非静默
    bad = bytearray(payload)
    bad[14] = 0xFF  # string len -> 0x000000ff
    spec_bad = TableSpec("unit", 8, "LANGUAGE", "variable")
    spec_bad.prog = PROG_T8
    res_bad = TableReader(spec_bad, None).verify(bytes(bad), sample_limit=1)
    ck("vm negative bounds", not res_bad["footer_closed"] and res_bad["error"] is not None,
       str(res_bad["error"])[:60])

    # --- 2 注册表组成（对 t96c 复算） ---
    if TRACE_JSON.is_file():
        traces = load_traces()
        specs, skipped = build_registry(traces)
        n_fixed = sum(1 for s in specs if s.kind == "fixed")
        n_var = sum(1 for s in specs if s.kind == "variable")
        n_empty = sum(1 for s in specs if s.kind == "empty")
        ck("registry composition", n_fixed >= 40 and n_var >= 14 and n_empty >= 2,
           f"fixed={n_fixed} variable={n_var} empty={n_empty} skipped={len(skipped)}")
        bad = []
        for t in traces["tables"]:
            tid = t["table_id"]
            if t.get("row_len_min") is None or tid in (45, 48) or t["rows_header"] == 0:
                continue
            if HEADER_END + t["rows_header"] * (1 + t["row_len_min"]) != t["footer_off"]:
                continue
            wsum = sum(r["n"] if isinstance(r["n"], int) else 0 for r in t.get("row0_reads") or [])
            if wsum != t["row_len_min"]:
                bad.append((t["archive"], tid, wsum, t["row_len_min"]))
        ck("row0 reads cover row body", not bad, str(bad[:4]))
    else:
        ck("traces available", False, str(TRACE_JSON))

    # --- 3 真机数据抽验 ---
    if TRACE_JSON.is_file() and (DB_DIR / "server_db.dat").is_file():
        traces = load_traces()
        l3 = load_l3()
        specs, _ = build_registry(traces)
        by_key = {s.key: s for s in specs}
        for key in ("server/8", "server/5", "server/2", "server/47", "client/41"):
            spec = by_key.get(key)
            if spec is None:
                ck(f"live {key}", False, "not in registry")
                continue
            payload = Archive(spec.archive).payload(spec.tid)
            res = TableReader(spec, l3).verify(payload, sample_limit=2)
            ck(f"live {key} closed", res["footer_closed"], str(res["error"]))
        spec = by_key.get("server/45")
        if spec is not None:
            payload = Archive("server").payload(45)
            mv = memoryview(payload)
            reader = TableReader(spec, l3)
            footer_off = len(payload) - FOOTER_SIZE
            pos, ok_rows, err = HEADER_END, 0, None
            for i in range(500):
                try:
                    _values, _touched, end = decode_row(mv, pos + 1, footer_off, spec.prog)
                    if payload[end] != 0:
                        raise WireError("identity terminator != 0")
                    ok_rows += 1
                    pos = end
                except WireError as exc:
                    err = f"row {i}: {exc}"
                    break
            ck("live server/45 500 rows", ok_rows == 500 and err is None, str(err))
    else:
        print("[SKIP] live data checks (scratch/data or traces missing)")

    print(f"--- t112_fm24_reader selftest: {'PASS' if not fails else 'FAIL'} "
          f"({len(fails)} failures) ---")
    return 0 if not fails else 1


# ---------------------------------------------------------------- CLI
def cmd_list() -> int:
    traces = load_traces()
    specs, skipped = build_registry(traces)
    by_key = {(t["archive"], t["table_id"]): t for t in traces["tables"]}
    print(f"{'archive':8s} {'tid':>4s} {'class':36s} {'kind':9s} {'rows':>9s}  note")
    for spec in sorted(specs, key=lambda s: (s.archive, s.tid)):
        nrows = by_key[(spec.archive, spec.tid)]["rows_header"]
        print(f"{spec.archive:8s} {spec.tid:>4d} {spec.klass[:36]:36s} {spec.kind:9s} {nrows:>9d}")
    for s in skipped:
        print(f"{s['archive']:8s} {s['table_id']:>4d} {s['class'][:36]:36s} {'SKIP':9s} "
              f"{'':>9s}  {s['reason']}")
    return 0


def cmd_dump(archive: str, tid: int, limit: int) -> int:
    traces = load_traces()
    l3 = load_l3()
    specs, _ = build_registry(traces)
    spec = next((s for s in specs if s.archive == archive and s.tid == tid), None)
    if spec is None or spec.unsupported_reason:
        print(f"ERROR: {archive}/{tid} not supported"
              + (f" ({spec.unsupported_reason})" if spec else ""), file=sys.stderr)
        return 2
    payload = Archive(archive).payload(tid)
    res = TableReader(spec, l3).verify(payload, sample_limit=limit)
    out = {
        "archive": archive,
        "table_id": tid,
        "class": spec.klass,
        "kind": spec.kind,
        "payload_size": len(payload),
        "verify": {k: res[k] for k in (
            "rows_header", "rows_decoded", "elapsed_ms", "footer_closed",
            "footer9_hex", "l3_named_fields", "error", "flags_seen")},
        "rows": res["sample_rows"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if res["footer_closed"] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="FM24 .dat 纯 Python 只读多表解析库 (t112)")
    ap.add_argument("--list", action="store_true", help="列出所有已支持表及类型")
    ap.add_argument("--dump", nargs=2, metavar=("ARCHIVE", "TABLE_ID"), help="解码样例行(JSON)")
    ap.add_argument("--limit", type=int, default=5, help="--dump 样例行数")
    ap.add_argument("--verify-all", action="store_true", help="全表 100%% 行解码 + footer 闭合校验")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="--verify-all 产物目录")
    ap.add_argument("--selftest", action="store_true", help="内置自检（合成 + 真机抽验）")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.list:
        return cmd_list()
    if args.dump:
        try:
            tid = int(args.dump[1])
        except ValueError:
            ap.error("TABLE_ID 必须是整数")
        return cmd_dump(args.dump[0], tid, max(0, args.limit))
    if args.verify_all:
        verify, results = verify_all(pathlib.Path(args.out))
        s = verify["summary"]
        print(
            f"tables_supported={s['tables_supported']} closed={s['tables_closed']} "
            f"failed={s['tables_failed']} skipped={s['tables_skipped']} "
            f"rows={s['rows_decoded_total']} elapsed={verify['elapsed_total_ms']}ms"
        )
        for r in results:
            if not r["footer_closed"]:
                print(f"  FAIL {r['archive']}/{r['table_id']} {r['class']}: {r['error']}")
        return 0 if not [r for r in results if not r["footer_closed"]] else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
