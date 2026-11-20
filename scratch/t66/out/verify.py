"""Independent t66 spot: archive entries, identity paths, two-mode item ledger and PE."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import pack, unpack_from
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
T59 = ROOT/'scratch/t59/out'
TABLES = (2,3,10,21,25)
NAMES = dict(vec30=('vec30',None), vec18=('vec18',None))
NAMES.update({f'+0x{k}':(f'obj_{k}',f'{k}_present') for k in ('a8','e0','e8','c0','c8','d0','d8')})
NAMES['+0x100'] = ('vec100',None)
LANES = {'vec18':('item.+1',), '+0xe8':('item.+2',), '+0xc0':('inner.+4','inner.+8'),
         '+0xd0':('item.+0','item.+4'), '+0xd8':('item.+0','item.+4')}
U = lambda b,p=0: unpack_from('<I',b,p)[0]
H = lambda b: sha256(b).hexdigest()
J = lambda p: json.loads(p.read_bytes())


class Mismatch(Exception):
    pass


def need(test, label):
    if not test:
        raise Mismatch(label)


def archive(path, side, accepted, extra):
    sys.path.insert(0, str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    def inflate(data):
        need(data[:4]==b'\x28\xb5\x2f\xfd', 'zstd tag')
        f=z.ZstdDecompressor().decompressobj(); out=f.decompress(data)
        need(f.eof, 'zstd EOF')
        return out,len(data)-len(f.unused_data)
    blob=path.read_bytes()
    shell=bytes.fromhex('0201666d662e080000')
    toc,base=(v+17 for v in unpack_from('<QQ',blob,17))
    need(H(blob)==accepted['archive_sha256'] and base==34 and blob[8:17]==blob[toc:toc+9]==shell,'archive envelope')
    toc_raw,n=inflate(blob[toc+9:]); need(toc+9+n==len(blob),'directory frame EOF')
    p=0; records={}
    def pull(w):
        nonlocal p
        v=toc_raw[p:p+w]; need(len(v)==w,'directory truncated'); p+=w
        return v
    def txt():
        return pull(U(pull(4))).decode('utf-8')
    def tree(parent,depth=0):
        need(depth<40,'directory recursion')
        folder=parent/txt()
        for _ in range(U(pull(4))):
            name=(folder/(txt()+txt())).as_posix()
            a,w,n,_,_=unpack_from('<5Q',pull(40))
            need(name not in records and '..' not in PurePosixPath(name).parts,(name,'invalid directory entry'))
            records[name]=[base+a,w,n]
        for _ in range(U(pull(4))):
            tree(folder,depth+1)
    tree(PurePosixPath())
    need(p==len(toc_raw) and len(records)==accepted['entries'],'directory closure')
    raw={}
    for t in TABLES:
        name=f'{side}_db/table_{t}.dat'; a,w,n=records[name]; end=a+w
        bound=min((x for x,_,_ in records.values() if x>a),default=toc)
        e=accepted['members'][str(t)]
        need(e['member']==name and e['range']==[a,end] and base<=a<end<=bound==e['bound'] and e['declared_size']==n and H(blob[a:end])==e['compressed_sha256'],(name,'bounded member'))
        frames=[]; matches=[]
        while a<end:
            b,k=inflate(blob[a:end]); frames.append([a,a+k,len(b)]); a+=k
            if len(b)==n:
                matches.append(b)
        need(len(matches)==1 and frames==e['frames'],(name,'unique sized frame'))
        b,=matches; need(H(b)==e['payload_sha256'] and U(b,8)==e['count'],(name,'payload'))
        raw[t]=b
    for name,e in extra.items():
        a,w,n=records[f'{side}_db/{name}']; end=a+w
        br=min((x for x,_,_ in records.values() if x>a),default=toc)
        need(base<=a<end<=br==e['bound'] and [a,end]==e['range'] and H(blob[a:end])==e['compressed_sha256'],(name,'extra entry'))
        frames=[]; selected=[]
        while a<end:
            b,k=inflate(blob[a:end]); frames.append([a,a+k,len(b)]); a+=k
            if len(b)==n:
                selected.append(b)
        need(len(selected)==1 and frames==e['frames'] and H(selected[0])==e['payload_sha256'],(name,'extra frame'))
        raw[name]=selected[0]
    return raw,records


def aux_keys(raw,side,notes):
    b=raw['table_23.dat']; meta=notes['23']; n=U(b,8)
    need(len(b)==13+14*n+9 and H(b)==meta[f'{side}_sha256'] and n==meta[f'{side}_count'],'t23 accepted envelope')
    pts=list(range(15,15+14*n,14))
    ids={23:witnesses(b,pts,dict(count=n,identity_sha256=meta['identity_trace_sha256']))}
    if side=='client':
        return ids
    b=raw['table_24.dat']; aux=raw['table_extra_24.dat']; meta=notes['24']; n=U(b,8)
    need(H(b)==meta['server_sha256'] and H(aux)==meta['sidecar_sha256'] and len(aux)==12+82*n and U(aux,8)==n==meta['server_count']==meta['sidecar_ordinal_count'],'t24 entries')
    need(all(U(aux,12+82*i)==i for i in range(n)),'t24 auxiliary ordinal witnesses')
    points=identity_path(b,[14,9,12,None,True,False],team=True)
    first=13; d={}; h=sha256(); selectors=Counter()
    for i,at in enumerate(points):
        x,u,v=unpack_from('<III',b,at)
        need(x==i and u==v and b[first] in (10,11) and at>first,(i,'t24 triple'))
        d[i]=u; selectors[b[first]]+=1; h.update(pack('<4I',i,first,at,u)); first=at+12
    need(len(set(d.values()))==n and first==len(b)-9 and h.hexdigest()==meta['identity_trace_sha256'] and histogram(selectors.elements())==meta['selector_counts'],'t24 raw ordinal digest')
    ids[24]=d
    return ids


def identity_path(b, option, team=False):
    """Raw triple census, backward DP, only the accepted t59 option."""
    import numpy as np
    start,footer,width,lookahead,nonzero,increasing=option
    n=U(b,8); end=len(b)-footer
    g=[[] for _ in range(n)]
    for shift in range(4):
        a=np.frombuffer(b,dtype='<u4',offset=shift,count=(len(b)-shift)//4)
        for x in np.flatnonzero((a[:-2]<n)&(a[1:-1]==a[2:])):
            at=4*int(x)+shift; uid=int(a[x+1]); i=int(a[x])
            if at>=start and at+width<=end and (not nonzero or uid) and (lookahead is None or b[at+12] in lookahead):
                if team and (uid>U(b,len(b)-4) or (i<n-1 and b[at+12] not in (10,11))):
                    continue
                if i!=n-1 or at+width==end:
                    g[i].append((at,uid))
    links=[]; nexts=[]
    for i in range(n-1,-1,-1):
        d={}; here=[]
        for a,u in g[i]:
            if i==n-1:
                d[a]=None; here.append((a,u,1)); continue
            total=0
            for z,v,c in nexts:
                if z>=a+width+team and (not increasing or u<v):
                    total=min(2,total+c); d[a]=z
            if total:
                here.append((a,u,total))
        links.append(d); nexts=here
    need(sum(c for _,_,c in nexts)==1,'identity path not unique')
    a=nexts[0][0]; points=[]
    for m in reversed(links):
        points.append(a); a=m[a]
    return points


def witnesses(b, points, acceptance):
    ids={}; digest=sha256()
    for i,a in enumerate(points):
        x,u,v=unpack_from('<III',b,a); need((x,v)==(i,u) and u>0,(i,a,'identity'))
        ids[i]=u; digest.update(b[a:a+12])
    need(len(ids)==U(b,8)==len(set(ids.values()))==acceptance['count'] and digest.hexdigest()==acceptance['identity_sha256']
         and points[-1]+12==len(b)-9 and b[-9:-4]==b'\0\0\0\0\1','target identity census')
    return ids


def item_ledger(name,b,p,limit):
    """Independent struct model; returns end, serialized count position, count, child ledger and fields."""
    fields=defaultdict(list); out=[]
    def scalar(fmt,key):
        nonlocal p
        w={'b':1,'B':1,'h':2,'H':2,'i':4,'I':4}[fmt]
        need(p+w<=limit,(name,p,'short field',w))
        v=unpack_from('<'+fmt,b,p)[0]; fields[key].append((p,w,v)); p+=w
        return v
    fp={'vec30':'I','vec18':'i','+0x100':'h','+0xe8':'I','+0xc0':'I'}
    if name in ('+0xc0','+0xe8','+0xc8'):
        scalar('I' if name=='+0xe8' else 'B','tag' if name=='+0xc8' else 'version')
    ca=p if name in fp else None
    n=scalar(fp[name],'count') if ca is not None else (4 if name=='+0xc8' else 1)
    mini={'vec30':2,'vec18':8,'+0x100':5,'+0xe8':10,'+0xc0':6,'+0xc8':6,'+0xd0':15,'+0xd8':15}[name]
    need(0<=n<=(limit-p)//mini,(name,ca,'invalid count',n))
    for _ in range(n):
        a=p; children=[]
        if name=='+0xc0':
            scalar('B','item.tag'); scalar('B','item.+1'); m=scalar('I','inner_count')
            need(m<=(limit-p)//12,(name,p,'invalid inner count',m))
            for _ in range(m):
                st=p; scalar('B','inner.tag')
                for idx,fmt in ((1,'B'),(2,'B'),(3,'B'),(4,'I'),(8,'I')):
                    scalar(fmt,f'inner.+{idx}')
                children.append([st,p])
        elif name=='vec18':
            tag=scalar('b','item.tag')
            for idx,fmt in ((1,'I'),(5,'H'),(7,'B'),*(((8,'B'),) if tag>=2 else ())):
                scalar(fmt,f'item.+{idx}')
        elif name=='+0xe8':
            tag=scalar('h','item.tag')
            for fmt,key in zip('IBB'+('H' if tag>=2 else 'B')+'B'+('B' if tag>=3 else ''),
                               ('item.+2','item.+6','item.+7','item.+8','item.tail0','item.tail1')):
                scalar(fmt,key)
        else:
            layout={'vec30':'H','+0x100':'BHH','+0xc8':'BBBBBB','+0xd0':'IIBBIB','+0xd8':'IIBBIB'}[name]
            for fmt in layout:
                scalar(fmt,f'item.+{p-a}')
        out.append([a,p,children])
    return p,ca,n,out,fields


def scan_rows(b,witness,side,frozen):
    # Identity bounds are solved independently above, not read from census.json.
    # Reuse frozen outer execution order and fixed widths. No other field replay.
    templates={tuple(t['sequence']):t['rows'] for t in frozen['execution_templates'][side]}
    template=list(dict.fromkeys(x for seq in templates for x in seq))
    # Use union order from t59's slots (execution_index excludes unobserved arms).
    table={d['key']:d for d in frozen['slots']}
    template.sort(key=lambda k:table[k]['execution_index'])
    inverse={slot:k for k,(slot,_) in NAMES.items()}
    seen=Counter(); cols=defaultdict(list); rows=[]; ledger={k:[] for k in NAMES}
    vals={k:defaultdict(list) for k in NAMES}
    p=frozen['envelopes'][side]['header']
    conditional={slot:flag for slot,flag in NAMES.values() if flag}; conditional['m14c']='wbcl_present'
    for i,ident in enumerate(witness):
        start=p; flags={}; events={}; seq=[]
        for slot in template:
            if slot in conditional and flags[conditional[slot]][1]==0:
                continue
            a=p
            if slot in inverse:
                name=inverse[slot]; flag=NAMES[name][1]
                p,c,n,it,fs=item_ledger(name,b,p,ident)
                events[name]=[i,flags[flag][0] if flag else None,a,p,c,n,it]
                for k,v in fs.items():
                    vals[name][k].extend((i,*x) for x in v)
            else:
                w=table[slot]['nominal_width']; p+=w
                if slot.endswith('_present'):
                    flags[slot]=(a,b[a]); need(b[a] in (0,1),(side,i,slot,'not 0/1'))
                if slot=='identity':
                    need(a==ident and w==12,(side,i,a,ident,'identity boundary'))
                else:
                    need(p<=ident,(side,i,slot,a,p,'past identity'))
            seq.append(slot); cols[slot].append((i,a,p-a))
        if side=='server':
            for name,(_,flag) in NAMES.items():
                ledger[name].append(events[name] if name in events else [i,flags[flag][0],None,None,None,None,[]])
        rows.append([start,ident,p,U(b,ident+4)]); seen[tuple(seq)]+=1
    env=frozen['envelopes'][side]
    need(seen==templates and b[p:].hex()==env['footer_hex'] and p-start>0 and len(b)==env['payload'],(side,'template and EOF'))
    need(H(b''.join(pack('<III',a,z,v) for a,_,z,v in rows))==env['row_trace_sha256'],(side,'row trace digest'))
    for slot,d in table.items():
        points=cols[slot]; prof=d['profiles'][side]
        need(len(points)==prof['events'] and sum(w for _,_,w in points)==prof['bytes'],(side,slot,'number of transfers'))
        if points:
            need(H(b''.join(pack('<III',*x) for x in points))==prof['coordinate_sha256'] and
                 H(b''.join(b[a:a+w] for _,a,w in points))==prof['content_sha256'],(side,slot,'t59 coordinates/data'))
    return rows,ledger,vals,cols


def histogram(xs):
    return {str(k):v for k,v in Counter(xs).items()}


def endpoints(spans):
    return [min(a for a,_ in spans),max(z for _,z in spans)] if spans else None


def probe(points,ids,b):
    # List comprehensions give an independent aggregation and first-event selection.
    rev={v:k for k,v in ids.items()}; live=[pt for pt in points if pt[3]!=0xffffffff]
    hits=[pt for pt in live if pt[3] in ids]; uid=[pt for pt in live if pt[3] in rev]
    cl=[pt for pt in uid if pt[3] in ids and rev[pt[3]]!=pt[3]]
    out=dict(live=len(live),all_ones=len(points)-len(live),ordinal_hits=len(hits),uid_hits=len(uid),
             different_target=len(cl),zero_live=sum(pt[3]==0 for pt in live))
    for k,it in [('first_live',iter(live)),('first_ordinal_miss',(p for p in live if p[3] not in ids)),
                 ('first_uid_miss',(p for p in live if p[3] not in rev)),('first_different_target',iter(cl))]:
        pt=next(it,None)
        if pt:
            row,a,w,v=pt
            out[k]=dict(row=row,at=a,raw=b[a:a+w].hex(),value=v,ordinal_to_uid=ids.get(v),uid_to_ordinal=rev.get(v))
    return out


def audit_static(doc,source):
    import capstone as cs
    import pefile
    path=Path(source['editor']); raw=path.read_bytes()
    need(doc['editor']==path.as_posix() and H(raw)==doc['sha256']==source['editor_sha256'],'editor provenance')
    pe=pefile.PE(data=raw,fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
    ds=cs.Cs(cs.CS_ARCH_X86,cs.CS_MODE_64); ds.detail=True
    va=lambda o: base+pe.get_rva_from_offset(o)
    off=lambda v: pe.get_offset_from_rva(v-base)
    decoded={}
    for r in doc['ranges']:
        a,z=r['range']; ins=list(ds.disasm(raw[a:z],va(a)))
        need([[i.address-va(a)+a,i.address,i.bytes.hex(),i.mnemonic,i.op_str] for i in ins]==r['instructions'],(a,'PE raw instructions'))
        decoded.update((i.address-va(a)+a,i) for i in ins)
    # Independent assertions of the mode edge and the nested reader entrypoints.
    for s,t in [(0xeb73a0,0xeb7a21),(0xeb770e,0xeb7dbe),(0xeb7544,0xeb75d7),(0xeb76d2,0xeb770b),
                (0xed0a40,0x3b3f0d0),(0x3b3f101,0xeb7000),(0xeb750e,0xeb7e50),(0xeb7e50,0x3b1f030),
                (0xeb7e1b,0x9f7c30),(0x9f7c30,0x37b8710),(0xeb7783,0x155b450),(0x155b450,0x4387ab0),(0x4387b46,0x155c120),
                (0xeb7804,0x155ce40),(0x155ce40,0x438b680),(0x438b6ba,0x155d010),(0xeb7860,0x155de30),
                (0x155de30,0x438e850),*((x,0x155dad0) for x in (0x438e880,0x438e890,0x438e8a0,0x438e8b3)),
                (0x155dad0,0x438bfd0),(0xeb78f2,0xeb5580),(0xeb7961,0xeb5580),(0xeb5580,0x3b1e790),
                (0xeb79f9,0x9f9840),(0x9f9840,0x37be3a0),(0x37b879c,0x37b87bd),(0x155c378,0x155c3a0),(0x155c3f3,0x155c419)]:
        need(off(decoded[s].operands[0].imm)==t,(hex(s),'branch/call target'))
    widths={0x3b1f05f:4,0x3b1f0d2:2,0xeb7dd2:4,0xeb7982:2}
    for sites,ws in [((0x37b8731,0x37b874c,0x37b8768,0x37b8784,0x37b87b4),(1,4,2,1,1)),
                     ((0x4387ae0,0x155c152,0x155c2f9,0x155c31a,0x155c33d,0x155c360,0x155c38d,0x155c3b5,0x155c3e0,0x155c40c),(4,4,2,4,1,1,2,1,1,1)),
                     ((0x438b6a1,0x155d053,0x155d244,0x155d268,0x155d28d,0x155d412,0x155d433,0x155d454,0x155d475,0x155d499,0x155d4b9),(1,4,1,1,4,1,1,1,1,4,4)),
                     ((0x438e871,0x438bff1,0x438c00c,0x438c028,0x438c044,0x438c060,0x438c089),(1,)*7),
                     ((0x3b1e7e2,0x3b1e7fc,0x3b1e84c,0x3b1e85f,0x3b1e87e,0x3b1e8b2),(4,4,1,1,4,1)),
                     ((0x37be3c0,0x37be3db,0x37be404),(1,2,2))]:
        widths.update(zip(sites,ws,strict=True))
    for s,w in widths.items():
        i=decoded[s]; need(i.mnemonic=='call' and i.op_str=='qword ptr [rax + 0x28]',(hex(s),'transfer'))
        prep=[decoded[x] for x in sorted(decoded) if s-16<=x<s and decoded[x].op_str.startswith('r8d, ')]
        need(prep and prep[-1].op_str==f'r8d, {w}',(hex(s),'width',w))
    cell=source['comp']['slots']['19']; need(unpack_from('<Q',raw,cell['file_offset'])[0]==va(0xed0a40),'COMP slot 19')
    need(decoded[0xeb739d].op_str=='r13b, r13b' and decoded[0x3b3f0f9].op_str=='byte ptr [rsp + 0x38], 0', 'mode and alternate flag are separate')
    rip=lambda s: decoded[s].address+decoded[s].size+next(o.mem.disp for o in decoded[s].operands if o.type==cs.CS_OP_MEM)
    ctx=rip(0xfb19b)
    need(ctx==rip(0xeb887f)==rip(0xeb87b4) and rip(0xeb88b1)==ctx+0x98 and rip(0x3b1e7c0)==ctx+0x90,'resolver context slots')
    for s,t in ((0xfb1a2,0xefee00),(0xefeea5,0xf026c0),(0xf04064,0xff9910),(0xf041a3,0xff9910),(0xeb88cb,0xf7e440),(0xf7e440,0x3bf3460),(0xeb87c4,0xf7f440),(0xf7f440,0x3bf70c0),(0xeb91bb,0x9f7b50),(0x9f7b50,0x37b81b0)):
        need(off(decoded[s].operands[0].imm)==t,(hex(s),'ref route'))
    for s,text in ((0xf0405c,'edx, 0x17'),(0xf0419b,'edx, 0x18'),(0xf04184,'qword ptr [r14 + 0x90], rdi'),
                   (0xf042c3,'qword ptr [r14 + 0x98], rdi'),(0x3ceb8e2,'dword ptr [rsi + 0x54], edi'),(0x37b81ee,'eax, dword ptr [rax + 8]')):
        need(decoded[s].op_str==text,(hex(s),'table/identity sink'))


def verify():
    d=J(HERE/'collections.json'); c=J(HERE/'census.json'); f=J(T59/'field_slots.json')
    need((c['identity_width'],c['header_width'],c['footer_width'],c['envelopes'])==(12,13,9,f['envelopes']),'t59 envelope metadata')
    manifest={r['path']:r['sha256'] for r in J(ROOT/'evidence/MANIFEST.json')['files']}
    need(all(H((ROOT/k).read_bytes())==v==manifest[k] for k,v in f['frozen'].items()),'t59 frozen manifest')
    rs=sum(x['grade']=='L3' for col in d['collections'].values() for x in col['reference_lanes'].values())
    need(d['L3_reference_lanes']==rs==4,'reference grade subtotal')
    for name in ('field_slots.json','field_map.json','REPORT.md'):
        need(H((T59/name).read_bytes())==d['t59_input_sha256'][name],(name,'t59 preservation'))
    need(d['t59_negatives']==J(T59/'field_map.json')['fixtures']['falsified_t01f'] and d['mode_tests']==f['external_modes'],'negative controls unchanged')
    need(d['L4']==0 and d['status']=='partial' and d['independent_member_binding'] is None and d['L3_grammars']==7 and set(d['collections'])==set(NAMES),'scope/grades')
    audit_static(d['static'],f['source'])
    basedir=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if basedir.drive.upper()=='Z:' or basedir.resolve().drive.upper()=='Z:':
        raise ValueError('Z: forbidden')
    paired={}; common={}; diagnostics={}
    notes=d['extra_identity_domains']; prior=J(ROOT/'scratch/t39/out/fields_tchl.json')['target_domains']
    need(notes=={k:prior[k] for k in ('23','24')},'accepted t39 key evidence')
    for side in ('client','server'):
        raw,entries=archive(basedir/f'{side}_db.dat',side,f['archives'][side],d['extra_identity_entries'][side]); need(entries==d['directory'][side],'entry census')
        need(f'{side}_db/table_extra_25.dat' not in entries and f'{side}_db/table_for_old_save_25.dat' in entries,'25 sidecar/legacy distinction')
        b=raw[25]; option=f['framing_options']['wire_triple']; w=identity_path(b,option)
        rows,ledger,vals,cols=scan_rows(b,w,side,f)
        need(c['sides'][side]==dict(rows=rows,collections=ledger),(side,'per-row and per-item ledger'))
        a=f['target_identity_domains'][side]
        t10=J(ROOT/'scratch/t47/out/cursor_nation_tax.json')[side]
        need(H(raw[10])==t10['payload_sha256'],'table 10 exact t47 witness source')
        t3=raw[3]; pts=[]
        if side=='client':
            pts=identity_path(t3,[13,9,12,[0,12],True,True])
        else:
            p=len(t3)-9
            for i,v in reversed(paired['client'][3].items()):
                p=t3.rfind(pack('<III',i,v,v),13,p); need(p>=0,('t3',i,'latest')); pts.append(p)
            pts.reverse(); p=13
            for i,x in enumerate(pts):
                need(t3.find(pack('<III',i,paired['client'][3][i],paired['client'][3][i]),p,len(t3)-9)==x,('t3',i,'earliest/latest')); p=x+12
        at={25:w,10:[r['identity_at'] for r in t10['rows']],3:pts}
        for t,stride in [(2,43),(21,38 if side=='client' else 181)]:
            n=U(raw[t],8); need(13+n*stride+9==len(raw[t]),(side,t,'fixed target envelope'))
            at[t]=range(13+stride-12,13+n*stride-11,stride)
        ids={t:witnesses(raw[t],at[t],a[str(t)]) for t in TABLES}; ids.update(aux_keys(raw,side,notes))
        paired[side]={t:data for t,data in ids.items() if t!=24}
        need(d['target_identity_domains'][side]=={str(t):a[str(t)] for t in TABLES},(side,'target domains'))
        common[side]=[(b[r[0]:r[0]+71],b[r[2]-56:r[2]]) for r in rows]
        # Force the opposite mode on row zero, with t59's first transfer positions.
        if side=='client':
            p=rows[0][0]+71+45
            diagnostics[side]=f'vec30: row 0 @{p}: invalid count {U(b,p)}'
        else:
            p=rows[0][0]+127-12
            diagnostics[side]=f'row 0 @{p}: identity {unpack_from("<III",b,p)}'
        for k,events in ledger.items():
            slot,flag=NAMES[k]; rec=d['collections'][k]; s=rec['sides'][side]
            spans=[(a,z) for _,_,a,z,*_ in events if a is not None]
            flags=[q for _,q,*_ in events if q is not None]; items=[x for *_,its in events for x in its]
            inner=[z for _,_,ch in items for z in ch]
            histograms={key:dict(count=len(p),minimum=min(x[3] for x in p),maximum=max(x[3] for x in p),histogram=histogram(x[3] for x in p)) for key,p in vals[k].items()}
            need(rec['slot']==slot and rec['presence_slot']==flag and rec['inline_member']=='table_25.dat' and rec['grade']==('L3' if k not in ('vec30','+0xa8','+0xe0') else 'held'),(k,'scope/slot'))
            ref_targets={'vec18':{'item.+1':24},'+0xd0':{'item.+0':23,'item.+4':23},'+0xd8':{'item.+0':23,'item.+4':23}}.get(k,{})
            probes={}
            for lane in LANES.get(k,()):
                if lane in vals[k]:
                    ts=(*TABLES,ref_targets[lane]) if lane in ref_targets else TABLES
                    probes[lane]={str(t):probe(vals[k][lane],ids[t],b) for t in ts}
            if side=='server':
                refs=rec['reference_lanes']; need(set(refs)==set(probes),(k,'reference lanes'))
                for lane,r in refs.items():
                    t=ref_targets.get(lane); jn=probes[lane].get(str(t))
                    passed=jn and jn['live']>0 and jn['ordinal_hits']==jn['live']
                    need(r['target_table']==t and r['grade']==('L3' if passed else 'held'),(k,lane,'reference grade'))
                    point=r['first_counterexample']
                    if not passed:
                        ar=vals[k][lane]; i,a,w,x=next((pt for pt in ar if pt[3]!=0xffffffff),ar[0])
                        wanted=jn.get('first_ordinal_miss') if jn else None
                        need(point==(wanted or dict(row=i,at=a,raw=b[a:a+w].hex(),value=x)),(k,lane,'first held reference'))
                    else:
                        need(point is None,(k,lane,'accepted reference'))
            need(s==dict(parent_rows=len(rows),mode_skipped_rows=0 if events else len(rows),events=len(events),payload_rows=len(spans),
                nonempty_ordinals=[i for i,_,_,_,_,n,_ in events if n],presence_histogram=histogram(b[q] for q in flags),
                presence_bounds=endpoints([(q,q+1) for q in flags]),payload_bounds=endpoints(spans),item_bounds=endpoints([(a,z) for a,z,_ in items]),
                count_histogram=histogram(n for *_,n,_ in events if n is not None),item_width_histogram=histogram(z-a for a,z,_ in items),
                items=len(items),inner_items=len(inner),inner_bounds=endpoints(inner),fields=histograms,
                ordinal_probes=probes),(side,k,'collection census and wrong-UID'))
            if side=='server':
                domains={'vec18':{'item.tag':2},'+0xe8':{'version':2,'item.tag':3},'+0xc0':{'version':1,'item.tag':1,'inner.tag':1},'+0xc8':{'tag':1,'item.+0':1},'vec30':{'count':0}}
                for lane,tag in domains.get(k,{}).items():
                    need(set(histograms[lane]['histogram'])=={str(tag)},(k,lane,'observed tag domain'))
                if rec['grade']=='held':
                    need(not items,(k,'unobserved item'))
                    i,q,a,z,*_=events[0]; a,z=(q,q+1) if q is not None else (a,z)
                    w=rec['first_counterexample']; need((w['row'],w['at'],w['raw'])==(i,a,b[a:z].hex()),(k,'first held case'))
    need(paired['server']==paired['client'] and common['server']==common['client'],'paired identities and public slices')
    for s,err in diagnostics.items():
        need(err==f['external_modes'][s]['forced_opposite_first_failure'],(s,err,'wrong mode control'))
    print('PASS verify: 2 x 7047; independent row path + bounded items, target joins, directory and PE')


def selftest():
    for tag,n in [(-2,10),(1,10),(2,11),(3,12)]:
        b=pack('<IIh',2,1,tag)+bytes(n-2)
        need(item_ledger('+0xe8',b,0,len(b))[:4]==(len(b),4,1,[[8,len(b),[]]]),'tag lengths')
        try:
            item_ledger('+0xe8',b,0,len(b)-1)
        except Mismatch:
            pass
        else:
            raise Mismatch('accepted truncated item')
    b=pack('<BIBBI',1,1,1,1,2)+(b'\1'+bytes(11))*2
    need(item_ledger('+0xc0',b,0,len(b))[3]==[[5,35,[[11,23],[23,35]]]],'nested counts')
    print('PASS selftest: tag and nested paths')


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--selftest',action='store_true')
    args=ap.parse_args()
    try:
        selftest() if args.selftest else verify()
    except Mismatch as exc:
        print(f'FAIL: {exc}',file=sys.stderr); return 1
    except Exception as exc:
        print(f'FATAL: {exc}',file=sys.stderr); return 2
    return 0


if __name__=='__main__':
    sys.exit(main())
