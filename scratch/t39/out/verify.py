#!/usr/bin/env python3
"""Independently replay Tchl/table 34 from the original PE and local archives."""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import struct as S
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXE=Path('<OLD_REPO>/input/editor.exe')
EXE_SHA='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'
PROV='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
MAGIC=bytes.fromhex('28b52ffd')
SLOTS={'tchc':(0x18,0,4,25),'styr':(0x48,8,2,None),'edyr':(0x4a,10,2,None),
       'mstn':(0x30,12,4,23),'sstn':(0x38,16,4,23),'dbrt':(0x4d,21,1,None),
       'posi':(0x4e,26,1,None),'cquf':(0x28,22,4,25),'tcop':(0x40,27,4,24)}
START,END=0x43a6890,0x43a6a6f

class Check(Exception): pass


def req(ok, why):
    if not ok:raise Check(why)


def js(path):return json.loads(path.read_bytes())
def sha(buf):return sha256(buf).hexdigest()
def u32(buf,at):return S.unpack_from('<I',buf,at)[0]


def single(zstd,buf):
    d=zstd.ZstdDecompressor().decompressobj(); raw=d.decompress(buf)
    req(d.eof,'truncated Zstd frame')
    return raw,len(buf)-len(d.unused_data)


def db_check(m):
    os.environ.setdefault('FM24_DB_DIR',str(ROOT/'scratch/data'))
    import zstandard as zstd
    import fm24_dump as fm
    codec=fm._reader(); fetch={}; main=None
    for archive in ('client','server'):
        name=archive+'_db.dat'; _,b,layout=codec['_entries'](fm.DB_DIR/name,name)
        ent={q['path'].rsplit('/',1)[-1]:q for q in layout['entries']};base=layout['data_base'];a=m[archive]
        req(sha(b)==a['archive_sha256'] and len(ent)==a['directory_entry_count'] and ('table_34.dat' in ent)==(archive=='server')==a['present'],f'{archive}: archive hash / table directory')
        def read(name, ent=ent, b=b, base=base, toc=layout['toc_offset']):
            q=ent[name];start=base+q['offset'];end=start+q['packed_size']
            next_=min((base+e['offset'] for e in ent.values() if e['offset']>q['offset']),default=toc)
            req(end<=next_ and b[start:start+4]==MAGIC,f'{name}: bounded directory frame')
            raw,w=single(zstd,b[start:end]);req(w==q['packed_size'] and len(raw)==q['size'],f'{name}: frame size')
            return raw
        fetch[archive]=read
        if archive=='client':
            req(all(a[k] is None for k in ('entry','row_count','stride','payload_sha256')),'client absence not empty')
            continue
        q=ent['table_34.dat'];o=q['offset'];start=base+o;end=start+q['packed_size']; req(q==a['entry'] and q['size']==313082,'table34 directory')
        # Old loader starts from raw directory-relative offset. Enumerate adjacent frames
        # through the official member end; select by size, then check SHA independently.
        pos=b.index(MAGIC,o,start+4); matches=[];hits=[]
        while pos<end and b[pos:pos+4]==MAGIC:
            body,used=single(zstd,b[pos:min(pos+q['packed_size'],end)])
            hit=dict(offset=pos,relative_offset=pos-o,compressed_bytes=used,payload_bytes=len(body),count=u32(body,8),sha256=sha(body));hits.append(hit)
            if len(body)==q['size']: matches.append((hit,body))
            pos+=used
        req(pos==end and len(matches)==1 and [x['relative_offset'] for x in hits]==[9,34] and hits[0]['payload_bytes']==12 and hits[0]['count']==0 and hits==a['frames'],'two bounded frames incl. stub')
        hit,main=matches[0];req(hit==a['selected_frame'] and hit['sha256']==a['payload_sha256']=='a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812','true frame SHA')
        previous=ent['non_player_bans.dat'];first=a['first_magic_counterexample'];next_=ent['table_37.dat']['offset']+base
        req(read('non_player_bans.dat')==bytes.fromhex('03017461642ef10d00000000') and previous==first['entry'] and
            base+previous['offset']==first['canonical_offset']==hits[0]['offset'] and
            hits[0]['offset']+previous['packed_size']==start and end==next_==a['next_member_or_toc'],'first magic belongs to preceding directory member')
    return main,fetch


