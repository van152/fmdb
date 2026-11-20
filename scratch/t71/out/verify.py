"""Independent t71 audit: reverse ordinal DP, bounded per-row parse, PE and domain checks."""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import struct
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT.parent/'fm24'
SIDES = ('client','server')
N = 84259
EXE_HASH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
BIG = 'evidence/fm24/reports/dbdat_decode/db_tables_big.json'


class Failure(Exception): pass


def check(ok, msg):
    if not ok: raise Failure(msg)


def sha(b): return sha256(b).hexdigest()
def j(p): return json.loads(p.read_bytes())
def uint(b, a, n=4): return int.from_bytes(b[a:a+n],'little')
def cd(a): return sha(np.asarray(a,dtype='<i4').tobytes())
def histogram(a): return {str(k):v for k,v in Counter(a.tolist()).items()}


def load_raw(archives):
    import zstandard
    location=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data')).resolve()
    if location.drive.upper()=='Z:': raise ValueError('Z: is forbidden')
    def decompress(blob):
        check(blob[:4]==bytes.fromhex('28b52ffd'),'frame signature')
        z=zstandard.ZstdDecompressor().decompressobj(); v=z.decompress(blob)
        check(z.eof,'frame EOF');return v,len(blob)-len(z.unused_data)
    out={}
    for side in SIDES:
        doc=archives[side]; raw=(location/f'{side}_db.dat').read_bytes()
        a=17+uint(raw,17,8); data_at=17+uint(raw,25,8)
        check(a==doc['toc_offset'] and data_at==doc['data_base']==34 and sha(raw)==doc['archive_sha256'],('archive',side))
        check(raw[8:17]==raw[a:a+9]==bytes.fromhex('0201666d662e080000'),'archive shell')
        toc,used=decompress(raw[a+9:]);check(a+9+used==len(raw),'TOC closure')
        def take_text(p):
            w=uint(toc,p);check(p+4+w<=len(toc),'TOC text');return toc[p+4:p+4+w].decode(),p+4+w
        def walk(i,parent,depth):
            check(depth<20,'TOC depth'); name,i=take_text(i); base=parent/name
            size=uint(toc,i);i+=4
            for _ in range(size):
                stem,i=take_text(i);suffix,i=take_text(i);off,w,n,_,_=struct.unpack_from('<5Q',toc,i);i+=40
                key=(base/(stem+suffix)).as_posix();check(key not in found and '..' not in PurePosixPath(key).parts,'TOC duplicate/traversal')
                found[key]=[data_at+off,data_at+off+w,n]
            size=uint(toc,i);i+=4
            for _ in range(size): i=walk(i,base,depth+1)
            return i
        found={}
        check(walk(0,PurePosixPath(),0)==len(toc) and found==doc['directory'],'full directory independently parsed')
        expected=('extra_3','3','2' if side=='client' else '21');check(set(doc['members'])==set(expected),'scope of members')
        for t in expected:
            name=f'{side}_db/table_{t}.dat'; m=doc['members'][t]; p,q,size=found[name]; data=raw[p:q]
            end=min((m[0] for m in found.values() if m[0]>p), default=a)
            check(data_at<=p<q<=end and m['path']==name and m['size']==size and sha(data)==m['packed_sha256'],'member named extent')
            frames=[]; hits=[]
            while p<q:
                v,length=decompress(raw[p:q]);frames.append([p,p+length,len(v)]);p+=length
                if len(v)==size: hits.append(v)
            check(len(hits)==1 and frames==m['frames'],'unique sized frame')
            v,=hits;check(v[:8].hex()=='03017461642ef10d' and sha(v)==m['payload_sha256'],'member payload')
            out[side,t]=v
    return out


