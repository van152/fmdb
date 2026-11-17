#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""t01-d: editor.exe 4CC(字段码)立即数形态全量普查。

纯标准库、只读输入、不启动任何程序。扫描 editor.exe 中「立即数 = 4 字节 ASCII 反序
字段码」的指令形态,产出 census.json:
  * per_form_counts  每形态命中数(raw 操作码出现数 / alnum 4CC 命中数)
  * per_code         每候选码的 (形态 × 次数) + 前 10 个文件偏移
  * entity_coverage  vocab.json 32 实体的字段码覆盖/零命中清单
  * density_top      0x100000 窗口密度 top20
  * anchor_check     cnam@0xebf093 / ccti@0xebf153 自检

用法:
  py -V:3.12 -I scripts/t01d_census.py --help
  py -V:3.12 -I scripts/t01d_census.py                  # 全量扫描 + 写 census.json
  py -V:3.12 -I scripts/t01d_census.py --selftest        # 形态/反序/覆盖逻辑自检
  py -V:3.12 -I scripts/t01d_census.py --verify FILE     # 随机抽 3 码回读原文件复现
  py -V:3.12 -I scripts/t01d_census.py --sample 20       # 抽 20 个命中打印上下文(人工核对用)

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

EDITOR_EXE = r"D:\tmp2b\fm24\input\editor.exe"
VOCAB = r"D:\tmp2b\fm24-db\scratch\t01\inbox\t01c\vocab.json"
MASTER = r"D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json"
OUT_DIR = r"D:\tmp2b\fm24-db\scratch\t01\inbox\t01d"
OUT_JSON = os.path.join(OUT_DIR, "census.json")

WINDOW = 0x100000     # 密度窗口 1MB
SAMPLE_CAP = 10       # 每码保留的偏移样本数
TOP_CODES = 20

ALNUM4 = rb"[A-Za-z0-9]{4}"

# (form_name, raw_regop_pattern, alnum_pattern, imm_offset_in_match, family)
# raw_regop_pattern: 只认操作码(用于给出「立即数看起来像 4CC」的概率分母)
FORMS = [
    ("mov_rbp_d8", re.compile(rb"\xc7\x45"), re.compile(rb"\xc7\x45." + ALNUM4), 3, "mov"),
    ("mov_rsp_d8", re.compile(rb"\xc7\x44\x24"), re.compile(rb"\xc7\x44\x24." + ALNUM4), 4, "mov"),
    ("mov_rbp_d32", re.compile(rb"\xc7\x85"), re.compile(rb"\xc7\x85...." + ALNUM4), 6, "mov"),
    ("mov_r32", re.compile(rb"[\xb8-\xbf]"), re.compile(rb"[\xb8-\xbf]" + ALNUM4), 1, "mov"),
    ("cmp_r32", re.compile(rb"\x81[\xf8-\xff]"), re.compile(rb"\x81[\xf8-\xff]" + ALNUM4), 2, "cmp"),
    ("cmp_eax", re.compile(rb"\x3d"), re.compile(rb"\x3d" + ALNUM4), 1, "cmp"),
]

# 锚点自检:(code, file_offset, expected_form)
ANCHORS = [("cnam", 0xEBF093, "mov_rbp_d8"), ("ccti", 0xEBF153, "mov_rbp_d8")]


# ---------------------------------------------------------------- PE sections
def pe_sections(buf):
    """返回 [(name, raw_ptr, raw_size)];失败返回 []。"""
    try:
        if buf[:2] != b"MZ":
            return []
        e = struct.unpack_from("<I", buf, 0x3C)[0]
        if buf[e:e + 4] != b"PE\x00\x00":
            return []
        nsec = struct.unpack_from("<H", buf, e + 6)[0]
        optsz = struct.unpack_from("<H", buf, e + 20)[0]
        base = e + 24 + optsz
        out = []
        for i in range(nsec):
            off = base + i * 40
            name = buf[off:off + 8].rstrip(b"\x00").decode("latin-1")
            _vs, _va, rawsz, rawptr = struct.unpack_from("<IIII", buf, off + 8)
            out.append((name, rawptr, rawsz))
        return out
    except Exception:
        return []


def section_of(offset, sections):
    for name, ptr, sz in sections:
        if sz and ptr <= offset < ptr + sz:
            return name
    return "?"


