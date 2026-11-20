#!/usr/bin/env python3
"""Build the offline FM24 Cmti/table 43 cursor and scoped field ledger."""
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
OUT = ROOT/'scratch/t32/out'
EXE = Path('<OLD_REPO>/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_43.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_43.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
SCOPE = ['club.xml','Cmti']
VT, SLOT = 0x141883a68, 0x14153d0a0
THUNK, START, END, JUMP, TAIL_THUNK, TAIL, TAIL_END = 0x153c6a0, 0x4370860, 0x43709c6, 0x43709c1, 0xfae340, 0x3c600f0, 0x3c6016e
FAIL, BULK, ID, SELECT = 0x437099e, 0x3c60119, 0x3c60131, 0xf2ba0e
FOOT = (0xffa602, 0xf2baa2, 0xf2bac2)
CLASSES = ['wire_data','runtime-external','IO-result','context-lifecycle','dead']
# consumer, destination LEA, width MOV, status producer, branch, optional wire pair normalization JNE
ARGS = (
    (0x437088f,0x437087b,0x4370886,0x43708b4,0x43708b6,0x4370896),
    (0x43708d8,0x43708c4,0x43708cf,0x43708fd,0x43708ff,0x43708df),
    (0x4370921,0x437090d,0x4370918,0x4370946,0x4370948,0x4370928),
    (0x437095d,0x437094d,0x4370954,0x4370960,0x4370964,None),
    (0x4370979,0x4370969,0x4370970,0x437097c,0x4370980,None),
    (0x4370995,0x4370985,0x437098c,0x4370998,0x437099c,None),
)
# 4CC match and first instruction of its semantic arm, not a name vote.
GET = {'icom':(0x153c9c4,0x153c9d0),'play':(0x153ca04,0x153ca10),'club':(0x153c9b8,0x153ca7f),
       'cash':(0x153c9b0,0x153ca21),'mths':(0x153c9ec,0x153ca9b),'pyiv':(0x153c9f8,0x153caf9)}


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
        check(self.slots[19]==SLOT and (self.rtti['class'],self.rtti['col_off'])==('STARTING_MONTHLY_INSTALLMENT',0x18859c0),'RTTI/slot19')
        base, handler = 0xf49d38, 0xf49675
        cell = base+4*43
        rel, = S.unpack_from('<i',self.pe.raw,cell)
        check(base+rel==handler and self.rip(0xf48b45)==self.pe.f2va(base) and self.rip(0xf496a2)==VT and
              self.ins(0xf496a9).op_str=='qword ptr [rsi], rax' and self.direct(0xf496c8)==0xf49ca9,'factory dispatch/constructor')
        self.factory = {'jump_base':base,'cell':cell,'rel32':rel,'cell_bytes':self.pe.raw[cell:cell+4].hex(),
                        'dispatch':self.span(0xf48b30,0xf48b55),'handler':self.span(handler,0xf496cd),'return':self.span(0xf49ca9,0xf49cb3)}
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
        t,b={},{}
        for o,l,w,p,j,norm in ARGS+((BULK,0x3c60106,0x3c6010d,None,None,None),):
            lea,r8=self.ins(l),self.ins(w)
            check(self.ins(o).op_str=='qword ptr [rax + 0x28]' and lea.mnemonic=='lea' and
                  lea.op_str.startswith('rbx, [rdi + ' if o==BULK else 'rdx, [rbx + ') and r8.op_str.startswith('r8d, '),'read setup')
            obj,width=lea.operands[1].mem.disp,r8.operands[1].imm
            t[o]={'site':o,'consumer':o,'object_offset':obj,'width':width,'setup':self.add(l,w),
                  'kind':'identity_bulk' if o==BULK else 'member'}
            if norm is not None:
                q=o+self.ins(o).size; copy=norm+self.ins(norm).size
                check(width==8 and self.ins(q).op_str==f'dword ptr [rbx + {obj+4:#x}], 0' and
                      self.ins(copy).op_str==f'eax, dword ptr [rbx + {obj:#x}]' and
                      self.ins(copy+self.ins(copy).size).op_str==f'dword ptr [rbx + {obj+4:#x}], eax' and
                      self.direct(norm)==copy+self.ins(copy).size+self.ins(copy+self.ins(copy).size).size,'paired lane zero normalization')
                b[norm]=self.branch(norm,q,'wire_data','second i32 from the 8-byte key; zero copies lane 0 without consuming bytes',
                                    (o,copy,copy+self.ins(copy).size),'taken',None)
                t[o]['zero_lane_branch']=norm
            if p is not None:
                saved=norm is not None
                check(self.ins(p).op_str==('ebp, ebp' if saved else 'dword ptr [rsi + 0x10], 0'),'IO status predicate')
                taken=self.ins(j).mnemonic=='je'; check((j+self.ins(j).size if taken else self.direct(j))==FAIL,'native AL=false edge')
                status=self.direct(norm) if saved else p
                check(self.ins(status).op_str==('ebp, dword ptr [rsi + 0x10]' if saved else 'dword ptr [rsi + 0x10], 0'),'status origin')
                b[j]=self.branch(j,p,'IO-result','stream +0x10 saved across release' if saved else 'direct stream +0x10 status',
                                 (o,status,FAIL),'taken' if taken else 'fallthrough',None)
        for j,p,load_stream,rejoin,deref in [(0x4370879,0x4370876,0x4370873,0x4370892,0x437089e),
                                           (0x43708c2,0x43708bf,0x43708bc,0x43708db,0x43708e7),
                                           (0x437090b,0x4370908,0x4370905,0x4370924,0x4370930)]:
            check(self.direct(j)==rejoin and self.ins(rejoin).mnemonic=='cmp' and
                  self.ins(deref).op_str=='ebp, dword ptr [rsi + 0x10]','null skips transfer, but rejoined status dereferences')
            b[j]=self.branch(j,p,'context-lifecycle','stream pointee from wrapper, not a caller layout mode',
                             (load_stream,rejoin,deref),'fallthrough',
                             f'row 0: injected null skips transfer, tests object pair, then dereferences null at {deref:#x}; not a valid alternate layout')
        for j,p,retain,dtor in [(0x43708a5,0x43708a1,0x437087f,0x43708b2),(0x43708ee,0x43708ea,0x43708c8,0x43708fb),
                                 (0x4370937,0x4370933,0x4370911,0x4370944)]:
            b[j]=self.branch(j,p,'context-lifecycle','local retain/release; ZF from dec after preserving stream status',
                             (retain,dtor,0xf2ba48),'taken',f'row 0: injected last reference invokes opaque destructor {dtor:#x}; live wrapper retains its stream')
        for j,p,cls,src,ev,edge,alt in [
            (0x3c60100,0x3c600fd,'context-lifecycle','same stream pointee as member reads',(0x4370982,0x43709ae,0x3c600fa),'fallthrough','row 0: null cannot follow successfully completed member I/O; injected tail-only null would skip the 12-byte identity'),
            (ID,0x3c6012a,'wire_data','unsigned raw identity lane 0 vs 10000001',(BULK,0x3c60127,0x3c60133,0x3c60138,0xf2ba3d),'taken',None),
            (0x3c6013e,0x3c6013b,'context-lifecycle','callback table this from caller stack, not R9',(0xf2b679,0xf2ba33,0x3c60122,0x3c60149),'fallthrough','row 0: caller passes table this; null would skip callback after bulk with no explicit transfer'),
            (0x3c6014f,0x3c6014c,'context-lifecycle','release checks same saved stream',(0x3c600fa,0x3c60102),'fallthrough','row 0: null stream would already lack identity'),
            (0x3c60155,0x3c60151,'context-lifecycle','ZF from decrement after local retain',(0x3c60102,0x3c60162,0xf2ba48),'taken','row 0: last reference would call opaque destructor; wrapper owns a live stream')]:
            b[j]=self.branch(j,p,cls,src,ev,edge,alt)
        check({o for o in self.edges if self.ins(o).mnemonic.startswith('j') and self.ins(o).mnemonic!='jmp'}==b.keys(),'complete branch census')
        check({o for o in self.edges if self.ins(o).mnemonic=='call'}-t.keys()=={0x43708b2,0x43708fb,0x4370944,0x3c60149,0x3c60162},'all non-transfer calls')
        return t,b

    def loader_model(self):
        # Same generic outer path as t31, specialized only for the case-43 constructor and record count.
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
            (0xf2baa9,0xf2baa5,FOOT[1],'fallthrough','after row 534: short footer flag @24627 width 1'),
            (0xf2bac9,0xf2bac5,FOOT[2],'fallthrough','after row 534: short footer last lane @24628 width 4'),
            (0xffa7af,0xffa7ab,0xffa7a8,'not visited','footer vector count 0; count 1 and short lane 0 would fail'),
            (0xffa7ce,0xffa7ca,0xffa7c7,'not visited','footer vector count 0; count 1 and short lane 1 would fail'),
            (0xffa7ed,0xffa7e9,0xffa7e6,'not visited','footer vector count 0; count 1 and short lane 2 would fail'),
            (0xffa7fa,0xffa7f6,0xffa7e6,'not visited','footer vector count 0; count 1 and nonzero final triplet status would fail'),
        ]:
            add(o,p,'IO-result','stream +0x10 status',(t,),edge,alt)
        add(0xf2ba89,0xf2ba84,'IO-result','footer vector helper return (status or bound error)',(0xf2ba7f,0xffa9a3,0xffa9b6),'fallthrough','after row 534: short vector count @24623 width 4 (replay); native helper checks status on nonzero paths')
        add(0xf2ba59,0xf2ba57,'IO-result','slot19 AL; explicit false for member IO error',(0xf2ba51,FAIL,0x3c60164),'taken','row 0: short first member @14 -> AL=false under IO error contract')
        add(0xf2ba2b,0xf2ba28,'context-lifecycle','factory result; table43 arm does not inspect selector',(SELECT,0xf2ba1b,0xf2ba20,0xf2ba23,0xf496a2),'fallthrough','row 0: case43 constructs vptr; null result would skip slot19 and lose the body')
        add(0xf2b9db,0xf2b9d6,'wire_data','header count, zero bypasses row loop',(0xf2b691,),'fallthrough','before row 0: real count=535, not 0')
        add(0xf2b9fa,0xf2b9f7,'wire_data','next ordinal vs header count',(0xf2b691,0xf2b9f0,0xf2b9f3),'both','after row 0: next=1<count; after row 534: next=count')
        add(0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end; same helper with same R8',(0xf2ba60,0xf2ba6e,0xf2ba72),'same cursor','both edges preserve footer cursor; actual pre-existing capacity is not from payload')
        add(0xffa610,0xffa609,'wire_data','footer vector count compared against process maximum',(FOOT[0],0xffa605,0xffa9a3),'fallthrough','footer count=0; out-of-bound count would return helper error')
        add(0xffa640,0xffa638,'context-lifecycle','existing vector capacity vs wire count',(0xffa61b,0xffa61f,0xffa646),'taken','footer count=0; no valid capacity below zero')
        add(0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets',(FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab),'taken','footer count=0; synthetic nonzero count would need 12 B/element')
        add(0xffa77f,0xffa77c,'wire_data','triplet loop index vs count',(0xffa775,0xffa778),'not visited','footer count=0; no first triplet')
        add(0xf48b3b,0xf48b38,'runtime-external','outer directory table type, not selector or caller layout mode',(0xf2ba20,0xf48b30,0xf48b45),'fallthrough','row 0: directory table type 43 <= factory bound; a different table type is outside scope')
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
        check(self.direct(0xe842b9)==0xe831c5 and self.direct(0xe831e4)==0xe57de0 and
              self.direct(0xe58339)==0x1523b10 and self.direct(0xe58355)==0xea12d0 and self.direct(0xea14d6)==0x153ce50 and
              self.direct(0x153ce50)==0x4371980,'Cmti collection/getter family')
        check(all(self.ins(o).operands[1].imm==int.from_bytes(b'Cmti','big') for o in (0xe842b3,0xe5831c)),'Cmti parent dispatch')
        check([self.direct(o) for o in (0x153c9a3,0xfe7ad0,0x153ccf4,0x153ccc1,0xf79f40,0x153c810)]==
              [0xfe7ad0,0x3ccca60,0xfe68b0,0xf79f40,0x3bf0bc0,0x4370ce0],'key helpers, current-club context, writer')
        return {'parent_dispatch':self.span(0xe842b3,0xe842bf)+self.span(0xe831c5,0xe831e9)+self.span(0xe5831c,0xe5835f),
            'parent_collection_keys':self.span(0x1523bd8,0x1523c11)+self.span(0x1523c43,0x1523cc8),
            'editor_context_and_slot3':self.add(0xea14d6,0x153ce50,0x3ccca90,0x3ccca96,0x3cccb2d,0x3cccb30,0xfe7ad0)+self.span(0x4371994,0x4371aad)+self.span(0x4371abf,0x4371b2d)+self.span(0x4371b3f,0x4371bcc),
            'boxed_person_key':self.span(0x153ca10,0x153ca21)+self.span(0xfe68c7,0xfe6913),
            'club_uid_resolver':self.add(0xf79f40,0x3bf0bcf,0x3bf0be5,0x3bf0c21,0x3bf0c25,0x3bf0c28,0x3bf0c2c,
                                          0x3bf0cad,0x3bf0cb1,0x3bf0cb4,0x3bf0cb8)+self.span(0x3bf0cc2,0x3bf0d17),
            'ref_fixup_noop_writer':self.span(0xbe0,0xbe3)+self.add(0x153c810)+self.span(0x4370d17,0x4370e23),
            'getter_semantic_arms':self.span(0x153ca21,0x153ca34)+self.span(0x153ca9b,0x153caae)+self.span(0x153caf9,0x153cb0d)+
                self.span(0x153c9d0,0x153c9ec)+self.span(0x153cb58,0x153cbb9)+self.span(0x153cc04,0x153cc18)+
                self.span(0x153ca7f,0x153ca9b)+self.span(0x153cc63,0x153ccfb),
            'runtime_arguments':self.add(0xf2ba33,0xf2ba38,0xf2ba3d,0xf2ba4b,0xf2ba4e,0x437086a,0x43709b1,0x43709b4,
                                         0x3c60122,0x3c60133,0x3c60146)}

    def getter(self,code):
        cmp_o,dest=GET[code]
        o=self.pe.va2f(self.slots[2]); x=int.from_bytes(code.encode('ascii'),'big')
        route=[]; cmp=None
        for _ in range(32):
            i=self.ins(o)
            check(i.address in self.getter_cfg.instructions,'getter reachable')
            route.extend(self.add(o))
            if o==dest:
                break
            if i.mnemonic=='cmp':
                check(i.op_str.startswith('esi, '),'4CC ESI compare, copied from EDX')
                cmp=i.operands[1].imm
            nxt=o+i.size
            if i.mnemonic.startswith('j'):
                nxt=self.direct(o) if {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic] else nxt
            o=nxt
        check(o==dest and cmp_o in route and self.ins(cmp_o).operands[1].imm==x,f'getter dispatch {code}')
        if code in ('cash','mths','pyiv'):
            i=self.ins(dest); operand=i.operands[1]
            check(operand.type==3 and i.reg_name(operand.mem.base)=='rdi' and i.mnemonic==('movsx' if code=='pyiv' else 'mov'),'scalar getter')
            bindings=[operand.mem.disp]
        elif code=='play':
            check(self.ins(0x153ca17).op_str=='edx, 0x50657273' and self.ins(dest).op_str=='rdi, 0x18' and
                  self.ins(0xfe68e4).op_str=='eax, dword ptr [rbx + 4]' and self.ins(0xfe68eb).op_str=='rbx, dword ptr [rbx]','8-byte person key')
            bindings=[0x18]
        elif code=='club':
            check(self.ins(0x153cc88).op_str=='rsi, [rdi + 0x20]' and self.ins(0x153ccb4).op_str=='rdi, 0x28' and
                  self.ins(0x153ccec).op_str=='edx, 0x43636c75','two alternate club key sinks')
            bindings=[0x20,0x28]
        else:
            check(self.ins(0x153cb73).op_str=='ecx, dword ptr [rdi + 0x28]' and self.ins(0x153cb78).op_str=='eax, dword ptr [rdi + 0x2c]' and
                  self.ins(0x153cbb2).op_str=='dword ptr [rbp - 8], 0' and self.ins(0x153cc0d).op_str=='dword ptr [rbp - 8], 1','direction is contextual, not a scalar wire sink')
            bindings=[]
        return {'route':route,'compare':cmp_o,'arm':o,'object_offsets':bindings}


def take(raw,p,w,label):
    check(p+w<=len(raw),f'{label}: short read @{p} width {w}')
    return raw[p:p+w]


def read_row(st,raw,p,ordinal,cut=None,fixture=False):
    start=p
    selector=take(raw,p,1,f'row {ordinal} selector')[0];p+=1
    check(selector==0,f'row {ordinal}: selector {selector} @{start} outside observed domain (not factory rejection)')
    body=p; pc=THUNK
    obj={0x18:(-1,-1),0x20:(-1,-1),0x28:(-1,-1)}
    io_error=None; lanes=None; stored=None; transfers=[]; conditions=[]
    statuses={j:o for o,_,_,_,j,_ in ARGS}
    normalize={j:st.transfers[o]['object_offset'] for o,_,_,_,_,j in ARGS if j is not None}
    for _ in range(len(st.edges)+1):
        if pc in st.transfers:
            tr=st.transfers[pc]; w=tr['width']; off=tr['object_offset']
            if p+w>len(raw) or pc==cut:
                msg=f'row {ordinal}: short transfer @{p} width {w} site {pc:#x}'
                if pc==BULK:
                    raise CheckError(msg+'; no immediate native bulk status test')
                io_error=msg     # model nonzero status, no bytes written on synthetic cut
            else:
                if pc==BULK:
                    lanes=S.unpack_from('<III',raw,p)
                elif w==8:
                    obj[off]=S.unpack_from('<ii',raw,p)
                transfers.append({**tr,'legacy_offset':p-body,'wire_offset':p-start})
                p+=w
        if pc in st.branches:
            b=st.branches[pc]
            if pc in normalize:
                off=normalize[pc]; a,z=obj[off]; taken=z!=0
                if not taken:
                    obj[off]=(a,a)
            elif pc==ID:
                check(lanes is not None,'identity predicate before bulk')
                taken=lanes[0]<10000001
                stored=lanes[0] if taken else ordinal
            elif pc in statuses:
                taken=(io_error is None)==(st.ins(pc).mnemonic=='je')
            else:
                taken=b['observed_edge']=='taken'
            conditions.append([pc,taken]); pc=b['taken_to' if taken else 'fallthrough_to']
        elif st.ins(pc).mnemonic=='ret':
            if pc==0x43709aa:
                check(io_error is None,f'{io_error}; IO-result -> {FAIL:#x} (AL=false)')
                raise CheckError('unexpected reader false')
            check(pc==0x3c6016d and st.ins(0x3c60164).op_str=='al, 1','native reader exit')
            rid,a,b=lanes
            check(rid==stored==ordinal and a==b and a!=0,f'row {ordinal}: identity @{p-12} raw={lanes}, stored ordinal={stored}')
            ret=dict(ordinal=ordinal,selector_start=start,body_start=body,body_end=p,identity=list(lanes),
                     body_sha256=sha(raw[body:p]),wire_hex=raw[start:p].hex())
            return ret,transfers,conditions,obj if fixture else None
        else:
            pc,=st.edges[pc]
    raise CheckError('nonterminating read')


def walk(st,raw):
    check(raw[:8]==bytes.fromhex('03017461642ef10d') and len(raw)>=13,'header marker/version')
    n,flag=S.unpack_from('<IB',raw,8)
    check(flag==0,'observed header byte')
    p=13; total=0; uids=set(); trace=sha256(); samples=[]; sels=Counter(); edges=Counter(); template=None
    for i in range(n):
        row,tr,c,_=read_row(st,raw,p,i); sels[raw[p]]+=1
        if template is None:
            template=(tr,c)
        check(template==(tr,c),f'row {i}: additional template not supported by this observed-archive seal')
        edges.update((site,taken) for site,taken in c)
        body,end=row['body_start'],row['body_end']; rid,a,b=row['identity']
        check(a not in uids,f'row {i}: duplicate identity {a}')
        uids.add(a); total+=end-p
        trace.update(S.pack('<7I',i,p,body,end,rid,a,b)+bytes.fromhex(row['body_sha256']));p=end
        if i in {0,1,2,n//2,n-1}:
            samples.append(row)
    footer=p
    vc=S.unpack('<I',take(raw,p,4,'footer vector count'))[0];p+=4
    check(vc==0,f'footer vector count {vc} @{footer} outside observed domain')
    ff=take(raw,p,1,'footer flag')[0];p+=1
    hi=S.unpack('<I',take(raw,p,4,'footer last lane'))[0];p+=4
    check(ff==1 and p==len(raw)==13+total+9,f'footer @{footer}: flag={ff}, last_u32={hi}, end={p}, len={len(raw)}')
    return dict(row_count=n,row_bytes=total,header_hex=raw[:13].hex(),wire_origin=13,legacy_origin=14,
                wire_footer_start=footer,legacy_footer_start=footer+1,wire_footer_hex=raw[footer:].hex(),legacy_footer_hex=raw[footer+1:].hex(),
                footer_values=[vc,ff,hi],uid_min=min(uids),uid_max=max(uids),selector_histogram=dict(sels),
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
        d=codec['list_tables'](p,fn); e=[r for r in d if r['table_id']==43]
        metadata[a]={'directory_entry_count':len(d),'archive_sha256':sha(p.read_bytes()),'table43_entries':e,'present':bool(e)}
    check(not metadata['client']['present'] and len(metadata['server']['table43_entries'])==1,'table43 presence')
    metadata['client'].update(row_count=None,stride=None,payload_sha256=None)
    e,=metadata['server']['table43_entries']; frame=load(PROFILE)['payload']['packed_offset']
    with (db.DB_DIR/'server_db.dat').open('rb') as fh:
        fh.seek(e['offset']); probe=fh.read(frame-e['offset']+4)
        check(probe.endswith(db.MAGIC),'profile packed_offset lacks Zstd magic')
        fh.seek(frame); packed=fh.read(e['packed_size'])
    first=e['offset']+probe.index(db.MAGIC)
    first_raw=db.load_payload(codec,'server',43)
    raw=first_raw if first==frame and len(first_raw)==e['size'] else codec['_stream_decompress'](packed,256*1024*1024)
    check(len(raw)==e['size'] and S.unpack_from('<HI',raw,6)==(e['payload_version'],e['record_count_header']),'directory/payload header')
    metadata['server'].update(payload_len=len(raw),payload_sha256=sha(raw),zstd_frame_offset=frame,
                              first_frame_offset=first,default_load_payload_len=len(first_raw),used_profile_frame=(first!=frame or len(first_raw)!=e['size']))
    return metadata,raw,codec,db


def targets(codec,db):
    # Read target identities ONLY. No person attributes or new Club layout work.
    blob=(db.DB_DIR/'basic_people_db.dat').read_bytes()
    check(blob[:12]==bytes.fromhex('03017461642ef10d28b52ffd'),'basic people direct frame')
    buf=codec['_stream_decompress'](blob[8:],128*1024*1024); n,flag=S.unpack_from('<IB',buf)
    check((n,flag)==(658011,0),'person framing (t01j grammar)')
    p=5; lengths={1:83,2:83,3:83,4:34,5:22}; ids={}; ords=set()
    for i in range(n):
        tag,cls=buf[p:p+2]; check(tag==17 and cls in lengths,f'person row {i} tag/class')
        p+=lengths[cls];o,a,b=S.unpack_from('<Iii',buf,p-12)
        check(o==i and a==b,f'person row {i} identity')
        ords.add(o)
        if cls==2:
            check((a,b) not in ids,'class 2 duplicate identity')
            ids[a,b]=o
    check(buf[p:]==bytes.fromhex('00000000014cbd5477'),'person footer')
    info={'person':{'archive':'basic_people_db.dat','source':'t01j target identity framing; class 2 join',
                    'archive_sha256':sha(blob),'payload_sha256':sha(buf),'row_count':n,'key_count':len(ids),'ordinal_count':len(ords),
                    'ordinal_bounds':[min(ords),max(ords)],'target_class':2}}
    domains={'person':(ids,ords)}
    f=ROOT/'scratch/t24/out'; trace=load(f/'cursor.json'); buf=db.load_payload(codec,'client',3)
    check(sha(buf)==trace['provenance']['payload_sha256'] and S.unpack_from('<I',buf,8)[0]==trace['row_count']==84259,'club target fingerprint')
    p=14; ids={}; ords=set(); dig=sha256()
    for part in trace['rows']['shards']:
        blob=(f/part).read_bytes();dig.update(blob)
        for i,body,selector,end,*rest in json.loads(blob)['rows']:
            check(body==p and selector==buf[body-1] and body+12<end,'club target row framing')
            o,a,b=S.unpack_from('<Iii',buf,end-12)
            check(o==i==len(ords) and a==b==rest[-1] and (a,b) not in ids,'club target identity')
            ids[a,b]=o; ords.add(o); p=end+1
    check(p==int(trace['old_footer'],16)==len(buf)-8 and len(ords)==84259,'club target closure')
    info['club']={'archive':'client','table_type':3,'source':'t24 closed target row ends; re-read archive identity lanes','payload_sha256':sha(buf),
                  'trace_sha256':dig.hexdigest(),'row_count':len(ords),'key_count':len(ids),'ordinal_count':len(ords),'ordinal_bounds':[min(ords),max(ords)]}
    return {**domains,'club':(ids,ords)},info


def compare_t29(raw,s):
    pp,rr=(ROOT/PROFILE).read_bytes(),(ROOT/ROWS).read_bytes()
    d=json.loads(pp); p,c=d['payload'],d['row_closure']; n,w,end=s['row_count'],s['stride'],s['legacy_footer_start']
    check(d['table_type']==43 and d['archive']=='server' and p['payload_sha256']==sha(raw) and p['payload_size']==len(raw)
          and p['packed_offset']==s['zstd_frame_offset'] and p['packed_size']==s['table43_entries'][0]['packed_size']
          and (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'])==(n,w,14,end)
          and c['rows_sha256']==sha(raw[14:end]) and d['full_rows_file']=='profiles/table_server_43.rows.jsonl'
          and d['full_rows_sha256']==sha(rr),'t29 same payload and row-dump digests')
    rows=rr.splitlines(); check(len(rows)==n,'t29 row dump count')
    for i,line in enumerate(rows):
        at=14+i*w
        check(json.loads(line)=={'row':i,'offset':at,'len':w,'raw_hex':raw[at:at+w].hex()},f't29 row bytes {i}')
    inv=None
    if (ROOT/INV).is_file():
        q,=[x for x in load(INV)['parents'] if x['parent_4cc']=='Cmti']
        check((q['table_type'],q['archive'],q['rtti_class'],q['reader_va'],q['count'],q['stride'])==
              (43,'server','STARTING_MONTHLY_INSTALLMENT',hex(SLOT),n,w) and
              [r['schema_idx'] for r in q['schema_item_fields']]==list(range(213,219)) and
              q['profile']['profile_sha256']==sha(pp) and q['profile']['rows_jsonl_sha256']==sha(rr),'t29 Cmti inventory framing')
        inv={'path':INV,'sha256':sha((ROOT/INV).read_bytes()),'link_status':q['link_status'],'usage':'scout only; not field acceptance'}
    meta={'profile':PROFILE,'profile_sha256':sha(pp),'rows':ROWS,'rows_sha256':sha(rr),'legacy_block_sha256':c['rows_sha256'],
          'matched_full_rows':n,'inventory':inv}
    return {(r['offset'],r['width']):r for r in d['columns']},meta


def unsigned_match(bs,col):
    u=Counter(int.from_bytes(b,'little') for b in bs); max_uint=(1<<(8*col['width']))-1
    stats=[col[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
    check(stats==[len(bs),len(u),min(u),max(u),u[0],u[max_uint]],f't29 differential at +{col.get("offset")} width {col["width"]}')
    return stats


def profile(raw,s,tr,cols,bounds=None,target=None):
    w,o=tr['width'],tr['legacy_offset']; offsets=range(14+o,s['legacy_footer_start'],s['stride'])
    bs=[raw[p:p+w] for p in offsets]; unsigned=unsigned_match(bs,cols[o,w])
    if target is not None:
        ids,ords=target; pairs=[S.unpack('<ii',b) for b in bs]
        fully_null=(-1,-1); live=[v for v in pairs if v!=fully_null]
        def misses(test):
            bad=[dict(row=i,offset=p,value=list(v),hex=b.hex()) for i,(p,b,v) in enumerate(zip(offsets,bs,pairs)) if v!=fully_null and not test(v)]
            return len(bad),bad[:5]
        fail,bad=misses(ids.__contains__); ordmiss,ordbad=misses(lambda v:v[0] in ords and v[1] in ords)
        return dict(count=len(bs),distinct=len(set(pairs)),min=min(v[0] for v in pairs),max=max(v[0] for v in pairs),
                    both_null_count=pairs.count(fully_null),second_zero_count=sum(b==0 for _,b in pairs),
                    any_minus_one_count=sum(-1 in v for v in pairs),matching_lanes_count=sum(a==b for a,b in pairs),
                    live_count=len(live),matches=len(bs)-fail,violations=fail,first_violations=bad,
                    ordinal_hypothesis=dict(matches=len(live)-ordmiss,violations=ordmiss,first_violations=ordbad),
                    first_target_ordinals=[ids.get(v) for v in pairs[:3]],t29_unsigned_stats=unsigned,
                    t29_lane_stats=[unsigned_match([b[i:i+4] for b in bs],cols[o+i,4]) for i in (0,4)])
    xs=Counter(int.from_bytes(b,'little',signed=True) for b in bs)
    lo,hi=bounds; bad=[dict(row=i,offset=p,value=x,hex=b.hex()) for i,(p,b) in enumerate(zip(offsets,bs))
                       if not lo<=(x:=int.from_bytes(b,'little',signed=True))<=hi]
    return dict(count=len(bs),distinct=len(xs),min=min(xs),max=max(xs),zero_count=xs[0],minus_one_count=xs[-1],
                sentinel=None,matches=len(bs)-len(bad),violations=len(bad),first_violations=bad[:5],
                histogram=dict(sorted(xs.items())) if len(xs)<=100 else None,t29_unsigned_stats=unsigned)


def ledger(st,raw,s,ts,domains,info,cols):
    m=load(MASTER); parent,=[p for p in m['entities']['club.xml'][0]['fields'] if p['field']=='Cmti']; specs=parent['list_item_fields']
    occ=[r for f in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for r in load(f)['nested_fields'] if r['parent']=='Cmti']
    check(len(specs)==len(occ)==len({p['field'] for p in specs})==6 and [r['idx'] for r in occ]==list(range(213,219)),'scoped occurrences')
    fields=[]; sinks={t['object_offset']:t for t in ts}
    for spec,x in zip(specs,occ,strict=True):
        code=spec['field']; typ=spec['type']; g=st.getter(code)
        check((x['code'],x['name'],x['type'])==(code,spec['name'],typ),'frozen schema/t24 join')
        ss=[{k:sinks[o][k] for k in ('legacy_offset','wire_offset','width','object_offset','site')} for o in g['object_offsets']]
        matched=True; rule=None
        if typ=='database_record_unique_id':
            key=spec['database_table_type']; kind='record_key_i32_pair'
            dom={'target':key,'native_null':[-1,-1],'zero_second_lane':'copy lane 0 on reader; not null','key_basis':'target identity at record +0xc/+0x10, not ordinal +8'}
            ps=[profile(raw,s,tr,cols,target=domains[key]) for tr in ss]
            matched=not any(p['violations'] for p in ps)
            if code=='club':
                rule='If current Cclu matches key at object+0x20 (exact or resolver equality), return resolved +0x28; otherwise return resolved +0x20.'
        elif code=='icom':
            kind='contextual_enum'; dom={'getter_outputs':[0,1],'independent_wire_sink':False}; ps=[]; matched=False
            rule='One if current Cclu matches +0x28 (exact or resolver equality), else zero; setter may swap both club keys instead of writing a direction flag.'
        else:
            kind='i8' if code=='pyiv' else 'i32'
            if code=='pyiv':
                check('enum_ref' not in spec,'re-evaluate frozen enum domain')
                bounds=(-128,127); dom={'native_signed_bounds':list(bounds),'frozen_enum':None,'labels_or_exhaustive_domain':None}
            else:
                bounds=tuple(int(spec[k]) for k in ('min_value','max_value')); dom={'xml_bounds':list(bounds)}
            tr,=ss
            check(tr['width']==(1 if kind=='i8' else 4),'scalar width')
            ps=[profile(raw,s,tr,cols,bounds=bounds)]; matched=not ps[0]['violations']
        grade=('L3_contextual_row_coordinates' if len(ss)>1 else 'L3_named_row_coordinate') if matched else (
            'held_derived_no_independent_wire_sink' if code=='icom' else 'held_static_sink_profile_conflict')
        fields.append(dict(schema_scope=[*SCOPE,x['idx']],code=code,name=spec['name'],schema=spec,grade=grade,
                           row_offset=ss[0]['legacy_offset'] if matched and len(ss)==1 else None,
                           wire_offset=ss[0]['wire_offset'] if matched and len(ss)==1 else None,
                           interpretation=kind,domain=dom,getter=g,sinks=ss,profiles=ps,context_rule=rule))
    # Same frozen row, two matched viewing clubs: flips direction and the returned counterparty.
    a,b=S.unpack_from('<ii',raw,22),S.unpack_from('<ii',raw,30)
    diff=sum(S.unpack_from('<ii',raw,p+8)!=S.unpack_from('<ii',raw,p+16) for p in range(14,s['legacy_footer_start'],s['stride']))
    check(a!=b and a in domains['club'][0] and b in domains['club'][0],'row 0 context fixture')
    example={'row':0,'same_wire_hex':s['samples'][0]['wire_hex'],'different_endpoint_rows':diff,'views':[
        {'context_key':list(a),'icom':0,'club_key':list(b),'selected_legacy_offset':16},
        {'context_key':list(b),'icom':1,'club_key':list(a),'selected_legacy_offset':8}]}
    for f in fields:
        if f['code'] in ('icom','club'):
            f['context_counterexample']=example
    return {'scope':SCOPE,'table_type':43,'occurrences':6,'baseline_L3':0,'L3':sum(f['grade'].startswith('L3') for f in fields),
            'L4':0,'date_fields':0,'reference_domains':info,'fields':fields}


def build():
    st=Static(); support=st.scope_support(); a,raw,codec,db=archives()
    s=a['server']; closure,(tr,conditions),edges=walk(st,raw);s.update(closure)
    n=s['row_count']; stride=sum(t['width'] for t in tr)+1
    check(stride==46 and n*stride==s['row_bytes'],'stride from executed CFG, not t29 input')
    s.update(stride=stride,row_template={'id':0,'condition_edges':conditions,'wire_selector':'13+46*i','legacy_body':'14+46*i',
        'body_end_exclusive':'59+46*i','trace_digest_record':'LE <7I>(i,selector,body,end,identity0,identity1,identity2) + SHA-256 bytes of body'},
        footer_transfers=[{'site':site,'offset':s['wire_footer_start']+d,'width':w,'value':v}
                          for site,d,w,v in zip(FOOT,(0,4,5),(4,1,4),s['footer_values'],strict=True)])
    check(s['footer_values']==[0,1,535] and s['uid_max']==535,'frozen footer observations, not a general invariant')
    negatives={t['site']:reject(lambda:read_row(st,raw,13,0,cut=t['site'])) for t in tr}
    off=14+tr[-1]['legacy_offset']
    overwrite=reject(lambda:read_row(st,raw[:off]+S.pack('<I',10000001)+raw[off+4:],13,0))
    synthetic={}
    for t in tr:
        if 'zero_lane_branch' not in t:
            continue
        p=14+t['legacy_offset']+4; j=t['zero_lane_branch']; obj=t['object_offset']
        row,y,cs,keys=read_row(st,raw[:p]+bytes(4)+raw[p+4:],13,0,fixture=True)
        check(not dict(cs)[j] and row['body_end']==s['samples'][0]['body_end'] and y==tr and keys[obj][0]==keys[obj][1], 'zero lane alternate no cursor change')
        synthetic[j]={'row':0,'offset':p,'observed_lane1':S.unpack_from('<i',raw,p)[0],'injected_lane1':0,
                      'stored_pair':list(keys[obj]),'body_end':row['body_end'],'branch':'fallthrough'}
    s['negative_replays']={'short_transfers':[{'site':o,'first_counterexample':msg} for o,msg in negatives.items()],
        'overwrite_does_not_mask_raw_error':overwrite,
        'selector_out_of_observed_domain':reject(lambda:read_row(st,raw[:13]+b'\x01'+raw[14:],13,0)),
        'duplicate_lane_mismatch':reject(lambda:read_row(st,raw[:off+8]+bytes(4)+raw[off+12:],13,0)),
        'zero_key_lane_alternates':synthetic}
    cols,t29=compare_t29(raw,s)
    domains,info=targets(codec,db); fields=ledger(st,raw,s,tr,domains,info,cols)
    branches=[]
    for o,b in sorted(st.branches.items()):
        c=b['class']; alt=b['alternative_or_first_counterexample']
        if c=='IO-result': alt=negatives[b['evidence'][0]]
        if o==ID: alt=overwrite
        if o in synthetic: alt=synthetic[o]
        branches.append({**b,'scope':'reader' if o>=START else 'identity_tail','alternative_or_first_counterexample':alt,
                         'taken_count':edges[o,True],'fallthrough_count':edges[o,False]})
    branches.extend({**b,'scope':'loader_footer_factory_slice'} for b in st.loader.values())
    OUT.mkdir(parents=True,exist_ok=True)
    cursor={'status':'complete_observed_row_cursor','scope':SCOPE,'table_type':43,
        'provenance':{'editor':str(EXE),'editor_sha256':EXE_SHA,'snapshot_manifest':st.snap},
        'factory':st.factory,'rtti':st.rtti,'slots':st.slots,'scope_evidence':support,
        'reader':{'chain':st.chain,'extent_source':'PE exception directory RUNTIME_FUNCTION','extents':st.extents,
                  'condition_count':len(st.branches),'runtime_mode_forks':[],
                  'mode_proof':'No caller mode tested. R9 forwarded and overwritten in low byte before callback; outer stack mode byte not read in either extent. Body clears R8D before tail and tail reloads from identity. The editor viewing club is a getter context, not a layout mode.'},
        'archives':a,'t29':t29,'transfers':[{'site':SELECT,'legacy_offset':-1,'wire_offset':0,'width':1,'sink':'loader stack+0x43'},*tr],
        'loader_transfers':st.loader_transfers,'wire_alignment':f'13 + {n}*(1+33+12) + 9 = {len(raw)}',
        'legacy_alignment':f'14 + {n}*46 + 8 = {len(raw)}; legacy +45 borrows next selector/first footer byte',
        'branch_taxonomy':CLASSES,'branch_census':{c:sum(b['class']==c for b in branches) for c in CLASSES},
        'limits':['Selector 0 and footer vector count 0 specialize this archive, not unconditional native constraints.',
                  'Identity bulk has no immediate status test; do not claim native AL=false for a short bulk.',
                  'Callback and release targets are opaque. Lifecycle counts assume live retained stream and table this; not runtime measurements.',
                  'Footer last u32 at table+0x50 equals both max observed identity UID and header count here; no general semantics inferred.'],
        'branch_shards':shards('branches',branches,24),'instruction_shards':shards('instructions',[st.records[o] for o in sorted(st.records)],120)}
    write('cursor_cmti.json',cursor);write('fields_cmti.json',fields)
    print(f"t32 build PASS: {n} x {stride} B; {fields['L3']}/6 L3, {6-fields['L3']} held, L4=0")


def selftest():
    buf=b'abc';check(take(buf,1,2,'fixture')==b'bc','bounded transfer')
    check('short read @1 width 3' in reject(lambda:take(buf,1,3,'fixture')),'short transfer fixture')
    b=bytes.fromhex('0100000000000000'); k=(1,1)
    c={(0,8):dict(width=8,count=1,distinct=1,min_unsigned=1,max_unsigned=1,zero_count=0,sentinel_count=0),
       (0,4):dict(width=4,count=1,distinct=1,min_unsigned=1,max_unsigned=1,zero_count=0,sentinel_count=0),
       (4,4):dict(width=4,count=1,distinct=1,min_unsigned=0,max_unsigned=0,zero_count=1,sentinel_count=0)}
    # In the raw join a zero second lane is not a sentinel and is not silently normalized into a successful raw match.
    p=profile(bytes(14)+b,dict(stride=8,legacy_footer_start=22),dict(width=8,legacy_offset=0),c,target=({k:3},{0,1,2,3}))
    check(p['violations']==1 and p['first_violations'][0]['value']==[1,0] and p['ordinal_hypothesis']['violations']==0,'raw key versus ordinal distinction')
    print('t32 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test bounded transfers and raw key vs ordinal domains')
    try:
        selftest() if p.parse_args().selftest else build()
        return 0
    except CheckError as e:
        print(f't32 check failed: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't32 fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
