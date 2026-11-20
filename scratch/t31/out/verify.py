#!/usr/bin/env python3
"""Independently verify the CSrs/table 62 PE paths, archive seal and full field profiles."""
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
sys.path.insert(0,str(ROOT/'scripts'))
EXE = Path('<OLD_REPO>/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
T29 = 'scratch/t29/out/profiles/table_server_62.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_62.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
N, STRIDE = 37214,42
PAYLOAD_SHA = '978066bc07e96f2e75ee8909635052d778322219abc0f266a9a9aa01f0a0a485'
# Audit geometry transcribed independently from the native argument setups.
# Legacy offset, wire width, object displacement, consumer site, scoped code(s).
LAYOUT = (
    (0,1,0x44,0x3e5d755,('Ttyp',)), (1,4,0x18,0x3e5d775,()),
    (5,4,0x20,0x3e5d795,('Tdvi',)), (9,4,0x30,0x3e5d7b5,('Tsti',)),
    (13,4,0x38,0x3e5d7d5,('Catd',)), (17,4,0x3c,0x3e5d7f5,('Cmxa',)),
    (21,4,0x40,0x3e5d815,('Cmna',)), (25,1,0x45,0x3e5d831,('Twhm',)),
    (26,1,0x46,0x3e5d84d,('Tmhm',)), (27,1,0x47,0x3e5d869,('tmno','tmnv')),
    (28,1,0x48,0x3e5d885,()), (29,12,8,0x3c60119,()),
)
BY_CODE = {code:(o,w,obj,site) for o,w,obj,site,codes in LAYOUT for code in codes}
# For this frozen input these independent console checks also pin sentinel or true counts.
SENTINELS = {'Ttyp':(-1,0),'Tdvi':(-1,29922),'Tsti':(-1,30311),'Twhm':(0,33197),'Tmhm':(0,33899)}
MASKS = {'tmno':(4,23792),'tmnv':(2,451)}
KINDS = {'Ttyp':'i8','Twhm':'i8','Tmhm':'i8','Tdvi':'ordinal','Tsti':'ordinal',
         'tmno':'bool','tmnv':'bool','Catd':'i32','Cmna':'i32','Cmxa':'i32'}


class Reject(Exception):
    pass


def req(ok, why):
    if not ok:
        raise Reject(why)


def read(p):
    return json.loads(p.read_bytes())


def sha(b):
    return sha256(b).hexdigest()


def wire(buf,count):
    end=13+42*count
    req(buf[:8]==bytes.fromhex('03017461642ef10d') and len(buf)==end+9,'header/envelope')
    req(S.unpack_from('<IB',buf,8)==(count,0) and buf[end:end+5]==bytes.fromhex('0000000001'),'header fields/footer prefix')
    return memoryview(buf)[13:end],S.unpack_from('<I',buf,end+5)[0]


def pe_check(c,f):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from t05_pe import PE
    pe=PE(EXE);pe.pe.parse_data_directories(directories=[3])
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    req(sha(pe.raw)==c['provenance']['editor_sha256']==EXE_SHA,'editor SHA')
    manifest={r['path']:r['sha256'] for r in read(ROOT/'evidence/MANIFEST.json')['files']}
    for p in (MASTER,PROV):
        req(sha((ROOT/p).read_bytes())==manifest[p]==c['provenance']['snapshot_manifest'][p],f'frozen {p}')
    req(manifest[MASTER].startswith('7d57477e') and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'),'snapshot provenance')
    ins={}
    for part in c['instruction_shards']:
        for r in read(OUT/part)['instructions']:
            o,va=int(r['file_offset'],16),int(r['VA'],16)
            i=next(md.disasm(pe.raw[o:o+15],va,count=1))
            req(o not in ins and pe.va2f(va)==o and pe.f2va(o)==va and i.bytes.hex()==r['bytes'] and
                f'{i.mnemonic} {i.op_str}'.rstrip()==r['instruction'],f'PE bytes/VA {o:#x}')
            ins[o]=i

    def dest(o):
        i=ins[o]; req(i.operands[0].type==2,f'indirect {o:#x}')
        return pe.va2f(i.operands[0].imm)

    def rip(o):
        i=ins[o]; return i.address+i.size+i.operands[1].mem.disp

    def text(o,s):
        req(ins[o].op_str==s,f'operand {o:#x}: {s}')

    vf=0x141884988; base=0xf49d38; cell=base+4*62
    j=c['factory']; rel=S.unpack_from('<i',pe.raw,cell)[0]
    req(rip(0xf48b45)==pe.f2va(base) and base+rel==0xf49a2b and (j['jump_base'],j['cell'],j['rel32'],j['cell_bytes'])==
        (base,cell,rel,pe.raw[cell:cell+4].hex()),'factory rel32')
    text(0xf48b4c,'rax, dword ptr [rcx + rax*4]'); text(0xf48b53,'rax'); text(0xf49a5f,'qword ptr [rsi], rax')
    req(rip(0xf49a58)==vf and dest(0xf49a99)==0xf49ca9,'constructor vptr/return')
    vt=pe.va2f(vf); col=pe.va2f(S.unpack_from('<Q',pe.raw,vt-8)[0]); sig,obj,_,tdrv=S.unpack_from('<4I',pe.raw,col)
    td=pe.r2f(tdrv)
    req(sig==1 and obj==0 and col==0x18840e0==c['rtti']['col_off'] and
        pe.raw[td+16:pe.raw.index(0,td+16)]==b'.?AVSTARTING_RESERVE_TEAM@db@@' and
        c['rtti']['class']=='STARTING_RESERVE_TEAM','RTTI descriptor')
    for k,v in {2:0x14119d0f0,19:0x14119c960,20:0x14119caf0,21:0x14119cb60}.items():
        req(S.unpack_from('<Q',pe.raw,vt+k*8)[0]==c['slots'][str(k)]==v,'vtable slot')
    reader=c['reader']
    req(reader['chain']==[0x119bf60,0x3e5d730,0x3e5d8af,0xfae340,0x3c600f0] and not reader['runtime_mode_forks'],'reader chain/mode')
    for a,b in [(0x119bf60,0x3e5d730),(0x3e5d8af,0xfae340),(0xfae340,0x3c600f0)]:
        req(ins[a].mnemonic=='jmp' and dest(a)==b,'real tail jumps')
    entries=[e.struct for e in pe.pe.DIRECTORY_ENTRY_EXCEPTION]
    def extent(o):
        rv=pe.f2va(o)-pe.base
        return [e for e in entries if e.BeginAddress<=rv<e.EndAddress]
    for o in (0x119bf60,0xfae340):
        req(not extent(o),'leaf thunk unexpectedly has extent')
    internal={}
    for d,(start,end,ic,bc) in zip(reader['extents'],[(0x3e5d730,0x3e5d8b4,113,13),(0x3c600f0,0x3c6016e,43,11)],strict=True):
        rt=extent(start)
        req(len(rt)==1 and pe.r2f(rt[0].BeginAddress)==d['entry']==start and pe.r2f(rt[0].EndAddress)==d['end_exclusive']==end
            and int(d['entry_VA'],16)==pe.f2va(start) and int(d['end_exclusive_VA'],16)==pe.f2va(end),'runtime-function extent')
        graph={}; external=[]; todo=[start]
        while todo:
            o=todo.pop()
            if o in graph:
                continue
            i=ins[o]; successors=[]
            if i.mnemonic.startswith('j'):
                t=dest(o)
                if not start<=t<end:
                    external.append({'from':hex(o),'kind':'tail_jump','target_va':hex(pe.f2va(t))})
                else:
                    successors.append(t)
            if i.mnemonic not in ('jmp','ret'):
                req(o+i.size<end,'fallthrough beyond runtime extent')
                successors.append(o+i.size)
            graph[o]=successors;todo.extend(successors)
        req(len(graph)==d['instruction_count']==ic and len(d['blocks'])==bc and external==d['external_edges'],'reachable extent graph')
        covered=[]
        for b in d['blocks']:
            sites=b['sites']; covered+=sites
            req(sites and all(graph[a]==[z] and not ins[a].mnemonic.startswith('j') for a,z in zip(sites,sites[1:])) and
                sorted(graph[sites[-1]])==b['successors'],'block path/exits')
        req(sorted(covered)==sorted(graph),'disjoint complete blocks')
        internal.update(graph)
    req({o for o in internal if ins[o].mnemonic=='call'}=={t[3] for t in LAYOUT}|{0x3c60149,0x3c60162},'every reader call accounted for')
    text(0x3e5d739,'r14, r9');text(0x3e5d8a3,'r9, r14');text(0x3c60146,'r9b, 1')
    text(0xf2ba38,'byte ptr [rsp + 0x30], r12b');text(0xf2ba33,'qword ptr [rsp + 0x38], rsi');text(0xf2ba3d,'dword ptr [rsp + 0x28], ebp')
    text(0x3c60122,'rcx, qword ptr [rsp + 0x78]');text(0x3c60133,'r8d, dword ptr [rsp + 0x68]');text(0x3c6012a,'r8d, 0x989681')
    text(0x3c60138,'dword ptr [rbx], r8d');text(0xf2ba51,'qword ptr [rbx + 0x98]')
    req(dest(0xf2ba23)==0xf48b30 and dest(0xf2ba7f)==0xffa5d0,'loader dispatch/footer helper')
    bs=[b for p in c['branch_shards'] for b in read(OUT/p)['branches']]
    by_site={b['site']:b for b in bs}
    cond={o for o,t in internal.items() if len(t)==2}
    req(len(bs)==len(by_site)==36 and {b['site'] for b in bs if b['scope']!='loader_footer_factory_slice'}==cond and
        len(cond)==reader['condition_count']==16,'branch inventory')
    req(c['branch_taxonomy']==['wire_data','runtime-external','IO-result','context-lifecycle','dead'] and
        Counter(b['class'] for b in bs)==c['branch_census']=={'IO-result':22,'context-lifecycle':7,'wire_data':6,'runtime-external':1},'branch sources')
    members={t[3] for t in LAYOUT[:-1]}
    for b in bs:
        o,p=b['site'],b['predicate'];prior=ins[p]; after=p+prior.size
        req(ins[o].mnemonic.startswith('j') and ins[o].mnemonic!='jmp' and b['taken_to']==dest(o) and b['fallthrough_to']==o+ins[o].size
            and all(x in ins for x in b['evidence']) and b['alternative_or_first_counterexample'],f'branch evidence {o:#x}')
        req(after==o or (o==0xffa640 and ins[after].mnemonic=='mov' and after+ins[after].size==o),'predicate flags stay live')
        if o in cond:
            taken=o in (0x3e5d88c,0x3c60131,0x3c60155)
            req((b['taken_count'],b['fallthrough_count'],b['observed_edge'])==((N,0,'taken') if taken else (0,N,'fallthrough')),'reader branch observations')
            if o>=0x3e5d730:
                req(b['class']=='IO-result' and b['evidence'][0] in members and prior.op_str=='dword ptr [rsi + 0x10], 0' and
                    (b['fallthrough_to'] if taken else b['taken_to'])==0x3e5d88e,'property IO result before next read')
            else:
                req(b['class']==('wire_data' if o==0x3c60131 else 'context-lifecycle'),'identity-tail predicate origin')
    req(c['transfers'][0]=={'site':0xf2ba0e,'legacy_offset':-1,'wire_offset':0,'width':1,'sink':'loader stack+0x43'},'loader selector')
    tape=c['transfers'][1:]
    req([(r['legacy_offset'],r['width'],r['object_offset'],r['site']) for r in tape]==[t[:4] for t in LAYOUT],'walk layout')
    for r in tape:
        o=r['site']; l,w,*_=r['setup']; operand=ins[l].operands[1]
        base={0x3e5d755:'rcx',0x3c60119:'rdi'}.get(o,'rbx')
        req(ins[o].mnemonic=='call' and ins[o].op_str=='qword ptr [rax + 0x28]' and r['consumer']==o and
            ins[l].mnemonic=='lea' and ins[l].reg_name(operand.mem.base)==base and operand.mem.disp==r['object_offset'] and
            ins[w].operands[1].imm==r['width'] and r['wire_offset']==r['legacy_offset']+1,'transfer exact sink/width')
    seq,used=[],[]
    o=0x3e5d730
    for _ in range(len(internal)+2):
        if o in {r['site'] for r in tape}:
            used.append(o)
        if o in cond:
            b=by_site[o]; t=b['observed_edge']=='taken'; seq.append([o,t])
            o=b['taken_to' if t else 'fallthrough_to']
        elif ins[o].mnemonic=='ret':
            break
        elif o in (0x3e5d8af,0xfae340):
            o=dest(o)
        else:
            o,=internal[o]
    req(o==0x3c6016d and used==[r['site'] for r in tape] and seq==c['archives']['server']['row_template']['condition_edges'],'executed success edge order')
    loader=c['loader_transfers']
    req([(t['site'],t['width']) for t in loader]==[(0xf2b691,4),(0xf2b6b1,1),(0xf2ba0e,1),(0xffa602,4),
         (0xffa7a8,4),(0xffa7c7,4),(0xffa7e6,4),(0xf2baa2,1),(0xf2bac2,4)],'outer transfer summary')
    for r in loader:
        req(r['consumer']==r['site'] and ins[r['consumer']].op_str=='qword ptr [rax + 0x28]' and
            ins[r['setup'][0]].operands[1].imm==r['width'],'loader native setup')

    req(all(o in ins for part in c['scope_evidence'].values() for o in part),'scope evidence references')
    req(ins[0xe8b6f0].operands[1].imm==int.from_bytes(b'CSrs','big') and
        [dest(o) for o in (0xe8b6f6,0xe8e286,0x152a840)]==[0xe8e27c,0x152a840,0x4354a30],'scoped collection')
    text(0x4354b01,'qword ptr [r14 + 0x18], rbx')
    req([dest(o) for o in (0x119c0f0,0x119c160,0x3e5d9d7,0xf7e280,0x3e5d9e9,0xf7f340)]==
        [0x3e5d990,0x3e5e690,0xf7e280,0x3bf3190,0xf7f340,0x3bf6ec0],'ref fixup/writer chain')
    for a,z,null,disp in [(0x3e5e722,0x3e5e72b,0x3e5e730,0x20),(0x3e5e75a,0x3e5e763,0x3e5e768,0x30)]:
        text(a,f'rax, qword ptr [rdi + {disp:#x}]');text(z,'eax, dword ptr [rax + 8]');text(null,'eax, 0xffffffff')
    text(0x3bf322c,'rax, qword ptr [rcx + rax*8]');text(0x3bf6f9a,'rax, qword ptr [rcx + rax*8]')
    text(0x119cd37,'edx, 0x636f6d70');text(0x119cd97,'edx, 0x73746164')
    req(dest(0x119ccae)==0x119c9fc and dest(0x119cc91)==0x119cd83,'reference null check')
    for r in f['fields']:
        code=r['code'];g=r['getter']; route=g['route']; x=int.from_bytes(code.encode(),'big'); cmp=None
        req(route[0]==0x119c6f0 and route[-1]==g['access'] and g['compare'] in route and
            ins[g['compare']].operands[1].imm==x,'unique 4CC route anchor')
        for a,b in zip(route,route[1:]):
            i=ins[a]
            if i.mnemonic=='cmp':
                req(i.op_str.startswith('edx, '),'getter dispatch predicate')
                cmp=i.operands[1].imm
            z=a+i.size
            if i.mnemonic.startswith('j') and {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic]:
                z=dest(a)
            req(z==b,'getter path edge')
        i=ins[g['access']];m=i.operands[1]; w=BY_CODE[code][1];kind=KINDS[code]
        req(i.mnemonic=={'i8':'movsx','i32':'mov','ordinal':'mov','bool':'movzx'}[kind] and i.reg_name(m.mem.base)=='rcx'
            and m.mem.disp==g['object_offset']==BY_CODE[code][2] and m.size==g['width']==(8 if kind=='ordinal' else w),'getter to actual member')
        if kind=='i8':
            a,b=g['proof']; text(a,'edi, -1' if code=='Ttyp' else 'edi, edi')
            req(a==g['access']+i.size and b==a+ins[a].size and ins[b].mnemonic=='je' and dest(b)==0x119cc0f,'signed byte sentinel')
        elif kind=='bool':
            a,b,z=g['proof'];text(a,f'bl, {MASKS[code][0].bit_length()-1}');text(b,'bl, 1');text(z,'byte ptr [rbp - 8], bl')
            req(ins[a].mnemonic=='shr' and ins[b].mnemonic=='and' and z==b+ins[b].size,'flag mask and bool output')
        elif kind=='i32':
            a,b,z=g['proof'];req(a==g['access']+i.size and b==a+ins[a].size and z==b+ins[b].size and dest(a)==0x83caf0,'attendance boxes direct i32')
            text(z,'dword ptr [rbp - 8], edi')
    return bs


def archive_check(c,f,branches):
    import numpy as np
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); ar=c['archives']
    for a,entries in [('client',31),('server',77)]:
        fn=a+'_db.dat'; disk=db.DB_DIR/fn; shard=ar[a]
        all_bytes=disk.read_bytes(); d=codec['list_tables'](disk,fn)
        hit=[r for r in d if r['table_id']==62]
        req(len(d)==shard['directory_entry_count']==entries and hit==shard['table62_entries'] and
            shard['present']==bool(hit) and sha(all_bytes)==shard['archive_sha256'],f'{a} directory/archive fingerprint')
        if a=='client':
            req(not hit and all(shard[k] is None for k in ('row_count','stride','payload_sha256')),'absent not empty')
        else:
            e,=hit; offset=e['offset']; frame=all_bytes.index(db.MAGIC,offset,offset+64)
            req(offset==26649596 and frame==26649630==shard['zstd_frame_offset'],'server directory offset and frame offset')
            raw=codec['_stream_decompress'](all_bytes[frame:],256*1024*1024)
    d=ar['server']; rows,hi=wire(raw,N);end=13+42*N
    req(len(raw)==d['payload_len']==e['size']==1563010 and sha(raw)==d['payload_sha256']==PAYLOAD_SHA and
        (e['payload_version'],e['record_count_header'])==(3569,N),'table62 payload')
    def col(wire_o,w,sign=False):
        return np.ndarray((N,),dtype=f'<{"i" if sign else "u"}{w}',buffer=rows,offset=wire_o,strides=(42,))
    selector=col(0,1); rid,u,v=(col(o,4) for o in (30,34,38))
    req(np.all(selector==0) and np.array_equal(rid,np.arange(N)) and np.all(rid<10000001) and np.array_equal(u,v) and
        np.unique(u).size==N and int(u.min())==1 and int(u.max())==hi==N,'selector, raw ordinal and duplicate identity lanes')
    req((d['row_count'],d['stride'],d['row_bytes'],d['wire_origin'],d['legacy_origin'],d['wire_footer_start'],d['legacy_footer_start'])==
        (N,42,42*N,13,14,end,end+1) and d['header_hex']==raw[:13].hex() and d['wire_footer_hex']==raw[end:].hex() and
        d['legacy_footer_hex']==raw[end+1:].hex() and d['footer_values']==[0,1,hi] and (d['uid_min'],d['uid_max'])==(1,hi) and
        d['selector_histogram']=={'0':N},'physical/legacy closure and footer observations')
    req(d['footer_transfers']==[dict(site=o,offset=k,width=w,value=int.from_bytes(raw[k:k+w],'little')) for o,k,w in
        [(0xffa602,end,4),(0xf2baa2,end+4,1),(0xf2bac2,end+5,4)]],'footer offsets/sinks')
    samples={s['ordinal']:s for s in d['samples']}; trace=sha256()
    req(len(samples)==len(d['samples']) and samples.keys()=={0,1,2,N//2,N-1},'sample coverage')
    for i,k in enumerate(range(13,end,42)):
        lanes=S.unpack_from('<3I',raw,k+30); bh=sha256(raw[k+1:k+42]).digest()
        trace.update(S.pack('<7I',i,k,k+1,k+42,*lanes)+bh)
        if i in samples:
            req(samples[i]==dict(ordinal=i,selector_start=k,body_start=k+1,body_end=k+42,identity=list(lanes),
                                 body_sha256=bh.hex(),wire_hex=raw[k:k+42].hex()),f'row sample {i}')
    req(trace.hexdigest()==d['row_trace_sha256'],'all-row trace digest')
    neg=d['negative_replays']; errors={}
    for o,w,_,site,_ in LAYOUT:
        reason='no immediate native bulk status test' if w==12 else 'IO-result -> 0x3e5d88e (AL=false)'
        errors[site]=f'row 0: short transfer @{14+o} width {w} site {site:#x}; {reason}'
    req(neg['short_transfers']==[{'site':o,'first_counterexample':e} for o,e in errors.items()],'IO cut first negatives')
    for b in branches:
        if b['scope']=='reader':
            req(b['alternative_or_first_counterexample']==errors[b['evidence'][0]],'branch negative paired to native transfer')
    r,a,b=S.unpack_from('<3I',raw,43)
    req((r,a,b)==(0,1,1) and neg['overwrite_does_not_mask_raw_error']==f'row 0: identity @43 raw={(10000001,a,b)}, stored ordinal=0' and
        neg['duplicate_lane_mismatch']==f'row 0: identity @43 raw={(r,a,0)}, stored ordinal=0' and
        neg['selector_out_of_observed_domain']=='row 0: selector 1 @13 outside observed domain (not factory rejection)','other raw first negatives')

    p=read(ROOT/T29); t=c['t29']; rc=p['row_closure']; rr=(ROOT/ROWS).read_bytes()
    req(t['profile']==T29 and t['rows']==ROWS and t['matched_full_rows']==N and t['profile_sha256']==sha((ROOT/T29).read_bytes()) and
        p['payload']['payload_sha256']==PAYLOAD_SHA and p['payload']['packed_offset']==26649630 and
        sha(rr)==p['full_rows_sha256']==t['rows_sha256'] and sha(raw[14:end+1])==rc['rows_sha256']==t['legacy_block_sha256'] and
        (rc['row_start'],rc['row_end_exclusive'],rc['count'],rc['stride'])==(14,end+1,N,42),'t29 independent snapshot/delta')
    for i,(k,line) in enumerate(zip(range(14,end+1,42),rr.splitlines(),strict=True)):
        rec=json.loads(line)
        req((rec['offset'],rec['row'],rec['len'])==(k,i,42) and bytes.fromhex(rec['raw_hex'])==raw[k:k+42],f't29 legacy row {i}')
    if t['inventory'] is not None:
        q,=[r for r in read(ROOT/INV)['parents'] if r['parent_4cc']=='CSrs']
        req(t['inventory']['path']==INV and t['inventory']['sha256']==sha((ROOT/INV).read_bytes()) and
            (q['table_type'],q['count'],q['stride'],q['status'])==(62,N,42,t['inventory']['status']),'t29 inventory')
    refs={}
    for key,tid,n,w,o in [('competition',25,7047,127,114),('stadium',21,48413,38,25)]:
        buf=db.load_payload(codec,'client',tid)
        req(f['reference_domains'][key]==dict(archive='client',table_type=tid,count=n,stride=w,ordinal_legacy_offset=o,payload_sha256=sha(buf)) and
            len(buf)==14+n*w+8 and S.unpack_from('<I',buf,8)[0]==n,'target member framing and fingerprint')
        ids=np.ndarray((n,),dtype='<u4',buffer=buf,offset=14+o,strides=(w,))
        req(np.array_equal(ids,np.arange(n)),'target identity ordinal domain, not UID')
        refs[key]=ids
    m=read(ROOT/MASTER); parent,=[x for x in m['entities']['club.xml'][0]['fields'] if x['field']=='CSrs']; specs=parent['list_item_fields']
    occ=[x for file in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for x in read(file)['nested_fields'] if x['parent']=='CSrs']
    req(len(specs)==len({s['field'] for s in specs})==len(occ)==10 and [x['idx'] for x in occ]==list(range(93,103)),'unique 10 scoped occurrences')
    unsigned={(q['offset'],q['width']):q for q in p['columns'] if q['interpretation'] in ('u8','u16','u32')}
    grades=Counter()
    def hist(x):
        v,n=np.unique(x,return_counts=True)
        return {str(int(a)):int(b) for a,b in zip(v,n)}
    for r,s,t in zip(f['fields'],specs,occ,strict=True):
        code=s['field']; o,w,obj,site=BY_CODE[code]; kind=KINDS[code]; typ=s['type']
        req(r['schema']==s and r['name']==t['name']==s['name'] and r['code']==t['code']==code and t['type']==typ and
            r['schema_scope']==['club.xml','CSrs',t['idx']] and r['interpretation']==kind,'scope ledger join')
        req(r['candidate_sink']==dict(legacy_offset=o,wire_offset=o+1,width=w,object_offset=obj,reader_site=site),'field sink coordinates')
        us=col(o+1,w); xs=col(o+1,w,kind!='bool'); sentinel,want_s=SENTINELS.get(code,(None,0)); mask=None
        if typ=='enum':
            live=[int(v['enum']) for v in m['enums'][s['enum_ref']]['values']]; ok=np.isin(xs,live)
            req(r['domain']==dict(frozen_enum='Rsty',values=sorted(live)),'Rsty code domain')
        elif typ=='database_record_unique_id':
            key=s['database_table_type']; ids=refs[key]; ok=np.isin(xs,ids)
            req(r['domain']==dict(target_ordinal=key,bounds=[0,len(ids)-1]),'reference target domain')
        elif typ=='day_of_week':
            ok=(xs>=1)&(xs<=7); req(r['domain']['live_values']==list(range(1,8)),'weekday category codes')
        elif typ=='boolean':
            mask,true=MASKS[code]; xs=(us&mask)!=0; ok=np.isin(xs,[0,1]); req(int(xs.sum())==true and
                r['domain']==dict(decoded_values=[0,1],mask=mask),'exact individual bit domain')
        else:
            req(typ=='integer','integer schema')
            lo,hi=int(s['min_value']),int(s['max_value']); ok=(xs>=lo)&(xs<=hi)
            req(r['domain']==dict(xml_bounds=[lo,hi]),'XML integer bounds')
        matches_s=int(np.count_nonzero(xs==sentinel)) if sentinel is not None else 0
        if sentinel is not None:
            ok|=xs==sentinel
        misses=np.flatnonzero(~ok)
        limits=[unsigned[o,w][k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')]
        req(limits==[N,len(np.unique(us)),int(us.min()),int(us.max()),int((us==0).sum()),int((us==(1<<(8*w))-1).sum())],'t29 unsigned profile')
        fail=[]
        for k in map(int,misses[:5]):
            at=14+k*42+o;fail.append(dict(row=k,offset=at,value=int(xs[k]),hex=raw[at:at+w].hex()))
        distinct=len(np.unique(xs)); live=xs if sentinel is None else xs[xs!=sentinel]
        req(matches_s==want_s and r['bit_mask']==mask and r['profile']==dict(count=N,distinct=distinct,min=int(xs.min()),max=int(xs.max()),
            zero_count=int((xs==0).sum()),sentinel=sentinel,sentinel_count=matches_s,live_count=len(live),
            live_min=int(live.min()) if len(live) else None,live_max=int(live.max()) if len(live) else None,
            matches=N-len(misses),violations=len(misses),
            first_violations=fail,histogram=hist(xs) if distinct<=100 else None,samples={str(i):int(xs[i]) for i in (0,N//2,N-1)},
            t29_unsigned_stats=limits,raw_shared_byte_histogram=hist(us) if mask else None),f'{code} full-profile replay')
        expected_grade='held_static_sink_profile_conflict' if len(misses) else 'L3_named_row_coordinate'; grades[expected_grade]+=1
        req(r['grade']==expected_grade and (r['row_offset'],r['wire_offset'])==((None,None) if len(misses) else (o,o+1)),f'{code} promotion/hold')
    req(grades=={'L3_named_row_coordinate':10} and f['L3']==f['occurrences']==10 and f['date_fields']==f['baseline_L3']==f['L4']==0,'grade totals')


def verify():
    c=read(OUT/'cursor_csrs.json');f=read(OUT/'fields_csrs.json')
    req(c['scope']==f['scope']==['club.xml','CSrs'] and c['table_type']==f['table_type']==62,'output scope')
    archive_check(c,f,pe_check(c,f))
    print('t31 verify PASS: 37214 rows / 42 B; 24 reader/tail blocks / 16 conditions; 10 L3, 0 held, L4=0')


def selftest():
    h=bytes.fromhex('03017461642ef10d0100000000');r=bytes(42);f=S.pack('<IBI',0,1,7)
    rows,hi=wire(h+r+f,1);req(bytes(rows)==r and hi==7,'synthetic physical envelope')
    for bad in (h+r+f[:-1],h+r+b'\x01'+f[1:],h[:12]+b'\x01'+r+f):
        try:
            wire(bad,1)
        except Reject:
            continue
        raise Reject('invalid envelope accepted')
    print('t31 verify selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='check a synthetic physical envelope and rejection paths')
    try:
        selftest() if p.parse_args().selftest else verify()
        return 0
    except Reject as e:
        print(f't31 verify FAIL: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't31 verify fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
