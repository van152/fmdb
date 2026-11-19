#!/usr/bin/env python3
"""Rebuild t49: offline NATIONAL_TEAM_CONTAINER wire replay and evidence."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t49/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
HEAD = bytes.fromhex('03017461642ef10d')
PARENTS = {'Nntp':(224,1,9,0x105e264,0x41ba910), 'Nctp':(225,1,8,0x105e2e9,0x41babb0),
           'Nrtp':(226,1,8,0x105e369,0x41babb0), 'NTRv':(228,1,4,0x105e9ec,0x105ea36),
           'NWGv':(229,1,4,0x105ea6b,0x105eab5), 'NSps':(230,1,4,0x105eaea,0x105eb34),
           'Nfmp':(233,2,9,0x105d99c,0x3d86430), 'NCro':(231,4,9,0x105f304,0x105f487)}
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'
T47='scratch/t47/out/discovery_nation_unknown.json'
BASE='scratch/t37/out/nation_subtable_inventory.json'
IDA='evidence/fm24/reports/qa/IDA_PROVENANCE.md'

class Check(Exception): pass

def need(cond,msg):
    if not cond: raise Check(msg)

def digest(x): return sha256(x).hexdigest()
def J(p): return json.loads((ROOT/p).read_bytes())
def put(name,obj): (OUT/name).write_text(json.dumps(obj,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8')
def hist(xs): return dict(sorted(Counter(xs).items()))

class Cursor:
    def __init__(self,b): self.b=b; self.p=13; self.row=-1; self.events=[]
    def fail(self,at,site,kind,**info):
        raise Check(dict(row=self.row,absolute=at,site=site,kind=kind,raw=self.b[at:at+8].hex(),**info))
    def cut(self,w,s,n=1):
        at=self.p; end=at+w*n
        if not 0<=w*n<=len(self.b)-at: self.fail(at,s,'short transfer',width=w,repeat=n)
        self.p=end; self.events.append([s,at,w,n]); return self.b[at:end]
    def num(self,w,s,signed=False): return int.from_bytes(self.cut(w,s),'little',signed=signed)
    def count(self,w,s,itemmin,signed=True):
        at=self.p; v=self.num(w,s,signed)
        if not 0<=v<=(len(self.b)-self.p)//itemmin: self.fail(at,s,'invalid count',value=v,width=w,item_min=itemmin)
        return v
    def vec(self,w,s,stride,s2,signed=True):
        n=self.count(w,s,stride,signed)
        if n: self.cut(stride,s2,n)
    def string(self):
        n=self.count(4,0x35b0828,1,False)
        if n: self.cut(1,0x35b0883,n)

def collection(c,rows,key,tag=None,gate=None):
    _,w,stride,s,item=PARENTS[key]; at=c.p
    n=c.count(w,s,stride,key not in ('NTRv','NWGv','NSps'))
    start=c.p
    for _ in range(n):
        for site,width in ITEM_TRANSFERS[key]: c.cut(width,site)
    need(c.p-start==stride*n, f'{key} item EOF')
    rows[key]=dict(count_at=at,count=n,start=start,end=c.p,gate=gate,tag=tag)

def full_prefix(c,cols):
    for s,w in [(0x105cbcf,2),(0x105cbf4,4),(0x105cc19,4),(0x105cc6c,4)]: c.cut(w,s)
    for _ in range(c.count(4,0x105cc9d,8)):
        c.cut(4,0x105cd0d); c.cut(4,0x105cd2d)
    for s,w in [(0x105cd5a,4),(0x105cd81,2),(0x105cdb6,4),(0x105cdda,2),(0x105cdfe,2),(0x105ce56,1),(0x105ce7a,4),(0x105cfcc,1),(0x105cff0,2),(0x105d014,4),(0x105d038,2),(0x105d088,4)]: c.cut(w,s)
    for s in (0x360e3ce,0x838b6b):
        at=c.p; n=c.count(4,s,6 if s==0x360e3ce else 2,False)
        if n: c.fail(at,s,'typed container not reduced (observed-zero path only)',value=n)
    for _ in range(2): c.vec(4,0x3d81aff,2,0x3d81b7b,False)
    c.vec(1,0x105d128,4,0x105d170)
    c.vec(2,0x105d1a9,4,0x105d1ef)
    for groups in range(5):
        for s,t in [(0x105d2d8,0x105d339),(0x105d375,0x105d3c1),(0x105d3fd,0x105d449),(0x105d485,0x105d4d1)]: c.vec(1,s,4,t)
    c.vec(2,0x105d52d,4,0x105d573)
    for s in (0x105d644,0x105d6ce):
        for _ in range(c.count(2,s,36)):
            tag=c.num(1,0x1570e83)
            for _ in range(3): c.string()
            for t,w in ((0x1570efa,2),(0x1570f2c,1),(0x1570f48,2),(0x1570f64,4),(0x1570f80,4)): c.cut(w,t)
            if tag>=2:
                c.cut(4,0x1570faf)
                for _ in range(c.count(4,0x15724b2,12)):
                    for t in (0x157262f,0x157264e,0x157266d): c.cut(4,t)
                c.cut(1,0x1570fe3); c.cut(4,0x39dd7d4)
            for t in (0x157100f,0x157102f,0x157104f,0x157106f): c.cut(1,t)
            if tag>=5: c.cut(1,0x1571096); c.cut(4,0x15710b6)
            for t in (0x15710d6,0x15710f6,0x1571116,0x1571136): c.cut(2,t)
            for t in (0x1571156,0x1571176,0x1571196): c.cut(1,t)
            for t in (0x15711b6,0x15711d6): c.cut(4,t)
            for gate,t in ((3,0x15711fd),(4,0x1571224),(6,0x157124e)):
                if tag>=gate: c.cut(1,t)
    at=c.p; present=c.num(1,0x105d8c6)
    if present:
        tag=c.num(1,0x105f2e7)
        collection(c,cols,'NCro',tag,[at,present])
    else: cols['NCro']=dict(count_at=None,count=None,start=None,end=None,gate=[at,present],tag=None)
    collection(c,cols,'Nfmp')
    for _ in range(2):
        for _ in range(c.count(4,0x10733c2,18)):
            for s,w in [(0x443aef1,1),(0x443af0d,1),(0x443af29,4),(0x443af46,1),(0x443af61,11)]: c.cut(w,s)
    for _ in range(c.count(2,0x105db62,14)):
        for s,w in [(0x3d8762f,4),(0x3d8764b,4),(0x3d87667,4),(0x3d87683,1),(0x3d876ac,1)]: c.cut(w,s)
    for _ in range(c.count(4,0x1073732,10)):
        for s,w in [(0x39b9d81,1),(0x39b9da1,1),(0x39b9dc0,4),(0x39b9ddc,1),(0x39b9df8,1),(0x39b9e14,1),(0x39b9e33,1)]: c.cut(w,s)
    c.cut(1,0x105dc2b); c.cut(4,0x105dcd5)
    if c.num(1,0x105dd07):
        c.cut(4,0x4387ae0)
        for _ in range(c.count(4,0x155c152,10)):
            tag=c.num(2,0x155c2f9,True)
            c.cut(4,0x155c31a); c.cut(1,0x155c33d); c.cut(1,0x155c360)
            c.cut(2 if tag>=2 else 1,0x155c38d if tag>=2 else 0x155c3b5)
            c.cut(1,0x155c3e0)
            if tag>=3: c.cut(1,0x155c40c)

def full_base_tail(c):
    # Same-width transfers grouped, with the vcall site order retained.
    for s in range(0x105e7e9,0x105e8c2,0x24): c.cut(4,s)
    for s,w in [(0x105e8e5,1),(0x105e95e,4),(0x105e982,1),(0x105e9a6,2),(0x105e9ca,1)]: c.cut(w,s)

def common(c,mode,cols):
    c.cut(4,0x105dd87)
    for s in (0x105dddf,0x105de03,0x105de23,0x105de43,0x105de63,0x105def3,0x105df21): c.cut(1,s)
    c.cut(4,0x105df58)
    for s in (*range(0x105df7c,0x105e109,0x24),0x105e15c,0x105e180,0x105e1a4,0x105e1c8): c.cut(1,s)
    for k in ('Nntp','Nctp','Nrtp'): collection(c,cols,k)
    for s in (0x105e619,0x105e63d,0x105e661,0x105e685): c.cut(2,s)
    if mode:
        full_base_tail(c)
        for k in ('NTRv','NWGv','NSps'): collection(c,cols,k)
        for s in range(0x105ec47,0x105edf8,0x24): c.cut(1,s)
        for s,w in [(0x105ee1b,4),(0x105ee3f,4),(0x105ee63,2),(0x105ee87,1),(0x105eeab,1),(0x105eecf,2)]: c.cut(w,s)

def team_tail(c,mode):
    c.cut(1,0x3fc2050)
    c.cut(2,0x11d0f6f)
    if mode:
        for s,t,sgn in [(0x11d10e0,0x11d1344,False),(0x11d139d,0x11d1564,False),(0x11d15c5,0x11d1725,True),(0x11d177b,0x11d18e5,True),(0x11d193b,0x11d1ab7,False)]:
            c.vec(1,s,4,t,sgn)
        c.vec(1,0x11d1b03,16,0x11d1b91,False)
        for _ in range(c.count(2,0x11d1bf2,28)):
            for s,w in [(0x11d1e65,4),(0x11d1e86,4),(0x11d1eb0,8),(0x11d1ef4,2),(0x11d1f1e,4),(0x39dd7d4,4),(0x11d1f68,1),(0x11d1f8c,1)]: c.cut(w,s)
    return c.p,struct.unpack('<III',c.cut(12,0x11d21df))

def walk(b,mode,limit=None):
    need(len(b)>=13 and b[:8]==HEAD,'header'); n=struct.unpack_from('<I',b,8)[0]
    c=Cursor(b); rows=[]; ids=set(); first={}
    for j in range(n if limit is None else limit):
        c.row=j; c.events=[]; a=c.p; cols={}
        selector=c.num(1,0xf2ba0e)
        if selector!=0: c.fail(a,0xf2ba0e,'selector outside confirmed domain',value=selector)
        if mode: full_prefix(c,cols)
        common(c,mode,cols)
        at,ident=team_tail(c,mode)
        if ident[0]!=j or ident[1]!=ident[2] or not ident[1] or ident[1] in ids:
            c.fail(at,0x11d21df,'identity after reader',value=ident)
        ids.add(ident[1]); end=c.p
        for s,p,w,nrep in c.events: first.setdefault(s,dict(row=j,absolute=p,width=w,repeat=nrep))
        rows.append(dict(row=j,selector=selector,wire13=a,legacy14=a+1,end=end,length=end-a,identity_at=at,identity=ident,
            wire_sha256=digest(b[a:end]),legacy_sha256=digest(b[a+1:end+1]),collections=cols,trace=c.events))
    footer=None
    if limit is None:
        if len(b)-c.p!=9: c.fail(c.p,0xf2ba99,'footer/EOF',remaining=len(b)-c.p)
        count,flag,maxid=struct.unpack_from('<IBI',b,c.p)
        if (count,flag,maxid)!=(0,1,max(ids,default=0)): c.fail(c.p,0xf2ba99,'footer disagreement',value=(count,flag,maxid))
        footer=dict(absolute=c.p,count=count,flag=flag,last_u32=maxid,equals_observed_max_identity=True,raw=b[c.p:].hex())
    return dict(mode=mode,payload_len=len(b),payload_sha256=digest(b),rows=rows,row_count=len(rows),row_sum=sum(r['length'] for r in rows),
        wire_header=13,wire_footer=9,legacy_header=14,legacy_footer=8,footer=footer,first_site=first,
        selector_hist=hist(r['selector'] for r in rows),row_len_hist=hist(r['length'] for r in rows))


ITEM_TRANSFERS={
    'Nntp':((0x41ba930,4),(0x41ba94c,1),(0x41ba967,1),(0x41ba983,1),(0x41ba99f,1),(0x41ba9c8,1)),
    'Nctp':((0x41babd0,4),(0x41babeb,1),(0x41bac07,1),(0x41bac23,1),(0x41bac4c,1)),
    'Nfmp':((0x3d86451,4),(0x3d86475,2),(0x3d86491,1),(0x3d864ad,1),(0x3d864d6,1)),
    'NCro':((0x105f487,1),(0x105f4a6,4),(0x105f4cf,4))}
ITEM_TRANSFERS['Nrtp']=ITEM_TRANSFERS['Nctp']
ITEM_TRANSFERS.update({k:((PARENTS[k][4],4),) for k in ('NTRv','NWGv','NSps')})

# Field, item offset, encoding, object offset, exact 4CC compare, getter load, transfer index.
def mappings():
    out={}
    for k,f,cmp,load in [('Nntp','nati',0x41bbabf,0x41bbac7),('Nctp','cont',0x3dae130,0x3dae138),('Nrtp','regi',0x3daefc0,0x3daefc8)]:
        z=int(k=='Nntp'); out[k]={f:(0,'i',8,cmp,load,0),
            'rati':(4+z,'b',0,0x41bdb64,0x41bdb70,1+z),
            'mina':(5+z,'b',2,0x41bdb58,0x41bdc32,2+z),
            'maxa':(6+z,'b',1,0x41bdaed,0x41bdaf9,3+z),
            'affl':(7+z,'b',3,0x41bdae1,0x41bdbce,4+z)}
        if z: out[k]['sckn']=(4,'b',4,0x41bbab7,0x41bbadd,1)
    for k in ('NTRv','NWGv','NSps'):
        out[k]={'repu':(None,None,12,0x449721f,0x449722b,None),'valu':(0,'i',8,0x4497217,0x4497287,0)}
    out['Nfmp']={'pers':(0,'i',0,0x1077dd8,0x1077de4,0),'desc':(4,'h',8,0x1077d33,0x1077df5,1),
        'heig':(6,'b',10,0x1077d3f,0x1077eb1,2),'side':(7,'B',11,0x1077dc0,0x1077e50,3),
        'perm':(7,'B',11,0x1077d4b,0x1077d57,3),'rtng':(8,'b',12,0x1077dcc,0x1077f0d,4)}
    out['NCro']={'comp':(1,'i',0,0x1076c08,0x1076c14,1),'crep':(5,'i',8,0x1076c00,0x1076c33,2)}
    return out

DB_KEYS=('table_9.dat','table_extra_9.dat','table_extra_10.dat','table_3.dat','table_5.dat','table_10.dat','table_19.dat','table_25.dat')

def dbroot():
    p=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if p.drive.upper()=='Z:': raise ValueError('Z: forbidden')
    return p

def archives():
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    entries=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    raw={}; meta={}
    for side,expected in [('client',31),('server',77)]:
        _,b,d=entries(dbroot()/f'{side}_db.dat'); es={e['path']:e for e in d['entries']}; base=d['data_base']
        need(base==34 and len(es)==expected,side+' directory')
        meta[side]=dict(data_base=base,directory_count=len(es),archive_sha256=digest(b),members={})
        for k in DB_KEYS:
            e=es.get(f'{side}_db/{k}')
            if not e:
                meta[side]['members'][k]={'present':False}; continue
            lo=base+e['offset']; hi=lo+e['packed_size']; bounds=min((base+x['offset'] for x in es.values() if x['offset']>e['offset']),default=d['toc_offset'])
            need(lo<hi<=bounds,(side,k,'bounds'))
            part=b[lo:hi]; fs=[]; good=[]; p=0
            while p<len(part):
                need(part[p:p+4]==b'\x28\xb5\x2f\xfd',(side,k,p,'magic'))
                stream=z.ZstdDecompressor().decompressobj(); payload=stream.decompress(part[p:]); w=len(part)-p-len(stream.unused_data)
                need(stream.eof and w>0,(side,k,p,'frame'))
                fs.append([lo+p,w,len(payload)])
                if len(payload)==e['size']: good.append((payload,fs[-1]))
                p+=w
            need(len(good)==1,(side,k,'frame size selector'))
            payload,frame=good[0]; raw[side,k]=payload
            meta[side]['members'][k]=dict(present=True,entry={**e,'sha256':digest(part)},bounds=[lo,hi,bounds],frame=frame,frames=fs,
                payload_sha256=digest(payload),payload_size=len(payload),header_count=struct.unpack_from('<I',payload,8)[0])
    return raw,meta


def targets(raw):
    import zstandard as z
    result={}; docs={}
    def save(key,vals,method,b):
        result[key]=vals; docs[key]=dict(method=method,count=len(vals),payload_sha256=digest(b),
            ordinal_trace_sha256=digest(b''.join(struct.pack('<I',i) for i in sorted(vals))))
    def read_tails(b,ats,markers=(0,)):
        d={}
        for i,o in enumerate(ats):
            j,u,v=struct.unpack_from('<III',b,o)
            need(i==j and u==v and u!=0 and b[o+12] in markers,(i,o,'target identity')); d[j]=u
        need(len(set(d.values()))==len(d),'target unique identities')
        return d
    for side in ('client','server'):
        for tid,strides in [(5,(34,48)),(19,(45,46)),(25,(127,None))]:
            w=strides[side=='server']; b=raw[side,f'table_{tid}.dat']
            if w is None: continue # NCro has no live join, no server competition claim.
            n=struct.unpack_from('<I',b,8)[0]; need(13+n*w+9==len(b),'fixed target EOF')
            d=read_tails(b,(13+(i+1)*w-12 for i in range(n)))
            save(f'{side}_t{tid}',d,f'ordered identity tails, measured {w}-byte rows',b)
    for side in ('client','server'):
        b=raw[side,'table_10.dat']; prior=J('scratch/t47/out/cursor_nation_tax.json')[side]
        need(digest(b)==prior['payload_sha256'],'t10 payload')
        save(f'{side}_t10',read_tails(b,(r['identity_at'] for r in prior['rows'])),'re-read byte-level identity at t47 closed row tail; no tax replay',b)
    b=raw['client','table_3.dat']; t24=J('scratch/t24/out/cursor.json'); need(digest(b)==t24['provenance']['payload_sha256'],'t3 payload')
    ends=[]
    for shard in t24['rows']['shards']:
        data=J('scratch/t24/out/'+shard)
        ends.extend(r[3] for r in (data if isinstance(data,list) else data['rows']))
    need(len(ends)==t24['row_count'] and ends[-1]==len(b)-9,'t3 source')
    save('client_t3',read_tails(b,(end-12 for end in ends),(0,12)),'actual client t24 CLUB rows; diagnostic only, no affl FK',b)
    part=(dbroot()/'basic_people_db.dat').read_bytes(); dz=z.ZstdDecompressor().decompressobj(); b=dz.decompress(part[8:]); need(dz.eof and not dz.unused_data,'person frame')
    need(part[:12]==HEAD+b'\x28\xb5\x2f\xfd' and struct.unpack_from('<IB',b)==(658011,0),'person framing')
    p=5; d={}; classes=Counter(); class_by_ordinal={}
    for i in range(658011):
        tag,cls=b[p:p+2]; w={1:83,2:83,3:83,4:34,5:22}.get(cls)
        need(tag==17 and w is not None and p+w<=len(b),(i,p,'person class/bounds'))
        class_by_ordinal[i]=cls
        j,u,v=struct.unpack_from('<III',b,p+w-12)
        need(j==i and u==v and u!=0,(i,p,'person identity')); d[j]=u; classes[cls]+=1; p+=w
    need(b[p:]==bytes.fromhex('00000000014cbd5477'),'person EOF')
    save('person',d,'basic_people_db whole class-width walk, key from raw identity tail',b)
    docs['person'].update(class_hist=dict(classes),footer=b[p:].hex(),compressed_sha256=digest(part[8:]))
    return result,docs,class_by_ordinal

REF_TABLE={'nati':10,'cont':5,'regi':19,'pers':'person','comp':25}
MASK={'side':7,'perm':8}
AGE_RATING={'mina':(14,44),'maxa':(15,45),'rtng':(1,20),'crep':(0,200)}
FIELD_ROUTE={'Nntp':[0x3db2abe,0x1074c70,0x3dabd68,0x141cff0,0x41bbb43,0x141d110],
    'Nctp':[0x3db2d5e,0x1075240,0x3dae158,0x141d110], 'Nrtp':[0x3db321e,0x10758a0,0x3daefe8,0x141d110],
    **{k:[0x15d1300,0x4496fb7,0x4496fbb,0x4496fdb,0x1079c90,0x3db59e1,0x10788d0,0x3db24f8,0x15d1540] for k in ('NTRv','NWGv','NSps')},
    'Nfmp':[0x3db537e,0x1077b20], 'NCro':[0x3db27f9,0x1076a50]}
FIXUPS={'nati':[0x3d88740,0x3d8874a,0xf7ef30], 'cont':[0x3d887a0,0x3d887aa,0xf7e820,0x3bf4a90],
        'regi':[0x3d88770,0x3d8877a,0xf7f240,0x3bf6120], 'pers':[0x3d887e0,0x3d887ea,0x3d887ed,0xf7f850,0x3bf9220,0x3bf9282,0x3bf92a2],
        'comp':[0x3d88830,0x3d88847,0xf7e280]}


def field_ledgers(raw,cursors,domains,classes,master,source):
    scope=master['entities']['nation.xml'][0]['fields']; by_parent={}
    for key, specs in mappings().items():
        idx,cw,stride,count_site,_=PARENTS[key]; node=scope[idx]; parent=source['parents'][key]
        need(node['field']==key and sum(r['field']==key for r in scope)==1 and parent['schema']==node,key+' frozen scope')
        by_side={}; samples={};
        for side,cur in cursors.items():
            b=raw[side,'table_9.dat']; sample=[]; counts=[]; absent=0; gate_absent=0; first_zero=None; first_absence=None; first_gate_absence=None; dg=sha256()
            for row in cur['rows']:
                j=row['row']; col=row['collections'].get(key)
                if col is None:
                    absent+=1
                    if first_absence is None: first_absence=dict(row=j,selector_at=row['wire13'],mode=cur['mode'])
                    continue
                n=col['count']
                if n is None:
                    gate_absent+=1
                    if first_gate_absence is None: first_gate_absence=dict(row=j,absolute=col['gate'][0],value=col['gate'][1])
                    continue
                counts.append(n)
                if n==0 and first_zero is None: first_zero=dict(row=j,absolute=col['count_at'],value=0)
                p=col['start']
                for i in range(n):
                    chunk=b[p:p+stride]; need(len(chunk)==stride and p+stride<=row['identity_at'],key+' bounds')
                    sample.append((j,i,p,chunk)); dg.update(chunk); p+=stride
                need(p==col['end'],key+' exact item EOF')
            samples[side]=sample
            by_side[side]=dict(mode=cur['mode'],count_sites_visited=len(counts),count_hist=hist(counts),wire_items=len(sample) if absent!=251 else None,
                rows_with_items=sum(n>0 for n in counts),mode_bypass_rows=absent,absent_gate_rows=gate_absent,
                first_zero=first_zero,first_mode_bypass=first_absence,first_gate_absence=first_gate_absence,item_sequence_sha256=dg.hexdigest() if counts else None)
        if key in ('Nntp','Nctp','Nrtp'):
            need([(a,b,d) for a,b,_,d in samples['client']]==[(a,b,d) for a,b,_,d in samples['server']],key+' cross-archive transfer bytes')
        ledger={}
        for field,(off,fmt,obj,cmp,load,idx_sink) in specs.items():
            occ=[x for x in node['list_item_fields'] if x['field']==field]
            need(len(occ)==1,key+' '+field+' unique occurrence')
            s=occ[0]; fmt2=struct.Struct('<'+fmt) if fmt else None; per_side={}; any_values=False; invalid=False
            enum=master['enums'].get(s.get('enum_ref',field),{}) if s['type']=='enum' else {}
            enum_values={int(e['enum_id'] or e['enum']) for e in enum.get('values',[])}
            bounds=AGE_RATING.get(field) or ((-2,20) if field=='rati' and key!='Nntp' else (0,2147483647) if field=='valu' else None)
            for side,items in samples.items():
                target=REF_TABLE.get(field); target_key=('person' if target=='person' else f'{side}_t{target}') if target else None
                domain=domains.get(target_key,{}); uid_set=set(domain.values()) if items and target else set()
                vs=[]; raw_vs=[]; sent=0; hits=0; misses=0; uid_hits=0; diag_hits=0; diag_n=0; bad=first=first_sent=first_miss=first_uid_miss=None; cls=Counter()
                for row,i,p,chunk in items:
                    v=fmt2.unpack_from(chunk,off)[0] if fmt2 else i
                    at=p+off if fmt2 else None; value=((v&MASK[field])>>(3 if field=='perm' else 0)) if field in MASK else v
                    sample=dict(row=row,item=i,absolute=at,raw=chunk[off:off+fmt2.size].hex() if fmt2 else None,raw_value=v,value=value)
                    if first is None: first=sample
                    raw_vs.append(v); vs.append(value)
                    if target:
                        if (target=='person' and v==0) or (target!='person' and v==-1): sent+=1; first_sent=first_sent or sample; continue
                        if v in domain:
                            hits+=1
                            if target=='person': cls[classes[v]]+=1
                        else: misses+=1; first_miss=first_miss or sample
                        if v in uid_set: uid_hits+=1
                        else: first_uid_miss=first_uid_miss or sample
                    if field=='affl' and v!=0: diag_n+=1; diag_hits+=int(v in domains['client_t3'])
                    if bounds and not bounds[0]<=value<=bounds[1]: bad=bad or sample
                    if enum_values and value not in enum_values and not (field=='affl' and value==0): bad=bad or sample
                any_values |= bool(vs); invalid |= bad is not None or misses!=0
                rec=dict(total=len(vs),range=[min(vs),max(vs)] if vs else None,distinct=len(set(vs)),zeros=vs.count(0),top=Counter(vs).most_common(12),
                         first=first,first_domain_failure=bad,wire_raw_hist=hist(raw_vs) if len(set(raw_vs))<=32 else None)
                if target:
                    rec['join']=dict(target=target_key,dataset_available=target_key in domains,ordinal_hits=hits,ordinal_misses=misses,sentinels=sent,
                        wrong_UID_hits=uid_hits,first_miss=first_miss,first_sentinel=first_sent,first_wrong_UID_miss=first_uid_miss,classes=dict(cls))
                if field=='affl': rec['ordinal_alias_negative']=dict(target='client_t3',hits=diag_hits,misses=diag_n-diag_hits,excluded_zeros=vs.count(0),
                    static_counterexample='41bdbce: signed byte boxed as integer, zero omitted; no Club resolver. Range overlap is not a reference.',first_nonzero=next((dict(row=j,item=i,absolute=p+off,raw=chunk[off:off+1].hex()) for j,i,p,chunk in items if chunk[off]),None))
                per_side[side]=rec
            if field=='repu': grade='held'; reason='UI index synthesized at 4496fdb, no persisted slot; crrp enum_id is not a byte lane'
            elif not any_values: grade='held'; reason='no live wire items (gate absent)'
            elif s['type']=='enum' and invalid: grade='held'; reason='raw/getter domain conflicts with frozen same-name enum probe; no relabeling'
            elif s['type']=='enum': grade='held'; reason='no explicit scoped enum_ref; same-name enum probe is not a scoped domain proof'
            elif invalid: grade='held'; reason='observed value outside accepted domain or ordinal join miss'
            elif field in REF_TABLE and not sum(k['join']['ordinal_hits'] for k in per_side.values()): grade='held'; reason='no live target join'
            else: grade='L3'; reason='scoped 4CC and matched stream sink with full observed domain'
            ledger[field]=dict(grade=grade,reason=reason,schema=s,scope=f'nation.xml#nation/{key}',schema_index=idx,scoped_occurrences=len(occ),
                getter_compare=cmp,getter_object_load=load,getter_object_offset=obj,getter_route=FIELD_ROUTE[key],
                wire_sink=ITEM_TRANSFERS[key][idx_sink][0] if idx_sink is not None else None,fixup_sites=FIXUPS.get(field),
                static_item_offset=off,accepted_item_offset=off if grade=='L3' else None,encoding=fmt,width=fmt2.size if fmt2 else None,
                mask=MASK.get(field),bounds=bounds,enum_probe_source=enum.get('file'),enum_probe_values=sorted(enum_values),profile=per_side,first_open_witness=(per_side['server']['first_domain_failure'] or per_side['server']['first'] or by_side['server']['first_gate_absence']) if grade=='held' else None)
            if field=='perm': ledger[field]['setter_mask_sites']=[0x107730d,0x107737e]
        if key=='Nfmp': by_side['server']['append_count_after_nonzero_guard']=sum(int.from_bytes(x[3][:4],'little',signed=True)!=0 for x in samples['server'])
        by_parent[key]=dict(parent=key,item_stride=stride,count_width=cw,count_site=count_site,transfer_sequence=ITEM_TRANSFERS[key],archives=by_side,fields=ledger,L3=sum(x['grade']=='L3' for x in ledger.values()),L4=0)
    return by_parent


def probe(b,mode):
    try: return walk(b,mode),None
    except Check as e: return None,e.args[0]


def test_controls(raw,cursors):
    b=raw['server','table_9.dat']; r=cursors['server']['rows'][0]; a=r['collections']['NTRv']['count_at']
    def mutate(at,rep,delta):
        z,err=probe(b[:at]+rep+b[at+1:],1); need(z and err is None and z['row_count']==251 and z['footer']['absolute']==len(b)-9+delta,'synthetic closure')
        return z
    z=mutate(a,b'\1'+struct.pack('<i',123),4); need(z['rows'][0]['collections']['NTRv']['count']==1,'literal reputation count')
    nc=r['collections']['NCro']['gate'][0]; synth_nc=mutate(nc,b'\1\x01'+struct.pack('<iBii',1,1,0,100),14)
    need(synth_nc['rows'][0]['collections']['NCro']['count']==1,'synthetic NCro count')
    item=r['collections']['Nfmp']['start']; z0,err=probe(b[:item]+b'\0'*4+b[item+4:],1)
    need(z0 and z0['footer']==cursors['server']['footer'],'Nfmp null lane has identical width')
    short_at=r['collections']['Nntp']['count_at']
    _,short=probe(b[:short_at],1); need(short['kind']=='short transfer','truncation rejected')
    _,bad=probe(b[:a]+b'\1'+b[a+1:],1); need(bad is not None,'count-only edit rejected')
    return dict(NTRv_count_1_inserted=dict(absolute=a,new_count=1,new_value=123,delta=4,footer_at=z['footer']['absolute']),
                NTRv_count_1_without_item=bad,NCro_presence_1_inserted=dict(absolute=nc,new_count=1,delta=14,footer_at=synth_nc['footer']['absolute']),
                Nfmp_zero_lane=dict(absolute=item,raw=b[item:item+4].hex(),new_raw='00000000',identical_footer=True,expected_append_delta=-1),
                short_transfer=short)


CFG_ENTRIES=(0x105cb10,0x11d0d30,0x105f2b0,0x41ba910,0x41babb0,0x3d86430,0x360e390,0x838a80,0x3d81ad0,
    0x1570e60,0x1572480,0x35b07f0,0x39dd7b0,0x1073390,0x1073700,0x443aed0,0x39b9d60,0x3d87610,0x4387ab0,0x155c120,
    0x3d885f0,0x1077b20,0x1076a50,0x41bbaa0,0x41bdac0,0x4497200,0x3db5890,0x3db2400)
# Branch predicates that alter the reduced grammar, or establish a non-layout counterexample.
MODE=(0x105cbb1,0x105e695,0x11d0fa4)
VERSION=(0x105cb56,0x105cc2f,0x105ccf1,0x105ce14,0x105ce90,0x105d04e,0x105d21d,0x105d5a1,0x105d7e4,0x105da80,0x105dbc5,
         0x105dd9d,0x105de8d,0x105df42,0x105e11e,0x105e1de,0x105e3dd,0x105e6a4,0x105e8fb,0x105eb5d,0x105ef2b,0x11d0dac,0x11d0e46,0x11d0f47)
COUNT_BRANCH={0x105ccb3:0x105cc9d,0x105cce5:0x105cc9d,0x105d151:0x105d128,0x105d192:0x105d128,0x105d1d3:0x105d1a9,
    0x105d212:0x105d1a9,0x105d301:0x105d2d8,0x105d31d:0x105d2d8,0x105d35e:0x105d2d8,0x105d389:0x105d375,0x105d3a5:0x105d375,
    0x105d3e6:0x105d375,0x105d411:0x105d3fd,0x105d42d:0x105d3fd,0x105d46e:0x105d3fd,0x105d499:0x105d485,0x105d4b5:0x105d485,
    0x105d4f6:0x105d485,0x105d557:0x105d52d,0x105d596:0x105d52d,0x105d669:0x105d644,0x105d6b7:0x105d644,0x105d6f3:0x105d6ce,
    0x105d78d:0x105d6ce,0x105d8d8:0x105d8c6,0x105d9c4:0x105d99c,0x105d9e0:0x105d99c,0x105da2d:0x3d86451,0x105db8a:0x105db62,
    0x105dbba:0x105db62,0x105dd19:0x105dd07,0x105e28d:0x105e264,0x105e2d2:0x105e264,0x105e312:0x105e2e9,0x105e352:0x105e2e9,
    0x105e392:0x105e369,0x105e3d2:0x105e369,0x105e9fe:0x105e9ec,0x105ea54:0x105e9ec,0x105ea7d:0x105ea6b,0x105ead3:0x105ea6b,
    0x105eafc:0x105eaea,0x105eb52:0x105eaea,0x105f413:0x105f304,0x105f45e:0x105f304,0x11d221a:0x11d21df,
    0x1570f9a:0x1570e83,0x1571081:0x1570e83,0x15711e8:0x1570e83,0x157120f:0x1570e83,0x1571236:0x1570e83,
    0x155c378:0x155c2f9,0x155c3f3:0x155c2f9,0x35b0847:0x35b0828,0x360e40d:0x360e3ce,0x838cb9:0x838b6b}
DEAD=(0x11d23df,0x11d23fd)  # xor eax,eax; test al,al; jne


def static(source,raw,cursors,attempts,controls):
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM
    pe=PE(EXE); need(digest(pe.raw)==EXEH,'editor SHA'); pe.pe.parse_data_directories(directories=[3])
    m=Cs(CS_ARCH_X86,CS_MODE_64); m.detail=True; ins={}; bb=[]; ext={}
    def record(off,i=None):
        if off in ins: return ins[off]
        i=i or next(m.disasm(pe.raw[off:off+15],pe.f2va(off),count=1))
        a=dict(file_offset=off,VA=i.address,bytes=i.bytes.hex(),instruction=(i.mnemonic+' '+i.op_str).rstrip())
        if i.operands and i.operands[0].type==X86_OP_IMM and (i.mnemonic=='call' or i.mnemonic.startswith('j')): a['direct_target']=pe.va2f(i.operands[0].imm)
        ins[off]=a; return a
    walk_sites={s for a in cursors.values() for r in a['rows'] for s,*_ in r['trace']}
    observed={}
    for side,a in cursors.items():
        b=raw[side,'table_9.dat']
        for r in a['rows']:
            for s,p,w,n in r['trace']:
                if s not in COUNT_BRANCH.values(): continue
                x=observed.setdefault(s,{})
                x.setdefault('zero' if not any(b[p:p+w]) else 'nonzero',dict(side=side,row=r['row'],absolute=p,raw=b[p:p+w].hex()))
    for f in CFG_ENTRIES:
        c=ReaderCFG(pe,m,f); prev={v+i.size:(v,i) for v,i in c.instructions.items()}
        ext[str(f)]=dict(entry=f,end_exclusive=c.function_end_off,reachable=len(c.instructions),external_edges=c.external_edges)
        for va,i in sorted(c.instructions.items()):
            s=pe.va2f(va); a=record(s,i)
            if not i.mnemonic.startswith('j') or i.mnemonic=='jmp': continue
            t=a.get('direct_target'); pred=prev.get(va); p=pe.va2f(pred[0]) if pred else None
            arg=pred[1].op_str if pred else ''; kind='unclassified'; why='not reduced; no alternate layout claimed'; first=None
            if s in MODE: kind='runtime-external'; why='r12b forwarded from loader; base-team helper uses stack mode'; first=attempts['server']['table_9.dat']['0']['first_failure']
            elif s in VERSION: kind='runtime-external'; why='word context +0x588 selects compatibility arm, modern 0xdf1 replay'; first=dict(hypothetical_version='0xdc3',scope='not exercised on archives')
            elif s in DEAD: kind='dead'; why='test AL after XOR EAX,EAX, JNE cannot be taken'; first=dict(AL=0,edge='fallthrough',preceding_xor=p-2)
            elif s in COUNT_BRANCH:
                origin=COUNT_BRANCH[s]; kind='wire_data'; why='count/tag/identity-derived predicate; loop guards may use index vs count'; first=observed.get(origin)
                if s in (0x105e9fe,0x105ea54): first=dict(observed=first,synthetic=controls['NTRv_count_1_inserted'])
                if s in (0x105d8d8,0x105f413,0x105f45e): first=dict(observed=first,synthetic=controls['NCro_presence_1_inserted'])
                if s==0x105da2d: first=controls['Nfmp_zero_lane']
                if s==0x11d221a: first=dict(ordinal_fallback_at=0x989681,accepted_raw_ordinals=[0,250],first_wrong_lane=attempts['server']['table_9.dat']['0']['first_failure'])
            elif s in (0x35b0835,0x360e3e5,0x838b83,0x3d81b12):
                kind='runtime-external'; why='wire length compared with global runtime limit'; first=dict(short_read_or_limit_is_not_layout=True)
            elif t in (0x105de6c,0x105f30d) or '+ 0x10], 0' in arg or (f==0x105cb10 and s in (0x105ef19,)):
                kind='IO-result'; why='success-path stream/out-status or helper AL'; tx=prev.get(pred[0]) if pred else None
                if tx:
                    site=pe.va2f(tx[0]); hit=next((r['first_site'][site] for r in cursors.values() if site in r['first_site']),None)
                    if hit: first=dict(**hit,control='truncate indicated transfer by one byte, not alternative grammar')
                if first is None: first=dict(control='short read unsuccessful; no per-site successful-path witness',example=controls['short_transfer'])
            elif s in (0x105cb77,0x105d8e8,0x105d947,0x105dd30,0x105f4e4,0x11d0d63,0x11d21c6,0x11d2229,0x11d2240):
                kind='context-lifecycle'; why='TLS, null/capacity, reference or callback; model assumes live successful stream'; first=dict(hypothetical='null stream skips identity bulk or allocation state changes; cannot be a valid row')
            bb.append(dict(function=f,site=s,predicate=p,predicate_instruction=record(p,pred[1])['instruction'] if pred else None,
                           taken=t,fallthrough=s+i.size,classification=kind,reason=why,first_counterexample=first))
    fact=source['factory']['9']; chain=source['t9_owner_fixup']; checked=[]
    for k in ('factory_rel32','case','td','col','col_ptr','slot2','slot19'):
        r=fact[k]; a=r['file_offset']; v=bytes.fromhex(r['bytes']); need(pe.raw[a:a+len(v)]==v and pe.f2va(a)==r['VA'],'t47 '+k)
    for s,z in [(0xf48b30,0xf48b57),(0xf48f12,0xf48f27),(0x1059a4f,0x1059a59),(0xf2b660,0xf2b6ba),(0xf2ba0e,0xf2bac5),
        (0x1065eb0,0x1065eb5),(0x3d95190,0x3d951d1),(0x105fc60,0x105fc65),(0x3fc2030,0x3fc2074),(0xf2b63c,0xf2b655),
        (0x4496fa0,0x449703c),(0x107730d,0x1077313),(0x107737e,0x1077384),(0x11d23db,0x11d23ef)]:
        for i in m.disasm(pe.raw[s:z],pe.f2va(s)): record(pe.va2f(i.address),i)
    for key,cfg in PARENTS.items():
        parent=source['parents'][key]; need(parent['reader']==0x105cb10 and parent['owner_type']==9 and parent['item_count'] is None,'t47 scope '+key)
        for s in (*parent['sites'],*FIELD_ROUTE[key]): record(s)
        for field,(_,_,obj,cmp,load,_) in mappings()[key].items():
            q=next(m.disasm(pe.raw[cmp:cmp+15],pe.f2va(cmp),count=1)); v=next(m.disasm(pe.raw[load:load+15],pe.f2va(load),count=1))
            need(q.mnemonic=='cmp' and q.operands[1].imm==int.from_bytes(field.encode(),'big') and v.operands[1].mem.disp==obj,key+' '+field+' getter')
            for s in (cmp,load,*FIXUPS.get(field,())): record(s)
        checked.append(key)
    for s in (0x12e66a0,0x814110,0x838890,0x105f040,0x105faa0,0x105f730,0x141caa0,0x141cb70,0xdb7f80,0x105d7af,0x105d068):
        # 0x105d068 is not on the modern trace and needs no independent window.
        if s!=0x105d068: record(s)
    for s in walk_sites: record(s)
    return fact,chain,ext,list(sorted(ins.values(),key=lambda r:r['file_offset'])),bb,checked


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={x['path']:x['sha256'] for x in J('evidence/MANIFEST.json')['files']}
    expected={MASTER:'7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda',IDA:manifest[IDA],
              BASE:'8af89c72efc2a63fac562140a3faaec7d7f212b923421396a0acc5d627b57d50',
              'scratch/t37/out/REPORT.md':'5656568e8abb0c721498bc310db3ae8964a0eb2bc878828f422df87f482bcfde',
              T47:'2c0a5b535fd280c1c1c46825b5e1b8ea7206ff5d5be40d13c7ed8d241b05b5d3',
              'scratch/t47/out/REPORT.md':'c0742c66ad5ed0819b222983c046c1b7ec83db02fdcbe67bd7063ea0eab563f8'}
    need(expected[MASTER]==manifest[MASTER] and EXEH.encode() in (ROOT/IDA).read_bytes(),'MANIFEST / PE provenance')
    for p,h in expected.items(): need(digest((ROOT/p).read_bytes())==h,p+' SHA')
    master=J(MASTER); source=J(T47); raw,meta=archives(); attempts={}; cursors={}
    for side in ('client','server'):
        a={}; attempts[side]=a
        for member in ('table_9.dat','table_extra_9.dat'):
            b=raw[side,member]; a[member]={}
            for mode in (0,1):
                result,err=probe(b,mode); ok=member=='table_9.dat' and mode==(side=='server')
                need(bool(result)==ok,dict(side=side,member=member,mode=mode,expected=ok,failure=err))
                a[member][str(mode)]=dict(closed=bool(result),first_failure=err)
                if result: cursors[side]=result
    need([r['identity'] for r in cursors['server']['rows']]==[r['identity'] for r in cursors['client']['rows']] and cursors['server']['row_count']==251,'dual identity join')
    for side,d in cursors.items():
        need(d['row_sum']+22==d['payload_len'],'closure'); d['member']='table_9.dat'; d['side']=side
        d['wrong_mode_first']=attempts[side]['table_9.dat'][str(1-d['mode'])]['first_failure']
        d['trace_schema']=['PE file offset (coalesced helper flushes are logical sites)','absolute payload offset','width','repeat']
        d['coordinate_rule']='legacy starts after selector and ends after borrowing one byte from next selector or footer; end excludes borrowed byte'
    targets_by_key,target_meta,classes=targets(raw)
    ledgers=field_ledgers(raw,cursors,targets_by_key,classes,master,source); ctr=test_controls(raw,cursors)
    fact,fix,ext,ii,bb,checked=static(source,raw,cursors,attempts,ctr)
    l3=sum(x['L3'] for x in ledgers.values()); held=sum(len(x['fields'])-x['L3'] for x in ledgers.values())
    put('discovery_t9_wire.json',dict(status='partial_sidecar_positive_reader_open',L3=l3,held=held,L4=0,editor_sha256=EXEH,provenance=expected,factory_9=fact,
        owner_fixup=fix,extents=ext,archives=meta,targets=target_meta,trials=attempts,controls=ctr,rechecked_parents=checked,
        t47_parents={k:source['parents'][k] for k in PARENTS},
        mode_flow=[0xf2b670,0xf2ba38,0xf2ba51,0x105cb2c,0x105cbb1,0x105e695,0x105eef7,0x105ef12,0x11d0fa4],
        binding={'table_9.dat':{'reader':0x105cb10,'client_mode':0,'server_mode':1,'modern_context_model':0xdf1},
                 'table_extra_9.dat':{'reader':None,'mode':None,'status':'both slot19 modern paths rejected; no positive auxiliary reader binding',
                 'first_bytes_after_12':{s:raw[s,'table_extra_9.dat'][12:31].hex() for s in cursors},'may_not_assign_any_target_parent_to_sidecar':True}},
        branch_census=hist(x['classification'] for x in bb)))
    for side,data in cursors.items(): put(f'cursor_t9_{side}.json',data)
    for key,ledger in ledgers.items(): put(f'fields_{key}.json',ledger)
    for kind,entries,size in [('instructions',ii,500),('branches',bb,250)]:
        for a in range(0,len(entries),size): put(f'{kind}.part{a//size+1:03}.json',entries[a:a+size])
    print(f't49 partial: two t9 main modes, 251+251 rows; L3={l3}, held={held}, L4=0; extra reader unbound')


def selftest():
    empty=HEAD+struct.pack('<IBIBI',0,0,0,1,0)
    for m in (0,1):
        need(walk(empty,m)['row_sum']==0,'empty shell')
        need(probe(empty+b'\0',m)[1]['kind']=='footer/EOF','trailing byte')
    need(all(sum(w for _,w in ITEM_TRANSFERS[k])==v[2] for k,v in PARENTS.items()),'item widths')


def main():
    p=argparse.ArgumentParser(description=__doc__); g=p.add_mutually_exclusive_group(); g.add_argument('--build',action='store_true'); g.add_argument('--selftest',action='store_true'); args=p.parse_args()
    try:
        if args.selftest: selftest(); print('t49 builder selftest PASS')
        else: build()
        return 0
    except Check as e: print('CHECK:',e,file=sys.stderr); return 1
    except Exception as e: print('FATAL:',type(e).__name__,e,file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
