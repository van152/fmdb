#!/usr/bin/env python3
"""Build the offline FM24 CNtp/table 66 cursor and scoped field ledger."""
from __future__ import annotations

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
OUT = ROOT/'scratch/t34/out'
EXE = Path('D:/tmp2b/fm24/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_66.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_66.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
SCOPE = ['club.xml','CNtp']
VT, SLOT = 0x141884e08, 0x141530120
THUNK, START, END, JUMP, TAIL_THUNK, TAIL, TAIL_END = 0x152f720, 0x43583b0, 0x435847a, 0x4358475, 0xfae340, 0x3c600f0, 0x3c6016e
FAIL, BULK, ID, SELECT = 0x4358452, 0x3c60119, 0x3c60131, 0xf2ba0e
FOOT = (0xffa602, 0xf2baa2, 0xf2bac2)
CLASSES = ['wire_data','runtime-external','IO-result','context-lifecycle','dead']
# stream call, destination LEA, width MOV, status predicate, Jcc
ARGS = ((0x43583d9,0x43583c9,0x43583d0,0x43583dc,0x43583e0),
        (0x43583f5,0x43583e5,0x43583ec,0x43583f8,0x43583fc),
        (0x4358411,0x4358401,0x4358408,0x4358414,0x4358418),
        (0x435842d,0x435841d,0x4358424,0x4358430,0x4358434),
        (0x4358449,0x4358439,0x4358440,0x435844c,0x4358450))
GET = {'nati':(0x152fae4,0x152faf0),'rati':(0x152fad8,0x152fbaa),
       'mina':(0x152fa6d,0x152fa79),'maxa':(0x152fa61,0x152fb4e)}
OCC = 'scratch/t24/out/subtables.part001.json'
NATION = 'scratch/t25/out/cursor_nation.json'


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
        k, items = next(iter(obj.items()))
        lines = [enc(k)+':['+'\n'+',\n'.join(map(enc,items))+'\n]']
    else:
        lines = [enc(k)+':'+enc(v) for k,v in obj.items()]
    text = '{\n'+',\n'.join(lines)+'\n}\n'
    check(len(text.encode('utf-8')) < 50000, f'oversized {name}')
    (OUT/name).write_text(text,encoding='utf-8',newline='\n')


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
        self.slots = {n:S.unpack_from('<Q',self.pe.raw,vt+8*n)[0] for n in (2,3,19,20,21)}
        self.rtti = parse_rtti(self.pe,VT)
        check(self.slots[19]==SLOT and (self.rtti['class'],self.rtti['col_off'])==('STARTING_CLUB_TRANSFER_PREFERENCE',0x1885660),'RTTI/slot19')
        base, handler = 0xf49d38, 0xf49b18
        cell = base+4*66
        rel, = S.unpack_from('<i',self.pe.raw,cell)
        check(base+rel==handler and self.rip(0xf48b45)==self.pe.f2va(base) and self.rip(0xf49b3c)==VT and
              self.ins(0xf49b43).op_str=='qword ptr [rsi], rax' and self.direct(0xf49b54)==0xf49ca9,'factory dispatch/constructor')
        check(not any(self.ins(o).mnemonic.startswith('j') for o in self.span(handler,0xf49b54)) and
              self.ins(0xf49b46).op_str=='qword ptr [rsi + 0x18], 0xffffffffffffffff','constructor selector independence and scalar defaults')
        self.factory = {'jump_base':base,'cell':cell,'rel32':rel,'cell_bytes':self.pe.raw[cell:cell+4].hex(),
                        'dispatch':self.span(0xf48b30,0xf48b55),'handler':self.span(handler,0xf49b59),'return':self.span(0xf49ca9,0xf49cb3)}
        self.chain = [THUNK,START,JUMP,TAIL_THUNK,TAIL]
        for a,b in ((THUNK,START),(JUMP,TAIL_THUNK),(TAIL_THUNK,TAIL)):
            check(self.ins(a).mnemonic=='jmp' and self.direct(a)==b,'tail-jump chain')
            self.add(a)
        self.getter_cfg = ReaderCFG(self.pe,self.md,self.pe.va2f(self.slots[2]))
        self.extents, self.edges = [], {}
        for start,end in ((START,END),(TAIL,TAIL_END)):
            cfg = ReaderCFG(self.pe,self.md,start)
            want = [{'from':hex(JUMP),'kind':'tail_jump','target_va':'0x140faed40'}] if start==START else []
            check(cfg.function_end_off==end and cfg.external_edges==want,'PE runtime function/external edge')
            sites = sorted(self.pe.va2f(k) for k in cfg.instructions)
            edges = {k:[self.pe.va2f(j) for j in cfg.successors[self.pe.f2va(k)]] for k in sites}
            self.edges.update(edges)
            self.add(*sites)
            self.extents.append({'entry':start,'entry_VA':hex(self.pe.f2va(start)),'end_exclusive':end,
                'end_exclusive_VA':hex(self.pe.f2va(end)), 'instruction_count':len(sites),
                'blocks':self.blocks(start,edges),'external_edges':cfg.external_edges})
        self.edges.update({THUNK:[START],JUMP:[TAIL_THUNK],TAIL_THUNK:[TAIL]})
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
        transfers, branches = {}, {}
        for site,l,w,p,j in (*ARGS,(BULK,0x3c60106,0x3c6010d,None,None)):
            lea, size = self.ins(l), self.ins(w)
            check(self.ins(site).op_str=='qword ptr [rax + 0x28]' and lea.mnemonic=='lea' and
                  lea.op_str.startswith('rbx, [rdi + ' if site==BULK else 'rdx, [rcx + ' if site==ARGS[0][0] else 'rdx, [rsi + ') and
                  size.op_str.startswith('r8d, '),'read setup')
            transfers[site]={'site':site,'object_offset':lea.operands[1].mem.disp,'width':size.operands[1].imm,
                'setup':self.add(l,w),'kind':'identity_bulk' if site==BULK else 'member'}
            if j is not None:
                ok_taken=self.ins(j).mnemonic=='je'
                check(self.ins(p).op_str=='dword ptr [rbx + 0x10], 0' and
                      (j+self.ins(j).size if ok_taken else self.direct(j))==FAIL,'stream status/failure edge')
                branches[j]=self.branch(j,p,'IO-result','stream +0x10 status after this read',
                    (site,FAIL),'taken' if ok_taken else 'fallthrough',None)
        for j,p,cls,src,ev,edge,alt in [
            (0x3c60100,0x3c600fd,'context-lifecycle','stream from forwarded wrapper',(0x43583c6,0x43583cd,0x4358462,0x3c600fa),'fallthrough','row 0: null stream would already be dereferenced at 0x43583cd; forced tail-only null skips the 12-byte bulk'),
            (ID,0x3c6012a,'wire_data','unsigned raw identity lane 0 vs 10000001',(BULK,0x3c60127,0x3c60133,0x3c60138,0xf2ba3d),'taken',None),
            (0x3c6013e,0x3c6013b,'context-lifecycle','callback table this from caller stack, not R9',(0xf2b679,0xf2ba33,0x3c60122,0x3c60149),'fallthrough','row 0: null callback this would skip opaque callback after bulk; loader supplies table this'),
            (0x3c6014f,0x3c6014c,'context-lifecycle','release tests saved stream',(0x3c600fa,0x3c60102),'fallthrough','row 0: injected null would already lack identity'),
            (0x3c60155,0x3c60151,'context-lifecycle','ZF from decrement of locally retained stream',(0x3c60102,0x3c60162,0xf2ba48),'taken','row 0: injected last reference would invoke opaque destructor; retained owner keeps stream live')]:
            branches[j]=self.branch(j,p,cls,src,ev,edge,alt)
        check({o for o in self.edges if self.ins(o).mnemonic.startswith('j') and self.ins(o).mnemonic!='jmp'}==branches.keys(),'branch census')
        check({o for o in self.edges if self.ins(o).mnemonic=='call'}-transfers.keys()=={0x3c60149,0x3c60162},'opaque call census')
        check(self.ins(0x43583bd).op_str=='ebp, r8d' and self.ins(0x4358465).op_str=='r8d, ebp' and
              self.ins(0x43583ba).op_str=='r14, r9' and self.ins(0x4358468).op_str=='r9, r14' and
              self.ins(0x3c60146).op_str=='r9b, 1','runtime argument forwarding, not mode')
        return transfers,branches
    def loader_model(self):
        # Same generic outer path as t32, specialized only for the case-66 constructor and record count.
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
            (0xf2baa9,0xf2baa5,FOOT[1],'fallthrough','after row 752: short footer flag @18089 width 1'),
            (0xf2bac9,0xf2bac5,FOOT[2],'fallthrough','after row 752: short footer last lane @18090 width 4'),
            (0xffa7af,0xffa7ab,0xffa7a8,'not visited','footer vector count 0; count 1 and short lane 0 would fail'),
            (0xffa7ce,0xffa7ca,0xffa7c7,'not visited','footer vector count 0; count 1 and short lane 1 would fail'),
            (0xffa7ed,0xffa7e9,0xffa7e6,'not visited','footer vector count 0; count 1 and short lane 2 would fail'),
            (0xffa7fa,0xffa7f6,0xffa7e6,'not visited','footer vector count 0; count 1 and nonzero final triplet status would fail'),
        ]:
            add(o,p,'IO-result','stream +0x10 status',(t,),edge,alt)
        add(0xf2ba89,0xf2ba84,'IO-result','footer vector helper return (status or bound error)',(0xf2ba7f,0xffa9a3,0xffa9b6),'fallthrough','after row 752: short vector count @18085 width 4 (replay); native helper checks status on nonzero paths')
        add(0xf2ba59,0xf2ba57,'IO-result','slot19 AL; explicit false for member IO error',(0xf2ba51,FAIL,0x3c60164),'taken','row 0: short first member @14 -> AL=false under IO error contract')
        add(0xf2ba2b,0xf2ba28,'context-lifecycle','factory result; table66 arm does not inspect selector',(SELECT,0xf2ba1b,0xf2ba20,0xf2ba23,0xf49b3c),'fallthrough','row 0: case66 constructs vptr; null result would skip slot19 and lose the body')
        add(0xf2b9db,0xf2b9d6,'wire_data','header count, zero bypasses row loop',(0xf2b691,),'fallthrough','before row 0: real count=753, not 0')
        add(0xf2b9fa,0xf2b9f7,'wire_data','next ordinal vs header count',(0xf2b691,0xf2b9f0,0xf2b9f3),'both','after row 0: next=1<count; after row 752: next=count')
        add(0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end; same helper with same R8',(0xf2ba60,0xf2ba6e,0xf2ba72),'same cursor','both edges preserve footer cursor; actual pre-existing capacity is not from payload')
        add(0xffa610,0xffa609,'wire_data','footer vector count compared against process maximum',(FOOT[0],0xffa605,0xffa9a3),'fallthrough','footer count=0; out-of-bound count would return helper error')
        add(0xffa640,0xffa638,'context-lifecycle','existing vector capacity vs wire count',(0xffa61b,0xffa61f,0xffa646),'taken','footer count=0; no valid capacity below zero')
        add(0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets',(FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab),'taken','footer count=0; synthetic nonzero count would need 12 B/element')
        add(0xffa77f,0xffa77c,'wire_data','triplet loop index vs count',(0xffa775,0xffa778),'not visited','footer count=0; no first triplet')
        add(0xf48b3b,0xf48b38,'runtime-external','outer directory table type, not selector or caller layout mode',(0xf2ba20,0xf48b30,0xf48b45),'fallthrough','row 0: directory table type 66 <= factory bound; a different table type is outside scope')
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
        check(self.ins(0xe83d9a).operands[1].imm==int.from_bytes(b'CNtp','big') and
              [self.direct(o) for o in (0xe83da0,0xe84f3d,0x152fd50,0x43591ce,0xea67c4,0x152f7f0)]==
              [0xe84f11,0xea6420,0x4359180,0xfe6f60,0xfe6f60,0x4358a00],'CNtp list apply -> same class and members')
        check(self.rip(0xea66ea)==VT and self.ins(0xea66f1).op_str=='qword ptr [rsi], rax' and
              self.ins(0xea66cc).op_str=='ebx, dword ptr [rax + 0xc]' and self.ins(0xea66f4).op_str=='dword ptr [rsi + 0x18], ebx' and
              self.ins(0xea64f6).op_str=='ebp, dword ptr [rdx + 0xc]','parent association in a separate member')
        check([self.pe.va2f(self.slots[n]) for n in (2,3,20,21)]==[0x152fa40,0x152fd50,0xbe0,0x152f7f0] and
              self.ins(0xbe0).op_str=='al, 1' and self.ins(0xbe2).mnemonic=='ret','same-class slots / no ordinal fixup')
        check(self.ins(0x4358a5d).op_str=='rdx, [rsi + 0x1c]' and self.ins(0x4358a65).op_str=='r8d, 4' and
              self.ins(0x4358a6e).op_str=='qword ptr [rax + 0x28]','writer emits same scalar member')
        return {'parent_dispatch_and_list_apply':self.span(0xe83d9a,0xe83da6)+self.span(0xe84f11,0xe84f49),
            'parent_key_and_constructor':self.span(0xea64cd,0xea6501)+self.span(0xea66c1,0xea671f),
            'list_field_arms':self.span(0xea6750,0xea675c)+self.span(0xea677b,0xea67a3)+self.span(0xea67b0,0xea67d2)+self.span(0xea67e0,0xea67f1),
            'scalar_writer_and_no_fixup':self.add(0x152f7f0,0xbe0,0xbe2)+self.span(0x4358a3d,0x4358a77),
            'slot3':self.add(0x152fd50)+self.span(0x4359180,0x4359204),
            'key_unbox_scalar_arm':self.span(0xfe707a,0xfe70ad)+self.add(0xfe70f3,0xfe718d),
            'arguments':self.add(0xf2ba33,0xf2ba38,0xf2ba3d,0xf2ba4b,0xf2ba4e,0x43583ba,0x43583bd,0x4358465,0x4358468,
                                 0x3c60122,0x3c60127,0x3c60133,0x3c60146)}

    def getter(self,code):
        match,arm=GET[code]; x=int.from_bytes(code.encode('ascii'),'big'); pc=self.pe.va2f(self.slots[2]); route=[]
        for _ in range(30):
            i=self.ins(pc)
            check(i.address in self.getter_cfg.instructions,'getter reachability')
            route.extend(self.add(pc))
            if pc==arm:
                break
            z=pc+i.size
            if i.mnemonic=='cmp':
                check(i.op_str.startswith('edx, '),'4CC argument')
                cmp=i.operands[1].imm
            elif i.mnemonic.startswith('j') and {'je':x==cmp,'jne':x!=cmp,'jg':x>cmp}[i.mnemonic]:
                z=self.direct(pc)
            pc=z
        check(pc==arm and match in route and self.ins(match).operands[1].imm==x,'specific 4CC route')
        i=self.ins(arm); op=i.operands[1]; n=4 if code=='nati' else 1
        check(i.mnemonic=={'nati':'mov','rati':'movsx'}.get(code,'movzx') and op.type==3 and
              i.reg_name(op.mem.base)=='rcx' and op.size==n,'getter member/sign')
        end={'nati':0x152fb03,'rati':0x152fbc2,'mina':0x152fa8d,'maxa':0x152fb62}[code]
        support=self.span(arm,end)
        if code=='rati':
            check(self.ins(0x152fbae).op_str=='edi, edi' and self.direct(0x152fbb0)==0x152fc15,'rating zero bypasses scalar boxing')
            support+=self.span(0x152fc15,0x152fc49)
        return {'route':route,'compare':match,'arm':arm,'object_offset':op.mem.disp,'width':op.size,'support':support}

def take(raw,p,w,label):
    check(p+w<=len(raw),f'{label}: short read @{p} width {w}')
    return raw[p:p+w]


def read_row(st,raw,p,ordinal,cut=None):
    start=p
    selector=take(raw,p,1,f'row {ordinal} selector')[0]; p+=1
    check(selector==0,f'row {ordinal}: selector {selector} @{start} outside observed domain (not factory rejection)')
    body=p; pc=THUNK; lanes=None; stored=None; io_error=None; sites=[]; decisions=[]
    for _ in range(len(st.edges)+1):
        if pc in st.transfers:
            tr=st.transfers[pc]; w=tr['width']
            if p+w>len(raw) or pc==cut:
                io_error=f'row {ordinal}: short transfer @{p} width {w} site {pc:#x}'
                if pc==BULK:
                    raise CheckError(io_error+'; no immediate native bulk status test')
            else:
                if pc==BULK:
                    lanes=S.unpack_from('<III',raw,p)
                sites.append({**tr,'legacy_offset':p-body,'wire_offset':p-start}); p+=w
        if pc in st.branches:
            b=st.branches[pc]
            if pc==ID:
                check(lanes is not None,'bulk precedes identity predicate')
                taken=lanes[0]<10000001; stored=lanes[0] if taken else ordinal
            elif b['class']=='IO-result':
                taken=(io_error is None)==(st.ins(pc).mnemonic=='je')
            else:
                taken=b['observed_edge']=='taken'
            decisions.append([pc,taken]); pc=b['taken_to' if taken else 'fallthrough_to']
        elif st.ins(pc).mnemonic=='ret':
            if pc==0x435845e:
                raise CheckError(f'{io_error}; IO-result -> {FAIL:#x} (AL=false)')
            check(pc==0x3c6016d and st.ins(0x3c60164).op_str=='al, 1','success return')
            rid,a,b=lanes
            check(rid==stored==ordinal and a==b and a!=0,f'row {ordinal}: identity @{p-12} raw={lanes}, stored ordinal={stored}')
            return dict(ordinal=ordinal,selector_start=start,body_start=body,body_end=p,identity=list(lanes),
                        body_sha256=sha(raw[body:p]),wire_hex=raw[start:p].hex()),sites,decisions
        else:
            pc,=st.edges[pc]
    raise CheckError('nonterminating row path')


def walk(st,raw):
    check(len(raw)>=13 and raw[:8].hex()=='03017461642ef10d','header magic/version')
    n,flag=S.unpack_from('<IB',raw,8)
    check(n==753 and flag==0,'observed count and header byte')
    p=13; uids=set(); trace=sha256(); samples=[]; sels=Counter(); edges=Counter(); template=None; total=0
    for i in range(n):
        r,tr,conds=read_row(st,raw,p,i)
        if template is None:
            template=tr,conds
        check(template==(tr,conds),f'row {i}: new observed path')
        end=r['body_end']; uid=r['identity'][1]; check(uid not in uids,f'row {i}: duplicate uid {uid}')
        uids.add(uid); sels[raw[p]]+=1; edges.update((site,taken) for site,taken in conds)
        trace.update(S.pack('<7I',i,p,r['body_start'],end,*r['identity'])+bytes.fromhex(r['body_sha256']))
        total+=end-p; p=end
        if i in {0,1,2,n//2,n-1}:
            samples.append(r)
    footer=p; foot=[]; footer_sites=[]
    for site,w in zip(FOOT,(4,1,4),strict=True):
        v=int.from_bytes(take(raw,p,w,'footer'),'little')
        check(site!=FOOT[0] or v==0,f'footer @{p}: nonzero vector count {v} outside observed path')
        foot.append(v); footer_sites.append(dict(site=site,offset=p,width=w,value=v)); p+=w
    check(foot[1]==1 and p==len(raw)==13+total+9,'wire/footer closure')
    return dict(row_count=n,row_bytes=total,header_hex=raw[:13].hex(),wire_origin=13,legacy_origin=14,
        wire_footer_start=footer,legacy_footer_start=footer+1,wire_footer_hex=raw[footer:].hex(),legacy_footer_hex=raw[footer+1:].hex(),
        footer_values=foot,footer_transfers=footer_sites,uid_min=min(uids),uid_max=max(uids),selector_histogram=dict(sels),
        row_trace_sha256=trace.hexdigest(),samples=samples),template,edges

def reject(fn):
    try:
        fn()
    except CheckError as e:
        return str(e)
    raise CheckError('negative probe accepted')


def archives():
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); metadata={}
    for a in ('client','server'):
        fn=a+'_db.dat'; p=db.DB_DIR/fn
        d=codec['list_tables'](p,fn); e=[r for r in d if r['table_id']==66]
        metadata[a]={'directory_entry_count':len(d),'archive_sha256':sha(p.read_bytes()),'table66_entries':e,'present':bool(e)}
    check(not metadata['client']['present'] and len(metadata['server']['table66_entries'])==1,'table66 presence')
    metadata['client'].update(row_count=None,stride=None,payload_sha256=None)
    e,=metadata['server']['table66_entries']; frame=load(PROFILE)['payload']['packed_offset']
    with (db.DB_DIR/'server_db.dat').open('rb') as fh:
        fh.seek(e['offset']); probe=fh.read(frame-e['offset']+4)
        check(probe.endswith(db.MAGIC),'profile packed_offset lacks Zstd magic')
        fh.seek(frame); packed=fh.read(e['packed_size'])
    first=e['offset']+probe.index(db.MAGIC)
    first_raw=db.load_payload(codec,'server',66)
    raw=first_raw if first==frame and len(first_raw)==e['size'] else codec['_stream_decompress'](packed,256*1024*1024)
    check(len(raw)==e['size'] and S.unpack_from('<HI',raw,6)==(e['payload_version'],e['record_count_header']),'directory/payload header')
    metadata['server'].update(payload_len=len(raw),payload_sha256=sha(raw),zstd_frame_offset=frame,
                              first_frame_offset=first,default_load_payload_len=len(first_raw),used_profile_frame=(first!=frame or len(first_raw)!=e['size']))
    return metadata,raw,codec,db


def compare_t29(raw,s):
    pp,rr=(ROOT/PROFILE).read_bytes(),(ROOT/ROWS).read_bytes()
    d=json.loads(pp); p,c=d['payload'],d['row_closure']; n,w,end=s['row_count'],s['stride'],s['legacy_footer_start']
    check(d['table_type']==66 and d['archive']=='server' and p['payload_sha256']==sha(raw) and p['payload_size']==len(raw)
          and p['packed_offset']==s['zstd_frame_offset'] and p['packed_size']==s['table66_entries'][0]['packed_size']
          and (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'])==(n,w,14,end)
          and c['rows_sha256']==sha(raw[14:end]) and d['full_rows_file']=='profiles/table_server_66.rows.jsonl'
          and d['full_rows_sha256']==sha(rr),'t29 same payload and row-dump digests')
    rows=rr.splitlines(); check(len(rows)==n,'t29 row dump count')
    for i,line in enumerate(rows):
        at=14+i*w
        check(json.loads(line)=={'row':i,'offset':at,'len':w,'raw_hex':raw[at:at+w].hex()},f't29 row bytes {i}')
    q,=[x for x in load(INV)['parents'] if x['parent_4cc']=='CNtp']
    check((q['table_type'],q['archive'],q['rtti_class'],q['reader_va'],q['count'],q['stride'])==
          (66,'server','STARTING_CLUB_TRANSFER_PREFERENCE',hex(SLOT),n,w) and
          [r['schema_idx'] for r in q['schema_item_fields']]==list(range(46,50)) and
          q['profile']['profile_sha256']==sha(pp) and q['profile']['rows_jsonl_sha256']==sha(rr),'t29 CNtp inventory framing')
    inv={'path':INV,'sha256':sha((ROOT/INV).read_bytes()),'link_status':q['link_status'],'usage':'scout only; not field acceptance'}
    meta={'profile':PROFILE,'profile_sha256':sha(pp),'rows':ROWS,'rows_sha256':sha(rr),'legacy_block_sha256':c['rows_sha256'],
          'matched_full_rows':n,'inventory':inv}
    return {(r['offset'],r['width']):r for r in d['columns']},meta


def unsigned_match(bs,col):
    u=Counter(int.from_bytes(b,'little') for b in bs); max_uint=(1<<(8*col['width']))-1
    stats=[col[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
    check(stats==[len(bs),len(u),min(u),max(u),u[0],u[max_uint]],f't29 differential at +{col.get("offset")} width {col["width"]}')
    return stats


def targets(codec,db):
    # Only reference validation; use the closed client nation identity positions, not guessed server row widths.
    c=load(NATION); client=db.load_payload(codec,'client',10); server=db.load_payload(codec,'server',10)
    n,=S.unpack_from('<I',client,8)
    check(n==c['row_count']==S.unpack_from('<I',server,8)[0]==251 and sha(client)==c['source_payload']['sha256'],
          'nation target header / t25 client payload')
    ids={}; positions=[]; last=12
    for i,row in enumerate(c['rows']):
        o=row['identity_payload']; v=client[o:o+12]; ordinal,a,b=S.unpack('<Iii',v)
        check(i==ordinal==row['row_index']==row['ordinal'] and a==b==row['row_id']==row['repeated_id'] and a>0 and a not in ids,
              f'nation target identity row {i}')
        check(o>last and row['marker_payload']==o+12 and client[o+12]==0,'client target framing')
        ids[a]=ordinal; last=o
        p=server.find(v,13,len(server)-9)
        check(p>(positions[-1] if positions else 12) and server.find(v,p+1,len(server)-9)==-1,f'nation server identity corroboration {i}')
        positions.append(p)
    check(len(ids)==n and last+12==c['footer']['start_payload']-1 and positions[-1]+12==len(server)-9,'nation target domain endpoints')
    return ids, {'table_type':10,'row_count':n,'ordinal_bounds':[min(ids.values()),max(ids.values())],
        'identity_count':len(ids),'identity_min':min(ids),'identity_max':max(ids),
        'client_sha256':sha(client),'server_sha256':sha(server),'t25_client_positions':NATION,
        'server_identity_match_count':len(positions),'server_position_sha256':sha(S.pack(f'<{n}I',*positions)),
        'server_basis':'Unique ordered exact identity triples from client; not a new server nation row parser.'}


def ledger(st,raw,s,transfers,ids,ref,cols):
    m=load(MASTER); parent,=[p for p in m['entities']['club.xml'][0]['fields'] if p['field']=='CNtp']; specs=parent['list_item_fields']
    occ=[r for r in load(OCC)['nested_fields'] if r['parent']=='CNtp']
    check(len(specs)==len(occ)==len({p['field'] for p in specs})==4 and [r['idx'] for r in occ]==list(range(46,50)), 'scoped occurrences')
    sinks={t['object_offset']:t for t in transfers}; fields=[]; arrays={}; ords=set(ids.values())
    for spec,x in zip(specs,occ,strict=True):
        code=spec['field']; g=st.getter(code)
        check((x['code'],x['name'],x['type'],x['optional'])==(code,spec['name'],spec['type'],spec.get('is_optional')=='true'),'frozen schema / scoped occurrence')
        t=sinks[g['object_offset']]; w,o=t['width'],t['legacy_offset']; check(w==g['width'],'exact member width')
        offsets=list(range(14+o,s['legacy_footer_start'],s['stride'])); bs=[raw[p:p+w] for p in offsets]
        xs=[int.from_bytes(b,'little',signed=code in ('nati','rati')) for b in bs]; arrays[code]=xs; hist=Counter(xs)
        check(len(xs)==s['row_count'],'all-row field coverage')
        def ex(i):
            return dict(row=i,offset=offsets[i],value=xs[i],hex=bs[i].hex())
        domain={}; pr=dict(count=len(xs),distinct=len(hist),min=min(hist),max=max(hist),zero_count=hist[0],minus_one_count=hist[-1],
                            histogram=dict(sorted(hist.items())) if len(hist)<32 else None,t29_unsigned_stats=unsigned_match(bs,cols[o,w]))
        if code=='nati':
            check(spec['database_table_type']=='nation','nation target')
            cast='scalar_i32_nation_identity'; domain={'target':'nation','key_basis':'first UID lane at nation object +0xc; not ordinal +8 or pair',
                'constructor_default':-1,'zero_is_not_minus_one':True}
            bad=[i for i,v in enumerate(xs) if v!=-1 and v not in ids]; ord_bad=[i for i,v in enumerate(xs) if v!=-1 and v not in ords]
            pr.update(live_count=len(xs)-hist[-1],identity_matches=len(xs)-hist[-1]-len(bad),
                first_target_ordinals=[ids.get(v) for v in xs[:3]], ordinal_misses=len(ord_bad),
                first_ordinal_counterexample={**ex(ord_bad[0]),'actual_target_ordinal':ids.get(xs[ord_bad[0]])} if ord_bad else None)
        elif code=='rati':
            cast='i8_enum'; check('enum_ref' not in spec,'frozen enum scope'); bad=[]
            domain={'native_signed_bounds':[-128,127],'zero_sentinel':'zero takes special getter arm instead of normal scalar boxing',
                    'frozen_enum_ref':None,'exhaustive_enum_domain':None}
            pr['observed_live_values']=sorted(k for k in hist if k!=0)
        else:
            cast='u8_integer'; lo,hi=(int(spec[k]) for k in ('min_value','max_value'))
            domain={'xml_bounds':[lo,hi],'native_unsigned_bounds':[0,255],'proven_zero_sentinel':False}
            bad=[i for i,v in enumerate(xs) if not lo<=v<=hi]
            pr['nonzero_xml_violations']=sum(xs[i]!=0 for i in bad)
        pr.update(violations=len(bad),first_violation=ex(bad[0]) if bad else None)
        grade='held_static_sink_profile_conflict' if bad else 'L3_named_row_coordinate'
        fields.append(dict(schema_scope=[*SCOPE,x['idx']],code=code,name=spec['name'],schema=spec,grade=grade,
            row_offset=None if bad else o,wire_offset=None if bad else o+1,interpretation=cast,getter=g,
            sink={k:t[k] for k in ('legacy_offset','wire_offset','width','object_offset','site')},domain=domain,profile=pr))
    age=list(zip(arrays['mina'],arrays['maxa'],strict=True)); bad=[i for i,(a,b) in enumerate(age) if a>b]
    def age_ex(i):
        at=14+i*s['stride']+sinks[0x21]['legacy_offset']
        return dict(row=i,offset=at,values=list(age[i]),hex=raw[at:at+2].hex())
    both=sum(a!=0 and b!=0 for a,b in age)
    relationship=dict(both_zero=age.count((0,0)),both_nonzero=both,only_min_zero=sum(not a and b!=0 for a,b in age),
        only_max_zero=sum(a!=0 and not b for a,b in age),raw_min_gt_max=len(bad),nonzero_min_gt_max=sum(all(age[i]) for i in bad),
        first_raw_min_gt_max=age_ex(bad[0]) if bad else None)
    return dict(scope=SCOPE,table_type=66,occurrences=4,baseline_L3=0,L3=sum(f['grade'].startswith('L3') for f in fields),L4=0,
        fields=fields,reference_domain=ref,age_relationship=relationship,
        rejected_record_pair=dict(row=0,offset=14,lanes=list(S.unpack_from('<ii',raw,14)),reason='Two separate 4 B reads; first member is the owning club UID, second is the nati getter scalar. No second-lane normalization.'))


def build():
    st=Static(); support=st.scope_support(); a,raw,codec,db=archives(); s=a['server']
    closure,(tr,conditions),edges=walk(st,raw); s.update(closure)
    n=s['row_count']; stride=1+sum(t['width'] for t in tr)
    check(stride==24 and n*stride==s['row_bytes'] and s['footer_values']==[0,1,753] and s['uid_max']==753,'observed closure from CFG')
    s.update(stride=stride,row_template={'id':0,'condition_edges':conditions,'wire_selector':'13+24*i','legacy_body':'14+24*i',
        'body_end_exclusive':'37+24*i','trace_digest_record':'LE <7I>(i,selector,body,end,identity0,identity1,identity2) + SHA-256 bytes of body'})
    short={t['site']:reject(lambda:read_row(st,raw,13,0,cut=t['site'])) for t in tr}
    off=14+tr[-1]['legacy_offset']
    bad_id=reject(lambda:read_row(st,raw[:off]+S.pack('<I',10000001)+raw[off+4:],13,0))
    s['negative_replays']={'short_transfers':[{'site':o,'first_counterexample':msg} for o,msg in short.items()],
        'overwrite_does_not_mask_raw_error':bad_id,
        'selector_out_of_observed_domain':reject(lambda:read_row(st,raw[:13]+b'\x01'+raw[14:],13,0)),
        'duplicate_lane_mismatch':reject(lambda:read_row(st,raw[:off+8]+bytes(4)+raw[off+12:],13,0))}
    cols,t29=compare_t29(raw,s); ids,ref=targets(codec,db); fields=ledger(st,raw,s,tr,ids,ref,cols)
    bs=[]
    for o,b in sorted(st.branches.items()):
        alt=short[b['evidence'][0]] if b['class']=='IO-result' else bad_id if o==ID else b['alternative_or_first_counterexample']
        bs.append({**b,'scope':'reader' if o>=START else 'identity_tail','alternative_or_first_counterexample':alt,
                   'taken_count':edges[o,True],'fallthrough_count':edges[o,False]})
    bs.extend({**b,'scope':'loader_footer_factory_slice'} for b in st.loader.values())
    OUT.mkdir(parents=True,exist_ok=True)
    c={'status':'complete_observed_row_cursor','scope':SCOPE,'table_type':66,
        'provenance':{'editor':str(EXE),'editor_sha256':EXE_SHA,'snapshot_manifest':st.snap},
        'factory':st.factory,'rtti':st.rtti,'slots':st.slots,'scope_evidence':support,
        'reader':{'chain':st.chain,'extent_source':'PE exception directory RUNTIME_FUNCTION','extents':st.extents,
                  'condition_count':len(st.branches),'runtime_mode_forks':[],
                  'mode_proof':'No caller mode tested. R8D and R9 forwarded by property reader; tail reloads R8D from raw identity (fallback: caller stack ordinal), sets R9B=1 before callback. Stack mode byte is never read.'},
        'archives':a,'t29':t29,'transfers':[{'site':SELECT,'legacy_offset':-1,'wire_offset':0,'width':1,'sink':'loader stack+0x43'},*tr],
        'loader_transfers':st.loader_transfers,'wire_alignment':f'13 + {n}*(1+11+12) + 9 = {len(raw)}',
        'legacy_alignment':f'14 + {n}*24 + 8 = {len(raw)}; legacy +23 borrows next selector/first footer byte',
        'branch_taxonomy':CLASSES,'branch_census':{k:sum(b['class']==k for b in bs) for k in CLASSES},
        'limits':['Selector and header/footer flag values are observed, not factory validation.',
                  'Callback/destructor are opaque. Lifecycle counts are replay under the loader contract, not runtime measurement.',
                  'Identity bulk has no immediate status check. Last footer u32 at table+0x50 equals both max observed UID and count here; no universal meaning inferred.'],
        'branch_shards':shards('branches',bs,24),'instruction_shards':shards('instructions',[st.records[o] for o in sorted(st.records)],120)}
    write('cursor_cntp.json',c); write('fields_cntp.json',fields)
    print(f"t34 build PASS: {n} x {stride} B; {fields['L3']}/4 L3, {4-fields['L3']} held, L4=0")


def selftest():
    check(take(b'abc',1,2,'fixture')==b'bc','bounded transfer')
    check('short read @1 width 3' in reject(lambda:take(b'abc',1,3,'fixture')),'short transfer fixture')
    check(S.unpack('<bBB',b'\xff\x00\xff')==(-1,0,255),'signed rating and unsigned age are distinct')
    print('t34 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test bounded transfers and signedness without reading local data')
    try:
        selftest() if p.parse_args().selftest else build()
        return 0
    except CheckError as e:
        print(f't34 check failed: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't34 fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
