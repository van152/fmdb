"""Independent t55 check: PE worklist, archive members, two cursors, domains and prior fixtures."""
from __future__ import annotations
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import math
import os
from pathlib import Path, PurePosixPath
from struct import unpack_from, pack
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MASTER='evidence/fm24/reports/editor_schema/master.json'
MASTERH='7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
HEAD=bytes.fromhex('03017461642ef10d')
TAIL=bytes.fromhex('0000000001ec7ae404')
ENTRY=0x103fac0
STEPS=[0xf2ba0e,0x103fb0e,0x103fb37,0x103fe72,0x104011f,0x1040360,0x1040384,0x10403a8,0x10403cc,0x10403f0,
       0x1040414,0x1040462,0x10404d1,0x3d74e62,0x10405c7,0x10405eb,0x104060f,0x1040633,0x1040657,0x104067b,
       0x104069f,0x10406c3,0x10406e7,0x1040717,0x10407b0,0x104086c,0x1040927,0x10409f0,0x1040a14,0x1040a38,
       0x1040a5c,0x1040a80,0x1040aa4,0x1040ac8,0x1040aec,0x1040b10,0x1040b34,0x1040b58,0x1040b7c,0x3c60119]
MATCH={1:'Nnsi',4:'Nftb',11:'Ntxr',14:'Ngct',15:'Ncti',16:'Nrgi',17:'Ncpi',18:'Ncur',19:'Nsod',20:'Necf',22:'Nygn',
       23:'Nlns',24:'Nefr',25:'Nnfr',26:'Nagr',34:'Npop',37:'Nndn'}
WIDTHS=[1,4,2,4,2,4,4,4,4,4,4,4,4,4,1,4,4,4,4,1,1,4,1,1,4,4,4,4,4,4,4,4,4,4,4,4,4,2,1,12]
OFFS=[None,0x118,0x128,0x158,0x170,0x184,0x188,0x18c,0x190,0x194,0x198,0x60,0xd8,0x78,0x1cb,0xf0,0xf8,0xe8,
      0x100,0x1cc,0x1d0,0x1b4,0x1cd,0x48,0xa8,0x90,0xc0,0x1a4,0x1a8,0x1b0,0x1ac,0x1b8,0x1bc,0x1c0,0x1c4,0x17c,
      0x180,0x1c8,0x1ca,8]
VEC={2:('h',4),3:('i',4),4:('h',37),11:('i',23),12:('I',12),13:('I',14),23:('b',5),24:('i',28),25:('i',28),26:('i',12)}
REF={1:21,15:5,16:19,17:2,18:41}

class Check(Exception): pass

def require(ok, why):
    if not ok: raise Check(why)

def sha(b): return sha256(b).hexdigest()
def j(path): return json.loads(path.read_bytes())
def u(b,off=0): return unpack_from('<I',b,off)[0]
def hist(v): return {str(k):n for k,n in Counter(v).items()}


