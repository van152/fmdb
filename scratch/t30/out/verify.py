#!/usr/bin/env python3
"""Independently verify Clhs cursor, frozen schema, PE anchors and whole-table profiles."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct as S
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
EXE = Path('<OLD_REPO>/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
T29 = 'scratch/t29/out/profiles/table_server_37.profile.json'
N, START, END = 465712, 0x3e62b90, 0x3e62de7
# Independent audit table: (body offset, width, object displacement, real transfer, scoped code).
LAYOUT = (
    (0,4,0x18,0x3e62bd3,'divi'), (4,4,0x20,0x3e62bf3,None), (8,4,0x28,0x3e62c13,None),
    (12,2,0x36,0x3e62c33,'year'), (14,1,0x39,0x3e62c53,'posi'), (15,1,0x3a,0x3e62c73,'play'),
    (16,1,0x3b,0x3e62c93,'wins'), (17,1,0x3c,0x3e62cb3,'draw'), (18,1,0x3d,0x3e62cd3,'lost'),
    (19,2,0x30,0x3e62cf3,'gfor'), (21,2,0x32,0x3e62d0f,'gaga'), (23,2,0x34,0x3e62d2b,'poin'),
    (25,1,0x38,0x3e62d47,'orde'), (26,1,0x3e,0x3e62d63,'mxtm'), (27,12,8,0x3e62d8f,None),
)
HELD = {'year':(87,114717,0),'posi':(691,6472,53),'mxtm':(2626,6269,54),'poin':(187,216,-3)}


class Reject(Exception):
    pass


def req(ok, why):
    if not ok:
        raise Reject(why)


def load(p):
    return json.loads((ROOT/p).read_bytes())


def out(p):
    return json.loads((OUT/p).read_bytes())


def hexdigest(b):
    return sha256(b).hexdigest()


def subrows(payload, count):
    end = 13 + count*40
    req(payload[:8]==bytes.fromhex('03017461642ef10d') and S.unpack_from('<IB',payload,8)==(count,0), 'prefix')
    req(len(payload)==end+9 and payload[end:end+5]==b'\0\0\0\0\1', 'physical footer')
    return memoryview(payload)[13:end], S.unpack_from('<I',payload,end+5)[0]


def image_check(c, f):
    from t05_pe import PE
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    pe=PE(EXE)
    pe.pe.parse_data_directories(directories=[3])
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    req(hexdigest(pe.raw)==c['provenance']['editor_sha256']==EXE_SHA, 'editor SHA')
    manifest={i['path']:i['sha256'] for i in load('evidence/MANIFEST.json')['files']}
    for p in (MASTER,PROV):
        req(hexdigest((ROOT/p).read_bytes())==manifest[p]==c['provenance']['snapshot_manifest'][p], f'frozen {p}')
    req(manifest[MASTER].startswith('7d57477e') and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'), 'provenance')
    ins={}
    for shard in c['instruction_shards']:
        for r in out(shard)['instructions']:
            pc=int(r['file_offset'],16); va=int(r['VA'],16)
            x=next(md.disasm(pe.raw[pc:pc+15],va,count=1))
            req(pc not in ins and pe.va2f(va)==pc and pe.f2va(pc)==va and x.bytes.hex()==r['bytes']
                and f'{x.mnemonic} {x.op_str}'.rstrip()==r['instruction'],f'instruction row {pc:#x}')
            ins[pc]=x

    def dest(o):
        return pe.va2f(ins[o].operands[0].imm)

    def rip(o):
        i=ins[o]; return i.address+i.size+i.operands[1].mem.disp

    j=c['factory']; base=0xf49d38; cell=base+4*37
    req(rip(0xf48b45)==pe.f2va(base) and ins[0xf48b4c].op_str=='rax, dword ptr [rcx + rax*4]' and
        ins[0xf48b53].op_str=='rax' and j['jump_base']==base and j['cell']==cell and
        j['cell_bytes']==pe.raw[cell:cell+4].hex() and base+S.unpack_from('<i',pe.raw,cell)[0]==0xf49558, 'factory rel32 dispatch')
    req(rip(0xf49574)==0x14188e118 and ins[0xf4957b].op_str=='qword ptr [rsi], rax' and dest(0xf495aa)==0xf49ca9, 'factory constructed vfptr')
    vt=pe.va2f(0x14188e118); col=pe.va2f(S.unpack_from('<Q',pe.raw,vt-8)[0])
    sig,obj,_,td_rva=S.unpack_from('<4I',pe.raw,col); td=pe.r2f(td_rva)
    td_name=pe.raw[td+16:pe.raw.index(b'\0',td+16)]
    req(sig==1 and obj==0 and col==0x188d870==c['rtti']['col_off'] and td_name==b'.?AVSTARTING_TEAM_LEAGUE_HISTORY@db@@'
        and c['rtti']['class']=='STARTING_TEAM_LEAGUE_HISTORY', 'vtable/COL/TD')
    for k,v in {2:0x14119f210,19:0x14119e7f0,20:0x14119ea50,21:0x14119eb10}.items():
        req(S.unpack_from('<Q',pe.raw,vt+8*k)[0]==c['slots'][str(k)]==v,'vtable slot')
    r=c['reader']; reader_va=0x143fce190
    req(pe.va2f(reader_va)==r['entry']==START and int(r['entry_VA'],16)==reader_va and r['end_exclusive']==END
        and pe.va2f(0x14119e7f0)==r['thunk']==0x119ddf0 and ins[0x119ddf0].mnemonic=='jmp' and dest(0x119ddf0)==START,'slot19 tail thunk')
    rva=reader_va-pe.base
    runtime=[e.struct for e in pe.pe.DIRECTORY_ENTRY_EXCEPTION if e.struct.BeginAddress<=rva<e.struct.EndAddress]
    req(len(runtime)==1 and runtime[0].BeginAddress==rva and pe.r2f(runtime[0].EndAddress)==END
        and int(r['end_exclusive_VA'],16)==pe.f2va(END), 'real PE RUNTIME_FUNCTION extent')
    req(not any(e.struct.BeginAddress<=0x119e7f0<e.struct.EndAddress for e in pe.pe.DIRECTORY_ENTRY_EXCEPTION),'leaf thunk has no extent')
    # Build graph independently of ReaderCFG; compare every edge and block.
    seen, edges, stack = set(), {}, [START]
    while stack:
        o=stack.pop()
        if o in seen:
            continue
        seen.add(o)
        req(START<=o<END,'out-of-extent successor')
        i=ins[o]; targets=[]
        if i.mnemonic.startswith('j'):
            targets.append(dest(o))
        if i.mnemonic not in ('jmp','ret'):
            targets.append(o+i.size)
        edges[o]=targets
        stack.extend(targets)
    req(len(seen)==r['instruction_count']==164 and not r['external_edges'] and len(r['blocks'])==27,'reader CFG tally')
    coverage=[]
    for b in r['blocks']:
        pcs=b['sites']
        coverage.extend(pcs)
        for a,z in zip(pcs,pcs[1:]):
            req(edges[a]==[z] and not ins[a].mnemonic.startswith('j'),'block interior')
        req(sorted(edges[pcs[-1]])==b['successors'],'block exits')
    req(sorted(coverage)==sorted(seen),'block partition')
    allbranches=[b for shard in c['branch_shards'] for b in out(shard)['branches']]
    bs={b['site']:b for b in allbranches if b['scope']=='reader'}
    rs={o for o,v in edges.items() if len(v)==2}
    req(len(rs)==len(bs)==r['condition_count']==20 and bs.keys()==rs,'reader condition coverage')
    req(len(allbranches)==39 and len({b['site'] for b in allbranches})==39 and
        Counter(b['class'] for b in allbranches)==c['branch_census'] and
        c['branch_taxonomy']==['wire_data','runtime-external','IO-result','context-lifecycle','dead'],'branch ledger uniqueness/taxonomy')
    nonio={0x3e62ba2:'runtime-external',0x3e62d76:'context-lifecycle',0x3e62da7:'wire_data',
           0x3e62db4:'context-lifecycle',0x3e62dc8:'context-lifecycle',0x3e62dce:'context-lifecycle'}
    for b in allbranches:
        o,p=b['site'],b['predicate']; i=ins[o]; prior=ins[p]
        req(i.mnemonic.startswith('j') and i.mnemonic!='jmp' and b['taken_to']==dest(o) and b['fallthrough_to']==o+i.size
            and all(x in ins for x in b['evidence']),f'branch bytes {o:#x}')
        end=p+prior.size
        req(end==o or (o==0xffa640 and end+ins[end].size==o and ins[end].mnemonic=='mov'),'predicate flow')
        if o in bs:
            req(b['class']==nonio.get(o,'IO-result'), 'reader predicate class')
            taken=o in (0x3e62d6a,0x3e62da7,0x3e62dce)
            req((b['taken'],b['fallthrough'])==((N,0) if taken else (0,N)),'branch outcome')
            if o not in nonio:
                req(prior.op_str=='dword ptr [rbx + 0x10], 0' and
                    ((b['fallthrough_to'] if taken else b['taken_to'])==0x3e62d6c),'IO failure edge')
    req(ins[0x3e62b9d].op_str=='byte ptr [rsp + 0x70], 0' and ins[0xf2b670].op_str=='r12d, r9d'
        and ins[0xf2ba38].op_str=='byte ptr [rsp + 0x30], r12b','external mode chain')
    req(ins[0x3e62da0].op_str=='r8d, 0x989681' and ins[0x3e62dae].op_str=='dword ptr [rbx], r8d'
        and ins[0xf2ba3d].op_str=='dword ptr [rsp + 0x28], ebp','identity overwrite proof')
    req(ins[0xf2ba51].op_str=='qword ptr [rbx + 0x98]' and ins[0xf2ba33].op_str=='qword ptr [rsp + 0x38], rsi'
        and dest(0xf2ba23)==0xf48b30 and dest(0xf2ba7f)==0xffa5d0,'wrapper chain')
    req(c['transfers'][0]=={'site':0xf2ba0e,'wire_offset':0,'legacy_offset':-1,'width':1,'sink':'loader stack+0x43'}, 'selector coordinate')
    ts=c['transfers'][1:]
    req([(t['legacy_offset'],t['width'],t['object_offset'],t['site']) for t in ts]==[x[:4] for x in LAYOUT], 'independent geometry')
    for t in ts:
        o,w,obj=t['site'],t['width'],t['object_offset']
        l,wp,*_=t['setup']
        req(t['consumer']==o and ins[o].mnemonic=='call' and ins[o].op_str=='qword ptr [rax + 0x28]'
            and ins[l].mnemonic=='lea' and ins[l].operands[1].mem.disp==obj and ins[wp].operands[1].imm==w,
            'transfer native width/sink')
        req(ins[l].reg_name(ins[l].operands[1].mem.base)=='rsi' and t['wire_offset']==t['legacy_offset']+1,'object base/coordinate')
    other={o for o in seen if ins[o].mnemonic=='call'}-{x[3] for x in LAYOUT}
    req(other=={0x3e62dbf,0x3e62ddb},'all reader calls classified')
    for t in c['loader_transfers']:
        req(ins[t['consumer']].mnemonic=='call' and ins[t['consumer']].op_str=='qword ptr [rax + 0x28]'
            and ins[t['setup'][0]].operands[1].imm==t['width'],'loader width')
    req([(t['site'],t['width']) for t in c['loader_transfers']]==[(0xf2b691,4),(0xf2b6b1,1),(0xf2ba0e,1),
           (0xffa602,4),(0xffa7a8,4),(0xffa7c7,4),(0xffa7e6,4),(0xf2baa2,1),(0xf2bac2,4)], 'header/footer transfer summary')
    for v in c['scope_evidence'].values():
        req(all(o in ins for o in v),'scope evidence sites')
    req(ins[0xe8c334].operands[1].imm==int.from_bytes(b'Clhs','big') and dest(0xe8c33a)==0xe8d3b2
        and dest(0xe8d3bc)==0x1521d30 and dest(0x1521d30)==0x4344a40 and ins[0x4344b15].op_str=='rax, qword ptr [r14 + 0x20]','club scope arm')
    req(dest(0x119e110)==0x3e65630 and dest(0x119e050)==0x3e65540 and dest(0x3e65576)==0xf7e280 and dest(0xf7e280)==0x3bf3190
        and ins[0x3e6567b].op_str=='rax, qword ptr [r14 + 0x18]' and ins[0x3e65684].op_str=='eax, dword ptr [rax + 8]'
        and ins[0x3e65689].operands[1].imm==0xffffffff and ins[0x3bf322c].op_str=='rax, qword ptr [rcx + rax*8]'
        and ins[0x119eda9].operands[1].imm==int.from_bytes(b'comp','big'),'divi writer/fixup/getter proof')
    for field in f['fields']:
        g=field['getter']; code=field['code']; x=int.from_bytes(code.encode(),'big'); path=g['path']; cmp=None
        req(path[0]==0x119e810 and path[-1]==g['access'] and g['cmp'] in path and ins[g['cmp']].operands[1].imm==x,'getter anchor')
        for a,z in zip(path,path[1:]):
            i=ins[a]
            if i.mnemonic=='cmp':
                req(i.reg_name(i.operands[0].reg)=='edx','dispatch register')
                cmp=i.operands[1].imm
            nxt=a+i.size
            if i.mnemonic in ('jg','je','jne') and {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic]:
                nxt=dest(a)
            req(z==nxt,'4CC matched route')
        i=ins[path[-1]]; op=i.operands[1]
        req(i.reg_name(op.mem.base)=='rcx' and op.mem.disp==g['object_offset']==field['candidate_sink']['object_offset']
            and op.size==g['width']==(8 if code=='divi' else field['candidate_sink']['width']), 'getter sink join')
        if code not in ('year','divi'):
            a,b=g['sentinel_proof']
            req(i.mnemonic=='movsx' and a==path[-1]+i.size and b==a+ins[a].size and ins[a].op_str==('edi, edi' if code=='orde' else 'edi, -1')
                and ins[b].mnemonic=='je' and dest(b)==0x119ed61,'getter explicit optional sentinel')
        elif code=='year':
            req(i.mnemonic=='movzx' and not g['sentinel_proof'],'year unsigned/required')


def archive_check(c,f):
    import numpy as np
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); artifacts=c['archives']
    for a in ('client','server'):
        fn=a+'_db.dat'; p=db.DB_DIR/fn
        directory=codec['list_tables'](p,fn)
        e=[x for x in directory if x['table_id']==37]
        d=artifacts[a]
        req(len(directory)==d['directory_entry_count'] and e==d['table37_entries'] and d['present']==bool(e)
            and hexdigest(p.read_bytes())==d['archive_sha256'],f'{a} directory/sha')
    d=artifacts['client']
    req(not d['present'] and all(d[k] is None for k in ('row_count','stride','payload_sha256')),'client table37 absent, not empty')
    d=artifacts['server']; raw=db.load_payload(codec,'server',37)
    req(d['present'] and len(raw)==18628502==d['payload_len']==d['table37_entries'][0]['size']
        and hexdigest(raw)==d['payload_sha256']=='46d9c5a7750a1d0fd2279b5f92b88936e98c143bfa4a0bd5faded5d710ef4f30','server table37 payload')
    rows, high = subrows(raw,N)
    def column(wire,w,signed=False):
        return np.ndarray((N,),dtype=f'<{"i" if signed else "u"}{w}',buffer=rows,offset=wire,strides=(40,))
    rid, uid, uid2 = (column(o,4) for o in (28,32,36))
    req(np.all(column(0,1)==0) and np.array_equal(rid,np.arange(N,dtype=np.uint32)) and np.all(rid<10000001)
        and np.array_equal(uid,uid2) and len(np.unique(uid))==N and int(uid.min())==1 and int(uid.max())==high==98206088, 'every selector and identity; footer relation')
    terminal=13+N*40
    req(d['row_count']==N and d['stride']==40 and d['row_bytes']==N*40 and d['mode'] is True and
        d['wire_origin']==13 and d['legacy_origin']==14 and d['wire_footer_start']==terminal and d['legacy_footer_start']==terminal+1
        and d['wire_footer_hex']==raw[terminal:].hex() and d['legacy_footer_hex']==raw[terminal+1:].hex()
        and d['footer_values']==[0,1,high] and d['header_hex']==raw[:13].hex() and d['uid_min']==1 and d['uid_max']==high,'wire / legacy seal')
    req(d['footer_transfers']==[{'site':site,'offset':at,'width':w,'value':int.from_bytes(raw[at:at+w],'little')}
         for site,at,w in [(0xffa602,terminal,4),(0xf2baa2,terminal+4,1),(0xf2bac2,terminal+5,4)]],'footer trace')
    s29=load(T29); p29=s29['payload']; c29=s29['row_closure']
    req(c['t29']['profile']==T29 and hexdigest((ROOT/T29).read_bytes())==c['t29']['sha256'] and
        p29['payload_sha256']==hexdigest(raw) and (c29['row_start'],c29['stride'],c29['count'])==(14,40,N) and
        c29['rows_sha256']==c['t29']['legacy_rows_sha256']==hexdigest(raw[14:terminal+1]),'t29 legacy delta')
    fail=S.unpack_from('<3I',raw,14)
    req(fail==(6330,51,0xffffffff) and d['negative_forks'][0]['first_counterexample']==f'row 0: identity at 14 raw={fail}, stored ordinal={fail[0]}'
        and d['negative_forks'][0]['mode'] is False and d['negative_forks'][0]['consumed_per_reader']==12,'opposite mode first counterexample')
    observed=[[b['site'],bool(b['taken'])] for p in c['branch_shards'] for b in out(p)['branches'] if b['scope']=='reader']
    req(d['row_template']['condition_edges']==observed,'observed tape conditions')
    alt=[[o,(not t if o==0x3e62ba2 else t)] for o,t in observed if not 0x3e62ba2<o<0x3e62d70]
    req(d['negative_forks'][0]['conditions']==alt,'alternate tape conditions')
    for failure,(o,w,_,site,_) in zip(d['stream_failure_examples'],LAYOUT,strict=True):
        reason='reader has no immediate bulk status check' if w==12 else 'IO-result -> 0x3e62d6c (AL=false)'
        req(failure=={'site':site,'first_counterexample':f'row 0: short transfer @{14+o} width {w} site {site:#x}; {reason}'},'IO negative example')
    trace=sha256(); samples={r['ordinal']:r for r in d['samples']}
    req(samples.keys()=={0,216,6269,6472,114717,N//2,N-1},'sample coverage')
    for i,k in enumerate(range(13,terminal,40)):
        body=raw[k+1:k+40]; lanes=S.unpack_from('<III',body,27); bh=sha256(body).digest()
        trace.update(S.pack('<7I',i,k,k+1,k+40,*lanes)+bh)
        if i in samples:
            req(samples[i]=={'ordinal':i,'selector_start':k,'body_start':k+1,'body_end':k+40,'wire_hex':raw[k:k+40].hex(),
                             'identity':list(lanes),'body_sha256':bh.hex()},f'sampled row {i}')
    req(trace.hexdigest()==d['row_trace_sha256'],'all-row trace digest')
    comp=db.load_payload(codec,'client',25)
    req(f['reference_domain']=={'archive':'client','id':25,'count':7047,'payload_sha256':hexdigest(comp),'ordinal_legacy_offset':114}
        and len(comp)==14+7047*127+8 and S.unpack_from('<I',comp,8)[0]==7047,'comp ordinal source')
    comp_ids=np.ndarray((7047,),dtype='<u4',buffer=comp,offset=128,strides=(127,))
    req(np.array_equal(comp_ids,np.arange(7047,dtype=np.uint32)),'comp ordinals, not public UID')
    master=load(MASTER); scopes=[s for s in master['entities']['club.xml'][0]['fields'] if s['field']=='Clhs']
    req(len(scopes)==1 and len(scopes[0]['list_item_fields'])==12,'unique club.xml.Clhs')
    expected=scopes[0]['list_item_fields']
    t24=[v for p in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for v in load(p)['nested_fields'] if v['parent']=='Clhs']
    by_code={x[4]:x for x in LAYOUT if x[4]}
    cols={(p['offset'],p['width']):p for p in s29['columns'] if p['interpretation'] in ('u8','u16','u32')}
    grade=Counter()
    for record,spec,scope in zip(f['fields'],expected,t24,strict=True):
        code=spec['field']; o,w,obj,site,_=by_code[code]
        req(sum(x['field']==code for x in expected)==1 and record['code']==scope['code']==code and record['name']==spec['name']
            and record['schema']==spec and record['schema_scope']==['club.xml','Clhs',scope['idx']], 'scope and occurrence')
        req(record['candidate_sink']=={'legacy_offset':o,'wire_offset':o+1,'width':w,'reader_site':site,'object_offset':obj},'field to walked sink')
        xs=column(o+1,w,code!='year')
        sentinel=0 if code=='orde' else -1 if spec.get('is_optional')=='true' else None
        bounds=[int(spec[k]) for k in ('min_value','max_value')] if spec['type']=='integer' else None
        if bounds:
            ok=(xs>=bounds[0])&(xs<=bounds[1])
        else:
            req(code=='divi' and spec['database_table_type']=='competition','reference field target')
            ok=np.isin(xs,comp_ids)
        if sentinel is not None:
            ok |= xs==sentinel
        misses=np.flatnonzero(~ok)
        stats=[cols[o,w][k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
        us=column(o+1,w)
        req(stats==[N,len(np.unique(us)),int(us.min()),int(us.max()),int(np.count_nonzero(us==0)),int(np.count_nonzero(us==((1<<(8*w))-1)))],'all-row t29 unsigned differential')
        failures=[{'row':i,'value':int(xs[i]),'offset':14+i*40+o,'hex':raw[14+i*40+o:14+i*40+o+w].hex()} for i in map(int,misses[:5])]
        p=record['profile']
        req(p=={'count':N,'distinct':stats[1],'min':int(xs.min()),'max':int(xs.max()),'sentinel':sentinel,
                'sentinel_count':int(np.count_nonzero(xs==sentinel)) if sentinel is not None else 0,
                'zero_count':stats[4],'matches':N-len(misses),'violations':len(misses),'bounds':bounds,'first_violations':failures,
                'samples':{str(i):int(xs[i]) for i in (0,N//2,N-1)}, 't29_unsigned_stats':stats},f'{code} full profile')
        if code in HELD:
            req((len(misses),failures[0]['row'],failures[0]['value'])==HELD[code] and record['row_offset'] is None and record['wire_offset'] is None
                and record['grade']=='held_static_sink_profile_conflict',f'{code} held and first negative retained')
        else:
            req(not len(misses) and (record['row_offset'],record['wire_offset'])==(o,o+1) and record['grade']=='L3_named_row_coordinate',f'{code} all three gates')
        grade[record['grade']]+=1
    req(grade=={'L3_named_row_coordinate':8,'held_static_sink_profile_conflict':4} and
        f['occurrences']==12 and f['L3']==8 and f['baseline_L3']==0 and f['L4']==f['date_fields']==0, 'grade totals')


def verify():
    c=out('cursor_clhs.json'); f=out('fields_clhs.json')
    req(c['scope']==f['scope']==['club.xml','Clhs'] and c['table_type']==f['table_type']==37,'output scope')
    image_check(c,f)
    archive_check(c,f)
    print('t30 verify PASS: 465712 rows / 40 B; 27 blocks / 20 reader conditions; 8 L3, 4 held, L4=0')


def selftest():
    h=bytes.fromhex('03017461642ef10d0100000000'); b=b'\0'*40; f=S.pack('<IBI',0,1,3)
    rows,hi=subrows(h+b+f,1)
    req(bytes(rows)==b and hi==3, 'synthetic framing')
    for bad in (h+b+f[:-1],h+b+b'\x01'+f[1:],h[:12]+b'\1'+b+f):
        try:
            subrows(bad,1)
        except Reject:
            continue
        raise Reject('bad framing accepted')
    print('t30 verify selftest PASS')


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--selftest',action='store_true',help='check synthetic framing rejection')
    try:
        selftest() if a.parse_args().selftest else verify()
        return 0
    except Reject as e:
        print(f't30 verify FAIL: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't30 verify fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
