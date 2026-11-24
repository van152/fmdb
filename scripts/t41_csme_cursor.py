#!/usr/bin/env python3
"""Build the offline Csme / table 59 variable cursor and field ledger."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

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
OUT = ROOT/'scratch/t41/out'
EXE = Path(str(_cfg.EDITOR_EXE))
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t33/out/profiles/table_server_59.profile.json'
ROWS = 'scratch/t33/out/profiles/table_server_59.rows.jsonl'
OLD = 'scratch/t33/out/REPORT.md'
OCC = 'scratch/t24/out/subtables.part001.json'
PAY_SHA = '7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7'
START, END, FAIL, RET = 0x15831a0, 0x1583580, 0x1583213, 0x1583227
VT, N, SIZE = 0x141882fa8, 9079, 224880
MAGIC = bytes.fromhex('28b52ffd')
CLASSES = ('wire_data', 'runtime-external', 'IO-result', 'context-lifecycle', 'dead')
# transfer -> (key, width, RDX setup, R8D setup, object or stack sink)
READS = {
    0x15831c9: ('owner',4,0x15831b9,0x15831c0,'outer+0x30'),
    0x15831e5: ('outer_byte',1,0x15831d5,0x15831dc,'outer+0x38'),
    0x158320a: ('count',4,0x15831fc,0x1583201,'rsp+0x40'),
    0x15832aa: ('tag',1,0x15832a5,0x158329c,'rsp+0x47'),
    0x15832d2: ('pair',8,0x15832cf,0x15832c6,'entry+0x0/+0x4'),
    0x1583317: ('finish',1,0x1583304,0x158330e,'entry+0x8'),
    0x158351f: ('identity',12,0x158351c,0x1583513,'outer+0x8/+0xc/+0x10'),
}
FOOT = (0xffa602,0xf2baa2,0xf2bac2)
SELECT = 0xf2ba0e
MODES = (1, 0)

class Check(Exception): pass

def req(ok, message):
    if not ok: raise Check(message)

def sha(b): return sha256(b).hexdigest()
def js(name): return json.loads((ROOT/name).read_bytes())
def u32(b, p=0): return S.unpack_from('<I', b, p)[0]
def hist(xs): return {str(k):v for k,v in sorted(Counter(xs).items())}

def emit(name, obj):
    enc = lambda x: json.dumps(x,ensure_ascii=False,separators=(',',':'))
    lines = [enc(k)+':'+ ('[\n'+',\n'.join(map(enc,v))+'\n]' if isinstance(v,list) else enc(v)) for k,v in obj.items()]
    msg = '{\n'+',\n'.join(lines)+'\n}\n'
    req(len(msg.encode('utf8'))<50000, f'{name} exceeds shard budget')
    (OUT/name).write_text(msg,encoding='utf8',newline='\n')

def shards(key, rows, size):
    names=[]
    for at in range(0,len(rows),size):
        n=f'{key}.part{at//size+1:03d}.json';emit(n,{key:rows[at:at+size]});names.append(n)
    return names

def negative(fn):
    try: fn()
    except Check as e: return str(e)
    raise Check('negative fixture was accepted')

class Static:
    def __init__(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t14_rtti_census import parse_rtti
        from t21b_control_flow import ReaderCFG
        frozen={x['path']:x['sha256'] for x in js('evidence/MANIFEST.json')['files']}
        self.hashes={p:sha((ROOT/p).read_bytes()) for p in (MASTER,PROV)}
        req(self.hashes[MASTER].startswith('7d57477e') and all(frozen[p]==h for p,h in self.hashes.items()),'frozen snapshot SHA')
        self.pe=PE(EXE);self.pe.pe.parse_data_directories(directories=[3]);self.md=Cs(CS_ARCH_X86,CS_MODE_64);self.md.detail=True
        req(sha(self.pe.raw)==EXE_SHA and EXE_SHA in (ROOT/PROV).read_text(encoding='utf8'),'editor provenance SHA')
        self.rtti=parse_rtti;self.get={};self.saved={}
        self.vt=parse_rtti(self.pe,VT);self.slots={j:self.slot(VT,j) for j in (2,3,19,20,21)}
        req(self.vt['class']=='STARTING_MEDIA_EXPECTATIONS' and self.slots=={2:0xfe3520,3:0xfe1d00,19:START,20:0x1583580,21:0x15835c0},'RTTI/slot19')
        base=self.pe.va2f(self.rip(0xf48b45));cell=base+4*59;rel,=S.unpack_from('<i',self.pe.raw,cell)
        req(base==0xf49d38 and base+rel==0xf49950 and self.rip(0xf4996c)==VT and self.i(0xf49973).op_str=='qword ptr [rsi], rax' and self.dest(0xf499b0)==0xf49ca9,'factory dispatch and constructor')
        self.factory=dict(base=base,cell=cell,rel32=rel,bytes=self.pe.raw[cell:cell+4].hex(),handler=0xf49950,selector_used=False,
                          instructions=self.span(0xf48b30,0xf48b55)+self.span(0xf49950,0xf499b5)+self.span(0xf49ca9,0xf49cb3))
        cfg=ReaderCFG(self.pe,self.md,START)
        req(cfg.function_end_off==END and not cfg.external_edges and len(cfg.instructions)==260 and self.i(START).mnemonic=='push','slot19 is a real, single RUNTIME_FUNCTION')
        self.edges={self.pe.va2f(k):[self.pe.va2f(v) for v in vs] for k,vs in cfg.successors.items()}
        self.add(*self.edges)
        self.blocks=self.partition()
        self.transfers=[]
        for site,(key,w,lea,wd,sink) in READS.items():
            req(self.i(site).op_str=='qword ptr [rax + 0x28]' and self.i(wd).op_str.startswith('r8d, ') and self.i(wd).operands[1].imm==w,'transfer width/site')
            expect={0x15831b9:'rdx, [rcx + 0x30]',0x15831d5:'rdx, [r13 + 0x38]',0x15831fc:'rdx, [rsp + 0x40]',0x15832a5:'rdx, [rsp + 0x47]',
                    0x15832cf:'rdx, r14',0x1583304:'rdx, 8',0x158351c:'rdx, rbx'}
            req(self.i(lea).op_str==expect[lea],'RDX setup')
            offsets={'owner':0,'outer_byte':4,'count':5,'tag':9,'pair':10,'finish':18,'identity':9}
            stride={'tag':10,'pair':10,'finish':10,'identity':10}
            self.transfers.append(dict(site=site,width=w,key=key,sink=sink,rdx_setup=lea,r8d_setup=wd,legacy_base=offsets[key],wire_base=offsets[key]+1,
                                       multiplier=stride.get(key,0),index='n' if key=='identity' else 'j' if key in ('tag','pair','finish') else None))
        self.branches=self.reader_branches()
        req(set(self.branches)=={o for o,v in self.edges.items() if len(v)==2},'complete reader conditional census')
        self.opaque={0x1583283:'entry allocation',0x15832f7:'entry stream last-reference release',0x1583394:'vector allocation',
                     0x15833b1:'vector copy',0x15833cf:'vector suffix copy',0x1583434:'old vector pool release',0x1583454:'old vector generic release',
                     0x158348d:'pool lifecycle callback',0x158349b:'TLS init guard enter',0x15834de:'TLS pool init',0x15834ea:'register pool cleanup',
                     0x15834f6:'TLS init guard leave',0x1583555:'table registration callback (RDX object, R8 ordinal; no stream argument)',
                     0x1583579:'tail stream last-reference release'}
        req({o for o in self.edges if self.i(o).mnemonic=='call'}==set(READS)|set(self.opaque),'complete reader call census')
        high_stack={op.mem.disp for o in self.edges for op in self.i(o).operands if op.type==3 and self.i(o).reg_name(op.mem.base)=='rsp' and op.mem.disp>=0xa0}
        req(high_stack=={0xc8,0xd8} and self.i(0xf2ba38).op_str=='byte ptr [rsp + 0x30], r12b' and self.i(0xf2b670).op_str=='r12d, r9d','ABI: forwarded mode at callee +0xd0 is unused')
        tag_access=[o for o in self.edges for op in self.i(o).operands if op.type==3 and self.i(o).reg_name(op.mem.base)=='rsp' and op.mem.disp==0x47]
        req(tag_access==[0x15832a5],'entry tag is transferred into scratch, never tested or loaded by slot19')
        self.outer=self.loader()
        self.scope=self.routes()

    def i(self,o):
        if o not in self.get:
            va=self.pe.f2va(o);req(va is not None and self.pe.va2f(va)==o,f'instruction address {o:#x}')
            self.get[o]=next(self.md.disasm(self.pe.raw[o:o+15],va,1))
        return self.get[o]

    def add(self,*sites):
        for o in sites:
            i=self.i(o);self.saved[o]=dict(file_offset=hex(o),VA=hex(i.address),bytes=i.bytes.hex(),instruction=(i.mnemonic+' '+i.op_str).rstrip())
        return list(sites)

    def span(self,a,z):
        os=[]
        while a<z:os.extend(self.add(a));a+=self.i(a).size
        req(a==z,f'instruction-aligned span end {z:#x}')
        return os

    def dest(self,o):return self.pe.va2f(self.i(o).operands[0].imm)
    def rip(self,o):
        i=self.i(o);m,=[x.mem for x in i.operands if x.type==3 and i.reg_name(x.mem.base)=='rip'];return i.address+i.size+m.disp
    def slot(self,v,j):return self.pe.va2f(S.unpack_from('<Q',self.pe.raw,self.pe.va2f(v)+8*j)[0])

    def partition(self):
        leaders={START}
        for o,es in self.edges.items():
            if self.i(o).mnemonic.startswith('j'):leaders.update(es)
        bs=[]
        for o in sorted(leaders):
            xs=[]
            while True:
                xs.append(o);es=self.edges[o]
                if len(es)!=1 or es[0] in leaders or self.i(o).mnemonic.startswith('j'):
                    bs.append(dict(sites=xs,successors=es));break
                o,=es
        req(sorted(o for b in bs for o in b['sites'])==sorted(self.edges),'block partition');return bs

    def br(self,o,p,k,why,ev,ex,scope='slot19',length=False):
        i=self.i(o);req(i.mnemonic.startswith('j') and i.mnemonic!='jmp','branch opcode')
        self.add(o,p,*ev)
        return dict(site=o,predicate=p,**{'class':k},taken_to=self.dest(o),fallthrough_to=o+i.size,evidence=list(ev),scope=scope,
                    changes_normal_row_length=length,source=why,first_counterexample_or_constraint=ex)

    def reader_branches(self):
        plain=[(0x15831d0,0x15831cc,0x15831c9),(0x15831ec,0x15831e8,0x15831e5),(0x1583211,0x158320d,0x158320a),
               (0x15832b1,0x15832ad,0x15832aa),(0x15832fb,0x15832f9,0x15832d2),(0x158331e,0x158331a,0x1583317),
               (0x158332b,0x1583327,0x1583317)]
        bs=[self.br(o,p,'IO-result','saved EBP = stream status after pair' if o==0x15832fb else 'stream status +0x10 (redundant re-read at 0x158332b, same live stream)',
                    [site,FAIL,0x15832e3] if o==0x15832fb else [site,FAIL],
                    'synthetic nonzero status first possible at row 2 after the entry scalar; returns AL=false, not a new layout' if o==0x158332b else 'short transfer fixture') for o,p,site in plain]
        for o,p,ev,src,ex,sz in [
            (0x158322d,0x1583228,[0x158320a,0x1583500],'u32 entry count at rsp+0x40, zero skips the loop','row 0 count=0 @19 → identity @23; row 2 count=1 @63 → one 10 B item, identity @77',True),
            (0x1583250,0x158324d,[0x1583246,0x1583249,0x158320a],'unsigned incremented element index >= u32 count','row 2: 1>=1 exits; synthetic row 2 count=2 executes back edge once',True),
            (0x15832da,0x15832d5,[0x15832d2,0x15832dc,0x15832df],'second signed lane tests raw zero; copy first lane if zero','row 2 pair (-1,-1) keeps lane1; synthetic (5,0) stores (5,5), same width',False),
            (0x158353a,0x1583533,[0x158351f,0x1583530,0x158353c,0x1583544,0xf2ba3d],'raw unsigned lane0 < 10000001, else caller ordinal','synthetic row 0 ordinal 10000001 is overwritten but raw validation rejects',False)]:
            bs.append(self.br(o,p,'wire_data',src,ev,ex,length=sz))
        entries=[
            (0x1583275,0x158326f,[0x1583256,0x1583262,0x158349b,0x158327b],'TLS pool epoch vs thread guard','row 2 first nonempty; cold guard may initialize, both returning arms reach same tag read'),
            (0x15832bd,0x15832ba,[0x15832b7,0x15832d2,0x15832e3],'stream wrapper pointee','row 2 null would skip bulk then dereference [rbx+0x10], excluded in live context'),
            (0x15832ea,0x15832e6,[0x15832bf,0x15832f7],'entry stream reference decrement ZF','row 2 shared retained wrapper, destructor not invoked by modeled live projection'),
            (0x1583339,0x1583335,[0x1583331,0x158323e,0x1583394,0x1583467],'vector end vs capacity','row 2 first push grows a newly empty factory vector; both push arms increment the same loop index'),
            (0x15833b9,0x15833b6,[0x1583331,0x15833a4,0x15833b1,0x15833cf],'reloaded end vs saved end after copy','row 2 append at end; no suffix copy under no-alias memcpy semantics'),
            (0x15833e2,0x15833d8,[0x15833d4,0xf499a8,0x158345a],'old vector base','row 2 first grow has null old base; synthetic count 2 visits old-vector release on second grow'),
            (0x15833f6,0x15833f2,[0x15833e4,0x1583401],'allocator old span != -1','no old backing allocation in observed rows; first possible at row 2 with synthetic count 2'),
            (0x1583407,0x1583403,[0x15833eb,0x1583454],'allocator pool-active flag','no old backing allocation observed; synthetic inactive allocator uses generic free'),
            (0x158341b,0x1583418,[0x1583409,0x1583414,0x158341d],'allocator pool array bound','no old backing allocation observed; synthetic pool index outside bound uses generic free'),
            (0x1583424,0x1583421,[0x158341d,0x1583454],'pool slot pointer','no old backing allocation observed; synthetic null pool slot uses generic free'),
            (0x158343f,0x158343a,[0x1583434,0x1583441,0x158347d],'pool-release flag','no old backing allocation observed; synthetic flag clear bypasses decrement'),
            (0x1583481,0x158347f,[0x1583446,0x158347d,0x158345a],'pool release AL','no old backing allocation observed; synthetic still-live pool bypasses destroy check'),
            (0x1583488,0x1583483,[0x158348d,0x158345a],'pool final-release callback gate','no old backing allocation observed; synthetic flag clear suppresses callback'),
            (0x15834a7,0x15834a0,[0x158349b,0x15834de,0x158327b],'TLS pool uninitialized sentinel -1','row 2 cold guard could initialize if sentinel, otherwise both reach allocation'),
            (0x1583506,0x1583503,[0x1583500,0x158351f,0x1583524],'tail stream pointee','row 0 null skips 12 B identity, but the header already requires live stream'),
            (0x158354a,0x1583547,[0x1583528,0xf2ba33,0x1583555],'loader table context pointer','row 0 hypothetical null skips callback, not a width change'),
            (0x158355e,0x158355b,[0x1583500,0x1583506,0x1583564],'tail stream pointer before release','row 0 null not a valid property read context'),
            (0x1583568,0x1583564,[0x1583508,0x1583579],'tail stream reference decrement ZF','row 0 shared retained wrapper; final release is opaque, no extra explicit read')]
        bs.extend(self.br(o,p,'context-lifecycle',src,ev,ex) for o,p,ev,src,ex in entries)
        return {b['site']:b for b in bs}

    def loader(self):
        for a,z in ((0xf2b660,0xf2b6cd),(0xf2b9d6,0xf2b9ea),(0xf2b9f0,0xf2bad7),(0xffa5d0,0xffa646),
                    (0xffa72a,0xffa752),(0xffa775,0xffa800),(0xffa99e,0xffa9cc),(0xf28bf9,0xf28c1b),(0xf4d82e,0xf4d841)):
            self.span(a,z)
        req(self.dest(0xf2ba23)==0xf48b30 and self.dest(0xf2ba7f)==0xffa5d0 and self.i(0xf2ba51).op_str=='qword ptr [rbx + 0x98]' and
            self.i(0xf28c13).op_str=='r9b, 1' and self.dest(0xf28c16)==self.dest(0xf4d83c)==0xf2b660,'loader mode forwarding and slot19 call')
        tx=[]
        for site,w,setup,sink in [(0xf2b691,4,0xf2b688,'header count'),(0xf2b6b1,1,0xf2b6a5,'header flag'),(SELECT,1,0xf2ba02,'selector'),
                                  (FOOT[0],4,0xffa5fc,'footer count'),(0xffa7a8,4,0xffa79c,'vector lane0'),(0xffa7c7,4,0xffa7bb,'vector lane1'),
                                  (0xffa7e6,4,0xffa7da,'vector lane2'),(FOOT[1],1,0xf2ba99,'footer byte'),(FOOT[2],4,0xf2bab9,'footer u32')]:
            req(self.i(site).op_str=='qword ptr [rax + 0x28]' and self.i(setup).operands[1].imm==w,'loader transfer')
            tx.append(dict(site=site,width=w,width_setup=setup,sink=sink))
        bs=[]
        for o,p,ev,ex in [(0xf2b698,0xf2b694,0xf2b691,'short header count @8'),(0xf2b6b8,0xf2b6b4,0xf2b6b1,'short header flag @12'),
                          (0xf2ba15,0xf2ba11,SELECT,'short selector row 0 @13'),(0xf2baa9,0xf2baa5,FOOT[1],'short footer flag'),
                          (0xf2bac9,0xf2bac5,FOOT[2],'short final footer u32'),(0xffa7af,0xffa7ab,0xffa7a8,'synthetic count 1 requires triplet lane0'),
                          (0xffa7ce,0xffa7ca,0xffa7c7,'synthetic count 1 requires triplet lane1'),(0xffa7ed,0xffa7e9,0xffa7e6,'synthetic count 1 requires triplet lane2'),
                          (0xffa7fa,0xffa7f6,0xffa7e6,'reloaded status after triplet lane2')]:
            bs.append(self.br(o,p,'IO-result','stream status +0x10',[ev],ex,'loader_slice'))
        for o,p,k,ev,src,ex in [
            (0xf2ba59,0xf2ba57,'IO-result',[0xf2ba51,FAIL],'slot19 AL','row 0 short owner transfer returns false'),
            (0xf2ba89,0xf2ba84,'IO-result',[0xf2ba7f,0xffa9a3],'footer vector helper AL','short count rejected by replay; not an immediate native status branch'),
            (0xf2b9db,0xf2b9d6,'wire_data',[0xf2b691],'header count==0','adjacent table52 count=0 belongs to different member'),
            (0xf2b9fa,0xf2b9f7,'wire_data',[0xf2b691,0xf2b9f0],'next ordinal >= header count','row 0 next=1; after row 9078 next=9079 exits'),
            (0xf2ba2b,0xf2ba28,'context-lifecycle',[SELECT,0xf2ba23,0xf49973],'factory result','null skips body; case 59 has no selector-dependent construction'),
            (0xf2ba6c,0xf2ba68,'context-lifecycle',[0xf2ba60,0xf2ba6e,0xf2ba7f],'vector begin/end','both edges enter same footer helper'),
            (0xffa610,0xffa609,'wire_data',[FOOT[0],0xffa9a3],'wire count vs process bound','count 0 observed; count over maximum returns error'),
            (0xffa640,0xffa638,'context-lifecycle',[FOOT[0],0xffa61b],'capacity vs vector count','with count 0 nonnegative capacity suffices'),
            (0xffa733,0xffa731,'wire_data',[FOOT[0],0xffa7a8],'zero count skips triplets','synthetic count 1 needs 12 more bytes'),
            (0xffa77f,0xffa77c,'wire_data',[0xffa775,0xffa778],'triplet index vs count','no iteration observed in table59'),
            (0xf48b3b,0xf48b38,'runtime-external',[0xf2ba20,0xf48b45],'table type from context, not selector','type 59 <= 73')]:
            bs.append(self.br(o,p,k,src,ev,ex,'loader_slice'))
        return dict(branches=bs,transfers=tx)

    def routes(self):
        vs={'CLUB':0x14187cd08,'TEAM':0x14188e2d8,'NATIONAL_TEAM':0x141889618,'MEDIA_SOURCE':0x1418bdd08}
        rt={k:self.rtti(self.pe,v) for k,v in vs.items()};req(all(k==v['class'] for k,v in rt.items()),'target RTTI')
        req(self.slot(vs['CLUB'],2)==0xe89a00 and self.slot(vs['CLUB'],3)==0xe82aa0 and self.slot(vs['MEDIA_SOURCE'],19)==0x15457c0,'owner and media slots')
        for o in (0xe8cb93,0xe8411d):req(self.i(o).operands[1].imm==0x43736d65,'Csme dispatch')
        req(self.i(0x4381577).operands[1].imm==0x4d656c66 and self.i(0x438157f).operands[1].imm==0x4d736964 and
            self.i(0x4381587).operands[1].imm==0x4d656453 and self.i(0x4381596).op_str=='edi, byte ptr [rcx + 8]','entry getter exact 4CCs')
        links={0xe8cb99:0xe8db41,0xe8db54:0xeb4430,0xeb4430:0x3b17180,0x3b173e8:0xeb0bd0,0xeb0bd0:0x3b0f420,
               0x3b0f452:0x154d690,0x154d690:0x43803c0,0x3b0f518:0x154d750,0x154d750:0x4381560,0x438157d:0x4381596,0x438158f:0xfe68b0,
               0xe84123:0xe854cc,0xe854eb:0xeafe10,0xeb0060:0x15329d0,0x15329d0:0x4365f50,
               0x4365fa4:0xf8d120,0xf8d120:0x3c0d7b0,0x3c0d817:0x1582d60,0x4365ff2:0x15837d0,
               0x1583580:0x43d2bb0,0x43d2bda:0xf7e440,0xf7e440:0x3bf3460,0x15835c0:0x43d2e40,
               0xf4911f:0x1052b30,0x1052b30:0x3d7afc0,0xf49ca4:0x11a0160,0x11a0160:0x3e68540,
               0xf48eb1:0x1545680,0x1545680:0x437a080,0x1545ec6:0xfae340,0xfae340:0x3c600f0,
               0x814110:0x35b07f0,0xfe96c0:0x3cd4360}
        req(all(self.dest(o)==z for o,z in links.items()),'collection, writer/fixup, target factory links')
        req(self.rip(0x1582d98)==VT and self.rip(0x3d7afdb)==vs['NATIONAL_TEAM'] and self.rip(0x3e6858b)==vs['TEAM'] and
            self.rip(0x437a0a5)==vs['MEDIA_SOURCE'] and self.i(0xf49106).op_str=='bl, 0xb','class constructor vptrs / full-team dispatch')
        g=self.rip(0x3b171ac);req(g==self.rip(0xeafe9b)==self.rip(0x4365f59)==self.rip(0x4365f97)+0x440 and
            self.i(0x3c0d81c).op_str=='rax, qword ptr [rsi + 0x440]' and self.i(0x3b171d3).op_str=='qword ptr [rbx + 0x30], rdx' and
            self.i(0x3b173c0).op_str=='rax, qword ptr [rsi + 0x18]' and self.i(0x1582dfd).op_str=='qword ptr [rsi + 0x30], rdi','same collection and joined owner')
        req(self.i(0x43d2e7c).op_str=='rax, qword ptr [r12 + 0x30]' and self.i(0x43d2e86).op_str=='eax, dword ptr [rax + 8]' and
            self.i(0x43d2e8b).op_str=='eax, 0xffffffff','owner writer uses ordinal, not ID')
        req(self.i(0xfe68ca).op_str=='dword ptr [rcx], 0' and self.i(0xfe68e4).op_str=='eax, dword ptr [rbx + 4]' and
            self.i(0xfe68eb).op_str=='rbx, dword ptr [rbx]' and self.i(0xeb00b9).op_str=='byte ptr [rsi + 8], al' and
            self.i(0xeb00fd).op_str=='qword ptr [rsi], rax','inner getter/ setter uses the same element as the read sinks')
        base=0xf49d38; cj={}
        for tid,target in ((7,0xf48ea6),(24,0xf490f9)):
            pos=base+4*tid;delta,=S.unpack_from('<i',self.pe.raw,pos);req(base+delta==target,'target table jump cell')
            cj[tid]=dict(cell=pos,rel32=delta,handler=target,bytes=self.pe.raw[pos:pos+4].hex())
        spans=[(0xe89a00,0xe89a6c),(0xe8cb93,0xe8cb9f),(0xe8db41,0xe8db5e),(0xe8411d,0xe84129),(0xe854cc,0xe854f0),
               (0x3b1719d,0x3b171e2),(0x3b1724f,0x3b17264),(0x3b173a0,0x3b17405),(0x3b0f4e0,0x3b0f529),
               (0x43803c0,0x4380440),(0x4381560,0x43815fe),(0xfe68b0,0xfe6913),(0xfe71d8,0xfe71fa),
               (0xeafe9b,0xeafee2),(0xeb004c,0xeb006a),(0xeb00b0,0xeb0102),(0x4365f50,0x4366001),
               (0x3c0d803,0x3c0d845),(0x1582d7d,0x1582e07),(0x43d2bb0,0x43d2be6),(0x43d2e6f,0x43d2f06),(0x43d2f49,0x43d2fba),
               (0x3bf349a,0x3bf3519),(0xf490f9,0xf49129),(0xf49c4a,0xf49ca9),(0x3d7afdb,0x3d7afe5),(0x3e6858b,0x3e68595),
               (0x437a096,0x437a0af),(0x3c60102,0x3c60133),(0x1545cf5,0x1545d01),(0x1545e92,0x1545ecb)]
        sites=self.add(*links,0xe82aa0,0x15837d0)
        for a,z in spans:sites+=self.span(a,z)
        # Target table 7 is read only for its real ordinal domain. Preserve its stream-width landmarks, not another field ledger.
        media_sites=self.add(*[0x15457e5,0x154580c,0x154582e,0x15458df,0x15458f9,0x154590d,0x154592a,0x1545951,0x1545975,
            0x1545997,0x1545a03,0x1545b10,0x1545b32,0x1545b79,0x1545bb2,0x1545bf9,0x1545c30,0x1545c4e,0x1545cb7,0x1545cce,
            0x1545d1e,0x1545d42,0x1545d59,0x1545d7b,0x1545dc6,0x1545e00,0x1545e4a,0x1545e85,0x35b0828,0x3cd4384,0x3c60119])
        return dict(rtti=rt,table_factory_cells=cj,collection_global_VA=hex(g),collection_vector_offset=0x80,owner_object_offset=0x30,
                    nested_vector_offsets=[0x18,0x20,0x28],instructions=sorted(set(sites)),target7_transfer_landmarks=media_sites,
                    parent_getter='CLUB slot 2 -> Csme -> outer collection filtered by owner pointer -> vector entries -> inner 4CC getter (not outer slot 2)',
                    full_team_caveat='table24 selector 11 chooses NATIONAL_TEAM in the full-team arm; runtime compatibility gate f49100 retained, no running configuration claimed',
                    exclusivity='not club-exclusive: actual owners include selector 11; play label is not a PLAYER pointer or dispatch proof')


def choose_frame(z, archive, offset, bound, ent):
    hits=[]; candidates=[]
    for p in range(offset,min(offset+64,bound-3)):
        if archive[p:p+4]!=MAGIC:continue
        end=min(p+ent['packed_size'],bound); dz=z.ZstdDecompressor().decompressobj()
        try:raw=dz.decompress(archive[p:end])
        except z.ZstdError:continue
        if not dz.eof:continue
        hit=dict(offset=p,relative_offset=p-offset,compressed_bytes=end-p-len(dz.unused_data),payload_bytes=len(raw),
                 count=u32(raw,8) if len(raw)>=12 and raw[2:6]==b'tad.' else None,sha256=sha(raw));hits.append(hit)
        if len(raw)==ent['size']:candidates.append((hit,raw))
    req(len(candidates)==1,f'no unique frame by directory size: {hits}')
    (hit,raw),=candidates;return raw,hit,hits


def archives():
    os.environ.setdefault('FM24_DB_DIR',str(ROOT/'scratch/data'))
    import fm24_dump as fm
    sys.path.append(str(_cfg.VENDOR_DIR))
    import zstandard as z
    codec=fm._reader();infos={};fetch={};payload=None
    for key,num in [('client',31),('server',77)]:
        name=key+'_db.dat';_,b,d=codec['_entries'](fm.DB_DIR/name,name)
        es={e['path'].rsplit('/',1)[-1]:e for e in d['entries']};base=d['data_base'];toc=d['toc_offset']
        member='table_59.dat';present=member in es
        req(len(es)==num and base==34 and present==(key=='server'),'archive directory presence')
        def get(n,b=b,es=es,base=base,toc=toc):
            e=es[n];o=e['offset'];lim=min((base+v['offset'] for v in es.values() if v['offset']>o),default=toc)
            buf,hit,hits=choose_frame(z,b,o,lim,e)
            req(hit['offset']==base+o and hit['compressed_bytes']==e['packed_size'] and hit['offset']+e['packed_size']<=lim,'selected canonical bounded frame')
            return buf,dict(entry=e,data_base=base,bound=lim,selected_frame=hit,frames=hits)
        fetch[key]=get;v=infos[key]=dict(directory_entry_count=num,archive_sha256=sha(b),present=present)
        if not present:
            v.update(entry=None,payload_sha256=None,row_count=None,stride=None,stride_histogram=None);continue
        payload,frame=get(member);v.update(frame)
        h=frame['selected_frame'];req((len(payload),sha(payload),h['offset'],h['compressed_bytes'],h['count'])==(SIZE,PAY_SHA,38661659,62202,N),'server payload anchor')
        before,meta=get('table_52.dat');prev=meta['selected_frame'];legacy=fm.load_payload(codec,key,59)
        req(len(before)==22 and u32(before,8)==0 and prev['offset']+prev['compressed_bytes']==h['offset'] and
            prev['offset']==frame['entry']['offset']-1 and len(frame['frames'])==1 and legacy==payload,'adjacent stub, not a table59 first-magic failure')
        _,_,near=choose_frame(z,b,prev['offset'],frame['bound'],frame['entry'])
        req(len(near)==2 and near[0]['sha256']==sha(before),'two-frame alternate-start control')
        v.update(adjacent_stub=dict(entry=meta['entry'],selected_frame=prev,scan_from_previous_magic=near,
                      note='Preceding empty table52 magic is one byte before table59 directory-relative start; legacy loader happens to return the right frame.'),
                 legacy_load=dict(payload_bytes=len(legacy),sha256=sha(legacy)),entry_sha256_field=frame['entry'].get('sha256'))
    return infos,payload,fetch


def take(b,p,w,what):
    req(0<=p<=len(b) and 0<=w<=len(b)-p,f'{what}: short @{p} width {w}')
    return b[p:p+w]

def footer(b,p):
    v=take(b,p,9,'footer')
    k,f,u=S.unpack('<IBI',v)
    req(k==0,f'footer @{p}: count {k}, requires {12*k} triplet bytes');req(p+9==len(b) and f==1,'footer observed flag/closure')
    return dict(offset=p,count=k,flag=f,last_u32=u,hex=v.hex(),semantic='last u32 equals maximum observed identity; no general meaning asserted')


def row(st,b,p,ordinal,mode,cut=None):
    req(mode in MODES,'caller mode probe option')
    start=p;sel=take(b,p,1,f'row {ordinal} selector')[0];p+=1;body=p;pc=START
    state={};ts=[];items=[];paths=[];partial={};io=None;cap=0;idx=0;stored=None
    # Valid loader context: wrapper retained, table callback present, allocations succeed.
    # Choose warm/no-final-ref and (for a synthetic second grow) generic free. No claim of runtime branch observations.
    assumed_taken={0x15833b9,0x1583407,0x15832ea,0x1583568}
    while True:
        if pc in READS:
            name,w,*_=READS[pc];label=f'row {ordinal} site {pc:#x} {name}';addr=p
            if pc==cut or p+w>len(b):
                io=f'{label}: short @{p} width {w}'
                if name=='identity':raise Check(io+'; replay rejects (no immediate native bulk status check)')
            else:
                data=b[p:p+w];p+=w;ts.append((pc,addr));state[name]=(data[0] if w==1 else u32(data) if w==4 else S.unpack('<ii',data) if w==8 else S.unpack('<III',data))
                if name=='tag':partial={'offset':addr,'tag':state[name]}
                if name=='pair':partial['raw_pair']=list(state[name])
                if name=='finish':partial['finish']=state[name]
        if pc==0x1583246:
            items.append(partial);idx+=1
        if pc==FAIL:raise Check(io+f'; IO-result -> {FAIL:#x} AL=false')
        if pc==RET:
            ids=state['identity'];req(ids[0]==stored==ordinal and ids[1]==ids[2]!=0,f'row {ordinal}: raw identity @{p-12} {ids}, stored ordinal={stored}')
            return dict(ordinal=ordinal,selector=sel,selector_start=start,body_start=body,end=p,owner=int.from_bytes(state['owner'].to_bytes(4,'little'),'little',signed=True),
                        outer_byte=state['outer_byte'],count=state['count'],items=items,identity=list(ids),stored=stored),ts,paths
        if pc in st.branches:
            branch=st.branches[pc];k=branch['class']
            if k=='IO-result':yes=(io is None) if pc==0x1583211 else (io is not None)
            elif pc==0x158322d:yes=state['count']==0
            elif pc==0x1583250:yes=idx>=state['count']
            elif pc==0x15832da:
                a,d=state.get('pair',(-1,-1));yes=d!=0;partial['stored_pair']=[a,d if yes else a]
            elif pc==0x158353a:
                a=state['identity'][0];yes=a<10000001;stored=a if yes else ordinal
            elif pc==0x1583339:yes=idx!=cap
            elif pc==0x15833e2:yes=cap==0
            elif pc==0x15833f6:yes=True # finite allocated span, not allocator special -1
            else:yes=pc in assumed_taken
            if k in ('wire_data','IO-result'):paths.append((pc,yes))
            pc=branch['taken_to' if yes else 'fallthrough_to']
        else:
            if pc==0x158346f:cap=max(cap+cap//2,idx+1)
            pc,=st.edges[pc]


def replay(st,b):
    req(b[:13]==bytes.fromhex('03017461642ef10d7723000000'),'main prelude/count')
    n=u32(b,8);forks={};rows=None
    for mode in MODES:
        p=13; seen=set(); samples=[]; sig=sha256();paths=Counter();rr=[];first_shape={}
        for i in range(n):
            r,tx,edges=row(st,b,p,i,mode);end=r['end'];cnt=r['count'];length=end-p
            req(length==22+10*cnt and len(r['items'])==cnt and r['identity'][1] not in seen,f'length/identity uniqueness row {i}')
            req(tx[0]==(0x15831c9,p+1) and tx[-1]==(0x158351f,end-12),'absolute transfer coordinates')
            seen.add(r['identity'][1]);paths.update(edges);sig.update(S.pack('<9I',i,p,p+1,end,r['selector'],cnt,*r['identity'])+sha256(b[p:end]).digest());rr.append(r)
            if cnt not in first_shape or i in (0,1,n-1):
                samples.append(dict(r,wire_hex=b[p:end].hex(),transfer_offsets=[list(s) for s in tx]));first_shape[cnt]=i
            p=end
        foot=footer(b,p)
        record=dict(rows=n,row_bytes=p-13,stride_histogram=hist(r['end']-r['selector_start'] for r in rr),counts=hist(r['count'] for r in rr),
                    selectors=hist(r['selector'] for r in rr),legacy_markers=hist(b[r['end']] for r in rr),identity_valid=n,trace_sha256=sig.hexdigest(),
                    edges={str(o):[paths[o,True],paths[o,False]] for o in st.branches if st.branches[o]['class'] in ('wire_data','IO-result')},samples=samples,footer=foot)
        req(record['counts']=={'0':6567,'1':2512} and record['selectors']==record['legacy_markers']=={'0':N} and p==224871 and foot['last_u32']==max(seen),'wire row/selector/marker/footer anchors')
        req(rows is None or (rr==rows and record==forks['1']),'ignored reader mode differential')
        rows=rr;forks[str(mode)]=record
    a,b2=rows[0],rows[2];patch=lambda p,x:b[:p]+x+b[p+len(x):];ident=a['end']-12;rank_at=b2['items'][0]['offset']+9
    zero_rank=row(st,patch(rank_at,b'\0'),b2['selector_start'],2,1)[0]
    req(zero_rank['end']==b2['end'] and zero_rank['items'][0]['finish']==0,'zero is a materialized scalar, not a missing entry')
    doub=patch(b2['body_start']+5,S.pack('<I',2));end=b2['end']-12;doub=doub[:end]+S.pack('<BiiB',0x80,5,0,0xff)+doub[end:]
    more,_,edge=row(st,doub,b2['selector_start'],2,1)
    req(more['end']==b2['end']+10 and more['items'][1]['stored_pair']==[5,5] and more['items'][1]['finish']==255 and
        (0x1583250,False) in edge,'second entry & normalization fixture')
    negatives=dict(short_transfers={str(site):negative(lambda:row(st,b,rows[i]['selector_start'],i,1,site))
                                    for site,(key,*_) in READS.items() for i in [2 if key in ('tag','pair','finish') else 0]},
                   identity_overwrite=negative(lambda:row(st,patch(ident,S.pack('<I',10000001)),13,0,1)),
                   unequal_identity=negative(lambda:row(st,patch(ident+8,bytes(4)),13,0,1)),
                   zero_identity=negative(lambda:row(st,patch(ident+4,bytes(8)),13,0,1)),
                   selector_one=row(st,patch(13,b'\x01'),13,0,1)[0],
                   materialized_zero_rank=dict(row=2,offset=rank_at,value=0,end=zero_rank['end'],count=zero_rank['count']),
                   changed_count_on_same_bytes=negative(lambda:row(st,patch(19,S.pack('<I',1)),13,0,1)),
                   second_entry=dict(row=more,loop_back_taken=True,tag='0x80 consumed; no predicate or bit mask',
                                     signedness='Melf 0xff native boxes 255 (outside schema cap), not -1; raw second Msid lane 0 copies lane0'),
                   nonzero_footer=negative(lambda:footer(patch(p,b'\x01'),p)),short_footer=negative(lambda:footer(b[:-1],p)))
    req(negatives['selector_one']['end']==a['end'],'selector does not determine length')
    return dict(row_count=n,stride=None,stride_histogram=forks['1']['stride_histogram'],payload_bytes=len(b),payload_sha256=sha(b),version=0xdf1,
                header_hex=b[:13].hex(),wire_origin=13,legacy_origin=14,wire_footer=forks['1']['footer'],legacy_footer_offset=p+1,legacy_footer_hex=b[p+1:].hex(),
                wire_equation='13 + 6567*22 + 2512*32 + 9 = 224880',legacy_equation='14 + sum(row_len=224858) + 8 = 224880',
                row_length='1 selector + (4+1+4) prefix + count*(1+8+1) entries + 12 identity = 22+10*count',
                legacy_marker='borrowed next selector, or first footer byte for last row; not read by slot19',forks=forks,negative_replays=negatives),rows


def t33_compare(raw,rows):
    pp=js(PROFILE);b=(ROOT/ROWS).read_bytes();lines=b.splitlines();f=pp['row_closure'];p=pp['payload']
    edge=rows[-1]['end']+1
    req(p['payload_sha256']==sha(raw) and p['packed_offset']==38661659 and p['packed_size']==62202 and f['model']=='variable' and
        f['rows_sha256']==sha(raw[14:edge]) and len(lines)==f['count']==N and pp['full_rows_sha256']==sha(b),'t33 existing image and rows')
    diff=[];old=[];next_=14
    for r,line in zip(rows,lines,strict=True):
        t=json.loads(line);i=r['ordinal'];p=r['body_start'];end=r['end']+1;w=end-p;q=t['offset'];z=q+t['len']
        req(t['row']==i and q==next_ and t['raw_hex']==raw[q:z].hex(),'historical JSONL was read unmodified');next_=z;old.append(t['len'])
        if (p,w)!=(q,t['len']):
            diff.append(dict(row=i,t33=t,native=dict(offset=p,len=w,bytes=raw[p:end].hex(),identity=r['identity']),
                             t33_tail=list(S.unpack_from('<III',raw,z-13)),marker=raw[z-1]))
    req([d['row'] for d in diff]==[0,1] and next_==edge and hist(old)=={'19':1,'22':6565,'25':1,'32':2512},'t33 precise frame counterexample')
    req(diff[0]['t33_tail']==[0,0x1000000,0x1000000] and diff[1]['t33_tail']==[1,2,2],'row 0 false shortest, row 1 recovers endpoint')
    note='tail id pair in every row equals 0x01000000, not a plausible media_source id; column semantics stay unresolved'
    req(note in (ROOT/OLD).read_text(encoding='utf8'),'preserve prior candidate negative verbatim')
    return dict(path=PROFILE,sha256=sha((ROOT/PROFILE).read_bytes()),rows_file=ROWS,rows_file_sha256=sha(b),row_block_sha256=f['rows_sha256'],
                matching_rows=N-len(diff),differences=diff,t33_stride_histogram=hist(old),t33_ambiguity=f['frame_ambiguity'],
                historical_negative=dict(path=OLD,sha256=sha((ROOT/OLD).read_bytes()),quote=note,clarification='The universal-pair wording in the old report does not match the actual JSONL. Do not rewrite it. The false row 0 pair is 0x01000000; true row 0 pair is (1,1).'))


def media_domain(raw, mode):
    """Read only table 7's ordinal/ID table; skip fields by its native widths and counts."""
    p=13; ids={}; trace=sha256(); ns=u32(raw,8)
    def take_here(w):
        nonlocal p
        x=take(raw,p,w,'table7 target access');p+=w;return x
    def number():return u32(take_here(4))
    def repeat(w):take_here(w*number())
    for i in range(ns):
        req(take_here(1)==b'\0','table7 selector')
        repeat(1);take_here(1);repeat(1);repeat(1);repeat(1);take_here(2);repeat(4)
        take_here(4);repeat(4);repeat(4);take_here(4)
        for _ in range(number()):take_here(8);repeat(1)
        if mode:
            take_here(6);cnt=take_here(1)[0];take_here(4*cnt)
        repeat(4);take_here(1)
        pos=p;k=take_here(12);j,x,y=S.unpack('<III',k)
        req(j==i and x==y!=0,'media target ordinal and two identity lanes');ids[j]=x;trace.update(S.pack('<I',pos)+k)
    f=footer(raw,p)
    req(ns==208 and len(set(ids.values()))==ns,'media live target set')
    return ids,dict(payload_sha256=sha(raw),payload_bytes=len(raw),count=ns,identity_trace_sha256=trace.hexdigest(),footer_offset=f['offset'])


