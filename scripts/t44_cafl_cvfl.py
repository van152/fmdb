#!/usr/bin/env python3
"""t44: static CLUB_LINK route, named-member cursor, and scoped field profiles."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import argparse
import calendar
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct as S
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/t44/out'
EXE=Path(str(_cfg.EDITOR_EXE))
OLD=Path(str(_cfg.LEGACY_DIR))
EXE_HASH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
PAY_HASH='8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2'
PACK_HASH='894f1efb9caf18482402198ed19294d04725a583ca262a6a01b2ed95c2222fe0'
T35={'scratch/t35/out/cafl_cvfl_discovery.json':'35a7553fc84406fab1ec2aa6ce7435ecdf596d7fbe4a2109462419391475ba3b',
     'scratch/t35/out/REPORT.md':'442e84bcd9a3c58352020a59db0ac6051eeba585b5986360a4eb7fc53c438cc5'}
MASTER='evidence/fm24/reports/editor_schema/master.json'
PROV='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
AUX='evidence/fm24/reports/dbdat_decode/DB_SERVER_TABLES.md'
NEST='scratch/t24/out/subtables.part003.json'
MAGIC=bytes.fromhex('28b52ffd')
HEADER=bytes.fromhex('03017461642ef10d')
N=9261
VERSION=0x0df1
CLASS=('wire_data','runtime-external','IO-result','context-lifecycle','dead')
READER,DATE=0x1529210,0x39dd7b0
# site, object offset, wire width, IO branch; negative object offset = external count
READ=[(0x152923a,-1,4,0x1529241),(0x15293e7,0,4,0x15293ee),(0x1529407,0x30,1,0x152940e),
      (0x1529427,0x1c,4,0x152942e),(0x1529447,8,4,0x152944e),(0x1529470,0x20,4,0x152948b),
      (0x15294ad,0x24,4,0x15294c8),(0x15294e1,0x14,4,0x15294e8),(0x1529501,0x10,4,0x1529508),
      (0x1529521,0x31,1,0x1529528),(0x1529541,0x32,1,0x1529548),(0x1529555,0x28,4,0x152955c),
      (0x1529575,0x33,1,0x152957c),(0x1529595,0x34,1,0x152959c),(0x15295b5,0x35,1,0x15295bc),
      (0x15295d5,0x18,4,0x15295dc),(0x15295f5,0x36,1,0x15295fc),(0x1529617,0x2c,4,0x152961e)]
CODES={
 'affl':(0x15265f1,0x1526ced,None,'other_endpoint'), 'ismc':(0x15264e5,0x1526bb7,None,'endpoint_role'),
 'clfr':(0x43656ca,0x43656d7,None,'runtime_enum'),
 'stdt':(0x15262d9,0x152630a,0x20,'date'), 'endt':(0x15263a4,0x15263d5,0x24,'date'),
 'type':(0x1526776,0x1526e47,0x30,'enum_i8'), 'yfee':(0x152657b,0x1526587,0x10,'cash_i32'),
 'fri%':(0x152622d,0x15269e8,0x33,'i8'), 'msls':(0x15268f7,0x1526903,0x34,'i8'), 'pwgp':(0x1526463,0x1526b18,0x36,'i8'),
}
# compare, member read, bit extraction, bit index in shared u32 slot; never infer from co-occurrence.
BITS={
 'frly':(0x1526239,0x1526245,0x1526252,1),'golo':(0x15266f8,0x1526de2,0x1526def,2),
 'fotb':(0x15267fc,0x1526808,0x1526815,3),'plfr':(0x1526687,0x1526693,0x15266a0,4),
 'yutr':(0x1526977,0x1526983,0x1526990,5),'perm':(0x152666f,0x1526d17,0x1526d24,6),
 'smbo':(0x15262cd,0x1526a50,0x1526a5d,7),'fnhl':(0x15267f0,0x1526ea6,0x1526eb2,9),
 'hlwf':(0x1526704,0x1526710,0x152671c,10),'mrrl':(0x15268eb,0x1526f72,0x1526f7e,13),
 'scks':(0x1526879,0x1526885,0x1526891,14),'cpsd':(0x1526398,0x1526ab2,0x1526abe,15),
 'ualf':(0x1526782,0x152678e,0x152679b,16),'lpfs':(0x15264f1,0x15264fd,0x1526509,17),
 'ustf':(0x152656f,0x1526c21,0x1526c2d,18),'yout':(0x152696b,0x1526fd8,0x1526fe4,19),
 'rsrv':(0x152686d,0x1526f0c,0x1526f18,20),'pfpr':(0x152667b,0x1526d7c,0x1526d88,21),
 'UsSK':(0x15265e5,0x1526c87,0x1526c93,23),'bttr':(0x15265fd,0x1526609,0x1526615,28),
}

class Check(Exception): pass

def require(ok,msg):
    if not ok: raise Check(msg)

def H(buf): return sha256(buf).hexdigest()
def load(path): return json.loads((ROOT/path).read_bytes())
def U(b,p=0): return S.unpack_from('<I',b,p)[0]
def hist(xs): return dict(sorted(Counter(xs).items()))
def write(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def shards(kind,rows,size):
    names=[]
    for i in range(0,len(rows),size):
        name=f'{kind}.part{i//size+1:03}.json';write(name,{kind:rows[i:i+size]});names.append(name)
    return names

def provenance():
    ss={r['path']:r['sha256'] for r in load('evidence/MANIFEST.json')['files']}
    for k in (MASTER,PROV,AUX): require(H((ROOT/k).read_bytes())==ss[k],f'manifest mismatch {k}')
    require(ss[MASTER].startswith('7d57477e') and EXE_HASH in (ROOT/PROV).read_text(encoding='utf-8'),'source identity')
    for k,sha in T35.items(): require(H((ROOT/k).read_bytes())==sha,f't35 negative changed {k}')
    require(H((ROOT/NEST).read_bytes())==load(next(iter(T35)))['provenance']['sha256'][NEST],'t24 nested provenance')
    return dict(editor=str(EXE),editor_sha256=EXE_HASH,frozen_snapshots={k:ss[k] for k in (MASTER,PROV,AUX)},
                t35_unchanged_sha256=T35,t24_nested_sha256=H((ROOT/NEST).read_bytes()))

class Static:
    def __init__(self):
        from t05_pe import PE
        from capstone import Cs,CS_ARCH_X86,CS_MODE_64
        from t21b_control_flow import ReaderCFG
        self.p=PE(EXE); self.p.pe.parse_data_directories(directories=[3]); self.md=Cs(CS_ARCH_X86,CS_MODE_64);self.md.detail=True
        require(H(self.p.raw)==EXE_HASH,'original PE SHA')
        self.saved={}; self.nodes={}; self.br=[]; self.graph={}
        for start in (READER,DATE):
            c=ReaderCFG(self.p,self.md,start); require(not c.external_edges,'unexpected extent-external edge')
            self.nodes[start]=c
            self.graph[start]={self.p.va2f(v):[self.p.va2f(w) for w in c.successors[v]] for v in c.instructions}
            for v,i in c.instructions.items(): self.saved[self.p.va2f(v)]=i
    def i(self,o):
        if o not in self.saved:
            va=self.p.f2va(o);self.saved[o]=next(self.md.disasm(self.p.raw[o:o+15],va,1))
        return self.saved[o]
    def span(self,a,z):
        while a<z: a+=self.i(a).size
        require(a==z,f'slice end not instruction boundary {z:#x}')
    def dest(self,o):return self.p.va2f(self.i(o).operands[0].imm)
    def edge(self,o,t):require(self.dest(o)==t,f'direct edge {o:#x}')
    def op(self,o,text):require(self.i(o).op_str==text,f'operand {o:#x} {text}: {self.i(o).op_str}')
    def rip(self,o):
        i=self.i(o);m,=[x.mem for x in i.operands if x.type==3 and i.reg_name(x.mem.base)=='rip'];return i.address+i.size+m.disp
    def blob(self,o,n):return dict(file_offset=hex(o),VA=hex(self.p.f2va(o)),bytes=self.p.raw[o:o+n].hex())
    def rec(self,o,i):
        r=self.blob(o,i.size);r['instruction']=(i.mnemonic+' '+i.op_str).rstrip();return r
    def route(self):
        p=self.p
        cells=[(0x187c300,8),(0x187c318,8),(0x187c530,24),(0x1aacb20,14),(p.va2f(0x1418e2c24),5),(p.va2f(0x14192ee21),10)]
        require(p.raw[0x1aacb20:0x1aacb20+14]==b'.?AVCLUB@db@@\0' and p.va2f(S.unpack_from('<Q',p.raw,0x187c318)[0])==0xe89a00,'CLUB slot2')
        for a,z in [(0xe89a00,0xe89a6c),(0xe8b4cf,0xe8b4e7),(0xe8c1dc,0xe8c22c),(0xe8f130,0xe8f15a),
                    (0x4363814,0x4363837),(0x4363851,0x43638cc),(0x15322c3,0x1532313),(0x1532320,0x1532356),(0x1532388,0x15323f1),
                    (0xe95a70,0xe95ac7),(0xe9649d,0xe964f7),(0xe96597,0xe965b7),(0x3b0e22c,0x3b0e24e),
                    (0x43656bc,0x43656e7),(0xe96635,0xe96653),(0x1528476,0x15284be),(0x434e39f,0x434e3b3),
                    (0x434e3d2,0x434e3ea),(0x434e42b,0x434e442),(0x3ad70a3,0x3ad70c0),
                    (0x434e468,0x434e488),(0xf2a395,0xf2a3b4),(0xf3dba1,0xf3dbb3),(0x434e63c,0x434e6df),
                    (0x3ad6f5f,0x3ad6f85),(0xf73e20,0xf73e60),(0xf7411f,0xf7416e),(0xf48b30,0xf48b55),
                    (0x3bf348e,0x3bf34b6),(0x3bf34fd,0x3bf351d),(0x3cccb20,0x3cccb36)]:self.span(a,z)
        edges={0xe8b4e1:0xe8f130,0xe8f13d:0x15320b0,0x15320b0:0x43637a0,0xe8c217:0x1532260,
               0xe8f148:0xe95720,0xe8c222:0xe962a0,0xe95aa8:0xeaeb80,0xeaeb80:0x3b0e140,
               0x3b0e238:0x15261e0,0xe965a0:0x15328f0,0x15328f0:0x43656a0,0x43656c2:0x15261e0,
               0x15323e4:0x1528460,0x434e483:READER,0xf2a3af:READER,0xf3dbae:0x1529850,0x1529850:0x434e5e0,
               0x434e664:0xf7e440,0xf7e440:0x3bf3460,0x434e686:0xf7e440,0x434e6ca:0xe6ca10,0x434e6d5:0xe6ca10,
               0xe6ca10:0x3ad6f50,0xf73e31:0xe6ca10,0xf73e42:0xe6ca10,0xf741c3:0xf73e10,0xdb7f80:DATE}
        for o,t in edges.items():self.edge(o,t)
        self.op(0xe8b4db,'ebx, 0x4361666c');self.op(0xe8c1e8,'ebx, 0x4376666c')
        require(self.rip(0x434e39f)==0x1418e2c24 and p.raw[cells[-2][0]:cells[-2][0]+5]==b'.dat\0','named source extension')
        require(self.rip(0x1529357)==self.rip(0x153230a)==self.rip(0xf7411f)==0x141b5ecc8 and
                p.raw[cells[-1][0]:cells[-1][0]+10]==b'CLUB_LINK\0','same allocated POD type')
        # Reader initializes four plain qwords: no vptr. CVFL copies all 0x38 bytes from the same POD.
        self.span(0x1529383,0x15293d5);self.span(0x15297ce,0x1529804)
        for o in (0x1529393,0x152939a,0x15293a2,0x15293aa):require(self.i(o).operands[1].imm==0,'POD initialized with null/scalars')
        branch_tree={0x43638ab:'skip null',0x43638b7:'increment leading-offset for 4..8',0x43638bc:'also increment for 20',
                     0x15322ed:'wrapper mode off -> no validated copies',0x1532301:'empty source',0x1532354:'skip null; no test of validation result before append'}
        return dict(entry_class='CLUB_LINK',entry_rtti=None,entry_vptr=None,object_size=56,
                    club_vector=dict(begin=0x118,end=0x120,capacity=0x128,element='CLUB_LINK*'),
                    staging=dict(context_member=0x680,begin=0,end=8,capacity=16,allocator_pool_VA='0x141b5ecc8'),
                    vtable_slot19=None,table_type=None,source_name='club_links',source_extension='.dat',
                    direct_edges=[dict(source=o,target=t) for o,t in edges.items()],raw_data=[self.blob(o,n) for o,n in cells],
                    view_branches=branch_tree)
    def transfers(self):
        step=[];r=0
        for site,o,w,br in READ:
            if site in (0x1529555,0x1529617):
                self.edge(site,0xdb7f80);self.op(0x39dd7c8,'r8d, 4');self.op(site-7,f'rcx, [rbp + {o:#x}]')
            else:
                seq=[i for a,i in sorted(self.saved.items()) if site-32<=a<site]; reg=[i for i in seq if i.op_str==f'r8d, {w}']
                require(reg and self.i(site).op_str=='qword ptr [rax + 0x28]',f'stream width {site:#x}')
                want='rdx, [rsp + 0x44]' if o<0 else 'rdx, rbp' if o==0 else f'rdx, [rbp + {o:#x}]'
                if o==8: want='rdx, [rbp + 8]'
                require(any(i.op_str==want for i in seq),f'sink {site:#x}')
            step.append(dict(site=site,object_offset=None if o<0 else o,width=w,row_offset=None if o<0 else r,
                             absolute_first=8 if o<0 else 12+r,status_branch=br,actual_read=0x39dd7d4 if site in (0x1529555,0x1529617) else site,
                             condition='external version >= 0x0dd6' if site==0x1529617 else 'always for live stream'))
            if o>=0:r+=w
        require(r==47,'row sum');return step
    def branch_data(self,replay,tx):
        io={t['status_branch']:t for t in tx}
        wire={0x152934e:('count zero shortcut',0x152923a,'count=0 synthetic 12-byte payload'),
              0x152962c:('raw endpoint equality suppresses staging append, but not stream consumption',0x1529447,'row 0: copy endpoint A into B; 47 B still consumed'),
              0x1529794:('wire count vs completed items',0x152923a,'real row 9260 falls through; synthetic count=1 exits after row 0')}
        ctx={0x152926f:'staging capacity',0x15292a8:'old staging buffer null',0x15292c0:'allocator old capacity sentinel',
             0x15292d1:'allocator mode',0x15292e5:'allocator pool-index range',0x15292ee:'allocator pool pointer null',0x152930c:'allocator refcount mode',
             0x152937d:'TLS initialization guard',0x152945a:'stream null (subsequent status access requires live stream)',0x152947a:'stream final release',
             0x1529497:'stream null (same constraint)',0x15294b7:'stream final release',0x1529636:'append capacity',
             0x15296ca:'old vector end equals insertion point',0x15296fa:'old vector buffer null',0x152970e:'allocator capacity sentinel',
             0x152971f:'allocator mode',0x1529733:'allocator pool-index range',0x152973c:'allocator pool pointer null',
             0x1529755:'allocator refcount mode',0x15297a9:'allocator cleanup flag',0x15297c8:'TLS init sentinel',
             0x1529831:'allocator cleanup flag',0x39dd7de:'stream final release'}
        dead={0x15297a3:0x152979f,0x1529825:0x1529821,0x39dd7bc:0x39dd7d7}
        for start,graph in self.graph.items():
            prior={a+i.size:a for a,i in self.saved.items() if a in graph}
            for o in sorted(graph):
                i=self.saved[o]
                if not (i.mnemonic.startswith('j') and i.mnemonic!='jmp'):continue
                evidence=[prior[o]]
                if o in io:
                    t=io[o];k='IO-result';src='stream +0x10 or date helper AL; error exits reader';evidence+=[t['site']];ex=replay['short_read'][t['site']]
                elif o in wire:
                    k='wire_data';src,site,ex=wire[o];evidence+=[site]
                elif o==0x152960e:
                    k='runtime-external';src='global version word VA 0x141b60330, not an item selector';evidence+=[0x1529602];ex=replay['old_version']
                elif o in dead:
                    k='dead';evidence+=[dead[o]]
                    src='xor eax,eax; test al,al: taken edge impossible' if o!=0x39dd7bc else 'null edge lands at mov edi,[rsi+0x10] and cannot complete a valid read'
                    ex='Proof by constant zero' if o!=0x39dd7bc else 'Hypothetical null RSI; explicitly outside valid stream context'
                else:
                    require(o in ctx,f'unclassified {o:#x}');k='context-lifecycle';src=ctx[o]
                    ex='Context fixture: initial empty vector, live stream, successful allocation; other allocation/TLS/release paths not observed or replayed.'
                self.br.append(dict(function=start,site=o,taken_to=self.dest(o),fallthrough_to=o+i.size,classification=k,
                                    evidence=evidence,source=src,first_counterexample_or_constraint=ex,
                                    changes_regular_item_width=o==0x152960e))
        cfg={}
        for start,g in self.graph.items():
            c=self.nodes[start];cfg[start]=dict(entry=start,end_exclusive=c.function_end_off,entry_VA=hex(c.start_va),
                end_VA=hex(c.function_end_rva+self.p.base),external_edges=c.external_edges,reachable=len(g),
                successors=g,calls=[a for a in sorted(g) if self.saved[a].mnemonic=='call'])
        return cfg
    def check_field(self,code):
        cmp,entry,obj,kind=CODES[code] if code in CODES else (*BITS[code][:2],0x1c,'bit')
        require(self.i(cmp).operands[1].imm==int.from_bytes(code.encode(),'big'),f'4CC {code}')
        if code!='clfr':
            b=cmp+self.i(cmp).size;i=self.i(b)
            arm=self.dest(b) if i.mnemonic=='je' else b+i.size if i.mnemonic=='jne' else None
            if kind=='date':self.span(arm,entry)
            else:require(arm==entry,f'getter arm {code}')
        if kind=='bit':
            _,_,extract,bit=BITS[code]
            self.span(entry,extract+self.i(extract).size)
            require(self.i(extract).operands[1].imm==(1 if code=='ualf' else bit) and
                    self.i(entry).operands[1].mem.disp==(0x1e if code=='ualf' else 0x1c),f'flag bit {code}')
            if code not in ('ualf','smbo'):require(self.i(extract+self.i(extract).size).operands[1].imm==1,'single bit mask')
        if kind in ('date','enum_i8','cash_i32','i8'):
            if kind=='date':
                a=0x1526327 if code=='stdt' else 0x15263f2;self.span(entry,a)
            require(self.i(entry).operands[1].mem.disp==obj,f'field object offset {code}')
            if kind=='i8':
                pred=entry+self.i(entry).size;self.op(pred,'edi, -1');self.edge(pred+self.i(pred).size,0x1526b7c);self.i(0x1526b7c)
        if code=='affl':self.span(entry,0x1526d17);self.span(0x152703b,0x152706a)
        if code=='ismc':self.span(entry,0x1526bce)
        if code=='clfr':
            for o in (0x152866a,0x152861f,0x1528b4b,0x1528c51,0x1528bca,0x1528fe3,0x15323d3,0x15323ed): self.i(o)
        return dict(compare=cmp,getter_case=entry,object_offset=obj,encoding=kind)


def archives():
    import fm24_dump as fm
    sys.path.append(str(OLD/'tools/python'));import zstandard as z
    codec=fm._reader();root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if root.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    a={};clubs={};links=None
    for side,n in [('client',31),('server',77)]:
        name=side+'_db.dat';_,b,d=codec['_entries'](root/name,name);es={e['path'].rsplit('/',1)[-1]:e for e in d['entries']};base=d['data_base'];toc=d['toc_offset']
        def frame(key):
            e=es[key];p=base+e['offset'];end=p+e['packed_size'];bound=min((base+x['offset'] for x in es.values() if x['offset']>e['offset']),default=toc)
            require(p<end<=bound and b[p:p+4]==MAGIC,f'{key} member bounds')
            region=b[p:end];packed=H(region); candidates=[];offset=0
            while offset<len(region):
                require(region[offset:offset+4]==MAGIC,'frame magic inside member');ctx=z.ZstdDecompressor().decompressobj();raw=ctx.decompress(region[offset:]);used=len(region)-offset-len(ctx.unused_data)
                require(ctx.eof and used>0,'bounded frame complete');offset+=used
                candidates.append((raw,offset-used,used))
            chosen=[x for x in candidates if len(x[0])==e['size']];require(len(chosen)==1,'unique member frame by size');raw,off,used=chosen[0]
            require(e.get('sha256',packed)==packed,'directory SHA must describe packed region')
            return raw,dict(entry={**e,'sha256':packed},entry_sha256_source='computed over compressed region (directory parser does not supply this field)',
                            member_start=p,member_end=end,next_member_start=bound,frame_count=len(candidates),selected_frame=dict(offset=p+off,compressed_bytes=used,payload_bytes=len(raw)),payload_sha256=H(raw))
        present='club_links.dat' in es
        require(len(es)==n and base==34 and present==(side=='server'),'archive directory presence/base')
        a[side]=dict(directory_entries=n,archive_sha256=H(b),data_base=base,present=present,entry=None,payload_sha256=None,count=None,stride=None)
        clubs[side],_=frame('table_3.dat')
        if present:
            links,v=frame('club_links.dat');require(v['frame_count']==1 and v['entry']['sha256']==PACK_HASH and v['payload_sha256']==PAY_HASH and v['member_start']==38906250,'club links payload anchor')
            a[side].update(v,count=U(links,8),stride=47,version=VERSION)
    return a,clubs,links


def club_domains(clubs):
    b=clubs['client'];s=clubs['server'];n=U(b,8);p=14;ids={};compact=[];positions=[]
    require(n==U(s,8)==84259 and b[:8]==s[:8]==HEADER,'club key input')
    for j in range(n):
        hits=[]
        def tail(q):return S.unpack_from('<III',b,q)[0]==j and U(b,q+4)==U(b,q+8) and b[q+12] in (0,12)
        for w in (4,5):
            q=p+21+w
            try:
                for _ in range(2):
                    ln=U(b,q);q+=4
                    if ln>200:raise ValueError()
                    b[q:q+ln].decode('utf-8');q+=ln
                q+=3
                if tail(q):hits.append(q)
            except (ValueError,IndexError,S.error):pass
        if not hits:
            compact.append(j);key=S.pack('<I',j);q=b.find(key,p+20,min(p+8192,len(b)-13))
            while q>=0:
                if tail(q):hits.append(q)
                q=b.find(key,q+1,min(p+8192,len(b)-13))
        require(len(hits)==1,f'actual club key boundary {j}');q=hits[0];ids[U(b,q)]=U(b,q+4);positions.append(q);p=q+13
    require(p+8==len(b) and len(set(ids.values()))==n and len(compact)==3,'client club identity framing')
    keys=[S.pack('<III',i,u,u) for i,u in ids.items()];after=13;server=[]
    for key in keys:
        q=s.find(key,after,len(s)-9);require(q>=0,'missing server club key');after=q+12;server.append(q)
    before=len(s)-9
    for key,expected in zip(reversed(keys),reversed(server)):
        q=s.rfind(key,13,before);require(q==expected,'nonunique server identity-chain placement');before=q
    require(after==len(s)-9 and s[-9:]==b[-9:],'server terminal key/footer')
    return ids,dict(role='club/t3 target domain only; not the affiliation storage',actual_ordinals=len(ids),client_compact_rows=compact,
        server_identity_earliest_equals_latest=len(server),key_map_sha256=H(b''.join(keys)),
        client_payload_sha256=H(b),server_payload_sha256=H(s),client_positions_sha256=H(S.pack(f'<{n}I',*positions)),
        server_positions_sha256=H(S.pack(f'<{n}I',*server)),first=[0,ids[0],positions[0],server[0]],last=[n-1,ids[n-1],positions[-1],server[-1]])


def walk(b,tx,version,cut=None):
    # Native member/header wrapper consumes first 8B; read count then exactly that many PODs.
    require(b[:6]==HEADER[:6],'member prefix')
    limit=len(b) if cut is None else min(cut,len(b));p=8
    def take(t,j):
        nonlocal p
        w=t['width'];require(p+w<=limit,f'row={j} @{p} w={w} site={t["site"]:#x} short read')
        raw=b[p:p+w];p+=w;return int.from_bytes(raw,'little')
    n=take(tx[0],None);rs=[]
    for j in range(n):
        start=p;d={}
        for t in tx[1:]:
            if t['object_offset']==0x2c and version<0xdd6:continue
            d[t['object_offset']]=take(t,j)
        rs.append((start,p,d))
    require(p==len(b),f'footer/EOF mismatch @{p}: {len(b)-p} trailing bytes')
    return rs

def negative(f):
    try:f()
    except Check as e:return str(e)
    raise Check('negative fixture accepted')

def replay(b,tx):
    require(b[:8]==HEADER and U(b,8)==N,'header')
    rs=walk(b,tx,VERSION);require(len(rs)==N and hist(z-a for a,z,_ in rs)=={47:N},'row sizes')
    trace=sha256();first=[]
    for j,(p,z,d) in enumerate(rs):
        digest=H(b[p:z]);trace.update(S.pack('<IIII',j,p,z,d[0])+S.pack('<I',d[8])+bytes.fromhex(digest))
        if j in (0,1,2,N-1):first.append(dict(index=j,start=p,end=z,sha256=digest,endpoints=[d[0],d[8]],type=d[0x30],raw_hex=b[p:z].hex()))
    zero=b[:8]+S.pack('<I',0);one=b[:8]+S.pack('<I',1)+b[12:59];eq=bytearray(one);eq[21:25]=eq[12:16]
    require(not walk(zero,tx,VERSION) and walk(eq,tx,VERSION)[0][2][0]==walk(eq,tx,VERSION)[0][2][8],'wire count and endpoint equality controls')
    require(len(walk(one[:-4],tx,0xdd5))==1,'old version synth 43B')
    r=dict(header_bytes=12,footer_bytes=0,count=N,stride=47,row_block_bytes=N*47,payload_bytes=len(b),
           closure='12 + 9261 * 47 + 0 = 435279',row_trace_sha256=trace.hexdigest(),row_block_sha256=H(b[12:]),sample_rows=first,
           selector=None,selector_histogram={},identity_tail=None,
           coordinates=dict(native='first row @12; next rows @12+47*i',legacy14='non-native: subtract 2 from first-row field offsets; first lane split across header/row',
                            wire13='non-native: subtract 1; byte @13 is part of endpoint A, not a selector',first_counterexample='@12 f6040000 = ordinal 1270; @13/@14 would start inside it'),
           type_histogram=hist(d[0x30] for _,_,d in rs),
           endpoint_selflinks=sum(d[0]==d[8] for _,_,d in rs),
           replayed_branch_edges={0x152934e:{'taken':0,'fallthrough':1},0x152962c:{'taken':sum(d[0]==d[8] for _,_,d in rs),'fallthrough':N},
                                  0x1529794:{'taken':N-1,'fallthrough':1},0x152960e:{'taken':0,'fallthrough':N}},
           unnamed_lanes=[dict(row_offset=o,width=w,first_hex=b[12+o:12+o+w].hex(),distinct=len({b[a+o:a+o+w] for a,_,_ in rs}))
                          for o,w in [(21,4),(29,1),(30,1),(31,4),(37,1),(38,4),(43,4)]],
           short_read={t['site']:negative(lambda t=t:walk(b,tx,VERSION,t['absolute_first']+t['width']-1)) for t in tx},
           old_version=negative(lambda:walk(b,tx,0xdd5)),old_version_first_divergence='row 0 @55: skip 4B +0x2c; modern row ends @59, old row ends @55')
    return rs,r


def scope():
    m=load(MASTER);e,=m['entities']['club.xml'];require(e['id']=='club','entity id')
    t=load(NEST)['nested_fields'];out={}
    for parent,lo,hi in [('Cafl',370,398),('Cvfl',400,418)]:
        f,=[x for x in e['fields'] if x['field']==parent];items=f['list_item_fields']
        r=[x for x in t if x['parent']==parent];require([x['idx'] for x in r]==list(range(lo,hi+1)),'schema occurrence range')
        require([(x['code'],x['type']) for x in r]==[(x['field'],x['type']) for x in items] and len({x['field'] for x in items})==len(items),'unique scoped schemas')
        out[parent]=[(rec['idx'],x) for rec,x in zip(r,items)]
    return out,m['enums']

def profile(st,b,rs,tx,ids):
    occ,enums=scope();byobj={t['object_offset']:t for t in tx}
    def sample(j,ofs,w,value):
        p=rs[j][0]+ofs;return dict(row=j,absolute=p,hex=b[p:p+w].hex(),value=value)
    def first(vals,test,ofs,w):
        return next((sample(j,ofs,w,v) for j,v in enumerate(vals) if test(v)),None)
    def small(vals):return dict(min=min(vals),max=max(vals),distinct=len(set(vals)),top=Counter(vals).most_common(12))
    endpoint={};uid=set(ids.values())
    for name,o in [('A',0),('B',8)]:
        vals=[d[o] for _,_,d in rs];ofs=byobj[o]['row_offset']
        require(all(v in ids for v in vals),'endpoint missing from actual club keys')
        endpoint[name]=dict(row_offset=ofs,width=4,reader_site=byobj[o]['site'],actual_ordinal_hits=len(vals),
            first={**sample(0,ofs,4,vals[0]),'target_identity':ids[vals[0]]},
            wrong_uid_misses=sum(v not in uid for v in set(vals)),distinct_ordinals=len(set(vals)),
            wrong_uid_first=first(vals,lambda v:v not in uid,ofs,4))
        endpoint[name]['wrong_uid_row_misses']=sum(v not in uid for v in vals)
    signed=lambda v,w:v-(1<<(8*w)) if v>>(8*w-1) else v
    result={};date_profiles={}
    for parent,items in occ.items():
        rows=[]
        for idx,schema in items:
            code=schema['field'];r=st.check_field(code);obj=r['object_offset'];k=r['encoding']
            r.update(parent=parent,schema_idx=idx,code=code,schema=schema,grade='L3',row_offset=None)
            if k=='runtime_enum':
                r.update(grade='runtime_only_no_wire_slot',runtime_wrapper_byte=8,domain=[int(x['enum']) for x in enums['clfr']['values']],
                         first_counterexample='Synthetic A=null copies runtime reason 1 (Missing Club); B=null is another check. Reader has no reason sink.',
                         first_observation='row 0: no validation byte; do not treat any packed flag or +40 aux byte as clfr')
            elif k in ('endpoint_role','other_endpoint'):
                r.update(endpoint_slots=endpoint,row_offset_candidates=[0,9],derived=True,
                         formula='view club==A' if k=='endpoint_role' else 'view club==A ? B : A',
                         first_row_view_roles=[dict(viewer_ordinal=1270,ismc=True,affl_ordinal=11272),dict(viewer_ordinal=11272,ismc=False,affl_ordinal=1270)],
                         caveat='only for link registered in the current club; fixup may exclude rows before view access')
            else:
                t=byobj[obj];w=t['width'];o=t['row_offset'];vals=[d[obj] for _,_,d in rs]
                r.update(candidate_row_offset=o,width=w,reader_site=t['site'],row_offset=o)
                if k=='bit':
                    bit=BITS[code][3];samples=[(v>>bit)&1 for v in vals];byte=o+bit//8;mask=1<<(bit%8)
                    r.update(bit_index=bit,bit_mask_u32=1<<bit,byte_offset=byte,byte_mask=mask,counts=hist(samples),
                             first_set=first(vals,lambda v:v&(1<<bit),o,4),first_clear=first(vals,lambda v:not v&(1<<bit),o,4),
                             synthetic_one_hot=next(i for i in range(32) if ((1<<i)>>bit)&1))
                elif k=='date':
                    pairs=[(v>>16,v&0x1ff) for v in vals];sent=0x076c0001
                    valid=lambda v:(v&0xfe00)==0 and 1900<=v>>16<=2100 and 1<=v&0x1ff<=365+calendar.isleap(v>>16)
                    bad=first(vals,lambda v:not valid(v),o,w)
                    if bad:r.update(grade='held_domain_conflict',row_offset=None,first_counterexample=bad)
                    r.update(year_min=min(y for y,_ in pairs),year_max=max(y for y,_ in pairs),ordinal_day_min=min(d for _,d in pairs),
                             ordinal_day_max=max(d for _,d in pairs),default_1900_day1_count=vals.count(sent),
                             first_non_default=first(vals,lambda v:v!=sent,o,w),decoded='year=u16 at +2, day=value&511; explicit 1900/day1 constructor default, not asserted blank')
                    date_profiles[code]=r['grade']
                else:
                    vals=[signed(v,w) for v in vals];r['profile']=small(vals)
                    if k=='enum_i8':
                        domain=[int(x['enum']) for x in enums['CAfT']['values']];r.update(schema_enum_crosscheck='CAfT (no explicit enum_ref in item)',domain=sorted(domain),counts=hist(vals));bad=lambda v:v not in domain
                    else:
                        lo=int(schema['min_value']);hi=int(schema['max_value']);sent=k=='i8';bad=lambda v:not lo<=v<=hi and not(sent and v==-1)
                        r.update(domain=[lo,hi],minus_one_count=vals.count(-1),minus_one_semantics='getter omits value' if sent else 'getter boxes i32 as-is; no -1 sentinel proved')
                    x=first(vals,bad,o,w)
                    if x:r.update(grade='held_domain_conflict',row_offset=None,first_counterexample=x,conflicting_rows=sum(map(bad,vals)))
                    elif k=='i8' and all(v==-1 for v in vals):r.update(grade='held_all_missing',row_offset=None,first_counterexample=sample(0,o,w,-1))
            rows.append(r)
        result[parent]=rows
    return dict(source='server_db/club_links.dat',uniform_row_count=N,occurrences=result,endpoint_profiles=endpoint,
                boolean_layout='20 masks share 4-byte word at row +5; ismc is derived from the viewer club, not a 21st packed bit',
                flag_counts=[sum(bool(d[0x1c]&(1<<bit)) for _,_,d in rs) for bit in range(32)],
                occurrence_grades={p:hist(r['grade'] for r in rows) for p,rows in result.items()},L4=0)


def build():
    prov=provenance();st=Static();route=st.route();tx=st.transfers();ar,clubs,b=archives();rs,rep=replay(b,tx);ids,domain=club_domains(clubs)
    fields=profile(st,b,rs,tx,ids);cfg=st.branch_data(rep,tx)
    OUT.mkdir(parents=True,exist_ok=True)
    instructions=shards('instructions',[st.rec(o,i) for o,i in sorted(st.saved.items())],180)
    branches=shards('branches',st.br,24)
    write('cursor_club_links.json',dict(provenance=prov,archives=ar,transfer_calls=tx,reader_cfg=cfg,replay=rep,
          target_club_domain=domain,branch_classes=CLASS,branch_counts={k:sum(r['classification']==k for r in st.br) for k in CLASS},
          instruction_shards=instructions,branch_shards=branches))
    write('discovery_cafl_cvfl.json',dict(status='shared_named_auxiliary_closed',provenance=prov,static_chain=route,
          table_type=None,table_type_disposition='no factory case for these POD items; neither view is numeric table_type 3',
          archives=ar,views={'Cafl':dict(wire_storage='shared',source='club+0x118/+0x120',mode=0,
                                      note='server-config route skips leading 4..8/20 types before boxing raw links; config-dependent'),
                             'Cvfl':dict(wire_storage='shared',source='same club vector',mode=1,
                                      note='copies every non-null source entry, computes validation reason in a separate wrapper, no success-only gate at append; UI further downstream not asserted')},
          view_hypothesis='one source collection, two views; not established as validated-only subset; no second on-disk collection',
          retained_t35={'paths':list(T35),'meaning':'74 RTTI/45 stage2 zero-hits retained unchanged; named auxiliary outside numeric factory scan'},
          cursor='cursor_club_links.json',fields='fields_cafl_cvfl.json',instruction_shards=instructions,branch_shards=branches,
          first_counterexamples={'not_parent_row':'@12 first ordinal of independent named member; club+0x118 is a memory vector',
                                'not_vptr':'1529393 initializes first qword to zero; 15293e7 reads endpoint ordinal there',
                                'not_clfr_wire':'15323d3/15323e4/15323ed initialize/compute/store reason only in Cvfl wrapper'},L4=0))
    write('fields_cafl_cvfl.json',fields)
    print('t44 builder PASS: shared named auxiliary, 9261 x 47; grades',fields['occurrence_grades'])


def selftest():
    tx=[];p=12
    for site,o,w,br in READ:
        tx.append(dict(site=site,object_offset=None if o<0 else o,width=w));p+=w if o>=0 else 0
    b=HEADER+S.pack('<I',1)+bytes(47)
    require(p==59 and walk(b,tx,VERSION)[0][:2]==(12,59) and walk(b[:-4],tx,0xdd5)[0][:2]==(12,55),'synthetic version arms')
    require('@55' in negative(lambda:walk(b[:-1],tx,VERSION)) and 'trailing' in negative(lambda:walk(b,tx,0xdd5)),'synthetic truncation and surplus')
    for code,(*_,bit) in BITS.items():require(sum((1<<i)>>bit&1 for i in range(32))==1,'single bit '+code)
    print('t44 builder selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true');a=ap.parse_args()
    sys.path.insert(0,str(ROOT/'scripts'))
    try: selftest() if a.selftest else build();return 0
    except Check as e: print(f't44 FAIL: {e}',file=sys.stderr);return 1
    except Exception as e: print(f't44 fatal: {e}',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
