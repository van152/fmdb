#!/usr/bin/env python3
"""t85_common — 共享层:只读装载 + E80 成员寻址 + 行框/指纹口径。

只用只读输入:
  scratch/t75/out/xref_reverse.json    (E114 99 槽裁决)
  scratch/t72/out/{inventory,fingerprints}.json (E112 槽位指纹)
  scratch/t78/out/buckets.json         (E116 分母)
  scratch/t50/out/profiles/*.rows.jsonl (t9/extra_9 行记录)
  evidence/fm24/reports/editor_schema/master.json (冻结 schema)

成员寻址沿用 E80:member start = data_base(34) + entry.offset;按 entry.size 选帧,
不回落首帧。本模块不 import t75/t72 builder,也不写任何 reports/。
"""
from __future__ import annotations

import json
import os
import pathlib
import runpy
import struct

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
MAGIC = bytes.fromhex("28b52ffd")
IDENT = 13
_CODEC = None


def codec():
    """旧仓只读 codec(目录/Zstd),与 t01k verify 同源。"""
    global _CODEC
    if _CODEC is None:
        k = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
        _CODEC = runpy.run_path(str(k["OLD_READER_PATH"]))
    return _CODEC


def entries(archive: str):
    c = codec()
    fn = f"{archive}_db.dat"
    p = DB / fn
    return c["list_tables"](p, fn), int(c["_archive_layout"](p.read_bytes())["data_base"])


def payload(archive: str, path: str, size: int) -> bytes:
    """E80: member start = data_base + entry.offset; 只取解压长度 == size 的帧。"""
    c = codec()
    fn = f"{archive}_db.dat"
    p = DB / fn
    db = p.read_bytes()
    e = next(x for x in c["list_tables"](p, fn) if x["path"] == path)
    base = int(c["_archive_layout"](db)["data_base"])
    s = base + int(e["offset"])
    end = s + int(e["packed_size"])
    if not (0 <= s < end <= len(db)):
        raise RuntimeError(f"{fn} {path}: member [{s},{end}) outside archive")
    z = c["_zstd_module"]()
    d = z.ZstdDecompressor()
    pos = s
    while pos + 4 <= end and db[pos:pos + 4] == MAGIC:
        obj = d.decompressobj()
        out = obj.decompress(db[pos:end])
        if len(out) == size:
            return out
        used = (end - pos) - len(obj.unused_data)
        if not obj.eof or used <= 0:
            break
        pos += used
    raise RuntimeError(f"{fn} {path}: no frame with decompressed length {size}")


def jload(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def jdump(rel: str, obj) -> pathlib.Path:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


def identity_offsets(raw: bytes, limit: int | None = None) -> list[int]:
    """13B identity trailer 游标: [ordinal u32][uid u32][uid u32][0] 且 uid 对相等。"""
    out: list[int] = []
    n = 0
    stop = len(raw) - IDENT
    for i in range(0, stop + 1):
        a, b, c = struct.unpack_from("<III", raw, i)
        if b == c and raw[i + 12] == 0 and a == n:
            out.append(i)
            n += 1
            if limit is not None and n >= limit:
                break
    return out


def rows_jsonl(name: str) -> list[dict]:
    p = ROOT / "scratch/t50/out/profiles" / f"{name}.rows.jsonl"
    with p.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
