#!/usr/bin/env python3
"""Independently verify t63 Club R2 against editor PE, archives and frozen E97."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from hashlib import sha256
import json
import math
import os
from pathlib import Path, PurePosixPath
from struct import pack, unpack_from
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
R1=ROOT/'scratch/t57/out'
MASTER='evidence/fm24/reports/editor_schema/master.json'
BIG='evidence/fm24/reports/dbdat_decode/db_tables_big.json'
PROV='evidence/fm24/reports/qa/IDA_PROVENANCE.md'
SCHEMA='reports/club_nation_subtable_schema.json'
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTERH='7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
N=84259
SIDES=('client','server')
ORDER='selector derived_170 derived_178 ref_d8 ref_e0 ref_e8 ref_f0 ref_f8 flags160 name_len name_bytes short_len short_bytes raw16a raw166 person148 raw16c vec110 obj150_tag obj150 vec130 vec138 raw168 stad140 base_ba base_b8 base18 base30 base60 base78 base90 base48 basea8 identity'.split()
# Independent expected join tuples; never use emitted offsets to decide which bytes to decode.
FIN={
    'Ccba':(0,0x14,0x55fc0,0x423ff1d,'i32'),
    'Cadm':(7,0x3b,0x147a52c,0x423ff5a,'bit1'),
    'Chaf':(5,0x39,0x147a5fc,0x423ff5a,'gated_bool'),
    'Chsd':(4,0x3c,0x147a65b,0x423ff44,'enum_i8'),
    'Cpfa':(7,0x3b,0x147a7f0,0x423ff5a,'enum_i8'),
    'CteA':(20,0x38,0x147a4cd,0x423ff70,'i8'),
    'Cesd':(8,0x2c,0x147a433,0x423ff70,'date'),
    'Ceed':(12,0x30,0x147a77a,0x423ff70,'date'),
    'Cead':(16,0x34,0x147a6df,0x423ff70,'date'),
    'Cmtp':(25,0x18,0x147a388,0x423ff98,'f32'),
    'Casp':(29,0x1c,0x147a590,0x423ff98,'f32'),
}
STOP=dict(Clri=0xe8bb8f,Cldi=0xe8d152,Cndi=0xe8ab1e,Codi=0xe8e3fa,Csmn=0xe96aad,Csna=0xe96aad,Csjd=0xe96aad,Csld=0xe96aad,
          Cebd=0xe96f7c,Cmls=0x3ebf736,Chdb=0xe8e12f,CssS=0x3ebcd5c,CssE=0x3ebcd5c,CssP=0x3ebcd5c,CssT=0x3ebcd5c)

class Bad(Exception): pass

def check(condition, msg):
    if not condition: raise Bad(msg)

def js(path):return json.loads(path.read_bytes())
def digest(b):return sha256(b).hexdigest()
def u(b,a=0):return unpack_from('<I',b,a)[0]
def histogram(vals):return {str(k):v for k,v in Counter(vals).items()}
def canonical(x):return json.loads(json.dumps(x))


def read_payloads(r1):
    depot=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if depot.drive.upper()=='Z:' or depot.resolve().drive.upper()=='Z:':raise ValueError('Z: forbidden')
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard
    shell=bytes.fromhex('0201666d662e080000')
    def decode(b):
        check(b.startswith(bytes.fromhex('28b52ffd')),'Zstd framing')
        d=zstandard.ZstdDecompressor().decompressobj(); data=d.decompress(b); span=len(b)-len(d.unused_data)
        check(d.eof and span>0,'bounded Zstd frame');return data,span
    all_raw={}
    for side,want in [('client',(3,10,2,'extra_3')),('server',(3,10,21))]:
        blob=(depot/f'{side}_db.dat').read_bytes(); rel_toc,rel_base=unpack_from('<QQ',blob,17); toc=rel_toc+17;base=rel_base+17;meta=r1['archives'][side]
        check(digest(blob)==meta['archive_sha256'] and base==meta['data_base']==34 and blob[8:17]==blob[toc:toc+9]==shell,'archive provenance')
        table,n=decode(blob[toc+9:]);check(toc+9+n==len(blob),'TOC EOF');p=0; files={}
        def read(w):
            nonlocal p
            check(p+w<=len(table),'TOC overrun');p+=w;return table[p-w:p]
        def num():return u(read(4))
        def text():return read(num()).decode('utf-8')
        def folder(parent,depth=0):
            check(depth<32,'TOC depth');here=parent/text()
            for _ in range(num()):
                f=here/(text()+text());a,w,r,_,_=unpack_from('<5Q',read(40));check('..' not in f.parts and f not in files,'TOC key');files[f]=(base+a,w,r)
            for _ in range(num()):folder(here,depth+1)
        folder(PurePosixPath());check(p==len(table) and len(files)==meta['entries'],'TOC walk')
        for t in want:
            m=meta['members'][str(t)]; a,w,n=files[PurePosixPath(f'{side}_db/table_{t}.dat')]; z=a+w; bound=min((x for x,_,_ in files.values() if x>a),default=toc)
            check([a,z]==m['range'] and n==m['declared_size'] and z<=bound and bound==m['bound'] and digest(blob[a:z])==m['compressed_sha256'],'member range')
            frames=[]; match=[]
            while a<z:
                pay,width=decode(blob[a:z]);frames.append([a,a+width,len(pay)]);a+=width
                if len(pay)==n:match.append(pay)
            check(len(match)==1 and frames==m['frames'] and digest(match[0])==m['payload_sha256'],'raw payload provenance')
            all_raw[side,t]=match[0]
    return all_raw


def club(b,server):
    check(b[:8]==bytes.fromhex('03017461642ef10d') and u(b,8)==N,'table3 header')
    columns=defaultdict(list); end=len(b)-9; cur=13; trace=sha256(); uid=[]; sels=[]
    for i in range(N):
        beg=cur; sel=b[cur];check(sel in (0,12),('row selector',i))
        def take(key,n):
            nonlocal cur
            at=cur;cur+=n;check(0<n and cur<=end,('row cut',i,key,at,n));columns[key].append((i,at,n));return at
        def vec(k,w,stride,signed):
            count=int.from_bytes(b[cur:cur+w],'little',signed=signed);check(count>=0,('count',i,k));take(k,w+stride*count)
        take('selector',1)
        if sel==12:take('derived_170',4);take('derived_178',1)
        for k in ORDER[3:8]:take(k,4)
        take('flags160',6)
        for k in ('name','short'):
            n=u(b,take(k+'_len',4))
            if n:take(k+'_bytes',n)
        if server:
            take('raw16a',1);take('raw166',2);take('person148',4);take('raw16c',1)
            vec('vec110',1,4,True);tag=b[take('obj150_tag',1)]
            if tag==0:take('obj150',45)
            else:check(tag==2,('unsupported tag',i,tag))
            vec('vec130',1,24,True);vec('vec138',1,12,True);take('raw168',2);take('stad140',4)
        take('base_ba',1);take('base_b8',2)
        if server:
            for k,stride in zip(ORDER[26:32],(4,4,4,4,4,16),strict=True):vec(k,1,stride,k in ('base60','base78'))
            vec('basea8',2,28,True)
        at=take('identity',12); j,v,w=unpack_from('<III',b,at)
        check(j==i and v==w and v>(uid[-1] if uid else 0),('identity',i,at));uid.append(v);sels.append(sel);trace.update(pack('<IIIB',beg,cur,v,sel))
    check(cur==end and b[end:]==bytes.fromhex('0000000001e3c03a77'),'table3 footer')
    return columns,uid,sels,trace.hexdigest()


def check_static(p,s57,ledger):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64,CS_OP_IMM,CS_OP_REG,CS_OP_MEM
    raw=(ROOT.parent/'fm24/input/editor.exe').read_bytes()
    check(digest(raw)==p['static_source']['sha256']==EXEH,'editor.exe SHA')
    pe=pefile.PE(data=raw,fast_load=True);pe.parse_data_directories(directories=[3]);base=pe.OPTIONAL_HEADER.ImageBase
    va=lambda x:base+pe.get_rva_from_offset(x)
    off=lambda v:pe.get_offset_from_rva(v-base)
    extent={off(base+r.struct.BeginAddress):off(base+r.struct.EndAddress) for r in pe.DIRECTORY_ENTRY_EXCEPTION}
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True; cached={}
    def instr(a):
        if a not in cached:cached[a]=next(md.disasm(raw[a:a+15],va(a),1))
        return cached[a]
    def target(q):return off(q.operands[0].imm) if q.operands and q.operands[0].type==CS_OP_IMM else None
    def rip(q):return off(q.address+q.size+q.operands[1].mem.disp)
    def blob(rec,w):
        a=rec['offset'];check(rec['va']==va(a) and rec['bytes']==raw[a:a+w].hex(),'literal bytes');return raw[a:a+w]
    def memb(a,m,width,reg=None):
        q=instr(a);op=q.operands[1]
        check(op.type==CS_OP_MEM and op.mem.disp==m and op.size==width and (reg is None or q.reg_name(op.mem.base)==reg),('getter load',hex(a)))
    saved={}
    for rec in p['instructions']:
        a=rec['offset'];q=instr(a);blob(rec,q.size);check(a not in saved and rec['insn']==f'{q.mnemonic} {q.op_str}'.strip(),('instruction record',hex(a)));saved[a]=q
    for rec,func in [('club_vtable_slots',{2:0xe89a00,19:0xe5a7a0,56:0x11f4550}),('tag0_vtable_slots',{2:0x147a290,4:0x1476470})]:
        vt=off(s57['source']['CLUB']['vtable']) if rec=='club_vtable_slots' else rip(instr(0xe5ae12))
        for k,t in func.items():
            d=p['static_source'][rec][str(k)];check(d['offset']==vt+8*k and off(int.from_bytes(blob(d,8),'little'))==t,('vtable',rec,k))
    gm={}; scans={}; total_read_branches=set(); seen_switches=set()
    old=s57['source']['runtime_function_extents']; readers=p['reader_extents']; getters=p['getter_extents']
    for s in readers+getters:
        a,z=s['root'],s['end'];check(extent[a]==z,'PE exception bound'); tabs={t['jump']:t for t in s['rel32_tables']}; reached={}; stack=[a];unresolved=[]
        while stack:
            x=stack.pop()
            if x in reached or not a<=x<z:continue
            q=instr(x);reached[x]=q;m=q.mnemonic
            if not m.startswith('j'):
                if m not in ('ret','retf','ud2','int3'):stack.append(x+q.size)
                continue
            dst=target(q)
            if dst is not None:stack.append(dst)
            if m!='jmp':stack.append(x+q.size)
            if m=='jmp' and dst is None:
                if x not in tabs:unresolved.append(x);continue
                t=tabs[x];seen_switches.add((a,x));low=t['base'];check(0<t['count']<=128,'table bounds')
                targets=[off(va(low)+unpack_from('<i',raw,low+4*i)[0]) for i in range(t['count'])]
                check(all(a<=y<z for y in targets),'local rel32 table');stack.extend(targets)
        branches={x for x,q in reached.items() if q.mnemonic.startswith('j') and q.mnemonic!='jmp'}
        check(len(reached)==s['reachable'] and len(branches)==s['conditionals'] and sorted(unresolved)==s['register_jumps_not_followed'],(hex(a),'reachable census'))
        if str(a) in old:
            check((z,len(reached),len(branches))==(old[str(a)]['end_exclusive'],old[str(a)]['reachable'],old[str(a)]['conditional']),'E97 CFG')
            calls={x for x,q in reached.items() if q.mnemonic=='call' and q.operands[0].type==CS_OP_MEM and q.operands[0].mem.disp==0x28}
            check(calls==set(s['transfers'])==set(old[str(a)]['direct_stream_reads']),'reader transfers');total_read_branches|=branches
        else:gm[a]=tabs;scans[a]=reached
    check(seen_switches=={(s['root'],t['jump']) for s in getters for t in s['rel32_tables']},'all bounded table descriptors reached')
    check(total_read_branches=={r['branch'] for r in p['reader_branches']} and len(total_read_branches)==len(p['reader_branches']),'reader branch closure')
    for b in p['reader_branches']:
        q=saved[b['branch']];check(b['fallthrough']==b['branch']+q.size and b['taken']==target(q),'reader successors')
        if b['gate'] is not None:check(saved[b['gate']].eflags,'reader predicate flags')
    # Compare the emitted occurrence census against raw bounded comparisons, bit gates,
    # and rel32 cells. Scope stops at the explicitly recorded register tail calls.
    ks={int.from_bytes(f['code'].encode('ascii'),'big'):f['code'] for f in ledger if len(f['code'])==4 and f['code'].isascii()}
    proven=defaultdict(set)
    for root,found in scans.items():
        for a,q in found.items():
            if q.mnemonic=='cmp' and q.operands[0].type==CS_OP_REG and q.operands[1].type==CS_OP_IMM and q.operands[1].imm in ks:
                nxt=instr(a+q.size)
                if nxt.mnemonic in ('je','jne'):proven[ks[q.operands[1].imm]].add((root,'compare',a,None))
            if q.mnemonic=='bt':
                # Only immediate-mask 4CC selectors, never dynamic object flag tests.
                loc=sorted(x for x in found if a-35<=x<a)[-4:]
                if len(loc)==4:
                    sub,bound,skip,mask=map(instr,loc)
                    if (sub.mnemonic,bound.mnemonic,skip.mnemonic) != ('lea','cmp','ja') or mask.mnemonic not in ('mov','movabs'):continue
                    low=-sub.operands[1].mem.disp
                    for i in range(bound.operands[1].imm+1):
                        if (mask.operands[1].imm>>i)&1 and i+low in ks:proven[ks[i+low]].add((root,'bt',loc[0],i))
        for jump,d in gm[root].items():
            for i in range(d['count']):
                cc=d['first_code']+i
                if cc in ks and off(va(d['base'])+unpack_from('<i',raw,d['base']+4*i)[0])!=d['default']:
                    proven[ks[cc]].add((root,'rel32_table',jump,i))
    fin=p['finance']; r=fin['reader_rel32'];check(r['offset']==0x1476470 and target(instr(0x1476470))==r['target']==0x423fef0,'finance reader thunk')
    r=fin['balance_vtable_cell'];check(r['offset']==rip(instr(0xe5ae12))+0x190 and off(int.from_bytes(blob(r,8),'little'))==0x55fc0 and instr(0x55fc3).mnemonic=='ret' and instr(0x147a2f5).op_str=='qword ptr [rax + 0x190]','finance balance virtual selector')
    r=fin['ticket_clamp_f32'];check(r['offset']==rip(instr(0x423ffa0)) and unpack_from('<f',blob(r,4))[0]==150 and target(instr(0x423ffa7))==0x423ffaf,'Cmtp clamp threshold')
    check(instr(0xe5aea6).op_str=='qword ptr [r14 + 0x150], rsi' and instr(0xe5aef1).op_str=='qword ptr [rax + 0x20]' and instr(0xe8c615).op_str=='rax, qword ptr [rax + 0x10]' and instr(0xe8eb9f).op_str=='rax' and instr(0x423fefe).op_str=='rdi, rcx' and instr(0x147a2ac).op_str=='rdi, rcx','same tag-0 subobject')
    win=((0x14,4),(0x3c,1),(0x39,3),(0x2c,13),(0x10,4),(0x18,20));cursor=0
    for t,(member,width) in zip(fin['transfer_spans'],win,strict=True):
        check(t['width']==width and t['relative_to_tag0_object']==member and t['wire_interval']==[cursor,cursor+width],'tag0 wire spans')
        dst=t['destination'];q=instr(dst);check(q.mnemonic=='lea' and q.operands[1].mem.disp==member and q.reg_name(q.operands[1].mem.base)=='rdi','tag0 reader destination')
        walk=[];a=dst
        while a<t['site']:
            q=instr(a);walk.append(f'{q.mnemonic} {q.op_str}');a+=q.size
        check(a==t['site'] and f'mov r8d, {width if width<10 else hex(width)}' in walk and instr(a).op_str=='qword ptr [rax + 0x28]','tag0 width/stream');cursor+=width
    check(cursor==45,'finance packet size')
    check(instr(0x147a539).op_str=='bl, 1' and instr(0x147a539).mnemonic=='shr' and instr(0x147a53b).op_str=='bl, 1' and instr(0x147a53b).mnemonic=='and','Cadm bit 1')
    check(instr(0x147a5f2).op_str=='byte ptr [rdi + 0x3c], 0' and target(instr(0x147a5f6))==0x147a8b7,'Chaf presence gate')
    for f,o in zip(ledger,p['occurrences'],strict=True):
        code=f['code'];check(o['id']==f['id'] and code==o['code'],'projection index');got=set()
        for t in o['dispatch']:
            root=t['root']; kind=t['kind']; seq=t['sites'];arm=t['arm']; ix=t['index'];cc=int.from_bytes(code.encode('ascii'),'big')
            check(all(a in scans[root] for a in seq) and arm in scans[root],('bounded arm',code,root))
            h=instr(seq[-1]); q=instr(seq[0]);q2=instr(seq[1]);n=seq[-1]+h.size
            got.add((root,kind,seq[-1] if kind=='rel32_table' else seq[0],ix))
            if kind=='compare':
                check(q.operands[1].imm==cc and h.mnemonic in ('je','jne') and (target(h) if h.mnemonic=='je' else n)==arm,('exact 4CC',code))
            elif kind=='bt':
                check(t['low']==-q.operands[1].mem.disp and ix+t['low']==cc and 0<=ix<=q2.operands[1].imm and t['mask']==instr(seq[3]).operands[1].imm and (t['mask']>>ix)&1 and (target(h) if h.mnemonic=='jb' else n)==arm,('bit gate',code))
            else:
                v=t['cell']; d=gm[root][seq[-1]]; low=d['base']; ix=t['index']; sub=q.operands[1]; bias=(-(sub.mem.disp if q.mnemonic=='lea' else sub.imm))&0xffffffff
                rel=unpack_from('<i',blob(v,4))[0]
                check(low==rip(instr(seq[3]))==v['table'] and d['first_code']==bias and ix+bias==cc and d['count']==q2.operands[1].imm+1 and v['offset']==low+4*ix and v['rel32']==rel and off(va(low)+rel)==v['target']==arm,('indexed rel32 cell',code))
            local=t['local_path'];check(local and local[0]==arm,'arm trace starts at target')
            for a,b in zip(local,local[1:]):
                z=instr(a);check(b==(target(z) if z.mnemonic=='jmp' else a+z.size),'equal arm trace')
            for e in t['direct_rel32']:
                i=instr(e['offset']);check(e['offset'] in local and i.mnemonic in ('jmp','call') and target(i)==e['target'] and unpack_from('<i',blob(e,5),1)[0]==e['rel32'],'helper edge')
        check(got==proven[code] and len(got)==len(o['dispatch']),('exact gate census',code))
        x=o['projection'];kind=f['projection_family'];check(kind==(x['family'] if x else None),'projection family')
        if code in FIN:
            lane,member,use,tx,codec=FIN[code]; check(x['gate'] in o['dispatch'] and x['helper'] in o['dispatch'] and x['gate']['root']==0xe89a00 and x['helper']['root']==0x147a290,'finance gates')
            check(x['object_path']==[0x150,member] and x['member_use']==use and x['cursor']==dict(r1_slot='obj150',tag=0,member_transfer=tx,lane=lane,codec=codec),('finance lane',code))
            memb(use,member,2 if codec=='date' else 4 if codec in ('i32','f32') else 1,'rcx' if code=='Ccba' else 'rdi')
            if codec=='date':
                loads=[a for a in x['proof'] if instr(a).mnemonic=='movzx'];check(len(loads)==1,'second date word');memb(loads[0],member+2,2,'rdi');check(any(instr(a).op_str.endswith(', 0x1ff') for a in x['proof']),'day mask')
        elif f['xml_domain'].get('enum_ref')=='cnst':
            h=x['helper'];t=x['gate'];check(t in o['dispatch'] and h in o['dispatch'] and t['root']==0xe89a00 and any(e['target']==h['root'] for e in t['direct_rel32']),'cnst helper route')
            add,site={0x151d9b0:(0xe0,0xe89bef),0x151e500:(0xe7,0xe89fe1)}[h['root']]
            q=instr(h['arm']);check(q.mnemonic=='movsx' and q.operands[1].size==1 and q.reg_name(q.operands[1].mem.base)=='rcx' and x['object_path']==[0x100,add+q.operands[1].mem.disp] and instr(site).op_str=='rcx, qword ptr [r12 + 0x100]' and site in t['local_path'] and x['cursor'] is None and x['first_counterexample']['site']==site,'cnst separate object stop')
        elif code=='rdui':
            check(x['gate'] in o['dispatch'] and x['cursor']=={'r1_slot':'identity','lane':8,'codec':'suppressed_uid'} and instr(0xfe38a2).op_str=='dword ptr [r12 + 0xc], esi' and target(instr(0xfe38a7))==0xfe4565 and target(instr(0x11f4550))==0xfe3520,'identity suppression proof');memb(0xfe389d,0x10,4,'r12')
        elif code in STOP:
            check(x['first_counterexample']['site']==STOP[code] and STOP[code] in saved and x['cursor'] is None,('static stop',code))
        else:check(x is None,('speculative binding',code))
    check(target(instr(0xe5c5b9))==target(instr(0xe5c5d9))==0xf7e280 and instr(0xe5c5a5).op_str==instr(0xe5c5c5).op_str=='r8, qword ptr [rsi + 0x28]','Nation type/path ordinal control')
    return len(saved)


def sample(b,i,a,w,v):return dict(row=i,absolute=a,raw=b[a:a+w].hex(),value=v)


def valid_date(y,d,flags):
    return flags==0 and 1<=y<=9999 and 1<=d<=date(y,12,31).timetuple().tm_yday


def numbers(b,cells,k,spec,domain):
    lane,codec=(8,'suppressed_uid') if k=='rdui' else (spec[0],spec[-1]);w=4 if codec in ('date','f32','i32','suppressed_uid') else 1
    value_list=[];examples=[]; invalid=[]; suppressed=0;raw_counts=Counter()
    for i,a,width in cells:
        at=a+lane;check(at+w<=a+width,'bounded numeric lane');r=b[at:at+w];v=None;reason=None
        if codec=='bit1':v=int(bool(r[0]&2));raw_counts[r[0]]+=1
        elif codec=='gated_bool':
            raw_counts[r[0]]+=1
            if b[a+4]:v=r[0]
            else:suppressed+=1
            if r[0] not in (0,1):reason='raw byte not boolean'
        elif codec=='date':
            n=int.from_bytes(r,'little');v=(n>>16,n&511,(n>>9)&127)
            if not valid_date(*v):reason='not an unflagged Gregorian ordinal date'
        elif codec=='suppressed_uid':
            v=int.from_bytes(r,'little');
            if r==b[at-4:at]:suppressed+=1;reason='equal UID: getter suppresses saved rdui'
        elif codec=='f32':
            v=unpack_from('<f',r)[0]
            if not math.isfinite(v):reason='nonfinite';v=str(v)
        else:
            v=int.from_bytes(r,'little',signed=True)
            if codec=='enum_i8':
                if not domain['allowed_enum']:reason='no scoped enum_ref'
                elif v not in domain['allowed_enum']:reason='outside scoped enum'
        if isinstance(v,(float,int)) and not float(domain.get('min_value','-inf'))<=v<=float(domain.get('max_value','inf')):reason='outside frozen XML min/max in local getter units'
        record=sample(b,i,at,w,v)
        if not examples:examples.append(record)
        if v is not None:
            if not value_list:examples.append(record)
            value_list.append(v)
        if reason:invalid.append(dict(record,reason=reason))
    vc=Counter(value_list);ordered=sorted(vc) if all(not isinstance(v,str) for v in vc) else sorted(vc,key=str)
    return dict(events=len(cells),bypassed=N-len(cells),suppressed=suppressed,values=len(value_list),minimum=ordered[0] if ordered else None,
        maximum=ordered[-1] if ordered else None,distinct=len(vc),histogram=histogram(value_list) if len(vc)<=128 else None,raw_byte_histogram={str(k):v for k,v in raw_counts.items()} if raw_counts else None,
        first=examples[0] if examples else None,first_value=examples[1] if len(examples)>1 else None,violations=len(invalid),first_counterexample=invalid[0] if invalid else None)


def date_order(b,cells):
    start_end=reverse=with_appeal=late=0; first=None
    for i,a,_ in cells:
        vals=unpack_from('<3I',b,a+8)
        start,end,appeal=[(x>>16,x&511) for x in vals]
        default=(1900,1)
        if default not in (start,end):
            start_end+=1;reverse+=end<start
        if default not in (start,appeal):
            with_appeal+=1
            if appeal>=start:
                late+=1
                if first is None:first=dict(sample(b,i,a+8,12,[list(x) for x in (start,end,appeal)]),reason='XML title says before start; not a wire-validity constraint')
    return dict(events=len(cells),start_end_nondefault=start_end,end_before_start=reverse,appeal_and_start_nondefault=with_appeal,appeal_not_before_start=late,first_appeal_order_counterexample=first)


def ordinal_set(b,side,r1):
    t=js(ROOT/'scratch/t47/out/cursor_nation_tax.json')[side];h=sha256();key={}
    check(digest(b)==t['payload_sha256'],'key table payload')
    for row in t['rows']:
        a=row['identity_at'];i,v,w=unpack_from('<III',b,a);check(i==len(key) and v==w and v>0,('key triple',i));key[i]=v;h.update(b[a:a+12])
    m=r1['target_identity_domains'][side]['10'];check(len(set(key.values()))==len(key)==u(b,8)==251 and h.hexdigest()==m['identity_sha256'],'actual ordinal key domain')
    return key


def wrong_uid(b,col,target):
    idset=set(target.values());live=[(i,a,w,u(b,a)) for i,a,w in col if u(b,a)!=0xffffffff];hit=[v for v in live if v[-1] in target];miss=[v for v in live if v[-1] not in target];wrong=[v for v in live if v[-1] not in idset]
    return dict(events=len(col),considered_live=len(live),null=len(col)-len(live),ordinal_hits=len(hit),ordinal_misses=len(miss),first_ordinal_miss=sample(b,*miss[0]) if miss else None,wrong_uid_hits=len(live)-len(wrong),first_wrong_uid_miss=sample(b,*wrong[0]) if wrong else None,
                first_live=dict(sample(b,*hit[0]),target_uid=target[hit[0][-1]]) if hit else None)


def verify_fixtures(data,raw,runs,old):
    reg=old['regression']; snap=js(ROOT/BIG)['tables'];b=raw['client',2];stad=raw['server',21];ex=raw['client','extra_3']
    check(data['city']==reg['city'] and data['stadium']==reg['stadium'] and data['founded_year_fixture_only']==reg['founded_year_fixture_only'],'fixture input match')
    for x in snap['2']['named_anchor_checks']:
        i=x['row_index'];p=14+43*i;r=data['city'][x['city']]
        check(unpack_from('<III',b,p+30)==(i,r[1],r[1]) and list(unpack_from('<ff',b,p+1))==r[2] and b[p+10]==r[3],'frozen city bytes')
    for x in snap['21']['landmark_cross_checks']:
        i=x['row_index'];p=14+181*i;r=data['stadium'][str(i)]
        check(unpack_from('<III',stad,p+168)==(i,r['uid'],r['uid']) and list(unpack_from('<II',stad,p))==r['capacity_and_seats'] and list(unpack_from('<ff',stad,p+160))==r['coordinates'] and u(stad,p+146)==r['city_ordinal'],'frozen stadium bytes')
    check(data['stadium']['430']['capacity_and_seats']==[81044,81044],'Bernabeu')
    for side in SIDES:
        b=raw[side,3];cols,ids,*_=runs[side];s=cols['short_len'][460][1];v=[460,ids[460],u(b,cols['ref_f8'][460][1]),u(b,cols['ref_d8'][460][1]),b[s+4:s+4+u(b,s)].decode('utf-8')]
        check(v==data['liverpool'][side]==[460,676,1061,139,'Liverpool'],'Liverpool')
    years={x['candidate_order_index']:x for x in snap['3']['field_validation']['Cyfn_named_year_checks']}
    check(digest(ex)==snap['extra_3']['source_payload_sha256']['client'] and len(years)==len(data['founded_year_fixture_only'])==14,'frozen year fixture source')
    for x in data['founded_year_fixture_only']:
        i=x['row'];j,y=unpack_from('<IH',ex,x['absolute']-4);check(j==i and y==x['year']==years[i]['client_extra_3_u16_at_row_plus_4'] and x['note']==years[i]['note'],'year fixture value')
    check(any(x['row']==460 and x['year']==1892 for x in data['founded_year_fixture_only']),'Liverpool founded year')


def verify():
    p=js(HERE/'projections.json');m=js(HERE/'field_map_r2.json');r1=js(R1/'field_slots.json');old=js(R1/'field_map.json');rows=m['fields']; schema=js(ROOT/SCHEMA)
    need={MASTER,BIG,PROV,SCHEMA,'scratch/t59/out/REPORT.md','scratch/t59/out/field_map.json',*(f'scratch/t57/out/{x}' for x in ('field_map.json','field_slots.json','REPORT.md'))}
    check(m['input_sha256']==p['input_sha256'] and set(p['input_sha256'])==need,'input provenance inventory')
    man={x['path']:x['sha256'] for x in js(ROOT/'evidence/MANIFEST.json')['files']}
    for path,h in p['input_sha256'].items():check(digest((ROOT/path).read_bytes())==h and (not path.startswith('evidence/') or man[path]==h),('input SHA',path))
    check(p['input_sha256'][MASTER]==MASTERH and EXEH in (ROOT/PROV).read_text(encoding='utf-8'),'master/editor snapshot')
    check(m['L4']==0 and m['r1_reference']=='E97' and schema['club_main_row_fields']['acceptance_ledger_entry']=='E97' and m['schema_version']==schema['schema_version'],'scope E97')
    master=js(ROOT/MASTER);xml=master['entities']['club.xml'][0]['fields'];base=old['fields'];check(len(xml)==len(base)==433 and all(f['schema']==xml[i] and f['xml_index']==i for i,f in enumerate(base)),'433 frozen occurrences')
    unm=[f for f in base if f['grade']=='unmapped'];check(len(unm)==len(rows)==len(p['occurrences'])==m['reviewed']==399,'increment coverage')
    check(m['preserved_grades']=={'L3':13,'held':11,'skipped_separate_member':10} and m['r1_held_indices']==[r['xml_index'] for r in base if r['grade']=='held'] and not m['superseded_r1_negatives'],'r1 holds/negatives not reopened')
    check([r['key'] for r in r1['slots']]==ORDER,'34 t57 positions');pe_count=check_static(p,r1,rows)
    raw=read_payloads(r1);runs={};ctrl=p['reference_controls']['ref_e0'];check(ctrl['target']=='t10' and ctrl['getter_binding'] is None,'reference control is not a field')
    for side in SIDES:
        b=raw[side,3];run=club(b,side=='server');cols,ids,sel,trace=runs[side]=run;env=r1['envelopes'][side];report=p['r1_envelopes'][side]
        check(trace==env['row_trace_sha256'] and len(b)==env['payload']==report['payload_bytes'] and report['rows']==N and report['payload_sha256']==digest(b) and report['coordinates_revalidated']==34,'frozen row trace')
        check(report['tag150']==histogram(b[a] for i,a,w in cols['obj150_tag']) and histogram(sel)==env['selector_counts'],'selector modes/tag150')
        for s in r1['slots']:
            cs=cols[s['key']];q=s['profiles'][side];check(len(cs)==q['rows'] and (not cs or digest(b''.join(pack('<III',*c) for c in cs))==q['coordinate_sha256']),('coordinate trace',side,s['key']))
        ref=wrong_uid(b,cols['ref_e0'],ordinal_set(raw[side,10],side,r1));check(ref==ctrl['sides'][side] and ref['ordinal_misses']==0 and ref['ordinal_hits']>ref['wrong_uid_hits'],'ordinal/UID control')
        check(date_order(b,cols['obj150'])==p['date_relationship_control'][side],('date ordering negative',side))
    check(runs['client'][1:3]==runs['server'][1:3],'paired identities/selectors')
    for prev,f,o in zip(unm,rows,p['occurrences'],strict=True):
        k=prev['code'];idx=prev['xml_index'];s=xml[idx];d=f['xml_domain'];er=s.get('enum_ref')
        check(k==f['code']==s['field'] and f['id']==f'E97/club.xml#club/{idx:03d}' and f['xml_type']==s['type'] and f['r1_id']=={'ledger':'E97','path':'scratch/t57/out/field_map.json','xml_index':idx,'grade':'unmapped'},'exact XML occurrence key')
        want={a:s[a] for a in ('min_value','max_value','enum_ref','store_pence','dependencies') if a in s};want['allowed_enum']=sorted(int(v['enum']) for v in master['enums'][er]['values']) if er else None
        check(want==d,('XML domain',k));proj=o['projection'];profile=None;counter=None;grade='unmapped'
        if k in FIN or k=='rdui':
            profile={side:canonical(numbers(raw[side,3],runs[side][0]['identity' if k=='rdui' else 'obj150'],k,FIN.get(k),d)) for side in SIDES}
            counter=next((r['first_counterexample'] for r in profile.values() if r['violations']),None);grade='held' if counter else 'L3'
            if k=='Cmtp':check(profile['server']['maximum']<=150,'reader clamp is not entered')
        elif proj:counter=proj['first_counterexample'];grade='held'
        check(profile==f['domain_profiles'] and counter==f['first_counterexample'] and grade==f['grade'] and f['wire']==(proj['cursor'] if grade=='L3' else None),('grade / full replay',k))
    check(histogram(f['grade'] for f in rows)==m['grade_counts']=={'L3':8,'held':41,'unmapped':350} and [f['code'] for f in rows if f['grade']=='L3']==m['new_L3'],'R2 grade tally')
    verify_fixtures(m['fixture_regression'],raw,runs,old)
    print(f't63 independent verify PASS: {N}+{N} rows; {pe_count} recorded instructions; 399 occurrence grades; 8 L3; L4=0')


def selftest():
    check(valid_date(2024,366,0) and not valid_date(2023,366,0) and not valid_date(2024,1,1),'date boundary')
    x=wrong_uid(pack('<III',0,1,0xffffffff),[(0,0,4),(1,4,4),(2,8,4)],{0:1,1:99});check(x['ordinal_hits']==2 and x['wrong_uid_hits']==1 and x['null']==1,'nullable ordinal control')
    b=bytes(7)+bytes([2]);x=numbers(b,[(0,0,8)],'Cadm',FIN['Cadm'],{'allowed_enum':None});check(x['histogram']=={'1':1},'bit codec')
    print('t63 verifier selftest PASS')


def main():
    q=argparse.ArgumentParser(description=__doc__);q.add_argument('--selftest',action='store_true');a=q.parse_args()
    try:selftest() if a.selftest else verify()
    except Bad as e:print('check failed:',e,file=sys.stderr);return 1
    except Exception as e:print(f'fatal: {type(e).__name__}: {e}',file=sys.stderr);return 2
    return 0

if __name__=='__main__':raise SystemExit(main())
