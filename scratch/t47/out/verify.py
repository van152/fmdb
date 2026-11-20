#!/usr/bin/env python3
"""Independently verify t47 PE evidence, archive bounds, Ntxr cursor and domains."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import runpy
from struct import Struct, unpack_from, pack
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXE=ROOT.parent/'fm24/input/editor.exe'
HEAD=bytes.fromhex('03017461642ef10d')
TAIL=bytes.fromhex('0000000001ec7ae404')
EXPECTED={'Nntp':9,'Nctp':9,'Nrtp':9,'NTRv':9,'NWGv':9,'NSps':9,'Ntxr':10,'Nfmp':9,'NCro':9,
          'Nftb':None,'Nrvn':None,'Calt':None,'TCrs':None,'EDfx':None,'EDsc':None}
TAX=Struct('<BiiiHbbfbb')
CODES=('tag','lowa','uppa','capa','year','ppty','txty','perc','fram','leve')
FIELD_POS=dict(zip(CODES, (0,1,5,9,13,15,16,17,21,22)))
T37={'scratch/t37/out/REPORT.md':'5656568e8abb0c721498bc310db3ae8964a0eb2bc878828f422df87f482bcfde',
     'scratch/t37/out/nation_subtable_inventory.json':'8af89c72efc2a63fac562140a3faaec7d7f212b923421396a0acc5d627b57d50'}

class Failed(Exception):pass

def require(ok, why):
    if not ok:raise Failed(why)

def digest(b):return sha256(b).hexdigest()
def get(path):return json.loads(path.read_bytes())
def hist(x):return {str(k):v for k,v in Counter(x).items()}


def archives(discovery):
    # Use only the existing read-only directory decoder; independently select and hash frames.
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard as zstd
    directory=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    db=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if db.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    tables={}
    for arch, size in [('server',77),('client',31)]:
        _,data,index=directory(db/f'{arch}_db.dat')
        known=discovery['archives'][arch]
        entries={e['path']:e for e in index['entries']}
        require(size==len(entries)==known['directory_entries'] and index['data_base']==known['data_base']==34 and digest(data)==known['archive_sha256'],arch+' directory')
        for name in ('table_9.dat','table_10.dat','table_extra_9.dat','table_extra_10.dat'):
            rep=known['members'][name]; entry=entries.get(f'{arch}_db/{name}')
            require(rep['present']==(entry is not None),arch+' '+name+' presence')
            if entry is None: continue
            start=entry['offset']+34; stop=start+entry['packed_size']
            next_start=min((34+e['offset'] for e in entries.values() if e['offset']>entry['offset']), default=index['toc_offset'])
            require(start==rep['member_start'] and stop==rep['member_end'] and start<stop<=next_start==rep['next_member_start'],name+' bounds')
            whole=data[start:stop]; pos=start; frames=[]; choices=[]
            while pos<stop:
                require(data[pos:pos+4]==b'\x28\xb5\x2f\xfd',name+' magic')
                dec=zstd.ZstdDecompressor().decompressobj(); p=dec.decompress(data[pos:stop]); length=stop-pos-len(dec.unused_data)
                require(dec.eof and length>0,name+' frame boundary')
                frame=dict(offset=pos,compressed_bytes=length,payload_bytes=len(p)); frames.append(frame)
                if len(p)==entry['size']: choices.append((p,frame))
                pos+=length
            require(len(choices)==1 and frames==rep['frames'],name+' frame choice')
            payload,frame=choices[0]
            require(rep['entry']=={**entry,'sha256':digest(whole)} and frame==rep['selected_frame'] and digest(payload)==rep['payload_sha256'],name+' hashes')
            require(unpack_from('<I',payload,8)[0]==rep['count'] and payload[:16].hex()==rep['head'],name+' payload head')
            tables[arch,name]=payload
    return tables


def unpack(b, modern):
    require(b.startswith(HEAD), 'payload header')
    n=unpack_from('<I',b,8)[0]; items=[]; rows=[]
    p=13
    def cut(width):
        nonlocal p
        require(0<=width<=len(b)-p, f'bounded transfer @{p} w{width}')
        v=b[p:p+width]; p+=width; return v
    def integer(w,sgn=False):return int.from_bytes(cut(w),'little',signed=sgn)
    def count(w,sgn=False):
        v=integer(w,sgn)
        require(0<=v<=len(b)-p,f'bounded count @{p-w}: {v}')
        return v
    ids=set()
    for o in range(n):
        start=p; selector=integer(1); tax=None
        if modern:
            cut(4)
            cut(4*count(2,True));cut(4*count(4,True))
            for _ in range(count(2,True)):
                cut(1)
                for _ in range(4):cut(count(4))
                cut(20)
            cut(24)
            where=p;num=count(4,True); a=p
            for j in range(num):
                at=p; rec=cut(TAX.size); tag=TAX.unpack(rec)[0]; tail=cut(2) if tag>=2 else b''
                items.append(dict(row=o,item=j,absolute=at,length=p-at,tag=tag,hex=(rec+tail).hex()))
            tax=[where,num,a,p]
            cut(12*count(4));cut(14*count(4))
        cut(24)
        cut(5*count(1,True));cut(28*count(4,True));cut(28*count(4,True));cut(12*count(4,True))
        if modern:cut(43)
        at=p; ident=list(unpack_from('<III',cut(12)))
        require(ident[0]==o and ident[1]==ident[2]!=0 and ident[1] not in ids,f'identity {o} @{at} {ident}')
        ids.add(ident[1]); rows.append(dict(row=o,wire13=start,legacy14=start+1,end=p,length=p-start,identity_at=at,
            identity=ident,wire_sha256=digest(b[start:p]),legacy_sha256=digest(b[start+1:p+1]),tax=tax,selector=selector))
    require(b[p:]==TAIL, 'wrong footer or EOF')
    return rows,items,p


def static(d, f):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM
    import pefile
    pe=pefile.PE(str(EXE),fast_load=True); pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    raw=EXE.read_bytes(); require(digest(raw)==d['provenance']['editor_sha256'],'binary hash')
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    va=lambda o:base+pe.get_rva_from_offset(o)
    of=lambda a:pe.get_offset_from_rva(a-base)
    recorded={}; decoded={}
    for path in sorted(HERE.glob('instructions.part*.json')):
        for r in get(path):
            o=r['file_offset']; bs=bytes.fromhex(r['bytes']); a=va(o)
            require(o not in recorded and a==r['VA'] and raw[o:o+len(bs)]==bs,'instruction source bytes')
            i=next(md.disasm(bs,a,count=1)); require(i.size==len(bs) and (i.mnemonic+' '+i.op_str).rstrip()==r['instruction'],'instruction decode')
            if r.get('direct_target') is not None: require(of(i.operands[0].imm)==r['direct_target'],'direct edge')
            recorded[o]=r; decoded[o]=i
    for t in ('9','10'):
        r=d['factory'][t]; exe_slots={9:(0x1065eb0,0x105cb10),10:(0x1041f30,0x103fac0)}
        for label in ('factory_rel32','td','col','col_ptr','slot2','slot19'):
            x=r[label]; o=x['file_offset']; bs=bytes.fromhex(x['bytes']);require(va(o)==x['VA'] and raw[o:o+len(bs)]==bs,label)
        vt=of(r['vtable_VA']); s2,s19=exe_slots[int(t)]
        require(unpack_from('<Q',raw,vt+16)[0]==va(s2) and unpack_from('<Q',raw,vt+152)[0]==va(s19),'vtable slots')
        j=0xf49d38; dest=va(j)+unpack_from('<i',raw,j+4*int(t))[0]
        require(of(dest)==r['case']['file_offset'],'factory rel32')
        col=of(unpack_from('<Q',raw,vt-8)[0]); td=pe.get_offset_from_rva(unpack_from('<I',raw,col+12)[0]); text=raw[td+16:raw.index(0,td+16)].decode()
        require(text==r['rtti'],'RTTI chain')
    # Independent instruction worklist, not ReaderCFG and not accepting a jump into a linear slice.
    extent_index={x.struct.BeginAddress:x.struct.EndAddress for x in pe.DIRECTORY_ENTRY_EXCEPTION}
    cfg_sites={}
    for v in d['extents'].values():
        start=v['entry']; rva=va(start)-base; end=of(base+extent_index[rva]); seen=set();q=deque([start]); conditions=set()
        require(end==v['end_exclusive'],'PE extent')
        while q:
            o=q.popleft()
            if o in seen or not start<=o<end: continue
            i=next(md.disasm(raw[o:min(o+15,end)],va(o),count=1));seen.add(o)
            require(o in recorded,'reachable instruction missing')
            if i.mnemonic.startswith('j'):
                if i.operands[0].type==X86_OP_IMM:q.append(of(i.operands[0].imm))
                if i.mnemonic=='jmp':continue
                conditions.add(o)
            if i.mnemonic in ('ret','int3','ud2'):continue
            q.append(o+i.size)
        require(len(seen)==v['reachable'],'reachability count '+hex(start));cfg_sites[start]=conditions
    done={}
    for path in sorted(HERE.glob('branches.part*.json')):
        for r in get(path):
            o=r['site']; parent=r['function']; i=decoded[o]
            require(o in cfg_sites[parent] and o not in done and r['taken']==of(i.operands[0].imm) and r['fallthrough']==o+i.size,'branch edges')
            require(r['classification'] in {'wire_data','runtime-external','IO-result','context-lifecycle','dead'},'branch class')
            done[o]=r
    for v in d['extents'].values():
        if v['coverage'].startswith('complete'):require(cfg_sites[v['entry']]<=done.keys(),'branch census incomplete')
    for k,r in f.items():
        ci=decoded[r['compare']]; li=decoded[r['getter_load']]; tx=decoded[r['reader_site']]
        require(ci.operands[1].imm==int.from_bytes(k.encode(),'big') and li.operands[1].mem.disp==r['object_offset'] and tx.op_str.endswith('+ 0x28]'),'field static gate '+k)
    dispatch={k:int.from_bytes(k.encode(),'big') for k in EXPECTED if k not in ('EDfx','EDsc')}
    for k,r in d['parents'].items():
        require(r['owner_type']==EXPECTED[k] and r['t37_original_status']=='partial_parent_to_table_unknown','parent claim '+k)
        if k in dispatch:require(any(any(op.type==X86_OP_IMM and op.imm==dispatch[k] for op in decoded[o].operands) for o in r['sites']),'dispatch '+k)


def fields(items, ledger, schema):
    offsets=FIELD_POS
    for code,r in ledger.items():
        x=next(q for q in schema if q['field']==code);require(x==r['schema'],'scope '+code)
        values=[TAX.unpack_from(bytes.fromhex(i['hex']))[CODES.index(code)] for i in items]
        def live(v):return v>=0 if code in ('capa','leve') else v>0 if code=='fram' else True
        active=[v for v in values if live(v)]
        require(len(active)==r['live'] and len(values)-len(active)==r['sentinels'] and min(active)==r['live_min'] and max(active)==r['live_max'] and len(set(active))==r['distinct_live'],'domain '+code)
        require([[v,n] for v,n in Counter(values).most_common(10)]==r['top'],'value histogram '+code)
        if r['status']=='L3':
            require(code not in ('ppty','txty') and r['accepted_item_offset']==offsets[code] and all(math.isfinite(v) and float(x['min_value'])<=v<=float(x['max_value']) for v in active),'L3 '+code)
        else:require(code in ('ppty','txty') and r['accepted_item_offset'] is None and r['first_counterexample'] is not None,'held '+code)
        if code=='ppty':
            require(r['stored_hist']==hist(v or 1 for v in values),'ppty post-read zero coercion')
            j=values.index(0); witness=items[j]; x=r['first_counterexample']
            require(x['absolute']==witness['absolute']+15 and x['raw']=='00','ppty first zero')


def verify():
    d=get(HERE/'discovery_nation_unknown.json'); c=get(HERE/'cursor_nation_tax.json'); l=get(HERE/'fields_nation_tax.json'); f=l['fields']; p=d['provenance']
    manifest={x['path']:x['sha256'] for x in get(ROOT/'evidence/MANIFEST.json')['files']}
    for k,h in p['frozen_snapshots'].items():require(h==manifest[k]==digest((ROOT/k).read_bytes()),k)
    require(p['baseline_unchanged']==T37,'t37 hash commitments')
    for k,h in {**T37,**p['t24_sha256']}.items():require(h==digest((ROOT/k).read_bytes()),k)
    master=get(ROOT/'evidence/fm24/reports/editor_schema/master.json')['entities']['nation.xml'][0]['fields']; require(d['parents'].keys()==EXPECTED.keys(),'scope')
    for k,r in d['parents'].items():require(master[r['schema_index']]==r['schema'] and r['schema']['field']==k,'frozen scope '+k)
    tables=archives(d); all_rows={}
    for side,mode in [('client',False),('server',True)]:
        b=tables[side,'table_10.dat']; rows,items,p=unpack(b,mode); rep=c[side];all_rows[side]=rows
        require(len(rows)==251 and p==rep['footer_at'] and p+9==len(b) and digest(b)==rep['payload_sha256'],'EOF '+side)
        require(rep['tax_items']==items and rep['selector_hist']==hist(r['selector'] for r in rows) and rep['row_len_hist']==hist(r['length'] for r in rows),'walk '+side)
        require(rep['item_len_hist']==hist(x['length'] for x in items) and rep['item_tag_hist']==hist(x['tag'] for x in items),'item widths '+side)
        for got,want in zip(rows,rep['rows'],strict=True):require(all(want[k]==v for k,v in got.items() if k!='selector'),'row report '+side)
        if mode:
            require(len(items)==1899,'server tax count');fields(items,f,master[232]['list_item_fields'])
            a=items[0]['absolute']; example=c['controls']['tax_tag1_remove_two_bytes']
            _,synthetic,end=unpack(b[:a]+bytes([1])+b[a+1:a+23]+b[a+25:],True)
            require(len(synthetic)==1899 and synthetic[0]['length']==example['new_length']==23 and end==example['new_footer_at']==p-2,'23-byte branch control')
            for broken in (b[:a]+bytes([1])+b[a+1:],b[:a-4]+pack('<I',1)+b[a:a+4]):
                try: unpack(broken,True)
                except Failed: pass
                else: raise Failed('bad tax mutation accepted')
        else: require(not items,'no tax segment in client mode')
        try:unpack(b,not mode)
        except Failed:pass
        else:raise Failed('other mode unexpectedly closes '+side)
    require([r['identity'] for r in all_rows['client']]==[r['identity'] for r in all_rows['server']],'cross archive identity sequence')
    require(sum(r['status']=='L3' for r in f.values())==d['new_L3']==l['L3']==7 and d['L4']==l['L4']==0,'L3/L4 total')
    static(d,f)


def selftest():
    b=HEAD+pack('<I',0)+b'\0'+TAIL
    require(unpack(b,False)==([],[],13),'empty cursor')
    require(TAX.size==23 and TAX.unpack(bytes(23))[0]==0,'old tax length')
    try:unpack(b[:-1],True)
    except Failed:pass
    else:raise Failed('selftest trailing bytes')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');a=p.parse_args()
    try:
        if a.selftest:selftest();print('t47 verifier selftest PASS')
        else:verify();print('t47 independent verify PASS (15 parent inventory; 502 rows; 1899 tax items; 7 L3)')
        return 0
    except Failed as e:print('CHECK:',e,file=sys.stderr);return 1
    except Exception as e:print('FATAL:',type(e).__name__,e,file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
