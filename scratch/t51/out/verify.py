#!/usr/bin/env python3
"""Independent t51 verification: original PE, E80 inputs, cursors, joins, holds."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import runpy
import struct as st
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MASTER='evidence/fm24/reports/editor_schema/master.json'
T47='scratch/t47/out/discovery_nation_unknown.json'
T37='scratch/t37/out/nation_subtable_inventory.json'
HEAD=bytes.fromhex('03017461642ef10d')
PE_SHA='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
SCOPE={'Nrvn':216,'Calt':235,'TCrs':64,'Nftb':234,'EDfx':342,'EDsc':344}

class Invalid(Exception): pass

def req(ok,msg):
    if not ok: raise Invalid(msg)

def H(b): return sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def from_out(p): return load(HERE/p)
def at(b,p,fmt): return st.unpack_from('<'+fmt,b,p)


def inputs(d):
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data');req(root.drive.upper()!='Z:','Z: forbidden')
    root=root.resolve();req(root.drive.upper()!='Z:','Z: forbidden')
    read=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    raw={}
    for side,num in [('client',31),('server',77)]:
        _,b,toc=read(root/f'{side}_db.dat'); es={e['path']:e for e in toc['entries']}; md=d['archives'][side]
        req(toc['data_base']==md['data_base']==34 and H(b)==md['archive_sha256'] and sorted(es)==md['directory_paths'] and len(es)==num==md['directory_count'],side+' directory')
        keys={'table_9.dat','table_extra_9.dat','table_extra_10.dat','table_10.dat'}
        if side=='client': keys|={'table_3.dat','table_21.dat','table_25.dat'}
        req(set(md['members'])==keys,'member audit coverage')
        for name in keys:
            doc=md['members'][name]; e=es.get(f'{side}_db/{name}'); req(bool(e)==doc['present']==(name!='table_extra_10.dat'),name+' presence')
            if e is None: continue
            a=34+e['offset']; hi=a+e['packed_size']; nxt=min((34+q['offset'] for q in es.values() if q['offset']>e['offset']),default=toc['toc_offset'])
            req(doc['bounds']==[a,hi,nxt] and a<hi<=nxt and doc['entry']=={**e,'sha256':H(b[a:hi])},name+' compressed frame bounds/hash')
            frames=[]; matches=[]; p=a
            while p<hi:
                req(b[p:p+4]==bytes.fromhex('28b52ffd'),name+' magic')
                dz=z.ZstdDecompressor().decompressobj(); data=dz.decompress(b[p:hi]); q=hi-len(dz.unused_data)
                req(dz.eof and q>p,name+' zstd EOF and progress')
                f=[p,q-p,len(data)];frames.append(f); p=q
                if len(data)==e['size']: matches.append((f,data))
            req(frames==doc['frames'] and len(matches)==1 and p==hi,name+' frame choice')
            (frame,data),=matches
            req(frame==doc['selected_frame'] and H(data)==doc['payload_sha256'] and data.startswith(HEAD) and at(data,8,'I')[0]==doc['count'],name+' payload')
            raw[side,name]=data
    src=(root/'basic_people_db.dat').read_bytes(); dz=z.ZstdDecompressor().decompressobj(); people=dz.decompress(src[8:])
    req(src[:8]==HEAD and dz.eof and not dz.unused_data and H(src[8:])==d['targets']['person']['compressed_sha256'],'people input')
    return raw,people


def pe(d):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM,X86_REG_RIP
    b=(ROOT.parent/'fm24/input/editor.exe').read_bytes();req(H(b)==PE_SHA==d['source']['editor_sha256'],'editor SHA')
    image=pefile.PE(data=b,fast_load=True); image.parse_data_directories(directories=[3]);base=image.OPTIONAL_HEADER.ImageBase
    def off(va):
        try: return image.get_offset_from_rva(va-base)
        except pefile.PEFormatError: return None
    def va(a): return base+image.get_rva_from_offset(a)
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    def ins(o): return next(md.disasm(b[o:o+15],va(o),1))
    def dest(i): return off(i.operands[0].imm) if i.operands and i.operands[0].type==X86_OP_IMM else None
    chunks={}
    for f in sorted(HERE.glob('instructions.part*.json')):
        for x in load(f):
            o=x['file_offset'];i=ins(o);req(o not in chunks and x['VA']==va(o) and x['bytes']==i.bytes.hex(),('ins bytes',o))
            req(x['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),('mnemonic',o))
            if (i.mnemonic=='call' or i.mnemonic.startswith('j')) and i.operands[0].type==X86_OP_IMM:
                req('direct_target' in x and x['direct_target']==dest(i),('direct edge',o))
            rip=[i.address+i.size+op.mem.disp for op in i.operands if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP]
            req(x.get('rip_targets_VA',[])==rip,('RIP xref',o));chunks[o]=x
    def runtime_walk(o,n):
        stride=va(o)-o; todo=deque([o]); seen=set(); edges=set()
        while todo:
            p=todo.popleft()
            if p in seen: continue
            i=ins(p); seen.add(p); m=i.mnemonic; q=p+i.size
            if m=='jmp': succ=[('tail_jump',i.operands[0].imm-stride)] if i.operands[0].type==X86_OP_IMM else []
            elif m.startswith('j'): succ=[('branch',i.operands[0].imm-stride),('fallthrough',q)]
            elif m not in ('ret','retf','iret','iretq','int3','ud2'): succ=[('fallthrough_out_of_bound',q)]
            else:succ=[]
            for kind,y in succ:
                if o<=y<n: todo.append(y)
                else: edges.add((p,kind,y+stride))
        return seen,edges
    extents={image.get_offset_from_rva(x.struct.BeginAddress):image.get_offset_from_rva(x.struct.EndAddress) for x in image.DIRECTORY_ENTRY_EXCEPTION}
    for k,dump in d['extents'].items():
        p=int(k); end=extents[p];req(end==dump['end_exclusive'] and dump['entry']==p,'runtime bound');s,e=runtime_walk(p,end)
        req(len(s)==dump['reachable'] and e=={(int(x['from'],16),x['kind'],int(x['target_va'],16)) for x in dump['external_edges']},('independent worklist',k))
    def blob(x):
        o=x['file_offset'];data=bytes.fromhex(x['bytes']);req(x['VA']==va(o) and data==b[o:o+len(data)],('PE data',o));return data
    for k,v in d['pe_data'].items():
        data=blob(v)
        if 'table' in v: req(off(va(v['table'])+at(data,0,'i')[0])==v['dest'] and v['dest_VA']==va(v['dest']),k+' rel32')
        if k.endswith('slot3'): req(off(at(data,0,'Q')[0])==v['dest'],k+' vptr')
    for k,f in d['factory'].items():
        t=int(k)
        for key in ('td','col','col_ptr','slot2','slot19','factory_rel32'): blob(f[key])
        req(off(at(b,off(f['vtable_VA'])+19*8,'Q')[0])==f['reader'],k+' slot19')
        req(f['rtti'].encode()+b'\0' in blob(f['td']),k+' RTTI')
    for k,obj in d['parents'].items():
        scans={x:[m.start() for m in re.finditer(re.escape(v),b)] for x,v in [('as_written',k.encode()),('reversed_le',k.encode()[::-1])]}
        req(scans==obj['immediate_scan'] and all(o in chunks for o in obj['t47_verbatim']['sites']),k+' t47/scan')
    expected={0x1043322:0x1065ef0,0x10685e1:0x11f0690,0x11f21b5:0x11ff710,0x10675f0:0x106ad10,
              0x105ef12:0x11d0d30,0x11d2aa9:0x1105860,0x1050e7d:0x15d07b0,0x4492a35:0x104b6f0,
              0x10401dd:0x15cf370,0x3d78818:0x10728c0,0x11d4bfe:0x155b450,0x4387b46:0x155c120,
              0x3bb97ec:0x11d3200,0x29c80:0x907f0,0xf51671:0xf55120,0x3bb9698:0xffa3b0,0xffa3b0:0x3cefbe0,
              0x3bb96d6:0x7d0570}
    req(all(chunks[o]['direct_target']==v for o,v in expected.items()),'route anchor chain')
    pref=at(ins(0x3cefca4).bytes,2,'Q')[0].to_bytes(8,'little')+ins(0x3cefcb2).bytes[-4:]
    req(pref==b'table_extra_' and blob(d['pe_data']['named_aux_generic_suffix'])==b'.dat\0','auxiliary filename family')
    req(chunks[0x29c37]['instruction']=='cmp esi, 0x45446678' and chunks[0x29c69]['instruction']=='cmp eax, 0xa' and 0x29c37 in runtime_walk(0x28150,extents[0x28150])[0],'EDfx reachable type gate')
    req(all(o in chunks for o in (0x3ecc093,0x11d1ca7,0x11f3e54,0x11d4bad,0x105dd56,0x104012c,0x448f996,0x11d1b15,0x3eba3e8)), 'collection sinks')
    kinds=Counter()
    for f in HERE.glob('branches.part*.json'):
        for x in load(f):
            p=x['site']; i=ins(p); kinds[x['classification']]+=1
            req(i.mnemonic.startswith('j') and i.mnemonic!='jmp' and dest(i)==x['taken'] and p+i.size==x['fallthrough'],'branch edge')
            req(chunks[x['predicate']]['instruction']==x['predicate_instruction'] and x['first_counterexample'],'branch predicate/negative')
            if x['classification']=='dead': req(p==0x3eba542 and chunks[p-4]['instruction']=='xor eax, eax','dead contradiction')
    req(set(kinds)=={'wire_data','runtime-external','IO-result','context-lifecycle','dead'},'five classes')
    return ins,chunks


def ftb(b,p,n,end):
    items=[]
    for j in range(n):
        origin=p; tag=b[p];p+=1; strings=[]
        for _ in range(4):
            q=p; length=at(b,p,'I')[0]; p+=4+length
            req(p<=end,('string crosses bound',q,length)); s=b[q+4:p]; strings.append([q,length,s.hex(),s.decode('UTF-8')])
        req(p+20<=end,'ftb trailer in bounds'); d,y=at(b,p,'HH'); ds={'absolute':p,'raw_le16':[d,y],'packed':(y*131072)+((d%512)*256)+(d//512)}
        lanes=[[p+4+4*i,v] for i,v in enumerate(at(b,p+4,'iiii'))]; p+=20
        items.append(dict(item=j,absolute=origin,end=p,length=p-origin,tag=tag,strings=strings,date=ds,lanes=lanes,raw=b[origin:p].hex()))
    return p,items


def cursors(raw,d):
    targets={k:[] for k in ('Nrvn','Nftb')}; ids={}; gates=[]
    tax=load(ROOT/'scratch/t47/out/cursor_nation_tax.json'); controls=d['controls']
    for side in ('client','server'):
        for k in (9,10):
            name=f'table_{k}.dat'; state=from_out(f'cursor_table_{k}_{side}.json'); b=raw[side,name]; full=(side=='server')
            prior=load(ROOT/f'scratch/t49/out/cursor_t9_{side}.json') if k==9 else tax[side]
            req(state['member']==name and state['side']==side and state['mode']==prior['mode']==int(full),'mode binding')
            req(state['payload_sha256']==H(b)==prior['payload_sha256'] and state['payload_size']==len(b) and len(prior['rows'])==len(state['rows'])==at(b,8,'I')[0]==state['count']==251,'row provenance')
            req((state['wire_header'],state['legacy_header'],state['wire_footer'],state['legacy_footer'])==(13,14,9,8),'coordinate bases')
            p=13; results={}
            for ordinal,(x,r) in enumerate(zip(state['rows'],prior['rows'])):
                ia=r['identity_at'];end=r['end']
                req(x['row']==ordinal==r['row'] and p==x['wire13']==r['wire13'] and p+1==x['legacy14']==r['legacy14'] and b[p]==x['selector']==0,'selector/row start')
                req(x['end']==end==ia+12 and x['identity_at']==ia and x['length']==end-p and x['wire_sha256']==H(b[p:end])==r['wire_sha256'] and x['legacy_sha256']==H(b[p+1:end+1])==r['legacy_sha256'],'wire/legacy row')
                if k==10:
                    if full:
                        n=at(b,p+5,'h')[0]; q=p+7+4*n; m=at(b,q,'i')[0]; q+=4+4*m; z=at(b,q,'h')[0]
                        req(n>=0 and m>=0 and z>=0 and q+2<=ia,'ftb count input')
                        e,it=ftb(b,q+2,z,ia);req(e+24==r['tax'][0],'ftb cursor closure at next transfer span')
                        req(x['Nftb']==dict(count_at=q,count=z,start=q+2,items=it,end=e),'ftb projected cursor')
                        targets['Nftb'] += [(ordinal,a) for a in it]
                    else:req(x['Nftb'] is None,'client ftb bypass')
                elif full:
                    tx={o:(a,w,c) for o,a,w,c in r['trace']}; q=tx[0x11d1b03][0]; n=b[q]; s=q+1
                    e=s+n*16; cn=at(b,e,'h')[0]; endca=e+2+cn*28
                    req(e==tx[0x11d1bf2][0] and endca==ia and cn==0,'Calt count/EOF')
                    req(x['Calt']==dict(count_at=e,count=cn,start=e+2,end=endca,stride=28),'Calt real zero witness')
                    its=[]
                    for j,ip in enumerate(range(s,e,16)):
                        lane,a0,a1,typ,tag,level,*_=at(b,ip,'q4Bb3B');req(typ==2 and tag==6 and lane==at(b,ip,'i')[0],'rival tag, target and high bits')
                        its.append(dict(item=j,absolute=ip,raw=b[ip:ip+16].hex(),ordinal_i32=lane,raw_qword=lane,target_type=typ,tag=tag,leve=level))
                    req(x['Nrvn']==dict(count_at=q,count=n,start=s,end=e,items=its),'rival target section');targets['Nrvn'] += [(ordinal,a) for a in its]
                    g=tx[0x105dd07][0]; after=tx[0x105dd87][0];gates.append(dict(row=ordinal,absolute=g,presence=b[g],bytes_after_gate=after-g-1))
                else:req(x['Nrvn'] is None and x['Calt'] is None,'client t9 bypass')
                a,uid,v=at(b,ia,'III');req(a==ordinal and uid==v!=0 and [a,uid,v]==x['identity']==r['identity'],'consume identity after target');results[a]=uid; p=end
            footer=at(b,p,'IBI'); req(len(set(results.values()))==251 and footer==(0,1,max(results.values())) and list(footer)==state['footer'] and len(b)==p+9 and p==state['footer_at'] and state['row_sum']==p-13 and b[p:].hex()==state['footer_hex'],'footer, ordinal and EOF')
            ids[side,k]=results
    for k in (9,10):req(ids['client',k]==ids['server',k],'parallel identities')
    req(gates==d['parents']['TCrs']['new_evidence']['main_t9_presence_gates'] and Counter(g['presence'] for g in gates)=={0:166,1:85},'TCrs other displacement gate coverage')
    req(len(targets['Nrvn'])==720 and len(targets['Nftb'])==7,'item coverage')
    req(controls['Nrvn_short']==['short transfer',1017,16,1032] and controls['Nftb_short']==['short transfer',278816,5,278816],'short transfer controls')
    return ids,targets


def domains(raw,people,ids,d):
    dt={side+'_nation':ids[side,10] for side in ('client','server')}
    def tails(b,positions):
        ans={}
        for i,p in enumerate(positions):
            j,v,w=at(b,p,'III');req(i==j and v==w!=0,('target identity',i,p));ans[i]=v
        req(len(ans)==len(set(ans.values())),'target UID uniqueness');return ans
    payload={s+'_nation':raw[s,'table_10.dat'] for s in ('client','server')}
    for k,tid,w in [('client_stadium',21,38),('client_competition',25,127)]:
        b=raw['client',f'table_{tid}.dat'];n=at(b,8,'I')[0];req(len(b)==22+n*w,k+' fixed outcome')
        dt[k]=tails(b,range(1+w,len(b)-9,w));payload[k]=b
    b=raw['client','table_3.dat']; cl=load(ROOT/'scratch/t24/out/cursor.json');req(cl['provenance']['payload_sha256']==H(b),'client club source')
    pos=[r[3]-12 for f in cl['rows']['shards'] for r in load(ROOT/'scratch/t24/out'/f)['rows']];dt['client_club']=tails(b,pos);payload['client_club']=b
    n,flag=at(people,0,'IB');req((n,flag)==(658011,0),'people header');end=5;pos=[]
    for i in range(n):
        k,c=at(people,end,'BB');req(k==17 and 1<=c<=5,'people selector/class'); end+={1:83,2:83,3:83,4:34,5:22}[c];pos.append(end-12)
    req(people[end:]==bytes.fromhex('00000000014cbd5477'),'people EOF');dt['person']=tails(people,pos);payload['person']=people
    for k,doc in d['targets'].items():
        m=dt[k];req(len(m)==doc['count'] and H(payload[k])==doc['payload_sha256'] and H(b''.join(st.pack('<II',p,m[p]) for p in sorted(m)))==doc['ordinal_uid_sha256'],k+' actual target rows')
    return dt


def fields(d,targets,ds,master,ins,chunks):
    def verify_join(ds,vals,j):
        uid={u:a for a,u in ds.items()}; ok_a=ok_u=null=0; first=None; miss_a=None; miss_u=None
        for row,item,p,v in vals:
            if v==-1:null+=1;continue
            t=dict(row=row,item=item,absolute=p,value=v,raw_i32_le=st.pack('<i',v).hex(),ordinal_target_uid=ds.get(v),uid_target_ordinal=uid.get(v));first=first or t
            if v in ds:ok_a+=1
            else:miss_a=miss_a or t
            if v in uid:ok_u+=1
            else:miss_u=miss_u or t
        req(j==dict(live=len(vals)-null,null=null,ordinal_matches=ok_a,uid_matches=ok_u,first_ordinal_miss=miss_a,first_uid_miss=miss_u,first_live=first),'reference full census')
    levels={}; rv=targets['Nrvn']; ff=targets['Nftb']
    official={'Nrvn':{'nati','leve'},'Nftb':{'NpFn','NpSn','NbPd','NbCn'},'Calt':set()}
    for k,l3 in official.items():
        f=from_out('fields_'+k+'.json'); got=f['fields']; fxml=master[SCOPE[k]]['list_item_fields'];req(set(got)=={x['field'] for x in fxml},'schema scope')
        req({key for key,g in got.items() if g['status']=='L3'}==l3 and f['L3']==len(l3) and f['L4']==0,'L3 scope')
        for key,g in got.items():
            match=[x for x in fxml if x['field']==key];i=ins(g['compare'])
            req(match==[g['schema']] and g['occurrences']==1 and i.mnemonic=='cmp' and i.operands[1].imm==int.from_bytes(key.encode(),'big'),'schema/exact getter')
            req(g['getter_load'] in chunks and g['reader_sink'] in chunks,'instruction references')
            if g['status']=='held':req('item_offset' not in g and 'row_offset' not in g,'held offset publication')
        if k=='Nrvn':
            verify_join(ds['server_nation'],[(r,a['item'],a['absolute'],a['ordinal_i32']) for r,a in rv],got['nati']['join'])
            req(got['nati']['object_offset']==0 and got['nati']['item_offset']==0 and got['nati']['join']['ordinal_matches']==720,'rival target/offset')
            req(got['leve']['item_offset']==12==got['leve']['object_offset'] and got['leve']['histogram']==dict(Counter(str(a['leve']) for _,a in rv)), 'rival level distribution')
        if k=='Nftb':
            for key,n in [('NpFn',0),('NpSn',1),('NbCn',3)]:req(got[key]['length_histogram']==dict(Counter(str(a['strings'][n][1]) for _,a in ff)),key+' lengths')
            req(all(a['tag']==1 and a['length']>=37 and 1900<=a['date']['raw_le16'][1]<=2024 and 1<=a['date']['raw_le16'][0]%512<=366 for _,a in ff),'dates and string framing')
            for key,n,target,wanted in [('NbPi',3,'person',2),('NbPn',1,'server_nation',0),('NbFt',0,'client_club',7)]:
                j=got[key]['join'];verify_join(ds[target],[(row,a['item'],*a['lanes'][n]) for row,a in ff],j)
                req(j['ordinal_matches']==wanted and j['uid_matches']==j['live'],key+' identifier encoding counterexample')
                sample=j['first_live'];req(sample['ordinal_target_uid']!=sample['value'] and sample['uid_target_ordinal'] is not None,key+' referent divergence')
        if k=='Calt':req(all(g['observed_items']==0 and g['first_counterexample']['absolute']==1097 for g in got.values()),'empty Calt; no synthetic target join')
        levels[k]=len(l3)
    req(d['L3']==sum(levels.values())==6 and d['L4']==0,'ledger totals')


def verify():
    d=from_out('discovery_unknown2.json'); s47=load(ROOT/T47); t37={x['parent_4cc']:x for x in load(ROOT/T37)['parents']}; master=load(ROOT/MASTER)
    req(set(d['parents'])==set(SCOPE) and d['status']=='partial','scope/status')
    req(H((ROOT/T37).read_bytes()).startswith('8af89c72') and H((ROOT/MASTER).read_bytes()).startswith('7d57477e') and H((ROOT/T47).read_bytes()).startswith('2c0a5b53'),'frozen anchors')
    for f,h in d['source']['unchanged'].items():req(H((ROOT/f).read_bytes())==h,f+' sealed prior')
    man={x['path']:x['sha256'] for x in load(ROOT/'evidence/MANIFEST.json')['files']}
    for p,h in d['source']['snapshots'].items():req(h==man[p]==H((ROOT/p).read_bytes()),p+' MANIFEST')
    xml=master['entities']['nation.xml'][0]['fields']
    expected={'Nrvn':(9,'table_9.dat',0x105cb10),'Calt':(9,'table_9.dat',0x105cb10),'TCrs':(9,None,0x11d3200),'Nftb':(10,'table_10.dat',0x103fac0),'EDfx':(10,None,None),'EDsc':(None,None,None)}
    for k,x in d['parents'].items():
        req(x['t47_verbatim']==s47['parents'][k] and x['t37_verbatim']==t37[k] and x['schema_index']==SCOPE[k] and x['t47_verbatim']['schema']==xml[SCOPE[k]],k+' prior quote/schema')
        req((x['table_type'],x['member'],x['reader'])==expected[k] and x['L4']==0,k+' scope not promoted')
    req(d['parents']['EDsc']['new_evidence']['rule_group_occurrence']==master['field_codes']['EDsc'],'EDsc cross-scope counterexample')
    td=load(ROOT/'scratch/t49/out/discovery_t9_wire.json'); req(d['source']['t9_sidecar_negative']==td['binding']['table_extra_9.dat'] and d['source']['t9_sidecar_trials']=={s:td['trials'][s]['table_extra_9.dat'] for s in ('client','server')}, 't49 original sidecar negatives')
    i,c=pe(d); raw,people=inputs(d); ids,t=cursors(raw,d); ds=domains(raw,people,ids,d);fields(d,t,ds,xml,i,c)
    print('t51 verify PASS: 6 scoped parents, 4 cursor projections, L3=6, L4=0')


def selftest():
    src=b'\1'+st.pack('<4I2H4i',0,0,0,0,39,1974,-1,788,-1,-1); p,x=ftb(src,0,1,len(src))
    req(p==len(src) and x[0]['date']['packed']==(1974<<17)|(39<<8),'selftest date')
    try:ftb(src,0,1,len(src)-1)
    except Invalid:print('t51 verifier selftest PASS');return
    raise Invalid('short input accepted')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');a=p.parse_args()
    try:
        (selftest if a.selftest else verify)();return 0
    except Invalid as x:print(f'check failed: {x}',file=sys.stderr);return 1
    except Exception as x:print(f'fatal: {type(x).__name__}: {x}',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
