#!/usr/bin/env python3
"""Independently verify Cmti/table 43 PE, archive, context and all-row field evidence."""
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
T29 = 'scratch/t29/out/profiles/table_server_43.profile.json'
ROWS = 'scratch/t29/out/profiles/table_server_43.rows.jsonl'
INV = 'scratch/t29/out/subtable_inventory.json'
N, W = 535, 46
PAYLOAD_SHA = '7981267028706e701d39a32126b5b2e85f9b4973266cf1545f09869a524a069e'
# Independently transcribed: legacy, width, object, stream call, setup LEA/MOV, schema code.
LAYOUT = (
    (0,8,0x18,0x437088f,0x437087b,0x4370886,'play'), (8,8,0x20,0x43708d8,0x43708c4,0x43708cf,'club'),
    (16,8,0x28,0x4370921,0x437090d,0x4370918,'club'), (24,4,0x30,0x437095d,0x437094d,0x4370954,'mths'),
    (28,4,0x34,0x4370979,0x4370969,0x4370970,'cash'), (32,1,0x38,0x4370995,0x4370985,0x437098c,'pyiv'),
    (33,12,8,0x3c60119,0x3c60106,0x3c6010d,None),
)
NORMS = {0x4370896:0,0x43708df:8,0x4370928:16}
STATUS = dict(zip((0x43708b6,0x43708ff,0x4370948,0x4370964,0x4370980,0x437099c),[r[3] for r in LAYOUT[:-1]],strict=True))
ARM = {'icom':0x153c9d0,'club':0x153ca7f,'play':0x153ca10,'cash':0x153ca21,'mths':0x153ca9b,'pyiv':0x153caf9}
CLASSES = {'wire_data':9,'runtime-external':1,'IO-result':17,'context-lifecycle':13,'dead':0}


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
    end=13+W*count
    req(buf[:8]==bytes.fromhex('03017461642ef10d') and len(buf)==end+9,'header/envelope')
    req(S.unpack_from('<IB',buf,8)==(count,0) and buf[end:end+5]==bytes.fromhex('0000000001'),'header fields/footer prefix')
    return [buf[k:k+W] for k in range(13,end,W)],S.unpack_from('<I',buf,end+5)[0]


