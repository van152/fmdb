#!/usr/bin/env python3
"""Independently check t49 archive replay, PE shards and item/ordinal ledgers."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as st
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
HEAD=bytes.fromhex('03017461642ef10d')
PE_SHA='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'

class Failure(Exception): pass

def req(ok,why):
    if not ok: raise Failure(why)

def h(x): return sha256(x).hexdigest()
def j(p): return json.loads(p.read_bytes())
def hist(seq): return {str(k):v for k,v in Counter(seq).items()}

def read_inputs(d):
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if root.drive.upper()=='Z:': raise ValueError('Z: forbidden')
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    read=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    raw={}
    for side,wanted in (('client',31),('server',77)):
        _,b,toc=read(root/f'{side}_db.dat'); meta=d['archives'][side]; es={x['path']:x for x in toc['entries']}
        req(wanted==len(es)==meta['directory_count'] and toc['data_base']==meta['data_base']==34 and h(b)==meta['archive_sha256'],side+' archive')
        for k,v in meta['members'].items():
            e=es.get(f'{side}_db/{k}'); req(bool(e)==v['present']==(k!='table_extra_10.dat'),k+' presence')
            if not e: continue
            start=34+e['offset']; end=start+e['packed_size']
            bound=min((34+t['offset'] for t in es.values() if 34+t['offset']>start),default=toc['toc_offset'])
            req(v['bounds']==[start,end,bound] and start<end<=bound,k+' bounds')
            req(v['entry']=={**e,'sha256':h(b[start:end])},k+' entry SHA')
            frames=[]; picked=[]
            for _ in range(len(v['frames'])):
                req(b[start:start+4]==b'\x28\xb5\x2f\xfd',k+' magic')
                dec=z.ZstdDecompressor().decompressobj(); payload=dec.decompress(b[start:end]); used=end-start-len(dec.unused_data)
                req(dec.eof and used>0,k+' frame EOF'); f=[start,used,len(payload)]; frames.append(f); start+=used
                if len(payload)==e['size']: picked.append((f,payload))
            req(start==end and frames==v['frames'] and len(picked)==1,k+' frame coverage')
            f,payload=picked[0]
            req(f==v['frame'] and h(payload)==v['payload_sha256'] and len(payload)==v['payload_size'] and payload.startswith(HEAD) and st.unpack_from('<I',payload,8)[0]==v['header_count'],k+' payload')
            raw[side,k]=payload
    b=(root/'basic_people_db.dat').read_bytes(); q=z.ZstdDecompressor().decompressobj(); people=q.decompress(b[8:])
    req(b[:8]==HEAD and q.eof and not q.unused_data and h(b[8:])==d['targets']['person']['compressed_sha256'],'person source')
    return raw,people

COLS={'Nntp':(1,9,True),'Nctp':(1,8,True),'Nrtp':(1,8,True),'NTRv':(1,4,False),'NWGv':(1,4,False),
      'NSps':(1,4,False),'Nfmp':(2,9,True),'NCro':(4,9,True)}


def decode(blob,full):
    """Independent grouped span interpreter; no identity search or builder trace as input."""
    req(blob.startswith(HEAD) and len(blob)>=13,'header')
    ptr=13; num_rows=st.unpack_from('<I',blob,8)[0]; rows=[]; seen=set(); ordinal=-1
    def fail(kind,at,value): raise Failure((ordinal,kind,at,value))
    def skip(n):
        nonlocal ptr
        p=ptr;ptr+=n
        if ptr>len(blob): fail('short transfer',p,n)
        return blob[p:ptr]
    def val(n,s=False): return int.from_bytes(skip(n),'little',signed=s)
    def count(n,each,s=True):
        at=ptr; k=val(n,s)
        if k<0 or k*each>len(blob)-ptr: fail('invalid count',at,k)
        return k
    def vec(w,s,sign=True): skip(count(w,s,sign)*s)
    def col(k,gate=None,tag=None):
        width,stride,sign=COLS[k]; at=ptr; q=count(width,stride,sign); start=ptr
        skip(stride*q)
        dst[k]=dict(count_at=at,count=q,start=start,end=ptr,gate=gate,tag=tag)
    for ordinal in range(num_rows):
        s=ptr; dst={}; sel=val(1)
        if sel: fail('selector outside confirmed domain',s,sel)
        if full:
            skip(14); vec(4,8); skip(32)
            for item_min in (6,2):
                at=ptr; c=count(4,item_min,False)
                if c: fail('typed container not reduced (observed-zero path only)',at,c)
            vec(4,2,False); vec(4,2,False)
            vec(1,4); vec(2,4)
            for _ in range(20): vec(1,4)
            vec(2,4)
            for _ in range(2):
                for _ in range(count(2,36)):
                    tag=val(1)
                    for _ in range(3): vec(4,1,False)
                    skip(13)
                    if tag>=2: skip(4); vec(4,12); skip(5)
                    skip(4)
                    if tag>=5: skip(5)
                    skip(19+sum(tag>=t for t in (3,4,6)))
            at=ptr; on=val(1)
            if on: col('NCro',[at,on],val(1))
            else: dst['NCro']=dict(count_at=None,count=None,start=None,end=None,gate=[at,on],tag=None)
            col('Nfmp')
            for w,z in ((4,18),(4,18),(2,14),(4,10)): vec(w,z)
            skip(5)
            if val(1):
                skip(4)
                for _ in range(count(4,10)):
                    tag=val(2,True); skip(10 if tag>=3 else 9 if tag>=2 else 8)
        skip(31)
        for k in ('Nntp','Nctp','Nrtp'): col(k)
        skip(8)
        if full:
            skip(37)
            for k in ('NTRv','NWGv','NSps'): col(k)
            skip(27)
        skip(3)
        if full:
            for sg in (False,False,True,True,False): vec(1,4,sg)
            vec(1,16,False); vec(2,28)
        q=ptr; ident=st.unpack('<III',skip(12))
        if ident[0]!=ordinal or ident[1]!=ident[2] or not ident[1] or ident[1] in seen: fail('identity after reader',q,list(ident))
        seen.add(ident[1]); rows.append((s,ptr,q,list(ident),dst))
    if len(blob)-ptr!=9: fail('footer/EOF',ptr,len(blob)-ptr)
    footer=st.unpack_from('<IBI',blob,ptr)
    if footer!=(0,1,max(seen,default=0)): fail('footer disagreement',ptr,list(footer))
    return rows,ptr


def input_domains(raw,people,d):
    ds={}; cls={}
    def identity(b,positions,allow):
        ans={}
        for i,p in enumerate(positions):
            a,u,v=st.unpack_from('<III',b,p); req(a==i and u==v and u and b[p+12] in allow,'target lanes'); ans[a]=u
        req(len(ans)==st.unpack_from('<I',b,8)[0] and len(set(ans.values()))==len(ans),'target uniqueness'); return ans
    def save(k,b,ids):
        meta=d['targets'][k]; req(meta['count']==len(ids) and meta['payload_sha256']==h(b)
            and meta['ordinal_trace_sha256']==h(b''.join(st.pack('<I',v) for v in sorted(ids))),k+' target fingerprints'); ds[k]=ids
    for side,num,w in (('client',5,34),('server',5,48),('client',19,45),('server',19,46),('client',25,127)):
        b=raw[side,f'table_{num}.dat']; req((len(b)-22)%w==0,'target fixed closure')
        save(f'{side}_t{num}',b,identity(b,range(1+w,len(b)-20,w),(0,)))
    prior=j(ROOT/'scratch/t47/out/cursor_nation_tax.json')
    for side in ('client','server'):
        b=raw[side,'table_10.dat']; req(h(b)==prior[side]['payload_sha256'],'t10 provenance')
        save(side+'_t10',b,identity(b,(r['identity_at'] for r in prior[side]['rows']),(0,)))
    t24=j(ROOT/'scratch/t24/out/cursor.json'); b=raw['client','table_3.dat']; req(h(b)==t24['provenance']['payload_sha256'],'t3 provenance')
    ends=[]; body=14
    for f in t24['rows']['shards']:
        for i,a,s,e,*_ in j(ROOT/'scratch/t24/out'/f)['rows']:
            req(body==a and b[a-1]==s and i==len(ends),'t3 frame'); ends.append(e-12); body=e+1
    req(body==len(b)-8,'t3 closure'); save('client_t3',b,identity(b,ends,(0,12)))
    n,flag=st.unpack_from('<IB',people); req((n,flag)==(658011,0),'people header'); q=5; ids={}
    for i in range(n):
        tag,c=st.unpack_from('<BB',people,q); req(tag==17 and 1<=c<=5,'people class')
        q+=(83,83,83,34,22)[c-1]; ordinal,u,v=st.unpack_from('<III',people,q-12)
        req(ordinal==i and u==v and u,'people identity'); ids[ordinal]=u; cls[ordinal]=c
    req(people[q:]==bytes.fromhex('00000000014cbd5477') and hist(cls.values())==d['targets']['person']['class_hist'],'people closure')
    save('person',people,ids)
    return ds,cls


def pe_check(d):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM
    b=(ROOT.parent/'fm24/input/editor.exe').read_bytes(); req(h(b)==PE_SHA==d['editor_sha256'],'PE SHA')
    pe=pefile.PE(data=b,fast_load=True); pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    rva=pe.get_rva_from_offset; off=pe.get_offset_from_rva
    cs=Cs(CS_ARCH_X86,CS_MODE_64); cs.detail=True
    def one(p): return next(cs.disasm(b[p:p+15],base+rva(p),count=1))
    table={}
    for f in sorted(HERE.glob('instructions.part*.json')):
        for r in j(f):
            p=r['file_offset']; i=one(p); req(p not in table and i.address==r['VA'] and i.bytes.hex()==r['bytes']
                and (i.mnemonic+' '+i.op_str).rstrip()==r['instruction'],f'instruction @{p:x}')
            if 'direct_target' in r: req(off(i.operands[0].imm-base)==r['direct_target'],f'edge @{p:x}')
            table[p]=r
    factory=d['factory_9']
    for k in ('factory_rel32','case','td','col','col_ptr','slot2','slot19'):
        v=factory[k]; p=v['file_offset']; x=bytes.fromhex(v['bytes']); req(b[p:p+len(x)]==x and base+rva(p)==v['VA'],'factory '+k)
    tab=0xf49d38; req(off(rva(tab)+st.unpack_from('<i',b,tab+9*4)[0])==0xf48f12 and off(st.unpack_from('<Q',b,off(factory['vtable_VA']-base)+19*8)[0]-base)==0x105cb10,'factory/vptr entry')
    by_rva={x.struct.BeginAddress:x.struct.EndAddress for x in pe.DIRECTORY_ENTRY_EXCEPTION}
    for key in ('17156880','18681136'):
        rep=d['extents'][key]; start=int(key); end=off(by_rva[rva(start)]); seen=set(); outside=set(); pending=deque([start])
        while pending:
            p=pending.popleft()
            if p in seen: continue
            seen.add(p); i=one(p); req(p in table,'CFG recorded')
            q=p+i.size; jump=i.mnemonic.startswith('j'); successors=[]
            if jump and i.operands[0].type==X86_OP_IMM: successors.append(off(i.operands[0].imm-base))
            if not (i.mnemonic in ('jmp','int3','ud2') or i.mnemonic.startswith('ret')): successors.append(q)
            for t in successors:
                if start<=t<end: pending.append(t)
                else: outside.add((p,t))
        req(end==rep['end_exclusive'] and len(seen)==rep['reachable'] and not outside and rep['external_edges']==[],key+' CFG')
    branches=[x for p in HERE.glob('branches.part*.json') for x in j(p)]
    for x in branches:
        i=one(x['site']); req(i.mnemonic.startswith('j') and i.mnemonic!='jmp' and x['fallthrough']==x['site']+i.size and x['taken']==table[x['site']].get('direct_target'),'branch graph')
        if x['predicate'] is not None: req(table[x['predicate']]['instruction']==x['predicate_instruction'],'predicate')
    req(hist(x['classification'] for x in branches)==d['branch_census'],'branch census')
    return table,one


def fields(rows_by_side,raw,d,ds,classes,static):
    manifest={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']}
    for p,x in d['provenance'].items():
        req(h((ROOT/p).read_bytes())==x and (not p.startswith('evidence/') or manifest[p]==x),p+' SHA')
    frozen=j(ROOT/MASTER); scope=frozen['entities']['nation.xml'][0]['fields']; table,ins=static; total=Counter()
    accepted={'Nntp':{'nati','mina','maxa'},'Nctp':{'cont','rati','mina','maxa'},'Nrtp':{'regi','rati','mina','maxa'},
        'NTRv':{'valu'},'NWGv':{'valu'},'NSps':{'valu'},'Nfmp':{'pers','perm','rtng'},'NCro':set()}
    key_for={'cont':'t5','nati':'t10','regi':'t19','pers':'person','comp':'t25'}
    for k in COLS:
        f=j(HERE/f'fields_{k}.json'); stride=COLS[k][1]; req(f['item_stride']==stride and f['L4']==0 and f['L3']==len(accepted[k]),k+' ledger')
        items={}
        for side,rs in rows_by_side.items():
            data=raw[side,'table_9.dat']; xs=[]; counts=[]; bypass=0; gated=0; ap=sha256()
            for i,(_,_,q,_,cols) in enumerate(rs):
                if k not in cols: bypass+=1; continue
                c=cols[k]; n=c['count']
                if n is None: gated+=1; continue
                counts.append(n); s=c['start']; e=c['end']; req(e<=q and e-s==stride*n,k+' item EOF')
                for a in range(s,e,stride): xs.append((i,(a-s)//stride,a,data[a:a+stride]))
                ap.update(data[s:e])
            m=f['archives'][side]
            req(m['wire_items']==(None if bypass==len(rs) else len(xs)) and m['mode_bypass_rows']==bypass and m['absent_gate_rows']==gated and m['count_hist']==hist(counts)
                and m['count_sites_visited']==len(counts) and m['item_sequence_sha256']==(ap.hexdigest() if counts else None),k+' count profile')
            items[side]=xs
        if k in ('Nntp','Nctp','Nrtp'): req([x[3] for x in items['client']]==[x[3] for x in items['server']],k+' shared data')
        if k=='Nfmp': req(sum(int.from_bytes(x[3][:4],'little',signed=True)!=0 for x in items['server'])==f['archives']['server']['append_count_after_nonzero_guard'],'Nfmp guard')
        for name,a in f['fields'].items():
            parent=scope[a['schema_index']]; occ=[x for x in parent['list_item_fields'] if x['field']==name]
            req(parent['field']==k and occ==[a['schema']] and a['scoped_occurrences']==1,k+name+' frozen scope')
            cmp=ins(a['getter_compare']); load=ins(a['getter_object_load']); req(cmp.mnemonic=='cmp' and cmp.operands[1].imm==int.from_bytes(name.encode(),'big') and load.operands[1].mem.disp==a['getter_object_offset'],k+name+' getter')
            grade='L3' if name in accepted[k] else 'held'; total[grade]+=1
            off=a['static_item_offset']; width=a['width']; sink=a['wire_sink']
            req(a['grade']==grade and a['accepted_item_offset']==(off if grade=='L3' else None) and (sink in table if off is not None else name=='repu' and sink is None),k+name+' grade/sink')
            if sink: req(ins(sink).mnemonic=='call' and '+ 0x28]' in ins(sink).op_str,k+name+' stream transfer')
            enum=frozen['enums'].get(occ[0].get('enum_ref',name),{}) if occ[0]['type']=='enum' else {}
            enum_values={int(x['enum_id'] or x['enum']) for x in enum.get('values',[])}
            req(a['enum_probe_values']==sorted(enum_values) and a['enum_probe_source']==enum.get('file'),k+name+' enum probe')
            for side,xs in items.items():
                p=a['profile'][side]; vals=[]; raw_vals=[]; first=None; invalid=None; join=p.get('join'); hits=misses=nulls=uid=0; cm=Counter(); uid_miss=miss=sent=None
                t=key_for.get(name); keys=ds.get(t if t=='person' else side+'_'+str(t),{}); uids=set(keys.values()) if t and xs else set()
                for r,i,s,b in xs:
                    raw_v=st.unpack_from('<'+a['encoding'],b,off)[0] if off is not None else i
                    v=(raw_v>>3)&1 if name=='perm' else raw_v&7 if name=='side' else raw_v
                    raw_vals.append(raw_v); vals.append(v)
                    w=dict(row=r,item=i,absolute=s+off if off is not None else None,raw=b[off:off+width].hex() if off is not None else None,raw_value=raw_v,value=v)
                    first=first or w
                    if (a['bounds'] and not a['bounds'][0]<=v<=a['bounds'][1]) or (enum_values and v not in enum_values and (name!='affl' or v!=0)):
                        invalid=invalid or w
                    if t:
                        if v==(0 if t=='person' else -1): nulls+=1; sent=sent or w; continue
                        if v in keys:
                            hits+=1
                            if t=='person': cm[classes[v]]+=1
                        else: misses+=1; miss=miss or w
                        if v in uids: uid+=1
                        else: uid_miss=uid_miss or w
                req(p['total']==len(vals) and p['distinct']==len(set(vals)) and p['zeros']==vals.count(0) and p['range']==([min(vals),max(vals)] if vals else None)
                    and p['top']==[list(v) for v in Counter(vals).most_common(12)] and p['first']==first and p['first_domain_failure']==invalid,(k,name,side,'numeric profile',p['range'],p['top'],Counter(vals).most_common(12),p['first'],first,invalid))
                if join: req((hits,misses,nulls,uid,miss,sent,uid_miss,hist(cm.elements()))==(join['ordinal_hits'],join['ordinal_misses'],join['sentinels'],join['wrong_UID_hits'],join['first_miss'],join['first_sentinel'],join['first_wrong_UID_miss'],join['classes']),k+name+' ordinal join')
                if name=='affl':
                    q=p['ordinal_alias_negative']; req(q['hits']==sum(v!=0 and v in ds['client_t3'] for v in vals) and q['hits']+q['misses']==len(vals)-vals.count(0),'affl diagnostic')
    req(total=={'L3':d['L3'],'held':d['held']} and d['L4']==0,'grade totals')


def verify():
    d=j(HERE/'discovery_t9_wire.json'); raw,people=read_inputs(d); ds,classes=input_domains(raw,people,d)
    static=pe_check(d); by_side={}
    for side,mode in (('client',0),('server',1)):
        for k in ('table_9.dat','table_extra_9.dat'):
            b=raw[side,k]
            for m in (0,1):
                trial=d['trials'][side][k][str(m)]
                try: rows,p=decode(b,m)
                except Failure as e:
                    row,kind,at,val=e.args[0]; fail=trial['first_failure']
                    req(not trial['closed'] and (row,kind,at,val)==(fail['row'],fail['kind'],fail['absolute'],fail['value']) and b[at:at+8].hex()==fail['raw'],(side,k,m,'first rejected mode',(row,kind,at,val),fail)); continue
                req(trial['closed'] and k=='table_9.dat' and mode==m,'unique archive mode')
                by_side[side]=rows; c=j(HERE/f'cursor_t9_{side}.json'); req(c['mode']==m and c['payload_sha256']==h(b) and c['row_count']==len(rows)==251,'bound cursor')
                req(c['row_sum']==p-13 and len(b)==13+c['row_sum']+9==14+c['row_sum']+8 and c['footer']['raw']==b[p:].hex() and c['footer']['absolute']==p,'arithmetic closure')
                req(c['row_len_hist']==hist(e-s for s,e,*_ in rows) and c['selector_hist']==hist(b[s] for s,*_ in rows),'whole table profile')
                for (s,e,q,ident,cols),r in zip(rows,c['rows'],strict=True):
                    req((s,s+1,e,q,ident,cols)==(r['wire13'],r['legacy14'],r['end'],r['identity_at'],r['identity'],r['collections'])
                        and h(b[s:e])==r['wire_sha256'] and h(b[s+1:e+1])==r['legacy_sha256'],'row boundaries')
                    a=s
                    for site,at,w,n in r['trace']:
                        req(a==at and w*n>=0 and site in static[0] and a+w*n<=e,'trace tiling / PE witness'); a+=w*n
                    req(a==e,'trace EOF')
    req([x[3] for x in by_side['client']]==[x[3] for x in by_side['server']],'dual identity')
    req(d['binding']['table_extra_9.dat']['reader'] is None and d['binding']['table_extra_9.dat']['mode'] is None,'sidecar no positive binding')
    p=d['controls']; b=raw['server','table_9.dat']
    for name,rep in [('NTRv_count_1_inserted',b'\1'+st.pack('<i',123)),('NCro_presence_1_inserted',b'\1\1'+st.pack('<iBii',1,1,0,100))]:
        q=p[name]; a=q['absolute']; rr,end=decode(b[:a]+rep+b[a+1:],1); req(end==q['footer_at'] and rr[0][4][name.split('_')[0]]['count']==1,name)
    a=p['Nfmp_zero_lane']['absolute']; rr2,e2=decode(b[:a]+b'\0'*4+b[a+4:],1); req(rr2==by_side['server'] and e2==len(b)-9,'Nfmp zero width')
    fields(by_side,raw,d,ds,classes,static)
    print(f't49 verify PASS: 251+251; six rejected member/mode attempts; L3={d["L3"]}, held={d["held"]}, L4=0; sidecar reader open')


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--selftest',action='store_true'); args=parser.parse_args()
    try:
        if args.selftest:
            x=HEAD+st.pack('<IBIBI',0,0,0,1,0)
            req(decode(x,0)==decode(x,1)==([],13),'empty shell'); print('t49 verify selftest PASS')
        else: verify()
        return 0
    except Failure as e: print('CHECK:',e,file=sys.stderr); return 1
    except Exception as e: print('FATAL:',type(e).__name__,e,file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
