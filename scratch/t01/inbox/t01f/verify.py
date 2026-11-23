#!/usr/bin/env python3
"""Rebuild/verify t01f from PE bytes and real Zstd members, without running either PE.

From fm24-db: py -V:3.12 -I -B scratch/t01/inbox/t01f/verify.py --selftest
--write writes only output.json next to this script; otherwise verify it read-only.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import mmap
import runpy
import struct
import sys
from contextlib import ExitStack
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = ROOT.parent / 'fm24'
DEFAULT_DB = Path('Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm')
SNAPSHOT = 'evidence/fm24/reports/'
EXPECTED_PE = {
    'editor.exe': 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4',
    'fm.exe': 'e1059eee82fa7832188831521a3fa633ec3260dd98d03da48b16661147e3ab48',
}
EXPECTED_SERVER = '98bb59ad08a6de9bc73992d8e7bf400ea6697159bf5911b5e56742a6bdb1d8f5'


class Failure(Exception):
    pass


def require(condition, explanation):
    if not condition:
        raise Failure(explanation)


def load(path):
    return json.loads(path.read_bytes())


def word(data, off=0, n=4, signed=False):
    return int.from_bytes(data[off:off + n], 'little', signed=signed)


class PE:
    def __init__(self, name, stack, cs):
        self.name = name
        self.path = OLD / 'input' / name
        f = stack.enter_context(self.path.open('rb'))
        self.data = stack.enter_context(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
        digest = hashlib.sha256(self.data).hexdigest()
        require(digest == EXPECTED_PE[name], f'{name}: SHA-256 != IDA_PROVENANCE snapshot')
        self.source = {'file': self.path.as_posix(), 'bytes': len(self.data), 'sha256': digest}
        p = word(self.data, 0x3c)
        require(self.data[p:p+6] == b'PE\0\0\x64\x86', name + ': not x64 PE')
        opt = p + 24
        require(word(self.data, opt, 2) == 0x20b, name + ': not PE32+')
        self.base = word(self.data, opt + 24, 8)
        st = opt + word(self.data, p + 20, 2)
        self.sections = {}
        for s in range(st, st + word(self.data, p+6, 2)*40, 40):
            self.sections[self.data[s:s+8].rstrip(b'\0').decode()] = struct.unpack_from('<IIII', self.data, s+8)
        self.md = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_64)
        self.md.detail = True
        self.rip = cs.x86_const.X86_REG_RIP

    def va(self, off):
        for _, rva, size, raw in self.sections.values():
            if size and raw <= off < raw + size:
                return self.base + rva + off - raw
        raise Failure(f'{self.name} unmapped file offset {off:#x}')

    def off(self, va):
        for _, rva, size, raw in self.sections.values():
            d = va - (self.base + rva)
            if 0 <= d < size:
                return raw + d
        raise Failure(f'{self.name} VA has no file bytes {va:#x}')

    def ev(self, off, size=None, *, exact=None):
        expected = bytes.fromhex(exact) if exact is not None else None
        size = len(expected) if expected is not None else size
        require(size is not None and size > 0, 'empty evidence span')
        actual = self.data[off:off+size]
        require(len(actual) == size and (expected is None or actual == expected),
                f'{self.name}@{off:#x}: unexpected bytes {actual.hex(" ")}')
        return {'file': self.name, 'file_offset': hex(off), 'va': hex(self.va(off)), 'bytes': actual.hex(' ')}

    def ins(self, off):
        i = next(self.md.disasm(self.data[off:off+15], self.va(off), 1), None)
        require(i is not None, f'{self.name}@{off:#x}: no instruction')
        return i

    def op(self, off, text=None):
        i = self.ins(off)
        op = (i.mnemonic + ' ' + i.op_str).strip()
        require(text is None or op == text, f'{self.name}@{off:#x}: {op}, wanted {text}')
        return {**self.ev(off, i.size), 'instruction': op}

    def rip_target(self, off):
        i = self.ins(off)
        ms = [o for o in i.operands if o.type == 3 and o.mem.base == self.rip]
        require(len(ms) == 1, f'{self.name}@{off:#x}: expected RIP operand')
        return i.address + i.size + ms[0].mem.disp

    def rel(self, off, expect_off, kind='call'):
        i = self.ins(off)
        require(i.mnemonic == kind and i.operands[0].type == 2 and i.operands[0].imm == self.va(expect_off),
                f'{self.name}@{off:#x}: not {kind} to file {expect_off:#x}')
        return {**self.op(off), 'target_file_offset': hex(expect_off)}

    def ptr(self, off, expect_off):
        return self.ev(off, exact=struct.pack('<Q', self.va(expect_off)).hex())

    def rtti(self, vptr, name):
        link = self.ev(vptr-8, 8)
        col = self.off(word(self.data, vptr-8, 8))
        signature, o, c, type_rva, _, self_rva = struct.unpack_from('<6I', self.data, col)
        require((signature, o, c, self_rva) == (1, 0, 0, self.va(col)-self.base), name + ': bad COL')
        typ = self.off(self.base + type_rva) + 16
        return {'name': name, 'vptr_file_offset': hex(vptr), 'vptr_va': hex(self.va(vptr)),
                'locator_pointer': link, 'complete_object_locator': self.ev(col, 24),
                'type_descriptor_name': self.ev(typ, exact=(name+'\0').encode('ascii').hex())}


# Table-25 reader landmarks. The cursor is a sum (no row displacement search).
# Scalar tuple: temporary or object destination, byte count, destination instruction,
# count instruction and stream call, plus the analogous writer transfer.
DIRECT = (
    ('obj_15c', 0x15c, 1, 0xeb701c, 0xeb7027, 0xeb7030, 0xeb8976),
    ('obj_15d', 0x15d, 1, 0xeb7040, 0xeb704b, 0xeb7054, 0xeb899a),
    ('obj_1a0', 0x1a0, 1, 0xeb707b, 0xeb7085, 0xeb7091, 0xeb89d8),
    ('levl', 0x1a2, 1, 0xeb70a1, 0xeb70ab, 0xeb70b7, 0xeb89fc),
    ('obj_1a3', 0x1a3, 1, 0xeb70c7, 0xeb70d1, 0xeb70dd, 0xeb8a20),
    ('Ccre', 0x1a4, 1, 0xeb70ed, 0xeb70f7, 0xeb7100, 0xeb8a44),
    ('CTty', 0x1a5, 1, 0xeb7110, 0xeb711a, 0xeb7123, 0xeb8a68),
    ('obj_f6', 0xf6, 1, 0xeb7161, 0xeb716b, 0xeb7174, 0xeb8aba),
    ('ccti', 0x58, 4, 0xeb725c, 0xeb7263, 0xeb726c, 0xeb8ba9),
    ('cnti', 0x60, 4, 0xeb727c, 0xeb7283, 0xeb728c, 0xeb8be2),
    ('lbc ', 0x70, 4, 0xeb729c, 0xeb72a3, 0xeb72ac, 0xeb8c54),
    ('cpcm', 0x68, 4, 0xeb72bc, 0xeb72c3, 0xeb72cc, 0xeb8c89),
    ('obj_150', 0x150, 2, 0xeb7363, 0xeb736d, 0xeb7376, 0xeb8caa),
    ('obj_148', 0x148, 4, 0xeb7a24, 0xeb7a2e, 0xeb7a37, 0xeb924e),
    ('obj_152', 0x152, 2, 0xeb7a47, 0xeb7a51, 0xeb7a5a, 0xeb9271),
    ('cmnl', 0x154, 2, 0xeb7a6a, 0xeb7a74, 0xeb7a80, 0xeb9294),
    ('cmnw', 0x156, 2, 0xeb7a90, 0xeb7a9a, 0xeb7aa8, 0xeb92b7),
    ('cmxl', 0x158, 2, 0xeb7ab8, 0xeb7ac2, 0xeb7ad0, 0xeb92da),
    ('cmxw', 0x15a, 2, 0xeb7ae0, 0xeb7aea, 0xeb7af8, 0xeb92fd),
    ('cnor', 0x80, 4, 0xeb7bc6, 0xeb7bd0, 0xeb7bdc, 0xeb9338),
    ('csou', 0x88, 4, 0xeb7bec, 0xeb7bf6, 0xeb7bff, 0xeb9373),
    ('cwes', 0x90, 4, 0xeb7c0f, 0xeb7c19, 0xeb7c22, 0xeb93ae),
    ('ceas', 0x98, 4, 0xeb7c32, 0xeb7c3c, 0xeb7c45, 0xeb93e9),
    ('wbcl_present', None, 1, 0xeb7c81, 0xeb7c86, 0xeb7c8f, 0xeb9416),
    ('cuae', 0xf7, 1, 0xeb7ceb, 0xeb7cf5, 0xeb7cfe, 0xeb9485),
    ('csso', 0xf8, 1, 0xeb7d0e, 0xeb7d18, 0xeb7d21, 0xeb94a8),
    ('cosr', 0xf9, 1, 0xeb7d31, 0xeb7d3b, 0xeb7d44, 0xeb94cb),
)

# 4CC compare + equality target, and first definitive object-member access on that path.
# The few non-member first instructions (date/colour VT setup) are checked in the linear prefix.
CASES = {
    'cfcl': (0xec0f6a, 0xec0f76, 0xec0f7b), 'cbcl': (0xec0704, 0xec3535, 0xec353a),
    'ctcl': (0xec1098, 0xec38f2, 0xec38f7), 'levl': (0xec1781, 0xec4672, 0xec4672),
    'Ccre': (0xec2c88, 0xec2c94, 0xec2c94), 'CTty': (0xec47b0, 0xec47b8, 0xec47b8),
    'ccti': (0xec2007, 0xec3792, 0xec3792), 'cnti': (0xec1fea, 0xec3780, 0xec3780),
    'lbc ': (0xecae87, 0xecc3a5, 0xecc3e2), 'cpcm': (0xec0a9d, 0xec0aa9, 0xec0aa9),
    'cmnl': (0xec0a44, 0xec33aa, 0xec33aa), 'cmnw': (0xec0a50, 0xec3576, 0xec3576),
    'cmxl': (0xec2114, 0xec37a4, 0xec37a4), 'cmxw': (0xec2120, 0xec212c, 0xec212c),
    'cnor': (0xec0fdb, 0xec0fe7, 0xec0fe7), 'csou': (0xec21d1, 0xec39f4, 0xec39f4),
    'cwes': (0xec0542, 0xec38e5, 0xec38e5), 'ceas': (0xec0f52, 0xec3416, 0xec3416),
    'wbcl': (0xec0786, 0xec320d, 0xec3221), 'wbst': (0xec079e, 0xec07aa, 0xec07af),
    'wben': (0xec0792, 0xec325d, 0xec3262), 'cuae': (0xec10b0, 0xec10bc, 0xec10bc),
    'csso': (0xec21dd, 0xec21e9, 0xec21e9), 'cosr': (0xec0a91, 0xec35da, 0xec35da),
    'crep': (0xec2190, 0xec3808, 0xec3808), 'PLgn': (0xec0baa, 0xec0bb6, 0xec0bb6),
    'dbty': (0xec152a, 0xec3896, 0xec3896), 'cext': (0xec0f5e, 0xec3629, 0xec3629),
    'cusn': (0xec0536, 0xec384e, 0xec384e), 'culn': (0xec0093, 0xec009f, 0xec009f),
}


def field_case(p, key, disp):
    cmp, head, mem = CASES[key]
    a = p.ins(cmp)
    require(a.mnemonic == 'cmp' and a.operands[1].imm == int.from_bytes(key.encode(), 'big'), key+' cmp')
    br = p.ins(cmp + a.size)
    if br.mnemonic == 'je':
        edge = p.rel(cmp+a.size, head, 'je')
    else:
        require(br.mnemonic == 'jne' and p.off(br.address+br.size) == head, key+' fallthrough')
        edge = p.op(cmp+a.size)
    b = p.ins(mem)
    require(any(x.type == 3 and x.mem.disp == disp and b.reg_name(x.mem.base) in ('r12', 'rdi') for x in b.operands),
            f'{key}: not an access to COMP+{disp:#x}')
    prefix = p.ev(head, mem-head) if mem != head else None
    return {'compare': p.op(cmp), 'equality_edge': edge, 'handler_prefix': prefix, 'member_access': p.op(mem)}


def sized_io(p, at, size, size_at=None, *, vslot_load=None):
    if size_at is None:
        needle = b'\x41\xb8' + struct.pack('<I', size)
        size_at = p.data.rfind(needle, at-20, at)
        require(size_at != -1, f'{p.name}@{at:#x} expected width {size}')
    end = p.ins(at)
    if vslot_load is None:
        require(end.mnemonic == 'call' and len(end.operands) == 1 and end.operands[0].type == 3
                and end.operands[0].mem.disp == 0x28, f'{p.name}@{at:#x} not stream IO vcall')
    else:
        require(vslot_load < size_at, 'stream slot must be resolved before the width')
        p.op(vslot_load, 'mov rax, qword ptr [rax + 0x28]')
        p.op(at, 'call rax')
    p.op(size_at, f'mov r8d, {hex(size) if size >= 10 else size}')
    # No alternate control transfer or intervening R8 assignment in the measured fragment.
    middle = list(p.md.disasm(p.data[size_at:at], p.va(size_at)))
    require(sum(i.size for i in middle) == at-size_at and
            all(not i.mnemonic.startswith(('j', 'call', 'ret')) for i in middle), 'bad width-to-call window')
    for i in middle[1:]:
        reg = {i.reg_name(r) for r in i.regs_access()[1]}
        require(not reg & {'r8', 'r8d', 'r8w', 'r8b'}, 'stream width overwritten')
    return p.ev(size_at, at+end.size-size_at)


def build_trait_manager(p, f, prior_reg):
    require(p.sections['.reloc'][1]-p.sections['.reloc'][3] == 0x16b600, 'editor .reloc mapping')
    fast = [p.op(0x3612d74), p.op(0x3612d7b), p.rel(0x3612d7e, 0x3612f0f, 'jne')]
    glob = p.rip_target(0x3612d74)
    require(glob == p.rip_target(0x3612da9) == p.rip_target(0x3612f01) == 0x141b5a490, 'singleton global')
    refs = [p.rel(0x83caf0, 0x3612d70, 'jmp'), *fast, p.op(0x3612f01), p.op(0x3612f13, 'ret')]
    manager_vp = p.off(p.rip_target(0x3612e17))
    trait_manager = p.rtti(manager_vp, '.?AVTYPED_TRAITS_MANAGER@sicore@@')
    wrappers = [
        (0x08, 0, 0x3612e21, None, 'NULL_TYPED_TRAITS@sicore', '.?AVNULL_TYPED_TRAITS@sicore@@'),
        (0x18, 3, 0x3612e30, 0x3612e2c, 'bool', '.?AV?$RAW_TYPED_TRAITS@_N@sicore@@'),
        (0x28, 1, 0x3612e3f, 0x3612e3b, 'signed int', '.?AV?$RAW_TYPED_TRAITS@H@sicore@@'),
        (0x38, 2, 0x3612e4e, 0x3612e4a, 'unsigned int', '.?AV?$RAW_TYPED_TRAITS@I@sicore@@'),
        (0x48, 15, 0x3612e5d, 0x3612e59, 'signed int64', '.?AV?$RAW_TYPED_TRAITS@_J@sicore@@'),
        (0x58, 24, 0x3612e6c, 0x3612e68, 'unsigned int64', '.?AV?$RAW_TYPED_TRAITS@_K@sicore@@'),
        (0x68, 25, 0x3612e7b, 0x3612e77, 'float', '.?AV?$RAW_TYPED_TRAITS@M@sicore@@'),
        (0x78, 5, 0x3612e8d, 0x3612e86, 'double', '.?AV?$RAW_TYPED_TRAITS@N@sicore@@'),
        (0x88, 26, 0x3612e9f, 0x3612e98, 'string', '.?AVSTRING_TYPED_TRAITS@sicore@@'),
        (0x98, 14, 0x3612eb4, 0x3612ead, 'symbol', '.?AVSYMBOL_TYPED_TRAITS@sicore@@'),
        (0xa8, 11, 0x3612ec9, 0x3612ec2, 'typed list', '.?AV?$INTERNAL_OBJECT_TYPED_TRAITS@VTYPED_LIST@sicore@@$0L@@sicore@@'),
        (0xb8, 10, 0x3612ede, 0x3612ed7, 'record', '.?AV?$INTERNAL_OBJECT_TYPED_TRAITS@VRECORD@sicore@@$09@sicore@@'),
        (0xc8, 27, 0x3612ef3, 0x3612eec, 'date/time', '.?AVDATE_TIME_TYPED_TRAITS@sicore@@'),
    ]
    traits = []
    for off, tag, lea, tag_at, name, cpp in wrappers:
        vptr = p.off(p.rip_target(lea))
        if tag_at is None:
            tag_evidence = [p.ev(0x3612dca, exact='0f 57 c0'), p.ev(0x3612dd1, exact='0f 29 40 10')]
        else:
            tag_evidence = [p.op(tag_at, f'mov byte ptr [rax + {off+8:#x}], '+(hex(tag) if tag >= 10 else str(tag)))]
        traits.append({'manager_offset': off, 'type': name, 'init_byte_at_trait_plus_8': tag,
                       'construct': [p.op(lea), p.op(lea+7, f'mov qword ptr [rax + {off if off == 8 else hex(off)}], rcx')],
                       'type_byte_evidence': tag_evidence, 'rtti': p.rtti(vptr, cpp)})
    reg = []
    for i, key in enumerate(prior_reg):
        off = 0xebf060 + i*0x30
        callB = p.rel(off-9, 0x83caf0)
        callA = p.rel(off+0x15, 0x83abf0)
        reg.append({'4cc': key, 'helperB': callB, 'same_manager_displacement': p.ev(off-4, exact='48 83 c0 38'),
                    'local_pair': p.ev(off, exact=(b'\xc7\x45\xf0'+key.encode()[::-1]+bytes.fromhex('48 89 45 e8')).hex()),
                    'helperA': callA})
    require(len(reg) == 51 and len({r['4cc'] for r in reg}) == 51, 'registration count')
    fm_example = [f.rel(0x22e8ca7, 0x197c670), f.ev(0x22e8cac, exact='48 83 c0 38'),
                  f.ev(0x197c6c0, exact='b9 d8 00 00 00')]
    slot = {
        'old_stride_0x38': 'Falsified: displacement immediate 0x38 is reapplied to a fresh call returning the same singleton, not an increment on a carried iterator.',
        'trait_subobjects': {'size_inferred_from_stride': 16, 'vptr_at': 0, 'vptr_width': 8, 'init_type_byte_at': 8,
                             'unknown_or_padding': 'trait +0x09..+0x0f; do not infer row offsets'},
        'register_argument_pair': {'size': 16, 'typed_trait_pointer_at': 0, 'payload_at': 8, 'comp_registration_payload': 'Big-endian 4CC as numeric u32, stored in low dword; upper dword not given 4CC semantics.',
                                   'copy_and_reset': [p.ev(0x83ad52, 15), p.rel(0x83ad60, 0x83caf0), p.ev(0x83ad65, 15)],
                                   'vector_slot_stride': 8, 'append': p.ev(0x83ad7e, exact='48 89 1f 49 83 47 08 08')},
        'comp_registrations': reg,
        'actual_runtime_object': 'db::COMP is a separately constructed instance; its object-member displacements are not row positions or trait offsets.',
    }
    init = {'manager_rtti': trait_manager,
            'inline_in_helperB_body': [p.ev(0x3612dc0, exact='b9 d8 00 00 00'), p.rel(0x3612dc5, 0x17502c0),
                                      p.op(0x3612e17), p.ev(0x3612e1e, exact='48 89 08')],
            'traits': traits, 'published_at_va': hex(glob)}
    b = {'role': 'arg-independent lazy sicore::TYPED_TRAITS_MANAGER singleton accessor',
         'return_path_and_thunk': refs, 'slow_start_uses_tls_guard': [p.op(0x3612d84), p.op(0x3612d90)],
         'fm_counterpart': fm_example,
         'field_dispatch_correction': 'helperB()+N is a type-handler pointer for a boxed value. The COMP object member is in the source operand of the getter (e.g. [r12+0x154]), not N.'}
    return slot, init, b


def build_codec(p, f):
    cursor = []
    pos = 0

    def add(key, size, dst, evidence, **more):
        nonlocal pos
        cursor.append({'step': key, 'row_offset': pos, 'width': size,
                       'object_offset': dst, 'evidence': evidence, **more})
        pos += size

    def scalar(x):
        key, dst, n, lea, size_at, call, write = x
        l = p.ins(lea)
        require(l.mnemonic == 'lea' and l.operands[1].mem.disp == (dst if dst is not None else 0x48), key + ' target')
        allowed = {'rbx', 'rcx'} if dst is not None else {'rsp'}
        require(l.reg_name(l.operands[1].mem.base) in allowed, key+' destination base')
        record = {'read_destination': p.op(lea), 'read_bytes': sized_io(p, call, n, size_at),
                  'destination_to_transfer': p.ev(lea, call+p.ins(call).size-lea),
                  'write_transfer_width_crosscheck': sized_io(p, write, n)}
        add(key, n, dst, record)

    direct = {x[0]: x for x in DIRECT}
    for key in ('obj_15c', 'obj_15d'):
        scalar(direct[key])
    color_reads = [0x4330d01, 0x4330d22, 0x4330d67, 0x4330dad, 0x4330df3, 0x4330e39, 0x4330e7d]
    color_write_marker = p.off(p.rip_target(0x4330753))
    color_proof = {'read_destination': p.op(0xeb7061, 'lea rcx, [rbx + 0x120]'),
                   'entry': p.rel(0xeb706b, 0x150ec50), 'thunk': p.rel(0x150ec50, 0x4330ce0, 'jmp'),
                   'widths': [sized_io(p, at, n) for at,n in zip(color_reads, [1,2,2,2,2,2,1], strict=True)],
                   'writer_thunk': p.rel(0x150ea80, 0x4330740, 'jmp'), 'writer_marker': p.ev(color_write_marker, exact='01')}
    add('colour_block_version', 1, None, color_proof, expected=1)
    for i,k in enumerate(('cfcl', 'cbcl', 'ctcl', 'colour_word_3', 'colour_word_4')):
        store = (0x4330d4d, 0x4330d92, 0x4330dd8, 0x4330e1e, 0x4330e60)[i]
        decode = color_reads[i+1] + p.ins(color_reads[i+1]).size
        add(k, 2, 0x120 + 4*i, {'colour_helper': 'colour_block_version',
                                'read_bytes': sized_io(p, color_reads[i+1], 2),
                                'decode_and_store': p.ev(decode, store+7-decode), 'decode_store_low_channel': p.op(store)})
    add('obj_134', 1, 0x134, {'colour_helper': 'colour_block_version', 'read_bytes': sized_io(p, color_reads[-1], 1),
                              'relative_destination': p.op(0x4330e6a, 'add rdi, 0x14')})
    for key in ('obj_1a0', 'levl', 'obj_1a3', 'Ccre', 'CTty'):
        scalar(direct[key])
    extra = [0x4339ed1, 0x4339eed, 0x4339f09, 0x4339f25, 0x4339f45, 0x4339f65, 0x4339f88]
    add('stat_block_a_version', 1, None,
        {'read_destination': p.op(0xeb7130, 'lea rcx, [rbx + 0x198]'), 'entry': p.rel(0xeb713a, 0x151d2e0),
         'thunk': p.rel(0x151d2e0, 0x4339e80, 'jmp'), 'read_bytes': sized_io(p, 0x4339ea1, 1),
         'branch': [p.ev(0x4339eb4, exact='80 7c 24 2f 01'), p.rel(0x4339ebc, 0x4339f9a, 'jbe')],
         'writer_marker_load': p.op(0x4339a53),
         'writer_marker': p.ev(p.off(p.rip_target(0x4339a53)), exact='02')}, expected=2)
    add('stat_block_a_values', len(extra), 0x198, {'byte_calls': [sized_io(p, at, 1) for at in extra]},
        unmapped=True, encoding='7 one-byte members')
    add('stat_block_b_version', 1, None,
        {'read_destination': p.op(0xeb7147, 'lea rcx, [rbx + 0x189]'), 'entry': p.rel(0xeb7151, 0x151d710),
         'thunk': p.rel(0x151d710, 0x433bbc0, 'jmp'), 'read_bytes': sized_io(p, 0x433bbe5, 1),
         'writer_marker_load': p.op(0x433a693),
         'writer_marker': p.ev(p.off(p.rip_target(0x433a693)), exact='03')}, expected=3)
    add('stat_block_b_values', 15, 0x189,
        {'choose_count': p.ev(0x433bbfc, 0x1b), 'byte_loop': sized_io(p, 0x433bc32, 1),
         'loop_back': p.rel(0x433bc41, 0x433bc20, 'jne')}, unmapped=True, encoding='15 one-byte members for tag 3')
    scalar(direct['obj_f6'])

    def date(key, dst, rd, wr):
        add(key, 4, dst, {'read_destination': p.op(rd-10, f'lea rcx, [rbx + {dst:#x}]'),
                          'read_date': p.rel(rd, 0xdb7f80), 'read_thunk': p.rel(0xdb7f80, 0x39dd7b0, 'jmp'),
                          'read_bytes': sized_io(p, 0x39dd7d4, 4, 0x39dd7c8),
                          'writer_call': p.rel(wr, 0xdb7fd0), 'writer_thunk': p.rel(0xdb7fd0, 0x39dd840, 'jmp'),
                          'writer_words': [sized_io(p, 0x39dd85f, 2), sized_io(p, 0x39dd882, 2)]})
    date('obj_138_date', 0x138, 0xeb718b, 0xeb8ad1)
    date('obj_13c_date', 0x13c, 0xeb71a2, 0xeb8ae8)
    for key in ('ccti', 'cnti', 'lbc ', 'cpcm', 'obj_150', 'obj_148', 'obj_152', 'cmnl', 'cmnw', 'cmxl', 'cmxw', 'cnor', 'csou', 'cwes', 'ceas', 'wbcl_present'):
        scalar(direct[key])
    cursor[-1]['expected'] = 1
    add('wbcl', 2, 0x14c, {'presence_edge': p.ev(0xeb7c9c, exact='80 7c 24 48 00 74 17'),
                           'read_destination': p.op(0xeb7ca3, 'lea rdx, [rbx + 0x14c]'),
                           'read_call': p.rel(0xeb7cad, 0x7e30c0), 'read_thunk': p.rel(0x7e30c0, 0x35025f0, 'jmp'),
                           'read_bytes': sized_io(p, 0x350260d, 2), 'decode_and_store': p.ev(0x3502617, 0x24),
                           'writer_call': p.rel(0xeb9434, 0x7e3070)})
    date('wbst', 0x140, 0xeb7cc4, 0xeb944b)
    date('wben', 0x144, 0xeb7cdb, 0xeb9462)
    for key in ('cuae', 'csso', 'cosr'):
        scalar(direct[key])
    base = {'parent_call': p.rel(0xeb7d84, 0xfae340), 'parent_thunk': p.rel(0xfae340, 0x3c600f0, 'jmp'),
            'parent_target_object_member': p.op(0x3c60106, 'lea rbx, [rdi + 8]'),
            'contiguous_read_bytes': sized_io(p, 0x3c60119, 12), 'writer_base_call': p.rel(0xeb94e6, 0xfe18b0),
            'writer_base_thunk': p.rel(0xfe18b0, 0x3cc1490, 'jmp'),
            'writer_base_destinations_and_dispatch': p.ev(0x3cc14a2, 0x3cc1508 - 0x3cc14a2),
            'writer_base_4_4_4': [sized_io(p, 0x3cc14b2, 4), sized_io(p, 0x3cc14d1, 4),
                                  sized_io(p, 0x3cc1508, 4, 0x3cc14fc, vslot_load=0x3cc14e4)]}
    add('rdui', 4, 8, base)
    add('duni', 8, 0xc, {'same_parent_transfer': 'rdui', 'second_dword_object_offset': 0x10})
    require(pos == 126, f'row body length {pos} != 126 without framing')
    # Match the familiar 14 + N*127 + 8 convention of the ledger, not a redefined row offset.
    add('following_zero_marker', 1, None,
        {'writer_emits_leading_zero': [p.ev(0xeb893b, exact='c6 44 24 28 00'), sized_io(p, 0xeb8952, 1)],
         'reader_body_does_not_emit_or_consume_trailing_byte': p.ev(0xeb7dae, exact='48 8b 06 83 78 10 00 40 0f 94 c5 e9 c3 f5 ff ff')}, expected=0)
    require(pos == 127, 'full row stride')

    wrappers = {'legacy_col_inclusive_indices': '0=RTTI pointer, 6=registrar, 8=25, 20/23=read wrappers, 22/24=write wrappers. True indices are one less.',
                'record_type_id': [p.ptr(0x187d2f0, 0xed0a30), p.ev(0xed0a30, exact='b8 19 00 00 00 c3')],
                'reader_from_vtable': [p.ptr(0x187d350, 0xed0a40), p.rel(0xed0a40, 0x3b3f0d0, 'jmp'),
                                       p.ev(0x3b3f0d0, 0x31), p.ev(0x3b3f0f9, exact='c6 44 24 38 00 45 31 c0'), p.rel(0x3b3f101, 0xeb7000)],
                'read_this_binding_and_frame_size': p.ev(0xeb7000, exact='41 57 41 56 41 55 41 54 56 57 55 53 48 83 ec 78 4d 89 cc 48 89 d6 48 89 cb'),
                'writer_from_vtable': [p.ptr(0x187d360, 0xed0a80), p.ev(0xed0a80, exact='45 89 c8 45 31 c9'), p.rel(0xed0a86, 0xeb8920, 'jmp')],
                'write_this_binding': p.op(0xeb8935, 'mov rdi, rcx'),
                'mode_note': 'In reader body (entry RSP minus 0xb8), [rsp+0xf8] is arg8, set to 0 by slot 19; [rsp+0xe8] is arg6, forwarded by the wrapper. The data correspond to no inline-name transfers, ordinal references, and arg6=0 (no server extra).',
                'member_base_in_getter': [p.ptr(0x187d2c8, 0xec0060), p.ev(0xec0090, exact='49 89 cc')],
                'client_read_path': [p.op(0xeb71b9), p.rel(0xeb71bd, 0xeb71f7, 'jne'), p.op(0xeb71f7), p.rel(0xeb7202, 0xeb7259, 'je'),
                                     p.op(0xeb7394), p.rel(0xeb73a0, 0xeb7a21, 'je')],
                'client_write_path': [p.op(0xeb8b36), p.rel(0xeb8b38, 0xeb8b48, 'je'), p.op(0xeb8cc4), p.rel(0xeb8cc7, 0xeb9238, 'je')],
                'reference_output_uses_ordinal_in_this_mode': [p.op(0xeb8b48, 'mov rax, qword ptr [rdi + 0x58]'),
                    p.op(0xeb8b4c, 'test rax, rax'), p.rel(0xeb8b4f, 0xeb8b8f, 'je'),
                    p.op(0xeb8b51, 'mov eax, dword ptr [rax + 8]'), p.op(0xeb8b8f, 'mov eax, 0xffffffff')],
                'storage': 'Serializer instruction order and requested byte widths; not an explicit table of row offsets. Conditional paths change the cursor.',
                'framing': 'Public row offsets remain relative to payload 14+i*127. The COMP body transfers through +125 only. The writer emits a leading 0; the captured leading byte at 13+i*127 fits that format. +126 is framing (the following zero in that view), not a COMP property. The precise end-marker ownership beyond the last record is not inferred.',
                'cursor_layout': cursor}
    fm_e = [f.ptr(0x5a53ed0, 0x22fab20), f.rel(0x22fab51, 0x22dfa70),
            f.ptr(0x5a53ee0, 0x22fab60), f.rel(0x22fab66, 0x22e1690, 'jmp'),
            f.ev(0x22dfa8c, exact='48 8d 91 5c 01 00 00'), sized_io(f, 0x22dfaa0, 1),
            f.ev(0x22e16ab, exact='c6 44 24 28 00'), sized_io(f, 0x22e16c2, 1)]
    wrappers['fm_crosscheck'] = fm_e
    return wrappers


def build_identity_names(p, steps):
    """Use the native 4CC accessors, not the names of the b47 byte anchors."""
    layout = {s['step']: s for s in steps}
    ordinal = layout['rdui']['row_offset']
    uid = layout['duni']['row_offset']
    require(ordinal == 114 and uid == ordinal+4 and layout['duni']['width'] == 8, 'identity block')
    return {
        'inherited_dispatch': {'rtti': p.rtti(0x1876fa8, '.?AVDATABASE_RECORD@db@@'),
            'getter_pointer_slot_2': p.ptr(0x1876fb8, 0xfe3520), 'comp_getter_fallback': p.rel(0xec4820, 0xfe3520, 'jmp'),
            'getter_this_binding': p.op(0xfe3548, 'mov r12, rcx')},
        'dsha': {'row_offset': ordinal, 'width': 4, 'object_offset': 8, 'description': 'Ordinal lane; called rdui in the b47 data anchor.',
            'compare': p.op(0xfe3a1b, 'cmp esi, 0x64736861'), 'equal': p.rel(0xfe3a21, 0xfe3c5d, 'je'),
            'member': p.op(0xfe3c5d, 'mov esi, dword ptr [r12 + 8]')},
        'duni': {'row_offset': uid, 'width': 4, 'object_offset': 12, 'description': 'Unique ID; +118..125 is the byte-anchor pair, not one property read.',
            'compare': p.op(0xfe3912, 'cmp esi, 0x64756e69'), 'equal': p.rel(0xfe3918, 0xfe3bff, 'je'),
            'member': p.op(0xfe3bff, 'mov esi, dword ptr [r12 + 0xc]')},
        'rdui': {'row_offset': uid+4, 'width': 4, 'object_offset': 16,
            'description': 'Saved Random ID lane. Writer uses obj+0xc if obj+0x10 is zero. Getter only exposes a difference from duni; does not expose the ordinal.',
            'compare': p.op(0xfe3862, 'cmp esi, 0x72647569'), 'equals_fallthrough': p.op(0xfe3868),
            'read_and_compare': p.ev(0xfe389d, exact='41 8b 74 24 10 41 39 74 24 0c'),
            'writer_fallback': p.ev(0x3cc14da, 0x2e)},
    }


def source_dat(db_dir):
    # Reuse the frozen repository's read-only FMF+Zstd decoder. No unpacked files written.
    library = runpy.run_path(str(OLD / 'scripts/modding_read_dbdat.py'))
    out = []
    for archive in ('client_db.dat', 'server_db.dat'):
        path, blob, layout = library['_entries'](db_dir, archive)
        e = next(x for x in layout['entries'] if x['path'] == archive[:-4] + '/table_25.dat')
        start = layout['data_base'] + e['offset']
        require(blob[start:start+4] == b'\x28\xb5\x2f\xfd', archive + ': table_25 member is not Zstd')
        raw = library['_decompress_entry'](blob, layout['data_base'], e)
        out.append((raw, {'archive_path': path.as_posix(), 'archive_sha256': hashlib.sha256(blob).hexdigest(),
                          'archive_member': e['path'], 'compressed_file_offset': hex(start),
                          'compressed_size': e['packed_size'], 'compressed_magic': blob[start:start+4].hex(' '),
                          'uncompressed_bytes': len(raw), 'payload_sha256': hashlib.sha256(raw).hexdigest(),
                          'payload_offset_domain': 'Offsets inside decompressed FMF member, not raw archive byte addresses.'}))
    return out


def at(raw, off, n):
    return {'payload_offset': hex(off), 'bytes': raw[off:off+n].hex(' ')}


def slots_for_row(raw_row, steps):
    require(len(raw_row) == 127, 'expected 127-byte recorded row')
    values = {}
    cursor = 0
    for s in steps:
        n, k = s['width'], s['step']
        require(cursor == s['row_offset'] and cursor+n <= len(raw_row), 'cursor continuity: '+k)
        b = raw_row[cursor:cursor+n]
        if 'expected' in s:
            require(n == 1 and b[0] == s['expected'], 'wrong fixed path byte: '+k)
        if k == 'obj_1a0':
            require(b[0] != 4, 'inline-name path, not this fixture')
        values[k] = b
        cursor += n
    require(cursor == len(raw_row), 'did not consume whole fixed record')
    return values


def validate_data(p, codec, archive, sv, known):
    raw, meta = archive
    server, srvmeta = sv
    steps = codec['cursor_layout']
    require(meta['payload_sha256'] == known['source_payload_sha256'], 'client payload differs from b47')
    require(srvmeta['payload_sha256'] == EXPECTED_SERVER, 'server payload not the verified 2430 fixture')
    n = word(raw, 8)
    require(raw[:14] == server[:14] == bytes.fromhex('03 01 74 61 64 2e f1 0d 87 1b 00 00 00 00'), 'tad header/version/count')
    require(n == 7047 and len(raw) == 14+127*n+8, 'client framing equation')
    off = lambda i: 14+127*i
    rows = [raw[off(i):off(i+1)] for i in range(n)]
    model = []
    ids = []
    for i, r in enumerate(rows):
        d = slots_for_row(r, steps)
        require(word(d['rdui']) == i and d['duni'][:4] == d['duni'][4:], f'row {i}: identity')
        require(word(d['ccti']) in {*range(6),0xffffffff}, f'row {i}: ccti range')
        require(word(d['cnti']) <= 250 or word(d['cnti']) == 0xffffffff, f'row {i}: cnti range')
        require(all(d[k] in (b'\0', b'\1') for k in ('cuae', 'csso')), f'row {i}: boolean bytes')
        require(all(word(d[k]) < 0x8000 for k in ('cfcl','cbcl','ctcl','colour_word_3','colour_word_4','wbcl')),
                f'row {i}: high bit set in colour word')
        ids.append(word(d['duni']))
        model.append(d)
    require(len(set(ids)) == n, 'unique DUNI across table')
    li = {dbid:i for i,dbid in enumerate(ids)}
    anchors = []
    for a in known['named_anchor_checks']:
        i = li[a['dbid']]
        require(i == a['row_index'] and word(model[i]['ccti']) == a['ccti'] and word(model[i]['cnti']) == a['cnti'], 'anchor '+a['expected_name'])
        anchors.append({'dbid': a['dbid'], 'prior_english_name': a['expected_name'], 'row_index': i,
                        'ccti': at(raw, off(i)+52, 4), 'cnti': at(raw, off(i)+56, 4)})
    parents = []
    for a in known['parent_reference_checks']:
        i, parent = li[a['child_dbid']], li[a['parent_dbid']]
        require(i == a['child_row_index'] and word(model[i]['cpcm']) == parent == 352, 'parent anchor')
        parents.append({'row_index': i, 'child_dbid': a['child_dbid'], 'expected_parent_ordinal': parent,
                        'parent_dbid': a['parent_dbid'], 'child_cpcm': at(raw, off(i)+64, 4), 'parent_identity': at(raw, off(parent)+114, 12)})
    # Bound the writer-shaped interval (one leading marker + 126-byte body).
    # This is a raw framing check, not a game serializer roundtrip.
    require(raw[13:13+127*n:127] == b'\0'*n, 'leading record markers')
    require(raw[-9:] == server[-9:] == bytes.fromhex('00 00 00 00 01 4e c4 3a 77'), 'residual after last COMP body')
    meta.update({'table_id': 25, 'rows': n, 'stride': 127, 'ledger_header_bytes': 14, 'ledger_footer_bytes': 8,
                 'header': at(raw, 0, 14), 'footer': at(raw, len(raw)-8, 8),
                 'first_leading_marker': at(raw, 13, 1), 'residual_after_last_body': at(raw, len(raw)-9, 9)})
    checks = {'validated_row_count': n,
              'identities': {'ordinal_equals_index': n, 'adjacent_duni_dwords_equal': n, 'unique_dbid': n},
              'continent_and_nation_named_anchors': anchors, 'cpcm_named_anchors': parents,
              'markers_verified_for_every_row': {s['step']: s['expected'] for s in steps if 'expected' in s},
              'leading_zero_marker_count': n, 'no_inline_name_branch_count': n, 'colour_and_boolean_domains_pass_count': n,
              'parent_ordinals_out_of_range': [{'index':i, 'value':word(d['cpcm']), **at(raw, off(i)+64, 4)} for i,d in enumerate(model) if n <= word(d['cpcm']) < 0xffffffff]}

    # Ordered 12-byte identities and independent common-prefix and common-suffix tests.
    # Find one record at a time, verify exact relative anchors, not a stride guess.
    extra, prev, server_samples = [], 14, []
    for i, r in enumerate(rows):
        tag = r[114:126]
        pos = server.find(tag, prev+70+44)
        require(pos >= 0 and pos+13 <= len(server)-8, f'server row {i}: missing ordered identity')
        require(server[prev:prev+70] == r[:70], f'server row {i}: prefix')
        require(server[pos-44:pos+13] == r[70:], f'server row {i}: suffix')
        start, se = prev, pos-44
        require(se >= start+72, f'server row {i}: missing extras')
        extra.append(se-start-70)
        prev = pos+13
        if i in (0, 7, 639, n-1):
            server_samples.append({'index': i, 'record_payload_start': hex(start), 'extra_length': extra[-1],
                                   'server_crep': {**at(server, start+70, 2),'value':word(server, start+70, 2, True)},
                                   'identity': at(server, pos, 12)})
    require(prev+8 == len(server), 'server footer and full ordered coverage')
    server_proof = {**srvmeta, 'row_count_with_client_prefix_and_suffix': n,
                    'layout': 'Common client [0,70) + variable server extra + common client [70,127); match includes the conventional +126 framing byte.',
                    'common_prefix_bytes': 70, 'common_suffix_bytes': 57,
                    'extra_length_histogram': dict(sorted(collections.Counter(extra).items())),
                    'crep_offset': 70, 'crep_width': 2, 'crep_examples': server_samples,
                    'extra_selection_and_crep_read': [p.op(0xeb7394), p.rel(0xeb73a0, 0xeb7a21, 'je'), p.op(0xeb73a6), sized_io(p, 0xeb73b9, 2)],
                    'crep_object_link': field_case(p, 'crep', 0x180),
                    'scope': 'Boundaries recovered from joined client identities; not a general parser of the variable server-only blocks.'}
    return meta, checks, server_proof, model, ids, off


def build(cs, db_dir):
    man = {r['path']:r['sha256'] for r in load(ROOT/'evidence/MANIFEST.json')['files']}
    paths = [SNAPSHOT+x for x in ('editor_schema/master.json', 'dbdat_decode/db_tables_big.json',
              'dbdat_decode/DB_TABLES_BIG.md', 'dbdat_decode/client_table_25_competition_samples.json',
              'qa/IDA_PROVENANCE.md', 'editor_gen/replicate/codec_tables.json')]
    manifest_check = {}
    for path in paths:
        got = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        require(got == man[path], 'frozen snapshot mismatch: '+path)
        manifest_check[path] = got
    master = load(ROOT/paths[0]); schema = {x['field']:x for x in next(q for q in master['entities']['comp.xml'] if q['id']=='comp')['fields']}
    prior = ROOT/'scratch/t01'
    reg = next(c['cc_list'] for c in load(prior/'t01a_editor_sweep.json')['clusters'] if c['start_off']=='0xebf060')
    b47 = load(ROOT/paths[1])['tables']['25']
    archives = source_dat(db_dir)
    with ExitStack() as stack:
        p, f = (PE(name, stack, cs) for name in ('editor.exe','fm.exe'))
        slot, init, helper = build_trait_manager(p, f, reg)
        codec = build_codec(p, f)
        identity_names = build_identity_names(p, codec['cursor_layout'])
        meta, checks, server, rows, ids, start = validate_data(p, codec, *archives, b47)

        comp = {'rtti': p.rtti(0x187d2b8, '.?AVCOMP@db@@'), 'rtti_fm': f.rtti(0x5a53e38, '.?AVCOMP@db@@'),
                'vptr_store': [p.op(0xeb5dd5), p.ev(0xeb5ddc, exact='48 89 01')],
                'registrar_pointer_slot_5': p.ptr(0x187d2e0, 0xebf040),
                'factory_allocation': [p.ev(0xf49129, exact='b9 b0 01 00 00'), p.rel(0xf4912e, 0xf6e0e0), p.rel(0xf49139, 0xeb5db0)],
                'extra_ctor_vptr_store': [p.op(0xeb6037), p.ev(0xeb603e, exact='48 89 01')]}
        require(p.rip_target(0xeb5dd5) == p.rip_target(0xeb6037) == p.va(0x187d2b8), 'COMP ctor vptr')
        jtb = p.rip_target(0xf48b45)
        entry = p.off(jtb+25*4)
        require(p.off(jtb+word(p.data,entry,4,True)) == 0xf49129, 'type 25 factory switch')
        table = {'rtti': p.rtti(0x187ecd8, '.?AV?$DATABASE_TABLE@VCOMP@db@@@db@@'),
                 'init_table_type_25': [p.ev(0xf02aa7, exact='ba 19 00 00 00'), p.rel(0xf02aaf, 0xff9910),
                                        p.op(0xf02ab4), p.ev(0xf02abb, exact='48 89 07'),
                                        p.rel(0xff9910, 0x3ceb7d0, 'jmp'), p.ev(0x3ceb8e2, exact='89 7e 54')],
                 'factory_switch_25': [p.op(0xf48b45), p.ev(0xf48b4c, exact='48 63 04 81 48 01 c8 ff e0'), p.ev(entry, exact='f1 f3 ff ff')],
                 'table_loop_family_example': {'bound': 'Generic table-loop sample; not an assertion of an archive-opener xref to this exact instantiation.',
                     'read_count': sized_io(p, 0xf2ad00, 4),'read_table_flag': sized_io(p, 0xf2ad1f, 1),
                     'one_byte_before_factory': sized_io(p, 0xf2af2f, 1), 'type_from_table': p.op(0xf2af41, 'mov ecx, dword ptr [rsi + 0x54]'),
                     'factory_call': p.rel(0xf2af44, 0xf48b30), 'virtual_call_setup': p.ev(0xf2af4e, 0x24),
                     'read_virtual_slot_19': p.ev(0xf2af72, exact='ff 95 98 00 00 00'),
                     'loop_back': p.rel(0xf2af7a, 0xf2af10, 'jne')}}
        require(p.rip_target(0xf02ab4) == p.va(0x187ecd8), 'table template vptr')
        same_block = p.ev(0xebf063, exact='6e 67 4c 50 48 89 45 e8 48 8d 7d e8 48 89 f1 48')
        comp['same_registrar_bytes'] = [same_block, f.ev(0x22e8cb3, exact=same_block['bytes'])]

        field_map = {}
        anchors = {'ccti':52, 'cnti':56, 'cpcm':64, 'rdui':114, 'duni':118}
        special = {'levl': 'i8; getter adds 1 unless raw 100 (null)', 'CTty': 'i8 enum',
                   'Ccre':'i8', 'cosr':'i8; -1 null', 'rdui':'u32 ordinal', 'duni':'u64 (two matching u32 in this data)'}
        verified = []
        for s in codec['cursor_layout']:
            key, x, n, dst = (s[k] for k in ('step','row_offset','width','object_offset'))
            if key not in CASES and key not in anchors:
                continue
            codec_desc = special.get(key)
            if not codec_desc:
                codec_desc = ('3x5-bit packed colour/u16le' if key in ('cfcl','cbcl','ctcl','wbcl') else
                              'i16le; getter divides by 10' if key in ('cmnl','cmnw','cmxl','cmxw') else
                              '4-byte packed date' if key in ('wben','wbst') else
                              'byte boolean' if key in ('cuae','csso') else 'u32le row reference (0xffffffff = null)')
            name = schema.get(key, {}).get('name')
            count = key in schema and key not in anchors and (x <= 51 or 68 <= x <= 113)
            if count:
                verified.append(key)
            # Add concrete non-default examples where the standard sample rows are all alike.
            examples = [7,639]
            alt = next((i for i,r in enumerate(rows) if r[key] != rows[7][key]), None)
            if alt is not None and alt not in examples:
                examples.append(alt)
            obj = {'row_offset':x,'width':n,'object_offset':dst, 'name':name, 'encoding':codec_desc,
                   'master_is_client_field': schema.get(key, {}).get('is_client_field') == 'true' if key in schema else None,
                   'counted_as_new_schema_business_field': count, 'evidence_level':'L3-static + L1-data',
                   'cursor_step':key,'examples': [{'index':i,'dbid':ids[i], **at(archives[0][0],start(i)+x,n)} for i in examples]}
            if key in CASES:
                obj['property_link'] = field_case(p,key,dst)
            elif key in ('rdui','duni'):
                obj['status'] = 'b47 byte-anchor label; native property names and widths are in native_identity_slots.'
                obj['native_storage_link'] = ['dsha'] if key == 'rdui' else ['duni','rdui']
            if key == 'levl':
                obj['normalization'] = [p.ev(0xec467b, exact='83 fe 64'),p.rel(0xec467e, 0xec4c84,'jne'),p.ev(0xec4c84, exact='ff c6')]
            elif key in ('cmnl','cmnw','cmxl','cmxw'):
                divide = {'cmnl':0xec33ba, 'cmnw':0xec3586, 'cmxl':0xec37b4, 'cmxw':0xec213c}[key]
                require(p.rip_target(divide)==p.va(0x1774b30), 'pitch divisor address')
                obj['normalization'] = [p.op(divide),p.ev(0x1774b30,exact='00 00 20 41')]
            elif key == 'wbcl':
                obj['conditional'] = 'Presence flag +100 is 1 in all 7,047 rows; do not hard-code this offset for other modes/samples.'
            elif key == 'cosr':
                obj['normalization'] = [p.op(0xec35e3, 'cmp esi, -1'), p.rel(0xec35e6, 0xec4eb4, 'je')]
            if key not in schema and key not in anchors:
                obj['status'] = 'Internal executable 4CC; no master schema entry; not counted.'
            field_map[key] = obj
        require({key: field_map[key]['row_offset'] for key in anchors} == anchors, 'all five offsets must reproduce prior anchors')
        flagged_client = [k for k in verified if field_map[k]['master_is_client_field']]
        require(len(verified) == 18 and len(flagged_client) == 14, 'new named business-field count')
        for k, m, off in (('plgn',0xf5,0xeb7676), ('dbty',0xf4,0xeb7643), ('bits',0x1a1,0xeb75fd)):
            require(p.ins(off).operands[1].mem.disp == m, 'server-only client contrast '+k)
        server['other_members_in_skipped_branch_not_client_fixed_offsets'] = {
            'PLgn': {'case': field_case(p,'PLgn',0xf5), 'server_io': sized_io(p,0xeb768c,1),'version_test':p.ev(0xeb766c,exact='3d c4 0d 00 00')},
            'dbty': {'case': field_case(p,'dbty',0xf4), 'server_io': sized_io(p,0xeb7656,1)},
            'cext_cusn_culn': {'cases': {k:field_case(p,k,0x1a1) for k in ('cext','cusn','culn')},'server_io':sized_io(p,0xeb7610,1)},
        }
        refs = {}
        r2 = load(prior/'inbox/t01b/round2/output.json')
        for key, tag, wrapper, cpp_kind in [('ccti','cont',0xfe6e60,'continent'),('cnti','Nnat',0xfcb710,'nation'),('cpcm','comp',0xfe6ba0,'competition'),('csou','city',0xfe6ca0,'city')]:
            require(schema[key]['database_table_type'] == cpp_kind, 'schema reference type '+key)
            h = CASES[key][1]
            access = p.ins(h)
            arg = h + access.size
            p.op(arg, 'mov rdx, r14')
            refs[key] = {'tag': tag, 'reference_target': cpp_kind, 'handler_call': p.rel(arg+3,wrapper),
                         'two_id_dwords': p.ev(wrapper+0xc, exact='8b 41 0c 8b 49 10'),
                         'tag_instruction':p.ev(wrapper+0x30,exact=(b'\xba'+tag.encode()[::-1]).hex()), 'shared_helper_call':p.rel(wrapper+0x35,0xfe68b0)}
        # R2 lexical census is input, not promoted to an end-to-end DBC apply chain.
        tags = {'traits_in_constructor': 'constructor.type_traits_manager.traits', 'reference_tag_examples': refs,
                'shared_reference_boxing': [p.ev(0xfe68e4,exact='8b 43 04 48 c1 e0 20 48 63 1b 48 09 c3'),
                                            p.rel(0xfe68f1,0x83caf0),p.ev(0xfe68f6,exact='48 83 c0 48'),p.rel(0xfe690e,0x8334b0),
                                            p.ev(0xfe693d, exact='48 8b 45 e8 48 8b 4d f0 48 89 4e 08 48 89 06')],
                'inherited_literal_census_not_row_wire_types':[t['tag'] for t in r2['common_helper_tag_census']['tags']],
                'note':'cont is the referenced continent category in this call, not a container type; +0x48 is signed-i64 typed traits. The tag-bearing reference wrapper is an export/boxing path, not the raw row serializer.'}

        return {'task':'t01-f', 'acceptance': {'met':True,'l3_new_client_packed_schema_business_fields':len(verified),
                    'new_codes':verified, 'new_codes_also_marked_client_in_master': flagged_client,
                    'all_mapped_keys_including_legacy_anchors_and_internal':len(field_map),
                    'client_anchor_offsets':anchors,'anchor_offsets_use_b47_labels':True,'L4':0},
                'sources': {'binary':[p.source,f.source], 'verified_frozen_snapshots':manifest_check,'client_table_25':meta,
                            'archive_unpack_dependency': (OLD/'scripts/modding_read_dbdat.py').as_posix(),
                            'layout_only_read':True, 'python':'py -V:3.12 -I -B', 'capstone':cs.__version__},
                'slot_layout':slot, 'constructor':{'type_traits_manager':init, 'comp_record':comp, 'comp_table':table},
                'helperB_semantics':helper, 'row_offset_map':field_map, 'native_identity_slots':identity_names,
                'row_codec':codec, 'verification':checks,
                'server_crosscheck':server, 'type_tags':tags,
                'falsified': [
                    {'old':'helperB points into an unreadable wall', 'disposition':'resolved for this thunk only', 'evidence_path':'helperB_semantics.return_path_and_thunk'},
                    {'old':'0x38 spacing iterates unique property descriptors (possibly holding row offsets)', 'disposition':'false for this registrar; all 51 refer to the same unsigned-int trait', 'evidence_path':'slot_layout.comp_registrations; constructor.type_traits_manager.traits'},
                    {'old':'switch helperB()+N gives an object member offset', 'disposition':'false for these patterns; trait pointer differs from actual COMP member access', 'evidence_path':'row_offset_map.cmnl; constructor.type_traits_manager.traits'},
                    {'old':'no hits from hard-coded row-displacement probes imply schema-array-driven .dat layout', 'disposition':'does not follow; typed COMP sequential I/O uses object displacements and access widths', 'evidence_path':'row_codec.cursor_layout; row_codec.reader_from_vtable'},
                    {'old':'cont is container here', 'disposition':'false for ccti; reference target is continent', 'evidence_path':'type_tags.reference_tag_examples.ccti'},
                    {'old':'the identity-anchor label rdui at +114 denotes the same native property', 'disposition':'false: +114 is the ordinal (native dsha); b47 labels retained for byte-compatibility only', 'evidence_path':'native_identity_slots'},
                    {'old':'helperA is vector<32B> or supplies a proven global registry', 'disposition':'8-byte pointer elements; specific registration consumer not proved in this task', 'evidence_path':'slot_layout.register_argument_pair'},
                ],
                'open_questions': [
                    'Semantic names for unidentified operations in row_codec.cursor_layout, including the two versioned stat arrays, are not promoted.',
                    'COMP client cursor verified for these v3569 rows, not alternate modes (inline names at obj+0x1a0==4; absent winter colour; legacy or server extras).',
                    'No end-to-end archive opener -> exact table-loop instantiation or full helperA registry-consumer xref is asserted.',
                    'No L4/load test, or generalized server extension parser or cross-table propagation was performed.',
                ]}


def selftest_model(out):
    # Negative controls: the old fixed model must reject a bad packed version or an
    # inline-name variant even when the nominal length and identity locations agree.
    steps = out['row_codec']['cursor_layout']
    sample = bytearray(127)
    for s in steps:
        if 'expected' in s:
            sample[s['row_offset']] = s['expected']
    slots_for_row(bytes(sample), steps)
    for offset, value in ((2,2),(14,4),(19,1),(27,2),(100,0),(126,1)):
        b = sample[:]; b[offset] = value
        try:
            slots_for_row(bytes(b), steps)
        except Failure:
            continue
        raise Failure(f'negative control accepted: offset {offset}')
    # Partial success must not allow an erroneous east/west swap or identity shift.
    keys = out['row_offset_map']
    require([keys[k]['row_offset'] for k in ('cnor','csou','cwes','ceas','rdui','duni')] == [84,88,92,96,114,118], 'named control lanes')
    native = out['native_identity_slots']
    require([native[k]['row_offset'] for k in ('dsha','duni','rdui')] == [114,118,122], 'native identity lanes')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db-dir', type=Path, default=DEFAULT_DB, help='existing read-only 2430_fm directory')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='rebuild only the colocated output.json')
    mode.add_argument('--selftest', action='store_true', help='also run negative controls and verify output.json (default verifies exact rebuild)')
    args = ap.parse_args()
    try:
        import capstone
        out = build(capstone, args.db_dir)
        if args.selftest or args.write:
            selftest_model(out)
        path = HERE/'output.json'
        # JSON uses string keys; normalize integer histogram keys for comparison.
        stable = json.dumps(out, ensure_ascii=False, indent=2) + '\n'
        if args.write:
            path.write_text(stable, encoding='utf-8',newline='\n')
        else:
            require(load(path) == json.loads(stable), 'output.json differs from reconstructed evidence')
    except Failure as e:
        print(f'FAIL: {e}', file=sys.stderr)
        return 1
    except (OSError, RuntimeError, ImportError, ValueError, KeyError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 2
    stats = out['acceptance']
    print(f"PASS: +{stats['l3_new_client_packed_schema_business_fields']} L3 client fields; five anchors; "
          f"{out['verification']['validated_row_count']} client rows and server joins; output.json {'rebuilt' if args.write else 'matches'}." )
    return 0


if __name__ == '__main__':
    sys.exit(main())
