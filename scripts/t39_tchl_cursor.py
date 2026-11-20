#!/usr/bin/env python3
"""Build the offline Tchl/table 34 cursor and scoped evidence ledger."""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t39/out'
EXE = Path('<OLD_REPO>/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_34.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_34.rows.jsonl'
T33 = 'scratch/t33/out/profiles/table_server_34.profile.json'
T37 = 'scratch/t37/out/profiles/table_server_34.profile.json'
NEG = 'scratch/t13d/out/quick_audit.md'
PAY_SHA = 'a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812'
THUNK, START, END, FAIL, RET = 0x156efd0, 0x43a6890, 0x43a6a6f, 0x43a69f4, 0x43a6a6e
MODE, ID, BULK = 0x43a68a2, 0x43a6a2f, 0x43a6a17
SELECT, FOOT = 0xf2ba0e, (0xffa602, 0xf2baa2, 0xf2bac2)
VT = 0x1418be628
N, SIZE = 7115, 313082
CLASSES = ('wire_data','runtime-external','IO-result','context-lifecycle','dead')
# read/width/lea, member, width, writer's read-or-write virtual transfer
READS = [(0x43a68bb,0x18,4,0x43a87e3),(0x43a68db,0x20,4,0x43a8817),
         (0x43a68fb,0x48,2,0x43a8833),(0x43a691b,0x4a,2,0x43a8853),
         (0x43a693b,0x30,4,0x43a888b),(0x43a695b,0x38,4,0x43a88c3),
         (0x43a697b,0x4c,1,0x43a88e3),(0x43a6997,0x4d,1,0x43a8903),
         (0x43a69b3,0x28,4,0x43a893b),(0x43a69cf,0x4e,1,0x43a895b),
         (0x43a69eb,0x40,4,0x43a8993),(BULK,8,12,None)]
GET = {'tchc':(0x156f895,0x156f8a1),'styr':(0x156f87d,0x156f980),'edyr':(0x156f941,0x156fa8c),
       'mstn':(0x156f94d,0x156f959),'sstn':(0x156f91f,0x156f92b),'dbrt':(0x156f8d2,0x156f8de),
       'posi':(0x156f913,0x156fa27),'cquf':(0x156f8c6,0x156f9fc),'tcop':(0x156f889,0x156f9df)}
# Fixup call and writer's source member load / ordinal load / null arm.
REFS = {0x18:(25,0x43a70b6,0x43a87bb,0x43a87c4,0x43a87c9,0x156fa1d),
        0x20:(24,0x43a70e0,0x43a87ef,0x43a87f8,0x43a87fd,None),
        0x30:(23,0x43a70fc,0x43a8863,0x43a886c,0x43a8871,0x156f976),
        0x38:(23,0x43a710b,0x43a889b,0x43a88a4,0x43a88a9,0x156f976),
        0x28:(25,0x43a7128,0x43a8913,0x43a891c,0x43a8921,0x156fa1d),
        0x40:(24,0x43a7152,0x43a896b,0x43a8974,0x43a8979,0x156fafc)}

class CheckError(Exception):
    pass


def require(ok, why):
    if not ok:
        raise CheckError(why)


def digest(b):
    return sha256(b).hexdigest()


def load(p):
    return json.loads((ROOT/p).read_bytes())


def dump(name, data):
    enc = lambda x: json.dumps(x, ensure_ascii=False, separators=(',',':'))
    body = ',\n'.join(enc(k)+':'+ ('[\n'+',\n'.join(map(enc,v))+'\n]' if isinstance(v,list) else enc(v)) for k,v in data.items())
    text = '{\n'+body+'\n}\n'
    require(len(text.encode('utf-8'))<50000, f'shard too large: {name}')
    (OUT/name).write_text(text, encoding='utf-8', newline='\n')


def shards(key, records, size):
    names=[]
    for i in range(0,len(records),size):
        name=f'{key}.part{i//size+1:03d}.json'
        dump(name,{key:records[i:i+size]});names.append(name)
    return names


class Static:
    def __init__(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t14_rtti_census import parse_rtti
        from t21b_control_flow import ReaderCFG
        self.get_rtti=parse_rtti
        manifest={r['path']:r['sha256'] for r in load('evidence/MANIFEST.json')['files']}
        self.sources={p:digest((ROOT/p).read_bytes()) for p in (MASTER,PROV)}
        require(self.sources[MASTER].startswith('7d57477e') and all(v==manifest[p] for p,v in self.sources.items()),'frozen snapshots')
        self.pe=PE(EXE)
        require(digest(self.pe.raw)==EXE_SHA and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'),'editor provenance')
        self.pe.pe.parse_data_directories(directories=[3]); self.md=Cs(CS_ARCH_X86,CS_MODE_64); self.md.detail=True
        self.ops={};self.out={}
        self.rtti=parse_rtti(self.pe,VT); self.slots={i:self.slot(VT,i) for i in (2,3,19,20,21)}
        require(self.rtti['class']=='STARTING_TEAM_CUP_HISTORY' and self.slots=={2:0x156f850,3:0x156fd50,19:THUNK,20:0x156f1b0,21:0x156f2a0},'case34 RTTI/slots')
        base=0xf49d38;cell=base+34*4;rel,=S.unpack_from('<i',self.pe.raw,cell)
        require(base+rel==0xf4949c and self.rip(0xf48b45)==self.pe.f2va(base) and self.rip(0xf494b8)==VT and
                self.ins(0xf494bf).op_str=='qword ptr [rsi], rax' and self.direct(0xf49503)==0xf49ca9,'factory jump table and vptr assignment')
        self.factory=dict(cell=cell,base=base,rel32=rel,raw=self.pe.raw[cell:cell+4].hex(),dispatch=self.span(0xf48b30,0xf48b55),
                          case=self.span(0xf4949c,0xf49508),return_slice=self.span(0xf49ca9,0xf49cb3),selector_used=False)
        require(self.direct(THUNK)==START and self.ins(THUNK).mnemonic=='jmp','slot19 thunk')
        require(not any(e.struct.BeginAddress<=self.pe.f2r(THUNK)<e.struct.EndAddress for e in self.pe.pe.DIRECTORY_ENTRY_EXCEPTION),'leaf thunk should have no extent')
        cfg=ReaderCFG(self.pe,self.md,START)
        require(cfg.function_end_off==END and not cfg.external_edges,'reader extent contains identity tail')
        self.edges={self.pe.va2f(pc):[self.pe.va2f(y) for y in ys] for pc,ys in cfg.successors.items()}
        self.add(THUNK,*self.edges)
        self.blocks=self.partition()
        self.transfers={}; self.branches={}
        for site,obj,w,wr in READS:
            lea=0x43a6a04 if site==BULK else site-16; width=0x43a6a0b if site==BULK else site-9
            require(self.ins(site).op_str=='qword ptr [rax + 0x28]' and self.ins(lea).operands[1].mem.disp==obj and
                    self.ins(lea).op_str.startswith(f'{"rbx" if site==BULK else "rdx"}, [rsi + ') and
                    self.ins(width).op_str.startswith('r8d, ') and self.ins(width).operands[1].imm==w,f'native transfer setup {site:#x}')
            self.transfers[site]=dict(site=site,width=w,object_offset=obj,setup=[lea,width],writer_site=wr,kind='identity_bulk' if site==BULK else 'property')
            if wr:require(self.ins(wr).op_str=='qword ptr [rax + 0x28]' and self.ins(wr-9).operands[1].imm==w,'writer transfer width')
            if site!=BULK:
                p=site+3;j=p+4
                require(self.ins(p).op_str=='dword ptr [rbx + 0x10], 0' and self.ins(j).mnemonic==('je' if j==0x43a69f2 else 'jne') and
                        (j+self.ins(j).size if j==0x43a69f2 else self.direct(j))==FAIL,'member I/O failure route')
                self.branch(j,p,'IO-result','stream [rbx+0x10] immediately after read',[site,FAIL],None)
        self.branch(MODE,0x43a689d,'runtime-external','caller stack mode byte: loader R9B → R12B → [loader rsp+0x30], no body selector involved',
                    [0xf28c13,0xf4d839,0xf2b670,0xf2ba38,0xf2ba51],None)
        self.branch(ID,0x43a6a28,'wire_data','unsigned raw bulk lane0 < 10000001; otherwise replace with caller ordinal',
                    [BULK,0x43a6a25,0x43a6a31,0x43a6a36,0xf2ba3d],None)
        for o,p,src,ev,note in [
            (0x43a69fe,0x43a69fb,'stream wrapper pointee',[0x43a69f8,BULK],'row 0, mode=1: null would fault at 0x43a68af; mode=0 null skips bulk and reaches identity logic, not an observed valid record'),
            (0x43a6a3c,0x43a6a39,'caller table context',[0x43a6a20,0xf2ba33,0x43a6a47],'row 0: null table context suppresses callback, not a body-size change'),
            (0x43a6a50,0x43a6a4d,'saved stream pointer for release',[0x43a69f8,0x43a6a00],'row 0: a null stream would already have skipped bulk in identity-only mode'),
            (0x43a6a56,0x43a6a52,'retain/release ZF',[0x43a6a00,0x43a6a63,0xf2ba48],'row 0: last-reference destructor is opaque; no extra explicit transfer')]:
            self.branch(o,p,'context-lifecycle',src,ev,note)
        require(set(self.branches)=={o for o,es in self.edges.items() if len(es)==2},'all reachable conditionals classified')
        require({o for o in self.edges if self.ins(o).mnemonic=='call'}==set(self.transfers)|{0x43a6a47,0x43a6a63},'all reachable calls summarized')
        require(self.ins(MODE-5).op_str=='byte ptr [rsp + 0x70], 0' and self.ins(0xf2ba38).op_str=='byte ptr [rsp + 0x30], r12b' and
                self.ins(0xf2b670).op_str=='r12d, r9d' and self.ins(0xf28c13).op_str=='r9b, 1','caller mode dataflow')
        self.outer,self.outer_reads=self.loader()
        self.scope=self.scope_proof()
        self.getcfg=ReaderCFG(self.pe,self.md,self.slots[2]); self.enum=self.enum_proof()
        self.ref_proof=self.references()

    def slot(self,vt,i):
        return self.pe.va2f(S.unpack_from('<Q',self.pe.raw,self.pe.va2f(vt)+8*i)[0])

    def ins(self,o):
        if o not in self.ops:
            va=self.pe.f2va(o);require(va is not None and self.pe.va2f(va)==o,f'unmapped {o:#x}')
            self.ops[o]=next(self.md.disasm(self.pe.raw[o:o+15],va,1))
        return self.ops[o]

    def add(self,*sites):
        for o in sites:
            i=self.ins(o); self.out[o]=dict(file_offset=hex(o),VA=hex(i.address),bytes=i.bytes.hex(),instruction=f'{i.mnemonic} {i.op_str}'.rstrip())
        return list(sites)

    def span(self,o,z):
        sites=[]
        while o<z:
            sites+=self.add(o);o+=self.ins(o).size
        require(o==z,f'span does not end at {z:#x}');return sites

    def rip(self,o):
        i=self.ins(o)
        return i.address+i.size+i.operands[1].mem.disp

    def direct(self,o):
        return self.pe.va2f(self.ins(o).operands[0].imm)

    def partition(self):
        leaders={START}
        for o,es in self.edges.items():
            if self.ins(o).mnemonic.startswith('j'):leaders.update(es)
        blocks=[]
        for o in sorted(leaders):
            sites=[]
            while True:
                sites.append(o); es=self.edges[o]
                if len(es)!=1 or es[0] in leaders or self.ins(o).mnemonic.startswith('j'):
                    blocks.append(dict(sites=sites,successors=es));break
                o,=es
        require(sorted(x for b in blocks for x in b['sites'])==sorted(self.edges),'block partition')
        return blocks

    def branch(self,o,p,kind,src,evidence,alt,scope='slot19'):
        i=self.ins(o);require(i.mnemonic.startswith('j') and i.mnemonic!='jmp',f'branch {o:#x}')
        self.add(o,p,*evidence)
        b=dict(site=o,predicate=p,taken_to=self.direct(o),fallthrough_to=o+i.size,
               source=src,evidence=evidence,scope=scope,first_counterexample_or_constraint=alt,**{'class':kind})
        if scope=='slot19':self.branches[o]=b
        return b

    def loader(self):
        # Cursor-relevant outer slice only; no claims about all loader CFG branches.
        for a,z in ((0xf2b660,0xf2b6cd),(0xf2b9d6,0xf2b9ea),(0xf2b9f0,0xf2bad7),
                    (0xffa5d0,0xffa646),(0xffa72a,0xffa752),(0xffa775,0xffa800),(0xffa99e,0xffa9cc),
                    (0xf28bf9,0xf28c1b),(0xf4d82e,0xf4d841)):
            self.span(a,z)
        require(self.direct(0xf2ba7f)==0xffa5d0 and self.direct(0xf2ba23)==0xf48b30 and self.direct(0xf28c16)==self.direct(0xf4d83c)==0xf2b660,'outer calls')
        def b(o,p,c,src,ev,note):return self.branch(o,p,c,src,ev,note,'loader_footer_factory_slice')
        end=313073
        bs=[b(o,p,'IO-result','stream status at +0x10',[call],note) for o,p,call,note in [
            (0xf2b698,0xf2b694,0xf2b691,'short count @8 width 4'),(0xf2b6b8,0xf2b6b4,0xf2b6b1,'short header byte @12 width 1'),
            (0xf2ba15,0xf2ba11,SELECT,'row 0: short selector @13 width 1'),
            (0xf2baa9,0xf2baa5,FOOT[1],f'after row 7114: short flag @{end+4} width 1'),
            (0xf2bac9,0xf2bac5,FOOT[2],f'after row 7114: short final lane @{end+5} width 4'),
            *[(j,p,s,f'footer count 0; synthetic count 1 requires a complete triplet (lane {lane} I/O check)')
               for j,p,s,lane in [(0xffa7af,0xffa7ab,0xffa7a8,0),(0xffa7ce,0xffa7ca,0xffa7c7,1),(0xffa7ed,0xffa7e9,0xffa7e6,2),(0xffa7fa,0xffa7f6,0xffa7e6,2)]]]]
        bs += [b(o,p,c,src,ev,note) for o,p,c,src,ev,note in [
            (0xf2ba89,0xf2ba84,'IO-result','footer vector helper return',[0xf2ba7f,0xffa9a3,0xffa9b6],f'footer: short vector count @{end}; replay rejects, native helper status on nonzero paths'),
            (0xf2ba59,0xf2ba57,'IO-result','slot19 AL',[0xf2ba51,FAIL],'row 0: short first member returns AL=false'),
            (0xf2ba2b,0xf2ba28,'context-lifecycle','factory result (case 34 not selector-dependent)',[SELECT,0xf2ba1b,0xf2ba20,0xf2ba23,0xf494bf],'row 0: null result would skip slot19 and not consume body'),
            (0xf2b9db,0xf2b9d6,'wire_data','header count',[0xf2b691],'empty stub count=0 is not selected member'),
            (0xf2b9fa,0xf2b9f7,'wire_data','next ordinal vs count',[0xf2b691,0xf2b9f0,0xf2b9f3],'next=1<7115 after row 0; next=7115 after row 7114'),
            (0xf2ba6c,0xf2ba68,'context-lifecycle','vector begin/end',[0xf2ba60,0xf2ba6e,0xf2ba72],'both edges call same footer helper with same R8'),
            (0xffa610,0xffa609,'wire_data','footer vector count vs process maximum',[FOOT[0],0xffa605,0xffa9a3],'footer count=0; over-limit count would return error'),
            (0xffa640,0xffa638,'context-lifecycle','vector capacity vs wire count',[0xffa61b,0xffa61f,0xffa646],'footer count=0; valid capacity cannot be below zero'),
            (0xffa733,0xffa731,'wire_data','zero vector count bypasses triplets',[FOOT[0],0xffa72a,0xffa7a8,0xffa7c7,0xffa7e6,0xffa9ab],'synthetic count 1 requires 12 extra bytes'),
            (0xffa77f,0xffa77c,'wire_data','triplet loop index vs count',[0xffa775,0xffa778],'no first triplet in observed archive'),
            (0xf48b3b,0xf48b38,'runtime-external','directory table type upper bound',[0xf2ba20,0xf48b45],'row 0: type 34 <= factory limit 73')]]
        ts=[]
        for o,w,wp,d,sink in [
            (0xf2b691,4,0xf2b688,0xf2b683,'loader stack+0x44 (count)'),(0xf2b6b1,1,0xf2b6a5,0xf2b69d,'table+0x5c'),
            (SELECT,1,0xf2ba02,0xf2b9e3,'loader stack+0x43 (selector)'),(FOOT[0],4,0xffa5fc,0xffa5f7,'vector count'),
            (0xffa7a8,4,0xffa79c,0xffa746,'vector lane0'),(0xffa7c7,4,0xffa7bb,0xffa739,'vector lane1'),
            (0xffa7e6,4,0xffa7da,0xffa73e,'vector lane2'),(FOOT[1],1,0xf2ba99,0xf2ba92,'table+0x58'),(FOOT[2],4,0xf2bab9,0xf2bab2,'table+0x50')]:
            require(self.ins(o).op_str=='qword ptr [rax + 0x28]' and self.ins(wp).operands[1].imm==w,'outer transfer width')
            ts.append(dict(site=o,width=w,setup=self.add(wp,d),sink=sink))
        return bs,ts

    def scope_proof(self):
        cv,nv,tv,ntv=0x14187cd08,0x1418893b8,0x14188e2d8,0x141889618
        rtti={key:self.get_rtti(self.pe,v) for key,v in zip(('CLUB','NATION','TEAM','NATIONAL_TEAM'),(cv,nv,tv,ntv))}
        require(all(k==d['class'] for k,d in rtti.items()),'owner RTTI')
        require([self.slot(v,i) for v,i in [(cv,2),(cv,3),(nv,2),(nv,3),(tv,2),(tv,3),(ntv,2),(ntv,3)]]==
                [0xe89a00,0xe82aa0,0x1041f30,0x1045300,0x11af7b0,0x11b4c30,0x1056a90,0x11b4c30],'owner vtable dispatch')
        links={0xe8c684:0xe8d584,0xe8d58f:0xe8f34a,0xe8f364:0x11f41d0,
               0xe83c50:0xe84d0e,0xe84d19:0xe85791,0xe857a3:0x11f6cf0,0x11f6dd2:0x11b4c30,
               0x1041f33:0x1041f40,0x1043322:0x1065ef0,0x1066987:0x10679fd,0x1067a08:0x1068559,0x1068576:0x11f41d0,
               0x1045300:0x3d61fc0,0x3d61fe9:0x1063530,0x1064780:0x106489c,0x10648b0:0x11f6cf0,
               0x1056a90:0x3d7d6c0,0x3d7d817:0x11af7b0,0x11af828:0x11b0f62,0x11b4ccd:0x11b5051,
               0x11b0f6c:0x15e9830,0x11b505f:0x15e9830,0x15e9830:0x44d7bf0,
               0xf4911f:0x1052b30,0x1052b30:0x3d7afc0,0xf49ca4:0x11a0160,0x11a0160:0x3e68540}
        require(all(self.direct(o)==z for o,z in links.items()),'club/nation shared parent routes')
        require(all(self.ins(o).operands[1].imm==0x5463686c for o in (0xe8c67e,0xe83c4a,0x1066981,0x11af822,0x11b4cc7)),'parent compares')
        require(self.rip(0x44d8364)==VT and self.rip(0x44d83ba)==self.rip(0x44d7c6a) and
                self.ins(0x44d8376).op_str=='qword ptr [rdi + 0x20], rax' and self.ins(0x44d7cc5).op_str=='rax, qword ptr [r14 + 0x20]' and
                self.ins(0x44d7cd1).op_str=='eax, dword ptr [rdi + 0xc]' and self.rip(0x3d7afdb)==ntv and self.rip(0x3e6858b)==tv,'shared collection / parent and selector11 class')
        case24_base=0xf49d38;case24_cell=case24_base+24*4
        require(case24_base+S.unpack_from('<i',self.pe.raw,case24_cell)[0]==0xf490f9 and self.ins(0xf49106).op_str=='bl, 0xb','team subtype selector')
        return dict(status='shared_editor_route; observed_live_owners_national_team_only', owner_rtti=rtti,
            offsets=self.add(*links,0x1041f30,0x1041f40,0x1045300,0x104588a,0x1064775,0x106477a,0xe8c67e,0xe83c4a,0x1066981,0x11af822,0x11b4cc7)+
                   sum((self.span(a,z) for a,z in [(0xe8d584,0xe8d594),(0xe84d0e,0xe84d1e),(0x10679fd,0x1067a0d),
                        (0x1043310,0x1043331),(0x1064775,0x1064785),(0x3e6858b,0x3e68595),
                        (0x11f4237,0x11f4255),(0x11f6db8,0x11f6dd7),(0x3d7d6da,0x3d7d72f),(0x3d7d80a,0x3d7d81c),
                        (0x11b0f62,0x11b0f7c),(0x11b5051,0x11b5064),(0x44d7c6a,0x44d7c8a),(0x44d7cbd,0x44d7cdd),
                        (0x44d8352,0x44d837a),(0x44d83ab,0x44d83d4),(0xf490f9,0xf49129),(0xf49c4a,0xf49ca9),
                        (0x3d7afdb,0x3d7afe5)]),[]),
            collection_global_VA=hex(self.rip(0x44d7c6a)),owner_member=0x20,case24_cell=case24_cell,
            case24_cell_bytes=self.pe.raw[case24_cell:case24_cell+4].hex(),
            caveat='Selector 11 dispatches NATIONAL_TEAM on the full-team factory arm; the process compatibility branch at f49100 is explicit, not a payload tag. Do not claim a runtime configuration was observed.')

    def references(self):
        require(self.direct(0x156f1b0)==0x43a7080 and self.direct(0x156f2a0)==0x43a8770,'slot20/21 thunks')
        self.add(0x156f1b0,0x156f2a0);self.span(0x43a7080,0x43a716e); self.span(0x43a8770,0x43a8a25)
        helper={'comp':(0xf7e280,0x3bf3190,0x3bf31df,0x3bf31f4,0x3bf322c),
                'team':(0xf7e440,0x3bf3460,0x3bf34b2,0x3bf34c7,0x3bf350e),
                'stage':(0xf7f440,0x3bf70c0,0x3bf7111,0x3bf7114,0x3bf719a)}
        for thunk,entry,load_,index,lookup in helper.values():
            require(self.direct(thunk)==entry,'fixup helper thunk'); self.add(thunk,entry,load_,index,lookup)
        self.span(0x3bf70c9,0x3bf7172);self.span(0x3bf7194,0x3bf71c0)
        self.span(0x3bf31df,0x3bf3237);self.span(0x3bf34b2,0x3bf3519)
        proof={}
        for obj,(tid,fix,source,ordinal,missing,tag) in REFS.items():
            kind={23:'stage',24:'team',25:'comp'}[tid];thunk,entry,load_,index,lookup=helper[kind]
            require(self.direct(fix)==thunk and self.ins(source).op_str==f'rax, qword ptr [r14 + {obj:#x}]' and
                    self.ins(ordinal).op_str=='eax, dword ptr [rax + 8]' and self.ins(missing).op_str=='eax, 0xffffffff','per-site ordinal writer/fixup')
            if tag:require(self.ins(tag).operands[1].imm=={23:0x7374676e,24:0x54746561,25:0x636f6d70}[tid],'getter target tag')
            proof[obj]=dict(target_table=tid,slot20_call=fix,helper=[thunk,entry,load_,index,lookup],writer_member=source,
                            writer_target_ordinal=ordinal,writer_null=missing,getter_tag=tag,encoding='i32_ordinal_or_minus_one')
        return proof

    def enum_proof(self):
        va=self.rip(0x156f8f3);o=self.pe.va2f(va);raw=self.pe.raw[o:o+48]
        arms=[self.pe.va2f(va+k) for k in S.unpack('<12i',raw)]
        boxed={}; sites=self.span(0x156f8de,0x156f903)+self.span(0x43a8dc6,0x43a8dd1)+self.span(0x43a8f0a,0x43a8f43)+self.add(0x156fb4a,0x156fbb7)
        for state,arm in enumerate(arms,1):
            if state in (*range(1,9),11):
                s=self.span(arm,arm+13 if state!=1 else arm+16);sites+=s
                i=self.ins(s[-2]);require(i.op_str==f'edi, [rcx + rcx*8 + {state if state!=11 else 9:#x}]'.replace('0x',''),'enum dispatcher arithmetic')
                boxed[state]=[state+9,state] if state!=11 else [18,9]
            elif state==12:
                require(self.ins(arm).op_str=='edi, 0x13','constant result 19');boxed[state]=[19,19]; sites+=self.add(arm)
            else:
                require(arm==0x156fbb7,'unsupported enum state defaults zero')
        setter=[]
        for site in (0x43a8f25,0x43a8f30):
            off=self.pe.va2f(self.rip(site));b=self.pe.raw[off:off+19];setter.append(dict(offset=off,VA=hex(self.rip(site)),bytes=b.hex()))
        for idx,(flag,state) in enumerate(zip(*(bytes.fromhex(x['bytes']) for x in setter)),1):
            require(boxed[state][flag]==idx,'Result setter table inversion')
        return dict(jump_table=dict(offset=o,VA=hex(va),bytes=raw.hex(),arms=arms),setter_tables=setter,
                    observed_flag_domain=[0,1],boxed_flag_zero_then_one=boxed,default_boxed=0,sites=sites)

    def getter(self,code):
        cmp_,arm=GET[code];pc=self.slots[2];path=[];c=None;x=int.from_bytes(code.encode('ascii'),'big')
        for _ in range(32):
            i=self.ins(pc);require(i.address in self.getcfg.instructions,'getter path unreachable');path+=self.add(pc)
            if pc==arm:break
            if i.mnemonic=='cmp':
                require(i.op_str.startswith('edx, '),'4CC compare not EDX');c=i.operands[1].imm
            nxt=pc+i.size
            if i.mnemonic.startswith('j') and {'jg':x>c,'jle':x<=c,'je':x==c,'jne':x!=c}[i.mnemonic]:nxt=self.direct(pc)
            pc=nxt
        require(pc==arm and cmp_ in path and self.ins(cmp_).operands[1].imm==x,'exact getter arm')
        i=self.ins(arm);mem=i.operands[1].mem
        require(i.reg_name(mem.base)=='rcx' and i.mnemonic==('movzx' if code in ('styr','edyr') else 'movsx' if code in ('posi','dbrt') else 'mov'),'getter member load')
        if code in ('styr','edyr'): require(i.operands[1].size==2,'year width')
        if code=='posi':require(self.ins(0x156fa2b).op_str=='edi, -1','position sentinel')
        if code=='dbrt':require(self.ins(0x156f8ef).op_str=='eax, byte ptr [rcx + 0x4c]','second Result lane')
        end={'tchc':0x156f8be,'cquf':0x156fa27,'tcop':0x156f9fc,'mstn':0x156f980,'sstn':0x156f941,
             'styr':0x156f994,'edyr':0x156faa0,'posi':0x156fa44,'dbrt':0x156f903}[code]
        evidence=self.span(arm,end)+self.span(0x156faf2,0x156fb09)+self.span(0x156fa09,0x156fa27)
        return dict(compare=cmp_,route=path,load=arm,object_offsets=[0x4c,0x4d] if code=='dbrt' else [mem.disp],evidence=evidence)


def pick_frame(zstd, archive, entry, offset, bound):
    """packed_size measures frame bytes from the frame's own magic, not from entry start."""
    hits=[]; matches=[];selected=None
    for start in range(offset,min(offset+64,bound-3)):
        if archive[start:start+4]!=b'\x28\xb5\x2f\xfd':continue
        end=min(start+entry['packed_size'],bound)
        dz=zstd.ZstdDecompressor().decompressobj()
        try: raw=dz.decompress(archive[start:end])
        except zstd.ZstdError: continue
        if not dz.eof:continue
        hits.append(dict(offset=start,relative_offset=start-offset,compressed_bytes=end-start-len(dz.unused_data),
                         payload_bytes=len(raw),count=S.unpack_from('<I',raw,8)[0] if len(raw)>=12 and raw[2:6]==b'tad.' else None,
                         sha256=digest(raw)))
        if len(raw)==entry['size']:matches.append(hits[-1]);selected=raw
    require(len(matches)==1,f"{entry['path']}: no unique complete frame matching directory size; observed {hits}")
    return selected,matches[0],hits


def read_archives():
    os.environ.setdefault('FM24_DB_DIR',str(ROOT/'scratch/data'))
    import fm24_dump as fm
    codec=fm._reader();sys.path.insert(0,'<OLD_REPO>/tools/python')
    import zstandard as zstd
    def open_db(archive):
        fn=archive+'_db.dat'; _,raw,d=codec['_entries'](fm.DB_DIR/fn,fn)
        base,toc=d['data_base'],d['toc_offset'];entries={e['path'].split('/')[-1]:e for e in d['entries']}
        def fetch(name):
            e=entries[name];o=e['offset']
            bound=min((base+r['offset'] for r in entries.values() if r['offset']>o),default=toc)
            payload,frame,frames=pick_frame(zstd,raw,e,o,bound)
            return payload,dict(entry=e,archive_offset=o,archive_data_base=base,next_member_or_toc=bound,selected_frame=frame,frames=frames)
        return dict(directory_entry_count=len(entries),archive_sha256=digest(raw),present='table_34.dat' in entries),fetch,entries
    c,cf,ce=open_db('client');s,sf,se=open_db('server')
    require(len(ce)==31 and len(se)==77 and not c['present'] and s['present'],'client/server directory presence')
    raw,info=sf('table_34.dat');s.update(info)
    c.update(entry=None,row_count=None,stride=None,payload_sha256=None)
    first=info['frames'][0]; prior=se['non_player_bans.dat']; base=s['archive_data_base']
    require(len(info['frames'])==2 and first['relative_offset']==9 and first['count']==0 and first['payload_bytes']==12 and
            info['selected_frame']['relative_offset']==base==34 and info['selected_frame']['compressed_bytes']==info['entry']['packed_size'] and
            len(raw)==SIZE and digest(raw)==PAY_SHA,f'E66 stub/real frame experiment: {info}')
    require((base+prior['offset'],prior['packed_size'],prior['size'])==(first['offset'],first['compressed_bytes'],first['payload_bytes']) and
            first['offset']+prior['packed_size']==info['selected_frame']['offset'] and
            info['selected_frame']['offset']+info['entry']['packed_size']==info['next_member_or_toc'],'canonical member is preceded by empty non_player_bans frame')
    legacy=fm.load_payload(codec,'server',34)
    require(len(legacy)==12 and digest(legacy)==first['sha256'],'reproduce unmodified load_payload counterexample')
    s['first_magic_counterexample']=dict(entry=prior,canonical_offset=first['offset'],historical_load_payload_bytes=len(legacy),
       note='Legacy scan incorrectly starts from directory-relative offset; the empty frame belongs to the immediately preceding member.')
    return {'client':c,'server':s},raw,sf,cf


def take(buf,p,w,label):
    require(p+w<=len(buf),f'{label}: short read @{p} width {w}')
    return buf[p:p+w]


def rejects(fn):
    try:fn()
    except CheckError as e:return str(e)
    raise CheckError('accepted negative fixture')


def row(st,raw,p,i,mode,strict=True,cut=None):
    sel=take(raw,p,1,f'row {i} selector')[0];start=p;body=p+1;p=body;pc=THUNK
    ident=None;stored=None;io=None;ts=[];seq=[]
    for _ in range(len(st.edges)+1):
        if pc in st.transfers:
            t=st.transfers[pc];w=t['width']
            if p+w>len(raw) or cut==pc:
                io=f'row {i}: short transfer @{p} width {w} site {pc:#x}'
                require(pc!=BULK,io+'; no immediate native bulk status test')
            else:
                ts.append(dict(t,legacy_offset=p-body,wire_offset=p-start))
                if pc==BULK:ident=S.unpack_from('<III',raw,p)
                p+=w
        if pc in st.branches:
            b=st.branches[pc]
            if pc==MODE: taken=mode==0
            elif pc==ID:
                require(ident is not None,'live stream required')
                taken=ident[0]<10000001;stored=ident[0] if taken else i
            elif b['class']=='IO-result':taken=(io is None)==(pc==0x43a69f2)
            else:taken=pc==0x43a6a56 # live stream / table context / retained owner
            seq.append((pc,taken));pc=b['taken_to' if taken else 'fallthrough_to']
        elif pc==THUNK:pc=START
        elif pc==FAIL:raise CheckError(f'{io}; IO-result -> {FAIL:#x} (AL=false)')
        elif pc==RET:
            a,b,c=ident
            if strict:require(a==stored==i and b==c and b!=0,f'row {i}: raw identity @{p-12} {ident}, stored ordinal={stored}')
            return dict(ordinal=i,selector=sel,selector_start=start,body_start=body,end=p,identity=list(ident),stored=stored),ts,seq
        else:pc,=st.edges[pc]
    raise CheckError('reader did not terminate')


def footer(buf,p):
    vec = int.from_bytes(take(buf,p,4,'footer vector count'),'little')
    require(not vec,f'footer vector count {vec} @{p}, nonzero path needs 12 B per element')
    flag=take(buf,p+4,1,'footer flag')[0];last=int.from_bytes(take(buf,p+5,4,'footer last lane'),'little')
    require(p+9==len(buf) and flag==1,f'footer @{p}: flag={flag}, end={p+9} not valid for {len(buf)} B')
    return [vec,flag,last]


def replay(st,raw):
    require(raw[:8]==bytes.fromhex('03017461642ef10d') and take(raw,8,5,'header')[4]==0,'header/version/flag')
    n=S.unpack_from('<I',raw,8)[0];require(n==N,'real header count')
    modes={}; accepted=[]
    for mode in (1,0):
        p=13; paths=Counter();sels=Counter(); sig=sha256(); first=None; violations=0; seen=set(); samples=[]; shape=None
        for i in range(n):
            r,ts,seq=row(st,raw,p,i,mode,False);sels[r['selector']]+=1;paths.update(seq)
            shape=ts if shape is None else shape;require(shape==ts,'transfer template varies unexpectedly')
            a,b,c=r['identity']; e=r['end']; bad=not(a==r['stored']==i and b==c and b!=0 and b not in seen)
            if bad:violations+=1;first=r if first is None else first
            seen.add(b);bodyhash=sha256(raw[p+1:e]).digest();sig.update(S.pack('<7I',i,p,p+1,e,a,b,c)+bodyhash)
            if i in (0,1,n//2,n-1): samples.append(dict(r,body_sha256=bodyhash.hex(),wire_hex=raw[p:e].hex()))
            if mode==1:accepted.append(r)
            p=e
        footer_status=footer(raw,p) if mode else rejects(lambda:footer(raw,p))
        stride=1+sum(t['width'] for t in shape)
        item=dict(tested_rows=n,row_bytes=p-13,stride=stride,proposed_footer_offset=p,footer_result=footer_status,
                  valid=bool(mode),first_identity_failure=first,rows_failing_identity_or_uniqueness=violations,
                  selector_histogram=dict(sorted(sels.items())),trace_sha256=sig.hexdigest(),samples=samples,
                  taken_counts={str(o):[paths[o,True],paths[o,False]] for o in st.branches},
                  transfer_sites=[t['site'] for t in shape])
        if mode:
            require(violations==0 and stride==44 and p-13==n*stride and sels=={0:n} and footer_status[2]==max(seen),'mode1 closure/identity/selector/footer')
            s=item;tr=shape
        else:require(first is not None and violations and stride==13 and p-13==n*stride and p!=s['proposed_footer_offset'],'mode0 must fail original member')
        modes[str(mode)]=item
    end=s['proposed_footer_offset'];pos=14+tr[-1]['legacy_offset']; patched=lambda where,octets:raw[:where]+octets+raw[where+len(octets):]
    changed,_,_=row(st,patched(13,b'\x01'),13,0,1)
    require(changed['selector']==1 and changed['end']==accepted[0]['end'],'factory case34 ignores selector')
    neg=dict(short_members=[dict(site=t['site'],message=rejects(lambda:row(st,raw,13,0,1,cut=t['site']))) for t in tr],
             mode0_strict_first=rejects(lambda:row(st,raw,13,0,0)),
             identity_overwrite=rejects(lambda:row(st,patched(pos,S.pack('<I',10000001)),13,0,1)),
             unequal_identity_lanes=rejects(lambda:row(st,patched(pos+8,bytes(4)),13,0,1)),
             unobserved_selector=dict(synthetic=changed,note='case34 accepts width; selector 1 outside observed domain, not factory rejection'),
             nonzero_footer=rejects(lambda:footer(patched(end,b'\x01'),end)),short_footer=rejects(lambda:footer(raw[:-1],end)))
    return dict(row_count=n,stride=44,payload_bytes=len(raw),payload_sha256=digest(raw),version=0xdf1,wire_origin=13,legacy_origin=14,
                header_hex=raw[:13].hex(),wire_footer_offset=end,legacy_footer_offset=end+1,wire_footer_hex=raw[end:].hex(),
                legacy_footer_hex=raw[end+1:].hex(),footer_transfers=[dict(site=o,offset=end+k,width=w,value=v) for o,k,w,v in zip(FOOT,[0,4,5],[4,1,4],s['footer_result'])],
                wire_equation='13 + 7115*(1+31+12) + 9 = 313082',legacy_equation='14 + 7115*44 + 8 = 313082',
                legacy_last_byte='legacy +43 borrows the next selector or first footer byte',modes=modes,negative_replays=neg),tr,accepted


def profile(raw,rows,frame):
    files={};p=load(PROFILE);n=len(rows);end=rows[-1]['end']+1
    for tag,path in [('t29',PROFILE),('t33',T33),('t37',T37)]:
        f=ROOT/path
        if not f.is_file():files[tag]=dict(path=path,status='not_available_in_checkout');continue
        q=load(path);v=q['payload'];c=q['row_closure']
        require((v['packed_offset'],v['payload_size'],v['payload_sha256'])==(frame['offset'],len(raw),digest(raw)) and
                (c['count'],c['stride'],c['row_start'],c['row_end_exclusive'],c['rows_sha256'])==(n,44,14,end,digest(raw[14:end])),f'{tag} independent framing')
        files[tag]=dict(path=path,status='matched',sha256=digest(f.read_bytes()),entity_tag=q.get('entity_tag'),
                        entity_tag_use='historical candidate only; not ownership proof')
    bs=(ROOT/ROWS).read_bytes();lines=bs.splitlines();require(p['full_rows_sha256']==digest(bs) and len(lines)==n,'independent t29 dump digest/count')
    for r,line in zip(rows,lines,strict=True):
        at=r['body_start'];require(json.loads(line)==dict(row=r['ordinal'],offset=at,len=44,raw_hex=raw[at:at+44].hex()),f'legacy differential row {r["ordinal"]}')
    return {(x['offset'],x['width']):x for x in p['columns']},dict(profiles=files,rows=ROWS,rows_sha256=digest(bs),matched_full_rows=n,
                legacy_block_sha256=digest(raw[14:end]),t13d_negative=dict(path=NEG,sha256=digest((ROOT/NEG).read_bytes()),
                    preserved='candidate club/nation and first-magic fake-frame finding; prior range votes are not field evidence'))


def targets(server,client):
    td={};maps={};team_selectors={};locations={}
    for tid,w in ((23,14),(25,127)):
        name=f'table_{tid}.dat';c,cmeta=client(name);s,smeta=server(name);n=S.unpack_from('<I',c,8)[0]
        require(S.unpack_from('<I',s,8)[0]==n and len(c)==13+w*n+9,'fixed target count and framing')
        d={};last=13;h=sha256()
        for i in range(n):
            e=13+w*(i+1);k=c[e-12:e];j,u,v=S.unpack('<III',k)
            at=s.find(k,last)
            require(j==i and u==v and u!=0 and at>=last,'fixed target ordinal-to-identity in both archive views')
            last=at+12;d[j]=u;h.update(k)
        require(last==len(s)-9,'server target final identity')
        td[tid]=dict(target_table=tid,client_count=n,server_count=n,client_sha256=digest(c),server_sha256=digest(s),
                     identity_trace_sha256=h.hexdigest(),method='fixed client record tails, exact ordered identity-triple witnesses in server member')
        maps[tid]=d
    b,bmeta=server('table_24.dat');x,xmeta=server('table_extra_24.dat');n=S.unpack_from('<I',b,8)[0]
    require(len(x)==12+82*n and S.unpack_from('<I',x,8)[0]==n and all(S.unpack_from('<I',x,12+k*82)[0]==k for k in range(n)),
            'actual team sidecar ordinal set')
    # Only a target identity query, not a Team serializer. Use the full-team selectors and the ordered repeated-lane constraints,
    # first prove the extrema by greedy feasibility in both directions, then require a unique witness for every ordinal.
    hmax=S.unpack_from('<I',b,len(b)-4)[0];cand=defaultdict(list)
    for m in re.finditer(rb'(?=(.{4})\1)', b[17:-9],re.S):
        at=m.start()+13;i,u=S.unpack_from('<II',b,at);end=at+12
        if i<n and 0<u<=hmax and (b[end] in (10,11) if i<n-1 else end==len(b)-9):cand[i].append((at,u))
    low=[];last=13
    for i in range(n):
        q=cand[i];k=bisect_left(q,(last+1,0));require(k<len(q),f'No forward target witness {i}')
        low.append(q[k]);last=q[k][0]+12
    high=[];next_=len(b)-9
    for i in range(n-1,-1,-1):
        q=cand[i];k=bisect_right(q,(next_-12,hmax))-1;require(k>=0,f'No reverse target witness {i}')
        high.append(q[k]);next_=q[k][0]-1
    require(low==high[::-1] and b[13] in (10,11),'ambiguous target team identity witness')
    last=13;h=sha256();d={}
    for i,(p,v) in enumerate(low):
        d[i]=v;team_selectors[i]=b[last];locations[i]=(last,p);h.update(S.pack('<4I',i,last,p,v));last=p+12
    require(last==len(b)-9 and len(set(d.values()))==n and Counter(team_selectors.values())=={10:84256,11:251},'target ordinal/identity/selector indices')
    td[24]=dict(target_table=24,server_count=n,server_sha256=digest(b),sidecar_sha256=digest(x),sidecar_ordinal_count=n,
                identity_trace_sha256=h.hexdigest(),selector_counts=dict(sorted(Counter(team_selectors.values()).items())),
                method='sidecar stores each ordinal; main payload has unique forward/backward-ordered repeated identity tails under full-team selectors 10/11; not a property decoder')
    maps[24]=d
    return td,maps,team_selectors,locations


def by_column(raw,rows,sink):
    o,w=sink['legacy_offset'],sink['width']
    return [raw[r['body_start']+o:r['body_start']+o+w] for r in rows]


def unsigned(bs,c):
    u=Counter(int.from_bytes(b,'little') for b in bs);w=c['width']; mask=(1<<8*w)-1
    numbers=[len(bs),len(u),min(u),max(u),u[0],u[mask]]
    require(numbers==[c[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')],
            f'independent unsigned profile mismatch +{c["offset"]} width {w}')
    return numbers


def ledger(st,raw,rows,tr,cols,td,maps,team_sels,team_sites):
    master=load(MASTER)['entities']
    scopes={k:[p for d in master[k] for p in d['fields'] if p['field']=='Tchl'] for k in ('club.xml','nation.xml')}
    require(all(len(v)==1 for v in scopes.values()) and scopes['club.xml'][0]==scopes['nation.xml'][0],'frozen club/nation scoped signature')
    spec=scopes['club.xml'][0]['list_item_fields']
    occ=[x for file in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for x in load(file)['nested_fields'] if x['parent']=='Tchl']
    require(len(spec)==len({s['field'] for s in spec})==9 and [x['idx'] for x in occ]==list(range(562,571)),'scoped occurrence uniqueness')
    members={t['object_offset']:t for t in tr}; records=[]
    def mkexample(i,x,sinks,bs):return dict(row=i,value=x,coordinates=[dict(offset=rows[i]['body_start']+s['legacy_offset'],hex=bb[i].hex()) for s,bb in zip(sinks,bs)])
    def field_profile(code,spec,sinks):
        bs=[by_column(raw,rows,t) for t in sinks]; stats=[unsigned(bb,cols[t['legacy_offset'],t['width']]) for bb,t in zip(bs,sinks)]
        def ex(i,x):return mkexample(i,x,sinks,bs)
        if code in ('tchc','mstn','sstn','cquf','tcop','_owner'):
            proof=st.ref_proof[sinks[0]['object_offset']];tid=proof['target_table'];dd=maps[tid];ids=set(dd.values());x=[S.unpack('<i',b)[0] for b in bs[0]]
            live=[(i,v) for i,v in enumerate(x) if v!=-1];miss=[(i,v) for i,v in live if v not in dd];uidmiss=[(i,v) for i,v in live if v not in ids]
            def joined(i,v):
                e=dict(ex(i,v),target_identity=dd[v]);
                if tid==24:e.update(target_selector=team_sels[v],target_selector_offset=team_sites[v][0],target_identity_offset=team_sites[v][1]);
                return e
            sample=next((joined(i,v) for i,v in live if v in dd),None)
            sels=Counter(team_sels[v] for _,v in live if v in dd) if tid==24 else None
            hist=Counter(x);z=next((joined(i,v) for i,v in live if v==0 and v in dd),None)
            return proof['encoding'],dict(target_table=tid,null=-1,proof=proof),dict(count=len(x),distinct=len(hist),min=min(x),max=max(x),null_count=hist[-1],
                first_null=next((ex(i,v) for i,v in enumerate(x) if v==-1),None),matches=len(live)-len(miss),violations=len(miss),first_violation=ex(*miss[0]) if miss else None,
                identity_lane_hypothesis=dict(matches=len(live)-len(uidmiss),misses=len(uidmiss),first_miss=ex(*uidmiss[0]) if uidmiss else None),
                target_selector_histogram=dict(sorted(sels.items())) if sels is not None else None,first_join=sample,first_zero_ordinal=z,t29_unsigned_stats=stats)
        if code=='dbrt':
            h=Counter((int.from_bytes(a,'little'),int.from_bytes(b,'little',signed=True)) for a,b in zip(*bs));xs=[(a[0],int.from_bytes(b,'little',signed=True)) for a,b in zip(*bs)]
            table=st.enum['boxed_flag_zero_then_one']; bad=[i for i,(f,s) in enumerate(xs) if f not in (0,1) or (s not in table and s!=-1)]
            box=lambda f,s:table[s][f] if s in table and f in (0,1) else 0
            boxed=Counter(box(*x) for x in xs); same_state={}
            for i,(f,s) in enumerate(xs):same_state.setdefault((s,f),i)
            s=next(s for s in sorted(table) if (s,0) in same_state and (s,1) in same_state)
            pair=[dict(ex(same_state[s,f],(f,s)),boxed=box(f,s)) for f in (0,1)]
            return 'two-lane native enum (u8 flag, i8 state; not a single byte)',dict(enum_ref=spec.get('enum_ref'),default_enum=0,static_result_ids=list(range(20)),ui_labels=None),dict(
                count=len(xs),raw_pairs={f'{f},{s}':c for (f,s),c in sorted(h.items())},boxed_histogram=dict(sorted(boxed.items())),violations=len(bad),
                first_violation=ex(bad[0],xs[bad[0]]) if bad else None,first_single_lane_counterexample=pair,t29_unsigned_stats=stats)
        year=code!='posi'; fmt='<H' if year else '<b';xs=[S.unpack(fmt,b)[0] for b in bs[0]];h=Counter(xs)
        lo,hi=(int(spec[k]) for k in ('min_value','max_value'));bad=[i for i,x in enumerate(xs) if not (lo<=x<=hi or (not year and x==-1))]
        return ('u16_year_integer' if year else 'i8_integer_minus_one_null'),dict(xml_bounds=[lo,hi],native_sentinel=None if year else -1),dict(
            count=len(xs),distinct=len(h),min=min(h),max=max(h),min_nonzero=min(x for x in h if x),zero_count=h[0],minus_one_count=h[-1],violations=len(bad),
            first_violation=ex(bad[0],xs[bad[0]]) if bad else None,histogram=dict(sorted(h.items())),
            first_sentinel=next((ex(i,x) for i,x in enumerate(xs) if not year and x==-1),None),t29_unsigned_stats=stats)
    owner=members[0x20];k,d,p=field_profile('_owner',{},[owner]);require(p['violations']==0 and p['target_selector_histogram']=={11:7084},'national-team-only live owner refs')
    parent=dict(sink=owner,interpretation=k,domain=d,profile=p,grade='L3_unscoped_owner_ordinal',
                club_exclusive_counterexample=p['first_join'])
    for s,x in zip(spec,occ,strict=True):
        code=s['field'];require((x['code'],x['name'],x['type'],x['optional'])==(code,s['name'],s['type'],s.get('is_optional')=='true'),'t24 scoped join')
        g=st.getter(code);sinks=[members[o] for o in g['object_offsets']];kind,domain,p=field_profile(code,s,sinks)
        ok=not p['violations'];grade='L3_table34_named_coordinate' if ok else 'held_domain_conflict'
        if len(sinks)>1 and ok:grade='L3_table34_named_compound_coordinate'
        records.append(dict(code=code,schema=s,scoped_occurrences=[['club.xml','Tchl',x['idx']],['nation.xml','Tchl']],getter=g,
                            sinks=sinks,row_offset=sinks[0]['legacy_offset'] if ok and len(sinks)==1 else None,
                            wire_offset=sinks[0]['wire_offset'] if ok and len(sinks)==1 else None,grade=grade,
                            club_grade='held_not_club_exclusive',club_first_counterexample=parent['club_exclusive_counterexample'],
                            interpretation=kind,domain=domain,profile=p))
    return dict(table_type=34,scope=['shared_editor:CLUB/NATION -> TEAM/NATIONAL_TEAM','Tchl'],occurrences=9,fields=records,
                L3=sum(r['grade'].startswith('L3') for r in records),club_exclusive_L3=0,L4=0,unscoped_owner=parent,target_domains=td)


def build():
    st=Static();a,raw,sf,cf=read_archives();s,tr,rows=replay(st,raw);a['server'].update(s)
    cols,prior=profile(raw,rows,a['server']['selected_frame']);domains=targets(sf,cf)
    fields=ledger(st,raw,rows,tr,cols,*domains)
    bs=[]
    for o,b in sorted(st.branches.items()):
        note=b['first_counterexample_or_constraint']
        if b['class']=='IO-result':note=next(x['message'] for x in s['negative_replays']['short_members'] if x['site']==b['evidence'][0])
        if o==MODE:note=s['negative_replays']['mode0_strict_first']
        if o==ID:note=s['negative_replays']['identity_overwrite']
        bs.append(dict(b,first_counterexample_or_constraint=note,edges_by_mode={k:v['taken_counts'][str(o)] for k,v in s['modes'].items()}))
    bs+=st.outer
    OUT.mkdir(parents=True,exist_ok=True)
    cur=dict(status='complete_mode1_observed_cursor; partial_field_acceptance',table_type=34,scope='Tchl (shared editor path; server live rows nation-team-backed)',
        provenance=dict(editor=str(EXE),editor_sha256=EXE_SHA,frozen_snapshots=st.sources),archives=a,factory=st.factory,rtti=st.rtti,slots=st.slots,
        reader=dict(chain=[THUNK,START,0x43a69f8,BULK,RET],entry=START,entry_VA=hex(st.pe.f2va(START)),end_exclusive=END,end_VA=hex(st.pe.f2va(END)),
                    extent_source='PE RUNTIME_FUNCTION; identity tail is inline, not a second extent',external_edges=[],reachable=len(st.edges),
                    blocks=st.blocks,caller_mode_site=MODE,forks=[1,0],condition_count=len(st.branches)),
        transfers=[dict(site=SELECT,width=1,legacy_offset=-1,wire_offset=0,kind='selector'),*tr],outer_transfers=st.outer_reads,
        scope_evidence=st.scope,enum_evidence=st.enum,profiles=prior,branch_classes=list(CLASSES),
        branch_counts={c:sum(b['class']==c for b in bs) for c in CLASSES},branch_shards=shards('branches',bs,25),
        instruction_shards=shards('instructions',[st.out[o] for o in sorted(st.out)],145))
    dump('cursor_tchl.json',cur);dump('fields_tchl.json',fields)
    print(f't39 build PASS: {N} x 44 bytes; table 34 {fields["L3"]}/9 L3; club-exclusive 0; L4=0')


def selftest():
    sys.path.insert(0,'<OLD_REPO>/tools/python')
    import zstandard as zs
    a=b'03017461642e';b=bytes(80);c=zs.ZstdCompressor();x=c.compress(a);y=c.compress(b);p=b'P'+x+y
    payload,hit,hits=pick_frame(zs,p,dict(path='fixture',size=len(b),packed_size=max(len(x),len(y))),0,len(p))
    require(payload==b and hit['relative_offset']==1+len(x) and len(hits)==2,'multi-frame preference')
    require(footer(S.pack('<IBI',0,1,33),0)==[0,1,33] and 'short' in rejects(lambda:take(b'',0,1,'fixture')),'footer/short transfer')
    print('t39 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true',help='test bounded frame selection and replay primitives')
    try:
        selftest() if p.parse_args().selftest else build();return 0
    except CheckError as e:
        print(f't39 check failed: {e}',file=sys.stderr);return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't39 fatal {type(e).__name__}: {e}',file=sys.stderr);return 2


if __name__=='__main__':
    sys.path.insert(0,str(ROOT/'scripts'))
    raise SystemExit(main())