def archives(doc):
    db=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    vendor=ROOT.parent/'fm24/tools/python'
    if any(p.drive.upper()=='Z:' for p in (db,vendor)): raise ValueError('Z: forbidden')
    sys.path.append(str(vendor))
    import zstandard
    magic=bytes.fromhex('0201666d662e080000')
    def frame(buf):
        require(buf[:4]==bytes.fromhex('28b52ffd'),'Zstd magic')
        z=zstandard.ZstdDecompressor().decompressobj(); p=z.decompress(buf)
        require(z.eof and len(z.unused_data)<len(buf),'Zstd frame EOF')
        return p,len(buf)-len(z.unused_data)
    tables={}
    for side,count in (('client',31),('server',77)):
        blob=(db/f'{side}_db.dat').read_bytes(); md=doc[side]
        require(sha(blob)==md['archive_sha256'] and blob[8:17]==magic,'archive hash/magic')
        toc,base=(17+x for x in unpack_from('<QQ',blob,17))
        require(34==base==md['data_base'] and base<toc<len(blob) and blob[toc:toc+9]==magic,'TOC offsets')
        idx,k=frame(blob[toc+9:]); require(toc+9+k==len(blob),'directory frame EOF')
        q=0; entries={}
        def take(n):
            nonlocal q
            require(0<=n<=len(idx)-q,'directory bounds'); q+=n; return idx[q-n:q]
        def integer():return int.from_bytes(take(4),'little')
        def string():return take(integer()).decode('utf-8')
        def folder(parent,depth=0):
            require(depth<40,'directory depth'); here=parent/string()
            for _ in range(integer()):
                name=here/(string()+string()); lo,packed,size,_,_=unpack_from('<5Q',take(40))
                require(not name.is_absolute() and '..' not in name.parts and name.as_posix() not in entries,'directory path')
                entries[name.as_posix()]=(base+lo,packed,size)
            for _ in range(integer()):folder(here,depth+1)
        folder(PurePosixPath()); require(q==len(idx) and count==len(entries)==md['entries'],'directory count and EOF')
        ids=(2,5,10,19,21,41)
        require(set(md['members'])=={str(t) for t in ids},'member scope')
        for tid in ids:
            lo,w,size=entries[f'{side}_db/table_{tid}.dat']; hi=lo+w; d=md['members'][str(tid)]
            bound=min((i for i,*_ in entries.values() if i>lo),default=toc)
            require(base<=lo<hi<=bound and (lo,hi,bound)==(d['start'],d['end'],d['neighbor_bound']),'entry bounds')
            require(sha(blob[lo:hi])==d['compressed_sha256'],'packed SHA')
            found=[]; fs=[]; x=lo
            while x<hi:
                payload,z=frame(blob[x:hi]); cell=[x,x+z,len(payload)]; fs.append(cell); x+=z
                if len(payload)==size:found.append((payload,cell))
            require(len(found)==1 and fs==d['frames'],'unique sized frame')
            payload,f=found[0]; require(f==d['selected'] and sha(payload)==d['payload_sha256'],'payload SHA')
            tables[side,tid]=payload
    return tables


