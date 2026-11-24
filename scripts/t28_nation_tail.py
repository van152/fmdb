#!/usr/bin/env python3
"""Symbolically replay the ordinary FM24 nation client reader (read-only)."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t28/out'
EDITOR = ROOT.parent / 'fm24/input/editor.exe'
DATA = Path(str(_cfg.DATA_DIR))
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
BASE = ROOT / 'scratch/t25/out'
T01 = ROOT / 'scratch/t01/inbox/t01g/output.json'
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MEMBER_SHA = '7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34'
ENTRY, FAIL, VT = 0x103fac0, 0x1040930, 0x1418893b8
DATE, ID = 0x39dd7b0, 0x3c600f0
# count read, signed loop gate, item call, increment-test backedge, vector address,
# item thunk, native helper, in-memory item stride, parent (scoped schema)
SETS = {
    'A': (0x1040717,0x104073b,0x104075b,0x1040779,0x48,0x105fb50,0x3d87700,16,'Nlns'),
    'B': (0x10407b0,0x10407d6,0x1040829,0x1040847,0xa8,0x15cf4a0,0x448fa90,48,'Nefr'),
    'C': (0x104086c,0x1040898,0x10408eb,0x1040908,0x90,0x15cf4a0,0x448fa90,48,'Nnfr'),
    'D': (0x1040927,0x1040980,0x10409a7,0x10409c9,0xc0,0x105fbb0,0x3d88300,16,'Nagr'),
}
# native stream read, width setup, sink setup, item object displacement
ITEM = {
    0x3d87700: [(0x3d8771f,0x3d87713,0x3d8771c,0),(0x3d87742,0x3d87736,0x3d8772f,8)],
    0x448fa90: [(a,b,c,n*8) for n,(a,b,c) in enumerate([
        (0x448faaf,0x448faa3,0x448faac),(0x448facf,0x448fac6,0x448fabf),
        (0x448faeb,0x448fae2,0x448fadb),(0x448fb07,0x448fafe,0x448faf7),
        (0x448fb23,0x448fb1a,0x448fb13)])],
    0x3d88300: [(0x3d88320,0x3d88314,0x3d8831d,0),(0x3d88345,0x3d8833c,0x3d88331,8),
                (0x3d8838c,0x3d88380,0x3d88375,12)],
}
PARENT = {
    'A': [0x1042216,0x104221c,0x1042f01,0x1042f06,0x1042f0b,0x1043490,0x104349d,0x10434ac,0x10434c5],
    'B': [0x1042047,0x104204d,0x1042053,0x1042057,0x104205b,0x1042252,0x104efb0,0x3d75bff,0x3d75c03,0x3d75c0a,0x3d75d99,0x3d75dc0,0x3d75dcc,0x3d75dd0,0x3d75ddb,0x3d75dff],
    'C': [0x104222e,0x1042234,0x104223a,0x104223e,0x1042252,0x104efb0,0x3d75bff,0x3d75c03,0x3d75c0a,0x3d75dc7,0x3d75dcc,0x3d75dd0,0x3d75ddb,0x3d75dff],
    'D': [0x10426c4,0x10426ca,0x104357d,0x1043591,0x104f500,0x3d763da,0x3d765a3,0x3d765b7,0x3d765bb,0x3d765d4],
}
# In wire order within each item. Repeated 4CCs are scoped by parent.
CODES = {'A': ('lang','perc'), 'B': ('nfrn','nfrc','fren','nfrr','nfra','stdt','endt'),
         'C': ('nfrn','nfrc','fren','nfrr','nfra','stdt','endt'), 'D': ('NGag','NGsd','NGed')}
GET = {
    'lang': [0x3da2790,0x3da29ef,0x3da29f5,0x3da29f7,0x3da2a80,0x3da2a88],
    'perc': [0x3da27c0,0x3da29e7,0x3da29ed,0x3da2a0c],
    'nfrn': [0x448fd30,0x15cf935,0x15cf940,0x15cf947,0x15cf94b,0x15cf94e,0x15cfa72],
    'nfrc': [0x448fd60,0x15cf935,0x15cf940,0x15cf947,0x15cf94b,0x15cf94e,0x15cfa4d,0x15cfa6b],
    'fren': [0x448fd90,0x15cf988,0x15cf98e,0x15cf994,0x15cfa8f],
    'nfrr': [0x448fdc0,0x15cf935,0x15cf940,0x15cf947,0x15cf94b,0x15cf94e,0x15cfa96,0x15cfab4],
    'nfra': [0x448fdf0,0x15cf935,0x15cf940,0x15cf947,0x15cf94b,0x15cf94e,0x15cf950,0x15cf972],
    'stdt': [0x448fe20,0x15cf9a6,0x15cf9ac,0x15cf9d7,0x15cf9dd,0x15cf9e6],
    'endt': [0x448fe50,0x15cf97c,0x15cf982,0x15cfb22,0x15cfb28,0x15cfb31],
    'NGag': [0x3d9f3a0,0x3da09cb,0x3da09d1,0x3da09d7,0x3da0b46],
    'NGsd': [0x3d9f3d0,0x3da09b7,0x3da09bd,0x3da09f3,0x3da0a20,0x3da0a25,0x3da0a2e],
    'NGed': [0x3d9f400,0x3da09bf,0x3da09c5,0x3da0a92,0x3da0abf,0x3da0ac4,0x3da0acd],
}
GET_LINK = {'A':[0x104eb50,0x3d753b2,0x10707d0,0x3d75478,0x1070890],
            'B':[0x104f2d0,0x3d760e2,0x15cf6c0,0x3d761a8],
            'D':[0x104f800,0x3d769d2,0x1070010,0x3d76a98,0x1070120]}
REFS = {'continent':5, 'language':8, 'nation':10, 'region':19, 'currency':41, 'agreement':56}
FOOTER = bytes.fromhex('0000000001ec7ae404')


class Check(Exception):
    pass


def need(condition, msg):
    if not condition:
        raise Check(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=True, indent=1) + '\n', encoding='utf-8')


def shards(stem, data, size=135):
    paths = []
    for i in range(0, len(data), size):
        name = f'{stem}.part{i//size+1:03d}.json'
        dump(name, data[i:i+size])
        paths.append({'file':name,'records':len(data[i:i+size]),'sha256':sha((OUT/name).read_bytes())})
    return paths


def archive(path):
    # Original read-only codec; no cached standalone member, no server archive.
    sys.path.insert(0, str(ROOT.parent/'fm24/scripts'))
    import modding_read_dbdat as dat
    packed, layout = dat._read_archive(path)
    payloads, entries = {}, {}
    for name, n in REFS.items():
        key = f'client_db/table_{n}.dat'
        e, = (x for x in layout['entries'] if x['path'] == key)
        b = dat._decompress_entry(packed, layout['data_base'], e)
        need(b[:8] == b'\x03\x01tad.\xf1\x0d', f'header {key}')
        entries[name] = {'table_id':n,'member':key,'count':struct.unpack_from('<I',b,8)[0],
                         'bytes':len(b),'sha256':sha(b)}
        payloads[name] = b
    need(sha(payloads['nation']) == MEMBER_SHA, 'unexpected nation payload revision')
    return payloads['nation'], entries, sha(packed)


class Static:
    def __init__(self, editor):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t21b_control_flow import ReaderCFG
        self.pe = PE(editor)
        need(sha(self.pe.raw) == EXE_SHA, 'wrong editor image')
        self.pe.pe.parse_data_directories(directories=[3])
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.records, self.cfg, self.succ, self.branch, self.t = {}, {}, {}, {}, {}
        functions = {ENTRY:'NATION reader', DATE:'packed date reader', ID:'base identity reader',
                     0x3d5ed90:'A/D vector reserve',0x8931e0:'B/C vector reserve',
                     0x36d4be0:'A append',0x36b5f20:'B/C append',0x3d5f790:'D indexed copy',
                     0x3d5fd80:'post-D in-memory Ntxr housekeeping'}
        functions.update({v[6]:f'item {k if k not in "BC" else "B/C"}' for k,v in SETS.items()})
        for f, label in functions.items():
            cfg = ReaderCFG(self.pe, self.md, f)
            ins = {self.pe.va2f(a):i for a,i in cfg.instructions.items()}
            succ = {self.pe.va2f(a):[self.pe.va2f(b) for b in bs] for a,bs in cfg.successors.items()}
            self.succ.update(succ)
            self.add(*ins)
            blocks, seen = [], set()
            leaders = {f} | {b for a,i in ins.items() if i.mnemonic.startswith('j') for b in succ[a]}
            for first in sorted(leaders):
                groups, pc = [], first
                while True:
                    need(pc not in seen, f'block overlap {pc:#x}')
                    seen.add(pc)
                    groups.append(pc)
                    ns = succ[pc]
                    if len(ns) != 1 or ns[0] in leaders or ins[pc].mnemonic.startswith('j'):
                        break
                    pc = ns[0]
                blocks.append({'start':first,'instructions':groups,'successors':ns})
            need(seen == set(ins), f'CFG coverage at {f:#x}')
            self.cfg[f] = {'label':label,'file_offset':f,'va':self.pe.f2va(f),'end_exclusive':cfg.function_end_off,
                           'external_edges':cfg.external_edges,'blocks':blocks}
            preds = defaultdict(list)
            for a, bs in succ.items():
                for b in bs:
                    preds[b].append(a)
            for a, i in ins.items():
                if not (i.mnemonic.startswith('j') and i.mnemonic != 'jmp'):
                    continue
                prev, prod = a, None
                while len(preds[prev]) == 1:
                    pp = preds[prev][0]
                    pi = ins[pp]
                    if pp+pi.size != prev or pi.mnemonic == 'call':
                        break
                    if pi.eflags:
                        prod = pp
                        break
                    prev = pp
                cls, src = self.classify(f, a, ins.get(prod))
                self.branch[a] = {'site':a,'function':f,'predicate':prod,'class':cls,'source':src,
                                  'taken':self.edge(a),'not_taken':a+i.size}
        self.setup()

    def ins(self, n):
        va = self.pe.f2va(n)
        need(va is not None and self.pe.va2f(va) == n, f'PE roundtrip {n:#x}')
        return next(self.md.disasm(self.pe.raw[n:n+15], va, count=1))

    def add(self, *sites):
        for n in sites:
            if n not in self.records:
                i = self.ins(n)
                self.records[n] = {'file_offset':n,'VA':i.address,'bytes':i.bytes.hex(),
                                   'instruction':(i.mnemonic+' '+i.op_str).rstrip()}
        return list(sites)

    def edge(self, site):
        return self.pe.va2f(self.ins(site).operands[0].imm)

    def classify(self, fn, a, i):
        if a in (0x103fae6,0x10409d3):
            return 'runtime_external', 'same caller stack mode byte [rsp+0x120], not row selector; ordinary enters and skips extra block'
        if a in (0x103fc81,0x103ff58) and fn == ENTRY:
            return 'unresolved', 'outside modeled arg8=0 path; no archive binding'
        if a in {v[j] for v in SETS.values() for j in (1,3)}:
            return 'wire_data', 'signed count from last count stream read; compare with zero or loop index'
        if a == 0x104078d:
            return 'wire_data', 'derived vector length (end-begin==16), equals one item for newly constructed NATION; writes percentage=100, consumes zero'
        if a == 0x3c60131:
            return 'wire_data', 'just-read identity ordinal vs 10000001; otherwise replace with caller ordinal'
        if a in (0x39dd7bc,0x3d8832f,0x3d88373):
            return 'dead', 'taken NULL-stream edge then dereferences same null register; no valid-input return'
        pred = '' if i is None else i.op_str
        if i is not None and i.mnemonic == 'test' and pred == 'al, al' and self.ins(self.edge(a)).mnemonic == 'xor' and a in (0x1040762,0x1040830,0x10408f2,0x10409ae,0x448fb3a):
            return 'runtime_external', 'item/date helper success vs stream failure'
        if i is not None and '+ 0x10], 0' in pred:
            return 'runtime_external', 'stream status (runtime I/O)' if fn == ENTRY or fn in ITEM else 'runtime/container state'
        if a in (0x3d88360,0x3c60100,0x3c6013e,0x3c6014f,0x3c60155,0x39dd7de,0x3d8834f,0x3d88396,0x448fb3a):
            return 'runtime_external', 'stream success, callback presence, or wrapper reference count (see predicate instruction)'
        if i is not None and i.mnemonic == 'test' and pred in ('al, al','eax, eax') and self.ins(a).mnemonic == 'jne':
            prev = self.succ.get(a, [])
            if i.address-2 >= self.pe.f2va(fn) and self.pe.raw[self.pe.va2f(i.address)-2:self.pe.va2f(i.address)] == b'\x31\xc0' and len(prev) == 2:
                return 'dead', 'same block XOR EAX,EAX forces zero predicate; jne taken edge dead'
        if fn not in (ENTRY, DATE, ID, *ITEM):
            return ('runtime_external' if 'reserve' in self.cfg[fn]['label'] or 'append' in self.cfg[fn]['label'] or fn == 0x3d5f790 else 'unresolved',
                    'capacity/allocation/ownership state; no wire interpretation' if fn != 0x3d5fd80 else 'existing Ntxr vector/sort state, no wire interpretation')
        if fn == ENTRY and a < 0x10405b0:
            return 'unresolved', 'off-path arg8!=0 predicate; no archive binding'
        return 'unresolved', 'not reduced'

    def transfer(self, site, w, sink, obj, *, logical=None, setup=()):
        vi = self.ins(w)
        need(vi.mnemonic == 'mov' and vi.op_str.startswith('r8d, ') and vi.operands[1].type == 2, f'width at {w:#x}')
        need(self.ins(site).op_str.endswith(' + 0x28]'), f'not stream slot {site:#x}')
        sx = self.ins(sink)
        if obj is not None and sx.mnemonic in ('lea','add'):
            op = sx.operands[1]
            need((op.mem.disp if op.type == 3 else op.imm) == obj, f'sink at {sink:#x}')
        logical = site if logical is None else logical
        self.t[logical] = {'site':logical,'native_site':site,'width':vi.operands[1].imm,'object_off':obj,
                           'setup':self.add(sink,w,site,logical,*setup)}

    def setup(self):
        v = self.pe.va2f(VT)
        need(struct.unpack_from('<Q',self.pe.raw,v+19*8)[0] == self.pe.f2va(ENTRY), 'NATION reader slot')
        need(struct.unpack_from('<Q',self.pe.raw,v+2*8)[0] == self.pe.f2va(0x1041f30), 'NATION getter slot')
        self.add(0x103ec17,0x103ec1e,0x103ec90,0x103ec94,0x103ec9a,0x103ec9c,0xf48f37,0x1041f30,0x1041f33)
        calls = sorted(n for n in self.succ if ENTRY <= n < self.cfg[ENTRY]['end_exclusive']
                       and self.records[n]['instruction'].startswith('call qword ptr [')
                       and self.records[n]['instruction'].endswith('+ 0x28]'))
        need(len(calls) == 40, 'reader stream call census')
        self.calls = calls
        # The three same-width prefix negatives are intentionally not named here.
        dest = [0x1cb,0xf0,0xf8,0xe8,0x100,0x1cc,0x1d0,0x1b4,0x1cd,None,None,None,None]
        for site,obj in zip(calls[15:28],dest,strict=True):
            sink = {0x1040717:0x1040709,0x10407b0:0x10407a2,0x104086c:0x104085b,0x1040927:0x1040919}.get(site,site-19)
            need(self.ins(sink).mnemonic=='lea' and self.ins(sink).op_str.startswith('rdx, ['), f'row sink {sink:#x}')
            self.transfer(site,site-9,sink,obj)
        for site in calls[28:]:
            self.transfer(site,site-9,site-19,self.ins(site-19).operands[1].mem.disp)
        for k,v in SETS.items():
            count,_,item,_,_,thunk,b,_,_ = v
            need(self.edge(item)==thunk and self.edge(thunk)==b, f'item thunk {k}')
            self.add(thunk)
            for args in ITEM[b]:
                self.transfer(*args)
            need(self.t[count]['width'] == (1 if k == 'A' else 4), f'count {k}')
        for call,sink,obj in [(0x448fb33,0x448fb2c,40),(0x448fb4d,0x448fb3c,44)]:
            need(self.edge(call)==0xdb7f80 and self.edge(0xdb7f80)==DATE, 'date thunk')
            self.transfer(0x39dd7d4,0x39dd7c8,sink,obj,logical=call,setup=(0xdb7f80,0x39dd7be,0x39dd7d1))
        need(self.edge(0x1040bcf)==0xfae340 and self.edge(0xfae340)==ID,'identity thunk')
        self.transfer(0x3c60119,0x3c6010d,0x3c60106,8,setup=(0xfae340,0x1040bcf,0x3c60116))
        for a in (0x1040eb0,0x8c8d70,0x87eb40,0x1040ff0,0x1041050):
            need(self.edge(a) in self.cfg,'memory helper thunk')
        self.add(0x1040eb0,0x8c8d70,0x87eb40,0x1040ff0,0x1041050,0x10518b0,0x17502c0)
        self.add(0xf2b9f7,0xf2b9fa,0xf2ba02,0xf2ba0b,0xf2ba0e,0xf2ba1b,0xf2ba20,0xf2ba23,0xf2ba33,
                 0xf2ba38,0xf2ba3d,0xf2ba4e,0xf2ba51,0xf2ba7f,0xf2ba89,0xf2ba99,0xf2baa2,0xf2bab9,0xf2bac2,
                 0xffa5d0,0xffa5fc,0xffa602)
        for vals in (*PARENT.values(),*GET_LINK.values(),*GET.values()):
            self.add(*vals)
        self.jump_table = []
        jt = self.ins(0x15cf940)
        va = jt.address + jt.size + jt.operands[1].mem.disp
        base = self.pe.va2f(va)
        need(base == 0x15cfca8, 'nested getter jump table base')
        for code in ('nfrn','nfrc','nfrr','nfra'):
            loc = base + (int.from_bytes(code.encode(),'big')-0x6e667261)*4
            b = self.pe.raw[loc:loc+4]
            target = self.pe.va2f(va+struct.unpack('<i',b)[0])
            need(target in GET[code],f'{code} jump arm')
            self.jump_table.append({'code':code,'file_offset':loc,'VA':self.pe.f2va(loc),'bytes':b.hex(),'target':target})
        # A small set of fixed assumptions on the success path, keyed by PC.
        self.fixed = {0x103fae6:True,0x104092e:True,0x3d87726:True,0x3d88360:True,
                      0x3d8834f:True,0x3d88396:True,0x39dd7de:True,0x3c60155:True}
        for x in (0x3d8832f,0x3d88373,0x39dd7bc,0x3c60100,0x3c6013e,0x3c6014f,0x3d88327,0x448fb3a,
                  0x448fab6,0x448fad6,0x448faf2,0x448fb0e,0x448fb2a):
            self.fixed[x] = False
        for x, b in self.branch.items():
            if b['function']==ENTRY and x >= 0x10405b0 and b['taken']==FAIL:
                self.fixed[x] = False

    def item_transfers(self, k):
        body = SETS[k][6]
        keys = [t[0] for t in ITEM[body]]
        if k in 'BC':
            keys += [0x448fb33,0x448fb4d]
        off, records = 0, []
        for key in keys:
            t = self.t[key]
            records.append(dict(t,item_offset=off))
            off += t['width']
        return records


def select(d, pc, jump):
    return d.branch[pc]['taken' if jump else 'not_taken']


def walk(raw, st, *, extra=False):
    """Interpret the selected instruction graph; interpose only at transfer/call events."""
    need(raw[:8] == b'\x03\x01tad.\xf1\x0d' and len(raw) >= 22 and raw[12] == 0, 'bad member header')
    n, = struct.unpack_from('<I', raw, 8)
    p, rows, outcomes, values, identities = 13, [], Counter(), defaultdict(list), set()
    heads = {v[0]:k for k,v in SETS.items()}
    gates = {v[1]:k for k,v in SETS.items()}
    items = {v[2]:k for k,v in SETS.items()}
    backs = {v[3]:k for k,v in SETS.items()}
    for row in range(n):
        def take(nbytes, site):
            nonlocal p
            need(nbytes>0 and p+nbytes<=len(raw), f'row {row}: short read at {p:#x}, site {site:#x}')
            data = raw[p:p+nbytes]
            p += nbytes
            return data

        front = p
        need(take(1,0xf2ba0e) == b'\0', f'row {row}: selector at {front:#x}')
        origin = p
        identity = None
        count, count_offsets, it_start, idx, trace = {}, {}, {}, {}, []

        def run(start, *, key=None, logical=None):
            nonlocal identity
            pc = start
            for _ in range(120000):
                if pc == FAIL:
                    raise Check(f'row {row}: reader error')
                if pc in items:
                    k = items[pc]
                    before = p
                    run(SETS[k][6],key=k)
                    size = sum(t['width'] for t in st.item_transfers(k))
                    need(p-before == size,f'row {row}: item {k} consumes {p-before}')
                elif pc in (0x448fb33,0x448fb4d):
                    run(DATE,key=key,logical=pc)
                    if pc == 0x448fb4d:  # tail jump
                        return
                elif pc == 0x1040bcf:
                    run(ID)
                elif pc in st.t or pc == 0x39dd7d4:
                    t = st.t[logical or pc]
                    off = p
                    b = take(t['width'],pc)
                    trace.append((logical or pc,off-origin,t['width']))
                    if pc in heads:
                        k = heads[pc]
                        count[k] = int.from_bytes(b,'little',signed=True)
                        need(count[k]>=0, f'row {row}: negative {k} count')
                        count_offsets[k], it_start[k], idx[k] = off,p,0
                    if pc == 0x3c60119:
                        identity = struct.unpack('<III',b)
                    if key:
                        rel = off-it_start[key]-idx[key]*sum(t['width'] for t in st.item_transfers(key))
                        values[key,rel].append((row,idx[key],off,b))
                if pc in st.branch:
                    if pc in gates:
                        jump = count[gates[pc]] <= 0
                    elif pc in backs:
                        k = backs[pc]
                        idx[k] += 1
                        jump = idx[k] < count[k]
                    elif pc == 0x104078d:
                        jump = count['A'] != 1
                    elif pc == 0x10409d3:
                        jump = not extra
                    elif pc == 0x3c60131:
                        jump = identity[0] < 10000001
                    else:
                        need(pc in st.fixed, f'unmodeled executed branch {pc:#x}')
                        jump = st.fixed[pc]
                    outcomes[pc,jump] += 1
                    pc = select(st,pc,jump)
                    continue
                edges = st.succ[pc]
                if not edges:
                    need(st.records[pc]['instruction']=='ret', f'path cut at {pc:#x}')
                    return
                need(len(edges)==1, f'ambiguous successor at {pc:#x}')
                pc = edges[0]
            raise Check(f'row {row}: instruction budget exceeded')

        run(ENTRY)
        need(identity is not None and identity[0] == row and identity[1] == identity[2],
             f'row {row}: identity postcondition at {p-12:#x}: {identity}')
        need(identity[1] not in identities, f'row {row}: duplicate DUNI')
        identities.add(identity[1])
        need(idx == count and sum(x[2] for x in trace)==p-origin, f'row {row}: trace coverage')
        rows.append({'row':row,'selector_at':front,'body_start':origin,'end_before_next_selector':p,
                     'counts':count,'count_at':count_offsets,'items_at':it_start,'identity_at':p-12,
                     'identity':list(identity),'body_sha256':sha(raw[origin:p]),'transfer_count':len(trace)})
    need(raw[p:]==FOOTER, f'footer / EOF mismatch at {p:#x}')
    return rows, outcomes, values, p


def profile(samples, schema, targets):
    values = [int.from_bytes(t[3], 'little') for t in samples]
    c = Counter(values)
    n = len(values)
    out = {'n':n,'distinct':len(c),'min':min(c),'max':max(c),'histogram':[[k,c[k]] for k in sorted(c)],
           'samples':[list(samples[i][:3])+[samples[i][3].hex()] for i in sorted({0,n//2,n-1})]}
    typ = schema['type']
    if typ == 'database_record_unique_id':
        target = schema['database_table_type']
        size = targets[target]['count']
        nullable = schema.get('is_optional')=='true'
        live = [v for v in values if v != 0xffffffff]
        ok = [0<=v<size or (nullable and v==0xffffffff) for v in values]
        out.update(target=target,target_table_id=targets[target]['table_id'],ordinal_domain=[0,size-1],
                   null_count=n-len(live),live_bounds=[min(live),max(live)] if live else None)
    elif typ == 'integer':
        lo,hi = int(schema['min_value']),int(schema['max_value'])
        ok = [lo<=v<=hi for v in values]
        out['schema_bounds'] = [lo,hi]
    elif typ == 'date':
        from calendar import isleap
        ds = [(v>>16,v&0x1ff,(v>>9)&127) for v in values]
        # Packed date getter separates the intra-day bits; don't assume all low16 are day.
        ok = [1<=y<=9999 and 1<=d<=365+isleap(y) for y,d,_ in ds]
        out.update(years=sorted(Counter(y for y,_,_ in ds).items()),day_range=[min(d for _,d,_ in ds),max(d for _,d,_ in ds)],
                   intraday_codes=sorted({t for _,_,t in ds}),default_1900_001=c[0x076c0001])
    else:
        raise Check(f'unsupported profile type: {typ}')
    out['matches'] = sum(ok)
    out['violations'] = [list(t[:3])+[t[3].hex()] for t, valid in zip(samples,ok,strict=True) if not valid]
    return out


def count_profile(rows, k):
    c = Counter(r['counts'][k] for r in rows)
    return {'rows':len(rows),'min':min(c),'max':max(c),'total':sum(n*f for n,f in c.items()),'histogram':sorted(c.items())}


def build(editor, data):
    manifest = {x['path']:x['sha256'] for x in load(ROOT/'evidence/MANIFEST.json')['files']}
    for source in (MASTER,PROV):
        need(sha((ROOT/source).read_bytes())==manifest[source], f'snapshot manifest mismatch {source}')
    need(EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'), 'editor provenance absent')
    st = Static(editor)
    raw, targets, archive_sha = archive(data/'client_db.dat')
    rows, hit, values, foot = walk(raw,st)
    old = load(BASE/'cursor_nation.json')
    need(len(rows)==251 and foot==24723 and len(raw)==24732, 'closure changed')
    for new, prev in zip(rows,old['rows'],strict=True):
        need(new['body_start']==prev['row_start_payload'] and new['counts']==prev['counts']
             and new['count_at']==prev['count_offsets_payload'] and new['identity_at']==prev['identity_payload']
             and new['end_before_next_selector']==prev['marker_payload'] and new['identity'][1]==prev['row_id'],
             f't25 differential row {new["row"]}')
    try:
        walk(raw,st,extra=True)
    except Check as exc:
        mode_counterexample = str(exc)
    else:
        raise Check('forced extra-tail control accepted')
    need(mode_counterexample.startswith('row 0: identity postcondition'), mode_counterexample)
    split = load(BASE/'schema_split.json')['classified_fields']
    originals = load(ROOT/MASTER)['entities']['nation.xml'][0]['fields']
    known = load(BASE/'fields_nation.json')['mapping_evidence']['fields']
    directs = split['client_direct']; nested = split['client_inherited_list_items']
    need((len(directs),len(nested),len(split['unknown_unmarked']))==(21,28,392), 'schema tally')
    need([f['field'] for f in originals if f.get('is_client_field')=='true']==[x['code'] for x in directs], 'direct inventory changed')
    count_expr = ['24','25+5*A','29+5*A+28*B','33+5*A+28*B+28*C']
    item_expr = ['25','29+5*A','33+5*A+28*B','37+5*A+28*B+28*C']
    cols, bound = {}, {}
    for i,(k,v) in enumerate(SETS.items()):
        ct,gate,call,back,obj,thunk,body,mem,parent = v
        inst = st.item_transfers(k)
        stride = sum(t['width'] for t in inst)
        cp = count_profile(rows,k)
        need((stride,cp['total'],cp['max']) == [(5,492,7),(28,214,40),(28,63,21),(12,162,2)][i], f'collection {k}')
        children = {x['field']:x for x in next(f for f in originals if f['field']==parent)['list_item_fields']}
        need(set(children)==set(CODES[k]), f'scoped schema {k}')
        bridge = {'A':[0x1040724,0x1040728,0x1040731,0x1040747,0x1040755,0x1040758,0x104076e,0x36d4be3],
                  'B':[0x10407bd,0x10407c4,0x10407cc,0x1040823,0x1040826,0x104083c],
                  'C':[0x1040879,0x1040880,0x104088b,0x10408e5,0x10408e8,0x10408fa],
                  'D':[0x1040967,0x104096e,0x1040976,0x1040993,0x10409a1,0x10409a4,0x10409b9,0x3d5f7c7,0x3d5f7d2,0x3d5f7d7]}[k]
        cols[k] = {'parent':parent,'object_off':obj,'getter_chain':PARENT[k],'wire_stride':stride,'item_object_stride':mem,
                   'count':dict(st.t[ct],row_offset=count_expr[i],signed=True,profile=cp), 'items_row_offset':item_expr[i],
                   'gate':gate,'loop_backedge':back,'item_call':call,'item_thunk':thunk,'item_body':body,
                   'reader_to_object':st.add(*bridge),'item_transfers':inst}
        for code,t in zip(CODES[k],inst,strict=True):
            r = t['item_offset']
            schema = children[code]
            pf = profile(values[k,r],schema,targets)
            need(pf['n']==cp['total'],'profile sample count')
            t['scoped_field'] = f'{parent}/{code}'
            bound[parent,code] = {'grade':'L3' if not pf['violations'] else 'candidate','row_offset':f'{item_expr[i]}+{stride}*j+{r}',
                                   'item_offset':r,'width':t['width'],'object_off':t['object_off'],'profile':pf,
                                   'collection':k,'reader_sites':[call,t['site'],t['native_site']],
                                   'getter_chain':PARENT[k]+GET_LINK['B' if k=='C' else k]+GET[code]}
        bound[None,parent] = {'grade':'L3' if all(bound[parent,c]['grade']=='L3' for c in children) else 'candidate',
                              'row_offset':count_expr[i],'width':st.t[ct]['width'],'width_semantics':'count only; variable list span',
                              'object_off':obj,'profile':cp,'collection':k,'getter_chain':PARENT[k],'reader_sites':[ct,call]}
    single_a = Counter(raw[r['items_at']['A']+4] for r in rows if r['counts']['A']==1)
    bound['Nlns','perc']['post_read_normalization'] = {
        'branch':0x104078d,'store':0x104078f,'wire_histogram_for_single_item_rows':sorted(single_a.items()),
        'rows_with_single_item':sum(single_a.values()),'rows_with_changed_object_value':sum(single_a.values())-single_a[100],
        'stored_object_value':100}
    dep = {}
    for k in 'BC':
        per_item = Counter((row,i) for off in range(0,20,4) for row,i,_,b in values[k,off] if b != b'\xff'*4)
        dep[k] = dict(Counter(per_item.values()))
        need(sum(per_item.values()) == len(per_item) == cols[k]['count']['profile']['total'], f'{k} selector exclusivity')
    for f in directs:
        code = f['code']
        if code in known:
            oldf = known[code]; off,width = oldf['row_offset'],oldf['width']
            schema = next(x for x in originals if x['field']==code)
            rr = [(r['row'],None,r['body_start']+off,raw[r['body_start']+off:r['body_start']+off+width]) for r in rows]
            pf = profile(rr,schema,targets)
            need(not pf['violations'],f'inherited anchor profile {code}')
            gets = st.add(*(int(x['file_offset'],16) for x in oldf['getter'].values() if isinstance(x,dict)))
            rd = st.add(*(int(x['file_offset'],16) for x in oldf['reader'].values()))
            bound[None,code] = dict(grade='L3',inherited='t01g/t25',row_offset=off,width=width,object_off=int(oldf['object_offset'],16),
                                   getter_chain=gets,reader_sites=rd,profile=pf)
    lang_candidates = {'Nnam':0x1042222,'Nsnm':0x104225c,'N3ln':0x10420a1,'Nnty':0x1041f9c}
    ledger = []
    for f in directs+nested:
        k = f['parent'], f['code']
        info = dict(grade='unresolved',row_offset=None,width=None,object_off=None,getter_chain=[],profile=None)
        if k in bound:
            info.update(bound[k])
        elif f['is_language_field']=='true':
            info.update(grade='candidate',reason='language-marked schema only; no row-local text transfer linked')
            if k[1] in lang_candidates:
                info['getter_chain'] = st.add(lang_candidates[k[1]])
        elif k[0]=='Ntxr' or k[1]=='Ntxr':
            info['reason'] = 'Ntxr uses object+0x60, not any A/B/C/D vector; no client coordinate (do not equate housekeeping with a read)'
            if k[1]=='Ntxr':
                info.update(object_off=0x60,getter_chain=st.add(0x1042274,0x104227a,0x1042289,0x104228e))
        else:
            info['reason']='no client reader-to-wire proof'
        ledger.append(f|info)
    summary = {name:dict(Counter(x['grade'] for x in ledger if (x['parent'] is None)==direct))
               for name,direct in [('direct',True),('nested',False)]}
    summary['new_L3'] = sum(x['grade']=='L3' and 'inherited' not in x for x in ledger)
    summary['L4'] = 0
    old_negative = load(T01)
    dump('fields_nation_client.json',{'schema_sha256':manifest[MASTER],'rows':251,'summary':summary,
         'scope':'49 active client-marked or inherited schema occurrences; parent-qualified child keys',
         't01g_negative_unchanged':{'source':str(T01.relative_to(ROOT)).replace('\\','/'),'sha256':sha(T01.read_bytes()),
                                   'negative_result':old_negative['negative_result'],'falsified_or_rejected':old_negative['falsified_or_rejected']},
         'fields':ledger})
    for pc,b in st.branch.items():
        b['observed_taken'] = hit[pc,True]
        b['observed_not_taken'] = hit[pc,False]
    ci = [{'zero_based_call':i,'one_based_call':i+1,'site':site,
           'ordinary': 'tail_count' if 24<=i<28 else 'excluded_extra_scalar' if i>=28 else 'last_prefix',
           'width':st.t[site]['width'],'object_off':st.t[site]['object_off'],
           'ordinary_row_offset':('23' if i==23 else count_expr[i-24] if 24<=i<28 else None)}
          for i,site in enumerate(st.calls) if i>=23]
    dump('cursor_nation_tail.json',{'scope':'FM24 2430 client_db/table_10, ordinary arg8=0 only','status':'client wire closed; off-path and some semantic fields unresolved',
         'provenance':{'editor':editor.as_posix(),'editor_sha256':EXE_SHA,'snapshot_manifest':{p:manifest[p] for p in (MASTER,PROV)},
                       'archive':(data/'client_db.dat').as_posix(),'archive_sha256':archive_sha,'referenced_members':targets},
         'factory':{'call':0xf48f37,'ctor_vtable_setup':0x103ec17,'vtable_va':VT,'slot19':ENTRY,'slot2':0x1041f30,
                    'evidence':st.add(0x1041f40,0x1041f5b,0x103ec17,0x103ec1e,0xf48f37)},
         'cfg':list(st.cfg.values()),'calls_24_39':ci,
         'transfer_table':list(st.t.values()),'collections':cols,'exclusive_reference_slots':dep,
         'getter_jump_table_cells':st.jump_table,'row_count':len(rows),'rows':rows,
         'closure':{'first_selector':13,'t25_row_origin':14,'legacy_span_bytes':24710,'physical_footer_at':foot,'physical_footer_hex':raw[foot:].hex(),
                    'loader_transfers':[[0xffa602,4],[0xf2baa2,1],[0xf2bac2,4]],
                    't25_footer_at':foot+1,'omitted_first_footer_zero_in_t25':True,'member_bytes':len(raw)},
         'mode_control':{'caller':0xf2ba38,'entry_test':0x103fae6,'post_D_test':0x10409d3,'forced_extra_counterexample':mode_counterexample,
                         'arg8_nonzero_entry_path':'excluded, not assigned to client or server'},
         'memory_summary':{'callers_zero_wire':[0x1040731,0x104076e,0x10407cc,0x10407ee,0x104083c,0x104088b,0x10408b0,0x10408fa,0x1040976,0x10409b9,0x1040ba5],
                           'note':'reserve/alloc/append/indexed copy or sort over existing object vector; no wrapper forwarded to these calls. Callbacks and transitive allocator internals not expanded.'},
         'branch_shards':shards('branches',[b for _,b in sorted(st.branch.items())]),
         'instruction_shards':shards('instructions',[b for _,b in sorted(st.records.items())])})
    print(f't28 builder: {summary}; {foot}+9={len(raw)}; 251 rows')


def selftest():
    pf = profile([(0,0,0,b'\x64'),(1,0,1,b'\x65')],{'type':'integer','min_value':'0','max_value':'100'}, {})
    need(pf['matches']==1 and pf['violations']==[[1,0,1,'65']], 'integer negative control')
    p = profile([(0,0,0,struct.pack('<I',(2020<<16) | (4<<9) | 366))],{'type':'date'}, {})
    need(p['matches']==1 and p['intraday_codes']==[4], 'date packed bits')
    print('t28 builder selftest: OK')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest',action='store_true')
    ap.add_argument('--editor',type=Path,default=EDITOR)
    ap.add_argument('--data-dir',type=Path,default=DATA)
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            OUT.mkdir(parents=True,exist_ok=True)
            build(args.editor,args.data_dir)
        return 0
    except Check as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        return 1
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}: {exc}',file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.path.insert(0,str(ROOT/'scripts'))
    sys.exit(main())
