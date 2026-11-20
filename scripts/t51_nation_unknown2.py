#!/usr/bin/env python3
"""t51: offline Nation static witnesses and target-only cursor projections."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t51/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
IDA = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
S47 = 'scratch/t47/out/discovery_nation_unknown.json'
CUR10 = 'scratch/t47/out/cursor_nation_tax.json'
CUR9 = 'scratch/t49/out/cursor_t9_{}.json'
T37 = 'scratch/t37/out/nation_subtable_inventory.json'
PE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
PARENTS = dict(Nrvn=216,Calt=235,TCrs=64,Nftb=234,EDfx=342,EDsc=344)
HEAD = bytes.fromhex('03017461642ef10d')
MEMBERS = ('table_9.dat','table_10.dat','table_extra_9.dat','table_extra_10.dat','table_3.dat','table_21.dat','table_25.dat')
SEALED = {T37:'8af89c72efc2a63fac562140a3faaec7d7f212b923421396a0acc5d627b57d50',
          S47:'2c0a5b535fd280c1c1c46825b5e1b8ea7206ff5d5be40d13c7ed8d241b05b5d3',
          'scratch/t47/out/REPORT.md':'c0742c66ad5ed0819b222983c046c1b7ec83db02fdcbe67bd7063ea0eab563f8',
          'scratch/t37/out/REPORT.md':'5656568e8abb0c721498bc310db3ae8964a0eb2bc878828f422df87f482bcfde',
          CUR10:'42b3e88db86c725221a23cd7b2bdd6e3d4c1b089d758ed844a56f84e103f2ea9',
          CUR9.format('server'):'ccf78eba3d1d845b530550987b093b120ca20dd9e4a079da3970ca590259e69b',
          CUR9.format('client'):'82a733f8157b1518d38dadafcc33249a34fa3d563ec2a37c4d60740bf1f6b004',
          'scratch/t49/out/REPORT.md':'0c0b1129c1edb5758d49403351950238383b5369d089097c9bfb8b0fe6d23974',
          MASTER:'7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'}

class Fail(Exception): pass

def ck(ok, msg):
    if not ok: raise Fail(msg)

def H(b): return sha256(b).hexdigest()
def J(p): return json.loads((ROOT/p).read_bytes())
def put(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
def i32(b,p): return S.unpack_from('<i',b,p)[0]
def u32(b,p): return S.unpack_from('<I',b,p)[0]
def first_failure(call):
    try: call()
    except Fail as e: return e.args[0]
    raise Fail('negative accepted')


def archives():
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    db=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
    ck(db.drive.upper()!='Z:','Z: prohibited')
    db=db.resolve(); ck(db.drive.upper()!='Z:','Z: prohibited')
    read=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    raw={}; meta={}
    for side,cnt in [('client',31),('server',77)]:
        _,b,d=read(db/f'{side}_db.dat'); es={e['path']:e for e in d['entries']}
        ck(len(es)==cnt and d['data_base']==34,side+' directory')
        meta[side]=dict(data_base=34,directory_count=cnt,archive_sha256=H(b),directory_paths=sorted(es),members={})
        keys=MEMBERS if side=='client' else MEMBERS[:4]
        for k in keys:
            e=es.get(f'{side}_db/{k}')
            if e is None:
                meta[side]['members'][k]={'present':False}; continue
            a=34+e['offset']; end=a+e['packed_size']; bound=min((34+x['offset'] for x in es.values() if x['offset']>e['offset']),default=d['toc_offset'])
            ck(a<end<=bound,(side,k,'bounds'))
            pos=a; frames=[]; selected=[]
            while pos<end:
                ck(b[pos:pos+4]==b'\x28\xb5\x2f\xfd',(side,k,pos,'magic'))
                obj=z.ZstdDecompressor().decompressobj(); data=obj.decompress(b[pos:end]); sz=end-pos-len(obj.unused_data)
                ck(obj.eof and sz>0,(side,k,'frame'))
                frames.append([pos,sz,len(data)]); pos+=sz
                if len(data)==e['size']: selected.append((frames[-1],data))
            ck(len(selected)==1,(side,k,'selection')); f,data=selected[0]
            ck(data[:8]==HEAD,(side,k,'version/header')); raw[side,k]=data
            meta[side]['members'][k]=dict(present=True,entry={**e,'sha256':H(b[a:end])},bounds=[a,end,bound],frames=frames,selected_frame=f,
                payload_sha256=H(data),count=u32(data,8),stride={'table_21.dat':38,'table_25.dat':127}.get(k))
    part=(db/'basic_people_db.dat').read_bytes(); dz=z.ZstdDecompressor().decompressobj(); people=dz.decompress(part[8:])
    ck(part[:8]==HEAD and dz.eof and not dz.unused_data,'person frame')
    return raw,meta,people,H(part[8:])


class Span:
    def __init__(self,b,p,end): self.b=b;self.p=p;self.end=end
    def cut(self,n):
        p=self.p; ck(0<=n<=self.end-p,('short transfer',p,n,self.end));self.p+=n
        return self.b[p:self.p]
    def num(self,n,signed=False): return int.from_bytes(self.cut(n),'little',signed=signed)
    def vec(self,n,w,signed=False):
        a=self.p; count=self.num(n,signed); ck(count>=0,('negative count',a,count)); self.cut(count*w)
        return a,count


def ftb_items(c,n):
    items=[]
    for j in range(n):
        a=c.p; tag=c.num(1); txt=[]
        for _ in range(4):
            p=c.p; z=c.num(4); bs=c.cut(z); txt.append([p,z,bs.hex(),bs.decode('utf8')])
        dt=c.p; d,y=S.unpack('<HH',c.cut(4)); lanes=[]
        for _ in range(4): lanes.append([c.p,c.num(4,True)])
        items.append(dict(item=j,absolute=a,end=c.p,length=c.p-a,tag=tag,strings=txt,
            date=dict(absolute=dt,raw_le16=[d,y],packed=(y<<17)|((d&511)<<8)|(d>>9)),lanes=lanes,raw=c.b[a:c.p].hex()))
    return items


def tail9(b,p,end):
    c=Span(b,p,end); a=c.p; n=c.num(1); start=c.p; items=[]
    for j in range(n):
        q=c.p; it=c.cut(16)
        items.append(dict(item=j,absolute=q,raw=it.hex(),ordinal_i32=i32(it,0),raw_qword=S.unpack_from('<q',it)[0],target_type=it[10],tag=it[11],leve=S.unpack_from('<b',it,12)[0]))
    r=dict(count_at=a,count=n,start=start,end=c.p,items=items)
    a=c.p; count=c.num(2,True); ck(count>=0,('negative Calt count',a,count)); start=c.p
    for _ in range(count):
        for w in (4,4,8,2,4,4,1,1): c.cut(w)
    return r,dict(count_at=a,count=count,start=start,end=c.p,stride=28),c.p


def cursor(raw,side,tid):
    b=raw[side,f'table_{tid}.dat']; mode=int(side=='server'); z=J(CUR9.format(side)) if tid==9 else J(CUR10)[side]
    ck(z['payload_sha256']==H(b) and z['mode']==mode and b[:8]==HEAD,'cursor provenance')
    p=13; rows=[]; ids=set()
    for j,r in enumerate(z['rows']):
        ck(j==r['row'] and p==r['wire13'] and p+1==r['legacy14'] and b[p]==0,'selector before row')
        end=r['end']; ia=r['identity_at']; ck(p+1<=ia and ia+12==end,'identity location from accepted cursor')
        ck(H(b[p:end])==r['wire_sha256'] and H(b[p+1:end+1])==r['legacy_sha256'],'row fingerprint')
        x={k:r[k] for k in ('row','wire13','legacy14','end','identity_at','length','wire_sha256','legacy_sha256')}; x['selector']=b[p]
        if tid==9:
            probe=[t for t in r['trace'] if t[0]==0x11d1b03]
            ck(len(probe)==mode,'Nrvn mode reachability')
            x['Nrvn']=x['Calt']=None
            if probe:
                rv,ca,q=tail9(b,probe[0][1],ia); ck(q==ia,'target suffix reaches identity')
                ck(next(t[1] for t in r['trace'] if t[0]==0x11d1bf2)==ca['count_at'],'Calt count from suffix, t49 transfer agreement')
                x.update(Nrvn=rv,Calt=ca)
        else:
            x['Nftb']=None
            if mode:
                c=Span(b,p+1,ia);c.cut(4); c.vec(2,4,True); c.vec(4,4,True)
                a=c.p; n=c.num(2,True); ck(n>=0 and n*37<=ia-c.p,('Nftb count',a,n)); start=c.p
                x['Nftb']=dict(count_at=a,count=n,start=start,items=ftb_items(c,n),end=c.p)
                ck(c.p+24==r['tax'][0],'target end agrees with next previously sealed transfer boundary')
        # The non-target spans are t47/t49 inputs, not a new semantic replay.
        ident=S.unpack_from('<III',b,ia); ck(list(ident)==r['identity'] and ident[0]==j and ident[1]==ident[2]!=0 and ident[1] not in ids,'identity after target walk')
        ids.add(ident[1]); x['identity']=ident; rows.append(x); p=end
    ck(len(rows)==u32(b,8)==251 and len(b)-p==9,'count/EOF'); footer=S.unpack_from('<IBI',b,p)
    ck(footer==(0,1,max(ids)),'footer vector/flag/max observed identity')
    return dict(member=f'table_{tid}.dat',side=side,mode=mode,count=len(rows),stride='variable',rows=rows,footer_at=p,footer=footer,
                footer_hex=b[p:].hex(),payload_sha256=H(b),payload_size=len(b),wire_header=13,legacy_header=14,wire_footer=9,legacy_footer=8,
                row_sum=p-13,row_length_range=[min(r['length'] for r in rows),max(r['length'] for r in rows)],
                source=CUR9.format(side) if tid==9 else CUR10,coordinates='absolute payload offsets; subtract wire13 or legacy14 row base; legacy row last byte is following selector/footer')


def domains(raw,people,compressed,cs):
    table={}; info={}
    def save(k,b,ats):
        d={};
        for j,p in enumerate(ats):
            a,u,v=S.unpack_from('<III',b,p);ck(a==j and u==v and u!=0,(k,p,'target identity'));d[a]=u
        ck(len(set(d.values()))==len(d),(k,'target uniqueness'))
        table[k]=d; info[k]=dict(count=len(d),payload_sha256=H(b),ordinal_uid_sha256=H(b''.join(S.pack('<II',a,u) for a,u in d.items())))
    for side in ('client','server'):
        save(f'{side}_nation',raw[side,'table_10.dat'],[r['identity_at'] for r in cs[side,10]['rows']])
    for name,tid,w in (('stadium',21,38),('competition',25,127)):
        b=raw['client',f'table_{tid}.dat']; n=u32(b,8); ck(len(b)==13+w*n+9,(name,'EOF'))
        save('client_'+name,b,range(13+w-12,len(b)-9,w))
    b=raw['client','table_3.dat']; d=J('scratch/t24/out/cursor.json'); ck(d['provenance']['payload_sha256']==H(b),'club payload')
    ends=[r[3]-12 for f in d['rows']['shards'] for r in J('scratch/t24/out/'+f)['rows']]
    ck(len(ends)==u32(b,8) and ends[-1]+12==len(b)-9,'club identity-only witness'); save('client_club',b,ends)
    p=5; ats=[]; n=u32(people,0);ck(n==658011 and people[4]==0,'people header')
    for _ in range(n):
        tag,k=people[p:p+2]; ck(tag==17 and 1<=k<=5,('person selector/class',p)); p+=(83,83,83,34,22)[k-1]; ats.append(p-12)
    ck(people[p:]==bytes.fromhex('00000000014cbd5477'),'people EOF');save('person',people,ats);info['person']['compressed_sha256']=compressed
    return table,info


def join(records,domain):
    byuid={u:j for j,u in domain.items()}; out=dict(live=0,null=0,ordinal_matches=0,uid_matches=0,first_ordinal_miss=None,first_uid_miss=None,first_live=None)
    for row,item,p,v in records:
        if v==-1: out['null']+=1; continue
        out['live']+=1; d=dict(row=row,item=item,absolute=p,value=v,raw_i32_le=S.pack('<i',v).hex(),ordinal_target_uid=domain.get(v),uid_target_ordinal=byuid.get(v))
        out['ordinal_matches']+=v in domain;out['uid_matches']+=v in byuid
        if out['first_live'] is None: out['first_live']=d
        for name,ds in [('ordinal',domain),('uid',byuid)]:
            if v not in ds and out['first_'+name+'_miss'] is None: out['first_'+name+'_miss']=d
    return out


# exact item-dispatch and its same-object load / reader destination
MAP={
 'Nrvn':{'nati':(0x1106bfd,0x11071ce,0x11d1b98,0),'leve':(0x1106de9,0x1106df5,0x11d1b98,12)},
 'Calt':{'cmid':(0x11fd28a,0x11fd44e,0x11d1e86,8),'stid':(0x11fd34d,0x11fd503,0x11d1e65,0)},
 'Nftb':{'NbPi':(0x10728f0,0x1072a95,0x448f996,48),'NpFn':(0x1072a02,0x1072b85,0x448f8c6,0),
         'NpSn':(0x1072a0e,0x1072a30,0x448f8dc,8),'NbPd':(0x107295b,0x107298c,0x448f925,32),
         'NbPn':(0x10728fc,0x1072908,0x448f954,40),'NbFt':(0x107294f,0x1072b34,0x448f938,36),
         'NbCn':(0x1072943,0x1072ab5,0x448f910,24)}}


def ledgers(cs,table,master):
    def items(tid,k): return [(r['row'],it) for r in cs['server',tid]['rows'] for it in r[k]['items']]
    rr=items(9,'Nrvn'); ff=items(10,'Nftb'); fields={}
    ck(all(it['target_type']==2 and it['tag']==6 and it['raw_qword']==it['ordinal_i32'] for _,it in rr),'rival projection subset')
    for k,ss in MAP.items():
        fs=master[PARENTS[k]]['list_item_fields']; fields[k]={}
        for key,(cmp,ld,sink,obj) in ss.items():
            xml=[f for f in fs if f['field']==key];ck(len(xml)==1,(k,key,'scope'))
            fields[k][key]=dict(schema=xml[0],occurrences=1,compare=cmp,getter_load=ld,reader_sink=sink,object_offset=obj,status='held')
    d=fields['Nrvn']; j=join(((row,it['item'],it['absolute'],it['ordinal_i32']) for row,it in rr),table['server_nation'])
    ck(j['live']==j['ordinal_matches'] and j['null']==0,'rival actual ordinal join')
    d['nati'].update(status='L3',item_offset=0,width=4,encoding='signed i32 in zero-extended qword transfer in this archive; object pointer fixed later',join=j)
    hist=Counter(it['leve'] for _,it in rr); ck(min(hist)>=0 and max(hist)<=100,'level range')
    d['leve'].update(status='L3',item_offset=12,width=1,encoding='i8',histogram=hist)
    d=fields['Calt']
    for k,o,target in [('cmid',4,'client_competition'),('stid',0,'client_stadium')]:
        d[k].update(candidate_item_offset=o,target_ordinal_basis=target,observed_items=0,reason='251 server i16 counts all zero; client mode bypass; no live target join',first_counterexample=dict(row=0,absolute=cs['server',9]['rows'][0]['Calt']['count_at'],raw='0000'))
    d=fields['Nftb'];ck(all(it['tag']==1 for _,it in ff),'observed Nftb tag')
    for k,n in [('NpFn',0),('NpSn',1),('NbCn',3)]:
        stats=Counter(it['strings'][n][1] for _,it in ff)
        d[k].update(status='L3',encoding='u32 byte length + bytes (observed UTF-8)',dynamic_component=['string_0','string_1','string_3'][('NpFn','NpSn','NbCn').index(k)],length_histogram=stats,
            first=dict(row=ff[0][0],absolute=ff[0][1]['strings'][n][0],length=ff[0][1]['strings'][n][1],raw=ff[0][1]['strings'][n][2]))
    d['NbPd'].update(status='L3',encoding='two LE u16; boxed (year<<17)|((word0&511)<<8)|(word0>>9)',dynamic_component='after fourth string',width=4,
                     first=dict(row=ff[0][0],**ff[0][1]['date']))
    for k,n,target in [('NbPi',3,'person'),('NbPn',1,'server_nation'),('NbFt',0,'client_club')]:
        j=join(((row,it['item'],*it['lanes'][n]) for row,it in ff),table[target]); ck(j['live']>0,'reference first live witness')
        why=('actual ordinal join rejects' if j['first_ordinal_miss'] else 'numeric ordinal membership is not enough: item setter stores target +0xc and getter uses identity lookup, not ordinal resolve')
        d[k].update(candidate_encoding='i32 passed to lookup by object identity, not ordinal coordinate promotion',dynamic_candidate=f'after date +{4*n}',
                    target_ordinal_basis=target,join=j,reason=why+'; alternate UID diagnostics do not pass requested ordinal gate')
    return fields


# Only selected functions/slices. ReaderCFG has no indirect-table resolver; explicit
# local rel32 cells below are separate PE evidence, not generic fallthrough.
WINDOWS={
 0x1041f40: [(0x1041f63,0x1041f6c),(0x1043306,0x1043331)],
 0x1065ef0: [(0x1065f1d,0x1065f25),(0x10665a6,0x10665b2),(0x10675e3,0x1067601),(0x10685d9,0x10685e8)],
 0x3d95190: None,0x3d95f10:None,0x3eba380:None,0xe94990:[(0xe94b78,0xe94bab)],
 0x3a14da0:[(0x3a14dc0,0x3a14df2),(0x3a14ea0,0x3a14eb1)],
 0x1106bc0:[(0x1106bd5,0x1106c09),(0x1106de9,0x1106e02),(0x1106f2a,0x1106f71),(0x11071c4,0x11071e8)],
 0x1105860:None,0x3ecb250:[(0x3ecb25d,0x3ecb285),(0x3ecb340,0x3ecb35f)],
 0x105cb10:[(0x105cb23,0x105cbb6),(0x105d7db,0x105d8a8),(0x105dcf9,0x105dd70),(0x105eedc,0x105ef35)],
 0x11d0d30:[(0x11d0d53,0x11d0d69),(0x11d0f9d,0x11d0faa),(0x11d1ac6,0x11d1c00),
            (0x11d1ca7,0x11d1ccc),(0x11d1e52,0x11d1fc8),(0x11d2189,0x11d21ea),(0x11d23d5,0x11d2405)],
 0x3fc2030:None,0x3d885f0:[(0x3d88602,0x3d8864c),(0x3d88859,0x3d88869)],
 0x11d2580:[(0x11d2590,0x11d25ac),(0x11d2a72,0x11d2b52)],
 0x11f0690:[(0x11f06bc,0x11f06c4),(0x11f139a,0x11f13a6),(0x11f15ab,0x11f15b7),(0x11f1e26,0x11f1e60),(0x11f219c,0x11f21bf)],
 0x11f4570:[(0x11f458d,0x11f4596),(0x11f45fe,0x11f4620),(0x11f4c32,0x11f4c43),(0x11f4e38,0x11f4e49)],
 0x11cf6e0:[(0x11cf6ff,0x11cf70b),(0x11cf7a1,0x11cf7d5),(0x11cfa56,0x11cfa8d)],
 0x3ecc060:[(0x3ecc08c,0x3ecc0b7),(0x3ecc24c,0x3ecc28b)],
 0x11fd060:[(0x11fd28a,0x11fd297),(0x11fd34d,0x11fd35a),(0x11fd447,0x11fd470),(0x11fd503,0x11fd546)],
 0x4391e40:[(0x4391e93,0x4391eb1)],0x11f3dc0:[(0x11f3e37,0x11f3e75),(0x11f409c,0x11f40dd)],
 0x11fc730:[(0x11fc7bf,0x11fc7de)],0x11fbb40:[(0x11fbbcf,0x11fbc02),(0x11fbce4,0x11fbcfb)],
 0x3ebb830:[(0x3ebb845,0x3ebb864),(0x3ebb8b0,0x3ebb928),(0x3ebb928,0x3ebb936)],
 0x3ec74d0:[(0x3ec74ed,0x3ec7507),(0x3ec75c0,0x3ec75cd)],0x4387250:None,0x155a320:[(0x155a335,0x155a35c)],
 0x4387ab0:None,0x155c120:[(0x155c130,0x155c184),(0x155c2bd,0x155c435),(0x155c61c,0x155c648)],
 0x11d3200:[(0x11d3226,0x11d322f),(0x11d32dd,0x11d32f6),(0x11d3429,0x11d3430),(0x11d366e,0x11d3675),
             (0x11d4b60,0x11d4c0b)],0x3bb9650:[(0x3bb965e,0x3bb9719),(0x3bb97cf,0x3bb97f9)],
 0x3b94b50:[(0x3b94b5d,0x3b94b8c),(0x3b94ba0,0x3b94bbf),(0x3b94c42,0x3b94c6a)],
 0x3cefbe0:[(0x3cefbe7,0x3cefbed),(0x3cefc5d,0x3cefcbf),(0x3cefd3f,0x3cefd53)],
 0xf50a50:[(0xf5164c,0xf51683)],0xf28830:[(0xf28e0f,0xf28e31),(0xf29296,0xf292bb)],
 0xf4d1e0:[(0xf4e131,0xf4e1da)],0xf2d810:[(0xf2dbbe,0xf2dc05)],
 0x3ea1420:[(0x3ea1490,0x3ea14c7),(0x3ea1574,0x3ea1594)],
 0x1045350:[(0x1045368,0x104536e),(0x1045b0d,0x1045b72),(0x104740b,0x1047412)],
 0x3d61fc0:None,0x1063530:[(0x1063554,0x106355a),(0x10647c0,0x10647dc)],
 0x1050d40:[(0x1050d50,0x1050daa),(0x1050e77,0x1050ee4),(0x1050fa8,0x1050fbc),(0x10511c9,0x105122d)],
 0x44929b0:[(0x44929b6,0x44929da),(0x44929da,0x4492a43)],0x3d6beb0:[(0x3d6bebf,0x3d6bee0)],
 0x3d78450:[(0x3d78470,0x3d78490),(0x3d7854a,0x3d78566)],0x3d78720:[(0x3d7873d,0x3d78757),(0x3d78810,0x3d78821)],
 0x3daaaf0:[(0x3daab15,0x3daab87),(0x3daac62,0x3daac91),(0x3daacdc,0x3daad14)],
 0x10728c0:[(0x10728d4,0x107293e),(0x1072943,0x1072967),(0x107298c,0x10729ad),(0x1072a02,0x1072a38),
             (0x1072a95,0x1072ab5),(0x1072ab5,0x1072ad5),(0x1072b34,0x1072b6f),(0x1072b85,0x1072b8b)],
 0x103fac0:[(0x103fae6,0x103faf0),(0x1040103,0x104016c),(0x1040191,0x10401ff),(0x1040bc6,0x1040be4)],
 0x448f890:None,0x35b07f0:[(0x35b0822,0x35b084d),(0x35b0875,0x35b0886)],0x39dd7b0:None,
 0x28150:[(0x28163,0x281cb),(0x285de,0x285e8),(0x29c37,0x29c8a)],
 0x907f0:[(0x90803,0x90835),(0x90851,0x90890),(0x90989,0x90a31)],
 0x11af7b0:[(0x11b0f62,0x11b0f71)],0x44d7bf0:[(0x44d7c6a,0x44d7c88),(0x44d7cbd,0x44d7cf0)]}

THUNKS=(0x1041f30,0x1041f33,0x1065eb0,0x106ad10,0x11e8900,0xdf41a0,0x11fe780,0x12e66a0,0x105fc60,
        0x11ff710,0x15634b0,0x11e9970,0x11fc500,0x155a760,0x155b450,0x11d01c0,0xf55120,0xf30db0,0xffa3b0,
        0x1045300,0x15d07b0,0x104b6f0,0x10512c0,0x1051580,0x1072d80,0x104ea1b,0x15cf370,0x814110,0xdb7f80,0x103f9f0,0x15e9830)
SITES=(0xf48b30,0xf48f12,0xf48f1d,0xf48f27,0xf48f37,0x1059a45,0x1059a4a,0x1059a4f,0x1059a56,0x103ec17,0x103ec1e,
       0xf2ba0e,0xf2ba23,0xf2ba38,0xf2ba51,0xf292ad,0xf51671,0x103eede,0x103eee5,0x1105ae0,0x1105ae3,0x1105ae6,0x1105af4,
       0x1105af8,0x1105afb,0x1105afe,0x103f9f0,0x3d5c080,0x3d5c084,0x3d5c08b,0x3d5c091,0x104536b,0x105dd56,0x11d366e)


def static(old):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM,X86_REG_RIP
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    p=PE(EXE); ck(H(p.raw)==PE_SHA,'editor SHA'); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
    ins={}; ext={}
    def blob(o,n): return dict(file_offset=o,VA=p.f2va(o),bytes=p.raw[o:o+n].hex())
    def rec(o,i=None):
        if o in ins: return ins[o]
        i=i or next(m.disasm(p.raw[o:o+15],p.f2va(o),count=1)); a=dict(**blob(o,i.size),instruction=(i.mnemonic+' '+i.op_str).rstrip())
        if i.operands and i.operands[0].type==X86_OP_IMM and (i.mnemonic.startswith('j') or i.mnemonic=='call'):
            a['direct_target']=p.va2f(i.operands[0].imm)
        rip=[i.address+i.size+x.mem.disp for x in i.operands if x.type==X86_OP_MEM and x.mem.base==X86_REG_RIP]
        if rip: a['rip_targets_VA']=rip
        ins[o]=a;return a
    for f,windows in WINDOWS.items():
        c=ReaderCFG(p,m,f); b=len(ins)
        for va,i in sorted(c.instructions.items()):
            o=p.va2f(va)
            if windows is None or any(a<=o<z for a,z in windows):rec(o,i)
        ext[str(f)]=dict(entry=f,end_exclusive=c.function_end_off,reachable=len(c.instructions),published_instructions=len(ins)-b,external_edges=c.external_edges,
                        coverage='direct in-extent CFG; indirect dispatch cells separate; branch labels selected')
    for s in THUNKS+SITES+tuple(x for k in PARENTS for x in old['parents'][k]['sites']): rec(s)
    for fs in MAP.values():
        for k,(a,b,c,_) in fs.items():
            ck(int.from_bytes(k.encode(),'big')==next(m.disasm(p.raw[a:a+12],p.f2va(a),count=1)).operands[1].imm,k+' exact dispatch')
            for s in (a,b,c):rec(s)
    cells={}
    for key,base,index,target in [('t9_factory',0xf49d38,9,0xf48f12),('t10_factory',0xf49d38,10,0xf48f27),
                                  ('Nrvn_kind2',0x11059f4,2,0x11058c8),('Nrvn_category6',0x1105b04,0,0x1105afe)]:
        o=base+4*index; va=p.f2va(base)+i32(p.raw,o); ck(p.va2f(va)==target,key);cells[key]=dict(**blob(o,4),table=base,dest=target,dest_VA=va)
    for key,vt in old['factory'].items():
        for k in ('td','col','col_ptr','slot2','slot19','factory_rel32'):
            a=vt[k];ck(blob(a['file_offset'],len(bytes.fromhex(a['bytes'])))==a,(key,k,'factory blob'))
    for tag,c in [('NATION',10),('NATIONAL_TEAM_CONTAINER',9)]:
        v=old['factory'][str(c)]['vtable_VA'];o=p.va2f(v+24);dest=p.va2f(S.unpack_from('<Q',p.raw,o)[0]); cells[tag+'_slot3']=dict(**blob(o,8),dest=dest)
        ck(dest=={10:0x1045300,9:0x1063450}[c],tag+' slot3')
    cells['named_aux_generic_suffix']=blob(p.va2f(0x1418e2c24),5)
    scans={}
    for code in PARENTS:
        scans[code]={k:[x.start() for x in re.finditer(re.escape(w),p.raw)] for k,w in [('as_written',code.encode()),('reversed_le',code.encode()[::-1])]}
    ck(scans['EDfx']=={'as_written':[],'reversed_le':[0x29c39]} and not any(scans['EDsc'].values()),'ED scan')
    ck(ins[0x29c37]['instruction']=='cmp esi, 0x45446678' and ins[0x29c80]['direct_target']==0x907f0,'reachable EDfx handler')
    return p,ext,cells,scans,ins,rec


def facts(cs,raw):
    srv=cs['server',9]['rows']; rv=srv[0]['Nrvn']; ca=srv[0]['Calt']; b=raw['server','table_9.dat']; nrv=rv['count_at']; cpos=ca['count_at']
    q=b[nrv:srv[0]['identity_at']]; a=cpos-nrv
    synthetic=q[:a]+b'\1\0'+bytes(28)+q[a+2:]
    r,c,e=tail9(synthetic,0,len(synthetic));ck(e==len(synthetic) and c['count']==1 and r['count']==rv['count'],'nonzero Calt check')
    ft=next(row for row in cs['server',10]['rows'] if row['Nftb']['count']); f=ft['Nftb']; t=raw['server','table_10.dat']
    control=dict(Nrvn_zero=next(dict(row=x['row'],absolute=x['Nrvn']['count_at'],raw='00') for x in srv if not x['Nrvn']['count']),
        Nrvn_tag_change=dict(row=0,absolute=rv['start']+11,raw='06',synthetic='05',effect='known 16-byte transfer unchanged; filter no longer returns item'),
        Nrvn_short=first_failure(lambda:tail9(b,nrv,rv['start']+15)),
        Calt_no_live=dict(row=0,absolute=cpos,raw=b[cpos:cpos+2].hex(),count=ca['count']),
        Calt_count1_synthetic=dict(absolute=cpos,old_suffix=len(q),new_suffix=len(synthetic),new_count=c['count']),
        Nftb_zero=dict(row=0,absolute=cs['server',10]['rows'][0]['Nftb']['count_at'],raw='0000'),
        Nftb_short=first_failure(lambda:ftb_items(Span(t,f['start'],f['start']+5),1)))
    gates=[]
    for x in J(CUR9.format('server'))['rows']:
        a=next(z[1] for z in x['trace'] if z[0]==0x105dd07); end=next(z[1] for z in x['trace'] if z[0]==0x105dd87)
        gates.append(dict(row=x['row'],absolute=a,presence=b[a],bytes_after_gate=end-a-1))
    return control,gates


BRANCHES={
 0x3eba398:('context-lifecycle',0x3eba394,'begin equals end; returns empty projection, not an absent member','Nrvn_zero'),
 0x3eba3ed:('context-lifecycle',0x3eba3e8,'UI predicate is object byte vs 6; view removes item, wire length unchanged','Nrvn_tag_change'),
 0x3eba542:('dead',0x3eba540,'taken is contradictory after xor eax,eax at 0x3eba53e',{'construction':'AL=0; ZF=1'}),
 0x11d1b0f:('wire_data',0x11d1b0c,'u8 count zero bypasses resize and loop','Nrvn_zero'),
 0x11d1b88:('context-lifecycle',0x11d1b85,'null stream bypasses pending transfer; not a valid persisted variant',{'construction':'stream=null suppresses pending read; 0x11d21c6 also skips identity'}),
 0x11d1bfc:('wire_data',0x11d1bf7,'signed count <= 0 skips allocation and items','Calt_count1_synthetic'),
 0x11d1e6c:('IO-result',0x11d1e68,'stream status after 4 B stadium transfer',{'synthetic':'nonzero Calt count with only 3 bytes available at item start (static short-read case)'}),
 0x11d0fa4:('runtime-external',0x11d0f9d,'caller mode, not selector; client bypasses Nrvn/Calt',{'client_mode':0,'server_mode':1,'selector_both':0}),
 0x11d2593:('runtime-external',0x11d2590,'fixup r9b zero bypasses base fixups; no claim all runtime loads resolve',{'construction':'r9b=0 skips 0x11d2aa9'}),
 0x105dd19:('wire_data',0x105dd14,'main-reader TCrs-shaped state has a presence gate; sink +0x188 is not +0xb0/+0x48','TCrs_main_gate'),
 0x4387b50:('IO-result',0x4387b4b,'out status from the responsibility reader',{'synthetic':'truncate nonempty item before 4 B person lane; 0x155c321 reaches error'}),
 0x155c378:('wire_data',0x155c372,'per-item tag <2 reads byte widened into +6, otherwise reads word',{'synthetic':'tag 1 width=1 vs tag 2 width=2 at same field'}),
 0x155c3f3:('wire_data',0x155c3ed,'per-item tag <3 skips +9 transfer',{'synthetic':'tag 2 vs 3 layout; no observed TCrs wire rows in t51'}),
 0x1045b14:('runtime-external',0x1045b0d,'Nftb typed-property import gate from global VA 0x141b60320',{'construction':'zero gate: 0x104740b returns false, yet archive reader can consume t10 independently'}),
 0x1040144:('wire_data',0x104013e,'Nftb count 0 skips item loop','Nftb_zero'),
 0x10401e4:('IO-result',0x10401e2,'AL from Nftb item reader','Nftb_short'),
 0x448f8d3:('IO-result',0x448f8ce,'string reader out-status after first text','Nftb_short'),
 0x29c48:('runtime-external',0x29c43,'UI flags can return before NATION callback',{'construction':'AL=0 returns early at 0x29f6a'}),
 0x29c5a:('context-lifecycle',0x29c57,'no selected object, so EDfx table-type gate is not reached',{'construction':'R15=null'}),
 0x29c6c:('context-lifecycle',0x29c69,'selected object table type must be 10 for this view',{'construction':'type 24 rejects even with exact EDfx key'})}


def build():
    for k,v in SEALED.items(): ck(H((ROOT/k).read_bytes())==v,k+' SHA')
    old=J(S47); gov={x['path']:x['sha256'] for x in J('evidence/MANIFEST.json')['files']}
    for k in (MASTER,IDA):ck(H((ROOT/k).read_bytes())==gov[k],k+' MANIFEST')
    ck(PE_SHA in (ROOT/IDA).read_text(encoding='utf-8'),'PE provenance')
    schema=J(MASTER); master=schema['entities']['nation.xml'][0]['fields']; t37={r['parent_4cc']:r for r in J(T37)['parents']}
    p,ext,cells,scans,ins,rec=static(old)
    raw,meta,people,compressed=archives(); cs={(s,t):cursor(raw,s,t) for t in (9,10) for s in ('client','server')}
    for t in (9,10): ck([r['identity'] for r in cs['client',t]['rows']]==[r['identity'] for r in cs['server',t]['rows']],f't{t} parallel identities')
    tables,targets=domains(raw,people,compressed,cs); fields=ledgers(cs,tables,master); ctrl,gates=facts(cs,raw)
    ctrl['TCrs_main_gate']=next(g for g in gates if not g['presence']); archive_open=J('scratch/t49/out/discovery_t9_wire.json')
    ps={k:dict(schema_index=idx,t47_verbatim=old['parents'][k],t37_verbatim=t37[k],immediate_scan=scans[k],
               independent_item_vptr=None,new_evidence={},L4=0) for k,idx in PARENTS.items()}
    for k,x in ps.items(): ck(master[PARENTS[k]]==x['t47_verbatim']['schema'] and master[PARENTS[k]]['field']==k,k+' frozen schema')
    ps['Nrvn'].update(owner='NATIONAL_TEAM_CONTAINER; NATION slot2 view',table_type=9,member='table_9.dat',reader=0x105cb10,status='cursor_closed',
        new_evidence=dict(getter=[0x1041f30,0x104330f,0x1043322,0x1065f22,0x10665a6,0x10675f0,0x106ad10,0x3d95f95,0x11e8900,0x3eba390,0x3eba3e8],
          projection=[0x10675fb,0xe94ba2,0xdf41a0,0x3a14ea8,0x1106bfd,0x1106de9],
          object_vector=[0x48,0x50,0x58],sink=[0x105ef12,0x11d0d56,0x11d1b03,0x11d1b15,0x11d1b20,0x11d1b98,0x11d1b9c,0x11d21a2],
          fixup=[0x105fc60,0x3d88864,0x11d2593,0x11d2aa9,0x110586b,0x11058c8,0x1105906],first_counterexample=ctrl['Nrvn_tag_change']))
    common=[0x1043322,0x1065f22,0x10685d9,0x10685e1,0x11f06c1]
    ps['Calt'].update(owner='NATIONAL_TEAM_CONTAINER via TEAM_CONTAINER base; NATION slot2 view; not TEAM/t24',table_type=9,member='table_9.dat',reader=0x105cb10,
        status='cursor_closed_empty_fields_held',new_evidence=dict(getter=common+[0x11f139a,0x11f21b5,0x11ff710,0x3ecc093,0x3ecc286],object_pointer=0xa8,
          setter=[0x1045300,0x3d61fd8,0x3d61fe9,0x10647d7,0x11f4c32,0x11f461b,0x11cf7a1,0x11cf7cb,0x11fc7c7],
          sink=[0x105ef12,0x11d1bf2,0x11d1ca7,0x11d1e65,0x11d1e86,0x11d1fbb],first_counterexample=ctrl['Calt_no_live']))
    ps['TCrs'].update(owner='NATIONAL_TEAM_CONTAINER via TEAM_CONTAINER base; NATION slot2 view; not TEAM/t24',table_type=9,member=None,reader=0x11d3200,
        status='owner_and_reader_static_member_unresolved',new_evidence=dict(getter=common+[0x11f15ab,0x11f1e30,0x15634b0,0x4391eaa,0x11f1e3b,0x11f3e37,0x11f3e44,0x11f3e54,0x11f40d8],
          setter=[0x11f4e38,0x11f461b,0x11cfa56,0x11cfa83,0x11fbcee,0x11e9970,0x3ebb845,0x3ebb8c7,0x3ebb8ec,0x3ebb921],
          projection=[0x11fc500,0x3ec7502,0x155a760,0x4387270,0x43872a0,0x43872d0,0x4387300,0x3ec75c8,0x155a35a],
          object_pointer_path=[0xb0,0x48],item_allocation_width=12,allocation_pool_VA=0x141b5e150,
          read_chain=[0x11d32e6,0x11d3429,0x11d366e,0x11d4bad,0x11d4bfe,0x155b450,0x4387ae0,0x4387b46,0x155c152,0x155c31a],
          archive_candidate_context=[0xf51665,0xf51671,0xf55120,0x3bb9670,0x3bb9698,0xffa3b0,0x3cefc62,0x3cefca4,0x3cefcb2,0x3cefd4e,0x3bb96d6,0x3bb97e2,0x3bb97ec,0x3b94c5d],
          main_table_context_comparison=[0xf4e131,0xf4e169,0xf4e1af,0xf4e1d5,0xf2dbd0,0xf2dbd3,0xf2dc01],
          extra_member_template='table_extra_<table[+0x54] decimal>.dat',archive_candidate='table_extra_9.dat (not an accepted binding)',
          archive_caveat='Named auxiliary opener takes the context +0x60 table pointer and constructs table_extra_ prefix plus table ID and .dat. No separately accepted ID/mode/EOF binding for TCrs here. Keep t49 Extra9 negatives. Main-reader reuses item reader at different +0x188 sink, not proof of alias.',
          main_t9_presence_gates=gates,first_counterexample=next(g for g in gates if g['presence']),field_hold='No verified wire cursor for getter collection; no PUnP ordinal or ftjn enum assertion.'))
    ps['Nftb'].update(owner='NATION; legacy t9 can write the linked NATION object',table_type=10,member='table_10.dat',reader=0x103fac0,status='cursor_closed_item_fields_partial',
        new_evidence=dict(setter=[0x1045300,0x3d61fcf,0x104536b,0x1045b0d,0x1045b34,0x1045b66,0x1050d90,0x1050e7d,0x15d07b0,0x44929da,0x4492a35,0x104b6f0,0x3d6bec2],
          item_getter=[0x10512c0,0x3d78479,0x3d78561,0x1051580,0x3d78752,0x3d78818,0x10728c0],
          parent_getter='Exact parent display getter remains unproven; matching child projection on same NATION+0x170 reached from import helper.',
          object_pointer=0x170,allocation_pool_VA=0x141b5f1b8,item_allocation_width=56,sink=[0x104011f,0x104012c,0x1040144,0x1040199,0x10401dd,0x15cf370,0x448f890,0x10401ea,0x1040155],
          legacy_t9=[0x105d7db,0x105d7e4,0x105d80c,0x105d813,0x105d883,0x105d897],first_counterexample=dict(row=162,absolute=278809,raw='0700',reason='debug only does not imply nonpersisted')))
    ps['EDfx'].update(owner='NATION (selected type 10 input to view); editor context owns output',table_type=10,member=None,reader=None,status='editor_view_path_proven_backing_unbound',
        new_evidence=dict(route=[0x28166,0x2816b,0x29c37,0x29c66,0x29c69,0x29c80,0x9082e,0x909d9,0x103f9f0,0x3d5c091,0x90a24],
          first_counterexample=dict(file_offset=0x29c37,reason='reachable exact compare, not just accidental raw bytes; builder uses runtime calendar object, not archive opener on shown route'),
          persistence_scope='Projection handler substantiated, no direct Nation or Team record-getter hit / wire sink or dedicated member established. Other calendar/rules inputs not excluded.'))
    ps['EDsc'].update(owner=None,table_type=None,member=None,reader=None,status='unresolved_rule_ui_schema_only',
        new_evidence=dict(rule_group_occurrence=schema['field_codes']['EDsc'],first_counterexample=dict(scope='advanced/database test/comp test.xml#cpts',reason='same schema parent code appears outside Nation view; cannot infer shared backing or a NATION reader'),
          persistence_scope='No verified code route / archive opener / wire member. Read-only schema and rule-test occurrence are not proof of non-persistence; computed/resource route remains open.'))
    br=[]
    for site,(kind,pred,reason,example) in BRANCHES.items():
        i=rec(site); b=rec(pred); br.append(dict(site=site,classification=kind,predicate=pred,predicate_instruction=b['instruction'],taken=i['direct_target'],fallthrough=site+len(bytes.fromhex(i['bytes'])),reason=reason,
            first_counterexample=ctrl[example] if isinstance(example,str) else example))
    for cspec in cs.values():put('cursor_'+cspec['member'].split('.')[0]+'_'+cspec['side']+'.json',cspec)
    for k,fs in fields.items():put('fields_'+k+'.json',dict(parent=k,scope='nation.xml#nation',fields=fs,L3=sum(x['status']=='L3' for x in fs.values()),L4=0))
    for kind,recs,n in [('instructions',sorted(ins.values(),key=lambda x:x['file_offset']),400),('branches',br,100)]:
        for q in range(0,len(recs),n):put(f'{kind}.part{q//n+1:03}.json',recs[q:q+n])
    put('discovery_unknown2.json',dict(status='partial',L3=sum(x['status']=='L3' for f in fields.values() for x in f.values()),L4=0,parents=ps,
        source=dict(editor=str(EXE),editor_sha256=PE_SHA,snapshots={k:gov[k] for k in (MASTER,IDA)},unchanged=SEALED,
            t9_owner_fixup=old['t9_owner_fixup'],t9_sidecar_negative=archive_open['binding']['table_extra_9.dat'],
            t9_sidecar_trials={s:archive_open['trials'][s]['table_extra_9.dat'] for s in ('client','server')}),
        factory=old['factory'],pe_data=cells,extents=ext,archives=meta,targets=targets,controls=ctrl,
        team_control=dict(path=[0x11b0f6c,0x15e9830,0x44d7c6a,0x44d7c71],global_VA=0x141b60158,
                         verdict='known global vector is a different TEAM dispatch path; neither Calt nor TCrs owner chain uses it'),
        scope='Six parents only; prior cursor spans reused for non-target bytes. No live editor or entire program reachability claim.'))
    print('t51 partial: Nrvn and Nftb live; Calt empty; TCrs reader unbound to member; EDfx view; EDsc unresolved; L3=6 L4=0')


def selftest():
    b=bytes([1])+S.pack('<q8b',29,0,0,2,6,90,1,0,-1)+b'\0\0'
    r,c,e=tail9(b,0,len(b));ck(r['items'][0]['leve']==90 and c['count']==0 and e==len(b),'tail9')
    ck(first_failure(lambda:tail9(b,0,4))[0]=='short transfer','bound check')
    b=bytes([1])+S.pack('<4I2H4i',0,0,0,0,39,1974,-1,788,-1,-1)
    ck(ftb_items(Span(b,0,len(b)),1)[0]['date']['packed']==(1974<<17)|(39<<8),'date pack')
    ck(join([(0,0,12,29)],{29:34})['ordinal_matches']==1,'join')
    print('t51 builder selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__); args=ap.add_mutually_exclusive_group();args.add_argument('--build',action='store_true');args.add_argument('--selftest',action='store_true');a=ap.parse_args()
    try:
        if a.selftest:selftest()
        else:build()
        return 0
    except Fail as e:print(f'check failed: {e}',file=sys.stderr); return 1
    except Exception as e:print(f'fatal: {type(e).__name__}: {e}',file=sys.stderr); return 2


if __name__=='__main__':raise SystemExit(main())
PY