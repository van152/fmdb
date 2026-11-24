"""t75 wire-first backtrace of t72 slots, with full nation item replay (0/1/2)."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t75/out'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
SIDES = ('client', 'server')
TABLES = {'nation': (10, 55, 65, 'E94', 'E108'), 'club': (3, 57, 63, 'E97', 'E106'),
          'comp': (25, 59, 64, 'E99', 'E107')}
REF = {'language': 8, 'nation': 10, 'continent': 5, 'region': 19, 'agreement': 56, 'club': 3}
ARCHIVE_TABLES = (3, 5, 8, 10, 19, 21, 25, 56)
GROUPS = {
    2: ('h', '4', (0x103fc63, 0x103fcb1, 0x103fcbd, 0x103fc88, 0x103fc9b, 0x3d60374, 0x3d60393, 0x3d603a7)),
    3: ('i', '4', (0x103ff2a, 0x103ff79, 0x103ff48, 0x103ff58)),
    4: ('h', 'tag + 4*(u32 length + bytes) + date4 + 4*4',
        (0x104012c, 0x10401dd, 0x15cf370, 0x448f8b1, 0x448f8c9, 0x448f8e5, 0x448f901, 0x448f919,
         0x448f92c, 0x448f948, 0x448f964, 0x448f980, 0x448f9a9, 0x814110, 0x35b0828, 0x35b0847, 0x35b0883)),
    11: ('i', '1+4+4+4+2+1+1+4+1+1+[2 if u8 tag>=2]',
         (0x1040485, 0x1040494, 0x144bca0, 0x420c913, 0x420c933, 0x420c953, 0x420c973,
          0x420c993, 0x420c9b6, 0x420c9d2, 0x420c9ed, 0x420ca09, 0x420ca25, 0x420ca3a,
          0x420ca3f, 0x420ca57, 0x420ca68)),
    12: ('I', '4+date4+date4', (0x10404e3, 0x10404e9, 0x1040529, 0x104053f, 0x1040554, 0x104056d, 0x104057c,
                          0x1040e00, 0x3d5df6b, 0x104e4c0, 0x3d745dc, 0x3d745df, 0x3d5dfa5, 0x3d5dfa7, 0x3d5dfaa, 0x3d5dfae)),
    13: ('I', '1+4+4+1+1+1+1+1', (0x104057e, 0x1040592, 0x104e6b0, 0x3d74f70, 0x3d74f9c, 0x1072560,
        0x3daa131, 0x3daa150, 0x3daa170, 0x3daa18c, 0x3daa1a8, 0x3daa1c4, 0x3daa1e0, 0x3daa209, 0x3d74fc3)),
    23: ('b', '4+1', (0x104073b, 0x104075b, 0x105fb50, 0x3d8771f, 0x3d87742, 0x1040779, 0x104078d, 0x104078f)),
    24: ('i', '5*4+date4+date4', (0x10407d6, 0x1040829, 0x15cf4a0, 0x448faaf, 0x448facf, 0x448faeb, 0x448fb07,
          0x448fb23, 0x448fb33, 0x448fb4d, 0x1040847)),
    25: ('i', '5*4+date4+date4', (0x1040898, 0x10408eb, 0x15cf4a0, 0x448faaf, 0x448facf, 0x448faeb, 0x448fb07,
          0x448fb23, 0x448fb33, 0x448fb4d, 0x1040908)),
    26: ('i', '4+date4+date4', (0x1040980, 0x10409a7, 0x105fbb0, 0x3d88320, 0x3d88345, 0x3d8838c, 0x10409c9)),
}
SPECIAL = {
    ('club','ref_e0'): ('t10 ordinal lane; no scoped exact 4CC', [0xe5a807,0xe5a81d,0xe5a821,0xe5a840,0xe5a843,0xe5c59e,0xe5c5a5,0xe5c5b9], []),
    ('club','raw168'): ('stadium ordinal hit is non-discriminating without a target resolver or exact gate', [0xe5bbd0,0xe5bbd4,0xe5bc18,0xe5bc1f], []),
    ('club','obj150_tag'): ('format tag selecting backing object; matching cnst values are coincidental', [0xe5ada9,0xe5adc8,0xe5add3,0xe5ae12], []),
    ('club','base_ba'): ('base byte selects subtype branches, not an established CLUB field', [0x11f1564,0x11f1570,0x11f157f,0x11f1558,0x11f1dec,0x11f1665,0x11f1f3b], ['TISN','TISC','TLeg']),
    ('comp','m1a4'): ('exact Ccre getter reaches this byte, but Ccre is absent from frozen field_codes', [0xeb70ed,0xeb7100,0xec2c88,0xec2c8e,0xec2c94,0xec2c9d], ['Ccre']),
    ('comp','mf9'): ('cosr suppresses -1 and is absent from frozen field_codes', [0xec0a91,0xec0a97,0xec35da,0xec35e3,0xec35e6], ['cosr']),
    ('comp','m184'): ('static clrp/lREp/cdif; no frozen occurrence and all ones in server', [0xec1f98,0xec1fa4,0xec2bfc,0xec2c08,0xec2013,0xec202e], ['clrp','lREp','cdif']),
    ('comp','m186'): ('static ccrp/cREp/cdif; no frozen occurrence and all ones in server', [0xec0710,0xec071c,0xec24f3,0xec462c,0xec2037], ['ccrp','cREp','cdif']),
    ('comp','m152'): ('perfect stadium ordinal membership alone does not establish a typed join', [0xeb7a47,0xeb7a51,0xeb7a5a], []),
    ('comp','m138'): ('packed date transfer, no exact scoped getter; wbst is +0x140', [0xeb718b,0xeb7cc4,0x39dd7d4], []),
    ('comp','m13c'): ('packed date transfer, no exact scoped getter; wben is +0x144', [0xeb71a2,0xeb7cdb,0x39dd7d4], []),
    ('comp','m1a8'): ('same literal displacement at ec18d1/ec3b86 is on context child RDI; reader destination is COMP RBX', [0xeb7633,0xec18c1,0xec18d1,0xec3b86], []),
    ('comp','mf4'): ('dbty domain violation remains; WpBn is computed, CICF is an unfrozen equality projection', [0xec152a,0xec3896,0xec2cda,0xec2ce6,0xec2cf7,0xec1ae0,0xec1ae6,0xec431e,0xec4335,0xec4341,0xec4346], ['dbty','WpBn','CICF']),
    ('nation','slot_31'): ('t25 ordinal membership does not bind a resolver or exact frozen getter', [0x1040a6d,0x1040a80], []),
    ('nation','slot_34'): ('Npop is not in frozen field_codes', [0x1041fa8,0x1041fb4,0x1040aec], ['Npop']),
    ('nation','slot_17'): ('Ncpi already established by t22 and t55, outside the frozen schema', [0x1042144,0x1042174,0x1040633,0x3d6035d], ['Ncpi']),
}

class Check(Exception):
    pass


def need(ok, why):
    if not ok:
        raise Check(why)


def h(b):
    return sha256(b).hexdigest()


def j(path):
    return json.loads((ROOT / path).read_bytes())


def old(t, name):
    return f'scratch/t{t}/out/{name}'


def run(path):
    return runpy.run_path(str(ROOT / path))


def witness(b, row, at, width, start=None):
    r = dict(row=int(row), absolute=int(at), width=int(width), raw=b[at:at+min(width,32)].hex())
    if start is not None:
        r['body_relative'] = int(at-start-1)
    return r


def hist(x):
    u, n = np.unique(x, return_counts=True)
    return {str(v.item()): int(k) for v, k in zip(u, n, strict=True)}


def profile(b, cells, fmt='I', spans=None):
    # cells have (ordinal, absolute, width); vectorize fixed-width lane values.
    a = np.array(cells, dtype='<u4').reshape(-1,3)
    out = dict(rows=len(a), bytes=int(a[:,2].sum()), width_histogram=hist(a[:,2]), coordinates_sha256=h(a.tobytes()))
    if not len(a):
        return out, np.array([], dtype=np.uint32)
    def pt(x):
        r,p,w = map(int,a[x]); return witness(b,r,p,w,None if spans is None else spans[r][0])
    out.update(first=pt(0), last=pt(-1))
    w = int(a[0,2]); out['fixed_width'] = w if np.all(a[:,2]==w) else None
    if w in (1,2,4,8) and out['fixed_width']:
        z = np.frombuffer(b, np.uint8)[a[:,1,None]+np.arange(w)].copy()
        x = z.view(f'<u{w}').ravel()
        out.update(value_sha256=h(z.tobytes()), distinct=int(np.unique(x).size), zero=int(np.count_nonzero(x==0)),
                   all_ones=int(np.count_nonzero(x==np.iinfo(x.dtype).max)), minimum=int(x.min()), maximum=int(x.max()))
        if fmt in ('b','h','i','f') and S.calcsize(fmt)==w:
            return out, z.view('<'+fmt).ravel()
        return out,x
    return out, np.array([], dtype=np.uint32)


def joins(b, cells, values, target):
    v = np.asarray(values, dtype=np.int64); uid = np.asarray(target, dtype=np.int64)
    live = v != 0xffffffff; ord_hit = live & np.isin(v,np.arange(len(uid))); uid_hit = live & np.isin(v,uid)
    equal = np.zeros(len(v),bool); equal[ord_hit] = uid[v[ord_hit]]==v[ord_hit]
    back = {int(u): i for i,u in enumerate(uid)}
    def first(mask):
        ix=np.flatnonzero(mask)
        if not ix.size:return None
        i=ix[0]; val=int(v[i]); return dict(witness(b,*cells[i]),value=val,
            ordinal_target_uid=int(uid[val]) if ord_hit[i] else None, uid_target_ordinal=back.get(val))
    return dict(live=int(live.sum()), all_ones=int((~live).sum()), ordinal_hit=int(ord_hit.sum()),
                ordinal_miss=int((live & ~ord_hit).sum()), uid_hit=int(uid_hit.sum()),
                uid_wrong_target=int((ord_hit & uid_hit & ~equal).sum()), legal_zero=int((v==0).sum()),
                first_live=first(live), first_ordinal_miss=first(live & ~ord_hit),
                first_uid_miss=first(live & ~uid_hit), first_wrong_target=first(ord_hit & uid_hit & ~equal))


def target_id(b, tid, side):
    n=S.unpack_from('<I',b,8)[0]; end=len(b)-9
    if tid==8:
        # Native identity is 12 B. The one valid initial candidate is the
        # UID=1 record; later ordinals each have one candidate.
        a=np.frombuffer(b,np.uint8); p=np.arange(13,end-11)
        x,y,z=[a[p[:,None]+i+np.arange(4)].copy().view('<u4').ravel() for i in (0,4,8)]
        keep=(x<n)&(y==z)&(y>0)&(y<=S.unpack_from('<I',b,end+5)[0]); p,x,y=p[keep],x[keep],y[keep]
        second=y[x==1]; need(len(second)==1 and np.all(np.bincount(x[x>0],minlength=n)[1:]==1),'t8 unique noninitial triples')
        p=p[(x!=0)|(y<second[0])]
    else:
        w={5:(34,48),19:(45,46),21:(38,181),56:(13,13)}[tid][side=='server']; p=13+w*np.arange(1,n+1)-12
    a=np.frombuffer(b,np.uint8)[p[:,None]+np.arange(12)].copy(); v=a.view('<u4').reshape(-1,3)
    need(len(p)==n and p[-1]+12==end and b[end:end+5]==bytes.fromhex('0000000001') and
         np.all(np.diff(p)>=13) and np.all(v[:,0]==np.arange(n)) and np.all(v[:,1]==v[:,2]) and
         np.all(v[:,1]!=0) and len(np.unique(v[:,1]))==n, (tid,side,'target actual identity'))
    return v[:,1], dict(count=n, identity_sha256=h(a.tobytes()),payload_sha256=h(b),last_identity=int(p[-1]))


def items(b, cells, position):
    fmt=GROUPS[position][0]; cw=S.calcsize(fmt); records=[]; columns=defaultdict(list); counts=[]
    if position not in (4,11):
        widths={2:(4,),3:(4,),12:(4,4,4),13:(1,4,4,1,1,1,1,1),23:(4,1),
                24:(4,)*7,25:(4,)*7,26:(4,)*3}[position]
        block=np.asarray(cells,dtype=np.int64).reshape(-1,3); step=sum(widths)
        gathered=np.frombuffer(b,np.uint8)[block[:,1,None]+np.arange(cw)].copy().view('<'+fmt).ravel()
        counts=gathered.astype(np.int64)
        need(np.all(counts>=0) and np.array_equal(block[:,2],cw+step*counts),(position,'fixed segment end'))
        stops=np.cumsum(counts); linear=np.arange(counts.sum()); index=np.searchsorted(stops,linear,side='right')
        order=linear-(stops-counts)[index]; start=block[index,1]+cw+step*order; row=block[index,0]
        records=np.column_stack((row,order,start,np.full(len(start),step))).tolist()
        if len(start):
            for off,z in zip(np.r_[0,np.cumsum(widths)[:-1]],widths,strict=True):
                columns[str(off)]=np.column_stack((row,start+off,np.full(len(start),z))).tolist()
        return records, columns, item_profile(b, records, counts)
    for row,at,w in cells:
        end=at+w; p=at+cw; n=S.unpack_from('<'+fmt,b,at)[0]; counts.append(n)
        need(0<=n<=w-cw,(position,row,at,'count'))
        for idx in range(n):
            a=p
            if position==4:
                parts=[('tag',p,1)]; p+=1
                for k in range(4):
                    need(p+4<=end,(position,row,p,'string prefix')); length=S.unpack_from('<I',b,p)[0]
                    parts.extend(((f'len{k}',p,4),(f'str{k}',p+4,length))); p+=4+length
                for key in ('date','after0','after4','after8','after12'):
                    parts.append((key,p,4)); p+=4
            else:
                widths=(1,4,4,4,2,1,1,4,1,1)
                need(a<end,(position,row,a,'item starts at end'))
                if b[a]>=2: widths+=(2,)
                parts=[]
                for z in widths:
                    parts.append((str(p-a),p,z)); p+=z
            need(p<=end,(position,row,idx,p,end,'item crosses segment end'))
            for key,q,z in parts: columns[key].append((row,q,z))
            records.append((row,idx,a,p-a))
        need(p==end,(position,row,at,p,end,'segment end'))
    return records, columns, item_profile(b, records, counts)


def item_profile(b, records, counts):
    m=np.array(records,dtype='<u4').reshape(-1,4)
    return dict(items=len(m),nonempty=int(np.count_nonzero(counts)),count_histogram=hist(np.asarray(counts,dtype=np.int64)),
                                   item_width_histogram=hist(m[:,3]),item_coordinates_sha256=h(m.tobytes()),
                                   first_item=item_witness(b,records[0]) if records else None,
                                   last_item=item_witness(b,records[-1]) if records else None)


def item_witness(b, item):
    r,i,a,w=item; return dict(witness(b,r,a,w),item=i)


def dates(v):
    v=v.astype(np.uint32); y=v>>16; d=v&511; flags=(v>>9)&127
    leap=(y%4==0)&((y%100!=0)|(y%400==0)); bad=(d<1)|(d>365+leap)|(y==0)
    return dict(year=[int(y.min()),int(y.max())], day=[int(d.min()),int(d.max())],
               flags=hist(flags), invalid=int(bad.sum()), default_1900_001=int(((y==1900)&(d==1)).sum()))


def scoped(master, table, code, parent=None):
    fs=master['entities'][table+'.xml'][0]['fields']; records=master['field_codes'].get(code)
    if parent is not None:
        roots=[f for f in fs if f['field']==parent]; need(len(roots)==1,(table,parent,'unique parent')); fs=roots[0]['list_item_fields']
    hits=[i for i,f in enumerate(fs) if f['field']==code]; loc=f'database/database/{table}.xml#'+master['entities'][table+'.xml'][0]['id']
    if parent:loc+='.'+parent
    if len(hits)!=1 or not records: return None
    return dict(index=hits[0],location=loc,schema=fs[hits[0]],field_codes_locations=records['locations'],
                location_listed=(loc in records['locations']))


def raw_load():
    depot=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if depot.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    os.environ['FM24_DB_DIR']=str(depot)
    d=run('scripts/fm24_dump.py'); r=d['_reader']()
    return {(side,t):d['load_payload'](r,side,t) for side in SIDES for t in ARCHIVE_TABLES}


def frozen():
    inv=j(old(72,'inventory.json')); f=j(old(72,'fingerprints.json')); manifest={x['path']:x['sha256'] for x in j('evidence/MANIFEST.json')['files']}
    need(all(h((ROOT/p).read_bytes())==sha for p,sha in f['inputs_sha256'].items()) and f['inputs_sha256']==inv['inputs_sha256'],'t72 frozen inputs')
    need(all(h((ROOT/p).read_bytes())==manifest[p] for p in (MASTER,PROV)) and EXEH in (ROOT/PROV).read_text(encoding='utf8'),'manifest')
    need(j('reports/club_nation_subtable_schema.json')['schema_version']==10,'schema v10')
    m=j(MASTER);need(len(m['field_codes'])==3009,'case-sensitive index')
    return inv,f,m


def refs_and_replays(raw, inv, slots):
    src=run('scripts/t72_slot_fingerprint.py'); cols,spans,targets,target_meta={}, {}, {}, {}
    for side in SIDES:
        for name,(tid,*_) in TABLES.items():
            b=raw[side,tid]; c,s,uid=src['replay_'+name](b,side)
            if name=='nation': c={f'slot_{k}':v for k,v in c.items()}
            v=np.column_stack((np.arange(len(uid)),uid,uid)).astype('<u4'); d=h(v.tobytes()); t=inv['targets'][str(tid)]
            need(d==t['identity_sha256'][side] and len(uid)==t['count'],(side,name,'identity'))
            need(len(b)==inv['replay'][name+'/'+side]['payload'] and s[0][0]==13 and s[-1][1]==len(b)-9,(side,name,'envelope'))
            for i,f in zip(inv['tables'][name]['slots'],slots[name]['slots'],strict=True):
                k=i['key']; a=np.asarray(c.get(k,[]),dtype='<u4').reshape(-1,3)
                need(len(a)==i['coverage'][side],(side,name,k,'coverage'))
                if name=='nation':need(a[:,1:].tolist()==f['coordinates'][side],(side,k,'t55 coordinates'))
                elif len(a):need(h(a.tobytes())==f['profiles'][side]['coordinate_sha256'],(side,k,'t57/t59 coordinates'))
            cols[side,name]=c;spans[side,name]=s;targets[side,tid]=v[:,1]
            target_meta[f'{side}/{tid}']=dict(count=len(v),identity_sha256=d,payload_sha256=h(b),last_identity=s[-1][1]-12)
        for tid in (5,8,19,21,56):
            v,m=target_id(raw[side,tid],tid,side);targets[side,tid]=v;target_meta[f'{side}/{tid}']=m
            if str(tid) in inv['targets']:need(m['identity_sha256']==inv['targets'][str(tid)]['identity_sha256'][side],(side,tid,'external target digest'))
    for tid in ARCHIVE_TABLES: need(np.array_equal(targets['client',tid],targets['server',tid]),(tid,'paired identities'))
    path=ROOT/old(46,'profiles/table_server_10.rows.jsonl'); b=raw['server',10]; lines=path.read_bytes()
    profile46=j(old(46,'profiles/table_server_10.profile.json'))
    need(h(lines)==profile46['full_rows_sha256'] and h(b)==profile46['payload']['payload_sha256'] and
         len(spans['server','nation'])==profile46['row_closure']['count'],'t46 frozen row profile')
    for (a,e,uid),line in zip(spans['server','nation'],lines.splitlines(),strict=True):
        x=json.loads(line);need((a+1,e-a,uid,b[a+1:e+1].hex())==(x['offset'],x['len'],x['identity']['row_id'],x['raw_hex']),('t46 legacy row',a))
    return cols,spans,targets,target_meta


def nation_grammar(raw, cols, spans, targets, inv, slots, master, recorded):
    t28=j(old(28,'fields_nation_client.json'))['fields']; tax=j(old(47,'fields_nation_tax.json'))['fields']; ftb=j(old(51,'fields_Nftb.json'))['fields']; t46=j(old(46,'grammar_diff_client_server.json'))
    groups=[]; reverified=[]
    for esc in inv['escalations']:
        p=int(esc['slot'].split('_')[1]); fmt,grammar,route=GROUPS[p]; s=slots['slots'][p]; parent=s['candidate_4cc']; a=s['collection'];
        prior='E64' if p>=23 else 'E90' if p==4 else 'E87' if p==11 else 'E108'
        group=dict(escalation=esc,grammar=grammar,count_format='<'+fmt,reader_site=s['site'],object_displacement=s['object_displacement'],
                   gate_helper_cursor=list(dict.fromkeys([0x103fae6,s['site'],a['proof'],*route])),
                   grade='held_no_items' if p in (2,3) else 'L3_physical_only', prior_ids=['E94',prior,'E112'],archives={},fields=[])
        recorded.update(group['gate_helper_cursor']); group['parent']=scoped(master,'nation',parent) if parent else None
        if p in (12,24,25): recorded.update((0xdb7f80,0x39dd7d4))
        if p==2:group['static_item_target_hint']='context +0x28 / shared Nation resolver; no live items, no indexed 4CC'
        if p==12:group['static_item_key']='item +0 is used as ordered i32 node key +0x1c; two packed dates stored at node +0x20/+0x24; container key use does not prove entity identity'
        if p>=23: group['t46_positional_reject_unchanged']=t46['segments'][esc['collection']]
        names={}
        for f in t28:
            if p>=23 and f.get('parent')==parent and f.get('grade')=='L3':
                names[str(f['item_offset'])]=(f['code'],'L3_reverified_server',f['object_off'],f['getter_chain'],f['reader_sites'], f['schema_index'])
        if p==11:
            names={str(x['static_item_offset']):(k,'L3_retained' if x['status']=='L3' else 'held',x['object_offset'],[x['compare'],x['getter_load']],[x['reader_site']],k) for k,x in tax.items()}
        if p==4:
            lane={'NpFn':'str0','NpSn':'str1','NbCn':'str3','NbPd':'date','NbFt':'after0','NbPn':'after4','NbPi':'after12'}
            names={lane[k]:(k,'L3_retained' if x['status']=='L3' else 'held',x['object_offset'],[x['compare'],x['getter_load']],[x['reader_sink']],k) for k,x in ftb.items()}
        data={}
        for side in SIDES:
            b=raw[side,10]; c=cols[side,'nation'].get(esc['slot'],[]); group['archives'][side]=profile(b,c,spans=spans[side,'nation'])[0]
            rr, lanes, pts=items(b,c,p); group['archives'][side].update(pts); data[side]=(c,rr,lanes)
            if p in (2,3):need(not rr,(p,side,'must stay zero-item'))
        if p>=23:
            c,srv=(np.asarray(data[side][0],dtype=np.int64) for side in SIDES)
            widths=c[:,2]; need(len(c)==len(srv)==251 and np.array_equal(widths,srv[:,2]),(p,'framed parity'))
            q=np.arange(widths.sum())-np.repeat(np.cumsum(widths)-widths,widths)
            a=np.frombuffer(raw['client',10],np.uint8)[np.repeat(c[:,1],widths)+q]
            b=np.frombuffer(raw['server',10],np.uint8)[np.repeat(srv[:,1],widths)+q]
            need(np.array_equal(a,b),(p,'full recordwise A/B/C/D byte parity'))
            group['cross_archive_equal_segments']=251
        if p==23:
            group['single_item_percent_rewrite']={}
            for side in SIDES:
                b=raw[side,10]; c=np.asarray(data[side][0]); one=c[c[:,2]==6]; v=np.frombuffer(b,np.uint8)[one[:,1]+5]
                group['single_item_percent_rewrite'][side]=dict(single_item_rows=len(one),wire_values_not_100=int((v!=100).sum()),wire_histogram=hist(v))
        for lk in dict.fromkeys([*data['server'][2],*names]):
            code,grade,disp,get,sink,pid=names.get(lk,(None,'held',None,[],[],None)); sf=scoped(master,'nation',code,parent) if code else None
            if code: need(sf is not None,(parent,code,'scoped exact field_codes'))
            opaque_dest={12:{'0':0x1c,'4':0x20,'8':0x24},13:{'1':0,'5':4,'9':8,'10':9,'11':0xa,'12':0xb,'13':0xc}}
            if p in opaque_dest:disp=opaque_dest[p].get(lk)
            rec=dict(lane=lk,code=code,grade=grade,item_object_displacement=disp,scoped_occurrence=sf,
                     getter_chain=get,reader_sites=sink,prior_id=f'{prior}/{parent}/{pid}' if code else prior,archives={})
            recorded.update([*get,*sink]); sch=sf['schema'] if sf else {}; typ=sch.get('type')
            for side in SIDES:
                b=raw[side,10]; c=data[side][2].get(lk,[]); valfmt=tax[code]['format'] if p==11 and code else 'I'
                stats,v=profile(b,c,valfmt,spans[side,'nation']); rec['archives'][side]=stats
                if not c:continue
                if typ=='date' or p==12 and lk in ('4','8'):
                    stats['date']=dates(v); need(stats['date']['invalid']==0,(p,lk,side,'calendar'))
                if typ=='database_record_unique_id' and sch['database_table_type'] in REF:
                    tid=REF[sch['database_table_type']]; stats['reference']=joins(b,c,v,targets[side,tid]); stats['reference']['table_id']=tid
                    if p>=23: need(stats['reference']['ordinal_miss']==0,(p,code,side,'actual ordinal join'))
                if p==12 and lk=='0':
                    stats['untyped_join_probes']={str(t):joins(b,c,v,targets[side,t]) for t in (3,10,25)}
                if p==4 and lk.startswith('str'):
                    lens=np.array([int.from_bytes(b[a-4:a],'little') for _,a,_ in c]); need(np.array_equal(lens,[w for _,_,w in c]),(p,lk,'prefix'))
                    stats['utf8_codepoint_lengths']=hist(np.array([len(b[a:a+w].decode('utf8')) for _,a,w in c]))
                if typ in ('integer','real','cash') and grade.startswith('L3'):
                    live=v[(v>0) if code=='fram' else (v>=0) if code=='leve' else np.ones(len(v),bool)]
                    need(np.all(np.isfinite(live)) and np.all(live>=float(sch.get('min_value','-inf'))) and
                         np.all(live<=float(sch.get('max_value','inf'))),(p,side,code,'frozen min/max'))
                    stats['scalar_domain']=dict(live=len(live),suppressed=len(v)-len(live),minimum=float(live.min()),maximum=float(live.max()))
            if p==4 and code in ftb and grade=='held':rec['prior_negative_verbatim']=ftb[code]
            if p==11 and code in tax and grade=='held':rec['prior_negative_verbatim']=tax[code]
            if grade=='held':
                ss=rec['archives']['server']; rec['first_counterexample']=(rec.get('prior_negative_verbatim',{}).get('first_counterexample') or
                    ss.get('reference',{}).get('first_ordinal_miss') or
                    rec.get('prior_negative_verbatim',{}).get('join',{}).get('first_ordinal_miss') or ss.get('first'))
                rec['blocker']=(rec.get('prior_negative_verbatim',{}).get('reason') or rec.get('prior_negative_verbatim',{}).get('status') or
                    'physical subtransfer only; no exact scoped field getter')
            if grade=='L3_reverified_server': reverified.append(dict(id=f't75/nation/{parent}/{code}',prior_id=rec['prior_id'],slot=p,
                grade=grade,scoped_occurrence=sf,server_domain=rec['archives']['server']))
            group['fields'].append(rec)
        if p in (24,25):
            for side in SIDES:
                b=raw[side,10]; lanes=data[side][2]; x=np.stack([profile(b,lanes[str(k)])[1] for k in range(0,20,4)])
                need(np.all(np.count_nonzero(x!=0xffffffff,axis=0)==1),(p,side,'selector exclusivity'))
            group['exactly_one_live_selector_per_item']=True
        if p in (2,3,4,12,13):
            group['first_naming_blocker']=group['archives']['server']['first_item'] or group['archives']['server']['first']
        groups.append(group)
    return groups,reverified


def comp_dispatch(pe, root):
    """Follow exact e(si)-normalized local rel32 dispatches; not arbitrary indirect edges."""
    from capstone import CS_OP_IMM, CS_OP_MEM, CS_OP_REG
    end=pe.ext[root]; previous=[]; tables={}; bit={}
    split={0xec0e24:0xec065b,0xec118e:0xec0317,0xec1504:0xec0bfc,0xec151e:0xec0927}
    def seq(at,n):
        items=[]
        for _ in range(n):
            q=pe.get(at);items.append(q);at+=q.size
        return items
    for q in pe.md.disasm(pe.raw[root:end],pe.va(root)):
        a=pe.off(q.address); pe.i[a]=q
        if len(previous)>=6 and q.mnemonic=='jmp' and q.operands[0].type==CS_OP_REG:
            s=(seq(split[a],3)+previous[-3:]) if a in split else previous[-6:]
            norm,bound,br,lea,mov,add=s
            if ([i.mnemonic for i in s] in (['lea','cmp','ja','lea','movsxd','add'],['lea','cmp','jbe','lea','movsxd','add'])
                and norm.op_str.startswith('eax, [rsi - ') and bound.op_str.startswith('eax, ')
                and lea.op_str.startswith('rcx, [rip ') and mov.op_str=='rax, dword ptr [rcx + rax*4]'
                and add.op_str=='rax, rcx' and q.op_str=='rax'):
                if a in split:need(pe.dst(br)==pe.off(lea.address),'COMP split rel32 gate')
                tables[a]=s
        if len(previous)>=4 and q.mnemonic=='bt':
            n,c,j,l=previous[-4:]; b=pe.get(a+q.size)
            if n.mnemonic=='lea' and n.operands[1].type==CS_OP_MEM and n.reg_name(n.operands[1].mem.base)=='rsi' and c.mnemonic=='cmp' and j.mnemonic=='ja' and l.mnemonic in ('mov','movabs') and l.operands[-1].type==CS_OP_IMM and b.mnemonic in ('jb','jae'):
                cnt=c.operands[-1].imm if c.operands[-1].type==CS_OP_IMM else -1
                if 0<=cnt<64 and n.operands[1].mem.disp<=-0x20000000 and c.operands[0].reg==n.operands[0].reg and q.operands[1].reg==n.operands[0].reg and q.operands[0].reg==l.operands[0].reg:
                    bit[a]=[n,c,j,l,q,b]
        previous.append(q)
    todo=[root]; seen={}; gates=defaultdict(list); unresolved=[]; resolved=[]
    while todo:
        a=todo.pop()
        if not root<=a<end or a in seen:continue
        q=pe.get(a); seen[a]=q; nxt=a+q.size; m=q.mnemonic
        if m=='cmp' and len(q.operands)==2 and q.operands[0].type==CS_OP_REG and q.operands[-1].type==CS_OP_IMM:
            b=pe.get(nxt)
            if b.mnemonic in ('je','jne'):
                k=q.operands[-1].imm; gates[k].append(dict(root=root,kind='compare',index=None,sites=[a,nxt],arm=pe.dst(b) if b.mnemonic=='je' else nxt+b.size))
        if a in bit:
            n,c,j,l,q,b=bit[a]; low=-n.operands[1].mem.disp; mask=l.operands[-1].imm
            for ix in range(c.operands[-1].imm+1):
                if (mask>>ix)&1: gates[low+ix].append(dict(root=root,kind='bt',index=ix,low=low,mask=mask,
                    sites=[pe.off(i.address) for i in bit[a]],arm=pe.dst(b) if b.mnemonic=='jb' else pe.off(b.address+b.size)))
        if m.startswith('j'):
            dst=pe.dst(q)
            if dst is not None:todo.append(dst)
            if m!='jmp':todo.append(nxt)
            elif dst is None:
                if a not in tables:unresolved.append(a);continue
                norm,bound,br,lea,*_=tables[a]; table=pe.rip(lea); n=bound.operands[-1].imm+1; low=-norm.operands[1].mem.disp
                need(0<n<=128,('COMP jump table count',a)); cells=[pe.cell(table,i) for i in range(n)]
                # Default padding may land in another dispatch subtree. Explore it,
                # but don't label those cells as exact schema arms.
                default=pe.dst(br) if br.mnemonic=='ja' else Counter(c['target'] for c in cells).most_common(1)[0][0]
                resolved.append(dict(jump=a,base=table,count=n,first_code=low,default=default))
                for i,c in enumerate(cells):
                    need(root<=c['target']<end,('COMP local cell',a,i));todo.append(c['target'])
                    if c['target']!=default:gates[low+i].append(dict(root=root,kind='rel32_table',index=i,cell=c,
                        sites=[pe.off(v.address) for v in (*tables[a],q)],arm=c['target']))
        elif m not in ('ret','retf','int3','ud2'):todo.append(nxt)
    return seen,gates,dict(root=root,end=end,reachable=len(seen),register_jumps_not_followed=sorted(unresolved),rel32_tables=sorted(resolved,key=lambda d:d['jump']))


def static_book(slots, master):
    base=run('scripts/t63_club_unmapped_r2.py'); p=base['PE'](); need(h(p.raw)==EXEH,'editor SHA')
    from capstone import CS_OP_MEM
    allroots={
        'club': [r for r in base['GETTERS'] if r not in (0x151d9b0,0x151e500)],
        'comp':[0xec0060,0xfe3520], 'nation':[0x1041f40,0xfe3520]}
    index={}; census={}; readers={}; branch={}; inst=set(); reader_names={}
    for name,(_,t,*_) in TABLES.items():
        source=slots[name]['source']; doc=source.get('extents',source.get('runtime_function_extents',{}))
        main={'nation':0x103fac0,'club':0xe5a7a0,'comp':0xeb7000}[name]
        reader_names[name]={main,*map(int,doc)}
        shards=sorted((ROOT/old(t,'')).glob('instructions.part*.json')); rows=[z for f in shards for z in json.loads(f.read_bytes())]
        branches={z['site']:z for f in sorted((ROOT/old(t,'')).glob('branches.part*.json')) for z in json.loads(f.read_bytes())}
        for z in rows:
            a=z['file_offset']; q=p.get(a)
            need(z['bytes']==q.bytes.hex() and int(str(z['VA']),0)==q.address,(name,hex(a),'frozen instruction'))
        readers[name]={z['file_offset']:z for z in rows}
        branch[name]=branches
        seen,g,info=base['scan'](p,main,False)
        need(len(seen)=={'nation':992,'club':1412,'comp':837}[name],(name,'main reader extent'))
        census[name]={'reader':info,'getter':[],'rooting':'vtable slot 2 / inherited bounded roots, no arbitrary indirect dispatch'}
        tree=defaultdict(list)
        for root in allroots[name]:
            seen,g,info=comp_dispatch(p,root) if root==0xec0060 else base['scan'](p,root)
            census[name]['getter'].append(dict(info,resolve_rel32_tables=True))
            mem=defaultdict(list)
            for at,q in seen.items():
                for op in q.operands:
                    if op.type==CS_OP_MEM and op.mem.base and q.reg_name(op.mem.base) not in ('rsp','rbp','rip') and op.mem.disp:
                        mem[at].append((int(op.mem.disp),q.reg_name(op.mem.base),q.mnemonic=='call' or q.mnemonic=='jmp'))
            keyed=defaultdict(list)
            for code,gates in g.items():
                if not 0<=code<2**32:continue
                k=code.to_bytes(4,'big').decode('ascii',errors='replace')
                if not k.isascii() or not k.isprintable():continue
                for gate in gates:
                    path=base['prefix'](p,seen,gate['arm'],40)
                    for at in path:
                        if at in mem:keyed[at].append((k,gate))
            for at,ops in sorted(mem.items()):
                for off,reg,virt in ops:
                    tree[off].append(dict(root=root,site=at,base_register=reg,indirect_call_or_jump=virt,
                        keyed_prefix=[dict(code=k,master_locations=master['field_codes'].get(k,{}).get('locations',[]),gate=g) for k,g in keyed[at]]))
        index[name]=tree
    return p,census,index,readers,branch,inst


def rank(name, kind, fp, enums, is_escalation, p):
    matches=set(); cleanliness=0.0; live=False; small=False
    for side in SIDES:
        z=fp.get(side,{})
        if not z.get('rows'):continue
        live|=not z.get('all_zero') and z.get('all_ones_ratio',0)<1
        f=z.get('fk_best',{}).get(side) or {}
        if f.get('ordinal_ratio',0)==1:cleanliness=max(cleanliness,1-(f.get('uid_ratio') or 0))
        v=z.get('value_histogram',{}); w=z.get('fixed_width')
        if w in (1,2) and 1<z.get('distinct',0)<=12 and v and z['distinct']==len(v):
            vals={int(k) for k in v}; signed={x-2**(w*8) if x>=2**(w*8-1) else x for x in vals}
            matches.update(k for k,v in enums.items() if signed<=v or vals<=v);small=True
    tier=1 if is_escalation else 2 if name!='nation' and kind=='unnamed' and live else 3 if live else 4
    return dict(tier=tier,scoped_enum_subset_only=sorted(matches),small_live_enum_shape=small,
                fk_ordinal_minus_uid_best=round(cleanliness,6),nonconstant_or_nontrivial=bool(live),position=p)


def extract_negatives(doc):
    """Preserve nested frozen rejection blocks unmodified, indexed by JSON pointer."""
    out={}
    def walk(obj,path):
        if not isinstance(obj,dict):return
        for k,v in obj.items():
            src=path+'/'+k.replace('~','~0').replace('/','~1')
            if any(y in k.lower() for y in ('negativ','falsif','reject')):out[src]=v
            elif k!='fields':walk(v,src)
    walk(doc,'');return out


def build():
    inv,fp,m=frozen(); slots={k:j(old(t,'field_slots.json')) for k,(_,t,*_) in TABLES.items()}; raw=raw_load()
    cols,spans,targets,tm=refs_and_replays(raw,inv,slots)
    pe,census,index,readers,branches,instructions=static_book(slots,m)
    groups,rev=nation_grammar(raw,cols,spans,targets,inv,slots['nation'],m,instructions)
    esc={r['escalation']['slot']:r for r in groups}; negatives={}; trials=[]
    for name,(tid,t,r2,e,e2) in TABLES.items():
        orig=j(old(t,'field_map.json')); prior=j(old(r2,'field_map_r2.json')); sf={x['key']:x for x in fp['tables'][name]['slots']};
        def held(x):return x.get('grade')=='held' or x.get('status')=='held' or x.get('r2_status') in ('held','candidate')
        negatives[name]=dict(r1_id=e,r2_id=e2,r1_negative_keys_verbatim=extract_negatives(orig),
                             r2_negative_keys_verbatim=extract_negatives(prior),
                             r2_held_verbatim=[x for x in prior['fields'] if held(x)],
                             r1_held_verbatim=[x for x in orig['fields'] if held(x)])
        if name=='comp':negatives[name]['t64_exclusions_verbatim']=j(old(64,'exclusions.json'))
        if name=='nation':negatives[name]['edsc_exclusions_verbatim']=j(old(62,'exclusions.json'))['excludes']
        active=m['entities'][name+'.xml'][0]['fields'];refs={x.get('enum_ref') for x in active}
        enums={k:{int(x['enum']) for x in v['values'] if str(x.get('enum','')).lstrip('-').isdigit()}
               for k,v in m['enums'].items() if k in refs and 'values' in v}
        for x,s in zip(inv['tables'][name]['slots'],slots[name]['slots'],strict=True):
            k=x['key'];kind=x['kind'];d=x['object_displacement'];at=x['site'];pos=x['position'];
            if kind not in ('held','unnamed'):continue
            f=sf[k]; g=esc.get(k) if name=='nation' else None
            r=dict(table=name,table_id=tid,slot=k,kind=kind,object_displacement=d,execution_index=x['execution_index'],
                   nominal_width=x['nominal_width'],reader_site=at,transfer=s.get('transfer'),
                   queue=rank(name,kind,f,enums,g is not None,pos),t72_claims=x['claims'],prior_ids=[f'{e}/slot/{pos}',e2,'E112'],archives={})
            if at is not None:instructions.add(at)
            if s.get('transfer'): instructions.update(a for a in (s['transfer'].get('destination_site'),s['transfer'].get('width_site')) if a is not None)
            r['reader_fragment']=readers[name].get(at)
            r['reader_mode_gate']=None
            if not x['coverage']['client'] and (x['coverage']['server'] or k in ('obj_a8','obj_e0')):
                mode={'nation':0x103fae6 if pos<14 else 0x10409d3,'club':0xe5a9ba,'comp':0xeb73a0}[name]
                r['reader_mode_gate']=branches[name].get(mode)
            if r['reader_mode_gate'] is not None:instructions.add(r['reader_mode_gate']['site'])
            match=index[name].get(d,[]); r['displacement_xrefs_untyped']=match
            for hit in match:
                instructions.add(hit['site'])
                for z in hit['keyed_prefix']:instructions.update(z['gate']['sites'])
            reason,route,codes=SPECIAL.get((name,k),(('loader envelope; not a field' if k=='selector' else
                'prior scoped gate/domain blocker retained' if kind=='held' else 'no proved same-owner scoped gate through bounded getter/helper'),[],[]))
            if g:
                reason='see nation item replay; no new parent 4CC'; route=g['gate_helper_cursor'];
            if s.get('getter'):
                get=s['getter']; route=[*route,*(get[a] for a in ('compare','equality_branch','load') if get.get(a) is not None)]
            code_set=list(dict.fromkeys([*(x['code'] for x in x['claims']),*codes]))
            r.update(grade='held',blocker=reason,selected_chain=list(dict.fromkeys(route)),
                     codes=[dict(code=z,master_locations=m['field_codes'].get(z,{}).get('locations',[]),scoped=scoped(m,name,z)) for z in code_set],
                     grammar_ref=f'nation/{k}' if g else None)
            instructions.update(route)
            old_held=[f for f in orig['fields'] if f.get('code') in code_set and held(f)]
            r['prior_held_codes']=[f['code'] for f in old_held]
            for side in SIDES:
                b=raw[side,tid]; c=cols[side,name].get(k,[]); a,v=profile(b,c,spans=spans[side,name]); z=f[side]
                need(len(c)==z['rows'] and (not c or a['bytes']==z['bytes']), (name,k,side,'t72 fingerprint coverage'))
                if len(v) and a['fixed_width']<=8:
                    need(a['distinct']==z['distinct'] and a['zero']==z['zero_count'] and a['all_ones']==z['all_ones_count'],(name,k,side,'t72 fixed fingerprint'))
                probes={('club','ref_e0'):10,('club','raw168'):21,('comp','m152'):21,('nation','slot_31'):25}
                if len(v) and (name,k) in probes:
                    ref=probes[name,k]; probe=joins(b,c,v,targets[side,ref]); probe['table_id']=ref
                    a['reference_probe']=probe
                    if probe['live'] and not probe['ordinal_miss']:
                        r['queue']['fk_ordinal_minus_uid_best']=max(r['queue']['fk_ordinal_minus_uid_best'],round(1-probe['uid_hit']/probe['live'],6))
                if len(v) and k in ('m138','m13c'):a['date_probe']=dates(v)
                a['t72']=z
                r['archives'][side]=a
            r['first_counterexample']=next((a['first'] for side in SIDES if (a:=r['archives'][side]).get('first')),None)
            if k=='ref_e0': r['first_counterexample']=r['archives']['client']['reference_probe']['first_uid_miss']
            for f in old_held:
                domain=f.get('domain_profiles',f.get('profiles',{})) or {}
                bad=f.get('first_counterexample') or next((p.get('first_counterexample') or p.get('first_violation') for p in domain.values() if isinstance(p,dict) and (p.get('first_counterexample') or p.get('first_violation'))),None)
                if bad:
                    r['first_counterexample']=bad; break
            r['prior_occurrence_ids']=[dict(code=f['code'],id=f.get('id',f'{e2}/{name}/{f.get("xml_index")}')) for f in prior['fields'] if f.get('code') in code_set]
            if not r['first_counterexample']:r['first_counterexample']={'file_offset':at,'reason':'static only; no payload observed'}
            trials.append(r)
    trials.sort(key=lambda r:(r['queue']['tier'], -bool(r['queue']['scoped_enum_subset_only']),-r['queue']['fk_ordinal_minus_uid_best'],not r['queue']['small_live_enum_shape'],r['table'],r['queue']['position']))
    pins=set(fp['inputs_sha256'])|{MASTER,PROV,'evidence/MANIFEST.json',*(old(72,s) for s in ('inventory.json','fingerprints.json')),
        *(old(t,'REPORT.md') for t in (28,46,47,51,55,57,59,62,63,64,65,66,71,72)),
        *(old(t,s) for t,s in ((28,'fields_nation_client.json'),(46,'grammar_diff_client_server.json'),(46,'profiles/table_server_10.rows.jsonl'),
            (46,'profiles/table_server_10.profile.json'),(47,'fields_nation_tax.json'),(51,'fields_Nftb.json'),(55,'abc_closure.json'),
            (62,'chain.json'),(62,'exclusions.json'),(64,'exclusions.json'),(71,'field_map_r3.json'))),
        'scripts/t72_slot_fingerprint.py','scripts/t63_club_unmapped_r2.py','scripts/fm24_dump.py',*(old(t,'verify.py') for t in (55,57,59))}
    for t in (55,57,59):pins.update(p.relative_to(ROOT).as_posix() for g in ('instructions.part*.json','branches.part*.json') for p in (ROOT/old(t,'')).glob(g))
    vtable={}
    for name,s in slots.items():
        src=s['source']; vt={'club':lambda:src['CLUB']['vtable'],'comp':lambda:src['comp']['vtable'],'nation':lambda:src['nation_vtable_VA']}[name]()
        vtable[name]={str(k):dict(pe.data(pe.off(vt)+8*k,8),target=pe.off(S.unpack_from('<Q',pe.raw,pe.off(vt)+8*k)[0])) for k in (2,19,20)}
    # Explicitly revisit the known computed EDsc dispatch rather than inferring
    # that a failed literal xref proves an absence of UI dispatch.
    edsc=j(old(62,'chain.json'))['conclusions']['EDsc']; edcell=pe.cell(0x2a7f0,0x32)
    need(edcell['target']==0x29389 and ((int.from_bytes(b'EDsc','big')+pe.get(0x282b9).operands[1].imm)&0xffffffff)==0x32,'EDsc normalization')
    edroute=[0x282b9,0x282bf,0x282c2,0x282c8,0x282cf,0x282d3,0x282d6,0x29389,0x293c5,0x2a23b]
    instructions.update(edroute)
    t71=j(old(71,'field_map_r3.json')); excluded_codes=[{'id':r['id'],'code':r['code']} for r in t71['fields'] if r['grade']=='L3']
    observed_codes={c['code'] for r in trials if r['table']=='club' for c in r['codes']}
    need(len(excluded_codes)==24 and observed_codes.isdisjoint(r['code'] for r in excluded_codes),'t71 no repeat')
    xref=dict(editor=dict(path=str(_cfg.EDITOR_EXE),sha256=EXEH),L4=0,addressing='PE file offset; archive offsets are member-relative; body_relative uses legacy14',
              excluded_t71_4cc=excluded_codes,edsc_control=dict(prior_id='E105',code='EDsc',dispatch=edroute,rel32_cell=edcell,conclusion_verbatim=edsc),
              inputs_sha256={p:h((ROOT/p).read_bytes()) for p in sorted(pins)},target_and_payload_identity=tm,
              t72_negative_notes_verbatim=inv['negative_notes'],negative_evidence=negatives,
              bounded_scan=census,vtable=vtable,nation_escalations=groups,slots=trials,instructions=[pe.record(a) for a in sorted(instructions)])
    delta=dict(scope='t75 append-only; no public schema write',L4=0,new_named_L3=0,physical_nation_replay=8,
               nation_existing_named_server_domain_reverified=rev,
               held_counts=dict(Counter(r['table'] for r in trials)),baseline_ids=['E64','E87','E90','E94','E97','E99','E104','E105','E106','E107','E108','E110','E112'],
               source='xref_reverse.json',note='Server revalidation is additional evidence for existing L3, not 19 new schema fields.')
    for name in TABLES:
        delta[name]=[dict(id=f't75/{name}/{r["slot"]}',slot=r['slot'],grade='held',reason=r['blocker'],
                          first_counterexample=r['first_counterexample'],prior_ids=r['prior_ids']) for r in trials if r['table']==name]
    delta['nation_physical_grammar']=[dict(slot=g['escalation']['slot'],grade=g['grade'],prior_ids=g['prior_ids']) for g in groups]
    OUT.mkdir(parents=True,exist_ok=True)
    for name,doc in [('xref_reverse',xref),('field_map_r3',delta)]:
        (OUT/(name+'.json')).write_text(json.dumps(doc,ensure_ascii=False,indent=1,allow_nan=False)+'\n',encoding='utf8')
    print(f't75: {len(trials)} slot trials, {len(groups)} escalations, {len(rev)} server lane revalidations; 0 new named L3')


def selftest():
    b=bytes.fromhex('0100')+bytes.fromhex('01000000')
    _,_,a=items(b,[(0,0,len(b))],2);need(a['items']==1 and a['first_item']['absolute']==2,'count replay')
    try: items(b,[(0,0,len(b)-1)],2)
    except Check: pass
    else: raise Check('truncation accepted')
    x=joins(bytes(12),[(0,0,4),(0,4,4),(0,8,4)],[0,1,0xffffffff],[1,2]);need(x['uid_wrong_target']==1 and x['legal_zero']==1 and x['all_ones']==1,'wrong UID control')
    need(dates(np.array([(2000<<16)+366,(1900<<16)+366]))['invalid']==1,'Gregorian')
    print('t75 builder selftest OK')


def main():
    ap=argparse.ArgumentParser(description=__doc__); sw=ap.add_mutually_exclusive_group(); sw.add_argument('--build',action='store_true');sw.add_argument('--selftest',action='store_true'); a=ap.parse_args()
    try: selftest() if a.selftest else build(); return 0
    except Check as e: print(f't75 CHECK FAILED: {e}',file=sys.stderr); return 1
    except Exception as e: print(f't75 fatal: {type(e).__name__}: {e}',file=sys.stderr); return 2


if __name__=='__main__':raise SystemExit(main())
