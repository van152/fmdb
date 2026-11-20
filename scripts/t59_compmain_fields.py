"""t57: bounded Competition table_25 identity census, reader replay and frozen schema join."""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t59/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
LOC = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
BIG = 'evidence/fm24/reports/dbdat_decode/db_tables_big.json'
BIGMD = 'evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md'
HEAD = bytes.fromhex('03017461642ef10d')
FOOT = bytes.fromhex('00000000014ec43a77')
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
SIDES = ('client','server')
IDS = (2,3,5,10,21,25)
PRIOR = 'reports/t01f_comp_row_offsets.json'
SAMPLES = 'evidence/fm24/reports/dbdat_decode/client_table_25_competition_samples.json'
N = 7047
OPTIONS = {}
CAP = 1000000

class Check(Exception): pass

def ck(ok, detail):
    if not ok: raise Check(detail)

def H(b): return sha256(b).hexdigest()
def J(path): return json.loads((ROOT/path).read_bytes())
def U(b, at=0): return S.unpack_from('<I',b,at)[0]
def hist(xs): return dict(sorted(Counter(xs).items()))
def emit(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def archives():
    depot=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if depot.drive.upper()=='Z:' or depot.resolve().drive.upper()=='Z:': raise ValueError('Z: forbidden')
    old=ROOT.parent/'fm24'
    sys.path.append(str(old/'tools/python'))
    import zstandard as z
    entries=runpy.run_path(str(old/'scripts/modding_read_dbdat.py'))['_entries']
    raw,meta={},{}
    for side in SIDES:
        _, b, d=entries(depot/f'{side}_db.dat'); base=d['data_base']
        index={e['path']:e for e in d['entries']}; ck(base==34 and len(index)==(31 if side=='client' else 77),(side,'directory'))
        meta[side]={'archive_sha256':H(b),'entries':len(index),'data_base':base,'members':{}}
        for tid in IDS:
            name=f'{side}_db/table_{tid}.dat'; e=index[name]; a=base+e['offset']; end=a+e['packed_size']
            bound=min((base+v['offset'] for v in index.values() if v['offset']>e['offset']),default=d['toc_offset'])
            ck(base<=a<end<=bound,(name,'range')); frames=[]; candidates=[]; p=a
            while p<end:
                ck(b[p:p+4]==b'\x28\xb5\x2f\xfd',(name,p,'magic'))
                dec=z.ZstdDecompressor().decompressobj(); payload=dec.decompress(b[p:end]); q=end-len(dec.unused_data)
                ck(dec.eof and q>p,(name,p,'zstd EOF'))
                frames.append([p,q,len(payload)])
                if len(payload)==e['size']: candidates.append(payload)
                p=q
            ck(len(candidates)==1,(name,'size selector'))
            payload,=candidates; ck(payload[:8]==HEAD,(name,'version'))
            raw[side,tid]=payload
            meta[side]['members'][str(tid)]=dict(member=name,range=[a,end],bound=bound,frames=frames,declared_size=e['size'],
                payload_sha256=H(payload),compressed_sha256=H(b[a:end]),count=U(payload,8))
    return raw,meta


def candidates(b):
    import numpy as np
    n=U(b,8); groups=[[] for _ in range(n)]; points=[]
    for k in range(4):
        v=np.frombuffer(b,dtype='<u4',offset=k,count=(len(b)-k)//4)
        w=np.flatnonzero((v[:-2]<n)&(v[1:-1]==v[2:]))
        points.extend(zip(v[w].tolist(),(4*w+k).tolist(),v[w+1].tolist()))
    for i,a,u in sorted(points): groups[i].append((a,u))
    return groups


def path_count(b, groups, header, footer, tail, markers, nonzero, increasing, recover=False):
    # Candidate positions are absolute triple starts. For tail=13, the lookahead byte
    # is assigned to the preceding row here (t50 coordinates), not to the PC reader.
    prev=[]; path_back=[]; limit=len(b)-footer
    for i,group in enumerate(groups):
        cur=[]; back={}; prefix=[0]; apos=[]
        if not increasing:
            for p,_,c in prev: apos.append(p); prefix.append(prefix[-1]+c)
        for a,u in group:
            end=a+tail
            if a<header or end>limit or (i==len(groups)-1 and end!=limit) or (nonzero and u==0): continue
            if markers is not None and (a+12>=len(b) or b[a+12] not in markers): continue
            if i==0: n=1; witness=None
            elif not increasing: n=prefix[bisect_right(apos,a-tail)]; witness=None
            else:
                n=0; witness=None
                for p,v,c in prev:
                    if p>a-tail: break
                    if v<u: n+=c; witness=p
            if n:
                cur.append((a,u,min(CAP,n)))
                if recover: back[a]=witness
        if not cur:
            return dict(paths=0,first_dead_ordinal=i,first_rejected_candidate=list(group[0]) if group else None),None
        if recover: path_back.append(back)
        prev=cur
    n=min(CAP,sum(v for _,_,v in prev)); at=None
    if recover and n==1:
        a=prev[0][0]; at=[]
        for back in reversed(path_back): at.append(a); a=back[a]
        at.reverse()
    return dict(paths=n,saturated=n==CAP,first_dead_ordinal=None),at


def framing(b):
    groups=candidates(b); n=U(b,8)
    opts={f'marker_0_footer_{k}':(13,k,13,{0},True,True) for k in (7,8,9,10,12)}
    opts.update({f'header_{k}':(k,8,13,{0,12},True,True) for k in range(11,16)})
    opts.update({f'triple_footer_{k}':(13,k,12,{0,12},True,True) for k in (7,8,9,10,12)})
    opts.update(selector_lookahead=(13,8,13,{0,12},True,True),no_marker=(13,8,13,None,True,True),
        allow_zero=(13,8,13,{0,12},False,True),no_uid_order=(13,8,13,{0,12},True,False),
        both_relaxed=(13,8,13,{0,12},False,False),wire_triple=(13,9,12,{0},True,True),
        triple_no_lookahead=(13,9,12,None,True,True))
    result={}; chosen=None; OPTIONS.update(opts)
    for key,args in opts.items():
        ans,at=path_count(b,groups,*args,recover=key=='wire_triple'); result[key]=ans
        if at is not None: chosen=at
    result.update(count=n,candidate_histogram=hist(map(len,groups)),cap=CAP)
    return result,chosen

# Logical outer positions. Collections and optional opaque inline objects have one
# complete outer span (presence/tag remains its own site where separately read).
COLOR=(0x4330d22,0x4330d67,0x4330dad,0x4330df3,0x4330e39)
SA=(0x4339ed1,0x4339eed,0x4339f09,0x4339f25,0x4339f45,0x4339f65,0x4339f88)
PRE=[('selector',0xf2ba0e,1,None),('m15c',0xeb7030,1,0x15c),('m15d',0xeb7054,1,0x15d),
     ('colour_tag',0x4330d01,1,None),*[(f'm{0x120+4*i:x}',s,2,0x120+4*i) for i,s in enumerate(COLOR)],
     ('m134',0x4330e7d,1,0x134),*[(f'm{d:x}',s,1,d) for d,s in zip((0x1a0,0x1a2,0x1a3,0x1a4,0x1a5),(0xeb7091,0xeb70b7,0xeb70dd,0xeb7100,0xeb7123))],
     ('stat_a_tag',0x4339ea1,1,None),*[(f'm{0x198+i:x}',s,1,0x198+i) for i,s in enumerate(SA)],
     ('stat_b_tag',0x433bbe5,1,None),('m189_197',0x433bc32,15,0x189),('mf6',0xeb7174,1,0xf6),
     ('m138',0xeb718b,4,0x138),('m13c',0xeb71a2,4,0x13c),('m58',0xeb726c,4,0x58),('m60',0xeb728c,4,0x60),
     ('m70',0xeb72ac,4,0x70),('m68',0xeb72cc,4,0x68),('m150',0xeb7376,2,0x150)]
EX0=[(f'm{d:x}',s,w,d) for d,s,w in [(0x180,0xeb73b9,2),(0xb8,0xeb73d5,4),(0x188,0xeb7400,1),(0x184,0xeb7423,2),
     (0x186,0xeb7446,2),(0x182,0xeb7469,2),(0x160,0xeb748c,8),(0x168,0xeb74af,8),(0x170,0xeb74d2,8),(0x178,0xeb74f5,8)]]
EX1=[('mf0',0xeb75ed,4,0xf0),('m1a1',0xeb7610,1,0x1a1),('m1a8',0xeb7633,1,0x1a8),('mf4',0xeb7656,1,0xf4),('mf5',0xeb768c,1,0xf5)]
EXT=EX0+[('vec30',0x3b1f05f,4,0x30),('a8_present',0xeb7532,1,None),('obj_a8',0xeb75ca,None,0xa8)]+EX1+[
     ('e0_present',0xeb76c0,1,None),('obj_e0',0xeb76fb,None,0xe0),('vec18',0xeb7dd2,4,0x18),
     ('e8_present',0xeb7728,1,None),('obj_e8',0xeb7783,None,0xe8),('c0_present',0xeb77a9,1,None),('obj_c0',0xeb7804,None,0xc0),
     ('c8_present',0xeb782a,1,None),('obj_c8',0xeb7860,None,0xc8),('m1a7',0xeb7883,1,0x1a7),
     ('d0_present',0xeb78a4,1,None),('obj_d0',0xeb78f2,15,0xd0),('d8_present',0xeb7913,1,None),('obj_d8',0xeb7961,15,0xd8),('vec100',0xeb7982,2,0x100)]
POST=[(f'm{d:x}',s,w,d) for d,s,w in [(0x148,0xeb7a37,4),(0x152,0xeb7a5a,2),(0x154,0xeb7a80,2),(0x156,0xeb7aa8,2),
      (0x158,0xeb7ad0,2),(0x15a,0xeb7af8,2),(0x80,0xeb7bdc,4),(0x88,0xeb7bff,4),(0x90,0xeb7c22,4),(0x98,0xeb7c45,4)]]+[
      ('wbcl_present',0xeb7c8f,1,None),('m14c',0x350260d,2,0x14c),('m140',0xeb7cc4,4,0x140),('m144',0xeb7cdb,4,0x144),
      ('mf7',0xeb7cfe,1,0xf7),('mf8',0xeb7d21,1,0xf8),('mf9',0xeb7d44,1,0xf9),('identity',0x3c60119,12,8)]
SPEC=PRE+EXT+POST
BY={s[0]:s for s in SPEC}

COLLECTIONS={'vec30':[0xeb750e,0x3b1f0d2],'vec18':[0xeb7e1b,0x37b8731,0x37b874c,0x37b8768,0x37b8784,0x37b87b4],
 'obj_a8':[0x37c18d7,0x37c18f6,0x37c1919,0x37c1939,0x37c1959,0x37c1979,0x37c1999,0x37c19b9,0x37c19d9,0x37c19f9,0x37c1a20,0x37c1a46,0x37c1a62,0x37c1a7e,0x37c1ab1,0x37c1ad0,0x37c1af8,0x37c1b17,0x37c1b4b],
 'obj_e0':[0x838b6b],'obj_e8':[0x4387ae0,0x155c152,0x155c2f9,0x155c31a,0x155c33d,0x155c360,0x155c38d,0x155c3b5,0x155c3e0,0x155c40c],
 'obj_c0':[0x438b6a1,0x155d053,0x155d244,0x155d268,0x155d28d,0x155d412,0x155d433,0x155d454,0x155d475,0x155d499,0x155d4b9],
 'obj_c8':[0x438e871,0x438bff1,0x438c00c,0x438c028,0x438c044,0x438c060,0x438c089],
 'obj_d0':[0x3b1e7e2,0x3b1e7fc,0x3b1e84c,0x3b1e85f,0x3b1e87e,0x3b1e8b2],
 'obj_d8':[0x3b1e7e2,0x3b1e7fc,0x3b1e84c,0x3b1e85f,0x3b1e87e,0x3b1e8b2],
 'vec100':[0xeb79f9,0x37be3c0,0x37be3db,0x37be404]}

class Cursor:
    def __init__(self,b):self.b=b;self.p=13;self.end=len(b)-9;self.i=-1
    def take(self,w):
        a=self.p;self.p+=w
        ck(w>=0 and self.p<=self.end,f'row {self.i} @{a}: short span {w}')
        return self.b[a:self.p]
    def v(self,w,signed=False):return int.from_bytes(self.take(w),'little',signed=signed)
    def count(self,w,signed=False):
        a=self.p;n=self.v(w,signed);ck(0<=n<=self.end-self.p,f'row {self.i} @{a}: invalid count {n}');return n

def replay(b,mode):
    c=Cursor(b); rows=[]; book=defaultdict(list); order=Counter()
    ck(b[:8]==HEAD and U(b,8)==N,'COMP header/count')
    for i in range(N):
        c.i=i; start=c.p; trace=[]
        def event(k,operation=None):
            a=c.p
            try: val=c.v(BY[k][2]) if operation is None else operation()
            except Check as e: raise Check(f'{k}: {e}') from e
            book[k].append((i,a,c.p-a));trace.append(k);return val
        def fixed(seq):
            for k,*_ in seq:event(k)
        def expect(k,expected):
            a=c.p;x=event(k);ck(x==expected,f'row {i} @{a}: {k} {x} != {expected}')
        def vec18():
            for _ in range(c.count(4,True)):
                v=c.v(1,True);c.take(7+(v>=2))
        def a8():
            v=c.v(1);c.take(32+4*(v>=2)+9+(2 if v>=3 else 1)+4+4)
        def e8():
            c.take(4)
            for _ in range(c.count(4)):
                v=c.v(2,True);c.take(6+(2 if v>=2 else 1)+1+(v>=3))
        def c0():
            c.take(1)
            for _ in range(c.count(4)):
                c.take(2);c.take(12*c.count(4))
        expect('selector',0);fixed(PRE[1:3]);expect('colour_tag',1);fixed(PRE[4:15]);expect('stat_a_tag',2)
        fixed(PRE[16:23]);expect('stat_b_tag',3);fixed(PRE[24:30]);
        at=book['m1a0'][-1][1];ck(b[at]!=4,f'row {i} @{at}: inline name alternative')
        fixed(PRE[30:]);
        if mode:
            fixed(EX0);event('vec30',lambda:c.take(2*c.count(4)))
            if event('a8_present'):event('obj_a8',a8)
            fixed(EX1)
            if event('e0_present'):
                # The type-erased item dispatch is not assumed to have a fixed stride.
                event('obj_e0',lambda:ck(c.count(4)==0,f'row {i}: untraced nonempty e0'))
            event('vec18',vec18)
            if event('e8_present'):event('obj_e8',e8)
            if event('c0_present'):event('obj_c0',c0)
            if event('c8_present'):event('obj_c8',lambda:c.take(25))
            event('m1a7')
            if event('d0_present'):event('obj_d0')
            if event('d8_present'):event('obj_d8')
            event('vec100',lambda:c.take(5*c.count(2,True)))
        fixed(POST[:10]);p=event('wbcl_present')
        if p:event('m14c')
        fixed(POST[12:-1]);a=c.p;event('identity');j,u,v=S.unpack_from('<III',b,a)
        ck(i==j and u==v and u>(rows[-1][2] if rows else 0),f'row {i} @{a}: identity {(j,u,v)}')
        rows.append((start,c.p,u));order[tuple(trace)]+=1
    ck(b[c.p:]==FOOT,f'footer @{c.p}, {b[c.p:c.p+9].hex()}')
    return rows,book,order

BASE_COMPS={'duni':(0xfe3912,0xfe3bff,4,'uid'), 'rdui':(0xfe3862,0xfe389d,8,'rdui')}
NEW_COMPS={
 'cext':('m1a1',0xec0f5e,0xec3629,'bit',2,[0xec363a,0xec363d]),
 'cusn':('m1a1',0xec0536,0xec384e,'bit',0,[0xec3856]),
 'culn':('m1a1',0xec0093,0xec009f,'bit',6,[0xec00b1,0xec00b4]),
 'LAUC':('m1a7',0xec1421,0xec142d,'enum',-1,[0xec1436,0xec1439]),
 'dbty':('mf4',0xec152a,0xec3896,'enum',-1,[0xec389f,0xec38a2]),
 'PLgn':('mf5',0xec0baa,0xec0bb6,'enum',None,[]),
 'CpRp':('m188',0xec03a9,0xec03d4,'context_number',None,[0xec03ce]),
 'cnam':(None,0xec0fc3,0xec3423,'not_read',None,[]),
 'csnm':(None,0xec1018,0xec1024,'not_read',None,[]),
 'c3ln':(None,0xec24d1,0xec45c4,'not_read',None,[]),
 'VARt':(None,0xec04b0,0xec04bc,'context_only',None,[0xec04bf,0xec1830]),
 'HKEt':(None,0xec0888,0xec0894,'context_only',None,[0xec0897,0xec1830]),
}
OLD_FORMAT={**dict.fromkeys(('cfcl','cbcl','ctcl','wbcl'),'colour'), 'levl':'level','CTty':'enum',
 **dict.fromkeys(('cmnl','cmnw','cmxl','cmxw'),'distance'), **dict.fromkeys(('wbst','wben'),'date'),
 **dict.fromkeys(('cuae','csso'),'bool'),'crep':'i16'}
REFS={'cnti':10,'ccti':5,'cpcm':25,**dict.fromkeys(('cnor','csou','ceas','cwes'),2)}
# Local getter routes: top bit-test gate, then helper rel32 case or exact compare.
# No XML index is used to calculate a wire lane.
STATUS_A=[('Pcsp',0x151de17,0),('Pcsk',0x151ddb8,1),('Pcsf',0x151dcfa,2),('Pcsr',0x151de75,3),
          ('Pcsb',0x151da62,4),('Pcsh',0x151dd59,5),('Pcsy',0x151ded1,6)]
STATUS_B=[('Pcjm',0x151ed23,0),('Pcja',0x151e5e6,1),('Pcjc',0x151ec65,2),('Pcjy',0x151ee9e,3),
          ('Pcji',0x151ee3f,4),('Pcjg',0x151ecc4,5),('Pcjp',0x151ed81,6),('Pcjs',0x151ede0,7)]
STATUS_C=[('Pcdf',0x151e65d,0x151e669,8,0xec09c0),('Pcda',0x151e651,0x151eefd,9,0xec09c0),
          ('Pcdr',0x151e839,0x151f079,10,0xec09c0),('Pcss',0x151e6d4,0x151efbb,11,0xec1b4c),('Pcsc',0x151e6c8,0x151ef5c,14,0xec1b4c)]
def target_domains(raw,rows):
    result={}; meta={s:{} for s in SIDES}
    for t in IDS:
        for s in SIDES:
            b=raw[s,t];n=U(b,8);end=len(b)-9
            if t==25: ats=[r[1]-12 for r in rows[s]]; method='independent main reader replay'
            elif t==10:
                f=J('scratch/t47/out/cursor_nation_tax.json')[s]
                ck(H(b)==f['payload_sha256'],(t,s,'t47 payload match'))
                ats=[r['identity_at'] for r in f['rows']]; method='t47 raw coordinates, each triple checked'
            elif t==3 and s=='server':
                ats=[];p=13
                for i,u in result['client',3].items():
                    p=b.find(S.pack('<III',i,u,u),p,end);ck(p>=0,(t,s,i,'earliest exact triple'));ats.append(p);p+=12
                p=end
                for (i,u),a in zip(reversed(result['client',3].items()),reversed(ats),strict=True):
                    p=b.rfind(S.pack('<III',i,u,u),13,p);ck(p==a,(t,s,i,'earliest/latest mismatch'))
                method='ordered client exact triple earliest=latest'
            else:
                w={2:(43,43),3:(127,127),5:(34,48),21:(38,181)}[t][s=='server']
                if t==3:
                    # t3 is variable; verify keys only. No club-field parser is run.
                    f,ats=path_count(b,candidates(b),13,9,12,{0,12},True,True,True)
                    ck(f['paths']==1,(t,s,'target uniqueness'));method='unique t3 raw identity path'
                else:
                    ck(end==13+n*w,(t,s,'fixed target EOF'));ats=[13+(i+1)*w-12 for i in range(n)];method=f'fixed {w} B target identity tails'
            ck(len(ats)==n and ats[-1]+12==end and b[end:end+5]==b'\0'*4+b'\1',(t,s,'target framing'))
            d={}; acc=bytearray()
            for i,a in enumerate(ats):
                j,u,v=S.unpack_from('<III',b,a);ck(i==j and u==v and u,(t,s,i,a,'target actual triple'));d[i]=u;acc+=b[a:a+12]
            ck(len(set(d.values()))==n,(t,s,'target UID uniqueness'))
            result[s,t]=d;meta[s][str(t)]={'method':method,'count':n,'identity_sha256':H(acc),'first':[0,d[0]],'last':[n-1,d[n-1]]}
    for t in IDS:ck(result['client',t]==result['server',t],(t,'paired target identities'))
    return result,meta

ROOTS=(0xeb7000,0x3b3f0d0,0x3c600f0,0x4330ce0,0x4339e80,0x433bbc0,0x39dd7b0,0x35025f0,
       0x3b1f030,0x37c18b0,0x838a80,0x37b8710,0x4387ab0,0x155c120,0x438b680,0x155d010,
       0x438e850,0x438bfd0,0x3b1e790,0x37be3a0,0xffa5d0)


def static(prior):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    pe=PE(EXE);ck(H(pe.raw)==EXEH,'editor sha');pe.pe.parse_data_directories(directories=[3]); md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    def ins(o):return next(md.disasm(pe.raw[o:o+15],pe.f2va(o),1))
    def blob(o,w):return dict(file_offset=o,VA=pe.f2va(o),bytes=pe.raw[o:o+w].hex())
    def tgt(i):return pe.va2f(i.operands[0].imm) if i.operands and i.operands[0].type==X86_OP_IMM else None
    def rip(o):i=ins(o);return i.address+i.size+i.operands[1].mem.disp
    def rec(o,i):
        d=dict(blob(o,i.size),instruction=(i.mnemonic+' '+i.op_str).strip())
        if i.mnemonic.startswith('j') or i.mnemonic=='call':d['direct_target']=tgt(i)
        return d
    records={}; branches=[]; extents={}
    wire={0xeb71bd,0xeb7544,0xeb76d2,0xeb773a,0xeb77bb,0xeb783c,0xeb78b6,0xeb7925,0xeb7995,0xeb7a1f,0xeb7ca1,0xeb7df5,0xeb7e3b,
          0x3b1f07a,0x3b1f0ba,0x4339ebc,0x433bc41,0x37c1a0b,0x37c1a9c,0x37b879c,0x155c378,0x155c3f3}
    external={0xeb7202,0xeb73a0,0xeb7671,0xeb770e,0x3b1e7a1,0xeb7c55,0xeb71b3}
    for root in ROOTS:
        g=ReaderCFG(pe,md,root); m={pe.va2f(a):i for a,i in g.instructions.items()}
        prev={o+i.size:(o,i) for o,i in m.items()}; io=[]; ncond=0
        for a,i in sorted(m.items()):
            records[a]=dict(rec(a,i),function=root,successors=[pe.va2f(v) for v in g.successors[i.address]])
            if i.mnemonic=='call' and i.operands[0].type==X86_OP_MEM and i.operands[0].mem.disp==0x28:io.append(a)
            if not i.mnemonic.startswith('j') or i.mnemonic=='jmp':continue
            ncond+=1;p=a;pred=None
            for _ in range(6):
                if p not in prev:break
                p,q=prev[p]
                if q.mnemonic.startswith(('call','j')):break
                if q.eflags:pred=p;break
            text=rec(pred,m[pred])['instruction'] if pred is not None else None
            typ='wire_or_wire_version' if a in wire else 'mode_or_runtime_version' if a in external else 'io_result' if (text and ('+ 0x10], 0' in text or tgt(i)==0xeb737f)) else 'unresolved_or_lifecycle'
            branches.append(dict(site=a,function=root,fallthrough=a+i.size,taken=tgt(i),predicate=pred,predicate_instruction=text,classification=typ))
        extents[str(root)]={'begin':root,'end_exclusive':g.function_end_off,'VA':pe.f2va(root),'reachable':len(m),'conditional':ncond,
                            'external_edges':g.external_edges,'direct_stream_calls':io}
    def add(*xs):
        for a in xs:
            if a not in records:records[a]=rec(a,ins(a))
    add(*(q[1] for q in SPEC),*(a for x in COLLECTIONS.values() for a in x))
    add(0xf48b41,0xf48b4c,0xf48b53,0xf49129,0xf4912e,0xf49139,0xf4913e,0xeb5dd5,0xeb5ddc,0xed0a30,0xed0a40,
        0xebf040,0xec4820,0xf02aa7,0xf02aaf,0xf02ab4,0xf02abb,0xff9910,0x3ceb8e2,0xf2ad00,0xf2ad1f,
        0xf2ba20,0xf2ba23,0xf2ba38,0xf2ba4b,0xf2ba51,0xf2ba7f,0xf2baa2,0xf2bac2,0xf2bacf,0xf2bad7,
        0xfae340,0xdb7f80,0x150ec50,0x151d2e0,0x151d710,0x7e30c0,0xeb7e50,0x9f9ab0,0x9f7c30,0x155b450,0x155ce40,
        0x155de30,0x155dad0,0xeb5580,0x9f9840,0xeb8b51,0xeb8b8f,0xeb893b,0xeb8952,0x3cc14da)
    f=0xf49d38;c=f+4*25;arm=pe.va2f(pe.f2va(f)+S.unpack_from('<i',pe.raw,c)[0]);ck(arm==0xf49129,'rel32 case 25')
    for a,b in [(0xf49139,0xeb5db0),(0xed0a40,0x3b3f0d0),(0x3b3f101,0xeb7000),(0xeb7d84,0xfae340),(0xfae340,0x3c600f0),
                (0xf2ba23,0xf48b30),(0xf2ba7f,0xffa5d0)]:ck(tgt(ins(a))==b,('chain',hex(a)))
    vt=rip(0xeb5dd5);tv=rip(0xf02ab4);ck(vt==0x14187dcb8 and tv==0x14187f6d8,'COMP/table vtables')
    def vslot(v,j,w):
        a=pe.va2f(v)+8*j;ck(pe.va2f(S.unpack_from('<Q',pe.raw,a)[0])==w,('vtable',j));return blob(a,8)
    def rtti(v,expected):
        a=pe.va2f(v);col=pe.va2f(S.unpack_from('<Q',pe.raw,a-8)[0]); td=pe.va2f(pe.pe.OPTIONAL_HEADER.ImageBase+U(pe.raw,col+12))
        s=pe.raw[td+16:pe.raw.index(b'\0',td+16)];ck(expected in s,('RTTI',s));return {'col':blob(col,24),'type_name':blob(td+16,len(s)+1),'name':s.decode()}
    cfg=ReaderCFG(pe,md,0xec0060); bg=ReaderCFG(pe,md,0xfe3520)
    def proof(k,cmp,member,g,expected=None,more=()):
        i=ins(cmp);j=ins(cmp+i.size)
        ck(i.mnemonic=='cmp' and i.operands[-1].type==X86_OP_IMM and i.operands[-1].imm==int.from_bytes(k.encode(),'big') and
           i.address in g.instructions and j.mnemonic in ('je','jne'),(k,'4CC equality'))
        first=j.operands[0].imm if j.mnemonic=='je' else j.address+j.size
        q=deque([(first,[])]);seen={first}
        while q:
            a,p=q.popleft();p=p+[pe.va2f(a)]
            if a==pe.f2va(member):break
            for v in g.successors.get(a,[]):
                if v not in seen:seen.add(v);q.append((v,p))
        else:raise Check((k,'getter path'))
        add(cmp,pe.va2f(j.address),*p,*more)
        if expected is not None:
            v=ins(member);ck(any(x.type==X86_OP_MEM and x.mem.disp==expected and v.reg_name(x.mem.base)=='r12' for x in v.operands),(k,'member displacement'))
        return dict(compare=cmp,equality=pe.va2f(j.address),equal_path=p,member_use=member,member=expected,additional_sites=list(more))
    joins={}
    for k,fmt in (OLD_FORMAT|dict.fromkeys(REFS,'ref')).items():
        x=prior['server_crosscheck']['crep_object_link'] if k=='crep' else prior['row_offset_map'][k]['property_link']
        d=0x180 if k=='crep' else prior['row_offset_map'][k]['object_offset'];slot=f'm{d:x}'
        cmp,mem=(int(x[n]['file_offset'],16) for n in ('compare','member_access'))
        more={'levl':[0xec467b,0xec4c84],'cmnl':[0xec33ba,0xec33c2],'cmnw':[0xec3586,0xec358e],
              'cmxl':[0xec37b4,0xec37bc],'cmxw':[0xec213c,0xec2144]}.get(k,[])
        joins[k]=dict(slot=slot,lane=0,format=fmt,arg=REFS.get(k),static=proof(k,cmp,mem,cfg,d,more),origin='t01f')
    for k,(slot,cmp,mem,fmt,arg,more) in NEW_COMPS.items():
        joins[k]=dict(slot=slot,lane=0,format=fmt,arg=arg,static=proof(k,cmp,mem,cfg,BY[slot][3] if slot else None,more),origin='t59')
    for k,(cmp,mem,lane,fmt) in BASE_COMPS.items():
        joins[k]=dict(slot='identity',lane=lane,format=fmt,arg=None,static=proof(k,cmp,mem,bg,lane+8,[0xfe38a2] if k=='rdui' else []),origin='t01f')
    helper=ReaderCFG(pe,md,0x151e500)
    gates={0xec061b:(0xec0604,0xec060a,0xec060d,0xec0613,0xec0618,0xec0621),
           0xec09a7:(0xec0994,0xec099a,0xec099d,0xec099f,0xec09a4,0xec2c5a),
           0xec09c0:(0xec09ad,0xec09b3,0xec09b6,0xec09b8,0xec09bd,0xec2c5a),
           0xec1b4c:(0xec0604,0xec060a,0xec060d,0xec1b44,0xec1b49,0xec2c5a)}
    add(0xec0140,0xec014c,0xec0151,0xec0166,0xec016b,0xeb7130,0xeb7147,0x433bc2f,0x433bc3b,0x433bc41)
    def status_join(k,branch,mem,lane):
        lea,cmp,range_jump,mask,bt,dst=gates[branch]; code=int.from_bytes(k.encode(),'big');i=ins(mem)
        ix=code+ins(lea).operands[1].mem.disp; limit=ins(cmp).operands[-1].imm; bits=ins(mask).operands[-1].imm
        ck(0<=ix<=limit and bits&(1<<ix) and ins(bt).op_str=='ecx, eax' and ins(range_jump).mnemonic=='ja' and
           ins(branch).mnemonic==('jae' if branch==0xec061b else 'jb') and (branch+ins(branch).size if branch==0xec061b else tgt(ins(branch)))==dst and
           (branch!=0xec1b4c or tgt(ins(0xec061b))==mask and not (ins(0xec0613).operands[-1].imm&(1<<ix))),('status gate',k))
        d,th=(0x198,0xec064a) if dst==0xec0621 else (0x189,0xec2c83); s=f'm{d+lane:x}' if d==0x198 else 'm189_197'
        ck(ins(dst).op_str==f'r12, {d:#x}' and ins(dst+7).op_str=='rcx, r12' and ins(dst+10).op_str=='edx, esi' and
           i.mnemonic=='movsx' and i.operands[1].mem.disp==lane and i.reg_name(i.operands[1].mem.base)=='rcx',('status member',k))
        add(lea,cmp,range_jump,mask,bt,branch,dst,dst+7,dst+10,th,mem,0xec061b,0xec0613)
        ev=dict(kind='local_status_gate',gate_sites=[lea,cmp,range_jump,mask,bt,branch],gate_index=ix,object_base_site=dst,helper_jump=th,member_use=mem,member=d+lane)
        joins[k]=dict(slot=s,lane=0 if d==0x198 else lane,format='enum',arg=None,static=ev,origin='t59')
        return ev
    for batch,branch,ops,root in [(STATUS_A,0xec061b,(0x151da43,0x151da49,0x151da4c,0x151da52,0x151da59,0x151da5d,0x151da60),0x151d9b0),
                                  (STATUS_B,0xec09a7,(0x151e5c7,0x151e5cd,0x151e5d0,0x151e5d6,0x151e5dd,0x151e5e1,0x151e5e4),0x151e500)]:
        add(*ops);t=rip(ops[3]);tab=pe.va2f(t)
        for k,mem,lane in batch:
            ev=status_join(k,branch,mem,lane);ck(tgt(ins(ev['helper_jump']))==root,('status helper root',k))
            ix=(int.from_bytes(k.encode(),'big')+ins(ops[0]).operands[-1].imm)&0xffffffff; cell=tab+4*ix
            ck(ix<=ins(ops[1]).operands[-1].imm and pe.va2f(t+S.unpack_from('<i',pe.raw,cell)[0])==mem,('status rel32 arm',k))
            ev['rel32_dispatch']=dict(sites=list(ops),table_va=t,index=ix,cell=blob(cell,4),target=mem)
    for k,hcmp,mem,lane,branch in STATUS_C:
        ev=status_join(k,branch,mem,lane);ck(tgt(ins(ev['helper_jump']))==0x151e500,('status helper compare root',k));ev['helper']=proof(k,hcmp,mem,helper)
    for k,hcmp,mem,lane,cmp in [('Pctd',0x151e6e0,0x151e6ec,12,0xec2c4e),('Pchd',0x151e845,0x151e851,13,0xec09c6)]:
        top=proof(k,cmp,0xec2c83,cfg,None,[0xec2c5a]); lo=proof(k,hcmp,mem,helper)
        ck(ins(mem).operands[1].mem.disp==lane and tgt(ins(0xec2c83))==0x151e500,'status byte')
        top['helper']=lo
        joins[k]=dict(slot='m189_197',lane=lane,format='enum',arg=None,static=top,origin='t59')
    direct=set(extents[str(0xeb7000)]['direct_stream_calls']);outer=direct&{s for _,s,*_ in SPEC}; alt=direct-outer
    ck(alt=={0xeb7218,0xeb72f8,0xeb7332},('main direct read accounting',sorted(alt)))
    for a,w in [(0x3c6010d,12),(0xf2ba02,1),(0xf2ba99,1),(0xf2bab9,4),(0xffa5fc,4)]:
        q=ins(a);ck(q.mnemonic=='mov' and q.op_str.startswith('r8d, ') and q.operands[-1].imm==w,('framing width',hex(a)));add(a)
    p={'editor':EXE.as_posix(),'editor_sha256':EXEH,'factory_case_25':{'base':f,'cell':blob(c,4),'arm':arm},
       'comp':{'vtable':vt,'rtti':rtti(vt,b'.?AVCOMP@db@@'),'slots':{str(j):vslot(vt,j,w) for j,w in [(2,0xec0060),(5,0xebf040),(19,0xed0a40)]}},
       'table_comp':{'vtable':tv,'rtti':rtti(tv,b'DATABASE_TABLE@VCOMP@db@@'),'ctor_sites':[0xf02aa7,0xf02aaf,0x3ceb8e2,0xf02ab4,0xf02abb]},
       'extents':extents,'main_direct_stream':{'outer':sorted(outer),'alternate_reference_mode':sorted(alt)},
       'framing_sites':{'header_count':0xf2ad00,'header_byte':0xf2ad1f,'row_selector':0xf2ba0e,'identity':0x3c60119,
           'footer_vector_count':0xffa602,'footer_byte':0xf2baa2,'footer_dword':0xf2bac2}}
    return p,sorted(records.values(),key=lambda x:x['file_offset']),branches,joins


def witness(i,a,raw,value=None,why=None):
    x=dict(row=i,at=a,raw=raw.hex(),value=value)
    if why:x['reason']=why
    return x


def profile(f,join,b,cells,keys):
    import calendar
    fmt,arg=join['format'],join['arg']; lo=f.get('min_value');hi=f.get('max_value'); er=f.get('enum_ref')
    target=keys.get(arg,{}) if fmt=='ref' else {}; wrong=set(target.values())
    freq=Counter();flags=Counter();vals=[];days=[]; first={};null=bad=live=wrong_hit=default_dates=0
    for i,a,w in cells:
        a+=join['lane'];ww={'uid':4,'rdui':4,'enum':1}.get(fmt,w); r=b[a:a+ww]; v=int.from_bytes(r,'little'); out=v; reason=None; absent=False
        if fmt=='ref':
            absent=v==0xffffffff
            if not absent:
                wrong_hit+=v in wrong
                if v not in wrong:first.setdefault('wrong_uid_miss',witness(i,a,r,v))
                if v not in target:reason='not a target ordinal'
                else:first.setdefault('target_hit',dict(witness(i,a,r,v),uid=target[v]))
        elif fmt=='colour':
            if v&0x8000:reason='bit 15 set in packed 15-bit colour'
        elif fmt in ('bit','bool'):
            if fmt=='bit':out=(v>>arg)&1
            elif v not in (0,1):reason='non-boolean byte'
            first.setdefault('first_'+str(out),witness(i,a,r,out))
        elif fmt=='date':
            day=v&511; flags[(v>>9)&127]+=1; year=v>>16;out=year
            if not (1<=year<=9999 and 1<=day<=365+calendar.isleap(year)):reason='invalid Gregorian packed year/day'
            days.append(day)
            if (year,day)==(1900,1):
                default_dates+=1;first.setdefault('first_1900_day1',witness(i,a,r,[year,day]))
            else:first.setdefault('first_nondefault_date',witness(i,a,r,[year,day]))
        elif fmt=='level':
            absent=v==100; out=int.from_bytes(r,'little',signed=True)+1
        elif fmt=='distance':
            signed=int.from_bytes(r,'little',signed=True);absent=signed<=0;out=signed/10
        elif fmt in ('i16','context_number'):
            out=int.from_bytes(r,'little',signed=True)
        elif fmt=='enum':
            out=int.from_bytes(r,'little',signed=(join['slot']!='mf5')); absent=arg is not None and out==arg
            if not absent and er and out not in f['_allowed']:reason=f'not in scoped enum {er}'
        elif fmt=='rdui':
            absent=r==b[a-4:a];out=v
        if not absent:
            live+=1; vals.append(out)
            if (lo is not None and out<float(lo)) or (hi is not None and out>float(hi)):reason='outside XML min/max after getter projection'
        else:null+=1;first.setdefault('first_null_or_suppressed',witness(i,a,r,out))
        freq[out]+=1
        if reason:bad+=1;first.setdefault('first_counterexample',witness(i,a,r,out,reason))
    note=None
    if cells:
        i,a,w=cells[0];a+=join['lane'];ww={'uid':4,'rdui':4,'enum':1}.get(fmt,w)
        if fmt=='enum' and not er:note='no scoped enum_ref; do not infer labels'
        elif fmt=='context_number':note='getter first tests context; raw byte is not unconditional editor value'
        elif not live:note='no live getter/domain witness'
        if note:first.setdefault('first_counterexample',witness(i,a,b[a:a+ww],None,note))
    return dict(tested=len(cells),live=live,null_or_suppressed=null,violations=bad,min_live=min(vals,default=None),max_live=max(vals,default=None),
                histogram=hist(freq) if len(freq)<=120 else None,distinct=len(freq),date_flag_histogram=hist(flags) if fmt=='date' else None,
                default_1900_day1=default_dates if fmt=='date' else None,day_range=[min(days),max(days)] if days else None,
                wrong_uid_hits=wrong_hit if fmt=='ref' else None,hold_reason=note,**first)


def fixture_checks(raw,runs,prior,keys):
    c,s=(raw[x,25] for x in SIDES); r0,b0,_=runs['client'];r1,b1,_=runs['server']
    ck(H(c)==prior['sources']['client_table_25']['payload_sha256'] and H(s)==prior['server_crosscheck']['payload_sha256'],'t01f exact two payloads')
    for (a,e,u),(k,q,v) in zip(r0,r1,strict=True):
        ck(u==v and c[a:a+71]==s[k:k+71] and c[e-56:e]==s[q-56:q],('t01f full common prefix/suffix',a,k))
    def point(side,slot,i,delta=0,w=None):
        cc=(b0 if side=='client' else b1)[slot];j,a,width=cc[i];ck(j==i,(slot,i)); w=width-delta if w is None else w
        return a+delta,raw[side,25][a+delta:a+delta+w]
    packed={}
    for k,d in prior['row_offset_map'].items():
        delta=0; slot=f'm{d["object_offset"]:x}' if 'object_offset' in d else None
        if k in ('rdui','duni'):slot='identity';delta=0 if k=='rdui' else 4
        width=d['width']; off=d['row_offset']
        for i in range(N):
            a,r=point('client',slot,i,delta,width);q,x=point('server',slot,i,delta,width)
            ck(a-r0[i][0]-1==off and r==x,(k,i,'full prior span'))
        for x in d['examples']:
            i=x['index'];a,r=point('client',slot,i,delta,width)
            ck((a,r,r0[i][2])==(int(x['payload_offset'],16),bytes.fromhex(x['bytes']),x['dbid']),(k,i,'frozen example'))
        packed[k]=dict(slot=slot,lane=delta,legacy_body_offset=off,width=width,rows_each=N,examples_verified=len(d['examples']))
    codec=[]
    for entry in prior['row_codec']['cursor_layout']:
        step=entry['step']; off=entry['row_offset']; width=entry['width']; d=entry['object_offset']; lane=0
        slot={'colour_block_version':'colour_tag','stat_block_a_version':'stat_a_tag','stat_block_b_version':'stat_b_tag','wbcl_present':'wbcl_present'}.get(step)
        if step=='following_zero_marker':
            ck(all(c[e:e+1]==s[q:q+1]==b'\0' for (_,e,_),(_,q,_) in zip(r0,r1,strict=True)), 't01f legacy lookahead')
            slot='legacy_lookahead'
        elif step in ('rdui','duni'):slot='identity';lane=0 if step=='rdui' else 4
        elif step=='stat_block_b_values':slot='m189_197'
        elif slot is None:slot=f'm{d:x}'
        for i in range(N):
            if slot=='legacy_lookahead':continue
            a,x=point('client',slot,i,lane,width);q,y=point('server',slot,i,lane,width)
            ck(a==r0[i][0]+1+off and x==y and len(x)==width,(step,i,'t01f complete cursor'))
            if 'expected' in entry:ck(int.from_bytes(x,'little')==entry['expected'],(step,i,'t01f expected byte'))
        codec.append(dict(step=step,slot=slot,legacy_body_offset=off,width=width,lane=lane))
    named=[]; parents=[]
    samples=J(BIG)['tables']['25']
    for d,x in zip(prior['verification']['continent_and_nation_named_anchors'],samples['named_anchor_checks'],strict=True):
        i=d['row_index'];uid=d['dbid'];ck(i==x['row_index'] and uid==x['dbid'] and r0[i][2]==uid,'named comp fixtures')
        z={}
        for k in ('ccti','cnti'):
            a,r=point('client',packed[k]['slot'],i);q,v=point('server',packed[k]['slot'],i)
            ck(a==int(d[k]['payload_offset'],16) and r==bytes.fromhex(d[k]['bytes'])==v and U(r)==x[k],(i,k,'anchor'))
            z[k]={'client_at':a,'server_at':q,'ordinal':U(r),'raw':r.hex()}
        named.append(dict(row=i,uid=uid,name=x['expected_name'],**z))
    live_cont={U(c,a) for i,a,w in b0['m58']} - {0xffffffff};ck(live_cont==set(range(6)),('six continents',live_cont))
    for d,x in zip(prior['verification']['cpcm_named_anchors'],samples['parent_reference_checks'],strict=True):
        i=d['row_index'];a,r=point('client','m68',i);q,v=point('server','m68',i);pa,pr=point('client','identity',352)
        ck(i==x['child_row_index'] and a==int(d['child_cpcm']['payload_offset'],16) and r==v==bytes.fromhex(d['child_cpcm']['bytes']) and U(r)==352 and
           pa==int(d['parent_identity']['payload_offset'],16) and pr==bytes.fromhex(d['parent_identity']['bytes']) and r0[352][2]==d['parent_dbid']==x['parent_dbid'] and r0[i][2]==x['child_dbid'], 'parent 352 anchor')
        parents.append(dict(row=i,client_at=a,server_at=q,parent_ordinal=352,parent_uid=r0[352][2],raw=r.hex()))
    for side in SIDES:ck([keys[side,10][139],keys[side,10][55]]==[765,110],(side,'England/China'))
    for d in prior['server_crosscheck']['crep_examples']:
        i=d['index'];a,r=point('server','m180',i)
        ck(a==int(d['server_crep']['payload_offset'],16) and r==bytes.fromhex(d['server_crep']['bytes']) and r1[i][1]-r1[i][0]-127==d['extra_length'],'t01f crep sample')
    return dict(t01f_sha256=H((ROOT/PRIOR).read_bytes()),accepted_client_slots=packed,complete_old_codec=codec,named=named,parents=parents,live_continents=sorted(live_cont),
                England=[139,765],China_PR=[55,110],native_identity_alias_note=prior['native_identity_slots']['dsha']['description'],falsified_t01f=prior['falsified'])


def describe(b,cells,rr):
    if not cells:return {'events':0,'bytes':0}
    a=bytearray();d=sha256();wcnt=Counter(); off=Counter()
    for i,p,w in cells:
        a+=S.pack('<III',i,p,w);d.update(b[p:p+w]);wcnt[w]+=1;off[p-rr[i][0]-1]+=1
    i,p,w=cells[0]
    return dict(events=len(cells),bytes=sum(k*v for k,v in wcnt.items()),span_histogram=hist(wcnt),coordinate_sha256=H(a),content_sha256=d.hexdigest(),
                body_offset_histogram=hist(off),first=witness(i,p,b[p:p+min(w,24)]))


def chunks(stem,x,n):
    for i in range(0,len(x),n):emit(f'{stem}.part{i//n+1:02d}.json',x[i:i+n])


def build():
    manifest={r['path']:r['sha256'] for r in J('evidence/MANIFEST.json')['files']}; frozen={k:H((ROOT/k).read_bytes()) for k in (MASTER,LOC,BIG,BIGMD,SAMPLES)}
    ck(all(manifest[k]==h for k,h in frozen.items()) and frozen[MASTER]==MASTERH and EXEH in (ROOT/LOC).read_text(encoding='utf-8'),'frozen manifest')
    prior=J(PRIOR);master=J(MASTER);xml=master['entities']['comp.xml'][0]['fields'];ck(len(xml)==255,'comp.xml denominator')
    raw,archives_info=archives(); sensitivity={};runs={};rr={};modes={};env={}
    for side in SIDES:
        b=raw[side,25];mode=int(side=='server');f,ats=framing(b); r,book,order=replay(b,mode);runs[side]=r,book,order;rr[side]=r
        ck(ats==[y-12 for x,y,u in r] and f['wire_triple']['paths']==1,(side,'independent identity path vs replay'))
        try:replay(b,1-mode)
        except Check as e:modes[side]={'mode':mode,'forced_opposite_first_failure':str(e)}
        else:raise Check('opposite mode unexpectedly closed')
        sensitivity[side]=f;end=r[-1][1];env[side]=dict(count=N,header=13,rows=end-13,footer=9,payload=len(b),
            header_hex=b[:13].hex(),footer_hex=b[end:].hex(),row_width_histogram=hist(y-x for x,y,u in r),
            row_trace_sha256=H(b''.join(S.pack('<III',x,y,u) for x,y,u in r)),uid_min=r[0][2],uid_max=r[-1][2])
    keys,targets=target_domains(raw,rr); fixtures=fixture_checks(raw,runs,prior,keys)
    prov,ins,branches,joins=static(prior)
    ledger=[]; inversions=[]; order_index={k:i for i,k in enumerate(k for k,*_ in SPEC if any(k in runs[s][1] for s in SIDES))}
    for i,f in enumerate(xml):
        code=f['field']; jo=joins.get(code); row=dict(xml_index=i,code=code,schema=f,status='unmapped',slot=None,lane=None,static=None)
        if jo:
            row.update(jo);k=jo['slot'];prof={}; row['status']='held'; reason=None
            if k:
                field=dict(f); er=f.get('enum_ref');field['_allowed']={int(v['enum']) for v in master['enums'][er]['values']} if er else set()
                for side in SIDES:
                    pp=profile(field,jo,raw[side,25],runs[side][1].get(k,[]),{t:keys[side,t] for t in IDS})
                    prof[side]=pp
                examined=[v for v in prof.values() if v['tested']]; ck(bool(examined),(code,'no samples on mapped slot'))
                passed=all(not p['violations'] and not p['hold_reason'] for p in examined)
                if passed:row['status']='L3'
                else:reason=next((q['first_counterexample']['reason'] for q in examined if 'first_counterexample' in q),'domain gate')
                row['execution_index']=order_index[k]
                row['domain_profiles']=prof
                if reason:row['first_counterexample']=next(p['first_counterexample'] for p in examined if 'first_counterexample' in p)
            else:
                reason={'not_read':'inline name selector never equals 4; even that reader arm transfers only COMP+0x48/+0x40, not +0x50',
                        'context_only':'getter enters rules/context path; no same COMP wire member proved'}[jo['format']]
                if jo['format']=='not_read':row['first_counterexample']=witness(0,28,b'\0',0,reason)
                else:row['first_counterexample']={'static_site':jo['static']['member_use'],'reason':reason,'at':None,'raw':None}
            if reason:row['hold_reason']=reason
        ledger.append(row)
    aligned=[r for r in ledger if r['slot'] is not None]
    for i,x in enumerate(aligned):
        for y in aligned[i+1:]:
            if x['execution_index']>y['execution_index']:
                inversions.append(dict(xml_pair=[x['xml_index'],y['xml_index']],codes=[x['code'],y['code']],execution_pair=[x['execution_index'],y['execution_index']]))
    status=hist(x['status'] for x in ledger); added=[r['code'] for r in ledger if r['status']=='L3' and r['origin']=='t59']
    assert sum(status.values())==255
    desc=[]; templates={s:[dict(rows=n,sequence=list(seq)) for seq,n in runs[s][2].most_common()] for s in SIDES}
    for k,a,w,m in SPEC:
        cells=runs['client'][1].get(k,[]); legacy_steps=[]
        if cells:
            _,p,span=cells[0]; rel=p-rr['client'][0][0]-1
            legacy_steps=[r['step'] for r in fixtures['complete_old_codec'] if r['legacy_body_offset']<rel+span and rel<r['legacy_body_offset']+r['width']]
        desc.append(dict(key=k,site=a,nominal_width=w,object_offset=m,execution_index=order_index.get(k),
            inner_sites=COLLECTIONS.get(k,[]),t01f_closed=[x for x,r in fixtures['accepted_client_slots'].items() if r['slot']==k],
            t01f_codec_steps=legacy_steps,xml_indices=[x['xml_index'] for x in aligned if x['slot']==k],
            profiles={s:describe(raw[s,25],runs[s][1].get(k,[]),rr[s]) for s in SIDES}))
    for s in SIDES:ck(sum(z['profiles'][s]['bytes'] for z in desc)==env[s]['rows'],(s,'slot bytes cover all rows'))
    emit('field_slots.json',dict(status='dual_archive_outer_replay_closed',L4=0,source=prov,frozen=frozen,archives=archives_info,target_identity_domains=targets,
        envelopes=env,framing_sensitivity=sensitivity,framing_options={k:[h,f,t,sorted(m) if m is not None else None,z,i] for k,(h,f,t,m,z,i) in OPTIONS.items()},
        execution_templates=templates,slots=desc,external_modes=modes,axes={'native':'selector at row start','legacy_body':'native row start+1',
            'trace':'coordinates are [ordinal, absolute payload offset, span], hashed as LE u32 triples; no selector lookahead assigned to body'}))
    emit('field_map.json',dict(status='partial_schema_join',L4=0,scope='comp.xml#comp top level only',count=255,summary=status,aligned=len(aligned),new_L3=added,
        inversions=inversions,fields=ledger,fixtures=fixtures,boundaries=['no subtable semantics','no club/nation field changes','no CLUB_LINK',
              'unmapped does not imply absent','L3 concerns wire projection, not runtime or editor write behaviour']))
    chunks('instructions',ins,600);chunks('branches',branches,150)
    print(f't59 PASS: {N} + {N} rows; {len(desc)} possible outer sites ({len(order_index)} observed); {len(ins)} instructions / {len(branches)} branches; {status}; new L3 {added}')


def selftest():
    raw=(b'\0'*8+S.pack('<I',2)+b'\0'+S.pack('<III',0,11,11)+b'\0'+S.pack('<III',1,12,12)+FOOT)
    grp=candidates(raw)
    assert path_count(raw,grp,13,9,12,{0},True,True,True)[1]==[13,26]
    assert path_count(raw,grp,13,8,13,{0},True,True)[0]['paths']==1
    assert path_count(raw,grp,13,8,12,{0},True,True)[0]['paths']==0
    p=profile({'min_value':'1','max_value':'20'},dict(format='level',arg=None,lane=0,slot='m1a2'),b'\0\x64\x14',[(0,0,1),(1,1,1),(2,2,1)],{})
    assert p['violations']==1 and p['null_or_suppressed']==1 and p['first_counterexample']['row']==2
    print('t59 builder selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__);g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--build',action='store_true',help='write only scratch/t59/out JSON artifacts');g.add_argument('--selftest',action='store_true',help='exercise framing and domain negative controls');a=ap.parse_args()
    try:
        sys.path.append(str(ROOT.parent/'fm24/tools/python'))
        selftest() if a.selftest else build()
        return 0
    except (Check,AssertionError) as e:print('FAIL:',e,file=sys.stderr);return 1
    except Exception as e:print('ERROR:',type(e).__name__,e,file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())



