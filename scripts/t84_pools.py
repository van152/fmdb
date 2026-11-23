#!/usr/bin/env python3
"""t84_pools — 只读解包 name_table_* / name_table_extra_* / lang_update_db 成员。

设计原则
--------
* 复用 `scripts/fm24_dump.py` 的 E80 寻址口径(不改该文件):member start =
  data_base(34) + entry.offset,frame 由 `len == size` 选出。
* 三池(0/1/2)主/extra 各自独立闭合:extra 池 = (u32 idx, u32 len, utf8) 记录流,
  主池 = 12 字节定长索引行;两者行数相等即闭合。
* 不猜码页:字符串按原始 UTF-8 解码,失败即记录 invalid_utf8,不替换。
* 负结果原样保留:未闭合的成员写 `closure: false` 与其首反例,不静默截断。

用法
----
  py -V:3.12 -I -B scripts/t84_pools.py --help
  py -V:3.12 -I -B scripts/t84_pools.py --selftest
  py -V:3.12 -I -B scripts/t84_pools.py --build scratch/t84/out/members_profile.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB_DIR = pathlib.Path(
    os.environ.get("FM24_DB_DIR")
    or r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
)
MAGIC = bytes.fromhex("28b52ffd")
TAD = bytes.fromhex("03017461642ef10d")  # b"\x03\x01tad.\xf1\x0d"

POOL_NAMES = [f"name_table_{n}.dat" for n in range(3)] + [
    f"name_table_extra_{n}.dat" for n in range(3)
]
LANGS = ["6", "7", "8", "10", "11", "12", "15", "16", "17", "18", "19",
         "21", "22", "24", "25", "30", "32", "1000000", "1000001", "1000002",
         "1000003", "1000004"]
LANG_TYPES = ["0", "2", "3", "5", "6", "7", "9", "18", "19", "21", "23", "25",
              "35", "47", "56", "person_names"]


class Fail(Exception):
    pass


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise Fail(msg)


def _codec():
    import runpy
    k = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    return k["_reader"]()


def load_member(codec, archive: str, member: str) -> bytes:
    """E80: member = [data_base+offset, +packed_size); zstd frame with len == size."""
    fn = f"{archive}_db.dat"
    p = DB_DIR / fn
    ents = codec["list_tables"](p, fn)
    hits = [e for e in ents if e["path"].split("/")[-1] == member]
    require(len(hits) == 1, f"{fn}: {member} not unique ({len(hits)})")
    e = hits[0]
    db = p.read_bytes()
    base = int(codec["_archive_layout"](db)["data_base"])
    start = base + int(e["offset"])
    end = start + int(e["packed_size"])
    size = int(e["size"])
    require(0 <= start < end <= len(db), f"{fn}/{member}: member out of archive")
    d = next((d for d in range(min(64, end - start))
              if db[start + d:start + d + 4] == MAGIC), None)
    require(d is not None, f"{fn}/{member}: no zstd frame")
    zstd = codec["_zstd_module"]()
    obj = zstd.ZstdDecompressor().decompressobj()
    out = obj.decompress(db[start + d:end])
    require(len(out) == size,
            f"{fn}/{member}: decompressed {len(out)} != declared {size}")
    return out


def parse_pool(raw: bytes) -> dict:
    """extra 池:(u32 idx, u32 len, utf8) 记录流,idx 连续 0..n-1。"""
    require(raw[:8] == TAD, "pool: bad tad. header")
    cnt = struct.unpack_from("<I", raw, 8)[0]
    pos, recs, invalid = 12, [], []
    while pos + 8 <= len(raw):
        idx, ln = struct.unpack_from("<II", raw, pos)
        require(pos + 8 + ln <= len(raw), f"pool: len {ln} overruns at {pos}")
        seg = raw[pos + 8: pos + 8 + ln]
        try:
            text = seg.decode("utf-8")
        except UnicodeDecodeError:
            invalid.append({"index": idx, "raw_hex": seg.hex()})
            text = None
        recs.append({"index": idx, "len": ln, "text": text, "raw_hex": seg.hex()})
        pos += 8 + ln
    return {
        "count_header": cnt,
        "records": len(recs),
        "end": pos,
        "payload_len": len(raw),
        "footer_len": len(raw) - pos,
        "index_contiguous": [r["index"] for r in recs] == list(range(len(recs))),
        "invalid_utf8": invalid[:20],
        "invalid_utf8_count": len(invalid),
        "recs": recs,
    }


def parse_index(raw: bytes) -> dict:
    """主池:12 字节定长行 = 6 x u16;第 2/3 列合成为记录序号。"""
    require(raw[:8] == TAD, "index: bad tad. header")
    cnt = struct.unpack_from("<I", raw, 8)[0]
    require(len(raw) == 12 + 12 * cnt,
            f"index: {len(raw)} != 12+12*{cnt}")
    rows = [struct.unpack_from("<6H", raw, 12 + 12 * i) for i in range(cnt)]
    keyed = all((r[1] | (r[2] << 16)) == i for i, r in enumerate(rows))
    return {
        "count_header": cnt,
        "rows": len(rows),
        "closure": True,
        "row_width": 12,
        "columns": ["f0", "f1", "f2", "f3", "f4", "f5"],
        "index_equals_f1_f2": keyed,
        "rows_data": rows,
    }


def lang_parse(raw: bytes, nfields: int, trailer: int = 3) -> dict:
    """lang_update 记录:uid u32,然后 nfields x ([0xFF] u32len utf8),尾 3 字节。"""
    require(raw[:8] == TAD, "lang: bad tad. header")
    cnt = struct.unpack_from("<I", raw, 8)[0]
    pos, recs = 12, []
    try:
        for _ in range(cnt):
            require(pos + 4 <= len(raw), "lang: eof at uid")
            uid = struct.unpack_from("<I", raw, pos)[0]
            pos += 4
            flds = []
            for _f in range(nfields):
                if pos < len(raw) and raw[pos] == 0xFF:
                    pos += 1
                require(pos + 4 <= len(raw), "lang: eof at len")
                ln = struct.unpack_from("<I", raw, pos)[0]
                require(ln <= 400 and pos + 4 + ln <= len(raw),
                        f"lang: bad len {ln} @{pos}")
                flds.append(raw[pos + 4: pos + 4 + ln].decode("utf-8"))
                pos += 4 + ln
            require(pos + trailer <= len(raw), "lang: eof at trailer")
            pos += trailer
            recs.append({"uid": uid, "fields": flds})
        ok = pos == len(raw) - 8
    except (Fail, UnicodeDecodeError, struct.error) as exc:
        return {"closure": False, "count_header": cnt, "parsed": len(recs),
                "end": pos, "first_counterexample": str(exc)[:120], "recs": []}
    return {"closure": ok, "count_header": cnt, "parsed": len(recs),
            "end": pos, "footer_start": len(raw) - 8,
            "uid_monotone": [r["uid"] for r in recs] == sorted(r["uid"] for r in recs),
            "recs": recs}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build(out: pathlib.Path) -> int:
    codec = _codec()
    res: dict = {"task": "t84", "db_dir": str(DB_DIR), "members": {}, "lang": {}}
    for archive in ("client", "server"):
        for member in POOL_NAMES:
            raw = load_member(codec, archive, member)
            key = f"{archive}/{member}"
            if "extra" in member:
                p = parse_pool(raw)
                samples = [{"index": r["index"], "text": r["text"]}
                           for r in p["recs"][:8]]
                p.pop("recs")
                res["members"][key] = {
                    "kind": "string_pool", "payload_len": len(raw),
                    "payload_sha256": sha(raw), **p, "samples": samples,
                }
            else:
                ix = parse_index(raw)
                rows = ix.pop("rows_data")
                # 索引行本身不带字符串;取同池 extra 的前 8 条做索引→字符串对照
                pl = parse_pool(load_member(
                    codec, archive, member.replace("name_table_", "name_table_extra_")))
                res["members"][key] = {
                    "kind": "index_rows", "payload_len": len(raw),
                    "payload_sha256": sha(raw), **ix,
                    "pairs_with_extra_pool": [
                        {"index": i, "columns": list(rows[i]),
                         "text": pl["recs"][i]["text"]} for i in range(min(8, len(rows)))
                    ],
                }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    return 0


def selftest() -> int:
    codec = _codec()
    ok = fail = 0
    for archive in ("client", "server"):
        for n in range(3):
            try:
                ix = parse_index(load_member(codec, archive, f"name_table_{n}.dat"))
                pl = parse_pool(load_member(codec, archive, f"name_table_extra_{n}.dat"))
                good = (ix["rows"] == pl["records"] and pl["index_contiguous"]
                        and pl["footer_len"] == 0 and ix["index_equals_f1_f2"])
                print(("PASS" if good else "FAIL"),
                      f"{archive} pool{n} rows={ix['rows']} strings={pl['records']}")
                ok += 1 if good else 0
                fail += 0 if good else 1
            except Fail as exc:
                print("FAIL", archive, n, exc)
                fail += 1
    print(f"--- {ok} PASS / {fail} FAIL ---")
    return 0 if fail == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t84 name pool unpacker (read-only)")
    ap.add_argument("--build", metavar="OUT.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.build:
        return build(pathlib.Path(a.build))
    ap.error("need --build OUT.json or --selftest")


if __name__ == "__main__":
    sys.exit(main())