# ---------------------------------------------------------------- scan
def scan(buf, sections, want_offsets=True):
    """扫描全部形态;返回计数与 per_code 统计。"""
    per_form = {}
    per_code = {}          # code -> {form: count, "offsets": [...]}
    tot = {}               # code -> total hits
    density = {}           # window_off -> hits
    sec_hits = {}          # section -> hits
    per_sec_form = {}      # (section, form) -> hits
    all_offsets = []       # (offset, code, form) 供抽样(仅主扫描保留,内存可承受)
    for form, raw_re, alnum_re, imm_off, _family in FORMS:
        t0 = time.time()
        n_raw = sum(1 for _ in raw_re.finditer(buf))
        n_hit = 0
        for m in alnum_re.finditer(buf):
            start = m.start()
            imm = buf[start + imm_off:start + imm_off + 4]
            code = imm[::-1].decode("ascii")   # 反序:imm 字节 -> 字段码
            n_hit += 1
            e = per_code.get(code)
            if e is None:
                e = per_code[code] = {"offsets": []}
            e[form] = e.get(form, 0) + 1
            if want_offsets and len(e["offsets"]) < SAMPLE_CAP:
                e["offsets"].append(start)
            tot[code] = tot.get(code, 0) + 1
            w = start & ~(WINDOW - 1)
            density[w] = density.get(w, 0) + 1
            s = section_of(start, sections)
            sec_hits[s] = sec_hits.get(s, 0) + 1
            per_sec_form[(s, form)] = per_sec_form.get((s, form), 0) + 1
            if want_offsets:
                all_offsets.append((start, code, form))
        per_form[form] = {
            "raw_opcode_occurrences": n_raw,
            "hits_alnum4cc": n_hit,
            "hit_rate_of_raw": round(n_hit / n_raw, 6) if n_raw else None,
            "imm_offset_in_match": imm_off,
            "scan_seconds": round(time.time() - t0, 2),
        }
        print(f"[form] {form:12s} raw={n_raw:9d} hits={n_hit:8d}", flush=True)
    for e in per_code.values():
        e["total"] = 0
    for code, n in tot.items():
        per_code[code]["total"] = n
    return per_form, per_code, density, sec_hits, per_sec_form, all_offsets


# ---------------------------------------------------------------- vocab
def load_vocab_entities(path=VOCAB):
    """返回 ({entity: [codes]}, meta)。vocab 优先,退回 master。"""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            v = json.load(f)
        ents = {k: list(v["entities"][k].get("codes") or []) for k in v["entities"]}
        return ents, {"source": path, "kind": "vocab.json entities[].codes"}
    with open(MASTER, encoding="utf-8") as f:
        m = json.load(f)
    ents = {}
    for k in (m.get("entity_summary") or {}):
        ents[k] = list((m["entity_summary"][k].get("codes") or []))
    return ents, {"source": MASTER, "kind": "master.json entity_summary[].codes (fallback)"}


def entity_coverage(entities, per_code):
    rows = {}
    for ent, codes in sorted(entities.items()):
        hit_codes = [c for c in codes if c in per_code]
        zero = [c for c in codes if c not in per_code]
        rows[ent] = {
            "total": len(codes),
            "total_distinct": len(set(codes)),
            "hit": len(hit_codes),
            "hit_distinct": len(set(hit_codes)),
            "zero_hit_codes": zero,
            "hit_codes": hit_codes,
        }
    return rows


# ---------------------------------------------------------------- verify
def read_back(path, offset, form):
    """按形态在 offset 处回读原始字节,验证反序码可复现。"""
    names = {f[0]: f for f in FORMS}
    form_name, _raw, _alnum, imm_off, _fam = names[form]
    with open(path, "rb") as f:
        f.seek(offset)
        head = f.read(imm_off + 4)
        f.seek(offset + imm_off)
        imm = f.read(4)
    return {"offset": offset, "form": form_name, "raw_bytes": head.hex(" "),
            "imm_bytes": imm.hex(" "), "code": imm[::-1].decode("ascii", "replace")}


def cmd_verify(args):
    with open(args.verify, encoding="utf-8") as f:
        c = json.load(f)
    rnd = random.Random(args.seed)
    codes = [k for k, v in c["per_code"].items() if v.get("offsets")]
    if not codes:
        print("[verify] 无可用码", flush=True)
        return 1
    ok = True
    for code in rnd.sample(codes, min(3, len(codes))):
        e = c["per_code"][code]
        form = next(k for k in e if k not in ("offsets", "total"))
        off = e["offsets"][0]
        rb = read_back(args.exe, off, form)
        good = (rb["code"] == code)
        ok = ok and good
        print(f"[verify] {code} @ {hex(off)} {form}: {rb['raw_bytes']} -> {rb['code']} "
              f"{'OK' if good else 'MISMATCH'}", flush=True)
    return 0 if ok else 1