def keys(a,b,ctx):
    """Observed exact lookup path: non-aliased, both endpoints re-joined to local identities."""
    return int(ctx==b), (b,16) if ctx==a else (a,8)


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

    vf=0x141883a68; base=0xf49d38; cell=base+4*43
    j=c['factory']; rel=S.unpack_from('<i',pe.raw,cell)[0]
    req(rip(0xf48b45)==pe.f2va(base) and base+rel==0xf49675 and (j['jump_base'],j['cell'],j['rel32'],j['cell_bytes'])==
        (base,cell,rel,pe.raw[cell:cell+4].hex()),'factory rel32')
    text(0xf48b4c,'rax, dword ptr [rcx + rax*4]');text(0xf48b53,'rax');text(0xf496a9,'qword ptr [rsi], rax')
    req(rip(0xf496a2)==vf and dest(0xf496c8)==0xf49ca9 and not any(ins[o].mnemonic.startswith('j') for o in j['handler'][:-1]),'constructor/selector independence')
    vt=pe.va2f(vf); col=pe.va2f(S.unpack_from('<Q',pe.raw,vt-8)[0]); sig,obj,_,tdrv=S.unpack_from('<4I',pe.raw,col)
    td=pe.r2f(tdrv)
    req(sig==1 and obj==0 and col==0x18859c0==c['rtti']['col_off'] and td==c['rtti']['td_off'] and
        pe.raw[td+16:pe.raw.index(0,td+16)]==b'.?AVSTARTING_MONTHLY_INSTALLMENT@db@@' and
        c['rtti']['class']=='STARTING_MONTHLY_INSTALLMENT','MSVC RTTI descriptor')
    for k,v in {2:0x14153d380,3:0x14153d850,19:0x14153d0a0,20:0x1400015e0,21:0x14153d210}.items():
        req(S.unpack_from('<Q',pe.raw,vt+k*8)[0]==c['slots'][str(k)]==v,'vtable slot')
    r=c['reader']; chain=[0x153c6a0,0x4370860,0x43709c1,0xfae340,0x3c600f0]
    req(r['chain']==chain and not r['runtime_mode_forks'],'reader chain/mode')
    for a,b in ((chain[0],chain[1]),(chain[2],chain[3]),(chain[3],chain[4])):
        req(ins[a].mnemonic=='jmp' and dest(a)==b,'real tail jumps')
    entries=[e.struct for e in pe.pe.DIRECTORY_ENTRY_EXCEPTION]
    def extent(o):
        rv=pe.f2va(o)-pe.base
        return [e for e in entries if e.BeginAddress<=rv<e.EndAddress]
    req(not extent(chain[0]) and not extent(chain[3]),'leaf jumps unexpectedly have extents')
    internal={}
    for d,(start,end,ic,bc) in zip(r['extents'],[(0x4370860,0x43709c6,118,26),(0x3c600f0,0x3c6016e,43,11)],strict=True):
        rt,=extent(start)
        req(pe.r2f(rt.BeginAddress)==d['entry']==start and pe.r2f(rt.EndAddress)==d['end_exclusive']==end and
            int(d['entry_VA'],16)==pe.f2va(start) and int(d['end_exclusive_VA'],16)==pe.f2va(end),'runtime-function extent')
        graph={}; external=[]; todo=[start]
        while todo:
            o=todo.pop()
            if o in graph:
                continue
            i=ins[o]; nxt=[]
            if i.mnemonic.startswith('j'):
                t=dest(o)
                if not start<=t<end:
                    req(i.mnemonic=='jmp' and o==chain[2] and t==chain[3],'unexpected exterior branch')
                    external.append({'from':hex(o),'kind':'tail_jump','target_va':hex(pe.f2va(t))})
                else:
                    nxt.append(t)
            if i.mnemonic not in ('jmp','ret'):
                req(o+i.size<end,'fallthrough past extent')
                nxt.append(o+i.size)
            graph[o]=nxt;todo.extend(nxt)
        req(len(graph)==d['instruction_count']==ic and len(d['blocks'])==bc and external==d['external_edges'],'reachable extent graph')
        covered=[]
        for b in d['blocks']:
            sites=b['sites']; covered+=sites
            req(sites and all(graph[a]==[z] and not ins[a].mnemonic.startswith('j') for a,z in zip(sites,sites[1:])) and
                sorted(graph[sites[-1]])==b['successors'],'block path/exits')
        req(sorted(covered)==sorted(graph),'disjoint complete blocks')
        internal.update(graph)
    req({o for o in internal if ins[o].mnemonic=='call'}=={t[3] for t in LAYOUT}|{0x43708b2,0x43708fb,0x4370944,0x3c60149,0x3c60162},'reader call census')
    text(0xf2ba38,'byte ptr [rsp + 0x30], r12b');text(0xf2ba33,'qword ptr [rsp + 0x38], rsi');text(0xf2ba3d,'dword ptr [rsp + 0x28], ebp')
    text(0x437086a,'r14, r9');text(0x43709b4,'r9, r14');text(0x43709b1,'r8d, r8d');text(0x3c60146,'r9b, 1')
    text(0x3c60122,'rcx, qword ptr [rsp + 0x78]');text(0x3c60133,'r8d, dword ptr [rsp + 0x68]');text(0x3c6012a,'r8d, 0x989681')
    text(0x3c60138,'dword ptr [rbx], r8d');text(0xf2ba51,'qword ptr [rbx + 0x98]');text(0x3c60164,'al, 1');text(0x437099e,'eax, eax')
    req(dest(0xf2ba23)==0xf48b30 and dest(0xf2ba7f)==0xffa5d0,'outer calls')
    bs=[b for p in c['branch_shards'] for b in read(OUT/p)['branches']]
    by={b['site']:b for b in bs};cond={o for o,t in internal.items() if len(t)==2}
    outer={0xf2b698,0xf2b6b8,0xf2ba15,0xf2baa9,0xf2bac9,0xffa7af,0xffa7ce,0xffa7ed,0xffa7fa,
           0xf2ba89,0xf2ba59,0xf2ba2b,0xf2b9db,0xf2b9fa,0xf2ba6c,0xffa610,0xffa640,0xffa733,0xffa77f,0xf48b3b}
    req(len(bs)==len(by)==40 and set(by)==outer|cond and len(cond)==r['condition_count']==20,'branch inventory')
    req(c['branch_taxonomy']==list(CLASSES) and {k:sum(b['class']==k for b in bs) for k in CLASSES}==c['branch_census']==CLASSES,'branch sources')
    for b in bs:
        o,p=b['site'],b['predicate']; after=p+ins[p].size
        req(ins[o].mnemonic.startswith('j') and ins[o].mnemonic!='jmp' and b['taken_to']==dest(o) and b['fallthrough_to']==o+ins[o].size
            and all(x in ins for x in b['evidence']) and b['alternative_or_first_counterexample'],f'branch evidence {o:#x}')
        req(after==o or (o==0xffa640 and ins[after].mnemonic=='mov' and after+ins[after].size==o),'predicate flags stay live')
        if o in cond:
            label='wire_data' if o in (0x3c60131,*NORMS) else 'IO-result' if o in STATUS else 'context-lifecycle'
            req(b['scope']==('reader' if o>=chain[1] else 'identity_tail') and b['class']==label,'reader branch source')
            if o in STATUS:
                text(p,'ebp, ebp' if o<=0x4370948 else 'dword ptr [rsi + 0x10], 0')
                if o<=0x4370948:
                    text(b['evidence'][1],'ebp, dword ptr [rsi + 0x10]')
                req(b['evidence'][0]==STATUS[o] and (b['fallthrough_to'] if o==0x437099c else b['taken_to'])==0x437099e,'IO failure edge')
            elif o in NORMS:
                off=0x18+NORMS[o]; z=o+ins[o].size
                text(p,f'dword ptr [rbx + {off+4:#x}], 0');text(z,f'eax, dword ptr [rbx + {off:#x}]')
                zz=z+ins[z].size;text(zz,f'dword ptr [rbx + {off+4:#x}], eax')
                req(b['taken_to']==zz+ins[zz].size,'zero lane edge rejoins without new transfer')
        else:
            req(b['scope']=='loader_footer_factory_slice','outer branch scope')
    for o,d in ((0x4370879,0x437089e),(0x43708c2,0x43708e7),(0x437090b,0x4370930)):
        text(d,'ebp, dword ptr [rsi + 0x10]');req(dest(o)<d and ins[dest(o)].mnemonic=='cmp','null skips to object cmp then unsafe status read')
    req(c['transfers'][0]=={'site':0xf2ba0e,'legacy_offset':-1,'wire_offset':0,'width':1,'sink':'loader stack+0x43'},'selector')
    for t,(legacy,w,obj,o,l,wp,_) in zip(c['transfers'][1:],LAYOUT,strict=True):
        m=ins[l].operands[1]; base='rdi' if w==12 else 'rbx'
        req((t['legacy_offset'],t['wire_offset'],t['width'],t['object_offset'],t['site'],t['consumer'],t['setup'])==
            (legacy,legacy+1,w,obj,o,o,[l,wp]) and ins[l].mnemonic=='lea' and ins[l].reg_name(m.mem.base)==base and m.mem.disp==obj and
            ins[wp].operands[1].imm==w and ins[o].mnemonic=='call' and ins[o].op_str=='qword ptr [rax + 0x28]','transfer instruction geometry')
    req([(t['site'],t['width']) for t in c['loader_transfers']]==[(0xf2b691,4),(0xf2b6b1,1),(0xf2ba0e,1),(0xffa602,4),
         (0xffa7a8,4),(0xffa7c7,4),(0xffa7e6,4),(0xf2baa2,1),(0xf2bac2,4)],'outer transfer summary')
    for t in c['loader_transfers']:
        req(t['consumer']==t['site'] and ins[t['site']].op_str=='qword ptr [rax + 0x28]' and ins[t['setup'][0]].operands[1].imm==t['width'],'outer native setup')

    req(all(o in ins for part in c['scope_evidence'].values() for o in part),'scope evidence references')
    for o in (0xe842b3,0xe5831c):
        req(ins[o].operands[1].imm==int.from_bytes(b'Cmti','big'),'club list 4CC')
    req([dest(o) for o in (0xe842b9,0xe831e4,0xe58339,0xe58355,0xea14d6,0x153ce50)]==
        [0xe831c5,0xe57de0,0x1523b10,0xea12d0,0x153ce50,0x4371980],'Cmti collection -> same class slot3')
    for o,s in {0x1523bdf:'ecx, dword ptr [rdi + 0xc]',0x1523be5:'edx, dword ptr [rdi + 0x10]',
        0x1523c52:'eax, dword ptr [r13 + 0x20]',0x1523c5b:'eax, dword ptr [r13 + 0x24]',
        0x1523c8c:'eax, dword ptr [r13 + 0x28]',0x1523c95:'eax, dword ptr [r13 + 0x2c]',
        0x153c99c:'esi, edx',0x153c99e:'rdi, rcx',0x153ca10:'rdi, 0x18',0x153ca17:'edx, 0x50657273',
        0x153ccec:'edx, 0x43636c75',0xfe68e4:'eax, dword ptr [rbx + 4]',0xfe68eb:'rbx, dword ptr [rbx]',
        0x153cc7e:'ecx, dword ptr [rdi + 0x20]',0x153cc83:'eax, dword ptr [rdi + 0x24]',0x153cc88:'rsi, [rdi + 0x20]',0x153ccb4:'rdi, 0x28',
        0x153cb73:'ecx, dword ptr [rdi + 0x28]',0x153cb78:'eax, dword ptr [rdi + 0x2c]',
        0x153cbb2:'dword ptr [rbp - 8], 0',0x153cc0d:'dword ptr [rbp - 8], 1',
        0x3bf0c25:'ebx, dword ptr [rax + 0xc]',0x3bf0cf0:'ecx, dword ptr [rax + 0x10]',
        0x4371b20:'qword ptr [r14 + 0x28], rax',0x4371b24:'qword ptr [r14 + 0x20], rcx',0xbe0:'al, 1',
        0x4371aa4:'byte ptr [r14 + 0x38], al',0x4371a8f:'dword ptr [r14 + 0x30], eax',0x4371a32:'dword ptr [r14 + 0x34], eax',
        0x4371a1d:'qword ptr [r14 + 0x18], rax'}.items():
        text(o,s)
    req([dest(o) for o in (0x153c9a3,0xfe7ad0,0x153ccf4,0x153ccc1,0xf79f40,0x153c810,0x153cc86,0x153ccb2,0x153cb7b,0x153cba7)]==
        [0xfe7ad0,0x3ccca60,0xfe68b0,0xf79f40,0x3bf0bc0,0x4370ce0,0x153ccb4,0x153ccbb,0x153cc04,0x153cc04],'context predicate, resolver and key/writer chain')
    req(ins[0xbe2].mnemonic=='ret','no ordinal fixup')
    for o,off in zip((0x4370d17,0x4370d3a,0x4370d57,0x4370d7a,0x4370d97,0x4370db6),range(0x18,0x30,4),strict=True):
        text(o,f'rdx, [rdi + {off:#x}]');req(ins[o].mnemonic=='lea','writer emits object keys, not target ordinals')
    for record in f['fields']:
        code=record['code']; g=record['getter']; route=g['route']; x=int.from_bytes(code.encode(),'big'); cmp=None
        req(route[0]==0x153c980 and route[-1]==g['arm']==ARM[code] and g['compare'] in route and
            ins[g['compare']].operands[1].imm==x,'unique code route')
        for a,b in zip(route,route[1:]):
            i=ins[a]
            if i.mnemonic=='cmp':
                req(i.op_str.startswith('esi, '),'getter compare origin')
                cmp=i.operands[1].imm
            z=a+i.size
            if i.mnemonic.startswith('j') and {'jg':x>cmp,'je':x==cmp,'jne':x!=cmp}[i.mnemonic]:
                z=dest(a)
            req(z==b,'getter edge')
        relevant=[t for t in LAYOUT if t[-1]==code]
        req(g['object_offsets']==[t[2] for t in relevant] and record['sinks']==[
            dict(legacy_offset=o,wire_offset=o+1,width=w,object_offset=obj,site=site) for o,w,obj,site,_,_,_ in relevant],'getter-to-reader sinks')
        if code in ('cash','mths','pyiv'):
            _,w,obj,*_=relevant[0]; i=ins[g['arm']]; m=i.operands[1]
            req(i.mnemonic==('movsx' if w==1 else 'mov') and i.reg_name(m.mem.base)=='rdi' and m.mem.disp==obj and m.size==w,'scalar native getter')
    return ins,by,cond,internal


