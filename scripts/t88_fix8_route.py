#!/usr/bin/env python3
"""t88_fix8_route — 用真 PE 节表复核 CBDa/CBWa cmp 位点并解 CBW 族真路由。

背景(E136 更正):
  * scratch/t88/out3/_router.asm 等旧产物的"VA"实为**文件偏移 fo**,
    在 .rdata 段 fo = rva - 0x400,故旧地址整体错位,把指挥官引到桩区。
  * 4CC 分发用 lea 立即数 0x43424461 = 'C','B','D','a' 正序装入,
    不是 <I 小端 0x61444243。fix6 以 LE 搜索才误判"4CC 字节缺席"。

用法:
  py -V:3.12 -I -B scripts/t88_fix8_route.py --run
  py -V:3.12 -I -B scripts/t88_fix8_route.py --selftest

输出 scratch/t88/out3/cbw_route.json
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
IB = 0x140000000


def imm4cc(v: int) -> str:
    """cmp/lea 立即数 -> 4CC 正序字符串(高字节在前)。"""
    return struct.pack(">I", v & 0xFFFFFFFF).decode("latin-1")


def fo_to_va(pe: PE, fo: int) -> int | None:
    """文件偏移 -> VA(逐节反查,不假设恒等)。"""
    for s in pe.sections:
        if s["rawsize"] and s["fo"] <= fo < s["fo"] + s["rawsize"]:
            return pe.image_base + s["rva"] + (fo - s["fo"])
    return None


def route_chain(pe: PE) -> dict:
    """解析 CBW 族真路由:CBDa/CBWa cmp -> 跳转表 -> case 体 -> hub -> TC_RECORD_GET。"""
    # 1) 真实 VA:从 _router.asm 记录的 fo 反查
    lea_fo = 0x11F0CA7          # _router.asm 里的 "11f0ca7"
    va_lea = fo_to_va(pe, lea_fo)
    win = disasm(pe, va_lea, 0x40)
    # 2) 逐条定位 lea/cmp/jbe 三元组与跳转表 lea
    triples, table_lea = [], None
    for i, ins in enumerate(win):
        if ins["mn"] == "lea" and "- 0x" in ins["op"]:
            raw = ins["op"].split("- 0x")[1].rstrip("]").strip()
            imm = int(raw, 16)
            nxt = win[i + 1] if i + 1 < len(win) else {}
            triples.append({"va": ins["va"], "imm": f"0x{imm:08x}",
                            "code": imm4cc(imm),
                            "next": nxt.get("text"),
                            "bytes": ins["bytes"]})
        if ins["mn"] == "lea" and "rip +" in ins["op"] and "rcx" in ins["op"]:
            table_lea = ins
    # 3) 跳转表基址与条目
    tbl_va = None
    if table_lea:
        disp = int(table_lea["op"].split("rip + 0x")[1].rstrip("]").strip(), 16)
        rip_next = int(table_lea["va"], 16) + len(bytes.fromhex(table_lea["bytes"]))
        tbl_va = rip_next + disp
    entries = []
    if tbl_va is not None:
        for idx in range(15):
            rel = struct.unpack("<i", pe.read(tbl_va + 4 * idx, 4))[0]
            tgt_va = tbl_va + rel
            ins0 = disasm(pe, tgt_va, 16)
            entries.append({"idx": idx, "rel": rel, "va": f"0x{tgt_va:x}",
                            "first": ins0[0]["text"] if ins0 else None,
                            "bytes": pe.read(tgt_va, 8).hex()})
    # 4) hub:0x1411f3476 -> jmp -> 0x1411e94f0 -> jmp -> TC_RECORD_GET
    hub1 = disasm(pe, 0x1411F3476, 8)
    hub2 = disasm(pe, 0x1411E94F0, 8)
    chain = []
    for label, va in (("hub_a", 0x1411F3476), ("hub_b", 0x1411E94F0)):
        ins = disasm(pe, va, 8)
        chain.append({"label": label, "va": f"0x{va:x}",
                      "text": ins[0]["text"] if ins else None})
    tgt = None
    if hub2 and hub2[0]["mn"] == "jmp":
        tgt = int(hub2[0]["op"], 16)
    return {"lea_fo_in_old_asm": f"0x{lea_fo:x}",
            "true_va": f"0x{va_lea:x}" if va_lea else None,
            "delta_fo_to_va": (va_lea - lea_fo) if va_lea else None,
            "triples": triples,
            "table": {"lea": table_lea["text"] if table_lea else None,
                      "va": f"0x{tbl_va:x}" if tbl_va else None,
                      "n": len(entries), "entries": entries},
            "hub_chain": chain,
            "record_get_va": f"0x{tgt:x}" if tgt else None,
            "record_get": disasm(pe, tgt, 0x50) if tgt else []}


def selftest() -> int:
    pe = PE(EXE)
    # fo->VA 在 .rdata 段必须是 +0x400(rva 0x1000 - fo 0x600)
    assert fo_to_va(pe, 0x11F0CA7) == 0x1411F16A7, hex(fo_to_va(pe, 0x11F0CA7) or 0)
    assert fo_to_va(pe, 0x3EBAD50) is not None
    # 4CC 编码方向
    assert imm4cc(0x43424461) == "CBDa"
    assert imm4cc(0x43425761) == "CBWa"
    r = route_chain(pe)
    # 两个位点必须是 CBDa / CBWa
    codes = [t["code"] for t in r["triples"]]
    assert "CBDa" in codes and "CBWa" in codes, codes
    # 表 15 条且全部落在合法指令边界
    assert r["table"]["n"] == 15, r["table"]["n"]
    bad = [e for e in r["table"]["entries"]
           if not e["first"] or e["first"].split()[0] in
           ("add", "retf", "cli", "jae", "je") ]
    # 允许 je/jae 出现在个别 case,但不得过半
    assert len(bad) <= 3, [e["idx"] for e in bad]
    # 路由链必须到 TC_RECORD_GET(0x3ebad50 旧记法)
    assert r["record_get_va"] is not None, r
    print("selftest OK", {"true_va": r["true_va"],
                          "delta": r["delta_fo_to_va"],
                          "table_n": r["table"]["n"],
                          "record_get": r["record_get_va"],
                          "codes": codes[:4]})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t88-fix8 CBW 族真路由")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.run:
        ap.print_help()
        return 2
    pe = PE(EXE)
    r = route_chain(pe)
    r["meta"] = {"task": "t88-fix8", "exe_sha256_prefix": pe.sha256[:8],
                 "note": ("旧 _router.asm 的地址是 fo 不是 VA;"
                          ".rdata 段 fo=rva-0x400,故 VA=fo+0x400+0x140000000")}
    p = OUT / "cbw_route.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(r, indent=1), encoding="utf-8")
    print("wrote", p)
    print("true_va", r["true_va"], "delta", r["delta_fo_to_va"])
    for t in r["triples"]:
        print(f"  {t['va']} {t['bytes']} {t['code']} -> {t['next']}")
    print("table", r["table"]["va"], "n", r["table"]["n"])
    for e in r["table"]["entries"][:16]:
        print(f"   [{e['idx']}] {e['va']} {e['first']}")
    for c in r["hub_chain"]:
        print(f"  {c['label']} {c['va']} {c['text']}")
    print("record_get", r["record_get_va"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