def pe_check(doc, prior):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    b=(OLD/'input/editor.exe').read_bytes(); p=pefile.PE(data=b,fast_load=True); base=p.OPTIONAL_HEADER.ImageBase
    p.parse_data_directories(directories=[3]); md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    check(sha(b)==doc['editor']['sha256']==EXE_HASH,'editor provenance')
    def va(a): return base+p.get_rva_from_offset(a)
    def off(v):return p.get_offset_from_rva(v-base)
    def read(i): return next(md.disasm(b[i:i+15],va(i),1))
    def checked_blob(d):
        a=d['file_offset']; contents=bytes.fromhex(d['bytes']);check(va(a)==d['VA'] and b[a:a+len(contents)]==contents,('raw PE evidence',hex(a)));return contents
    for a,s in doc['instructions'].items():
        bb=checked_blob(s); u=read(int(a));check(int(a)==s['file_offset'] and u.bytes==bb and f'{u.mnemonic} {u.op_str}'.rstrip()==s['instruction'],('decode',a))
    for a,t in doc['edges'].items():
        ins=read(int(a));check(ins.operands[0].type==2 and off(ins.operands[0].imm)==t,('recorded branch',a))
    def op(a,s):check(read(a).op_str==s,('operand',hex(a),s))
    def direct(a,t):check(off(read(a).operands[0].imm)==t,('direct',hex(a),hex(t)))
    def rip(a):
        i=read(a);return i.address+i.size+next(o.mem.disp for o in i.operands if o.type==3 and i.reg_name(o.mem.base)=='rip')
    def cell(r):return struct.unpack('<Q',checked_blob(r))[0]
    rt=doc['routes']; main=rt['main']; c=main['factory_cell']; tab=rip(0xf48b45)
    check(c['file_offset']==off(tab)+12 and off(tab+struct.unpack('<i',checked_blob(c))[0])==0xf48daf,'case 3')
    vtable=off(rip(0x3aad0fd))
    for s,target in ((2,0xe89a00),(19,0xe5a7a0),(43,0xe5f3d0)):
        d=main['vtable_cells'][str(s)];check(d['file_offset']==vtable+s*8 and off(cell(d))==target,'CLUB vslot')
    check(any(off(base+x.struct.BeginAddress)==0xe5a7a0 and off(base+x.struct.EndAddress)==0xe5bfca for x in p.DIRECTORY_ENTRY_EXCEPTION),'slot 19 bounds')
    op(0xf4d4db,'rbp, qword ptr [r13 + 0x10]');op(0xf5164c,'rcx, qword ptr [r14 + 0x10]')
    op(0xf2b580,'ecx, dword ptr [rsi + 0x54]');direct(0xf2b583,0xf48b30);op(0xf2b5b1,'qword ptr [rbx + 0x98]')
    direct(0xf51658,0xf54f00);direct(0xf54f00,0x3bb8b70);op(0x3bb8bb2,'r8b, 1');op(0x3bb8bb5,'r9d, r9d')
    direct(0x3bb8bb8,0xffa3b0);direct(0xffa3b0,0x3cefbe0);op(0x3cefc62,'eax, dword ptr [rcx + 0x54]')
    name=''.join(read(a).operands[1].imm.to_bytes(w,'little').decode() for a,w in ((0x3cefca4,8),(0x3cefcb2,4)))
    check(name==rt['split']['prefix']=='table_extra_' and off(rip(0x3bb8b90))==rt['split']['extension_bytes']['file_offset'] and checked_blob(rt['split']['extension_bytes'])==b'.dat\0','split member name')
    check(off(rip(0x3573126))==rt['split']['decimal_format']['file_offset'] and checked_blob(rt['split']['decimal_format'])==b'%d\0','decimal formatter')
    ctx=rt['context_init'];vt=off(rip(0xf02978)); loc=off(cell(ctx['COL_ptr'])); check(ctx['COL_ptr']['file_offset']==vt-8 and ctx['COL']['file_offset']==loc,'typed table COL')
    rtti=struct.unpack_from('<I',checked_blob(ctx['COL']),12)[0]
    check(off(base+rtti)+16==ctx['RTTI']['file_offset'] and checked_blob(ctx['RTTI'])==b'.?AV?$DATABASE_TABLE@VCLUB@db@@@db@@\0','DATABASE_TABLE<CLUB> RTTI')
    op(0xf0296b,'edx, 3');op(0x3ceb7e8,'edi, edx');op(0x3ceb8e2,'dword ptr [rsi + 0x54], edi');op(0xf02a93,'qword ptr [r14 + 0x10], rdi')
    op(0xf2a395,'rcx, qword ptr [rdi + 0x680]'); direct(0xf2a3af,0x1529210)
    for a,w in ((0x3bb8c1f,4),(0x3bb8c5c,4),(0xe5d382,2)):
        check(read(a).operands[1].imm==w,('native transfer width',hex(a)))
    op(0x3bb8d02,'rcx, qword ptr [rcx + rax*8]');op(0x3bb8d09,'r8d, r15d');direct(0x3bb8d0c,0xe5d210)
    op(0xe5d29d,'qword ptr [rsi + 0x100], r14');op(0xe5d33b,'r14, 0xd8');direct(0xe5d2ba,0xe5d338)
    op(0xe5dc73,'qword ptr [r14 + 0x78], rdi');op(0x4342975,'rdx, [rsi + 8]');op(0x4342989,'qword ptr [rax + 0x28]')
    op(0xe9717c,'edi, dword ptr [rcx + 8]');op(0xe8e6b1,'esi, word ptr [rax + 0xd8]');direct(0xe8b97d,0xe8e6a9)
    op(0xe89bef,'rcx, qword ptr [r12 + 0x100]');op(0xe89fe1,'rcx, qword ptr [r12 + 0x100]')
    for a in (0x3aabb22,0x3aabb29,0x3aabb30):check(read(a).mnemonic=='mov','extra default store')
    check(read(0x3aabb18).operands[1].imm==0x0606060606060606,'client default 6')
    direct(0xe5de44,0x151d2e0);direct(0x151d2e0,0x4339e80);direct(0xe5dea5,0x151d710);direct(0x151d710,0x433bbc0)
    op(0x4339eb4,'byte ptr [rsp + 0x2f], 1');op(0x433bc0c,'al, 2')
    op(0x433bc3b,'rbx');op(0x433bc3e,'rsi');direct(0x433bc41,0x433bc20)
    for a in (0x4339ed1,0x4339eed,0x4339f09,0x4339f25,0x4339f45,0x4339f65,0x4339f88,0x433bc32):op(a,'qword ptr [rax + 0x28]')
    for key,e in doc['base0_tag_cases'].items():
        tb=0x14d0184; c=e['cell']; check(c['file_offset']==tb+int(key)*4 and off(va(tb)+struct.unpack('<i',checked_blob(c))[0])==e['arm'],'base type dispatch')
        check(off(rip(e['install_lea']))+16==e['vtable_slot_2']['file_offset'] and off(cell(e['vtable_slot_2']))==e['entry'],'base type vslot')
        if e['entry']!=e['reader']:direct(e['entry'],e['reader'])
    for code,x in prior.items():
        root=x['helper']['root']; origin=0xe0 if root==0x151d9b0 else 0xe7
        u=read(x['member_use']);check(u.mnemonic=='movsx' and u.operands[1].size==1 and x['object_path']==[0x100,origin+u.operands[1].mem.disp],('frozen signed load',code))
        check(any(e['target']==root for e in x['gate']['direct_rel32']),'gate → helper');
        for g in (x['gate'],x['helper']):
            if g.get('cell'):
                c=g['cell'];a=c['offset'];r=bytes.fromhex(c['bytes']);check(b[a:a+4]==r and off(va(c['table'])+int.from_bytes(r,'little',signed=True))==g['arm'],'frozen rel32 cell')
            for e in g['direct_rel32']:
                check(e['bytes']==bytes(read(e['offset']).bytes).hex(),'frozen rel32');direct(e['offset'],e['target'])