# ---------------------------------------------------------------- sample / FP
def cmd_sample(args):
    """抽 N 个命中打印上下文,供人工核对真/误报。"""
    with open(args.exe, "rb") as f:
        buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        rnd = random.Random(args.seed)
        hits = []
        for form, _raw, alnum_re, imm_off, _fam in FORMS:
            for m in alnum_re.finditer(buf):
                hits.append((m.start(), form, buf[m.start() + imm_off:m.start() + imm_off + 4][::-1].decode()))
        print(f"[sample] total hits={len(hits)}", flush=True)
        for off, form, code in rnd.sample(hits, min(args.sample, len(hits))):
            lo = max(0, off - 16)
            ctx = buf[lo:off + 16]
            print(f"{hex(off)} {form:12s} {code} | {ctx.hex(' ')}", flush=True)
    return 0


# ---------------------------------------------------------------- selftest
def cmd_selftest(args):
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + msg)
        ok = ok and bool(cond)

    # 1) 反序语义:cnam -> 6d 61 6e 63
    chk(b"cnam"[::-1] == b"\x6d\x61\x6e\x63", "反序:'cnam' -> 6d 61 6e 63")
    # 2) 每个形态在构造样本上定位到正确 imm
    for form, _raw, alnum_re, imm_off, _fam in FORMS:
        prefix = {"mov_rbp_d8": b"\xc7\x45\xf0",
                  "mov_rsp_d8": b"\xc7\x44\x24\x10",
                  "mov_rbp_d32": b"\xc7\x85\x34\x12\x00\x00",
                  "mov_r32": b"\xb9",
                  "cmp_r32": b"\x81\xfa",
                  "cmp_eax": b"\x3d"}[form]
        # imm 在文件里是字段码的**反序**字节,故此处写 b'cnam'[::-1]
        sample = b"\x90" * 3 + prefix + b"cnam"[::-1] + b"\x90" * 3
        ms = list(alnum_re.finditer(sample))
        chk(len(ms) == 1, f"{form}: 单命中")
        if ms:
            m = ms[0]
            got = sample[m.start() + imm_off:m.start() + imm_off + 4][::-1]
            chk(got == b"cnam", f"{form}: imm 定位正确 -> {got!r}")
    # 3) 非 alnum 立即数不得命中
    chk(not re.search(rb"\xc7\x45." + ALNUM4, b"\xc7\x45\xf0\x00\x00\x00\x00"), "mov_rbp_d8 拒绝全零 imm")
    chk(not re.search(rb"\xc7\x45." + ALNUM4, b"\xc7\x45\xf0ab d"), "4 字符但含空格不命中")
    # 4) 词汇表可加载且实体非空
    ents, meta = load_vocab_entities()
    chk(len(ents) == 32, f"词汇表实体数 = 32 (实际 {len(ents)}) via {meta['kind']}")
    chk(all(v for v in ents.values()), "每实体 codes 非空")
    # 5) 覆盖逻辑:人为构造命中集
    fake = {"cnam": {"total": 1, "mov_rbp_d8": 1, "offsets": [0]}}
    cov = entity_coverage({"comp.xml#comp": ["cnam", "ccti"]}, fake)
    chk(cov["comp.xml#comp"]["hit"] == 1 and cov["comp.xml#comp"]["zero_hit_codes"] == ["ccti"],
        "覆盖计数/零命中清单正确")
    # 6) 真实锚点回读(只读这 2 个偏移,不做全扫)
    if os.path.exists(args.exe):
        for code, off, form in ANCHORS:
            rb = read_back(args.exe, off, form)
            chk(rb["code"] == code, f"锚点 {code}@{hex(off)} 回读 = {rb['code']} ({rb['raw_bytes']})")
    else:
        print("  skip   锚点回读(exe 不存在)")
    print("[selftest]", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="editor.exe 4CC imm 形态普查(t01-d)")
    ap.add_argument("--exe", default=EDITOR_EXE, help="目标 exe(默认 editor.exe,只读)")
    ap.add_argument("--out", default=OUT_JSON, help="输出 census.json 路径")
    ap.add_argument("--vocab", default=VOCAB, help="vocab.json 路径(缺失则退回 master.json)")
    ap.add_argument("--no-offsets", action="store_true", help="不保留偏移样本(仅计数)")
    ap.add_argument("--sample", type=int, default=0, help="抽样 N 个命中打印上下文后退出")
    ap.add_argument("--verify", metavar="CENSUS_JSON", help="对已有 census.json 抽 3 码回读复现")
    ap.add_argument("--selftest", action="store_true", help="逻辑自检,不写产物")
    ap.add_argument("--seed", type=int, default=20241118)
    args = ap.parse_args()

    if not os.path.exists(args.exe):
        print(f"[err] exe 不存在: {args.exe}", file=sys.stderr)
        return 2
    if args.selftest:
        return cmd_selftest(args)
    if args.verify:
        return cmd_verify(args)
    if args.sample:
        return cmd_sample(args)

    t0 = time.time()
    with open(args.exe, "rb") as f:
        buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        sections = pe_sections(buf)
        per_form, per_code, density, sec_hits, per_sec_form, all_offsets = scan(
            buf, sections, want_offsets=not args.no_offsets)

        # 锚点自检
        anchor_rows = []
        anchor_ok = True
        for code, off, form in ANCHORS:
            e = per_code.get(code) or {}
            hits = sorted(e.get("offsets") or [])
            present = off in hits
            # 全扫里该码是否至少出现一次且形态相符
            form_hit = e.get(form, 0) > 0
            anchor_ok = anchor_ok and (code in per_code) and form_hit
            anchor_rows.append({
                "code": code, "expected_offset": off, "expected_form": form,
                "code_present": code in per_code, "form_present": form_hit,
                "offset_in_sample10": present,
                "offset_hits_count": (e.get(form, 0) or 0) if code in per_code else 0,
                "offsets_first10": hits[:10],
                "note": "" if present else "偏移不在前 10 样本内(需看全量偏移)",
            })
            print(f"[anchor] {code} @ {hex(off)}: present={code in per_code} "
                  f"form={form_hit} in_top10={present}", flush=True)

        entities, vmeta = load_vocab_entities(args.vocab)
        cov = entity_coverage(entities, per_code)
        all_codes = sorted({c for codes in entities.values() for c in codes})

        # 全 4CC(3009 词汇表)命中情况
        with open(vmeta["source"], encoding="utf-8") as f:
            vraw = json.load(f)
        all_vocab_codes = list(vraw.get("field_codes", {}).keys())
        vocab_hit = [c for c in all_vocab_codes if c in per_code]
        vocab_zero = [c for c in all_vocab_codes if c not in per_code]

        top_codes = sorted(per_code.items(), key=lambda kv: -kv[1]["total"])[:TOP_CODES]
        density_top = sorted(density.items(), key=lambda kv: -kv[1])[:20]
        total_hits = sum(v["total"] for v in per_code.values())

        out = {
            "meta": {
                "task": "t01-d editor.exe 4CC imm 形态普查",
                "exe": args.exe,
                "exe_size": os.path.getsize(args.exe),
                "forms": [{"name": f[0], "family": f[4], "imm_offset_in_match": f[3],
                           "pattern": f[2].pattern.decode("latin-1")} for f in FORMS],
                "byte_order": "imm32 按 4 字节反序即字段码 ASCII(如 6d 61 6e 63 -> cnam)",
                "charset": "[A-Za-z0-9]{4}",
                "window_bytes": WINDOW,
                "sample_cap_per_code": SAMPLE_CAP if not args.no_offsets else 0,
                "vocab": vmeta,
                "generated_unix": int(time.time()),
                "scan_seconds": round(time.time() - t0, 2),
                "offsets_are_file_offsets": True,
            },
            "totals": {
                "hits_alnum4cc": total_hits,
                "distinct_codes": len(per_code),
                "vocab_codes": len(all_vocab_codes),
                "vocab_codes_hit": len(vocab_hit),
                "vocab_codes_zero": len(vocab_zero),
            },
            "per_form_counts": per_form,
            "per_code": per_code,
            "per_code_top": [{"code": c, "total": v["total"],
                              "forms": {k: v[k] for k in v if k not in ("offsets", "total")}}
                             for c, v in top_codes],
            "entity_coverage": cov,
            "vocab_zero_hit_codes": vocab_zero,
            "density_top": [{"window_off": w, "count": n} for w, n in density_top],
            "density_windows_covered": len(density),
            "sections": {
                "pe_sections": [{"name": n, "raw_ptr": p, "raw_size": s} for n, p, s in sections],
                "hits_by_section": sec_hits,
                "hits_by_section_form": {f"{s}|{f}": n for (s, f), n in sorted(per_sec_form.items())},
            },
            "anchor_check": {"pass": anchor_ok, "rows": anchor_rows},
            "entity_codes_union": len(set(all_codes)),
        }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[out] {args.out} ({os.path.getsize(args.out)} bytes)")
    print(f"[summary] hits={total_hits} distinct={len(per_code)} "
          f"vocab_hit={len(vocab_hit)}/{len(all_vocab_codes)} anchors={'PASS' if anchor_ok else 'FAIL'}")
    return 0 if anchor_ok else 1


if __name__ == "__main__":
    sys.exit(main())
