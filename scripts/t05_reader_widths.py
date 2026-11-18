"""t05_reader_widths — 批量扫描每个实体的 reader 指令流宽度序列。

方法论(E20):
    行内布局 = reader 序列化指令流的宽度累加。
    每个 `mov r8d, N` 后紧跟 `call [rax+0x28]`(流写入), N 即该字段字节宽。
    顺序即行内顺序, 累加即偏移。

本工具:
  1. 从 census 取每个 type 的 slot19 reader 入口(63/74 可用)
  2. capstone 线性扫描 + 基本块分支标记, 配对 (宽度, call)
  3. 按"分支屏障"把序列切成若干连续段(对应互斥臂 / client-server 分叉)
  4. 与各表实际业务区宽度(client/server)比对, 找精确匹配的段

用法:
    py -V:3.12 -I -B scripts/t05_reader_widths.py            # 全实体扫描
    py -V:3.12 -I -B scripts/t05_reader_widths.py --type 6   # 单实体详表
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
CENSUS = ROOT / "scratch/t01/inbox/t01h/output.json"
COVERAGE = ROOT / "scratch/t05/COVERAGE.json"
OUT = ROOT / "scratch/t05/reader_widths.json"

BRANCH_MNEMONICS = {
    "jmp", "je", "jne", "jz", "jnz", "jbe", "ja", "jb", "jae", "js", "jns",
    "jl", "jg", "jle", "jge", "jo", "jno", "jp", "jnp", "jecxz", "jrcxz",
}
# 注意: test/cmp 只是为后续条件跳转准备, 不是控制流转移, 不能当屏障
SCAN_BYTES = 0x2000


def scan_reader(md, raw: bytes, start: int, size: int = SCAN_BYTES, max_hops: int = 8) -> dict:
    """扫描一个 reader 主体, 输出按地址顺序的 (宽度, call) 序列 + 分支位置。

    多数 census 入口是 `jmp <abs>` 跳板, 需走 PE 映射(不是简单减 delta)跟进到真身。
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("_pe", ROOT / "scripts/t05_pe.py")
    pe_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe_mod)
    pe = pe_mod.default()

    r = pe.resolve(start, max_hops=max_hops)
    cur = r["body"]
    chain = r["chain"]

    # 反汇编 base 必须是 VA, 否则 jmp 目标算错
    base_va = pe.f2va(cur) or cur

    items: list[tuple[str, int, object]] = []
    for ins in md.disasm(raw[cur:cur + size], base_va):
        m = ins.mnemonic
        o = ins.op_str.replace(" ", "")
        if m == "mov" and o.startswith("r8d,"):
            try:
                v = int(o.split(",")[-1], 0)
            except ValueError:
                v = None
            items.append(("W", ins.address, v))
        elif m == "lea" and o.startswith("rdx,"):
            # 对象内偏移: lea rdx, [reg + OFF]
            off = None
            if "+" in o:
                tail = o.split("+")[-1].rstrip("]")
                try:
                    off = int(tail, 0)
                except ValueError:
                    off = None
            items.append(("O", ins.address, off))
        elif m == "call" and "0x28]" in o:
            items.append(("C", ins.address, None))
        elif m in BRANCH_MNEMONICS:
            items.append(("B", ins.address, f"{m} {ins.op_str}"))
        elif m == "ret":
            items.append(("R", ins.address, None))

    calls: list[dict] = []
    cur_w: int | None = None
    cur_obj: int | None = None
    seq: list[int | None] = []
    obj_seq: list[int | None] = []
    barriers: list[int] = []
    pending_barrier = False
    for kind, addr, val in items:
        if kind == "W":
            cur_w = val
        elif kind == "O":
            cur_obj = val
        elif kind in ("B", "R"):
            pending_barrier = True
            cur_w = None
            cur_obj = None
        elif kind == "C":
            seq.append(cur_w)
            obj_seq.append(cur_obj)
            calls.append({"call_va": hex(addr), "width": cur_w, "object_off": cur_obj})
            barriers.append(1 if pending_barrier else 0)
            pending_barrier = False
            cur_w = None
            cur_obj = None

    segments: list[list[int | None]] = []
    cur_seg: list[int | None] = []
    for i, w in enumerate(seq):
        cur_seg.append(w)
        if barriers[i]:
            segments.append(cur_seg)
            cur_seg = []
    if cur_seg:
        segments.append(cur_seg)

    return {"calls": calls, "seq": seq, "obj_seq": obj_seq, "segments": segments,
            "body": hex(cur), "thunk_chain": [hex(x) for x in chain]}


def segment_sums(segments: list[list[int | None]]) -> list[dict]:
    out = []
    for i, seg in enumerate(segments):
        known = [w for w in seg if w is not None]
        out.append({
            "index": i,
            "fields": len(seg),
            "unknown": sum(1 for w in seg if w is None),
            "sum": sum(known),
            "widths": seg,
        })
    return out