def reverse_paths(layers, start, bound, minimum):
    """Backward DP, no parser decisions (builder uses forward prefix sums)."""
    links=[]; follow=[]
    for ordinal in range(len(layers)-1,-1,-1):
        suffix=[0]*(len(follow)+1); p=[a for a,_ in follow]
        for j in range(len(follow)-1,-1,-1):suffix[j]=suffix[j+1]+follow[j][1]
        f=[]
        for a in sorted(layers[ordinal]):
            if a+minimum>bound or (ordinal==0 and a!=start):continue
            w=suffix[bisect_left(p,a+minimum)] if ordinal+1<len(layers) else 1
            if w:f.append((a,min(1_000_000,w)))
        links.append(f);follow=f
        if not f:return 0,None
    n=min(1_000_000,sum(w for _,w in follow)); t=[]; a=start-minimum
    if n==1:
        for f in reversed(links):
            a=next(x for x,w in f if x>=a+minimum and w);t.append(a)
    return n,t


def boundaries(b,side,m):
    rule={6:255,7:255,8:255,9:255,11:0,13:0,14:0,15:0} if side=='client' else {6:0,7:0,8:0,9:1,19:1,43:1}
    mi=25 if side=='client' else 238
    n=uint(b,8);strong=[[] for _ in range(n)];weak=[[] for _ in strong];counts=[]; buf=np.frombuffer(b,np.uint8)
    for r in range(4):
        ar=np.arange(12+r,len(b)-max(rule),4);v=np.ndarray((len(ar),),'<u4',buffer=b,offset=12+r,strides=(4,)); fl=(v<n)
        hist=[int(fl.sum())]
        for k,(d,code) in enumerate(rule.items(),1):
            fl &= (buf[ar+d]==code)
            if k in (4,len(rule)):
                for ordinal,a in map(tuple,np.c_[v[fl],ar[fl]].tolist()): (weak if k==4 else strong)[ordinal].append(a)
                hist.append(int(fl.sum()))
        counts.append(hist)
    check(counts==m['candidates_by_alignment'] and histogram(np.array([len(g) for g in strong]))==m['layer_histogram'],'data-only candidate census')
    npath,t=reverse_paths(strong,12,len(b),mi)
    check(npath==m['strong']['paths']==1 and reverse_paths(weak,12,len(b),mi)[0]==m['weak']['paths'],'reverse DP')
    check(reverse_paths(strong,12,len(b),4)[0]==m['identity_min4']['paths']==1,'signature DP without row span prior')
    for foot,a in m['footer_sensitivity'].items(): check(reverse_paths(strong,12,len(b)-int(foot),mi)[0]==a['paths'],('footer',foot))
    for head,a in m['header_sensitivity'].items(): check(reverse_paths(strong,int(head),len(b),mi)[0]==a['paths'],('header',head))
    return t


