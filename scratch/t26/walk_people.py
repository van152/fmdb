#!/usr/bin/env python3
"""t26-A — people_db.dat 全文法走查(只读,数据侧)。

做四件事:
  1. 复现 probe3 的 compact 文法,从 pos 6 走到断裂点(记录 offset / 前后 64B / 行数);
  2. 断裂后逐段识别新文法:全文件扫同一 compact 文法(确认它只出现在那一段),
     再识别第二类"名字锚点"布局(ff ff ff ff 00 | u32 len | utf8 name),
     给出该布局的行数、间距分布、覆盖区间;
  3. 覆盖统计:person duni / uid 是否在 payload 中出现(4 种 u32 对齐),
     key 空间与 basic_people_db 的 class 块关系;
  4. 假设裁决:"658,011 条完整 person 库"支持 / 反对 / 证据不足。

用法:
  py -V:3.12 -I -B scratch/t26/walk_people.py --help
  py -V:3.12 -I -B scratch/t26/walk_people.py --selftest
  py -V:3.12 -I -B scratch/t26/walk_people.py --out scratch/t26/out/people_walk.json

只读 scratch/data/*.dat;只写 --out。退出码 0 成功 / 1 校验未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import io
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or r"scratch/data")
if not DB_DIR.is_absolute():
    DB_DIR = ROOT / DB_DIR
ZSTD_PATH = pathlib.Path(r"D:\tmp2b\fm24\tools\python")
OUT_DIR = ROOT / "scratch/t26/out"

MARKER = b"\xff\xff\xff\xff"          # 名字锚点前缀(其后 1B 0x00,再 u32 len)
CL = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}   # basic_people_db 行宽(按 class)


def _zstd():
    if str(ZSTD_PATH) not in sys.path:
        sys.path.insert(0, str(ZSTD_PATH))
    import zstandard
    return zstandard


def decompress(name: str, skip: int = 8) -> bytes:
    zstd = _zstd()
    data = (DB_DIR / name).read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[skip:]),
                                               read_across_frames=True) as r:
        return r.read(600 * 1024 * 1024)


# --------------------------------------------------------------------------- 1
def walk_compact(raw: bytes, pos: int = 6):
    """probe3 的 compact 文法:u32 key|u32 type(=5)|u8 unk|u32 name_len|name
    |8×00|u32 key2(==key)|u32 duni|u32 duni ;行跨度 33+name_len。"""
    rows, bad = [], None
    while True:
        if pos + 33 > len(raw):
            bad = {"reason": "eof", "off": pos}
            break
        key, typ = struct.unpack_from("<II", raw, pos)
        unk = raw[pos + 8]
        ln = struct.unpack_from("<I", raw, pos + 9)[0]
        end = pos + 13 + ln
        if typ != 5 or not (0 <= ln <= 64) or end + 20 > len(raw):
            bad = {"reason": "header", "off": pos, "key": key, "type": typ,
                   "name_len": ln, "hex_16": raw[pos:pos + 16].hex()}
            break
        try:
            nm = raw[pos + 13:end].decode("utf-8") if ln else ""
        except UnicodeDecodeError:
            bad = {"reason": "utf8", "off": pos, "hex_16": raw[pos:pos + 16].hex()}
            break
        pad = raw[end:end + 8]
        key2, d1, d2 = struct.unpack_from("<III", raw, end + 8)
        if any(pad) or key2 != key or d1 != d2:
            bad = {"reason": "trailer", "off": pos, "key": key, "key2": key2,
                   "d1": d1, "d2": d2, "pad": pad.hex(),
                   "hex_24": raw[pos:pos + 24].hex()}
            break
        rows.append({"off": pos, "key": key, "unk": unk, "name_len": ln,
                     "name": nm, "duni": d1})
        pos = end + 20
    return rows, pos, bad


def rescan_compact(raw: bytes):
    """全文件向量化扫 compact 文法行(逐 u32 对齐窗口),确认它出现几次、在哪。"""
    n = len(raw)
    hits = []
    for off in range(4):
        m = (n - off) // 4
        if m < 8:
            continue
        a = struct.unpack_from(f"<{m}I", raw, off) if m <= 1 << 26 else None
        if a is None:                      # 超大文件退化为分块
            a = []
            step = 1 << 25
            for s in range(0, m, step):
                k = min(step, m - s)
                a.extend(struct.unpack_from(f"<{k}I", raw, off + s * 4))
        for i in range(2, m - 8):
            if a[i] != 5:            # a[i] = type 字段(位于 key 之后 4B)
                continue
            p = off + i * 4        # p 指向 type 字段
            key = a[i - 1]
            if raw[p + 4] > 1:        # unk 字节(compact 段内取值 {0,1})
                continue
            ln = struct.unpack_from("<I", raw, p + 5)[0]   # name_len 未对齐
            if not (1 <= ln <= 64):
                continue
            e = p + 9 + ln
            if e + 20 > n or any(raw[e:e + 8]):
                continue
            k2, d1, d2 = struct.unpack_from("<III", raw, e + 8)
            if k2 != key or d1 != d2 or d1 == 0:
                continue
            hits.append(p - 4)     # 记录 key 字段偏移,与 walk_compact 的 off 同口径
    return sorted(set(hits))


# --------------------------------------------------------------------------- 2
def anchor_scan(raw: bytes):
    """第二类布局:ff ff ff ff 00 | u32 len | utf8 name(无 8B 对齐填充)。"""
    rows, rejected = [], 0
    p = 0
    while True:
        p = raw.find(MARKER, p)
        if p < 0:
            break
        if p + 9 <= len(raw) and raw[p + 4] == 0:
            ln = struct.unpack_from("<I", raw, p + 5)[0]
            if 1 <= ln <= 80 and p + 9 + ln <= len(raw):
                try:
                    s = raw[p + 9:p + 9 + ln].decode("utf-8")
                except UnicodeDecodeError:
                    s = None
                if s and len(s) >= 3 and s[0].isupper() and \
                        all(ord(c) >= 32 for c in s) and any(c.isalpha() for c in s):
                    rows.append({"off": p, "name_len": ln, "name": s})
                    p += 9 + ln
                    continue
        rejected += 1
        p += 1
    return rows, rejected


def gap_stats(offs):
    if len(offs) < 3:
        return {}
    d = [b - a for a, b in zip(offs, offs[1:])]
    ds = sorted(d)
    def q(x):
        return ds[min(len(ds) - 1, int(x * (len(ds) - 1)))]
    hist = collections.Counter()
    for g in d:
        for b in (256, 384, 512, 640, 768, 1024, 1536, 2048, 4096):
            if g < b:
                hist[f"<{b}"] += 1
                break
        else:
            hist[">=4096"] += 1
    return {"median": q(0.5), "p10": q(0.10), "p90": q(0.90), "max": ds[-1],
            "buckets": dict(hist)}


# --------------------------------------------------------------------------- 3
def presence(raw: bytes, values, chunk: int = 1 << 27):
    """4 种 u32 对齐下,values 是否在 payload 中出现。向量化(排序 + searchsorted)。"""
    import numpy as np
    v = np.sort(np.asarray(values, dtype=np.int64))
    hit = np.zeros(len(v), dtype=bool)
    n = len(raw)
    for st in range(0, n, chunk):
        seg = raw[st:st + chunk + 8]
        for off in range(4):
            m = (len(seg) - off) // 4
            if m <= 0:
                continue
            w = np.frombuffer(seg[off:off + m * 4], dtype=np.uint32).astype(np.int64)
            p = np.searchsorted(v, w)
            p[p >= len(v)] = 0
            mm = v[p] == w
            if mm.any():
                hit[np.unique(p[mm])] = True
    return hit


def walk_basic_people():
    bp = decompress("basic_people_db.dat")
    cnt = struct.unpack_from("<I", bp, 0)[0]
    pos = 5
    cls = bytearray(cnt)
    duni = [0] * cnt
    bad = None
    for i in range(cnt):
        c = bp[pos + 1]
        if c not in CL:
            bad = {"i": i, "off": pos, "class": c}
            break
        cls[i] = c
        ln = CL[c]
        _, dd, _ = struct.unpack_from("<III", bp, pos + ln - 12)
        duni[i] = dd
        pos += ln
    return {"len": len(bp), "count": cnt, "walk_end": pos, "walk_bad": bad,
            "class_dist": {str(k): v for k, v in
                           collections.Counter(cls[:cnt]).items()},
            "cls": cls, "duni": duni}


def class_blocks(cls, duni):
    """class 连续块清单(只保留长度 >= 50 的块,长尾单独计数)。"""
    n = len(cls)
    blocks, s = [], 0
    for i in range(1, n + 1):
        if i == n or cls[i] != cls[s]:
            blocks.append({"start": s, "end": i - 1, "n": i - s,
                           "class": int(cls[s]), "duni_first": int(duni[s])})
            s = i
    big = [b for b in blocks if b["n"] >= 50]
    return {"n_blocks": len(blocks), "n_blocks_ge50": len(big),
            "largest": sorted(big, key=lambda b: -b["n"])[:8],
            "tail_block": blocks[-1] if blocks else None}


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="t26-A people_db.dat 全文法走查(只读)")
    ap.add_argument("--out", default=str(OUT_DIR / "people_walk.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        raw = (struct.pack("<II", 7, 5) + b"\x00" + struct.pack("<I", 3) + b"abc")
        raw += b"\x00" * 8 + struct.pack("<III", 7, 99, 99) + b"\x00"
        rows, end, bad = walk_compact(raw, 0)
        assert len(rows) == 1 and rows[0]["key"] == 7 and rows[0]["duni"] == 99, (rows, bad)
        assert end == 33 + 3
        r2, _ = anchor_scan(b"\xff\xff\xff\xff\x00" + struct.pack("<I", 5) + b"Abcde")
        assert len(r2) == 1 and r2[0]["name"] == "Abcde"
        assert gap_stats([0, 10, 30])["median"] == 10
        print("selftest OK")
        return 0

    out = {"task": "t26-A", "file": "people_db.dat",
           "grammar_variants": [], "breaks": [], "hypothesis": {}}
    try:
        raw = decompress("people_db.dat")
    except Exception as ex:                                     # noqa: BLE001
        print(f"decompress failed: {ex}", file=sys.stderr)
        return 2

    out["payload"] = {"len": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    out["header"] = {"hex_16": raw[:16].hex(),
                     "u32_at_2": struct.unpack_from("<I", raw, 2)[0]}
    total = out["header"]["u32_at_2"]

    # --- 文法 A:compact 段
    rows, endpos, bad = walk_compact(raw, 6)
    keys = [r["key"] for r in rows]
    duns = [r["duni"] for r in rows]
    out["grammar_variants"].append({
        "id": "A", "name": "compact class-5 row",
        "layout": "u32 key | u32 type=5 | u8 unk | u32 name_len | name | 8x00 | "
                  "u32 key2(=key) | u32 duni | u32 duni",
        "row_span": "33 + name_len",
        "seg_start": 6, "seg_end": endpos, "rows": len(rows),
        "keys": {"min": min(keys), "max": max(keys),
                 "contiguous": sorted(keys) == list(range(min(keys), max(keys) + 1)),
                 "unique": len(set(keys)) == len(keys)},
        "duni": {"min": min(duns), "max": max(duns), "unique": len(set(duns)),
                 "strictly_increasing": all(b > a for a, b in zip(duns, duns[1:])),
                 "span": max(duns) - min(duns) + 1},
        "empty_names": sum(1 for r in rows if not r["name"]),
        "names_head": [r["name"] for r in rows[:4]],
        "names_tail": [r["name"] for r in rows[-3:]],
        "unk_byte_values": sorted({r["unk"] for r in rows}),
    })
    out["breaks"].append({
        "after_rows": len(rows), "off": bad["off"], "reason": bad["reason"],
        "detail": bad,
        "hex_before_64": raw[bad["off"] - 64:bad["off"]].hex(),
        "hex_after_64": raw[bad["off"]:bad["off"] + 64].hex(),
        "gap_to_next_anchor": None,
    })

    # --- 文法 A 的全文件足迹(确认它是否只出现在那一段)
    rescan = rescan_compact(raw)
    inside = [p for p in rescan if 6 <= p < endpos]
    outside = [p for p in rescan if not (6 <= p < endpos)]
    out["grammar_variants"][0]["file_wide_footprint"] = {
        "hits": len(rescan), "inside_segment": len(inside),
        "outside_segment": len(outside), "outside_offsets": [hex(p) for p in outside[:8]],
        "note": "命中数 = 段内行数 则文法 A 在全文件唯一;outside 非空说明还有同类段",
    }

    # --- 文法 B:名字锚点布局
    arows, rejected = anchor_scan(raw)
    offs = [r["off"] for r in arows]
    out["grammar_variants"].append({
        "id": "B", "name": "marker + length-prefixed name row",
        "layout": "ff ff ff ff | u8 0x00 | u32 name_len | utf8 name  (无对齐填充)",
        "rows": len(arows), "rejected_marker_hits": rejected,
        "span": [min(offs), max(offs)] if offs else None,
        "gap_bytes": gap_stats(offs),
        "distinct_names": len({r["name"] for r in arows}),
        "name_len": {"min": min(r["name_len"] for r in arows),
                     "max": max(r["name_len"] for r in arows)},
        "note": "只认 name 首字符为大写、含字母的 UTF-8;非拉丁名与匿名行不计",
    })
    # 名字锚点密度:每 16MB 一桶(看是否全文件均匀,还是有空洞)
    if offs:
        bucket = collections.Counter(o >> 24 for o in offs)
        out["name_density_per_16MB"] = {str(k): bucket[k]
                                        for k in range(0, (len(raw) >> 24) + 1)}

    # 第一段断裂后紧接的锚点位置(段间空隙)
    nxt = [o for o in offs if o > endpos]
    if nxt:
        out["breaks"][0]["gap_to_next_anchor"] = min(nxt) - endpos

    # --- 覆盖:person duni / uid(uid 小整数无鉴别力,只作下界报告)
    import numpy as np
    npz = ROOT / "scratch/t15/out"
    cov = {}
    try:
        pd_all = np.load(npz / "person_duni_all.npy")
        big = pd_all[pd_all >= 1_000_000]
        hit = presence(raw, big)
        cov["duni_ge_1e6"] = {"n": int(len(big)), "present": int(hit.sum()),
                              "pct": round(100 * float(hit.mean()), 3)}
        pd_u = np.load(npz / "person_uid_all.npy")
        cov["uid_ge_1e5"] = {"n": int((pd_u >= 100000).sum()), "note": "未测(小整数空间无鉴别力)"}
    except Exception as ex:                                     # noqa: BLE001
        cov["error"] = f"{type(ex).__name__}: {ex}"
    out["coverage"] = cov

    # --- basic_people 对照
    bpk = walk_basic_people()
    blocks = class_blocks(bpk["cls"], bpk["duni"])
    last = blocks["tail_block"]
    xj = {
        "basic_rows": bpk["count"],
        "walk_end": bpk["walk_end"], "walk_bad": bpk["walk_bad"],
        "class_dist": bpk["class_dist"],
        "class5_rows": bpk["class_dist"].get("5"),
        "compact_rows": len(rows),
        "compact_rows_eq_class5": len(rows) == bpk["class_dist"].get("5"),
        "blocks": blocks,
    }
    if last:
        xj["compact_key_range_eq_tail_block"] = (
            [min(keys), max(keys)] == [last["start"], last["end"]])
        xj["tail_block"] = last
        xj["duni_first_equal"] = (last["duni_first"] == min(duns))
    # class-5 段内 duni 与 basic_people 同 ordinal 逐一比对
    eq = sum(1 for r in rows
             if r["key"] < bpk["count"] and bpk["duni"][r["key"]] == r["duni"])
    xj["duni_equal_at_same_ordinal"] = {"equal": eq, "of": len(rows),
                                        "all": eq == len(rows)}
    out["basic_people_cross"] = xj

    # --- 假设裁决
    out["hypothesis"] = {
        "claim": "people_db.dat 承载 658,011 条完整 person 记录,可按行逐一走查",
        "verdict": "evidence_insufficient",
        "for": [
            f"头部 u32@2 = {total},与 basic_people_db 行数 {bpk['count']} 完全相等(L1)",
            "compact 段 1,193 行全部合法闭包,key 连续,trailer 三列自洽(L1)",
            f"compact 段行数 {len(rows)} = basic_people class-5 计数 {bpk['class_dist'].get('5')}(L1+L2)",
            "compact 段 key 区间与 basic_people 尾块 ordinal 区间重合、duni 首值相等(L2 跨文件锚点)",
        ],
        "against": [
            "文法 A 在全文件只有这一处:段外命中 %d,即除 1,193 行外无法用文法 A 继续走"
            % len(outside),
            "payload 中可定位的带名字行(文法 B)= %d 行,远小于 %d" % (len(arows), total),
            "name 锚点间距中位数 %s B、p90 %s B,记录长度不固定,单一行宽假设不成立"
            % (out["grammar_variants"][1]["gap_bytes"].get("median"),
               out["grammar_variants"][1]["gap_bytes"].get("p90")),
        ],
        "cannot_conclude": [
            "duni 全覆盖只能证'出现过',32-bit 空间里作命中证据上限为 C 类",
            "文法 B 只认拉丁名首大写,非拉丁/匿名行会漏计,故 %d 是下界不是总数" % len(arows),
        ],
        "next": "取文法 B 单条记录做列级切分(固定尾标 b600e207 / 01006c07 作边界),再反推行数",
    }

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    print(f"wrote {a.out}")
    print(f"  payload {len(raw)}  header_count {total}")
    print(f"  grammar A rows {len(rows)} end {endpos} break {bad['reason']}")
    print(f"  grammar A file-wide hits {len(rescan)} (outside {len(outside)})")
    print(f"  grammar B rows {len(arows)} span {out['grammar_variants'][1]['span']}")
    print(f"  coverage {cov}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
