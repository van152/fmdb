#!/usr/bin/env python3
"""Build the offline FM24 CSrs/table 62 cursor and scoped field ledger."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
OUT = ROOT/'scratch/t31/out'
EXE = Path(str(_cfg.EDITOR_EXE))
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_62.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_62.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
SCOPE = ['club.xml','CSrs']
VT, SLOT, START, END, TAIL_THUNK, TAIL, TAIL_END = 0x141884988, 0x14119c960, 0x3e5d730, 0x3e5d8b4, 0xfae340, 0x3c600f0, 0x3c6016e
FAIL, BULK, ID, SELECT = 0x3e5d88e, 0x3c60119, 0x3c60131, 0xf2ba0e
FOOT = (0xffa602, 0xf2baa2, 0xf2bac2)
CLASSES = ['wire_data','runtime-external','IO-result','context-lifecycle','dead']
# Matched compare, terminal object access, interpretation, optional/mask proof.
GETTERS = {
    'Ttyp':(0x119c881,0x119cbab,'i8',-1,(0x119cbaf,0x119cbb2)),
    'Tdvi':(0x119c9d7,0x119cca7,'ordinal',-1,(0x119ccab,0x119ccae,0x119ccb4,0x119ccb9,0x119cd37)),
    'tmno':(0x119ca0c,0x119ccc6,'bool',4,(0x119ccd3,0x119ccd6,0x119ccd9)),
    'tmnv':(0x119ca18,0x119ca24,'bool',2,(0x119ca31,0x119ca33,0x119ca36)),
    'Tsti':(0x119c973,0x119cc8a,'ordinal',-1,(0x119cc8e,0x119cc91,0x119cd83,0x119cd88,0x119cd97)),
    'Twhm':(0x119c88d,0x119c899,'i8',0,(0x119c89d,0x119c89f)),
    'Tmhm':(0x119c777,0x119cae6,'i8',0,(0x119caea,0x119caec)),
    'Catd':(0x119c72a,0x119ca88,'i32',None,(0x119ca8b,0x119ca90,0x119ca94)),
    'Cmna':(0x119c7ff,0x119cb4d,'i32',None,(0x119cb50,0x119cb55,0x119cb59)),
    'Cmxa':(0x119c80b,0x119c817,'i32',None,(0x119c81a,0x119c81f,0x119c823)),
}


class CheckError(Exception):
    pass


def check(ok, why):
    if not ok:
        raise CheckError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def load(p):
    return json.loads((ROOT/p).read_bytes())


def write(name, obj):
    enc = lambda v: json.dumps(v, ensure_ascii=False,separators=(',',':'))
    if '.part' in name:
        key, items = next(iter(obj.items()))
        lines = [enc(key)+':['+'\n'+',\n'.join(map(enc,items))+'\n]']
    else:
        lines = [enc(k)+':'+enc(v) for k,v in obj.items()]
    text = '{\n'+',\n'.join(lines)+'\n}\n'
    check(len(text.encode('utf-8')) < 50000, f'oversized {name}')
    (OUT/name).write_text(text,encoding='utf-8')


def shards(key, records, step):
    names = []
    for i in range(0,len(records),step):
        name = f'{key}.part{i//step+1:03d}.json'
        write(name,{key:records[i:i+step]})
        names.append(name)
    return names


class Static:
    def __init__(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t14_rtti_census import parse_rtti
        from t21b_control_flow import ReaderCFG
        manifest = {i['path']:i['sha256'] for i in load('evidence/MANIFEST.json')['files']}
        self.snap = {p:sha((ROOT/p).read_bytes()) for p in (MASTER,PROV)}
        check(all(d==manifest[p] for p,d in self.snap.items()) and self.snap[MASTER].startswith('7d57477e'),'frozen evidence manifest')
        self.pe = PE(EXE)
        check(sha(self.pe.raw)==EXE_SHA and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'),'editor provenance')
        self.pe.pe.parse_data_directories(directories=[3])
        self.md = Cs(CS_ARCH_X86,CS_MODE_64)
        self.md.detail = True
        self.ops, self.records = {}, {}
        vt = self.pe.va2f(VT)
        self.slots = {n:S.unpack_from('<Q',self.pe.raw,vt+8*n)[0] for n in (2,19,20,21)}
        self.rtti = parse_rtti(self.pe,VT)
        check(self.slots[19]==SLOT and (self.rtti['class'],self.rtti['col_off'])==('STARTING_RESERVE_TEAM',0x18840e0),'RTTI/slot19')
        self.thunk = self.pe.va2f(SLOT)
        base, handler = 0xf49d38, 0xf49a2b
        cell = base+4*62
        rel, = S.unpack_from('<i',self.pe.raw,cell)
        check(base+rel==handler and self.rip(0xf48b45)==self.pe.f2va(base) and self.rip(0xf49a58)==VT
              and self.ins(0xf49a5f).op_str=='qword ptr [rsi], rax' and self.direct(0xf49a99)==0xf49ca9,'factory dispatch/constructor')
        self.factory = {'jump_base':base,'cell':cell,'rel32':rel,'cell_bytes':self.pe.raw[cell:cell+4].hex(),
                        'dispatch':self.span(0xf48b30,0xf48b55),'handler':self.span(handler,0xf49a9e),'return':self.span(0xf49ca9,0xf49cb3)}
        self.chain = [self.thunk,START,0x3e5d8af,TAIL_THUNK,TAIL]
        for a,b in ((self.thunk,START),(0x3e5d8af,TAIL_THUNK),(TAIL_THUNK,TAIL)):
            check(self.ins(a).mnemonic=='jmp' and self.direct(a)==b,'tail-jump chain')
            self.add(a)
        entry = self.pe.va2f(self.slots[2])
        self.getter_cfg = ReaderCFG(self.pe,self.md,entry)
        self.extents = []
        self.edges = {}
        for start,end in ((START,END),(TAIL,TAIL_END)):
            cfg = ReaderCFG(self.pe,self.md,start)
            want = [{'from':'0x3e5d8af','kind':'tail_jump','target_va':'0x140faed40'}] if start==START else []
            check(cfg.function_end_off==end and cfg.external_edges==want,'PE runtime function/external edge')
            sites = sorted(self.pe.va2f(k) for k in cfg.instructions)
            edges = {k:[self.pe.va2f(j) for j in cfg.successors[self.pe.f2va(k)]] for k in sites}
            self.edges.update(edges)
            self.add(*sites)
            self.extents.append({'entry':start,'entry_VA':hex(self.pe.f2va(start)),'end_exclusive':end,
                'end_exclusive_VA':hex(self.pe.f2va(end)), 'instruction_count':len(sites),
                'blocks':self.blocks(start,edges),'external_edges':cfg.external_edges})
        self.edges[0x3e5d8af] = [TAIL_THUNK]
        self.edges[TAIL_THUNK] = [TAIL]
        self.transfers, self.branches = self.reader_model()
        self.loader, self.loader_transfers = self.loader_model()

    def ins(self,o):
        if o not in self.ops:
            va = self.pe.f2va(o)
            check(va is not None and self.pe.va2f(va)==o,f'unmapped instruction {o:#x}')
            self.ops[o] = next(self.md.disasm(self.pe.raw[o:o+15],va,count=1))
        return self.ops[o]

    def add(self,*places):
        for o in places:
            i = self.ins(o)
            self.records[o] = {'file_offset':hex(o),'VA':hex(i.address),'bytes':i.bytes.hex(),
                               'instruction':f'{i.mnemonic} {i.op_str}'.rstrip()}
        return list(places)

    def span(self,o,end):
        sites = []
        while o<end:
            sites.extend(self.add(o))
            o += self.ins(o).size
        check(o==end,f'span endpoint {end:#x}')
        return sites

    def rip(self,o):
        i=self.ins(o)
        return i.address+i.size+i.operands[1].mem.disp

    def direct(self,o):
        return self.pe.va2f(self.ins(o).operands[0].imm)

    def blocks(self,start,edges):
        leaders={start}
        for o in edges:
            if self.ins(o).mnemonic.startswith('j'):
                leaders.update(edges[o])
        result=[]
        for o in sorted(leaders):
            pcs=[]
            while True:
                pcs.append(o)
                if len(edges[o])!=1 or edges[o][0] in leaders or self.ins(o).mnemonic.startswith('j'):
                    result.append({'sites':pcs,'successors':edges[o]})
                    break
                o,=edges[o]
        check(sorted(x for b in result for x in b['sites'])==sorted(edges),'basic block partition')
        return result

    def branch(self,o,p,c,source,evidence,observed,alternative):
        i,prior=self.ins(o),self.ins(p)
        end=p+prior.size
        check(i.mnemonic.startswith('j') and i.mnemonic!='jmp' and (end==o or
              (o==0xffa640 and self.ins(end).mnemonic=='mov' and end+self.ins(end).size==o)),f'branch/predicate {o:#x}')
        self.add(o,p,*evidence)
        return {'site':o,'predicate':p,'class':c,'source':source,'evidence':list(evidence),
                'taken_to':self.direct(o),'fallthrough_to':o+i.size,'observed_edge':observed,
                'alternative_or_first_counterexample':alternative}

    def reader_model(self):
        # Actual consumer in tail, not the slot-19 thunk or its JMP instruction.
        t,b={},{}
        fixed={
            0x3c60100:(0x3c600fd,'context-lifecycle','same stream pointee already dereferenced by the row body',(0x3e5d742,0x3e5d749,0x3e5d89d,0x3c600fa),'fallthrough','row 0: null entry stream dereferences before first transfer @14; cannot reach tail by that path. Tail-only null skips 12 B and cannot validate raw identity.'),
            ID:(0x3c6012a,'wire_data','unsigned lane0 just read; >=10000001 overwrites with caller ordinal',(BULK,0x3c60127,0x3c60133,0x3c60138,0xf2ba3d),'taken','row 0: raw lane0=0, not >=10000001. Synthetic lane0=10000001 overwrites but raw ordinal postcondition still rejects.'),
            0x3c6013e:(0x3c6013b,'context-lifecycle','callback pointer from caller stack, table this (not R9)',(0xf2b679,0xf2ba33,0x3c60122,0x3c60149),'fallthrough','row 0: wrapper passes live table this. An injected null callback would skip the call after bulk, no new explicit transfer.'),
            0x3c6014f:(0x3c6014c,'context-lifecycle','same saved RSI stream as initial tail guard',(0x3c600fa,0x3c60102),'fallthrough','row 0: same non-null saved RSI; null alternative would skip release and already lack identity.'),
            0x3c60155:(0x3c60151,'context-lifecycle','ZF from decrement after local retain; wrapper owns live stream',(0x3c60102,0x3c60162,0xf2ba48),'taken','row 0: under retained-owner contract no final release; injected last reference would call opaque destructor, not establish another row layout.'),
        }
        sites=sorted(self.edges)
        for x,o in enumerate(sites):
            i=self.ins(o)
            if i.mnemonic=='call' and i.op_str=='qword ptr [rax + 0x28]':
                if o==BULK:
                    l,wp,setup=0x3c60106,0x3c6010d,(0x3c6010a,0x3c60113,0x3c60116)
                else:
                    l,wp=sites[x-4],sites[x-2]
                    setup=sites[x-3],sites[x-1]
                lea=self.ins(l)
                prefix={BULK:'rbx, [rdi + ',0x3e5d755:'rdx, [rcx + '}.get(o,'rdx, [rbx + ')
                check(lea.mnemonic=='lea' and lea.op_str.startswith(prefix)
                      and self.ins(wp).op_str.startswith('r8d, '),f'native transfer setup {o:#x}')
                obj,w=lea.operands[1].mem.disp,self.ins(wp).operands[1].imm
                t[o]={'site':o,'consumer':o,'object_offset':obj,'width':w,'setup':self.add(l,wp,*setup),
                      'sink':f'object+{obj:#x}','kind':'identity_bulk' if o==BULK else 'member'}
            if i.mnemonic.startswith('j') and i.mnemonic!='jmp':
                if o in fixed:
                    args=fixed[o]
                else:
                    call,p=sites[x-2:x]
                    check(call in t and self.ins(p).op_str=='dword ptr [rsi + 0x10], 0','member IO predicate')
                    obs='taken' if i.mnemonic=='je' else 'fallthrough'
                    check((o+i.size if obs=='taken' else self.direct(o))==FAIL,'member failure target')
                    args=(p,'IO-result','stream +0x10 status immediately after member read',(call,FAIL),obs,None)
                b[o]=self.branch(o,*args)
        check(len(t)==12 and sum(v['width'] for v in t.values())==41 and len(b)==16,'combined reader tally')
        check({o for o in sites if self.ins(o).mnemonic=='call'}-t.keys()=={0x3c60149,0x3c60162},'opaque calls')
        return t,b

    def loader_model(self):
        for a,z in ((0xf2b660,0xf2b6cd),(0xf2b9d6,0xf2b9ea),(0xf2b9f0,0xf2bad7),
                    (0xffa5d0,0xffa646),(0xffa72a,0xffa752),(0xffa775,0xffa785),
                    (0xffa785,0xffa800),(0xffa99e,0xffa9cc)):
            self.span(a,z)
        check(self.direct(0xf2ba7f)==0xffa5d0 and self.direct(0xf2ba23)==0xf48b30,'loader helper/factory')
        b={}
        def add(o,p,c,src,ev,edge,alt):
            b[o]=self.branch(o,p,c,src,ev,edge,alt)
        for o,p,t,edge,alt in [
            (0xf2b698,0xf2b694,0xf2b691,'fallthrough','before row 0: short count @8 width 4'),
            (0xf2b6b8,0xf2b6b4,0xf2b6b1,'taken','before row 0: short header byte @12 width 1'),
            (0xf2ba15,0xf2ba11,SELECT,'fallthrough','row 0: short selector @13 width 1'),
            (0xf2baa9,0xf2baa5,FOOT[1],'fallthrough','after final row: short footer flag, width 1'),
            (0xf2bac9,0xf2bac5,FOOT[2],'fallthrough','after final row: short footer last lane, width 4'),
            (0xffa7af,0xffa7ab,0xffa7a8,'not visited','footer count 0; synthetic count 1 and missing lane 0 would fail'),
            (0xffa7ce,0xffa7ca,0xffa7c7,'not visited','footer count 0; synthetic count 1 and missing lane 1 would fail'),
            (0xffa7ed,0xffa7e9,0xffa7e6,'not visited','footer count 0; synthetic count 1 and missing lane 2 would fail'),
            (0xffa7fa,0xffa7f6,0xffa7e6,'not visited','footer count 0; synthetic count 1 with nonzero status at final triplet status check'),
        ]:
            add(o,p,'IO-result','stream +0x10 status',(t,),edge,alt)
        add(0xf2ba89,0xf2ba84,'IO-result','footer vector helper return (status or bound error)',(0xf2ba7f,0xffa9a3,0xffa9b6),'fallthrough','after final row: synthetic short vector count, width 4')
        add(0xf2ba59,0xf2ba57,'IO-result','slot19 AL; explicit false for member IO error',(0xf2ba51,FAIL,0x3c60164),'taken','row 0: short first member @14 -> AL=false')
        add(0xf2ba2b,0xf2ba28,'context-lifecycle','factory result; table62 arm does not branch on selector',(SELECT,0xf2ba1b,0xf2ba20,0xf2ba23,0xf49a58),'fallthrough','row 0: resolved constructor/vptr; null result skips slot19 and cannot supply observed body')
        add(0xf2b9db,0xf2b9d6,'wire_data','header count, zero bypasses row loop',(0xf2b691,),'fallthrough','before row 0: real count=37214, not 0')
        add(0xf2b9fa,0xf2b9f7,'wire_data','next ordinal vs header count',(0xf2b691,0xf2b9f0,0xf2b9f3),'both','after row 0: next=1<count; after row 37213: next=count')
        add(0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end; both edges join before helper with same R8',(0xf2ba60,0xf2ba6e,0xf2ba72),'same cursor','both edges preserve footer cursor; actual pre-existing capacity not read from payload')
        add(0xffa610,0xffa609,'wire_data','footer vector count compared against process maximum',(FOOT[0],0xffa605,0xffa9a3),'fallthrough','footer count=0; out-of-bound count would return helper error')
        add(0xffa640,0xffa638,'context-lifecycle','existing vector capacity vs wire count; zero needs no growth',(0xffa61b,0xffa61f,0xffa646),'taken','footer count=0; no valid capacity below zero')
        add(0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets',(FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab),'taken','footer count=0; synthetic nonzero count would require 12 B/element')
        add(0xffa77f,0xffa77c,'wire_data','triplet loop index vs count',(0xffa775,0xffa778),'not visited','footer count=0')
        add(0xf48b3b,0xf48b38,'runtime-external','outer table-type dispatch parameter, not row selector',(0xf2ba20,0xf48b30,0xf48b45),'fallthrough','row 0: directory table type=62 <= factory bound; a different table type is outside this task')
        ts=[]
        for o,wp,lp,w,sink in [
            (0xf2b691,0xf2b688,0xf2b683,4,'loader stack+0x44 (row count)'),
            (0xf2b6b1,0xf2b6a5,0xf2b69d,1,'table+0x5c (header byte)'),
            (SELECT,0xf2ba02,0xf2b9e3,1,'loader stack+0x43 (factory selector)'),
            (FOOT[0],0xffa5fc,0xffa5f7,4,'helper stack+0x2c (vector count)'),
            (0xffa7a8,0xffa79c,0xffa746,4,'helper stack+0x30 (vector lane 0)'),
            (0xffa7c7,0xffa7bb,0xffa739,4,'helper stack+0x34 (vector lane 1)'),
            (0xffa7e6,0xffa7da,0xffa73e,4,'helper stack+0x38 (vector lane 2)'),
            (FOOT[1],0xf2ba99,0xf2ba92,1,'table+0x58'),(FOOT[2],0xf2bab9,0xf2bab2,4,'table+0x50')]:
            check(self.ins(o).op_str=='qword ptr [rax + 0x28]' and self.ins(wp).operands[1].imm==w,'loader transfer')
            ts.append({'site':o,'consumer':o,'width':w,'sink':sink,'setup':self.add(wp,lp)})
        return b,ts

    def scope_support(self):
        check(self.ins(0xe8b6f0).operands[1].imm==int.from_bytes(b'CSrs','big') and
              [self.direct(o) for o in (0xe8b6f6,0xe8e286,0x152a840)]==[0xe8e27c,0x152a840,0x4354a30]
              and self.ins(0x4354b01).op_str=='qword ptr [r14 + 0x18], rbx','club CSrs collection arm')
        fix,wr=(self.pe.va2f(self.slots[k]) for k in (20,21))
        check(self.direct(fix)==0x3e5d990 and self.direct(wr)==0x3e5e690,'ref slots')
        check([self.direct(o) for o in (0x3e5d9ba,0x3e5d9d7,0x3e5d9e9,0xf7e440,0xf7e280,0xf7f340)]==
              [0xf7e440,0xf7e280,0xf7f340,0x3bf3460,0x3bf3190,0x3bf6ec0],'ref resolver chain')
        return {'CSrs_collection':self.span(0xe8b6f0,0xe8b6fc)+self.span(0xe8e27c,0xe8e29b)
                +self.add(0x152a840,0x4354a4d,0x4354a50,0x4354aaf,0x4354ab6,0x4354abd,0x4354ac0,0x4354ae0,0x4354afe,0x4354b01,0x4354b05,0x4354b6a),
                'ref_writers':self.add(wr)+self.span(0x3e5e6e7,0x3e5e78f),
                'ref_fixup':self.add(fix)+self.span(0x3e5d990,0x3e5d9f8)+self.add(0xf7e440,0xf7e280,0xf7f340,
                    0x3bf34b2,0x3bf34fd,0x3bf350e,0x3bf3512,0x3bf31df,0x3bf321b,0x3bf322c,0x3bf3230,
                    0x3bf6f8c,0x3bf6f9a,0x3bf6f9e),
                'Tdvi_direct_pointer_only':self.span(0x119cca7,0x119ccc6)+self.span(0x119c9fc,0x119ca0c)+self.span(0x119cd33,0x119cd44),
                'Tsti_direct_pointer_only':self.span(0x119cc8a,0x119cca7)+self.span(0x119cd83,0x119cd9e),
                'runtime_arguments':self.add(0xf2ba33,0xf2ba38,0xf2ba3d,0xf2ba4b,0xf2ba4e,0x3e5d739,0x3e5d8a0,0x3e5d8a3,0x3c60122,0x3c60133,0x3c60146)}

    def getter(self,code):
        cmp_o,dest,kind,param,proof=GETTERS[code]
        o=self.pe.va2f(self.slots[2]); x=int.from_bytes(code.encode('ascii'),'big')
        route=[]; cmp=None
        for _ in range(32):
            i=self.ins(o)
            check(i.address in self.getter_cfg.instructions,'getter reachable')
            route.extend(self.add(o))
            if o==dest:
                break
            if i.mnemonic=='cmp':
                check(i.op_str.startswith('edx, '),'4CC EDX compare')
                cmp=i.operands[1].imm
            nxt=o+i.size
            if i.mnemonic.startswith('j'):
                nxt=self.direct(o) if {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic] else nxt
            o=nxt
        check(o==dest and cmp_o in route and self.ins(cmp_o).operands[1].imm==x,f'getter dispatch {code}')
        i=self.ins(o); src=i.operands[1]
        check(i.reg_name(src.mem.base)=='rcx' and i.mnemonic=={'i8':'movsx','bool':'movzx','i32':'mov','ordinal':'mov'}[kind],'getter access')
        if kind=='i8':
            check(self.ins(proof[0]).op_str==('edi, -1' if param==-1 else 'edi, edi') and self.direct(proof[1])==0x119cc0f,'signed sentinel')
        if kind=='bool':
            check(self.ins(proof[0]).mnemonic=='shr' and 1<<self.ins(proof[0]).operands[1].imm==param
                  and self.ins(proof[1]).op_str=='bl, 1','individual flag mask')
        return {'route':route,'compare':cmp_o,'access':o,'proof':self.add(*proof),'object_offset':src.mem.disp,'width':src.size}

    def tape(self):
        o=START
        transfers,conditions=[],[]
        for _ in range(len(self.edges)):
            if o in self.transfers:
                transfers.append(self.transfers[o])
            if o in self.branches:
                b=self.branches[o]; taken=b['observed_edge']=='taken'
                conditions.append([o,taken])
                o=b['taken_to' if taken else 'fallthrough_to']
            elif self.ins(o).mnemonic=='ret':
                check(o==0x3c6016d and self.ins(0x3c60164).op_str=='al, 1','reader success')
                return transfers,conditions
            else:
                o,=self.edges[o]
        raise CheckError('nonterminating reader tape')


def take(raw,p,w,label):
    check(p+w<=len(raw),f'{label}: short read @{p} width {w}')
    return raw[p:p+w]


def walk(raw,tape,cut_site=None):
    check(raw[:8]==bytes.fromhex('03017461642ef10d') and len(raw)>=13,'header marker/version')
    n,flag=S.unpack_from('<IB',raw,8)
    check(flag==0,'observed header byte')
    p=13; total=0; uids=set(); trace=sha256(); samples=[]; sels=Counter()
    for i in range(n):
        start=p
        selector=take(raw,p,1,f'row {i} selector')[0]
        sels[selector]+=1
        check(selector==0,f'row {i}: selector {selector} @{p} outside observed domain (not factory rejection)')
        p+=1; body=p; lanes=None
        for t in tape:
            w,o=t['width'],t['site']
            if p+w>len(raw) or (i==0 and cut_site==o):
                effect='no immediate native bulk status test' if o==BULK else f'IO-result -> {FAIL:#x} (AL=false)'
                raise CheckError(f'row {i}: short transfer @{p} width {w} site {o:#x}; {effect}')
            if o==BULK:
                lanes=S.unpack_from('<III',raw,p)
            p+=w
        check(lanes is not None,'no identity transfer')
        rid,a,b=lanes
        stored=rid if rid<10000001 else i   # execute real wire predicate; keep raw lane independent
        check(rid==stored==i and a==b and a!=0 and a not in uids,
              f'row {i}: identity @{p-12} raw={lanes}, stored ordinal={stored}')
        uids.add(a); total+=p-start
        h=sha256(raw[body:p]).digest()
        trace.update(S.pack('<7I',i,start,body,p,*lanes)+h)
        if i in {0,1,2,n//2,n-1}:
            samples.append(dict(ordinal=i,selector_start=start,body_start=body,body_end=p,identity=list(lanes),
                                body_sha256=h.hex(),wire_hex=raw[start:p].hex()))
    footer=p
    vc=S.unpack('<I',take(raw,p,4,'footer vector count'))[0];p+=4
    check(vc==0,f'footer vector count {vc} @{footer} outside observed domain')
    ff=take(raw,p,1,'footer flag')[0];p+=1
    hi=S.unpack('<I',take(raw,p,4,'footer last lane'))[0];p+=4
    uid_max=max(uids,default=0)
    check(ff==1 and hi==uid_max and p==len(raw)==13+total+9,
          f'footer @{footer}: flag={ff}, last_u32={hi}, UID max={uid_max}, end={p}, len={len(raw)}')
    return {'row_count':n,'row_bytes':total,'header_hex':raw[:13].hex(),'wire_origin':13,'legacy_origin':14,
            'wire_footer_start':footer,'legacy_footer_start':footer+1,'wire_footer_hex':raw[footer:].hex(),
            'legacy_footer_hex':raw[footer+1:].hex(),'footer_values':[vc,ff,hi], 'uid_min':min(uids,default=0),'uid_max':uid_max,
            'selector_histogram':dict(sels),'row_trace_sha256':trace.hexdigest(),'samples':samples}


def reject(f):
    try:
        f()
    except CheckError as e:
        return str(e)
    raise CheckError('negative probe accepted')


def archives():
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); metadata={}
    for a in ('client','server'):
        fn=a+'_db.dat'; p=db.DB_DIR/fn
        d=codec['list_tables'](p,fn); e=[r for r in d if r['table_id']==62]
        metadata[a]={'directory_entry_count':len(d),'archive_sha256':sha(p.read_bytes()),'table62_entries':e,'present':bool(e)}
    check(not metadata['client']['present'] and len(metadata['server']['table62_entries'])==1,'table62 presence')
    metadata['client'].update(row_count=None,stride=None,payload_sha256=None)
    raw=db.load_payload(codec,'server',62)
    e,=metadata['server']['table62_entries']
    check(len(raw)==e['size'] and S.unpack_from('<HI',raw,6)==(e['payload_version'],e['record_count_header']),'directory/payload header')
    p=db.DB_DIR/'server_db.dat'
    with p.open('rb') as fh:
        fh.seek(e['offset']); hit=fh.read(64).find(db.MAGIC)
    check(hit>=0,'table62 zstd frame')
    metadata['server'].update(payload_len=len(raw),payload_sha256=sha(raw),zstd_frame_offset=e['offset']+hit)
    domains, ids={},{}
    for key,tid,count,stride,off in [('competition',25,7047,127,114),('stadium',21,48413,38,25)]:
        ref=db.load_payload(codec,'client',tid)
        check(S.unpack_from('<I',ref,8)[0]==count and len(ref)==14+count*stride+8,f'{key} target framing')
        nums={S.unpack_from('<I',ref,14+i*stride+off)[0] for i in range(count)}
        check(nums==set(range(count)),f'{key} target ordinals')
        ids[key]=nums
        domains[key]={'archive':'client','table_type':tid,'count':count,'stride':stride,'ordinal_legacy_offset':off,'payload_sha256':sha(ref)}
    return metadata,raw,ids,domains


def compare_t29(raw,s):
    pp,rr=(ROOT/PROFILE).read_bytes(),(ROOT/ROWS).read_bytes()
    d=json.loads(pp); p,c=d['payload'],d['row_closure']; n,w,end=s['row_count'],s['stride'],s['legacy_footer_start']
    check(d['table_type']==62 and d['archive']=='server' and p['payload_sha256']==sha(raw) and p['payload_size']==len(raw)
          and p['packed_offset']==s['zstd_frame_offset'] and (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'])==(n,w,14,end)
          and c['rows_sha256']==sha(raw[14:end]) and d['full_rows_file']=='profiles/table_server_62.rows.jsonl'
          and d['full_rows_sha256']==sha(rr),'t29 same payload and row-dump digests')
    rows=rr.splitlines(); check(len(rows)==n,'t29 row dump count')
    for i,line in enumerate(rows):
        at=14+i*w
        check(json.loads(line)=={'row':i,'offset':at,'len':w,'raw_hex':raw[at:at+w].hex()},f't29 row bytes {i}')
    inv=None
    if (ROOT/INV).is_file():
        q,=[x for x in load(INV)['parents'] if x['parent_4cc']=='CSrs']
        check((q['table_type'],q['count'],q['stride'])==(62,n,w),'t29 CSrs inventory framing')
        inv={'path':INV,'sha256':sha((ROOT/INV).read_bytes()),'status':q['status'],'usage':'scout only; candidate columns do not set grades'}
    meta={'profile':PROFILE,'profile_sha256':sha(pp),'rows':ROWS,'rows_sha256':sha(rr),'legacy_block_sha256':c['rows_sha256'],
          'matched_full_rows':n,'inventory':inv}
    return {(r['offset'],r['width']):r for r in d['columns'] if r['interpretation'] in ('u8','u16','u32')},meta


def profile(raw,n,stride,tr,kind,param,allowed,t29):
    o,w=tr['legacy_offset'],tr['width']
    fmt={'i8':'b','i32':'i','ordinal':'i','bool':'B'}[kind]
    actor=lambda v: int(bool(v&param)) if kind=='bool' else v
    sentinel=None if kind=='bool' else param
    xs,us,bad=Counter(),Counter(),[]; matches=0; sample={}
    for i in range(n):
        at=14+i*stride+o
        b=raw[at:at+w]; r=S.unpack('<'+fmt,b)[0]; v=actor(r)
        xs[v]+=1; us[int.from_bytes(b,'little')]+=1
        ok=v==sentinel or v in allowed
        matches+=ok
        if not ok and len(bad)<5:
            bad.append({'row':i,'offset':at,'value':v,'hex':b.hex()})
        if i in (0,n//2,n-1):
            sample[str(i)]=v
    stats=[t29[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
    check(stats==[n,len(us),min(us),max(us),us[0],us[(1<<(8*w))-1]],f't29 differential body+{o}')
    hist = dict(sorted(xs.items())) if len(xs)<=100 else None
    live = [v for v in xs if v!=sentinel]
    return {'count':n,'distinct':len(xs),'min':min(xs),'max':max(xs),'zero_count':xs[0],
            'sentinel':sentinel,'sentinel_count':xs[sentinel],'live_count':n-xs[sentinel],
            'live_min':min(live,default=None),'live_max':max(live,default=None),'matches':matches,'violations':n-matches,
            'first_violations':bad,'histogram':hist,'samples':sample,'t29_unsigned_stats':stats,
            'raw_shared_byte_histogram':dict(sorted(us.items())) if kind=='bool' else None}


def ledger(st,raw,s,ts,ids,domains,cols):
    master=load(MASTER)
    p,=[x for x in master['entities']['club.xml'][0]['fields'] if x['field']=='CSrs']
    specs=p['list_item_fields']
    t24=[r for file in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for r in load(file)['nested_fields'] if r['parent']=='CSrs']
    check(len(specs)==len(t24)==len({x['field'] for x in specs})==len(GETTERS)==10,'unique scoped occurrences')
    fields=[]
    for spec,occ in zip(specs,t24,strict=True):
        code=spec['field']; kind,param=GETTERS[code][2:4]
        check((occ['code'],occ['type'],occ['name'])==(code,spec['type'],spec['name']),'t24/frozen schema join')
        g=st.getter(code)
        tr,=[t for t in ts if t['object_offset']==g['object_offset']]
        o,w=tr['legacy_offset'],tr['width']
        check((w,g['width'])=={'ordinal':(4,8),'i8':(1,1),'bool':(1,1),'i32':(4,4)}[kind],'getter/wire width')
        typ=spec['type']
        if typ=='enum':
            allowed={int(r['enum']) for r in master['enums'][spec['enum_ref']]['values']}
            domain={'frozen_enum':spec['enum_ref'],'values':sorted(allowed)}
        elif typ=='database_record_unique_id':
            key=spec['database_table_type']; allowed=ids[key]
            domain={'target_ordinal':key,'bounds':[min(allowed),max(allowed)]}
        elif typ=='day_of_week':
            allowed=range(1,8); domain={'live_values':list(allowed),'note':'seven nonzero weekday codes, mapping to weekday names not claimed; getter zero is absent'}
        elif typ=='boolean':
            allowed={0,1};domain={'decoded_values':[0,1],'mask':param}
        else:
            check(typ=='integer','unexpected schema domain')
            lo,hi=(int(spec[k]) for k in ('min_value','max_value'))
            allowed=range(lo,hi+1);domain={'xml_bounds':[lo,hi]}
        p=profile(raw,s['row_count'],s['stride'],tr,kind,param,allowed,cols[o,w]); promote=not p['violations']
        fields.append({'schema_scope':[*SCOPE,occ['idx']],'code':code,'name':spec['name'],'schema':spec,
            'grade':'L3_named_row_coordinate' if promote else 'held_static_sink_profile_conflict',
            'row_offset':o if promote else None,'wire_offset':tr['wire_offset'] if promote else None,
            'bit_mask':param if kind=='bool' else None,'interpretation':kind,'domain':domain,'getter':g,
            'candidate_sink':{'legacy_offset':o,'wire_offset':tr['wire_offset'],'width':w,'object_offset':tr['object_offset'],'reader_site':tr['site']},'profile':p})
    return {'scope':SCOPE,'table_type':62,'occurrences':10,'baseline_L3':0,'L3':sum(f['grade'].startswith('L3') for f in fields),
            'L4':0,'date_fields':0,'reference_domains':domains,'fields':fields,
            'negative_policy':'Strict per-field domains and exact native sentinels; no clipping, guessed weekday names, UID stand-ins, or replacement of raw violations.'}


def build():
    st=Static(); support=st.scope_support(); tape,conditions=st.tape()
    a,raw,ids,domains=archives();s=a['server'];s.update(walk(raw,tape))
    ts=[];wire=1
    for t in tape:
        ts.append({**t,'wire_offset':wire,'legacy_offset':wire-1});wire+=t['width']
    n=s['row_count'];check(wire==42 and n*wire==s['row_bytes'],'closed stride from tape')
    s.update(stride=wire,row_template={'id':0,'condition_edges':conditions,'wire_selector':'13+42*i','legacy_body':'14+42*i',
        'body_end_exclusive':'55+42*i','trace_digest_record':'LE <7I>(i,selector,body,end,identity0,identity1,identity2) + 32 raw SHA-256 bytes of body'},
        footer_transfers=[{'site':site,'offset':s['wire_footer_start']+d,'width':w,'value':v}
                          for site,d,w,v in zip(FOOT,(0,4,5),(4,1,4),s['footer_values'],strict=True)])
    failures={t['site']:reject(lambda:walk(raw,tape,t['site'])) for t in tape}
    identity_at=14+ts[-1]['legacy_offset']
    s['negative_replays']={'short_transfers':[{'site':o,'first_counterexample':msg} for o,msg in failures.items()],
        'overwrite_does_not_mask_raw_error':reject(lambda:walk(raw[:identity_at]+S.pack('<I',10000001)+raw[identity_at+4:],tape)),
        'selector_out_of_observed_domain':reject(lambda:walk(raw[:13]+b'\x01'+raw[14:],tape)),
        'duplicate_lane_mismatch':reject(lambda:walk(raw[:identity_at+8]+S.pack('<I',0)+raw[identity_at+12:],tape))}
    cols,t29=compare_t29(raw,s)
    fields=ledger(st,raw,s,ts,ids,domains,cols)
    branches=[]
    for o,b in st.branches.items():
        taken=dict(conditions)[o]
        branches.append({**b,'scope':'reader' if o>=START else 'identity_tail',
                         'alternative_or_first_counterexample':failures[b['evidence'][0]] if b['class']=='IO-result' else b['alternative_or_first_counterexample'],
                         'taken_count':n if taken else 0,'fallthrough_count':0 if taken else n})
    branches.extend({**b,'scope':'loader_footer_factory_slice'} for b in st.loader.values())
    OUT.mkdir(parents=True,exist_ok=True)
    cursor={'status':'complete_observed_row_cursor_partial_runtime_only_edges','scope':SCOPE,'table_type':62,
        'provenance':{'editor':str(EXE),'editor_sha256':EXE_SHA,'snapshot_manifest':st.snap},
        'factory':st.factory,'rtti':st.rtti,'slots':st.slots,'scope_evidence':support,
        'reader':{'chain':st.chain,'extent_source':'PE exception directory RUNTIME_FUNCTION','extents':st.extents,
                  'condition_count':len(st.branches),'runtime_mode_forks':[],
                  'mode_proof':'CSrs body always reads 29 B; no caller mode gate in either reachable extent. Tail JMP preserves the caller stack. R9 forwarded to tail but R9B overwritten for the callback; neither R9 nor the stack mode byte tests layout. Outer factory bound uses known directory table type.'},
        'archives':a,'t29':t29,'transfers':[{'site':SELECT,'legacy_offset':-1,'wire_offset':0,'width':1,'sink':'loader stack+0x43'},*ts],
        'loader_transfers':st.loader_transfers,'wire_alignment':f'13 + {n}*(1+29+12) + 9 = {len(raw)}',
        'legacy_alignment':f'14 + {n}*42 + 8 = {len(raw)}; legacy +41 borrows next selector/first footer byte',
        'branch_taxonomy':CLASSES,'branch_census':dict(Counter(b['class'] for b in branches)),
        'not_named':[{'legacy_offset':1,'object_offset':24,'note':'CSrs parent collection back-reference; not a nested field'},
                     {'legacy_offset':27,'object_offset':71,'note':'only masks 0x04 and 0x02 named here; no whole-byte assignment'},
                     {'legacy_offset':28,'object_offset':72,'note':'unscoped byte; do not infer another weekday field'}],
        'limits':['Selector 0 and footer vector count 0 specialize this archive, not unconditional native constraints.',
                  'Identity bulk has no immediate status check; replay rejects shortage but does not assert native AL=false.',
                  'Callback and release targets are opaque; callback receives object, not stream. Lifecycle counts are conditional on a live retained stream/table, not measured runtime traces.',
                  'Footer last u32 stored at table+0x50 equals both max observed duplicate UID and row count here; header count is read separately, no general semantics inferred.'],
        'branch_shards':shards('branches',branches,24),'instruction_shards':shards('instructions',[st.records[o] for o in sorted(st.records)],120)}
    write('cursor_csrs.json',cursor);write('fields_csrs.json',fields)
    print(f"t31 build PASS: {n} x {wire} B; {fields['L3']}/10 L3, {10-fields['L3']} held, L4=0")


def selftest():
    h=bytes.fromhex('03017461642ef10d0100000000');t=[{'site':BULK,'width':12}]
    raw=h+b'\0'+S.pack('<IIIIBI',0,5,5,0,1,5)
    check(walk(raw,t)['wire_footer_start']==26,'synthetic cursor')
    for x in (raw[:-1],h+b'\x01'+raw[14:],raw[:14]+S.pack('<I',10000001)+raw[18:]):
        reject(lambda:walk(x,t))
    check('no immediate native bulk status test' in reject(lambda:walk(raw,t,BULK)),'bulk failure distinction')
    print('t31 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test synthetic framing, raw identity and IO negatives')
    try:
        selftest() if p.parse_args().selftest else build()
        return 0
    except CheckError as e:
        print(f't31 check failed: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't31 fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
