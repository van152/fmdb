#!/usr/bin/env python3
"""t15b — 未覆盖档案只读清点(容器层 + 表清单 + 基数对照),不解析字段。

用法:
  py -V:3.12 -I -B scratch/t15b/probe.py --help
  py -V:3.12 -I -B scratch/t15b/probe.py --selftest
  py -V:3.12 -I -B scratch/t15b/probe.py --out scratch/t15b/out/probe.json

只读 FM24_DB_DIR 下的 .dat;唯一写入是 --out 指定的 JSON。
退出码:0 成功 / 1 校验未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import pathlib
import runpy
import struct
import sys
import collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or r"scratch/data")
if not DB_DIR.is_absolute():
    DB_DIR = ROOT / DB_DIR
MAGIC = bytes.fromhex("28b52ffd")
FMF = bytes.fromhex("0201666d662e080000")
SEP = b"\xff\xff\xff\xff\x03"

FILES = [
    "people_db.dat",
    "pl_hist_dt.dat", "pl_hist_id.dat", "pl_hist_index.dat",
    "non_pl_hist_dt.dat", "non_pl_hist_id.dat", "non_pl_hist_index.dat",
    "summary.dat", "lang_update_db.dat",
]
# 已知基数(来自 scratch/t13e/out/baselines.json)
BASELINE = {
    "basic_people_db_rows": 658011,
    "basic_people_class_counts": {1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193},
    "t49_server_rows": 792149,
    "club_rows": 84259,
    "person_duni_head_range": [2002040996, 2002042188],
}


def _zstd():
    v = pathlib.Path(r"D:\tmp2b\fm24\tools\python")
    if str(v) not in sys.path:
        sys.path.insert(0, str(v))
    import zstandard
    return zstandard


def classify(head: bytes, size: int) -> dict:
    tag = head[2:6].decode("ascii", "replace") if len(head) >= 6 else ""
    ver = struct.unpack_from("<H", head, 6)[0] if len(head) >= 8 else None
    out = {
        "tag": tag, "version_u16": ver,
        "zstd_at_8": head[8:12] == MAGIC,
        "fmf_at_8": len(head) >= 17 and head[8:17] == FMF,
    }
    if out["fmf_at_8"]:
        out["kind"] = "tad. + embedded fmf. directory (listable)"
    elif tag == "tadc" and out["zstd_at_8"]:
        out["kind"] = "tadc + concatenated zstd frames"
    elif tag == "tad." and out["zstd_at_8"]:
        out["kind"] = "tad. + single zstd stream at 8"
    elif tag == "tad." and ver == 1 and (size - 8) % 4 == 0:
        out["kind"] = "tad. v1 raw u32 array (no zstd)"
    elif tag == "tad.":
        out["kind"] = "tad. own grammar (no zstd, no fmf)"
    else:
        out["kind"] = "unclassified"
    return out


def stream_decompress(buf: bytes, limit: int = 512 * 1024 * 1024) -> bytes:
    zstd = _zstd()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(buf), read_across_frames=True) as r:
        out = r.read(limit + 1)
    if len(out) > limit:
        raise RuntimeError(f"decompressed > limit {limit}")
    return out


def frame_census(buf: bytes) -> dict:
    """扫描串联 zstd 帧:首尾帧头参数 + 命中计数。"""
    zstd = _zstd()
    offs, p = [], buf.find(MAGIC)
    while p != -1 and len(offs) < 200000:
        offs.append(p)
        p = buf.find(MAGIC, p + 1)
    ok_head = bad_head = 0
    sizes = collections.Counter()
    for o in offs[:200]:
        try:
            pr = zstd.get_frame_parameters(buf[o:o + 18])
            ok_head += 1
            sizes[pr.content_size] += 1
        except Exception:
            bad_head += 1
    tail = []
    for o in offs[-3:]:
        try:
            pr = zstd.get_frame_parameters(buf[o:o + 18])
            tail.append({"off": o, "content_size": pr.content_size, "nbytes": len(buf) - o})
        except Exception:
            tail.append({"off": o, "parse": "fail"})
    return {"magic_hits": len(offs), "first_offsets": offs[:4],
            "head_frames_parsed": ok_head, "head_frames_bad": bad_head,
            "head_content_sizes": {str(k): v for k, v in sizes.items()},
            "tail_frames": tail}


def token_census(buf: bytes, windows: int = 8, win: int = 65536) -> dict:
    """在等距窗口内统计可打印 ASCII 4 字节 token(找 4CC 表名/前缀)。"""
    n = len(buf)
    if n == 0:
        return {"windows": 0}
    step = max(1, n // windows)
    cnt: collections.Counter = collections.Counter()
    allowed = set(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    for i in range(windows):
        s = min(i * step, max(0, n - win))
        blob = buf[s:s + win]
        for j in range(0, len(blob) - 4):
            t = blob[j:j + 4]
            if all(c in allowed for c in t):
                cnt[t] += 1
    return {"windows": windows, "win": win, "top": [[t.decode(), c] for t, c in cnt.most_common(12)]}


def anchor_counts(buf: bytes) -> dict:
    return {
        "ffffffff_00_markers": buf.count(b"\xff\xff\xff\xff\x00"),
        "ffffffff_markers": buf.count(b"\xff\xff\xff\xff"),
        "len": len(buf),
    }


def chain_sample(buf: bytes, stride: int, next_off: int, n: int = 3000) -> dict:
    """抽样校验 next 指针链:中间行 next==off+stride,末行 0xffffffff。"""
    total = len(buf) // stride
    idxs = list(range(min(n, total))) + list(range(max(0, total - n), total))
    ok = bad = term = 0
    bad_ex = []
    for i in sorted(set(idxs)):
        o = i * stride
        if o + stride > len(buf):
            break
        nxt = struct.unpack_from("<I", buf, o + next_off)[0]
        if nxt == 0xFFFFFFFF:
            term += 1
            continue
        if nxt == o + stride:
            ok += 1
        else:
            bad += 1
            if len(bad_ex) < 3:
                bad_ex.append({"row": i, "next": nxt, "expect": o + stride})
    return {"rows_total": total, "checked": ok + bad + term, "chain_ok": ok,
            "chain_bad": bad, "terminal": term, "bad_examples": bad_ex}


def u32_array(buf: bytes, base: int = 8) -> dict:
    n = (len(buf) - base) // 4
    k = min(n, 400)
    head = list(struct.unpack_from(f"<{k}I", buf, base)) if k else []
    vals = head[:8]
    last = list(struct.unpack_from(f"<{min(n,8)}I", buf, base + 4 * (n - min(n, 8)))) if n >= 8 else []
    pairs = [(head[i], head[i + 1]) for i in range(0, k - 1, 2)]
    gaps = {p[0] - p[1] for p in pairs[1:]} if len(pairs) > 1 else set()
    al24 = sum(1 for p in pairs if p[0] % 24 == 0 and p[1] % 24 == 0)
    inc = all(pairs[i + 1][0] > pairs[i][0] for i in range(len(pairs) - 1)) if len(pairs) > 1 else None
    return {"count_u32": n, "pairs_if_std": n // 2, "first_8": vals,
            "last_8": last, "sample_pair_gap_set": sorted(gaps)[:6],
            "sample_pairs_24_aligned": f"{al24}/{len(pairs)}",
            "sample_start_strictly_increasing": inc}


def index_payload(buf: bytes) -> dict:
    count = struct.unpack_from("<I", buf, 0)[0]
    expect = 4 + count * 8
    ids, ords, asc = [], [], True
    prev = None
    for i in range(min(count, 5000)):
        a, b = struct.unpack_from("<II", buf, 4 + i * 8)
        ids.append(a)
        ords.append(b)
        if prev is not None and a < prev:
            asc = False
        prev = a
    sent = ords.count(0xFFFFFFFF)
    return {"count": count, "payload_len": len(buf), "expected_len": expect,
            "len_matches": len(buf) == expect, "ids_sorted_head": asc,
            "first_ids": ids[:6], "ordinals_sentinel_in_head": sent}


def summary_probe(buf: bytes) -> dict:
    hits = buf.count(SEP)
    pos, lens = [], collections.Counter()
    start = buf.find(SEP)
    while start != -1 and len(pos) < 60000:
        nxt = buf.find(SEP, start + 5)
        lens[(nxt if nxt != -1 else len(buf)) - (start + 5)] += 1
        pos.append(start)
        start = nxt
    block1 = list(struct.unpack_from("<8I", buf, 8)) if len(buf) >= 40 else []
    block2 = list(struct.unpack_from("<5I", buf, 40)) if len(buf) >= 60 else []
    return {"separators": hits, "bodies": max(0, hits - 1), "body_len_top": lens.most_common(4),
            "block1_u32_at_8": block1, "block2_u32_at_40": block2,
            "first_sep_offset": pos[0] if pos else None,
            "byte_accounting": {"file": len(buf), "head_before_first_sep": pos[0] if pos else None}}


def main() -> int:
    ap = argparse.ArgumentParser(description="t15b 未覆盖档案清点(只读)")
    ap.add_argument("--out", default=str(ROOT / "scratch/t15b/out/probe.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        h = bytes.fromhex("03017461642ef10d") + FMF
        assert classify(h, 100)["kind"].startswith("tad. + embedded")
        h2 = bytes.fromhex("0301746164630300") + MAGIC
        assert classify(h2, 100)["kind"].startswith("tadc")
        h3 = bytes.fromhex("03017461642e0100")
        assert classify(h3, 16)["kind"].startswith("tad. v1")
        b = SEP + b"abcd" + SEP + b"ef" + SEP
        assert summary_probe(b)["separators"] == 3
        assert frame_census(MAGIC + b"\x00" * 10)["magic_hits"] == 1
        print("selftest OK")
        return 0

    codec = None
    try:
        k = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
        codec = runpy.run_path(str(k["OLD_READER_PATH"]))
    except Exception as ex:  # noqa: BLE001
        print(f"codec load failed: {ex}", file=sys.stderr)

    res = {"task": "t15b", "generated": "2026-11-18", "db_dir": str(DB_DIR),
           "baseline_ref": "scratch/t13e/out/baselines.json", "files": {}}

    for fn in FILES:
        p = DB_DIR / fn
        if not p.is_file():
            res["files"][fn] = {"status": "missing"}
            continue
        data = p.read_bytes()
        head = data[:64]
        rec = {"path": str(p), "size": len(data),
               "sha256": hashlib.sha256(data).hexdigest(),
               "header_hex_64": head.hex(), "container": classify(head, len(data)),
               "container_ok": False}
        cont = rec["container"]
        try:
            if cont["fmf_at_8"] and codec:
                ents = codec["list_tables"](p, fn)
                tabs = [e for e in ents if e.get("entry_type") == "table"]
                rec["container_ok"] = True
                rec["tables"] = {
                    "entries": len(ents), "table_entries": len(tabs),
                    "aux_entries": len(ents) - len(tabs),
                    "table_ids": sorted({e["table_id"] for e in tabs})[:80],
                    "sample": [{"id": e.get("table_id"), "path": e["path"],
                                "packed": e["packed_size"], "size": e["size"],
                                "count": e.get("record_count_header"),
                                "magic": e.get("payload_magic")} for e in ents[:6]],
                }
            elif cont["kind"].startswith("tad.") and cont["zstd_at_8"]:
                raw = stream_decompress(data[8:])
                rec["container_ok"] = True
                rec["decompressed"] = {"len": len(raw),
                                       "sha256": hashlib.sha256(raw).hexdigest()}
                rec["anchors"] = anchor_counts(raw)
                rec["tokens"] = token_census(raw)
                u32s = [struct.unpack_from("<I", raw, i)[0] for i in range(0, min(512, len(raw) - 4), 4)]
                rec["head_u32_128"] = u32s
                rec["contains_658011_u32_le"] = 658011 in u32s
                rec["contains_1193_u32_le"] = 1193 in u32s
            elif cont["kind"].startswith("tadc"):
                fc = frame_census(data[8:])
                raw = stream_decompress(data[8:])
                rec["container_ok"] = True
                rec["frames"] = fc
                rec["decompressed"] = {"len": len(raw),
                                       "sha256": hashlib.sha256(raw).hexdigest()}
                stride = 44 if fn.startswith("pl_") else 24
                rec["chain"] = chain_sample(raw, stride, stride - 4)
                rec["chain"]["stride"] = stride
            elif cont["kind"].startswith("tad. v1"):
                rec["container_ok"] = True
                rec["array"] = u32_array(data)
            elif cont["kind"].startswith("tad. own grammar"):
                rec["container_ok"] = True
                rec["summary"] = summary_probe(data)
        except Exception as ex:  # noqa: BLE001
            rec["error"] = f"{type(ex).__name__}: {ex}"
        res["files"][fn] = rec

    # index 档案单独解压计数
    for fn in ("pl_hist_index.dat", "non_pl_hist_index.dat"):
        rec = res["files"].get(fn) or {}
        try:
            raw = stream_decompress((DB_DIR / fn).read_bytes()[8:])
            rec["container_ok"] = True
            rec["decompressed"] = {"len": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
            rec["index"] = index_payload(raw)
            rec.pop("error", None)
        except Exception as ex:  # noqa: BLE001
            rec["error"] = f"{type(ex).__name__}: {ex}"
        res["files"][fn] = rec

    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {a.out}")
    for fn, r in res["files"].items():
        bits = [f"ok={r.get('container_ok')}"]
        if "decompressed" in r:
            bits.append(f"raw={r['decompressed']['len']}")
        if "tables" in r:
            bits.append(f"tables={r['tables']['table_entries']}")
        if "index" in r:
            bits.append(f"count={r['index']['count']}")
        if "array" in r:
            bits.append(f"u32={r['array']['count_u32']}")
        if "chain" in r:
            bits.append(f"rows={r['chain']['rows_total']} bad={r['chain']['chain_bad']}")
        if "summary" in r:
            bits.append(f"bodies={r['summary']['bodies']}")
        if "error" in r:
            bits.append("ERR " + r["error"][:60])
        print(f"  {fn:24s} " + " ".join(bits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
