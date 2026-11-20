"""Independent t57 verifier: archive TOC, bounded PE CFG, dual cursors, domains and fixtures."""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import unpack_from, pack
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MASTER='evidence/fm24/reports/editor_schema/master.json'
L2='evidence/fm24/reports/dbdat_decode/db_tables_big.json'
HEAD=bytes.fromhex('03017461642ef10d')
FOOT=bytes.fromhex('0000000001e3c03a77')
SIDES=('client','server')
TARGETS=(2,3,10,21,25)

class Failed(Exception):pass

def ck(ok,msg):
    if not ok:raise Failed(msg)
def j(p):return json.loads(p.read_bytes())
def sha(b):return sha256(b).hexdigest()
def u(b,p=0):return unpack_from('<I',b,p)[0]
def hist(vals):return {str(k):v for k,v in Counter(vals).items()}


def archive_contents(md):
    p=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data')).resolve()
    if p.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard
    shell=bytes.fromhex('0201666d662e080000'); magic=bytes.fromhex('28b52ffd'); all_raw={}
    def frame(blob):
        ck(blob.startswith(magic),'frame magic')
        d=zstandard.ZstdDecompressor().decompressobj(); x=d.decompress(blob); span=len(blob)-len(d.unused_data)
        ck(d.eof and span>0,'frame end'); return x,span
    for side,count in (('client',31),('server',77)):
        b=(p/f'{side}_db.dat').read_bytes(); toc,base=(x+17 for x in unpack_from('<QQ',b,17))
        rec=md[side]; ck(sha(b)==rec['archive_sha256'] and base==34==rec['data_base'] and b[8:17]==b[toc:toc+9]==shell,(side,'archive'))
        directory,used=frame(b[toc+9:]); ck(toc+9+used==len(b),'TOC EOF'); pos=0; entries={}
        def pull(w):
            nonlocal pos
            ck(w<=len(directory)-pos,'short TOC'); pos+=w;return directory[pos-w:pos]
        def num():return u(pull(4))
        def txt():return pull(num()).decode('utf-8')
        def walk(parent,depth):
            ck(depth<40,'TOC recursion'); name=parent/txt()
            for _ in range(num()):
                file=(name/(txt()+txt())).as_posix(); ck(file not in entries and '..' not in PurePosixPath(file).parts,'TOC duplicate/invalid path')
                oid,span,n,_,_=unpack_from('<5Q',pull(40)); entries[file]=(base+oid,span,n)
            for _ in range(num()):walk(name,depth+1)
        walk(PurePosixPath(),0);ck(pos==len(directory) and len(entries)==count==rec['entries'],'TOC walk')
        for t in (*TARGETS,*(['extra_3'] if side=='client' else [])):
            name=f'{side}_db/table_{t}.dat';lo,w,n=entries[name];hi=lo+w;d=rec['members'][str(t)]
            bound=min((x for x,*_ in entries.values() if x>lo),default=toc)
            ck(base<=lo<hi<=bound and d['range']==[lo,hi] and d['bound']==bound and d['member']==name and d['declared_size']==n,'TOC member bounds')
            ck(sha(b[lo:hi])==d['compressed_sha256'],'packed digest'); found=[]; frames=[]
            while lo<hi:
                payload,span=frame(b[lo:hi]); frames.append([lo,lo+span,len(payload)]);lo+=span
                if len(payload)==n:found.append(payload)
            ck(len(found)==1 and frames==d['frames'],'unique sized frame'); payload=found[0]
            ck(sha(payload)==d['payload_sha256'] and payload[:8]==HEAD and u(payload,8)==d['count'],'raw signature/count')
            all_raw[side,t]=payload
    return all_raw