def team_domain(raw, extra):
    n=u32(raw,8);z=len(raw)-9
    req(n==84507==u32(extra,8) and len(extra)==12+82*n and all(u32(extra,12+82*i)==i for i in range(n)),'team ordinal sidecar witnesses')
    # Boundaries only, not a Team field decoder. Use repeat-lane evidence and a full-team selector, independent of table59.
    cand=defaultdict(list)
    for m in re.finditer(rb'(?=(.{4})\1)',raw[17:z],re.S):
        o=m.start()+13;i,k=S.unpack_from('<II',raw,o);e=o+12
        if k and (i<n-1 and e<z and raw[e] in (10,11) or i==n-1 and e==z):cand[i].append(o)
    earliest=[];last=13
    for i in range(n):
        q=cand[i];j=bisect_left(q,last+1);req(j<len(q),f'team forward identity {i}');earliest.append(q[j]);last=q[j]+12
    limit=z-12
    for i in range(n-1,-1,-1):
        q=cand[i];j=bisect_right(q,limit)-1;req(j>=0 and q[j]==earliest[i],f'team nonunique ordinal witness {i}');limit=q[j]-13
    trace=sha256();ids={};last=13
    for i,o in enumerate(earliest):
        val=u32(raw,o+4);sel=raw[last];ids[i]=(sel,last,o,val);trace.update(S.pack('<5I',i,*ids[i]));last=o+12
    sels=hist(x[0] for x in ids.values());req(last==z and sels=={'10':84256,'11':251} and len({x[3] for x in ids.values()})==n,'target Team keys and selectors')
    return ids,dict(table=24,count=n,payload_sha256=sha(raw),sidecar_sha256=sha(extra),ordinal_witness_count=n,selector_histogram=sels,
                    identity_trace_sha256=trace.hexdigest(),method='sidecar ordinals; unique monotone repeated-lane tail chain in actual t24 under selectors 10/11; no footer u32 bound needed')


