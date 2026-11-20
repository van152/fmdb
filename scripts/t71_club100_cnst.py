"""Build t71: CLUB+0x100 split-member cursor and the 24 held occurrences."""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t71/out'
OLD = ROOT.parent / 'fm24'
EXE = OLD / 'input/editor.exe'
EXE_HASH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
HEAD = bytes.fromhex('03017461642ef10d')
SIDES = ('client', 'server')
A = 'Ccsp Ccsk Ccsf Ccsr Ccsb Ccsh Ccsy'.split()
# Frozen t63 object-path order (the prompt lists B's membership, not lane order).
B = 'Ccjm Ccja Ccjc Ccjy Ccji Ccjg Ccjp Ccjs Ccjd Ccda Ccdr Ccss Ccjt Ccjh Ccpc'.split()
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
BIG = 'evidence/fm24/reports/dbdat_decode/db_tables_big.json'
BIGMD = 'evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md'
INPUTS = {
    'scratch/t57/out/field_map.json': '0b04de7b15c455ccb85212d43221d5cbecb8fd5ccbf830ba71d5f4f3011f3664',
    'scratch/t57/out/field_slots.json': 'da3d3abd76e3d96a4db989c2dec3fcc1d352d1ccaac5267b00ab12731bbd6489',
    'scratch/t63/out/field_map_r2.json': '5bdf1fc6e35c6c0cabe666a0e173228f6127a770392b73ca8d23b0a35c24dd46',
    'scratch/t63/out/projections.json': '2526ecc58871f7d994e58fcf2d42aab11d1ccf0e45afa79d525e16f86ed3a08b',
    'scratch/t59/out/field_map.json': 'fdbcb6120cf87b1f7987d50bc2b2283e8a25d23594060f4b348defbfc546d168',
    'scratch/t64/out/REPORT.md': 'fe9c92c540fa7344a76e25b9310543c181af91d59cbedc736c53b7e9dec7f5d8',
    'scratch/t44/out/cursor_club_links.json': 'e62d5f4c978186817558c67b5503028dde3d4328276405b7a2bda8f6c909a0e2',
}
N = 84259
CAP = 1_000_000
MINIMUM = {'client':25, 'server':238}
SIGNATURE = {'client': [(6,255),(7,255),(8,255),(9,255),(11,0),(13,0),(14,0),(15,0)],
             'server': [(6,0),(7,0),(8,0),(9,1),(19,1),(43,1)]}


class Check(Exception):
    """An evidence check failed (as distinct from fatal I/O or usage)."""


def require(ok, detail):
    if not ok:
        raise Check(detail)


def h(b): return sha256(b).hexdigest()
def load(p): return json.loads((ROOT / p).read_bytes())
def u(b, a=0): return struct.unpack_from('<I', b, a)[0]
def digest(x): return h(np.asarray(x, dtype='<i4').tobytes())
def hist(v): return {str(int(k)):int(n) for k,n in zip(*np.unique(v, return_counts=True), strict=True)}


def provenance():
    manifest = {f['path']:f['sha256'] for f in load('evidence/MANIFEST.json')['files']}
    pins = INPUTS | {p:manifest[p] for p in (MASTER, BIG, BIGMD)}
    for p, expected in pins.items():
        require(h((ROOT / p).read_bytes()) == expected, ('input SHA',p))
    return pins


def archives():
    import zstandard as zstd
    depot = Path(os.environ.get('FM24_DB_DIR', ROOT/'scratch/data'))
    if depot.drive.upper() == 'Z:' or depot.resolve().drive.upper() == 'Z:':
        raise ValueError('Z: is forbidden')
    def frame(b):
        require(b.startswith(b'\x28\xb5\x2f\xfd'), 'Zstandard magic')
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(b)
        used = len(b)-len(d.unused_data)
        require(d.eof and used > 0, 'Zstandard frame closure')
        return v, used
    out, meta = {}, {}
    for side in SIDES:
        b = (depot/f'{side}_db.dat').read_bytes()
        toc, base = (x+17 for x in struct.unpack_from('<QQ', b, 17))
        require(base == 34 and b[8:17] == b[toc:toc+9] == b'\x02\x01fmf.\x08\x00\x00', (side,'FMF shell'))
        directory, used = frame(b[toc+9:])
        require(toc+9+used == len(b),(side,'TOC EOF'))
        p = 0
        entries = {}
        def pull(n):
            nonlocal p
            require(p+n <= len(directory), 'TOC truncation')
            p+=n
            return directory[p-n:p]
        def num(): return u(pull(4))
        def text(): return pull(num()).decode('utf-8')
        def node(parent, depth):
            require(depth<20,'TOC nesting')
            prefix=parent+text()+'/'
            for _ in range(num()):
                name=prefix+text()+text()
                require(name not in entries and '..' not in name.split('/'),'TOC path')
                off,size,unpacked,_,_=struct.unpack('<5Q', pull(40))
                entries[name] = [base+off,base+off+size,unpacked]
            for _ in range(num()): node(prefix,depth+1)
        node('',0)
        require(p==len(directory) and len(entries)==(31 if side=='client' else 77), 'TOC count')
        m = meta[side] = dict(archive_sha256=h(b), data_base=base, toc_offset=toc, directory=entries, members={})
        for tid in ('extra_3','3','2' if side=='client' else '21'):
            name=f'{side}_db/table_{tid}.dat'
            lo,hi,n=entries[name]
            bound=min((v[0] for v in entries.values() if v[0]>lo), default=toc)
            require(base<=lo<hi<=bound,'member range')
            q=lo; frames=[]; choices=[]
            while q<hi:
                payload,w=frame(b[q:hi]); frames.append([q,q+w,len(payload)]); q+=w
                if len(payload)==n: choices.append(payload)
            require(len(choices)==1 and choices[0][:8]==HEAD, (name,'sized frame/head'))
            payload=out[side,tid]=choices[0]
            m['members'][tid]=dict(path=name,size=n,payload_sha256=h(payload),packed_sha256=h(b[lo:hi]),frames=frames)
    return out, meta


