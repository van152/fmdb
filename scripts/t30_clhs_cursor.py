#!/usr/bin/env python3
"""Build the offline Clhs/table-37 cursor and scoped field ledger."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
OUT = ROOT / 'scratch/t30/out'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EDITOR = Path('<OLD_REPO>/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
T29 = 'scratch/t29/out/profiles/table_server_37.profile.json'
INV = 'scratch/t29/out/subtable_inventory.json'
SLOT = 0x14119e7f0
VT = 0x14188e118
START, MODE, FAIL, BULK, ID_BRANCH, RET = 0x3e62b90, 0x3e62ba2, 0x3e62d6c, 0x3e62d8f, 0x3e62da7, 0x3e62de6
SELECT = 0xf2ba0e
FOOT = (0xffa602, 0xf2baa2, 0xf2bac2)
SCOPE = ['club.xml', 'Clhs']
GETTER = {
    'year': (0x119ea09, 0x119ea15), 'orde': (0x119e8d9, 0x119eaf9),
    'divi': (0x119e841, 0x119ea74), 'posi': (0x119e9f1, 0x119ec98),
    'mxtm': (0x119e97d, 0x119e989), 'poin': (0x119e8f1, 0x119e8fd),
    'play': (0x119e8e5, 0x119eb60), 'wins': (0x119e9fd, 0x119ed00),
    'draw': (0x119e84d, 0x119ea91), 'lost': (0x119e971, 0x119ec30),
    'gfor': (0x119e965, 0x119ebc8), 'gaga': (0x119e859, 0x119e865),
}


class CheckError(Exception):
    pass


def check(ok, message):
    if not ok:
        raise CheckError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_bytes())


def write(name, value):
    # Top-level object compacted by key; instruction shards by individual record.
    enc = lambda x: json.dumps(x, ensure_ascii=False, separators=(',', ':'))
    if name.startswith(('instructions.part', 'branches.part')):
        key, items = next(iter(value.items()))
        text = '{' + enc(key) + ':[\n' + ',\n'.join(map(enc, items)) + '\n]}\n'
    else:
        text = '{\n' + ',\n'.join(enc(k)+':'+enc(v) for k, v in value.items()) + '\n}\n'
    check(len(text.encode('utf-8')) < 50000, f'oversized shard: {name}')
    (OUT / name).write_text(text, encoding='utf-8')


def shards(stem, records, step):
    names = []
    for j in range(0, len(records), step):
        name = f'{stem}.part{len(names)+1:03d}.json'
        write(name, {stem: records[j:j+step]})
        names.append(name)
    return names


class Static:
    def __init__(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t14_rtti_census import parse_rtti
        from t21b_control_flow import ReaderCFG
        manifest = {x['path']: x['sha256'] for x in load('evidence/MANIFEST.json')['files']}
        self.prov = {p: sha((ROOT/p).read_bytes()) for p in (MASTER, PROV)}
        check(all(self.prov[p] == manifest[p] for p in self.prov) and self.prov[MASTER].startswith('7d57477e'), 'snapshot manifest')
        self.pe = PE(EDITOR)
        check(sha(self.pe.raw) == EXE_SHA and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'), 'editor provenance')
        self.pe.pe.parse_data_directories(directories=[3])
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.ops, self.records = {}, {}
        vf = self.pe.va2f(VT)
        self.slots = {n: struct.unpack_from('<Q', self.pe.raw, vf+n*8)[0] for n in (2,19,20,21)}
        self.rtti = parse_rtti(self.pe, VT)
        check(self.slots[19] == SLOT and self.rtti['class'] == 'STARTING_TEAM_LEAGUE_HISTORY' and self.rtti['col_off'] == 0x188d870, 'RTTI/slot19')
        jump_base, cell = 0xf49d38, 0xf49d38+4*37
        rel = struct.unpack_from('<i', self.pe.raw, cell)[0]
        check(jump_base+rel == 0xf49558, 'factory rel32')
        self.factory = {'jump_base': jump_base, 'cell': cell, 'rel32': rel, 'cell_bytes': self.pe.raw[cell:cell+4].hex(),
                        'dispatch': self.span(0xf48b30,0xf48b55), 'handler': self.span(0xf49558,0xf495af),
                        'return': self.span(0xf49ca9,0xf49cb3)}
        check(self.rip(0xf48b45) == self.pe.f2va(jump_base) and self.rip(0xf49574) == VT
              and self.ins(0xf4957b).op_str == 'qword ptr [rsi], rax', 'factory dispatch/vptr store')
        thunk = self.pe.va2f(SLOT)
        self.add(thunk)
        check(self.ins(thunk).mnemonic == 'jmp' and self.direct(thunk) == START, 'reader thunk')
        self.cfg = ReaderCFG(self.pe, self.md, START)
        self.cfg_getter = ReaderCFG(self.pe, self.md, self.pe.va2f(self.slots[2]))
        check(not self.cfg.external_edges and self.cfg.function_end_off == RET+1, 'reader PE extent')
        self.reader_sites = sorted(self.pe.va2f(v) for v in self.cfg.instructions)
        self.successors = {self.pe.va2f(v): [self.pe.va2f(t) for t in edges] for v,edges in self.cfg.successors.items()}
        self.add(*self.reader_sites)
        self.transfers, self.branches = self.reader_model()
        self.wrapper, self.wrapper_transfers = self.wrapper_model()

    def ins(self, o):
        if o not in self.ops:
            va = self.pe.f2va(o)
            check(va is not None and self.pe.va2f(va) == o, f'unmapped instruction {o:#x}')
            self.ops[o] = next(self.md.disasm(self.pe.raw[o:o+15], va, count=1))
        return self.ops[o]

    def add(self, *places):
        for o in places:
            i = self.ins(o)
            self.records[o] = {'file_offset': hex(o), 'VA': hex(i.address), 'bytes': i.bytes.hex(),
                               'instruction': f'{i.mnemonic} {i.op_str}'.rstrip()}
        return list(places)

    def span(self, o, end):
        result = []
        while o < end:
            result.extend(self.add(o))
            o += self.ins(o).size
        check(o == end, f'bad span endpoint {end:#x}')
        return result

    def rip(self, off):
        i = self.ins(off)
        return i.address+i.size+i.operands[1].mem.disp

    def direct(self, o):
        i = self.ins(o)
        check(i.operands[0].type == 2, f'not direct {o:#x}')
        return self.pe.va2f(i.operands[0].imm)

    def branch(self, o, prev, cls, origin, proof, default):
        i, p = self.ins(o), self.ins(prev)
        check(i.mnemonic.startswith('j') and i.mnemonic != 'jmp' and (prev+p.size == o or (o==0xffa640 and prev+p.size==0xffa63b and self.ins(0xffa63b).mnemonic=='mov' and 0xffa63b+self.ins(0xffa63b).size==o)), f'predicate origin {o:#x}')
        self.add(o, prev)
        return {'site': o, 'predicate': prev, 'class': cls, 'source': origin, 'evidence': proof,
                'taken_to': self.direct(o), 'fallthrough_to': o+i.size, 'observed_edge': default}

    def reader_model(self):
        t, b = {}, {}
        fixed = {
            MODE: ('runtime-external', 'loader R12B -> caller rsp+0x30 -> reader rsp+0x70', self.add(0xf2b670,0xf2ba38,0xf2ba51), 'fallthrough'),
            0x3e62d76: ('context-lifecycle', 'wrapper stream pointee; same live object used by property calls', self.add(0x3e62bc4,0x3e62bc7,0x3e62d70), 'fallthrough'),
            ID_BRANCH: ('wire_data', 'unsigned lane 0 of 12B bulk; >=10000001 stores caller ordinal', self.add(BULK,0x3e62d9d,0x3e62da9,0x3e62dae,0xf2ba3d), 'taken'),
            0x3e62db4: ('context-lifecycle', 'callback = caller table this (non-null), not R9 argument', self.add(0xf2b679,0xf2ba33,0x3e62d98,0x3e62dbf), 'fallthrough'),
            0x3e62dc8: ('context-lifecycle', 'same local stream as tail null guard', self.add(0x3e62d70,0x3e62d73), 'fallthrough'),
            0x3e62dce: ('context-lifecycle', 'ZF from release; local addref plus wrapper owns one live reference', self.add(0x3e62d78,0x3e62dca,0x3e62ddb), 'taken'),
        }
        for j, o in enumerate(self.reader_sites):
            i = self.ins(o)
            if i.mnemonic == 'call' and i.op_str == 'qword ptr [rax + 0x28]':
                block = self.reader_sites[j-8:j]
                wp, = [x for x in block if self.ins(x).op_str.startswith('r8d, ')]
                lp, = [x for x in block if self.ins(x).mnemonic == 'lea' and self.ins(x).op_str.startswith(('rdx, [rsi + ', 'rbx, [rsi + '))]
                obj = self.ins(lp).operands[1].mem.disp
                w = self.ins(wp).operands[1].imm
                setup = self.add(lp,wp,*self.reader_sites[j-2:j])
                t[o] = {'site': o, 'consumer': o, 'width': w, 'object_offset': obj, 'setup': setup,
                        'sink': f'object+{obj:#x}', 'kind': 'identity_bulk' if o == BULK else 'member'}
            if i.mnemonic.startswith('j') and i.mnemonic != 'jmp':
                prev = self.reader_sites[j-1]
                if o in fixed:
                    annotation = fixed[o]
                else:
                    check(self.ins(prev).op_str == 'dword ptr [rbx + 0x10], 0' and self.reader_sites[j-2] in t,
                          f'unclassified reader branch {o:#x}')
                    annotation = ('IO-result', 'stream +0x10 status after property transfer', [self.reader_sites[j-2]],
                                  'taken' if i.mnemonic == 'je' else 'fallthrough')
                b[o] = self.branch(o,prev,*annotation)
        check(len(t) == 15 and sum(v['width'] for v in t.values()) == 39 and len(b) == 20, 'reader transfer/branch tally')
        check([o for o in self.reader_sites if self.ins(o).mnemonic == 'call' and o not in t] == [0x3e62dbf,0x3e62ddb], 'reader other calls')
        return t, b

    def wrapper_model(self):
        self.span(0xf2b660,0xf2b6cd)
        self.span(0xf2b9d6,0xf2b9ea)
        self.span(0xf2b9f0,0xf2bad7)
        self.span(0xffa5d0,0xffa646)
        self.span(0xffa72a,0xffa752)
        self.span(0xffa785,0xffa800)
        self.span(0xffa99e,0xffa9cc)
        self.add(0xffa778,0xffa77c,0xffa77f)
        check(self.direct(0xf2ba7f) == 0xffa5d0 and self.direct(0xf2ba23) == 0xf48b30, 'wrapper helper/factory')
        b = {}
        def add(o,p,c,s,e,v):
            b[o] = self.branch(o,p,c,s,e,v)
        for o,p,t in [(0xf2b698,0xf2b694,0xf2b691),(0xf2b6b8,0xf2b6b4,0xf2b6b1),
                      (0xf2ba15,0xf2ba11,SELECT),(0xf2baa9,0xf2baa5,FOOT[1]),(0xf2bac9,0xf2bac5,FOOT[2]),
                      (0xffa7af,0xffa7ab,0xffa7a8),(0xffa7ce,0xffa7ca,0xffa7c7),
                      (0xffa7ed,0xffa7e9,0xffa7e6),(0xffa7fa,0xffa7f6,0xffa7e6)]:
            add(o,p,'IO-result','stream +0x10 status',self.add(t),'taken' if o==0xf2b6b8 else 'fallthrough' if o<0xff0000 else 'not visited')
        add(0xf2ba89,0xf2ba84,'IO-result','footer vector helper status (stream result or count bound failure)',self.add(0xf2ba7f,0xffa9a3,0xffa9b6),'fallthrough')
        add(0xf2ba59,0xf2ba57,'IO-result','slot19 AL composite result; for mode=1 false after member IO failure',self.add(0xf2ba51,FAIL,0x3e62ddd),'taken')
        add(0xf2ba2b,0xf2ba28,'context-lifecycle','factory result; table37 handler does not branch on selector',self.add(0xf2ba1b,0xf2ba20,0xf2ba23,0xf49574,0xf49ca9),'fallthrough')
        add(0xf2b9db,0xf2b9d6,'wire_data','header count; zero bypasses row loop',self.add(0xf2b691),'fallthrough')
        add(0xf2b9fa,0xf2b9f7,'wire_data','loop ordinal versus header count; check starts after first row',self.add(0xf2b691,0xf2b9f0,0xf2b9f3),'both')
        add(0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end; both edges join before helper with same R8',self.add(0xf2ba60,0xf2ba6e,0xf2ba72),'same cursor')
        add(0xffa610,0xffa609,'wire_data','footer vector count compared to process maximum',self.add(FOOT[0],0xffa605,0xffa9a3),'fallthrough')
        add(0xffa640,0xffa638,'context-lifecycle','existing vector capacity versus count; zero requires no growth',self.add(0xffa61b,0xffa61f,0xffa646),'taken')
        add(0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets, returns stream status',self.add(FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab),'taken')
        add(0xffa77f,0xffa77c,'wire_data','optional vector loop index versus footer count',self.add(0xffa775,0xffa778),'not visited')
        transfers = []
        for o, wp, lp, w, sink in [
            (0xf2b691,0xf2b688,0xf2b683,4,'loader stack+0x44 (row count)'),
            (0xf2b6b1,0xf2b6a5,0xf2b69d,1,'table+0x5c (header byte)'),
            (SELECT,0xf2ba02,0xf2b9e3,1,'loader stack+0x43 (factory selector)'),
            (FOOT[0],0xffa5fc,0xffa5f7,4,'helper stack+0x2c (vector count)'),
            (0xffa7a8,0xffa79c,0xffa746,4,'helper stack+0x30 (vector lane 0)'),
            (0xffa7c7,0xffa7bb,0xffa739,4,'helper stack+0x34 (vector lane 1)'),
            (0xffa7e6,0xffa7da,0xffa73e,4,'helper stack+0x38 (vector lane 2)'),
            (FOOT[1],0xf2ba99,0xf2ba92,1,'table+0x58'), (FOOT[2],0xf2bab9,0xf2bab2,4,'table+0x50')]:
            check(self.ins(o).op_str == 'qword ptr [rax + 0x28]' and self.ins(wp).operands[1].imm == w, 'wrapper transfer')
            transfers.append({'site':o,'consumer':o,'width':w,'sink':sink,'setup':self.add(wp,lp)})
        return b, transfers

    def scope_support(self):
        # Scope is established by the Clhs arm and the twelve exact same-class 4CCs;
        # no assignment of the unexposed back-reference schema names.
        check(self.ins(0xe8c334).operands[1].imm == int.from_bytes(b'Clhs','big') and self.direct(0xe8c33a) == 0xe8d3b2
              and self.direct(0xe8d3bc) == 0x1521d30 and self.direct(0x1521d30) == 0x4344a40, 'Clhs collection getter arm')
        thunk20, thunk21 = [self.pe.va2f(self.slots[i]) for i in (20,21)]
        check(self.direct(thunk20) == 0x3e65540 and self.direct(thunk21) == 0x3e65630
              and self.direct(0x3e65576) == 0xf7e280 and self.direct(0xf7e280) == 0x3bf3190, 'ref fixup/writer thunks')
        return {'club_Clhs_arm': self.span(0xe8c334,0xe8c340)+self.span(0xe8d3b2,0xe8d3d1)+self.add(0x1521d30)
                + self.add(0x4344a5d,0x4344aba,0x4344ac1,0x4344ac8,0x4344acb,0x4344b0d,0x4344b15,0x4344b1e,0x4344b21,0x4344ae0),
                'divi_writer': self.add(thunk21)+self.span(0x3e65670,0x3e656ac),
                'divi_fixup': self.add(thunk20)+self.span(0x3e65540,0x3e6557b)+self.add(0xf7e280,0x3bf3197,0x3bf31cd,0x3bf31df,0x3bf31e3,0x3bf31f4,0x3bf3226,0x3bf3229,0x3bf322c,0x3bf3230),
                'unscoped_pointer_slots':self.span(0x3e656ac,0x3e65718)+self.span(0x3e6557b,0x3e655e9),
                'divi_getter_comp_tag':self.span(0x119ea74,0x119ea91)+self.span(0x119ed95,0x119edb6)}

    def getter_path(self, code):
        cmp_o, dest = GETTER[code]
        o = self.pe.va2f(self.slots[2]); x = int.from_bytes(code.encode('ascii'), 'big')
        path = []
        cmp = None
        while len(path) < 32:
            i = self.ins(o)
            check(i.address in self.cfg_getter.instructions, 'getter route outside CFG')
            path.extend(self.add(o))
            if o == dest:
                break
            nxt = o+i.size
            if i.mnemonic == 'cmp':
                check(i.op_str.startswith('edx, '), 'getter EDX dispatch')
                cmp = i.operands[1].imm
            if i.mnemonic.startswith('j'):
                take = {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic]
                nxt = self.direct(o) if take else nxt
            o = nxt
        check(o == dest and cmp_o in path and self.ins(cmp_o).operands[1].imm == x, f'getter match {code}')
        src = self.ins(dest)
        check(src.operands[1].type == 3 and src.reg_name(src.operands[1].mem.base) == 'rcx', 'getter object origin')
        extra = [] if code in ('year','divi') else self.add(dest+src.size, dest+src.size+self.ins(dest+src.size).size)
        if extra:
            check(self.ins(extra[0]).op_str == ('edi, edi' if code=='orde' else 'edi, -1')
                  and self.direct(extra[1]) == 0x119ed61, 'integer getter sentinel')
        return {'path':path,'cmp':cmp_o,'access':dest,'width':src.operands[1].size,
                'object_offset':src.operands[1].mem.disp,'sentinel_proof':extra}

    def layout(self, mode):
        # Compile the branch-specialized reader tape; ID_BRANCH still executes from
        # the actual identity transfer on each iteration. No arithmetic stride input.
        o, trace, conditions = START, [], []
        for _ in range(len(self.reader_sites)):
            if o == RET:
                return trace, conditions
            check(o != FAIL, 'compiled failure path')
            if o in self.transfers:
                trace.append(self.transfers[o])
            if o in self.branches:
                b = self.branches[o]
                taken = not mode if o == MODE else b['observed_edge']=='taken'
                conditions.append([o,taken])
                o = b['taken_to' if taken else 'fallthrough_to']
            else:
                o, = self.successors[o]
        raise CheckError('reader path exceeds CFG bound')

    def blocks(self):
        leaders = {START}
        for o in self.reader_sites:
            if self.ins(o).mnemonic.startswith('j'):
                leaders.update(self.successors[o])
        results = []
        for o in sorted(leaders):
            sites = []
            while True:
                sites.append(o)
                edges = self.successors[o]
                if len(edges)!=1 or edges[0] in leaders or self.ins(o).mnemonic.startswith('j'):
                    results.append({'sites':sites,'successors':edges})
                    break
                o = edges[0]
        check(sorted(o for b in results for o in b['sites']) == self.reader_sites, 'block partition')
        return results


def walk(raw, trace, *, cut_site=None, cut_at=0):
    check(len(raw)>=13 and raw[:8]==bytes.fromhex('03017461642ef10d'), 'header magic/version')
    n, flags = struct.unpack_from('<IB',raw,8)
    check(flags==0, f'header byte {flags}')
    p, max_uid, min_uid = 13, 0, 0xffffffff
    uid_set, samples = set(), []
    digest = hashlib.sha256()
    update = digest.update
    raw_hash = hashlib.sha256
    sample_ids = {0,n//2,n-1,216,6269,6472,114717}
    row_bytes = 0
    for ordinal in range(n):
        start = p
        # Loader selector is not used by this factory case. Reject nonzero as
        # out-of-observed-domain, not as an executable factory failure.
        check(p<len(raw), f'row {ordinal}: selector short read @{p}')
        if raw[p]:
            raise CheckError(f'row {ordinal}: selector {raw[p]} @{p} outside observed domain')
        p += 1
        body = p
        identity = None
        for tr in trace:
            w = tr['width']
            q = p+w
            if q>len(raw) or (tr['site']==cut_site and ordinal==cut_at):
                path = 'reader has no immediate bulk status check' if tr['site']==BULK else f'IO-result -> {FAIL:#x} (AL=false)'
                raise CheckError(f'row {ordinal}: short transfer @{p} width {w} site {tr["site"]:#x}; {path}')
            if tr['site']==BULK:
                identity = struct.unpack_from('<III',raw,p)
            p = q
        check(identity is not None, 'no identity sink')
        rdui, uid1, uid2 = identity
        # Run unsigned branch first; raw ordinal is tested independently of the possible overwrite.
        stored = rdui if rdui<10000001 else ordinal
        if not (stored==rdui==ordinal and uid1==uid2 and uid1 and uid1 not in uid_set):
            raise CheckError(f'row {ordinal}: identity at {p-12} raw={identity}, stored ordinal={stored}')
        uid_set.add(uid1)
        max_uid=max(max_uid,uid1);min_uid=min(min_uid,uid1)
        row_bytes+=p-start
        h=raw_hash(raw[body:p]).digest()
        update(struct.pack('<7I',ordinal,start,body,p,*identity)+h)
        if ordinal in sample_ids:
            samples.append({'ordinal':ordinal,'selector_start':start,'body_start':body,'body_end':p,
                            'identity':list(identity),'body_sha256':h.hex(),'wire_hex':raw[start:p].hex()})
    footer_at=p
    check(p+4<=len(raw),f'footer vector count short read @{p}')
    vec,=struct.unpack_from('<I',raw,p);p+=4
    # Observed domain only; nonzero would cause 3x4-byte helper transfers per element.
    check(vec==0,f'footer vector count {vec} at {footer_at} (outside observed domain)')
    check(p+5<=len(raw),f'footer tail short read @{p}')
    flag, high=struct.unpack_from('<BI',raw,p);p+=5
    check(flag==1 and high==max_uid and p==len(raw),f'footer @ {footer_at}: flag={flag}, last_u32={high}, max_uid={max_uid}, end={p}, len={len(raw)}')
    check(13+row_bytes+9==len(raw), 'cursor accounting')
    return {'row_count':n,'row_bytes':row_bytes,'wire_origin':13,'legacy_origin':14,'wire_footer_start':footer_at,
            'legacy_footer_start':footer_at+1,'wire_footer_hex':raw[footer_at:].hex(),'legacy_footer_hex':raw[footer_at+1:].hex(),
            'header_hex':raw[:13].hex(),'footer_values':[vec,flag,high], 'uid_min':min_uid,'uid_max':max_uid,
            'row_trace_sha256':digest.hexdigest(),'samples':samples}


def reject(f):
    try:
        f()
    except CheckError as exc:
        return str(exc)
    raise CheckError('negative path accepted')


def archives():
    os.environ['FM24_DB_DIR'] = str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader()
    result = {}
    for a in ('client','server'):
        name=a+'_db.dat'; fp=db.DB_DIR/name
        directory=codec['list_tables'](fp,name)
        e=[v for v in directory if v['table_id']==37]
        result[a]={'directory_entry_count':len(directory),'archive_sha256':sha(fp.read_bytes()),
                   'table37_entries':e,'present':bool(e)}
    check(not result['client']['present'] and len(result['server']['table37_entries'])==1, 'archive presence')
    result['client'].update({'row_count':None,'stride':None,'payload_sha256':None})
    raw=db.load_payload(codec,'server',37)
    e,=result['server']['table37_entries']
    check(e['size']==len(raw) and struct.unpack_from('<HI',raw,6)==(e['payload_version'],e['record_count_header']), 'server entry header')
    result['server'].update({'payload_sha256':sha(raw),'payload_len':len(raw)})
    # Auxiliary read-only target domain; no table25 field promotion.
    comp=db.load_payload(codec,'client',25)
    cn,=struct.unpack_from('<I',comp,8)
    check(cn==7047 and len(comp)==14+cn*127+8,'comp target framing')
    ids={struct.unpack_from('<I',comp,14+127*i+114)[0] for i in range(cn)}
    check(ids==set(range(cn)),'comp target ordinal domain')
    return result, raw, ids, {'archive':'client','id':25,'count':cn,'payload_sha256':sha(comp),'ordinal_legacy_offset':114}


def legacy_profile(raw, s):
    check((ROOT/T29).is_file(), 't29 table37 profile is required for this frozen build')
    source=load(T29); p=source['payload']; c=source['row_closure']
    check(source['table_type']==37 and p['payload_sha256']==sha(raw) and p['payload_size']==len(raw)
          and (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'])==(s['row_count'],s['stride'],14,s['legacy_footer_start'])
          and c['rows_sha256']==sha(raw[14:s['legacy_footer_start']]),'t29 same-payload framing differential')
    notes={'profile':T29,'sha256':sha((ROOT/T29).read_bytes()),'legacy_rows_sha256':c['rows_sha256'],
           'usage':'consume t29 stride/profile, compare unsigned distributions of walked fields; no re-dump'}
    if (ROOT/INV).is_file():
        r, = [x for x in load(INV)['parents'] if x['parent_4cc']=='Clhs']
        check((r['table_type'], r['count'], r['stride'])==(37,s['row_count'],s['stride']), 't29 inventory frame')
        notes['inventory']={'path':INV,'status':r['status'],'candidate_fields':len(r['item_field_candidates']),
                            'usage':'scout only; candidate column suggestions do not set field grades'}
    else:
        notes['inventory']=None
    return {(v.get('offset'),v.get('width')):v for v in source['columns'] if v.get('interpretation') in ('u8','u16','u32')}, notes


def ledger(st,raw,s,ts,ids,cols,domain):
    master=load(MASTER)
    parent, = [x for x in master['entities']['club.xml'][0]['fields'] if x['field']=='Clhs']
    specs=parent['list_item_fields']
    inv=[x for fn in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for x in load(fn)['nested_fields'] if x['parent']=='Clhs']
    check(len(specs)==len(inv)==len(GETTER)==12,'12 scoped occurrences')
    check(len({v['field'] for v in specs})==len(specs),'duplicate occurrence')
    fields=[]
    n, stride=s['row_count'],s['stride']
    for spec, occurrence in zip(specs,inv):
        code=spec['field']
        check((code,spec['name'],spec['type'])==(occurrence['code'],occurrence['name'],occurrence['type']), 'scope occurrence mismatch')
        g=st.getter_path(code)
        tr,=[t for t in ts if t.get('object_offset')==g['object_offset']]
        o,w=tr['legacy_offset'],tr['width']
        check((w,g['width'])==((4,8) if code=='divi' else (w,w)),'getter/reader width')
        typ=spec['type']
        fmt={(1,True):'<b',(2,True):'<h',(2,False):'<H',(4,True):'<i'}[w,code!='year']
        counter, bad=Counter(),[]
        matched=0
        sentinel=0 if code=='orde' else -1 if spec.get('is_optional')=='true' else None
        bounds=None if code=='divi' else [int(spec[k]) for k in ('min_value','max_value')]
        check(typ == ('database_record_unique_id' if code=='divi' else 'integer'), 'unexpected schema type')
        for i in range(n):
            at=14+stride*i+o
            v,=struct.unpack_from(fmt,raw,at)
            counter[v]+=1
            valid=(v==sentinel or (v in ids if code=='divi' else bounds[0]<=v<=bounds[1]))
            matched+=valid
            if not valid and len(bad)<5:
                bad.append({'row':i,'value':v,'offset':at,'hex':raw[at:at+w].hex()})
        unsigned={v% (1<<(w*8)):k for v,k in counter.items()}
        old=cols[o,w]
        t29_stats=[old[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
        check(t29_stats==[n,len(unsigned),min(unsigned),max(unsigned),unsigned.get(0,0),unsigned.get((1<<(w*8))-1,0)],f't29 unsigned differential {code}')
        promote=matched==n
        fields.append({'schema_scope':[*SCOPE,occurrence['idx']], 'code':code,'name':spec['name'],'schema':spec,
                       'grade':'L3_named_row_coordinate' if promote else 'held_static_sink_profile_conflict',
                       'row_offset':o if promote else None, 'wire_offset':tr['wire_offset'] if promote else None,
                       'candidate_sink':{'legacy_offset':o,'wire_offset':tr['wire_offset'],'width':w,'reader_site':tr['site'],
                                         'object_offset':tr['object_offset']}, 'getter':g,
                       'profile':{'count':n,'distinct':len(counter),'min':min(counter),'max':max(counter),'sentinel':sentinel,
                                  'sentinel_count':counter[sentinel], 'zero_count':counter[0], 'matches':matched,'violations':n-matched,
                                  'bounds':bounds,'first_violations':bad,'t29_unsigned_stats':t29_stats,
                                  'samples':{str(i):struct.unpack_from(fmt,raw,14+i*stride+o)[0] for i in (0,n//2,n-1)}}})
    return {'table_type':37,'scope':SCOPE,'occurrences':12,'baseline_L3':0,'L3':sum(f['grade'].startswith('L3') for f in fields),
            'L4':0,'fields':fields,'reference_domain':domain,'date_fields':0,
            'negative_policy':'Strict frozen XML ranges plus getter-proven optional sentinel; no clipping, unsigned reinterpretation, or global relabeling on conflict.'}


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    st=Static()
    support=st.scope_support()
    active, cond=st.layout(True)
    skip, skip_cond=st.layout(False)
    archives_out, raw, ids, domain=archives()
    s=archives_out['server']
    s.update(walk(raw,active))
    w=1+sum(t['width'] for t in active)
    s.update({'stride':w,'mode':True,'mode_source':'unique archive-consistent fork, not a wire flag',
              'negative_forks':[{'mode':False,'conditions':skip_cond,'consumed_per_reader':sum(t['width'] for t in skip),
                                 'first_counterexample':reject(lambda:walk(raw,skip))}],
              'stream_failure_examples':[{'site':t['site'], 'first_counterexample':reject(lambda t=t:walk(raw,active,cut_site=t['site']))} for t in active],
              'footer_transfers':[{'site':site,'offset':s['wire_footer_start']+delta,'width':width,'value':value}
                                  for site,delta,width,value in zip(FOOT,(0,4,5),(4,1,4),s['footer_values'],strict=True)],
              'row_template':{'id':0,'condition_edges':cond,'wire_selector':'13+40*i','legacy_body':'14+40*i',
                              'body_end_exclusive':'53+40*i','trace_digest_record':'LE <7I>(i, selector, body, end, identity0, identity1, identity2) then 32 raw SHA-256 bytes of body'}})
    check(s['row_count']*w==s['row_bytes'] and w==40,'closed stride')
    cols, t29=legacy_profile(raw,s)
    ts=[]; wire=1
    for t in active:
        ts.append({**t,'wire_offset':wire,'legacy_offset':wire-1})
        wire+=t['width']
    check(wire==w,'transfer geometry')
    fields=ledger(st,raw,s,ts,ids,cols,domain)
    branches=[]
    for site,b in st.branches.items():
        visited=dict(cond).get(site)
        branches.append({**b,'scope':'reader','taken':s['row_count'] if visited is True else 0,'fallthrough':s['row_count'] if visited is False else 0})
    for b in st.wrapper.values():
        branches.append({**b,'scope':'loader_or_footer_slice'})
    cursor={'status':'complete_observed_row_cursor_partial_runtime_only_edges','table_type':37,'scope':SCOPE,
            'provenance':{'editor':str(EDITOR),'editor_sha256':EXE_SHA,'snapshot_manifest':st.prov},
            'factory':st.factory,'rtti':st.rtti,'slots':st.slots,
            'reader':{'thunk':st.pe.va2f(SLOT),'entry':START,'entry_VA':hex(st.pe.f2va(START)),
                      'end_exclusive':st.cfg.function_end_off,'end_exclusive_VA':hex(st.pe.f2va(st.cfg.function_end_off)),
                      'extent_source':'PE exception directory RUNTIME_FUNCTION','blocks':st.blocks(),
                      'instruction_count':len(st.reader_sites),'condition_count':len(st.branches),'external_edges':st.cfg.external_edges},
            'scope_evidence':support,'archives':archives_out,'t29':t29,
            'transfers':[{'site':SELECT,'wire_offset':0,'legacy_offset':-1,'width':1,'sink':'loader stack+0x43'},*ts],
            'loader_transfers':st.wrapper_transfers,
            'wire_alignment':'13 + 465712*(1+27+12) + 9 = 18628502',
            'legacy_alignment':'14 + 465712*40 + 8 = 18628502; legacy +39 is next selector/first footer byte',
            'framing_policy':'Header prefix 8 is archive marker/version; selector 0 and footer zero vector are observed specialization, not unconditional native constraints.',
            'branch_taxonomy':['wire_data','runtime-external','IO-result','context-lifecycle','dead'],
            'branch_census':dict(Counter(b['class'] for b in branches)),
            'unscoped_member_sinks':[{'legacy_offset':4,'wire_offset':5,'width':4,'object_offset':32,'note':'collection getter uses object+0x20 after fixup; no nested 4CC'},
                                     {'legacy_offset':8,'wire_offset':9,'width':4,'object_offset':40,'note':'writer/fixup indicate reference-like object member; no nested 4CC'}],
            'limits':['No branch in the reader itself erased as dead. R9 is not consulted. The two opaque indirect calls in reader are table callback (no stream passed) and terminal owner release (not visited on retained-owner path).',
                      'Nonnull stream and owning wrapper are caller contracts, not alternative data layouts. In property mode null stream already dereferences before the tail guard; mode=0 null would skip identity read and cannot satisfy archive postconditions.',
                      'Identity bulk has no immediate status test in slot19. Short read is rejected by verifier/cursor; do not equate this with native AL=false. Footer/loader slice does not enumerate generic allocation/setup branches.',
                      'Observed footer last u32 equals max of duplicate UID lanes, not record count; not an asserted invariant for future payloads.'],
            'branch_shards':shards('branches',branches,30),
            'instruction_shards':shards('instructions',[st.records[o] for o in sorted(st.records)],130)}
    write('cursor_clhs.json',cursor)
    write('fields_clhs.json',fields)
    print(f"t30 build PASS: {s['row_count']} x {s['stride']}B; {fields['L3']}/12 L3, {12-fields['L3']} held, L4=0")


def selftest():
    h=bytes.fromhex('03017461642ef10d0100000000')
    raw=h+b'\0'+struct.pack('<IIIIBI',0,5,5,0,1,5)
    t=[{'site':BULK,'width':12}]
    check(walk(raw,t)['wire_footer_start']==26,'synthetic cursor')
    for x in (raw[:-1],h+b'\x01'+raw[14:],raw[:14]+b'\xff'*4+raw[18:]):
        reject(lambda:walk(x,t))
    check('no immediate bulk status check' in reject(lambda:walk(raw,t,cut_site=BULK)), 'bulk negative')
    print('t30 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test synthetic walk and rejections')
    args=p.parse_args()
    try:
        selftest() if args.selftest else build()
        return 0
    except CheckError as e:
        print(f't30 check failed: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,struct.error) as e:
        print(f't30 fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
