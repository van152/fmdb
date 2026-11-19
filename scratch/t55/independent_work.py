#!/usr/bin/env python3
"""Independent t55 verifier: PE worklist, direct archive replay, scoped joins and old fixtures."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import runpy
import struct as S
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MASTER='evidence/fm24/reports/editor_schema/master.json'
IDA='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH='7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
FOOT=bytes.fromhex('0000000001ec7ae404')
READER=0x103fac0
PRIOR='scratch/t47/out/cursor_nation_tax.json'
ABC=(('A','Nlns',0x1040717,0x48,5),('B','Nefr',0x10407b0,0xa8,28),('C','Nnfr',0x104086c,0x90,28),('D','Nagr',0x1040927,0xc0,12))
TARGET={2:(43,43),5:(34,48),19:(45,46),21:(38,181),41:(None,None)}
REF={'Nnsi':21,'Ncti':5,'Nrgi':19,'Ncpi':2,'Ncur':41}
PINS={'scratch/t46/out/REPORT.md':'71fd3df89c852b17e7428dd3d380a8c44fbf52687eadc9b33926917484a1231a',
      'scratch/t46/out/grammar_diff_client_server.json':'b14d5a9deb49d4404aa8c1e236d227769d4840ed8e1466112ecf2e51efe62d97',
      PRIOR:'42b3e88db86c725221a23cd7b2bdd6e3d4c1b089d758ed844a56f84e103f2ea9',
      'reports/t22_nation_capital.json':'72a1054552b767d8b93440beb8c2d41983884757a73dc91f151b05780e6c1c5e',
      'scratch/t01/inbox/t01f/output.json':'ddb26beb24045edd29dd9ddbe769c7ca523bb63cb74cf19fa9afa7541c35c1c0',
      'scratch/t47/out/fields_nation_tax.json':'b7b57595a3b8e4d60458f14f1e923b660e751304fdab1feff7c85b035a4af9b7',
      'scratch/t51/out/fields_Nftb.json':'69f83b15f3143e2305846967d36d6afc340b6626222527a04232fc90da1fa7b0',
      **{f'scratch/t53/out/fields_PUn{k}.json':h for k,h in {
      'I':'b0ecbba661c1633fcd7ce937a26b920cf23d0418301f450f953c24b862702b6e',
      'J':'17124f10abaa07d83c76d097c7bc2dcfeaac7d03bfd176c9599b0a16a3a2dd4f',
      'P':'994e4a11e01e10c7735275dca81fc44beac05d47a5a9bca83f9d782c8d5af37c',
      'T':'589bc4bf61bc2bf26c5d3b160adc7a34a885b6f9601a054bf2a385fc9040ff31'}.items()}}

class Failed(Exception): pass

def require(ok,msg):
    if not ok: raise Failed(msg)

def J(path):return json.loads((ROOT/path).read_bytes())
def out(path):return json.loads((HERE/path).read_bytes())
def digest(blob):return sha256(blob).hexdigest()
def U(b,p):return S.unpack_from('<I',b,p)[0]
def hist(x):return {str(k):v for k,v in Counter(x).items()}


def load_payloads(doc):
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as z
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if root.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    read_directory=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    out={}
    for side,size in (('client',31),('server',77)):
        _, b, toc=read_directory(root/(side+'_db.dat'))
        require(toc['data_base']==34 and len(toc['entries'])==size,'archive directory')
        entries=sorted(toc['entries'],key=lambda x:x['offset']);prefix=side+'_db/table_'
        for tid in (10,*TARGET):
            idx=next(i for i,row in enumerate(entries) if row['path']==f'{prefix}{tid}.dat'); e=entries[idx]
            lo=e['offset']+34; hi=lo+e['packed_size']; bound=entries[idx+1]['offset']+34 if idx+1<len(entries) else toc['toc_offset']
            require(34<=lo<hi<=bound<=len(b),'member bounds')
            remaining=b[lo:hi]; ptr=lo; matches=[]; frames=[]
            while remaining:
                require(remaining[:4]==b'\x28\xb5\x2f\xfd','Zstd frame magic')
                obj=z.ZstdDecompressor().decompressobj(); payload=obj.decompress(remaining); end=hi-len(obj.unused_data)
                require(obj.eof and ptr<end<=hi,'Zstd frame extent')
                frames.append([ptr,end,len(payload)])
                if len(payload)==e['size']:matches.append(payload)
                remaining=obj.unused_data;ptr=end
            require(len(matches)==1,'directory size selector'); raw=matches[0]
            require(doc[side][str(tid)]==dict(start=lo,end=hi,bound=bound,frames=frames,payload_sha256=digest(raw),compressed_sha256=digest(b[lo:hi])),'published archive metadata')
            out[side,tid]=raw
    return out


def pe_check(inv):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    image=(ROOT.parent/'fm24/input/editor.exe').read_bytes(); require(digest(image)==EXEH==inv['editor_sha256'],'editor SHA')
    p=pefile.PE(data=image,fast_load=True);p.parse_data_directories(directories=[3]); base=p.OPTIONAL_HEADER.ImageBase
    f2v=lambda o:p.get_rva_from_offset(o)+base
    v2f=lambda v:p.get_offset_from_rva(v-base)
    m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
    def dec(o): return next(m.disasm(image[o:o+15],f2v(o),1))
    def directed(i):return v2f(i.operands[0].imm)
    def walk(entry):
        rva=f2v(entry)-base; rt=next(x.struct for x in p.DIRECTORY_ENTRY_EXCEPTION if x.struct.BeginAddress==rva)
        end=p.get_offset_from_rva(rt.EndAddress); accesses={}; outedges=[]; pending=deque([entry])
        while pending:
            a=pending.popleft()
            if a in accesses:continue
            i=dec(a); k=i.mnemonic; fall=a+i.size
            if k=='jmp': edges=[directed(i)] if i.operands[0].type==2 else []
            elif k.startswith('j'): edges=[directed(i),fall]
            elif k in ('ret','retf','int3','ud2'): edges=[]
            else:edges=[fall]
            keep=sorted(b for b in edges if entry<=b<end);outedges.extend(b for b in edges if b not in keep)
            accesses[a]=(i,keep);pending.extend(keep)
        return end,accesses,outedges
    vt=inv['vtable_VA'];require(vt==0x1418893b8 and inv['reader']==READER,'class entry')
    v=v2f(vt); require(v2f(S.unpack_from('<Q',image,v+152)[0])==READER and v2f(S.unpack_from('<Q',image,v+16)[0])==0x1041f30 and directed(dec(0x1041f33))==0x1041f40,'vslots')
    end,cfg,ext=walk(READER);require((end,len(cfg),ext)==(0x1040be4,992,[]),'independent PE extent and CFG')
    require(inv['extents'][str(READER)]==dict(entry=READER,end_exclusive=end,reachable=992,external_edges=[],full_instruction_shards=True),'declared CFG')
    _,g,_=walk(0x1041f40); ins=[r for path in sorted(HERE.glob('instructions.part*.json')) for r in json.loads(path.read_bytes())]
    shard={r['file_offset']:r for r in ins};require(len(shard)==len(ins),'unique instruction records')
    require({a for a,r in shard.items() if r.get('function')==READER}==set(cfg),'instruction coverage')
    for a,r in shard.items():
        i=dec(a);require(r['VA']==i.address and r['bytes']==i.bytes.hex() and r['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),f'PE instruction @{a:x}')
        if a in cfg:require(r.get('successors')==cfg[a][1],f'CFG successors @{a:x}')
        if 'direct_target' in r:require(r['direct_target']==directed(i),f'PE direct target @{a:x}')
    check_br=[r for path in HERE.glob('branches.part*.json') for r in json.loads(path.read_bytes())]
    bset={a for a,(i,_) in cfg.items() if i.mnemonic.startswith('j') and i.mnemonic!='jmp'}
    require(set(r['site'] for r in check_br)==bset and len(check_br)==len(bset),'branch census')
    notes={r['site']:r for r in check_br}
    for a,r in notes.items():
        i,_=cfg[a];require(r['taken']==directed(i) and r['fallthrough']==a+i.size,'branch edges')
        if r['predicate'] is not None:require(r['predicate'] in cfg and cfg[r['predicate']][0].eflags,'predicate before branch')
    require(directed(dec(0x103fae6))==0x10405b0 and directed(dec(0x10409d3))==0x1040b89,'external mode edges')
    require(all(notes[a]['counterexamples']==J(PRIOR)['wrong_mode_first'] for a in (0x103fae6,0x10409d3)),'original wrong-mode negatives')
    reads={a for a,(i,_) in cfg.items() if i.mnemonic=='call' and i.op_str=='qword ptr [rax + 0x28]'}
    omitted={0x103fcbd,0x103ff79,0x1040529}; helpers={0x3d74e62,0xf2ba0e,0x3c60119}
    require(len(reads)==inv['reader_direct_stream_vcalls']==40 and set(inv['reader_vcalls_inside_opaque_items'])==omitted,'direct streams')
    slots=inv['slots'];actual=[r['site'] for r in slots]; expected=[0xf2ba0e,*sorted(a for a in reads-omitted if a<0x10405b0),0x3d74e62,*sorted(a for a in reads-omitted if a>=0x10405b0),0x3c60119]
    require(actual==expected and len(actual)==inv['slot_count']==40,'ordered outer transfer census')
    require([s['position'] for s in slots]==list(range(40)),'slot numbering')
    for s in slots:
        a=s['site']; i=dec(a);require(a in shard and i.mnemonic=='call' and i.operands[0].type==3 and i.operands[0].mem.disp==0x28,'stream call')
        if a not in helpers:
            nearby=[];q=a
            for _ in range(6):
                preceding=next((o for o,(j,_) in cfg.items() if o+j.size==q),None)
                if preceding is None:break
                q=preceding;nearby.append(q)
            require(any(cfg[q][0].op_str==f'r8d, {s["width"]}' for q in nearby),'transfer width')
        if 'member_instruction' in s:
            k=dec(s['member_instruction']);obj=s['object_displacement'];require(any(op.type==3 and op.mem.disp==obj for op in k.operands),'parent/field displacement')
            if s['role']=='scalar':require(s['member_instruction'] in nearby and k.mnemonic=='lea' and k.reg_name(k.operands[0].reg)=='rdx','scalar sink')
        if s['getter']:
            w=s['getter'];code=s['candidate_4cc']; a=w['compare']; i=g[a][0]; x=a+i.size; j=g[x][0]
            require(i.mnemonic=='cmp' and i.operands[1].imm==int.from_bytes(code.encode(),'big') and j.mnemonic in ('je','jne'),'exact getter key')
            t=directed(j) if j.mnemonic=='je' else x+j.size
            chain=w['arm_instructions'];require(chain[:3]==[a,x,t] and chain[-1]==w['load'] and all(q in shard and q in g for q in chain),'getter chain')
            require(all(n in g[q][1] for q,n in zip(chain,chain[1:])),'getter CFG edges')
            if s['role']=='scalar' or code in ('Ntxr','Nlns'):
                k=dec(w['load']);require(any(op.type==3 and k.reg_name(op.mem.base)=='r12' and op.mem.disp==s['object_displacement']==w['object_displacement'] for op in k.operands),'getter to reader displacement')
    require(dec(0x1043605).op_str=='esi, 9' and dec(0x1043608).op_str=='sil, 1','bool mask')
    require(directed(dec(0x1040592))==0x104e6b0 and directed(dec(0x104e6b0))==0x3d74e30,'helper extent chain')
    require(directed(dec(0x1040bcf))==0xfae340 and directed(dec(0xfae340))==0x3c600f0,'identity thunk')
    return len(cfg),len(bset)


def independent_rows(raw,server,previous):
    p=13; cells=[]; ids={}; string_data=[[],[],[],[]];dates=[[],[]]
    require(raw[:8]==bytes.fromhex('03017461642ef10d') and U(raw,8)==251 and digest(raw)==previous['payload_sha256'],'nation input')
    for row in range(251):
        start=p; cur={}; ref=previous['rows'][row]
        def entry(pos,width,fmt=None,mult=0):
            nonlocal p
            a=p;p+=width
            require(p<=len(raw),'short transfer')
            n=S.unpack_from(fmt,raw,a)[0] if fmt else None
            if n is not None: require(n>=0,'negative collection count');p+=n*mult
            require(p<=len(raw),'short collection')
            fact=dict(row=row,absolute=a,body_offset=a-start-1,end=p,hex=raw[a:a+width].hex())
            if fmt:fact['count']=n
            cur[pos]=fact;return fact
        require(raw[p]==0,'selector');entry(0,1)
        if server:
            entry(1,4);entry(2,2,'<h',4);entry(3,4,'<i',4)
            x=entry(4,2,'<h');a=p
            for it in range(x['count']):
                a+=1
                for k in range(4):
                    length=U(raw,a);string_data[k].append(dict(row=row,item=it,index=k,absolute=a,length=length));a+=4+length
                a+=20
            require(a<=len(raw),'takeover extent');p=x['end']=a
            for pos in range(5,11):entry(pos,4)
            x=entry(11,4,'<i'); require(ref['tax'][:3]==[x['absolute'],x['count'],p],'tax frozen entry');p=x['end']=ref['tax'][3]
            x=entry(12,4,'<I',12)
            for it,a in enumerate(range(x['absolute']+4,p,12)):
                for k in range(2):
                    q=a+4+k*4; w,y=S.unpack_from('<HH',raw,q)
                    dates[k].append(dict(row=row,item=it,absolute=q,hex=raw[q:q+4].hex(),year=y,day=w%512,upper7=w//512,boxed=(y<<17)|((w%512)<<8)|(w//512)))
            entry(13,4,'<I',14)
        for i,w in enumerate((1,4,4,4,4,1,1,4,1),14):entry(i,w)
        for i,(w,fmt,step) in enumerate(((1,'<b',5),(4,'<i',28),(4,'<i',28),(4,'<i',12)),23):entry(i,w,fmt,step)
        if server:
            for i,w in enumerate((4,)*10+(2,1),27):entry(i,w)
        at=p; r,u,v=S.unpack_from('<III',raw,at);entry(39,12)
        require(r==row and u==v!=0 and [r,u,v]==ref['identity'],'nation ID triple'); ids[row]=u
        require((start,p,at)==(ref['wire13'],ref['end'],ref['identity_at']) and digest(raw[start:p])==ref['wire_sha256'] and digest(raw[start+1:p+1])==ref['legacy_sha256'],'nation fixed row/span witness')
        cells.append(cur)
    require(raw[p:]==FOOT and p==previous['footer_at'] and len(set(ids.values()))==251,'country EOF and identity uniqueness')
    return cells,ids,p,string_data,dates


def targets(raw,ledger):
    ids={}
    for (side,t),b in raw.items():
        if t==10:continue
        n=U(b,8); width=TARGET[t][side=='server']; end=13; domain={}
        for i in range(n):
            if width is None:
                require(b[end]==0,'currency selector');end+=1
                for _ in range(4):end=end+4+U(b,end)
                end+=8+7*U(b,end+4)+12
            else:end+=width
            j,u,v,sel=S.unpack_from('<IIIB',b,end-12)
            require(i==j and u==v!=0 and sel==0,'target tail');domain[j]=u
        require(end+9==len(b) and len(set(domain.values()))==n,'target EOF/UIDs')
        require(ledger[f'{side}_t{t}']==dict(rows=n,width=width,payload_sha256=digest(b),identity_offset_from_wire_row_end=-12),'target ledger')
        ids[side,t]=domain
    return ids


def profiles(inv,data):
    for slot in inv['slots']:
        k=slot['position'];w=slot['width']
        for side,(rows,_,_,_,_) in data.items():
            src=[r[k] for r in rows if k in r]; pub=slot['profiles'][side]
            require(slot['coordinates'][side]==[[x['absolute'],x['end']] for x in src] and pub['samples']==len(src),'slot coordinate/samples')
            require(bool(src)==(side=='server' or slot['mode']=='both'),'slot conditional site')
            if not src:continue
            offs=[x['body_offset'] for x in src]; require((pub['first'],pub['body_offset_min'],pub['body_offset_max'])==(src[0],min(offs),max(offs)),'first slot witness')
            if 'count' in src[0]:
                c=[x['count'] for x in src];require(pub['count_hist']==hist(c) and pub['item_total']==sum(c) and pub['first_live']==next((x for x in src if x['count']),None),'collection profile')
            elif k!=39:
                bb=[bytes.fromhex(x['hex']) for x in src]; u=[int.from_bytes(b,'little') for b in bb]; i=[int.from_bytes(b,'little',signed=True) for b in bb]
                require([pub[k] for k in ('u_min','u_max','i_min','i_max','zero','all_ones','distinct')]==[min(u),max(u),min(i),max(i),u.count(0),i.count(-1),len(set(u))],'numeric profile')
                if 'u_hist' in pub:require(pub['u_hist']==hist(u),'numeric histogram')
                if w==4:
                    vals=[S.unpack('<f',b)[0] for b in bb]; f=[v for v in vals if math.isfinite(v)]; first=next((x for x,v in zip(src,vals) if not math.isfinite(v)),None)
                    require(pub['f32_probe']==dict(finite=len(f),nonfinite=len(src)-len(f),min=min(f,default=None),max=max(f,default=None),first_not_finite=first),'float bit probe')
    rows,_,_,strings,dates=data['server']
    published=inv['slots'][4]['opaque_string_lengths'];require(published==[dict(witness_first=next(iter(x),None),length_hist=hist(y['length'] for y in x)) for x in strings],'string lengths')
    for lane,ref in zip(dates,inv['slots'][12]['opaque_date_lanes'],strict=True):
        ds=[x['day'] for x in lane]; bad=next((x for x in lane if not 1<=x['day']<=365+(x['year']%4==0 and (x['year']%100!=0 or x['year']%400==0))),None)
        require(ref==dict(samples=len(lane),year_hist=hist(x['year'] for x in lane),day_range=[min(ds,default=None),max(ds,default=None)],upper7_hist=hist(x['upper7'] for x in lane),first=next(iter(lane),None),first_bad=bad),'packed date probe')


def check_domains(inv,mapping,master,data,target):
    fields=master['entities']['nation.xml'][0]['fields']; rows=mapping['fields']; linked={s['schema_candidates'][0]:s for s in inv['slots'] if len(s['schema_candidates'])==1}
    for s in inv['slots']:
        c=s.get('candidate_4cc');require(s['schema_candidates']==[i for i,f in enumerate(fields) if c and f.get('field')==c],'unique exact scope')
    require(len(fields)==len(rows)==mapping['fields_total']==346,'full schema ledger')
    mismatches=0
    for i,(f,r) in enumerate(zip(fields,rows)):
        code=f['field'];require(r['schema']==f and r['schema_index']==i and r['code']==code and r['scope_occurrences']==sum(x.get('field')==code for x in fields),'frozen XML occurrence')
        s=linked.get(i)
        if s is None:require(r['slot_position'] is None and r['grade'] in ('unmapped','no_t10_wire_slot') and r['alignment']=='unbound','no guessed join');continue
        pos=s['position'];require(pos==r['slot_position'],'schema/slot bridge')
        order=[(j,t) for j,t in linked.items() if (i-j)*(pos-t['position'])<0]
        if order:
            j,t=order[0]; a=data['server'][0][0];mismatches+=1
            require(r['alignment']=='mismatch' and r['order_first_counterexample']==dict(other_schema_index=j,other_code=t['candidate_4cc'],other_position=t['position'],position=pos,row=0,absolute=a[pos]['absolute'],other_absolute=a[t['position']]['absolute'],archive='server'),'order inversion retained')
        else:require(r['alignment']=='joined_without_order_conflict','order check')
        if s['role']=='collection':require(r['grade']==('prior_collection_parent_dispatch_held' if code=='Nftb' else 'prior_collection'),'no collection promotion');continue
        valid=True
        for side,d in r['domain'].items():
            src=[x[pos] for x in data[side][0] if pos in x]
            if not src:require(d=={'status':'mode skipped'},'no fabricated client observations');continue
            v=[int.from_bytes(bytes.fromhex(x['hex']),'little',signed=s['wire_type']=='i8') for x in src]
            if code in REF:
                actual=target[side,REF[code]]; uids=set(actual.values()); nulls=v.count(0xffffffff); live=[x for x in v if x!=0xffffffff]; allow=lambda x:x in actual or x==0xffffffff
                require(d['target_rows']==len(actual) and d['target_table']==REF[code] and d['nulls']==nulls and d['live_hit']==sum(x in actual for x in live) and d['uid_control_hit']==sum(x in uids for x in live),'ordinal join/control')
            elif f['type']=='enum':
                en=master['enums'][f.get('enum_ref',code)]; allowed={int(x['enum']) for x in en['values']}; allow=lambda x:x in allowed
                require(d['allowed']==sorted(allowed) and d['enum_source']==en['file'] and en['file'].endswith('\\nation.xml'),'scoped inline enum')
            elif f['type']=='boolean':
                require(d['mask']==512 and d['raw_other_bits_first']==next((dict(x,value=y) for x,y in zip(src,v) if y&~512),None),'mask isolation')
                v=[int(bool(x&512)) for x in v];allow=lambda x:x in (0,1);require(d['hist']==hist(v),'mask count')
            else:
                a,b=int(f['min_value']),int(f['max_value']);allow=lambda x:a<=x<=b;require((d['min'],d['max'])==(a,b),'XML range')
            bad=[dict(x,value=y) for x,y in zip(src,v) if not allow(y)]; status='held' if bad else 'pass';valid &= not bad
            require(d['status']==status and d['first_counterexample']==next(iter(bad),None) and (d['hit'],d['miss'])==(len(v)-len(bad),len(bad)),'domain and first counterexample '+code+' '+side)
        require(r['grade']==('L3' if valid else 'held'),'grade '+code)
    ctr=hist(r['grade'] for r in rows);require(mapping['grades']==ctr and mapping['L3']==ctr['L3'] and mapping['L4']==0 and mapping['aligned']==len(linked) and mapping['order_mismatches']==mismatches,'coverage totals')
    require(mapping['alignment_rate']==len(linked)/346 and mapping['L3_rate']==ctr['L3']/346,'coverage rates')
    require(mapping['supplemental']['Npop']['grade']=='held' and not inv['slots'][34]['schema_candidates'],'Npop not frozen schema')


def closure_and_regress(inv,mapping,abc,data,raw,target):
    prior=J('scratch/t46/out/grammar_diff_client_server.json')
    require(abc['old_status']==prior['status'] and abc['status']=='A_B_C_D_explained_in_both_modes','old t46 status')
    for i,(k,code,site,obj,stride) in enumerate(ABC,23):
        a=abc['segments'][k];require((a['parent'],a['count_site'],a['object_displacement'],a['item_width'],a['position'])==(code,site,obj,stride,i) and a['old_probe_preserved']==prior['segments'][k],'ABC static and negative')
        for side,(rows,_,_,_,_) in data.items():
            seq=[r[i] for r in rows];counts=[x['count'] for x in seq];require(a['arms'][side]==dict(first=seq[0],first_live=next(x for x in seq if x['count']),rows=len(seq),items=sum(counts),count_hist=hist(counts),nonempty=sum(bool(n) for n in counts)),'ABC count replay')
            require(all(x['end']-x['absolute']==(1 if k=='A' else 4)+stride*x['count'] for x in seq),'ABC stride equation')
        require(a['arms']['server']['items']==a['arms']['client']['items'] and a['arms']['server']['first']['body_offset']!=a['old_probe_preserved']['same_offset_probe']['offset'],'moved server count')
    c=data['client'][0]; s=data['server'][0]; cap=J('reports/t22_nation_capital.json'); require(cap['schema']['commented'],'capital scope')
    for side,(rows,ids,_,_,_) in data.items():
        idcities=target[side,2]; city_b=raw[side,2]; require(digest(city_b)==cap['data']['city_payload_sha256'],'capital target hash')
        v=[int.from_bytes(bytes.fromhex(r[17]['hex']),'little') for r in rows]; live=[x for x in v if x!=0xffffffff];require(all(x in idcities for x in live),'capital ordinal join')
        uid_set=set(idcities.values()); ctrl=sum(x in uid_set for x in live); require((len(live),ctrl,v[149])==(231,25,0xffffffff),'capital t22 fixture counts')
        d=mapping['supplemental']['Ncpi']['domain'][side];require(d['status']=='pass' and d['live_hit']==231 and d['nulls']==20 and not d['miss'] and d['uid_control_hit']==25,'capital ledger')
        for w in cap['holdouts']+cap['cross_nation']:
            o=w['nation_row'];x=v[o]; require(x==w['city_row'] and idcities[x]==w['city_duni'] and U(city_b,24+43*x)==w['city_nation_row'],'capital target witness')
            if side=='client':require(rows[o][17]['absolute']==int(w['field_payload_offset'],16) and rows[o][17]['body_offset']==9,'capital client coordinate')
        require(ids[139]==765 and ids[55]==110 and len(ids)==251,'England / China ordinal separate from UID')
    require(data['client'][1]==data['server'][1] and mapping['regression']['nation_ordinals']=={'55':110,'139':765},'all nation ordinal/ID pairs')
    ver=J('scratch/t01/inbox/t01f/output.json')['verification'];par=ver['cpcm_named_anchors'];require(len(par)==2 and mapping['regression']['parent_352']['fixture']==par,'parent fixture provenance')
    for x in par:
        require(S.unpack('<III',bytes.fromhex(x['parent_identity']['bytes']))==(352,150990,150990) and U(bytes.fromhex(x['child_cpcm']['bytes']),0)==x['expected_parent_ordinal']==352,'parent 352, no t25 archive access')
    tax=J('scratch/t47/out/fields_nation_tax.json');require(sorted(k for k,r in tax['fields'].items() if r['status']=='L3')==mapping['regression']['Ntxr_L3'] and tax['L3']==7,'Ntxr retained L3s')
    tc={k:J(f'scratch/t53/out/fields_{k}.json')['grade'] for k in ('PUnI','PUnT','PUnP','PUnJ')};require(tc==mapping['regression']['TCrs'] and set(tc.values())=={'held'},'TCrs retained holds')


def verify():
    inv=out('field_slots.json'); ledger=out('field_map.json');abc=out('abc_closure.json')
    manifest={x['path']:x['sha256'] for x in J('evidence/MANIFEST.json')['files']}
    require(manifest[MASTER]==MASTERH==ledger['schema_sha256'] and all(digest((ROOT/p).read_bytes())==manifest[p] for p in (MASTER,IDA)),'frozen manifest')
    require(PINS.items()<=inv['fixture_sha256'].items() and all(digest((ROOT/p).read_bytes())==h for p,h in inv['fixture_sha256'].items()),'accepted/unmodified fixtures')
    n,b=pe_check(inv); raw=load_payloads(inv['archives']); prior=J(PRIOR)
    data={side:independent_rows(raw[side,10],side=='server',prior[side]) for side in ('client','server')}
    require(inv['footer']==FOOT.hex() and inv['footer_at']=={a:r[2] for a,r in data.items()} and inv['slot_count_by_archive']=={'client':15,'server':40},'row frames')
    target=targets(raw,ledger['targets']);profiles(inv,data);check_domains(inv,ledger,J(MASTER),data,target);closure_and_regress(inv,ledger,abc,data,raw,target)
    print(f'PASS t55: {n} reachable instructions / {b} conditional branches; 40 ordered slots; 251+251 rows; A/B/C/D; 346 fields, L3={ledger["L3"]}, L4=0')


def selftest():
    require(U(bytes.fromhex('60010000'),0)==352,'little endian')
    require(hist([0,2,2])=={'0':1,'2':2},'histogram')
    try:independent_rows(b'\0'*22,False,{'payload_sha256':digest(b'\0'*22)})
    except Failed:pass
    else:raise Failed('bad header accepted')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    try:
        if args.selftest:selftest();print('t55 verify selftest PASS')
        else:verify()
        return 0
    except Failed as e: print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e: print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