def pe_check(inv,slots):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64,CS_OP_IMM,CS_OP_MEM
    path=ROOT.parent/'fm24/input/editor.exe'
    if path.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    raw=path.read_bytes(); require(sha(raw)==EXEH==inv['editor_SHA256'],'editor SHA')
    pe=pefile.PE(data=raw,fast_load=True); pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    def va(off):return base+pe.get_rva_from_offset(off)
    def off(addr):return pe.get_offset_from_rva(addr-base)
    cap=Cs(CS_ARCH_X86,CS_MODE_64);cap.detail=True
    def dec(o):return next(cap.disasm(raw[o:o+15],va(o),1))
    def direct(i):return off(i.operands[0].imm) if i.operands[0].type==CS_OP_IMM else None
    def succ(o,i):
        q=o+i.size
        if i.mnemonic=='jmp':return [direct(i)]
        if i.mnemonic.startswith('j'):return sorted({q,direct(i)})
        if i.mnemonic in ('ret','retf','iret','iretq','int3','ud2'):return []
        return [q]
    rows=[r for f in sorted(HERE.glob('instructions.part*.json')) for r in j(f)]
    ev={r['file_offset']:r for r in rows};require(len(ev)==len(rows),'unique instruction offsets')
    for o,r in ev.items():
        i=dec(o); require(r['VA']==i.address and r['bytes']==i.bytes.hex() and r['instruction']==(i.mnemonic+' '+i.op_str).strip(),('instruction',hex(o)))
        if i.mnemonic.startswith('j') or i.mnemonic=='call':require(r.get('direct_target')==direct(i),('direct target',hex(o)))
    require(inv['entry']==ENTRY,'reader entry')
    def walk(entry):
        rt=[x.struct for x in pe.DIRECTORY_ENTRY_EXCEPTION if x.struct.BeginAddress==va(entry)-base]
        require(len(rt)==1,('runtime function',entry)); end=off(base+rt[0].EndAddress)
        q=deque([entry]); graph={}; ext=[]
        while q:
            o=q.pop()
            if o in graph:continue
            i=dec(o); outs=succ(o,i); graph[o]=[p for p in outs if p is not None and entry<=p<end]
            ext.extend((o,p) for p in outs if p not in graph[o]); q.extend(graph[o])
        return end,graph,ext
    end,graph,ext=walk(ENTRY)
    require(end==0x1040be4==inv['end_exclusive'] and len(graph)==992==inv['reachable'] and not ext and inv['external_edges']==[],'reachable extent')
    require(graph=={o:r['successors'] for o,r in ev.items() if r.get('function')==ENTRY},'whole CFG')
    brs=[r for f in sorted(HERE.glob('branches.part*.json')) for r in j(f)]
    sites={o for o in graph if dec(o).mnemonic.startswith('j') and dec(o).mnemonic!='jmp'}
    require(sites=={r['site'] for r in brs} and len(sites)==len(brs),'branch census')
    for r in brs:
        o=r['site']; i=dec(o); require((direct(i),o+i.size)==(r['taken'],r['fallthrough']),('branch edges',o))
        p=r['predicate']; require(p is None or dec(p).eflags and ev[p]['instruction']==r['predicate_instruction'],('flags',o))
    for o,w,d in ((0x10409d3,0x1040b89,0x10409d9),(0x103fae6,0x10405b0,0x103faec)):
        require(graph[o]==sorted([w,d]),'mode edges')
    def vcall(i):return i.mnemonic=='call' and i.operands[0].type==CS_OP_MEM and i.operands[0].mem.disp==0x28
    calls={o for o in graph if vcall(dec(o))}; extra={0x103fcbd,0x103ff79,0x1040529}
    require(calls==({x['site'] for x in slots}-{STEPS[0],STEPS[13],STEPS[39]})|extra and len(calls)==inv['stream_slot_28_count']==40,'stream sites')
    require(set(inv['nation_vslots'])=={'2','19','20'} and inv['nation_vtable_VA']==0x1418893b8,'vtable')
    for k,r in inv['nation_vslots'].items():
        o=off(inv['nation_vtable_VA']+8*int(k)); require(r['file_offset']==o and r['VA']==va(o) and r['bytes']==raw[o:o+8].hex(),'vslot bytes')
        require(off(unpack_from('<Q',raw,o)[0])=={'2':0x1041f30,'19':ENTRY,'20':0x1041130}[k],'vslot pointer')
    require(direct(dec(0x1041f33))==0x1041f40 and direct(dec(0x1041130))==0x3d60300,'getter/fixup thunk')
    for k,r in inv['factory_cells'].items():
        o=0xf49d38+int(k)*4; require(r['file_offset']==o and r['bytes']==raw[o:o+4].hex() and
            off(va(0xf49d38)+unpack_from('<i',raw,o)[0])=={'10':0xf48f27,'41':0xf49622}[k],'factory case')
    r=inv['currency_reader_slot'];cur=0x18bf648+19*8
    require(r['file_offset']==cur and r['bytes']==raw[cur:cur+8].hex() and off(unpack_from('<Q',raw,cur)[0])==0x157ed50 and direct(dec(0x157ed50))==0x43c5800,'t41 reader')
    require([direct(dec(o)) for o in (0x43c581d,0x43c5835,0x43c584d,0x43c5865)]==[0x814110]*4 and direct(dec(0x43c589a))==0x157f770,'t41 target transfers')
    for name,w in [(0x157f79c,4),(0x157f918,1),(0x157f937,2),(0x157f956,4),(0x3c6010d,12)]:
        i=dec(name)
        require(i.mnemonic=='mov' and cap.reg_name(i.operands[0].reg)=='r8d' and i.operands[1].imm==w,'helper width')
    _,getter,_=walk(0x1041f40)
    for x in slots:
        p,o,k,w,d=(x[key] for key in ('position','site','candidate_4cc','width','object_displacement'))
        require(o==STEPS[p] and k==MATCH.get(p) and w==WIDTHS[p] and d==OFFS[p],('ordered tuple',p))
        if o in calls:
            t=x['transfer']; s=dec(t['width_site']); destination=dec(t['destination_site'])
            require(s.mnemonic=='mov' and cap.reg_name(s.operands[0].reg)=='r8d' and s.operands[1].imm==w and
                    destination.op_str==t['destination_operand'] and t['width']==w,'argument preparation')
            if x['type']!='collection':require(destination.mnemonic=='lea' and destination.operands[1].mem.disp==d,'destination displacement')
            scan=min(t['width_site'],t['destination_site'])
            while scan<o:
                i=dec(scan);require(len(graph[scan])==1 and graph[scan][0]==scan+i.size,('local argument flow',o));scan+=i.size
            require(scan==o,'argument path ends at transfer')
        g=x['getter']
        if g:
            c=g['compare']; i=dec(c); br=dec(g['equality_branch']); a=off(br.address)
            start=direct(br) if br.mnemonic=='je' else a+br.size
            require(c in getter and i.mnemonic=='cmp' and i.operands[1].imm==int.from_bytes(k.encode(),'big') and c+i.size==a
              and br.mnemonic in ('je','jne') and start==g['equal_successor'],'scoped equality branch')
            if 'success_path' in g:
                gp=g['success_path']; ld=dec(g['load']); base_reg=cap.reg_name(ld.operands[1].mem.base)
                require(gp[0]==start and gp[-1]==g['load'] and all(y in getter[z] for z,y in zip(gp,gp[1:])) and
                        base_reg=='r12' and ld.operands[1].mem.disp==d,'same object use at getter')
            else:
                require(all(y in ev for y in g['selected_instructions']),'parent selected instructions')
        if p==37:
            require(x['mask']==512 and dec(0x1043605).op_str=='esi, 9' and dec(0x1043608).op_str=='sil, 1','bit mask')


