"""t57: bounded Club table_3 identity census, reader replay and frozen schema join."""
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
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t57/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
LOC = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
BIG = 'evidence/fm24/reports/dbdat_decode/db_tables_big.json'
BIGMD = 'evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md'
HEAD = bytes.fromhex('03017461642ef10d')
FOOT = bytes.fromhex('0000000001e3c03a77')
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
SIDES = ('client','server')
IDS = (2,3,10,21,25)
PRIOR = ('scratch/t24/out/cursor.json','scratch/t39/out/REPORT.md','scratch/t44/out/discovery_cafl_cvfl.json',
         'reports/club_nation_subtable_schema.json','scratch/t01/inbox/t01f/output.json','reports/t01f_comp_row_offsets.json')
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
        for tid in (*IDS,*(['extra_3'] if side=='client' else [])):
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
        both_relaxed=(13,8,13,{0,12},False,False),wire_triple=(13,9,12,{0,12},True,True),
        triple_no_lookahead=(13,9,12,None,True,True))
    result={}; chosen=None
    for key,args in opts.items():
        ans,at=path_count(b,groups,*args,recover=key=='wire_triple'); result[key]=ans
        if at is not None: chosen=at
    result.update(count=n,candidate_histogram=hist(map(len,groups)),cap=CAP)
    return result,chosen

# Logical outer positions, in execution sequence (not sorted by address). A count and
# its opaque item payload occupy one outer span. Width=prefix width for such spans.
# key / site / type / width / object displacement; displacements on base helper still use CLUB this.
PRE=[('selector',0xf2ba0e,'selector',1,None),('derived_170',0x43bebef,'raw32',4,0x170),('derived_178',0x43bec0e,'raw8',1,0x178),
     ('ref_d8',0xe5a81a,'ordinal_u32',4,0xd8),('ref_e0',0xe5a843,'raw32',4,0xe0),('ref_e8',0xe5a877,'ordinal_u32',4,0xe8),
     ('ref_f0',0xe5a8a0,'ordinal_u32',4,0xf0),('ref_f8',0xe5a8cd,'ordinal_u32',4,0xf8),('flags160',0xe5a92a,'bit_block',6,0x160),
     ('name_len',0x35b0828,'string_length',4,0xc0),('name_bytes',0x35b0883,'utf8',None,0xc0),
     ('short_len',0x35b0828,'string_length',4,0xc8),('short_bytes',0x35b0883,'utf8',None,0xc8)]
EXT=[('raw16a',0xe5aa3e,'raw8',1,0x16a),('raw166',0xe5aa7c,'raw16',2,0x166),('person148',0xe5aaab,'raw32',4,0x148),
     ('raw16c',0xe5aae3,'raw8',1,0x16c),('vec110',0xe5ab0a,'count_i8',1,0x110),('obj150_tag',0xe5ada9,'tag_i8',1,0x150),
     ('obj150',0xe5aef1,'opaque_subobject',45,0x150),('vec130',0xe5af76,'count_i8',1,0x130),('vec138',0xe5b661,'count_i8',1,0x138),
     ('raw168',0xe5bc1f,'raw16',2,0x168),('stad140',0xe5bc6b,'ordinal_u32',4,0x140)]
BASE=[('base_ba',0x3fc2050,'raw8',1,0xba),('base_b8',0x11d0f6f,'bit_block',2,0xb8)]
BC=[('base18',0x11d10e0,'count_u8',1,0x18),('base30',0x11d139d,'count_u8',1,0x30),('base60',0x11d15c5,'count_i8',1,0x60),
    ('base78',0x11d177b,'count_i8',1,0x78),('base90',0x11d193b,'count_u8',1,0x90),('base48',0x11d1b03,'count_u8',1,0x48),
    ('basea8',0x11d1bf2,'count_i16',2,0xa8)]
SPEC=PRE+EXT+BASE+BC+[('identity',0x11d21df,'identity',12,8)]
SPEC_BY={s[0]:s for s in SPEC}
COL={k:(w, sites) for k,w,sites in [
    ('vec110',4,[0xe5ad2b,0xe5ad69]),('vec130',24,[0xe5b25d,0xe5b27f,0xe5b2a8,0xe5b2ea,0xe5b323,0xe5b345,0xe5b367,0xe5b389,0xe5b3ab,0xe5b3cd,0xe5b3f1]),
    ('vec138',12,[0xe5b8ef,0xe5b911,0xe5b93a,0xe5b983]),
    ('base18',4,[0x11d1344,0x11d137f,0x3fc2050]),('base30',4,[0x11d1564,0x11d15a3,0x3fc2050]),
    ('base60',4,[0x11d1725,0x11d1759,0x3fc2050]),('base78',4,[0x11d18e5,0x11d1919,0x3fc2050]),
    ('base90',4,[0x11d1ab7,0x11d1ae5,0x3fc2050]),('base48',16,[0x11d1b91,0x11d1bcb,0x3fc2050]),
    ('basea8',28,[0x11d1e65,0x11d1e86,0x11d1eb0,0x11d1ef4,0x11d1f1e,0x39dd7d4,0x11d1f68,0x11d1f8c]) ]}