def static_check(c,f):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from t05_pe import PE
    from t14_rtti_census import parse_rtti
    p=PE(EXE); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
    req(sha(p.raw)==c['provenance']['editor_sha256']==EXE_SHA,'editor SHA')
    man={r['path']:r['sha256'] for r in js(ROOT/'evidence/MANIFEST.json')['files']}
    for name in (MASTER,PROV):req(sha((ROOT/name).read_bytes())==man[name]==c['provenance']['frozen_snapshots'][name],f'frozen {name}')
    req(man[MASTER].startswith('7d57477e') and EXE_SHA in (ROOT/PROV).read_text(encoding='utf8'),'snapshot provenance')
    recs={}
    def ins(o):
        if o not in recs:recs[o]=next(m.disasm(p.raw[o:o+15],p.f2va(o),1))
        return recs[o]
    def target(o):return p.va2f(ins(o).operands[0].imm)
    def rip(o):
        i=ins(o);return i.address+i.size+i.operands[1].mem.disp
    def slots(v,*idx):return [p.va2f(S.unpack_from('<Q',p.raw,p.va2f(v)+i*8)[0]) for i in idx]
    instructions={}
    for name in c['instruction_shards']:
        for r in js(HERE/name)['instructions']:
            o=int(r['file_offset'],16);i=ins(o)
            req(o not in instructions and p.va2f(i.address)==o and r['VA']==hex(i.address) and i.bytes.hex()==r['bytes'] and
                r['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),f'instruction bytes/VA {o:#x}');instructions[o]=i
    branches={}
    for name in c['branch_shards']:
        for r in js(HERE/name)['branches']:
            o=r['site'];i=ins(o)
            req(o not in branches and r['taken_to']==target(o) and r['fallthrough_to']==o+i.size and
                all(x in instructions for x in [o,r['predicate'],*r['evidence']]) and r['first_counterexample_or_constraint'],f'branch evidence {o:#x}')
            branches[o]=r
    req({k:sum(b['class']==k for b in branches.values()) for k in c['branch_classes']}==c['branch_counts'],'branch tally by category')
    jbase=p.va2f(rip(0xf48b45));cell=jbase+34*4;rel=S.unpack_from('<i',p.raw,cell)[0]
    v=rip(0xf494b8);o,=slots(v,19)
    req((jbase,cell,rel,p.raw[cell:cell+4].hex())==tuple(c['factory'][k] for k in ('base','cell','rel32','raw')) and jbase+rel==0xf4949c and
        o==0x156efd0 and target(o)==START and parse_rtti(p,v)['decorated']==c['rtti']['decorated']=='.?AVSTARTING_TEAM_CUP_HISTORY@db@@','factory/RTTI/slot19')
    req(dict(zip(c['slots'],slots(v,*map(int,c['slots']))))==c['slots'],'vtable slots')
    extent=[(p.r2f(e.struct.BeginAddress),p.r2f(e.struct.EndAddress)) for e in p.pe.DIRECTORY_ENTRY_EXCEPTION if e.struct.BeginAddress==p.f2r(START)]
    req(extent==[(START,END)] and c['reader']['entry_VA']==hex(p.f2va(START)) and c['reader']['end_VA']==hex(p.f2va(END)),'runtime-function extent')
    q=[START]; graph={}; transfers={};cond={}
    while q:
        o=q.pop()
        if o in graph:continue
        req(START<=o<END and o in instructions,'reachable instruction outside extent/evidence')
        i=ins(o);nxt=o+i.size
        if i.mnemonic=='ret':es=[]
        elif i.mnemonic=='jmp':es=[target(o)]
        elif i.mnemonic.startswith('j'):
            es=[nxt,target(o)];b=branches[o];p0=ins(b['predicate']);req(p0.address+p0.size==i.address,'reader predicate adjacency')
            cond[o]=('IO-result' if '+ 0x10], 0' in p0.op_str else 'runtime-external' if '[rsp + 0x70]' in p0.op_str else
                     'wire_data' if '0x989681' in p0.op_str else 'context-lifecycle')
            req(cond[o]==b['class'],f'static branch class {o:#x}')
        else:es=[nxt]
        if i.op_str=='qword ptr [rax + 0x28]' and i.mnemonic=='call':
            if o==0x43a6a17:l,w=ins(o-19),ins(o-12)
            else:l,w=ins(o-16),ins(o-9)
            req(l.mnemonic=='lea' and w.mnemonic=='mov' and w.op_str.startswith('r8d, '),'read width and sink dataflow')
            require_mem=l.operands[1];req(l.reg_name(require_mem.mem.base)=='rsi','row object sink base')
            transfers[o]=(l.operands[1].mem.disp,w.operands[1].imm)
        graph[o]=es;q+=es
    saved={}
    for b in c['reader']['blocks']:
        for ix,o in enumerate(b['sites']):saved[o]=[b['sites'][ix+1]] if ix+1<len(b['sites']) else b['successors']
    req({k:set(v) for k,v in saved.items()}=={k:set(v) for k,v in graph.items()} and len(graph)==137==c['reader']['reachable'] and
        set(cond)=={o for o,b in branches.items() if b['scope']=='slot19'},'reachable graph and branch census')
    req(ins(0xf2b670).op_str=='r12d, r9d' and ins(0xf2ba38).op_str=='byte ptr [rsp + 0x30], r12b' and
        ins(0xf2ba51).op_str=='qword ptr [rbx + 0x98]' and ins(0xf28c13).op_str=='r9b, 1' and
        all(ins(o).op_str=='qword ptr [rax + 0x28]' for o in (0xf2b691,0xf2b6b1,0xf2ba0e,0xffa602,0xf2baa2,0xf2bac2)),'caller mode and outer transfers')
    o=0
    for t in c['transfers'][1:]:
        disp,w=transfers[t['site']];req((disp,w,o,o+1)==tuple(t[k] for k in ('object_offset','width','legacy_offset','wire_offset')),'transfers vs native width/member')
        o+=w
    req(o==43 and len(transfers)==len(c['transfers'])-1,'complete body width')
    # Independently follow getter dispatch based on actual EDX compares, stopping at member load.
    enum={k:([k+9,k] if k<=8 else [18,9] if k==11 else [19,19]) for k in (*range(1,9),11,12)}
    ed=c['enum_evidence']; raw=bytes.fromhex(ed['jump_table']['bytes']); jump=ed['jump_table'];tmp=p.raw[jump['offset']:jump['offset']+48]
    req(raw==tmp and rip(0x156f8f3)==int(jump['VA'],16),'native Result jump table')
    for state,d in enumerate(S.unpack('<12i',tmp),1):
        arm=p.va2f(rip(0x156f8f3)+d);req(arm==jump['arms'][state-1],f'enum state {state} arm')
        if state in (*range(1,9),11):req(ins(arm+7).mnemonic=='lea' and ins(arm+7).operands[1].mem.disp==enum[state][1],'enum state plus 9 iff flag zero')
        else:req(ins(arm).op_str=='edi, 0x13' if state==12 else arm==0x156fbb7,'result constant/default state')
    setter=[bytes.fromhex(t['bytes']) for t in ed['setter_tables']]
    req(all(p.raw[t['offset']:t['offset']+19]==r for t,r in zip(ed['setter_tables'],setter)) and
        [enum[s][f0] for f0,s in zip(*setter)]==list(range(1,20)) and {int(k):v for k,v in ed['boxed_flag_zero_then_one'].items()}==enum,'setter inversion')
    for field in f['fields']:
        code=field['code'];obj,coord,width,tid=SLOTS[code];o,=slots(v,2);n=int.from_bytes(code.encode(),'big');path=[];cmp=None;imm=None
        for _ in range(35):
            i=ins(o);path.append(o)
            if i.mnemonic=='cmp':
                req(i.op_str.startswith('edx, '),'getter compare of schema code');imm=i.operands[1].imm
                if imm==n:cmp=o
            elif cmp is not None and i.mnemonic in ('mov','movzx','movsx'):
                break
            nxt=o+i.size
            if i.mnemonic.startswith('j') and {'jle':n<=imm,'jg':n>imm,'je':n==imm,'jne':n!=imm}[i.mnemonic]:nxt=target(o)
            o=nxt
        g=field['getter'];req(path==g['route'] and cmp==g['compare'] and o==g['load'] and i.operands[1].mem.disp==obj and
                              i.reg_name(i.operands[1].mem.base)=='rcx',f'{code}: getter route/member')
        ss=[(t['object_offset'],t['legacy_offset'],t['width']) for t in field['sinks']];req(ss==([(0x4c,20,1)] if code=='dbrt' else [])+[(obj,coord,width)],f'{code}: sink coordinates')
        for t in field['sinks']:req(t in c['transfers'],f'{code}: actual sink')
        if code=='posi':req(i.mnemonic=='movsx' and ins(o+i.size).op_str=='edi, -1','position sentinel')
        if code in ('styr','edyr'):req(i.mnemonic=='movzx' and i.operands[1].size==2,'year integer, not packed date')
    for field in [*f['fields'],f['unscoped_owner']]:
        if 'proof' not in field['domain']:continue
        q=field['domain']['proof'];tid=q['target_table'];thunk,body,_,_,end=q['helper']
        req(target(q['slot20_call'])==thunk and target(thunk)==body and ins(end).operands[1].mem.scale==8 and
            ins(q['writer_target_ordinal']).op_str=='eax, dword ptr [rax + 8]' and ins(q['writer_null']).op_str=='eax, 0xffffffff',f'ordinal not identity: {field.get("code","owner")}')
        if q['getter_tag']:req(ins(q['getter_tag']).operands[1].imm=={23:0x7374676e,24:0x54746561,25:0x636f6d70}[tid],'target class tag')
    sc=c['scope_evidence'];rc=sc['owner_rtti'];cv,nv,tv,nt=(rc[x]['vtable_va'] for x in ('CLUB','NATION','TEAM','NATIONAL_TEAM'))
    req(all(parse_rtti(p,m)['class']==k for k,m in [('CLUB',cv),('NATION',nv),('TEAM',tv),('NATIONAL_TEAM',nt)]),'club/nation/team RTTI')
    req(slots(cv,2)==[0xe89a00] and slots(nv,2)==[0x1041f30] and slots(nt,2,3)==[0x1056a90,0x11b4c30] and slots(tv,2,3)==[0x11af7b0,0x11b4c30],'shared parent vtable edges')
    req(all(target(s)==d for s,d in [(0xe8c684,0xe8d584),(0xe8f364,0x11f41d0),(0x1041f33,0x1041f40),(0x1043322,0x1065ef0),
        (0x1066987,0x10679fd),(0x1068576,0x11f41d0),(0x3d7d817,0x11af7b0),(0x11af828,0x11b0f62),(0x11b4ccd,0x11b5051),
        (0x11b505f,0x15e9830),(0x11b0f6c,0x15e9830),(0x15e9830,0x44d7bf0),(0xf4911f,0x1052b30),(0x1052b30,0x3d7afc0)]),'CLUB and NATION converge, TEAM collection')
    req(p.raw[sc['case24_cell']:sc['case24_cell']+4].hex()==sc['case24_cell_bytes'] and jbase+S.unpack_from('<i',p.raw,sc['case24_cell'])[0]==0xf490f9 and
        ins(0xf49106).op_str=='bl, 0xb' and rip(0x3d7afdb)==nt and rip(0x3e6858b)==tv and
        rip(0x44d8364)==v and rip(0x44d7c6a)==rip(0x44d83ba)==int(sc['collection_global_VA'],16) and
        ins(0x44d7cc5).op_str=='rax, qword ptr [r14 + 0x20]' and ins(0x44d7cd1).op_str=='eax, dword ptr [rdi + 0xc]',
        'selector 11 national variant and collection links to same child class; owner pointer in +0x20')
    return graph,transfers,branches,enum


def replay(raw,a,graph,transfers,branches):
    n=u32(raw,8); req(n==a['row_count']==7115 and raw[:13].hex()==a['header_hex'] and raw[:8]==bytes.fromhex('03017461642ef10d'),'13-byte wire prelude')
    accepted=[]
    for mode in (0,1):
        m=a['modes'][str(mode)];digest=sha256();p=13;h=Counter();seen=set();bad=0;first=None;edge=Counter();sample={x['ordinal']:x for x in m['samples']}
        for row in range(n):
            b=p+1;h[raw[p]]+=1;at=b;o=START;k=None;stored=None;sites=[]
            for _ in graph:
                if o in transfers:
                    obj,w=transfers[o];sites.append(o);req(at+w<=len(raw),'row transfer overrun')
                    if obj==8:k=S.unpack_from('<III',raw,at)
                    at+=w
                es=graph[o]
                if not es:break
                if len(es)==1:o=es[0];continue
                cond=branches[o]
                if cond['class']=='IO-result':yes=o==0x43a69f2
                elif cond['class']=='runtime-external':yes=mode==0
                elif cond['class']=='wire_data':yes=k[0]<10000001;stored=k[0] if yes else row
                else:yes=o==0x43a6a56
                edge[o,yes]+=1;o=cond['taken_to' if yes else 'fallthrough_to']
            req(o==0x43a6a6e and sites==m['transfer_sites'],'replay reached successful epilog')
            j,x,y=k
            if j!=row or j!=stored or x!=y or x==0 or x in seen:
                bad+=1
                if first is None:first=dict(ordinal=row,selector=raw[p],selector_start=p,body_start=b,end=at,identity=list(k),stored=stored)
            seen.add(x);bodyhash=sha256(raw[b:at]).digest();digest.update(S.pack('<7I',row,p,b,at,j,x,y)+bodyhash)
            if row in sample:req((b,at,list(k),bodyhash.hex(),raw[p:at].hex())==tuple(sample[row][s] for s in ('body_start','end','identity','body_sha256','wire_hex')),'row trace sample')
            if mode:accepted.append(b)
            p=at
        req(m['tested_rows']==n and m['first_identity_failure']==first and m['rows_failing_identity_or_uniqueness']==bad and m['selector_histogram']==
            {str(k):v for k,v in h.items()} and m['trace_sha256']==digest.hexdigest() and m['proposed_footer_offset']==p,'mode fork full replay')
        req(all([edge[o,True],edge[o,False]]==v==branches[int(o)]['edges_by_mode'][str(mode)] for o0,v in m['taken_counts'].items() for o in [int(o0)]),'mode edges')
        if mode:
            req(h=={0:n} and bad==0 and p==313073==a['wire_footer_offset'] and p+9==len(raw) and max(seen)==u32(raw,p+5) and
                S.unpack_from('<IBI',raw,p)==tuple(m['footer_result'])==(0,1,98041869),'wire end, footer and identities')
        else:req(bad==n and p==92508 and u32(raw,p)==131661824 and first['identity']==[637,50,132188129],'mode=0 first failure and nonclosing end')
    neg=a['negative_replays'];b=accepted[0]
    for t,s in zip(transfers.values(),transfers,strict=True):
        # CFG traversal order need not be transfer order, so probe by reported site below.
        req(START<=s<END and t[1]>0,'bounded transfer census')
    p=b
    for r in neg['short_members']:
        site=r['site'];w=transfers[site][1];suffix='no immediate native bulk status test' if w==12 else 'IO-result -> 0x43a69f4 (AL=false)'
        req(r['message']==f'row 0: short transfer @{p} width {w} site {site:#x}; {suffix}' and len(raw[p:p+w-1])<w,'short transfer fixture');p+=w
    req(neg['identity_overwrite']=='row 0: raw identity @45 (10000001, 103, 103), stored ordinal=0' and u32(raw,49)==u32(raw,53)==103 and
        neg['unobserved_selector']['synthetic']['end']==57 and neg['nonzero_footer'].startswith('footer vector count 1 @313073'),'negative anchor fixtures')
    return accepted


def identities(fetch,domain):
    maps={};team={}
    for tid,step in ((23,14),(25,127)):
        n=f'table_{tid}.dat';s=fetch['server'](n);c=fetch['client'](n);d=domain[str(tid)];cnt=u32(c,8)
        req(d['server_sha256']==sha(s) and d['client_sha256']==sha(c) and d['server_count']==u32(s,8)==cnt==d['client_count'] and len(c)==22+cnt*step,'competition/stage domain framing')
        pos=13;h=sha256();x={}
        for ordinal,end in enumerate(range(13+step,len(c)-8,step)):
            tail=c[end-12:end];i,j,k=S.unpack('<III',tail);at=s.find(tail,pos)
            req(i==ordinal and j==k!=0 and at>=pos,'competition/stage target key witness');x[i]=j;h.update(tail);pos=at+12
        req(len(x)==cnt and pos==len(s)-9 and h.hexdigest()==d['identity_trace_sha256'],'competition/stage target trace')
        maps[tid]=x
    d=domain['24'];b=fetch['server']('table_24.dat');extra=fetch['server']('table_extra_24.dat');n=u32(b,8)
    req(sha(b)==d['server_sha256'] and sha(extra)==d['sidecar_sha256'] and len(extra)==12+82*n and n==84507==u32(extra,8)==d['sidecar_ordinal_count'],'team target and ordinal sidecar')
    req(all(u32(extra,p)==i for i,p in enumerate(range(12,len(extra),82))),'team sidecar ordinal set')
    # Scan only candidates whose following byte has a native full-team selector.
    # For each ordinal constrain against the earliest prefix and latest suffix.
    rows=[[] for _ in range(n)];z=len(b)-9;limit=u32(b,len(b)-4)
    for match in re.finditer(rb'(?=[\x0a\x0b])',b[26:z]):
        end=26+match.start();p=end-12;i,x,y=S.unpack_from('<III',b,p)
        if i<n-1 and 0<x==y<=limit:rows[i].append(p)
    i,x,y=S.unpack_from('<III',b,z-12);req(i==n-1 and 0<x==y==limit,'team last tail');rows[-1].append(z-12)
    lo=14
    for seq in rows:
        j=bisect_left(seq,lo);req(j<len(seq),'team ordered prefix');del seq[:j];lo=seq[0]+13
    hi=z-12
    for seq in reversed(rows):
        del seq[bisect_right(seq,hi):];req(len(seq)==1,'team ordered witnesses not unique');hi=seq[-1]-13
    h=sha256();s=13;m={}
    for i,(end,) in enumerate(rows):
        m[i]=u32(b,end+4); team[i]=(b[s],s,end);h.update(S.pack('<4I',i,s,end,m[i]));s=end+12
    req(s==z and h.hexdigest()==d['identity_trace_sha256'] and Counter(x[0] for x in team.values())=={10:84256,11:251},'team identity trace / subtype counts')
    maps[24]=m
    return maps,team


def fields_check(c,f,buf,body,maps,team,enum):
    source=c['profiles']; pa=js(ROOT/source['profiles']['t29']['path']);end=body[-1]+44
    ps=pa['row_closure'];lines=(ROOT/source['rows']).read_bytes()
    req(len(body)==len(lines.splitlines())==7115==source['matched_full_rows'] and sha(lines)==pa['full_rows_sha256']==source['rows_sha256'] and
        sha(buf[14:end])==ps['rows_sha256']==source['legacy_block_sha256'],'t29 full-row and block SHA')
    for i,(p,line) in enumerate(zip(body,lines.splitlines(),strict=True)):
        req(json.loads(line)==dict(row=i,offset=p,len=44,raw_hex=buf[p:p+44].hex()),f't29 row {i}')
    for q in source['profiles'].values():
        path=ROOT/q['path']
        if q['status']=='not_available_in_checkout':continue
        src=js(path);req(sha(path.read_bytes())==q['sha256'] and src['payload']['payload_sha256']==sha(buf) and src['row_closure']['rows_sha256']==sha(buf[14:end]),'secondary profile')
    q=source['t13d_negative'];req(sha((ROOT/q['path']).read_bytes())==q['sha256'],'t13d original negative preserved')
    evidence=js(ROOT/MASTER)['entities'];catalog=[]
    for name in ('club.xml','nation.xml'):
        (t,)= [p for e in evidence[name] for p in e['fields'] if p['field']=='Tchl'];catalog.append(t['list_item_fields'])
    req(catalog[0]==catalog[1] and len(catalog[0])==len({p['field'] for p in catalog[0]})==9,'scoped unique occurrences')
    nested=[x for s in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for x in js(s)['nested_fields'] if x['parent']=='Tchl']
    independent={(v['offset'],v['width']):v for v in pa['columns']};owner=f['unscoped_owner'];count=0
    for i,field in enumerate([*f['fields'],owner]):
        code=field.get('code','_owner'); p=field['profile'];sinks=field['sinks'] if code in SLOTS else [field['sink']]; cols=[];stats=[]
        for sink in sinks:
            off,w=sink['legacy_offset'],sink['width'];column=[buf[x+off:x+off+w] for x in body];cb=Counter(int.from_bytes(b,'little') for b in column);cols.append(column)
            z=independent[off,w];p0=[len(body),len(cb),min(cb),max(cb),cb[0],cb[(1<<(w*8))-1]];stats.append(p0)
            req(p0==[z[k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')],'t29 independent column metrics')
        req(stats==p['t29_unsigned_stats'],'ledger profile differential')
        def fixture(i,v):return dict(row=i,value=v,coordinates=[dict(offset=body[i]+s['legacy_offset'],hex=b[i].hex()) for s,b in zip(sinks,cols)])
        if code!='_owner':
            t=nested[i];req(field['schema']==catalog[0][i] and t['code']==code and t['idx']==562+i and t['type']==field['schema']['type'] and
                    field['scoped_occurrences']==[['club.xml','Tchl',562+i],['nation.xml','Tchl']],f'{code}: frozen and t24 occurrence tuple')
        if 'target_table' in field['domain']:
            tid=field['domain']['target_table'];m=maps[tid];keys=set(m.values());values=[S.unpack('<i',x)[0] for x in cols[0]];nn=values.count(-1)
            fail=[(i,x) for i,x in enumerate(values) if x!=-1 and x not in m];alt=[(i,x) for i,x in enumerate(values) if x!=-1 and x not in keys]
            req(p['violations']==len(fail)==0 and p['matches']==len(body)-nn and p['null_count']==nn and p['first_null']==fixture(values.index(-1),-1) and
                p['identity_lane_hypothesis']==dict(matches=len(body)-nn-len(alt),misses=len(alt),first_miss=fixture(*alt[0]) if alt else None),'ordinal domain and negative UID hypothesis')
            j=next(i for i,x in enumerate(values) if x>=0);v=values[j];w=dict(fixture(j,v),target_identity=m[v]);
            if tid==24:
                s,o,e=team[v];w.update(target_selector=s,target_selector_offset=o,target_identity_offset=e)
                req(Counter(team[x][0] for x in values if x!=-1)=={11:len(body)-nn} and p['target_selector_histogram']=={'11':len(body)-nn},'all live owner/opponent references to selector 11')
            req(w==p['first_join'],f'{code}: target key fixture')
            if code=='_owner':req(w==owner['club_exclusive_counterexample'] and (v,m[v],w['target_selector'])==(50,55,11),'club-only counterexample')
        elif code=='dbrt':
            xs=[(u[0],S.unpack('<b',v)[0]) for u,v in zip(*cols)];h=Counter(enum[v][u] if v in enum and u in (0,1) else 0 for u,v in xs)
            req(all(u in (0,1) and (v==-1 or v in enum) for u,v in xs) and {str(k):v for k,v in h.items()}==p['boxed_histogram'] and
                {f'{u},{v}':n for (u,v),n in Counter(xs).items()}==p['raw_pairs'],'two-byte Result domain')
            for t in p['first_single_lane_counterexample']:
                j=t['row'];u,v=xs[j];req(t==dict(fixture(j,[u,v]),boxed=enum[v][u]),'non-scalar enum counterexample')
        else:
            fmt='<b' if code=='posi' else '<H';xs=[S.unpack(fmt,x)[0] for x in cols[0]];hist=Counter(xs)
            lo,hi=(int(field['schema'][k]) for k in ('min_value','max_value'));bad=[(i,x) for i,x in enumerate(xs) if not lo<=x<=hi and not (code=='posi' and x==-1)]
            req(len(bad)==p['violations'] and p['first_violation']==(fixture(*bad[0]) if bad else None) and {str(k):v for k,v in hist.items()}==p['histogram'],'year/position domain')
            if code=='posi':req(p['first_sentinel']==fixture(xs.index(-1),-1) and hist[-1]==2650,'position sentinel count')
            else:req(len(bad)==(161 if code=='styr' else 21) and all(x==0 for _,x in bad),'years held on raw zero; no inferred sentinel')
        if code!='_owner':
            promoted=field['grade'].startswith('L3');req(promoted==(not p['violations']) and field['club_grade']=='held_not_club_exclusive' and
                field['club_first_counterexample']==owner['club_exclusive_counterexample'],'grade gating')
            for k in ('row_offset','wire_offset'):req(field[k]==(sinks[0]['legacy_offset' if k=='row_offset' else 'wire_offset'] if promoted and len(sinks)==1 else None),'do not publish scalar coordinates for held or compound entries')
            count+=promoted
    req(count==f['L3']==7 and f['club_exclusive_L3']==f['L4']==0,'ledger totals')


def verify():
    sys.path.extend([str(ROOT/'scripts'),'<OLD_REPO>/tools/python'])
    c=js(HERE/'cursor_tchl.json'); f=js(HERE/'fields_tchl.json'); req(c['table_type']==f['table_type']==34,'table scope')
    g,t,b,en=static_check(c,f);print('PASS PE CFG, native sinks, and shared parent dispatch')
    raw,fetch=db_check(c['archives']);rows=replay(raw,c['archives']['server'],g,t,b);print('PASS E66 frames, both 7,115-row mode forks, and footer')
    maps,team=identities(fetch,f['target_domains']);fields_check(c,f,raw,rows,maps,team,en);print('PASS independent profiles, actual target keys, 7 table L3 / 0 club-exclusive / 2 domain holds / L4=0')


def selftest():
    sys.path.append('<OLD_REPO>/tools/python')
    import zstandard as zs
    a,b=b'stub',b'full'*60;zc=zs.ZstdCompressor();x,y=zc.compress(a),zc.compress(b)
    aa,k=single(zs,x+y);bb,m=single(zs,(x+y)[k:]);req((aa,bb,k,m)==(a,b,len(x),len(y)),'independent frame ends')
    req(S.unpack('<i',b'\xff'*4)==(-1,) and S.unpack('<H',b'\xe1\x07')==(2017,), 'independent signed/null and year primitives')
    print('t39 verifier selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true',help='check frame and scalar primitives')
    try:
        selftest() if p.parse_args().selftest else verify();return 0
    except Check as e:print(f't39 verify FAIL: {e}',file=sys.stderr);return 1
    except (OSError,ValueError,RuntimeError,TypeError,KeyError,IndexError,ImportError,StopIteration,S.error) as e:
        print(f't39 verify fatal {type(e).__name__}: {e}',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
