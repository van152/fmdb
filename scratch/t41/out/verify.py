#!/usr/bin/env python3
"""Independently verify t41 against original PE bytes, archives, and frozen schema."""
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
EXE=Path('D:/tmp2b/fm24/input/editor.exe')
EXE_HASH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'
PROV='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
PAY_HASH='7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7'
MAGIC=b'\x28\xb5\x2f\xfd'
PRFX=bytes.fromhex('03017461642ef10d')
N=9079
START,END=0x15831a0,0x1583580
READ_SITE=(0x15831c9,0x15831e5,0x158320a,0x15832aa,0x15832d2,0x1583317,0x158351f)
IO_COND=(0x15831d0,0x15831ec,0x1583211,0x15832b1,0x15832fb,0x158331e,0x158332b)
WIRE=(0x158322d,0x1583250,0x15832da,0x158353a)
MODELS=('wire_data','runtime-external','IO-result','context-lifecycle','dead')

class Check(Exception): pass

def check(ok,msg):
    if not ok: raise Check(msg)

def js(p):return json.loads(p.read_bytes())
def sha(data):return sha256(data).hexdigest()
def uint(buf,p):return int.from_bytes(buf[p:p+4],'little')
def hist(values):return {str(k):v for k,v in sorted(Counter(values).items())}
def fail(fn):
    try:fn()
    except Check as e:return str(e)
    raise Check('negative fixture accepted')


def one_frame(z,b):
    d=z.ZstdDecompressor().decompressobj();a=d.decompress(b)
    check(d.eof,'incomplete zstd frame');return a,len(b)-len(d.unused_data)


def check_archives(c):
    os.environ.setdefault('FM24_DB_DIR',str(ROOT/'scratch/data'))
    import zstandard as z
    import fm24_dump as fm
    codec=fm._reader();reads={};main=None
    for side in ('client','server'):
        name=side+'_db.dat';_,data,layout=codec['_entries'](fm.DB_DIR/name,name)
        base=layout['data_base'];toc=layout['toc_offset'];es={e['path'].split('/')[-1]:e for e in layout['entries']}
        info=c[side];present=side=='server'
        check(base==34 and sha(data)==info['archive_sha256'] and len(es)==info['directory_entry_count']==(77 if present else 31) and
              ('table_59.dat' in es)==info['present']==present,'archive directory and digest')
        def read(member,data=data,base=base,toc=toc,es=es):
            e=es[member];beg=base+e['offset'];end=beg+e['packed_size']
            bound=min((base+v['offset'] for v in es.values() if v['offset']>e['offset']),default=toc)
            check(data[beg:beg+4]==MAGIC and end<=bound,member+' canonical magic/bound')
            b,used=one_frame(z,data[beg:end]);check(len(b)==e['size'] and used==end-beg,member+' canonical frame lengths')
            return b,beg,end,bound
        reads[side]=lambda name,read=read:read(name)[0]
        if not present:
            check(all(info[key] is None for key in ('entry','payload_sha256','row_count','stride','stride_histogram')),'client is absent, not a table with count zero');continue
        e=es['table_59.dat'];main,p,z_end,bound=read('table_59.dat');stub,s,z_stub,_=read('table_52.dat');old=es['table_52.dat']
        check(e==info['entry'] and len(main)==e['size']==224880 and p==38661659 and e['packed_size']==62202 and bound==z_end==info['bound'],
              'directory entry checked without treating entry SHA as payload SHA')
        check(info['entry_sha256_field']==e.get('sha256') and sha(main)==info['payload_sha256']==PAY_HASH,'independent decompressed SHA')
        check(s==e['offset']-1 and z_stub==p and len(stub)==22 and uint(stub,8)==0,'adjacent preceding member is not part of table59')
        start=e['offset'];first=data.index(MAGIC,start,start+68)
        check(first==p and len(info['frames'])==1,'old first-magic good for table59; no invented E66 failure')
        def frame(b,p,o,c):return dict(offset=p,relative_offset=p-o,compressed_bytes=c,payload_bytes=len(b),count=uint(b,8),sha256=sha(b))
        good=frame(main,p,start,z_end-p);prev=frame(stub,s,old['offset'],p-s)
        near=[frame(stub,s,s,p-s),frame(main,p,s,z_end-p)]
        q=info['adjacent_stub']
        check(info['frames']==[good] and info['selected_frame']==good and q['selected_frame']==prev and q['entry']==old and
              q['scan_from_previous_magic']==near and [x['offset'] for x in near if x['payload_bytes']==e['size']]==[p] and
              info['legacy_load']==dict(payload_bytes=len(main),sha256=sha(main)),'E66 all frame evidence')
    return main,reads


