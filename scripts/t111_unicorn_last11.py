"""t111_unicorn_last11 — 攻克 Unicorn 剩余最后 11 张表（冲刺 79/79 全库闭合）.

在 t96c_unicorn_master 的真机微执行框架上修复四类根因，使最后 11 对失败表闭合：

  R1  DB-context 全局单例未初始化：AWARD(t0×2)/STARTING_PAST_TRADE(t72) 的 slot19 辅助函数
      (sub_140F92AB0 等) 解引用 [qword_141B5FDC8/DD0/E00/FE10] 处的 ctx，再取 [ctx+0x80] 的
      ID→对象向量；模拟器中为 NULL → UC_ERR_READ addr=0x80 (0x140f92cc4 / 0x140f83b02)。
      修复：四个 .sbss 全局指向 db_a3 页 (+0x80 = {0,0,0} 空向量，cmp/jbe 越界即跳过解析)。
  R2  模式版本全局 0x141B60330/32/34 未初始化：STARTING_PAST_TRANSFER(t71) /
      STARTING_FUTURE_TRANSFER(t32) 等组读取器 (sub_1411919D0 家族) 用
      `movzx eax, word [rip+..]; cmp eax, 0xDDD` 分派新旧字段布局；为 0 时走旧布局，
      每组漏读 11 字节 (this+0x81/0x82/0x60 三字段) → 行边界错位 → t71 row9 的
      2 字节 count 读到 0xBA81，movsx 符号扩展为负 → vector::_Xlength_error
      (0x141d193f0 → msvcp140!_Xlength_error)；t32 则越过 footer (diff=-8)。
      修复：按表头版本 0x0DF1 写入三个全局。
  R3  行上下文 ctx (R9，版本在 +0x588) 与工厂对象由 bump 堆分配，会被 CLUB 等表的
      62 KB 级 this+0xC0 blob 读覆写 → 解析路径随堆布局漂移（t96c 原跑 flaky 的根源，
      t3/t36/t41/t45/t48 属此类）。修复：OBJ/CTX 专用隔离区，每行清零，blob 永不出槽。
  R4  行切片含 9 字节 footer，整表读者读穿 footer（t32 diff=-8）。修复：切片止于 footer_off。
  R5  内部堆回退分配器 (0x1412d31c0 → 0x144104200，mimalloc 式) 的堆上下文全局在模拟器
      中未初始化 → `div r15` 除零 (t72 typed-vector 元素循环)。修复：UC_HOOK_CODE 拦截
      入口，按 r8d 尺寸改走 emu._alloc 弹性分配并伪造 ret。
  R6  t72 (STARTING_PAST_TRADE) 专用流配置：真实运行期为每条流设置标志位与配置全局 —
      [stream+0xC] bit1=2 (ID 引用后不读可选 1B 标记、datetime/ID 字段定长)，
      byte_141B60352=1 (跳过参数门控)、byte_141B5FC2C=1 (datetime 4B 定长)、
      byte_141B55C2C=1 (元素 +8 处 ID 4B)。15B/元素布局经 wire 语义验证
      (elem+0x10 = 年份 u16，默认 0x76C=1900，实测 2024/2025)。另要求 slot19
      返回 rax==1 才判行成功 (strict_rax)。

用法:
  py -V:3.12 -B scripts/t111_unicorn_last11.py --selftest
  py -V:3.12 -B scripts/t111_unicorn_last11.py --last11     # 仅 11 对目标表 + 交付物
  py -V:3.12 -B scripts/t111_unicorn_last11.py              # 全库 79 对 sweep + 交付物
  py -V:3.12 -B scripts/t111_unicorn_last11.py --only server/3,client/0
退出码: 0 全部干净, 1 有失败(partial), 2 fatal。
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

OUT_DIR = ROOT / "scratch/t111/out"

# ---- 修复参数 (见模块 docstring R1/R2) ----
# DBCTX_GLOBALS: 全镜像字节码扫描 `mov r,[rip+d]` → `mov r,[r+0x80]` 得到的
# dbctx 单例家族 (0x141B5FDB0-0x141B5FE60 簇 + 0x141BF7E10).
# 0x141B5FDC0 (44 处引用) 即 server/t0 行 3301 崩溃点 0x140f80f87.
DBCTX_GLOBALS = [
    0x141B5FDB0, 0x141B5FDB8, 0x141B5FDC0, 0x141B5FDC8, 0x141B5FDD0,
    0x141B5FDE0, 0x141B5FDE8, 0x141B5FDF0, 0x141B5FDF8,
    0x141B5FE00, 0x141B5FE08, 0x141B5FE10,
    0x141B5FE20, 0x141B5FE28, 0x141B5FE30, 0x141B5FE40,
    0x141B5FE48, 0x141B5FE58, 0x141B5FE60, 0x141BF7E10,
]
VER_GLOBALS = [0x141B60330, 0x141B60332, 0x141B60334]

# ---- 隔离区 (R3): 与 t95 已映射区间互不相交 ----
OBJ_BASE = 0x0000_0006_0000_0000   # 工厂对象槽, 1 MB/槽, 16 槽轮转
OBJ_SLOT = 0x0010_0000
OBJ_ZERO = 0x0001_0000             # 每槽清零前 64 KB (覆盖 62 KB blob)
OBJ_SLOTS = 16
CTX_BASE = 0x0000_0007_0000_0000   # 行上下文槽, 16 KB/槽, 64 槽轮转
CTX_SLOT = 0x0000_4000
CTX_ZERO = 0x0000_4000
CTX_SLOTS = 64

# R5: 游戏内部堆回退分配器入口 (0x1412d31c0 → 0x144104200, 上下文全局未初始化)
FALLBACK_ALLOC_ENTRY = 0x1412D31C0

# R7: 非 LAST11 表的 dbctx 作用域回退. R1 把整个 20 元素家族设为 db_a3 指针,
# 但部分 deref 位点带 `test rcx,rcx; jz` 空检查: 全局为 NULL 时走"跳过"分支,
# 为指针(空向量)时走进查找分支 → 行为不同 → server/t24 (NATIONAL_TEAM) 行 5
# 解析错位 (基线 t96c 用 3 全局集 50/50 通过). 对这类表恢复 t96c 最小集.
TABLE_OVERRIDES = {
    ("server", 24): dict(dbctx_only=[0x141B5FDB8, 0x141B5FE08, 0x141B5FE40]),
}

# ---- 最后 11 对表的运行配置 ----
# full=True → 整表跑到 footer; sample=N → 只跑前 N 行 (N==nrows 时仍判闭合)
# stream_flags: 逐行写入 [stream+0xC]; extra_globals: 追加的运行期配置全局;
# strict_rax: 行成功还需 slot19 返回 rax==1
LAST11 = {
    ("server", 0): dict(full=True),    # AWARD 3,545
    ("client", 0): dict(full=True),    # AWARD 3,545
    ("server", 3): dict(sample=200),   # CLUB 84,259 (整表过慢, 前 200 行零异常)
    ("client", 3): dict(sample=200),   # CLUB 84,259
    ("server", 32): dict(full=True),   # STARTING_FUTURE_TRANSFER 315 → 闭合
    ("server", 36): dict(sample=200),  # STARTING_MANAGER_HOF_RECORD 6,535
    ("server", 41): dict(full=True),   # CURRENCY_RECORD 173 → 闭合
    ("server", 45): dict(sample=200),  # STARTING_RECORD 84,477
    ("server", 48): dict(full=True),   # STARTING_RECORD 5,210 → 闭合
    ("server", 71): dict(sample=50),   # STARTING_PAST_TRANSFER 616,665
    ("server", 72): dict(              # STARTING_PAST_TRADE 138 → 闭合 (R5/R6)
        full=True, stream_flags=2, strict_rax=True, heap_hook=True,
        extra_globals={0x141B60352: 1, 0x141B5FC2C: 1, 0x141B55C2C: 1},
    ),
}
LAST11_BASELINE = {  # t96c 基线 (scratch/t96c/out/REPORT.md)
    ("server", 0): "FAIL 1/3545 row 1 flag=0xc8 rip=0x140f92cc4 addr=0x80",
    ("client", 0): "FAIL 1/3545 row 1 flag=0xc8 rip=0x140f92cc4 addr=0x80",
    ("server", 3): "FAIL 3/84259 row 3 huge_read n=104418048 rip=0x14371be8d",
    ("client", 3): "FAIL 12/84259 row 12 flag=0x4d huge_read rip=0x14371be8d",
    ("server", 32): "FAIL 1/315 row 1 pos 19111 >= footer 19103 (diff=-8)",
    ("server", 36): "FAIL 1/6535 row 1 consumed=18 UC_ERR_READ_UNMAPPED rip=0x14371bf6e",
    ("server", 41): "FAIL 0/173 row 0 consumed=16 UC_ERR_READ_UNMAPPED rip=0x14371bf6e",
    ("server", 45): "FAIL 0/84477 row 0 consumed=55 UC_ERR_READ_UNMAPPED rip=0x14371bf6e",
    ("server", 48): "FAIL 3/5210 row 3 consumed=55 UC_ERR_READ_UNMAPPED rip=0x14371bf6e",
    ("server", 71): "FAIL 9/616665 row 9 consumed=29393 _Xlength_error rip=0x141d19401",
    ("server", 72): "FAIL 0/138 row 0 rip=0x140f83b02 addr=0x80",
}


def setup_emulator_v2(heap_hook: bool = False):
    """t96c 框架 + R1/R3 修复. heap_hook=True 时启用 R5 分配器拦截 (有每指令开销).
    返回 (ut, emu, db_a3_ptr)."""
    import t96c_unicorn_master as M

    ut, emu, db_a3 = M.setup_emulator()
    emu.mu.mem_map(OBJ_BASE, OBJ_SLOT * OBJ_SLOTS)
    emu.mu.mem_map(CTX_BASE, CTX_SLOT * CTX_SLOTS)
    emu._obj_bump = 0
    emu._ctx_bump = 0
    emu._alloc_mode = "heap"

    orig_alloc = emu._alloc

    def alloc_v2(size, caller=0):
        mode = getattr(emu, "_alloc_mode", "heap")
        if mode == "obj":
            slot = OBJ_BASE + emu._obj_bump
            emu._obj_bump = (emu._obj_bump + OBJ_SLOT) % (OBJ_SLOT * OBJ_SLOTS)
            emu.mu.mem_write(slot, b"\x00" * OBJ_ZERO)
            emu.heap_ptr = slot + size
            return slot
        if mode == "ctx":
            slot = CTX_BASE + emu._ctx_bump
            emu._ctx_bump = (emu._ctx_bump + CTX_SLOT) % (CTX_SLOT * CTX_SLOTS)
            emu.mu.mem_write(slot, b"\x00" * CTX_ZERO)
            emu._ctx_addr = slot
            return slot
        return orig_alloc(size, caller)

    emu._alloc = alloc_v2

    # R1: DB-context 全局 → db_a3 页 ([+0x80] = 空向量, ID 解析越界即跳过)
    for g in DBCTX_GLOBALS:
        emu.mu.mem_write(g, struct.pack("<Q", db_a3))
    emu._db_a3 = db_a3

    # R5: 内部堆回退分配器 0x1412d31c0 (mimalloc 式, 上下文全局未初始化 → div/0)
    #     拦截入口改走 emu._alloc 弹性分配. 仅需该路径的表 (t72) 才启用 (有每指令开销).
    if heap_hook:
        from unicorn import UC_HOOK_CODE  # noqa: E402
        import unicorn.x86_const as XC  # noqa: E402

        def on_heap_alloc(uc, address, size, ud):
            sz = uc.reg_read(XC.UC_X86_REG_R8)
            rsp = uc.reg_read(XC.UC_X86_REG_RSP)
            ret = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
            ptr = alloc_v2(max(sz, 16), address)
            uc.reg_write(XC.UC_X86_REG_RAX, ptr)
            uc.reg_write(XC.UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(XC.UC_X86_REG_RIP, ret)

        emu.mu.hook_add(UC_HOOK_CODE, on_heap_alloc, begin=FALLBACK_ALLOC_ENTRY, end=FALLBACK_ALLOC_ENTRY)
    return ut, emu, db_a3


def set_version_globals(emu, ver: int):
    """R2: 模式版本全局 (0x141B60330/32/34) ← 表头版本."""
    for g in VER_GLOBALS:
        emu.mu.mem_write(g, struct.pack("<H", ver))


def construct_v2(ut, emu, tid: int, flag: int):
    """工厂构造 (对象落 OBJ 槽); 失败时回退零初始化 THIS_BASE + fallback slot19."""
    emu.heap_ptr = ut.HEAP_BASE
    emu.unhandled_calls = []
    emu.heap_allocs = []
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], tid)
    emu.mu.reg_write(emu.REG["RDX"], flag)
    emu._alloc_mode = "obj"
    try:
        emu.mu.emu_start(0x140F49530, ut.STOP_ADDR, count=300_000)
    except Exception:
        emu._alloc_mode = "heap"
        return 0, 0, 0
    emu._alloc_mode = "heap"
    obj = emu.mu.reg_read(emu.REG["RAX"])
    if obj == 0:
        return 0, 0, 0
    vt = struct.unpack("<Q", bytes(emu.mu.mem_read(obj, 8)))[0]
    if not (0x140000000 <= vt < 0x145000000):
        return obj, vt, 0
    s19 = struct.unpack("<Q", bytes(emu.mu.mem_read(vt + 19 * 8, 8)))[0]
    return obj, vt, s19


def run_row_v2(ut, emu, obj, s19, row_slice, ver, a7, a3_ptr=0, stream_flags=0):
    """执行一次 slot19; ctx 落 CTX 槽 (+0x588=ver), 切片由调用方给出 (R4)."""
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x0C, struct.pack("<I", stream_flags))
    emu.payload = row_slice
    emu.wire_pos = 0
    emu.reads = []
    emu.unhandled_calls = []

    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu._alloc_mode = "ctx"
    ctx_ptr = emu._alloc(0x2000)
    emu._alloc_mode = "heap"
    emu.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", ver))
    emu.mu.mem_write(rsp + 0x00, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.mem_write(rsp + 0x28, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x30, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x38, struct.pack("<Q", a7))
    emu.mu.mem_write(rsp + 0x40, struct.pack("<Q", 0))

    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], obj)
    emu.mu.reg_write(emu.REG["RDX"], ut.STREAM_PTR_ADDR)
    emu.mu.reg_write(emu.REG["R8"], a3_ptr)
    emu.mu.reg_write(emu.REG["R9"], ctx_ptr)

    err = None
    try:
        # R4 整行切片后大行 (t24 行5 = 229,813B 内层循环 ~40M 指令) 需要高上限;
        # 3M 上限会把这类行误判 timeout (t96c 的 64KB 定长切片恰好截断了大行)
        emu.mu.emu_start(s19, ut.STOP_ADDR, count=200_000_000)
    except Exception as exc:
        err = str(exc)
    rip = emu.mu.reg_read(emu.REG["RIP"])
    rax = emu.mu.reg_read(emu.REG["RAX"])
    ok = err is None and rip == ut.STOP_ADDR and emu.wire_pos > 0
    return {
        "ok": ok,
        "rax": rax,
        "error": err if err else (None if ok else "timeout_or_no_progress"),
        "end_rip": hex(rip),
        "bytes_consumed": emu.wire_pos,
        "reads": emu.reads,
        "unhandled": emu.unhandled_calls[:5],
    }


def load_all_numbered_tables():
    import t96c_unicorn_master as M
    return M.load_all_numbered_tables()


def load_vtable_fallback():
    import t96c_unicorn_master as M
    return M.load_vtable_fallback()


def aggregate_canonical(row_reads_samples):
    import t96c_unicorn_master as M
    return M.aggregate_canonical(row_reads_samples)


def trace_table_v2(ut, emu, vt_fallback, arch, tid, payload, full_limit=1500, sample_rows=50, force=None):
    """单表追踪 (fresh emulator 已含 R1-R3 修复; 切片止于 footer, R4)."""
    a7 = 1 if arch == "server" else 0
    cls_name, fb_s19 = vt_fallback.get(tid, (f"TT{tid}", 0))
    ver = struct.unpack_from("<H", payload, 6)[0]
    nrows = struct.unpack_from("<I", payload, 8)[0]
    footer_off = len(payload) - 9
    set_version_globals(emu, ver)
    stream_flags = force.get("stream_flags", 0) if force else 0
    strict_rax = bool(force.get("strict_rax")) if force else False
    if force and force.get("extra_globals"):
        for g, v in force["extra_globals"].items():
            emu.mu.mem_write(g, struct.pack("<B", v))
    if force and force.get("dbctx_only") is not None:
        # R7: 恢复该表的最小 dbctx 集 (其余家族成员回零 = 空检查走跳过分支)
        for g in DBCTX_GLOBALS:
            emu.mu.mem_write(g, struct.pack("<Q", 0))
        for g in force["dbctx_only"]:
            emu.mu.mem_write(g, struct.pack("<Q", emu._db_a3))

    if force and force.get("full"):
        rows_target = nrows
    elif force and force.get("sample"):
        rows_target = min(force["sample"], nrows)
    else:
        rows_target = nrows if nrows <= full_limit else sample_rows

    rec = {
        "archive": arch,
        "table_id": tid,
        "class": cls_name,
        "a7": a7,
        "version": hex(ver),
        "payload_size": len(payload),
        "footer_off": footer_off,
        "rows_header": nrows,
        "rows_target": rows_target,
        "rows_ok": 0,
        "closed_to_footer": False,
        "end_pos": 13,
        "diff_bytes": footer_off - 13,
        "flags_seen": {},
        "vtables_seen": [],
        "row_len_min": None,
        "row_len_max": None,
        "unique_row_lens": 0,
        "error": None,
        "row0_reads": [],
        "canonical_fields": [],
    }
    if nrows == 0:
        rec["closed_to_footer"] = (13 == footer_off)
        rec["diff_bytes"] = footer_off - 13
        return rec

    pos = 13
    flags_cnt: Counter[int] = Counter()
    vts_seen = set()
    row_lens = []
    samples = []
    limit = rows_target

    for r in range(limit):
        if pos >= footer_off:
            rec["error"] = f"row {r}: pos {pos} >= footer {footer_off}"
            break
        flag = payload[pos]
        pos += 1
        flags_cnt[flag] += 1

        obj, vt, s19 = construct_v2(ut, emu, tid, flag)
        if s19 == 0:
            # 回退: 零初始化 THIS_BASE + fallback slot19 (保底, 同 t96c)
            emu.mu.mem_write(ut.THIS_BASE, b"\x00" * 0x4000)
            obj, s19 = ut.THIS_BASE, fb_s19
            vts_seen.add(f"fallback:{hex(s19)}")
        else:
            vts_seen.add(f"{hex(vt)}->{hex(s19)}")

        res = run_row_v2(ut, emu, obj, s19, payload[pos:footer_off], ver, a7, stream_flags=stream_flags)
        row_ok = res["ok"] and (not strict_rax or res.get("rax") == 1)
        if not row_ok:
            rec["error"] = (
                f"row {r} flag={flag:#x} s19={hex(s19)} consumed={res['bytes_consumed']} "
                f"err={res['error']} rip={res['end_rip']} rax={res.get('rax', 0):#x} un={res['unhandled'][:1]}"
            )
            break

        pos += res["bytes_consumed"]
        row_lens.append(res["bytes_consumed"])
        rec["rows_ok"] += 1
        if r == 0:
            rec["row0_reads"] = res["reads"]
        if r < 20:
            samples.append(res["reads"])

    rec["end_pos"] = pos
    rec["diff_bytes"] = footer_off - pos
    rec["closed_to_footer"] = (rec["rows_ok"] == nrows and pos == footer_off)
    rec["flags_seen"] = {hex(k): v for k, v in sorted(flags_cnt.items())}
    rec["vtables_seen"] = sorted(vts_seen)
    if row_lens:
        rec["row_len_min"] = min(row_lens)
        rec["row_len_max"] = max(row_lens)
        rec["unique_row_lens"] = len(set(row_lens))
    rec["canonical_fields"] = aggregate_canonical(samples)
    return rec


def status_of(rec):
    if rec["closed_to_footer"]:
        return "CLOSED"
    if rec["rows_ok"] == rec["rows_target"] and rec["rows_ok"] > 0:
        return "OK_SAMPLE"
    return "FAIL"


def run_sweep(pairs=None, full_limit=1500, sample_rows=50):
    """跑 (部分或全部) 79 对表. 每对表独立 fresh emulator (R3 隔离态)."""
    vt_fallback = load_vtable_fallback()
    tables = load_all_numbered_tables()
    results = []
    t0 = time.time()
    for arch, tid, payload in tables:
        if pairs is not None and (arch, tid) not in pairs:
            continue
        force = dict(LAST11.get((arch, tid)) or {})
        force.update(TABLE_OVERRIDES.get((arch, tid), {}))
        ut, emu, db_a3 = setup_emulator_v2(heap_hook=bool(force and force.get("heap_hook")))
        rec = trace_table_v2(ut, emu, vt_fallback, arch, tid, payload, full_limit, sample_rows, force)
        results.append(rec)
        tag = status_of(rec)
        print(
            f"{arch:6s}/t{tid:<2d} {rec['class'][:30]:30s} {tag:9s} rows={rec['rows_ok']:5d}/{rec['rows_header']:<6d} "
            f"diff={rec['diff_bytes']:9d} fields={len(rec['canonical_fields']):3d} "
            f"({time.time()-t0:6.1f}s) {rec['error'] or ''}",
            flush=True,
        )
    return results, time.time() - t0


def write_deliverables(results, elapsed):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_key = {(r["archive"], r["table_id"]): r for r in results}

    n_closed = sum(1 for r in results if r["closed_to_footer"])
    n_sample = sum(1 for r in results if not r["closed_to_footer"] and status_of(r) == "OK_SAMPLE")
    n_fail = len(results) - n_closed - n_sample

    master = {
        "status": "complete" if n_fail == 0 else "partial",
        "elapsed_sec": round(elapsed, 1),
        "total_archive_tables": len(results),
        "closed_to_footer": n_closed,
        "sample_rows_all_ok": n_sample,
        "failed": n_fail,
        "fixes": {
            "R1_dbctx_globals": [hex(g) for g in DBCTX_GLOBALS],
            "R2_version_globals": [hex(g) for g in VER_GLOBALS],
            "R3_isolated_obj_ctx_arenas": True,
            "R4_footer_bounded_slice": True,
        },
        "tables": results,
    }
    (OUT_DIR / "wire_traces_t111.json").write_text(
        json.dumps(master, indent=1, ensure_ascii=False), encoding="utf-8")

    last11_keys = list(LAST11.keys())
    last11 = []
    for k in last11_keys:
        r = by_key.get(k)
        if r is None:
            continue
        last11.append({
            "pair": f"{k[0]}/t{k[1]}",
            "class": r["class"],
            "baseline_t96c": LAST11_BASELINE[k],
            "after_t111": {
                "status": status_of(r),
                "rows_ok": r["rows_ok"],
                "rows_header": r["rows_header"],
                "rows_target": r["rows_target"],
                "end_pos": r["end_pos"],
                "footer_off": r["footer_off"],
                "diff_bytes": r["diff_bytes"],
                "closed_to_footer": r["closed_to_footer"],
                "unique_row_lens": r["unique_row_lens"],
                "row_len_min": r["row_len_min"],
                "row_len_max": r["row_len_max"],
                "error": r["error"],
                "canonical_fields_count": len(r["canonical_fields"]),
            },
            "row0_reads": r["row0_reads"][:64],
            "canonical_fields": r["canonical_fields"],
            "flags_seen": r["flags_seen"],
            "vtables_seen": r["vtables_seen"],
        })
    last11_clean = sum(1 for e in last11 if e["after_t111"]["status"] != "FAIL")
    last11_json = {
        "status": "complete" if last11_clean == len(last11) else "partial",
        "fixes_applied": master["fixes"],
        "root_causes": {
            "R1": "AWARD(t0×2)/t72 等 slot19 辅助函数解引用未初始化 .sbss dbctx 单例家族 (0x141B5FDB0-0x141B5FE60 簇 + 0x141BF7E10, 共 20 个; 全镜像扫描 `mov r,[rip+d]→mov r,[r+0x80]` 得到; 0x141B5FDC0 有 44 处引用) 再取 [ctx+0x80] ID→对象向量 → addr=0x80 读失败 (0x140f92cc4 / 0x140f83b02 / 0x140f80f87)。修复=全部指向 db_a3 页 ([+0x80]={0,0,0} 空向量, cmp/jbe 越界即跳过)",
            "R2": "STARTING_PAST_TRANSFER(t71)/STARTING_FUTURE_TRANSFER(t32): 组读取器 sub_1411919D0 按 .sbss 版本全局 0x141B60330 (cmp 0xDDD) 分派字段布局, 未初始化=0 走旧布局每组漏读 11B (this+0x81/0x82/0x60) → 行边界错位 → t71 row9 count=0xBA81 movsx 负数 → vector::_Xlength_error (0x141d193f0→0x141d19401); t32 越过 footer (diff=-8)。修复=按表头 0x0DF1 写入 0x141B60330/32/34",
            "R3": "t3/t36/t41/t45/t48 (t96c 原跑 flaky): 行 ctx (+0x588 版本) 与工厂对象位于 bump 堆, 被 CLUB 62KB 级 this+0xC0 blob 读覆写 → 版本漂移引发 huge_read(0x14371be86)/写崩(0x14371be8d)/interner 崩(0x14371bf6e)。修复=OBJ/CTX 专用隔离区+每行清零",
            "R4": "行切片含 9B footer → 整表读者读穿 footer (t32 diff=-8)。修复=切片止于 footer_off",
            "R5": "t72 typed-vector 元素循环的内部堆回退分配器 (0x1412d31c0→0x144104200, mimalloc 式) 堆上下文全局未初始化 → `div r15` 除零。修复=UC_HOOK_CODE 拦截入口按 r8d 尺寸走 emu._alloc 并伪造 ret",
            "R6": "t72 流配置: 真实运行期 [stream+0xC] bit1=2 (ID 引用后不读可选 1B; datetime/ID 定长) + byte_141B60352/141B5FC2C/141B55C2C=1 → 元素定长 15B (elem+0x10=年份 u16, 默认 1900, 实测 2024/2025 语义吻合); 138/138 行 rax==1, diff==0 闭合",
            "R7": "dbctx 家族作用域 (R1 副作用): 部分 deref 位点带 `test rcx,rcx; jz` 空检查 — 全局为 NULL 走跳过分支, 为指针(空向量)走查找分支, 两者行行为不同 → server/t24 NATIONAL_TEAM 行 5 解析错位 (t96c 基线 3 全局集 50/50). 修复=TABLE_OVERRIDES 按表恢复 t96c 最小集",
        },
        "tables": last11,
    }
    (OUT_DIR / "last11_traces.json").write_text(
        json.dumps(last11_json, indent=1, ensure_ascii=False), encoding="utf-8")

    # REPORT.md
    n_clean = n_closed + n_sample
    lines = [
        "# t111 — Unicorn 最后 11 张表修复报告 (冲刺 79/79)",
        "",
        f"- 耗时: `{master['elapsed_sec']}s` | 本轮结果: **整表 `diff==0` 闭合 {n_closed}** | 大表样本干净 {n_sample} | 失败 {n_fail} / 共 {len(results)} 对",
        f"- **总进度: t96c 基线 68/79 干净 (41 CLOSED + 27 OK_SAMPLE + 11 FAIL) → t111 {n_clean}/79 干净 ({n_closed} CLOSED + {n_sample} OK_SAMPLE + {n_fail} FAIL)**",
        f"- 修复根因: **R1** dbctx 全局家族 (0x141B5FDB0-FE60 簇 + 0x141BF7E10 ← db_a3 空向量页) · **R2** 版本全局 (0x141B60330/32/34 ← 0x0DF1) · **R3** OBJ/CTX 隔离区 (ctx+0x588 不再被 blob 覆写) · **R4** 行切片止于 footer · **R5** 内部堆回退分配器拦截 (t72 div/0) · **R6** t72 流标志 bit1 + 配置全局 (15B 元素布局)",
        "",
        "## 11 对目标表 修复前后对比",
        "",
        "| pair | class | t96c 基线 | t111 结果 | rows | diff | 根因 |",
        "|---|---|---|---|---|---:|---|",
    ]
    for e in last11:
        arch = e["pair"].split("/")[0]
        tid = int(e["pair"].split("/t")[1])
        r = by_key[(arch, tid)]
        tag = status_of(r)
        if (arch, tid) == ("server", 72):
            rc = "R1+R5+R6"
        elif (arch, tid) in (("server", 0), ("client", 0)):
            rc = "R1"
        elif (arch, tid) in (("server", 32), ("server", 71)):
            rc = "R2+R4"
        elif (arch, tid) in (("server", 3), ("client", 3)):
            rc = "R3"
        else:
            rc = "R3"
        rows = f"{r['rows_ok']}/{r['rows_header']}"
        if r["rows_target"] != r["rows_header"]:
            rows += f" (target {r['rows_target']})"
        lines.append(
            f"| {e['pair']} | `{r['class']}` | {e['baseline_t96c']} | **{tag}** | {rows} | {r['diff_bytes']} | {rc} |"
        )
    lines += [
        "",
        "## 全表结果 (本轮)",
        "",
        "| archive | tt | class | 状态 | rows_ok/total | diff | uniq_lens | fields | 备注 |",
        "|---|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for r in results:
        tag = status_of(r)
        lines.append(
            f"| {r['archive']} | {r['table_id']} | `{r['class']}` | **{tag}** | "
            f"{r['rows_ok']}/{r['rows_header']} | {r['diff_bytes']} | {r['unique_row_lens']} | "
            f"{len(r['canonical_fields'])} | {(r['error'] or '')[:80]} |"
        )
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (OUT_DIR / "DONE.md").write_text(
        f"DONE type=t111\nstatus={master['status']}\nclosed={n_closed}\nsample_ok={n_sample}\nfailed={n_fail}\n"
        f"total={len(results)}\nclean={n_clean}/79 (t96c baseline 68/79)\nlast11_clean={last11_clean}/11\n",
        encoding="utf-8",
    )
    return master


def rebuild_report_from_json() -> int:
    """从 wire_traces_t111.json 重建 last11_traces.json/REPORT.md/DONE.md (不重跑模拟)."""
    import t96c_unicorn_master as M  # noqa: F401  (状态函数依赖)
    data = json.loads((OUT_DIR / "wire_traces_t111.json").read_text(encoding="utf-8"))
    results = data["tables"]
    elapsed = data.get("elapsed_sec", 0)
    write_deliverables(results, elapsed)
    n_closed = sum(1 for r in results if r["closed_to_footer"])
    n_fail = sum(1 for r in results if status_of(r) == "FAIL")
    print(f"rebuilt deliverables from wire_traces_t111.json: closed={n_closed} fail={n_fail} total={len(results)}")
    return 0 if n_fail == 0 else 1


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(
        description="t111: fix the last 11 failing Unicorn table pairs (R1 dbctx globals, R2 version globals, R3 isolated arenas, R4 footer-bounded slice).")
    ap.add_argument("--last11", action="store_true", help="只跑最后 11 对目标表")
    ap.add_argument("--only", type=str, default="", help="逗号分隔 arch/tid (如 server/3,client/0)")
    ap.add_argument("--full-limit", type=int, default=1500, help="nrows<=该值时整表跑 (默认 1500)")
    ap.add_argument("--sample-rows", type=int, default=50, help="大表采样行数 (默认 50)")
    ap.add_argument("--selftest", action="store_true",
                    help="闭合校验: server/t5, client/t5, server/t10, client/t10, server/t32(315), server/t41(173), server/t72(138) 全部 diff=0")
    ap.add_argument("--rebuild-report", action="store_true",
                    help="从 wire_traces_t111.json 重建 last11_traces.json/REPORT.md/DONE.md (不重跑模拟)")
    args = ap.parse_args()

    if args.rebuild_report:
        return rebuild_report_from_json()

    if args.selftest:
        targets = {("server", 5), ("client", 5), ("server", 10), ("client", 10),
                   ("server", 32), ("server", 41), ("server", 72)}
        results, _ = run_sweep(pairs=targets, full_limit=1500, sample_rows=50)
        all_ok = True
        for r in results:
            print(f"SELFTEST {r['archive']}/{r['table_id']} rows={r['rows_ok']}/{r['rows_header']} "
                  f"diff={r['diff_bytes']} closed={r['closed_to_footer']}")
            all_ok = all_ok and r["closed_to_footer"]
        return 0 if all_ok else 1

    if args.last11:
        pairs = set(LAST11.keys())
    elif args.only:
        pairs = set()
        for tok in args.only.split(","):
            tok = tok.strip()
            if not tok:
                continue
            a, t = tok.split("/")
            pairs.add((a, int(t)))
    else:
        pairs = None

    results, elapsed = run_sweep(pairs=pairs, full_limit=args.full_limit, sample_rows=args.sample_rows)
    # --only / --selftest 是诊断跑: 不覆写交付物 (完整 sweep/--last11 才落盘)
    if args.only or args.selftest:
        tag = " ".join(
            f"{r['archive']}/t{r['table_id']}={status_of(r)}" for r in results)
        print(f"\nDIAG (no deliverables written): {tag}")
        return 0 if all(status_of(r) != "FAIL" for r in results) else 1
    master = write_deliverables(results, elapsed)
    print(f"\nDONE t111 in {master['elapsed_sec']}s: closed={master['closed_to_footer']} "
          f"sample_ok={master['sample_rows_all_ok']} fail={master['failed']} / {master['total_archive_tables']}")
    return 0 if master["failed"] == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
