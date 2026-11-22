#!/usr/bin/env python3
"""t88_fix8_tags — 用 edx=4CC 值遍历 TC_RECORD_GET 的二叉搜索树,解出 tag -> (case 体, reader_off)。

TC_RECORD_GET 真身 = 0x1415446a0(旧记法 fo 0x15446a0;旧报告的 0x1543ca0 是错位地址)。
它按 edx(4CC 标签)做 cmp/jg/jle/je/jne 二分树,叶子处 mov dl,<rec_type> / add rax,<off>。

用法:
  py -V:3.12 -I -B scripts/t88_fix8_tags.py --run
  py -V:3.12 -I -B scripts/t88_fix8_tags.py --selftest
  py -V:3.12 -I -B scripts/t88_fix8_tags.py --trace ogls

输出 scratch/t88/out3/tag_dispatch.json
退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from t88_pe import PE, EXE, disasm  # noqa: E402

OUT = pathlib.Path("scratch/t88/out3")
RECGET = 0x1415446A0
SPAN = 0x800


def imm4cc(v: int) -> str:
    return struct.pack(">I", v & 0xFFFFFFFF).decode("latin-1")


def build_ins(pe: PE) -> tuple[dict, list]:
    """从 RECGET 起分块反汇编;遇不可解码处断开继续,覆盖整个函数区。"""
    ins = []
    start = RECGET
    end = RECGET + SPAN
    cur = start
    while cur < end:
        chunk = disasm(pe, cur, min(0x100, end - cur))
        if not chunk:
            cur += 0x10
            continue
        ins.extend(chunk)
        nxt = int(chunk[-1]["va"], 16) + len(bytes.fromhex(chunk[-1]["bytes"]))
        if nxt <= cur:
            cur += 0x10
        else:
            cur = nxt
    by_va = {int(i["va"], 16): i for i in ins}
    return by_va, ins


def trace(pe: PE, tag: str, max_steps: int = 200) -> dict:
    """线性扫描:定位 cmp edx,<tag> 及其紧邻 jcc,直接得出 case 体。

    jne <reject> : 不相等跳走 -> 命中体 = jcc 的下一条(顺序落入)
    je  <body>   : 相等跳走   -> 命中体 = 目标
    """
    by_va, ins = build_ins(pe)
    val = struct.unpack(">I", tag.encode("latin-1"))[0]
    for k, i in enumerate(ins):
        if i["mn"] != "cmp" or not i["op"].startswith("edx, 0x"):
            continue
        if int(i["op"].split(", ")[1], 16) != val:
            continue
        if k + 1 >= len(ins):
            return {"tag": tag, "hit": None, "status": "no_jcc", "path": []}
        j = ins[k + 1]
        if j["mn"] not in ("je", "jne", "jg", "jle", "jl", "ja", "jb"):
            return {"tag": tag, "hit": None, "status": "no_jcc", "path": []}
        fall = int(j["va"], 16) + len(bytes.fromhex(j["bytes"]))
        if j["mn"] == "jne":
            hit = fall          # 相等时不跳 -> 顺序落入 case 体
            kind = "fallthrough"
        elif j["mn"] == "je":
            hit = int(j["op"], 16)
            kind = "branch_target"
        else:
            return {"tag": tag, "hit": None, "status": "range_jcc",
                    "path": [{"va": i["va"], "text": i["text"]},
                             {"va": j["va"], "text": j["text"]}]}
        return {"tag": tag, "hit": f"0x{hit:x}", "status": "hit",
                "kind": kind,
                "path": [{"va": i["va"], "text": i["text"]},
                         {"va": j["va"], "text": j["text"]}]}
    return {"tag": tag, "hit": None, "status": "not_found", "path": []}


def parse_case(pe: PE, va: int) -> dict:
    """解析 case 体:rec_type(mov dl,X) + reader_off(add rax,X / [rdi+X])。"""
    body = disasm(pe, va, 0x40)
    out = {"va": f"0x{va:x}", "rec_type": None, "reader_off": None,
           "ins": [i["text"] for i in body[:6]]}
    for i in body[:8]:
        if i["mn"] == "mov" and i["op"].startswith("dl, 0x"):
            out["rec_type"] = int(i["op"].split(", ")[1], 16)
        if i["mn"] == "mov" and i["op"].startswith("add rax, 0x"):
            out["reader_off"] = int(i["op"].split(", ")[1], 16)
        if i["mn"] == "add" and i["op"].startswith("rax, 0x"):
            out["reader_off"] = int(i["op"].split(", ")[1], 16)
        # 变体:直接 [rdi + X] 读
        if i["mn"] == "movsx" or i["mn"] == "movzx" or i["mn"] == "mov":
            if "rdi + 0x" in i["op"] and out["reader_off"] is None:
                try:
                    out["reader_off"] = int(i["op"].split("rdi + 0x")[1].rstrip("]").strip(), 16)
                    out["reader_off_kind"] = "direct_field"
                except ValueError:
                    pass
    return out


def resolve_all(pe: PE) -> dict:
    by_va, ins = build_ins(pe)
    tags = []
    for i in ins:
        if i["mn"] == "cmp" and i["op"].startswith("edx, 0x"):
            v = int(i["op"].split(", ")[1], 16)
            tags.append(imm4cc(v))
    tags = sorted(set(tags))
    rows = []
    for t in tags:
        r = trace(pe, t)
        row = {"tag": t, "hit": r["hit"], "status": r["status"],
               "path_len": len(r["path"])}
        if r["hit"]:
            row["case"] = parse_case(pe, int(r["hit"], 16))
        rows.append(row)
    return {"recget_va": f"0x{RECGET:x}", "n_tags": len(rows), "tags": rows}


def selftest() -> int:
    pe = PE(EXE)
    assert imm4cc(0x6F676C73) == "ogls"
    r = resolve_all(pe)
    assert r["n_tags"] >= 20, r["n_tags"]
    m = {t["tag"]: t for t in r["tags"]}
    # 关键 tag 必须命中
    for t in ("ogls", "gols", "stdb", "stdt", "comp"):
        assert m[t]["status"] == "hit", (t, m[t]["status"])
    # ogls 的 case 必须是 rec_type 9(CBD)或 8(CBW) 家族之外 -> 检查 reader_off 非空
    assert m["ogls"]["case"]["reader_off"] is not None, m["ogls"]
    assert m["stdb"]["case"]["reader_off"] is not None, m["stdb"]
    print("selftest OK", {"n_tags": r["n_tags"],
                          "ogls": m["ogls"]["case"],
                          "stdb": m["stdb"]["case"]})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t88-fix8 TC_RECORD_GET tag 分发")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--trace")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    pe = PE(EXE)
    if a.trace:
        r = trace(pe, a.trace)
        print(json.dumps(r, indent=1)[:4000])
        return 0 if r["hit"] else 1
    if not a.run:
        ap.print_help()
        return 2
    r = resolve_all(pe)
    r["meta"] = {"task": "t88-fix8", "exe_sha256_prefix": pe.sha256[:8]}
    p = OUT / "tag_dispatch.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(r, indent=1), encoding="utf-8")
    print("wrote", p, "n_tags", r["n_tags"])
    for t in r["tags"]:
        c = t.get("case") or {}
        print(f"  {t['tag']} {t['status']:6s} rt={c.get('rec_type')} off={c.get('reader_off')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
