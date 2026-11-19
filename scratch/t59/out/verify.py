"""Independent t59 verifier: archive TOC, bounded PE CFG, dual cursors, domains and fixtures."""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import unpack_from, pack
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MASTER='evidence/fm24/reports/editor_schema/master.json'
L2='evidence/fm24/reports/dbdat_decode/db_tables_big.json'
HEAD=bytes.fromhex('03017461642ef10d')
FOOT=bytes.fromhex('00000000014ec43a77')
SIDES=('client','server')
TARGETS=(2,3,5,10,21,25)

class Failed(Exception):pass

def ck(ok,msg):
    if not ok:raise Failed(msg)
def j(p):return json.loads(p.read_bytes())
def sha(b):return sha256(b).hexdigest()
def u(b,p=0):return unpack_from('<I',b,p)[0]
def hist(vals):return {str(k):v for k,v in Counter(vals).items()}


def archive_contents(md):
    p=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if p.drive.upper()=='Z:' or p.resolve().drive.upper()=='Z:':raise ValueError('Z: forbidden')
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
        for t in TARGETS:
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
    for entry in source['extents'].values():
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
        ck(found==stored_graph[first] and len(found)==entry['reachable'] and xfers==set(entry['direct_stream_calls']),('reachable CFG',hex(first)))
        ck(external=={(x['from'],x['kind'],x['target_va']) for x in entry['external_edges']},'CFG outgoing edges')
        ck(sum(branches[o]['function']==first for o in seen_b)==entry['conditional'],'conditional total')
    ck(seen_b==set(branches),'branch census')
    f=source['factory_case_25'];a=f['cell']['file_offset'];t=f['base'];ck(a==t+25*4 and off(va(t)+unpack_from('<i',raw,a)[0])==f['arm']==0xf49129,'factory rel32')
    ck(raw[a:a+4].hex()==f['cell']['bytes'],'factory bytes')
    for owner in ('comp','table_comp'):
        d=source[owner]
        for k in ('col','type_name'):
            block=d['rtti'][k];a=block['file_offset'];s=bytes.fromhex(block['bytes']);ck(raw[a:a+len(s)]==s,'RTTI bytes')
        a=off(d['vtable']);ck(off(unpack_from('<Q',raw,a-8)[0])==d['rtti']['col']['file_offset'],'RTTI pointer')
    for slot_no,t in [(2,0xec0060),(5,0xebf040),(19,0xed0a40)]:
        a=off(source['comp']['vtable'])+8*slot_no;ck(off(unpack_from('<Q',raw,a)[0])==t and raw[a:a+8].hex()==source['comp']['slots'][str(slot_no)]['bytes'],'COMP vslot')
    for a,t in [(0xf49139,0xeb5db0),(0xed0a40,0x3b3f0d0),(0x3b3f101,0xeb7000),(0xeb7d84,0xfae340),(0xfae340,0x3c600f0),(0xf2ba23,0xf48b30),(0xf2ba7f,0xffa5d0)]:ck(direct(inputs[a])==t,'reader/loader chain')
    for a,width in [(0xf2ba02,1),(0x3c6010d,12),(0xffa5fc,4),(0xf2ba99,1),(0xf2bab9,4)]:ck(inputs[a].op_str.startswith('r8d, ') and inputs[a].operands[-1].imm==width,'row framing transfer')
    for s in slots:ck(s['site'] in inputs and all(a in inputs for a in s['inner_sites']),('slot static',s['key']))
    def getter(k,d):
        i=inputs[d['compare']];h=inputs[d['equality']];path=d['equal_path'];ck(i.mnemonic=='cmp' and i.operands[-1].imm==int.from_bytes(k.encode(),'big') and h.address==i.address+i.size,'getter exact compare')
        ck(path[0]==(direct(h) if h.mnemonic=='je' else off(h.address+h.size)) and path[-1]==d['member_use'],'getter arm endpoints')
        for a,b in zip(path,path[1:]):
            z=inputs[a]; ck(b in ({direct(z)} if z.mnemonic=='jmp' else {off(z.address+z.size),direct(z)} if z.mnemonic.startswith('j') else {off(z.address+z.size)}),'getter path edge')
        if d['member'] is not None:ck(any(op.type==CS_OP_MEM and md.reg_name(op.mem.base)=='r12' and op.mem.disp==d['member'] for op in inputs[path[-1]].operands),'member load')
        if 'helper' in d:getter(k,d['helper'])
    slots_by={s['key']:s for s in slots}
    for f in ledger:
        d=f['static'];k=f['code']
        if not d:continue
        if d.get('kind')!='local_status_gate':
            getter(k,d)
            if f['slot'] and d['member'] is not None:ck(d['member']==slots_by[f['slot']]['object_offset']+f['lane'],'getter to wire member')
            continue
        code=int.from_bytes(k.encode(),'big');l,c,r,m,b,h=map(inputs.get,d['gate_sites'])
        ix=code+l.operands[1].mem.disp;ck(l.mnemonic=='lea' and l.op_str.startswith('eax, [rsi - ') and c.op_str.startswith('eax, ') and r.mnemonic=='ja' and
            0<=ix<=c.operands[-1].imm and ix==d['gate_index'] and m.op_str.startswith('ecx, ') and b.mnemonic=='bt' and b.op_str=='ecx, eax' and ((m.operands[-1].imm>>ix)&1),'local status bit gate')
        dest=d['object_base_site'];ck((h.mnemonic=='jb' and direct(h)==dest) or (h.mnemonic=='jae' and off(h.address+h.size)==dest),'local status taken route')
        if d['gate_sites'][-1]==0xec1b4c:ck(direct(inputs[0xec061b])==off(m.address) and not ((inputs[0xec0613].operands[-1].imm>>ix)&1),'secondary status gate')
        s=slots_by[f['slot']];base_disp=inputs[dest].operands[-1].imm;member=inputs[d['member_use']];op=member.operands[-1]
        ck(inputs[dest].mnemonic=='add' and inputs[dest+7].op_str=='rcx, r12' and inputs[dest+10].op_str=='edx, esi' and member.mnemonic=='movsx' and
            op.type==CS_OP_MEM and md.reg_name(op.mem.base)=='rcx' and base_disp+op.mem.disp==s['object_offset']+f['lane']==d['member'],'status getter member')
        root=direct(inputs[d['helper_jump']]);ck(root=={0x198:0x151d9b0,0x189:0x151e500}[base_disp],'status helper chain')
        if 'rel32_dispatch' in d:
            q=d['rel32_dispatch']; a,l,jump,lea,read,add,jmp=map(inputs.get,q['sites']); key=(code+a.operands[-1].imm)&0xffffffff
            t=lea.address+lea.size+lea.operands[-1].mem.disp; cell=q['cell'];o=off(t)+4*key
            ck(a.mnemonic=='add' and a.op_str.startswith('edx, ') and jump.mnemonic=='ja' and l.mnemonic=='cmp' and key==q['index']<=l.operands[-1].imm and
                t==q['table_va'] and read.mnemonic=='movsxd' and add.mnemonic=='add' and jmp.mnemonic=='jmp' and
                o==cell['file_offset'] and raw[o:o+4].hex()==cell['bytes'] and off(t+unpack_from('<i',raw,o)[0])==q['target']==d['member_use'],'status rel32 cell')
        else:getter(k,d['helper'])
    for a,text in [(0xeb7130,'rcx, [rbx + 0x198]'),(0xeb7147,'rcx, [rbx + 0x189]'),(0x433bc2f,'rdx, rbx'),(0x433bc3b,'rbx')]:ck(inputs[a].op_str==text,'packed status read sink')
    return len(inputs),len(branches)


