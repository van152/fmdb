#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""t01-a2: fm.exe 4CC 注册块/比较式机械扫描。

纯标准库、只读输入。扫描 fm.exe(可选同时扫 editor.exe 做对照),
产出 fm_sweep.json 需要的全部字段:anchor_check / density_top20 /
clusters / entity_match / editor_compare。

用法:
  py -V:3.12 -I scripts/t01a2_fm_sweep.py --help
  py -V:3.12 -I scripts/t01a2_fm_sweep.py             # 全量扫描 + 写 fm_sweep.json
  py -V:3.12 -I scripts/t01a2_fm_sweep.py --no-editor # 只扫 fm.exe(跳过 editor 对照)
  py -V:3.12 -I scripts/t01a2_fm_sweep.py --selftest  # 形态/聚类/校验逻辑自检
  py -V:3.12 -I scripts/t01a2_fm_sweep.py --verify OUT.json   # 随机抽 3 个 offset 回读复现

退出码: 0 成功 / 1 检查未过 / 2 用法或致命错误。
"""

import argparse
import json
import mmap
import os
import random
import re
import struct
import sys
import time

FM_EXE = r"D:\tmp2b\fm24\input\fm.exe"
EDITOR_EXE = r"D:\tmp2b\fm24\input\editor.exe"
MASTER = r"D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json"
OUT_DIR = r"D:\tmp2b\fm24-db\scratch\t01\inbox\t01a2"

WINDOW = 1 << 20      # 密度剖面窗口: 1MB
CLUSTER_GAP = 4096    # 相邻 <4096B 归簇
CLUSTER_MIN_HITS = 3  # 簇保留阈值(命中数)
CC_LIST_CAP = 50      # 每簇保留的 4CC 列表上限
SAMPLE_CAP = 10       # 每个码保留的样本 offset 数

ALNUM4 = rb"[A-Za-z0-9]{4}"

# (name, regex, imm_offset_within_match, family)
FORMS = [
    ("mov_rbp_d8", re.compile(rb"\xc7\x45." + ALNUM4), 3, "mov"),
    ("mov_rsp_d8", re.compile(rb"\xc7\x44\x24." + ALNUM4), 4, "mov"),
    ("mov_rbp_d32", re.compile(rb"\xc7\x85...." + ALNUM4), 6, "mov"),
    ("cmp_r32", re.compile(rb"\x81[\xf8-\xff]" + ALNUM4), 2, "cmp"),  # 含 81 fa / 81 fe
    ("cmp_eax", re.compile(rb"\x3d" + ALNUM4), 1, "cmp"),
]

ANCHOR_CODES = ["cnam", "cnsm", "cl3n", "cnti", "ccti",
                "cpcm", "crep", "cext", "PLgn", "dbty"]
# 修正拼写:任务书的 cnsm/cl3n 在 master.json 与二进制里实际是 csnm/c3ln
ANCHOR_CODES_CORRECTED = ["cnam", "csnm", "c3ln", "cnti", "ccti",
                          "cpcm", "crep", "cext", "PLgn", "dbty"]


# ---------------------------------------------------------------- 扫描核心
def scan(path):
    """全文件扫描,返回 {hits:[(off, form_name, code_bytes)], size, sec}。"""
    size = os.path.getsize(path)
    hits = []
    t0 = time.time()
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for name, rx, imm_off, _fam in FORMS:
                for m in rx.finditer(mm):
                    hits.append((m.start() + imm_off, name, mm[m.start() + imm_off:
                                                               m.start() + imm_off + 4]))
        finally:
            mm.close()
    hits.sort(key=lambda h: h[0])
    return {"hits": hits, "size": size, "sec": round(time.time() - t0, 2)}


def readings(cb):
    """返回适用于该 imm 的读法集合: 'fwd' / 'rev'(两者都可能,回文时两个都有)。"""
    out = []
    if all(48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122 for b in cb):
        out.append("fwd")
    rb = cb[::-1]
    if all(48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122 for b in rb):
        out.append("rev")
    return out


def norm_code(cb):
    """editor 口径: ASCII 反序显示。返回 (rev, readings)。"""
    return cb[::-1].decode("ascii", "replace")


def raw_occurrences(path, needle, cap=10):
    """needle 在文件中的原始字节出现次数 + 前 cap 个 offset。"""
    n, offs = 0, []
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            i = mm.find(needle)
            while i != -1:
                n += 1
                if len(offs) < cap:
                    offs.append(i)
                i = mm.find(needle, i + 1)
        finally:
            mm.close()
    return n, offs


def walk_imm4(path, prefix):
    """扫 prefix + 4 bytes 的原始形态(用于 add rax,0x38 之类步进统计)。"""
    n, first = 0, None
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            i = mm.find(prefix)
            while i != -1:
                n += 1
                if first is None:
                    first = i
                i = mm.find(prefix, i + 1)
        finally:
            mm.close()
    return n, first


# ---------------------------------------------------------------- 分析
def density(hits, window=WINDOW, topn=20):
    buckets = {}
    for off, _n, _cb in hits:
        buckets[off // window] = buckets.get(off // window, 0) + 1
    top = sorted(buckets.items(), key=lambda kv: (-kv[1], kv[0]))[:topn]
    covered = len(buckets)
    return ([{"window_off": w * window, "count": c} for w, c in top],
            covered)


def clusterize(hits, gap=CLUSTER_GAP, min_hits=CLUSTER_MIN_HITS):
    if not hits:
        return []
    clusters, cur = [], [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < gap:
            cur.append(h)
        else:
            if len(cur) >= min_hits:
                clusters.append(cur)
            cur = [h]
    if len(cur) >= min_hits:
        clusters.append(cur)
    return clusters


def cluster_record(cl):
    forms = {"mov": 0, "cmp": 0}
    fam = {n: f for n, _r, _o, f in FORMS}
    codes, seen = [], set()
    for off, name, cb in cl:
        forms[fam[name]] += 1
        if cb not in seen:
            seen.add(cb)
            codes.append((off, cb))
    n = len(codes)
    if forms["mov"] and forms["cmp"]:
        ratio = round(forms["mov"] / forms["cmp"], 3)
    else:
        ratio = None
    return {
        "start": cl[0][0],
        "end": cl[-1][0],
        "span": cl[-1][0] - cl[0][0],
        "n_hits": len(cl),
        "n_distinct4CC": n,
        "forms": forms,
        "mov_cmp_ratio": ratio,
        "cc_list": [norm_code(cb) for _o, cb in codes[:CC_LIST_CAP]],
        "cc_offsets": [o for o, _cb in codes[:CC_LIST_CAP]],
    }


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def anchor_check(path, hits, codes=None):
    """锚点自检: 指定 comp 码的命中数 + 前 10 个 offset。"""
    codes = codes or ANCHOR_CODES
    by_code_fwd, by_code_rev = {}, {}
    for off, name, cb in hits:
        for r in readings(cb):
            if r == "fwd":
                by_code_fwd.setdefault(cb.decode("ascii"), []).append((off, name))
            else:
                by_code_rev.setdefault(cb[::-1].decode("ascii"), []).append((off, name))
    out = {}
    for code in codes:
        hit_codes_fwd = by_code_fwd.get(code, [])
        hit_codes_rev = by_code_rev.get(code, [])
        raw_f, offs_f = raw_occurrences(path, code.encode("ascii"))
        raw_r, offs_r = raw_occurrences(path, code.encode("ascii")[::-1])
        out[code] = {
            "n_hits_as_imm_rev": len(hit_codes_rev),
            "n_hits_as_imm_fwd": len(hit_codes_fwd),
            "sample_offs_rev": [o for o, _n in hit_codes_rev[:SAMPLE_CAP]],
            "sample_offs_fwd": [o for o, _n in hit_codes_fwd[:SAMPLE_CAP]],
            "sample_forms_rev": [n for _o, n in hit_codes_rev[:SAMPLE_CAP]],
            "raw_ascii_fwd": {"count": raw_f, "first_offs": offs_f},
            "raw_ascii_rev": {"count": raw_r, "first_offs": offs_r},
            "present": bool(hit_codes_fwd or hit_codes_rev),
        }
    return out


def code_set(hits, direction):
    s = set()
    for _off, _n, cb in hits:
        if direction in readings(cb):
            s.add(cb.decode("ascii") if direction == "fwd" else cb[::-1].decode("ascii"))
    return s


def entity_match(hits, master):
    es = master["entity_summary"]
    fwd = code_set(hits, "fwd")
    rev = code_set(hits, "rev")
    rows = []
    for ent, info in es.items():
        codes = info["codes"]
        jr = jaccard(codes, rev)
        jf = jaccard(codes, fwd)
        rows.append({
            "entity": ent,
            "n_codes": len(codes),
            "jaccard_rev": round(jr, 4),
            "jaccard_fwd": round(jf, 4),
            "best": round(max(jr, jf), 4),
            "hit_rev": len(set(codes) & rev),
            "hit_fwd": len(set(codes) & fwd),
            "coverage_rev": round(len(set(codes) & rev) / len(codes), 4) if codes else 0.0,
        })
    rows.sort(key=lambda r: (-r["best"], -r["n_codes"], r["entity"]))
    return rows, fwd, rev


def editor_compare(fm_hits, ed_hits, master, fm_path, ed_path):
    fm_fwd, fm_rev = code_set(fm_hits, "fwd"), code_set(fm_hits, "rev")
    ed_fwd, ed_rev = code_set(ed_hits, "fwd"), code_set(ed_hits, "rev")
    ed_codes = master_all_codes(master)

    blk_fm = stride30_blocks(fm_hits)
    blk_ed = stride30_blocks(ed_hits)
    bcmp = block_compare(blk_fm, blk_ed)

    def block_rows(blocks):
        rows = []
        for movs in blocks:
            ds = [b[0] - a[0] for a, b in zip(movs, movs[1:])]
            rows.append({"start": movs[0][0], "end": movs[-1][0],
                         "n_mov": len(movs), "stride30": ds.count(0x30)})
        return rows

    # 缺席实体码: master 的 code 在 fm 的两种读法里都没有
    missing_by_entity = {}
    for ent, info in master["entity_summary"].items():
        codes = info["codes"]
        miss = [c for c in codes if c not in fm_rev and c not in fm_fwd]
        have = [c for c in codes if c in fm_rev or c in fm_fwd]
        missing_by_entity[ent] = {"n_missing": len(miss),
                                  "n_present": len(have),
                                  "missing_sample": miss[:20]}
    tot_miss = sum(v["n_missing"] for v in missing_by_entity.values())
    tot_codes = sum(len(info["codes"]) for info in master["entity_summary"].values())

    return {
        "editor": {
            "exe": ed_path, "size": os.path.getsize(ed_path),
            "n_hits": len(ed_hits),
            "n_distinct4CC_fwd": len(ed_fwd),
            "n_distinct4CC_rev": len(ed_rev),
            "n_stride30_blocks": len(blk_ed),
            "stride30_blocks_first10": block_rows(blk_ed)[:10],
        },
        "fm": {
            "exe": fm_path, "size": os.path.getsize(fm_path),
            "n_hits": len(fm_hits),
            "n_distinct4CC_fwd": len(fm_fwd),
            "n_distinct4CC_rev": len(fm_rev),
            "n_stride30_blocks": len(blk_fm),
            "stride30_blocks": block_rows(blk_fm),
        },
        "block_match": bcmp,
        "comp_registration_blocks": {
            "fm": comp_blocks(fm_hits, blk_fm),
            "editor": comp_blocks(ed_hits, blk_ed),
        },
        "code_overlap": {
            "master_codes_union": len(ed_codes),
            "fm_rev_intersect_master": len(ed_codes & fm_rev),
            "fm_fwd_intersect_master": len(ed_codes & fm_fwd),
            "editor_rev_intersect_master": len(ed_codes & ed_rev),
            "jaccard_fm_rev_vs_master": round(jaccard(fm_rev, ed_codes), 4),
            "jaccard_fm_fwd_vs_master": round(jaccard(fm_fwd, ed_codes), 4),
            "jaccard_ed_rev_vs_master": round(jaccard(ed_rev, ed_codes), 4),
            "fm_rev_vs_ed_rev_jaccard": round(jaccard(fm_rev, ed_rev), 4),
        },
        "missing_entity_codes": {
            "total_codes": tot_codes,
            "total_missing_in_fm": tot_miss,
            "whole_entity_absent": sorted(
                [e for e, v in missing_by_entity.items() if v["n_present"] == 0]),
            "by_entity": missing_by_entity,
        },
    }


def master_all_codes(master):
    s = set()
    for info in master["entity_summary"].values():
        s.update(info["codes"])
    return s


# ---------------------------------------------------------------- PE 节区
def pe_sections(path):
    """读 PE 头,返回 [(name, raw_off, raw_size, va)]。"""
    with open(path, "rb") as f:
        d = f.read(0x1000)
    e = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    opt = struct.unpack_from("<H", d, e + 20)[0]
    st = e + 24 + opt
    out = []
    for i in range(nsec):
        o = st + i * 40
        name = d[o:o + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
        out.append((name, ro, rs, va))
    return out


def section_profile(path, hits, sections):
    """每节区的命中数 / 密度(每 MB) / 原始 offset→VA 换算。"""
    def to_va(off):
        for _nm, ro, rs, va in sections:
            if ro <= off < ro + rs:
                return off - ro + va
        return None

    rows = []
    for nm, ro, rs, va in sections:
        n = sum(1 for o, _n, _cb in hits if ro <= o < ro + rs)
        rows.append({
            "name": nm, "raw_off": ro, "raw_size": rs, "va": va,
            "n_hits": n,
            "hits_per_mb": round(n / (rs / 1048576), 2) if rs else 0.0,
            "va_base": hex(va),
        })
    code = [r for r in rows if r["n_hits"]]
    return rows, code, to_va


# ---------------------------------------------------------------- 块比对
def stride30_blocks(hits, min_stride=5):
    """0x30 步进 mov-imm 块:返回 [[(off, code_bytes)...]]。"""
    fam = {n: f for n, _r, _o, f in FORMS}
    out = []
    for c in clusterize(hits):
        movs = [(o, cb) for o, n, cb in c if fam[n] == "mov"]
        ds = [b[0] - a[0] for a, b in zip(movs, movs[1:])]
        if ds.count(0x30) >= min_stride:
            out.append(movs)
    return out


def block_compare(fm_blocks, ed_blocks, cap=40):
    import difflib

    seq = lambda movs: [cb[::-1].decode("ascii", "replace") for _o, cb in movs]
    fs = [seq(b) for b in fm_blocks]
    es = [seq(b) for b in ed_blocks]
    exact = []
    for i, a in enumerate(fs):
        for j, b in enumerate(es):
            if a == b:
                exact.append({"fm_off": fm_blocks[i][0][0],
                              "ed_off": ed_blocks[j][0][0],
                              "n_codes": len(a),
                              "codes_head": a[:8]})
    fm_only, ed_only = [], []
    eset = {tuple(b) for b in es}
    fset = {tuple(a) for a in fs}
    for i, a in enumerate(fs):
        if tuple(a) not in eset:
            fm_only.append({"fm_off": fm_blocks[i][0][0], "n_codes": len(a),
                            "codes_head": a[:12]})
    for j, b in enumerate(es):
        if tuple(b) not in fset:
            ed_only.append({"ed_off": ed_blocks[j][0][0], "n_codes": len(b),
                            "codes_head": b[:12]})
    return {
        "n_fm_blocks": len(fm_blocks), "n_ed_blocks": len(ed_blocks),
        "n_exact_block_matches": len(exact),
        "exact_matches": exact[:cap],
        "fm_only_blocks": fm_only[:cap],
        "ed_only_blocks": ed_only[:cap],
    }


def comp_blocks(hits, blocks, wanted=("cnam",), cap_codes=60):
    """包含指定 comp 码的 0x30 块(注册块),返回完整码序列。"""
    out = []
    for movs in blocks:
        codes = [cb[::-1].decode("ascii", "replace") for _o, cb in movs]
        if any(w in codes for w in wanted):
            out.append({"off": movs[0][0], "n_codes": len(codes),
                        "codes": codes[:cap_codes],
                        "has_nsm_variant": [c for c in codes
                                            if c in ("cnsm", "csnm")],
                        "has_l3n_variant": [c for c in codes
                                            if c in ("cl3n", "c3ln")]})
    return out


# ---------------------------------------------------------------- 校验
def verify_offsets(json_path, fm_path, n=3, rng=None):
    """随机抽 n 个 offset,回读 fm.exe 字节复现形态。"""
    data = json.load(open(json_path, encoding="utf-8"))
    cands = []
    for cl in data["clusters"]:
        for off, code in zip(cl["cc_offsets"], cl["cc_list"]):
            cands.append((off, code))
    for code, info in data["anchor_check"].items():
        for off in info["sample_offs_rev"][:2]:
            cands.append((off, code))
    if not cands:
        print("[verify] 无候选 offset", file=sys.stderr)
        return 1
    rng = rng or random.Random()
    picks = rng.sample(cands, min(n, len(cands)))
    fam_by_name = {nm: (rx, imm_off) for nm, rx, imm_off, _f in FORMS}
    ok_all = True
    with open(fm_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for off, code in picks:
                imm = mm[off:off + 4]
                rev = imm[::-1].decode("ascii", "replace")
                ctx = mm[max(0, off - 8):off + 4]
                ok = len(imm) == 4 and rev == code
                # 找能匹配该位置的形态
                form = None
                for nm, (rx, io) in fam_by_name.items():
                    for m in rx.finditer(mm, max(0, off - 8), off + 5):
                        if m.start() + io == off:
                            form = nm
                            break
                    if form:
                        break
                ok_all &= ok and form is not None
                print(f"[verify] off={off} imm={imm.hex(' ')} rev='{rev}' "
                      f"expect='{code}' form={form} ctx={ctx.hex(' ')} -> "
                      f"{'OK' if ok and form else 'FAIL'}")
        finally:
            mm.close()
    return 0 if ok_all else 1


def selftest():
    # 1) 形态识别
    buf = bytearray(b"\x90" * 64)
    put = [
        (4, b"\xc7\x45\xf0" + b"cnam"[::-1]),        # mov [rbp-0x10], 'cnam'
        (12, b"\xc7\x44\x24\x08" + b"cnsm"[::-1]),   # mov [rsp+8], 'cnsm'
        (22, b"\xc7\x85\x00\x01\x00\x00" + b"cl3n"[::-1]),
        (36, b"\x81\xfe" + b"ccti"[::-1]),           # cmp esi, 'ccti'
        (44, b"\x81\xfa" + b"cpcm"[::-1]),           # cmp edx, 'cpcm'
        (52, b"\x3d" + b"cext"[::-1]),               # cmp eax, 'cext'
        (58, b"\x81\xf8\x00\x00\x00\x00"),           # 非 4CC,应被丢弃
    ]
    for off, b in put:
        buf[off:off + len(b)] = b
    got = []
    for name, rx, imm_off, fam in FORMS:
        for m in rx.finditer(bytes(buf)):
            got.append((m.start() + imm_off, name, bytes(buf[m.start() + imm_off:
                                                            m.start() + imm_off + 4]),
                        fam))
    got.sort()
    # imm 起始 offset = 形态起始 + imm_off(不是形态起始)
    offs = [g[0] for g in got]
    assert len(got) == 6, f"expected 6 hits, got {len(got)}: {got}"
    assert offs == [7, 16, 28, 38, 46, 53], f"offsets wrong: {offs}"
    assert got[0][1] == "mov_rbp_d8" and got[0][2] == b"manc"
    assert got[2][1] == "mov_rbp_d32" and got[2][2] == b"n3lc"
    assert got[3][1] == "cmp_r32" and got[3][2] == b"itcc"
    assert got[5][1] == "cmp_eax" and got[5][2] == b"txec"
    # 读法与规范化(4 字节全 alnum 时两个读法都成立,方向本身即待验假设)
    assert readings(b"manc") == ["fwd", "rev"]
    assert readings(b"cnam") == ["fwd", "rev"]
    assert readings(b"abab") == ["fwd", "rev"]
    assert norm_code(b"manc") == "cnam"
    # 2) 聚类
    hits = [(0, "cmp_r32", b"aaaa"), (1000, "cmp_r32", b"bbbb"),
            (2000, "cmp_r32", b"cccc"), (20000, "cmp_r32", b"dddd")]
    cl = clusterize(hits)
    assert len(cl) == 1 and len(cl[0]) == 3, cl
    cl2 = clusterize(hits, gap=20001)
    assert len(cl2) == 1 and len(cl2[0]) == 4, cl2
    rec = cluster_record(cl[0])
    assert rec["n_hits"] == 3 and rec["forms"]["cmp"] == 3 and rec["forms"]["mov"] == 0
    assert rec["mov_cmp_ratio"] is None
    assert rec["cc_list"] == ["aaaa", "bbbb", "cccc"]
    # 3) 密度
    top, covered = density(hits)
    assert covered == 1 and top[0] == {"window_off": 0, "count": 4}, (top, covered)
    # 4) jaccard
    assert jaccard({"a", "b"}, {"b", "c"}) == 1 / 3
    assert jaccard(set(), set()) == 0.0
    # 5) 输入存在性(只检查,不扫描)
    assert os.path.isfile(FM_EXE), f"missing {FM_EXE}"
    print("[selftest] OK: 6 hits / 3 forms / cluster / density / jaccard 全部通过")
    print(f"[selftest] fm.exe size={os.path.getsize(FM_EXE)} "
          f"editor.exe size={os.path.getsize(EDITOR_EXE) if os.path.isfile(EDITOR_EXE) else 'n/a'}")
    return 0


# ---------------------------------------------------------------- 主流程
def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(
        description="t01-a2: fm.exe 4CC 注册块/比较式扫描(纯 stdlib,只读)")
    ap.add_argument("--fm", default=FM_EXE, help=f"fm.exe 路径(默认 {FM_EXE})")
    ap.add_argument("--editor", default=EDITOR_EXE,
                    help=f"editor.exe 路径(默认 {EDITOR_EXE})")
    ap.add_argument("--master", default=MASTER, help="master.json 路径")
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "fm_sweep.json"),
                    help="输出 JSON 路径")
    ap.add_argument("--no-editor", action="store_true", help="跳过 editor.exe 对照扫描")
    ap.add_argument("--cluster-cap", type=int, default=0,
                    help="clusters 列表最多写多少条(0=全部,默认 0)")
    ap.add_argument("--selftest", action="store_true", help="跑内置自检后退出")
    ap.add_argument("--verify", metavar="JSON", help="随机抽 3 offset 回读复现后退出")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.verify:
        return verify_offsets(args.verify, args.fm, n=3)

    if not os.path.isfile(args.fm):
        print(f"[fatal] 找不到 {args.fm}", file=sys.stderr)
        return 2
    if not os.path.isfile(args.master):
        print(f"[fatal] 找不到 {args.master}", file=sys.stderr)
        return 2

    master = json.load(open(args.master, encoding="utf-8"))

    print(f"[fm] scan {args.fm} ({os.path.getsize(args.fm)} bytes) ...")
    fm = scan(args.fm)
    fam = {n: f for n, _r, _o, f in FORMS}
    n_mov = sum(1 for h in fm["hits"] if fam[h[1]] == "mov")
    n_cmp = sum(1 for h in fm["hits"] if fam[h[1]] == "cmp")
    by_form = {}
    for _o, nm, _cb in fm["hits"]:
        by_form[nm] = by_form.get(nm, 0) + 1
    print(f"[fm] hits={len(fm['hits'])} (mov={n_mov} cmp={n_cmp}) "
          f"distinct4CC={len({h[2] for h in fm['hits']})} {fm['sec']}s")
    print(f"[fm] by_form={by_form}")

    anchors = anchor_check(args.fm, fm["hits"])
    anchors_fixed = anchor_check(args.fm, fm["hits"], ANCHOR_CODES_CORRECTED)
    print("[fm] anchor_check(任务书拼写):")
    for code, info in anchors.items():
        print(f"   {code}: imm(rev)={info['n_hits_as_imm_rev']:5d} "
              f"imm(fwd)={info['n_hits_as_imm_fwd']:5d} "
              f"raw_rev={info['raw_ascii_rev']['count']:5d} "
              f"raw_fwd={info['raw_ascii_fwd']['count']:5d} "
              f"present={info['present']}")
    print("[fm] anchor_check(修正拼写 csnm/c3ln):")
    for code, info in anchors_fixed.items():
        print(f"   {code}: imm(rev)={info['n_hits_as_imm_rev']:5d} "
              f"raw_rev={info['raw_ascii_rev']['count']:5d} present={info['present']}")

    top20, covered = density(fm["hits"])
    print(f"[fm] density: {covered} 个窗口有命中; top5="
          f"{[(t['window_off'], t['count']) for t in top20[:5]]}")

    sections = pe_sections(args.fm)
    sec_rows, sec_hit, to_va = section_profile(args.fm, fm["hits"], sections)
    for r in sec_hit:
        print(f"[fm] section {r['name']:<9} raw={r['raw_off']:<10} "
              f"size={r['raw_size']:<10} hits={r['n_hits']:<6} "
              f"per_MB={r['hits_per_mb']}")

    clusters = clusterize(fm["hits"])
    recs = [cluster_record(c) for c in clusters]
    recs.sort(key=lambda r: (-r["n_hits"], r["start"]))
    for r in recs:
        r["section"] = None
        for nm, ro, rs, va in sections:
            if ro <= r["start"] < ro + rs:
                r["section"] = nm
                r["va_start"] = hex(r["start"] - ro + va)
                break
    n_distinct_ge3 = sum(1 for r in recs if r["n_distinct4CC"] >= 3)
    print(f"[fm] clusters(>=3 hits, gap<{CLUSTER_GAP})={len(recs)} "
          f"(其中 distinct4CC>=3 的 {n_distinct_ge3} 个); "
          f"top3 命中数={[r['n_hits'] for r in recs[:3]]}")

    ent_rows, fm_fwd, fm_rev = entity_match(fm["hits"], master)
    # 无噪声版:只取 .sdata(真实代码区),排除 .arch 打包资源里的随机 4CC
    sdata_lo, sdata_hi = None, None
    for nm, ro, rs, va in sections:
        if nm == ".sdata":
            sdata_lo, sdata_hi = ro, ro + rs
    sdata_hits = [h for h in fm["hits"] if sdata_lo <= h[0] < sdata_hi]
    ent_rows_sd, fm_fwd_sd, fm_rev_sd = entity_match(sdata_hits, master)
    print("[fm] entity_match top3(.sdata only):")
    for r in ent_rows_sd[:3]:
        print(f"   {r['best']:.4f} (rev={r['jaccard_rev']:.4f}) {r['entity']} "
              f"n={r['n_codes']} hit_rev={r['hit_rev']}")
    print("[fm] entity_match top3:")
    for r in ent_rows[:3]:
        print(f"   {r['best']:.4f} (rev={r['jaccard_rev']:.4f} fwd={r['jaccard_fwd']:.4f}) "
              f"{r['entity']} n={r['n_codes']} hit_rev={r['hit_rev']}")

    ed = None
    if args.no_editor or not os.path.isfile(args.editor):
        cmp_block = {"skipped": True, "reason": "--no-editor or editor.exe missing"}
        print("[editor] 跳过对照")
    else:
        print(f"[editor] scan {args.editor} ({os.path.getsize(args.editor)} bytes) ...")
        ed = scan(args.editor)
        print(f"[editor] hits={len(ed['hits'])} {ed['sec']}s")
        cmp_block = editor_compare(fm["hits"], ed["hits"], master, args.fm, args.editor)
        co = cmp_block["code_overlap"]
        print(f"[editor] jaccard(fm_rev, master_codes)={co['jaccard_fm_rev_vs_master']} "
              f"jaccard(ed_rev, master_codes)={co['jaccard_ed_rev_vs_master']} "
              f"jaccard(fm_rev, ed_rev)={co['fm_rev_vs_ed_rev_jaccard']}")
        print(f"[editor] stride30 块: editor={cmp_block['editor']['n_stride30_blocks']} "
              f"fm={cmp_block['fm']['n_stride30_blocks']}; "
              f"完全同序列块={cmp_block['block_match']['n_exact_block_matches']}")
        for side in ("fm", "editor"):
            for b in cmp_block["comp_registration_blocks"][side]:
                print(f"[editor] comp 注册块 {side}: off={b['off']} "
                      f"n={b['n_codes']} head={b['codes'][:8]} "
                      f"nsm={b['has_nsm_variant']} l3n={b['has_l3n_variant']}")
        me = cmp_block["missing_entity_codes"]
        print(f"[editor] 实体码缺席: {me['total_missing_in_fm']}/{me['total_codes']}; "
              f"整实体缺席 {len(me['whole_entity_absent'])} 个")

    # 步进/回归锚点(raw 字节)
    n38, f38 = walk_imm4(args.fm, b"\x48\x83\xc0\x38")
    n30, f30 = walk_imm4(args.fm, b"\x48\x83\xc0\x30")
    ssds = b"\x81\xfa\x63\x70\x61\x63"
    nss, fss = walk_imm4(args.fm, ssds)
    print(f"[fm] stepper add rax,0x38={n38} first={f38}; add rax,0x30={n30} first={f30}")
    print(f"[fm] '81 fa 63 70 61 63' (cmp edx,'cpac') count={nss} first={fss}")

    out = {
        "meta": {
            "exe": args.fm,
            "size": fm["size"],
            "scan_sec": fm["sec"],            "forms": {
                "mov_rbp_d8": "c7 45 <disp8> <imm32>  (mov dword [rbp+d8], imm32)",
                "mov_rsp_d8": "c7 44 24 <disp8> <imm32>  (mov dword [rsp+d8], imm32)",
                "mov_rbp_d32": "c7 85 <disp32> <imm32>  (mov dword [rbp+d32], imm32)",
                "cmp_r32": "81 f8..ff <imm32>  (cmp r32, imm32; 含 81 fa / 81 fe)",
                "cmp_eax": "3d <imm32>  (cmp eax, imm32)",
                "filter": "imm32 必须可读为 [A-Za-z0-9]{4}(fwd 或 rev)",
                "readings": "fwd=文件顺序 ASCII; rev=字节反序(=editor.exe 的存储口径/IDA 大端显示)",
            },
            "params": {"window": WINDOW, "cluster_gap": CLUSTER_GAP,
                       "cluster_min_hits": CLUSTER_MIN_HITS,
                       "cc_list_cap": CC_LIST_CAP, "sample_cap": SAMPLE_CAP},
            "counts": {"n_hits": len(fm["hits"]), "n_mov": n_mov, "n_cmp": n_cmp,
                       "n_distinct4CC": len({h[2] for h in fm["hits"]}),
                       "by_form": by_form},
            "raw_anchors": {
                "add_rax_0x38": {"count": n38, "first_off": f38},
                "add_rax_0x30": {"count": n30, "first_off": f30},
                "81_fa_63706163": {"bytes": "81 fa 63 70 61 63", "count": nss,
                                   "first_off": fss},
            },
        },
        "anchor_check": anchors,
        "anchor_check_corrected": anchors_fixed,
        "anchor_note": "cnsm/cl3n 为任务书笔误;master.json 与两个二进制的实际码均为 csnm/c3ln",
        "sections": {
            "note": "PE 节区归属;.sdata=真实代码/数据主体,.arch=打包资源(命中属随机噪声对照)",
            "all": sec_rows,
            "with_hits": sec_hit,
        },
        "density_top20": top20,
        "density_windows_covered": covered,
        "clusters": recs if args.cluster_cap <= 0 else recs[:args.cluster_cap],
        "clusters_meta": {"n_clusters": len(recs),
                          "n_clusters_distinct_ge3": n_distinct_ge3,
                          "written": len(recs) if args.cluster_cap <= 0
                          else min(args.cluster_cap, len(recs))},
        "entity_match": {
            "method": "Jaccard(master entity_summary.codes, fm 4CC 集合);比对 rev(editor 口径)与 fwd 两向",
            "caveat": "Jaccard 分母含 fm 全量 4CC(含大量与实体无关的比较即时数),故绝对值偏低;看 coverage_rev 更有意义",
            "top3": ent_rows[:3],
            "top10": ent_rows[:10],
            "all": ent_rows,
            "fm_fwd_codes_n": len(fm_fwd),
            "fm_rev_codes_n": len(fm_rev),
        },
        "entity_match_sdata_only": {
            "method": "同上,但只用 .sdata 区的命中(剔除 .arch 打包资源噪声)",
            "n_hits_used": len(sdata_hits),
            "top3": ent_rows_sd[:3],
            "top10": ent_rows_sd[:10],
            "all": ent_rows_sd,
            "fm_fwd_codes_n": len(fm_fwd_sd),
            "fm_rev_codes_n": len(fm_rev_sd),
        },
        "editor_compare": cmp_block,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[out] {args.out} ({os.path.getsize(args.out)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