def check_pe(source,ledger,slots):
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM
    raw=(ROOT.parent/'fm24/input/editor.exe').read_bytes(); p=pefile.PE(data=raw,fast_load=True); p.parse_data_directories(directories=[3]); base=p.OPTIONAL_HEADER.ImageBase
    ck(sha(raw)==source['editor_sha256']=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4','editor provenance')
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    def va(o):return base+p.get_rva_from_offset(o)
    def off(v):return p.get_offset_from_rva(v-base)
    def decode(o):return next(md.disasm(raw[o:o+15],va(o),1))
    def direct(i):return off(i.operands[0].imm) if i.operands and i.operands[0].type==CS_OP_IMM else None
    inputs={}; stored_graph=defaultdict(dict); shards=sorted(HERE.glob('instructions.part*.json'))
    for part in shards:
        for d in j(part):
            o=d['file_offset']; i=decode(o)
            ck(o not in inputs and i.address==d['VA'] and bytes(i.bytes).hex()==d['bytes'] and (' '.join((i.mnemonic,i.op_str))).strip()==d['instruction'],('instruction',hex(o)))
            if 'direct_target' in d:ck(direct(i)==d['direct_target'],('target',hex(o)))
            inputs[o]=i
            if 'function' in d:stored_graph[d['function']][o]=d['successors']
    branches={}
    for f in sorted(HERE.glob('branches.part*.json')):
        for d in j(f):
            o=d['site']; ck(o not in branches,'duplicate branch');branches[o]=d
    seen_b=set()
    expected_bounds={off(base+e.struct.BeginAddress):off(base+e.struct.EndAddress) for e in p.DIRECTORY_ENTRY_EXCEPTION}
    for entry in source['runtime_function_extents'].values():
        first,end=entry['begin'],entry['end_exclusive'];ck(expected_bounds[first]==end and va(first)==entry['VA'],'PE extent')
        to_visit=[first]; found={}; external=set(); xfers=set()
        while to_visit:
            o=to_visit.pop()
            if o in found:continue
            i=decode(o); nx=o+i.size; m=i.mnemonic; nexts=[]
            if m.startswith('j'):
                t=direct(i)
                if t is not None:nexts.append((t,'tail_jump' if m=='jmp' else 'branch'))
                if m!='jmp':
                    nexts.append((nx,'fallthrough'));d=branches[o];seen_b.add(o)
                    ck((d['function'],d['taken'],d['fallthrough'])==(first,t,nx),('branch',hex(o)))
                    if d['predicate'] is not None:
                        q=inputs[d['predicate']]; ck(q.eflags and d['predicate_instruction']==f'{q.mnemonic} {q.op_str}'.strip(),'predicate record')
            elif m not in ('ret','retf','iret','iretq','int3','ud2'):nexts=[(nx,'fallthrough_out_of_bound')]
            children=[]
            for v,k in nexts:
                if first<=v<end:children.append(v);to_visit.append(v)
                else:external.add((hex(o),k,hex(va(v))))
            found[o]=sorted(set(children))
            if m=='call' and i.operands[0].type==CS_OP_MEM and i.operands[0].mem.disp==0x28:xfers.add(o)
        ck(found==stored_graph[first] and len(found)==entry['reachable'] and xfers==set(entry['direct_stream_reads']),('reachable graph',hex(first)))
        ck(external=={(x['from'],x['kind'],x['target_va']) for x in entry['external_edges']},'outgoing CFG edges')
    ck(seen_b==set(branches),'branch census')
    tav=source['factory_3']['base'];a=source['factory_3']['cell']['file_offset']
    ck(a==0xf49d44 and a==tav+12 and off(va(tav)+unpack_from('<i',raw,a)[0])==0xf48daf==source['factory_3']['arm'],'rel32 factory arm')
    for d,targets in [(source['CLUB'],{2:0xe89a00,19:0xe5a7a0,20:0xe5c550,21:0xe5ca50}),(source['LEAGUE_BODY_CLUB'],{19:0x157cff0})]:
        for n,t in targets.items():
            a=off(d['vtable'])+8*n; saved=d['slots'][str(n)] if 'slots' in d else d['slot19']; ck(a==saved['file_offset'] and off(int.from_bytes(raw[a:a+8],'little'))==t,'vslot')
        for block in d['rtti'].values():
            sig=bytes.fromhex(block['bytes']);a=block['file_offset'];ck(raw[a:a+len(sig)]==sig,'RTTI bytes')
    for s in slots:ck(s['site'] in inputs and all(a in inputs for a in s['inner_or_flush_sites'] or []),('wire site',s['key']))
    for f in ledger:
        d=f['static']
        if d is None or 'compare' not in d:continue
        i=inputs[d['compare']]; h=inputs[d['branch']]; path=d['equal_path']
        ck(i.mnemonic=='cmp' and i.operands[1].imm==int.from_bytes(f['code'].encode(),'big') and h.address==i.address+i.size,'getter compare')
        ck(path[0]==(direct(h) if h.mnemonic=='je' else off(h.address+h.size)) and path[-1]==d['member_use'],'getter equality path')
        for a,b in zip(path,path[1:]):
            z=inputs[a]; ck(b in ({direct(z)} if z.mnemonic=='jmp' else {off(z.address+z.size),direct(z)} if z.mnemonic.startswith('j') else {off(z.address+z.size)}),'getter arm edge')
        if f['code']=='Cncl':
            a=d['type_case_1']['file_offset'];jt=d['type_case_table']; i=inputs[0x1105881]
            ck(off(i.address+i.size+i.operands[1].mem.disp)==jt==a-4 and off(va(jt)+unpack_from('<i',raw,a)[0])==0x110589d,'typed base reference jump')
            ck(inputs[0x110586b].op_str=='eax, byte ptr [rcx + 0xa]' and inputs[0x3ae4a80].op_str=='byte ptr [rsi], 0x37','typed item/4CC selector distinction')
            ck(direct(inputs[0x11d2aa9])==0x1105860 and direct(inputs[0x11058b4])==direct(inputs[0x434e664])==0xf7e440 and direct(inputs[0xf7e440])==0x3bf3460,'club family resolver')
            ck(inputs[0x110589d].op_str=='r8, qword ptr [rsi + 0x10]' and inputs[0x434e64c].op_str=='r8, qword ptr [r12 + 0x10]','same loader context table displacement')
    return len(inputs),len(branches)


# Independent cursor uses grouped fixed formats, bounded slice arithmetic, and actual
# scope/prior knowledge; the emitted schema/positions never decide what bytes to consume.
ORDER='selector derived_170 derived_178 ref_d8 ref_e0 ref_e8 ref_f0 ref_f8 flags160 name_len name_bytes short_len short_bytes raw16a raw166 person148 raw16c vec110 obj150_tag obj150 vec130 vec138 raw168 stad140 base_ba base_b8 base18 base30 base60 base78 base90 base48 basea8 identity'.split()
GROUPS={17:(1,4),20:(1,24),21:(1,12),26:(1,4),27:(1,4),28:(1,4),29:(1,4),30:(1,4),31:(1,16),32:(2,28)}

def table3(b,is_server):
    n=u(b,8); footer=len(b)-9; h=sha256(); q=13; cols=[[] for _ in ORDER]; orders=Counter(); ids=[]; starts=[]; ends=[]; sels=[]
    for ordinal in range(n):
        p=q; start=q; indexes=[]
        def span(k,w):
            nonlocal p
            if w<=0 or p+w>footer:raise Failed((ordinal,p,k,w,'overrun'))
            cols[k].append((ordinal,p,w)); indexes.append(k); p+=w
        sel=b[q];ck(sel in (0,12),(ordinal,q,'selector')); span(0,1)
        if sel:span(1,4);span(2,1)
        for k in range(3,8):span(k,4)
        span(8,6)
        for k in (9,11):
            text_at=p;span(k,4);length=u(b,text_at)
            if length:span(k+1,length)
        def group(k):
            w,s=GROUPS[k]; raw=int.from_bytes(b[p:p+w],'little'); ck(k not in (17,20,21,28,29,32) or raw<1<<(8*w-1),(ordinal,p,'positive count')); span(k,w+raw*s)
        if is_server:
            for k,w in enumerate((1,2,4,1),13):span(k,w)
            group(17);tag=b[p];span(18,1)
            if tag==0:span(19,45)
            else:ck(tag==2,(ordinal,p,'tag branch'))
            group(20);group(21);span(22,2);span(23,4)
        span(24,1);span(25,2)
        if is_server:
            for k in range(26,33):group(k)
        at=p;span(33,12); got,a,c=unpack_from('<III',b,at);q=p
        ck(got==ordinal and a==c and a>(ids[-1] if ids else 0),(ordinal,at,'nonzero, increasing triple'))
        ids.append(a);sels.append(sel);starts.append(start);ends.append(q);h.update(pack('<IIIB',start,q,a,sel));orders[tuple(indexes)]+=1
    ck(q==footer and b[q:]==FOOT,'EOF/footer')
    return cols,ids,sels,starts,ends,orders,h.hexdigest()


def check_framing(b,f,predicted):
    # Rediscover every possible repeated lane using unaligned NumPy views with
    # byte-by-byte construction (no candidate data from the builder). Reverse DP.
    import numpy as np
    n=len(predicted); groups=[[] for _ in predicted]; data=np.frombuffer(b,dtype='u1').astype('u4')
    v=data[:-3] | data[1:-2]<<8 | data[2:-1]<<16 | data[3:]<<24
    pp=np.flatnonzero((v[:-8]<n)&(v[4:-4]==v[8:]))
    for a in pp.tolist():groups[int(v[a])].append((a,int(v[a+4])))
    ck(hist(map(len,groups))==f['candidate_histogram'],'candidate histogram')
    def counts(header,footer,tail,valid,nonzero,mono):
        prior=[]; end=len(b)-footer
        for i in range(n-1,-1,-1):
            stage=[]
            if not mono:
                apos=[]; suffix=[0]
                for a,_,ways in prior:apos.append(-a);suffix.append(suffix[-1]+ways)
            for a,t in reversed(groups[i]):
                q=a+tail
                if a<header or q>end or (i==n-1 and q!=end) or (valid is not None and (a+12>=len(b) or b[a+12] not in valid)) or (nonzero and t==0):continue
                if i==n-1:num=1
                elif not mono:num=suffix[bisect_right(apos,-q)]
                else:
                    num=0
                    for a2,t2,k in prior:
                        if a2<q:break
                        if t<t2:num+=k
                if num:stage.append((a,t,min(f['cap'],num)))
            if not stage:return 0
            prior=stage
        return min(f['cap'],sum(w for _,_,w in prior))
    for key,r in f.items():
        if not isinstance(r,dict) or 'paths' not in r:continue
        h,foot,tail,valid,nz,mono=13,8,13,{0,12},True,True
        if key.startswith('marker_0_footer_'):foot=int(key.rsplit('_',1)[1]);valid={0}
        if key.startswith('header_'):h=int(key.rsplit('_',1)[1])
        if key.startswith('triple_footer_'):foot=int(key.rsplit('_',1)[1]);tail=12
        if key in ('wire_triple','triple_no_lookahead'):foot,tail=9,12
        if key in ('no_marker','triple_no_lookahead'):valid=None
        if key in ('allow_zero','both_relaxed'):nz=False
        if key in ('no_uid_order','both_relaxed'):mono=False
        ck(counts(h,foot,tail,valid,nz,mono)==r['paths'],('reverse DP',key))
        if 'first_rejected_candidate' in r and r['first_rejected_candidate'] is not None:
            a,x=r['first_rejected_candidate']; ck(x==u(b,a+4) and b[a:a+13].hex()==r['first_rejected_raw'],'data negative')
    ck(all(any(a==e-12 for a,k in groups[i]) for i,e in enumerate(predicted)) and f['wire_triple']['paths']==1,'independent unique raw path and cursor')


def extract_targets(raw,runs,docs):
    result={}
    for side in SIDES:
        for tid in TARGETS:
            b=raw[side,tid];n=u(b,8);end=len(b)-9
            if tid==3:pos=[x-12 for x in runs[side][4]]
            elif tid==10:
                old=j(ROOT/'scratch/t47/out/cursor_nation_tax.json')[side];ck(sha(b)==old['payload_sha256'],'t10 reuse exact bytes')
                pos=[x['identity_at'] for x in old['rows']]
            elif tid==25 and side=='server':
                keys=result['client',25];q=end; rr=[]
                for i in reversed(range(n)):
                    record=pack('<III',i,keys[i],keys[i]);q=b.rfind(record,13,q);ck(q>=0,'missing comp triple');rr.append(q)
                pos=list(reversed(rr));q=13
                for i,k in enumerate(pos):
                    a=b.find(pack('<III',i,keys[i],keys[i]),q,end);ck(a==k,'ambiguous comp triple');q=a+12
            else:
                stride={(2,'client'):43,(2,'server'):43,(21,'client'):38,(21,'server'):181,(25,'client'):127}[tid,side]
                ck(13+stride*n==end,'target fixed length');pos=list(range(13+stride-12,end,stride))
            ck(len(pos)==n and pos[-1]==end-12 and b[end:end+5]==b'\0'*4+b'\1','target envelope')
            ids={};h=sha256()
            for i,a in enumerate(pos):
                k,l,r=unpack_from('<III',b,a);ck(k==i and l==r and l,('target triple',side,tid,i));ids[k]=l;h.update(b[a:a+12])
            d=docs[side][str(tid)];ck(len(set(ids.values()))==n==d['count'] and h.hexdigest()==d['identity_sha256'] and [0,ids[0]]==d['first'] and [n-1,ids[n-1]]==d['last'],'full target census')
            result[side,tid]=ids
    return result


def check_ledger(ledger,fs,cols,b,ids,keys,side):
    keymap={'duni':(33,4,4),'Cnam':(10,0,0),'Csnm':(12,0,0),'Cext':(3,0,4),'PLgn':(25,1,1),'Cedp':(31,0,0),
        'Cnti':(3,0,4),'Cbni':(5,0,4),'Cccn':(6,0,4),'Cncl':(31,0,0),'Ccty':(7,0,4),'Cprs':(13,0,1),
        'CIns':(8,1,1),'CASt':(8,1,1),'Csot':(8,0,1),'Ctsi':(23,0,4),'Cdof':(15,0,4),'CnCV':(8,3,1)}
    refs={'Cnti':10,'Cbni':10,'Cccn':10,'Ccty':2,'Ctsi':21,'Cext':10,'Cncl':3};masks={'CIns':4,'CASt':1,'Csot':2,'CnCV':1}
    ck(len(fs)==len(ledger)==433,'433 frozen occurrences')
    for f,x in zip(ledger,fs,strict=True):
        k=f['code'];ck(x==f['schema'] and k==x['field'],'schema bytes/scoping')
        if k not in keymap:
            ck(f['candidate_position'] is None and f['accepted_position'] is None,'unbound no coordinates');continue
        s,d,w=keymap[k];r=f['domain_profiles'][side];ck(f['candidate_position']==s and f['lane']==d,'manual slot/byte binding')
        if not cols[s] and s not in (10,12):ck(r=={'rows':0,'status':'bypassed'},(k,side,'bypass'));continue
        coords=[];vals=[];duplicates=0;invalid=None;types=Counter(); first_item=None
        if k in ('Cnam','Csnm'):
            coords=[(i,a+4,u(b,a)) for i,a,_ in cols[s-1]]
            for i,a,z in coords:
                try: vals.append(len(b[a:a+z].decode('utf-8')))
                except UnicodeDecodeError:
                    vals.append(-1)
                    if invalid is None:invalid=i
        elif k in ('Cncl','Cedp'):
            coords=cols[s];prop=0x37 if k=='Cncl' else 0x6f
            for i,a,z in coords:
                tagged=[a+1+16*x for x in range(b[a]) if b[a+1+16*x+11]==prop];duplicates+=len(tagged)>1
                if tagged:types[str(b[tagged[0]+10])]+=1
                if k=='Cncl':
                    if tagged and b[tagged[0]+10]==1:
                        p=tagged[0]; vals.append(u(b,p))
                        if first_item is None:first_item=dict(row=i,absolute=p,raw=b[p:p+16].hex(),value=vals[-1])
                    else:vals.append(0xffffffff)
                else:
                    on=bool(tagged and b[tagged[0]+12]==3); vals.append(int(on))
                    if on and first_item is None:
                        p=tagged[0];first_item=dict(row=i,absolute=p,raw=b[p:p+16].hex(),value=1)
        else:
            coords=[(i,a+d,w) for i,a,_ in cols[s]];vals=[int.from_bytes(b[a:a+w],'little',signed=k in ('PLgn','Cprs')) for _,a,w in coords]
        def pt(i):
            ix,a,w=coords[i];return dict(row=ix,absolute=a,raw=b[a:a+w].hex(),value=vals[i])
        n=len(vals);vc=Counter(vals);ck((r['rows'],r['min'],r['max'],r['distinct'],r['first'])==(n,min(vc),max(vc),len(vc),pt(0)),(k,side,'full raw domain'))
        if 'hist' in r:ck(r['hist']==hist(vals),(k,side,'histogram'))
        bad_at=None; grade='pass'
        if k in refs:
            target=keys[side,refs[k]];uid_set=set(target.values()); hit=[];miss=[];null=[];wrong=[]
            for i,v in enumerate(vals):
                if v==0xffffffff:null.append(i)
                elif v in target:hit.append(i)
                else:miss.append(i)
                if v!=0xffffffff and v not in uid_set:wrong.append(i)
            ck((r['hit'],r['miss'],r['null'],r['wrong_uid_hit'],r['first_wrong_uid_miss'])==(len(hit),len(miss),len(null),sum(vc[v] for v in vc if v!=0xffffffff and v in uid_set),pt(wrong[0]) if wrong else None),(k,side,'actual target domains'))
            ck(r['first_null']==(pt(null[0]) if null else None) and r['first_live']==(dict(pt(hit[0]),target_uid=target[vals[hit[0]]]) if hit else None),'ref witnesses')
            if miss or not hit or (null and k not in ('Cext','Cncl') and x.get('is_optional')!='true'):
                grade='held';bad_at=miss[0] if miss else 0
            elif k=='Cncl':
                ck(r['records_with_multiple_tags']==duplicates and r['type_when_tagged']==dict(types) and r['first_live_item']==first_item,'new club multi-tags/live item')
                ck(duplicates==0 and set(types)=={'1'},'new club type-1 domain')
            elif k=='Cext':ck(r['decoded']=={'0':len(hit),'1':len(null)},'derived extinct')
        elif k in masks:ck(r['mask']==masks[k] and r['decoded']==hist(int(bool(v&masks[k])) for v in vals),'mask profile')
        elif k=='Cedp':ck(r['decoded']==hist(vals) and r['records_with_multiple_tags']==duplicates and r['type_when_tagged']==dict(types) and r['first_true_item']==first_item,'base48 tag projection')
        elif k=='duni':ck(vals==ids,'identity projection')
        elif k in ('Cnam','Csnm'):
            maxc=int(x['max_length']) if 'max_length' in x else None; bad=[i for i,v in enumerate(vals) if maxc is not None and v>maxc]
            ck(r['max_chars']==maxc and r['max_bytes']==max(t[2] for t in coords) and r['empty']==vc[0] and r['violations']==len(bad),'string domain')
            if invalid is not None or bad or k=='Cnam':grade='held';bad_at=invalid if invalid is not None else bad[0] if bad else 0
        else:
            if k in ('PLgn','Cprs'):ck('enum_ref' not in x,'no scoped enum')
            grade='held';bad_at=0
        ck(r.get('domain')==grade,(k,side,'gate'))
        if grade=='held':ck(r['first_counterexample']==pt(bad_at),'first counterexample')


def fixture_checks(raw,runs,m,keys):
    d=j(ROOT/L2)['tables'];note=m['regression'];c=raw['client',2];s=raw['server',21]
    for f in d['2']['named_anchor_checks']:
        i=f['row_index'];a=14+43*i;ll=list(unpack_from('<ff',c,a+1))
        ck(note['city'][f['city']]==[i,keys['client',2][i],ll,c[a+10]] and all(abs(x-y)<0.000002 for x,y in zip(ll,f['coordinates_approx'],strict=True)),'frozen city coordinates')
    for f in d['21']['landmark_cross_checks']:
        i=f['row_index'];a=14+181*i;row=note['stadium'][str(i)];caps=list(unpack_from('<II',s,a))
        ck(row['capacity_and_seats']==caps==[f['server_row_capacity_candidate_u32_at_0'],f['server_row_seating_capacity_candidate_u32_at_4']] and
           row['coordinates']==list(unpack_from('<ff',s,a+160))==f['coordinates_f32_at_160_164'] and row['city_ordinal']==u(s,a+146),'stadium coordinates/capacity frozen witness')
    ck(note['stadium']['430']['capacity_and_seats']==[81044,81044] and note['stadium']['71']['capacity_and_seats']==[74031,74031],'Bernabeu and negative Old Trafford')
    for i,k,uid in note['old_owner']:ck(u(s,14+181*i+16)==k and keys['server',3][k]==uid,'stadium owner fixture')
    for side in SIDES:
        b=raw[side,3]; cols,ids,*_=runs[side]; ck(ids[460]==676 and u(b,cols[7][460][1])==1061 and u(b,cols[3][460][1])==139,'Liverpool identity/city')
        for i,ref in note['city_joins']:ck(u(b,cols[7][i][1])==ref,'club city fixtures')
        for i,ref in note['short_names']:
            p=cols[11][i][1];ck(b[p+4:p+4+u(b,p)].decode('utf-8','replace')==ref,'short name fixtures')
        for i,ns in note['nation_refs']:ck([u(b,cols[k][i][1]) for k in (3,5,6)]==ns,'nation refs fixtures')
        ck([keys[side,10][139],keys[side,10][55],keys[side,25][352]]==[765,110,150990],'t01f target identities')
    x=raw['client','extra_3'];exp={e['candidate_order_index']:e for e in d['3']['field_validation']['Cyfn_named_year_checks']}
    ck(len(exp)==len(note['founded_year_fixture_only'])==14 and sha(x)==d['extra_3']['source_payload_sha256']['client'],'frozen year sample')
    for e in note['founded_year_fixture_only']:
        a=e['absolute'];i=e['row'];ck((u(x,a-4),unpack_from('<H',x,a)[0])==(i,exp[i]['client_extra_3_u16_at_row_plus_4']) and e['note']==exp[i]['note'],'founding year actual anchor')
    ck(note['t01f']=={'0x3bf':139,'0x7c4c':55,'0x15f0b':352,'0x15f8a':352} and all(u(raw['client',25],int(k,16))==y for k,y in note['t01f'].items()),'t01f exact legacy bytes')
    ck([note['frozen_club_negatives'],note['frozen_stadium_negatives']]==[d['3']['negative_results'],d['21']['negative_results']],'negative verbatim')
    old=j(ROOT/'scratch/t24/out/cursor.json');ck(note['original_Cccn_negative']==old['controls']['E60_original'],'E60 verbatim')
    sb=note['legacy_Shanghai_index_correction']; c=raw['client',3]; cols=runs['client'][0]; o=sb['same_name_ordinal']; p=cols[9][o][1]
    ck(o==32356 and sb['frozen_index']==32354 and c[p+4:p+4+u(c,p)]==b'Shanghai Port' and u(c,cols[7][o][1])==1693 and u(c,cols[7][32354][1])==10149,'legacy ordinal correction')


def verify():
    d=j(HERE/'field_slots.json'); m=j(HERE/'field_map.json'); slots=d['slots']; ledger=m['fields']
    ck(d['L4']==m['L4']==0 and [s['key'] for s in slots]==ORDER and [s['position'] for s in slots]==list(range(34)), 'scope and positions')
    manifest={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']}
    for path,h in d['provenance_sha256'].items():ck(sha((ROOT/path).read_bytes())==h and (not path.startswith('evidence/') or manifest[path]==h),path+' SHA')
    ck(sha((ROOT/MASTER).read_bytes())==m['frozen_sha256']=='7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda','master SHA')
    k=d['skipped']; ck(k['v6_git_object']=='8b04fc2:reports/club_nation_subtable_schema.json','pinned v6'); blob=subprocess.check_output(['git','show',k['v6_git_object']],cwd=ROOT)
    vv=json.loads(blob); ck(sha(blob)==k['v6_sha256'] and vv['schema_version']==6 and {t['parent_code']:t['table_type'] for t in vv['tables'][:8]}==k['subtables'],'v6 eight tables unchanged')
    fs=j(ROOT/MASTER)['entities']['club.xml'][0]['fields']; pe_stats=check_pe(d['source'],ledger,slots); raw=archive_contents(d['archives']); runs={}
    for side in SIDES:
        server=side=='server'; b=raw[side,3];run=table3(b,server);runs[side]=run; cols,ids,sels,starts,ends,seq,h=run; e=d['envelopes'][side]
        ck(len(ids)==len(set(ids))==e['rows']==84259 and e['selector_counts']==hist(sels) and e['row_trace_sha256']==h and e['first']==[starts[0],ends[0],ids[0],sels[0]] and e['last']==[starts[-1],ends[-1],ids[-1],sels[-1]],'row census')
        ck(e['header']+e['row_bytes']+9==len(b)==e['payload'] and e['row_bytes']==sum(q-p for p,q in zip(starts,ends,strict=True)) and e['footer_at']==ends[-1] and e['footer']==FOOT.hex(),'framing equation')
        census=e['identity_census'];ck(census['strictly_increasing'] and census['min_uid']==ids[0] and census['max_uid']==ids[-1] and census['identity_sha256']==sha(b''.join(pack('<III',i,v,v) for i,v in enumerate(ids))),'identity lanes')
        check_framing(b,d['framing_sensitivity'][side],ends)
        try:table3(b,not server)
        except Failed:pass
        else:raise Failed('wrong mode accepted')
        ck({tuple(x['execution_order']):x['rows'] for x in d['execution_templates'][side]}==seq,'realized ordering')
        for k,c in enumerate(cols):
            slot=slots[k];v=slot['profiles'][side]
            ck(v['rows']==len(c) and slot['execution_index'][side]==sorted({seq2.index(k) for seq2 in seq if k in seq2}),'slot path incidence')
            if not c:continue
            sizes=[w for _,_,w in c]; i,a,w=c[0]; ck(v['bytes']==sum(sizes) and v['width_range']==[min(sizes),max(sizes)] and v['coordinate_sha256']==sha(b''.join(pack('<III',*t) for t in c)),'all coordinate spans')
            ck(v['first']==dict(row=i,absolute=a,width=w,raw_prefix=b[a:a+min(w,64)].hex()) and v['last']==list(c[-1]),'first/last coordinate')
            if k in GROUPS:
                pl,it=GROUPS[k]; ck(v['item_counts']==hist((n-pl)//it for n in sizes) and v['items']==sum((n-pl)//it for n in sizes),'count domain')
            elif 'unsigned_min' in v:
                h=Counter(int.from_bytes(b[a:a+w],'little') for _,a,w in c)
                ck((v['unsigned_min'],v['unsigned_max'],v['distinct'])==(min(h),max(h),len(h)) and (v['histogram'] is None or v['histogram']=={str(k):v for k,v in h.items()}),'raw scalar profile')
    ck(runs['client'][1:3]==runs['server'][1:3],'matching identities/selectors')
    cp,ce=runs['client'][3:5]; sp,se=runs['server'][3:5]; extra=[(y-x)-(b-a) for a,b,x,y in zip(cp,ce,sp,se,strict=True)]
    ck(min(extra)>0 and d['server_minus_client_row_bytes']==dict(min=min(extra),max=max(extra),strictly_positive_rows=len(extra),total=sum(extra)),'per-row length delta')
    keys=extract_targets(raw,runs,d['target_identity_domains'])
    for side in SIDES:check_ledger(ledger,fs,runs[side][0],raw[side,3],runs[side][1],keys,side)
    for e in ledger:
        if e['domain_profiles'] is None:continue
        check=[(s,p) for s,p in e['domain_profiles'].items() if p['rows'] and p['domain']!='pass']
        ck((e['grade'],e['accepted_position'])==('held',None) if check else (e['grade'],e['accepted_position'])==('L3',e['candidate_position']),'promote or hold')
        if check:
            side,p=check[0];ck(e['first_counterexample']==dict(p['first_counterexample'],archive=side),'ledger first held')
    pts=sorted((e['candidate_position'],e['xml_index'],e['code']) for e in ledger if e['candidate_position'] is not None)
    inv=[[list(a),list(b)] for a in pts for b in pts if a[0]<b[0] and a[1]>b[1]]
    ck(m['order']['all_inversions']==inv and m['order']['inversions']==len(inv) and m['fields_with_unique_XML_alignment']==len(pts),'XML inversions')
    ck(m['grade_counts']==hist(e['grade'] for e in ledger) and m['new_L3']==[e['code'] for e in ledger if e['grade']=='L3' and e['previous_client_grade'] is None],'grade census')
    fixture_checks(raw,runs,m,keys)
    print(f't57 independent verify PASS: 84259 + 84259 rows; {pe_stats[0]} PE instructions / {pe_stats[1]} branches; {len(inv)} inversions; L4=0')


def selftest():
    row=b'\0'*39+pack('<III',0,7,7); b=HEAD+pack('<I',1)+row+FOOT; run=table3(b,False)
    ck(run[1]==[7] and run[4]==[63] and set(run[5])=={(0,3,4,5,6,7,8,9,11,24,25,33)},'synthetic cursor')
    try:table3(b+b'!',False)
    except Failed:pass
    else:raise Failed('trailing data accepted')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');args=p.parse_args()
    try:
        if args.selftest:selftest();print('t57 verifier selftest PASS')
        else:verify()
    except Failed as e:print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e:print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