def groups(b):
    import numpy as np
    n=u(b,8);ret=[[] for _ in range(n)]
    for k in range(4):
        q=np.frombuffer(memoryview(b)[k:k+(len(b)-k)//4*4],dtype='<u4'); matches=(q[:-2]<n)&(q[1:-1]==q[2:])
        for x in np.flatnonzero(matches).tolist():ret[int(q[x])].append((4*x+k,int(q[x+1])))
    return [sorted(t) for t in ret]


def reversed_paths(b,gg,option):
    h,f,w,markers,nz,inc=option;lim=len(b)-f;back=[];links=[]
    for i in reversed(range(len(gg))):
        now=[];link={}
        for a,v in gg[i]:
            if a<h or a+w>lim or (nz and not v) or (markers is not None and (a+12>=len(b) or b[a+12] not in markers)):continue
            if i==len(gg)-1:cnt=int(a+w==lim)
            else:
                cnt=0
                for p,q,t in back:
                    if p>=a+w and (not inc or q>v):
                        cnt+=t;link[a]=p
                        if cnt>=1000000:break
            if cnt:now.append((a,v,min(cnt,1000000)))
        links.append(link);back=now
        if not back:return 0,None
    count=min(sum(t for a,v,t in back),1000000)
    if count!=1:return count,None
    a=back[0][0];ats=[a]
    for link in reversed(links[1:]):a=link[a];ats.append(a)
    return count,ats


def replay(b,server):
    # Independent grouped wire model: decode into spans without using the emitted
    # JSON, candidate identity positions, or the builder's Cursor.
    rr=[];cols=defaultdict(list);seqs=Counter();p=13
    fixed_a='selector m15c m15d colour_tag m120 m124 m128 m12c m130 m134 m1a0 m1a2 m1a3 m1a4 m1a5 stat_a_tag m198 m199 m19a m19b m19c m19d m19e stat_b_tag m189_197 mf6 m138 m13c m58 m60 m70 m68 m150'.split()
    ext='m180 mb8 m188 m184 m186 m182 m160 m168 m170 m178'.split()
    suffix='m148 m152 m154 m156 m158 m15a m80 m88 m90 m98 wbcl_present'.split()
    for i in range(u(b,8)):
        a=p;seq=[]
        def record(k,start,finish):
            ck(start<=finish<=len(b)-9,(k,i,start,finish));cols[k].append((i,start,finish-start));seq.append(k)
        def transfer(k,w):
            nonlocal p
            q=p;p+=w;record(k,q,p);return int.from_bytes(b[q:p],'little')
        def block(keys,widths):return [transfer(k,w) for k,w in zip(keys,widths,strict=True)]
        vals=block(fixed_a,[1]*4+[2]*5+[1]*15+[15,1]+[4]*6+[2]);ck(vals[0]==0 and vals[3]==1 and vals[10]!=4 and vals[15]==2 and vals[23]==3,(i,'fixed revision tags'))
        if server:
            block(ext,[2,4,1,2,2,2,8,8,8,8]);q=p;p+=4+2*u(b,p);record('vec30',q,p)
            if transfer('a8_present',1):
                ver=b[p];transfer('obj_a8',1+32+4*(ver>=2)+9+(2 if ver>=3 else 1)+8)
            block(['mf0','m1a1','m1a8','mf4','mf5'],[4,1,1,1,1])
            if transfer('e0_present',1):ck(transfer('obj_e0',4)==0,'untraced e0 items')
            q=p;n=unpack_from('<i',b,p)[0];ck(0<=n<(len(b)-p)//7,'vec18 count');p+=4
            for _ in range(n):p+=8+(unpack_from('<b',b,p)[0]>=2)
            record('vec18',q,p)
            if transfer('e8_present',1):
                q=p;n=u(b,p+4);ck(n<(len(b)-p)//8,'e8 count');p+=8
                for _ in range(n):
                    ver=unpack_from('<h',b,p)[0];p+=10+(ver>=2)+(ver>=3)
                record('obj_e8',q,p)
            if transfer('c0_present',1):
                q=p;n=u(b,p+1);ck(n<(len(b)-p)//6,'obj c0 outer count');p+=5
                for _ in range(n):p+=6+12*u(b,p+2)
                record('obj_c0',q,p)
            if transfer('c8_present',1):transfer('obj_c8',25)
            transfer('m1a7',1)
            if transfer('d0_present',1):transfer('obj_d0',15)
            if transfer('d8_present',1):transfer('obj_d8',15)
            n=unpack_from('<h',b,p)[0];ck(n>=0,'vec100 count');transfer('vec100',2+5*n)
        if block(suffix,[4,2,2,2,2,2,4,4,4,4,1])[-1]:transfer('m14c',2)
        block(['m140','m144','mf7','mf8','mf9'],[4,4,1,1,1]);j,uid,repeat=unpack_from('<III',b,p);transfer('identity',12)
        ck(j==i and uid==repeat and uid>(rr[-1][2] if rr else 0),(i,p-12,'identity triple'));rr.append((a,p,uid));seqs[tuple(seq)]+=1
    ck(b[p:]==FOOT,'native footer');return rr,cols,seqs


def target_keys(raw,runs,notes):
    result={}
    for t in TARGETS:
        for s in SIDES:
            b=raw[s,t];n=u(b,8);end=len(b)-9
            if t==25:ats=[y-12 for x,y,v in runs[s][0]]
            elif t==3 and s=='client':
                npath,ats=reversed_paths(b,groups(b),[13,9,12,[0,12],True,True]);ck(npath==1,'t3 client unique keys')
            elif t==3:
                ats=[];p=end
                for i in reversed(range(n)):
                    v=result['client',3][i];p=b.rfind(pack('<III',i,v,v),13,p);ck(p>=0,'t3 server latest');ats.append(p)
                ats.reverse();p=13
                for i,a in enumerate(ats):
                    v=result['client',3][i];ck(b.find(pack('<III',i,v,v),p,end)==a,'t3 server earliest');p=a+12
            elif t==10:
                d=j(ROOT/'scratch/t47/out/cursor_nation_tax.json')[s];ck(d['payload_sha256']==sha(b),'t47 exact input');ats=[x['identity_at'] for x in d['rows']]
            else:
                w={2:(43,43),5:(34,48),21:(38,181)}[t][s=='server'];ats=range(13+w-12,13+w*n-11,w)
            ids={};parts=[]
            for i,a in enumerate(ats):
                d,v,w=unpack_from('<III',b,a);ck(d==i and v==w and v!=0,(t,s,'valid target identity'));ids[d]=v;parts.append(b[a:a+12])
            meta=notes[s][str(t)];ck(meta['count']==len(ids)==n==len(set(ids.values())) and meta['identity_sha256']==sha(b''.join(parts)) and ats[-1]+12==end and b[end:end+5]==b'\0\0\0\0\1','target envelope');result[s,t]=ids
        ck(result['client',t]==result['server',t],(t,'paired target keys'))
    return result


def check_domains(m,schemas,raw,runs,keys):
    from calendar import isleap
    from math import inf
    fields=m['fields'];ck(len(fields)==len(schemas['entities']['comp.xml'][0]['fields'])==255,'XML total')
    inv=[];aligned=[];new=[]
    for i,(d,f) in enumerate(zip(fields,schemas['entities']['comp.xml'][0]['fields'],strict=True)):
        ck((d['xml_index'],d['code'],d['schema'])==(i,f['field'],f),'frozen occurrence')
        if d['slot'] is None:ck(d['status']==('held' if d['static'] else 'unmapped'),'unbound disposition');continue
        aligned.append(d);fmt=d['format'];arg=d['arg'];lo=float(f.get('min_value',-inf));hi=float(f.get('max_value',inf))
        er=f.get('enum_ref');allowed={int(v['enum']) for v in schemas['enums'][er]['values']} if er else set(); holds=[]
        for s in SIDES:
            b=raw[s,25];cells=runs[s][1].get(d['slot'],[]);p=d['domain_profiles'][s];freq=Counter();flags=Counter();viol=[];active=[];days=[];def_dates=wrong=0
            target=keys[s,arg] if fmt=='ref' else {};uids=set(target.values());lane=d['lane'];point=None
            for row,at,w in cells:
                at+=lane;size=min(w,4) if fmt in ('rdui','uid') else 1 if fmt=='enum' else w
                data=b[at:at+size];v=int.from_bytes(data,'little');sg=int.from_bytes(data,'little',signed=True);x=v;valid=True;live=True
                if fmt=='ref':live=v!=0xffffffff;valid=v in target;wrong+=live and v in uids
                elif fmt=='level':x=sg+1;live=v!=100
                elif fmt=='distance':x=sg/10;live=sg>0
                elif fmt=='colour':valid=v<32768
                elif fmt=='date':
                    y=v>>16;day=v&511;x=y;days.append(day);flags[(v>>9)&127]+=1;def_dates+=y==1900 and day==1;valid=1<=y<=9999 and 1<=day<=365+isleap(y)
                elif fmt=='bit':x=int(bool(v&(1<<arg)))
                elif fmt=='bool':valid=v in {0,1}
                elif fmt=='enum':x=v if d['slot']=='mf5' else sg;live=x!=arg;valid=not er or x in allowed
                elif fmt in ('i16','context_number'):x=sg
                elif fmt=='rdui':live=b[at-4:at]!=data
                freq[x]+=1
                if live:
                    active.append(x)
                    if not valid or not lo<=x<=hi:viol.append((row,at,data.hex(),x))
                if point is None:point=(row,at,data.hex())
            expected_hold=bool(cells) and ((fmt=='enum' and not er) or fmt=='context_number' or not active)
            holds.append(bool(viol) or expected_hold)
            ck((p['tested'],p['live'],p['null_or_suppressed'],p['violations'],p['min_live'],p['max_live'],p['distinct'])==(len(cells),len(active),len(cells)-len(active),len(viol),min(active,default=None),max(active,default=None),len(freq)),(s,d['code'],'whole column domain'))
            ck(p['histogram']==({str(k):v for k,v in freq.items()} if len(freq)<=120 else None),'value histogram')
            ck(p['wrong_uid_hits']==(wrong if fmt=='ref' else None) and p['date_flag_histogram']==({str(k):v for k,v in flags.items()} if fmt=='date' else None),'date/UID controls')
            ck(p['day_range']==([min(days),max(days)] if days else None) and p['default_1900_day1']==(def_dates if fmt=='date' else None),'packed calendar')
            ck(bool(p['hold_reason'])==expected_hold,'held rule')
            if viol:ck(tuple(p['first_counterexample'][k] for k in ('row','at','raw','value'))==viol[0],'first raw counterexample')
            elif expected_hold:ck(tuple(p['first_counterexample'][k] for k in ('row','at','raw'))==point,'held first raw witness')
        ck(d['status']==('held' if any(holds) else 'L3'),('field gate',d['code']))
        if d['status']=='L3' and d['origin']=='t59':new.append(d['code'])
    for i,a in enumerate(aligned):
        for b in aligned[i+1:]:
            x,y=a['execution_index'],b['execution_index']
            if x>y:inv.append(dict(xml_pair=[a['xml_index'],b['xml_index']],codes=[a['code'],b['code']],execution_pair=[x,y]))
    ck(inv==m['inversions'] and hist(d['status'] for d in fields)==m['summary'] and len(aligned)==m['aligned'] and new==m['new_L3'],'field summary/inversions')


def fixtures(raw,runs,m,keys):
    path=ROOT/'reports/t01f_comp_row_offsets.json';p=j(path);f=m['fixtures'];ck(f['t01f_sha256']==sha(path.read_bytes()) and f['falsified_t01f']==p['falsified'],'untouched t01f negative')
    r0,c0,_=runs['client'];r1,c1,_=runs['server'];b0=raw['client',25];b1=raw['server',25]
    for (x,y,v),(a,e,w) in zip(r0,r1,strict=True):ck(v==w and b0[x:x+71]==b1[a:a+71] and b0[y-56:y]==b1[e-56:e],'t01f common spans')
    ck(set(f['accepted_client_slots'])==set(p['row_offset_map']),'all accepted prior slots')
    for k,v in p['row_offset_map'].items():
        s=f['accepted_client_slots'][k];ln=s['lane'];w=v['width'];ck(s['legacy_body_offset']==v['row_offset'] and s['width']==w,'prior slot coordinate')
        for (i,a,_),(row_index,b,_) in zip(c0[s['slot']],c1[s['slot']],strict=True):ck(i==row_index and a+ln-r0[i][0]-1==v['row_offset'] and b0[a+ln:a+ln+w]==b1[b+ln:b+ln+w],'prior span per row')
        for x in v['examples']:
            i=x['index'];at=c0[s['slot']][i][1]+ln;ck(at==int(x['payload_offset'],16) and b0[at:at+w]==bytes.fromhex(x['bytes']) and r0[i][2]==x['dbid'],'t01f prior example')
    ck(len(f['complete_old_codec'])==len(p['row_codec']['cursor_layout']),'complete prior layout')
    for s,v in zip(f['complete_old_codec'],p['row_codec']['cursor_layout'],strict=True):
        k=s['slot'];ln=s['lane'];w=v['width'];o=v['row_offset']
        ck((s['step'],s['legacy_body_offset'],s['width'])==(v['step'],o,w),'prior layout step')
        if k=='legacy_lookahead':
            ck(o==126 and w==1 and all(b0[y:y+1]==b1[e:e+1]==b'\0' for (_,y,_),(_,e,_) in zip(r0,r1)),'legacy lookahead')
            continue
        for (i,a,_),(ix,b,_) in zip(c0[k],c1[k],strict=True):
            aa=a+ln;bb=b+ln;ck(i==ix and aa==r0[i][0]+1+o and b0[aa:aa+w]==b1[bb:bb+w],'full prior layout span')
            if 'expected' in v:ck(w==1 and b0[aa]==v['expected'],'frozen prior tag')
    old=j(ROOT/L2)['tables']['25'];ck(len(f['named'])==len(old['named_anchor_checks'])==10 and len(f['parents'])==len(old['parent_reference_checks'])==2,'L2 fixtures counts')
    for x,d in zip(f['named'],old['named_anchor_checks']):
        i=x['row'];ck(i==d['row_index'] and x['uid']==r0[i][2]==d['dbid'],'named anchor row')
        for k,slot in [('ccti','m58'),('cnti','m60')]:
            a=c0[slot][i][1];b=c1[slot][i][1];ck((a,b,u(b0,a),u(b1,b))==(x[k]['client_at'],x[k]['server_at'],d[k],d[k]),'named anchor raw')
    ck({u(b0,a) for _,a,_ in c0['m58']}-{0xffffffff}==set(range(6)),'six continent ordinals')
    for x,d in zip(f['parents'],old['parent_reference_checks']):
        i=x['row'];a=c0['m68'][i][1];b=c1['m68'][i][1];ck(i==d['child_row_index'] and r0[i][2]==d['child_dbid'] and u(b0,a)==u(b1,b)==352 and r0[352][2]==d['parent_dbid']==150990,'parent 352')
    ck([keys['client',10][i] for i in (139,55)]==[765,110],'England/China')
    for x in p['server_crosscheck']['crep_examples']:
        i=x['index'];a=c1['m180'][i][1];ck(a==int(x['server_crep']['payload_offset'],16) and b1[a:a+2]==bytes.fromhex(x['server_crep']['bytes']) and r1[i][1]-r1[i][0]-127==x['extra_length'],'crep prior')


def verify():
    s=j(HERE/'field_slots.json');m=j(HERE/'field_map.json');ck(s['L4']==m['L4']==0,'L4 boundary')
    manifest={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']};ck(s['frozen'][MASTER].startswith('7d57477e'),'master frozen')
    for path,h in s['frozen'].items():ck(sha((ROOT/path).read_bytes())==h==manifest[path],('frozen manifest',path))
    raw=archive_contents(s['archives']);ni,nb=check_pe(s['source'],m['fields'],s['slots']);runs={}
    for side in SIDES:
        b=raw[side,25];server=side=='server';rr,cols,seqs=replay(b,server);runs[side]=rr,cols,seqs;env=s['envelopes'][side]
        ck(len(rr)==7047 and sum(y-x for x,y,v in rr)==env['rows'] and rr[-1][1]+9==env['payload']==len(b) and rr[0][0]==env['header']==13 and env['footer']==9,'native row envelope')
        ck(sha(b''.join(pack('<III',*r) for r in rr))==env['row_trace_sha256'] and hist(y-x for x,y,v in rr)==env['row_width_histogram'],'row trace')
        gg=groups(b);f=s['framing_sensitivity'][side];ck(hist(map(len,gg))==f['candidate_histogram'],'raw identity input census')
        for key,opt in s['framing_options'].items():
            n,at=reversed_paths(b,gg,opt);ck(n==f[key]['paths'],(side,key,'reverse path count'))
            if key=='wire_triple':ck(at==[y-12 for x,y,v in rr],(side,'independent identity positions'))
        try:replay(b,not server)
        except (Failed,IndexError):pass
        else:raise Failed('swapped mode should not close')
        ck({tuple(x['sequence']):x['rows'] for x in s['execution_templates'][side]}==seqs,'execution templates')
        for x in s['slots']:
            cells=cols.get(x['key'],[]);z=x['profiles'][side];ck(z['events']==len(cells) and z['bytes']==sum(w for _,_,w in cells),'slot coverage')
            if cells:
                ck(z['coordinate_sha256']==sha(b''.join(pack('<III',*v) for v in cells)) and z['content_sha256']==sha(b''.join(b[a:a+w] for _,a,w in cells)) and z['span_histogram']==hist(w for _,_,w in cells) and z['body_offset_histogram']==hist(a-rr[i][0]-1 for i,a,w in cells),'ordered site replay')
    observed=[x['key'] for x in s['slots'] if any(x['profiles'][t]['events'] for t in SIDES)]
    for k,seqs in [(t,runs[t][2]) for t in SIDES]:
        for seq in seqs:ck(tuple(z for z in observed if z in seq)==seq,'global execution order')
    ck({x['key']:x['execution_index'] for x in s['slots'] if x['execution_index'] is not None}=={k:i for i,k in enumerate(observed)},'execution indices')
    keys=target_keys(raw,runs,s['target_identity_domains']);check_domains(m,j(ROOT/MASTER),raw,runs,keys);fixtures(raw,runs,m,keys)
    print(f't59 independent PASS: 7047 client + 7047 server; {len(observed)} observed sites; {ni} instructions, {nb} branches; {m["summary"]}')


def selftest():
    x=b'\0'*8+pack('<I',2)+b'\0'+pack('<III',0,50,50)+b'\0'+pack('<III',1,51,51)+FOOT
    assert reversed_paths(x,groups(x),[13,9,12,[0],True,True])==(1,[13,26])
    assert reversed_paths(x,groups(x),[13,8,12,[0],True,True])==(0,None)
    assert reversed_paths(x,groups(x),[13,8,13,[0],True,True])==(1,[13,26])
    print('t59 independent selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true',help='test reverse framing on synthetic bytes');args=ap.parse_args()
    try:
        sys.path.append(str(ROOT.parent/'fm24/tools/python'))
        selftest() if args.selftest else verify()
        return 0
    except (Failed,AssertionError) as e:print('FAIL:',e,file=sys.stderr);return 1
    except Exception as e:print('ERROR:',type(e).__name__,e,file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