def window_hits(seq: list[int | None], budget: int, max_unknown: int = 2) -> list[dict]:
    """在宽度序列上找连续子序列, 其和(忽略 unknown)接近 budget。

    返回按 |sum-budget| 升序的前若干个候选, 每个给出起止下标与字段数。
    """
    n = len(seq)
    hits = []
    for i in range(n):
        total = 0
        unknown = 0
        for j in range(i, n):
            w = seq[j]
            if w is None:
                unknown += 1
                if unknown > max_unknown:
                    break
            else:
                total += w
            if total > budget:
                break
            if abs(total - budget) <= unknown:      # unknown 各按 0..2B 计, 允许 ±1/个
                hits.append({
                    "start": i, "end": j, "fields": j - i + 1,
                    "sum": total, "unknown": unknown,
                    "widths": seq[i:j + 1],
                })
    hits.sort(key=lambda x: (abs(x["sum"] - budget) + x["unknown"], -x["fields"]))
    return hits[:6]


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", type=int, default=None, help="只详查某个 type_id")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    from capstone import CS_ARCH_X86, CS_MODE_64, Cs

    raw = EXE.read_bytes()
    md = Cs(CS_ARCH_X86, CS_MODE_64)

    census = (load_json(CENSUS) or {}).get("census") or []

    # 业务区宽度: 直接复用导出器的定长规格(唯一权威), 业务区 = 行宽 - 13B 身份尾
    budgets: dict[int, dict] = {}
    import importlib.util
    spec = importlib.util.spec_from_file_location("_dmp", ROOT / "scripts/fm24_dump.py")
    dmp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dmp)
    for (arch, tid), sp in dmp.fixed_specs().items():
        if sp.get("count", 0) < 2:
            continue
        budgets.setdefault(tid, {})[arch] = int(sp["stride"]) - 13

    results = []
    for it in sorted(census, key=lambda x: x["type_id"]):
        tid = it["type_id"]
        if args.type is not None and tid != args.type:
            continue
        rd = it.get("reader") or {}
        slot = (rd.get("slot19_readers") or [{}])[0]
        entry = slot.get("entry_file_offset")
        ent = it.get("entity") or {}
        name = (ent.get("matched") or ent.get("candidates") or ["?"])[0]
        if not entry:
            results.append({"type_id": tid, "entity": name, "reader": None,
                            "note": "no slot19 reader entry"})
            continue
        start = int(str(entry), 16)
        sc = scan_reader(md, raw, start)
        sums = segment_sums(sc["segments"])
        b = budgets.get(tid, {})
        hits = []
        for arch, want in b.items():
            for h in window_hits(sc["seq"], want):
                hits.append({"archive": arch, "want": want, **h})
        results.append({
            "type_id": tid,
            "entity": name,
            "mode": rd.get("mode"),
            "reader": hex(start),
            "body": sc.get("body"),
            "thunk_chain": sc.get("thunk_chain"),
            "calls": len(sc["calls"]),
            "seq": sc["seq"],
            "obj_seq": sc.get("obj_seq"),
            "segments": sums,
            "budgets": b,
            "hits": hits,
        })

    Path(args.out).write_text(json.dumps({"exe_sha256": __import__("hashlib").sha256(raw).hexdigest(),
                                          "results": results}, ensure_ascii=False, indent=1),
                              encoding="utf-8")

    if args.type is not None:
        for r in results:
            print(f"type {r['type_id']} entity={r['entity']} mode={r.get('mode')} reader={r.get('reader')}")
            print(f"  calls={r.get('calls')} budgets={r.get('budgets')}")
            print(f"  完整宽度序列: {r.get('seq')}")
            print(f"  和={sum(w for w in (r.get('seq') or []) if w)}  unknown={sum(1 for w in (r.get('seq') or []) if w is None)}")
            print(f"  窗口命中({len(r.get('hits') or [])}):")
            for h in r.get("hits") or []:
                print(f"    {h['archive']}: want={h['want']} -> sum={h['sum']} fields={h['fields']} "
                      f"unknown={h['unknown']} seq[{h['start']}:{h['end']+1}]={h['widths']}")
        return 0

    def ok(r):
        return any(h["sum"] == h["want"] and h["unknown"] == 0 for h in (r.get("hits") or []))

    nhit = sum(1 for r in results if ok(r))
    print(f"扫描 {len(results)} 个实体, 业务区宽度**精确命中**(unknown=0): {nhit}")
    print()
    print("type entity        mode          calls  命中(archive:want=sum/fields)")
    for r in results:
        if r.get("reader") is None:
            print(f"{r['type_id']:>4} {str(r['entity']):<13} {'-':<13} {'-':>5}  (无 reader)")
            continue
        exact = [h for h in (r.get("hits") or []) if h["sum"] == h["want"] and h["unknown"] == 0]
        hs = ", ".join(f"{h['archive']}:{h['want']}={h['sum']}/{h['fields']}f" for h in exact[:2]) if exact else ""
        print(f"{r['type_id']:>4} {str(r['entity']):<13} {str(r.get('mode'))[:13]:<13} "
              f"{r['calls']:>5}  {hs}")
    print()
    print(f"写出 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