def replay(b, mode):
    p=13; limit=len(b)-9; rows=[]; book=defaultdict(list); order=Counter(); uids=set()
    ck(b[:8]==HEAD and mode in (0,1) and len(b)>=22,'header/mode')
    for i in range(U(b,8)):
        start=p; row=[]
        def cut(key,w=None,extra=0):
            nonlocal p
            if w is None: w=SPEC_BY[key][3]
            a=p; p+=w+extra
            if w<0 or p>limit: raise Check(f'row {i} @{a} {key} short span {w+extra}')
            row.append(key); book[key].append((i,a,w+extra)); return a
        def coll(key):
            nwidth=SPEC_BY[key][3]
            n=int.from_bytes(b[p:p+nwidth],'little',signed=SPEC_BY[key][2]!='count_u8')
            if n<0: raise Check(f'row {i} @{p} {key} unobserved negative count {n}')
            cut(key,nwidth,n*COL[key][0]); return n
        sel=b[cut('selector')]; ck(sel in (0,12),f'row {i} @{start}: selector {sel}')
        if sel==12: cut('derived_170');cut('derived_178')
        for k,*_ in PRE[3:9]: cut(k)
        for k in ('name','short'):
            n=U(b,cut(k+'_len'))
            if n: cut(k+'_bytes',n)
        if mode:
            for k,*_ in EXT[:4]:cut(k)
            coll('vec110')
            tag=b[cut('obj150_tag')]
            if tag==0:cut('obj150')
            elif tag!=2:raise Check(f'row {i} @{p-1} unobserved tag {tag}')
            coll('vec130');coll('vec138');cut('raw168');cut('stad140')
        cut('base_ba');cut('base_b8')
        if mode:
            for k,*_ in BC:coll(k)
        a=cut('identity'); ordinal,u,v=S.unpack_from('<III',b,a)
        ck(ordinal==i and u==v and u and u not in uids,f'row {i} @{a} bad identity {(ordinal,u,v)}')
        uids.add(u); rows.append((start,p,u,sel)); order[tuple(row)]+=1
    ck(b[p:]==FOOT,f'footer @{p}: {b[p:p+9].hex()} (EOF {len(b)})')
    return rows,book,order


def target_domains(raw, main):
    all_t={}; note={s:{} for s in SIDES}
    for t in IDS:
        for side in SIDES:
            b=raw[side,t]; n=U(b,8); end=len(b)-9
            if t==3: ats=[r[1]-12 for r in main[side]]; m='main replay'
            elif t in (2,21) or (t==25 and side=='client'):
                w={2:43,21:38 if side=='client' else 181,25:127}[t]
                ck(end==13+n*w,(side,t,'target fixed EOF')); ats=[13+w*(i+1)-12 for i in range(n)]; m=f'fixed {w} B identity tails'
            else:
                if t==10:
                    # Revalidate previously accepted nation identities against current archive bytes; no nation field parsing.
                    ref=J('scratch/t47/out/cursor_nation_tax.json')[side]
                    ck(H(b)==ref['payload_sha256'] and len(ref['rows'])==n,(side,t,'t47 payload'))
                    ats=[r['identity_at'] for r in ref['rows']]; m='t47 coordinates, raw identities rechecked'
                else:
                    triples=all_t['client',25]; ats=[]; p=13
                    for i,u in triples.items():
                        q=b.find(S.pack('<III',i,u,u),p,end); ck(q>=0,(side,t,i,'target triple')); ats.append(q);p=q+12
                    p=end
                    for (i,u),a in zip(reversed(triples.items()),reversed(ats),strict=True):
                        p=b.rfind(S.pack('<III',i,u,u),13,p); ck(p==a,(side,t,i,'target ambiguity'))
                    m='ordered client exact triples, earliest=latest'
            ck(len(ats)==n and ats[-1]+12==end and b[end:end+5]==b'\0'*4+b'\1',(side,t,'target framing'))
            keys={}; traces=bytearray()
            for i,a in enumerate(ats):
                j,u,v=S.unpack_from('<III',b,a); ck(j==i and u==v and u,(side,t,i,a,'target identity'))
                keys[i]=u; traces.extend(b[a:a+12])
            ck(len(set(keys.values()))==n,(side,t,'target unique UID'))
            all_t[side,t]=keys; note[side][str(t)]=dict(method=m,count=n,identity_sha256=H(traces),first=[0,keys[0]],last=[n-1,keys[n-1]])
    return all_t,note

# 4CC, exact compare, member-use evidence, outer site, relative lane, format, argument.
JOINS=[('Cnti',0xe8af47,0xe8af53,'ref_d8',0,'ref',10),('Cbni',0xe8b7a7,0xe8e3d3,'ref_e8',0,'ref',10),
       ('Cccn',0xe8b7bf,0xe8b7cb,'ref_f0',0,'ref',10),('Ccty',0xe8c22c,0xe8e566,'ref_f8',0,'ref',2),
       ('Csot',0xe8b1cc,0xe8b1d8,'flags160',0,'bit',2),('CASt',0xe8c9a8,0xe8c9b4,'flags160',1,'bit',1),
       ('CnCV',0xe8cded,0xe8cdf9,'flags160',3,'bit',1),('CIns',0xe8afac,0xe8dc37,'flags160',1,'bit',4),
       ('Cext',0xe8c8ef,0xe8d972,'ref_d8',0,'null_bool',10),('Cprs',0xe8c48d,0xe8d46f,'raw16a',0,'enum_i8',None),
       ('Ctsi',0xe8c57d,0xe8c589,'stad140',0,'ref',21),('Cdof',0xe8b17c,0xe8b188,'person148',0,'unvalidated_ref',None),
       ('Csnm',0xe8a451,0xe8a460,'short_bytes',0,'str',None),('Cnam',0xe8bc91,0xe8e8f2,'name_bytes',0,'proxy_str',None),
       ('Cncl',0xe8ab01,0xe8d39d,'base48',0,'link',0x37),('Cedp',0xe8c3b2,0xe8c3c1,'base48',0,'link_bool',0x6f),
       ('PLgn',None,0x11f0756,'base_b8',1,'enum_i8',None),('duni',None,0xfe3bff,'identity',4,'uid',None)]