def ledger(raw,rows,fetch,scope):
    evidence=js(MASTER)['entities'];parents=[x for e in evidence['club.xml'] for x in e['fields'] if x['field']=='Csme']
    specs=parents[0]['list_item_fields'];occ=[x for x in js(OCC)['nested_fields'] if x['parent']=='Csme']
    req(len(parents)==1 and len(specs)==len(occ)==2 and [s['field'] for s in specs]==['Msid','Melf'] and [x['idx'] for x in occ]==[174,175] and
        all((s['field'],s['name'],s['type'],s.get('is_optional')=='true')==(x['code'],x['name'],x['type'],x['optional']) for s,x in zip(specs,occ)), 'unique frozen scoped occurrences')
    media={}; keys={}
    for archive,mode in [('client',0),('server',1)]:
        keys[archive],media[archive]=media_domain(fetch[archive]('table_7.dat')[0],mode)
    md=keys['server'];req(md==keys['client'],'same actual media_source ordinal -> ID mapping in both archives')
    targets,tm=team_domain(fetch['server']('table_24.dat')[0],fetch['server']('table_extra_24.dat')[0]); media_meta=dict(table=7,archives=media,
                     ordinal_keys=list(md),uid_trace_sha256=sha(b''.join(S.pack('<II',i,v) for i,v in md.items())))
    def owner_ex(r):
        o=r['body_start'];v=r['owner'];s,q,t,k=targets[v];return dict(row=r['ordinal'],offset=o,bytes=raw[o:o+4].hex(),value=v,
                      target_selector=s,target_selector_offset=q,target_identity_offset=t,target_identity=[v,k,k])
    req(all(r['owner'] in targets for r in rows),'owner target actual ordinal membership')
    own=Counter(targets[r['owner']][0] for r in rows);req(own=={10:8941,11:138},'owner split')
    firsts={str(s):owner_ex(next(r for r in rows if targets[r['owner']][0]==s)) for s in sorted(own)}
    def sample(r,j):
        it=r['items'][j];p=it['offset'];return dict(row=r['ordinal'],entry=j,entry_offset=p,hex=raw[p:p+10].hex(),pair_offset=p+1,
                               finish_offset=p+9,pair=it['raw_pair'],finish=it['finish'],outer_offset=r['body_start']+4,outer_byte=r['outer_byte'])
    flat=[(r,j) for r in rows for j in range(r['count'])];f0=sample(*flat[0]);pairs=[r['items'][j]['raw_pair'] for r,j in flat]
    vals=[r['items'][j]['finish'] for r,j in flat];tags=[r['items'][j]['tag'] for r,j in flat]
    limit=int(specs[1]['max_value']);bad=[sample(r,j) for (r,j),v in zip(flat,vals) if v>limit]
    null=sum(x==[-1,-1] for x in pairs);live=[tuple(x) for x in pairs if x[0]>=0]
    req(null==2512 and not live and not bad and set(tags)=={1} and min(vals)==1 and max(vals)==33,'full-table observed domain anchors')
    owns=dict(object_offset=0x30,legacy_offset=0,wire_offset=1,width=4,type='i32 ordinal to team/table24; -1 writer null',matches=N,
              distinct=len({r['owner'] for r in rows}),minus_one_count=sum(r['owner']==-1 for r in rows),selector_histogram={str(k):v for k,v in sorted(own.items())},
              first_by_selector=firsts,field_not_in_schema=True,scope_counterexample=firsts['11'])
    alias_misses=[r for r in rows if r['owner'] not in md]
    pair=dict(code='Msid',schema=specs[0],occurrence=['club.xml','Csme',174],getter=dict(compare=0x438157f,box_call=0x438158f,tag='MedS',member_offsets=[0,4],
                negative_guard=0xfe68cd,lane_loads=[0xfe68e4,0xfe68eb]),static_binding='verified 8 B tagged identity-pair sink (not the outer team ordinal)',
                candidate_sink=dict(site=0x15832d2,width=8,legacy='10+10*j',wire='11+10*j',when='0 <= j < count'),
                grade='held_no_live_media_reference',row_offset=None,wire_offset=None,reason='All materialized entries are null. No populated reference to adjudicate against actual media_source keys; no scalar ordinal coordinate.',
                profile=dict(rows=N,no_entry_rows=N-len(flat),entries=len(flat),raw_pairs={'-1,-1':null},null_pairs=null,zero_lane_count=sum(x.count(0) for x in pairs),
                    normalized_copy_count=sum(x[1]==0 for x in pairs),live=len(live),ordinal_matches=sum(a in md for a,_ in live),uid_matches=sum(a in set(md.values()) for a,_ in live),
                    first_null=f0,first_not_a_live_ordinal=f0,first_domain_conflict=None,
                    rejected_outer_owner_as_media_ordinal=dict(matches=N-len(alias_misses),misses=len(alias_misses),first_miss=owner_ex(alias_misses[0]))),
                write_sites=[0x43d2f7a,0x43d2f96],
                live_contract='Getter boxes both signed lanes with MedS; generic setter helper packs target +0xc/+0x10 or null. Do not assert an observed UID/ordinal join.')
    rank=dict(code='Melf',schema=specs[1],occurrence=['club.xml','Csme',175],getter=dict(compare=0x4381577,member_load=0x4381596,member_offsets=[8],extension='movzx'),
              sink=dict(site=0x1583317,width=1,legacy='18+10*j',wire='19+10*j',when='0 <= j < count',writer_site=0x43d2fb2),
              row_offset=18,wire_offset=19,offset_semantics='first entry only, not a scalar present on every outer row',grade='L3_table59_conditional_named_coordinate',
              profile=dict(rows=N,no_entry_rows=N-len(flat),entries=len(flat),histogram=hist(vals),min=min(vals),max=max(vals),zero_count=vals.count(0),
                           minus_one_count=0,raw_ff_count=vals.count(255),bit_mask=None,first_value=f0,first_domain_conflict=None,violations=len(bad),
                           interpretation='u8 zero-extended; no native -1 sentinel and no zero rewrite; absence is count=0, not an integer zero'),
              negative_outer_byte_alias=f0,domain=dict(xml_max=limit,xml_default=int(specs[1]['default_value']),native_signed=False))
    return dict(table_type=59,parent='Csme',scope=['club.xml','Csme'],occurrences_source=OCC,occurrences_sha256=sha((ROOT/OCC).read_bytes()),
                native_binding_count=2,L3=1,club_exclusive_L3=0,L4=0,fields=[pair,rank],unscoped_owner=owns,targets={'media_source':media_meta,'team':tm},
                outer_non_schema_byte=dict(object_offset=0x38,legacy_offset=4,wire_offset=5,unsigned_histogram=hist(r['outer_byte'] for r in rows),
                    zero_count=sum(r['outer_byte']==0 for r in rows),mask=None,note='Unscoped 1 B sink, not Melf: first inner row has outer 2 vs inner 4; no 4CC evidence for an empty-vector fallback.'),
                inner_tag=dict(entries=len(flat),histogram=hist(tags),sink='rsp+0x47, discarded',tested_mask=None,boolean_claim=False),scope_caveat=scope['exclusivity'])