def read_rows(b, server):
    require(b[:8]==HEAD and len(b)>=22,'nation header')
    results=[]; shape={}; ids=set(); pos=13
    for r in range(u(b,8)):
        start=pos; row={}
        order=range(40) if server else (0,*range(14,27),39)
        for k in order:
            a=pos; width=WIDTHS[k]; require(a+width<=len(b)-9,('short fixed',r,k,a)); pos+=width; n=None
            if k in VEC:
                code,w=VEC[k]; n=unpack_from('<'+code,b,a)[0]
                require(0<=n<=(len(b)-9-pos)//w, f'row {r} @{a} invalid count {n}')
                if k==4:
                    for _ in range(n):
                        pos+=1
                        for f in range(4):
                            require(pos+4<=len(b)-9,('Nftb string length',pos)); L=u(b,pos); pos+=4+L
                            require(pos<=len(b)-9,('Nftb string bounds',pos)); shape.setdefault(f'Nftb_lengths_{f}',[]).append(L)
                        pos+=20
                elif k==11:
                    for _ in range(n):
                        require(pos<len(b)-9,('Ntxr tag',pos)); tag=b[pos]; pos+=25 if tag>=2 else 23
                        shape.setdefault('Ntxr_tags',[]).append(tag)
                else:
                    if k==12:
                        for item in range(n):
                            for f in (0,1):
                                at=pos+item*12+4+4*f; dd,yy=unpack_from('<HH',b,at)
                                shape.setdefault(f'opaque_d8_date_{f}',[]).append([r,at,dd&511,yy,dd>>9])
                    pos+=n*w
            require(pos<=len(b)-9,('main transfer bounds',r,k,pos)); row[k]=(a,pos-a,n)
        ia=row[39][0]; i,uid,rep=unpack_from('<III',b,ia)
        require(b[start]==0 and i==r and uid==rep!=0 and uid not in ids,('identity',r,ia,i,uid,rep)); ids.add(uid)
        results.append((start,pos,[i,uid,rep],row))
    require(b[pos:]==TAIL,'footer or trailing bytes');return results,shape


def target_keys(tid,b,side,rows,doc):
    require(b[:8]==HEAD,'target header'); n=u(b,8)
    if tid==10: ends=[q for _,q,_,_ in rows]
    elif tid==41:
        p=13;ends=[]
        for _ in range(n):
            require(b[p]==0,'currency selector');p+=1
            for _ in range(4):
                p+=4+u(b,p); require(p<=len(b)-29,'currency string bounds')
            p+=4
            p+=4+7*u(b,p)+12; require(p<=len(b)-9,'currency series bounds');ends.append(p)
    else:
        step={2:(43,43),5:(34,48),19:(45,46),21:(38,181)}[tid][side=='server']
        ends=list(range(13+step,13+step*(n+1),step))
    require(len(ends)==n and ends[-1]+9==len(b) and b[-9:-4]==b'\0\0\0\0\1','target EOF')
    result={}; compact=bytearray()
    for o,p in enumerate(ends):
        i,v,z=unpack_from('<III',b,p-12)
        require(o==i and v==z!=0 and b[p]==0,('target identity',side,tid,p)); result[i]=v; compact+=b[p-12:p]
    require(len(set(result.values()))==n==doc['count'] and sha(b)==doc['payload_sha256'] and sha(compact)==doc['identity_sha256'],'target domain')
    return result


def domains(s,b,rows,slots,xml,targets):
    def sample(pts,i,v):
        r,a,w,_=pts[i]; return dict(row=r,absolute=a,raw=b[a:a+w].hex(),value=v)
    for k,x in enumerate(slots):
        pts=[(r,*row[k]) for r,(*_,row) in enumerate(rows) if k in row]
        require([list(t[1:3]) for t in pts]==x['coordinates'][s] and x['coverage'][s]==len(pts),('slot coordinates',s,k))
        pf=x['domain_profiles'][s]; require(pf['rows']==len(pts),('profile size',s,k))
        if not pts:require(pf['status']=='bypassed_mode','mode bypass');continue
        if k in VEC:
            require(pf['counts']==hist(t[3] for t in pts) and pf['items']==sum(t[3] for t in pts) and
                pf['byte_range']==[func(t[2] for t in pts) for func in (min,max)],('collection distribution',s,k))
            r,a,w,n=pts[0];require(pf['first']==dict(row=r,start=a,span=w,count=n),'first collection');continue
        if k==39:require(pf['first']==sample(pts,0,rows[0][2]),'identity sample');continue
        signed=k in (14,19,20,22,34)
        vals=[int.from_bytes(b[a:a+w],'little',signed=signed) for _,a,w,_ in pts]
        require((pf['min'],pf['max'],pf['distinct'],pf['first'])==(min(vals),max(vals),len(set(vals)),sample(pts,0,vals[0])),('scalar statistics',s,k))
        if 'hist' in pf:require(pf['hist']==hist(vals),('scalar distribution',s,k))
        if k in REF:
            tgt=targets[REF[k]]; uidset=set(tgt.values()); n=0xffffffff
            require(x['target_table']==REF[k] and x['type']=='ref_ordinal_u32','reference type')
            v=[(i,z) for i,z in enumerate(vals) if z not in tgt and z!=n]
            first=lambda pairs:sample(pts,*pairs[0]) if pairs else None
            hits=sum(z in tgt for z in vals); nil=vals.count(n)
            require((pf['hit'],pf['miss'],pf['null'],pf['wrong_uid_hit'])==(hits,len(v),nil,sum(z in uidset for z in vals)),('ordinal join',s,k))
            require(pf['first_miss']==first(v) and pf['first_null']==first([(i,z) for i,z in enumerate(vals) if z==n]) and
                pf['first_wrong_uid_miss']==first([(i,z) for i,z in enumerate(vals) if z not in uidset and z!=n]),'reference first samples')
            clashes=[(i,z) for i,z in enumerate(vals) if z in uidset and z in tgt and tgt[z]!=z]
            require(pf['first_ordinal_UID_collision']==({**first(clashes),'ordinal_to_UID':tgt[clashes[0][1]],
               'UID_to_ordinal':next(q for q,z in tgt.items() if z==clashes[0][1])} if clashes else None),'reference collision')
            if k!=17:require(xml[x['xml_candidates'][0]]['is_optional']=='true','reference optional scope')
            require(pf['domain']==('pass' if hits and not v else 'held'),'reference domain grade')
        if k in (14,19):
            f=xml[x['xml_candidates'][0]]; require(f['type']=='enum' and not f.get('enum_ref') and pf['domain']=='held' and
                    pf['first_unverifiable']==sample(pts,0,vals[0]),'missing enum gate')
        if k in (20,22):
            f=xml[x['xml_candidates'][0]];lo,hi=int(f['min_value']),int(f['max_value'])
            bad=[(i,v) for i,v in enumerate(vals) if not lo<=v<=hi]
            require(pf['xml_bounds']==[lo,hi] and pf['violations']==len(bad) and pf['domain']==('held' if bad else 'pass') and
                    pf['first_violation']==(sample(pts,*bad[0]) if bad else None),'numeric bounds and counterexample')
        if k==37:
            bits=0
            for v in vals:bits|=v&~512
            bad=next((i for i,v in enumerate(vals) if bool(v)!=bool(v&512)),None)
            require(pf['mask']==512 and pf['decoded']==hist(int(bool(v&512)) for v in vals) and pf['other_bits_or']==bits and
                pf['whole_word_counterexample']==(sample(pts,bad,vals[bad]) if bad is not None else None) and pf['domain']=='pass','boolean bitfield')
        if 'float32_diagnostic' in pf:
            f=pf['float32_diagnostic']; floats=[unpack_from('<f',b,a)[0] for _,a,_,_ in pts]; finite=[t for t in floats if math.isfinite(t)]
            i=next((i for i,t in enumerate(floats) if not math.isfinite(t)),None)
            require(f==dict(finite=len(finite),min=min(finite,default=None),max=max(finite,default=None),
                    finite_nonzero_normal=sum(abs(t)>=2**-126 for t in finite),first_nonfinite=sample(pts,i,None) if i is not None else None),'float diagnostic')


def verify():
    inv=j(HERE/'field_slots.json'); fld=j(HERE/'field_map.json'); abc=j(HERE/'abc_closure.json'); slots=inv['slots']
    require(len(slots)==40 and [x['position'] for x in slots]==list(range(40)),'main position census')
    require(inv['L4']==fld['L4']==0,'L4 boundary')
    hashes={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']}
    for p,k in inv['provenance_sha256'].items():
        require(sha((ROOT/p).read_bytes())==k and (not p.startswith('evidence/') or hashes[p]==k),('prior SHA',p))
    require(hashes[MASTER]==fld['frozen_sha256']==MASTERH,'master SHA')
    xml=j(ROOT/MASTER)['entities']['nation.xml'][0]['fields']; require(len(xml)==fld['fields_total']==346,'XML count')
    pe_check(inv['source'],slots)
    raw=archives(inv['archive']); prev=j(ROOT/'scratch/t47/out/cursor_nation_tax.json'); allrows={}; alltargets={}; bad_modes={}
    for s in ('client','server'):
        b=raw[s,10]; r,shape=read_rows(b,s=='server'); allrows[s]=r
        require(len(r)==251 and sha(b)==prev[s]['payload_sha256'],'reference t47 payload')
        require(all((a,z,ids,sl[39][0],sha(b[a:z]))==(t['wire13'],t['end'],t['identity'],t['identity_at'],t['wire_sha256'])
                    for (a,z,ids,sl),t in zip(r,prev[s]['rows'],strict=True)),('t47 spans/identity',s))
        env=inv['envelopes'][s];require((env['header'],env['body'],env['footer_at'],env['footer'])==(13,r[-1][1]-13,r[-1][1],TAIL.hex()),'envelope')
        seq=list(r[0][3]); require([x['execution_index'][s] for x in slots]==[seq.index(i) if i in seq else None for i in range(40)],'executed ordering')
        alltargets[s]={t:target_keys(t,raw[s,t],s,r,inv['targets'][s][str(t)]) for t in (2,5,10,19,21,41)}
        domains(s,b,r,slots,xml,alltargets[s]);
        try:read_rows(b,s!='server')
        except Check as e:bad_modes[s]=str(e)
        else:raise Check('wrong mode success')
        if s=='server':
            require(set(shape)==set(inv['opaque_collection_shape_profiles']),'opaque helper shapes')
            for k,v in shape.items():
                want=inv['opaque_collection_shape_profiles'][k]
                if not k.startswith('opaque_d8'):require(want==hist(v),('helper histogram',k));continue
                def maxd(y): return 365+int(y%4==0 and (y%100!=0 or y%400==0))
                require(want['count']==len(v) and want['year']==hist(x[3] for x in v) and want['high7']==hist(x[4] for x in v) and
                    want['day']==[min(x[2] for x in v),max(x[2] for x in v)] and want['first']==v[0] and
                    want['first_calendar_counterexample']==next((x for x in v if x[3]==0 or not 1<=x[2]<=maxd(x[3])),None),'date shape')
    require(alltargets['server'][10]==alltargets['client'][10], 'archive identity equality')
    require(bad_modes=={'client':'row 0 @7188 invalid count 1507845','server':'row 0 @38 invalid count -90'},'wrong mode first counterexamples')
    sc={}
    for x in slots:
        k=x['candidate_4cc']; indexes=[i for i,f in enumerate(xml) if k is not None and f['field']==k]
        require(x['xml_candidates']==indexes and len(indexes)<=1,('unique occurrence',k))
        if indexes:sc[indexes[0]]=x
    require(len(sc)==fld['positions_with_unique_XML']==15 and fld['alignment_ratio']==15/346,'join denominator')
    order=list(sc); pairs=[(i,h) for p,i in enumerate(order) for h in order[p+1:] if i>h]
    require(len(pairs)==fld['order']['inversions'] and fld['order']['status']=='mismatch','order inversions')
    x,y=pairs[0]
    expected={a:dict(position=sc[i]['position'],xml_index=i,code=xml[i]['field']) for a,i in [('earlier',x),('later',y)]}
    require(fld['order']['first_counterexample']==expected,'order first counterexample')
    rs=fld['fields'];require(len(rs)==346,'one record per XML occurrence')
    for i,(f,r) in enumerate(zip(xml,rs,strict=True)):
        require(r['schema']==f and r['xml_index']==i and r['code']==f['field'],'exact schema row')
        x=sc.get(i); k=f['field']
        require(r['slot']==(x['position'] if x else None) and r['order_status']==('mismatch' if any(i in t for t in pairs) else
                    'not_falsified_on_subset' if x else 'not_aligned'),'mapping and order status')
        if x:
            actual=[(s,v) for s,v in x['domain_profiles'].items() if v['rows']]
            grade=('linked_parent_held' if k=='Nftb' else 'prior_collection') if x['type']=='collection' else (
                'L3' if all(v.get('domain')=='pass' for s,v in actual) else 'held')
            require(r['grade']==grade,('promotion gate',k))
            if grade=='held':
                s,v=next((s,v) for s,v in actual if v.get('domain')!='pass'); w=v.get('first_violation') or v.get('first_unverifiable') or v.get('first_miss') or v['first']
                require(r['first_counterexample']=={'side':s,**w},'field holdout witness')
        else:
            require(r['grade'] in ('no_wire_slot','no_main_wire_slot','held','prior_identity','unmapped') and r['grade']!='L3','no slot no L3')
    require(hist(r['grade'] for r in rs)==fld['grade_counts'] and fld['domain_pass_L3']==5 and
         {r['code'] for r in rs if r['grade']=='L3'}=={'Ncti','Nrgi','Ncur','Nnsi','Nndn'},'accepted L3 set')
    t46=j(ROOT/'scratch/t46/out/grammar_diff_client_server.json')
    require(abc['original_sha256']==sha((ROOT/abc['original']).read_bytes()) and abc['original_differential']==t46['overall_row_grammar'],'unchanged t46')
    for k,letter in enumerate('ABCD',23):
        seg=abc['segments'][letter]
        require(seg['parent']==MATCH[k] and seg['position']==k and seg['item_stride']==VEC[k][1] and
               seg['status']=='explained' and seg['original_negative']==t46['segments'][letter],'A/B/C/D identity and negative')
        for s,rows in allrows.items():
            for _,_,_,r in rows:
                a,w,n=r[k]; following=k+1 if k<26 or s=='server' else 39
                require(w==WIDTHS[k]+n*VEC[k][1] and a+w==r[following][0],('segment span',s,k))
            require(seg['first_row_legacy_offset'][s]==rows[0][3][k][0]-rows[0][0]-1 and seg['profiles'][s]==slots[k]['domain_profiles'][s],'A/B/C/D published coordinates')
        require(all(raw['client',10][a:a+w]==raw['server',10][b:b+v] for (_,_,_,rc),(_,_,_,rs_) in zip(allrows['client'],allrows['server'])
                    for (a,w,_),(b,v,_) in [(rc[k],rs_[k])]),('matched collection bytes',letter))
    old=j(ROOT/'reports/t22_nation_capital.json'); require(old['schema']['commented'] and fld['supplemental']['Ncpi']['prior_grade']=='L3','inactive capital')
    for s,rows in allrows.items():
        city=raw[s,2]; require(sha(city)==old['data']['city_payload_sha256'],'city member')
        p=slots[17]['domain_profiles'][s]; require((p['hit'],p['miss'],p['null'],p['wrong_uid_hit'])==(231,0,20,25),'capital regression counts')
        cross=[]
        for o,(a,_,_,m) in enumerate(rows):
            q=m[17][0]; v=u(raw[s,10],q)
            if s=='client':require(q==a+10,'capital legacy offset +9')
            if v!=0xffffffff and u(city,14+43*v+10)!=o:cross.append(o)
        require(cross==[69,83,124,248,250] and u(raw[s,10],rows[149][3][17][0])==0xffffffff,'capital owner/775')
    for h in old['holdouts']:
        a=allrows['client'][h['nation_row']][3][17][0]
        require(a==int(h['field_payload_offset'],16) and raw['client',10][a:a+4].hex(' ')==h['field_wire_hex'],'capital holdout')
    w=j(ROOT/'scratch/t01/inbox/t01f/output.json')['verification']; reg=fld['regression']
    probes={x['payload_offset']:u(bytes.fromhex(x['bytes'])) for record in w['continent_and_nation_named_anchors'] if record['row_index'] in (7,250) for x in [record['cnti']]}
    parents=w['cpcm_named_anchors']
    for row in parents:
        x=row['child_cpcm']; probes[x['payload_offset']]=u(bytes.fromhex(x['bytes']))
    require([probes[o] for o in ('0x3bf','0x7c4c','0x15f0b','0x15f8a')]==[139,55,352,352] and
            all(unpack_from('<III',bytes.fromhex(p['parent_identity']['bytes']))==(352,150990,150990) for p in parents) and
            reg['legacy_nation_ordinals']=={str(o):alltargets['client'][10][o] for o in (139,55)},'England/China/parent ordinal regression')
    require(j(ROOT/'scratch/t47/out/fields_nation_tax.json')['L3']==reg['Ntxr_prior_L3']==7 and inv['opaque_collection_shape_profiles']['Ntxr_tags']=={'2':1899},'Ntxr regression')
    require(all(j(ROOT/f'scratch/t53/out/fields_{k}.json')['grade']=='held' for k in ('PUnI','PUnT','PUnP','PUnJ')) and reg['TCrs_prior_held']==4,'TCrs regression')
    print('t55 verify PASS: 992 instructions; 40/15 positions; 251+251 rows; 15/346 alignments; L3=5, L4=0')


def selftest():
    b=HEAD+pack('<I',1)+b'\0'*39+pack('<III',0,7,7)+TAIL
    r,_=read_rows(b,False);require(r[0][3][23]==(38,1,0) and r[0][2]==[0,7,7],'synthetic cursor')
    for bad in (b[:-1],b+b'\0',b[:38]+b'\xff'+b[39:]):
        try:read_rows(bad,False)
        except Check:pass
        else:raise Check('accepts truncated/trailing/invalid count control')
    print('t55 verifier selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');a=p.parse_args()
    try:selftest() if a.selftest else verify()
    except Check as e:print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e:print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