def static():
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    pe=PE(EXE); ck(H(pe.raw)==EXEH,'editor SHA'); pe.pe.parse_data_directories(directories=[3])
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    def ins(o): return next(md.disasm(pe.raw[o:o+15],pe.f2va(o),1))
    def blob(o,w): return dict(file_offset=o,VA=pe.f2va(o),bytes=pe.raw[o:o+w].hex())
    def tgt(i): return pe.va2f(i.operands[0].imm) if i.operands and i.operands[0].type==X86_OP_IMM else None
    def rip(o):
        i=ins(o); return i.address+i.size+i.operands[1].mem.disp
    def row(o,i):
        d=dict(blob(o,i.size),instruction=(i.mnemonic+' '+i.op_str).strip());
        if i.mnemonic.startswith('j') or i.mnemonic=='call':d['direct_target']=tgt(i)
        return d
    roots=(0xe5a7a0,0x43beba0,0x35b07f0,0x3fc2030,0x11d0d30,0x423fef0,0x39dd7b0)
    records={};branches=[];extents={}; all_main=set()
    wr={0xe5a900,0x11d0dac,0x11d0f47,0x11d221a,0xe5ab17,0xe5acb7,0xe5acfd,0xe5adcb,0xe5add3,0xe5af99,
        0xe5b578,0xe5b682,0xe5b810,0xe5b854,0x35b0835,0x35b0847,0x11d15d1,0x11d1787,0x11d1947,0x11d1b0f,0x11d1bfc}
    io={0xe5a95b,0xe5a9a8,0xe5aef6,0xe5bcae,0x35b083f,0x11d1f4e}
    for root in roots:
        g=ReaderCFG(pe,md,root); m={pe.va2f(a):i for a,i in g.instructions.items()}
        prev={o+i.size:(o,i) for o,i in m.items()}; direct=[]; bc=0
        for o,i in sorted(m.items()):
            successors=[pe.va2f(v) for v in g.successors[i.address]]
            records[o]=dict(row(o,i),function=root,successors=successors)
            if i.mnemonic=='call' and i.operands[0].type==X86_OP_MEM and i.operands[0].mem.disp==0x28:direct.append(o)
            if not i.mnemonic.startswith('j') or i.mnemonic=='jmp':continue
            bc+=1;k=o; pred=None
            for _ in range(6):
                if k not in prev:break
                k,q=prev[k]
                if q.mnemonic.startswith(('j','call')):break
                if q.eflags:pred=k;break
            cls=('wire_data_or_version' if o in wr else 'runtime_external' if o in (0xe5a9ba,0x11d0fa4,0xe5bc3c) else
                 'IO_result' if o in io or tgt(i)==0xe5bb94 else 'unresolved_or_lifecycle')
            branches.append(dict(site=o,function=root,taken=tgt(i),fallthrough=o+i.size,predicate=pred,
                predicate_instruction=row(pred,m[pred])['instruction'] if pred is not None else None,classification=cls))
        extents[str(root)]=dict(begin=root,VA=pe.f2va(root),end_exclusive=g.function_end_off,reachable=len(m),conditional=bc,
                                external_edges=g.external_edges,direct_stream_reads=direct)
        if root==roots[0]:all_main=set(direct)
    uses={
      'read_scalar_or_count':[0xe5a81a,0xe5a843,0xe5a877,0xe5a8a0,0xe5a8cd,0xe5a92a,0xe5aa3e,0xe5aa7c,0xe5aaab,0xe5aae3,0xe5ada9,0xe5af76,0xe5b661,0xe5bc1f,0xe5bc6b,0xe5bccc],
      'collection_item_or_terminal_flush':[0xe5ad2b,0xe5ad69,*COL['vec130'][1],*COL['vec138'][1]],
      'alternate_or_no_pending_width_under_modern_success':[0xe5a976,0xe5a9ea,0xe5aec6,0xe5af45,0xe5b22f,0xe5b618,0xe5b8c1,0xe5bbcd]}
    ck(set(sum(uses.values(),[]))==all_main and sum(map(len,uses.values()))==len(all_main),'direct read accounting')
    def add(*xs):
        for o in xs:
            if o not in records: records[o]=row(o,ins(o))
    add(0xf48b41,0xf48b4c,0xf48b53,0xf48daf,0xf48db2,0xf48dc3,0xf48dc8,0xf48dcf,0xf49c3f,0x3aad0fd,0x157cff0,
        0xf2ba0e,0xf2ba23,0xf2ba38,0xf2ba4b,0xf2ba51,0xf2ba7f,0xffa602,0xf2baa2,0xf2bac2,
        0x814110,0x12e66a0,0xdb7f80,0x1476470,0x147620e,0x1476760,0xe5c626,0xe5c633,0xe5c638,0xe5c675,
        0xe5c599,0xe5c5b9,0xe5c5d9,0xe5c5f9,0xe5c619,0xe5caa5,0xe5caaa,0xe5cae1,0xe5cae6,
        0x11d2a76,0x11d2a9c,0x11d2aa9,0x110586b,0x1105881,0x1105888,0x110588c,0x110588f,0x110589d,0x11058a1,0x11058a6,0x11058b4,0x11058b9,0x11059e6,
        0xf7e440,0x3bf348e,0x3bf34b2,0x3bf34b4,0x3bf34c7,0x3bf350e,0x3bf3512,0x434e64c,0x434e664,
        0x110593a,0x1105942,0x110595e,0x110596c,0x11059df,0x11d2aae,0x11d2ad5,0x11d2ada,
        0xe8f51d,0x11f06fe,0x11f0704,0x11f0756,0x11f2a98,0x11f2aba,0x11f4550,0xfe3912,0xfe3918,0xfe3bff,
        0xe8e6a9,0xe8e6b1,0xe8e6ba,0xe8afb8,0xe8afc4,0xe8dc81,0xe8afd9,0xe8b939,0xe8b945,0xe8b955,0xe8b961,0xe8b96e,0xe8be31,0xe8ea2e,0xe8ea47,
        0xe8b1e9,0xe8b1eb,0xe8c9c5,0xe8ce0a,0xe8dc48,0xe8dc4b,0xe8d97f,0xe8d982,
        0x3ae4a55,0x3ae4a80,0x3ae4a96,0x3ae4a9c,0xe74ff0,0xe63110,0x3ac1f90,0x3ac1fc0,0x3ac1fd2)
    vt=0x14187cd08; dvt=rip(0xf48dc8)
    def vslot(va,j,target):
        a=pe.va2f(va)+j*8; ck(pe.va2f(S.unpack_from('<Q',pe.raw,a)[0])==target,('slot',va,j)); return blob(a,8)
    def rtti(va,cls):
        a=pe.va2f(va); col=pe.va2f(S.unpack_from('<Q',pe.raw,a-8)[0]); rva=U(pe.raw,col+12)
        td=pe.va2f(pe.pe.OPTIONAL_HEADER.ImageBase+rva); name=f'.?AV{cls}@db@@'.encode()+b'\0'
        ck(pe.raw[td+16:td+16+len(name)]==name,('RTTI',cls)); return dict(col=blob(col,24),name=blob(td+16,len(name)))
    factory=0xf49d38; cell=factory+12
    ck(pe.va2f(pe.f2va(factory)+S.unpack_from('<i',pe.raw,cell)[0])==0xf48daf,'factory case 3')
    ck(rip(0x3aad0fd)==vt and tgt(ins(0xf48dc3))==0xe59a40 and tgt(ins(0xf49c3f))==0xe59a40,'factory constructors')
    csv={str(j):vslot(vt,j,a) for j,a in [(2,0xe89a00),(19,0xe5a7a0),(20,0xe5c550),(21,0xe5ca50)]}
    dv=vslot(dvt,19,0x157cff0); ck(tgt(ins(0x157cff0))==0x43beba0,'derived thunk')
    g=ReaderCFG(pe,md,0xe89a00); ev={}
    for k,cmp,o,slot,lane,typ,arg in JOINS:
        if cmp is None:
            ev[k]=dict(bridge='t24 inherited getter and base serializer',member_use=o); continue
        q=ins(cmp); eq=ins(cmp+q.size)
        ck(q.address in g.instructions and q.mnemonic=='cmp' and len(q.operands)>1 and q.operands[1].type==X86_OP_IMM and
           q.operands[1].imm==int.from_bytes(k.encode(),'big') and eq.mnemonic in ('je','jne'),(k,'exact reachable compare'))
        start=eq.operands[0].imm if eq.mnemonic=='je' else eq.address+eq.size
        queue=deque([(start,[])]); seen={start}
        while queue:
            a,path=queue.popleft(); path=path+[pe.va2f(a)]
            if a==pe.f2va(o):break
            for b in g.successors.get(a,[]):
                if b not in seen:queue.append((b,path));seen.add(b)
        else:raise Check((k,'equal getter arm not reachable',hex(o)))
        add(cmp,pe.va2f(eq.address),*path)
        if typ in ('ref','null_bool','bit','unvalidated_ref','enum_i8'):
            base=SPEC_BY[slot][4]; i=ins(o); m=i.operands[1].mem
            ck(i.operands[1].type==X86_OP_MEM and md.reg_name(m.base)=='r12' and m.disp==(base+lane if k!='CIns' else base), (k,'same this member'))
        ev[k]=dict(compare=cmp,branch=pe.va2f(eq.address),equal_path=path,member_use=o)
    base_fix=pe.va2f(rip(0x1105881)); type_one=base_fix+4
    ck(pe.va2f(pe.f2va(base_fix)+S.unpack_from('<i',pe.raw,type_one)[0])==0x110589d and
       tgt(ins(0x11058b4))==tgt(ins(0x434e664))==0xf7e440 and tgt(ins(0xf7e440))==0x3bf3460 and
       ins(0x110589d).op_str=='r8, qword ptr [rsi + 0x10]' and ins(0x434e64c).op_str=='r8, qword ptr [r12 + 0x10]', 'Cncl target context family')
    ev['Cncl'].update(item_count_site=0x11d1b03,item_stride=16,ref_lane=0,item_type_byte=10,item_selector_byte=11,
        item_type=1,item_selector=0x37,base_fixup_call=0x11d2aa9,type_case_table=base_fix,type_case_1=blob(type_one,4),
        type_case_1_target=0x110589d,club_context_displacement=0x10,fixup_call=0x11058b4,reference_t44_context_use=0x434e64c,
        raw_ordinal_load=0x3bf34b2,note='runtime flags and remap retained; absence when no kind 0x37 / wrong type or null pointer')
    ev['Cedp'].update(item_count_site=0x11d1b03,item_stride=16,item_selector_byte=11,item_selector=0x6f,
        value_byte=12,true_when=3,helper=0x3ac1f90,compare_tag=0x3ac1fc0,compare_value=0x3ac1fd2,
        scope='wire projection of matching item; no claim on runtime retention/Team pointer')
    prov=dict(editor=str(EXE),editor_sha256=EXEH,factory_3=dict(cell=blob(cell,4),base=factory,arm=0xf48daf),
        CLUB=dict(vtable=vt,rtti=rtti(vt,'CLUB'),slots=csv),LEAGUE_BODY_CLUB=dict(vtable=dvt,rtti=rtti(dvt,'LEAGUE_BODY_CLUB'),slot19=dv),
        tag_vcall={'0':vslot(rip(0xe5ae12),4,0x1476470),'1_unobserved':vslot(rip(0x147620e),4,0x1476760)},
        runtime_function_extents=extents,club_direct_transfer_accounting=uses)
    return prov, sorted(records.values(),key=lambda r:r['file_offset']),branches,ev