def build():
    st=Static();a,raw,fetch=archives();r,rows=replay(st,raw);a['server'].update(r)
    prior=t33_compare(raw,rows);fields=ledger(raw,rows,fetch,st.scope)
    bs=[]
    for o,b in sorted(st.branches.items()):
        rpl={mode:f['edges'][str(o)] for mode,f in r['forks'].items() if str(o) in f['edges']}
        note=b['first_counterexample_or_constraint']
        if note=='short transfer fixture':note=r['negative_replays']['short_transfers'][str(b['evidence'][0])]
        bs.append(dict(b,edges_by_mode=rpl or None,first_counterexample_or_constraint=note))
    bs+=st.outer['branches'];OUT.mkdir(parents=True,exist_ok=True)
    cursor=dict(table_type=59,parent='Csme',status='variable cursor closed; one conditional L3 field, one no-live-reference hold',
        provenance=dict(editor=str(EXE),editor_sha256=EXE_SHA,frozen_snapshots=st.hashes),archives=a,factory=st.factory,rtti=st.vt,slots=st.slots,
        reader=dict(entry=START,end_exclusive=END,entry_VA=hex(st.pe.f2va(START)),end_VA=hex(st.pe.f2va(END)),extent_source='PE RUNTIME_FUNCTION, direct slot 19; inline identity tail',
                    chain=[START,0x1583500,0x158351f,RET],external_edges=[],blocks=st.blocks,reachable=len(st.edges),branches=len(st.branches),
                    caller_mode=dict(forwarded_site=0xf2ba38,callee_slot='rsp+0xd0',read=False,forks=list(MODES)),summarized_nontransfer_calls=st.opaque,
                    context_projection='First vector empty; live retained stream and table, allocation/copy/init/release/registration summarized. No actual observation of allocator/TLS/refcounts.'),
        transfers=[dict(site=SELECT,width=1,legacy_base=-1,wire_base=0,sink='loader selector'),*st.transfers],outer_transfers=st.outer['transfers'],
        scope_evidence=st.scope,t33_differential=prior,branch_classes=list(CLASSES),branch_counts={k:sum(b['class']==k for b in bs) for k in CLASSES},
        branch_shards=shards('branches',bs,26),instruction_shards=shards('instructions',[st.saved[i] for i in sorted(st.saved)],150))
    emit('cursor_csme.json',cursor);emit('fields_csme.json',fields)
    print('t41 build PASS: table59 9079 rows (6567*22 + 2512*32); both caller mode values close; L3=1, held=1, club-exclusive=0, L4=0')


