#!/usr/bin/env python3
"""Build the offline FM24 Cdbt/table 33 cursor and scoped field ledger."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
OUT = ROOT/'scratch/t36/out'
EXE = Path('D:/tmp2b/fm24/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_33.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_33.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
SCOPE = ['club.xml','Cdbt']
VT, SLOT = 0x1418835e8, 0x141535af0
THUNK, START, JUMP, TAIL_THUNK, TAIL = 0x15350f0, 0x4367ac0, 0x4367d4e, 0xfae340, 0x3c600f0
DATE_THUNK, DATE, DATE_READ = 0xdb7f80, 0x39dd7b0, 0x39dd7d4
FAIL, BULK, ID, SELECT = 0x4367d2d, 0x3c60119, 0x3c60131, 0xf2ba0e
FOOT = (0xffa602, 0xf2baa2, 0xf2bac2)
CLASSES = ['wire_data','runtime-external','IO-result','context-lifecycle','dead']
# Actual call sites (including the two caller sites of the shared date helper).
BODY = (0x4367ae5,0x4367b05,0x4367b25,0x4367b45,0x4367b65,0x4367b8c,0x4367ba0,0x4367bb4,
        0x4367bd4,0x4367bf4,0x4367c14,0x4367c34,0x4367c54,0x4367c74,0x4367c94,0x4367cb4,
        0x4367cd0,0x4367cec,0x4367d08,0x4367d24)
GET = {'cash':(0x15357c4,0x1535bc4,0x1535bc4), 'sour':(0x15358d4,0x15358e0,0x15358e0),
       'stdt':(0x1535ae6,0x1535dda,0x1535dff), 'endt':(0x15359c9,0x15359d5,0x15359fa),
       'inrt':(0x15358c8,0x1535c81,0x1535c81)}
DATE_CALLS = {0x4367ba0:0x4367b99,0x4367bb4:0x4367bad}

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
        manifest = {x['path']:x['sha256'] for x in load('evidence/MANIFEST.json')['files']}
        self.snap = {p:sha((ROOT/p).read_bytes()) for p in (MASTER,PROV)}
        check(all(v==manifest[p] for p,v in self.snap.items()) and self.snap[MASTER].startswith('7d57477e'),'frozen snapshots')
        self.pe=PE(EXE)
        check(sha(self.pe.raw)==EXE_SHA and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'),'editor SHA/provenance')
        self.pe.pe.parse_data_directories(directories=[3])
        self.md=Cs(CS_ARCH_X86,CS_MODE_64); self.md.detail=True
        self.ops,self.records,self.edges={}, {}, {}
        v=self.pe.va2f(VT)
        self.slots={k:S.unpack_from('<Q',self.pe.raw,v+8*k)[0] for k in (2,3,19,20,21)}
        self.rtti=parse_rtti(self.pe,VT)
        check(self.slots[19]==SLOT and (self.rtti['class'],self.rtti['col_off'])==('STARTING_CLUB_DEBT',0x1882d40),'vtable and RTTI')
        base=0xf49d38; cell=base+4*33; rel=S.unpack_from('<i',self.pe.raw,cell)[0]; h=base+rel
        check(h==0xf4941b and self.rip(0xf48b45)==self.pe.f2va(base) and self.direct(0xf49492)==0xf72430 and
              self.direct(0xf72430)==0x3bdb220 and self.direct(0xf49497)==0xf49ca9 and
              self.rip(0x3bdb232)==VT and self.ins(0x3bdb239).op_str=='qword ptr [rax], rcx','case33 constructor chain')
        self.factory=dict(jump_base=base,cell=cell,rel32=rel,cell_bytes=self.pe.raw[cell:cell+4].hex(),
                          dispatch=self.span(0xf48b30,0xf48b55),handler=self.span(h,0xf4949c),
                          constructor=self.add(0xf72430)+self.span(0x3bdb220,0x3bdb2a3),return_path=self.span(0xf49ca9,0xf49cb3))
        leafs={THUNK:START,TAIL_THUNK:TAIL,DATE_THUNK:DATE}
        for a,b in {**leafs,JUMP:TAIL_THUNK}.items():
            check(self.ins(a).mnemonic=='jmp' and self.direct(a)==b,f'thunk chain @{a:#x}')
            self.add(a)
        for a in leafs:
            rva=self.pe.f2va(a)-self.pe.base
            check(not any(e.struct.BeginAddress<=rva<e.struct.EndAddress for e in self.pe.pe.DIRECTORY_ENTRY_EXCEPTION),'leaf unexpectedly has extent')
        self.extents=[]
        for start,end in ((START,0x4367d53),(TAIL,0x3c6016e),(DATE,0x39dd7f9)):
            cfg=ReaderCFG(self.pe,self.md,start)
            ext=[dict(kind='tail_jump',target_va=hex(self.pe.f2va(TAIL_THUNK)),**{'from':hex(JUMP)})] if start==START else []
            check(cfg.function_end_off==end and cfg.external_edges==ext,'runtime-function bound or external edge')
            edges={self.pe.va2f(a):[self.pe.va2f(b) for b in bs] for a,bs in cfg.successors.items()}
            self.add(*edges);self.edges.update(edges)
            self.extents.append(dict(entry=start,entry_VA=hex(self.pe.f2va(start)),end_exclusive=end,end_exclusive_VA=hex(self.pe.f2va(end)),
                                     instruction_count=len(edges),blocks=self.blocks(start,edges),external_edges=ext))
        self.edges.update({a:[b] for a,b in {**leafs,JUMP:TAIL_THUNK}.items()})
        self.getcfg=ReaderCFG(self.pe,self.md,self.pe.va2f(self.slots[2]))
        self.transfers,self.branches=self.reader_model()
        self.loader,self.loader_transfers=self.loader_model()
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

    def loader_model(self):
        # Same generic outer path as t31, specialized only for the case-33 constructor and record count.
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
            (0xf2baa9,0xf2baa5,FOOT[1],'fallthrough','after row 32408: short footer flag @2560328 width 1'),
            (0xf2bac9,0xf2bac5,FOOT[2],'fallthrough','after row 32408: short footer last lane @2560329 width 4'),
            (0xffa7af,0xffa7ab,0xffa7a8,'not visited','footer vector count 0; count 1 and short lane 0 would fail'),
            (0xffa7ce,0xffa7ca,0xffa7c7,'not visited','footer vector count 0; count 1 and short lane 1 would fail'),
            (0xffa7ed,0xffa7e9,0xffa7e6,'not visited','footer vector count 0; count 1 and short lane 2 would fail'),
            (0xffa7fa,0xffa7f6,0xffa7e6,'not visited','footer vector count 0; count 1 and nonzero final triplet status would fail'),
        ]:
            add(o,p,'IO-result','stream +0x10 status',(t,),edge,alt)
        add(0xf2ba89,0xf2ba84,'IO-result','footer vector helper return (status or bound error)',(0xf2ba7f,0xffa9a3,0xffa9b6),'fallthrough','after row 32408: short vector count @2560324 width 4 (replay); native helper checks status on nonzero paths')
        add(0xf2ba59,0xf2ba57,'IO-result','slot19 AL; explicit false for member IO error',(0xf2ba51,FAIL,0x3c60164),'taken','row 0: short first member @14 -> AL=false under IO error contract')
        add(0xf2ba2b,0xf2ba28,'context-lifecycle','factory result; table33 arm does not inspect selector',(SELECT,0xf2ba1b,0xf2ba20,0xf2ba23,0x3bdb232),'fallthrough','row 0: case33 constructs vptr; null result would skip slot19 and lose the body')
        add(0xf2b9db,0xf2b9d6,'wire_data','header count, zero bypasses row loop',(0xf2b691,),'fallthrough','before row 0: real count=32409, not 0')
        add(0xf2b9fa,0xf2b9f7,'wire_data','next ordinal vs header count',(0xf2b691,0xf2b9f0,0xf2b9f3),'both','after row 0: next=1<count; after row 32408: next=count')
        add(0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end; same helper with same R8',(0xf2ba60,0xf2ba6e,0xf2ba72),'same cursor','both edges preserve footer cursor; actual pre-existing capacity is not from payload')
        add(0xffa610,0xffa609,'wire_data','footer vector count compared against process maximum',(FOOT[0],0xffa605,0xffa9a3),'fallthrough','footer count=0; out-of-bound count would return helper error')
        add(0xffa640,0xffa638,'context-lifecycle','existing vector capacity vs wire count',(0xffa61b,0xffa61f,0xffa646),'taken','footer count=0; no valid capacity below zero')
        add(0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets',(FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab),'taken','footer count=0; synthetic nonzero count would need 12 B/element')
        add(0xffa77f,0xffa77c,'wire_data','triplet loop index vs count',(0xffa775,0xffa778),'not visited','footer count=0; no first triplet')
        add(0xf48b3b,0xf48b38,'runtime-external','outer directory table type, not selector or caller layout mode',(0xf2ba20,0xf48b30,0xf48b45),'fallthrough','row 0: directory table type 33 <= factory bound; a different table type is outside scope')
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

    def reader_model(self):
        t,b={},{}
        for call in (*BODY,BULK):
            if call in DATE_CALLS:
                lea=DATE_CALLS[call]; w=0x39dd7c8; consumer=DATE_READ
                check(self.direct(call)==DATE_THUNK and self.ins(call-3).op_str=='rdx, rdi' and
                      self.ins(0x39dd7be).op_str=='rax, rcx' and self.ins(0x39dd7d1).op_str=='rdx, rax' and
                      self.ins(0x39dd7ef).mnemonic=='sete','date argument forwarding + AL result')
                setup=self.add(lea,w,call-3,DATE_THUNK,0x39dd7be,0x39dd7d1)
            else:
                consumer=call;w=call-(12 if call==BULK else 9)
                lea=0x3c60106 if call==BULK else 0x4367b72 if call==0x4367b8c else call-16
                setup=self.add(lea,w)
            i=self.ins(lea); z=self.ins(w)
            check(i.mnemonic=='lea' and i.op_str.startswith('rcx, [rbx + ' if call in DATE_CALLS else 'rbx, [rdi + ' if call==BULK else 'rdx, [rcx + ' if call==BODY[0] else 'rdx, [rbx + ') and z.op_str.startswith('r8d, ') and
                  self.ins(consumer).op_str==('qword ptr [rdi + 0x28]' if call in DATE_CALLS else 'qword ptr [rax + 0x28]'),'call width/destination setup')
            t[call]=dict(site=call,consumer=consumer,object_offset=i.operands[1].mem.disp,width=z.operands[1].imm,setup=setup,
                         kind='date_helper' if call in DATE_CALLS else 'identity_bulk' if call==BULK else 'member')
            if call!=BULK:
                p=call+self.ins(call).size; j=p+self.ins(p).size
                prior=self.ins(p); branch=self.ins(j); ok_edge='taken' if branch.mnemonic=='je' and call not in DATE_CALLS else 'fallthrough'
                check(prior.op_str==('al, al' if call in DATE_CALLS else 'dword ptr [rsi + 0x10], 0') and
                      (j+branch.size if ok_edge=='taken' else self.direct(j))==FAIL,'native AL=false path')
                b[j]=self.branch(j,p,'IO-result','helper AL from saved stream status' if call in DATE_CALLS else 'stream +0x10 status',
                                 (call,0x39dd7d7,0x39dd7ef,FAIL) if call in DATE_CALLS else (call,FAIL),ok_edge,None)
        for j,p,cls,src,ev,edge,alt in [
            (0x39dd7bc,0x39dd7b9,'context-lifecycle','stream pointee from RDX wrapper',(0x39dd7b6,0x39dd7d7),'fallthrough','row 0 first date: injected null skips read but dereferences null at 0x39dd7d7, not another valid width'),
            (0x39dd7de,0x39dd7da,'context-lifecycle','local retain/release after status save',(0x39dd7c1,0x39dd7eb),'taken','row 0 first date: last ref calls opaque destructor, not a different layout'),
            (0x3c60100,0x3c600fd,'context-lifecycle','tail wrapper stream',(0x4367d3c,0x3c600fa),'fallthrough','row 0: passing null initially faults at 0x4367ad9; a synthetic tail-only null would skip identity'),
            (ID,0x3c6012a,'wire_data','unsigned just-read identity lane 0 vs 10000001',(BULK,0x3c60127,0x3c60133,0x3c60138,0xf2ba3d),'taken',None),
            (0x3c6013e,0x3c6013b,'context-lifecycle','caller stack table this',(0xf2ba33,0x3c60122,0x3c60149),'fallthrough','row 0: null table context would skip callback, no explicit transfer'),
            (0x3c6014f,0x3c6014c,'context-lifecycle','saved stream release guard',(0x3c600fa,0x3c60102),'fallthrough','row 0: injected null would already lack the bulk'),
            (0x3c60155,0x3c60151,'context-lifecycle','ZF from release after local retain',(0x3c60102,0x3c60162,0xf2ba48),'taken','row 0: last ref calls opaque destructor, not an observed alternate body')]:
            b[j]=self.branch(j,p,cls,src,ev,edge,alt)
        check({o for o in self.edges if len(self.edges[o])==2}==b.keys(),'branch census')
        check({o for o in self.edges if self.ins(o).mnemonic=='call'}==set(t)|{DATE_READ,0x39dd7eb,0x3c60149,0x3c60162},'all reachable calls')
        return t,b

    def scope_support(self):
        links={0xe58165:0xe58420,0xe58433:0xe58448,0xe58448:0x1521740,0x1521740:0x4343880,0xe58464:0xe9dee0,0xe9e1a6:0x1536380,
               0x1535390:0x4367e00,0x4367e3a:0xf7e440,0xf7e440:0x3bf3460,0x4367e67:0xf7e280,0xf7e280:0x3bf3190,
               0x1535410:0x4367f80}
        check(all(self.direct(a)==b for a,b in links.items()) and self.ins(0xe5815e).op_str=='r8d, 0x43646274' and
              self.pe.va2f(self.slots[3])==0x1536380,'parent source and same-class property dispatch')
        evidence={
            'parent':self.span(0xe5815e,0xe5816b)+self.span(0xe58420,0xe58435)+self.span(0xe58448,0xe5846e)+
                     self.add(0x1521740,0x434389d,0x43438fa,0x4343904,0x4343924)+self.span(0x434394d,0x4343975)+
                     self.span(0x4343a40,0x4343a63)+self.span(0xe9e190,0xe9e1b4),
            'references':self.add(0x1535390,0xf7e440,0xf7e280,0x1535410,0x3bf34b2,0x3bf34c7,0x3bf31df,0x3bf31f4,0x3bf322c,0x3bf3230)+
                         self.span(0x4367e00,0x4367e76)+self.span(0x4367fba,0x4367fe5)+self.span(0x436820e,0x4368239)+
                         self.span(0x1535d56,0x1535d73)+self.span(0x1535ebb,0x1535ed2),
            'mode':self.add(0x4367ac9,0x4367d39,0x4367d3c,0x4367d3f,0x4367d42,0x3c60122,0x3c60133,0x3c60146,0xf2ba33,0xf2ba38,0xf2ba3d,0xf2ba51),
            'real_sentinel':self.span(0x1535c81,0x1535cad)+self.span(0x1535e72,0x1535e8c)+self.span(0x1535ee4,0x1535f05),
            'date_box':self.span(0x15359d5,0x1535a25)+self.span(0x1535dda,0x1535e2a),
            'scalar_box':self.span(0x1535bc4,0x1535bd7)+self.span(0x15358e0,0x15358f4)}
        self.sentinels=[]
        for o,expect in ((0x1535c86,-99.0),(0x1535e72,-1.0)):
            i=self.ins(o); a=self.pe.va2f(i.address+i.size+i.operands[1].mem.disp);raw=self.pe.raw[a:a+4]
            check(S.unpack('<f',raw)==(expect,),'fp32 constant')
            self.sentinels.append(dict(site=o,offset=a,VA=hex(self.pe.f2va(a)),bytes=raw.hex(),value=expect))
        return evidence

    def getter(self,code):
        cmp_o,arm,load_o=GET[code]; x=int.from_bytes(code.encode('ascii'),'big'); o=self.pe.va2f(self.slots[2]); path=[]; c=None
        for _ in range(48):
            i=self.ins(o); check(i.address in self.getcfg.instructions,'getter reachability'); path.extend(self.add(o))
            if o==arm: break
            if i.mnemonic=='cmp':
                check(i.op_str.startswith('edx, '),'4CC comes from EDX'); c=i.operands[1].imm
            nxt=o+i.size
            if i.mnemonic.startswith('j') and {'jg':x>c,'je':x==c,'jne':x!=c}[i.mnemonic]: nxt=self.direct(o)
            o=nxt
        check(o==arm and cmp_o in path and self.ins(cmp_o).operands[1].imm==x,'exact getter arm')
        i=self.ins(load_o); m=i.operands[1]; expected={'cash':('mov',4),'sour':('movsx',1),'inrt':('movss',4),'stdt':('movzx',2),'endt':('movzx',2)}[code]
        check(i.reg_name(m.mem.base)=='rbx' and (i.mnemonic,m.size)==expected and self.ins(0x153570c).op_str=='rbx, rcx','same object load')
        if code in ('stdt','endt'):
            yr=self.ins(0x1535e0e if code=='stdt' else 0x1535a09)
            check(yr.mnemonic=='movzx' and yr.operands[1].size==2 and yr.operands[1].mem.disp==m.mem.disp+2,'both u16 read by date getter')
        return dict(route=path,compare=cmp_o,arm=arm,load=load_o,object_offset=m.mem.disp)

def take(raw,p,w,label):
    check(p+w<=len(raw),f'{label}: short read @{p} width {w}')
    return raw[p:p+w]


def reject(fn):
    try:
        fn()
    except CheckError as e:
        return str(e)
    raise CheckError('negative probe accepted')


def archives():
    os.environ.setdefault('FM24_DB_DIR', str(ROOT/'scratch/data'))
    import fm24_dump as db
    codec=db._reader(); metadata={}
    for a in ('client','server'):
        fn=a+'_db.dat'; p=db.DB_DIR/fn
        d=codec['list_tables'](p,fn); e=[r for r in d if r['table_id']==33]
        metadata[a]={'directory_entry_count':len(d),'archive_sha256':sha(p.read_bytes()),'table33_entries':e,'present':bool(e)}
    check(not metadata['client']['present'] and len(metadata['server']['table33_entries'])==1,'table33 presence')
    metadata['client'].update(row_count=None,stride=None,payload_sha256=None)
    e,=metadata['server']['table33_entries']; frame=load(PROFILE)['payload']['packed_offset']
    with (db.DB_DIR/'server_db.dat').open('rb') as fh:
        fh.seek(e['offset']); probe=fh.read(frame-e['offset']+4)
        check(probe.endswith(db.MAGIC),'profile packed_offset lacks Zstd magic')
        fh.seek(frame); packed=fh.read(e['packed_size'])
    first=e['offset']+probe.index(db.MAGIC)
    first_raw=db.load_payload(codec,'server',33)
    raw=first_raw if first==frame and len(first_raw)==e['size'] else codec['_stream_decompress'](packed,256*1024*1024)
    check(len(raw)==e['size'] and S.unpack_from('<HI',raw,6)==(e['payload_version'],e['record_count_header']),'directory/payload header')
    metadata['server'].update(payload_len=len(raw),payload_sha256=sha(raw),zstd_frame_offset=frame,
                              first_frame_offset=first,default_load_payload_len=len(first_raw),used_profile_frame=(first!=frame or len(first_raw)!=e['size']))
    return metadata,raw,codec,db


def compare_t29(raw,s):
    pp,rr=(ROOT/PROFILE).read_bytes(),(ROOT/ROWS).read_bytes()
    d=json.loads(pp); p,c=d['payload'],d['row_closure']; n,w,end=s['row_count'],s['stride'],s['legacy_footer_start']
    check(d['table_type']==33 and d['archive']=='server' and p['payload_sha256']==sha(raw) and p['payload_size']==len(raw)
          and p['packed_offset']==s['zstd_frame_offset'] and p['packed_size']==s['table33_entries'][0]['packed_size']
          and (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'])==(n,w,14,end)
          and c['rows_sha256']==sha(raw[14:end]) and d['full_rows_file']=='profiles/table_server_33.rows.jsonl'
          and d['full_rows_sha256']==sha(rr),'t29 same payload and row-dump digests')
    rows=rr.splitlines(); check(len(rows)==n,'t29 row dump count')
    for i,line in enumerate(rows):
        at=14+i*w
        check(json.loads(line)=={'row':i,'offset':at,'len':w,'raw_hex':raw[at:at+w].hex()},f't29 row bytes {i}')
    inv=None
    if (ROOT/INV).is_file():
        q,=[x for x in load(INV)['parents'] if x['parent_4cc']=='Cdbt']
        check((q['table_type'],q['archive'],q['rtti_class'],q['reader_va'],q['count'],q['stride'])==
              (33,'server','STARTING_CLUB_DEBT',hex(SLOT),n,w) and
              [r['schema_idx'] for r in q['schema_item_fields']]==list(range(188,193)) and
              q['profile']['profile_sha256']==sha(pp) and q['profile']['rows_jsonl_sha256']==sha(rr),'t29 Cdbt inventory framing')
        inv={'path':INV,'sha256':sha((ROOT/INV).read_bytes()),'link_status':q['link_status'],'usage':'scout only; not field acceptance'}
    meta={'profile':PROFILE,'profile_sha256':sha(pp),'rows':ROWS,'rows_sha256':sha(rr),'legacy_block_sha256':c['rows_sha256'],
          'matched_full_rows':n,'inventory':inv}
    return {(r['offset'],r['width']):r for r in d['columns']},meta


def unsigned_match(bs,col):
    u=Counter(int.from_bytes(b,'little') for b in bs); max_uint=(1<<(8*col['width']))-1
    stats=[col[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
    check(stats==[len(bs),len(u),min(u),max(u),u[0],u[max_uint]],f't29 differential at +{col.get("offset")} width {col["width"]}')
    return stats


def read_row(st,raw,p,ordinal,cut=None):
    start=p; selector=take(raw,p,1,f'row {ordinal} selector')[0]; p+=1
    check(selector==0,f'row {ordinal}: selector {selector} @{start} outside observed domain (not factory rejection)')
    body=p; pc=THUNK; active=None; identity=None; stored=None; io=None; ts=[]; seq=[]
    for _ in range(len(st.edges)+2*26):
        native=pc if pc in st.transfers and pc not in DATE_CALLS else active if pc==DATE_READ else None
        if native is not None:
            tr=st.transfers[native]; w=tr['width']
            if p+w>len(raw) or cut==native:
                io=f'row {ordinal}: short transfer @{p} width {w} site {native:#x} consumer {pc:#x}'
                check(pc!=BULK,io+'; no immediate native bulk status test')
            else:
                if pc==BULK: identity=S.unpack_from('<III',raw,p)
                ts.append(dict(**tr,legacy_offset=p-body,wire_offset=p-start)); p+=w
        if pc in DATE_CALLS:
            check(active is None,'unexpected date nesting');active=pc;pc=DATE_THUNK
        elif pc in st.branches:
            b=st.branches[pc]
            if pc==ID:
                check(identity is not None,'identity before branch')
                taken=identity[0]<10000001;stored=identity[0] if taken else ordinal
            elif b['class']=='IO-result':
                taken=(b['observed_edge']=='taken')==(io is None)
            else:
                taken=b['observed_edge']=='taken'
            seq.append([pc,taken,active]);pc=b['taken_to' if taken else 'fallthrough_to']
        elif pc==0x39dd7f8:
            pc=active+st.ins(active).size;active=None
        elif pc==0x4367d38:
            raise CheckError(f'{io}; IO-result -> {FAIL:#x} (AL=false)')
        elif pc==0x3c6016d:
            rid,a,b=identity
            check(rid==stored==ordinal and a==b and a!=0,f'row {ordinal}: identity @{p-12} raw={identity}, stored ordinal={stored}')
            return dict(ordinal=ordinal,selector_start=start,body_start=body,body_end=p,identity=list(identity),
                        body_sha256=sha(raw[body:p]),wire_hex=raw[start:p].hex()),ts,seq
        else:
            pc,=st.edges[pc]
    raise CheckError('reader did not terminate')


def footer(raw,p):
    out=[]
    for d,w in ((0,4),(4,1),(5,4)):
        out.append(int.from_bytes(take(raw,p+d,w,'footer'),'little'))
        if d==0: check(out[0]==0,f'footer vector count {out[0]} @{p}: observed 0; nonzero path would need 12 B/element')
    check(out[1]==1 and p+9==len(raw),f'footer @{p}: invalid flag or end')
    return out


def walk(st,raw):
    check(raw[:8]==bytes.fromhex('03017461642ef10d') and len(raw)>=13,'header marker/version')
    n,h=S.unpack_from('<IB',raw,8);check(h==0,'observed header byte')
    p=13;trace=sha256();samples=[];sels=Counter();seen=set();edges=Counter();tpl=None
    for i in range(n):
        row,ts,seq=read_row(st,raw,p,i);sels[raw[p]]+=1
        if tpl is None:tpl=ts,seq
        check(tpl==(ts,seq),f'row {i}: nonuniform reader path')
        rid,a,b=row['identity'];end=row['body_end'];check(a not in seen,f'row {i}: duplicate identity {a}');seen.add(a)
        edges.update((o,t,ctx) for o,t,ctx in seq);trace.update(S.pack('<7I',i,p,p+1,end,rid,a,b)+bytes.fromhex(row['body_sha256']))
        if i in (0,1,2,n//2,n-1):samples.append(row)
        p=end
    ff=footer(raw,p);tr,seq=tpl;w=1+sum(t['width'] for t in tr)
    check(n==32409 and w==79 and p-13==n*w,'stride derived from executed graph')
    return dict(row_count=n,stride=w,row_bytes=p-13,header_hex=raw[:13].hex(),wire_origin=13,legacy_origin=14,
                wire_footer_start=p,legacy_footer_start=p+1,wire_footer_hex=raw[p:].hex(),legacy_footer_hex=raw[p+1:].hex(),
                footer_values=ff,footer_transfers=[dict(site=o,offset=p+d,width=w,value=v) for o,d,w,v in zip(FOOT,(0,4,5),(4,1,4),ff,strict=True)],
                uid_min=min(seen),uid_max=max(seen),selector_histogram=dict(sels),row_trace_sha256=trace.hexdigest(),samples=samples,
                row_template=dict(id=0,condition_edges=seq,wire_selector='13+79*i',legacy_body='14+79*i',body_end_exclusive='92+79*i',
                   trace_digest_record='LE <7I>(i,selector,body,end,identity0,identity1,identity2) + SHA-256 bytes of body')),tr,edges


def values(raw,s,tr):
    o,w=tr['legacy_offset'],tr['width']
    return [raw[p+o:p+o+w] for p in range(14,s['legacy_footer_start'],s['stride'])]


def item_profile(code,bs,tr,col,spec):
    n=len(bs);o=tr['legacy_offset'];w=tr['width']
    u=unsigned_match(bs,col)
    def example(i,x):return dict(row=i,offset=14+i*79+o,value=x,hex=bs[i].hex())
    def first(pred,xs):return next((example(i,x) for i,x in enumerate(xs) if pred(x)),None)
    if code in ('stdt','endt'):
        check(w==4,'date width'); xs=[S.unpack('<HH',b) for b in bs]
        ys={y for _,y in xs};bad=lambda x:not(1<=x[0]<=366 and 1850<=x[1]<=2100)
        t=col['packed_day_year'];narrow=lambda x:not(1<=x[0]<=366 and 1900<=x[1]<=2035)
        subset=[(d,y) for d,y in xs if not narrow((d,y))];sy={y for d,y in subset}
        check([t[k] for k in ('nonblank_count','valid_count','year_min','year_max','year_distinct','day_max')]==
              [n,len(subset),min(sy),max(sy),len(sy),max(d for d,_ in subset)],'t29 packed date diagnostics')
        return 'packed_u16_day_year',dict(day_bounds=[1,366],year_bounds=[1850,2100],mid7='zero in valid day lane'),dict(count=n,
            distinct=len(set(xs)),year_min=min(ys),year_max=max(ys),year_distinct=len(ys),day_min=min(d for d,_ in xs),day_max=max(d for d,_ in xs),
            mid7_nonzero=sum(bool(d&0xfe00) for d,_ in xs),default_1900_day1_count=xs.count((1,1900)),violations=sum(map(bad,xs)),
            first_violation=first(bad,xs),t29_narrow_valid=len(subset),first_outside_t29_narrow=first(narrow,xs),t29_unsigned_stats=u)
    if code=='inrt':
        check(w==4,'binary32 width'); xs=[S.unpack('<f',b)[0] for b in bs];fs=Counter(xs);norm=[x for x in xs if math.isfinite(x) and x not in (-99.,-1.)]
        lo,hi=min(norm),max(norm); fp=col['float32'];bad=lambda x:not math.isfinite(x) or (x<0 and x not in (-99.,-1.))
        finite=sum(math.isfinite(x) for x in xs)
        check((fp['finite_count'],fp['min_finite'],fp['max_finite'])==(finite,min(xs),max(xs)),'t29 float32 diagnostics')
        ix=next(i for i,x in enumerate(xs) if 0<x<1)
        return 'ieee754_binary32_le',dict(native_specials={'-99':'boxed float 0','-1':'empty variant'},ordinary_profile='finite nonnegative; no XML max or units inferred'),dict(
            count=n,distinct=len(fs),min=min(xs),max=max(xs),finite_count=finite,zero_count=fs[0.],minus_99_count=fs[-99.],minus_one_count=fs[-1.],
            ordinary_min=lo,ordinary_max=hi,violations=sum(map(bad,xs)),first_violation=first(bad,xs),
            first_minus_99=first(lambda x:x==-99.,xs),first_minus_one=first(lambda x:x==-1.,xs),
            fractional_fixture=dict(**example(ix,xs[ix]),raw_i32=int.from_bytes(bs[ix],'little',signed=True)),t29_unsigned_stats=u)
    check(w==(4 if code=='cash' else 1),'cash or enum width');xs=[int.from_bytes(b,'little',signed=True) for b in bs];h=Counter(xs)
    if code=='cash':
        bounds=[int(spec[k]) for k in ('min_value','max_value')];domain=dict(xml_bounds=bounds);kind='i32_le';bad=lambda x:not bounds[0]<=x<=bounds[1]
    else:
        check('enum_ref' not in spec,'unexpected enum catalog'); domain=dict(native_signed_bounds=[-128,127],enum_ref=None,labels=None,
            list_excluded_for_R8D_zero=[-5,-3,0]);kind='i8_enum';bad=lambda x:not -128<=x<=127
    return kind,domain,dict(count=n,distinct=len(h),min=min(h),max=max(h),zero_count=h[0],minus_one_count=h[-1],violations=sum(map(bad,xs)),
        first_violation=first(bad,xs),histogram=dict(sorted(h.items())) if code=='sour' else None,
        first_collection_exclusion=first(lambda x:x in (-5,-3,0),xs) if code=='sour' else None,t29_unsigned_stats=u)


def references(raw,s,tr,codec,db,cols):
    # Reuse only existing target framing; no target fields are interpreted.
    t24=ROOT/'scratch/t24/out';cx=load(t24/'cursor.json');club=db.load_payload(codec,'client',3)
    check(sha(club)==cx['provenance']['payload_sha256'],'club target SHA'); domain={};p=13
    for part in cx['rows']['shards']:
        for i,k,sel,end, *rest in load(t24/part)['rows']:
            j,a,b=S.unpack_from('<III',club,end-12)
            check(k==p+1 and j==i==len(domain) and a==b==rest[-1] and club[p]==sel,'club ordinal/identity target')
            domain[i]=a;p=end
    check(len(domain)==84259 and p==len(club)-9,'club target closure')
    comp=db.load_payload(codec,'client',25);c=S.unpack_from('<I',comp,8)[0];check(c==7047 and len(comp)==13+c*127+9,'comp target framing')
    comps={}
    for i in range(c):
        j,a,b=S.unpack_from('<III',comp,128+127*i);check(j==i and a==b,'comp target ordinal/identity');comps[j]=a
    result=[]
    for obj,target,buf,ids in ((0x18,'club/table3',club,domain),(0x20,'comp/table25',comp,comps)):
        q,=[x for x in tr if x['object_offset']==obj];bs=values(raw,s,q);o=q['legacy_offset'];v=[S.unpack('<i',b)[0] for b in bs];live=[(i,x) for i,x in enumerate(v) if x!=-1];uids=set(ids.values())
        def cross(d):
            bad=[(i,x) for i,x in live if x not in d];return dict(matches=len(live)-len(bad),misses=len(bad),first_miss=next((dict(row=i,value=x,offset=14+i*79+o,hex=bs[i].hex()) for i,x in bad),None))
        a,z=cross(ids),cross(uids); ix,x=live[0]
        result.append(dict(object_offset=obj,legacy_offset=o,wire_offset=o+1,width=4,target=target,target_payload_sha256=sha(buf),target_count=len(ids),
                      evidence='slot21 writes target +8 or -1; slot20 resolves i32 to pointer',null_count=v.count(-1),ordinal=a,uid_hypothesis=z,
                      first_live=dict(row=ix,offset=14+ix*79+o,value=x,target_uid=ids.get(x)),t29_unsigned_stats=unsigned_match(bs,cols[o,4])))
    return result


def ledger(st,raw,s,tr,columns,refs):
    parent,=[p for p in load(MASTER)['entities']['club.xml'][0]['fields'] if p['field']=='Cdbt']; specs=parent['list_item_fields']
    occ=[r for f in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for r in load(f)['nested_fields'] if r['parent']=='Cdbt']
    check(len(specs)==len({x['field'] for x in specs})==5 and [r['idx'] for r in occ]==list(range(188,193)),'unique scoped schema')
    records=[]
    for spec,x in zip(specs,occ,strict=True):
        code=spec['field'];check((x['code'],x['name'],x['type'],x['optional'])==(code,spec['name'],spec['type'],spec.get('is_optional')=='true'),'t24 schema join')
        g=st.getter(code);s0,=[t for t in tr if t['object_offset']==g['object_offset']];o,w=s0['legacy_offset'],s0['width']
        kind,domain,p=item_profile(code,values(raw,s,s0),s0,columns[o,w],spec);ok=not p['violations']
        records.append(dict(code=code,name=spec['name'],schema=spec,schema_scope=[*SCOPE,x['idx']],getter=g,
                            sink={k:s0[k] for k in ('site','consumer','object_offset','width','legacy_offset','wire_offset')},
                            row_offset=o if ok else None,wire_offset=o+1 if ok else None,interpretation=kind,domain=domain,profile=p,
                            grade='L3_named_row_coordinate' if ok else 'held_static_sink_profile_conflict'))
    return dict(scope=SCOPE,table_type=33,occurrences=5,baseline_L3=0,L3=sum(r['grade'].startswith('L3') for r in records),L4=0,
                fields=records,unscoped_references=refs,unscoped_properties_bytes=66-sum(r['sink']['width'] for r in records))


def build():
    st=Static(); support=st.scope_support();a,raw,codec,db=archives();s=a['server']
    result,tr,edges=walk(st,raw);s.update(result);cols,t29=compare_t29(raw,s); refs=references(raw,s,tr,codec,db,cols);fields=ledger(st,raw,s,tr,cols,refs)
    short={t['site']:reject(lambda:read_row(st,raw,13,0,cut=t['site'])) for t in tr}
    o=14+tr[-1]['legacy_offset'];e=s['wire_footer_start']
    overwrite=reject(lambda:read_row(st,raw[:o]+S.pack('<I',10000001)+raw[o+4:],13,0))
    s['negative_replays']=dict(short_transfers=[dict(site=k,first_counterexample=v) for k,v in short.items()],raw_ordinal_overwrite=overwrite,
        mismatched_identity_lanes=reject(lambda:read_row(st,raw[:o+8]+bytes(4)+raw[o+12:],13,0)),
        selector_not_observed=reject(lambda:read_row(st,raw[:13]+b'\x01'+raw[14:],13,0)),
        short_footer=reject(lambda:footer(raw[:-1],e)),nonzero_vector=reject(lambda:footer(raw[:e]+b'\x01'+raw[e+1:],e)))
    bs=[]
    for o,b in sorted(st.branches.items()):
        ev=b['evidence'][0]; alt=short[ev] if b['class']=='IO-result' else overwrite if o==ID else b['alternative_or_first_counterexample']
        contexts={str(x):[edges[o,True,x],edges[o,False,x]] for x in (*DATE_CALLS,None) if edges[o,True,x]+edges[o,False,x]}
        bs.append(dict(**{k:v for k,v in b.items() if k!='alternative_or_first_counterexample'},
                       alternative_or_first_counterexample=alt,scope='reader' if o>=START else 'date_helper' if o< TAIL else 'identity_tail',
                       taken_count=sum(x[0] for x in contexts.values()),fallthrough_count=sum(x[1] for x in contexts.values()),context_counts=contexts))
    bs.extend(dict(**b,scope='loader_footer_factory_slice') for b in st.loader.values())
    OUT.mkdir(parents=True,exist_ok=True)
    cursor=dict(status='complete_observed_row_cursor',scope=SCOPE,table_type=33,provenance=dict(editor=str(EXE),editor_sha256=EXE_SHA,snapshot_manifest=st.snap),
        factory=st.factory,rtti=st.rtti,slots=st.slots,scope_evidence=support,real_constants=st.sentinels,
        reader=dict(chain=[THUNK,START,JUMP,TAIL_THUNK,TAIL],date_chain=[*DATE_CALLS,DATE_THUNK,DATE,DATE_READ],extents=st.extents,
            extent_source='PE exception directory RUNTIME_FUNCTION',condition_count=len(st.branches),runtime_mode_forks=[],
            mode_proof='No row-layout predicate reads a stack mode or R9. Body forwards R9, resets R8D; identity tail loads the raw lane, uses caller ordinal/table this, and sets R9B for the callback. Separate slot20 fixup flags are not reader layout controls.'),
        archives=a,t29=t29,transfers=[dict(site=SELECT,legacy_offset=-1,wire_offset=0,width=1,sink='loader stack+0x43'),*tr],loader_transfers=st.loader_transfers,
        wire_alignment=f'13 + 32409*(1+66+12) + 9 = {len(raw)}',legacy_alignment=f'14 + 32409*79 + 8 = {len(raw)}; legacy +78 borrows next selector/first footer byte',
        branch_taxonomy=CLASSES,branch_census={c:sum(r['class']==c for r in bs) for c in CLASSES},
        limits=['Foot vector count and selector zero specialize the observed archive only.',
                'No immediate native bulk status check. Callback/destruction are opaque; replay assumes live retained stream/owner and table this.',
                'Footer last u32 at table+0x50 equals both header count and max UID; no general meaning inferred.',
                'Cdbt parent filters by source and repaired club reference; physical rows are not all displayed under Cdbt.'],
        branch_shards=shards('branches',bs,24),instruction_shards=shards('instructions',[st.records[o] for o in sorted(st.records)],120))
    write('cursor_cdbt.json',cursor);write('fields_cdbt.json',fields)
    print(f"t36 build PASS: {s['row_count']} x {s['stride']} B; {fields['L3']}/5 L3, {5-fields['L3']} held, L4=0")


def selftest():
    check(take(b'abc',1,2,'fixture')==b'bc' and 'short read @1' in reject(lambda:take(b'abc',1,3,'fixture')),'bounded transfer')
    b=S.pack('<HH',366,2073);check(S.unpack('<HH',b)==(366,2073) and int.from_bytes(b,'little')&0xfe00==0,'packed date')
    check(S.unpack('<f',bytes.fromhex('0000c6c2'))==(-99.0,) and footer(S.pack('<IBI',0,1,42),0)==[0,1,42],'binary32 and footer')
    print('t36 builder selftest PASS')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test bounded transfers and field encodings')
    try:
        selftest() if p.parse_args().selftest else build()
        return 0
    except CheckError as e:
        print(f't36 check failed: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't36 fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
