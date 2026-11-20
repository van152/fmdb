#!/usr/bin/env python3
"""Build t47: Nation collection backtrace and Ntxr cursor on frozen FM24 inputs."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t47/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
IDA = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
NEG = ('scratch/t37/out/REPORT.md','scratch/t37/out/nation_subtable_inventory.json')
PARENTS = dict(Nntp=224,Nctp=225,Nrtp=226,NTRv=228,NWGv=229,NSps=230,Ntxr=232,Nfmp=233,Nftb=234,EDfx=342,EDsc=344,Nrvn=216,NCro=231,Calt=235,TCrs=64)
HEAD = bytes.fromhex('03017461642ef10d')
FOOT = bytes.fromhex('0000000001ec7ae404')
# file offsets; dispatch, helper edges, collection access and stream/append sites in order.
ROUTES = {
'Nntp':(9,[0x10662de,0x10662e4,0x1066303,0x1078df0,0x3db28d3,0x3db28da,0x3db28ea,0x3db2a80,0x3db2abe,0x1074c70,0x105e264,0x105e271,0x105e28d,0x105e2b2,0x141caa0,0x105e2c7,0x105e2d2],'+f0/+f8 inline vector, 16 B object stride; i8 count, 9 B item reader'),
'Nctp':(9,[0x1066276,0x106627c,0x106644d,0x10790e0,0x3db2b73,0x3db2b7a,0x3db2b8a,0x3db2d20,0x3db2d5e,0x1075240,0x105e2e9,0x105e2f6,0x105e312,0x105e332,0x141cb70,0x105e347,0x105e352],'+108/+110 inline vector, 16 B object stride; i8 count, 8 B item reader'),
'Nrtp':(9,[0x1066371,0x1066377,0x10666ae,0x10793d0,0x3db3033,0x3db303a,0x3db304a,0x3db31e0,0x3db321e,0x10758a0,0x105e369,0x105e376,0x105e392,0x105e3b2,0x141cb70,0x105e3c7,0x105e3d2],'+120/+128 inline vector, 16 B object stride; i8 count, 8 B item reader; shares item reader, not vector, with Nctp'),
'NTRv':(9,[0x106734f,0x1067355,0x106838b,0x106838e,0x15d1300,0x4496f8a,0x4496f91,0x4497007,0x4496fb7,0x4496fd5,0x10683bc,0x105e9ec,0x105e9fe,0x105ea0a,0x105ea36,0x105ea54],'+438 optional i32 array; getter synthesizes 20 reputation rows using rank index and defaults missing array to 0'),
'NWGv':(9,[0x106735b,0x1067361,0x1067371,0x1067374,0x15d1300,0x4496f91,0x4497027,0x4496fb7,0x4496fd5,0x10673a2,0x105ea6b,0x105ea7d,0x105ea9d,0x105eab5,0x105ead3],'+440 optional i32 array; 20 synthesized reputation rows'),
'NSps':(9,[0x106686b,0x1066871,0x1066881,0x1066884,0x1067374,0x15d1300,0x4496f91,0x4496fa7,0x4496fb7,0x4496fd5,0x105eaea,0x105eafc,0x105eb08,0x105eb1c,0x105eb34,0x105eb52],'+448 optional i32 array; 20 synthesized reputation rows'),
'Ntxr':(10,[0x1042274,0x104227a,0x1042289,0x104228e,0x104229d,0x1043546,0x104355e,0x104ed80,0x3d75a02,0x3d75ac8,0x1040462,0x104046f,0x1040485,0x1040494,0x144bca0,0x10404a7,0x10404b2],'+60/+68 inline vector, 24 B object stride; i32 count, 23/25 B items; no independent tax member in this route'),
'Nfmp':(9,[0x106748b,0x1067491,0x10674b0,0x10799c0,0x3db51a3,0x3db51a9,0x3db51af,0x3db5353,0x3db535a,0x3db537e,0x105d99c,0x105d9a9,0x105d9c4,0x105d9e2,0x105f680,0x105da1b,0x105f730,0x105da2d,0x105d9d2],'+6e0/+6e8 pointer vector, signed i16 count, dedicated allocation and POD item reader; 9 B item reader; nonzero sign-extended first lane required before append'),
'NCro':(9,[0x10660c1,0x10660c7,0x10660e6,0x1078b00,0x3db2603,0x3db2616,0x3db2623,0x3db27c4,0x3db27d0,0x105d8c6,0x105d96d,0x105d8d8,0x105d97a,0x105f2b0,0x105f2e7,0x105f304,0x105f487,0x105f4a6,0x105f4cf],'+4f8 nullable pointer to vector of 16 B objects; presence byte, container tag + i32 count, 9 B wire items'),
'Nftb':(None,[0x1045b34,0x1045b3a,0x1045b66,0x1050d40,0x1050d65,0x1050d90],'setter-shaped import route with posl code lookup; no getter/storage proof'),
'Nrvn':(None,[0x10665a6,0x10665ac,0x10675f0,0x106ad10,0x3d95f7a,0x3d95f8d,0x3d95f95,0x11e8900,0x3eba390,0x3eba394,0x3eba3db,0x3eba3e8],'constructed wrapper: filters 16 B objects in current container +48/+50 on item +b == 6; reader/fill source not yet proven'),
'Calt':(None,[0x11cf7a1,0x11cf7a7,0x11cf7cb,0x11f4c32,0x11f4c38],'Team-container candidates; name match alone does not join NATION storage or a member'),
'TCrs':(None,[0x11cfa56,0x11cfa5c,0x11cfa6b,0x11cfa83,0x11f4e38,0x11f4e3e],'Team-container candidates; source vector/reader not proven'),
'EDfx':(None,[],'only reversed raw immediate at file 0x29c39; no reachable exact getter proven'),
'EDsc':(None,[],'neither raw 4CC byte order in editor PE; computed or resource route not excluded')}
for_key = {
'lowa':(0x144c1ad,0x144c1b9,4,1,'i'), 'uppa':(0x144c22f,0x144c4c3,8,5,'i'),
'capa':(0x144c2a6,0x144c521,12,9,'i'), 'perc':(0x144c31d,0x144c5bb,0,17,'f'),
'year':(0x144c23b,0x144c247,16,13,'H'), 'ppty':(0x144c329,0x144c335,18,15,'b'),
'txty':(0x144c223,0x144c464,19,16,'b'), 'fram':(0x144c195,0x144c394,20,21,'b'),
'leve':(0x144c1a1,0x144c3fc,21,22,'b')}
TAX_TX = ((0x420c913,1,None),(0x420c933,4,4),(0x420c953,4,8),(0x420c973,4,12),
 (0x420c993,2,16),(0x420c9b6,1,18),(0x420c9d2,1,19),(0x420c9ed,4,0),
 (0x420ca09,1,20),(0x420ca25,1,21),(0x420ca57,2,22))

class Check(Exception): pass

def ck(ok,msg):
    if not ok: raise Check(msg)

def H(b): return sha256(b).hexdigest()
def J(path): return json.loads(path.read_bytes())
def output(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def hist(seq): return dict(sorted(Counter(seq).items()))
def u(b,p=0): return S.unpack_from('<I',b,p)[0]

def read_archives():
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    codec=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if root.drive.upper()=='Z:': raise ValueError('Z: forbidden')
    meta,payload={},{}
    for side,n in [('client',31),('server',77)]:
        _,blob,d=codec['_entries'](root/(side+'_db.dat'))
        base=d['data_base']; es={x['path']:x for x in d['entries']}
        ck(len(es)==n and base==34,side+' directory')
        a=meta[side]={'directory_entries':n,'data_base':base,'archive_sha256':H(blob),'members':{}}
        for key in ('table_10.dat','table_9.dat','table_extra_9.dat','table_extra_10.dat'):
            path=f'{side}_db/{key}'; e=es.get(path)
            if e is None:
                a['members'][key]={'present':False,'entry':None,'count':None,'stride':None}; continue
            lo=base+e['offset']; hi=lo+e['packed_size']
            bound=min((base+t['offset'] for t in es.values() if t['offset']>e['offset']),default=d['toc_offset'])
            ck(lo<hi<=bound,path+' bounds'); part=blob[lo:hi]
            i=0; frames=[]; matches=[]
            while i<len(part):
                ck(part[i:i+4]==b'\x28\xb5\x2f\xfd',path+' frame')
                ctx=z.ZstdDecompressor().decompressobj(); b=ctx.decompress(part[i:]); size=len(part)-i-len(ctx.unused_data)
                ck(ctx.eof and size>0,path+' EOF')
                frm={'offset':lo+i,'compressed_bytes':size,'payload_bytes':len(b)}; frames.append(frm)
                if len(b)==e['size']: matches.append((b,frm))
                i+=size
            ck(len(matches)==1 and e.get('sha256',H(part))==H(part),path+' size/SHA selector')
            b,frm=matches[0]; payload[side,key]=b
            a['members'][key]=dict(present=True,entry={**e,'sha256':H(part)},member_start=lo,member_end=hi,next_member_start=bound,
                selected_frame=frm,frames=frames,payload_sha256=H(b),head=b[:16].hex(),count=u(b,8),stride=None,
                count_basis='u32 at 8; not row closure for unresolved readers')
    return meta,payload


def walk(b,mode,only=None):
    ck(b[:8]==HEAD,'bad NATION header')
    p=13; rows=[]; tax=[]; visits={}; sels=Counter(); lens=Counter(); ids=set()
    for j in range(u(b,8) if only is None else only):
        begin=p; events=[]; collections={}
        def take(w,site,repeat=1,record=True):
            nonlocal p
            width=w*repeat; q=p+width
            ck(0<=width<=len(b)-p,f'row {j} @{p} width={width} site={site:#x}')
            chunk=b[p:q]
            if record:
                events.append([site,p,w,repeat]); visits.setdefault(site,dict(row=j,absolute=p,width=w))
            p=q; return chunk
        def number(w,site,signed=False): return int.from_bytes(take(w,site),'little',signed=signed)
        def vec(k,w,site,body,signed=False):
            at=p; n=number(w,site,signed)
            ck(n>=0 and n<=len(b)-p,f'row {j} {k} invalid count {n} @{at}')
            first=p
            for i in range(n): body(i)
            collections[k]=[at,n,first,p]
        sels[number(1,0xf2ba0e)]+=1
        if mode:
            take(4,0x103fb0e)
            vec('extra_128',2,0x103fb37,lambda i:take(4,0x103fcbd),True)
            vec('extra_158',4,0x103fe72,lambda i:take(4,0x103ff79),True)
            def strings(i):
                take(1,0x448f8b1)
                for site in (0x448f8c9,0x448f8e5,0x448f901,0x448f919):
                    n=number(4,0x35b0828)
                    if n: take(n,0x35b0883)
                take(4,0x448f92c); take(4,0x448f948); take(4,0x448f964); take(4,0x448f980); take(4,0x448f9a9)
            vec('extra_170',2,0x104011f,strings,True)
            for s in range(0x1040360,0x1040415,0x24): take(4,s)
            def item(i):
                start=p; tag=number(1,TAX_TX[0][0]);
                for s,w,_ in TAX_TX[1:10+(tag>=2)]: take(w,s)
                tax.append(dict(row=j,item=i,absolute=start,length=p-start,tag=tag,hex=b[start:p].hex()))
            vec('Ntxr',4,0x1040462,item,True)
            def date_pair(i):
                for s in (0x1040529,0x104053f,0x1040554): take(4,s)
            vec('extra_d8',4,0x10404d1,date_pair)
            def last(i):
                for s,w in zip((0x3daa131,0x3daa150,0x3daa170,0x3daa18c,0x3daa1a8,0x3daa1c4,0x3daa1e0,0x3daa209),(1,4,4,1,1,1,1,1)): take(w,s)
            vec('extra_78',4,0x3d74e62,last)
        # Opaque previously closed client-tail grammar, reused only to reach identity.
        for s,w in zip(range(0x10405c7,0x10406e8,0x24),(1,4,4,4,4,1,1,4,1)): take(w,s)
        for w,s,k,tx in [(1,0x1040717,'A',((0x3d8771f,4),(0x3d87742,1))),
                          (4,0x10407b0,'B',((0x448faaf,4),(0x448facf,4),(0x448faeb,4),(0x448fb07,4),(0x448fb23,4),(0x448fb33,4),(0x448fb4d,4))),
                          (4,0x104086c,'C',((0x448faaf,4),(0x448facf,4),(0x448faeb,4),(0x448fb07,4),(0x448fb23,4),(0x448fb33,4),(0x448fb4d,4))),
                          (4,0x1040927,'D',((0x3d88320,4),(0x3d88345,4),(0x3d8838c,4)))]:
            vec(k,w,s,lambda i:[take(ww,ss) for ss,ww in tx],True)
        if mode:
            for s,w in zip(range(0x10409f0,0x1040b7d,0x24),[4]*10+[2,1]): take(w,s)
        ident_at=p; ident=S.unpack('<III',take(12,0x3c60119))
        ck(ident[0]==j and ident[0]<10000001 and ident[1]!=0 and ident[1]==ident[2] and ident[1] not in ids,
            f'identity row {j} @{ident_at} {ident}')
        ids.add(ident[1]); lens[p-begin]+=1
        ck(sum(w*n for _,_,w,n in events)==p-begin,'trace coverage')
        rows.append(dict(row=j,wire13=begin,legacy14=begin+1,end=p,identity_at=ident_at,identity=list(ident),
                         length=p-begin,wire_sha256=H(b[begin:p]),legacy_sha256=H(b[begin+1:p+1]),
                         tax=collections.get('Ntxr'),trace_sha256=H(json.dumps(events,separators=(',',':')).encode())))
    if only is None: ck(b[p:]==FOOT and p+9==len(b),'footer/EOF')
    return dict(mode=mode,rows=rows,tax_items=tax,visits=visits,wire_header=13,wire_footer=9,footer_at=p,footer_hex=b[p:].hex(),
                legacy_header=14,legacy_footer=8,selector_hist=hist(sels),row_len_hist=hist(lens),row_count=len(rows),
                tax_count=len(tax),tax_count_hist=hist(r['tax'][1] for r in rows if r['tax']),item_len_hist=hist(x['length'] for x in tax),
                item_tag_hist=hist(x['tag'] for x in tax),payload_sha256=H(b),payload_len=len(b))


def field_results(items,fs):
    ans={}
    for k,(cmp,load,obj,off,fmt) in for_key.items():
        xml=next(x for x in fs if x['field']==k); w=S.calcsize('<'+fmt)
        vals=[S.unpack_from('<'+fmt,bytes.fromhex(r['hex']),off)[0] for r in items]
        minv,maxv=xml.get('min_value'),xml.get('max_value')
        sentinel=(lambda v:v<0) if k in ('capa','leve') else (lambda v:v<=0) if k=='fram' else (lambda v:False)
        live=[v for v in vals if not sentinel(v)]
        sample=lambda r,v:{'row':r['row'],'item':r['item'],'absolute':r['absolute']+off,'raw':r['hex'][2*off:2*(off+w)],'value':v}
        first=lambda f:next((sample(r,v) for r,v in zip(items,vals) if f(v)),None)
        invalid=first(lambda v:not sentinel(v) and minv is not None and not float(minv)<=v<=float(maxv))
        status='L3' if live and invalid is None and minv is not None else 'held'
        # The reader canonicalizes ppty 0 to 1; keep a raw histogram and separately report the getter-visible domain.
        reason=('scoped 4CC/getter/sink and all live values within XML numeric domain' if status=='L3' else
                'raw live domain conflicts with frozen XML' if invalid else 'no live samples' if not live else
                'XML enum has no enum_ref; direct boxing proven, enum domain not independently closed')
        tx=next(s for s,_,m in TAX_TX if m==obj)
        ans[k]=dict(status=status,reason=reason,schema=xml,compare=cmp,getter_load=load,object_offset=obj,reader_site=tx,
                    static_item_offset=off,accepted_item_offset=off if status=='L3' else None,format=fmt,width=w,
                    total=len(vals),live=len(live),sentinels=len(vals)-len(live),live_min=min(live,default=None),live_max=max(live,default=None),
                    distinct_live=len(set(live)),top=Counter(vals).most_common(10),first_live=first(lambda v:not sentinel(v)),
                    first_sentinel=first(sentinel),first_counterexample=invalid or (first(lambda v:v==0) if k=='ppty' else first(lambda v:True) if status=='held' else None))
        if k=='ppty': ans[k]['stored_hist']=hist(1 if v==0 else v for v in vals)
    return ans

VTS={9:0x1418898d8,10:0x1418893b8}
READERS={9:0x105cb10,10:0x103fac0}
CFGS=(0x103fac0,0x420c8f0,0x35b07f0,0x448f890,0x39dd7b0,0x3d74e30,0x3daa110,
      0x3c600f0,0x3d87700,0x448fa90,0x3d88300,0x105cb10,0x41ba910,0x41babb0,0x3d86430,0x105f2b0)
WIRE={0x103fb76,0x103fc63,0x103fc9b,0x103fea6,0x103ff2a,0x103ff58,0x1040144,0x1040166,
      0x1040485,0x10404b2,0x10404e3,0x104057c,0x104073b,0x1040779,0x10407d6,0x1040847,
      0x1040898,0x1040908,0x1040980,0x10409c9,0x420ca3f,0x420ca66,0x3c60131,
      0x35b0847,0x3d74f70,0x3d74fc3}
EXTERNAL={0x103fae6,0x10409d3,0x35b0835,0x3d74e70}
DEAD={0x104094a,0x39dd7bc,0x3d74fef,0x3d8832f,0x3d88373}


def static(visits):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    p=PE(EXE); ck(H(p.raw)==EXEH,'editor SHA'); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64); m.detail=True
    rec={}; branches=[]; extents={}
    def ins(o): return next(m.disasm(p.raw[o:o+15],p.f2va(o),count=1))
    def blob(o,n):return dict(file_offset=o,VA=p.f2va(o),bytes=p.raw[o:o+n].hex())
    def record(o,i=None):
        if o not in rec:
            i=i or ins(o); t=i.operands[0] if i.operands else None
            rec[o]={**blob(o,i.size),'instruction':(i.mnemonic+' '+i.op_str).rstrip()}
            if t and t.type==X86_OP_IMM and (i.mnemonic=='call' or i.mnemonic.startswith('j')):
                rec[o]['direct_target']=p.va2f(t.imm)
        return rec[o]
    # Full cursor CFGs for table10; table9 graph captured, branch reduction limited to evidenced slices.
    for entry in CFGS:
        c=ReaderCFG(p,m,entry)
        extents[str(entry)]=dict(entry=entry,end_exclusive=c.function_end_off,reachable=len(c.instructions),external_edges=c.external_edges,
            coverage='partial branch reduction' if entry in (0x105cb10,0x105f2b0) else 'complete conditional branch census')
        for va,i in sorted(c.instructions.items()):
            o=p.va2f(va); record(o,i)
            if not i.mnemonic.startswith('j') or i.mnemonic=='jmp': continue
            t=rec[o]['direct_target']; q=o+i.size
            preds=[(v,ip) for v,ip in c.instructions.items() if v+ip.size==va]
            preceding=[]; v=va
            for _ in range(7):
                prev=next(((v0,ip) for v0,ip in c.instructions.items() if v0+ip.size==v),None)
                if prev is None:break
                v,ip=prev; preceding.append((p.va2f(v),ip))
                if ip.eflags or ip.mnemonic.startswith('j'):break
            pred,pi=preceding[-1] if preceding else (None,None)
            tx=next((p.va2f(v0) for v0,ii in c.instructions.items() if v0+ii.size==(p.f2va(pred) if pred else 0) and ii.mnemonic=='call'),None)
            operand=pi.op_str if pi else ''
            if entry in (0x105cb10,0x105f2b0):
                if entry!=0x105cb10:continue
                if not any(a<=o<=z for a,z in [(0x105d8ae,0x105da37),(0x105e24f,0x105e3d2),(0x105e9d7,0x105eb53)]):continue
            if o in DEAD:
                typ='dead'; why='taken requires zeroed AL to be nonzero, or null stream is subsequently dereferenced (effective-path exclusion)'
            elif o in EXTERNAL or (entry==0x105cb10 and '+ 0x588' in operand):
                typ='runtime-external'; why='caller mode or runtime length guard, not row selector/item tag'
            elif o in WIRE or (entry==0x105cb10 and (operand.startswith(('bl, byte ptr [rsp','rbp, rax','edi, eax','word ptr [rsp','byte ptr [rsp')))):
                typ='wire_data'; why='fresh stream count/item tag or computed directly from read data'
            elif (entry==0x103fac0 and t==0x1040930) or (entry==0x105cb10 and t==0x105de6c) or (pi and pi.mnemonic in ('cmp','test') and '+ 0x10], 0' in operand and tx is not None) or (entry in (0x420c8f0,0x41ba910,0x41babb0,0x3d86430) and '0x10], 0' in operand) or o in {0x35b083f,0x3d74fa3,0x3d74fac,0x448f8d3,0x448f8ef,0x448f90b,0x448f923,0x448f933,0x3d88360}:
                typ='IO-result'; why='stream status or call result; failure does not define an alternate valid record'
            else:
                typ='context-lifecycle'; why='memory/reference/allocation or callback state; no alternate supported wire layout inferred'
            branches.append(dict(site=o,function=entry,predicate=pred,predicate_instruction=rec.get(pred,{}).get('instruction'),taken=t,fallthrough=q,
                classification=typ,reason=why,first_counterexample=(dict(visits[str(tx)],mutation='truncate one byte before end of indicated first transfer') if typ=='IO-result' and str(tx) in visits else None)))
    common=[0x1041f30,0x1041f33,0x1043306,0x104330f,0x104331a,0x1043322,0x1065ef0,0x1065f22,0x1065f50,
        0x1065eb0,0x3d9519f,0x3d951a9,0x3d951cb,0x105fc60,0x3d8860d,0x3d88614,0x3d88628,0x3d88631,0x3d8863d,0x3d88644,
        0x105cb49,0x105cb56,0x105cb99,0x105cba0,0x105e1d6,0x105e1de,0x105e3dd,0xf2ba0e,0xf2ba23,0xf2ba38,0xf2ba51,0xf2b670,0xf28c13,
        0xf48f1d,0x1059a4f,0x1059a56,0xf48f37,0x103ec17,0x103ec1e,0xf48b30,0x1040bcf,0xfae340,0x144bcA0,
        0x814110,0xdb7f80,0x104e6b0,0x1072560,0x15cf370,0x105fb50,0x15cf4a0,0x105fbb0,0x104e6b0,0x1050d40]
    for o in common+[a for _,os,_ in ROUTES.values() for a in os]+[a for x in for_key.values() for a in x[:2]]:
        record(o)
    for k,(cmp,load,obj,*_) in for_key.items():
        ck(ins(cmp).operands[1].imm==int.from_bytes(k.encode(),'big') and ins(load).operands[1].mem.disp==obj,k+' getter')
    result={}
    for tid,vt in VTS.items():
        o=p.va2f(vt); col=p.va2f(S.unpack_from('<Q',p.raw,o-8)[0]); td=p.r2f(u(p.raw,col+12)); s=td+16; e=p.raw.index(0,s)
        slot2=S.unpack_from('<Q',p.raw,o+16)[0]; slot19=S.unpack_from('<Q',p.raw,o+152)[0]
        ck(p.va2f(slot2)=={9:0x1065eb0,10:0x1041f30}[tid] and p.va2f(slot19)==READERS[tid],f't{tid} slots')
        tab=0xf49d38; slot=tab+4*tid; dest=p.va2f(p.f2va(tab)+S.unpack_from('<i',p.raw,slot)[0]);ck(dest=={9:0xf48f12,10:0xf48f27}[tid],f't{tid} factory')
        result[str(tid)]=dict(factory=0xf48b30,factory_rel32=blob(slot,4),case=record(dest),rtti=p.raw[s:e].decode(),td=blob(td,e+1-td),col=blob(col,24),
            vtable_VA=vt,col_ptr=blob(o-8,8),slot2=blob(o+16,8),slot19=blob(o+152,8),reader=READERS[tid])
    for b in branches:
        b['predicate_instruction']=rec.get(b['predicate'],{}).get('instruction')
    return result,extents,list(rec.values()),branches


def negative(b,mode):
    try: walk(b,mode)
    except Check as e: return str(e)
    raise Check('wrong mode unexpectedly closed')


def build():
    manifest={x['path']:x['sha256'] for x in J(ROOT/'evidence/MANIFEST.json')['files']}
    for path in (MASTER,IDA): ck(H((ROOT/path).read_bytes())==manifest[path],path+' snapshot SHA')
    ck(manifest[MASTER]==MASTERH and EXEH in (ROOT/IDA).read_text(encoding='utf-8'),'input SHA anchors')
    master=J(ROOT/MASTER)['entities']['nation.xml'][0]['fields']; t37=J(ROOT/NEG[1]); t37m={r['parent_4cc']:r for r in t37['parents']}
    subs=sorted((ROOT/'scratch/t24/out').glob('subtables.part*.json')); indexes=[x for s in subs for x in J(s)['nested_fields']]
    meta,raw=read_archives(); srv=walk(raw['server','table_10.dat'],1); cli=walk(raw['client','table_10.dat'],0)
    ck(srv['row_count']==cli['row_count']==251 and [r['identity'] for r in srv['rows']]==[r['identity'] for r in cli['rows']], 'two archives identity')
    ck(not cli['tax_items'] and srv['tax_count']>0,'Ntxr reader modes have distinct coverage')
    visits={str(k):v for k,v in {**cli['visits'],**srv['visits']}.items()}
    factories,extents,ii,bb=static(visits)
    fields=field_results(srv['tax_items'],master[PARENTS['Ntxr']]['list_item_fields']); l3=sum(x['status']=='L3' for x in fields.values())
    sv=raw['server','table_10.dat']; cl=raw['client','table_10.dat']
    for side,replay in [('client',cli),('server',srv)]:
        md=meta[side]['members']['table_10.dat']; md.update(count_basis='251 checked identities read after cursor',stride='variable',row_len_hist=replay['row_len_hist'])
    parents={}
    for code,idx in PARENTS.items():
        f=master[idx]; n=t37m[code];tid,sites,note=ROUTES[code]; ck(f['field']==code and n['link_status']=='partial_parent_to_table_unknown','frozen scope '+code)
        match=[x for x in indexes if x['parent']==code]
        parents[code]=dict(schema_index=idx,schema=f,t24_nested_occurrences=match,t24_scope_status='unscoped matching parent code only' if match else 'not present in t24 shards; frozen master scope used',
            t37_original_status=n['link_status'],status='cursor_closed' if code=='Ntxr' else 'inline_static_reader_link_archive_replay_open' if tid else 'partial',
            owner_type=tid,table_type=tid,table_type_scope='owner only; no dedicated list case shown' if tid else 'unknown',
            independent_list_table=None,owner_rtti=factories[str(tid)]['rtti'] if tid else None,
            item_vptr_assessment='inline non-polymorphic values or pointers to POD; no per-item slot19 on this path' if tid else 'unresolved',
            persisted_item_stride={'Nntp':9,'Nctp':8,'Nrtp':8,'Nfmp':9,'NCro':9,'NTRv':4,'NWGv':4,'NSps':4,'Ntxr':[23,25]}.get(code),
            item_count=srv['tax_count'] if code=='Ntxr' else None,
            member=f'table_{tid}.dat' if tid else None,member_assessment='reader confirmed; specific archive modes unbound for table9; sidecar not assigned' if tid==9 else 'server mode has Ntxr; client mode bypasses Ntxr' if tid else 'unknown',
            reader=READERS[tid] if tid else None,sites=sites,collection=note)
    prov=dict(editor_path=str(EXE),editor_sha256=EXEH,frozen_snapshots={x:manifest[x] for x in (MASTER,IDA)},
              baseline_unchanged={x:H((ROOT/x).read_bytes()) for x in NEG},t24_sha256={s.relative_to(ROOT).as_posix():H(s.read_bytes()) for s in subs})
    a=srv['tax_items'][0]['absolute']; port=sv[:a]+b'\1'+sv[a+1:a+23]+sv[a+25:]
    older=walk(port,1); ck(older['item_len_hist']=={23:1,25:1898} and older['footer_at']==srv['footer_at']-2,'tag=1 synthetic path')
    tag_only=sv[:a]+b'\1'+sv[a+1:]; bad_tag=negative(tag_only,1)
    controls={'tax_tag1_remove_two_bytes':dict(at=a,raw_tag=sv[a],synthetic_tag=1,new_length=older['tax_items'][0]['length'],new_footer_at=older['footer_at']),
              'tax_tag1_without_deletion_first_failure':bad_tag,
              'server_mode0':negative(sv,0),'client_mode1':negative(cl,1),
              'tax_item_short_read':negative(sv[:a-4]+S.pack('<I',1)+sv[a:a+4],1)}
    first_empty=next(r for r in srv['rows'] if r['tax'][1]==0)
    manual={0x420ca3f:controls['tax_tag1_remove_two_bytes'],0x420ca66:{'row':0,'item':0,'absolute':a+15,'mutation':'zero person-type input makes stored byte 1; consumes same bytes'},
            0x1040485:{'row':first_empty['row'],'absolute':first_empty['tax'][0],'count':0},
            0x10404b2:{'row':0,'count':8,'taken':7,'fallthrough':1},0x103fae6:{'wrong_mode':controls['server_mode0']},
            0x10409d3:{'wrong_mode':controls['client_mode1']},0x420c93a:{'negative':controls['tax_item_short_read']}}
    for br in bb:
        if br['site'] in manual: br['first_counterexample']=manual[br['site']]
    for kind,rs,n in [('instructions',sorted(ii,key=lambda r:r['file_offset']),500),('branches',bb,220)]:
        for j in range(0,len(rs),n): output(f'{kind}.part{j//n+1:03}.json',rs[j:j+n])
    output('discovery_nation_unknown.json',dict(status='partial_static_discovery',provenance=prov,archives=meta,factory=factories,extents=extents,
        parents=parents,static_inline_links=9,closed_parents=1,unknown_links=6,new_L3=l3,L4=0,
        t9_owner_fixup=dict(slot20=0x105fc60,body=0x3d885f0,nation_pointer_sink=0x3d88628,backlink_write=0x3d88644,
            equation='NATION+0x108+8*container[0xb9] = container; slot2 uses index=0',
            scope='conditional resolver success and nonnull; no assumption that all archive nation rows have index 0')))
    output('cursor_nation_tax.json',dict(archives={s:meta[s]['members']['table_10.dat'] for s in ('client','server')},server=srv,client=cli,
        item_transfer_sequence=TAX_TX,controls=controls,wrong_mode_first={k:controls[k] for k in ('client_mode1','server_mode0')},
        footer_semantics='wire vector count=0, flag 1, observed final value equals maximum identity; identity is checked after each complete row',
        item_coordinates='Ntxr item starts at current cursor; parent-relative offset varies by row; legacy base differs from selector base by 1'))
    output('fields_nation_tax.json',dict(scope='nation.xml#nation / Ntxr',L3=l3,L4=0,fields=fields,xml_occurrence_source=MASTER))
    print(f'15 parents; 9 inline static reader links; Ntxr {srv["tax_count"]} items, 251 rows per archive, L3={l3}, L4=0')


def selftest():
    b=HEAD+S.pack('<I',0)+b'\0'+FOOT
    ck(walk(b,0)['footer_at']==13,'zero rows')
    ck('footer' in negative(b+b'\0',1),'reject trailing bytes')
    ck(sum(w for _,w,_ in TAX_TX)==25 and sum(w for _,w,_ in TAX_TX[:-1])==23,'tax transfer widths')


def main():
    p=argparse.ArgumentParser(description=__doc__); g=p.add_mutually_exclusive_group(); g.add_argument('--selftest',action='store_true');g.add_argument('--build',action='store_true'); a=p.parse_args()
    try:
        if a.selftest:selftest();print('t47 selftest PASS')
        else:build()
        return 0
    except Check as e: print('CHECK:',e,file=sys.stderr); return 1
    except Exception as e: print('FATAL:',type(e).__name__,e,file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