def selftest():
    sys.path.append(str(_cfg.VENDOR_DIR));import zstandard as z
    enc=z.ZstdCompressor();a,b=b'stub',b'payload'*40;ea,eb=enc.compress(a),enc.compress(b)
    raw,hit,hits=choose_frame(z,ea+eb,0,len(ea+eb),dict(size=len(b),packed_size=max(len(ea),len(eb))))
    req(raw==b and hit['offset']==len(ea) and len(hits)==2,'size beats first magic')
    req(footer(S.pack('<IBI',0,1,17),0)['last_u32']==17 and 'short' in negative(lambda:take(b'',0,1,'fixture')),'short transfer and footer distinction')
    st=Static()
    def make(n):return S.pack('<BiBI',0,0,3,n)+S.pack('<BiiB',3,5,0,255)*n+S.pack('<III',0,1,1)
    for n in range(3):
        one,tx,edges=row(st,make(n),0,0,1);two,_,_=row(st,make(n),0,0,0)
        req(one==two and one['end']==22+10*n and len(tx)==4+3*n and len(one['items'])==n and all(e['stored_pair']==[5,5] for e in one['items']), 'native graph loop/normalization/mode fixture')
    print('t41 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true',help='test bounded frames and native CFG with 0/1/2 entries')
    try:
        selftest() if p.parse_args().selftest else build();return 0
    except Check as e:print('t41 check failed:',e,file=sys.stderr);return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't41 fatal {type(e).__name__}: {e}',file=sys.stderr);return 2


if __name__=='__main__':
    sys.path.insert(0,str(ROOT/'scripts'))
    raise SystemExit(main())
