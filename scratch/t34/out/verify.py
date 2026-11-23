#!/usr/bin/env python3
"""Independently verify the table-66 native cursor and scoped field evidence."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import struct as S
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
EXE = Path('D:/tmp2b/fm24/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PROFILE = 'scratch/t29/out/profiles/table_server_66.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_66.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
OCC = 'scratch/t24/out/subtables.part001.json'
NATION = 'scratch/t25/out/cursor_nation.json'
PAYLOAD_SHA = '3ddd47bbeec04ff6789dafdfe40148367abc4373700b082452fc79be06e02911'
N,W = 753,24
CHAIN = [0x152f720,0x43583b0,0x4358475,0xfae340,0x3c600f0]
# Transcribed from native call order. legacy, width, object, call, destination setup, width setup.
LAYOUT = [(0,4,0x18,0x43583d9,0x43583c9,0x43583d0),(4,4,0x1c,0x43583f5,0x43583e5,0x43583ec),
          (8,1,0x20,0x4358411,0x4358401,0x4358408),(9,1,0x21,0x435842d,0x435841d,0x4358424),
          (10,1,0x22,0x4358449,0x4358439,0x4358440),(11,12,8,0x3c60119,0x3c60106,0x3c6010d)]
STATUS = dict(zip((0x43583e0,0x43583fc,0x4358418,0x4358434,0x4358450),[t[3] for t in LAYOUT[:5]],strict=True))
ARMS = {'nati':(0x152faf0,'mov',1),'rati':(0x152fbaa,'movsx',2),'mina':(0x152fa79,'movzx',3),'maxa':(0x152fb4e,'movzx',4)}
OUTER = {'wire_data':{0xf2b9db,0xf2b9fa,0xffa610,0xffa733,0xffa77f},'runtime-external':{0xf48b3b},
         'IO-result':{0xf2b698,0xf2b6b8,0xf2ba15,0xf2baa9,0xf2bac9,0xffa7af,0xffa7ce,0xffa7ed,0xffa7fa,0xf2ba89,0xf2ba59},
         'context-lifecycle':{0xf2ba2b,0xf2ba6c,0xffa640},'dead':set()}
FOOT = (0xffa602,0xf2baa2,0xf2bac2)


class Reject(Exception):
    pass


def req(ok, why):
    if not ok:
        raise Reject(why)


def js(p):
    return json.loads(p.read_bytes())


def sha(buf):
    return sha256(buf).hexdigest()


def pe_check(c,f):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from t05_pe import PE
    pe=PE(EXE); pe.pe.parse_data_directories(directories=[3]); md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    req(sha(pe.raw)==c['provenance']['editor_sha256']==EXE_SHA,'editor SHA')
    man={r['path']:r['sha256'] for r in js(ROOT/'evidence/MANIFEST.json')['files']}
    for p in MASTER,PROV:
        req(sha((ROOT/p).read_bytes())==man[p]==c['provenance']['snapshot_manifest'][p],'frozen SHA '+p)
    req(man[MASTER].startswith('7d57477e') and EXE_SHA in (ROOT/PROV).read_text(encoding='utf-8'),'provenance')
    ins={}
    for part in c['instruction_shards']:
        for r in js(OUT/part)['instructions']:
            o,va=int(r['file_offset'],16),int(r['VA'],16); i=next(md.disasm(pe.raw[o:o+15],va,count=1))
            req(o not in ins and pe.va2f(va)==o and pe.f2va(o)==va and i.bytes.hex()==r['bytes'] and
                f'{i.mnemonic} {i.op_str}'.rstrip()==r['instruction'],f'shard PE bytes/VA {o:#x}')
            ins[o]=i
    def dest(o):
        return pe.va2f(ins[o].operands[0].imm)
    def rip(o):
        i=ins[o]; return i.address+i.size+i.operands[1].mem.disp
    def text(o,s):
        req(ins[o].op_str==s,f'operand {o:#x}: {s}')
    vf=0x141884e08; base=0xf49d38; cell=base+4*66; rel,=S.unpack_from('<i',pe.raw,cell); j=c['factory']
    req(rip(0xf48b45)==pe.f2va(base) and base+rel==0xf49b18 and
        (j['jump_base'],j['cell'],j['rel32'],j['cell_bytes'])==(base,cell,rel,pe.raw[cell:cell+4].hex()),'factory rel32 encoding')
    o=base+rel
    while o<0xf49b54:
        req(not ins[o].mnemonic.startswith('j'),'case constructor selector independence'); o+=ins[o].size
    req(o==0xf49b54 and ins[o].mnemonic=='jmp' and dest(o)==0xf49ca9 and rip(0xf49b3c)==vf,'constructor vptr')
    text(0xf49b43,'qword ptr [rsi], rax'); text(0xf49b46,'qword ptr [rsi + 0x18], 0xffffffffffffffff')
    vt=pe.va2f(vf); col=pe.va2f(S.unpack_from('<Q',pe.raw,vt-8)[0]); sig,obj,_,tdrv=S.unpack_from('<4I',pe.raw,col); td=pe.r2f(tdrv)
    decorated='.?AVSTARTING_CLUB_TRANSFER_PREFERENCE@db@@'
    req(sig==1 and obj==0 and col==c['rtti']['col_off']==0x1885660 and td==c['rtti']['td_off'] and
        pe.raw[td+16:pe.raw.index(0,td+16)].decode()==c['rtti']['decorated']==decorated,'RTTI actual COL/TD')
    for k,v in {2:0x141530440,3:0x141530750,19:0x141530120,20:0x1400015e0,21:0x1415301f0}.items():
        req(S.unpack_from('<Q',pe.raw,vt+k*8)[0]==c['slots'][str(k)]==v,'vtable slots')
    r=c['reader']; req(r['chain']==CHAIN and not r['runtime_mode_forks'],'reader chain/no mode fork')
    for a,b in ((CHAIN[0],CHAIN[1]),(CHAIN[2],CHAIN[3]),(CHAIN[3],CHAIN[4])):
        req(ins[a].mnemonic=='jmp' and dest(a)==b,'tail chain')
    entries=[e.struct for e in pe.pe.DIRECTORY_ENTRY_EXCEPTION]
    def ext(o):
        rv=pe.f2va(o)-pe.base; return [e for e in entries if e.BeginAddress<=rv<e.EndAddress]
    req(not ext(CHAIN[0]) and not ext(CHAIN[3]),'leaf thunks outside pdata extents')
    graph={}
    for d,(start,end,ni,nb) in zip(r['extents'],[(0x43583b0,0x435847a,69,7),(0x3c600f0,0x3c6016e,43,11)],strict=True):
        e,=ext(start)
        req(pe.r2f(e.BeginAddress)==d['entry']==start and pe.r2f(e.EndAddress)==d['end_exclusive']==end and
            pe.f2va(start)==int(d['entry_VA'],16) and pe.f2va(end)==int(d['end_exclusive_VA'],16),'runtime-function extent')
        g={}; ext_edges=[]; pending=[start]
        while pending:
            o=pending.pop()
            if o in g:
                continue
            # Decode the native extent independently; the shard must cover every independently reachable instruction.
            i=next(md.disasm(pe.raw[o:o+15],pe.f2va(o),count=1)); req(o in ins and i.bytes==ins[o].bytes,'reachable coverage')
            nxt=[]
            if i.mnemonic.startswith('j'):
                t=pe.va2f(i.operands[0].imm)
                if start<=t<end:
                    nxt.append(t)
                else:
                    req(i.mnemonic=='jmp' and (o,t)==(CHAIN[2],CHAIN[3]),'only exterior CFG edge')
                    ext_edges.append({'from':hex(o),'kind':'tail_jump','target_va':hex(i.operands[0].imm)})
            if i.mnemonic not in ('jmp','ret'):
                req(o+i.size<end,'fallthrough inside extent'); nxt.append(o+i.size)
            g[o]=nxt; pending.extend(nxt)
        covered=[]
        for b in d['blocks']:
            pcs=b['sites']; covered+=pcs
            req(pcs and sorted(g[pcs[-1]])==b['successors'] and all(g[a]==[z] and not ins[a].mnemonic.startswith('j') for a,z in zip(pcs,pcs[1:])),'block paths')
        req(sorted(covered)==sorted(g) and len(g)==d['instruction_count']==ni and len(d['blocks'])==nb and ext_edges==d['external_edges'],'CFG partition')
        graph.update(g)
    req({o for o in graph if ins[o].mnemonic=='call'}=={t[3] for t in LAYOUT}|{0x3c60149,0x3c60162},'call census')
    for o,s in {0xf2ba33:'qword ptr [rsp + 0x38], rsi',0xf2ba38:'byte ptr [rsp + 0x30], r12b',0xf2ba3d:'dword ptr [rsp + 0x28], ebp',
        0x43583ba:'r14, r9',0x43583bd:'ebp, r8d',0x4358465:'r8d, ebp',0x4358468:'r9, r14',0x43583cd:'rax, qword ptr [rbx]',
        0x3c60122:'rcx, qword ptr [rsp + 0x78]',0x3c6012a:'r8d, 0x989681',0x3c60133:'r8d, dword ptr [rsp + 0x68]',
        0x3c60146:'r9b, 1',0x4358452:'eax, eax',0x3c60164:'al, 1'}.items():
        text(o,s)
    branches=[b for p in c['branch_shards'] for b in js(OUT/p)['branches']]; by={b['site']:b for b in branches}
    cond={o for o,links in graph.items() if len(links)==2}
    expected={o:k for k,osites in OUTER.items() for o in osites}
    expected.update({o:'wire_data' if o==0x3c60131 else 'IO-result' if o in STATUS else 'context-lifecycle' for o in cond})
    req(len(cond)==r['condition_count']==10 and set(by)==set(expected) and len(by)==len(branches)==30,'complete audited branch census')
    count=Counter(expected.values()); req(c['branch_taxonomy']==list(OUTER) and c['branch_census']=={k:count[k] for k in OUTER},'five branch classes')
    for o,b in by.items():
        p=b['predicate']; z=p+ins[p].size; i=ins[o]
        req(i.mnemonic.startswith('j') and i.mnemonic!='jmp' and
            (z==o or o==0xffa640 and ins[z].mnemonic=='mov' and z+ins[z].size==o),'predication geometry')
        req((dest(o),o+i.size,expected[o])==(b['taken_to'],b['fallthrough_to'],b['class']) and all(e in ins for e in b['evidence']) and
            bool(b['alternative_or_first_counterexample']),'branch source/edge/negative')
        req(b['scope']==('loader_footer_factory_slice' if o not in cond else 'reader' if o>=CHAIN[1] else 'identity_tail'),'branch scope')
        if o in STATUS:
            text(p,'dword ptr [rbx + 0x10], 0'); req(b['evidence'][0]==STATUS[o] and (o+i.size if i.mnemonic=='je' else dest(o))==0x4358452,'read status failure')
    req(c['transfers'][0]==dict(site=0xf2ba0e,legacy_offset=-1,wire_offset=0,width=1,sink='loader stack+0x43'),'wire selector')
    for rec,(off,w,obj,site,l,wp) in zip(c['transfers'][1:],LAYOUT,strict=True):
        req((rec['legacy_offset'],rec['wire_offset'],rec['width'],rec['object_offset'],rec['site'],rec['setup'])==(off,off+1,w,obj,site,[l,wp]),'read coordinate')
        m=ins[l].operands[1]; req(ins[l].mnemonic=='lea' and m.mem.disp==obj and ins[l].reg_name(m.mem.base)==('rdi' if w==12 else 'rcx' if off==0 else 'rsi'),'destination LEA')
        text(wp,f'r8d, {w:#x}' if w==12 else f'r8d, {w}'); text(site,'qword ptr [rax + 0x28]')
    req([(t['site'],t['width']) for t in c['loader_transfers']]==[(0xf2b691,4),(0xf2b6b1,1),(0xf2ba0e,1),(0xffa602,4),
        (0xffa7a8,4),(0xffa7c7,4),(0xffa7e6,4),(0xf2baa2,1),(0xf2bac2,4)],'outer I/O geometry')
    for t in c['loader_transfers']:
        text(t['site'],'qword ptr [rax + 0x28]'); req(ins[t['setup'][0]].operands[1].imm==t['width'],'outer width immediate')
    req(dest(0xf2ba23)==0xf48b30 and dest(0xf2ba7f)==0xffa5d0,'outer factory and vector helper')
    req(all(o in ins for sites in c['scope_evidence'].values() for o in sites),'scope shard references')
    req(ins[0xe83d9a].operands[1].imm==int.from_bytes(b'CNtp','big') and rip(0xea66ea)==vf and
        [dest(o) for o in (0xe83da0,0xe84f3d,0x152fd50,0x43591ce,0xea67c4,0x152f7f0)]==
        [0xe84f11,0xea6420,0x4359180,0xfe6f60,0xfe6f60,0x4358a00],'CNtp list to class and setter/writer')
    for o,s in {0xea66cc:'ebx, dword ptr [rax + 0xc]',0xea66f1:'qword ptr [rsi], rax',0xea66f4:'dword ptr [rsi + 0x18], ebx',
        0xea64f6:'ebp, dword ptr [rdx + 0xc]',0xea67cd:'dword ptr [rsi + 0x1c], eax',0xea67e9:'byte ptr [rsi + 0x20], al',
        0xea679e:'byte ptr [rsi + 0x21], al',0xea6759:'byte ptr [rsi + 0x22], al',0x4358a5d:'rdx, [rsi + 0x1c]',
        0x4358a65:'r8d, 4',0x4358a6e:'qword ptr [rax + 0x28]',0xbe0:'al, 1',0x152fbae:'edi, edi'}.items():
        text(o,s)
    req(ins[0xbe2].mnemonic=='ret' and dest(0x152fbb0)==0x152fc15,'no ordinal fixup/rating zero box path')
    for d in f['fields']:
        code=d['code']; arm,mn,ix=ARMS[code]; g=d['getter']; path=g['route']; x=int.from_bytes(code.encode(),'big')
        req(path[0]==0x152fa40 and path[-1]==g['arm']==arm and g['compare'] in path and ins[g['compare']].operands[1].imm==x and
            all(o in ins for o in g['support']),'scoped getter dispatch')
        for o,nxt in zip(path,path[1:]):
            i=ins[o]; n=o+i.size
            if i.mnemonic=='cmp':
                req(i.op_str.startswith('edx, '),'getter 4CC argument'); cmp=i.operands[1].imm
            elif i.mnemonic.startswith('j') and {'je':x==cmp,'jne':x!=cmp,'jg':x>cmp}[i.mnemonic]:
                n=dest(o)
            req(n==nxt,'getter route edge')
        off,w,obj,site,*_=LAYOUT[ix]; i=ins[arm]; m=i.operands[1]
        req(i.mnemonic==mn and i.reg_name(m.mem.base)=='rcx' and m.mem.disp==g['object_offset']==obj and m.size==g['width']==w and
            d['sink']==dict(legacy_offset=off,wire_offset=off+1,width=w,object_offset=obj,site=site),'getter member and actual wire sink')
    for a,b in ((CHAIN[0],CHAIN[1]),(CHAIN[2],CHAIN[3]),(CHAIN[3],CHAIN[4])):
        graph[a]=[b]
    return graph,by,ins,cond


def physical_rows(raw,n):
    end=13+W*n
    req(len(raw)==end+9 and raw[:8].hex()=='03017461642ef10d' and S.unpack_from('<IB',raw,8)==(n,0),'envelope')
    vec,flag,hi=S.unpack_from('<IBI',raw,end); req(vec==0 and flag==1,'observed footer prefix')
    return [raw[i:i+W] for i in range(13,end,W)],(vec,flag,hi)


def archives(c):
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); p=js(ROOT/PROFILE)
    for a,expected in [('client',31),('server',77)]:
        fn=a+'_db.dat'; disk=db.DB_DIR/fn; blob=disk.read_bytes(); all_entries=codec['list_tables'](disk,fn); ar=c['archives'][a]
        hits=[r for r in all_entries if r['table_id']==66]
        req(sha(blob)==ar['archive_sha256'] and len(all_entries)==ar['directory_entry_count']==expected and
            hits==ar['table66_entries'] and bool(hits)==ar['present'],'archive directory/SHA '+a)
        if a=='client':
            req(not hits and all(ar[k] is None for k in ('row_count','stride','payload_sha256')),'client absent is not zero rows')
            continue
        e,=hits; frame=p['payload']['packed_offset']; magic=blob.index(db.MAGIC,e['offset'],e['offset']+64)
        req((e['offset'],frame,e['packed_size'])==(24307967,24308001,5834) and
            magic==frame==ar['zstd_frame_offset']==ar['first_frame_offset'] and not ar['used_profile_frame'],'first frame equals t29 profile frame')
        raw=codec['_stream_decompress'](blob[frame:frame+e['packed_size']],256*1024*1024)
    s=c['archives']['server']; rows,foot=physical_rows(raw,N); end=len(raw)-9
    req(sha(raw)==s['payload_sha256']==PAYLOAD_SHA==p['payload']['payload_sha256'] and
        len(raw)==e['size']==s['payload_len']==s['default_load_payload_len']==18094 and (e['record_count_header'],e['payload_version'])==(N,3569),'table66 payload')
    req((s['row_count'],s['stride'],s['row_bytes'],s['wire_origin'],s['legacy_origin'],s['wire_footer_start'],s['legacy_footer_start'])==
        (N,W,N*W,13,14,end,end+1) and s['wire_footer_hex']==raw[end:].hex() and s['legacy_footer_hex']==raw[end+1:].hex() and
        s['header_hex']==raw[:13].hex() and tuple(s['footer_values'])==foot==(0,1,753),'dual closure')
    req(s['footer_transfers']==[dict(site=o,offset=k,width=w,value=v) for o,k,w,v in zip(FOOT,(end,end+4,end+5),(4,1,4),foot,strict=True)],'footer sites')
    t=c['t29']; rr=(ROOT/ROWS).read_bytes(); rc=p['row_closure']
    req((t['profile'],t['rows'],t['matched_full_rows'])==(PROFILE,ROWS,N) and t['profile_sha256']==sha((ROOT/PROFILE).read_bytes()) and
        sha(rr)==p['full_rows_sha256']==t['rows_sha256'] and sha(raw[14:end+1])==t['legacy_block_sha256']==rc['rows_sha256'] and
        (rc['row_start'],rc['row_end_exclusive'],rc['count'],rc['stride'])==(14,end+1,N,W),'t29 provenance')
    for i,(k,line) in enumerate(zip(range(14,end+1,W),rr.splitlines(),strict=True)):
        r=json.loads(line); req((r['row'],r['offset'],r['len'],bytes.fromhex(r['raw_hex']))==(i,k,W,raw[k:k+W]),f't29 row {i}')
    inv=js(ROOT/INV); q,=[r for r in inv['parents'] if r['parent_4cc']=='CNtp']; v=t['inventory']
    req(v['path']==INV and v['sha256']==sha((ROOT/INV).read_bytes()) and (q['table_type'],q['count'],q['stride'],q['link_status'])==
        (66,N,W,v['link_status']) and [r['schema_idx'] for r in q['schema_item_fields']]==list(range(46,50)) and
        q['profile']['profile_sha256']==t['profile_sha256'] and q['profile']['rows_jsonl_sha256']==t['rows_sha256'],'inventory framing, not hint votes')
    return rows,codec,db,{(x['offset'],x['width']):x for x in p['columns']}


def row_path(row,i,pe,cut=None):
    graph,by,ins,cond=pe; base=13+W*i; p=1; site=CHAIN[0]; raw_id=None; visits=[]; short=None
    req(row[0]==0,f'row {i}: selector {row[0]} @{base} outside observed domain (not factory rejection)')
    reads={t[3]:t for t in LAYOUT}
    for _ in range(len(graph)+1):
        if site in reads:
            off,w,*_=reads[site]; req(p==off+1,'CFG read order vs physical row coordinate')
            if p+w>len(row) or site==cut:
                short=f'row {i}: short transfer @{base+p} width {w} site {site:#x}'
                if w==12:
                    raise Reject(short+'; no immediate native bulk status test')
            else:
                if w==12:
                    raw_id=S.unpack_from('<III',row,p)
                p+=w
        if site in cond:
            if site in STATUS:
                take=(short is None)==(ins[site].mnemonic=='je')
            elif site==0x3c60131:
                take=raw_id[0]<0x989681
                stored=raw_id[0] if take else i
            else:
                take=site==0x3c60155
            visits.append([site,take]); site=by[site]['taken_to' if take else 'fallthrough_to']
        elif ins[site].mnemonic=='ret':
            if site==0x435845e:
                raise Reject(short+'; IO-result -> 0x4358452 (AL=false)')
            req(p==W and site==0x3c6016d,'CFG success and full row consumption')
            rid,a,b=raw_id
            req(rid==i==stored and a==b and a!=0,f'row {i}: identity @{base+W-12} raw={raw_id}, stored ordinal={stored}')
            return raw_id,visits
        else:
            site,=graph[site]
    raise Reject('nonterminating reader')


def rejection(fn):
    try:
        fn()
    except Reject as e:
        return str(e)
    raise Reject('negative probe accepted')


def verify_rows(rows,s,pe):
    trace=sha256(); visits=Counter(); samples=[]; uids=set(); sh=Counter()
    for i,row in enumerate(rows):
        raw_id,choices=row_path(row,i,pe)
        req(choices==s['row_template']['condition_edges'] and raw_id[1] not in uids,'observed path and unique identity')
        sh[str(row[0])]+=1; visits.update(map(tuple,choices)); uids.add(raw_id[1]); off=13+i*W
        h=sha256(row[1:]).digest(); trace.update(S.pack('<7I',i,off,off+1,off+W,*raw_id)+h)
        if i in (0,1,2,N//2,N-1):
            samples.append(dict(ordinal=i,selector_start=off,body_start=off+1,body_end=off+W,identity=list(raw_id),body_sha256=h.hex(),wire_hex=row.hex()))
    req((min(uids),max(uids))==(s['uid_min'],s['uid_max'])==(1,753) and sh==s['selector_histogram']=={'0':N} and
        s['row_trace_sha256']==trace.hexdigest() and s['samples']==samples,'full row trace')
    neg=s['negative_replays']; r=rows[0]; short={t[3]:rejection(lambda:row_path(r,0,pe,cut=t[3])) for t in LAYOUT}
    bad_id=rejection(lambda:row_path(r[:12]+S.pack('<I',0x989681)+r[16:],0,pe))
    req(neg==dict(short_transfers=[dict(site=o,first_counterexample=e) for o,e in short.items()],overwrite_does_not_mask_raw_error=bad_id,
        selector_out_of_observed_domain=rejection(lambda:row_path(b'\x01'+r[1:],0,pe)),
        duplicate_lane_mismatch=rejection(lambda:row_path(r[:-4]+bytes(4),0,pe))),'independent first negative replays')
    _,by,_,cond=pe
    for o in cond:
        b=by[o]; t,z=visits[o,True],visits[o,False]
        req((t,z)==(b['taken_count'],b['fallthrough_count']) and t+z==N and b['observed_edge']==('taken' if t else 'fallthrough'),'per-branch full-table visits')
        if o in STATUS or o==0x3c60131:
            req(b['alternative_or_first_counterexample']==(short[STATUS[o]] if o in STATUS else bad_id),'branch first counterexample')


def target_domain(codec,db,d):
    c=js(ROOT/NATION); a,b=[db.load_payload(codec,s,10) for s in ('client','server')]
    req(c['source_payload']['sha256']==sha(a) and len(a)==24732 and len(b)==422345 and
        S.unpack_from('<I',a,8)==S.unpack_from('<I',b,8)==(251,),'nation payload fingerprints and headers')
    m={}; pos=[]; last_wire=13
    for i,row in enumerate(c['rows']):
        k=row['identity_payload']; triple=a[k:k+12]; o,v,w=S.unpack('<Iii',triple)
        req(k>last_wire and o==i==row['ordinal'] and v==w==row['row_id'] and v>0 and v not in m and a[k+12]==0,'read actual nation identity')
        last_wire=k; m[v]=o
        positions=[x.start()+13 for x in re.finditer(re.escape(triple),b[13:-9])]
        req(len(positions)==1 and (not pos or positions[0]>pos[-1]),'corroborate identity triple in server')
        pos+=positions
    req(last_wire+13==len(a)-8 and pos[-1]+12==len(b)-9,'target domain last identity')
    req((d['table_type'],d['row_count'],d['identity_count'],d['ordinal_bounds'],d['identity_min'],d['identity_max'],d['client_sha256'],d['server_sha256'],
        d['t25_client_positions'],d['server_identity_match_count'],d['server_position_sha256'])==
        (10,251,len(m),[0,250],min(m),max(m),sha(a),sha(b),NATION,len(pos),sha(S.pack('<251I',*pos))),'target domains and positions')
    return m


def fields_check(f,rows,cols,ids):
    m=js(ROOT/MASTER); p,=[x for x in m['entities']['club.xml'][0]['fields'] if x['field']=='CNtp']; specs=p['list_item_fields']
    occ=[x for x in js(ROOT/OCC)['nested_fields'] if x['parent']=='CNtp']
    req(len({x['field'] for x in specs})==4 and [x['idx'] for x in occ]==[46,47,48,49],'unique scoped occurrences')
    ords=set(ids.values()); fields={}; grades=Counter()
    for d,x,e in zip(f['fields'],specs,occ,strict=True):
        code=x['field']; off,w,*_=LAYOUT[ARMS[code][2]]; bs=[r[off+1:off+1+w] for r in rows]
        req(d['schema']==x and d['schema_scope']==['club.xml','CNtp',e['idx']] and
            (d['code'],d['name'],x['type'],x.get('is_optional')=='true')==(e['code'],e['name'],e['type'],e['optional']),'schema gate identity')
        kind={'nati':'<i','rati':'<b'}.get(code,'<B'); vals=[S.unpack(kind,b)[0] for b in bs]; h=Counter(vals); fields[code]=vals
        u=Counter(int.from_bytes(b,'little') for b in bs); t=[N,len(u),min(u),max(u),u[0],u[(1<<(8*w))-1]]
        req(t==[cols[off,w][k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')],'independent unsigned t29 differential')
        def ex(i):
            return dict(row=i,offset=14+W*i+off,value=vals[i],hex=bs[i].hex())
        exp=dict(count=N,distinct=len(h),min=min(h),max=max(h),zero_count=h[0],minus_one_count=h[-1],
            histogram={str(k):v for k,v in h.items()} if len(h)<32 else None,t29_unsigned_stats=t)
        if code=='nati':
            cast='scalar_i32_nation_identity'; req(x['database_table_type']=='nation' and d['domain']['constructor_default']==-1 and d['domain']['zero_is_not_minus_one'],'scalar default is not zero')
            bad=[i for i,v in enumerate(vals) if v!=-1 and v not in ids]; wrong=[i for i,v in enumerate(vals) if v!=-1 and v not in ords]
            req(not bad and h[0]==h[-1]==0 and len(wrong)==602 and (wrong[0],vals[wrong[0]],ids[vals[wrong[0]]])==(1,1651,189),'identity vs ordinal exact domain')
            exp.update(live_count=N-h[-1],identity_matches=N-h[-1]-len(bad),first_target_ordinals=[ids.get(v) for v in vals[:3]],
                ordinal_misses=len(wrong),first_ordinal_counterexample={**ex(wrong[0]),'actual_target_ordinal':ids[vals[wrong[0]]]})
        elif code=='rati':
            cast='i8_enum'; bad=[]
            req(h=={0:34,1:263,2:211,3:114,4:88,5:43} and 'enum_ref' not in x and d['domain']['exhaustive_enum_domain'] is None,'observed enum only')
            exp['observed_live_values']=sorted(v for v in h if v!=0)
        else:
            cast='u8_integer'; lo,hi=int(x['min_value']),int(x['max_value']); bad=[i for i,v in enumerate(vals) if not lo<=v<=hi]
            exp['nonzero_xml_violations']=sum(vals[i]!=0 for i in bad)
            req(d['domain']==dict(xml_bounds=[lo,hi],native_unsigned_bounds=[0,255],proven_zero_sentinel=False) and
                len(bad)=={'mina':436,'maxa':395}[code] and exp['nonzero_xml_violations']==0,'age domain conflict retained')
        exp.update(violations=len(bad),first_violation=ex(bad[0]) if bad else None)
        grade='held_static_sink_profile_conflict' if bad else 'L3_named_row_coordinate'; grades[grade]+=1
        req(exp==d['profile'] and d['interpretation']==cast and d['grade']==grade and (d['row_offset'],d['wire_offset'])==
            ((None,None) if bad else (off,off+1)),'field profile/grade '+code)
    age=list(zip(fields['mina'],fields['maxa'],strict=True)); order=[i for i,(a,b) in enumerate(age) if a>b]; kinds=Counter((bool(a),bool(b)) for a,b in age)
    i=order[0]; req((i,len(order),age[i])==(57,6,(18,0)),'first inverted raw age')
    req(f['age_relationship']==dict(both_zero=kinds[False,False],both_nonzero=kinds[True,True],only_min_zero=kinds[False,True],
        only_max_zero=kinds[True,False],raw_min_gt_max=len(order),nonzero_min_gt_max=sum(all(age[j]) for j in order),
        first_raw_min_gt_max=dict(row=i,offset=23+i*W,values=list(age[i]),hex=rows[i][10:12].hex())),'all-row age relation')
    req(f['rejected_record_pair']['lanes']==list(S.unpack_from('<ii',rows[0],1)) and f['rejected_record_pair']['offset']==14,'pair hypothesis negative')
    req(grades=={'L3_named_row_coordinate':2,'held_static_sink_profile_conflict':2} and
        (f['occurrences'],f['L3'],f['baseline_L3'],f['L4'])==(4,2,0,0),'grade counts')


def verify():
    c=js(OUT/'cursor_cntp.json'); f=js(OUT/'fields_cntp.json')
    req(c['scope']==f['scope']==['club.xml','CNtp'] and c['table_type']==f['table_type']==66,'scope')
    pe=pe_check(c,f); rows,codec,db,cols=archives(c)
    verify_rows(rows,c['archives']['server'],pe)
    fields_check(f,rows,cols,target_domain(codec,db,f['reference_domain']))
    print('t34 verify PASS: 753 rows / 24 B; 18 reader/tail blocks; 2 L3, 2 held, L4=0')


def selftest():
    r=bytes(W); h=bytes.fromhex('03017461642ef10d0100000000'); f=S.pack('<IBI',0,1,15)
    req(physical_rows(h+r+f,1)==([r],(0,1,15)),'physical envelope fixture')
    req('envelope' in rejection(lambda:physical_rows(h+r+f[:-1],1)) and
        'footer prefix' in rejection(lambda:physical_rows(h+r+b'\x01'+f[1:],1)),'negative fixture')
    req(S.unpack('<ibB',bytes.fromhex('ffffffffff00'))==(-1,-1,0),'scalar sentinel and signedness fixture')
    print('t34 verify selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test the envelope and scalar sentinel models without local data')
    try:
        selftest() if p.parse_args().selftest else verify()
        return 0
    except Reject as e:
        print(f't34 verify FAIL: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't34 verify fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