def main_ids(b, info):
    # t57 fixed tail positions, independently chosen backward with strict UID increase;
    # use two bounds (earliest and latest) rather than the builder's path-count algorithm.
    n=uint(b,8); g=[[] for _ in range(n)]
    for k in range(4):
        x=np.frombuffer(b,'<u4',(len(b)-k)//4,k)
        i=np.flatnonzero((x[:-2]<n)&(x[1:-1]>0)&(x[1:-1]==x[2:]))
        for o,a,u in np.column_stack((x[i],4*i+k,x[i+1])).tolist():
            if 13<=a<=len(b)-21:g[o].append((a,u))
    f={(len(b)-21,uint(b,len(b)-17)):[None]}; layers=[f]
    check(next(iter(f)) in g[-1],'main last triple')
    for a in reversed(g[:-1]):
        f={p:[q for q in f if q[0]>=p[0]+12 and q[1]>p[1]] for p in a}
        f={p:q for p,q in f.items() if q};check(f,'main DP disconnect');layers.append(f)
    check(len(f)==1,'main first ambiguous');p=next(iter(f));r=[]
    for f in reversed(layers):
        r.append(p);check(len(f[p])==1,'main main path not unique');p=f[p][0]
    at,uid=np.asarray(r,dtype=np.int64).T; a=np.c_[np.arange(n),uid,uid].astype('<u4')
    check(sha(a.tobytes())==info['identity_census']['identity_sha256'],'main t57 triple digest');return at,uid


def inspect_rows(b, limits, full, *, external_old=False):
    # Parse each *bounded* DP interval independently. Never use the next row to pad a short read.
    coords=[]; summary=Counter(); d=memoryview(b)
    for i,(a,z) in enumerate(zip(limits,limits[1:])):
        p=a
        def step(n):
            nonlocal p
            o=p;p+=n
            check(n>=0 and p<=z,('row transfer outside DP frame',i,o,n,z));return o
        def read(n=1, signed=False):
            o=step(n);return int.from_bytes(d[o:p],'little',signed=signed)
        def observed(n,want):
            o=p;v=read(n);check(v in want,('unexpected branch/tag',i,o,v));return v
        def text():step(read(4))
        check(read(4)==i,('ordinal',i,a)); ep=ap=bp=apv=bpv=-1
        if full:
            step(3);step(4*read(2));step(5+1+4+24)
            if observed(1,(0,1)):step(24)
            step(2+4+1+4+4)
            if observed(1,(0,1)):ep=step(19)+4
            step(5)
            for _ in range(2):
                observed(1,(3,));step(20)
            apv=observed(1,(2,));ap=step(7);bpv=observed(1,(3,));bp=step(15)
            step(4+8);step(4 if external_old else 5);step(8)
            step(22*read(1,True));step(10*read())
            if observed(1,(0,1)):
                observed(1,(1,));step(24);step(4*read())
            observed(1,(0,));observed(1,(0,));observed(1,(0,));observed(4,(0,))
            for _ in range(read(2)):
                observed(1,(2,));step(10)
            observed(1,(0,));step(2)
        yp=step(2);cp=step(4);step(2);text()
        for _ in range(read()):observed(1,(1,));step(12);step(14)
        step(8)
        if full:
            step(read(2,True)*(1+8+3+8));step(read(1,True)*6);step(4);step(12)
            for _ in range(read(2)):
                t=read();summary[t]+=1
                if t==9:
                    step(8+2+8+2)
                    for _ in range(4):text()
                elif t==16:step(read(1,True)*4)
                elif t==38:
                    for _ in range(read(4)):
                        observed(1,(1,));observed(4,(0,));step(12+2);observed(4,(0,))
                elif t in (4,5,6,7,37):
                    chunks={4:(8,2,4,4,4,2,1,4,4,1,4,1,4),5:(8,4,1,1,4,4,1,1),6:(8,4,4,1,1,1),7:(8,4,4,4,4),37:(4,1,1,1,1,8,4,4,1,1,1)}
                    step(sum(chunks[t]))
                else:raise Failure(('unknown base0 arm',i,p-1,t))
            if observed(1,(0,1)):
                observed(4,(2,)); n=read(4)
                for _ in range(n): observed(2,(3,));step(10)
        check(p==z,('replay frame endpoint',i,a,p,z))
        coords.append([a,z,yp,cp,ep,ap,bp,apv,bpv])
    return np.asarray(coords),{str(k):v for k,v in summary.items()}


def getvalues(b,points,width,signed=False):
    p=points[points>=0]; buf=np.frombuffer(b,np.uint8); span=buf[p[:,None]+np.arange(width)].copy(); return span.view(f'<{"i" if signed else "u"}{width}').ravel()


def first(b,points,keys,i,w):
    p=int(points[i]);return dict(ordinal=int(i),uid=int(keys[i]),absolute=p,raw=b[p:p+w].hex() if p>=0 else None)


def compare_prof(b,p,k,w,x,prof):
    live=np.flatnonzero(p>=0)
    check((prof['wire'],prof['absent'])==(len(x),len(p)-len(x)) and prof['coordinate_sha256']==cd(p) and prof['value_sha256']==sha(x.tobytes()),'profile digests/counts')
    check(histogram(x)==prof['histogram'] and prof['zero']==int((x==0).sum()),'histogram/zero')
    check(prof['signed_minus_one']==(int((x==-1).sum()) if w==1 else None) and prof['raw_ffffffff']==(int((x==0xffffffff).sum()) if w==4 else None),'sentinel counts')
    check(prof['first']==(first(b,p,k,live[0],w) if len(live) else None),'first raw witness')


def verify():
    chain=j(HERE/'chain.json'); rows=j(HERE/'rows_extra3.json'); fmap=j(HERE/'field_map_r3.json')
    manifest={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']}
    for p,v in chain['frozen_inputs'].items():
        check(sha((ROOT/p).read_bytes())==v and (not p.startswith('evidence/') or manifest[p]==v),('frozen sha',p))
    check({MASTER,BIG} <= set(chain['frozen_inputs']),'minimum snapshot evidence')
    t57=j(ROOT/'scratch/t57/out/field_map.json'); slot=j(ROOT/'scratch/t57/out/field_slots.json')
    t63=j(ROOT/'scratch/t63/out/field_map_r2.json'); old=j(ROOT/'scratch/t63/out/projections.json')
    prior={x['code']:x['projection'] for x in old['occurrences'] if (x.get('projection') or {}).get('family')=='cnst_extra'}
    check(len(prior)==22,'frozen 22')
    pe_check(chain,prior)
    raw=load_raw(rows['archives']); ds={}; ids={}
    check(chain['routes']['split']['member_paths']==[f'{s}_db/table_extra_3.dat' for s in SIDES],'confirmed names')
    for s,plen in zip(SIDES,(13053908,35009248),strict=True):
        r=rows['envelopes'][s]; b=raw[s,'extra_3']; server=s=='server'; m=raw[s,'3']
        check(len(b)==plen==r['payload'] and uint(b,8)==uint(m,8)==r['count']==N and r['header']==12 and r['footer']==0 and r['body']==plen-12,'row envelope')
        check(sha(m)==slot['archives'][s]['members']['3']['payload_sha256'],'t57 member payload')
        check(next(x for x in slot['slots'] if x['key']=='base_ba')['profiles'][s]['histogram']=={'0':N},'main +ba frozen mode')
        ids[s]=main_ids(m,slot['envelopes'][s]); uid=ids[s][1]
        ends=boundaries(b,s,r['data_dp'])+[len(b)]; ar, tag=inspect_rows(b,ends,server); ds[s]=ar
        check(len(ar)==N and ar[0].tolist()==r['first'] and ar[-1].tolist()==r['last'] and cd(ar)==r['replay_sha256'],'row spans and all coordinates')
        check([int((ar[:,1]-ar[:,0]).min()),int((ar[:,1]-ar[:,0]).max())]==r['width'],'min/max row lengths')
        check(cd(np.c_[np.arange(N),uid])==r['ordinal_uid_sha256'],'ordinal to UID relation')
        if server:check(tag==r['branch_histograms']['base0 type'],'virtual replay tag census')
        x,y=(getvalues(b,ar[:,0]+p,4) for p in (4,8));check(int(((x!=uid)|(y!=uid)).sum())==r['width_negative']['failures']==N and b[12:26].hex()==r['width_negative']['first']['raw'],'main triple rejected as extra identity')
        check(np.all(ar[:,0]+4==ar[:,2]) if not server else np.all(ar[:,5]==ar[:,0]+132+19*(ar[:,4]>=0)),'absolute formula check')
        compare_prof(b,ar[:,3],uid,4,getvalues(b,ar[:,3],4),r['unsigned32_control_cc'])
        check(r['unsigned32_control_cc']['raw_ffffffff']==N and r['unsigned32_control_cc']['zero']==0,'all-ones vs zero dword control')
        for mode,version in [(not server,False)]+([(True,True)] if server else []):
            try:inspect_rows(b,ends[:2],mode,external_old=version)
            except Failure:pass
            else:raise Failure(('swapped mode/version fits first row',s,version))
    uid=ids['client'][1];check(np.array_equal(uid,ids['server'][1]) and len(np.unique(uid))==N,'UID join')
    left=raw['client','extra_3']; right=raw['server','extra_3']; rr=ds['server']; lr=ds['client']; keys=np.argsort(ids['server'][1]); match=keys[np.searchsorted(ids['server'][1][keys],uid)]
    check(np.array_equal(ids['server'][1][match],uid),'UID search')
    fields=j(ROOT/MASTER); allowable=sorted(int(x['enum']) for x in fields['enums']['cnst']['values']); doc=fmap['scoped_enum']
    check(allowable==[0,1,2,3,4,6]==doc['allowed'] and doc['values']==fields['enums']['cnst']['values'],'frozen enum definition')
    schema=fields['entities']['club.xml'][0]['fields']; k1={r['code']:r for r in t57['fields']}; k2={r['code']:r for r in t63['fields']}
    check(len(fmap['fields'])==24 and {f['code'] for f in fmap['fields']}==set(prior)|{'Cyfn','Cebd'} and fmap['L4']==0,'24-field scope')
    club_obs=set(); grades=Counter()
    for f in fmap['fields']:
        code=f['code']; old=k1[code]; prev=k2.get(code,old); idx=old['xml_index']; wire=f['wire']; it=f['uid_pair_control']
        check(f['id']==f'E97/club.xml#club/{idx:03}' and sum(x['field']==code for x in schema)==1 and old['schema']==f['schema']==schema[idx],'frozen occurrence')
        check(f['prior']['ledger']==('E106' if code in k2 else 'E97') and prev['grade']==f['prior']['grade']=='held' and prev['first_counterexample']==f['prior']['first_counterexample'] and prev['reason']==f['prior']['reason'],'negative unchanged')
        missing=np.full(N,-1,dtype=np.int64); case=f['profiles']; w=wire['width']; fail=None; diff=None
        if code in prior:
            check(f['static_getter']==prior[code] and wire['object_path']==prior[code]['object_path'] and schema[idx]['enum_ref']=='cnst','frozen gate/path')
            offset=prior[code]['object_path'][1]; p=rr[:,0]+(132+offset-0xe0 if offset<0xe7 else 140+offset-0xe7)+19*(rr[:,4]>=0)
            q=missing; rederived=(rr[:,5]+offset-0xe0 if offset<0xe7 else rr[:,6]+offset-0xe7)
            check(np.array_equal(p,rederived) and np.all(p<rr[:,1]) and w==1 and wire['side']=='server','cnst absolute rule')
            s=getvalues(right,p,w,True); valid=np.isin(s,allowable);club_obs.update(map(int,s)); actual_diff=np.flatnonzero(s[match]!=6)
            expect=dict(value=6,equal_to_server=N-len(actual_diff),different_from_server=len(actual_diff),first_difference=first(right,p,uid,actual_diff[0],w) if len(actual_diff) else None)
            check(it['client_constructor_default_only']==expect,'full UID join to constructor default')
            bad=np.flatnonzero(~valid)
            if len(bad):fail=first(right,p,uid,bad[0],w)|{'value':int(s[bad[0]])}
        elif code=='Cebd':
            check(w==4 and wire['object_path']==[256,120,8] and wire['side']=='server' and f['static_getter']==chain['target_witnesses'][code],'Cebd metadata')
            q=missing;p=rr[:,4];s=getvalues(right,p,w);live=np.flatnonzero(p>=0)
            check(np.array_equal(p[live],rr[live,0]+88),'Cebd cursor')
            yr=s>>16; day=s&511; leap=(yr%4==0)&((yr%100!=0)|(yr%400==0))
            bad=np.flatnonzero((yr==0)|(day==0)|(day>365+leap)|((s&0xfe00)!=0))
            if len(bad):fail=first(right,p,uid,live[bad[0]],w)|{'value':int(s[bad[0]])}
            check(case['server']['calendar']==dict(year_range=[int(yr.min()),int(yr.max())],day_range=[int(day.min()),int(day.max())],default_1900_day1=int(sum(s==0x076c0001))),'calendar summary')
        else:
            check(w==2 and wire['side']=='both' and wire['object_path']==[256,216] and f['static_getter']==chain['target_witnesses'][code],'Cyfn metadata')
            q,p=lr[:,2],rr[:,2]; s=getvalues(right,p,w)
            byte=np.frombuffer(right,np.uint8); at=rr[:,0]+180+19*(rr[:,4]>=0)
            flag=at+2+22*byte[at].astype(np.int64); count=flag+8+66*byte[flag].astype(np.int64)
            check(np.array_equal(count+5+11*getvalues(right,count,2),p),'simplified server Cyfn coordinate')
            check(wire['absolute_rule']=={'client':'row_start+4', 'server':'a68+5+11*u16le[a68]; a68=f48+8+66*u8[f48]; f48=a28+2+22*u8[a28]; a28=row_start+180+19*election_present'},'published year rule')
            lo,hi=map(int,(schema[idx]['min_value'],schema[idx]['max_value']))
            for side,z,x,tp in [('client',left,getvalues(left,q,w),q),('server',right,s,p)]:
                bad=np.flatnonzero((x!=0)&((x<lo)|(x>hi)))
                check(case[side]['bad']==len(bad),'Cyfn range histogram')
                if len(bad) and fail is None:fail=first(z,tp,uid,bad[0],w)|{'value':int(x[bad[0]])}
            ck=getvalues(left,q,w); diff=np.flatnonzero(ck!=s[match]); check(np.array_equal(getvalues(left,lr[:,3],4),getvalues(right,rr[:,3],4)[match]),'unbound neighboring dword remains all-ones')
        x=getvalues(left,q,w,w==1);compare_prof(left,q,uid,w,x,case['client']);compare_prof(right,p,uid,w,s,case['server'])
        check(case['server']['bad']==len(bad),'server full-domain violator count')
        n=0 if diff is None else len(diff); paired=0 if diff is None else N
        counter=None if not n else {'client':first(left,q,uid,diff[0],w),'server':first(right,p,uid,match[diff[0]],w)}
        check(tuple(it[k] for k in ('uid_joined','both_wire','equal','different','client_station_absent','server_station_absent','first_difference'))==(N,paired,paired-n,n,N-len(x),N-len(s),counter),'same UID controls')
        check(f['first_counterexample']==(fail or counter) and f['grade']==('held' if fail or counter else 'L3'),'grade guard')
        grades[f['grade']]+=1
    comp=j(ROOT/'scratch/t59/out/field_map.json'); comp_obs=set()
    for v in comp['fields']:
        if v.get('status')=='L3' and (v.get('schema') or {}).get('enum_ref')=='cnst':
            for side in SIDES: comp_obs.update(map(int,v['domain_profiles'][side]['histogram']))
    check(doc['observed_club_wire']==sorted(club_obs) and doc['observed_comp_control']==sorted(comp_obs)==[0,1,2,4,6],'comp control only')
    check(dict(grades)==fmap['counts'],'grade census')
    f=rows['fixtures']; frozen=j(ROOT/BIG)['tables']; tf=t57['regression']
    check(sha(left)==frozen['extra_3']['source_payload_sha256']['client'],'frozen extra payload')
    years={a['candidate_order_index']:a for a in frozen['3']['field_validation']['Cyfn_named_year_checks']}
    check(len(f['year_witnesses'])==len(years)==len(tf['founded_year_fixture_only'])==14,'14 witnesses')
    for item,v in zip(f['year_witnesses'],tf['founded_year_fixture_only'],strict=True):
        i=v['row'];a,b=int(lr[i,2]),int(rr[i,2]);e=years[i]
        check(item==v|dict(uid=int(uid[i]),server_absolute=b) and a==v['absolute'] and (uint(left,a,2),uint(right,b,2))==(e['client_extra_3_u16_at_row_plus_4'],v['year']) and e['note']==v['note'],'exact year witness')
    for s in SIDES:
        b=raw[s,'3']; a=int(ids[s][0][459])+12; name_len=uint(b,a+27); p=a+31+name_len; short=b[p+4:p+4+uint(b,p)].decode('utf-8')
        check(f['liverpool'][s]==dict(ordinal=460,uid=int(uid[460]),city_ordinal=uint(b,a+17),nation_ordinal=uint(b,a+1),short_name=short)==dict(ordinal=460,uid=676,city_ordinal=1061,nation_ordinal=139,short_name='Liverpool'),'Liverpool')
    city=raw['client','2']; cityat=14+43*1061+30
    check(struct.unpack_from('<III',city,cityat)==(1061,100047,100047) and f['city_uid']==100047,'Liverpool city')
    sd=raw['server','21']; a=14+181*430
    check(struct.unpack_from('<II',sd,a)==(81044,81044) and struct.unpack_from('<III',sd,a+168)==(430,1056,1056) and f['bernabeu']==dict(ordinal=430,capacity=81044,seats=81044),'Bernabeu')
    check(uint(sd,14+181*71)==74031 and f['old_trafford']==dict(ordinal=71,wire_capacity=74031,external=74140),'Old Trafford negative')
    check(all(tf[k]==v for k,v in f['prior_negatives'].items()) and f['prior_negatives']['frozen_club_negatives']==frozen['3']['negative_results'] and f['prior_negatives']['frozen_stadium_negatives']==frozen['21']['negative_results'],'frozen negatives verbatim')
    print(f't71 independent verify PASS: 2 x {N:,} rows, 14 year witnesses, {dict(grades)}')


def selftest():
    check(reverse_paths([[12],[37,40],[62]],12,87,25)==(1,[12,37,62]),'reverse prune')
    check(reverse_paths([[12],[37],[62]],12,86,25)==(0,None),'footer control')
    check(getvalues(b'\x00\xff',np.array([0,-1,1]),1,True).tolist()==[0,-1],'i8 not u32 sentinel')
    b=bytes(12)+bytes(25);rr,_=inspect_rows(b,[12,37],False);check(rr[0,2]==16 and rr[0,3]==18,'client minimal row')
    print('t71 verifier selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true'); args=ap.parse_args()
    sys.path.append(str(OLD/'tools/python'))
    try:selftest() if args.selftest else verify()
    except Failure as e:print(f'FAIL: {e}',file=sys.stderr);return 1
    except (OSError,ValueError,KeyError,IndexError,ImportError,struct.error) as e:print(f'FATAL: {e}',file=sys.stderr);return 2
    return 0


if __name__=='__main__':sys.exit(main())