def check_pe(c,f):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from t05_pe import PE
    from t14_rtti_census import parse_rtti
    p=PE(EXE);p.pe.parse_data_directories(directories=[3]);md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    check(sha(p.raw)==EXE_HASH==c['provenance']['editor_sha256'],'read-only original editor SHA')
    manifest={d['path']:d['sha256'] for d in js(ROOT/'evidence/MANIFEST.json')['files']}
    for file in (MASTER,PROV):check(sha((ROOT/file).read_bytes())==manifest[file]==c['provenance']['frozen_snapshots'][file],f'frozen {file}')
    check(manifest[MASTER].startswith('7d57477e') and EXE_HASH in (ROOT/PROV).read_text(encoding='utf8'),'snapshot provenance')
    saved={}
    for path in c['instruction_shards']:
        for row in js(HERE/path)['instructions']:
            o=int(row['file_offset'],16);va=p.f2va(o);i=next(md.disasm(p.raw[o:o+15],va,1))
            check(o not in saved and p.va2f(va)==o and row['VA']==hex(va) and row['bytes']==i.bytes.hex() and
                  row['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),f'instruction shard byte/VA {o:#x}')
            saved[o]=i
    def direct(o):return p.va2f(saved[o].operands[0].imm)
    def rip(o):
        i=saved[o];m,=[x.mem for x in i.operands if x.type==3 and i.reg_name(x.mem.base)=='rip'];return i.address+i.size+m.disp
    def vs(v,j):return p.va2f(S.unpack_from('<Q',p.raw,p.va2f(v)+8*j)[0])
    def op(o,s):check(saved[o].op_str==s,f'{o:#x} operand assertion')
    def edge(o,t):check(direct(o)==t,f'{o:#x} direct edge')
    def imm(o,k):check(saved[o].operands[1].imm==k,f'{o:#x} immediate')
    base=p.va2f(rip(0xf48b45));case=c['factory'];cell=base+59*4;delta,=S.unpack_from('<i',p.raw,cell)
    check((base,cell,delta,base+delta,p.raw[cell:cell+4].hex())==tuple(case[x] for x in ('base','cell','rel32','handler','bytes')) and
          base+delta==0xf49950 and not case['selector_used'],'type59 rel32 dispatch')
    v=rip(0xf4996c);op(0xf49973,'qword ptr [rsi], rax');edge(0xf499b0,0xf49ca9)
    check(c['rtti']==parse_rtti(p,v) and c['rtti']['decorated']=='.?AVSTARTING_MEDIA_EXPECTATIONS@db@@' and
          {j:vs(v,int(j)) for j in c['slots']}==c['slots'] and vs(v,19)==START,'vptr COL/TD/slot19 direct')
    reader=c['reader'];rf=[(p.r2f(r.struct.BeginAddress),p.r2f(r.struct.EndAddress)) for r in p.pe.DIRECTORY_ENTRY_EXCEPTION if r.struct.BeginAddress==p.f2r(START)]
    check(rf==[(START,END)] and (hex(p.f2va(START)),hex(p.f2va(END)))==(reader['entry_VA'],reader['end_VA']) and
          reader['entry']==START and reader['end_exclusive']==END and saved[START].mnemonic=='push' and not reader['external_edges'],'real function extent/VA')
    branches={}
    for path in c['branch_shards']:
        for b in js(HERE/path)['branches']:
            o=b['site'];i=saved[o]
            check(o not in branches and i.mnemonic.startswith('j') and i.mnemonic!='jmp' and b['taken_to']==direct(o) and
                  b['fallthrough_to']==o+i.size and all(x in saved for x in [b['predicate'],*b['evidence']]) and b['source'] and b['first_counterexample_or_constraint'],
                  f'branch link/predicate/negative {o:#x}')
            branches[o]=b
    check(c['branch_classes']==list(MODELS) and hist(b['class'] for b in branches.values())=={k:v for k,v in c['branch_counts'].items() if v},'five-class counts')
    graph={};stack=[START];cond=set();calls=set()
    while stack:
        o=stack.pop()
        if o in graph:continue
        check(START<=o<END and o in saved,'CFG reachable extent/evidence');i=saved[o];nxt=o+i.size
        if i.mnemonic=='ret':xs=[]
        elif i.mnemonic=='jmp':xs=[direct(o)]
        elif i.mnemonic.startswith('j'):
            xs=[direct(o),nxt];cond.add(o);b=branches[o];check(b['scope']=='slot19','reader branch scope')
            expected='wire_data' if o in WIRE else 'IO-result' if o in IO_COND else 'context-lifecycle'
            pred=saved[b['predicate']]
            check(b['class']==expected and b['changes_normal_row_length']==(o in WIRE[:2]) and
                  (pred.address+pred.size==i.address or o in (0x15833e2,)),'wire vs context predicate and length rule')
        else:xs=[nxt]
        if i.mnemonic=='call':calls.add(o)
        graph[o]=set(xs);stack+=xs
    listed={}
    for block in reader['blocks']:
        seq=block['sites']
        for k,o in enumerate(seq):
            check(o not in listed,'duplicate CFG instruction');listed[o]=set([seq[k+1]] if k+1<len(seq) else block['successors'])
    check(listed==graph and len(graph)==reader['reachable']==260 and len(reader['blocks'])==49 and
          len(cond)==reader['branches']==29 and cond=={o for o,b in branches.items() if b['scope']=='slot19'} and
          calls==set(READ_SITE)|set(map(int,reader['summarized_nontransfer_calls'])),'independent CFG, all calls and conditionals enumerated')
    check([saved[b].mnemonic for b in WIRE]==['je','jae','jne','jb'],'wire predicates direction')
    for o,s in [(0x1583228,'dword ptr [rsp + 0x40], 0'),(0x1583246,'rsi'),(0x1583249,'eax, dword ptr [rsp + 0x40]'),
                (0x158324d,'rsi, rax'),(0x15832d5,'dword ptr [r14 + 4], 0'),(0x15832df,'dword ptr [r14 + 4], eax'),
                (0x1583533,'r8d, 0x989681'),(0x158353c,'r8d, dword ptr [rsp + 0xc8]'),(0x1583544,'dword ptr [rbx], r8d'),
                (0x158350c,'rbx, [r13 + 8]'),(0x158328b,'byte ptr [rax + 8], 1'),(0x1583241,'qword ptr [r13 + 0x20], 8')]:op(o,s)
    def stack_uses(d):return [o for o in graph for x in saved[o].operands if x.type==3 and saved[o].reg_name(x.mem.base)=='rsp' and x.mem.disp==d]
    check(stack_uses(0x47)==[0x15832a5],'tag has no subsequent in-reader load or predicate')
    check(stack_uses(0xd0)==[] and
          reader['caller_mode']==dict(forwarded_site=0xf2ba38,callee_slot='rsp+0xd0',read=False,forks=[1,0]),'no slot19 mode read')
    op(0x15831ac,'rsp, 0x58');check(sum(saved[o].mnemonic=='push' for o in graph)==8,'callee mode slot calculation')
    for o,s in [(0xf2b670,'r12d, r9d'),(0xf2ba38,'byte ptr [rsp + 0x30], r12b'),(0xf28c13,'r9b, 1'),
                (0xf2ba51,'qword ptr [rbx + 0x98]'),(0xf2ba0e,'qword ptr [rax + 0x28]')]:op(o,s)
    edge(0xf2ba23,0xf48b30);edge(0xf2ba7f,0xffa5d0)
    check([r['site'] for r in c['transfers']]==[0xf2ba0e,*READ_SITE],'selector, prefix, loop item and identity sites')
    for r,w,b,m,rdx in zip(c['transfers'][1:],(4,1,4,1,8,1,12),(0,4,5,9,10,18,9),(0,0,0,10,10,10,10),
                         ('rdx, [rcx + 0x30]','rdx, [r13 + 0x38]','rdx, [rsp + 0x40]','rdx, [rsp + 0x47]','rdx, r14','rdx, 8','rdx, rbx'),strict=True):
        op(r['site'],'qword ptr [rax + 0x28]');op(r['rdx_setup'],rdx);op(r['r8d_setup'],f'r8d, {w:#x}' if w>=10 else f'r8d, {w}')
        check((r['width'],r['legacy_base'],r['wire_base'],r['multiplier'])==(w,b,b+1,m),'cursor transfer coordinates')
    for r in c['outer_transfers']:
        op(r['site'],'qword ptr [rax + 0x28]');imm(r['width_setup'],r['width'])
    sc=c['scope_evidence'];rt=sc['rtti'];vt={name:tr['vtable_va'] for name,tr in rt.items()}
    check(all(parse_rtti(p,tr['vtable_va'])==tr and tr['class']==name for name,tr in rt.items()),'owner and Media Source RTTIs')
    check(vs(vt['CLUB'],2)==0xe89a00 and vs(vt['CLUB'],3)==0xe82aa0 and vs(vt['MEDIA_SOURCE'],19)==0x15457c0,'actual editor entry slots')
    for o in (0xe8cb93,0xe8411d):imm(o,0x43736d65)
    for o,t in [(0xe8cb99,0xe8db41),(0xe8db54,0xeb4430),(0xeb4430,0x3b17180),(0x3b173e8,0xeb0bd0),(0xeb0bd0,0x3b0f420),
                (0x3b0f452,0x154d690),(0x154d690,0x43803c0),(0x3b0f518,0x154d750),(0x154d750,0x4381560),
                (0xe84123,0xe854cc),(0xe854eb,0xeafe10),(0xeb0060,0x15329d0),(0x15329d0,0x4365f50),(0x4365fa4,0xf8d120),
                (0xf8d120,0x3c0d7b0),(0x3c0d817,0x1582d60),(0x1583580,0x43d2bb0),(0x43d2bda,0xf7e440),(0xf7e440,0x3bf3460),(0x15835c0,0x43d2e40),
                (0xf4911f,0x1052b30),(0x1052b30,0x3d7afc0),(0xf49ca4,0x11a0160),(0x11a0160,0x3e68540),(0xf48eb1,0x1545680),(0x1545680,0x437a080)]:edge(o,t)
    check(rip(0x1582d98)==v and rip(0x3d7afdb)==vt['NATIONAL_TEAM'] and rip(0x3e6858b)==vt['TEAM'] and rip(0x437a0a5)==vt['MEDIA_SOURCE'],'RTTI constructor anchors')
    check(rip(0x3b171ac)==rip(0xeafe9b)==rip(0x4365f59)==rip(0x4365f97)+0x440==int(sc['collection_global_VA'],16),'collection getter/add/constructor share table')
    for o,s in [(0x3b171b3,'rcx, qword ptr [rax + 0x80]'),(0x3b171d3,'qword ptr [rbx + 0x30], rdx'),(0x3b173c0,'rax, qword ptr [rsi + 0x18]'),
                (0x3b173c4,'rsi, qword ptr [rax + rbx*8]'),(0x1582dfd,'qword ptr [rsi + 0x30], rdi'),(0x43d2e7c,'rax, qword ptr [r12 + 0x30]'),
                (0x43d2e86,'eax, dword ptr [rax + 8]'),(0x43d2e8b,'eax, 0xffffffff'),(0x3bf34b2,'edx, dword ptr [rsi]'),
                (0x3bf350e,'rax, qword ptr [rcx + rax*8]'),(0x3bf3512,'qword ptr [rsi], rax'),(0xf49106,'bl, 0xb')]:op(o,s)
    edge(0xf49100,0xf49c4a)
    for k,q in sc['table_factory_cells'].items():
        o=base+4*int(k);d,=S.unpack_from('<i',p.raw,o);check(q==dict(cell=o,rel32=d,handler=base+d,bytes=p.raw[o:o+4].hex()),'target factory cells')
    ms,me=f['fields'];check(ms['code']=='Msid' and me['code']=='Melf','exact field census')
    for r in (ms,me):imm(r['getter']['compare'],int.from_bytes(r['code'].encode(),'big'))
    edge(0x438157d,0x4381596);edge(0x438158f,0xfe68b0);edge(0xfe68cd,0xfe6983)
    imm(0x4381587,0x4d656453)
    check(saved[me['getter']['member_load']].mnemonic=='movzx' and me['getter']['member_offsets']==[8] and
          ms['getter']['lane_loads']==[0xfe68e4,0xfe68eb] and ms['getter']['member_offsets']==[0,4],'native unsigned scalar and native two lanes')
    for o,s in [(0x4381596,'edi, byte ptr [rcx + 8]'),(0xfe68ca,'dword ptr [rcx], 0'),(0xfe68e4,'eax, dword ptr [rbx + 4]'),
                (0xfe68eb,'rbx, dword ptr [rbx]'),(0xfe71ec,'ecx, dword ptr [rax + 0xc]'),(0xfe71f2,'eax, dword ptr [rax + 0x10]'),
                (0xeb00b9,'byte ptr [rsi + 8], al'),(0xeb00fd,'qword ptr [rsi], rax'),(0x43d2f77,'rdx, r15'),(0x43d2f86,'rdx, [r15 + 4]'),
                (0x43d2fa2,'r15, 8'),(0x43d2faf,'rdx, r15')]:op(o,s)
    check([ms['candidate_sink'][k] for k in ('site','width','legacy','wire')]==[READ_SITE[4],8,'10+10*j','11+10*j'] and
          [me['sink'][k] for k in ('site','width','legacy','wire','writer_site')]==[READ_SITE[5],1,'18+10*j','19+10*j',0x43d2fb2] and
          me['sink']['when']==ms['candidate_sink']['when']=='0 <= j < count' and ms['write_sites']==[0x43d2f7a,0x43d2f96],'actual, conditional native field sinks')
    # table7 landmark checks; no dependency on t41 builder or on a saved t41 row dump.
    edge(0x1545ec6,0xfae340);edge(0xfae340,0x3c600f0);op(0x3c60119,'qword ptr [rax + 0x28]');op(0x3c6010d,'r8d, 0xc')
    return branches


def decode(buf,p,i):
    """Sequential wire reference decoder (no CFG execution or tail search)."""
    def span(o,w):
        check(o+w<=len(buf),f'short transfer @{o} width {w}');return buf[o:o+w]
    a=p;span(a,1);span(a+1,4);span(a+5,1);span(a+6,4)
    sel,owner,outer,count=S.unpack_from('<B i B I',buf,a);p+=10;pairs=[];tx=[(READ_SITE[0],a+1),(READ_SITE[1],a+5),(READ_SITE[2],a+6)]
    for j in range(count):
        span(p,1);span(p+1,8);span(p+9,1);tag,x,y,rank=S.unpack_from('<BiiB',buf,p)
        pairs.append(dict(offset=p,tag=tag,raw_pair=[x,y],stored_pair=[x,y if y else x],finish=rank))
        tx.extend(zip(READ_SITE[3:6],(p,p+1,p+9)));p+=10
    triple=S.unpack('<III',span(p,12));stored=triple[0] if triple[0]<10000001 else i
    check(triple[0]==i==stored and triple[1]==triple[2]!=0,f'row {i}: raw identity @{p} {triple}, stored ordinal={stored}')
    tx.append((READ_SITE[6],p));p+=12
    return dict(ordinal=i,selector=sel,selector_start=a,body_start=a+1,end=p,owner=owner,outer_byte=outer,count=count,
                items=pairs,identity=list(triple),stored=stored),[list(t) for t in tx]


def decode_footer(buf,p):
    check(p+9<=len(buf),f'footer: short @{p} width 9');vec,flag,last=S.unpack_from('<IBI',buf,p)
    check(vec==0,f'footer @{p}: count {vec}, requires {12*vec} triplet bytes');check(p+9==len(buf) and flag==1,'footer closure')
    return vec,flag,last


def replay(buf,a,branches):
    check(buf[:8]==PRFX and buf[:13].hex()==a['header_hex'] and uint(buf,8)==N==a['row_count'] and
          (a['wire_origin'],a['legacy_origin'],a['version'],a['stride'])==(13,14,0xdf1,None),'main header and dual-coordinate origins')
    modes=a['forks'];rs=None
    for mode in ('0','1'):
        m=modes[mode];p=13;seen=set();lengths=[];items=[];entries=[];sigs=sha256();rlist=[];edge=Counter()
        for i in range(N):
            r,tx=decode(buf,p,i);e=r['end'];ct=r['count'];q=r['identity'];check(q[1] not in seen and e-p==22+10*ct,'identity unique / variable extent')
            seen.add(q[1]);lengths.append(e-p);items.append(ct);entries.extend(r['items']);rlist.append(r)
            sigs.update(S.pack('<9I',i,p,p+1,e,r['selector'],ct,*q)+sha256(buf[p:e]).digest())
            for o in IO_COND[:3]:edge[o,o==IO_COND[2]]+=1
            for o in IO_COND[3:]:edge[o,False]+=ct
            edge[WIRE[0],ct==0]+=1;edge[WIRE[1],True]+=bool(ct);edge[WIRE[1],False]+=max(0,ct-1)
            for entry in r['items']:edge[WIRE[2],entry['raw_pair'][1]!=0]+=1
            edge[WIRE[3],q[0]<10000001]+=1
            if i in (0,1,2,N-1):
                s=[w for w in m['samples'] if w['ordinal']==i];check(s==[dict(r,wire_hex=buf[p:e].hex(),transfer_offsets=tx)],f'mode {mode} row sample {i}')
            p=e
        check(sigs.hexdigest()==m['trace_sha256'] and (sum(lengths),len(seen),m['row_bytes'],m['identity_valid'],m['rows'])==(224858,N,224858,N,N),
              'full replay traces in both forwarded modes')
        check(hist(lengths)==a['stride_histogram']==m['stride_histogram']=={'22':6567,'32':2512} and hist(items)==m['counts']=={'0':6567,'1':2512} and
              hist(r['selector'] for r in rlist)==m['selectors']==hist(buf[r['end']] for r in rlist)==m['legacy_markers']=={'0':N},'native row lengths/selector/legacy marker')
        check(all([edge[o,True],edge[o,False]]==m['edges'][str(o)]==branches[o]['edges_by_mode'][mode] for o in (*IO_COND,*WIRE)),'all replayed conditional edges')
        foot=a['wire_footer'];check(foot==m['footer'] and p==foot['offset']==224871 and p+9==len(buf)==a['payload_bytes']==224880 and
              buf[p:].hex()==foot['hex']=='00'+a['legacy_footer_hex'] and a['legacy_footer_offset']==p+1 and
              decode_footer(buf,p)==(foot['count'],foot['flag'],foot['last_u32'])==(0,1,9079) and
              foot['last_u32']==max(seen),'9-byte footer, last u32 observation and legacy framing')
        check(rs is None or rlist==rs,'both ABI modes identical');rs=rlist
    neg=a['negative_replays'];base=rs[2];pos=base['items'][0]['offset'];after=base['end']-12
    changed=bytearray(buf);changed[13]=1
    check(decode(changed,13,0)[0]==neg['selector_one'],'selector 1 changes neither native width nor identity')
    for start,w,value,key in [(23,4,10000001,'identity_overwrite'),(31,4,0,'unequal_identity'),(27,8,0,'zero_identity'),(19,4,1,'changed_count_on_same_bytes')]:
        b=bytearray(buf);b[start:start+w]=value.to_bytes(w,'little')
        check(neg[key]==fail(lambda:decode(b,13,0)),f'negative replay {key}')
    b=bytearray(buf);S.pack_into('<I',b,base['body_start']+5,2);b[after:after]=S.pack('<BiiB',128,5,0,255)
    new,_=decode(b,base['selector_start'],2)
    check(new==neg['second_entry']['row'] and neg['second_entry']['loop_back_taken'] and new['end']==base['end']+10 and
          new['items'][1]['stored_pair']==[5,5] and new['items'][1]['finish']==255 and new['items'][1]['tag']==0x80,'observable loop backedge fixture, no tag mask, no signed -1')
    b=bytearray(buf);b[pos+9]=0;z,_=decode(b,base['selector_start'],2)
    check(dict(row=2,offset=pos+9,value=z['items'][0]['finish'],end=z['end'],count=z['count'])==neg['materialized_zero_rank'] and
          z['items'][0]['finish']==0 and z['count']==1,'zero remains a materialized scalar')
    setup=[(14,4,0),(18,1,0),(19,4,0),(pos,1,2),(pos+1,8,2),(pos+9,1,2),(23,12,0)]
    for site,(off,w,i) in zip(READ_SITE,setup):
        # A truncated stream is independent of the builder's injected status at a site.
        message=fail(lambda:decode(buf[:off+w-1],rs[i]['selector_start'],i))
        check(message==f'short transfer @{off} width {w}' and f'@{off} width {w}' in neg['short_transfers'][str(site)],'short transfer repro')
    b=bytearray(buf);b[p]=1
    check(neg['nonzero_footer']==fail(lambda:decode_footer(b,p)) and neg['short_footer']==fail(lambda:decode_footer(buf[:-1],p)),'footer negative anchors')
    return rs


def check_prior(c,raw,rs):
    d=c['t33_differential'];pro=js(ROOT/d['path']);b=(ROOT/d['rows_file']).read_bytes();old=pro['row_closure'];q=pro['payload'];p=14;diff=[];lens=[]
    check(d['path']=='scratch/t33/out/profiles/table_server_59.profile.json' and q['payload_sha256']==sha(raw) and
          q['payload_size']==len(raw) and sha((ROOT/d['path']).read_bytes())==d['sha256'] and sha(b)==d['rows_file_sha256']==pro['full_rows_sha256'] and
          old['frame_ambiguity']==d['t33_ambiguity'] and old['count']==N,'unchanged t33 profile anchor')
    for r,line in zip(rs,b.splitlines(),strict=True):
        t=json.loads(line);e=p+t['len'];i=r['ordinal'];lens.append(t['len'])
        check((t['row'],t['offset'],t['raw_hex'])==(i,p,raw[p:e].hex()),'t33 raw row slices')
        if t['offset']!=r['body_start'] or e!=r['end']+1:
            s=r['body_start'];w=r['end']+1
            diff.append(dict(row=i,t33=t,native=dict(offset=s,len=w-s,bytes=raw[s:w].hex(),identity=r['identity']),
                             t33_tail=list(S.unpack_from('<III',raw,e-13)),marker=raw[e-1]))
        p=e
    check(hist(lens)==d['t33_stride_histogram']=={'19':1,'22':6565,'25':1,'32':2512} and p==224872 and
          sha(raw[14:p])==old['rows_sha256']==d['row_block_sha256'] and diff==d['differences'] and d['matching_rows']==9077,
          'native corrects two t33 rows without changing legacy row-block digest')
    check(diff[0]['t33_tail']==[0,16777216,16777216] and diff[0]['native']['len']==diff[1]['native']['len']==22 and
          diff[1]['native']['offset']==36 and diff[1]['t33']['offset']==33,'first false shortest-tail witness, then resync')
    h=d['historical_negative'];orig=(ROOT/h['path']).read_bytes()
    check(sha(orig)==h['sha256'] and h['quote'] in orig.decode('utf8'),'old negative retained verbatim')


def media_keys(buf,server,rec):
    # Walk table7 only to extract its identity keys. Width groups follow slot19 and string/pair helpers.
    pos=13;keys={};digest=sha256();n=uint(buf,8)
    def skip(count):
        nonlocal pos
        check(0<=count<=len(buf)-pos,'target table7 overrun');at=pos;pos+=count;return at
    def group(width):
        k=uint(buf,skip(4));skip(k*width)
    for nr in range(n):
        check(buf[skip(1)]==0,'target selector 0')
        group(1);skip(1);group(1);group(1);group(1);skip(2)  # name/vector/both text lanes, 2 bytes
        group(4);skip(4);group(4);group(4);skip(4)
        for _ in range(uint(buf,skip(4))):skip(8);group(1)
        if server:skip(6);skip(4*buf[skip(1)])
        group(4);skip(1);q=skip(12);a,b,c=S.unpack_from('<III',buf,q)
        check(a==nr and b==c and b!=0,'table7 actual key frames');keys[a]=b;digest.update(S.pack('<4I',q,a,b,c))
    check(n==208==len(set(keys.values())) and pos+9==len(buf) and buf[pos:pos+5]==bytes.fromhex('0000000001') and
          rec==dict(count=n,payload_bytes=len(buf),payload_sha256=sha(buf),footer_offset=pos,identity_trace_sha256=digest.hexdigest()),'table7 key coverage and footer')
    return keys


def team_keys(b,extra,d):
    n=uint(b,8);z=len(b)-9
    check(n==84507==uint(extra,8)==d['ordinal_witness_count']==d['count'] and sha(b)==d['payload_sha256'] and sha(extra)==d['sidecar_sha256'] and
          len(extra)==12+82*n and [uint(extra,p) for p in range(12,len(extra),82)]==list(range(n)),'team ordinal sidecar')
    # Alternative enumeration: index legal *next selector* bytes rather than duplicate lanes.
    seq=[[] for _ in range(n)];x,y,q=S.unpack_from('<III',b,z-12)
    check(x==n-1 and y==q!=0 and b[13] in (10,11),'team first selector and last identity')
    seq[-1].append(z-12)
    for m in re.finditer(rb'[\x0a\x0b]',b[26:z]):
        p=14+m.start();j,u,v=S.unpack_from('<III',b,p)
        if j<n-1 and u==v!=0:seq[j].append(p)
    limit=14
    for s in seq:
        k=bisect_left(s,limit);check(k<len(s),'team earliest prefix feasible');del s[:k];limit=s[0]+13
    limit=z-12
    for s in reversed(seq):
        del s[bisect_right(s,limit):];check(len(s)==1,'team latest suffix and unique boundary');limit=s[0]-13
    r={};pos=13;h=sha256()
    for j,(p,) in enumerate(seq):
        r[j]=(b[pos],pos,p,uint(b,p+4));h.update(S.pack('<5I',j,*r[j]));pos=p+12
    check(pos==z and len({v[3] for v in r.values()})==n and h.hexdigest()==d['identity_trace_sha256'] and
          hist(v[0] for v in r.values())==d['selector_histogram']=={'10':84256,'11':251},'Team uniqueness/selector witnesses')
    return r


def check_fields(f,raw,rs,fetch):
    entities=js(ROOT/MASTER)['entities'];p,=[x for v in entities['club.xml'] for x in v['fields'] if x['field']=='Csme']
    occ=ROOT/f['occurrences_source'];oo=[x for x in js(occ)['nested_fields'] if x['parent']=='Csme']
    check(sha(occ.read_bytes())==f['occurrences_sha256'] and len(p['list_item_fields'])==len(oo)==len(f['fields'])==2,'unique Csme scoped schema occurrence')
    for y,x,r in zip(p['list_item_fields'],oo,f['fields'],strict=True):
        check(r['schema']==y and r['occurrence']==['club.xml','Csme',x['idx']] and r['code']==y['field']==x['code'] and y['type']==x['type'],'frozen and t24 occurrence joins')
    check([x['idx'] for x in oo]==[174,175],'t24 stable indices')
    ms,me=f['fields'];pm,pe=ms['profile'],me['profile'];media=f['targets']['media_source'];check(media['table']==7 and ms['schema']['database_table_type']=='media_source','target table identity')
    mc=media_keys(fetch['client']('table_7.dat'),False,media['archives']['client']);msrv=media_keys(fetch['server']('table_7.dat'),True,media['archives']['server'])
    check(mc==msrv and list(mc)==media['ordinal_keys'] and sha(b''.join(S.pack('<II',i,u) for i,u in mc.items()))==media['uid_trace_sha256'],
          'both table7 domains and ordinal-to-ID digest')
    team=team_keys(fetch['server']('table_24.dat'),fetch['server']('table_extra_24.dat'),f['targets']['team'])
    owners=f['unscoped_owner'];keys=[r['owner'] for r in rs];check(all(k in team for k in keys),'owner actual FK hits')
    check(owners['matches']==owners['distinct']==len(set(keys))==N and owners['minus_one_count']==0 and
          hist(team[k][0] for k in keys)==owners['selector_histogram']=={'10':8941,'11':138},'owner split, not exclusive')
    examples={}
    for r in rs:
        o=r['body_start'];v=r['owner'];s,b,p,t=team[v];examples.setdefault(str(s),dict(row=r['ordinal'],offset=o,bytes=raw[o:o+4].hex(),value=v,target_selector=s,
                                                                                     target_selector_offset=b,target_identity_offset=p,target_identity=[v,t,t]))
    check(examples==owners['first_by_selector'] and examples['11']==owners['scope_counterexample'] and
          examples['11']['row']==examples['11']['value']==0 and examples['11']['target_identity']==[0,5,5],'first counterexample to club exclusivity')
    items=[(r,j,x) for r in rs for j,x in enumerate(r['items'])];absent=sum(r['count']==0 for r in rs);vals=[v['finish'] for _,_,v in items];pairs=[tuple(v['raw_pair']) for _,_,v in items]
    for prof in (pm,pe):check((prof['entries'],prof['rows'],prof['no_entry_rows'])==(len(items),N,absent)==(2512,N,6567),'conditional coverage counts')
    r,j,x=items[0];pos=x['offset'];first=dict(row=r['ordinal'],entry=j,entry_offset=pos,hex=raw[pos:pos+10].hex(),pair_offset=pos+1,finish_offset=pos+9,
                                             pair=x['raw_pair'],finish=x['finish'],outer_offset=r['body_start']+4,outer_byte=r['outer_byte'])
    live=[x for x in pairs if x[0]>=0];uids=set(mc.values())
    check(hist(f'{a},{b}' for a,b in pairs)==pm['raw_pairs']=={'-1,-1':2512} and pm['null_pairs']==2512 and pm['zero_lane_count']==pm['normalized_copy_count']==0 and
          (pm['live'],pm['ordinal_matches'],pm['uid_matches'])==(len(live),sum(a in mc for a,_ in live),sum(a in uids for a,_ in live))==(0,0,0) and
          pm['first_null']==pm['first_not_a_live_ordinal']==first and -1 not in mc and pm['first_domain_conflict'] is None,'no populated media key, not an ordinal miss on optional null')
    alias=pm['rejected_outer_owner_as_media_ordinal'];no=[r for r in rs if r['owner'] not in mc];r=no[0];q=r['body_start'];n=r['owner'];s,o,p,k=team[n]
    check(alias==dict(matches=N-len(no),misses=len(no),first_miss=dict(row=r['ordinal'],offset=q,bytes=raw[q:q+4].hex(),value=n,
          target_selector=s,target_selector_offset=o,target_identity_offset=p,target_identity=[n,k,k])),'reject outer owner as a media_source ordinal')
    max_xml=int(me['schema']['max_value']);check(max_xml==127 and pe['min']==min(vals)==1 and pe['max']==max(vals)==33 and hist(vals)==pe['histogram'] and
          pe['zero_count']==vals.count(0)==pe['minus_one_count']==pe['raw_ff_count']==vals.count(255)==pe['violations']==sum(n>max_xml for n in vals)==0 and
          pe['bit_mask'] is None and pe['first_domain_conflict'] is None and pe['first_value']==me['negative_outer_byte_alias']==first and first['outer_byte']==2!=first['finish']==4,
          'unsigned rank profile and negative outer scalar alias')
    outer=f['outer_non_schema_byte'];tag=f['inner_tag'];check(hist(r['outer_byte'] for r in rs)==outer['unsigned_histogram'] and outer['zero_count']==114 and
          tag['histogram']==hist(x['tag'] for _,_,x in items)=={'1':2512} and tag['tested_mask'] is None and tag['boolean_claim'] is False,'no bool or sentinel invented')
    check(ms['grade']=='held_no_live_media_reference' and ms['row_offset'] is None and ms['wire_offset'] is None and
          me['grade']=='L3_table59_conditional_named_coordinate' and (me['row_offset'],me['wire_offset'])==(18,19) and
          f['native_binding_count']==2 and f['L3']==1 and f['club_exclusive_L3']==f['L4']==0,'grade gate, conditional publication only')


def verify():
    sys.path.extend([str(ROOT/'scripts'),'D:/tmp2b/fm24/tools/python'])
    c=js(HERE/'cursor_csme.json');f=js(HERE/'fields_csme.json');check(c['table_type']==f['table_type']==59 and c['parent']==f['parent']=='Csme','task scope')
    branches=check_pe(c,f);print('PASS PE extent, independent CFG, native transfers, mode ABI, and 4CC/owner routes')
    b,fetch=check_archives(c['archives']);rs=replay(b,c['archives']['server'],branches);check_prior(c,b,rs)
    print('PASS bounded frames, both 9079-row forks, variable closure and two t33 counterexamples')
    check_fields(f,b,rs,fetch);print('PASS actual target keys; Melf conditional L3, Msid held, club-exclusive 0, L4=0')


def selftest():
    sys.path.append('D:/tmp2b/fm24/tools/python');import zstandard as z
    q=z.ZstdCompressor();a=q.compress(b'short');b=q.compress(bytes(range(40)))
    check(one_frame(z,a+b)==(b'short',len(a)) and one_frame(z,(a+b)[len(a):])==(bytes(range(40)),len(b)),'two-frame boundaries')
    for n in range(3):
        a=S.pack('<BiBI',0,0,2,n)+S.pack('<BiiB',128,0,0,255)*n+S.pack('<III',0,1,1)
        r,t=decode(a,0,0);check(r['end']==22+n*10 and len(t)==4+n*3 and all(e['finish']==255 and e['stored_pair']==[0,0] for e in r['items']),
                                    'zero ordinal is distinct from null; 0xff is unsigned and count controls extent')
        check('short' in fail(lambda:decode(a[:-1],0,0)),'short tail fixture')
    print('t41 verifier selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true',help='test independent framing, count loop and signed/unsigned decoding')
    try:
        selftest() if ap.parse_args().selftest else verify();return 0
    except Check as e:print('t41 verify FAIL:',e,file=sys.stderr);return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't41 verify fatal {type(e).__name__}: {e}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