def point(b,cell,val):
    i,a,w=cell; return dict(row=i,absolute=a,raw=b[a:a+w].hex(),value=val)


def describe_slot(side,b,cells,key):
    if not cells: return dict(rows=0,status='bypassed')
    hh=sha256(); counts=Counter(); vals=Counter()
    for i,a,w in cells:
        hh.update(S.pack('<III',i,a,w))
        if key in COL: counts[(w-SPEC_BY[key][3])//COL[key][0]]+=1
        elif SPEC_BY[key][3] is not None and w<=6: vals[int.from_bytes(b[a:a+w],'little')]+=1
    f=dict(rows=len(cells),bytes=sum(c[2] for c in cells),width_range=[min(c[2] for c in cells),max(c[2] for c in cells)],
           coordinate_sha256=hh.hexdigest(),first=dict(row=cells[0][0],absolute=cells[0][1],width=cells[0][2],raw_prefix=b[cells[0][1]:cells[0][1]+min(cells[0][2],64)].hex()),last=list(cells[-1]))
    if counts:f.update(item_counts=dict(sorted(counts.items())),items=sum(n*c for n,c in counts.items()))
    if vals:f.update(unsigned_min=min(vals),unsigned_max=max(vals),distinct=len(vals),histogram=dict(sorted(vals.items())) if len(vals)<=32 else None)
    return f


def domain(field,join,b,book,keys,side,rows,master):
    code,_,_,slot,lane,kind,arg=join; cells=book.get(slot,[])
    if kind in ('str','proxy_str'):
        lengths=book[slot.replace('_bytes','_len')]; offsets={i:(a,w) for i,a,w in cells}
        cells=[(i,*offsets.get(i,(a+4,0))) for i,a,_ in lengths]
    if not cells:return dict(rows=0,status='bypassed')
    specs={'bit':1,'enum_i8':1,'ref':4,'null_bool':4,'unvalidated_ref':4,'uid':4}
    if kind in specs:cells=[(i,a+lane,specs[kind]) for i,a,w in cells]
    def raw(c, signed=False):return int.from_bytes(b[c[1]:c[1]+c[2]],'little',signed=signed)
    values=[]; first_invalid=None
    if kind in ('str','proxy_str'):
        for c in cells:
            i,a,w=c
            try: s=b[a:a+w].decode('utf-8'); values.append(len(s))
            except UnicodeDecodeError:
                if first_invalid is None:first_invalid=point(b,c,None)
                values.append(-1)
    elif kind in ('link','link_bool'):
        multiple=0; tag_types=Counter(); first_live_tag=None
        for i,a,w in cells:
            tagged=[o for o in range(a+1,a+w,16) if b[o+11]==arg]
            multiple+=len(tagged)>1
            if tagged:tag_types[b[tagged[0]+10]]+=1
            if kind=='link':
                if tagged and b[tagged[0]+10]==1:
                    p=tagged[0]; values.append(U(b,p))
                    if first_live_tag is None:first_live_tag=point(b,(i,p,16),U(b,p))
                else:values.append(0xffffffff)
            else:
                on=bool(tagged and b[tagged[0]+12]==3); values.append(int(on))
                if on and first_live_tag is None:first_live_tag=point(b,(i,tagged[0],16),1)
    else:values=[raw(c,kind=='enum_i8') for c in cells]
    def witness(i,v):return point(b,cells[i],v)
    vals=Counter(values); result=dict(rows=len(values),min=min(vals),max=max(vals),distinct=len(vals),first=witness(0,values[0]))
    if len(vals)<=32:result['hist']=dict(sorted(vals.items()))
    def hold(reason,idx=0):result.update(domain='held',reason=reason,first_counterexample=witness(idx,values[idx]))
    if kind in ('ref','null_bool','link'):
        t=keys[side,3 if kind=='link' else arg]; uids=set(t.values()); live=0; nulls=0; bad=[]; wrong=0; first_wrong=None; first_live=None; first_null=None
        for j,v in enumerate(values):
            if v==0xffffffff:
                nulls+=1
                if first_null is None:first_null=witness(j,v)
            elif v in t:
                live+=1
                if first_live is None:first_live=dict(witness(j,v),target_uid=t[v])
            else:bad.append(j)
            if v!=0xffffffff:
                wrong+=v in uids
                if v not in uids and first_wrong is None:first_wrong=witness(j,v)
        result.update(hit=live,miss=len(bad),null=nulls,wrong_uid_hit=wrong,first_wrong_uid_miss=first_wrong,first_live=first_live,first_null=first_null)
        if bad:hold('live ordinal absent from actual target; no sentinel invented',bad[0])
        elif kind=='link':
            result.update(records_with_multiple_tags=multiple,type_when_tagged=dict(tag_types),first_live_item=first_live_tag)
            if not live:hold('no live tagged item')
            elif multiple or set(tag_types)!={1}:
                bad_tag=next(j for j,(_,a,w) in enumerate(cells) if (hits:=[o for o in range(a+1,a+w,16) if b[o+11]==arg]) and (len(hits)>1 or b[hits[0]+10]!=1))
                hold('multi-tag or non-type-1 item needs runtime removal/order analysis',bad_tag)
            else:result['domain']='pass'
        elif not live or (nulls and field.get('is_optional')!='true' and kind!='null_bool'):hold('no qualifying live domain or required-null conflict')
        else:
            result['domain']='pass'
            if kind=='null_bool':result['decoded']={0:live,1:nulls}
    elif kind=='bit':
        result.update(mask=arg,decoded=hist(int(bool(v&arg)) for v in values),domain='pass')
    elif kind=='link_bool':
        result.update(records_with_multiple_tags=multiple,type_when_tagged=dict(tag_types),decoded=hist(values),first_true_item=first_live_tag)
        result['domain']='pass'
    elif kind=='enum_i8':
        er=field.get('enum_ref'); ck(not er,(code,'add scoped enum_ref decoder'))
        hold('no scoped enum_ref; case/control bytes are not labels')
    elif kind=='uid':
        ck(all(values[k]==r[2] for k,r in enumerate(rows)),(side,code,'identity'))
        result['domain']='pass'
    elif kind=='unvalidated_ref':hold('person target not in this task; no target census or naming promotion')
    else:
        maximum=int(field['max_length']) if 'max_length' in field else None
        bad=[j for j,n in enumerate(values) if maximum is not None and n>maximum]
        result.update(max_chars=maximum,max_bytes=max(c[2] for c in cells),empty=vals[0],violations=len(bad),invalid_utf8=first_invalid)
        if first_invalid:hold('invalid UTF-8',first_invalid['row'])
        elif bad:hold('stored text exceeds XML max_length in Unicode code points',bad[0])
        elif kind=='proxy_str':hold('localized getter route is not equated to the backing string')
        else:result['domain']='pass'
    return result


def regression(raw,rows,books,targets,big):
    v=big['tables']; note={'city':{},'stadium':{},'old_owner':[],'city_joins':[]}
    for code in (2,3,21):
        for side in SIDES:
            digest=v[str(code)]['source_payload_sha256']; ck(H(raw[side,code])==(digest[side] if isinstance(digest,dict) else digest),(side,code,'frozen snapshot payload'))
    for f in v['2']['named_anchor_checks']:
        o=f['row_index']; a=14+o*43; b=raw['client',2]; ll=S.unpack_from('<ff',b,a+1)
        ck(b[a+10]==f['nation_row_ordinal'] and targets['client',2][o]==f['duni_dbid'] and
           all(abs(x-y)<0.000002 for x,y in zip(ll,f['coordinates_approx'],strict=True)),('city anchor',f))
        note['city'][f['city']]=[o,f['duni_dbid'],list(ll),b[a+10]]
    b=raw['server',21]
    for f in v['21']['landmark_cross_checks']:
        i=f['row_index']; a=14+181*i; loc=S.unpack_from('<ff',b,a+160); caps=list(S.unpack_from('<II',b,a))
        ck(targets['server',21][i]==f['dbid'] and list(loc)==f['coordinates_f32_at_160_164'] and U(b,a+146)==f['city_reference_candidate_rdui_at_146'] and
           caps==[f['server_row_capacity_candidate_u32_at_0'],f['server_row_seating_capacity_candidate_u32_at_4']],('stadium anchor',f))
        note['stadium'][str(i)]=dict(uid=f['dbid'],coordinates=list(loc),capacity_and_seats=caps,city_ordinal=U(b,a+146),public_capacity=f['public_capacity'])
    for f in v['21']['owner_cross_checks']:
        i=f['stadium_row_index']; o=U(b,14+181*i+16)
        ck(o==f['candidate_table3_order_index']==f['server_row_u32_at_16'],('stadium owner',f));note['old_owner'].append([i,o,rows['server'][o][2]])
    t3=v['3']['field_validation']
    for f in t3['Ccty_named_city_checks']:
        i=f['candidate_order_index']; o=f.get('city_rdui_candidate')
        if o is None: o=f.get('city_ref_rdui')
        ck(o is not None,('frozen city check keys',f))
        if f['club']=='Shanghai Port':
            matches=[j for j,a,w in books['client']['name_bytes'] if raw['client',3][a:a+w]==b'Shanghai Port']
            ck(len(matches)==1,('Shanghai full-name identity',matches)); actual=matches[0]
            c=books['client']['ref_f8'][i]; note['legacy_Shanghai_index_correction']=dict(frozen_index=i,frozen_expected=o,
                old_position=point(raw['client',3],c,U(raw['client',3],c[1])),same_name_ordinal=actual)
            i=actual
        for side in SIDES:
            c=books[side]['ref_f8'][i]; ck(c[0]==i and U(raw[side,3],c[1])==o,(side,i,'club city anchor'))
        note['city_joins'].append([i,o])
    note['short_names']=[]; note['nation_refs']=[]
    for f in t3['Csnm_language_checks']:
        i=f['candidate_order_index']; short=f['inline_second_string']
        for side in SIDES:
            a=books[side]['short_len'][i][1]; b=raw[side,3]
            ck(b[a+4:a+4+U(b,a)].decode('utf-8','replace')==short,(side,i,'short name fixture'))
        note['short_names'].append([i,short])
    for f in t3['nation_reference_checks']:
        i=f['candidate_order_index']; expect=f['observed_ordinals']
        for side in SIDES:
            b=raw[side,3]; ck([U(b,books[side][k][i][1]) for k in ('ref_d8','ref_e8','ref_f0')]==expect,(side,i,'nation fixture'))
        note['nation_refs'].append([i,expect])
    ck(all(rows[s][460][2]==676 and U(raw[s,3],books[s]['ref_d8'][460][1])==139 and U(raw[s,3],books[s]['ref_f8'][460][1])==1061 for s in SIDES),'Liverpool club/city/nation')
    x=raw['client','extra_3']; ck(H(x)==v['extra_3']['source_payload_sha256']['client'],'year fixture sidecar SHA')
    expected={f['candidate_order_index']:f for f in t3['Cyfn_named_year_checks']}; p=12; years=[]
    for i in range(max(expected)+1):
        tag=S.pack('<I',i); a=x.find(tag,p)
        while a>=0:
            year=S.unpack_from('<H',x,a+4)[0]
            if year==0 or 1800<=year<=2100:break
            a=x.find(tag,a+1)
        ck(a>=0,('accepted extra_3 fixture rule',i)); p=a+6
        if i in expected:
            f=expected[i]; ck(year==f['client_extra_3_u16_at_row_plus_4'],('year',i,a,year))
            years.append(dict(row=i,club=f['club'],absolute=a+4,year=year,external_year=f['external_year_anchor'],note=f['note']))
    note['founded_year_fixture_only']=years
    note['original_Cccn_negative']=J(PRIOR[0])['controls']['E60_original']
    note['frozen_club_negatives']=v['3']['negative_results']; note['frozen_stadium_negatives']=v['21']['negative_results']
    pin=J(PRIOR[4])['verification']; probes=[x['cnti'] for x in pin['continent_and_nation_named_anchors'] if x['row_index'] in (7,250)]
    parents=pin['cpcm_named_anchors']; probes.extend(x['child_cpcm'] for x in parents)
    note['t01f']={x['payload_offset']:U(bytes.fromhex(x['bytes'])) for x in probes}
    ck(note['t01f']=={'0x3bf':139,'0x7c4c':55,'0x15f0b':352,'0x15f8a':352} and len(parents)==2 and all(S.unpack('<III',bytes.fromhex(x['parent_identity']['bytes']))==(352,150990,150990) for x in parents),'t01f accepted fixtures')
    ck(all(targets[s,10][139]==765 and targets[s,10][55]==110 and targets[s,25][352]==150990 for s in SIDES),'accepted identities')
    comp=raw['client',25]
    for k,y in note['t01f'].items():ck(U(comp,int(k,16))==y,(k,'t01f raw comp witness'))
    return note


def build():
    manifest={r['path']:r['sha256'] for r in J('evidence/MANIFEST.json')['files']}
    for path in (MASTER,LOC,BIG,BIGMD):ck(H((ROOT/path).read_bytes())==manifest[path],('manifest',path))
    ck(manifest[MASTER]==MASTERH and EXEH in (ROOT/LOC).read_text(encoding='utf-8'),'frozen anchors')
    master=J(MASTER); xml=master['entities']['club.xml'][0]['fields']; ck(len(xml)==433,'433 occurrences')
    by_code=defaultdict(list)
    for i,f in enumerate(xml):by_code[f['field']].append(i)
    raw,archive=archives(); frames={}; rows={}; books={}; envelope={}; paths={}; bad_mode={}
    for side in SIDES:
        b=raw[side,3]; mode=int(side=='server'); f,at=framing(b); frames[side]=f
        print(side,'data-only candidates',f['wire_triple'],flush=True)
        rr,bk,pp=replay(b,mode); rows[side]=rr; books[side]=bk; paths[side]=pp
        ck(len(rr)==84259 and (at is None or at==[r[1]-12 for r in rr]),(side,'data-only/CFG identity'))
        breaks=[(i,rr[i-1][2],rr[i][2]) for i in range(1,len(rr)) if rr[i][2]<=rr[i-1][2]]
        if not breaks:ck(at is not None,(side,'strict data-only path must be unique'))
        for o in (f for f in frames[side].values() if isinstance(f,dict) and f.get('first_rejected_candidate')):
            a,u=o['first_rejected_candidate']; o['first_rejected_raw']=b[a:a+13].hex()
        end=rr[-1][1]; sizes=[r[1]-r[0] for r in rr]
        envelope[side]=dict(header=13,row_bytes=sum(sizes),footer_at=end,footer=b[end:].hex(),payload=len(b),rows=len(rr),
            selector_counts=hist(r[3] for r in rr),row_width=[min(sizes),max(sizes)],identity_census=dict(ordinal_complete=True,nonzero=True,unique=True,
            repeats_equal=True,strictly_increasing=not breaks,inversions=len(breaks),first_inversion=breaks[0] if breaks else None,
            min_uid=min(r[2] for r in rr),max_uid=max(r[2] for r in rr),identity_sha256=H(b''.join(b[e-12:e] for _,e,_,_ in rr))),
            row_trace_sha256=H(b''.join(S.pack('<IIIB',*r) for r in rr)),first=list(rr[0]),last=list(rr[-1]))
        try:replay(b,1-mode)
        except Check as e:bad_mode[side]=str(e)
        else:raise Check((side,'wrong mode accepted'))
        ck(13+sum(sizes)+9==len(b),(side,'equation'))
    ck([r[2:] for r in rows['client']]==[r[2:] for r in rows['server']],'same identity and selector')
    sizes=[(s[1]-s[0])-(c[1]-c[0]) for c,s in zip(rows['client'],rows['server'],strict=True)]
    ck(min(sizes)>0,'server row not longer than matched client row')
    targets,td=target_domains(raw,rows)
    reg=regression(raw,rows,books,targets,J(BIG)); reg['wrong_mode_first_counterexample']=bad_mode
    provenance,ins,branches,ev=static()
    positions={k:i for i,(k,*_) in enumerate(SPEC)}
    profiles={}; ledger=[]
    # The shared branch may already contain v7. Read the requested immutable v6 blob.
    v6_source='8b04fc2:'+PRIOR[3]
    v6_blob=subprocess.check_output(['git','show',v6_source],cwd=ROOT)
    v6=json.loads(v6_blob); t44=J(PRIOR[2]); ck(v6['schema_version']==6 and t44['L4']==0,'preserved t44/v6 scope')
    skip={t['parent_code']:t['table_type'] for t in v6['tables'][:8]}; ck(set(skip.values())=={22,33,34,37,43,59,62,66},'eight skip tables')
    join_map={j[0]:j for j in JOINS}; pairs=[]
    old_codes={'Cnti','Cbni','Cccn','Ccty','Csot','CASt','CnCV','Csnm','PLgn','duni'}
    for i,field in enumerate(xml):
        k=field['field']; j=join_map.get(k); grade='unmapped'; reason='no scoped same-object main-row wire binding'; slot=None; first=None
        if j:
            ck(by_code[k]==[i],(k,'scoped unique XML')); slot=positions[j[3]]; pairs.append((slot,i,k))
            pf={s:domain(field,j,raw[s,3],books[s],targets,s,rows[s],master) for s in SIDES}; profiles[k]=pf
            held=[(s,p) for s,p in pf.items() if p['rows'] and p.get('domain')!='pass']
            if held:
                s,p=held[0]; grade='held'; reason=p['reason']; first=dict(p['first_counterexample'],archive=s)
            else:grade='L3'; reason='scoped static projection and full live-domain replay' if k not in old_codes else 'prior static projection, full archive revalidation'
        elif k in skip:
            grade='skipped_separate_member'; reason=f'table_{skip[k]}, prior v6; not a main-row slot'
        elif k in ('Cafl','Cvfl'):
            grade='skipped_separate_member'; reason='t44 shared club_links.dat; object vector +0x118/+0x120 not a main-row span'
        elif k in ('CLat','CLon','Cyfn','Csti','Cdvi','Crep'):
            grade='held'; reason={
              'CLat':'exact getter e8afb8 boxes zero via e8dc81; Liverpool city/stadium coordinates are not Club coordinates',
              'CLon':'exact getter e8afc4 boxes zero via e8afd9; no direct coordinate sink',
              'Cyfn':'getter e8e6a9/e8e6b1 reads +0x100 -> +0xd8 (extra record), fixture only',
              'Csti':'prior one-row positive and six negative direct probes do not establish Club main stadium',
              'Cdvi':'getter e8b945 uses first team then +0x30/+0x50; no same-object Club competition lane',
              'Crep':'getter e8ea2e/e8ea47 uses first team and default 1500; no same-object Club reputation lane'}[k]
            if k=='Cyfn': first=dict(reg['founded_year_fixture_only'][0],archive='client extra_3')
            if k in ('CLat','CLon','Csti','Crep'):first=dict(row=460,anchor='Liverpool',club_uid=676,note='L2 city/stadium/name is not same-object proof')
            if k=='Cdvi':first=dict(getter_site=0xe8b961,operand='qword ptr [rax + 0x30]',base='first Team pointer obtained from CLUB+0x18 at e8b945/e8b955')
        ledger.append(dict(xml_index=i,code=k,schema=field,grade=grade,reason=reason,candidate_position=slot,
            accepted_position=slot if grade=='L3' else None,previous_client_grade='L3' if k in old_codes else None,
            first_counterexample=first,static=ev.get(k),domain_profiles=profiles.get(k),lane=j[4] if j else None))
    pairs.sort(); inversions=[[[p,i,k],[q,j,c]] for a,(p,i,k) in enumerate(pairs) for q,j,c in pairs[a+1:] if p<q and i>j]
    order=dict(inversions=len(inversions),first_counterexample=inversions[0] if inversions else None,all_inversions=inversions,
               tie_policy='no ordering claim within shared physical slot',key='[outer position, XML occurrence, 4CC]')
    slot_data=[]; selectors={}
    for side in SIDES:
        selectors[side]=[dict(rows=n,execution_order=[positions[k] for k in order]) for order,n in sorted(paths[side].items())]
    for pos,(key,site,kind,w,off) in enumerate(SPEC):
        e={}; details={}
        for side in SIDES:
            e[side]=sorted({order.index(key) for order in paths[side] if key in order})
            details[side]=describe_slot(side,raw[side,3],books[side].get(key,[]),key)
        slot_data.append(dict(position=pos,key=key,site=site,type=kind,width=w,object_displacement=off,execution_index=e,
             candidate_4cc=[k for k,_,_,where,*_ in JOINS if where==key],profiles=details,
             item_width=COL[key][0] if key in COL else None,inner_or_flush_sites=COL[key][1] if key in COL else
             [0x423ff1d,0x423ff44,0x423ff5a,0x423ff70,0x423ff86,0x423ff98] if key=='obj150' else None,
             site_notes={'stad140':'ordinary e5bc6b; derived e5bccc before tail-call base',
                         'obj150_tag':'e5ada9; 0 invokes 45B tag reader; 2 invokes none; 1 static alternate not replayed',
                         'vec110':'count via e5ab0a -> 3fc2050', 'base_ba':'both classes call shared base; via 11d0d89 -> 3fc2050'}.get(key)))
    for side in SIDES:ck(sum(d['profiles'][side].get('bytes',0) for d in slot_data)==envelope[side]['row_bytes'],(side,'outer span coverage'))
    sha_paths={p:H((ROOT/p).read_bytes()) for p in (*PRIOR,MASTER,LOC,BIG,BIGMD,'scratch/t47/out/cursor_nation_tax.json') if p!=PRIOR[3]}
    for stem,items,size in [('instructions',ins,400),('branches',branches,200)]:
        for i in range(0,len(items),size):emit(f'{stem}.part{i//size+1:03}.json',items[i:i+size])
    cnt=hist(f['grade'] for f in ledger)
    emit('field_slots.json',dict(status='observed_dual_archive_outer_census_complete_unobserved_dispatch_not_replayed',L4=0,source=provenance,
         provenance_sha256=sha_paths,archives=archive,target_identity_domains=td,framing_sensitivity=frames,envelopes=envelope,
         axes='position indexes logical union; per-side execution_index lists possible zero-based event indexes over realized paths; coordinates digest hashes concatenated little-endian (u32 ordinal, u32 absolute, u32 span)',
         execution_templates=selectors,server_minus_client_row_bytes=dict(min=min(sizes),max=max(sizes),strictly_positive_rows=sum(d>0 for d in sizes),total=sum(sizes)),
         external_modes=dict(client=0,server=1,note='inferred from envelope replay; distinct from on-wire factory selector'),
         skipped=dict(subtables=skip,v6_git_object=v6_source,v6_sha256=H(v6_blob),club_links=['Cafl','Cvfl'],vector_offsets=[0x118,0x120]),slots=slot_data))
    emit('field_map.json',dict(status='partial',scope='club.xml#club top-level occurrences only',frozen_sha256=MASTERH,fields_total=433,
         L4=0,grade_counts=cnt,fields_with_unique_XML_alignment=len(JOINS),alignment_ratio=len(JOINS)/len(xml),domain_pass_L3=cnt.get('L3',0),
         new_L3=[f['code'] for f in ledger if f['grade']=='L3' and f['previous_client_grade'] is None],order=order,fields=ledger,regression=reg))
    print('t57 positions',len(SPEC),'grade counts',cnt,'inversions',len(inversions),'L4=0')


def selftest():
    b=HEAD+S.pack('<I',1)+b'\0'*39+S.pack('<III',0,5,5)+FOOT
    rows,bk,seq=replay(b,0); ck(rows==[(13,len(b)-9,5,0)] and sum(seq.values())==1 and bk['identity'][0]==(0,len(b)-21,12),'synthetic client cursor')
    try:replay(b,1)
    except Check:pass
    else:raise Check('bad mode accepted')
    k=[[(20,5),(21,6)],[(32,6)]]
    b=b'\0'*53
    ans,tr=path_count(b,k,13,9,12,{0},True,True,True); ck(ans['paths']==1 and tr==[20,32],'exact DP')
    ans,_=path_count(b,k,13,9,12,{0},True,False); ck(ans['paths']==1,'nonoverlap DP')


def main():
    ap=argparse.ArgumentParser(description=__doc__);g=ap.add_mutually_exclusive_group();g.add_argument('--build',action='store_true');g.add_argument('--selftest',action='store_true');args=ap.parse_args()
    try:
        if args.selftest:selftest();print('t57 builder selftest PASS')
        else:build()
    except Check as e:print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e:print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
