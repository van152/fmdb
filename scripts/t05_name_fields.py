"""t05_name_fields — 自动命名: 用 4CC getter 把 reader 布局挂上字段名。

完整链条(三段全部机械化):
    1) reader  : `lea rdx,[obj+OFF]` + `mov r8d,W` + `call [rax+0x28]`
                 -> (row_off, W, OFF)            [t05_reader_widths.py]
    2) 分发链  : `cmp edx, <4CC imm32>` + `je <target>`
                 -> (4CC, getter_target)
    3) getter  : `mov/movzx/movsx reg, [reg+OFF]`
                 -> (4CC, OFF, access_size)
    用 OFF 把 1) 与 3) 连接, 得到 (4CC, row_off, W)。

用法:
    py -V:3.12 -I -B scripts/t05_name_fields.py                # 全部实体
    py -V:3.12 -I -B scripts/t05_name_fields.py --type 6       # 详表
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "scratch/t05/layouts.json"
OUT = ROOT / "scratch/t05/named_fields.json"

# getter 分发链搜索窗口(相对 reader body)
DISPATCH_WINDOW = 0x6000
GETTER_BODY_BYTES = 72

ACCESS_SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8}

# 行缓冲成员访问:  getter `mov reg,[rdi+OFF]` / setter `mov [rsi+OFF],reg`
RE_MEM = re.compile(r"^(?:mov|movzx|movsx|movsxd|movss|movsd)\s+([a-z0-9]+),\s*(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\]$")
RE_MEM_ST = re.compile(r"^mov\s+(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\],\s*([a-z0-9]+)$")
RE_JE = re.compile(r"^j(?:e|z|ne|nz)\s+(0x[0-9a-f]+)$")

# 行缓冲/对象指针允许的寄存器(reader 里是 rsi/rdi/rcx/rbx)
BUF_REGS = {"rsi", "rdi", "rcx", "rbx", "rdx", "r12", "r13", "r14", "r15"}
# 合理的字段偏移范围(排除 0x8/0x10/0x28 这类容器或虚表偏移)
OFF_MIN, OFF_MAX = 0x20, 0x200


def is_4cc(v: int) -> bool:
    b = v.to_bytes(4, "little", signed=False)
    return all(32 <= c < 127 for c in b)


def code4cc(v: int) -> str:
    """imm32 -> 4CC 字符串(generator 里 cmp edx,0x49636470 表示 'Icdp')。"""
    return v.to_bytes(4, "little", signed=False)[::-1].decode("latin1")


def _mem_access(x):
    """从一条指令里抽出行缓冲成员访问 (OFF, size, kind)。"""
    text = x.mnemonic + " " + x.op_str
    m = RE_MEM.match(text)
    if m and m.group(3) in BUF_REGS:
        off = int(m.group(4), 16)
        if OFF_MIN <= off <= OFF_MAX:
            return off, ACCESS_SIZE.get(m.group(2) or "dword", 4), "read"
    m = RE_MEM_ST.match(text)
    if m and m.group(2) in BUF_REGS:
        off = int(m.group(3), 16)
        if OFF_MIN <= off <= OFF_MAX:
            return off, ACCESS_SIZE.get(m.group(1) or "dword", 4), "write"
    return None


def find_code_offsets(md, raw: bytes, pe, body_off: int,
                      window: int = DISPATCH_WINDOW):
    """在 reader body 之后找 4CC 分发/写入链, 返回 [{code, object_off, access_size, kind, ...}]。

    exe 里存在两条形态:
      getter: cmp edx,<4CC>; je  <tgt>   ... tgt: mov reg,[rdi+OFF]
      setter: cmp edx,<4CC>; jne <skip>  ...      mov [rsi+OFF],reg

    关键纪律: **下一个 `cmp <reg>,<4CC>` 是本段的硬边界**。
    早期版本用"向后扫 N 条"会在 getter 密集区串到相邻字段(实测 6 个不同 4CC
    全被解析成同一偏移 0x57), 故必须按段切分。
    """
    base_va = pe.f2va(body_off)
    if base_va is None:
        return []
    end = min(body_off + window, len(raw))
    ins = list(md.disasm(raw[body_off:end], base_va))

    # 先定位所有 4CC cmp, 作为段边界
    bounds: list[tuple[int, str, int]] = []      # (index, code, imm)
    for i, x in enumerate(ins):
        if x.mnemonic != "cmp":
            continue
        o = x.op_str.replace(" ", "")
        m = re.match(r"^([a-z0-9]+),0x([0-9a-f]+)$", o)
        if not m:
            continue
        val = int(m.group(2), 16)
        if 0 <= val <= 0xFFFFFFFF and is_4cc(val):
            bounds.append((i, code4cc(val), val))

    # 同一个 4CC 可能因二分查找/双链出现多次, 保留每次都参与匹配(去重留最优)
    out: list[dict] = []
    for k, (i, code, _imm) in enumerate(bounds):
        seg_end = bounds[k + 1][0] if k + 1 < len(bounds) else min(i + 20, len(ins))
        write_hit = read_hit = None
        for j in range(i + 1, seg_end):
            acc = _mem_access(ins[j])
            if not acc:
                continue
            off, size, kind = acc
            if kind == "write" and write_hit is None:
                write_hit = (off, size, hex(ins[j].address))
            elif kind == "read" and read_hit is None:
                read_hit = (off, size, hex(ins[j].address))
        # je/jne 目标块: 只取该块内第一条访问
        tgt_hit = None
        for j in range(i + 1, min(i + 3, len(ins))):
            jm = RE_JE.match(ins[j].mnemonic + " " + ins[j].op_str)
            if not jm:
                continue
            tgt_va = int(jm.group(1), 16)
            tgt_off = pe.va2f(tgt_va)
            if tgt_off is None:
                continue
            for y in md.disasm(raw[tgt_off:tgt_off + GETTER_BODY_BYTES], tgt_va):
                acc = _mem_access(y)
                if acc:
                    tgt_hit = (acc[0], acc[1], acc[2], hex(y.address))
                    break
                if y.mnemonic in ("ret", "jmp"):
                    break
            break
        # 优先级: 目标块直读 > 段内 write > 段内 read
        if tgt_hit:
            out.append({"code": code, "cmp_va": hex(ins[i].address),
                        "object_off": tgt_hit[0], "access_size": tgt_hit[1],
                        "kind": tgt_hit[2], "access_va": tgt_hit[3]})
        elif write_hit:
            out.append({"code": code, "cmp_va": hex(ins[i].address),
                        "object_off": write_hit[0], "access_size": write_hit[1],
                        "kind": "write", "access_va": write_hit[2]})
        elif read_hit:
            out.append({"code": code, "cmp_va": hex(ins[i].address),
                        "object_off": read_hit[0], "access_size": read_hit[1],
                        "kind": "read", "access_va": read_hit[2]})
    return out



def parse_getter(md, raw: bytes, pe, target_va: int):
    """在 getter 目标处找 `mov reg, [reg + OFF]`, 返回 (OFF, size)。"""
    off = pe.va2f(target_va)
    if off is None:
        return None
    ins = list(md.disasm(raw[off:off + GETTER_BODY_BYTES], target_va))
    for x in ins:
        if x.mnemonic not in ("mov", "movzx", "movsx", "movsxd", "movss", "movsd"):
            continue
        m = RE_MEM.match(x.mnemonic + " " + x.op_str)
        if not m:
            continue
        size = ACCESS_SIZE.get(m.group(2) or "dword", 4)
        return {"object_off": int(m.group(4), 16), "access_size": size,
                "va": hex(x.address), "insn": f"{x.mnemonic} {x.op_str}"}
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", type=int, default=None)
    ap.add_argument("--layouts", default=str(LAYOUTS))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    import importlib.util
    spec = importlib.util.spec_from_file_location("_pe", ROOT / "scripts/t05_pe.py")
    pm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm)
    pe = pm.default()

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    lay = json.loads(Path(args.layouts).read_text(encoding="utf-8"))

    # layouts.json 里的 fields 尚未带 object_off, 回读 reader_widths.json 补上
    rw = json.loads((ROOT / "scratch/t05/reader_widths.json").read_text(encoding="utf-8"))
    objmap = {}
    for r in rw["results"]:
        if r.get("reader") is None:
            continue
        objmap[r["type_id"]] = (r.get("obj_seq") or [], r.get("hits") or [])

    results = []
    for L in lay["layouts"]:
        bitfield_offsets: set[int] = set()
        tid = L["type_id"]
        if args.type is not None and tid != args.type:
            continue
        body = L.get("reader_body")
        if not body:
            continue
        body_off = int(body, 16)
        found = find_code_offsets(md, pe.raw, pe, body_off)
        if not found:
            results.append({"type_id": tid, "entity": L["entity"], "dispatch": 0,
                            "named": [], "note": "no 4CC dispatch chain found"})
            continue

        # 同一 4CC 可能多处出现: 优先 read(语义直读), 其次 write
        code2off: dict[str, dict] = {}
        for f in sorted(found, key=lambda z: 0 if z["kind"] == "read" else 1):
            code2off.setdefault(f["code"], f)
        obj2code: dict[int, str] = {}
        grouped: dict[int, list[str]] = {}
        for code, f in code2off.items():
            obj2code.setdefault(f["object_off"], code)
            grouped.setdefault(f["object_off"], []).append(code)

        # 位打包: 多个 4CC 共享同一 1 字节偏移 -> 该字节是 bitfield, 需按位拆分
        for off, codes in list(grouped.items()):
            sizes = {code2off[c]["access_size"] for c in codes}
            if len(codes) > 1 and sizes == {1}:
                bitfield_offsets.add(off)

        # 用 reader 的 obj_seq 连接
        obj_seq, hits = objmap.get(tid, ([], []))
        archives = {}
        for arch, v in L["archives"].items():
            # 找该 archive 对应的窗口, 取其 start 以对齐 obj_seq
            win = v.get("window") or [0, 0]
            start_i = win[0]
            named = []
            for f in v["fields"]:
                gi = start_i + f["idx"]
                oo = obj_seq[gi] if gi < len(obj_seq) else None
                code = obj2code.get(oo) if isinstance(oo, int) else None
                is_bit = isinstance(oo, int) and oo in bitfield_offsets
                named.append({
                    "idx": f["idx"], "row_off": f["row_off"], "width": f["width"],
                    "object_off": oo,
                    "code": None if is_bit else code,
                    "bitfield_candidates": sorted(grouped.get(oo, [])) if is_bit else None,
                    "confidence": ("bitfield_group" if is_bit
                                   else ("readpair" if code else "layout_only")),
                })
            archives[arch] = {"business_width": v["business_width"], "fields": named}

        n_named = sum(1 for a in archives.values() for f in a["fields"] if f["code"])
        n_bit = sum(1 for a in archives.values() for f in a["fields"]
                    if f.get("confidence") == "bitfield_group")
        results.append({"type_id": tid, "entity": L["entity"],
                        "reader_body": body, "dispatch": len(found),
                        "codes": sorted(code2off.keys()),
                        "named_count": n_named, "bitfield_slots": n_bit,
                        "archives": archives})

    Path(args.out).write_text(json.dumps({
        "note": "code 来自 exe 的 `cmp edx,<4CC>; je <getter>` 分发链, 由 getter 内 [reg+OFF] 与 "
                "reader 的 lea rdx,[obj+OFF] 同 OFF 连接。confidence=readpair 表示两侧指令均已核对。",
        "exe_sha256": pe.__class__ and __import__("hashlib").sha256(pe.raw).hexdigest(),
        "results": results,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    tot = sum(r.get("named_count", 0) for r in results)
    print(f"实体 {len(results)}, 命名字段合计 {tot}")
    print()
    for r in results:
        if args.type is not None:
            print(f"type {r['type_id']} {r['entity']} body={r.get('reader_body')} dispatch={r.get('dispatch')}")
            print(f"  codes({len(r.get('codes') or [])}): {r.get('codes')}")
            for arch, a in (r.get("archives") or {}).items():
                print(f"  [{arch}] {a['business_width']}B")
                for f in a["fields"]:
                    tag = f['code'] or ('|'.join(f.get('bitfield_candidates') or []) + ' [bitfield]'
                                        if f.get('confidence') == 'bitfield_group' else '?')
                    print(f"    row+{f['row_off']:<3} w={f['width']}  obj={f['object_off']}  {tag}")
            print()
        else:
            print(f"{r['type_id']:>4} {str(r['entity']):<12} dispatch={r.get('dispatch', 0):>3} "
                  f"codes={len(r.get('codes') or []):>3} named={r.get('named_count', 0):>3} "
                  f"bitfield={r.get('bitfield_slots', 0):>2}")
    print()
    print(f"写出 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