def verify_paths(raw,rows,s,pe):
    ins,by,cond,graph=pe; visits=Counter(); trace=sha256(); samples=[]; uids=set()
    for i,row in enumerate(rows):
        k=13+i*W; req(row[0]==0,f'row {i} selector')
        identity=S.unpack_from('<III',row,34); rid,a,b=identity
        req(rid==i and a==b and a and a not in uids,'raw identity');uids.add(a)
        site=0x4370860; cursor=1; seq=[]
        consumes={t[3]:t for t in LAYOUT}
        for _ in range(165):
            if site in consumes:
                o,w,*_=consumes[site];req(o+1==cursor,'row transfer order');cursor+=w
            if site in cond:
                j=by[site]
                if site in NORMS:
                    take=S.unpack_from('<i',row,NORMS[site]+5)[0]!=0
                elif site==0x3c60131:
                    take=rid<10000001
                else:
                    take=site in (0x43708a5,0x43708ee,0x4370937,0x437099c,0x3c60155)
                visits[site,take]+=1;seq.append([site,take]);site=j['taken_to' if take else 'fallthrough_to']
            elif site in (0x43709c1,0xfae340):
                site=0xfae340 if site==0x43709c1 else 0x3c600f0
            elif ins[site].mnemonic=='ret':
                break
            else:
                site,=graph[site]
        req(site==0x3c6016d and cursor==W and seq==s['row_template']['condition_edges'],f'row {i} CFG replay')
        bh=sha256(row[1:]).digest()
        trace.update(S.pack('<7I',i,k,k+1,k+W,*identity)+bh)
        if i in (0,1,2,N//2,N-1):
            samples.append(dict(ordinal=i,selector_start=k,body_start=k+1,body_end=k+W,identity=list(identity),body_sha256=bh.hex(),wire_hex=row.hex()))
    req((min(uids),max(uids))==(s['uid_min'],s['uid_max'])==(1,535) and trace.hexdigest()==s['row_trace_sha256'] and
        samples==s['samples'] and s['selector_histogram']=={'0':N},'full row trace and selector')
    neg=s['negative_replays']; short={}
    for o,w,_,site,*_ in LAYOUT:
        effect='no immediate native bulk status test' if site==0x3c60119 else 'IO-result -> 0x437099e (AL=false)'
        short[site]=f'row 0: short transfer @{14+o} width {w} site {site:#x}; {effect}'
    req(neg['short_transfers']==[{'site':k,'first_counterexample':e} for k,e in short.items()],'all first short-transfer counterexamples')
    r,a,b=S.unpack_from('<III',raw,47)
    req(neg['overwrite_does_not_mask_raw_error']==f'row 0: identity @47 raw={(10000001,a,b)}, stored ordinal=0' and
        neg['duplicate_lane_mismatch']==f'row 0: identity @47 raw={(r,a,0)}, stored ordinal=0' and
        neg['selector_out_of_observed_domain']=='row 0: selector 1 @13 outside observed domain (not factory rejection)','raw rejections')
    for o in cond:
        rec=by[o];t,z=visits[o,True],visits[o,False]
        req((t,z)==(rec['taken_count'],rec['fallthrough_count']) and t+z==N and rec['observed_edge']==('taken' if t else 'fallthrough'),'observed branch counts')
        alt=rec['alternative_or_first_counterexample']
        if o in STATUS:
            req(alt==short[STATUS[o]],'IO negative per branch')
        elif o in NORMS:
            p=14+NORMS[o];a,b=S.unpack_from('<ii',raw,p)
            req(alt==neg['zero_key_lane_alternates'][str(o)]==dict(row=0,offset=p+4,observed_lane1=b,injected_lane1=0,
                stored_pair=[a,a],body_end=59,branch='fallthrough') and b!=0,'zero lane first alternate, unchanged cursor')
        elif o==0x3c60131:
            req(alt==neg['overwrite_does_not_mask_raw_error'],'identity overwrite negative per branch')


def archive_check(c):
    os.environ['FM24_DB_DIR']=str(ROOT/'scratch/data')
    import fm24_dump as db
    codec=db._reader(); ar=c['archives']
    for a,entries in [('client',31),('server',77)]:
        fn=a+'_db.dat'; disk=db.DB_DIR/fn; report=ar[a]; blob=disk.read_bytes()
        entries_now=codec['list_tables'](disk,fn)
        hit=[r for r in entries_now if r['table_id']==43]
        req(len(entries_now)==report['directory_entry_count']==entries and report['table43_entries']==hit and report['present']==bool(hit) and
            sha(blob)==report['archive_sha256'],f'{a} directory and file SHA')
        if a=='client':
            req(not hit and all(report[k] is None for k in ('row_count','stride','payload_sha256')),'absent is not empty')
        else:
            e,=hit; start=e['offset']; frame=blob.index(db.MAGIC,start,start+64)
            req((start,frame,e['packed_size'])==(24766564,24766598,8796) and frame==report['zstd_frame_offset']==report['first_frame_offset'] and
                not report['used_profile_frame'] and report['default_load_payload_len']==24632,'first frame is the complete table43 member')
            raw=codec['_stream_decompress'](blob[frame:frame+e['packed_size']],256*1024*1024)
    s=ar['server']; rows,hi=wire(raw,N);end=13+W*N
    req(sha(raw)==s['payload_sha256']==PAYLOAD_SHA and len(raw)==e['size']==s['payload_len']==24632 and
        (e['record_count_header'],e['payload_version'])==(N,3569),'server payload SHA/header')
    req((s['row_count'],s['stride'],s['row_bytes'],s['wire_origin'],s['legacy_origin'],s['wire_footer_start'],s['legacy_footer_start'])==
        (N,W,N*W,13,14,end,end+1) and s['header_hex']==raw[:13].hex() and s['wire_footer_hex']==raw[end:].hex() and
        s['legacy_footer_hex']==raw[end+1:].hex() and s['footer_values']==[0,1,hi]==[0,1,535],'dual closure/footer')
    req(s['footer_transfers']==[dict(site=o,offset=k,width=w,value=int.from_bytes(raw[k:k+w],'little')) for o,k,w in
        ((0xffa602,end,4),(0xf2baa2,end+4,1),(0xf2bac2,end+5,4))],'footer transfer geometry')
    pp=(ROOT/T29).read_bytes(); p=json.loads(pp); t=c['t29']; rc=p['row_closure']; rr=(ROOT/ROWS).read_bytes()
    req(t['profile']==T29 and t['rows']==ROWS and t['matched_full_rows']==N and t['profile_sha256']==sha(pp) and
        p['payload']['payload_sha256']==PAYLOAD_SHA and p['payload']['packed_offset']==24766598 and
        sha(rr)==p['full_rows_sha256']==t['rows_sha256'] and sha(raw[14:end+1])==rc['rows_sha256']==t['legacy_block_sha256'] and
        (rc['row_start'],rc['row_end_exclusive'],rc['count'],rc['stride'])==(14,end+1,N,W),'t29 snapshot')
    for i,(k,line) in enumerate(zip(range(14,end+1,W),rr.splitlines(),strict=True)):
        rec=json.loads(line)
        req((rec['offset'],rec['row'],rec['len'])==(k,i,W) and bytes.fromhex(rec['raw_hex'])==raw[k:k+W],f't29 legacy row {i}')
    if t['inventory'] is not None:
        b=(ROOT/INV).read_bytes(); q,=[r for r in json.loads(b)['parents'] if r['parent_4cc']=='Cmti']
        req(t['inventory']['path']==INV and t['inventory']['sha256']==sha(b) and
            (q['table_type'],q['count'],q['stride'],q['link_status'])==(43,N,W,t['inventory']['link_status']) and
            q['profile']['profile_sha256']==sha(pp) and q['profile']['rows_jsonl_sha256']==sha(rr),'inventory scope and hashes')
    return codec,db,raw,rows,{(r['offset'],r['width']):r for r in p['columns']}


def target_keys(codec,db,meta):
    pf=(db.DB_DIR/'basic_people_db.dat').read_bytes()
    req(pf[:12].hex()=='03017461642ef10d28b52ffd','target person direct frame')
    people=codec['_stream_decompress'](pf[8:],128*1024*1024); n=S.unpack_from('<I',people)[0]
    req(n==658011 and people[4]==0,'person target count and flag')
    widths=(0,83,83,83,34,22); person={}; p=5; ordinals=set()
    while p<len(people)-9:
        tag,c=people[p:p+2];req(tag==17 and 1<=c<=5,'person tag/class');p+=widths[c]
        ordinal,u,v=S.unpack_from('<Iii',people,p-12)
        req(ordinal not in ordinals and u==v,'person identity in target')
        ordinals.add(ordinal)
        if c==2:
            person[u,v]=ordinal
    q=meta['person'];req(ordinals==set(range(n)) and people[p:].hex()=='00000000014cbd5477','person identity-domain closure')
    req((q['archive_sha256'],q['payload_sha256'],q['row_count'],q['ordinal_count'],q['ordinal_bounds'],q['key_count'],q['target_class'])==
        (sha(pf),sha(people),n,len(ordinals),[0,n-1],len(person),2) and len(person)==476158,'person target fingerprints')
    t24=ROOT/'scratch/t24/out'; tr=read(t24/'cursor.json');buf=db.load_payload(codec,'client',3);d=sha256()
    req(sha(buf)==tr['provenance']['payload_sha256'] and S.unpack_from('<I',buf,8)[0]==tr['row_count']==84259,'club target header/SHA')
    club={}; co=set(); last=13
    for name in tr['rows']['shards']:
        b=(t24/name).read_bytes();d.update(b)
        for i,p,sel,end,_,_,uid in json.loads(b)['rows']:
            j,x,y=S.unpack_from('<Iii',buf,end-12)
            req(p==last+1 and buf[last]==sel and i==j and j not in co and x==y==uid,'t24 coordinates vs raw target identity')
            last=end;co.add(j);club[x,y]=j
    q=meta['club'];req(co==set(range(84259)) and last==len(buf)-9 and (q['archive'],q['table_type'])==('client',3),'club ordinal-domain closure')
    req((q['payload_sha256'],q['trace_sha256'],q['row_count'],q['ordinal_count'],q['ordinal_bounds'],q['key_count'])==
        (sha(buf),d.hexdigest(),84259,84259,[0,84258],len(club)) and len(club)==84259,'club target fingerprints')
    return {'person':(person,ordinals),'club':(club,co)}


def verify_fields(f,rows,columns,refs):
    m=read(ROOT/MASTER); parent,=[v for v in m['entities']['club.xml'][0]['fields'] if v['field']=='Cmti']; specs=parent['list_item_fields']
    occ=[x for p in sorted((ROOT/'scratch/t24/out').glob('subtables.part00*.json')) for x in read(p)['nested_fields'] if x['parent']=='Cmti']
    req(len(specs)==len({s['field'] for s in specs})==6 and [x['idx'] for x in occ]==list(range(213,219)),'scoped six occurrences')
    def stats(values,o,w):
        u=set(values)
        a=[N,len(u),min(u),max(u),values.count(0),values.count((1<<(8*w))-1)]
        req(a==[columns[o,w][k] for k in ('count','distinct','min_unsigned','max_unsigned','zero_count','sentinel_count')],'unsigned t29 profile')
        return a
    def examples(ix,raw,xs,o):
        return [dict(row=i,offset=14+W*i+o,value=list(xs[i]) if isinstance(xs[i],tuple) else xs[i],hex=raw[i].hex()) for i in ix[:5]]
    grades=Counter(); club_a=[S.unpack_from('<ii',r,9) for r in rows];club_b=[S.unpack_from('<ii',r,17) for r in rows]
    # Exercise both view choices for every row (not a reader mode fork).
    for a,b in zip(club_a,club_b,strict=True):
        req(a!=b and keys(a,b,a)==(0,(b,16)) and keys(a,b,b)==(1,(a,8)),'both club endpoint views')
    def example(a,b):
        views=[]
        for ctx in (a,b):
            v,(key,o)=keys(a,b,ctx)
            views.append(dict(context_key=list(ctx),icom=v,club_key=list(key),selected_legacy_offset=o))
        return dict(row=0,same_wire_hex=rows[0].hex(),different_endpoint_rows=N,views=views)
    for r,s,x in zip(f['fields'],specs,occ,strict=True):
        code=s['field']; typ=s['type']
        req((r['code'],r['name'],typ)==(x['code'],x['name'],x['type']) and r['schema']==s and
            r['schema_scope']==['club.xml','Cmti',x['idx']],'unique schema and field code')
        expected=[]; cast=None
        for tr in r['sinks']:
            o,w=tr['legacy_offset'],tr['width']; bs=[a[o+1:o+1+w] for a in rows]; u=stats([int.from_bytes(b,'little') for b in bs],o,w)
            if typ=='database_record_unique_id':
                cast='record_key_i32_pair'; target=s['database_table_type']; ids,ords=refs[target]
                req(r['domain']==dict(target=target,native_null=[-1,-1],zero_second_lane='copy lane 0 on reader; not null',
                    key_basis='target identity at record +0xc/+0x10, not ordinal +8'),'key domain and sentinel distinction')
                xs=[S.unpack('<ii',b) for b in bs];live=[i for i,v in enumerate(xs) if v!=(-1,-1)]
                bad=[i for i in live if xs[i] not in ids];no=[i for i in live if any(y not in ords for y in xs[i])]
                req(len(no)=={0:535,8:19,16:39}[o] and not bad,'actual keys vs rejected ordinal hypothesis')
                lane_stats=[stats([int.from_bytes(b[j:j+4],'little') for b in bs],o+j,4) for j in (0,4)]
                expected.append(dict(count=N,distinct=len(set(xs)),min=min(a for a,b in xs),max=max(a for a,b in xs),both_null_count=N-len(live),
                    second_zero_count=sum(b==0 for a,b in xs),any_minus_one_count=sum(-1 in v for v in xs),matching_lanes_count=sum(a==b for a,b in xs),
                    live_count=len(live),matches=N-len(bad),violations=len(bad),first_violations=examples(bad,bs,xs,o),
                    ordinal_hypothesis=dict(matches=len(live)-len(no),violations=len(no),first_violations=examples(no,bs,xs,o)),
                    first_target_ordinals=[ids.get(v) for v in xs[:3]],t29_unsigned_stats=u,t29_lane_stats=lane_stats))
            else:
                cast='i8' if w==1 else 'i32'
                xs=[S.unpack('<b' if w==1 else '<i',b)[0] for b in bs];h=Counter(xs);bad=[]
                if w==1:
                    lo,hi=-128,127
                    req('enum_ref' not in s and h=={1:8,6:11,12:516} and r['domain']==
                        dict(native_signed_bounds=[lo,hi],frozen_enum=None,labels_or_exhaustive_domain=None),'interval byte, not exhaustive enum')
                else:
                    lo,hi=int(s['min_value']),int(s['max_value']);req(r['domain']==dict(xml_bounds=[lo,hi]),'frozen numeric bounds')
                bad=[i for i,v in enumerate(xs) if not lo<=v<=hi]
                expected.append(dict(count=N,distinct=len(h),min=min(h),max=max(h),zero_count=h[0],minus_one_count=h[-1],sentinel=None,
                                     matches=N-len(bad),violations=len(bad),first_violations=examples(bad,bs,xs,o),
                                     histogram={str(k):v for k,v in h.items()} if len(h)<=100 else None,t29_unsigned_stats=u))
        if code in ('icom','club'):
            req(r['context_counterexample']==example(club_a[0],club_b[0]),'same-row context negative')
        if code=='icom':
            cast='contextual_enum';grade='held_derived_no_independent_wire_sink';coord=(None,None)
            req(not r['sinks'] and r['domain']==dict(getter_outputs=[0,1],independent_wire_sink=False),'derived enum no sink')
        elif any(z['violations'] for z in expected):
            grade='held_static_sink_profile_conflict';coord=(None,None)
        elif code=='club':
            grade='L3_contextual_row_coordinates';coord=(None,None)
        else:
            grade='L3_named_row_coordinate';coord=(o,o+1)
        req(r['interpretation']==cast and r['profiles']==expected and r['grade']==grade and (r['row_offset'],r['wire_offset'])==coord,'field grade/profile '+code)
        grades[grade]+=1
    req(grades=={'L3_named_row_coordinate':4,'L3_contextual_row_coordinates':1,'held_derived_no_independent_wire_sink':1} and
        f['occurrences']==6 and f['L3']==5 and f['date_fields']==f['baseline_L3']==f['L4']==0,'final grades')


def verify():
    c=read(OUT/'cursor_cmti.json');f=read(OUT/'fields_cmti.json')
    req(c['scope']==f['scope']==['club.xml','Cmti'] and c['table_type']==f['table_type']==43,'scope')
    pe=pe_check(c,f);codec,db,raw,rows,cols=archive_check(c)
    verify_paths(raw,rows,c['archives']['server'],pe)
    verify_fields(f,rows,cols,target_keys(codec,db,f['reference_domains']))
    print('t32 verify PASS: 535 rows / 46 B; 37 reader/tail blocks / 20 conditions; 4 fixed L3 + 1 contextual L3, 1 held, L4=0')


def selftest():
    h=bytes.fromhex('03017461642ef10d0100000000');r=bytes(W);f=S.pack('<IBI',0,1,7)
    rows,hi=wire(h+r+f,1);req(rows==[r] and hi==7,'synthetic envelope')
    for bad in (h+r+f[:-1],h+r+b'\x01'+f[1:],h[:12]+b'\x01'+r+f):
        try:
            wire(bad,1)
        except Reject:
            continue
        raise Reject('invalid envelope accepted')
    a,b=(2,2),(4,4);req(keys(a,b,a)==(0,(b,16)) and keys(a,b,b)==(1,(a,8)),'same bytes, distinct context')
    print('t32 verify selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',help='test the physical envelope and same-row context counterexample')
    try:
        selftest() if p.parse_args().selftest else verify()
        return 0
    except Reject as e:
        print(f't32 verify FAIL: {e}',file=sys.stderr)
        return 1
    except (OSError,ValueError,TypeError,KeyError,IndexError,ImportError,RuntimeError,StopIteration,S.error) as e:
        print(f't32 verify fatal: {type(e).__name__}: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
