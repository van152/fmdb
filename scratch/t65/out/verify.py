#!/usr/bin/env python3
"""Independent verification of t65: archive keys, frozen t55 coordinates, PE and round-2 ledger."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import unpack_from
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'scratch/t55/out'
MASTER='evidence/fm24/reports/editor_schema/master.json'
PROV='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
SIDES=('client','server')
COMMON=(0,*range(14,27),39)
ONLY=(*range(1,14),*range(27,39))
GATES={'Nnam':0x1042222,'Nsnm':0x104225c,'N3ln':0x10420a1,'Nnty':0x1041f9c,'nhrl':0x104251e,
       'dbnm':0xfe375d,'ttcl':0xfe35bc,'tbcl':0xfe3980,'rdui':0xfe3862}
REG={'local_get':0x1041f40,'base_get':0xfe3520,'helper_78':0x3d74e30,'item_78':0x3daa110,
     'identity':0x3c600f0,'packed_date':0x39dd7b0}


class Check(Exception): pass

def need(ok,msg):
    if not ok: raise Check(msg)


def J(p): return json.loads((ROOT/p).read_bytes())
def H(b): return sha256(b).hexdigest()
def C(v): return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def U(b,p=0): return unpack_from('<I',b,p)[0]
def hist(v): return {str(x):y for x,y in Counter(v).items()}


def archives(meta):
    old=ROOT.parent/'fm24/tools/python'
    depot=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
    if any(p.drive.upper()=='Z:' or p.resolve().drive.upper()=='Z:' for p in (old,depot)):raise ValueError('Z: forbidden')
    sys.path.append(str(old))
    import zstandard
    mm=bytes.fromhex('0201666d662e080000')
    def frame(buf):
        need(buf[:4]==b'\x28\xb5\x2f\xfd','zstd frame magic')
        d=zstandard.ZstdDecompressor().decompressobj(); data=d.decompress(buf); used=len(buf)-len(d.unused_data)
        need(d.eof and used>0,'zstd end'); return data,used
    result={}
    for side in SIDES:
        b=(depot/f'{side}_db.dat').read_bytes(); md=meta[side]; need(H(b)==md['archive_sha256'] and b[8:17]==mm,(side,'archive'))
        toc,base=(17+x for x in unpack_from('<QQ',b,17)); need(base==34==md['data_base'] and base<toc and b[toc:toc+9]==mm,'TOC')
        buf,used=frame(b[toc+9:]); need(toc+9+used==len(b),'directory EOF'); p=0; members={}
        def take(w):
            nonlocal p
            need(0<=w<=len(buf)-p,'directory bounds');p+=w;return buf[p-w:p]
        def ui():return U(take(4))
        def text():return take(ui()).decode('utf-8')
        def walk(parent,depth):
            need(depth<40,'dir depth'); base_path=parent/text()
            for _ in range(ui()):
                key=base_path/(text()+text()); a,n,w,_,_=unpack_from('<5Q',take(40))
                need(not key.is_absolute() and '..' not in key.parts and str(key) not in members,'dir key')
                members[str(key)]=(base+a,n,w)
            for _ in range(ui()):walk(base_path,depth+1)
        walk(PurePosixPath(),0);need(p==len(buf) and len(members)==md['entries'],'directory closure')
        for t in ((10,21) if side=='server' else (10,)):
            a,n,w=members[f'{side}_db/table_{t}.dat']; hi=a+n; s=md['members'][str(t)]; q=a; found=[]; frames=[]
            bound=min((v[0] for v in members.values() if v[0]>a),default=toc)
            need(base<=a<hi<=bound and [a,hi,bound]==[s[k] for k in ('start','end','neighbor_bound')],(side,t,'entry bounds'))
            need(H(b[a:hi])==s['compressed_sha256'],(side,t,'compressed SHA'))
            while q<hi:
                d,n=frame(b[q:hi]); f=[q,q+n,len(d)];frames.append(f);q+=n
                if len(d)==w:found.append((d,f))
            need(len(found)==1 and frames==s['frames'],(side,t,'frame selector'))
            d,f=found[0];need(f==s['selected'] and H(d)==s['payload_sha256'],(side,t,'payload SHA'))
            result[side,t]=d
    return result


def point(i,a,b,v):return dict(row=i,absolute=a,raw=b.hex(),value=v)


def join(samples,keys):
    inverse={v:k for k,v in keys.items()}; h=miss=uid=bad=null=0; fm=fu=cl=None
    for s in samples:
        v=s['value']
        if v==0xffffffff:null+=1;continue
        if v in keys:h+=1
        else:miss+=1;fm=fm or s
        if v in inverse:uid+=1
        else:bad+=1;fu=fu or s
        if cl is None and v in keys and v in inverse and keys[v]!=v:
            cl={**s,'ordinal_to_UID':keys[v],'UID_to_ordinal':inverse[v]}
    return dict(rows=len(samples),ordinal_hit=h,ordinal_miss=miss,null=null,wrong_UID_hit=uid,wrong_UID_miss=bad,
                first_ordinal_miss=fm,first_wrong_UID_miss=fu,first_collision_distinct_owner=cl)


def geometry(raw,slots,proj,source):
    cells={}; records={}; rdui={}; targets={}
    cases={2:(True,4),3:(True,4),4:(True,None),11:(True,None),12:(False,12),13:(False,14),
           23:(True,5),24:(True,28),25:(True,28),26:(True,12)}
    head=bytes.fromhex('03017461642ef10d'); foot=bytes.fromhex('0000000001ec7ae404')
    for side in SIDES:
        b=raw[side,10]; end=len(b)-9; seq=COMMON if side=='client' else tuple(range(40))
        need(b[:8]==head and U(b,8)==251 and b[end:]==foot,'main header/footer')
        need(proj['envelopes'][side]==dict(rows=251,bytes=len(b),first_selector=13,identity_bytes=12,footer_at=end,selector_hist={'0':251},
              mode=int(side=='server'),execution_positions=list(seq),payload_sha256=H(b),body_bytes=end-13),(side,'envelope'))
        spans={i:slots[i]['coordinates'][side] for i in range(40)}
        need(all(len(v)==(251 if i in seq else 0) for i,v in spans.items()),(side,'position census'))
        # Verify complete partition against accepted t55 coordinates, independent of builder's forward cursor.
        cells[side]={i:[] for i in seq}; records[side]=[]; rdui[side]=[]; targets[side]={}; cursor=13
        for row in range(251):
            for i in seq:
                a,w=spans[i][row]; s=slots[i]; m=s['width']; need(a==cursor and m<=w<=end-a,(side,row,i,'gap/width'))
                q=b[a:a+w]; cursor=a+w; n=None
                if i in cases:
                    signed,stride=cases[i];n=int.from_bytes(q[:m],'little',signed=signed)
                    need(n>=0 and (w==m+n*stride if stride is not None else (w==m if n==0 else w>m)),(side,row,i,'span/count'))
                else:need(w==m,(side,row,i,'fixed width'))
                if i==0:need(q==b'\x00',(side,row,'selector'))
                if i==39:
                    o,u,v=unpack_from('<III',q);need(o==row and u==v!=0,(side,row,'identity'))
                    targets[side][o]=u;rdui[side].append(point(row,a+8,q[8:12],v));records[side].append(q)
                cells[side][i].append((a,q,n))
        need(cursor==end and len(set(targets[side].values()))==251 and H(b''.join(records[side]))==source['targets'][side]['10']['identity_sha256'],(side,'keys/EOF'))
    eq={str(i):sum(x[1]==y[1] for x,y in zip(cells['client'][i],cells['server'][i],strict=True)) for i in COMMON}
    need(eq==proj['common_byte_equal_rows']=={str(i):251 for i in COMMON},'cross-archive common bytes')
    need([x['position'] for x in proj['server_only']]==list(ONLY),'server-only inventory')
    ctype={1:'prior_reference',4:'frozen_parent',11:'frozen_parent',34:'out_of_frozen_schema',37:'prior_word_bit'}
    for x in proj['server_only']:
        i=x['position']; s=slots[i]; v=cells['server'][i]; w=s['width']
        a,b,n=v[0]; values=[(n if i in cases else int.from_bytes(q,'little')) for _,q,n in v]
        pf=dict(rows=251,bytes=sum(len(q) for _,q,_ in v),sha256=H(b''.join(q for _,q,_ in v)),
                first=point(0,a,b[:w],values[0]),distinct=len(set(values)),min=min(values),max=max(values))
        if i in cases:
            first=next((point(r,q,z[:w],n) for r,(q,z,n) in enumerate(v) if n),None)
            spans=[len(z) for _,z,_ in v];pf.update(items=sum(values),empty_rows=values.count(0),count_hist=hist(values),first_nonempty=first,span_range=[min(spans),max(spans)])
        need(x['server']==pf and x['client']=={'rows':0,'condition':'external mode != 0; t55 client replay uses mode 0'},(i,'coverage/profile'))
        need([x[k] for k in ('site','object_displacement','wire_type','t55_code','transfer','collection')]==
             [s.get(k) for k in ('site','object_displacement','type','candidate_4cc','transfer','collection')],(i,'slot identity'))
        need(x['classification']==ctype.get(i,'opaque_collection' if i in cases else 'unnamed_fixed_transfer'),(i,'class'))
    headers=[point(r,a+k,b[k:k+1],b[k]) for r,(a,b,n) in enumerate(cells['server'][13]) for k in range(4,len(b),14)]
    actual=proj['opaque_78_item_header'];need((len(headers),hist(x['value'] for x in headers),headers[0],14)==
                           tuple(actual[k] for k in ('items','header_byte_hist','first','item_wire_width')),'+0x78 observed item width/header')
    b=raw['server',21];n=U(b,8); at=13+n*181; trials=[]; stadium={}
    need(b[:8]==head and at+9==len(b) and b[at:at+5]==bytes.fromhex('0000000001'),'stadium EOF')
    for k,e in enumerate(range(13+181,at+1,181)):
        q=b[e-12:e];i,u,v=unpack_from('<III',q);need(i==k and u==v!=0 and b[e]==0,'stadium identity');trials.append(q);stadium[i]=u
    need(len(stadium)==len(set(stadium.values()))==n==source['targets']['server']['21']['count'] and H(b''.join(trials))==source['targets']['server']['21']['identity_sha256'],'stadium key set')
    for side in SIDES:
        def samples(i):return [point(r,a,q,U(q)) for r,(a,q,_) in enumerate(cells[side][i])]
        d=dict(rdui_identity_NOT_reference=join(rdui[side],targets[side]),t10_target_count=251,
               raw_t10_hypotheses={str(i):join(samples(i),targets[side]) for i in (5,6,7,21,35,36) if i in cells[side]},
               Nnsi_prior_control=join(samples(1),stadium) if side=='server' else {'status':'bypassed_mode'})
        need(d==proj['reference_controls'][side],(side,'ordinal and wrong-UID controls'))
    for side,at,w,value,label in (('client',7188,4,1507845,'extra_158 count'),('server',38,1,-90,'A count')):
        q=raw[side,10][at:at+w]
        need(int.from_bytes(q,'little',signed=True)==value and proj['wrong_mode_witnesses'][side]=={
            **point(0,at,q,value),'label':label,'forced_mode':int(side=='client'),'source':'t55 first bad transfer; raw bytes rechecked'},(side,'wrong-mode raw witness'))
    return rdui


def static(p,s):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64,CS_OP_IMM,CS_OP_MEM
    path=ROOT.parent/'fm24/input/editor.exe'
    if path.drive.upper()=='Z:' or path.resolve().drive.upper()=='Z:':raise ValueError('Z: forbidden')
    b=path.read_bytes();need(H(b)==p['editor']['sha256']==EXEH,'editor SHA')
    pe=pefile.PE(data=b,fast_load=True); pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    va=lambda o:base+pe.get_rva_from_offset(o)
    off=lambda a:pe.get_offset_from_rva(a-base)
    cs=Cs(CS_ARCH_X86,CS_MODE_64);cs.detail=True
    def dec(o):return next(cs.disasm(b[o:o+15],va(o),1))
    def dst(i):return off(i.operands[0].imm) if i.operands and i.operands[0].type==CS_OP_IMM else None
    def raw(r):
        o=r['file_offset'];z=bytes.fromhex(r['bytes']);need(va(o)==r['VA'] and b[o:o+len(z)]==z,('raw PE',o));return o
    def instruction(r):
        o=raw(r);i=dec(o); need(r['instruction']==(i.mnemonic+' '+i.op_str).strip() and len(i.bytes)*2==len(r['bytes']),('disassembly',o))
        if i.mnemonic.startswith('j') or i.mnemonic=='call':need(dst(i)==r['direct_target'],('edge',o))
    for r in p['instructions']:instruction(r)
    need(len(p['vslots'])==4,'vslot census')
    for k,r in p['vslots'].items():
        o=raw(r);need(va(o)==s['source']['nation_vtable_VA']+8*int(k) and off(unpack_from('<Q',b,o)[0])==r['target'],'vtable cell')
    need({k:v['target'] for k,v in p['vslots'].items()}=={'2':0x1041f30,'10':0x1041eb0,'19':0x103fac0,'25':0x103f1f0},'vtable binding')
    need(dst(dec(0x1041f33))==REG['local_get'] and dst(dec(0x104334d))==REG['base_get'],'getter entry and tail')
    need(dec(0x1041eb0).op_str=='rax, qword ptr [rcx + 0xf0]' and dec(0xfe4b47).op_str=='qword ptr [rax + 0x50]','base virtual lookup boundary')
    main={r['file_offset']:r for f in sorted(OLD.glob('instructions.part*.json')) for r in J(f) if r.get('function')==0x103fac0}
    graph={k:v['successors'] for k,v in main.items()}; need(len(graph)==992,'main CFG size')
    def walk(entry,neighbors):
        seen=set();todo=[entry]
        while todo:
            o=todo.pop()
            if o not in seen:seen.add(o);todo.extend(neighbors(o))
        return seen
    need(walk(0x103fac0,graph.__getitem__)==set(graph),'frozen graph coverage')
    brs={r['site']:r for r in J(OLD/'branches.part001.json')}; need(len(brs)==109,'frozen conditional census')
    mode={o:brs[o] for o in (0x103fae6,0x10409d3)}; need(list(mode.values())==p['mode_edges'],'mode edges')
    for o,r in mode.items():
        i=dec(o);need(i.mnemonic=='je' and dst(i)==r['taken'] and o+i.size==r['fallthrough'],'mode branch decode')
    need(dec(0xf2ba38).op_str=='byte ptr [rsp + 0x30], r12b' and dec(0x103fadc).op_str=='eax, byte ptr [rsp + 0x120]' and dec(0x10409cb).op_str=='byte ptr [rsp + 0x120], 0','external mode chain')
    client=walk(0x103fac0,lambda o:[mode[o]['taken']] if o in mode else graph[o]); static_only=[]
    for sl in s['slots'][1:39]:
        i=sl['position']; pc=sl['site']; rep=0x1040592 if i==13 else pc
        need((rep in client)==(i in COMMON),('client reach',i))
        if i in ONLY:
            g=0x103fae6 if i<14 else 0x10409d3
            need(rep not in walk(0x103fac0,lambda o:[] if o==g else graph[o]) and rep in walk(mode[g]['fallthrough'],graph.__getitem__),('gate dominance',i))
            static_only.append(dict(position=i,outer_gate=g,main_site=rep,cursor=pc,client_reachable=False))
    need(static_only==p['server_only_static'],'server-only static evidence')
    extent={base+x.struct.BeginAddress:base+x.struct.EndAddress for x in pe.DIRECTORY_ENTRY_EXCEPTION}
    regions={'main':set(main)}
    need(set(p['regions'])==set(REG),'bounded region keys')
    for name,entry in REG.items():
        end=off(extent[va(entry)]); ext=[]
        def neighbors(o):
            i=dec(o); nxt=o+i.size
            possible=[] if i.mnemonic in ('ret','retf','int3','ud2') else [dst(i)] if i.mnemonic=='jmp' else [nxt,dst(i)] if i.mnemonic.startswith('j') else [nxt]
            for edge in possible:
                if edge is not None and entry<=edge<end:yield edge
                else:ext.append([o,edge])
        addresses=walk(entry,neighbors); regions[name]=addresses
        need(p['regions'][name]==dict(entry=entry,end_exclusive=end,reachable=len(addresses),external_edges=sorted(ext),addresses_sha256=H(C(sorted(addresses)))),(name,'bounded walk'))
    for r in p['shift_mask_inventory']:instruction(r)
    actual={(name,o) for name,addresses in regions.items() for o in addresses if dec(o).mnemonic in ('shr','sar','shl','and','bt','bts','btr','btc')}
    observed={(r['region'],r['file_offset']) for r in p['shift_mask_inventory']}
    need(actual==observed and len(observed)==len(p['shift_mask_inventory']),'shift/mask completeness')
    need([dec(x).op_str for x in (0x10435f3,0x1043605,0x1043608)]==['esi, word ptr [r12 + 0x1c8]','esi, 9','sil, 1'],'Nndn prior bit control')
    for name in ('helper_78','item_78','packed_date','identity'):
        ops={o:dec(o) for o in regions[name]}
        actual=sorted(o for o,i in ops.items() if i.mnemonic=='call' and i.operands[0].type==CS_OP_MEM and i.operands[0].mem.disp==40)
        need(actual==p['helper_transfer_sites'][name],(name,'helper stream sites'))
    need([dst(dec(x)) for x in (0x1040592,0x104e6b0,0x3d74f9c,0x1072560,0x1040bcf,0xfae340,0xdb7f80)]==
         [0x104e6b0,REG['helper_78'],0x1072560,REG['item_78'],0xfae340,REG['identity'],REG['packed_date']],'helper route')
    need(dec(0x3c60106).op_str=='rbx, [rdi + 8]' and dec(0x3c6010d).operands[1].imm==12,'base identity destination and width')
    need([dec(x).op_str for x in (0xfe389d,0xfe38a2)]==['esi, dword ptr [r12 + 0x10]','dword ptr [r12 + 0xc], esi'] and dec(0xfe38a7).mnemonic=='je','suppression gate')
    size={2:(0x103fc63,4),3:(0x103ff2a,4),4:(0x1040144,None),11:(0x1040485,None),12:(0x10404e3,12),13:(0x3d74f70,14),
          23:(0x104073b,5),24:(0x10407d6,28),25:(0x1040898,28),26:(0x1040980,12)}
    need([x['position'] for x in p['collection_gate_helper_cursor']]==list(size),'collection census')
    for x in p['collection_gate_helper_cursor']:
        i=x['position']; g,w=size[i]; ins=dec(g); sl=s['slots'][i]; call=sl['collection']['item']
        need((x['item_gate'],x['wire_stride'],x['empty_edge'],x['count_cursor'],x['member'])==(g,w,dst(ins),sl['site'],sl['object_displacement']),('item control',i))
        need(x['item_activation']=={'je':'count != 0','jle':'count > 0'}[ins.mnemonic] and call in x['item_path'],('item condition and call',i))
    return regions,dec,dst


def ledger(doc,baseline,mast,st,regions,dec,dst,rdui):
    fields=baseline['fields']; frozen=mast['entities']['nation.xml'][0]['fields']; enums=mast['enums']; got=doc['fields']
    need(len(got)==len(fields)==len(frozen)==346 and doc['before']==baseline['grade_counts'],'ledger counts')
    need(frozen==[x['schema'] for x in fields],'frozen occurrence records')
    keys={int.from_bytes(f['code'].encode(),'big'):f for f in fields}; actual=[]
    for name in ('local_get','base_get'):
        addresses=regions[name]
        for o in sorted(addresses):
            ins=dec(o);at=o+ins.size
            if ins.mnemonic!='cmp' or ins.operands[-1].type!=2 or ins.operands[-1].imm not in keys or at not in addresses:continue
            br=dec(at)
            if br.mnemonic not in ('je','jne'):continue
            f=keys[ins.operands[-1].imm];actual.append(dict(region=name,code=f['code'],xml_index=f['xml_index'],baseline_grade=f['grade'],gate=o,branch=at,
                        equal_edge=dst(br) if br.mnemonic=='je' else at+br.size))
    need(actual==st['exact_frozen_gates'],'exact gate census')
    trials={x['code']:x for x in st['unmapped_gate_trials']}; need(len(trials)==len(st['unmapped_gate_trials'])==9 and {k:v['gate'] for k,v in trials.items()}==GATES,'9 trials')
    need({x['code'] for x in actual if x['baseline_grade']=='unmapped'}==set(trials),'trial completeness')
    counts=Counter()
    for i,(a,f) in enumerate(zip(got,fields,strict=True)):
        code=f['code']; old=f['grade']; schema=f['schema']; need((a['code'],a['xml_index'],a['t55_grade'])==(code,i,old),'occurrence identity')
        if old!='unmapped':need(a==dict(xml_index=i,code=code,t55_grade=old,grade=old,status='unchanged_e94'),('prior unchanged',code));continue
        domain={k:schema[k] for k in ('type','min_value','max_value','max_length','enum_ref','database_table_type','is_optional') if k in schema}
        if domain.get('enum_ref'):domain['enum_definition_rows']=len(enums.get(domain['enum_ref'],{}).get('values',[]))
        want='held' if code in trials else 'unmapped'; counts[want]+=1; need(a['schema_domain']==domain and a['grade']==want,(code,'domain/grade'))
        if code=='rdui':
            for side,samples in rdui.items():
                v=[x['value'] for x in samples]; z=dict(status='held_getter_suppressed',rows=251,suppressed=251,exposed=0,
                   raw_unsigned_range=[min(v),max(v)],raw_values_sha256=H(b''.join(x.to_bytes(4,'little') for x in v)),
                   xml_min=None,xml_max=None,xml_enum_ref=None,first_unexposed=samples[0])
                need(a['archives'][side]==z,(code,side,'suppressed samples'))
            need(domain=={'type':'integer'} and a['projection_gate']==GATES[code] and a['slot']==39 and a['wire_lane']==[8,4]
                 and trials[code]['cursor']==0x3c60119 and a['first_counterexample']==rdui['client'][0],'rdui disclosure')
        elif code in trials:
            tr=trials[code]; e=a['first_counterexample']
            need(a['slot'] is None and tr['cursor'] is None and a['projection_gate']==tr['gate']==e['gate'] and e['absolute'] is None and
                 e['first_evidence']==tr['helper_route'][0] and e['kind']=='static_member_or_helper_mismatch' and a['domain_status']=='no_bound_samples',('unbound',code))
        else:need(a['status']=='no_bounded_exact_getter_gate' and a['domain_status']=='not_evaluable_without_wire_binding',('unmapped',code))
    need(dict(counts)==doc['round2_of_327']=={'unmapped':318,'held':9} and doc['new_L3']==doc['L4']==0 and not doc['public_schema_changed'],'round2 totals')


def check():
    p=J(HERE/'projections.json'); f=J(HERE/'field_map_r2.json'); s=J(OLD/'field_slots.json'); m=J(OLD/'field_map.json')
    manifest={x['path']:x['sha256'] for x in J('evidence/MANIFEST.json')['files']}
    for name,h in p['provenance']['files'].items():need(H((ROOT/name).read_bytes())==h,('source SHA',name))
    for name in (MASTER,PROV):need(manifest[name]==p['provenance']['files'][name],('manifest',name))
    public=J('reports/club_nation_subtable_schema.json')['nation_main_row_fields']
    need(public['acceptance_ledger_entry']=='E94' and public['source_records']['field_slots']==s and public['source_records']['field_map']==m
         and H(C(public))==p['provenance']['public_nation_main_row_fields_sha256'],'E94 public section')
    r=geometry(archives(s['archive']),s['slots'],p,s); regions,dec,dst=static(p['static'],s)
    ledger(f,m,J(MASTER),p['static'],regions,dec,dst,r)
    print('t65 verify: PASS (251+251, 40/15, 25 server-only; 327 surveyed, 9 held, 0 new L3)')


def selftest():
    p=[point(i,20+4*i,x.to_bytes(4,'little'),x) for i,x in enumerate((0,1,2,0xffffffff))]
    j=join(p,{0:2,1:7}); need((j['ordinal_hit'],j['ordinal_miss'],j['wrong_UID_hit'],j['null'])==(2,1,1,1),'ordinal vs UID test')
    print('t65 verify selftest: OK')


def main():
    a=argparse.ArgumentParser(description=__doc__);g=a.add_mutually_exclusive_group()
    g.add_argument('--check',action='store_true',help='run verification (default)');g.add_argument('--selftest',action='store_true');opt=a.parse_args()
    try:
        selftest() if opt.selftest else check();return 0
    except Check as e:print(f't65 check failed: {e}',file=sys.stderr);return 1
    except Exception as e:print(f't65 fatal: {type(e).__name__}: {e}',file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