def groups_extra(b, side):
    """All four byte alignments; do not use reader cursors, enum or cross-archive UID to choose rows."""
    n=u(b,8); groups=[[] for _ in range(n)]; weak=[[] for _ in range(n)]
    counts=[]; bb=np.frombuffer(b, np.uint8)
    for phase in range(4):
        v=np.frombuffer(b, '<u4', (len(b)-phase)//4, phase)
        ix=np.flatnonzero(v<n); p=ix*4+phase
        ix=ix[(p>=12)&(p<len(b)-SIGNATURE[side][-1][0])]; p=ix*4+phase
        use=np.ones(len(p), bool); counts.append([len(p)])
        for j,(d,k) in enumerate(SIGNATURE[side],1):
            use &= bb[p+d]==k
            if j in (4,len(SIGNATURE[side])):
                counts[-1].append(int(use.sum()))
                dest=weak if j==4 else groups
                for i,a in zip(v[ix[use]].tolist(),p[use].tolist(),strict=True): dest[i].append(a)
    for group in (*groups,*weak): group.sort()
    return groups,weak,counts


def dp(groups, first, end, minimum, recover=False):
    prev=[]; back=[]
    for ordinal, group in enumerate(groups):
        pos=[a for a,_ in prev]; prefix=[0]
        for _,count in prev: prefix.append(prefix[-1]+count)
        cur=[]
        for a in group:
            if a+minimum>end: continue
            count=prefix[bisect_right(pos,a-minimum)] if ordinal else int(a==first)
            if count: cur.append((a,min(CAP,count)))
        if not cur:
            return dict(paths=0, first_dead_ordinal=ordinal, candidates=group[:4]),None
        if recover: back.append(cur)
        prev=cur
    paths=min(sum(c for _,c in prev),CAP); trace=None
    if recover and paths==1:
        a=prev[0][0]; trace=[a]
        for layer in reversed(back[:-1]):
            a=next(p for p,c in layer if c and p+minimum<=a); trace.append(a)
        trace.reverse()
    return dict(paths=paths,first_dead_ordinal=None),trace


def data_framing(b,side):
    groups,weak,counts=groups_extra(b,side)
    full, trace=dp(groups,12,len(b),MINIMUM[side],True)
    require(full['paths']==1,(side,'data-side frame',full))
    return dict(alignment_count_columns=['all bounded ordinal u32','weak u32 + first four signature bytes','strong signature'],
                candidates_by_alignment=counts, layer_histogram=hist([len(x) for x in groups]),
                first_multicandidate=next(([i,*x] for i,x in enumerate(groups) if len(x)>1),None),
                signature=SIGNATURE[side],minimum_span=MINIMUM[side],cap=CAP,
                strong=full,weak=dp(weak,12,len(b),MINIMUM[side])[0],
                identity_min4=dp(groups,12,len(b),4)[0],
                footer_sensitivity={str(f):dp(groups,12,len(b)-f,MINIMUM[side])[0] for f in (0,1,2,4,7,8,9,10,12)},
                header_sensitivity={str(a):dp(groups,a,len(b),MINIMUM[side])[0] for a in (11,12,13,14)}), trace


def main_identity(b, trace_profile):
    """t57 identity model only: extract the ordinal→UID keys, not a new main-row field census."""
    n=u(b,8); groups=[[] for _ in range(n)]
    for phase in range(4):
        v=np.frombuffer(b,'<u4',(len(b)-phase)//4,phase)
        for i in np.flatnonzero((v[:-2]<n)&(v[1:-1]==v[2:])&(v[1:-1]!=0)).tolist():
            a=phase+4*i
            if 13<=a<=len(b)-21: groups[int(v[i])].append((a,int(v[i+1])))
    back=[]; prev={}
    for i,group in enumerate(groups):
        curr={}
        for a,v in group:
            if i==n-1 and a!=len(b)-21: continue
            ps=[(p,c) for p,(w,c,_) in prev.items() if p+12<=a and w<v]
            paths=sum(c for _,c in ps) if i else 1
            if paths: curr[a]=(v,paths,ps[0][0] if ps else None)
        require(curr,('main identity DP',i)); back.append(curr); prev=curr
    require(sum(x[1] for x in prev.values())==1,'main identity uniqueness')
    a=next(iter(prev)); seq=[]
    for g in reversed(back):
        v,_,p=g[a]; seq.append((a,v)); a=p
    at,uid=np.array(seq[::-1], np.int64).T
    ids=np.column_stack((np.arange(n),uid,uid)).astype('<u4')
    require(h(ids.tobytes())==trace_profile['identity_census']['identity_sha256'],'t57 identity SHA')
    return at,uid


def replay(b, server, *, old=False):
    """Sequential transfer replay from @12; never scan for a next ordinal to repair a cursor."""
    n=u(b,8); p=12; rows=[]; branches={}
    def take(w,label):
        nonlocal p
        a=p; p+=w
        require(0<=w and p<=len(b),('short span',i,label,a,w,b[a:a+24].hex()))
        return a
    def num(w,label, signed=False, log=True):
        a=take(w,label); v=int.from_bytes(b[a:p],'little',signed=signed)
        if log: branches.setdefault(label,Counter())[v]+=1
        return v
    def count(w,label,stride,signed=False):
        k=num(w,label,signed);take(k*stride,label+' items')
    def tag(label): return num(1,label)
    def text(label): take(num(4,label+' length'),label)
    def zero(label,w=1):
        require(num(w,label)==0,('unobserved arm',i,label,p-w,b[p-w:p+20].hex()))
    def flag(label):
        a=p; v=tag(label);require(v in (0,1),('noncanonical flag',i,label,a,v));return v
    for i in range(n):
        r=p; o=num(4,'ordinal',log=False)
        require(o==i,('ordinal',i,r,o,b[r:r+20].hex()))
        date=a=btag_at=-1; ta=tb=-1
        if server:
            take(3,'+120'); count(2,'extra18',4)
            take(34,'+da decoder(5), +123(1), +c0(4), +88(24)')
            if flag('extra dates'): take(24,'+a0')
            take(15,'+de(2), +b8(4), +125(1), +84(4), +80(4)')
            if flag('election present'): date=take(19,'election')+4
            take(5,'+126')
            for label in ('+f8','+10c'):
                t=tag(label+' version'); take((8 if t>=3 else 0)+5+(t>=2)+(6 if t>=3 else 5),label)
            ta=tag('A version'); a=p; take(7 if ta>1 else 6,'A')
            tb=tag('B version'); btag_at=p; take(12 if tb<2 else 14 if tb==2 else 15,'B')
            take(4+8+(4 if old else 5)+8,'+bc, +c4, version-dependent +12b, +d0')
            count(1,'extra28',22,True);count(1,'extra20',10)
            if flag('extra48 present'):
                t=num(1,'extra48 version',True);take(16+8*(t>0),'extra48 fixed');count(1,'extra48 count',4)
            for label,w in (('extra30',1),('extra38',1),('extra70',1),('extra50',4)):zero(label,w)
            for _ in range(num(2,'extra68')):tag('extra68 version');take(10,'extra68 item')
            zero('extra40'); take(2,'+dc')
        year=take(2,'+d8'); cc=take(4,'+cc')
        # Base +ba is 0 in both frozen table_3 profiles. Therefore the +90 string is skipped.
        take(2,'base +ac');text('base +98')
        for _ in range(tag('base78 count')):
            t=tag('base78 outer tag');require(t==1,('unobserved base78 type',i,p-1,t));take(26,'base78 item')
        take(8,'base scalars')
        if server:
            count(2,'base18',20,True);count(1,'base30',6,True);take(16,'base +74(4), +68(12)')
            for _ in range(num(2,'base0')):
                t=tag('base0 type')
                if t in (4,5,6,7,37): take({4:43,5:24,6:19,7:24,37:27}[t],f'base0 type {t}')
                elif t==9:
                    take(20,'base0 type 9 fixed')
                    for _ in range(4): text('base0 type 9 text')
                elif t==16: count(1,'base0 type 16',4,True)
                elif t==38:
                    for _ in range(num(4,'base0 type 38 count')):
                        tag('type 38 version');zero('type 38 map',4);take(14,'type 38 fixed');text('type 38 text')
                else: raise Check(('unobserved base0 type',i,p-1,t))
            if flag('base48 present'):
                num(4,'base48 version')
                for _ in range(num(4,'base48 count')):
                    t=num(2,'base48 item version',True);take(8+(t>=2)+(t>=3),'base48 item')
        rows.append((r,p,year,cc,date,a,btag_at,ta,tb))
    require(p==len(b),('EOF',p,len(b),b[p:p+20].hex()))
    return np.array(rows,dtype=np.int64), {k:{str(v):n for v,n in sorted(c.items())} for k,c in branches.items()}


def member_lane(rows,j):
    """Return payload offset (+(-1) is never dereferenced); legacy A/B copies retain source attribution."""
    a,b,ta,tb=rows[:,5:9].T
    if j<7:
        return np.where(a<0,-1,a+np.where(ta<2,max(j-1,0),j))
    j-=7
    lane=np.full(len(rows),j)
    if j==12: lane=np.where(tb<2,8,lane)
    if j==13: lane=np.where(tb<2,4,lane)
    if j==14: lane=np.where(tb==2,4,np.where(tb<2,-1,lane))
    return np.where((b<0)|(lane<0),-1,b+lane)


def values(b,coords,w,signed=False):
    a=coords[coords>=0]; d=np.frombuffer(b,np.uint8)
    acc=np.zeros(len(a),dtype=f'<u{w}')
    for j in range(w): acc |= d[a+j].astype(acc.dtype) << (8*j)
    return acc.view(f'<i{w}') if signed else acc


def witness(b,coord,uid,i,w):
    a=int(coord[i]);return dict(ordinal=int(i),uid=int(uid[i]),absolute=a,raw=b[a:a+w].hex() if a>=0 else None)


def profile(b,coord,uid,w,signed=False,check=None):
    live=np.flatnonzero(coord>=0); x=values(b,coord,w,signed); bad=np.flatnonzero(~check(x)) if check is not None else []
    return dict(wire=len(x),absent=len(uid)-len(x),histogram=hist(x),zero=int(np.count_nonzero(x==0)),
                raw_ffffffff=int(np.count_nonzero(x==0xffffffff)) if w==4 else None,
                signed_minus_one=int(np.count_nonzero(x==-1)) if signed else None,
                coordinate_sha256=digest(coord),value_sha256=h(x.tobytes()),
                first=witness(b,coord,uid,live[0],w) if len(live) else None,
                bad=len(bad),first_violation=witness(b,coord,uid,live[bad[0]],w) | {'value':int(x[bad[0]])} if len(bad) else None)


def date_ok(v):
    y=v>>16; d=v&511
    leap=(y%4==0)&((y%100!=0)|(y%400==0))
    return (y>=1)&(d>=1)&(d<=365+leap)&(((v>>9)&127)==0)


def wrong(b,server,old=False):
    try: replay(b,server,old=old)
    except Check as e: return e.args[0]
    raise Check('negative control unexpectedly reached EOF')


def fixture(raw,rows,main,legacy):
    big=load(BIG)['tables']; anchors=legacy['regression']; p=rows['client'][:,2]
    client=raw['client','extra_3']; server=raw['server','extra_3']
    require(h(client)==big['extra_3']['source_payload_sha256']['client'],'frozen client extra SHA')
    exp={x['candidate_order_index']:x for x in big['3']['field_validation']['Cyfn_named_year_checks']}
    records=[]
    require(len(exp)==len(anchors['founded_year_fixture_only'])==14,'year fixture count')
    for e in anchors['founded_year_fixture_only']:
        i=e['row']; y=int.from_bytes(client[p[i]:p[i]+2],'little'); q=int(rows['server'][i,2]); x=exp[i]
        require(p[i]==e['absolute'] and y==e['year']==x['client_extra_3_u16_at_row_plus_4'] and e['note']==x['note'] and int.from_bytes(server[q:q+2],'little')==y,('year witness',i))
        records.append(e | dict(uid=int(main['client'][1][i]),server_absolute=q))
    liv={}
    for s in SIDES:
        b=raw[s,'3']; at,keys=main[s]; start=int(at[459])+12
        require(b[start]==0 and keys[460]==676 and u(b,start+1)==139 and u(b,start+17)==1061,('Liverpool main identity/span',s))
        p1=start+27; p2=p1+4+u(b,p1)
        require(b[p2+4:p2+4+u(b,p2)]==b'Liverpool','Liverpool short name')
        liv[s]=dict(ordinal=460,uid=676,city_ordinal=1061,nation_ordinal=139,short_name='Liverpool')
    c=raw['client','2']; stadium=raw['server','21']; city_at=14+43*1061
    require(struct.unpack_from('<III',c,city_at+30)==(1061,100047,100047),'Liverpool city UID')
    for j, cap in ((430,81044),(71,74031)):
        a=14+181*j
        require(struct.unpack_from('<II',stadium,a)==(cap,cap) and u(stadium,a+168)==j,('stadium anchor',j))
    negatives={k:anchors[k] for k in ('original_Cccn_negative','frozen_club_negatives','frozen_stadium_negatives','legacy_Shanghai_index_correction')}
    require(negatives['frozen_club_negatives']==big['3']['negative_results'] and negatives['frozen_stadium_negatives']==big['21']['negative_results'],'negative verbatim')
    return dict(liverpool=liv,city_uid=100047,bernabeu=dict(ordinal=430,capacity=81044,seats=81044),
                old_trafford=dict(ordinal=71,wire_capacity=74031,external=74140),year_witnesses=records,prior_negatives=negatives)

# Each named range starts at a decoded entry or instruction boundary. These are evidence ranges,
# not new mappings for other club fields. Offsets in this module are PE file offsets.
RANGES = {
 'main_named_open': (0xf4d4db,0xf4d584), 'main_factory_slot': (0xf2b550,0xf2b5bb),
 'typed_table_init': (0xf0295b,0xf02a97), 'init_db_this': (0xf026c0,0xf026e0),
 'type_ctor_arguments': (0x3ceb7d0,0x3ceb7fc), 'type_ctor_store': (0x3ceb8d2,0x3ceb8f0),
 'decimal_suffix_fast': (0x3573020,0x357304d), 'decimal_suffix': (0x35730d9,0x3573138), 'name_concat': (0x808b85,0x808bb9),
 'null_election_default':(0x3aaba92,0x3aaba9a), 'modern_split_call_1':(0x35118,0x35123), 'modern_split_call_2':(0x352c7,0x352d2),
 'factory_dispatch': (0xf48b30,0xf48b55), 'club_factory_case': (0xf48daf,0xf48de9),
 'club_factory_plain': (0xf49c34,0xf49c46), 'club_construct_vptr': (0x3aad0f3,0x3aad107),
 'club_construct_null': (0x3aad1a9,0x3aad1b4), 'aux_default_status': (0x3aabb18,0x3aabb37),
 'split_aux_selection': (0xf5164c,0xf51681), 'split_mode_copy': (0xf50a63,0xf50a6f),
 'split_aux_loader': (0x3bb8b70,0x3bb8d2d), 'combined_aux_loader': (0x3b92ca0,0x3b92dd2),
 'name_formatter': (0x3cefbe0,0x3cefd53), 'stream_open': (0x7d0585,0x7d05ab),
 'aux_row_reader': (0xe5d210,0xe5ed32),
 'status_reader_calls': (0xe5dd96,0xe5e0a9), 'aux_server_tail': (0xe5e1be,0xe5ec30),
 'status_A_reader': (0x4339e80,0x433a069), 'status_B_reader': (0x433bbc0,0x433bc7a),
 'election_reader': (0x4342940,0x4342aa0), 'year_gate': (0xe8b977,0xe8b983),
 'year_getter': (0xe8e6a9,0xe8e6bc), 'election_gate': (0xe8a39d,0xe8a3a9),
 'election_forward': (0xe8c65a,0xe8c67e), 'election_object': (0xe96f6c,0xe96f8b),
 'election_exact_case': (0xe97023,0xe9702f), 'election_date_getter': (0xe9717c,0xe971c5),
 'competing_club_links': (0xf2a395,0xf2a3b4),
}
EDGES = {0xf4d519:0xffa3b0,0xf4d559:0x7d0570,0xf4d57f:0xf2b350,0xf2b583:0xf48b30,
         0xf48db2:0xf49c34,0xf48dc3:0xe59a40,0xf49c3f:0xe59a40,0xe59a40:0x3aad0e0,
         0xf51658:0xf54f00,0xf54f00:0x3bb8b70,0x3bb8bb8:0xffa3b0,0xffa3b0:0x3cefbe0,
         0x3bb8bf6:0x7d0570,0x3bb8d0c:0xe5d210,0xe5d298:0xe566d0,0xe566d0:0x3aaba20,
         0xe5d2ba:0xe5d338,0xe5d5a6:0x11d3200,0xe5dc3f:0xe5dcc9,0xe5dcc4:0x15211a0,
         0x15211a0:0x4342940,0xe5de44:0x151d2e0,0x151d2e0:0x4339e80,0xe5dea5:0x151d710,
         0x151d710:0x433bbc0,0xe8a3a3:0xe8c65a,0xe8c679:0xe96f20,0xe97029:0xe9717c,
         0xe8b97d:0xe8e6a9,0xe89c13:0x151d9b0,0xe8a005:0x151e500,
         0xf2926d:0xf30c70,0xf30c70:0x3b92ca0,0x3b92dad:0xe5d210,
         0xe5dfb0:0xe5dfb7,0xe5ec2b:0xe5d342,0xf02973:0xff9910,0xff9910:0x3ceb7d0,
         0x3cefc73:0x807ba0,0x807ba0:0x3573020,0x3573133:0x80af90,0x3cefd4e:0x808b50,
         0xf2a3af:0x1529210,0x3511e:0xf50a50,0x352cd:0xf50a50}


def static(prior, archive_metadata, pins):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    import pefile
    raw=EXE.read_bytes(); require(h(raw)==EXE_HASH,'editor SHA')
    pe=pefile.PE(data=raw,fast_load=True);base=pe.OPTIONAL_HEADER.ImageBase
    pe.parse_data_directories(directories=[3]); fn={pe.get_offset_from_rva(x.struct.BeginAddress):pe.get_offset_from_rva(x.struct.EndAddress) for x in pe.DIRECTORY_ENTRY_EXCEPTION}
    def va(o): return base+pe.get_rva_from_offset(o)
    def off(v): return pe.get_offset_from_rva(v-base)
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    def decode(a): return next(md.disasm(raw[a:a+15],va(a),1))
    def blob(a,w): return dict(file_offset=a,VA=va(a),bytes=raw[a:a+w].hex())
    def rip(i): return i.address+i.size+next(o.mem.disp for o in i.operands if o.type==3 and i.reg_name(o.mem.base)=='rip')
    insns={}
    def add(i):
        a=off(i.address); insns[a]=i
    def get(a):
        if a not in insns: add(decode(a))
        return insns[a]
    sections={}
    for name,(a,z) in RANGES.items():
        sections[name]=[a,z]
        for i in md.disasm(raw[a:z],va(a)): add(i)
        require(a in insns,('instruction range',name))
    leaves=(0x4348ef0,0x4340450,0x3aaf9e0,0x3ab0750,0x39aa1f0,0x42674a0,0x4349ce0,
            0x11d3200,0x4330ce0,0x3ea5150,0x4387ab0,0x155c120,0x35b07f0,
            0x42c8f90,0x156a3d0,0x42d2710,0x42d6a10,0x42c66f0,0x42dba50,0x14d7530,0x42d9380,0x14da470,0x360e390)
    for a in leaves:
        z=fn[a]; sections[f'grammar_{a:x}']=[a,z]
        for i in md.disasm(raw[a:z],va(a)): add(i)
    def edge(a,z):
        x=get(a);require(x.operands[0].type==2 and off(x.operands[0].imm)==z,('PE branch',hex(a),hex(z),x.op_str))
    for a,z in EDGES.items(): edge(a,z)
    records={}
    for r in prior['occurrences']:
        if r['code'] not in A+B: continue
        x=r['projection']; records[r['code']]=x
        for gate in (x['gate'],x['helper']):
            for a in gate['sites']+gate['local_path']:get(a)
        get(x['member_use'])
    for j,k in enumerate(A+B):
        x=records[k]; i=get(x['member_use']); origin=0xe0 if j<7 else 0xe7
        require(i.mnemonic=='movsx' and i.operands[1].size==1 and i.operands[1].mem.disp==0xe0+j-origin
                and x['object_path']==[0x100,0xe0+j],('t63 byte path',k))
    require(fn[0xe5a7a0]==0xe5bfca and fn[0xe5d210]==0xe5ed32,'PE exception extent')
    vptr=off(rip(get(0x3aad0fd))); require(vptr==0x187c308,'CLUB vptr')
    cells={}
    for slot,a in ((2,0xe89a00),(19,0xe5a7a0),(43,0xe5f3d0)):
        p=vptr+slot*8; require(off(struct.unpack_from('<Q',raw,p)[0])==a,('vslot',slot)); cells[str(slot)]=blob(p,8)|{'target':a}
    fac=0xf49d38; rel=struct.unpack_from('<i',raw,fac+12)[0]
    require(off(va(fac)+rel)==0xf48daf, 'CLUB factory table cell 3')
    prefix=(int(get(0x3cefca4).operands[1].imm).to_bytes(8,'little')+int(get(0x3cefcb2).operands[1].imm).to_bytes(4,'little')).decode('ascii')
    ext=off(rip(get(0x3bb8b90)));require(prefix=='table_extra_' and raw[ext:ext+5]==b'.dat\0','split file format')
    vt=off(rip(get(0xf02978))); require(vt==0x187ec08 and off(struct.unpack_from('<Q',raw,vt-8)[0])==0x187ec70,'typed context vtable/COL')
    td=off(base+u(raw,0x187ec70+12)); rtti=b'.?AV?$DATABASE_TABLE@VCLUB@db@@@db@@\0'; require(raw[td+16:td+16+len(rtti)]==rtti,'typed table RTTI')
    fmt=off(rip(get(0x3573126))); require(raw[fmt:fmt+3]==b'%d\0','numeric suffix format')
    for a,op in ((0xf026dd,'r14, rcx'),(0xf0296b,'edx, 3'),(0xf0297f,'qword ptr [rdi], rax'),(0xf02a93,'qword ptr [r14 + 0x10], rdi'),(0x3ceb8e2,'dword ptr [rsi + 0x54], edi')):
        require(get(a).op_str==op,('CLUB context sink',hex(a)))
    routes={
        'context_init': {'type':3,'type_store':0x3ceb8e2,'db_slot_store':0xf02a93,'vtable_lea':0xf02978,
                         'COL_ptr':blob(vt-8,8),'COL':blob(0x187ec70,24),'RTTI':blob(td+16,len(rtti))},
        'main': {'context_displacement':0x10,'type_displacement':0x54,'type':3,'name':'table_3.dat','factory_cell':blob(fac+12,4)|{'table_base':fac,'target':0xf48daf},'vtable_cells':cells},
        'split': {'context_displacement':0x10,'type_displacement':0x54,'formatter':0x3cefbe0,'extra_flag':1,'old_save_flag':0,'prefix':prefix,'extension_bytes':blob(ext,5),
                  'template':prefix+'<decimal type>.dat','decimal_format':blob(fmt,3),'member_paths':[archive_metadata[s]['members']['extra_3']['path'] for s in SIDES],
                  'stream_reader':0x3bb8b70,'row_reader':0xe5d210,'counts_as':{'header_count_u32':0x3bb8c28,'row_ordinal_u32':0x3bb8c68},
                  'slow_lookup':'context +0x20 remap tree when +0x28 set/out of vector bound; missing target can call reader using scratch extra, not a standalone identity'},
        'combined_control': {'reader':0x3b92ca0,'mode':1,'sites':[0xf29264,0xf2926d,0x3b92cc7,0x3b92d06,0x3b92da3,0x3b92daa,0x3b92dad],
                             'note':'same ordinal/body reader but not the split-member name proof'},
    }
    for a in (0xf29264,): get(a)
    tag_cases={}
    for t,s,v,r in ((4,0x14cf767,0x18b86b8,0x42c8f90),(5,0x14cf7bd,0x18b8768,0x42d2710),(6,0x14cf7f8,0x18b8818,0x42d6a10),
                     (7,0x14cf82c,0x18b8608,0x42c66f0),(9,0x14cf8c4,0x18b9208,0x42dba50),(16,0x14cf9e8,0x18b9a88,0x14d7530),
                     (37,0x14cfd26,0x18b88d8,0x42d9380),(38,0x14cfd51,0x18b9428,0x14da470)):
        c=0x14d0184+t*4; arm=off(va(0x14d0184)+struct.unpack_from('<i',raw,c)[0]); vr=off(struct.unpack_from('<Q',raw,v+16)[0]); require(off(rip(get(s)))==v,'base tag vptr')
        if vr!=r:edge(vr,r)
        tag_cases[t]={'cell':blob(c,4),'arm':arm,'install_lea':s,'vtable_slot_2':blob(v+16,8),'entry':vr,'reader':r}
    evidence={str(a):blob(a,i.size)|dict(instruction=f'{i.mnemonic} {i.op_str}'.rstrip()) for a,i in sorted(insns.items())}
    return dict(editor={'path':str(EXE),'sha256':EXE_HASH}, frozen_inputs=pins,addressing='all sites are PE file offsets; every witness carries its VA',
                routes=routes, sections=sections, edges=EDGES, instructions=evidence, base0_tag_cases=tag_cases,
                target_witnesses={
                  'Cyfn':{'object_path':[0x100,0xd8], 'size':2,'client_sites':[0xe5d33b,0xe5d388],'server_sites':[0xe5ec24,0xe5ec2b,0xe5d342,0xe5d388], 'getter':[0xe8b977,0xe8b97d,0xe8e6a9,0xe8e6b1]},
                  'Cebd':{'object_path':[0x100,0x78,8],'flag_test':0xe5dc38,'allocate_store':0xe5dc73,'transfer':0x4342989,'body_lane':4,'size':4,'getter':[0xe8a39d,0xe8a3a3,0xe8c679,0xe96f6c,0xe96f7c,0xe97023,0xe97029,0xe9717c]},
                  'A':{'tag':0x4339ea1,'modern_transfers':[0x4339ed1,0x4339eed,0x4339f09,0x4339f25,0x4339f45,0x4339f65,0x4339f88],
                       'legacy':'tag <= 1: read six to member +1..+6; copy +1 into +0 (433a057/5b)'},
                  'B':{'tag':0x433bbe5,'one_byte_loop':0x433bc32,'length_sites':[0x433bc03,0x433bc08,0x433bc0c,0x433bc0e,0x433bc13],
                       'legacy':'tag <2 reads 12; +12=+8, +13=+4, no +14 wire. tag==2 reads 14, +14=+4. tag>=3 reads all 15.'}},
                disjoint_readers={'numbered_subtable':{'schema_parents':dict(Cstc=22,Clhs=37,CSrs=62,Cmti=43,CNtp=66,Cdbt=33,Tchl=34,Csme=59),
                       'note':'ordinary table_<type>.dat uses type/selector factory and slot 19. Aux uses table_extra_ prefix and existing Club ordinal lookup, not per-row construction.'},
                       'club_links':{'member':'server_db/club_links.dat','reader':0x1529210,'context_displacement':0x680,'club_vector':[0x118,0x120],
                       'prior':'scratch/t44/out/cursor_club_links.json','note':'t44 named POD reader, not +0x100'},
                       'name_table':{'note':'neither name_table_ nor name_table_extra_ prefix can be produced on this route (directory only; not reopened)',
                                     'paths':{s:[p for p in archive_metadata[s]['directory'] if p.split('/')[-1].startswith('name_table_')] for s in SIDES}}},
                limits=['Split function forwards external r8b; the visible 0x3511e/0x352cd callers pass 1. Mode 0 on the client payload is proved by reader replay, not a claim that the editor displayed or opened the installed client DB.',
                        'Replay covers the observed modern arm; alternative flags and legacy variants not in the two payloads are not treated as unreachable.'])


def build():
    pins=provenance(); raw, am=archives(); master=load(MASTER); old=load('scratch/t57/out/field_map.json'); slots=load('scratch/t57/out/field_slots.json')
    prior=load('scratch/t63/out/projections.json'); t63=load('scratch/t63/out/field_map_r2.json')
    chain=static(prior,am,pins)
    rows={}; main={}; env={}
    for side, payload_size in zip(SIDES,(13053908,35009248), strict=True):
        extra=raw[side,'extra_3']; tab=raw[side,'3']; server=side=='server'
        require(len(extra)==payload_size and u(extra,8)==u(tab,8)==N,('count/size',side))
        require(h(tab)==slots['archives'][side]['members']['3']['payload_sha256'],'t57 main digest')
        require(next(x for x in slots['slots'] if x['key']=='base_ba')['profiles'][side]['histogram']=={'0':N},'base+ba profile')
        main[side]=main_identity(tab,slots['envelopes'][side]); d, tr=data_framing(extra,side)
        r, branches= replay(extra,server); rows[side]=r
        require(np.array_equal(r[:,0],tr),('independent data vs replay',side))
        require(min(r[:,1]-r[:,0])==MINIMUM[side] and r[-1,1]==len(extra),'frame widths/EOF')
        uid=main[side][1]; extra12=np.column_stack([values(extra,r[:,0]+k,4) for k in (0,4,8)])
        trip_miss=np.flatnonzero((extra12[:,1]!=uid)|(extra12[:,2]!=uid)); require(len(trip_miss)==N,'not a main triple')
        env[side]=dict(count=N,header=12,footer=0,body=len(extra)-12,payload=len(extra),width=[int(min(r[:,1]-r[:,0])),int(max(r[:,1]-r[:,0]))],
                       first=r[0].tolist(),last=r[-1].tolist(),data_dp=d,branch_histograms=branches,
                       replay_sha256=digest(r),ordinal_uid_sha256=digest(np.c_[np.arange(N),uid]),
                       width_negative={'candidate':'ordinal | UID | UID (also rules out those 12 lanes with 13/14-byte lookahead)',
                                       'failures':len(trip_miss),'first':dict(absolute=12,raw=extra[12:26].hex(),dwords=extra12[0].tolist(),expected_uid=int(uid[0]))},
                       wrong_external_mode=wrong(extra,not server),old_version_probe=wrong(extra,True,True) if server else None,
                       unsigned32_control_cc=profile(extra,r[:,3],uid,4))
    uid=main['client'][1]; require(np.array_equal(uid,main['server'][1]),'same UID per ordinal after main join')
    matched=np.searchsorted(main['server'][1],uid); require(np.array_equal(matched,np.arange(N)),'UID bijection')
    fix=fixture(raw,rows,main,old)
    allowed=sorted(int(v['enum']) for v in master['enums']['cnst']['values']); require(allowed==[0,1,2,3,4,6],'frozen enum')
    comp=load('scratch/t59/out/field_map.json'); comp_union=set()
    comp_fields=[f for f in comp['fields'] if (f.get('schema') or {}).get('enum_ref')=='cnst' and f.get('status')=='L3']
    require(len(comp_fields)==22,'frozen comp baseline')
    for f in comp_fields:
        for s in SIDES: comp_union.update(map(int,f['domain_profiles'][s]['histogram']))
    require(comp_union=={0,1,2,4,6},'comp observed subset')
    first_by_code={f['code']:f for f in old['fields']}; second_by_code={f['code']:f for f in t63['fields']}; frozen=master['entities']['club.xml'][0]['fields']
    proj={r['code']:r['projection'] for r in prior['occurrences'] if r['code'] in A+B}
    cv=[]; club_union=set()
    for j,k in enumerate(A+B+['Cebd','Cyfn']):
        r1=first_by_code[k]; r2=second_by_code.get(k); xi=r1['xml_index']; schema=frozen[xi]
        require(sum(x['field']==k for x in frozen)==1 and schema==r1['schema'] and (r2 or r1)['grade']=='held',('held/frozen unique',k))
        if k in A+B:
            w=1; coords={s:member_lane(rows[s],j) for s in SIDES}; validate=lambda x:np.isin(x,allowed)
            require(schema.get('enum_ref')=='cnst','scoped enum'); getter=proj[k]; wire={'object_path':[0x100,0xe0+j], 'width':w,
                    'side':'server', 'body_anchor':'A' if j<7 else 'B', 'modern_lane':j if j<7 else j-7,
                    'absolute_rule':f'row_start + {132+j if j<7 else 140+j-7} + 19*election_present',
                    'absent_client_default':6}
            rr=rows['server']; expect=rr[:,0]+(132+j if j<7 else 140+j-7)+19*(rr[:,4]>=0)
            require(np.array_equal(coords['server'],expect) and np.all(rr[:,7:9]==[2,3]),('observed fixed formula',k))
        elif k=='Cebd':
            w=4;coords={s:rows[s][:,4] for s in SIDES};validate=date_ok;getter=chain['target_witnesses'][k]
            wire={'object_path':[0x100,0x78,8], 'width':4,'side':'server','absolute_rule':'row_start + 88 iff u8[row_start+83] != 0', 'client':'absent'}
            rr=rows['server']; require(np.array_equal(coords['server'],np.where(rr[:,4]>=0,rr[:,0]+88,-1)),'observed election formula')
        else:
            w=2;coords={s:rows[s][:,2] for s in SIDES}; lo=int(schema['min_value']);hi=int(schema['max_value']);validate=lambda x: (x==0)|((x>=lo)&(x<=hi)); getter=chain['target_witnesses'][k]
            rr=rows['server']; bb=np.frombuffer(raw['server','extra_3'],np.uint8); e=rr[:,4]>=0
            a28=rr[:,0]+180+19*e; n28=bb[a28].astype(np.int64); f48=a28+2+22*n28
            a68=f48+8+66*bb[f48].astype(np.int64); n68=values(raw['server','extra_3'],a68,2)
            require(np.array_equal(a68+5+11*n68,coords['server']),'Cyfn simplified observed cursor')
            wire={'object_path':[0x100,0xd8],'width':2,'side':'both','absolute_rule':{'client':'row_start+4',
                   'server':'a68+5+11*u16le[a68]; a68=f48+8+66*u8[f48]; f48=a28+2+22*u8[a28]; a28=row_start+180+19*election_present'},
                  'zero':'optional; getter suppresses zero'}
        profiles={s:profile(raw[s,'extra_3'],coords[s],uid,w,w==1,validate) for s in SIDES}
        x=values(raw['client','extra_3'],coords['client'],w,w==1); y=values(raw['server','extra_3'],coords['server'],w,w==1)
        if k=='Cyfn':
            ix=np.flatnonzero(x!=y[matched]); intersect=N; equal=N-len(ix); diff=len(ix); absent=0
        else: ix=[]; intersect=equal=diff=0; absent=N
        pair=dict(uid_joined=N,both_wire=intersect,equal=equal,different=diff,client_station_absent=absent,
                  server_station_absent=N-profiles['server']['wire'],first_difference=None)
        if len(ix):
            i=ix[0];pair['first_difference']={s:witness(raw[s,'extra_3'],coords[s],uid,i,w) for s in SIDES}
        if w==1:
            change=np.flatnonzero(y[matched]!=6); pair['client_constructor_default_only']={'value':6,'equal_to_server':N-len(change),'different_from_server':len(change),
              'first_difference':witness(raw['server','extra_3'],coords['server'],uid,change[0],1) if len(change) else None}
            club_union.update(map(int,profiles['server']['histogram']))
        if k=='Cebd':
            profiles['server']['calendar']={'year_range':[int((y>>16).min()),int((y>>16).max())], 'day_range':[int((y&511).min()),int((y&511).max())], 'default_1900_day1':int(np.count_nonzero(y==0x076c0001))}
        bad=next((p['first_violation'] for p in profiles.values() if p['bad']),None) or pair['first_difference']
        cv.append(dict(code=k,id=f'E97/club.xml#club/{xi:03}',prior={'ledger':'E106' if r2 else 'E97','grade':'held','path':'scratch/t63/out/field_map_r2.json' if r2 else 'scratch/t57/out/field_map.json',
                         'first_counterexample':(r2 or r1)['first_counterexample'],'reason':(r2 or r1)['reason']},
                       grade='held' if bad else 'L3',schema=schema,static_getter=getter,wire=wire,profiles=profiles,uid_pair_control=pair,first_counterexample=bad))
    grades=dict(Counter(f['grade'] for f in cv));
    fieldmap=dict(scope='24 increments; no main row changes and no L4', counts=grades,L4=0,scoped_enum={'id':'cnst','values':master['enums']['cnst']['values'],
                   'allowed':allowed,'observed_club_wire':sorted(club_union),'observed_comp_control':sorted(comp_union),'comp_source':'t59/E99 baseline retained by t64/E107 (not a Club coordinate source)'}, fields=cv)
    rowmap=dict(archives=am,identity='row-prefix u32 ordinal only; UID via exact table_3 ordinal join',
                columns=['row_start','end_exclusive','Cyfn','extra_cc_control','Cebd','A_payload','B_payload','A_tag','B_tag'],
                missing=-1, coordinate_digest='contiguous LE i32 (including -1), in ordinal order',envelopes=env,fixtures=fix)
    OUT.mkdir(parents=True,exist_ok=True)
    for name,doc in (('chain.json',chain),('rows_extra3.json',rowmap),('field_map_r3.json',fieldmap)):
        (OUT/name).write_text(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(f't71 build: 84259 x 2 rows, UID bijection; {grades}')


def selftest():
    d,t=dp([[12],[37,44],[62]],12,87,25,True);require(t==[12,37,62] and d['paths']==1,'DP lookahead')
    require(dp([[12],[37],[62]],12,86,25)[0]['first_dead_ordinal']==2,'footer selftest')
    rows=np.array([[0,0,0,0,-1,100,200,1,1],[0,0,0,0,-1,100,200,2,2],[0,0,0,0,-1,-1,-1,-1,-1]])
    require(member_lane(rows,0).tolist()==[100,100,-1] and member_lane(rows,1).tolist()==[100,101,-1] and member_lane(rows,21).tolist()==[-1,204,-1],'legacy tag lanes')
    require(values(b'\0\xff',np.array([0,1,-1]),1,True).tolist()==[0,-1],'signed sentinel')
    require(date_ok(np.array([2024<<16|366,2023<<16|366,0],dtype=np.uint32)).tolist()==[True,False,False],'calendar')
    print('t71 builder selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ex=ap.add_mutually_exclusive_group();ex.add_argument('--selftest',action='store_true');ex.add_argument('--build',action='store_true',help='build artifacts (default)')
    args=ap.parse_args();sys.path.append(str(OLD/'tools/python'))
    try:
        selftest() if args.selftest else build()
    except Check as e:
        print(f'FAIL: {e}',file=sys.stderr);return 1
    except (OSError,ValueError,KeyError,IndexError,ImportError,struct.error) as e:
        print(f'FATAL: {e}',file=sys.stderr);return 2
    return 0


if __name__=='__main__': sys.exit(main())