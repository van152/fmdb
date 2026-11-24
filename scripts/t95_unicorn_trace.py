"""t95_unicorn_trace — Real x86_64 Unicorn micro-execution wire tracer for FM24 editor.exe.

Maps editor.exe (all 18 PE sections including 45MB .reloc) into Unicorn at ImageBase 0x140000000,
stubs the stream vtable (+0x28 read) + minimal bump allocator + Windows x64 TEB/TLS + IAT stubs,
and executes ANY table's slot19 (read_server) or slot20 (read_client) directly on real .dat row bytes.

Every stream->read(stream, dst, n) call is logged with exact:
  (wire_pos, nbytes, dst_kind, obj_offset, caller_va, raw_hex)

Usage:
  py -V:3.12 -I -B scripts/t95_unicorn_trace.py --selftest
  py -V:3.12 -I -B scripts/t95_unicorn_trace.py --func 0x141544130 --archive server --table 45 --row-offset 13 --max-bytes 200
Exit codes: 0 ok, 1 emulation incomplete/error, 2 bad usage.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PE = Path(str(_cfg.EDITOR_EXE))

# Memory map constants (disjoint from editor.exe 0x140000000..0x145000000)
STACK_BASE = 0x0000_0001_0000_0000
STACK_SIZE = 0x0020_0000  # 2 MB
THIS_BASE = 0x0000_0002_0000_0000
THIS_SIZE = 0x0004_0000  # 256 KB zero-init object buffer
STREAM_PTR_ADDR = 0x0000_0002_1000_0000  # a2 points here; [a2] = STREAM_OBJ_ADDR
STREAM_OBJ_ADDR = 0x0000_0002_1000_1000  # *a2 (stream object)
STREAM_VT_ADDR = 0x0000_0002_1000_2000   # stream vtable
STUB_CODE_BASE = 0x0000_0002_2000_0000   # 64 KB stub trampolines (ret / hooks)
HEAP_BASE = 0x0000_0003_0000_0000
HEAP_SIZE = 0x0400_0000  # 64 MB bump heap
TEB_BASE = 0x0000_0004_0000_0000
TEB_SIZE = 0x0004_0000
STOP_ADDR = STUB_CODE_BASE + 0x0000      # return sentinel
STREAM_READ_STUB = STUB_CODE_BASE + 0x0100
STREAM_OTHER_BASE = STUB_CODE_BASE + 0x0200
IAT_STUB_BASE = STUB_CODE_BASE + 0x1000


def align_up(x: int, a: int = 0x1000) -> int:
    return (x + a - 1) & ~(a - 1)


class EditorEmulator:
    def __init__(self, pe_path: Path = DEFAULT_PE):
        sys.path.insert(0, str(_cfg.LEGACY_TOOLS_DIR))
        import pefile  # noqa: E402
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
        from unicorn.x86_const import (  # noqa: E402
            UC_X86_REG_GS_BASE,
            UC_X86_REG_RAX,
            UC_X86_REG_RCX,
            UC_X86_REG_RDX,
            UC_X86_REG_R8,
            UC_X86_REG_R9,
            UC_X86_REG_RIP,
            UC_X86_REG_RSP,
        )

        self.REG = {
            "GS_BASE": UC_X86_REG_GS_BASE,
            "RAX": UC_X86_REG_RAX,
            "RCX": UC_X86_REG_RCX,
            "RDX": UC_X86_REG_RDX,
            "R8": UC_X86_REG_R8,
            "R9": UC_X86_REG_R9,
            "RIP": UC_X86_REG_RIP,
            "RSP": UC_X86_REG_RSP,
        }

        self.pe_path = pe_path
        self.pe = pefile.PE(str(pe_path), fast_load=True)
        self.pe.parse_data_directories(
            directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]]
        )
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.image_size = align_up(self.pe.OPTIONAL_HEADER.SizeOfImage, 0x10000)
        self.raw = pe_path.read_bytes()

        self.mu = Uc(UC_ARCH_X86, UC_MODE_64)
        # Map entire PE image cleanly
        self.mu.mem_map(self.base, self.image_size)
        # Copy headers
        hdr_sz = self.pe.OPTIONAL_HEADER.SizeOfHeaders
        self.mu.mem_write(self.base, self.raw[:hdr_sz])
        for s in self.pe.sections:
            fo = s.PointerToRawData
            raw_sz = s.SizeOfRawData
            va = self.base + s.VirtualAddress
            if raw_sz > 0 and fo < len(self.raw):
                chunk = self.raw[fo : fo + raw_sz]
                self.mu.mem_write(va, chunk)

        # Map runtime regions
        self.mu.mem_map(STACK_BASE, STACK_SIZE)
        self.mu.mem_map(THIS_BASE, THIS_SIZE)
        self.mu.mem_map(STREAM_PTR_ADDR, 0x10000)
        self.mu.mem_map(STUB_CODE_BASE, 0x20000)
        self.mu.mem_map(HEAP_BASE, HEAP_SIZE)
        self.mu.mem_map(TEB_BASE, TEB_SIZE)

        # Fill STUB_CODE_BASE with RET (0xC3) so every stub auto-returns after hook
        self.mu.mem_write(STUB_CODE_BASE, b"\xC3" * 0x20000)

        # Setup Windows x64 TEB/TLS at GS_BASE
        # TEB+0x30 = self ptr, TEB+0x58 = ThreadLocalStoragePointer -> array of TLS slots
        tls_array = TEB_BASE + 0x1000
        tls_slot0 = TEB_BASE + 0x2000
        self.mu.mem_write(TEB_BASE + 0x30, struct.pack("<Q", TEB_BASE))
        self.mu.mem_write(TEB_BASE + 0x58, struct.pack("<Q", tls_array))
        for i in range(64):
            self.mu.mem_write(tls_array + i * 8, struct.pack("<Q", tls_slot0 + i * 0x200))
        # Set TLS init epoch high so static guard checks pass without calling _Init_thread_header
        for i in range(64):
            self.mu.mem_write(tls_slot0 + i * 0x200 + 4, struct.pack("<i", 0x7FFFFFFF))
        self.mu.reg_write(self.REG["GS_BASE"], TEB_BASE)

        # Patch IAT entries to stub addresses and map stub -> API name
        self.iat_map: dict[int, str] = {}
        stub_addr = IAT_STUB_BASE
        if hasattr(self.pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                dll = entry.dll.decode("ascii", errors="ignore").lower()
                for imp in entry.imports:
                    name = (imp.name.decode("ascii", errors="ignore") if imp.name else f"ord_{imp.ordinal}")
                    self.iat_map[stub_addr] = f"{dll}!{name}"
                    if self.base <= imp.address < self.base + self.image_size:
                        self.mu.mem_write(imp.address, struct.pack("<Q", stub_addr))
                    stub_addr += 8

        # Setup stream object & vtable
        self.mu.mem_write(STREAM_PTR_ADDR, struct.pack("<Q", STREAM_OBJ_ADDR))
        self.mu.mem_write(STREAM_OBJ_ADDR + 0x00, struct.pack("<Q", STREAM_VT_ADDR))
        self.mu.mem_write(STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))  # refcount
        self.mu.mem_write(STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))     # error flag = 0
        for idx in range(32):
            off = idx * 8
            if off == 0x28:
                self.mu.mem_write(STREAM_VT_ADDR + off, struct.pack("<Q", STREAM_READ_STUB))
            else:
                self.mu.mem_write(STREAM_VT_ADDR + off, struct.pack("<Q", STREAM_OTHER_BASE + off))

        # Hook SI internal pool allocators (0x1407e4490, 0x1407e58c0) & operator new (0x141750cc0)
        # Patch their entry points in emulated RAM to jump to stub trampolines in STUB_CODE_BASE
        self.pool_alloc_stubs: dict[int, str] = {}
        POOL_STUB_BASE = STUB_CODE_BASE + 0x0800
        for idx, (target_va, kind) in enumerate([
            (0x1407E4490, "pool_rdx"),  # SI pool alloc(pool=rcx, size=rdx)
            (0x143671D70, "pool_rdx"),  # .reloc body of 0x1407E4490
            (0x1407E58C0, "pool_rdx"),  # SI pool alloc(pool=rcx, size=rdx)
            (0x143676CA0, "pool_rdx"),  # .reloc body of 0x1407E58C0
            (0x141750CC0, "new_rcx"),   # operator new(size=rcx)
        ]):
            stub = POOL_STUB_BASE + idx * 8
            self.pool_alloc_stubs[stub] = kind
            # Write: mov rax, imm64; jmp rax (12 bytes) at target_va
            tramp = b"\x48\xB8" + struct.pack("<Q", stub) + b"\xFF\xE0"
            self.mu.mem_write(target_va, tramp)

        # Per-run state
        self.heap_ptr = HEAP_BASE
        self.payload = b""
        self.wire_pos = 0
        self.reads: list[dict] = []
        self.unhandled_calls: list[dict] = []
        self.heap_allocs: list[tuple[int, int, int]] = []  # (addr, size, caller)

        from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED  # noqa: E402
        self.mu.hook_add(UC_HOOK_CODE, self._on_stub, begin=STUB_CODE_BASE, end=STUB_CODE_BASE + 0x1FFFF)
        self.mu.hook_add(UC_HOOK_MEM_UNMAPPED, self._on_unmapped)

    def _alloc(self, size: int, caller: int = 0) -> int:
        sz = max(16, (size + 15) & ~15)
        addr = self.heap_ptr
        self.heap_ptr += sz
        if self.heap_ptr < HEAP_BASE + HEAP_SIZE:
            self.mu.mem_write(addr, b"\x00" * min(sz, 0x10000))
        self.heap_allocs.append((addr, sz, caller))
        return addr

    def _classify_dst(self, dst: int) -> tuple[str, int | None]:
        if THIS_BASE <= dst < THIS_BASE + THIS_SIZE:
            return "this", dst - THIS_BASE
        if STACK_BASE <= dst < STACK_BASE + STACK_SIZE:
            return "stack", dst - (STACK_BASE + STACK_SIZE)
        if HEAP_BASE <= dst < HEAP_BASE + HEAP_SIZE:
            return "heap", dst - HEAP_BASE
        return "other", None

    def _on_stub(self, uc, address: int, size: int, user_data):
        rsp = uc.reg_read(self.REG["RSP"])
        caller = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]

        if address == STOP_ADDR:
            uc.emu_stop()
            return

        if address == STREAM_READ_STUB:
            # stream->read(RCX=stream, RDX=dst, R8=nbytes)
            dst = uc.reg_read(self.REG["RDX"])
            n = uc.reg_read(self.REG["R8"])
            if n > 0x100000:
                self.unhandled_calls.append({"kind": "huge_read", "n": n, "caller": hex(caller)})
                uc.mem_write(STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 1))
                uc.reg_write(self.REG["RAX"], 0)
                return
            avail = self.payload[self.wire_pos : self.wire_pos + n]
            if len(avail) < n:
                # EOF
                uc.mem_write(STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 1))
                uc.reg_write(self.REG["RAX"], len(avail))
                self.reads.append({
                    "wire_pos": self.wire_pos,
                    "n": n,
                    "eof": True,
                    "dst": hex(dst),
                    "caller": hex(caller),
                })
                return
            uc.mem_write(dst, avail)
            kind, off = self._classify_dst(dst)
            val_preview = avail.hex() if n <= 16 else avail[:16].hex() + "..."
            int_val = None
            if n == 1:
                int_val = avail[0]
            elif n == 2:
                int_val = struct.unpack("<H", avail)[0]
            elif n == 4:
                int_val = struct.unpack("<I", avail)[0]
            elif n == 8:
                int_val = struct.unpack("<Q", avail)[0]
            self.reads.append({
                "wire_pos": self.wire_pos,
                "n": n,
                "dst_kind": kind,
                "obj_off": hex(off) if (kind == "this" and off is not None) else None,
                "obj_off_dec": off if kind == "this" else None,
                "dst": hex(dst),
                "caller": hex(caller),
                "hex": val_preview,
                "u_val": int_val,
            })
            self.wire_pos += n
            uc.reg_write(self.REG["RAX"], n)
            return

        if address in self.pool_alloc_stubs:
            kind = self.pool_alloc_stubs[address]
            sz = uc.reg_read(self.REG["RDX"]) if kind == "pool_rdx" else uc.reg_read(self.REG["RCX"])
            if sz == 0 or sz > 0x400000:
                sz = 256
            uc.reg_write(self.REG["RAX"], self._alloc(sz, caller))
            return

        if STREAM_OTHER_BASE <= address < IAT_STUB_BASE:
            vt_off = address - STREAM_OTHER_BASE
            self.unhandled_calls.append({"kind": "stream_vcall", "vt_off": hex(vt_off), "caller": hex(caller)})
            uc.reg_write(self.REG["RAX"], 0)
            return

        if address in self.iat_map:
            api = self.iat_map[address]
            low = api.lower()
            rcx = uc.reg_read(self.REG["RCX"])
            rdx = uc.reg_read(self.REG["RDX"])
            r8 = uc.reg_read(self.REG["R8"])
            if any(k in low for k in ("heapalloc",)):
                uc.reg_write(self.REG["RAX"], self._alloc(r8, caller))
            elif any(k in low for k in ("!malloc", "!_aligned_malloc", "!calloc", "??2@")):
                sz = rcx * rdx if "!calloc" in low else rcx
                uc.reg_write(self.REG["RAX"], self._alloc(sz, caller))
            elif any(k in low for k in ("!realloc", "heaprealloc")):
                new_sz = r8 if "heaprealloc" in low else rdx
                old_p = rdx if "heaprealloc" in low else rcx
                new_p = self._alloc(new_sz, caller)
                if HEAP_BASE <= old_p < HEAP_BASE + HEAP_SIZE:
                    try:
                        old_data = bytes(uc.mem_read(old_p, min(new_sz, 0x4000)))
                        uc.mem_write(new_p, old_data)
                    except Exception:
                        pass
                uc.reg_write(self.REG["RAX"], new_p)
            elif any(k in low for k in ("!free", "heapfree", "entercriticalsection", "leavecriticalsection", "initializecriticalsection")):
                uc.reg_write(self.REG["RAX"], 1)
            elif "getprocessheap" in low:
                uc.reg_write(self.REG["RAX"], 0x1000)
            elif "getcurrentthreadid" in low:
                uc.reg_write(self.REG["RAX"], 1)
            elif "tlsgetvalue" in low:
                uc.reg_write(self.REG["RAX"], TEB_BASE + 0x2000)
            elif "acquire" in low or "release" in low or "srwlock" in low or "sleepcondition" in low:
                uc.reg_write(self.REG["RAX"], 1)
            elif "memcpy" in low or "memmove" in low:
                if r8 <= 0x100000:
                    data = bytes(uc.mem_read(rdx, r8))
                    uc.mem_write(rcx, data)
                uc.reg_write(self.REG["RAX"], rcx)
            elif "memset" in low:
                if r8 <= 0x100000:
                    uc.mem_write(rcx, bytes([rdx & 0xFF]) * r8)
                uc.reg_write(self.REG["RAX"], rcx)
            else:
                self.unhandled_calls.append({"kind": "iat", "api": api, "caller": hex(caller)})
                uc.reg_write(self.REG["RAX"], 0)
            return

    def _on_unmapped(self, uc, access, address, size, value, user_data):
        rip = uc.reg_read(self.REG["RIP"])
        self.unhandled_calls.append({
            "kind": "unmapped_mem",
            "access": access,
            "addr": hex(address),
            "size": size,
            "rip": hex(rip),
        })
        return False

    def trace_read(
        self,
        func_va: int,
        payload: bytes,
        version: int = 0x0DF1,
        a5: int = 0,
        a6: int = 0,
        a7: int = 0,
        max_insns: int = 200_000,
    ) -> dict:
        # Reset object, stream error flag, heap, logs
        self.mu.mem_write(THIS_BASE, b"\x00" * 0x4000)
        self.mu.mem_write(STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))
        self.mu.mem_write(STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))
        self.heap_ptr = HEAP_BASE
        self.payload = payload
        self.wire_pos = 0
        self.reads = []
        self.unhandled_calls = []
        self.heap_allocs = []

        # Setup stack for Windows x64 fastcall (8 args: RCX, RDX, R8, R9, [rsp+0x28], [rsp+0x30], [rsp+0x38], [rsp+0x40])
        rsp = STACK_BASE + STACK_SIZE - 0x2000
        # Return address at [rsp+0x00] = STOP_ADDR
        self.mu.mem_write(rsp + 0x00, struct.pack("<Q", STOP_ADDR))
        # Allocate db context struct (a4 / R9): [ctx+0x588] = u16 version, plus valid sub-pointers
        ctx_ptr = self._alloc(0x2000)
        sub_ptr = self._alloc(0x1000)
        self.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", version))
        # Shadow space [rsp+0x08..0x28], stack args 5..8
        self.mu.mem_write(rsp + 0x28, struct.pack("<Q", a5))
        self.mu.mem_write(rsp + 0x30, struct.pack("<Q", a6))
        self.mu.mem_write(rsp + 0x38, struct.pack("<Q", a7))
        self.mu.mem_write(rsp + 0x40, struct.pack("<Q", 0))  # a8=NULL skips post-read DB callback

        self.mu.reg_write(self.REG["RSP"], rsp)
        self.mu.reg_write(self.REG["RCX"], THIS_BASE)
        self.mu.reg_write(self.REG["RDX"], STREAM_PTR_ADDR)
        self.mu.reg_write(self.REG["R8"], 0)                 # a3=NULL skips post-read callback
        self.mu.reg_write(self.REG["R9"], ctx_ptr)

        err = None
        try:
            self.mu.emu_start(func_va, STOP_ADDR, count=max_insns)
        except Exception as exc:
            err = str(exc)

        ret_rax = self.mu.reg_read(self.REG["RAX"])
        end_rip = self.mu.reg_read(self.REG["RIP"])
        return {
            "func_va": hex(func_va),
            "ok": err is None and end_rip == STOP_ADDR,
            "error": err,
            "end_rip": hex(end_rip),
            "ret_rax": hex(ret_rax),
            "bytes_consumed": self.wire_pos,
            "read_count": len(self.reads),
            "reads": self.reads,
            "unhandled_calls": self.unhandled_calls[:20],
        }


def load_table_payload(archive: str, table_id: int) -> bytes:
    sys.path.insert(0, str(ROOT / "scripts"))
    import t38_multiframe as mf  # noqa: E402
    codec = mf._codec()
    info = mf.archive_info(codec, archive)
    target = f"{archive}_db/table_{table_id}.dat"
    for e in info["entries"]:
        if e["path"] == target:
            start, end = mf.member_bounds(e, info["data_base"])
            frames = mf.decode_frames_unbounded(info["data"], start)
            for f in frames:
                if f["length"] == int(e["size"]):
                    return f["data"]
            raise RuntimeError(f"No matching frame for {target}")
    raise FileNotFoundError(target)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Unicorn x86_64 micro-execution wire tracer for editor.exe.")
    ap.add_argument("--pe", type=Path, default=DEFAULT_PE)
    ap.add_argument("--func", type=lambda s: int(s, 0), default=0x141544130, help="Function VA to emulate")
    ap.add_argument("--archive", choices=["server", "client"], default="server")
    ap.add_argument("--table", type=int, default=45)
    ap.add_argument("--row-offset", type=int, default=13, help="Byte offset into decompressed table payload")
    ap.add_argument("--max-bytes", type=int, default=4096)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--selftest", action="store_true", help="Emulate STARTING_RECORD::read_server (table_45 row 0)")
    args = ap.parse_args()

    emu = EditorEmulator(args.pe)
    payload = load_table_payload(args.archive, args.table)
    version = struct.unpack_from("<H", payload, 6)[0]
    row_slice = payload[args.row_offset : args.row_offset + args.max_bytes]
    res = emu.trace_read(args.func, row_slice, version=version)

    print(
        f"func={res['func_va']} ok={res['ok']} ret={res['ret_rax']} "
        f"consumed={res['bytes_consumed']}B reads={res['read_count']} version={hex(version)}"
    )
    if res["error"]:
        print("ERROR:", res["error"], "end_rip=", res["end_rip"])
    if res["unhandled_calls"]:
        print("UNHANDLED:", res["unhandled_calls"][:5])
    for r in res["reads"]:
        print(
            f"  wire+{r['wire_pos']:4d} len={r['n']:2d} dst={r.get('dst_kind','?'):5s}"
            f"[{str(r.get('obj_off','-')):>6s}] caller={r['caller']} hex={r.get('hex','')}"
        )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(res, indent=2), encoding="utf-8")
    return 0 if res["ok"] and res["bytes_consumed"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
