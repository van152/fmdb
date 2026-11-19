"""t55: enumerate and replay NATION slot-19 main-row transfers (read-only inputs)."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t55/out'
EXE = ROOT.parent / 'fm24/input/editor.exe'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
LOCATOR = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
HEAD = bytes.fromhex('03017461642ef10d')
FOOT = bytes.fromhex('0000000001ec7ae404')
ENTRY, GET, VT = 0x103fac0, 0x1041f40, 0x1418893b8
PRIOR = (
    'scratch/t46/out/REPORT.md', 'scratch/t46/out/grammar_diff_client_server.json',
    'scratch/t47/out/cursor_nation_tax.json', 'scratch/t47/out/fields_nation_tax.json',
    'scratch/t28/out/REPORT.md', 'scratch/t51/out/fields_Nftb.json',
    'scratch/t53/out/REPORT.md', *(f'scratch/t53/out/fields_{k}.json' for k in ('PUnI','PUnT','PUnP','PUnJ')),
    'reports/t22_nation_capital.json', 'scratch/t01/inbox/t01f/REPORT.md',
    'scratch/t01/inbox/t01f/output.json',
)
# Count site, count format, object displacement, address proof, item call, wire stride.
ABC = dict(zip('ABCD', (
    (0x1040717,'b',0x48,0x1040724,0x104075b,5,'Nlns'),
    (0x10407b0,'i',0xa8,0x10407bd,0x1040829,28,'Nefr'),
    (0x104086c,'i',0x90,0x1040879,0x10408eb,28,'Nnfr'),
    (0x1040927,'i',0xc0,0x1040967,0x10409a7,12,'Nagr'),
)))
# Exact equality compare, first same-member use, read interpretation. Ref = ordinal.
DIRECT = {
    0x103fb0e: ('Nnsi',0x10432e8,0x10432f0,'ref',21),
    0x10405c7: ('Ngct',0x1042385,0x1042a47,'i8',None),
    0x10405eb: ('Ncti',0x104218a,0x1042ed7,'ref',5),
    0x104060f: ('Nrgi',0x10424e5,0x10424f1,'ref',19),
    0x1040633: ('Ncpi',0x1042144,0x1042174,'ref',2),
    0x1040657: ('Ncur',0x1042196,0x1042c7d,'ref',41),
    0x104067b: ('Nsod',0x1042268,0x1042e6f,'i8',None),
    0x104069f: ('Necf',0x10421a2,0x10421ae,'i8',None),
    0x10406e7: ('Nygn',0x1042078,0x1042aaf,'i8',None),
    0x1040aec: ('Npop',0x1041fa8,0x1041fb4,'i32',None),
    0x1040b58: ('Nndn',0x10426d0,0x10435f3,'u16_bitfield',None),
}
COL_GET = {'A':(0x1042216,0x1042f06), 'B':(0x1042047,0x3d75dd0), 'C':(0x104222e,0x3d75dd0),
           'D':(0x10426c4,0x3d765bb), 'Ntxr':(0x1042274,0x1042289)}
REPAIR = {2:0x3d6035d,5:0x3d6032b,19:0x3d6033d,41:0x3d6036f,21:0x3d60614}
TYPES = {'b':'i8','h':'i16','i':'i32','I':'u32'}

class Failed(Exception): pass

def need(ok, why):
    if not ok:
        raise Failed(why)

def digest(data): return sha256(data).hexdigest()
def load(path): return json.loads((ROOT/path).read_bytes())
def u(b, p=0): return S.unpack_from('<I', b, p)[0]
def hist(xs): return {str(k):v for k,v in sorted(Counter(xs).items())}
def emit(name, body):
    (OUT/name).write_text(json.dumps(body, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def archives():
    paths=(Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve(), ROOT.parent/'fm24')
    if any(x.drive.upper()=='Z:' for x in paths):
        raise ValueError('Z: forbidden')
    sys.path.append(str(paths[1]/'tools/python'))
    import zstandard as z
    directory = runpy.run_path(str(paths[1]/'scripts/modding_read_dbdat.py'))['_entries']
    raw, meta = {}, {}
    for side, n in [('client',31),('server',77)]:
        _, blob, index = directory(paths[0]/f'{side}_db.dat')
        base = index['data_base']; entries={e['path']:e for e in index['entries']}
        need(base==34 and len(entries)==n, (side,'directory'))
        meta[side]=dict(archive_sha256=digest(blob),entries=n,data_base=base,members={})
        for tid in (2,5,10,19,21,41):
            e=entries[f'{side}_db/table_{tid}.dat']; lo=base+e['offset']; hi=lo+e['packed_size']
            bound=min((base+x['offset'] for x in entries.values() if x['offset']>e['offset']),default=index['toc_offset'])
            need(base<=lo<hi<=bound, (side,tid,'bounds'))
            off=lo; candidates=[]; frames=[]
            while off<hi:
                need(blob[off:off+4]==bytes.fromhex('28b52ffd'), (side,tid,off,'zstd magic'))
                dec=z.ZstdDecompressor().decompressobj(); b=dec.decompress(blob[off:hi]); end=hi-len(dec.unused_data)
                need(dec.eof and end>off, (side,tid,off,'frame EOF'))
                f=[off,end,len(b)]; frames.append(f)
                if len(b)==e['size']: candidates.append((b,f))
                off=end
            need(len(candidates)==1,(side,tid,'declared size selector'))
            b,f=candidates[0]; raw[side,tid]=b
            meta[side]['members'][str(tid)]=dict(start=lo,end=hi,neighbor_bound=bound,frames=frames,selected=f,
                compressed_sha256=digest(blob[lo:hi]),payload_sha256=digest(b))
    return raw,meta


def replay(b, mode):
    need(mode in (0,1) and b[:8]==HEAD and len(b)>=22,'mode/header')
    p=13; rows=[]; ids=set(); book={}; shapes={}; ordered=[]
    for row in range(u(b,8)):
        begin=p; order=[]; spans={}; limit=len(b)-9
        def cut(n):
            nonlocal p
            if not 0<=n<=limit-p: raise Failed(f'row {row} @{p} short transfer w={n}')
            p+=n
            return b[p-n:p]
        def mark(site,a,num=None):
            need(site not in order,f'duplicate main event {site:#x}')
            order.append(site); book.setdefault(site,[]).append([row,a,p-a,num]); spans[site]=[a,p-a,num]
        def scalar(site,n):
            a=p; cut(n); mark(site,a)
        def count(fmt, stride, label):
            at=p; v=S.unpack('<'+fmt,cut(S.calcsize(fmt)))[0]
            if not 0<=v<=(limit-p)//stride:
                raise Failed(f'row {row} @{at} {label} invalid count {v}')
            return v
        def vector(site,fmt,w,label,body=None):
            a=p; n=count(fmt,w,label)
            if body is None: cut(n*w)
            else:
                for _ in range(n): body()
            mark(site,a,n)
        scalar(0xf2ba0e,1)
        if mode:
            scalar(0x103fb0e,4)
            vector(0x103fb37,'h',4,'extra_128')
            vector(0x103fe72,'i',4,'extra_158')
            def ftb():
                cut(1)
                for j in range(4):
                    n=count('I',1,'Nftb str length'); cut(n)
                    shapes.setdefault('Nftb_lengths_'+str(j),[]).append(n)
                cut(20)
            vector(0x104011f,'h',37,'Nftb',ftb)
            for site in range(0x1040360,0x1040415,0x24): scalar(site,4)
            def tax():
                tag=cut(1)[0]; cut(22+2*(tag>=2))
                shapes.setdefault('Ntxr_tags',[]).append(tag)
            vector(0x1040462,'i',23,'Ntxr',tax)
            def dates():
                cut(4)
                for j in range(2):
                    where=p; d,y=S.unpack('<HH',cut(4)); doy=d&511
                    shapes.setdefault('opaque_d8_date_'+str(j),[]).append([row,where,doy,y,d>>9])
            vector(0x10404d1,'I',12,'extra_d8',dates)
            vector(0x3d74e62,'I',14,'extra_78')
        for site,w in zip(range(0x10405c7,0x10406e8,0x24),(1,4,4,4,4,1,1,4,1),strict=True): scalar(site,w)
        for seg,(site,fmt,_,_,_,w,_) in ABC.items(): vector(site,fmt,w,seg)
        if mode:
            for site,w in zip(range(0x10409f0,0x1040b7d,0x24),[4]*10+[2,1],strict=True): scalar(site,w)
        iat=p; scalar(0x3c60119,12)
        j,a,c=S.unpack_from('<III',b,iat)
        need(j==row and a==c!=0 and a not in ids,f'row {row} @{iat} bad identity {(j,a,c)}')
        need(b[begin]==0 and sum(x[1] for x in spans.values())==p-begin,(row,'selector/covered bytes'))
        ids.add(a)
        rows.append(dict(row=row,start=begin,end=p,identity_at=iat,identity=[j,a,c],sha256=digest(b[begin:p])))
        if row==0: ordered=order
        else: need(ordered==order,(row,'main execution order'))
    need(b[p:]==FOOT,'footer/EOF')
    return rows, book, ordered, shapes


def target(side,tid,b,rows):
    n=u(b,8); p=13; at=[]; tail=len(b)-9
    need(b[:8]==HEAD,(side,tid,'target header'))
    if tid==10:
        at=[r['identity_at'] for r in rows]; p=rows[-1]['end']; method='t10 replayed identity'
    elif tid==41:
        method='t41 slot-19 cursor: selector, 4 length-prefixed strings, 4B, u32 count × 7B, identity'
        def take(k):
            nonlocal p
            need(0<=k<=tail-p,(side,tid,p,k,'target bounds'))
            p+=k; return p-k
        for _ in range(n):
            need(b[take(1)]==0,(side,tid,'target selector'))
            for _ in range(4): take(u(b,take(4)))
            take(4); take(7*u(b,take(4))); at.append(take(12))
    else:
        stride={2:(43,43),5:(34,48),19:(45,46),21:(38,181)}[tid][side=='server']
        method=f'checked {stride} B row identity tails'; p+=n*stride
        at=[13+(i+1)*stride-12 for i in range(n)]
    need(p==tail and b[p:p+5]==bytes.fromhex('0000000001') and n==len(at),(side,tid,'target EOF'))
    ids={}
    for i,o in enumerate(at):
        v,a,c=S.unpack_from('<III',b,o)
        need(i==v and a==c!=0 and b[o+12]==0,(side,tid,i,o,'target identity'))
        ids[v]=a
    need(len(set(ids.values()))==n,(side,tid,'target UID uniqueness'))
    return ids,dict(method=method,count=n,payload_sha256=digest(b),identity_sha256=digest(b''.join(b[o:o+12] for o in at)))


def static():
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    pe=PE(EXE); need(digest(pe.raw)==EXEH,'editor SHA'); pe.pe.parse_data_directories(directories=[3])
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    def ins(o):
        i=next(md.disasm(pe.raw[o:o+15],pe.f2va(o),1),None)
        need(i is not None,f'instruction decode at {o:#x}')
        return i
    def xt(i): return pe.va2f(i.operands[0].imm) if i.operands[0].type==X86_OP_IMM else None
    def blob(o,n): return dict(file_offset=o,VA=pe.f2va(o),bytes=pe.raw[o:o+n].hex())
    rr=ReaderCFG(pe,md,ENTRY); gg=ReaderCFG(pe,md,GET)
    main={pe.va2f(v):i for v,i in rr.instructions.items()}; get={pe.va2f(v):i for v,i in gg.instructions.items()}
    need(rr.function_end_off==0x1040be4 and len(main)==992 and not rr.external_edges,'main CFG')
    def rec(o,i):
        d={**blob(o,i.size),'instruction':(i.mnemonic+' '+i.op_str).strip()}
        if i.mnemonic.startswith('j') or i.mnemonic=='call': d['direct_target']=xt(i)
        return d
    records={o:dict(rec(o,i),function=ENTRY,successors=[pe.va2f(v) for v in rr.successors[i.address]]) for o,i in main.items()}
    def add(*xs):
        for o in xs:
            if o not in records: records[o]=rec(o,ins(o))
    def path(cfg,start,goal):
        queue=[[start]]; seen={start}
        for p in queue:
            if p[-1]==goal:return [pe.va2f(v) for v in p]
            for x in cfg.successors[p[-1]]:
                if x not in seen: seen.add(x); queue.append([*p,x])
        raise Failed(f'unreachable getter {start:x} → {goal:x}')
    prev={o+i.size:(o,i) for o,i in main.items()}
    xfers={}
    for o,i in main.items():
        if i.mnemonic!='call' or i.operands[0].type!=X86_OP_MEM or i.operands[0].mem.disp!=0x28: continue
        j=o; width=dest=None
        for _ in range(9):
            j,q=prev[j]
            if q.mnemonic=='mov' and q.op_str.startswith('r8d, ') and width is None:
                width=(j,q.operands[1].imm)
            if q.op_str.startswith('rdx, ') and q.mnemonic in ('mov','lea') and dest is None:
                dest=(j,q.op_str,q.operands[1].mem.disp if q.operands[1].type==X86_OP_MEM and md.reg_name(q.operands[1].mem.base) in ('r14','r15') else None)
            if dest and width: break
        need(width is not None and dest is not None, (o,'RDX / R8D'))
        xfers[o]=dict(width=width[1],width_site=width[0],destination_site=dest[0],destination_operand=dest[1],object_displacement=dest[2])
    need(len(xfers)==40,'all direct +0x28 sites')
    getter_evidence={}
    for site,(k,cmp,src,_,tid) in DIRECT.items():
        q=get[cmp]; branch=cmp+q.size; br=get[branch]; dst=xt(br) if br.mnemonic=='je' else branch+br.size
        need(q.mnemonic=='cmp' and q.operands[1].imm==int.from_bytes(k.encode(),'big') and br.mnemonic in ('je','jne'),(k,'exact compare'))
        route=path(gg,pe.f2va(dst),pe.f2va(src)); load_ins=get[src]
        need(load_ins.operands[1].type==X86_OP_MEM and md.reg_name(load_ins.operands[1].mem.base)=='r12' and
             load_ins.operands[1].mem.disp==xfers[site]['object_displacement'],(k,'same this displacement'))
        add(cmp,branch,*route)
        getter_evidence[site]=dict(compare=cmp,equality_branch=branch,equal_successor=dst,success_path=route,load=src,
                                   target_fixup_call=REPAIR.get(tid))
    for name,(cmp,src) in COL_GET.items():
        q=get[cmp]; branch=cmp+q.size; br=get[branch]; dst=xt(br) if br.mnemonic=='je' else branch+br.size
        k=name if name=='Ntxr' else ABC[name][-1]
        need(q.operands[1].imm==int.from_bytes(k.encode(),'big'),(name,'parent compare'))
        if src in get: route=path(gg,pe.f2va(dst),pe.f2va(src))
        else:
            route=(path(gg,pe.f2va(dst),pe.f2va(0x1043591 if name=='D' else 0x1042252)) +
                ([0x104f500,0x3d763da,0x3d765a3,0x3d765b7,0x3d765bb,0x3d765d4] if name=='D' else
                 [0x104efb0,0x3d75d99,0x3d75dc0,0x3d75dc4,0x3d75dc7,0x3d75dcc,0x3d75dd0,0x3d75ddb]))
        add(cmp,branch,*route)
        site=0x1040462 if name=='Ntxr' else ABC[name][0]
        getter_evidence[site]=dict(compare=cmp,equality_branch=branch,equal_successor=dst,selected_instructions=route,load=src)
    extra=(0xf2ba0e,0xf2ba38,0xf2ba51,0x103ec17,0x103ec1e,0xf48f27,0xf48f37,0x1041f30,0x1041f33,
       0x1041130,0x1043605,0x1043608,0x104330f,0x104334d,0xfe3912,0xfe3918,0xfe3bff,
       0xfae340,0x3c600f0,0x3c60106,0x3c6010d,0x3c60113,0x3c60116,0x3c60119,
       0x104e6b0,0x3d74e30,0x3d74e5c,0x3d74e62,0x3d74f9c,0x1072560,
       0x144bca0,0x420c913,0x420ca3f,0x15cf370,0x448f8c9,0x448f8e5,0x448f901,0x448f919,0x35b0828,0x35b0883,
       0xdb7f80,0x39dd7b0,0x39dd7d4,0x3d8771f,0x3d87742,0x448faaf,0x448fb33,0x448fb4d,0x3d88320,0x3d88345,0x3d8838c,
       0xf49622,0xf4962d,0x157e980,0x43c3425,0x43c342c,0x157ed50,0x43c581d,0x43c5835,0x43c584d,0x43c5865,
       0x43c5885,0x43c589a,0x43c58f0,0x157f7a2,0x157f924,0x157f943,0x157f962,
       0x3d6031e,0x3d60330,0x3d60342,0x3d60362,0x3d60604,*REPAIR.values())
    add(*extra)
    vt=pe.va2f(VT); need([pe.va2f(S.unpack_from('<Q',pe.raw,vt+8*d)[0]) for d in (2,19,20)]==[0x1041f30,ENTRY,0x1041130],'NATION vslots')
    factory=0xf49d38
    def cell(t,d):
        o=factory+4*t; need(pe.va2f(pe.f2va(factory)+S.unpack_from('<i',pe.raw,o)[0])==d,'factory rel32');return blob(o,4)
    need(pe.va2f(S.unpack_from('<Q',pe.raw,0x18bf648+19*8)[0])==0x157ed50,'currency vslot')
    provenance=dict(editor=str(EXE),editor_SHA256=EXEH,entry=ENTRY,end_exclusive=rr.function_end_off,
        reachable=len(main),external_edges=rr.external_edges,stream_slot_28_count=len(xfers),
        nation_vtable_VA=VT,nation_vslots={str(d):blob(vt+8*d,8) for d in (2,19,20)},
        factory_cells={'10':cell(10,0xf48f27),'41':cell(41,0xf49622)},currency_reader_slot=blob(0x18bf648+19*8,8))
    bb=[]
    for o,i in sorted(main.items()):
        if not i.mnemonic.startswith('j') or i.mnemonic=='jmp': continue
        p=o; producer=None
        for _ in range(7):
            if p not in prev: break
            p,q=prev[p]
            if q.mnemonic.startswith('j'):break
            if q.eflags:producer=p;break
        j=xt(i); cls='unresolved'
        if o in (0x103fae6,0x10409d3):cls='runtime-external'
        elif o==0x104094a:cls='dead_taken_edge_only'
        elif j==0x1040930:cls='IO-result'
        elif o in (0x1040485,0x10404b2,0x10404e3,0x104073b,0x1040779,0x10407d6,0x1040847,0x1040898,0x1040908,0x1040980,0x10409c9):cls='wire_data'
        bb.append(dict(site=o,predicate=producer,predicate_instruction=records[producer]['instruction'] if producer is not None else None,
                       taken=j,fallthrough=o+i.size,classification=cls))
    return xfers,getter_evidence,provenance,sorted(records.values(),key=lambda r:r['file_offset']),bb


def point(b,cell,value):
    row,a,w,_=cell
    return dict(row=row,absolute=a,raw=b[a:a+w].hex(),value=value)


def profile(side, slot, b, cells, field, targets):
    if not cells: return dict(status='bypassed_mode',rows=0)
    def dec(c,signed=False): return int.from_bytes(b[c[1]:c[1]+c[2]],'little',signed=signed)
    def witness(i,v): return point(b,cells[i],v)
    kind=slot['type']; first=cells[0]
    if kind=='collection':
        return dict(rows=len(cells),items=sum(c[-1] for c in cells),counts=hist(c[-1] for c in cells),
                    byte_range=[min(c[2] for c in cells),max(c[2] for c in cells)],first=dict(row=0,start=first[1],span=first[2],count=first[3]))
    if kind=='identity':return dict(rows=len(cells),first=witness(0,list(S.unpack_from('<III',b,first[1]))))
    vals=[dec(c,kind in ('i8','i32')) for c in cells]
    result=dict(rows=len(cells),min=min(vals),max=max(vals),distinct=len(set(vals)),first=witness(0,vals[0]))
    if len(set(vals))<=32:result['hist']=hist(vals)
    if kind=='ref_ordinal_u32':
        tid=slot['target_table']; tgt=targets[side,tid]; uids=set(tgt.values()); null=0xffffffff
        yes=[i for i,v in enumerate(vals) if v in tgt]; misses=[i for i,v in enumerate(vals) if v!=null and v not in tgt]
        nn=[i for i,v in enumerate(vals) if v==null]; wrong=next((i for i,v in enumerate(vals) if v!=null and v not in uids),None)
        clash=next((i for i,v in enumerate(vals) if v in tgt and v in uids and tgt[v]!=v),None)
        result.update(target_table=tid,hit=len(yes),miss=len(misses),null=len(nn),wrong_uid_hit=sum(v in uids for v in vals),
                      first_miss=witness(misses[0],vals[misses[0]]) if misses else None,
                      first_null=witness(nn[0],null) if nn else None,first_wrong_uid_miss=witness(wrong,vals[wrong]) if wrong is not None else None,
                      first_ordinal_UID_collision=({**witness(clash,vals[clash]),'ordinal_to_UID':tgt[vals[clash]],
                          'UID_to_ordinal':next(o for o,a in tgt.items() if a==vals[clash])} if clash is not None else None))
        result['domain']='pass' if not misses and yes and (not nn or slot['candidate_4cc']=='Ncpi' or field.get('is_optional')=='true') else 'held'
    elif kind=='u16_bitfield':
        mask=slot['mask']; samples=[int(bool(v&mask)) for v in vals]
        i=next((i for i,v in enumerate(vals) if bool(v)!=bool(v&mask)),None)
        result.update(mask=mask,decoded=hist(samples),other_bits_or=0,whole_word_counterexample=witness(i,vals[i]) if i is not None else None,domain='pass')
        for v in vals: result['other_bits_or'] |= v&~mask
    elif field and field['type']=='integer' and 'min_value' in field and 'max_value' in field:
        lo,hi=int(field['min_value']),int(field['max_value']); bad=[i for i,v in enumerate(vals) if not lo<=v<=hi]
        result.update(xml_bounds=[lo,hi],violations=len(bad),first_violation=witness(bad[0],vals[bad[0]]) if bad else None, domain='held' if bad else 'pass')
    elif field and field['type']=='enum':
        # These two frozen occurrences have no enum_ref, do not use same-name enums.
        need(not field.get('enum_ref'),'implement explicit enum join before using a new enum_ref')
        result.update(domain='held',first_unverifiable=result['first'],reason='no scoped enum_ref')
    if kind.startswith('raw') or slot['candidate_4cc']=='Npop':
        result['signed_diagnostic']=[min(dec(c,True) for c in cells),max(dec(c,True) for c in cells)]
        if first[2]==4:
            floats=[S.unpack_from('<f',b,c[1])[0] for c in cells]; finite=[x for x in floats if math.isfinite(x)]
            bad=next((i for i,v in enumerate(floats) if not math.isfinite(v)),None)
            result['float32_diagnostic']=dict(finite=len(finite),min=min(finite,default=None),max=max(finite,default=None),
                finite_nonzero_normal=sum(abs(x)>=2**-126 for x in finite),first_nonfinite=witness(bad,None) if bad is not None else None)
    return result


def order_check(pairs):
    conflicts=[]
    for i,(pos,idx,k) in enumerate(pairs):
        for q,j,c in pairs[i+1:]:
            if j<idx:conflicts.append(dict(earlier=dict(position=pos,xml_index=idx,code=k),later=dict(position=q,xml_index=j,code=c)))
    return dict(status='mismatch' if conflicts else 'monotonic_on_evidenced_subset',inversions=len(conflicts),
                first_counterexample=conflicts[0] if conflicts else None,involved=sorted({x[d]['xml_index'] for x in conflicts for d in ('earlier','later')}))


def build():
    manifest={e['path']:e['sha256'] for e in load('evidence/MANIFEST.json')['files']}
    for p in (MASTER,LOCATOR):need(digest((ROOT/p).read_bytes())==manifest[p],p+' manifest SHA')
    need(manifest[MASTER]==MASTERH and EXEH in (ROOT/LOCATOR).read_text(encoding='utf-8'),'frozen SHA anchors')
    fs=load(MASTER)['entities']['nation.xml'][0]['fields']; need(len(fs)==346,'schema count')
    loc={k:[i for i,f in enumerate(fs) if f['field']==k] for k in {f['field'] for f in fs}}
    prior=load(PRIOR[2]); raw, meta=archives()
    xfers,get,prov,ins,branches=static(); sides=('client','server')
    rows={}; books={}; orders={}; shape={}; targets={}; td={}
    for s in sides:
        b=raw[s,10]; mode=int(s=='server'); rows[s],books[s],orders[s],shape[s]=replay(b,mode)
        ref=prior[s]; need(digest(b)==ref['payload_sha256'] and len(rows[s])==251,(s,'t47 SHA/count'))
        for r,t in zip(rows[s],ref['rows'],strict=True):
            need((r['start'],r['end'],r['identity_at'],r['identity'],r['sha256'])==(t['wire13'],t['end'],t['identity_at'],t['identity'],t['wire_sha256']),(s,r['row'],'t47 row bounds/hash'))
        td[s]={}
        for tid in (2,5,10,19,21,41):targets[s,tid],td[s][str(tid)]=target(s,tid,raw[s,tid],rows[s])
    need([r['identity'] for r in rows['client']]==[r['identity'] for r in rows['server']], 'cross-mode identity')
    scalar_order=orders['server']; need([o for o in scalar_order if o in books['client']]==orders['client'],'mode subsequence')
    col={site:dict(name=k,fmt=f,disp=d,proof=a,item=call,stride=w,k=code) for k,(site,f,d,a,call,w,code) in ABC.items()}
    col.update({
      0x103fb37:dict(name='extra_128',fmt='h',disp=0x128,proof=0x103fc3f,item=0x103fcbd,stride=4,k=None),
      0x103fe72:dict(name='extra_158',fmt='i',disp=0x158,proof=0x103ff08,item=0x103ff79,stride=4,k=None),
      0x104011f:dict(name='Nftb',fmt='h',disp=0x170,proof=0x104012c,item=0x10401dd,stride=None,k='Nftb',shape='u8 tag + 4 × (u32 length + bytes) + 4B packed date + 4 × 4B'),
      0x1040462:dict(name='Ntxr',fmt='i',disp=0x60,proof=0x104046f,item=0x1040494,stride=None,k='Ntxr',shape='tag <2 → 23B, otherwise 25B; t47'),
      0x10404d1:dict(name='extra_d8',fmt='I',disp=0xd8,proof=0x10404e9,item=0x1040529,stride=12,k=None,shape='4B opaque + two packed-date helper calls'),
      0x3d74e62:dict(name='extra_78',fmt='I',disp=0x78,proof=0x104057e,item=0x3d74f9c,stride=14,k=None)})
    hidden=[0x103fcbd,0x103ff79,0x1040529]
    need(set(xfers)==(set(scalar_order)-{0xf2ba0e,0x3d74e62,0x3c60119})|set(hidden),'coverage of direct transfer sites')
    slots=[]; joins={}
    for pos,o in enumerate(scalar_order):
        e=xfers.get(o,{}); w=e.get('width',{0xf2ba0e:1,0x3c60119:12,0x3d74e62:4}.get(o)); k=None
        slot=dict(position=pos,site=o,type={1:'raw8',2:'raw16',4:'raw32',12:'identity'}[w],width=w,
                  object_displacement=e.get('object_displacement'),modes=[int(side=='server') for side in sides if o in books[side]],
                  execution_index={s:orders[s].index(o) if o in books[s] else None for s in sides},transfer=e or None)
        if o==0xf2ba0e:slot.update(type='selector_u8',scope='loader envelope, not slot-19 field')
        if o==0x3c60119:slot.update(object_displacement=8,scope='already-closed identity, not new business field',top_level_call=0x1040bcf)
        if o in col:
            c=col[o]; k=c['k']; need(w==S.calcsize(c['fmt']),(o,'count width'))
            slot.update(type='collection',count_type=TYPES[c['fmt']],object_displacement=c['disp'],
                collection={kk:vv for kk,vv in c.items() if kk not in ('disp','fmt','k')},scope='parent span only; items not named here')
            if k=='Nftb':slot.update(collection_binding='t51 setter and item projection; exact parent getter unproved')
            if k=='Ntxr':slot.update(collection_binding='t47; mode 0 has no count transfer')
        if o in DIRECT:
            k,_,_,typ,tid=DIRECT[o]; slot.update(type='ref_ordinal_u32' if tid else typ)
            if tid:slot['target_table']=tid
            if k=='Nndn':slot['mask']=0x200;slot['projection_instructions']=[0x1043605,0x1043608]
        ix=loc.get(k,[]); need(len(ix)<=1,(k,'not unique top-level scope'))
        f=fs[ix[0]] if ix else None
        slot.update(candidate_4cc=k,xml_candidates=ix,getter=get.get(o),coverage={s:len(books[s].get(o,[])) for s in sides})
        slot['domain_profiles']={s:profile(s,slot,raw[s,10],books[s].get(o,[]),f,targets) for s in sides}
        slot['coordinates']={s:[[c[1],c[2]] for c in books[s].get(o,[])] for s in sides}
        slots.append(slot)
        if ix:joins[ix[0]]=slot
    by_site={sl['site']:sl for sl in slots}
    # Out-of-scope and already closed regression fixtures; no new field assignment.
    cap=load(PRIOR[11]); city_cl=raw['client',2]; capsite=by_site[0x1040633]; can=[]
    need(cap['field']['code']=='Ncpi' and cap['schema']['commented'] and 'Ncpi' not in loc,'capital inactive schema')
    need(digest(city_cl)==cap['data']['city_payload_sha256'] and raw['server',2]==city_cl,'t22 city payload')
    for side in sides:
        pf=capsite['domain_profiles'][side]; need((pf['hit'],pf['miss'],pf['null'],pf['wrong_uid_hit'])==(231,0,20,25),(side,'t22 capital domain'))
        cross=[]
        for r,a,_,_ in books[side][capsite['site']]:
            v=u(raw[side,10],a)
            if v!=0xffffffff and u(raw[side,2],14+43*v+10)!=r:cross.append(r)
        need(cross==[69,83,124,248,250] and u(raw[side,10],books[side][capsite['site']][149][1])==0xffffffff,'t22 capital owner/775')
        can.append(cross)
    need(all(a==rows['client'][r]['start']+10 for r,a,_,_ in books['client'][capsite['site']]),'t22 client row+9')
    for r in cap['holdouts']:
        o=r['nation_row']; a=books['client'][capsite['site']][o][1]
        need(a==int(r['field_payload_offset'],16) and raw['client',10][a:a+4].hex(' ')==r['field_wire_hex'],'t22 holdout coordinates')
    # Byte-only regression against accepted t01f; do not extract table_25.
    witness=load('scratch/t01/inbox/t01f/output.json')['verification']
    probes=[x['cnti'] for x in witness['continent_and_nation_named_anchors'] if x['row_index'] in (7,250)]
    parents=witness['cpcm_named_anchors']; probes.extend(x['child_cpcm'] for x in parents)
    a_refs={x['payload_offset']:u(bytes.fromhex(x['bytes'])) for x in probes}
    need(a_refs=={'0x3bf':139,'0x7c4c':55,'0x15f0b':352,'0x15f8a':352} and len(parents)==2 and all(S.unpack('<III',bytes.fromhex(x['parent_identity']['bytes']))==(352,150990,150990) for x in parents),'accepted t01f byte-only anchors')
    need(all(targets[s,10][139]==765 and targets[s,10][55]==110 for s in sides),'nation ordinals / distinct UIDs')
    tax=load(PRIOR[3]); need(tax['L3']==7 and tax['L4']==0,'Ntxr preserved')
    crs={load(f'scratch/t53/out/fields_{code}.json')['grade'] for code in ('PUnI','PUnT','PUnP','PUnJ')}
    need(crs=={'held'},'t53 held')
    need(sum(shape['server']['Ntxr_tags'])==3798 and set(shape['server']['Ntxr_tags'])=={2},'t47 Ntxr span control')
    controls={}
    for s in sides:
        try: replay(raw[s,10],int(s=='client'))
        except Failed as e:controls[s]=str(e)
        else: raise Failed(f'{s} wrong mode passed')
    regressions=dict(capital_cross_owner=can,capital='t22 prior L3 supplemental only; client coordinates and both city joins verified',
        legacy_nation_ordinals={str(r):targets['client',10][r] for r in (139,55)},comp_t01f_anchor_only=a_refs,
        Ntxr_prior_L3=7,Ntxr_items=1899,TCrs_prior_held=4,TCrs_main_slot=None,wrong_mode_rejected=controls)
    order=order_check([(sl['position'],sl['xml_candidates'][0],sl['candidate_4cc']) for sl in slots if sl['xml_candidates']])
    disposition=[]
    for i,f in enumerate(fs):
        k=f['field']; sl=joins.get(i); grade=None; reason=None; counter=None; scope='unresolved'
        if sl:
            scope='main-row'; passed=[]
            if sl['type']=='collection':
                grade='prior_collection' if k!='Nftb' else 'linked_parent_held'
                reason='reference earlier parent only; no nested promotion' if k!='Nftb' else 't51 item projection / setter, no exact parent getter'
            else:
                active=[(s,sl['domain_profiles'][s]) for s in sides if s in books and sl['site'] in books[s]]
                passed=[s for s,pf in active if pf.get('domain')=='pass']
                grade='L3' if len(active)==len(passed) else 'held'
                if grade=='held':
                    s,pf=next((s,pf) for s,pf in active if pf.get('domain')!='pass')
                    counter=dict(side=s,**(pf.get('first_violation') or pf.get('first_unverifiable') or pf.get('first_miss') or pf['first']))
                    reason=pf.get('reason','schema bounds/reference domain or ambiguous missing/live values')
        elif k in ('EDfx','TCrs','duni','EDsc'):
            scope,grade,reason={
              'EDfx':('editor-output','no_wire_slot','t53 generated UI output only; no claim about persistent inputs'),
              'TCrs':('out_of_scope_sidecar','no_main_wire_slot','t53 getter binds to sidecar; 4 held unchanged'),
              'duni':('identity_envelope','prior_identity','reuses closed identity; base getter fe3912 → fe3bff selects +0xc, not a separate business slot'),
              'EDsc':('unresolved','held','t53 missing dispatch; not evidence of absence')}[k]
        else:
            grade='unmapped'; reason='no exact same-member slot-19 path proven; do not infer absence or align by index'
        disposition.append(dict(xml_index=i,code=k,schema=f,scope=scope,slot=sl['position'] if sl else None,grade=grade,
                                reason=reason,first_counterexample=counter,
                                order_status='mismatch' if i in order['involved'] else 'not_falsified_on_subset' if sl else 'not_aligned'))
    t46=load(PRIOR[1]); segs={}
    for name,(site,fmt,disp,ds,item,w,k) in ABC.items():
        vals={s:by_site[site]['domain_profiles'][s] for s in sides}
        for s in sides:
            for o,a,size,n in books[s][site]: need(size==S.calcsize(fmt)+n*w,(name,s,o,'item stride'))
        segs[name]=dict(status='explained',parent=k,frozen_index=loc[k][0],position=by_site[site]['position'],count_site=site,
            count_type=TYPES[fmt],object_displacement=disp,object_site=ds,item_call=item,item_stride=w,profiles=vals,
            first_row_legacy_offset={s:books[s][site][0][1]-rows[s][0]['start']-1 for s in sides},
            original_negative=t46['segments'][name])
    shape_profiles={}
    for k,v in shape['server'].items():
        if not k.startswith('opaque_d8'):
            shape_profiles[k]=hist(v)
        else:
            bad=next((x for x in v if not 1<=x[2]<=(366 if x[3]%4==0 and (x[3]%100!=0 or x[3]%400==0) else 365) or x[3]==0),None)
            shape_profiles[k]=dict(count=len(v),year=hist(x[3] for x in v),day=[min(x[2] for x in v),max(x[2] for x in v)] if v else None,
                high7=hist(x[4] for x in v),first=v[0] if v else None,first_calendar_counterexample=bad,
                status='shape only: no named date in opaque collection')
    for kind, items, n in [('instructions',ins,400),('branches',branches,200)]:
        names=set()
        for i in range(0,len(items),n):
            name=f'{kind}.part{i//n+1:03}.json'; names.add(name); emit(name,items[i:i+n])
        for stale in OUT.glob(f'{kind}.part[0-9][0-9][0-9].json'):
            if stale.name not in names: stale.unlink()
    emit('field_slots.json',dict(status='main_row_census_complete_for_two_archive_modes_names_partial',L4=0,source=prov,
        provenance_sha256={p:digest((ROOT/p).read_bytes()) for p in (*PRIOR,MASTER,LOCATOR)},archive=meta,targets=td,
        axes='0-based positions in server execution; execution_index gives mode-specific order; coordinates are [absolute, complete consumed span] in ordinal order',
        envelopes={s:dict(header=13,body=sum(r['end']-r['start'] for r in rows[s]),footer=FOOT.hex(),rows=251,
                         footer_at=rows[s][-1]['end'],first=rows[s][0],last=rows[s][-1]) for s in sides},
        loop_internal_direct_transfers={str(o):xfers[o] for o in hidden},opaque_collection_shape_profiles=shape_profiles,slots=slots))
    cnt=hist(d['grade'] for d in disposition)
    emit('field_map.json',dict(scope='top-level frozen nation.xml#nation; excludes nested fields and supplemental Ncpi',frozen_sha256=MASTERH,
        fields_total=346,positions_with_unique_XML=len(joins),alignment_ratio=len(joins)/len(fs),domain_pass_L3=cnt.get('L3',0),
        L4=0,grade_counts=cnt,order=order,fields=disposition,regression=regressions,
        supplemental={'Ncpi':dict(prior_grade='L3',position=capsite['position'],active_XML=False,source=PRIOR[11]),
                      'Npop':dict(position=by_site[0x1040aec]['position'],status='held_out_of_schema',first_counterexample=by_site[0x1040aec]['domain_profiles']['server']['first'])}))
    emit('abc_closure.json',dict(status='A_B_C_D_explained_for_both_modes',original_sha256=digest((ROOT/PRIOR[0]).read_bytes()),
         original=PRIOR[0],original_differential=t46['overall_row_grammar'],segments=segs,
         formula='after mode-1 prelude if present: 24B common prefix; A=1+5a, B=4+28b, C=4+28c, D=4+12d; then mode-1 43B and identity',
         limit='server prelude is structurally bounded; unnamed prelude and suffix scalars are not explained semantically by these four lists'))
    print(f't55: {len(slots)} positions ({len(orders["client"])} client); XML joins {len(joins)}/346; grades {cnt}; L4=0')


def selftest():
    b=HEAD+S.pack('<I',1)+b'\0'+b'\0'*(1+24+13)+S.pack('<III',0,5,5)+FOOT
    r,bk,order,_=replay(b,0)
    need(len(r)==1 and len(order)==15 and bk[0x1040717][0]==[0,38,1,0],'tiny cursor')
    try:replay(b+b'!',0)
    except Failed:pass
    else:raise Failed('accepted trailing bytes')
    need(order_check([(0,7,'ABCD'),(1,3,'EFGH')])['inversions']==1,'order mismatch control')


def main():
    p=argparse.ArgumentParser(description=__doc__); g=p.add_mutually_exclusive_group()
    g.add_argument('--selftest',action='store_true'); g.add_argument('--build',action='store_true',help='build (default)')
    a=p.parse_args()
    try:
        if a.selftest:selftest(); print('t55 builder selftest PASS')
        else:build()
    except Failed as e:print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e:print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
